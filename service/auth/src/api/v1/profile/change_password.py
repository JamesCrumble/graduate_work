from fastapi import Depends, Request

from ..auth_service import AuthService, auth_service
from ..common.auth_credentials import get_user_from_access_token
from ..http_exceptions import NotAuthenticated
from ..schemas import ChangePasswordModel
from ..schemas.user import BaseUserAuth


async def change_password(
    request: Request,
    new_password: ChangePasswordModel,
    auth_service: AuthService = Depends(auth_service),
    user_auth: BaseUserAuth = Depends(get_user_from_access_token),
):
    if not user_auth.is_authenticated:
        raise NotAuthenticated

    await auth_service.change_user_password(
        new_password,
        user_auth,
        request.headers.get('user-agent', '')
    )
