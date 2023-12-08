import enum

from sqlalchemy import (
    TIMESTAMP,
    UUID,
    Boolean,
    Column,
    Enum,
    Integer,
    SmallInteger,
    String,
    Text,
)

from .base import Base
from .mixins import TrackableMixin, UUIDPkMixin


class FilmEventState(enum.Enum):
    PENDING: str = 'PENDING'
    FINISHED: str = 'FINISHED'
    CANCELED: str = 'CANCELED'


class FilmEvent(Base, UUIDPkMixin, TrackableMixin):
    __tablename__ = 'film_events'

    title = Column(String(1024), default='')
    description = Column(Text, default='')
    movie_id = Column(UUID, nullable=False)
    user_host_id = Column(UUID, nullable=False)
    is_private = Column(Boolean)
    start_event_time = Column(TIMESTAMP(timezone=True), nullable=False)
    event_location = Column(String(1024), nullable=False)
    duration_in_seconds = Column(Integer, nullable=False)
    seats_number = Column(SmallInteger, nullable=False)
    price_rub = Column(Integer, nullable=False)
    state = Column(Enum(FilmEventState), default=FilmEventState.PENDING, nullable=False)
    notification_state = Column(String(255), nullable=True)
