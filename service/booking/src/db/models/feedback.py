from sqlalchemy import UUID, Column, ForeignKey, SmallInteger, String, Text

from .base import Base
from .film_event import FilmEvent
from .mixins import TrackableMixin, UUIDPkMixin


class FilmEventFeedback(Base, UUIDPkMixin, TrackableMixin):
    __tablename__ = 'film_event_feedbacks'

    title = Column(String(1024), default='')
    description = Column(Text, default='')
    film_event_id = Column(UUID, ForeignKey(FilmEvent.id, ondelete='CASCADE'))
    user_id = Column(UUID, nullable=False)

    rank = Column(SmallInteger, nullable=False)


class UserFeedback(Base, UUIDPkMixin, TrackableMixin):
    __tablename__ = 'user_feedbacks'

    title = Column(String(1024), default='')
    description = Column(Text, default='')
    film_event_id = Column(UUID, ForeignKey(FilmEvent.id, ondelete='CASCADE'))
    user_id = Column(UUID, nullable=False)
    about_user_id = Column(UUID, nullable=False)
    rank = Column(SmallInteger, nullable=False)
