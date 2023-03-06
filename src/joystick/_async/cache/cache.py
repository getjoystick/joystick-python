import typing as t
from abc import ABC
from abc import abstractmethod


class AsyncCacheInterface(ABC):
    @abstractmethod
    async def get(self, key: str) -> t.Optional[t.Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: t.Any, cache_expiration_seconds: int) -> None:
        pass

    @abstractmethod
    async def clear(self) -> None:
        pass
