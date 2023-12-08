from http import HTTPStatus

import aiohttp
import pytest


@pytest.fixture
def get_request_as_json_data(http_session: aiohttp.ClientSession):
    async def inner(
        url: str,
        params: dict | None = None,
        body_data: dict | None = None,
        **kwargs
    ) -> list[dict] | dict:
        response = await http_session.get(url, params=params, data=body_data, **kwargs)
        assert response.status in (HTTPStatus.OK, HTTPStatus.NOT_MODIFIED)
        return await response.json()

    return inner
