import typing as t
from abc import ABC
from abc import abstractmethod


class SyncCacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> t.Optional[t.Any]:
        pass

    @abstractmethod
    def set(self, key: str, value: t.Any, cache_expiration_seconds: int) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
