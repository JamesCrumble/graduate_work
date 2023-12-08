import logging
from contextlib import contextmanager

import psycopg2
import settings
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


@contextmanager
def pg_context():
    """
    Генерация подключения к Postgres

    Args:
        dsl (dict): Параметры подключения

    Yields:
        [Открытое соединение, курсор,]
    """
    conn = psycopg2.connect(
        dbname=settings.program_settings.postgres_db,
        user=settings.program_settings.postgres_user,
        password=settings.program_settings.postgres_password,
        host=settings.program_settings.postgres_host,
        port=settings.program_settings.postgres_port,
        options='-c search_path=content',
        connect_timeout=20
    )
    cur = conn.cursor()
    try:
        yield [conn, cur, ]
    finally:
        cur.close()
        conn.close()


@contextmanager
def mongo_context():
    client = MongoClient(settings.program_settings.mongo_host, settings.program_settings.mongo_port)
    try:
        client.server_info()
        yield client
    except ServerSelectionTimeoutError:
        logging.info('___!! Не удалось подключиться к Монго !!___')
    finally:
        client.close()
