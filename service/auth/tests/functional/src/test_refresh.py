from http import HTTPStatus

import aiohttp
import orjson
import pytest
from faker import Faker

from ..testdata.users import UserDB
from ..utils.helpers import build_endpoint_path

fake = Faker('en_US')
refresh_url_endpoint = build_endpoint_path('users/refresh')
login_url_endpoint = build_endpoint_path('users/login')
history_url_endpoint = build_endpoint_path('users/user_history')
pytestmark = pytest.mark.asyncio


async def test_refresh_without_login(http_session: aiohttp.ClientSession):
    response = await http_session.post(refresh_url_endpoint)
    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_refresh_with_login(
    http_session: aiohttp.ClientSession,
    user_create: UserDB
):
    user_data = user_create.dict(include={'email', 'password'})
    response = await http_session.post(login_url_endpoint, data=orjson.dumps(user_data))
    assert response.status == HTTPStatus.OK
    response = await http_session.post(refresh_url_endpoint)
    assert response.status == HTTPStatus.OK
    body = await response.json()
    assert 'access_token' in body
    assert 'refresh_token' in body


async def test_login_access_token_expired_after_refresh(
    http_session: aiohttp.ClientSession,
    user_create: UserDB
):
    user_data = user_create.dict(include={'email', 'password'})
    response = await http_session.post(login_url_endpoint, data=orjson.dumps(user_data))
    login_tokens = await response.json()

    assert response.status == HTTPStatus.OK
    response = await http_session.post(refresh_url_endpoint)

    response_login_cred = await http_session.get(history_url_endpoint, cookies=login_tokens)
    assert response_login_cred.status == HTTPStatus.UNAUTHORIZED
