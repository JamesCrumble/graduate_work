import logging
from uuid import UUID

import settings
from api.v1.flim_events.exceptions import NoUpdatedRowsError
from api.v1.tickets.db_proxy import TicketDBProxy
from api.v1.tickets.structure import TicketCreate, TicketInfoModel, TicketUpdate
from core.authorization import get_auth_user_from_access_token
from core.http_exceptions import NotFound
from core.logger import logger
from core.users import AuthenicatedUser
from fastapi import Depends, HTTPException, status


class TicketController:
    __slots__ = '_db_proxy', '_user_info',

    def __init__(
            self,
            db_proxy: TicketDBProxy = Depends(),
            user_info: AuthenicatedUser = Depends(get_auth_user_from_access_token),
    ) -> None:
        self._db_proxy = db_proxy
        self._user_info = user_info

    def __repr__(self) -> str:
        return self.__class__.__name__

    async def get_user_tickets(self, page_number: int, page_size: int) -> list[TicketInfoModel]:
        return [
            TicketInfoModel(**ticket) async for ticket in self._db_proxy.get_user_tickets(page_number, page_size)
        ]

    async def get_all_tickets(self, page_number: int, page_size: int) -> list[TicketInfoModel]:

        return [
            TicketInfoModel(**ticket)
            async for ticket in self._db_proxy.get_user_tickets(page_number, page_size, True)
        ]

    async def get_user_ticket(self, ticket_id: UUID) -> TicketInfoModel:
        ticket = await self._db_proxy.get_user_ticket_info(ticket_id)
        if ticket is None:
            raise NotFound()

        return ticket

    async def create_user_ticket(self, event: TicketCreate) -> UUID:
        try:
            created_ticket_id = await self._db_proxy.create_ticket(event)
        except ValueError as exc:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))

        return created_ticket_id

    async def update_user_ticket(self, event: TicketUpdate) -> None:
        try:
            await self._db_proxy.update_ticket(event)
        except NoUpdatedRowsError as exc:
            logger.error(exc, exc_info=settings.logging_level == logging.DEBUG)
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, f'Looks like ticket does not exists. No rows updated by "{event.ticket_id}" id'
            )
