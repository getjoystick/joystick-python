import pytest

from joystick._async.client import AsyncClient

VALID_API_KEY = 'valid api key'


def test_no_api_key_should_throw_exception():
    with pytest.raises(TypeError):
        client = AsyncClient()


def non_string_values():
    return [
        123,
        0.0,
        True,
        False,
        [],
        ('1', '2'),
        {'a': 'b'},
        {'1'}
    ]


@pytest.mark.parametrize("non_string_value", [*non_string_values(), ''])
def test_api_key_should_be_string(non_string_value):
    with pytest.raises(TypeError):
        client = AsyncClient(api_key=non_string_value)


# PARAMS
def test_set_param_value_before_setting_params():
    client = AsyncClient(api_key=VALID_API_KEY)
    client.params['param'] = 'value'

    assert client.params['param'] == 'value'


def test_set_param_value_after_setting_params():
    client = AsyncClient(api_key=VALID_API_KEY)
    client.params = {
        'param_first': 'value_first'
    }
    client.params['param_second'] = 'value_second'

    assert client.params['param_first'] == 'value_first'
    assert client.params['param_second'] == 'value_second'


def wrong_params():
    return [
        [],
        '123',
        1234,
        ['asd', 'dsa'],
    ]


@pytest.mark.parametrize("wrong_param", wrong_params())
def test_exception_should_be_thrown_on_wrong_params(wrong_param):
    client = AsyncClient(api_key=VALID_API_KEY)
    with pytest.raises(ValueError):
        client.params = wrong_param


def valid_params():
    return [
        # Simple case
        {'asd': 'dsa'},
        # Complex structures like lists
        {'asd': ['first', 'second']},
        # Nested objects
        {'first_level': {
            'second_level': {'third_level': 'value'}
        }}
    ]


@pytest.mark.parametrize("valid_params", valid_params())
def test_valid_params_via_constructor(valid_params):
    client = AsyncClient(api_key=VALID_API_KEY, params=valid_params)
    assert client.params == valid_params


@pytest.mark.parametrize("valid_params", valid_params())
def test_valid_params_via_setter(valid_params):
    client = AsyncClient(api_key=VALID_API_KEY, params=valid_params)
    client.params = valid_params
    assert client.params == valid_params


# SEMVER


def valid_semvers():
    return [
        '0.0.1',
        '0.1.1',
        '1.0.1',
        '1.2.2',
        '10.20.30',
    ]


@pytest.mark.parametrize("valid_sem_ver", valid_semvers())
def test_valid_semver_via_constructor(valid_sem_ver):
    client = AsyncClient(api_key=VALID_API_KEY)
    client.sem_ver = valid_sem_ver
    assert client.sem_ver == valid_sem_ver


@pytest.mark.parametrize("valid_sem_ver", valid_semvers())
def test_valid_semver_via_setter(valid_sem_ver):
    client = AsyncClient(api_key=VALID_API_KEY, sem_ver=valid_sem_ver)

    assert client.sem_ver == valid_sem_ver


def invalid_semvers():
    return ['0.0.0-prerelease', '0.0.1-beta', '1.0.-1', '1.-2.2', '-1.20.30', '1.00.00', '01.02.03']


@pytest.mark.parametrize("invalid_sem_ver", invalid_semvers())
def test_valid_semver_via_constructor(invalid_sem_ver):
    with pytest.raises(ValueError):
        AsyncClient(api_key=VALID_API_KEY, sem_ver=invalid_sem_ver)


@pytest.mark.parametrize("invalid_sem_ver", [*invalid_semvers(), *non_string_values()])
def test_valid_semver_via_setter(invalid_sem_ver):
    client = AsyncClient(api_key=VALID_API_KEY)
    with pytest.raises(ValueError):
        client.sem_ver = invalid_sem_ver


# EXPIRATION SECONDS

def wrong_expiration_seconds():
    return [-1, 1.1, '123', [], {}]


@pytest.mark.parametrize("expiration_seconds", wrong_expiration_seconds())
def test_wrong_cache_expiration_seconds_in_constructor(expiration_seconds):
    with pytest.raises(ValueError):
        AsyncClient(api_key=VALID_API_KEY, cache_expiration_seconds=expiration_seconds)


@pytest.mark.parametrize("expiration_seconds", wrong_expiration_seconds())
def test_wrong_cache_expiration_seconds_in_setter(expiration_seconds):
    client = AsyncClient(api_key=VALID_API_KEY)
    with pytest.raises(ValueError):
        client.cache_expiration_seconds = expiration_seconds
