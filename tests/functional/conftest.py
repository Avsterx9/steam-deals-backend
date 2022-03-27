import pytest
from requests import Response
from starlette import status
from starlette.testclient import TestClient


@pytest.fixture(name='example_user', scope='session')
def fixture_example_user() -> dict:
    return {
        'username': 'johndoe',
        'email': 'john@doe.com',
        'password': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
    }


@pytest.fixture(name='register_user')
def fixture_register_user(example_user: dict, api_client: TestClient) -> Response:
    # ARRANGE
    url = '/users'

    # ACT
    response = api_client.post(url=url, json=example_user)
    result = response.json()

    # ASSERT
    assert response.status_code == status.HTTP_200_OK, result
    assert result['username'] == 'johndoe'
    assert result['email'] == 'john@doe.com'
    assert result['first_name'] == 'John'
    assert result['last_name'] == 'Doe'
    return response


@pytest.fixture(name='login_user')
def fixture_login_user(register_user: Response, api_client: TestClient) -> Response:
    # ARRANGE
    url = '/token'
    response_register = register_user
    result_register = response_register.json()

    form_data = {
        'username': result_register['username'],
        'password': result_register['username'],
    }

    # ACT
    response_login = api_client.post(url=url, data=form_data)
    result_login = response_login.json()

    # ASSERT
    assert response_login.status_code == status.HTTP_200_OK, result_login
    assert result_login['access_token']
    assert result_login['token_type'] == 'bearer'
    return response_login
