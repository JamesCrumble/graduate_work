import http
from http.client import HTTPException
from uuid import uuid4

import aio_pika
from aio_pika.abc import AbstractRobustChannel
from core.rabbit import get_rabbit_channel
from fastapi import Depends
from models import NotificationEvent
from settings import settings


def _create_message(data: bytes):
    return aio_pika.Message(
        body=data,
        content_type='application/json',
        content_encoding='utf-8',
        message_id=uuid4().hex,
        delivery_mode=aio_pika.abc.DeliveryMode.PERSISTENT,
        app_id=settings.api_name,
    )


async def send_notification_to_queue(data: NotificationEvent, channel: AbstractRobustChannel, queue_name: str):
    try:
        message = _create_message(data.json().encode())
        await channel.default_exchange.publish(
            message,
            routing_key=queue_name,
        )

    except Exception:
        raise HTTPException(http.HTTPStatus.INTERNAL_SERVER_ERROR)


async def add_notification_to_queue_by_email(data: NotificationEvent, email_channel=Depends(get_rabbit_channel)):
    await send_notification_to_queue(data, email_channel, settings.rabbit_queue_email_name)
    return {http.HTTPStatus.CREATED: 'Event created success'}


async def add_notification_to_queue_by_email_on_registration(user_id: str,
                                                             channel=Depends(get_rabbit_channel)):
    data = NotificationEvent(
        is_broadcast=False,
        template_id=settings.template_id_on_registration,
        user_ids=[user_id],
        context={}
    )

    await send_notification_to_queue(data, channel, settings.rabbit_queue_email_name)
    return {http.HTTPStatus.CREATED: 'Event created success'}


async def add_notification_to_queue_by_web_push(data: NotificationEvent, channel=Depends(get_rabbit_channel)):
    await send_notification_to_queue(data, channel, settings.rabbit_queue_web_push_name)
    return {http.HTTPStatus.CREATED: 'Event created success'}
