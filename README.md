# Pythong client for [Joystick](https://www.getjoystick.com/)

[![GitHub Actions](https://github.com/getjoystick/joystick-python/actions/workflows/on-publishing.yml/badge.svg)](<(https://github.com/getjoystick/joystick-python/actions?query=branch%3Amain)>)
[![Latest Stable Version](https://img.shields.io/pypi/v/joystick-python.svg)](https://pypi.org/project/joystick-python)
[![PyPI Wheel](https://img.shields.io/pypi/wheel/joystick-python.svg)](https://pypi.org/project/joystick-python)
[![Supported versions](https://img.shields.io/pypi/pyversions/joystick-python.svg)](https://pypi.org/project/joystick-python)
[![Supported implementations](https://img.shields.io/pypi/implementation/joystick-python.svg)](https://pypi.org/project/joystick-python)
[![License](https://img.shields.io/pypi/l/joystick-python.svg)](https://pypi.org/project/joystick-python)

This is the library that simplifies the way how you can communicate with [Joystick API](https://docs.getjoystick.com/).

## Installation

You can install the package via [Pip](https://pip.pypa.io/en/stable/installation/):

```bash
pip install joystick-python
```

## Usage

We provide two types of clients: asynchronous and synchronous. They have exactly the same interfaces,
the only difference is a way you import them.

### Async / Sync

#### Sync

```python
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
```

#### Async

```python
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

```

> All examples below will be provided for `async` version of the client. For sync it's enough to
> use proper Client and avoid `await` keyword

### Requesting content by single Content Id

```python
...
await client.get_content('cid1')
...
```

### Specifying additional parameter

When creating the `Client`/`AsyncClient` instance, you can specify additional parameters which will
be used by all API calls from the client, for more details see
[API documentation](https://docs.getjoystick.com/api-reference/):

```python
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
```

### Options

#### `full_response`

In most of the cases you will be not interested in the full response from the API, but if you're you can specify
`fullResponse` option to the client methods. The client will return you raw API response:

```python
get_content_response = await client.get_content('cid1', full_response=True)
# OR
get_contents_response = await client.get_contents({'cid1'}  , full_response=True)
```

#### `serialized`

When `true`, we will pass query parameter `responseType=serialized`
to [Joystick API](https://docs.getjoystick.com/api-reference-combine/).

```python
get_content_response = await client.get_content('cid1', serialized=True)
# OR
get_contents_response = await client.get_contents({'cid1'}  , serialized=True)
```

This option can be set for every API call from the client by setting `serialized` as `true` via
constructor, or via propert setter.

```python
client = AsyncClient(
    api_key=joystick_api_key,
    serialized=True,
)
```

#### `refresh`

If you want to ignore existing cache and request the new config – pass this option as `true`.

```python
get_content_response = await client.get_content('cid1', refresh=True)
# OR
get_contents_response = await client.get_contents({'cid1'}  , refresh=True)
```

### Caching

By default, the client uses [in-memory caching](./src/joystick/_async/cache/in_memory.py),
which means that if you build the distributed application, every instance will go to the Joystick
API for at least first call and the cache will be erased after the application is closed.

You can specify your cache implementation which implements either
[`AsyncCacheInterface`](./src/joystick/_async/cache/cache.py) if you use `AsyncClient`,
or [`SyncCacheInterface`](./src/joystick/_sync/cache/cache.py) if you use `SyncClient`.

### Async support

We rely on library [`httpx`](https://www.python-httpx.org/) to make requests to Joystick API and we
support the [same platforms as `httpx`](https://www.python-httpx.org/async/#supported-async-environments).

#### Clear the cache

If you want to clear the cache – run `await client.clear_cache()`.

## Library development

We use the `pyenv` to install multiple versions of Python on the developer's machine and `venv` to create the virtual environment for these versions:

```bash
pyenv global 3.5.10
rm -rf ./venv # This one might fail, if it's the first time you create `venv` in this proj.
python3 -m venv venv
source ./venv/bin/activate
pip install -e '.[dev]'
```

### Run unit tests

```bash
nox -e test
```

### Very code style and format

```bash
nox -e format
```