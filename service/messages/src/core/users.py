from abc import ABC, abstractmethod

from .auth_token import TokenPayload, get_jwt_token_payload


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


async def get_user_from_token(
    token: str,
) -> BaseUserAuth:

    if token is None:
        return UnauthenticatedUser()

    token_payload: TokenPayload = get_jwt_token_payload(token)
    if token_payload is None:
        return UnauthenticatedUser()

    if token_payload.is_super_user:
        return SuperUserAuth(user_payload=token_payload)

    return SimpleUserAuth(user_payload=token_payload)
