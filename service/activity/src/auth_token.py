from typing import Any
from urllib.parse import unquote

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from settings import settings

AUTH_PUBLIC_SECRET_KEY = settings.auth_public_secret_key.replace('\\n', '\n').encode('utf8')

access_token = APIKeyHeader(name='access_token', auto_error=False)


class ForbiddenHTTPException(HTTPException):

    def __init__(self, detail: Any = None) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class TokenPayload(BaseModel):
    user_id: str = ''
    username: str = ''
    groups: list[str] = list()
    browser_fingerprint: str = ''
    grant_type: str = ''
    is_super_user: bool = False
    exp: int = 0
    iat: int = 0


def token_payload_dependency(
    access_token: str | None = Depends(access_token),
) -> TokenPayload:
    if access_token is not None:
        token = access_token
    else:
        raise ForbiddenHTTPException('Not authenticated')

    return get_jwt_token_payload(token)


def get_jwt_token_payload(token: str):
    token = unquote(token)
    try:
        payload = jwt.decode(token, AUTH_PUBLIC_SECRET_KEY, algorithms=['RS256'])
    except jwt.ExpiredSignatureError:
        raise ForbiddenHTTPException('Token had been expired')
    except jwt.InvalidSignatureError:
        raise ForbiddenHTTPException('Invalid token signature')
    except jwt.InvalidTokenError:
        raise ForbiddenHTTPException()

    return TokenPayload(**payload)
