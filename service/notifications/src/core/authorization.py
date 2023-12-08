from auth_token import access_token as token
from core.users import BaseUserAuth, get_user_from_token
from fastapi import Depends


async def get_user_from_access_token(access_token: str = Depends(token),) -> BaseUserAuth:
    return await get_user_from_token(access_token)
