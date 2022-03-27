import pytest
from requests import Response
from starlette import status
from starlette.testclient import TestClient


@pytest.fixture()
def register_user(api_client: TestClient) -> Response:
    # ARRANGE
    url = '/users'
    body = {
        'username': 'johndoe',
        'email': 'john@doe.com',
        'password': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
    }
    # ACT
    response = api_client.post(url=url, json=body)
    result = response.json()

    # ASSERT
    assert response.status_code == status.HTTP_200_OK, result
    assert result['username'] == 'johndoe'
    assert result['email'] == 'john@doe.com'
    assert result['first_name'] == 'John'
    assert result['last_name'] == 'Doe'
    return response
