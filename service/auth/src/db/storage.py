from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any

from core.logger import logger
from orjson import orjson
from redis.asyncio import Redis
from settings import settings


class Storage(ABC):

    @abstractmethod
    async def save_to_cache(self, key: str, data: dict[str, Any], expiration_time) -> None:
        """Сохранить состояние в хранилище."""

    @abstractmethod
    async def get_from_cache(self, key: str) -> dict[str, Any]:
        """Получить состояние из хранилища."""


class RedisStorage(Storage):
    __slots__ = '_redis'

    def __init__(self, redis: Redis):
        self._redis = redis

    async def save_to_cache(self, key: str, data: dict[str, Any], expiration_time: timedelta | float) -> None:
        value = orjson.dumps(data)
        await self._redis.set(key, value, expiration_time)

    async def get_from_cache(self, key: str) -> dict[str, Any] | None:
        data = await self._redis.get(key)
        if not data:
            return None
        return orjson.loads(data)


if __name__ == '__main__':
    import asyncio

    async def main():
        redis = Redis(host=settings.redis_host, port=settings.redis_port,)
        storage = RedisStorage(redis)
        await storage.save_to_cache('test', {'data': 'string'}, 1000)
        logger.debug(await storage.get_from_cache('test'))
        await redis.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
