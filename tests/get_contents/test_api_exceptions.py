

from httpx import Response
import respx
import pytest

from joystick._async.client import AsyncClient
from joystick.errors.api import BadRequestError, MultipleContentsApiError, ServerError

import json


from .fixtures import api_response_get_contents, api_response_get_contents_serialized, valid_content_ids, valid_api_key


# ! ||--------------------------------------------------------------------------------||
# ! ||                                  API Exceptions                                ||
# ! ||--------------------------------------------------------------------------------||


def valid_response_with_errors():
    return [
        {
            "cid1": "Error 404,  https://api.getjoystick.com/api/v1/config/cid1/dynamic?responsetype=serialized {\"data\":null,\"status\":2,\"message\":null,\"details\":null}.",
            "cid2": {
                "data": "{\"title\":\"Simple data for unit testings\",\"description\":\"This is config which will be used during unit tests to use a sample of Joystick API response\",\"created\":{\"at\":\"2023-03-28T12:05:44.524Z\",\"by\":\"Joystick developers\"},\"contentId\":\"cid2\"}",
                "hash": "2418a36d",
                "meta": {
                    "uid": 0,
                    "mod": 0,
                    "variants": [],
                    "seg": []
                }
            }
        },
        {
            "cid1": "Error 404,  https://api.getjoystick.com/api/v1/config/cid1/dynamic?responsetype=serialized {\"data\":null,\"status\":2,\"message\":null,\"details\":null}.",
            "cid2": "Error 404,  https://api.getjoystick.com/api/v1/config/cid2/dynamic?responsetype=serialized {\"data\":null,\"status\":2,\"message\":null,\"details\":null}.",
        },
    ]


@pytest.mark.parametrize("api_response_json", valid_response_with_errors())
@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_valid_errors_in_content(respx_mock, valid_api_key, valid_content_ids, api_response_json):
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
    ).mock(return_value=Response(200, content=json.dumps(api_response_json)))

    with pytest.raises(MultipleContentsApiError):
        await client.get_contents(content_ids=valid_content_ids)

    assert combine_api_call.called


def four_xx_status_codes():
    return [
        400,
        401,
        403,
        404,
        405,
    ]


@pytest.mark.parametrize("status_code", four_xx_status_codes())
@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_4xx_status_code(respx_mock, valid_api_key, valid_content_ids, status_code):
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
    ).mock(return_value=Response(status_code))

    with pytest.raises(BadRequestError):
        await client.get_contents(content_ids=valid_content_ids)

    assert combine_api_call.called


def five_xx_status_codes():
    return [
        500,
        501,
        502,
        503,
        504,
    ]


@pytest.mark.parametrize("status_code", five_xx_status_codes())
@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_5xx_status_code(respx_mock, valid_api_key, valid_content_ids, status_code):
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
    ).mock(return_value=Response(status_code))

    with pytest.raises(ServerError):
        await client.get_contents(content_ids=valid_content_ids)

    assert combine_api_call.called


@pytest.mark.asyncio
@pytest.mark.respx()
async def test_get_contents_wrong_json_returned(respx_mock, valid_api_key, valid_content_ids, api_response_get_contents):
    client = AsyncClient(api_key=valid_api_key)

    malformed_json = api_response_get_contents[:-1]

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

    ).mock(return_value=Response(200, content=malformed_json))

    with pytest.raises(json.decoder.JSONDecodeError):
        await client.get_contents(content_ids=valid_content_ids)

    assert combine_api_call.called
