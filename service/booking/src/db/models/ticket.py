import enum

from sqlalchemy import UUID, Column, Enum, ForeignKey

from .base import Base
from .film_event import FilmEvent
from .mixins import TrackableMixin, UUIDPkMixin


class TicketState(enum.Enum):
    DRAFT: str = 'DRAFT'
    PAYED: str = 'PAYED'
    UNPAYED: str = 'UNPAYED'
    DELETED: str = 'DELETED'


class Ticket(Base, UUIDPkMixin, TrackableMixin):
    __tablename__ = 'booking_tickets'

    user_guest_id = Column(UUID, nullable=False)
    film_event_id = Column(UUID, ForeignKey(FilmEvent.id))
    state = Column(Enum(TicketState), nullable=False, default=TicketState.DRAFT)
