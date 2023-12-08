from http import HTTPStatus

import aiohttp
import orjson
import pytest
from faker import Faker

from ..utils.helpers import build_endpoint_path

fake = Faker('en_US')
sign_url_endpoint = build_endpoint_path('users/sign')

fake_email: str = fake.email()
fake_password: str = fake.password(length=12, special_chars=True, upper_case=True)


pytestmark = pytest.mark.asyncio


async def test_invalid_password(http_session: aiohttp.ClientSession) -> None:
    password = fake.password(length=7, special_chars=True, upper_case=True)
    response = await http_session.post(sign_url_endpoint, data=orjson.dumps({'email': fake_email, 'password': password}))
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY, password

    password = fake.password(length=12, special_chars=False, upper_case=True)
    response = await http_session.post(sign_url_endpoint, data=orjson.dumps({'email': fake_email, 'password': password}))
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY, password

    password = fake.password(length=12, special_chars=True, upper_case=False)
    response = await http_session.post(sign_url_endpoint, data=orjson.dumps({'email': fake_email, 'password': password}))
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY, password


async def test_invalid_email(http_session: aiohttp.ClientSession) -> None:
    email = fake_email.replace('@', '')
    response = await http_session.post(sign_url_endpoint, data=orjson.dumps({'email': email, 'password': fake_password}))
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY, email

    email = fake_email.split('@')[0]
    response = await http_session.post(sign_url_endpoint, data=orjson.dumps({'email': email, 'password': fake_password}))
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY, email

    email = fake_email.split('@')[1]
    response = await http_session.post(sign_url_endpoint, data=orjson.dumps({'email': email, 'password': fake_password}))
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY, email


async def test_creation_when_doesnt_exists(http_session: aiohttp.ClientSession) -> None:
    response = await http_session.post(sign_url_endpoint, data=orjson.dumps({'email': fake_email, 'password': fake_password}))
    text = await response.text()
    assert response.status == HTTPStatus.OK, text


async def test_creation_when_already_exists(http_session: aiohttp.ClientSession) -> None:
    response = await http_session.post(sign_url_endpoint, data=orjson.dumps({'email': fake_email, 'password': fake_password}))
    text = await response.text()
    assert response.status == HTTPStatus.CONFLICT, text
