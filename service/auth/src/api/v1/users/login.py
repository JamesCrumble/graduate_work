from fastapi import Depends, Request, Response

from ..auth_service import AuthService, auth_service
from ..roles.user_role.user_role_service import UserRoleService, get_user_role_service
from ..schemas import UserLogin


async def user_login(
    user_login: UserLogin,
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(auth_service),
    user_role_service: UserRoleService = Depends(get_user_role_service),
):
    result = await auth_service.login(
        user_login=user_login,
        response=response,
        user_agent=request.headers.get('user-agent', ''),
        user_role_service=user_role_service,
    )

    return result
