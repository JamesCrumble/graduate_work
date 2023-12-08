import random
import uuid
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from uuid import UUID

import aiohttp
import orjson
import pytest

from ..utils.helpers import build_endpoint_path

pytestmark = pytest.mark.asyncio

FILM_EVENTS_ENDPOINT_PATH = build_endpoint_path('film_event')

TEST_EVENTS_CREATION_COUNT: int = random.randint(15, 20)
CREATED_FILM_EVENTS: list[UUID] = list()
CREATE_FILM_EVENT_BODY: dict = {
    'title': 'test title',
    'description': 'test description',
    'movie_id': str(uuid.uuid4()),
    'is_private': bool(random.randint(0, 1)),
    'start_event_time': datetime.now(tz=timezone(timedelta(hours=3), name='Moscow')).isoformat(),
    'event_location': 'test location',
    'duration_in_seconds': random.randint(1, 10000),
    'seats_number': random.randint(1, 20),
    'price_rub': random.randint(200, 1000),
}


async def test_create_film_events(http_session: aiohttp.ClientSession):
    for _ in range(TEST_EVENTS_CREATION_COUNT):
        response = await http_session.post(FILM_EVENTS_ENDPOINT_PATH, data=orjson.dumps(CREATE_FILM_EVENT_BODY))
        assert response.status == HTTPStatus.CREATED, (await response.json())['detail']
        film_id = await response.json()

        try:
            CREATED_FILM_EVENTS.append(UUID(film_id))
        except BaseException as exc:
            raise Exception(f'{exc}. Film id => "{film_id}"')


async def test_get_all_film_events(http_session: aiohttp.ClientSession):
    page_number = 1
    page_size = min(10, TEST_EVENTS_CREATION_COUNT // 2)

    while page_number * page_size <= TEST_EVENTS_CREATION_COUNT:
        response = await http_session.get(FILM_EVENTS_ENDPOINT_PATH, params={'page_number': page_number, 'page_size': page_size})
        assert response.status == HTTPStatus.OK, (await response.json())['detail']

        data = await response.json()
        assert len(data) <= page_size and all(UUID(e['id']) in CREATED_FILM_EVENTS for e in data)

        page_number += 1


async def test_get_film_events_by_uid(http_session: aiohttp.ClientSession):
    assert len(CREATED_FILM_EVENTS) != 0
    for film_event_id in CREATED_FILM_EVENTS:
        response = await http_session.get(f'{FILM_EVENTS_ENDPOINT_PATH}/{film_event_id}')
        assert response.status == HTTPStatus.OK, (await response.json())['detail']


async def test_update_film_event(http_session: aiohttp.ClientSession):
    assert len(CREATED_FILM_EVENTS) != 0
    response = await http_session.get(f'{FILM_EVENTS_ENDPOINT_PATH}/{CREATED_FILM_EVENTS[0]}')
    assert response.status == HTTPStatus.OK, (await response.json())['detail']

    film_event: dict = await response.json()
    film_event['price_rub'] = 0
    await http_session.put(
        f'{FILM_EVENTS_ENDPOINT_PATH}/{film_event["id"]}', data=orjson.dumps(film_event), params={'notify_about_updates': False}
    )

    response = await http_session.get(f'{FILM_EVENTS_ENDPOINT_PATH}/{film_event["id"]}')
    assert response.status == HTTPStatus.OK and (await response.json()) == film_event, (await response.json())['detail']
