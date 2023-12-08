import aiohttp
import orjson
import pytest
import pytest_asyncio
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from testdata.tables import UserTable
from testdata.users import UserDB, UserDBFactory
from utils.hasher import PBKDHasher

from .helpers import build_endpoint_path, execute_stmt

login_url_endpoint = build_endpoint_path('users/login')
logout_url_endpoint = build_endpoint_path('users/logout')


@pytest.fixture(scope='module')
def user_get():
    user: UserDB = UserDBFactory.build()
    yield user


@pytest.fixture(scope='module')
def super_user_get():
    user: UserDB = UserDBFactory.build()
    user.is_super_user = True
    yield user


@pytest_asyncio.fixture(scope='module')
async def user_create(user_get: UserDB, db_session: AsyncSession):
    user_dict = user_get.dict(exclude_none=True)
    user_dict['password'] = PBKDHasher().encode(user_dict['password'])
    stmt = insert(UserTable).values(**user_dict)
    await execute_stmt(db_session, stmt)
    yield user_get
    stmt_delete = delete(UserTable).where(UserTable.id == user_get.id)
    await execute_stmt(db_session, stmt_delete)


@pytest_asyncio.fixture(scope='module')
async def super_user_create(super_user_get: UserDB, db_session: AsyncSession):
    user_dict = super_user_get.dict(exclude_none=True)
    user_dict['password'] = PBKDHasher().encode(user_dict['password'])
    stmt = insert(UserTable).values(**user_dict)
    await db_session.execute(stmt)
    await db_session.commit()
    yield super_user_get
    stmt_delete = delete(UserTable).where(UserTable.id == super_user_get.id)
    await db_session.execute(stmt_delete)
    await db_session.commit()


@pytest_asyncio.fixture(scope='function')
async def user_login(user_create: UserDB, http_session: aiohttp.ClientSession):
    user_data = user_create.dict(include={'email', 'password'})
    await http_session.post(login_url_endpoint, data=orjson.dumps(user_data))
    yield user_create
    # await http_session.post(logout_url_endpoint)


@pytest_asyncio.fixture(scope='function')
async def super_user_login(super_user_create: UserDB, http_session: aiohttp.ClientSession):
    user_data = super_user_create.dict(include={'email', 'password'})
    await http_session.post(login_url_endpoint, data=orjson.dumps(user_data))
    yield super_user_create
    # await http_session.post(logout_url_endpoint)
