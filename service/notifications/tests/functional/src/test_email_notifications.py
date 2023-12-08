import uuid
from http import HTTPStatus

import aiohttp
import orjson
import pytest

from ..utils.helpers import build_endpoint_path

pytestmark = pytest.mark.asyncio

EMAIL_NOTIFICATIONS_ENDPOINT_PATH = build_endpoint_path('queue/email')


SEND_DATA = {
    'is_broadcast': False,
    'template_id': 10,
    'user_ids': [str(uuid.uuid4())],
    'context': {
        'test': 'test message to send'
    }
}

SEND_BED_DATA = {
    'field': 'nodata'
}

SEND_BROADCAST_DATA = {
    'is_broadcast': True,
    'template_id': 111,
    'context': {
        'test': 'test broadcast message to send'
    }
}


@pytest.mark.asyncio
async def test_create_email_notification(http_session: aiohttp.ClientSession):
    response = await http_session.post(EMAIL_NOTIFICATIONS_ENDPOINT_PATH, data=orjson.dumps(SEND_DATA))
    assert response.status == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_broadcast_email_notification(http_session: aiohttp.ClientSession):
    response = await http_session.post(EMAIL_NOTIFICATIONS_ENDPOINT_PATH, data=orjson.dumps(SEND_BROADCAST_DATA))
    assert response.status == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_bad_email_notification(http_session: aiohttp.ClientSession):
    response = await http_session.post(EMAIL_NOTIFICATIONS_ENDPOINT_PATH, data=orjson.dumps(SEND_BED_DATA))
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
