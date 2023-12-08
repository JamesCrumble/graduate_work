import enum
import uuid

from models import UserHistoryOperation
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
    inspect,
)
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import as_declarative


class OAuthType(enum.Enum):
    google = 'google'


@as_declarative()
class Base:
    __table_args__ = ({'schema': 'content'},)

    def dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }


class UserTable(Base):
    __tablename__ = 'users'  # noqa
    id = Column(UUID(as_uuid=True), primary_key=True)  # noqa
    email = Column(String(100), index=True, unique=True, nullable=False)
    first_name = Column(String(100))
    second_name = Column(String(100))
    password = Column(String(1000), nullable=False)
    active = Column(Boolean, default=True)
    is_super_user = Column(Boolean, default=False)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_default=func.now(), onupdate=func.now())


class RolesTable(Base):
    __tablename__ = 'roles'  # noqa
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), index=True, unique=True, nullable=False)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_default=func.now(), onupdate=func.now())


class UserRoleTable(Base):
    __tablename__ = 'user_role'  # noqa
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID, ForeignKey(RolesTable.id, ondelete='CASCADE'))
    user_id = Column(UUID, ForeignKey(UserTable.id, ondelete='CASCADE'))
    created = Column(DateTime, server_default=func.now())


class AccessToken(Base):
    __tablename__ = 'access_tokens'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey(UserTable.id, ondelete='CASCADE'))
    user_token = Column(String(2000), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default='False')
    user_agent = Column(String(255), nullable=False, server_default='default UA')
    created = Column(DateTime, server_default=func.now())


class UserHistory(Base):
    __tablename__ = 'user_history'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey(UserTable.id, ondelete='CASCADE'))
    operation_datetime = Column(DateTime(timezone=True), server_default=func.now())
    operation = Column(ENUM(UserHistoryOperation), nullable=False)
    user_agent = Column(Text, nullable=False, server_default='default UA')


class OAuthUser(Base):
    __tablename__ = 'oauth_user'
    id = Column(String(100), primary_key=True, nullable=False)
    oauth_type = Column(ENUM(OAuthType), primary_key=True, nullable=False)
    user_id = Column(UUID, ForeignKey(UserTable.id, ondelete='CASCADE'), index=True)
