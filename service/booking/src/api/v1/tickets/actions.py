from typing import Annotated
from uuid import UUID

from fastapi import Depends, Query

from .controller import TicketController
from .structure import TicketCreate, TicketInfoModel, TicketUpdate


async def get_user_tickets(
        controller: TicketController = Depends(),
        page_number: Annotated[int, Query(gt=0, description='page number')] = 1,
        page_size: Annotated[int, Query(le=50, ge=10, description='number of objects on page')] = 10
) -> list[TicketInfoModel]:
    return await controller.get_user_tickets(page_number, page_size)


async def get_ticket_list_all(
        controller: TicketController = Depends(),
        page_number: Annotated[int, Query(gt=0, description='page number')] = 1,
        page_size: Annotated[int, Query(le=50, ge=10, description='number of objects on page')] = 10
) -> list[TicketInfoModel]:
    return await controller.get_all_tickets(page_number, page_size)


async def get_user_ticket_info(ticket_id: UUID, controller: TicketController = Depends()) -> TicketInfoModel:
    return await controller.get_user_ticket(ticket_id)


async def create_user_ticket(event_create: TicketCreate, controller: TicketController = Depends()) -> UUID:
    return await controller.create_user_ticket(event_create)


async def update_user_ticket(event: TicketUpdate, controller: TicketController = Depends()) -> None:
    await controller.update_user_ticket(event)
