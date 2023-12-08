import json
from base64 import b64decode

from authlib.integrations.starlette_client import OAuth, OAuthError
from core.utils import make_password
from fastapi import Depends, Request, Response
from itsdangerous.exc import BadSignature
from settings import settings
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import HTTPConnection
from starlette.types import Message, Receive, Scope, Send

from ..auth_service import AuthService, auth_service
from ..common.auth_credentials import get_user_from_access_token
from ..http_exceptions import NotAuthenticated
from ..roles.user_role.user_role_service import UserRoleService, get_user_role_service
from ..schemas.user import OAuthUserDB, RequestSuccess, SimpleUserAuth, UserLogin

config_data = {
    'GOOGLE_CLIENT_ID': settings.google_client_id,
    'GOOGLE_CLIENT_SECRET': settings.google_client_secret
}

starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url=settings.google_redirect_url,
    client_kwargs={'scope': 'openid email profile'},
)


class CustomSessionMiddleware(SessionMiddleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] not in ('http', 'websocket'):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)

        if self.session_cookie in connection.cookies:
            data = connection.cookies[self.session_cookie].encode('utf-8')
            try:
                data = self.signer.unsign(data, max_age=self.max_age)
                scope['session'] = json.loads(b64decode(data))
            except BadSignature:
                scope['session'] = {}
        else:
            scope['session'] = {}

        async def send_wrapper(message: Message) -> None:
            await send(message)

        await self.app(scope, receive, send_wrapper)


async def login(oauth_type: str, request: Request):
    oauth_client = oauth.create_client(oauth_type)
    redirect_uri = request.url_for('auth', oauth_type=oauth_type)
    return await oauth_client.authorize_redirect(request, redirect_uri)


async def auth(
    request: Request,
    response: Response,
    oauth_type: str,
    auth_service: AuthService = Depends(auth_service),
    user_role_service: UserRoleService = Depends(get_user_role_service),
):
    try:
        oauth_client = getattr(oauth, oauth_type)
        access_token = await oauth_client.authorize_access_token(request)
    except OAuthError:
        return

    user_data = access_token['userinfo']
    oauth_user_db = OAuthUserDB(id=user_data['sub'], oauth_type=oauth_type, user_id=None)
    user_data_db = UserLogin(email=user_data['email'], password=make_password())

    result = await auth_service.oauth_login(
        user_login=user_data_db,
        oauth_user_db=oauth_user_db,
        response=response,
        user_agent=request.headers.get('user-agent', ''),
        user_role_service=user_role_service,
    )
    return result


async def link(
    oauth_type: str,
    request: Request,
    user_auth: SimpleUserAuth = Depends(get_user_from_access_token),
):
    if not user_auth.is_authenticated:
        raise NotAuthenticated

    oauth_client = oauth.create_client(oauth_type)
    redirect_uri = request.url_for('link_perform', oauth_type=oauth_type)
    if 'access_token' in request.cookies:
        request.cookies.pop('access_token')
    if 'refresh_token' in request.cookies:
        request.cookies.pop('refresh_token')
    return await oauth_client.authorize_redirect(request, redirect_uri)


async def link_perform(
    request: Request,
    oauth_type: str,
    auth_service: AuthService = Depends(auth_service),
    user_auth: SimpleUserAuth = Depends(get_user_from_access_token),
):
    try:
        oauth_client = getattr(oauth, oauth_type)
        access_token = await oauth_client.authorize_access_token(request)
    except OAuthError:
        return

    user_data = access_token['userinfo']
    oauth_user_db = OAuthUserDB(id=user_data['sub'], oauth_type=oauth_type, user_id=user_auth.user_payload.user_id)

    await auth_service.oauth_link(
        oauth_user_db=oauth_user_db,
    )

    return RequestSuccess(detail='success')


async def untie(
    oauth_type: str,
    request: Request,
    auth_service: AuthService = Depends(auth_service),
    user_auth: SimpleUserAuth = Depends(get_user_from_access_token),
):
    if not user_auth.is_authenticated:
        raise NotAuthenticated

    oauth_user_db = OAuthUserDB(oauth_type=oauth_type, user_id=user_auth.user_payload.user_id)
    await auth_service.oauth_untie(
        oauth_user_db=oauth_user_db,
    )

    return RequestSuccess(detail='success')
