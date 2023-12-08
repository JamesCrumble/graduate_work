from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    success = 'success'
    error = 'error'


class RoleRead(BaseModel):
    id: UUID
    title: str
    created: datetime
    modified: datetime


class RoleCreate(BaseModel):
    title: str = Field(min_length=3)


class RoleUpdate(BaseModel):
    id: UUID
    title: str


class RoleList(BaseModel):
    list: list[RoleRead]


class UserRole(BaseModel):
    id: UUID
    role_id: UUID
    user_id: UUID
    created: datetime | None


class User(BaseModel):
    id: UUID
    email: str
    first_name: str
    second_name: str
    password: str
    active: bool
    is_super_user: bool
    created: datetime
    modified: datetime


class ActionStatus(BaseModel):
    status: StatusEnum
    error_message: str | None
