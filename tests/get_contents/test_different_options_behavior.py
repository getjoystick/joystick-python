

from httpx import Response
import pytest

from joystick._async.client import AsyncClient

import json
import respx

from .fixtures import api_response_get_contents, api_response_get_contents_serialized, valid_content_ids, valid_api_key


# ! ||--------------------------------------------------------------------------------||
# ! ||                         Different options behavior                             ||
# ! ||--------------------------------------------------------------------------------||


@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_minimal_is_provided(respx_mock, valid_api_key, valid_content_ids, api_response_get_contents):
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

    await client.get_contents(content_ids=valid_content_ids)

    assert combine_api_call.called


@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_user_id_provided(respx_mock, valid_api_key, valid_content_ids, api_response_get_contents):

    client = AsyncClient(api_key=valid_api_key, user_id='valid-user-id')

    combine_api_call = respx_mock.post(
        "https://api.getjoystick.com/api/v1/combine/?c=[\"cid1\", \"cid2\"]&dynamic=true",
        headers={
            'Content-Type': 'application/json',
            'x-api-key': valid_api_key
        },
        json={
            'u': 'valid-user-id',
            "p": {}
        }
    ).mock(return_value=Response(200, content=api_response_get_contents))

    await client.get_contents(content_ids=valid_content_ids)

    assert combine_api_call.called


@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_params_provided(respx_mock, valid_api_key, valid_content_ids, api_response_get_contents):

    params = {'paramKey1': 'paramValue1', 'moreComplexParam': {
        "nestingWithArrays": ["item1", True, False, None]}}
    client = AsyncClient(api_key=valid_api_key, params=params)

    combine_api_call = respx_mock.post(
        "https://api.getjoystick.com/api/v1/combine/?c=[\"cid1\", \"cid2\"]&dynamic=true",
        headers={
            'Content-Type': 'application/json',
            'x-api-key': valid_api_key
        },
        json={
            'u': '',
            "p": params
        }
    ).mock(return_value=Response(200, content=api_response_get_contents))

    await client.get_contents(content_ids=valid_content_ids)

    assert combine_api_call.called


@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_semver_provided(respx_mock, valid_api_key, valid_content_ids, api_response_get_contents):

    client = AsyncClient(api_key=valid_api_key, sem_ver='0.0.2')

    combine_api_call = respx_mock.post(
        "https://api.getjoystick.com/api/v1/combine/?c=[\"cid1\", \"cid2\"]&dynamic=true",
        headers={
            'Content-Type': 'application/json',
            'x-api-key': valid_api_key
        },
        json={
            'u': '',
            "p": {},
            'v': '0.0.2'
        }
    ).mock(return_value=Response(200, content=api_response_get_contents))

    await client.get_contents(content_ids=valid_content_ids)

    assert combine_api_call.called


@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_all_options_provided(respx_mock, valid_api_key, valid_content_ids, api_response_get_contents_serialized):

    client = AsyncClient(api_key=valid_api_key, user_id='valid user id', params={
                         'param1': 'param1value'}, sem_ver='1.20.1', serialized=True)

    combine_api_call = respx_mock.post(
        "https://api.getjoystick.com/api/v1/combine/?c=[\"cid1\", \"cid2\"]&dynamic=true&responseType=serialized",
        headers={
            'Content-Type': 'application/json',
            'x-api-key': valid_api_key
        },
        json={
            'u': 'valid user id',
            "p": {'param1': 'param1value'},
            'v': '1.20.1'
        }
    ).mock(return_value=Response(200, content=api_response_get_contents_serialized))

    await client.get_contents(content_ids=valid_content_ids)

    assert combine_api_call.called


# ! ||--------------------------------------------------------------------------------||
# ! ||                             Serialized option test                             ||
# ! ||--------------------------------------------------------------------------------||


@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_serialized_option_provided(respx_mock, valid_api_key, valid_content_ids, api_response_get_contents_serialized):

    client = AsyncClient(api_key=valid_api_key)

    combine_api_call = respx_mock.post(
        "https://api.getjoystick.com/api/v1/combine/?c=[\"cid1\", \"cid2\"]&dynamic=true&responseType=serialized",
        headers={
            'Content-Type': 'application/json',
            'x-api-key': valid_api_key
        },
        json={
            'u': '',
            "p": {}

        }
    ).mock(return_value=Response(200, content=api_response_get_contents_serialized))

    await client.get_contents(content_ids=valid_content_ids, serialized=True)

    assert combine_api_call.called


def no_serialization():
    return [

        (
            # Client level
            False,
            # Call-level
            None,
        ),
        (
            # Client level
            False,
            # Call-level
            False,
        ),
        (
            # Client level
            True,
            # Call-level
            False,
        ),
    ]


@pytest.mark.parametrize("client_serialized,call_serialized", no_serialization())
@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_no_serialization(respx_mock, valid_api_key, valid_content_ids, api_response_get_contents, client_serialized, call_serialized):

    client = AsyncClient(api_key=valid_api_key, serialized=client_serialized)

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

    response = await client.get_contents(content_ids=valid_content_ids, serialized=call_serialized)

    assert combine_api_call.called

    assert isinstance(response['cid1'], dict)
    assert isinstance(response['cid2'], dict)


def to_be_serialized():
    return [

        (
            # Client level
            False,
            # Call-level
            True,
        ),
        (
            # Client level
            True,
            # Call-level
            True,
        ),
        (
            # Client level
            True,
            # Call-level
            None,
        ),


    ]


@pytest.mark.parametrize("client_serialized,call_serialized", to_be_serialized())
@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_should_request_serialized(respx_mock, valid_api_key, valid_content_ids, api_response_get_contents_serialized, client_serialized, call_serialized):

    client = AsyncClient(api_key=valid_api_key, serialized=client_serialized)

    combine_api_call = respx_mock.post(
        "https://api.getjoystick.com/api/v1/combine/?c=[\"cid1\", \"cid2\"]&dynamic=true&responseType=serialized",
        headers={
            'Content-Type': 'application/json',
            'x-api-key': valid_api_key
        },
        json={
            'u': '',
            "p": {}
        }
    ).mock(return_value=Response(200, content=api_response_get_contents_serialized))

    response = await client.get_contents(content_ids=valid_content_ids, serialized=call_serialized)

    assert combine_api_call.called
    assert len(response['cid1']) > 0
    assert isinstance(response['cid1'], str)
    assert isinstance(json.loads(response['cid1']), dict)
    assert len(response['cid2']) > 0
    assert isinstance(response['cid2'], str)
    assert isinstance(json.loads(response['cid2']), dict)
