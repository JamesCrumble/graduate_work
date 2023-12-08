from fastapi import Depends, Request

from ..auth_service import AuthService, auth_service
from ..schemas import BaseUser


async def user_sign(
    user_data: BaseUser,
    request: Request,
    auth_service: AuthService = Depends(auth_service)
):
    result = await auth_service.sign(user_data=user_data, user_agent=request.headers.get('user-agent', ''))

    return result
