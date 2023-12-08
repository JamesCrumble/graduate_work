from uuid import UUID

import sqlalchemy as sq
from core.logger import logger
from db.tables import OAuthUser, UserHistory, UserTable
from models import UserHistoryOperation
from sqlalchemy import Insert, Select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .http_exceptions import UserExists
from .schemas import UserDB, UserHistoryRecord
from .schemas.user import OAuthUserDB


class UserControl:

    __slots__ = '_session',

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _get_user(self, stmt: Select) -> UserDB:
        """Retrieves a single user from the database based on the provided statement."""
        try:
            result = await self._session.execute(stmt)
            user: UserTable = result.scalars().one()
        except NoResultFound as exc:
            raise UserDoesntExistsError(exc)
        except MultipleResultsFound as exc:
            raise UserMultipleResultsError(exc)

        return UserDB(id=user.id, email=user.email, password=user.password, is_super_user=user.is_super_user)

    async def _create_user(self, stmt: Insert):

        try:
            await self._session.execute(stmt)
            await self._session.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise UserExists

    async def delete_oauth_user(self, oauth_data: OAuthUserDB):

        stmt = sq.delete(
            OAuthUser
        ).where(
            sq.and_(OAuthUser.user_id == oauth_data.user_id, OAuthUser.oauth_type == oauth_data.oauth_type)
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_user_by_oauth(self, oauth_data: OAuthUserDB) -> UserDB | None:
        try:
            user_db = await self._get_user(
                sq.select(
                    UserTable
                ).join(
                    OAuthUser
                ).where(
                    sq.and_(OAuthUser.id == oauth_data.id, OAuthUser.oauth_type == oauth_data.oauth_type)
                )
            )
        except UserDoesntExistsError:
            return None
        return user_db

    async def get_user_by_email(self, email: str) -> UserDB:
        """Retrieves a single user from the database based on email."""
        return await self._get_user(sq.select(UserTable).where(UserTable.email == email))

    async def get_user_by_uid(self, uid: UUID) -> UserDB:
        """Retrieves a single user from the database based on uid."""
        return await self._get_user(sq.select(UserTable).where(UserTable.id == uid))

    async def update_user_login_history(self, user_id: UUID, operation: UserHistoryOperation, user_agent: str = '') -> None:
        user_history = UserHistory(user_id=user_id, operation=operation)
        if user_agent:
            user_history.user_agent = user_agent

        try:
            self._session.add(user_history)
            await self._session.commit()
        except BaseException as exc:
            logger.warning(exc)

    async def get_user_history(
        self,
        user_id: UUID,
        operations: list[UserHistoryOperation],
        offset: int,
        limit: int
    ) -> list[UserHistoryRecord]:
        stmt = (
            sq.select(UserHistory).where(
                UserHistory.user_id == user_id, UserHistory.operation.in_(operations)
            )
            .order_by(UserHistory.operation_datetime).offset(offset).limit(limit)
        )

        return [UserHistoryRecord(**record.dict()) for batch in (await self._session.execute(stmt)).all() for record in batch]

    async def get_user_roles(self, user_id: UUID):
        ...

    async def create_user(self, user_data: UserDB) -> UserDB:
        stmt = sq.insert(UserTable).values(**user_data.dict())
        await self._create_user(stmt)

        return user_data

    async def create_oauth_user(self, oauth_user: OAuthUserDB, user_data: UserDB = None) -> UserDB | None:
        try:
            if user_data:
                await self._session.execute(sq.insert(UserTable).values(**user_data.dict()))
            await self._session.execute(sq.insert(OAuthUser).values(**oauth_user.dict()))
            await self._session.commit()
        except SQLAlchemyError:
            return None

        return user_data

    async def change_user_password(self, user_id: UUID, new_user_password_hash: str) -> None:
        """Updates the password of a user in the database by uuid."""
        stmt = sq.update(UserTable).where(UserTable.id == user_id).values(password=new_user_password_hash)
        await self._session.execute(stmt)
        await self._session.commit()


class UserDoesntExistsError(BaseException):
    ...


class UserMultipleResultsError(BaseException):
    ...
