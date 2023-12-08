import uuid
from collections.abc import AsyncIterator
from uuid import UUID

import backoff
from api.v1.flim_events.exceptions import NoUpdatedRowsError
from api.v1.tickets.structure import TicketCreate, TicketInfoModel, TicketUpdate
from core import logger
from core.authorization import get_auth_user_from_access_token
from core.http_exceptions import ForbiddenRequest, NotFound
from core.users import AuthenicatedUser
from db.models import FilmEvent as FilmEventModel
from db.models import Ticket as TicketModel
from db.postgres import service_session
from fastapi import Depends
from sqlalchemy import CursorResult, Select, Update, func, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

BATCH: int = 100


class TicketDBProxy:

    __slots__ = '_session', '_user_info',

    def __init__(
            self,
            session: AsyncSession = Depends(service_session),
            user_info: AuthenicatedUser = Depends(get_auth_user_from_access_token)
    ) -> None:
        self._session = session
        self._user_info = user_info

    def _with_user_filter(self, stmt: Select | Update) -> Select | Update:
        return stmt.where(TicketModel.user_guest_id == self._user_info.user_payload.user_id)

    @backoff.on_exception(backoff.expo, SQLAlchemyError)
    async def get_user_tickets(self, page_number: int, page_size: int,
                               all_tickets: bool = False) -> AsyncIterator[TicketInfoModel]:
        try:
            stmt = (Select(TicketModel.id, TicketModel.film_event_id, TicketModel.state, TicketModel.created,
                           TicketModel.modified,  FilmEventModel.title, FilmEventModel.description,
                           FilmEventModel.duration_in_seconds, FilmEventModel.movie_id, FilmEventModel.start_event_time,
                           FilmEventModel.event_location,  FilmEventModel.price_rub,
                           FilmEventModel.state.label('film_event_state'))
                    .select_from(FilmEventModel)
                    .join(TicketModel, TicketModel.film_event_id == FilmEventModel.id)
                    .where(TicketModel.user_guest_id == self._user_info.user_payload.user_id)
                    .order_by(TicketModel.created.desc())
                    .limit(page_size)
                    .offset((page_number - 1) * page_size)
                    )
            if all_tickets:
                stmt = (Select(TicketModel.id, TicketModel.film_event_id, TicketModel.state, TicketModel.created,
                               TicketModel.modified,  FilmEventModel.title, FilmEventModel.description,
                               FilmEventModel.duration_in_seconds, FilmEventModel.movie_id, FilmEventModel.start_event_time,
                               FilmEventModel.event_location, FilmEventModel.price_rub,
                               FilmEventModel.state.label('film_event_state'))
                        .select_from(FilmEventModel)
                        .join(TicketModel, TicketModel.film_event_id == FilmEventModel.id)
                        .order_by(TicketModel.created.desc())
                        .limit(page_size)
                        .offset((page_number - 1) * page_size)
                        )

            result: CursorResult = await self._session.execute(stmt)
        except Exception as e:
            raise e

        while batch := result.mappings().fetchmany(BATCH):
            for ticket in batch:
                yield ticket

    @backoff.on_exception(backoff.expo, SQLAlchemyError)
    async def get_user_ticket_info(self, id_: UUID) -> TicketInfoModel | None:
        ticket_info = None
        try:
            stmt = (Select(TicketModel.id, TicketModel.film_event_id, TicketModel.state, TicketModel.created,
                           TicketModel.modified,  FilmEventModel.title, FilmEventModel.description,
                           FilmEventModel.duration_in_seconds, FilmEventModel.movie_id, FilmEventModel.start_event_time,
                           FilmEventModel.event_location, FilmEventModel.duration_in_seconds, FilmEventModel.price_rub,
                           FilmEventModel.state.label('film_event_state'))
                    .select_from(FilmEventModel)
                    .join(TicketModel, TicketModel.film_event_id == FilmEventModel.id)
                    .where(TicketModel.id == id_ and TicketModel.user_guest_id == self._user_info.user_payload.user_id))

            result = await self._session.execute(stmt)
            results_as_dict = result.mappings().all()
            if len(results_as_dict) > 0:
                ticket_info = TicketInfoModel(**results_as_dict[0])

        except Exception as e:
            logger.logger.error('Error execution sql ', e)

        return ticket_info

    @backoff.on_exception(backoff.expo, SQLAlchemyError)
    async def create_ticket(self, event: TicketCreate) -> UUID:
        user_guest_id = UUID(self._user_info.user_payload.user_id)

        try:
            film_event = await self._session.get(FilmEventModel, event.film_event_id)

            if film_event.user_host_id == user_guest_id:
                raise ForbiddenRequest

            stmt = (Select(func.count(TicketModel.id))
                    .select_from(TicketModel)
                    .where(TicketModel.film_event_id == film_event.id))

            result = (await self._session.execute(stmt)).scalar()
            if film_event.seats_number < result:
                raise NotFound
            stmt = (Select(TicketModel).where(TicketModel.film_event_id == event.film_event_id and
                                              TicketModel.user_guest_id == user_guest_id))

            ticket = (await self._session.execute(stmt)).scalar()
            if ticket:
                return ticket.dict()['id']

        except Exception as exc:
            raise exc

        ticket_id = uuid.uuid4()

        ticket = TicketModel(id=ticket_id, **event.dict())
        ticket.user_guest_id = user_guest_id

        try:
            self._session.add(ticket)
            await self._session.commit()
        except SQLAlchemyError as exc:
            await self._session.rollback()
            raise exc

        return ticket_id

    @backoff.on_exception(backoff.expo, SQLAlchemyError)
    async def update_ticket(self,  event: TicketUpdate) -> None:
        stmt = self._with_user_filter(update(TicketModel).where(TicketModel.id == event.ticket_id).values(state=event.state))

        try:
            result: CursorResult = await self._session.execute(stmt)
            if result.rowcount <= 0:
                raise NoUpdatedRowsError(
                    f'Cannot update ticket state with "{event.ticket_id}" for user with'
                    f' "{self._user_info.user_payload.user_id}" id'
                )

            await self._session.commit()
        except (SQLAlchemyError, NoUpdatedRowsError) as exc:
            await self._session.rollback()
            raise exc
