from starlette import status
from starlette.testclient import TestClient

from tests.functional.conftest import LoginUserMaker


def test_me_endpoint_successful(example_user: dict, login_user: LoginUserMaker, api_client: TestClient):
    # pylint: disable=unused-argument
    # REASON: the `login_user` argument is used indirectly - we need to login before reaching `/me` endpoint

    # ARRANGE
    url = '/me'
    login_user(verified=False)

    # ACT
    response_me = api_client.get(url=url)
    result_me = response_me.json()

    # ASSERT
    assert response_me.status_code == status.HTTP_200_OK, result_me
    assert result_me['username'] == example_user['username']
    assert result_me['email'] == example_user['email']
    assert result_me['first_name'] == example_user['first_name']
    assert result_me['last_name'] == example_user['last_name']
    assert result_me['timestamp']
    assert result_me['disabled'] is False
    assert result_me['verified'] is False


def test_me_verified_endpoint_successful(example_user: dict, login_user: LoginUserMaker, api_client: TestClient):
    # pylint: disable=unused-argument
    # REASON: the `login_user` argument is used indirectly - we need to login before reaching `/me` endpoint

    # ARRANGE
    url = '/meVerified'
    login_user(verified=True)

    # ACT
    response_me = api_client.get(url=url)
    result_me = response_me.json()

    # ASSERT
    assert response_me.status_code == status.HTTP_200_OK, result_me
    assert result_me['username'] == example_user['username']
    assert result_me['email'] == example_user['email']
    assert result_me['first_name'] == example_user['first_name']
    assert result_me['last_name'] == example_user['last_name']
    assert result_me['timestamp']
    assert result_me['disabled'] is False
    assert result_me['verified'] is True
