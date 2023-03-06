import os

from joystick import Client

joystick_api_key = os.getenv("JOYSTICK_API_KEY")

if joystick_api_key is None:
    raise ValueError("Please set JOYSTICK_API_KEY environment variable.")

client = Client(
    api_key=joystick_api_key,
)

response = client.get_contents({"cid1", "cid2"})

print(f'First content: {response["cid1"]}')
print(f'Second content: {response["cid2"]}')
