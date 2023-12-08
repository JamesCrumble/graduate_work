import httpx
import backoff
import asyncio

from uuid import UUID
from typing import Any
from http import HTTPStatus

from settings import settings
from core.logger import logger

from .helpers import get_film_event_users


class Notifications:

    __slots__ = (
        '_client',
    )
    __notification_url__ = 'http://%s:%s/notifications/api/email' % (
        settings.notification_service_host, settings.notification_service_port,
    )

    def __init__(self):
        self._client = httpx.AsyncClient()

    @backoff.on_exception(backoff.expo, httpx.HTTPError, max_tries=10)
    async def notify(
        self,
        users_ids: set[UUID],
        template_id: int,
        context: dict[str, Any]
    ) -> None:
        if not settings.notification_service_host:
            return

        data = {
            'is_broadcast': False,
            'template_id': template_id,
            'user_ids': [str(user_id) for user_id in users_ids],
            'context': context
        }

        async with self._client as client:
            response = await client.post(
                self.__notification_url__,
                data=data,
                headers={
                    'access_token': settings.notification_user_token,
                }
            )
            if response.status_code != HTTPStatus.OK:
                logger.error(
                    f'Wrong "{response.status_code}" status code for creation notification event.\n'
                    f'Content: {data=}\nDetail: {response.text=}'
                )

    async def notify_about_film_event_updates(self, context: dict[str, Any], event_id: UUID) -> None:
        # no exc raise to the global context inside task scope
        asyncio.create_task(self.notify(await get_film_event_users(event_id, include_host_user=True), 5, context))
