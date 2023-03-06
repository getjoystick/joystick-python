import hashlib
import json
import typing as t

from .params_dict import ParamsDict


def build_cache_key(
    *,
    api_key: str,
    sem_ver: str,
    user_id: str,
    params: ParamsDict,
    additional_segments: t.List[t.Any]
) -> str:
    params_sorted = sorted(params.items(), key=lambda p: p[0])

    key_segments = [api_key, params_sorted, sem_ver, user_id, *additional_segments]

    encoded_key_segments = json.dumps(key_segments).encode("utf-8")

    return hashlib.sha256(encoded_key_segments).hexdigest()
