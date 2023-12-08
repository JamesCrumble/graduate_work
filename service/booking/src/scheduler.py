import asyncio

from sqlalchemy import select, func
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.notifications import Notifications
from db.postgres import service_session_maker
from core.helpers import get_film_event_users
from db.models import FilmEvent, FilmEventState

BATCH: int = 100


async def notify_about_one_hour_before_start_event() -> None:
    notifications = Notifications()
    notification_state = 'notified_about_one_hour_before_start'

    async with service_session_maker() as session, session.begin():
        stmt = select(FilmEvent).where(
            func.coalesce(FilmEvent.notification_state, '') != notification_state,
            FilmEvent.state == FilmEventState.PENDING,
            FilmEvent.start_event_time.between(
                FilmEvent.start_event_time - timedelta(hours=1), datetime.now(tz=timezone(timedelta(hours=3), name='Moscow'))
            ),
        )
        result = await session.execute(stmt)

        while batch := result.scalars().fetchmany(BATCH):
            for film_event in batch:
                film_event_users = await get_film_event_users(film_event.id, include_host_user=True)
                await notifications.notify(
                    film_event_users, 6,
                    {
                        'message': (
                            'Здравствуйте. '
                            f'До начала проведения "{film_event.title}" мероприятия остался всего час, поспешите <3. '
                            f'Место проведения по адресу {film_event.event_location}'
                        ),
                    }
                )
                film_event.notification_state = notification_state


async def notify_about_one_day_before_start_event() -> None:
    notifications = Notifications()
    notification_state = 'notified_about_one_day_before_start'

    async with service_session_maker() as session, session.begin():
        stmt = select(FilmEvent).where(
            func.coalesce(FilmEvent.notification_state, '') != notification_state,
            FilmEvent.state == FilmEventState.PENDING,
            FilmEvent.start_event_time.between(
                FilmEvent.start_event_time - timedelta(days=1), datetime.now(tz=timezone(timedelta(hours=3), name='Moscow'))
            ),
        )
        result = await session.execute(stmt)

        while batch := result.scalars().fetchmany(BATCH):
            for film_event in batch:
                film_event_users = await get_film_event_users(film_event.id, include_host_user=True)
                await notifications.notify(
                    film_event_users, 7,
                    {
                        'message': (
                            'Здравствуйте. '
                            f'До начала проведения "{film_event.title}" мероприятия остался 1 день. '
                            f'Место проведения по адресу {film_event.event_location}'
                        ),
                    }
                )
                film_event.notification_state = notification_state


async def main() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(notify_about_one_hour_before_start_event, trigger='interval', minutes=20)
    scheduler.add_job(notify_about_one_day_before_start_event, trigger='interval', minutes=60)
    scheduler.start()

if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.create_task(main())
    event_loop.run_forever()
