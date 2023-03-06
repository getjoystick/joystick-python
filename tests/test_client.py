
from joystick import AsyncClient
from joystick._async.cache.in_memory import InMemoryCache
import pytest
from unittest.mock import MagicMock, patch
from mock import AsyncMock

TEST_API_KEY = 'test-api-key'


def test_no_api_key_should_throw_exception():
    with pytest.raises(TypeError):
        client = AsyncClient()


@pytest.mark.asyncio
@patch('joystick._async.cache.in_memory.InMemoryCache')
async def test_clear_cache(CacheMock):

    clear_method_mock = AsyncMock()
    cache = CacheMock()
    cache.clear = clear_method_mock

    client = AsyncClient(api_key=TEST_API_KEY, cache=cache)
    await client.clear_cache()

    cache.clear.assert_called_once_with()
