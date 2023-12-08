import json
from http import HTTPStatus
from uuid import uuid4

import aiohttp
import pytest
import websockets
from websockets import Headers

from ..testdata.auth_test_user import TEST_USER_ID, test_user_token
from ..utils.helpers import build_endpoint_path, build_ws_endpoint_path

pytestmark = pytest.mark.asyncio

WS_ENDPOINT_PATH = build_ws_endpoint_path('/sms/ws')
SEND_ENDPOINT_PATH = build_endpoint_path('/sms/send')


async def test_websocket_connection_noauth():
    extra_headers = Headers(
        {
            'X-Request-Id': uuid4(),
            'User-Agent': uuid4(),
        }
    )
    try:
        async with websockets.connect(WS_ENDPOINT_PATH, extra_headers=extra_headers):
            assert False
    except websockets.exceptions.InvalidStatusCode:
        assert True


async def test_websocket_connection():

    extra_headers = Headers(
        {
            'X-Request-Id': uuid4(),
            'User-Agent': uuid4(),
            'access_token': test_user_token
        }
    )
    async with websockets.connect(WS_ENDPOINT_PATH, extra_headers=extra_headers) as websocket:
        await websocket.send('test')
        message = await websocket.recv()
        assert message == 'Message text was: test'


async def test_websocket_send_message(http_session: aiohttp.ClientSession):
    extra_headers = Headers(
        {
            'X-Request-Id': uuid4(),
            'User-Agent': uuid4(),
            'access_token': test_user_token
        }
    )
    cookies = {
        'access_token': test_user_token
    }
    async with websockets.connect(WS_ENDPOINT_PATH, extra_headers=extra_headers) as websocket:
        data = {
            'message': 'test'
        }
        params = {
            'user_id': TEST_USER_ID
        }
        response = await http_session.get(
            SEND_ENDPOINT_PATH,
            data=json.dumps(data),
            params=params,
            cookies=cookies,
        )
        assert response.status == HTTPStatus.OK
        message = await websocket.recv()
        assert message == json.dumps(data)
