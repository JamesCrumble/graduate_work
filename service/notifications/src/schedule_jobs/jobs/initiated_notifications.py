from datetime import datetime, timedelta

from core.logger import logger
from core.psql import async_service_session_maker
from message_worker import Email
from models import (
    NotificationStatus,
    NotificationTask,
    NotificationTaskChannel,
    NotificationTaskState,
    NotifiedStatus,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import coalesce

CHUNK_SIZE: int = 1 * 1024
DELAY_GAP: int = 10  # minutes


async def job() -> None:
    email_worker = Email()
    current_datetime = datetime.utcnow()
    query = (
        select(
            NotificationStatus.user_id,
            NotificationTask.id,
            NotificationTask.channel,
        )
        .join(
            NotificationTask,
            NotificationTask.id == NotificationStatus.notification_task_id,
        )
        .where(
            NotificationStatus.status == NotifiedStatus.INITIATED.value,
            NotificationTask.state == NotificationTaskState.IN_QUEUE.value,
            coalesce(NotificationStatus.updated_at, NotificationStatus.created_at).between(
                current_datetime - timedelta(days=1), current_datetime - timedelta(minutes=DELAY_GAP)
            )
        )
    ).execution_options(yield_per=CHUNK_SIZE)

    async with async_service_session_maker() as session:
        session: AsyncSession
        result = await session.stream(query)

        while batch := await result.fetchmany(CHUNK_SIZE):
            for user_id, task_id, channel in batch:
                if channel is NotificationTaskChannel.EMAIL.value:
                    await email_worker.send(user_id, task_id)
                else:
                    logger.debug(f'Channel with "{channel}" value is not implemented')
                    continue

    logger.debug('Job "initiated notifications" executed correctly')
