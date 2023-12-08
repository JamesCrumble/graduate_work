from datetime import datetime
from uuid import UUID

from db.models import FilmEventState, TicketState
from pydantic import BaseModel


class TicketModel(BaseModel):
    id: UUID | None = None
    film_event_id: UUID | None = None
    state: TicketState


class TicketCreate(BaseModel):
    film_event_id: UUID | None = None
    state: TicketState


class TicketUpdate(BaseModel):
    ticket_id: UUID | None = None
    state: TicketState


class TicketInfoModel(BaseModel):
    id: UUID
    film_event_id: UUID
    state: TicketState
    created: datetime
    modified: datetime | None = None
    title: str
    description: str
    movie_id: UUID
    start_event_time: datetime
    event_location: str
    duration_in_seconds: int
    price_rub: int
    film_event_state: FilmEventState
