import logging
from typing import Optional

from env import init_env
from pydantic_settings import BaseSettings

init_env()


class Settings(BaseSettings):
    api_name: str = 'messages'

    PORT: int = 4800
    HOST: str = '0.0.0.0'

    auth_public_secret_key: str
    enable_authorization: bool = True

    workers: Optional[int]
    enable_autoreload: bool = True
    ignore_request_id: bool = False
    logging_level: int = logging.DEBUG
    test_list: list[str] = []

    project_name: str = 'INSTANT MESSAGES'

    version: str = '1.0.1'

    description: str = 'Instant messages FASTAPI service'

    sentry_dsn: str

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings()
