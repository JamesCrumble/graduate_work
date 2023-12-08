from env import init_env
from pydantic import BaseSettings, Field

init_env()


class Settings(BaseSettings):

    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(6378, env='REDIS_PORT')

    service_host: str = Field('127.0.0.1', env='SERVICE_HOST')
    service_port: int = Field(4001, env='SERVICE_PORT')

    es_id_field_name: str = 'id'

    postgres_db: str = Field(env='POSTGRES_DB')
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int


test_settings = Settings()
