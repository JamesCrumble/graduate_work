from auth_token import access_token
from core.users import BaseUserAuth, get_user_from_token
from fastapi import Depends


async def get_user_from_access_token(
    access_token: str = Depends(access_token),
) -> BaseUserAuth:
    return await get_user_from_token(access_token)
