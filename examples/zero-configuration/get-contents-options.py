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

    full_response_true_option = await client.get_contents({"cid1"}, full_response=True)
    print(f"Full response with full_response=True option: {full_response_true_option}")

    serialized_true_option = await client.get_contents({"cid1"}, serialized=True)
    print(f"Serialized response with serialized=True option: {serialized_true_option}")


asyncio.run(main())
