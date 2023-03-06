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

    response = await client.get_contents({"cid1", "cid2"})

    print(f'First content: {response["cid1"]}')
    print(f'Second content: {response["cid2"]}')


asyncio.run(main())
