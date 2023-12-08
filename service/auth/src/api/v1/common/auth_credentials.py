from core.jwt import JWTToken, JWTTokenPairRaw
from core.logger import logger
from core.redis import get_redis
from db.storage import RedisStorage
from fastapi import Depends
from fastapi.security.api_key import APIKeyCookie

from ..http_exceptions import ForbiddenRequest
from ..schemas.user import (
    BaseUserAuth,
    SimpleUserAuth,
    SuperUserAuth,
    UnauthenticatedUser,
)

api_key_access = APIKeyCookie(name='access_token', auto_error=False)
api_key_refresh = APIKeyCookie(name='refresh_token', auto_error=False)


async def get_user_from_access_token(
    access_token: str = Depends(api_key_access),
    redis_storage: RedisStorage = Depends(get_redis),
) -> BaseUserAuth:
    logger.debug(f'access_token is: {access_token}')
    return await get_user_from_token(redis_storage, access_token)


async def get_user_from_refresh_token(
    refresh_token: str = Depends(api_key_refresh),
    redis_storage: RedisStorage = Depends(get_redis),
) -> BaseUserAuth:
    return await get_user_from_token(redis_storage, refresh_token)


async def get_user_tokens(access_token: str = Depends(api_key_access), refresh_token: str = Depends(api_key_refresh)):

    return JWTTokenPairRaw(access_token=access_token, refresh_token=refresh_token)


async def get_user_from_token(
    redis_storage: RedisStorage,
    token,
) -> BaseUserAuth:

    if token is None:
        return UnauthenticatedUser()

    token_disabled = await JWTToken.token_disabled(redis_storage, token)
    if token_disabled:
        return UnauthenticatedUser()

    token_payload = JWTToken.get_jwt_token_payload(token)
    if token_payload is None:
        return UnauthenticatedUser()

    if token_payload.is_super_user:
        return SuperUserAuth(user_payload=token_payload)

    return SimpleUserAuth(user_payload=token_payload)


async def get_superuser_from_access_token(
    auth_user: BaseUserAuth = Depends(get_user_from_access_token),
) -> BaseUserAuth:
    if not auth_user.is_super_user:
        raise ForbiddenRequest

    return auth_user
