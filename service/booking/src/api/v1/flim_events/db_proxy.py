import uuid
from collections.abc import AsyncIterator
from typing import Any
from uuid import UUID

import backoff
from core.authorization import get_auth_user_from_access_token
from core.users import AuthenicatedUser
from db.models import FilmEvent as FilmEventModel
from db.postgres import service_session
from fastapi import Depends
from sqlalchemy import Select, Update, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import NoUpdatedRowsError
from .structure import FilmEventCreate, FilmEvent

BATCH: int = 100


class FilmEventsDBProxy:

    __slots__ = '_session', '_user_info',

    def __init__(
        self,
        session: AsyncSession = Depends(service_session),
        user_info: AuthenicatedUser = Depends(get_auth_user_from_access_token)
    ) -> None:
        self._session = session
        self._user_info = user_info

    def _with_user_filter(self, stmt: Select | Update) -> Select | Update:
        if not self._user_info.is_super_user:
            return stmt.where(FilmEventModel.user_host_id == self._user_info.user_payload.user_id)
        return stmt

    @backoff.on_exception(backoff.expo, SQLAlchemyError, max_tries=15)
    async def get_user_events(self, page_number: int, page_size: int) -> AsyncIterator[FilmEventModel]:
        stmt = self._with_user_filter((
            select(FilmEventModel)
            .order_by(FilmEventModel.start_event_time.desc())
            .limit(page_size)
            .offset((page_number - 1) * page_size)
        ))

        result: CursorResult = await self._session.execute(stmt)
        while batch := result.scalars().fetchmany(BATCH):
            for film_event in batch:
                yield film_event

    @backoff.on_exception(backoff.expo, SQLAlchemyError, max_tries=15)
    async def get_user_event(self, id_: UUID) -> FilmEventModel | None:
        stmt = self._with_user_filter(select(FilmEventModel).where(FilmEventModel.id == id_))
        result: CursorResult = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    @backoff.on_exception(backoff.expo, SQLAlchemyError, max_tries=15)
    async def create_user_event(self, event: FilmEventCreate) -> UUID:
        film_event_id = uuid.uuid4()
        film_event = FilmEventModel(id=film_event_id, **event.dict())

        try:
            self._session.add(film_event)
            await self._session.commit()
        except SQLAlchemyError as exc:
            await self._session.rollback()
            raise exc

        return film_event_id

    @backoff.on_exception(backoff.expo, SQLAlchemyError, max_tries=15)
    async def update_user_event(self, id_: UUID, fields: dict[str, Any]) -> tuple[FilmEvent, FilmEvent]:
        select_stmt = self._with_user_filter(select(FilmEventModel).where(FilmEventModel.id == id_))
        updating_stmt = self._with_user_filter(
            update(FilmEventModel).where(FilmEventModel.id == id_).values(**fields)
        ).returning(FilmEventModel)

        try:
            async with self._session.begin():
                result: CursorResult = await self._session.execute(select_stmt)
                old_event_data = result.scalar_one_or_none()
                if old_event_data is None:
                    raise NoUpdatedRowsError(
                        f'Cannot update film event with "{id_}" for user with "{self._user_info.user_payload.user_id}" id.'
                    )
                old_event_data = FilmEvent(**old_event_data.dict())

                result: CursorResult = await self._session.execute(updating_stmt)
                new_event_data = FilmEvent(**result.scalar_one().dict())
        except (SQLAlchemyError, NoUpdatedRowsError) as exc:
            await self._session.rollback()
            raise exc

        return old_event_data, new_event_data
