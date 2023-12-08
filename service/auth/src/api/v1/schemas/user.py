import re
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from core.jwt import TokenPayload
from models import UserHistoryOperation
from pydantic import BaseModel, EmailStr, Field, ValidationError, validator
from pydantic.error_wrappers import ErrorWrapper
from pydantic.fields import ModelField

PASSWORD_DOC: str = '''
    Has minimum 8 characters in length.
    At least one uppercase English letter.
    At least one lowercase English letter.
    At least one digit.
    At least one special character.
'''

# Has minimum 8 characters in length. Adjust it by modifying {8,}
# At least one uppercase English letter. You can remove this condition by removing (?=.*?[A-Z])
# At least one lowercase English letter. You can remove this condition by removing (?=.*?[a-z])
# At least one digit. You can remove this condition by removing (?=.*?[0-9])
# At least one special character, You can remove this condition by removing (?=.*?[_#?!@$%^&*-])
PASSWORD_REGEXP: re.Pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[\(\)_#?!@$%^&*-]).{8,}$')

PasswordField = Field(..., description=PASSWORD_DOC)


def password_validator(cls, password: str, field: ModelField) -> str:
    if not PASSWORD_REGEXP.fullmatch(password):
        raise ValidationError(
            [ErrorWrapper(ValueError(PASSWORD_DOC), loc=field.name)], cls
        )
    return password


class BaseUser(BaseModel):
    email: EmailStr
    is_super_user: bool | None = None
    password: str = PasswordField

    _password_validator = validator('password', allow_reuse=True)(password_validator)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = PasswordField
    set_cookie: bool = True

    _password_validator = validator('password', allow_reuse=True)(password_validator)


class ChangePasswordModel(BaseModel):
    email: EmailStr | None = None
    new_password: str = PasswordField

    _password_validator = validator('new_password', allow_reuse=True)(password_validator)


class UserProfile(BaseModel):
    id: UUID
    email: str
    ...


class UserDB(UserProfile):
    password: str
    is_super_user: bool | None = None


class OAuthUserDB(BaseModel):
    id: str | None
    oauth_type: str
    user_id: UUID | None


class UserRole(BaseModel):
    title: str


class BaseUserAuth(ABC):
    @property
    @abstractmethod
    def is_authenticated(self) -> bool:
        ...

    @property
    @abstractmethod
    def display_name(self) -> str:
        ...

    @property
    @abstractmethod
    def is_super_user(self) -> bool:
        ...


class SimpleUserAuth(BaseUserAuth):
    user_payload: TokenPayload
    username: str

    def __init__(self, user_payload: TokenPayload) -> None:
        self.user_payload = user_payload
        self.username = user_payload.username

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

    @property
    def is_super_user(self) -> bool:
        return False


class UnauthenticatedUser(BaseUserAuth, ABC):
    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def display_name(self) -> str:
        return ''

    @property
    def is_super_user(self) -> bool:
        return False


class SuperUserAuth(SimpleUserAuth):
    @property
    def is_super_user(self) -> bool:
        return True
    ...


class UserHistoryRecord(BaseModel):

    operation: UserHistoryOperation = Field(..., description='in context of history its always "LOGIN" operation')
    operation_datetime: datetime
    user_agent: str


class RequestSuccess(BaseModel):
    detail: str
