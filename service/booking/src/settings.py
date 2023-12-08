import logging
from typing import Optional

from env import init_env
from pydantic import BaseSettings

init_env()


class Settings(BaseSettings):
    api_name: str = 'booking'

    PORT: int = 4800
    HOST: str = '127.0.0.1'

    auth_public_secret_key: str
    enable_authorization: bool = True

    workers: Optional[int]
    enable_autoreload: bool = True
    ignore_request_id: bool = True
    logging_level: int = logging.DEBUG
    test_list: list[str] = []

    project_name: str = 'BOOKING'

    version: str = '1.0.1'

    description: str = 'Booking FASTAPI service'

    sentry_dsn: str

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    notification_service_host: str = ''
    notification_service_port: int = 0
    notification_user_token: str = ''

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings()
