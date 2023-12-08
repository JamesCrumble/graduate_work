import logging
from uuid import UUID

from core.authorization import get_auth_user_from_access_token
from core.http_exceptions import NotFound
from core.logger import logger
from core.users import AuthenicatedUser
from core.notifications import Notifications
from db.models import FilmEventState
from fastapi import Depends, HTTPException, status
from settings import settings

from .db_proxy import FilmEventsDBProxy
from .exceptions import NoUpdatedRowsError
from .structure import FilmEvent, FilmEventCreate, FilmEventEdit


class FilmEventsController:

    __slots__ = '_db_proxy', '_user_info',

    def __init__(
        self,
        db_proxy: FilmEventsDBProxy = Depends(),
        user_info: AuthenicatedUser = Depends(get_auth_user_from_access_token),
    ) -> None:
        self._db_proxy = db_proxy
        self._user_info = user_info

    async def get_user_film_events(self, page_number: int, page_size: int) -> list[FilmEvent]:
        return [
            FilmEvent(**film_event.dict()) async for film_event in self._db_proxy.get_user_events(page_number, page_size)
        ]

    async def get_user_film_event(self, event_id: UUID) -> FilmEvent:
        film_event = await self._db_proxy.get_user_event(event_id)
        if film_event is None:
            raise NotFound()

        return FilmEvent(**film_event.dict())

    async def create_user_film_event(self, event: FilmEventCreate) -> UUID:
        user_host_id = UUID(self._user_info.user_payload.user_id)
        if self._user_info.is_super_user:
            if event.user_host_id is None:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY, 'Cannot create film event without user_host_id when is super user'
                )
            user_host_id = event.user_host_id

        event.user_host_id = user_host_id
        created_event_id = await self._db_proxy.create_user_event(event)

        return created_event_id

    async def update_user_film_event(
        self,
        event_id: UUID,
        event_edit: FilmEventEdit,
        notify_about_updates: bool
    ) -> None:
        try:
            old_event_data, new_event_data = await self._db_proxy.update_user_event(event_id, event_edit.dict())
        except NoUpdatedRowsError as exc:
            logger.error(exc, exc_info=settings.logging_level == logging.DEBUG)
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, f'Looks like film event does not exists. No rows updated by "{event_id}" id'
            )

        if not notify_about_updates or new_event_data.state is not FilmEventState.PENDING:
            return

        context = dict()
        if old_event_data.price_rub != new_event_data.price_rub:
            context['price_rub'] = 'Цена билета была изменена с %d на %d' % (
                old_event_data.price_rub, new_event_data.price_rub,
            )
        if old_event_data.event_location != new_event_data.event_location:
            context['event_location'] = 'Место мероприятия было изменено на %s' % (
                new_event_data.event_location
            )

        if not context:
            return

        notifications = Notifications()
        await notifications.notify_about_film_event_updates(context, new_event_data.id)
