from fastapi import Depends

from .auth_token import token_cookie_access, token_header_access
from .users import AuthenicatedUser, BaseUserAuth, get_auth_user, get_user_from_token


async def get_user_from_access_token(
    token_header: str | None = Depends(token_header_access),
    token_cookie: str | None = Depends(token_cookie_access),
) -> type[BaseUserAuth]:
    return await get_user_from_token(token_cookie or token_header)


async def get_auth_user_from_access_token(
    token_header: str | None = Depends(token_header_access),
    token_cookie: str | None = Depends(token_cookie_access),
) -> AuthenicatedUser:
    return await get_auth_user(token_cookie or token_header)
