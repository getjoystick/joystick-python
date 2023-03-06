

import pytest

from joystick._async.client import AsyncClient

from .fixtures import valid_content_ids, valid_api_key


# ! ||--------------------------------------------------------------------------------||
# ! ||                                Validation                                      ||
# ! ||--------------------------------------------------------------------------------||


@pytest.mark.asyncio
async def test_get_content_no_content_ids(respx_mock, valid_api_key):
    client = AsyncClient(api_key=valid_api_key)
    with pytest.raises(AssertionError):
        await client.get_contents(content_ids={})


@pytest.mark.asyncio
async def test_get_content_content_ids_is_not_set(respx_mock, valid_api_key):
    client = AsyncClient(api_key=valid_api_key)
    with pytest.raises(AssertionError):
        await client.get_contents(content_ids=('cid1', 'cid2'))


def wrong_content_ids_params():
    return [
        (
            ['cid1', 'cid2'],
            'Only set is acceptable content ids structure'
        ),
        (
            {1, 2, 3},
            'Set of content ids can be only strings'
        ),
        (
            set(),
            'Non-empty set is a valid content ids parameters'
        ),
        (
            {True, True},
            'Set of content ids can be only strings'
        ),
        (
            {''},
            'Content id can not be empty'
        ),
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize("content_ids,error_message", wrong_content_ids_params())
async def test_get_content_content_ids_are_wrong(respx_mock, content_ids, error_message, valid_api_key):
    client = AsyncClient(api_key=valid_api_key)
    try:
        await client.get_contents(content_ids=content_ids)
    except AssertionError:
        return
    except:
        pass
    raise AssertionError(f"Expected to receive AssertionError from {error_message}")


def non_boolean_items():
    return [
        'True',
        'False',
        0,
        1,
        0.0,
        1.1,
        [],
        set(),
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize("non_boolean_value", non_boolean_items())
async def test_wrong_refresh_option(respx_mock, non_boolean_value, valid_content_ids, valid_api_key):
    client = AsyncClient(api_key=valid_api_key)
    with pytest.raises(AssertionError):
        await client.get_contents(content_ids=valid_content_ids, refresh=non_boolean_value)


@pytest.mark.asyncio
@pytest.mark.parametrize("non_boolean_value", non_boolean_items())
async def test_wrong_serialized_option(respx_mock, non_boolean_value, valid_api_key, valid_content_ids):
    client = AsyncClient(api_key=valid_api_key)
    with pytest.raises(AssertionError):
        await client.get_contents(content_ids=valid_content_ids, serialized=non_boolean_value)


@pytest.mark.asyncio
@pytest.mark.parametrize("non_boolean_value", non_boolean_items())
async def test_wrong_full_response_option(respx_mock, non_boolean_value, valid_content_ids, valid_api_key):
    client = AsyncClient(api_key=valid_api_key)
    with pytest.raises(AssertionError):
        await client.get_contents(content_ids=valid_content_ids, full_response=non_boolean_value)
