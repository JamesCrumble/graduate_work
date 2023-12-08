import uuid
from datetime import datetime
from http import HTTPStatus

import aiohttp
import orjson
import pytest

from ..testdata import TEST_USER_ID
from ..utils.helpers import build_endpoint_path

pytestmark = pytest.mark.asyncio

REVIEWS_ENDPOINT_PATH = build_endpoint_path('reviews')

ROW_ID: str = str(uuid.uuid4())
MOVIE_ID: str = str(uuid.uuid4())
REVIEW_ROW_DATA = {
    'id': ROW_ID,
    'description': 'TEST DESCRIPTION',
    'text': 'TEST TEXT',
    'created': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '000',
    'updated': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '000',
    'author_id': TEST_USER_ID,
    'movie_id': MOVIE_ID,
}


@pytest.mark.asyncio
async def test_create_review(http_session: aiohttp.ClientSession):
    response = await http_session.post(REVIEWS_ENDPOINT_PATH, data=orjson.dumps(REVIEW_ROW_DATA))
    assert response.status == HTTPStatus.OK, await response.text()


@pytest.mark.asyncio
async def test_get_reviewed_movie(get_request_as_json_data):
    data: list[dict] = await get_request_as_json_data(REVIEWS_ENDPOINT_PATH, params={'movie_id': MOVIE_ID})
    assert data and any(row_ == REVIEW_ROW_DATA for row_ in data)

    data: dict = await get_request_as_json_data(f'{REVIEWS_ENDPOINT_PATH}/{ROW_ID}')
    assert data == REVIEW_ROW_DATA


@pytest.mark.asyncio
async def test_update_reviewed_movie(http_session: aiohttp.ClientSession, get_request_as_json_data):
    REVIEW_ROW_DATA['text'] = 'TEST UPDATED TEXT'

    response = await http_session.put(f'{REVIEWS_ENDPOINT_PATH}/{ROW_ID}', data=orjson.dumps(REVIEW_ROW_DATA))
    assert response.status == HTTPStatus.OK, await response.text()

    data: dict = await get_request_as_json_data(f'{REVIEWS_ENDPOINT_PATH}/{ROW_ID}')
    assert data == REVIEW_ROW_DATA


@pytest.mark.asyncio
async def test_remove_review_from_movie(http_session: aiohttp.ClientSession):
    response = await http_session.delete(f'{REVIEWS_ENDPOINT_PATH}/{ROW_ID}')
    assert response.status == HTTPStatus.OK, await response.text()

    response = await http_session.get(f'{REVIEWS_ENDPOINT_PATH}/{ROW_ID}')
    assert response.status == HTTPStatus.NOT_FOUND, await response.text()
