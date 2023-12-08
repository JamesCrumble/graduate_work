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


class UnauthenticatedUser(BaseUserAuth):
    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def display_name(self) -> str:
        return ''

    @property
    def is_super_user(self) -> bool:
        return False


class AuthenicatedUser(BaseUserAuth):
    def __init__(self, user_payload: TokenPayload) -> None:
        self.user_payload = user_payload

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.user_payload.username

    @property
    def is_super_user(self) -> bool:
        return self.user_payload.is_super_user


async def get_auth_user(token: str | None) -> AuthenicatedUser:
    token_payload: TokenPayload = get_jwt_token_payload(token)
    return AuthenicatedUser(user_payload=token_payload)


async def get_user_from_token(token: str | None) -> type[BaseUserAuth]:
    if token is None:
        return UnauthenticatedUser()
    return await get_auth_user(token)
