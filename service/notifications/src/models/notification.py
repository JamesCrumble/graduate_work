import enum
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import TIMESTAMP, UUID, Boolean, Column, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base
from .templates import Template


class NotificationTaskState(enum.Enum):
    SENDED = 'S'
    IN_QUEUE = 'Q'
    CANCELED = 'C'


class NotificationTaskChannel(enum.Enum):
    SMS = 'S'
    EMAIL = 'E'
    PHONE = 'P'


class NotifiedStatus(enum.Enum):
    READED = 'R'
    INITIATED = 'I'
    FAILED = 'F'
    DELIVERED = 'D'


class NotificationTask(Base):
    __tablename__ = 'notificationtask'

    id = Column(UUID, primary_key=True)
    template_id = Column(Integer, ForeignKey(Template.id, ondelete='CASCADE'), name='template_id_id')
    body = Column(JSONB, nullable=False, default=dict(), server_default='{}')
    state = Column(Enum(NotificationTaskState), default=NotificationTaskState.IN_QUEUE.value, nullable=False)
    is_broadcast = Column(Boolean)
    importance = Column(Integer, default=0)
    channel = Column(Enum(NotificationTaskChannel), default=NotificationTaskChannel.EMAIL.value, nullable=False)
    dispatch_datetime = Column(TIMESTAMP(timezone=True), name='datetime_of_dispatch')
    sended_datetime = Column(TIMESTAMP(timezone=True), name='datetime_when_sended')
    created_at = Column(TIMESTAMP,  default=datetime.utcnow(), server_default=sa.text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(), server_onupdate=sa.text('CURRENT_TIMESTAMP')
    )


class NotificationStatus(Base):
    __tablename__ = 'notificationstatus'

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, primary_key=True, nullable=False)
    notification_task_id = Column(
        UUID,
        ForeignKey(NotificationTask.id, ondelete='CASCADE'),
        primary_key=True, nullable=False, name='notification_tasks_id_id'
    )
    status = Column(Enum(NotifiedStatus), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow())

    def __repr__(self) -> str:
        return f'NotificationStatus<{self.user_id=}, {self.notification_task_id=}, {self.status.value=}>'
