import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, UUID, Column, text


class UUIDPkMixin:
    id = Column(UUID, primary_key=True, default=uuid.uuid4, nullable=False)


class TrackableMixin:
    created = Column(TIMESTAMP, nullable=True, default=datetime.utcnow, server_default=text('CURRENT_TIMESTAMP'))
    modified = Column(TIMESTAMP, nullable=True, onupdate=datetime.utcnow, server_onupdate=text('CURRENT_TIMESTAMP'))
