from uuid import UUID, uuid4

from faker import Faker
from pydantic import BaseModel
from pydantic_factories import ModelFactory

fake = Faker('en_US')


class Role(BaseModel):
    id: UUID
    title: str


class RoleFactory(ModelFactory):
    __model__ = Role
    title = 'role_admin'
    id = uuid4


class UserRole(BaseModel):
    id: UUID
    user_id: UUID
    role_id: UUID


class UserRoleFactory(ModelFactory):
    __model__ = UserRole
    id = uuid4
    user_id = uuid4
    role_id = uuid4
