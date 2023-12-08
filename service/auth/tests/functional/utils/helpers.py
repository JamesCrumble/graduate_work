import random
import string

from settings import test_settings


def build_endpoint_path(endpoint: str) -> str:
    endpoint = endpoint.removeprefix('/').removesuffix('/')
    return f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/{endpoint}'  # noqa


def random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


async def execute_stmt(db_session, stmt):
    await db_session.execute(stmt)
    await db_session.commit()
