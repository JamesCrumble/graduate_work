from core.jwt import JWTTokenPairRaw
from fastapi import Depends, Response

from ..auth_service import AuthService, auth_service
from ..common.auth_credentials import get_user_from_refresh_token, get_user_tokens
from ..http_exceptions import NotAuthenticated
from ..schemas.user import BaseUserAuth


async def user_token_refresh(
    response: Response,
    service: AuthService = Depends(auth_service),
    user_tokens: JWTTokenPairRaw = Depends(get_user_tokens),
    auth_user: BaseUserAuth = Depends(get_user_from_refresh_token),
):
    if not auth_user.is_authenticated:
        raise NotAuthenticated

    result = await service.refresh(
        response=response,
        user_tokens=user_tokens,
    )

    return result
