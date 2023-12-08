import pytest
import pytest_asyncio
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from testdata.roles import Role, RoleFactory, UserRole, UserRoleFactory
from testdata.tables import RoleTable, UserRoleTable
from testdata.users import UserDB


@pytest.fixture(scope='module')
def role_get():
    user: Role = RoleFactory.build()
    yield user


@pytest.fixture(scope='module')
def user_role_get(user_get: UserDB, role_get: Role):
    user_role: UserRole = UserRoleFactory.build()
    user_role.user_id = user_get.id
    user_role.role_id = role_get.id
    yield user_role


@pytest.fixture(scope='module')
def super_user_role_get(super_user_get: UserDB, role_get: Role):
    user_role: UserRole = UserRoleFactory.build()
    user_role.user_id = super_user_get.id
    user_role.role_id = role_get.id
    yield user_role


@pytest_asyncio.fixture(scope='module')
async def role_create(role_get: Role, db_session: AsyncSession):
    stmt = insert(RoleTable).values(**role_get.dict())
    await db_session.execute(stmt)
    await db_session.commit()
    yield role_get
    stmt_delete = delete(RoleTable).where(RoleTable.id == role_get.id)
    await db_session.execute(stmt_delete)
    await db_session.commit()


@pytest_asyncio.fixture(scope='function')
async def user_role_create(user_role_get: UserRole, user_create: UserDB, role_create: Role, db_session: AsyncSession):
    stmt = insert(UserRoleTable).values(**user_role_get.dict())
    await db_session.execute(stmt)
    await db_session.commit()
    yield user_role_get
    stmt_delete = delete(UserRoleTable).where(UserRoleTable.id == user_role_get.id)
    await db_session.execute(stmt_delete)
    await db_session.commit()


@pytest_asyncio.fixture(scope='function')
async def super_user_role_create(
    super_user_role_get: UserRole,
    super_user_create: UserDB,
    role_create: Role,
    db_session: AsyncSession
):
    stmt = insert(UserRoleTable).values(**super_user_role_get.dict())
    await db_session.execute(stmt)
    await db_session.commit()
    yield super_user_role_get
    stmt_delete = delete(UserRoleTable).where(UserRoleTable.id == super_user_role_get.id)
    await db_session.execute(stmt_delete)
    await db_session.commit()
