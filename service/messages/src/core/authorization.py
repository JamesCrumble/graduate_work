from fastapi import Depends, Header

from .auth_token import api_key_access
from .users import BaseUserAuth, get_user_from_token


async def get_user_from_header_access_token(
    access_token: str = Header(alias='access_token'),
) -> BaseUserAuth:
    return await get_user_from_token(access_token)


async def get_user_from_access_token(
    access_token: str = Depends(api_key_access),
) -> BaseUserAuth:
    return await get_user_from_token(access_token)
