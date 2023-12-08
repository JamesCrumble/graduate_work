from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    __table_args__ = ({'schema': 'content'},)


class UserTable(Base):
    __tablename__ = 'users'  # noqa
    id = Column(UUID(as_uuid=True), primary_key=True)  # noqa
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_super_user = Column(Boolean, default=False)


class RoleTable(Base):
    __tablename__ = 'roles'  # noqa
    id = Column(UUID(as_uuid=True), primary_key=True)  # noqa
    title = Column(String, index=True, unique=True, nullable=False)


class UserRoleTable(Base):
    __tablename__ = 'user_role'  # noqa
    id = Column(UUID(as_uuid=True), primary_key=True)  # noqa
    user_id = Column(UUID(as_uuid=True))  # noqa
    role_id = Column(UUID(as_uuid=True))  # noqa
