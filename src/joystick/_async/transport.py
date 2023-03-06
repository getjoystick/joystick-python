import typing as t

import httpx

from joystick.errors import BadRequestError
from joystick.errors import ServerError
from joystick.errors import UnknownError
from joystick.errors.api import ApiHttpError


class AsyncTransport:
    def __init__(self, api_key: str):
        self.__client = httpx.AsyncClient()
        self.__api_key = api_key

    async def make_request(
        self, http_method: str, url: str, body: t.Optional[t.Any]
    ) -> t.Any:
        # callable: t.Optional[(url: str): t.Coroutine[t.Any, t.Any, httpx.Response]] = None
        if http_method == "POST":
            callable = self.__client.post
        elif http_method == "PUT":
            callable = self.__client.put
        else:
            raise AssertionError("Invalid HTTP method is provided")

        headers = {
            "x-api-key": self.__api_key,
            "Content-Type": "application/json",
        }

        response = await callable(url=url, json=body, headers=headers)

        if response.status_code != 200:
            raise self.map_response_to_error(response)

        return response.json()

    def map_response_to_error(self, response: httpx.Response) -> ApiHttpError:
        status_code = response.status_code

        error_message = (
            f"Joystick returned status code {status_code} (body: {response.text})"
        )

        if status_code >= 400 and status_code < 500:
            return BadRequestError(error_message)
        elif status_code >= 500:
            return ServerError(error_message)
        else:
            return UnknownError(error_message)
