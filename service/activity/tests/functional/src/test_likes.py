import uuid
from datetime import datetime
from http import HTTPStatus

import aiohttp
import orjson
import pytest

from ..testdata import TEST_USER_ID
from ..utils.helpers import build_endpoint_path

pytestmark = pytest.mark.asyncio

LIKES_ENDPOINT_PATH = build_endpoint_path('likes')

ROW_ID: str = str(uuid.uuid4())
MOVIE_ID: str = str(uuid.uuid4())
LIKE_ROW_DATA = {
    'id': ROW_ID,
    'user_id': TEST_USER_ID, 'movie_id': MOVIE_ID,
    'like': 1, 'created': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '000'
}


@pytest.mark.asyncio
async def test_create_like(http_session: aiohttp.ClientSession):
    response = await http_session.post(LIKES_ENDPOINT_PATH, data=orjson.dumps(LIKE_ROW_DATA))
    assert response.status == HTTPStatus.OK, await response.text()


@pytest.mark.asyncio
async def test_get_liked_movie(get_request_as_json_data):
    data: list[dict] = await get_request_as_json_data(LIKES_ENDPOINT_PATH, params={'movie_id': MOVIE_ID})
    assert data and any(row_ == LIKE_ROW_DATA for row_ in data)

    data: dict = await get_request_as_json_data(f'{LIKES_ENDPOINT_PATH}/{ROW_ID}')
    assert data == LIKE_ROW_DATA


@pytest.mark.asyncio
async def test_update_liked_movie(http_session: aiohttp.ClientSession, get_request_as_json_data):
    LIKE_ROW_DATA['like'] = 2

    response = await http_session.put(f'{LIKES_ENDPOINT_PATH}/{ROW_ID}', data=orjson.dumps(LIKE_ROW_DATA))
    assert response.status == HTTPStatus.OK, await response.text()

    data: dict = await get_request_as_json_data(f'{LIKES_ENDPOINT_PATH}/{ROW_ID}')
    assert data == LIKE_ROW_DATA


@pytest.mark.asyncio
async def test_remove_like_from_movie(http_session: aiohttp.ClientSession):
    response = await http_session.delete(f'{LIKES_ENDPOINT_PATH}/{ROW_ID}')
    assert response.status == HTTPStatus.OK, await response.text()

    response = await http_session.get(f'{LIKES_ENDPOINT_PATH}/{ROW_ID}')
    assert response.status == HTTPStatus.NOT_FOUND, await response.text()
