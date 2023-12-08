from http import HTTPStatus

import aiohttp
import orjson
import pytest
from faker import Faker
from testdata.roles import Role, UserRole
from testdata.users import UserDB
from utils.helpers import build_endpoint_path

fake = Faker('en_US')
pytestmark = pytest.mark.asyncio


async def test_get_user_roles_deny_permissions(
    http_session: aiohttp.ClientSession,
    user_login: UserDB,
):
    user_role_url_endpoint = build_endpoint_path(f'user_role/{user_login.id}/')
    response = await http_session.get(user_role_url_endpoint)
    assert response.status == HTTPStatus.FORBIDDEN


async def test_get_user_roles_allow_permissions(
    http_session: aiohttp.ClientSession,
    user_role_create: UserRole,
    user_login: UserDB,
):
    user_role_url_endpoint = build_endpoint_path(f'user_role/{user_login.id}/')
    response = await http_session.get(user_role_url_endpoint)
    assert response.status == HTTPStatus.OK


async def test_get_super_user_roles_allow_permissions(
    http_session: aiohttp.ClientSession,
    super_user_login: UserDB,
):
    user_role_url_endpoint = build_endpoint_path(f'user_role/{super_user_login.id}/')
    response = await http_session.get(user_role_url_endpoint)
    assert response.status == HTTPStatus.OK


async def test_delete_post_user_roles_allow_permissions(
    http_session: aiohttp.ClientSession,
    user_role_create: UserRole,
    super_user_create: UserDB,
    role_create: Role,
    super_user_role_get: UserRole,
    user_login: UserDB,
):

    user_role_post_url_endpoint = build_endpoint_path('user_role')
    user_role_data = {
        'user_id': str(super_user_create.id),
        'role_id': str(role_create.id)
    }
    user_role_data = orjson.loads(orjson.dumps(user_role_data))
    response = await http_session.post(user_role_post_url_endpoint, params=user_role_data)
    assert response.status == HTTPStatus.OK

    resp_data = await response.json()
    new_user_role_data = UserRole(**resp_data)
    user_role_url_endpoint = build_endpoint_path('user_role')
    user_role_delete_data = {
        'record_id': str(new_user_role_data.id)
    }
    response = await http_session.delete(user_role_url_endpoint, params=user_role_delete_data)
    assert response.status == HTTPStatus.OK
