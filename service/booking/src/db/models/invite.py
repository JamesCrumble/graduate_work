import enum

from sqlalchemy import UUID, Column, Enum, ForeignKey

from .base import Base
from .film_event import FilmEvent
from .mixins import TrackableMixin, UUIDPkMixin


class InviteState(enum.Enum):
    CREATED: str = 'CREATED'
    SENDED: str = 'SENDED'
    VIEWED: str = 'VIEWED'


class PrivateInvite(Base, UUIDPkMixin, TrackableMixin):
    __tablename__ = 'private_invites'

    user_guest_id = Column(UUID, nullable=False)
    film_event_id = Column(UUID, ForeignKey(FilmEvent.id, ondelete='CASCADE'))
    state = Column(Enum(InviteState), nullable=False, default=InviteState.CREATED)
