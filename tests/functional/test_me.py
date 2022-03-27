from requests import Response
from starlette import status
from starlette.testclient import TestClient


def test_me_endpoint_successful(example_user: dict, login_user: Response, api_client: TestClient):
    # ARRANGE
    url = '/me'

    response_login = login_user
    result_login = response_login.json()
    headers = {'Authorization': f'Bearer {result_login["access_token"]}'}

    # ACT
    response_me = api_client.get(url=url, headers=headers)
    result_me = response_me.json()

    # ASSERT
    assert response_me.status_code == status.HTTP_200_OK, result_me
    assert result_me['username'] == example_user['username']
    assert result_me['email'] == example_user['email']
    assert result_me['first_name'] == example_user['first_name']
    assert result_me['last_name'] == example_user['last_name']
    assert result_me['timestamp']
    assert result_me['disabled'] is False
