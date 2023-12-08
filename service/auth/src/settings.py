import logging

from env import init_env
from pydantic import BaseSettings

init_env()


class Settings(BaseSettings):
    api_name: str = 'movapi'

    port: int = 4200
    host: str = '127.0.0.1'

    workers: int
    enable_autoreload: bool = True
    logging_level: int = logging.DEBUG
    ignore_request_id: bool = False

    redis_host: str
    redis_port: int

    cache_expire_in_seconds = 1200

    project_name = 'Auth service'

    version = '1.0.0'

    description = 'Authorization FASTAPI service'

    private_secret_key: str
    public_secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 7200

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    google_client_id: str
    google_client_secret: str
    google_redirect_url: str

    jaeger_host = '127.0.0.1'
    jaeger_port = 6831
    enable_tracer: bool = True

    throttling_limit: int = 10
    throttling_window: int = 60

    sentry_dsn: str

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings()
