import asyncio
import sys
import uuid as uuid_pkg

import typer
from core.hasher import PBKDHasher
from core.logger import logger
from db.postgres import get_postgres_engine
from db.tables import UserTable
from env import init_env
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

init_env()


async def create_user(email: str, password: str, name: str = '', surname: str = ''):
    user = UserTable(id=uuid_pkg.uuid4(), email=email, password=PBKDHasher().encode(password), is_super_user=True,
                     first_name=name, second_name=surname)
    engine = get_postgres_engine()

    async with engine.begin() as conn:
        async_session = sessionmaker(conn, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            try:
                session.add(user)
                await session.commit()
                logger.debug(f'Superuser {email} was successfully created')
            except Exception as e:
                logger.debug(f'Error while creating Superuser {email} ' + (e.message if hasattr(e, 'message') else str(e)))

    await engine.dispose()


def main(email: str, password: str, name: str = '', surname: str = ''):
    """
    Create superuser auth service\n
    Example python create_super_user.py admin@yandex.ru 123qwe\n
    :param email: the email address is used as a login\n
    :param password: superuser password\n
    :param name: superuser first name\n
    :param surname: superuser surname\n
    """
    asyncio.run(create_user(email, password, name, surname))


if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    typer.run(main)
