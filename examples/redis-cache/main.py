import os
import time
import uuid

from aiohttp import web
from redis_cache import RedisCache

from joystick import AsyncClient

REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
REDIS_PORT = int(os.getenv("REDIS_PORT") or "6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or "CbwK98r6JMpo"
JOYSTICK_API_KEY = os.getenv("JOYSTICK_API_KEY") or ""
JOYSTICK_CONFIG_ID = os.getenv("JOYSTICK_CONFIG_ID") or ""
SERVER_ID = str(uuid.uuid4())


async def make_measured_call(func):
    start_time = time.perf_counter()

    response = await func()

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    return (response, execution_time)


redis_cache = RedisCache(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)


client = AsyncClient(
    api_key=JOYSTICK_API_KEY, cache=redis_cache, cache_expiration_seconds=10
)

routes = web.RouteTableDef()


@routes.get("/")
async def get_config(request):
    print("Making request for Joystick config id: ", JOYSTICK_CONFIG_ID)

    response, execution_time = await make_measured_call(
        lambda: client.get_content(JOYSTICK_CONFIG_ID)
    )
    return web.json_response(
        {"response": response, "execution_time": execution_time, "server_id": SERVER_ID}
    )


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=8000)
