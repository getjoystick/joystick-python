import pytest
import json


@pytest.fixture
def valid_content_ids():
    return {'cid1', 'cid2'}


@pytest.fixture
def valid_api_key():
    return 'valid-api-key'


@pytest.fixture
def api_response_get_contents():
    return json.dumps({
        "cid1": {
            "data": {
                "title": "Simple data for unit testings",
                "description": "This is config which will be used during unit tests to use a sample of Joystick API response",
                "created": {
                    "at": "2023-03-28T12:05:44.524Z",
                    "by": "Joystick developers"
                },
                "contentId": "cid1"
            },
            "hash": "e6ffe854",
            "meta": {
                "uid": 0,
                "mod": 0,
                "variants": [],
                "seg": []
            }
        },
        "cid2": {
            "data": {
                "title": "Simple data for unit testings",
                "description": "This is config which will be used during unit tests to use a sample of Joystick API response",
                "created": {
                    "at": "2023-03-28T12:05:44.524Z",
                    "by": "Joystick developers"
                },
                "contentId": "cid2"
            },
            "hash": "2418a36d",
            "meta": {
                "uid": 0,
                "mod": 0,
                "variants": [],
                "seg": []
            }
        }
    })


@pytest.fixture
def api_response_get_contents_cache_key():
    return '90932fd045eaa8cb5ca601dd046fdaf9a13d323751010f1c3e5ef304d67fff75'


@pytest.fixture
def api_response_get_contents_serialized():
    return json.dumps({
        "cid1": {
            "data": "{\"title\":\"Simple data for unit testings\",\"description\":\"This is config which will be used during unit tests to use a sample of Joystick API response\",\"created\":{\"at\":\"2023-03-28T12:05:44.524Z\",\"by\":\"Joystick developers\"},\"contentId\":\"cid1\"}",
            "hash": "e6ffe854",
            "meta": {
                "uid": 0,
                "mod": 0,
                "variants": [],
                "seg": []
            }
        },
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
    })
