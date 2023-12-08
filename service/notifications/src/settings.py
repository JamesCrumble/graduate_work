import logging

from env import init_env
from pydantic import BaseSettings

init_env()


class Settings(BaseSettings):
    api_name: str = 'notif'

    port: int = 4777

    host: str = '0.0.0.0'

    echo: bool = False
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    auth_public_secret_key: str
    enable_authorization: bool = True

    workers: int
    enable_autoreload: bool = True

    ignore_request_id: bool = True
    ignore_access_token: bool = True

    logging_level: int = logging.DEBUG

    project_name = 'NOTIFICATIONS'

    version = '1.0.1'

    description = 'Film Notifications FASTAPI service'

    sentry_dsn: str

    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    RABBITMQ_HOST: str = '127.0.0.1'
    RABBITMQ_PORT: str = 5672

    rabbit_exchange_name: str = 'notifications'
    rabbit_queue_email_name: str = 'email'
    rabbit_queue_web_push_name: str = 'web_push'

    rabbit_channel_exchange_type: str = 'direct'

    template_id_on_registration: int = 3

    from_email: str = ''
    sg_api_key: str = ''

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings()
