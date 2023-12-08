import asyncio

import aiohttp
import pytest
import pytest_asyncio

from .testdata import test_user_token


# NOT FOR USE !!! Fix any async fixture
@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def http_session() -> aiohttp.ClientSession:
    session = aiohttp.ClientSession(
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Request-Id': 'test',
            'access_token': test_user_token,
        }
    )
    yield session  # type: ignore
    await session.close()


pytest_plugins = ['utils.fixtures']
