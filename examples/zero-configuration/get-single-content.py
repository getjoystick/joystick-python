import asyncio
import os

from joystick import AsyncClient


async def main():
    joystick_api_key = os.getenv("JOYSTICK_API_KEY")

    if joystick_api_key is None:
        raise ValueError("Please set JOYSTICK_API_KEY environment variable.")

    client = AsyncClient(
        api_key=joystick_api_key,
    )

    print(await client.get_content("cid1"))


asyncio.run(main())
