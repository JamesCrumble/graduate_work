from db.storage import RedisStorage
from redis.asyncio import Redis

redis: Redis | None = None


async def get_redis() -> RedisStorage:
    return RedisStorage(redis)
