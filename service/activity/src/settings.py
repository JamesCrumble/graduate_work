import logging

from env import init_env
from pydantic import BaseSettings

init_env()


class Settings(BaseSettings):
    api_name: str = 'ugc'

    PORT: int = 4600
    HOST: str = '0.0.0.0'

    auth_public_secret_key: str
    enable_authorization: bool = True

    workers: int
    enable_autoreload: bool = True
    ignore_request_id: bool = False
    logging_level: int = logging.DEBUG

    mongodb_host: str
    mongodb_port: int
    mongodb_username: str
    mongodb_password: str
    mongodb_database: str = 'activity'

    project_name = 'UGC'

    version = '1.0.1'

    description = 'Film UGC FASTAPI service'

    sentry_dsn: str

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings()
