import json
import re
import typing as t
import urllib.parse

from joystick.errors.api import MultipleContentsApiError

from .cache.cache import SyncCacheInterface
from .cache.in_memory import InMemoryCache
from .cache_key_builder import build_cache_key
from .params_dict import ParamsDict
from .transport import SyncTransport


class Client:
    # API KEY
    def get_api_key(self) -> str:
        return self.__api_key

    def set_api_key(self, api_key: str) -> None:
        if not isinstance(api_key, str) or len(api_key) == 0:
            raise TypeError("API key should be a valid non-empty string")

        self.__api_key = api_key

    api_key = property(get_api_key, set_api_key)

    # USER ID
    def get_user_id(self) -> t.Optional[str]:
        return self.__user_id

    def set_user_id(self, user_id: str) -> None:
        assert isinstance(user_id, str)
        self.__user_id = user_id

    user_id = property(get_user_id, set_user_id)

    # PARAMS
    def get_params(self) -> ParamsDict:
        return self.__params

    # def set_params(self, params: t.Dict[str, t.Any]):
    def set_params(self, params: t.Dict[str, t.Any]) -> None:
        if not isinstance(params, dict):
            raise ValueError("Params should be a valid dictionary")
        self.__params = ParamsDict(params)

    params = property(get_params, set_params)

    # SEM VER
    def get_sem_ver(self) -> str:
        return self.__sem_ver

    def set_sem_ver(self, sem_ver: str) -> None:
        if sem_ver != "":
            if not isinstance(sem_ver, str):
                raise ValueError("Semver should be a valid string")

            semver_str_valid = re.search(
                r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)$",
                sem_ver,
            )

            if semver_str_valid is None:
                raise ValueError('Provided value of semver "%s" is not valid' % sem_ver)
        self.__sem_ver = sem_ver

    sem_ver = property(get_sem_ver, set_sem_ver)

    # SERIALIZED
    def get_serialized(self) -> bool:
        return self.__serialized

    def set_serialized(self, serialized: bool) -> None:
        assert isinstance(serialized, bool)
        self.__serialized = serialized

    serialized = property(get_serialized, set_serialized)

    # CACHE EXPIRATION SECONDS
    def get_cache_expiration_seconds(self) -> int:
        return self.__cache_expiration_seconds

    def set_cache_expiration_seconds(self, cache_expiration_seconds: int) -> None:
        if (
            not isinstance(cache_expiration_seconds, int)
            or cache_expiration_seconds < 0
        ):
            raise ValueError(
                "Cache expiration seconds should be a valid non-negative integer"
            )
        self.__cache_expiration_seconds = cache_expiration_seconds

    cache_expiration_seconds = property(
        get_cache_expiration_seconds, set_cache_expiration_seconds
    )

    # CACHE
    def get_cache(self) -> SyncCacheInterface:
        return self.__cache

    def set_cache(self, cache: SyncCacheInterface) -> None:
        self.__cache = cache

    cache = property(get_cache, set_cache)

    def __init__(
        self,
        api_key: str,
        user_id: str = "",
        params: t.Optional[t.Dict[str, t.Any]] = None,
        sem_ver: str = "",
        serialized: bool = False,
        cache: t.Optional[SyncCacheInterface] = None,
        cache_expiration_seconds: int = 300,
    ) -> None:
        self.api_key = api_key
        self.user_id = user_id
        self.params = ParamsDict() if params is None else params
        self.sem_ver = sem_ver
        self.serialized = serialized
        self.cache_expiration_seconds = cache_expiration_seconds
        self.cache = InMemoryCache() if cache is None else cache
        self.__transport = SyncTransport(api_key=self.api_key)

    def get_contents(
        self,
        content_ids: t.Set[str],
        serialized: t.Optional[bool] = None,
        refresh: bool = False,
        full_response: bool = False,
    ) -> t.Dict[str, t.Any]:
        assert isinstance(
            content_ids, set
        ), "Content IDs should be a set to enforce unique content ids"

        assert len(content_ids) > 0, "Set of content IDs should be non-empty"
        assert all(
            [isinstance(cid, str) and len(cid) > 0 for cid in content_ids]
        ), "Every content id should be a str"
        assert isinstance(serialized, bool) or (
            serialized is None
        ), "Serialized option should be either boolean, or None (default - value from instance property `serialized`)"
        assert isinstance(
            refresh, bool
        ), "Refresh option should be boolean (default – False)"
        assert isinstance(full_response, bool)

        serialized_normalized = (
            serialized if serialized is not None else self.serialized
        )

        content_ids_sorted = sorted(list(content_ids))

        cache_key = build_cache_key(
            api_key=self.api_key,
            sem_ver=self.sem_ver,
            user_id=self.user_id,
            params=self.params,
            additional_segments=[
                content_ids_sorted,
                serialized_normalized,
                full_response,
            ],
        )

        if not refresh:
            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                assert isinstance(cached_result, dict)
                return cached_result

        query_params = {
            "c": json.dumps(content_ids_sorted),
            "dynamic": "true",
            **({"responseType": "serialized"} if serialized_normalized else {}),
        }

        request_body = {
            "u": self.user_id,
            "p": self.params,
            **({"v": self.sem_ver} if self.sem_ver != "" else {}),
        }

        query_params_encoded = urllib.parse.urlencode(query_params)

        response = self.__transport.make_request(
            "POST",
            "https://api.getjoystick.com/api/v1/combine/?" + query_params_encoded,
            request_body,
        )

        assert isinstance(response, dict)

        self.validate_get_contents_response(response)

        processed_response = response
        if not full_response:
            processed_response = dict(
                (key, content["data"]) for (key, content) in response.items()
            )

        self.cache.set(
            key=cache_key,
            value=processed_response,
            cache_expiration_seconds=self.cache_expiration_seconds,
        )

        return processed_response

    def get_content(
        self,
        content_id: str,
        serialized: t.Optional[bool] = None,
        refresh: bool = False,
        full_response: bool = False,
    ) -> t.Any:
        contents = self.get_contents(
            {content_id},
            serialized=serialized,
            refresh=refresh,
            full_response=full_response,
        )

        if contents.get(content_id, None) is None:
            raise MultipleContentsApiError(
                f'No key was returned for content_id "{content_id}"'
            )

        return contents.get(content_id)

    def publish_content_update(
        self,
        content_id: str,
        description: str,
        content: t.Any,
        dynamic_content_map: t.List[t.Any] = [],
    ) -> None:
        assert (
            isinstance(content_id, str) and len(content_id) > 0
        ), "Content ID should be non-empty string"
        assert (
            50 > len(description) > 0
        ), "Description should be non empty string lower than 50 characters"
        assert isinstance(dynamic_content_map, list)

        body = {"d": description, "c": content, "m": dynamic_content_map}

        self.__transport.make_request(
            "PUT", f"https://capi.getjoystick.com/api/v1/config/{content_id}", body
        )

    def validate_get_contents_response(
        self, get_contents_response: t.Dict[str, t.Union[str, t.Dict[str, t.Any]]]
    ) -> None:
        string_contents = [
            "Content ID: %s, error: %s" % (key, content)
            for (key, content) in get_contents_response.items()
            if type(content) == str
        ]

        if len(string_contents) != 0:
            # TODO: use correction Error
            raise MultipleContentsApiError(
                "Some of the keys are failed:\n - " + "\n\t- ".join(string_contents)
            )

    def clear_cache(self) -> None:
        self.__cache.clear()
