import typing as t
from time import time

import pylru  # type: ignore

from .cache import AsyncCacheInterface


class InMemoryCache(AsyncCacheInterface):
    def __init__(self) -> None:
        # Magic number, use your implementation if you need another value for the maximum number of
        # elements
        self.__cache = pylru.lrucache(1000)

    async def get(self, key: str) -> t.Optional[t.Any]:
        if key in self.__cache:
            value, expire_at = self.__cache[key]
            if time() > expire_at:
                del self.__cache[key]
                return None
            return value
        return None

    async def set(self, key: str, value: t.Any, cache_expiration_seconds: int) -> None:
        expire_at = time() + cache_expiration_seconds
        self.__cache[key] = (value, expire_at)

    async def clear(self) -> None:
        self.__cache.clear()
