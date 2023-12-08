from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    service_host: str = Field('127.0.0.1', env='SERVICE_HOST')
    service_port: int = Field(4800, env='SERVICE_PORT')


test_settings = Settings()
