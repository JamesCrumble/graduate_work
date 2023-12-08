from pydantic import Field
from pydantic_settings import BaseSettings


class ProgramSettings(BaseSettings):
    mongo_host: str = Field(env='MONGO_HOST')
    mongo_port: int = Field(env='MONGO_PORT')
    mongo_local_port: int = Field(env='MONGO_LOCAL_PORT')
    postgres_host: str = Field(env='POSTGRES_HOST')
    postgres_port: int = Field(env='POSTGRES_PORT')
    postgres_local_port: int = Field(env='POSTGRES_LOCAL_PORT')
    postgres_db: str = Field(env='POSTGRES_DB')
    postgres_user: str = Field(env='POSTGRES_USER')
    postgres_password: str = Field(env='POSTGRES_PASSWORD')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


program_settings = ProgramSettings()
