from core.jwt import JWTTokenPairRaw
from fastapi import Depends, Response

from ..auth_service import AuthService, auth_service
from ..common.auth_credentials import get_user_from_access_token, get_user_tokens
from ..http_exceptions import NotAuthenticated
from ..schemas.user import BaseUserAuth, RequestSuccess


async def user_logout(
    response: Response,
    auth_service: AuthService = Depends(auth_service),
    user_tokens: JWTTokenPairRaw = Depends(get_user_tokens),
    auth_user: BaseUserAuth = Depends(get_user_from_access_token),
) -> RequestSuccess:
    if not auth_user.is_authenticated:
        raise NotAuthenticated

    await auth_service.logout(response, user_tokens)

    return RequestSuccess(detail='success')
