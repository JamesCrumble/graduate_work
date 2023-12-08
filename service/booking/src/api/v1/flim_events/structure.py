from datetime import datetime
from uuid import UUID

from db.models import FilmEventState
from pydantic import BaseModel, validator


class FilmEvent(BaseModel):
    id: UUID
    title: str
    description: str
    movie_id: UUID
    is_private: bool
    start_event_time: datetime
    event_location: str
    duration_in_seconds: int
    seats_number: int
    price_rub: int
    state: FilmEventState

    @validator('is_private', pre=True)
    def _validate_private_field(cls, value: bool | None) -> bool:
        '''is_private field can be nullable from db'''
        return bool(value)


class FilmEventCreate(BaseModel):
    title: str
    description: str
    movie_id: UUID
    is_private: bool
    user_host_id: UUID | None = None
    start_event_time: datetime
    event_location: str
    duration_in_seconds: int
    seats_number: int
    price_rub: int


class FilmEventEdit(BaseModel):
    title: str
    description: str
    is_private: bool
    start_event_time: datetime
    event_location: str
    seats_number: int
    price_rub: int
    state: FilmEventState
