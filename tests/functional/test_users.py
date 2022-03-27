import pytest
from starlette import status
from starlette.testclient import TestClient


def test_create_user(register_user):
    # pylint: disable=unused-argument
    # REASON: `register_user` is a fixture that registers one, example user, need to test it as well
    pass


@pytest.mark.parametrize('key', ['username', 'email', 'password', 'first_name', 'last_name'])
def test_create_user_without_key(api_client: TestClient, key: str):
    # ARRANGE
    url = '/users'
    body = {
        'username': 'doesnt_matter',
        'email': 'doesnt@matter.com',
        'password': 'doesnt_matter',
        'first_name': 'doesnt_matter',
        'last_name': 'doesnt_matter',
    }

    body.pop(key)

    # ACT
    response = api_client.post(url=url, json=body)
    result = response.json()

    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert result == {'detail': [{'loc': ['body', key], 'msg': 'field required', 'type': 'value_error.missing'}]}
