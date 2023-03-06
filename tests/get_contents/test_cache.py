

from httpx import Response
import pytest

from joystick._async.client import AsyncClient

from .fixtures import api_response_get_contents, api_response_get_contents_serialized, valid_content_ids, valid_api_key, api_response_get_contents_cache_key
import respx
from mock import AsyncMock, patch

# ! ||--------------------------------------------------------------------------------||
# ! ||                                  Caching Tests                                 ||
# ! ||--------------------------------------------------------------------------------||


@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_default_cache_integration(respx_mock, valid_api_key, valid_content_ids, api_response_get_contents):
    client = AsyncClient(api_key=valid_api_key)

    combine_api_call = respx_mock.post(
        "https://api.getjoystick.com/api/v1/combine/?c=%5B%22cid1%22%2C+%22cid2%22%5D&dynamic=true",
        headers={
            'Content-Type': 'application/json',
            'x-api-key': valid_api_key
        },
        json={
            'u': '',
            "p": {}
        }
    ).mock(return_value=Response(200, content=api_response_get_contents))

    response_first = await client.get_contents(content_ids=valid_content_ids)
    response_second = await client.get_contents(content_ids=valid_content_ids)

    assert combine_api_call.call_count == 1
    assert response_first == response_second


@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_with_different_options(respx_mock, valid_api_key, valid_content_ids, api_response_get_contents, api_response_get_contents_serialized):
    client = AsyncClient(api_key=valid_api_key)

    not_serialized = respx_mock.post(
        "https://api.getjoystick.com/api/v1/combine/?c=%5B%22cid1%22%2C+%22cid2%22%5D&dynamic=true",
        headers={
            'Content-Type': 'application/json',
            'x-api-key': valid_api_key
        },
        json={
            'u': '',
            "p": {}
        }
    ).mock(return_value=Response(200, content=api_response_get_contents))

    serialized = respx_mock.post(
        "https://api.getjoystick.com/api/v1/combine/?c=%5B%22cid1%22%2C+%22cid2%22%5D&dynamic=true&responseType=serialized",
        headers={
            'Content-Type': 'application/json',
            'x-api-key': valid_api_key
        },
        json={
            'u': '',
            "p": {}
        }
    ).mock(return_value=Response(200, content=api_response_get_contents_serialized))

    response_first = await client.get_contents(content_ids=valid_content_ids, serialized=True)
    response_second = await client.get_contents(content_ids=valid_content_ids)

    assert not_serialized.call_count == 1
    assert serialized.call_count == 1
    assert response_first != response_second

    response_first_2nd_time = await client.get_contents(content_ids=valid_content_ids, serialized=True)
    response_second_2nd_time = await client.get_contents(content_ids=valid_content_ids)

    assert not_serialized.call_count == 1
    assert serialized.call_count == 1

    assert response_first == response_first_2nd_time
    assert response_second == response_second_2nd_time


@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_refresh_option(respx_mock, valid_api_key, valid_content_ids, api_response_get_contents):
    client = AsyncClient(api_key=valid_api_key)

    combine_api_call = respx_mock.post(
        "https://api.getjoystick.com/api/v1/combine/?c=[\"cid1\", \"cid2\"]&dynamic=true",
        headers={
            'Content-Type': 'application/json',
            'x-api-key': valid_api_key
        },
        json={
            'u': '',
            "p": {}
        }
    ).mock(return_value=Response(200, content=api_response_get_contents))

    response_first = await client.get_contents(content_ids=valid_content_ids)
    response_second = await client.get_contents(content_ids=valid_content_ids, refresh=True)

    assert combine_api_call.call_count == 2
    assert response_first == response_second


@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_refresh_option_should_write_to_cache(respx_mock, valid_api_key, valid_content_ids, api_response_get_contents):
    client = AsyncClient(api_key=valid_api_key)

    combine_api_call = respx_mock.post(
        "https://api.getjoystick.com/api/v1/combine/?c=[\"cid1\", \"cid2\"]&dynamic=true",
        headers={
            'Content-Type': 'application/json',
            'x-api-key': valid_api_key
        },
        json={
            'u': '',
            "p": {}
        }
    ).mock(return_value=Response(200, content=api_response_get_contents))

    response_first = await client.get_contents(content_ids=valid_content_ids, refresh=True)
    response_second = await client.get_contents(content_ids=valid_content_ids)

    assert combine_api_call.call_count == 1
    assert response_first == response_second


# ! ||--------------------------------------------------------------------------------||
# ! ||                              Caching expiration                                ||
# ! ||--------------------------------------------------------------------------------||

@pytest.mark.asyncio
@patch('joystick._async.cache.in_memory.InMemoryCache')
@pytest.mark.respx()
async def test_get_contents_default_cache_expiration(CacheMock, respx_mock, valid_api_key, valid_content_ids, api_response_get_contents, api_response_get_contents_cache_key):
    cache = CacheMock()
    cache.set = AsyncMock()
    cache.get = AsyncMock(return_value=None)

    client = AsyncClient(api_key=valid_api_key, cache=cache)

    combine_api_call = respx_mock.post(
        "https://api.getjoystick.com/api/v1/combine/?c=[\"cid1\", \"cid2\"]&dynamic=true",
        headers={
            'Content-Type': 'application/json',
            'x-api-key': valid_api_key
        },
        json={
            'u': '',
            "p": {}
        }
    ).mock(return_value=Response(200, content=api_response_get_contents))

    response = await client.get_contents(content_ids=valid_content_ids)

    #
    cache.get.assert_awaited()
    cache.set.assert_awaited()
    cache.set.assert_called_with(key=api_response_get_contents_cache_key, value=response, cache_expiration_seconds=300)


@pytest.mark.asyncio
@patch('joystick._async.cache.in_memory.InMemoryCache')
@pytest.mark.respx()
async def test_get_contents_respect_user_cache_expiration_seconds(CacheMock, respx_mock, valid_api_key, valid_content_ids, api_response_get_contents, api_response_get_contents_cache_key):
    cache = CacheMock()
    cache.set = AsyncMock()
    cache.get = AsyncMock(return_value=None)

    cache_expiration_seconds = 600
    client = AsyncClient(api_key=valid_api_key, cache=cache, cache_expiration_seconds=cache_expiration_seconds)

    combine_api_call = respx_mock.post(
        "https://api.getjoystick.com/api/v1/combine/?c=[\"cid1\", \"cid2\"]&dynamic=true",
        headers={
            'Content-Type': 'application/json',
            'x-api-key': valid_api_key
        },
        json={
            'u': '',
            "p": {}
        }
    ).mock(return_value=Response(200, content=api_response_get_contents))

    response = await client.get_contents(content_ids=valid_content_ids)

    #
    cache.get.assert_awaited()
    cache.set.assert_awaited()
    cache.set.assert_called_with(key=api_response_get_contents_cache_key, value=response,
                                 cache_expiration_seconds=cache_expiration_seconds)
