from datetime import timedelta
from uuid import UUID, uuid4

import core.jwt as jwt_core
from core.hasher import PBKDHasher
from core.jwt import JWTTokenPair, UserPayload, format_datetime
from core.logger import logger
from core.redis import get_redis
from core.utils import get_random_string, make_password
from db.postgres import service_session
from db.storage import RedisStorage
from db.tables import AccessToken as AccessTokenModel
from fastapi import Depends, Response, status
from models import UserHistoryOperation
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from .http_exceptions import ChangePasswordError, LoginError, UserExists
from .roles.user_role.user_role_service import UserRoleService
from .schemas import BaseUser, ChangePasswordModel, Tokens, UserDB, UserLogin
from .schemas.user import OAuthUserDB, SimpleUserAuth
from .user_control import UserControl, UserDoesntExistsError, UserMultipleResultsError


class AuthService:

    __slots__ = '_redis_storage', '_session', '_user_control', '_hasher',

    def __init__(self, session: AsyncSession, redis_storage: RedisStorage) -> None:
        self._redis_storage = redis_storage
        self._session = session
        self._user_control = UserControl(session)
        self._hasher = PBKDHasher()

    # TODO: move to something like psql service mb ?
    async def _insert_access_token(self, access_token: AccessTokenModel) -> None:
        self._session.add(access_token)
        await self._session.commit()
        await self._session.refresh(access_token)

    # TODO: move to something like redis service mb ?
    async def _save_user_token(
        self,
        user_id: str,
        access_token: str,
        ex: timedelta,
        user_agent: str
    ) -> None:
        user = await self._redis_storage.get_from_cache(user_id)
        user = user or {}
        user[user_agent] = access_token

        await self._redis_storage.save_to_cache(user_id, user, ex)

    async def _get_user_token_pair(self, user_payload: UserPayload) -> Tokens:
        jwt_tokens_pair = jwt_core.JWTTokenPair(user_payload)
        access_token, refresh_token = jwt_tokens_pair.access_token, jwt_tokens_pair.refresh_token

        await self._save_user_token(
            str(user_payload.user_id),
            refresh_token,
            jwt_core.REFRESH_EXPIRATION_TIME,
            user_payload.browser_fingerprint
        )

        await self._insert_access_token(AccessTokenModel(
            user_id=user_payload.user_id,
            user_token=access_token,
            is_active=True,
            user_agent=user_payload.browser_fingerprint,
        ))

        return jwt_tokens_pair

    async def _set_token_pair_cookie(self, response: Response, jwt_tokens_pair: JWTTokenPair):
        acc_ex = jwt_core.JWTTokenPair.access_expiration(jwt_tokens_pair.created)
        ref_ex = jwt_core.JWTTokenPair.refresh_expiration(jwt_tokens_pair.created)

        response.set_cookie(
            'access_token',
            jwt_tokens_pair.access_token,
            format_datetime(acc_ex, True),
            acc_ex,
            httponly=True
        )
        response.set_cookie(
            'refresh_token',
            jwt_tokens_pair.refresh_token,
            format_datetime(ref_ex, True),
            ref_ex,
            httponly=True
        )

    async def get_user_with_validation(self, email: EmailStr, password: str, validate_password: bool = True) -> UserDB:
        try:
            user_db = await self._user_control.get_user_by_email(email)
        except UserDoesntExistsError as exc:
            logger.error(exc)
            raise LoginError(status.HTTP_404_NOT_FOUND, 'User doesn\'t exists')
        except UserMultipleResultsError as exc:
            logger.error(exc)
            raise LoginError(status.HTTP_409_CONFLICT, 'Cannot found user properly')

        if validate_password and not self._hasher.check(password, user_db.password):
            raise LoginError(status.HTTP_401_UNAUTHORIZED, 'User current password invalid')

        return user_db

    async def _remove_token(self, response: Response, token: str, key: str):
        if token:
            access_token_payload = JWTTokenPair.get_jwt_token_payload(token)
            if access_token_payload:
                await JWTTokenPair.token_set_disable(self._redis_storage, token, access_token_payload)
            response.delete_cookie(key=key)

    async def _get_user_payload(self, user_db: UserDB, user_agent: str):

        user_payload = jwt_core.UserPayload(
            user_id=str(user_db.id),
            browser_fingerprint=user_agent
        )
        if user_db.is_super_user:
            user_payload.is_super_user = True
        return user_payload

    async def sign(self, user_data: BaseUser, user_agent: str):

        try:
            await self._user_control.get_user_by_email(user_data.email)
            raise UserExists(status.HTTP_409_CONFLICT, 'User allready exists')
        except UserDoesntExistsError:
            pass

        new_id = uuid4()
        pass_hash = self._hasher.encode(user_data.password)

        user_db = UserDB(id=new_id, email=user_data.email, password=pass_hash)
        user_db = await self._user_control.create_user(user_db)

        await self._user_control.update_user_login_history(user_db.id, UserHistoryOperation.SIGN, user_agent)

        return user_db

    async def login(
        self,
        user_login: UserLogin,
        response: Response,
        user_agent: str,
        user_role_service: UserRoleService
    ) -> Tokens:

        user_db = await self.get_user_with_validation(user_login.email, user_login.password)

        user_payload = await self._get_user_payload(user_db, user_agent)

        user_payload.groups = await user_role_service.get_user_roles(user_payload.user_id)

        jwt_tokens_pair = await self._get_user_token_pair(user_payload)

        if user_login.set_cookie:
            await self._set_token_pair_cookie(response, jwt_tokens_pair)

        await self._user_control.update_user_login_history(user_payload.user_id, UserHistoryOperation.LOGIN, user_agent)

        return Tokens(access_token=jwt_tokens_pair.access_token, refresh_token=jwt_tokens_pair.refresh_token)

    async def oauth_login(
        self,
        user_login: UserLogin,
        oauth_user_db: OAuthUserDB,
        response: Response,
        user_agent: str,
        user_role_service: UserRoleService
    ) -> Tokens:

        try:
            user_db = await self._user_control.get_user_by_oauth(oauth_data=oauth_user_db)
        except UserDoesntExistsError:
            user_db = None

        if user_db is None:
            try:
                await self._user_control.get_user_by_email(user_login.email)
                raise UserExists(status.HTTP_409_CONFLICT, 'User with that email allready exists')
            except UserDoesntExistsError:
                new_id = uuid4()
                if not user_login.email:
                    user_login.email = f'!{get_random_string(20)}@fake.com'
                user_db = UserDB(id=new_id, email=user_login.email, password=make_password())
                oauth_user_db.user_id = new_id
                user_db = await self._user_control.create_oauth_user(oauth_user_db, user_db)

        user_payload = await self._get_user_payload(user_db, user_agent)

        user_payload.groups = await user_role_service.get_user_roles(user_payload.user_id)

        jwt_tokens_pair = await self._get_user_token_pair(user_payload)

        if user_login.set_cookie:
            await self._set_token_pair_cookie(response, jwt_tokens_pair)

        await self._user_control.update_user_login_history(user_payload.user_id, UserHistoryOperation.LOGIN, user_agent)

        return Tokens(access_token=jwt_tokens_pair.access_token, refresh_token=jwt_tokens_pair.refresh_token)

    async def oauth_link(
        self,
        oauth_user_db: OAuthUserDB,
    ) -> Tokens:

        try:
            await self._user_control.get_user_by_oauth(oauth_data=oauth_user_db)
        except UserDoesntExistsError:
            raise UserExists(status.HTTP_409_CONFLICT, 'User with that email allready link account')

        await self._user_control.create_oauth_user(oauth_user_db)

    async def oauth_untie(
        self,
        oauth_user_db: OAuthUserDB,
    ) -> Tokens:

        await self._user_control.delete_oauth_user(oauth_data=oauth_user_db)

    async def logout(self, response: Response, user_tokens: jwt_core.JWTTokenPairRaw):

        await self._remove_token(response, user_tokens.access_token, 'access_token')
        await self._remove_token(response, user_tokens.refresh_token, 'refresh_token')

        access_token_payload_dict: dict = JWTTokenPair.verify_jwt_token(user_tokens.access_token)

        user_payload = UserPayload(**access_token_payload_dict)

        await self._user_control.update_user_login_history(
            user_payload.user_id,
            UserHistoryOperation.LOGOUT,
            user_payload.browser_fingerprint
        )

    async def change_user_password(
        self,
        change_pass_model: ChangePasswordModel,
        user_auth: SimpleUserAuth,
        user_agent: str
    ) -> None:
        if user_auth.is_super_user:
            user_db = await self.get_user_with_validation(
                change_pass_model.email,
                password=change_pass_model.new_password,
                validate_password=False
            )
            if self._hasher.check(change_pass_model.new_password, user_db.password):
                raise ChangePasswordError(status.HTTP_400_BAD_REQUEST, 'New password and current password are the same')

            await self._user_control.change_user_password(user_db.id, self._hasher.encode(change_pass_model.new_password))
            await self._user_control.update_user_login_history(user_db.id, UserHistoryOperation.CHANGE_PASSWORD, user_agent)
            return

        user_payload: UserPayload = user_auth.user_payload
        user_id = UUID(user_payload.user_id)

        await self._user_control.change_user_password(user_id, self._hasher.encode(change_pass_model.new_password))
        await self._user_control.update_user_login_history(user_id, UserHistoryOperation.CHANGE_PASSWORD, user_agent)

    async def refresh(
        self,
        response: Response,
        user_tokens: jwt_core.JWTTokenPairRaw,
    ):
        refresh_token_payload_dict: dict = JWTTokenPair.verify_jwt_token(user_tokens.refresh_token)

        user_payload = UserPayload(**refresh_token_payload_dict)

        await self.logout(response, user_tokens)

        jwt_tokens_pair = await self._get_user_token_pair(user_payload)

        await self._set_token_pair_cookie(response, jwt_tokens_pair)

        return Tokens(access_token=jwt_tokens_pair.access_token, refresh_token=jwt_tokens_pair.refresh_token)


def auth_service(
    session: AsyncSession = Depends(service_session),
    redis_storage: RedisStorage = Depends(get_redis),
) -> AuthService:
    return AuthService(session=session, redis_storage=redis_storage)
