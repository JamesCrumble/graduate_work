from datetime import datetime, timedelta

from core.logger import logger
from core.psql import async_service_session_maker
from models import (
    NotificationStatus,
    NotificationTask,
    NotificationTaskState,
    NotifiedStatus,
)
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import coalesce

CHUNK_SIZE: int = 1 * 1024
DELAY_GAP: int = 20  # minutes


async def job() -> None:
    current_datetime = datetime.utcnow()
    query = (
        select(
            NotificationTask.id,
            NotificationStatus.user_id,
        )
        .join(
            NotificationTask,
            NotificationTask.id == NotificationStatus.notification_task_id
        )
        .where(
            NotificationStatus.status == NotifiedStatus.FAILED.value,
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
            for task_id, user_id in batch:
                try:
                    await session.execute((
                        update(NotificationStatus).
                        where(NotificationStatus.user_id == user_id, NotificationStatus.notification_task_id == task_id).
                        values(status=NotifiedStatus.INITIATED.value)
                    ))
                    await session.commit()
                except BaseException as exc:
                    logger.debug(f'Cannot initiate message of "{user_id}" user id by "{task_id}" task id => {exc}')

    logger.debug('Job "unfinished notifications" executed correctly')
