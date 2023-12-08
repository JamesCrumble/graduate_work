from uuid import UUID

from sqlalchemy import select

from db.models import FilmEvent, Ticket
from db.postgres import service_session_maker


async def get_film_event_users(event_id: UUID, include_host_user: bool) -> set[UUID]:
    users_ids: set[UUID] = set()

    async with service_session_maker() as session:
        if include_host_user:
            stmt = select(FilmEvent.user_host_id).where(FilmEvent.id == event_id)
            result = await session.execute(stmt)
            user_host_id = result.scalar_one_or_none()
            if user_host_id is None:
                return users_ids

            users_ids.add(user_host_id)

        stmt = select(Ticket.user_guest_id).where(Ticket.film_event_id == event_id)
        result = await session.execute(stmt)
        users_ids.update(result.scalars().all())

    return users_ids
