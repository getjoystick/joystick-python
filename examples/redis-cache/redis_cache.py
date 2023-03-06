import json
import typing as t

from redis.asyncio import Redis as AsyncRedis

from joystick._async.cache.cache import AsyncCacheInterface


class RedisCache(AsyncCacheInterface):
    def __init__(self, host: str, port: int, password: str) -> None:
        self.__redis = AsyncRedis(host=host, port=port, password=password, db=0)

    async def get(self, key: str) -> t.Optional[t.Any]:
        result = await self.__redis.get(key)
        if result is None:
            print("RedisCache: key not found: " + key)
            return None
        else:
            print("RedisCache: key found: " + key)
            return json.loads(result)

    async def set(self, key: str, value: t.Any, cache_expiration_seconds: int) -> None:
        await self.__redis.set(
            key, value=json.dumps(value), ex=cache_expiration_seconds
        )

    async def clear(self) -> None:
        await self.__redis.flushall()
