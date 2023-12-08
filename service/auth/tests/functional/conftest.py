import asyncio

import aiohttp
import pytest
import pytest_asyncio
from redis.asyncio import Redis
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .settings import test_settings
from .testdata.tables import RoleTable, UserRoleTable, UserTable
from .utils.test_dbs_clear_all import delete_all_data


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='module')
async def http_session() -> aiohttp.ClientSession:
    jar = aiohttp.CookieJar(unsafe=True)
    session = aiohttp.ClientSession(
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Request-Id': 'test',
        },
        cookie_jar=jar
    )
    yield session  # type: ignore
    await session.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client() -> Redis:
    redis: Redis = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    yield redis  # type: ignore
    await redis.close()


@pytest.fixture(scope='module')
def redis_delete_data() -> bool:
    delete_all_data()
    yield True  # type: ignore
    delete_all_data()


@pytest_asyncio.fixture(scope='session')
async def sqla_engine():
    dsl = {
        'dbname': test_settings.postgres_db,
        'user': test_settings.postgres_user,
        'password': test_settings.postgres_password,
        'host': test_settings.postgres_host,
        'port': test_settings.postgres_port,
    }
    connection_string = (
        'postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}'
    ).format(
        **dsl,
    )
    engine = create_async_engine(connection_string)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def db_session(sqla_engine: AsyncEngine):
    connection = await sqla_engine.connect()

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = Session()

    try:
        yield session
    finally:
        await session.close()
        await connection.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def delete_data(db_session: AsyncSession):
    tables = [UserRoleTable, UserTable, RoleTable]
    for table in tables:
        stmt = delete(table)
        await db_session.execute(stmt)
    await db_session.commit()
    yield
    tables = [UserRoleTable, UserTable, RoleTable]
    for table in tables:
        stmt = delete(table)
        await db_session.execute(stmt)
    await db_session.commit()

pytest_plugins = ['utils.roles_fixtures', 'utils.user_fixtures']
