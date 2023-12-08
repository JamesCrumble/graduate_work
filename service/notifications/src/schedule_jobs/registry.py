from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .jobs import initiated_notifications_job, unfinished_notifications_job


async def jobs_registry(scheduler: AsyncIOScheduler) -> None:
    scheduler.add_job(
        unfinished_notifications_job,
        trigger='interval',
        minutes=30
    )

    scheduler.add_job(
        initiated_notifications_job,
        trigger='interval',
        minutes=20
    )
