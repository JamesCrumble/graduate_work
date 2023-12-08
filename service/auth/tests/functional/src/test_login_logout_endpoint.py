from collections.abc import Sequence
from http import HTTPStatus

import pytest
from aiohttp import ClientSession

from ..utils.helpers import build_endpoint_path, random_word


def generate_email():
    return 'test_' + random_word(10)+'@'+random_word(6)+'.com'


USER_EXIST_MESSAGE = 'User allready exists'
test_user = dict(email=generate_email(), password='#test123QEWRzzTest#', is_super_user=False)


@pytest.mark.asyncio
async def test_register(http_session: ClientSession):
    global test_user

    endpoint = build_endpoint_path('users/sign')
    user = dict(email='test@gmail.com', password='test', is_super_user=False)
    res = await http_session.post(endpoint, data=user)
    assert res.status == HTTPStatus.UNPROCESSABLE_ENTITY

    while True:
        res = await http_session.post(endpoint, json=test_user)
        json = await res.json()

        if res.status == HTTPStatus.CONFLICT and 'detail' in json.keys() and json['detail'] == USER_EXIST_MESSAGE:
            test_user['email'] = generate_email()
            continue

        assert res.status == HTTPStatus.OK
        test_user = dict(list(test_user.items()) + list(json.items()))
        break


@pytest.mark.asyncio
async def test_login(http_session: ClientSession):
    global test_user

    endpoint = build_endpoint_path('users/login')

    user = dict(email='test@gmail', password='test', set_cookie=True)
    res = await http_session.post(endpoint, json=user)
    assert res.status == HTTPStatus.UNPROCESSABLE_ENTITY

    user = dict(email=test_user['email'], password=test_user['password'], set_cookie=True)
    res = await http_session.post(endpoint, json=user)
    assert res.status == HTTPStatus.OK

    res_body = await res.json()

    assert 'access_token' in res_body.keys()
    test_user['access_token'] = str(res_body['access_token'])
    assert 'refresh_token' in res_body.keys()
    test_user['refresh_token'] = str(res_body['refresh_token'])
    test_user['cookie'] = {'access_token': test_user['access_token'], 'refresh_token': test_user['refresh_token']}


@pytest.mark.asyncio
async def test_profile_edit():
    global test_user

    endpoint_edit = build_endpoint_path('profile/change_password')

    async def set_new_password(email: str, pwd: str, cookie: dict, code: int):
        async with ClientSession(cookies=cookie) as session:
            data = dict(email=email, new_password=pwd)
            res = await session.post(endpoint_edit, json=data)
            assert res.status == code

    await set_new_password(test_user['email'], test_user['password'][::-1], test_user['cookie'], HTTPStatus.OK)
    await set_new_password(test_user['email'],  '111', test_user['cookie'], HTTPStatus.UNPROCESSABLE_ENTITY)
    await set_new_password(test_user['email'],  test_user['password'], test_user['cookie'], HTTPStatus.OK)


@pytest.mark.asyncio
async def test_history(http_session: ClientSession):
    global test_user

    endpoint = build_endpoint_path('users/user_history')

    async with ClientSession(cookies=test_user['cookie']) as session:
        res = await session.get(endpoint, json=test_user,  params={'page_number': 1, 'page_size': 100})
        assert res.status == HTTPStatus.OK

        res_body = await res.json()

        assert isinstance(res_body, Sequence)
        assert len(res_body) == 1


@pytest.mark.asyncio
async def test_logout():
    global test_user
    endpoint = build_endpoint_path('users/logout')

    async with ClientSession(cookies=test_user['cookie']) as session:
        res = await session.post(endpoint)
        assert res.status == HTTPStatus.OK

    async with ClientSession(cookies=test_user['cookie']) as session:
        res = await session.post(endpoint)
        assert res.status == HTTPStatus.UNAUTHORIZED
