from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

mongo_db: AsyncIOMotorClient = None


class MongoDBConnectionString(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str

    def __str__(self) -> str:
        return 'mongodb://{username}:{password}@{host}:{port}'.format(
            **self.dict()
        )


def get_client() -> AsyncIOMotorClient:
    return mongo_db


class MongoDBException(Exception):
    ...
