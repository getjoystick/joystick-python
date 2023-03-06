import asyncio
import os

from joystick import AsyncClient


async def main():
    joystick_api_key = os.getenv("JOYSTICK_API_KEY")

    if joystick_api_key is None:
        raise ValueError("Please set JOYSTICK_API_KEY environment variable.")

    client = AsyncClient(
        api_key=joystick_api_key,
        cache_expiration_seconds=60,
        serialized=True,
        params={
            "param1": "value1",
            "param2": "value2",
        },
        sem_ver="0.0.1",
        user_id="user-id-1",
    )

    print(type(await client.get_content("cid1")))


asyncio.run(main())
