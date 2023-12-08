import uuid
import asyncio

import orjson
import backoff
import aio_pika

from message_worker.send_emails import Email
from sqlalchemy.exc import SQLAlchemyError
from aio_pika.abc import AbstractRobustChannel
from sqlalchemy.ext.asyncio import AsyncSession
from aio_pika.exceptions import AMQPConnectionError
from core.psql import async_service_session_maker
from core.logger import consume_worker_logger
from pydantic import ValidationError
from models import (
    NotificationEvent,
    NotificationStatus,
    NotificationTask,
    NotificationTaskChannel,
    NotifiedStatus,
)
from settings import settings


@backoff.on_exception(backoff.expo, SQLAlchemyError, max_tries=5)
async def insert_notification_event(
    session: AsyncSession,
    event: NotificationEvent,
    channel: NotificationTaskChannel,
    status: NotifiedStatus
) -> uuid.UUID:
    task_id = uuid.uuid4()
    async with session.begin():
        task = NotificationTask(
            id=task_id,
            template_id=event.template_id,
            body=event.context,
            is_broadcast=event.is_broadcast,
            channel=channel.value
        )
        session.add(task)

        user_ids = event.user_ids
        if user_ids is None:
            # Take all users ids from auth db (not from api) and add into notification status marked with created task id
            user_ids: list[str] = list()

        for user_id in user_ids:
            session.add(NotificationStatus(
                id=uuid.uuid4(),
                user_id=user_id,
                notification_task_id=task.id,
                status=status.value
            ))

    return task_id


async def consume_worker(rabbit_channel: AbstractRobustChannel, queue_name: str, channel: NotificationTaskChannel):
    email_worker = Email()
    queue = await rabbit_channel.declare_queue(queue_name, durable=True)

    async with async_service_session_maker() as session:
        async for message in queue.iterator():
            async with message.process():
                try:
                    notification_event = NotificationEvent(**orjson.loads(message.body))
                except (orjson.JSONDecodeError, ValidationError) as exc:
                    consume_worker_logger.error(f'Cannot deserialize message with exc => {exc}.\nContent: {message.body}')
                    continue

                try:
                    task_id = await insert_notification_event(session, notification_event, channel, NotifiedStatus.INITIATED)
                except SQLAlchemyError as exc:
                    consume_worker_logger.error(
                        f'Cannot insert notification event with exc => {exc}.\nEvent body => {notification_event.dict()}'
                    )
                    continue

                # Take all users ids from auth db (not from api) and add into notification status marked with created task id
                for user_id in (notification_event.user_ids or list()):
                    asyncio.create_task(email_worker.send(user_id, str(task_id)))


if __name__ == '__main__':
    async def main():
        @backoff.on_exception(backoff.expo,  AMQPConnectionError)
        async def _connect():
            return await aio_pika.connect_robust(
                f'amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASS}@' +
                f'{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/'
            )

        async with await _connect() as rabbit_connection:
            rabbit_channel = await rabbit_connection.channel()
            consume_worker_task = consume_worker(rabbit_channel, settings.rabbit_queue_email_name, NotificationTaskChannel.EMAIL)

            await asyncio.gather(consume_worker_task,)

    asyncio.run(main())
