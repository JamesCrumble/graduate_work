import uuid
from datetime import datetime
from http import HTTPStatus

import aiohttp
import orjson
import pytest

from ..testdata import TEST_USER_ID
from ..utils.helpers import build_endpoint_path

pytestmark = pytest.mark.asyncio

BOOKMARK_ENDPOINT_PATH = build_endpoint_path('bookmarks')

ROW_ID: str = str(uuid.uuid4())
MOVIE_ID: str = str(uuid.uuid4())
MOVIE_ID_FOR_UPDATE: str = str(uuid.uuid4())
BOOKMARK_ROW_DATA = {
    'id': ROW_ID,
    'user_id': TEST_USER_ID, 'movie_id': MOVIE_ID,
    'created': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '000'
}


@pytest.mark.asyncio
async def test_create_bookmark(http_session: aiohttp.ClientSession):
    response = await http_session.post(BOOKMARK_ENDPOINT_PATH, data=orjson.dumps(BOOKMARK_ROW_DATA))
    assert response.status == HTTPStatus.OK, await response.text()


@pytest.mark.asyncio
async def test_get_bookmark_movie(get_request_as_json_data):
    data: list[dict] = await get_request_as_json_data(BOOKMARK_ENDPOINT_PATH, params={'movie_id': MOVIE_ID})
    assert data and any(row_ == BOOKMARK_ROW_DATA for row_ in data)

    data: dict = await get_request_as_json_data(f'{BOOKMARK_ENDPOINT_PATH}/{ROW_ID}')
    assert data == BOOKMARK_ROW_DATA


@pytest.mark.asyncio
async def test_update_bookmark_movie(http_session: aiohttp.ClientSession, get_request_as_json_data):
    BOOKMARK_ROW_DATA['movie_id'] = MOVIE_ID_FOR_UPDATE

    response = await http_session.put(f'{BOOKMARK_ENDPOINT_PATH}/{ROW_ID}', data=orjson.dumps(BOOKMARK_ROW_DATA))
    assert response.status == HTTPStatus.OK, await response.text()

    data: dict = await get_request_as_json_data(f'{BOOKMARK_ENDPOINT_PATH}/{ROW_ID}')
    assert data == BOOKMARK_ROW_DATA


@pytest.mark.asyncio
async def test_remove_bookmark_from_movie(http_session: aiohttp.ClientSession):
    response = await http_session.delete(f'{BOOKMARK_ENDPOINT_PATH}/{ROW_ID}')
    assert response.status == HTTPStatus.OK, await response.text()

    response = await http_session.get(f'{BOOKMARK_ENDPOINT_PATH}/{ROW_ID}')
    assert response.status == HTTPStatus.NOT_FOUND, await response.text()
