from typing import Annotated
from uuid import UUID

from fastapi import Depends, Query

from ..controller import FilmEventsController
from ..structure import FilmEvent, FilmEventCreate, FilmEventEdit


async def get_user_film_events(
    controller: FilmEventsController = Depends(),
    page_number: Annotated[int, Query(gt=0, description='page number')] = 1,
    page_size: Annotated[int, Query(le=50, ge=10, description='number of objects on page')] = 10
) -> list[FilmEvent]:
    return await controller.get_user_film_events(page_number, page_size)


async def get_user_film_event(event_id: UUID, controller: FilmEventsController = Depends()) -> FilmEvent:
    return await controller.get_user_film_event(event_id)


async def create_user_film_event(event_create: FilmEventCreate, controller: FilmEventsController = Depends()) -> UUID:
    return await controller.create_user_film_event(event_create)


async def update_user_film_event(
    event_id: UUID,
    event_edit: FilmEventEdit,
    notify_about_updates: bool = True,
    controller: FilmEventsController = Depends()
) -> None:
    await controller.update_user_film_event(event_id, event_edit, notify_about_updates)
