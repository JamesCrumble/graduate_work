from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import TIMESTAMP, Column, Integer, String, Text

from .base import Base


class Template(Base):
    __tablename__ = 'template'

    id = Column(Integer, primary_key=True)
    name = Column(String(512), default='', nullable=False)
    template_text = Column(Text, default='', server_default='', nullable=False)
    template_title = Column(String(255), default='', server_default='', nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow(), server_default=sa.text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(), server_onupdate=sa.text('CURRENT_TIMESTAMP')
    )
