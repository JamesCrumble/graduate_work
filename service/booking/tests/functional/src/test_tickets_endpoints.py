from http import HTTPStatus
from uuid import UUID

import aiohttp
import orjson
import pytest

from ..utils.helpers import build_endpoint_path
from .test_filmevents_endpoints import CREATE_FILM_EVENT_BODY, FILM_EVENTS_ENDPOINT_PATH

pytestmark = pytest.mark.asyncio

TICKET_ENDPOINT_PATH = build_endpoint_path('ticket/')

TEST_TICKETS_CREATION_COUNT: int = CREATE_FILM_EVENT_BODY['seats_number'] + 1
CREATED_TICKETS: list[UUID] = list()
TICKET_ID = ''


async def test_create_ticket(http_session: aiohttp.ClientSession, http_session_guest: aiohttp.ClientSession):
    global TICKET_ID

    response = await http_session.post(FILM_EVENTS_ENDPOINT_PATH, data=orjson.dumps(CREATE_FILM_EVENT_BODY))
    assert response.status == HTTPStatus.CREATED, (await response.json())['detail']
    film_event_id = await response.json()

    data = {'film_event_id': film_event_id, 'state': 'PAYED'}
    response = await http_session_guest.post(TICKET_ENDPOINT_PATH, data=orjson.dumps(data))
    assert response.status == HTTPStatus.CREATED, (await response.json())['detail']
    ticket_id = await response.json()
    TICKET_ID = ticket_id

    response = await http_session_guest.post(TICKET_ENDPOINT_PATH, data=orjson.dumps(data))
    assert response.status == HTTPStatus.CREATED, (await response.json())['detail']
    ticket_id_2 = await response.json()
    assert ticket_id_2 == ticket_id


async def test_get_all_tickets(http_session_guest: aiohttp.ClientSession):
    page_number = 1
    page_size = 10

    response = await http_session_guest.get(TICKET_ENDPOINT_PATH, params={'page_number': page_number, 'page_size': page_size})
    assert response.status == HTTPStatus.OK, (await response.json())['detail']

    data = await response.json()
    assert len(data) > 0


async def test_get_ticket_by_uid(http_session_guest: aiohttp.ClientSession):
    response = await http_session_guest.get(f'{TICKET_ENDPOINT_PATH}/{TICKET_ID}')
    assert response.status == HTTPStatus.OK, (await response.json())['detail']


async def test_update_ticket(http_session_guest: aiohttp.ClientSession):
    data = {'ticket_id': TICKET_ID, 'state': 'DRAFT'}
    response = await http_session_guest.put(f'{TICKET_ENDPOINT_PATH}', data=orjson.dumps(data))
    assert response.status == HTTPStatus.OK
