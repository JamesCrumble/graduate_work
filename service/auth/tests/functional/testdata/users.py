from uuid import UUID, uuid4

from faker import Faker
from pydantic import BaseModel
from pydantic_factories import ModelFactory

fake = Faker('en_US')


def generate_password():
    def inner():
        password = fake.password(length=12, special_chars=True, upper_case=True)
        return password
    return inner


class User(BaseModel):
    id: UUID
    email: str
    password: str


class UserDB(User):
    is_super_user: bool = False


class UserDBFactory(ModelFactory):
    __model__ = UserDB
    email = fake.email
    password = generate_password()
    id = uuid4
    is_super_user = False
