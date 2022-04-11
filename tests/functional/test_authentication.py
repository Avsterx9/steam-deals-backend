from typing import Optional

import pytest
from requests import Response
from starlette import status
from starlette.testclient import TestClient

from tests.functional.conftest import LoginUserMaker, RegisterUserMaker


def _build_detail(*args: Optional[dict]) -> list:
    detail = []
    for arg in args:
        key, value = list(arg.items())[0]
        if not value:
            detail.append({'loc': ['body', key], 'msg': 'field required', 'type': 'value_error.missing'})

    return detail


def test_login_for_access_token_successful(login_user: Response):
    # pylint: disable=unused-argument
    # REASON: `login_user` is a fixture that logs the example user in, need to test it as well
    pass


@pytest.mark.parametrize(
    ('username', 'password'),
    [
        ('str("incorrect_username")', 'str("doesnt_matter")'),
        ('result_register["username"]', 'str("wrong_password")'),
    ],
    ids=[
        'incorrect username',
        'correct username, wrong password',
    ],
)
def test_login_for_access_token_credentials_incorrect(
    username: str, password: str, api_client: TestClient, register_user: RegisterUserMaker
):
    # pylint: disable=unused-variable
    # REASON: `result_register` is used indirectly by pytest parametrize parameters

    # ARRANGE
    url = '/token'

    response_register = register_user()
    result_register = response_register.json()

    form_data = {
        'username': eval(username),
        'password': eval(password),
    }

    # ACT
    response_login = api_client.post(url=url, data=form_data)
    result_login = response_login.json()

    # ASSERT
    assert response_login.status_code == status.HTTP_401_UNAUTHORIZED
    assert result_login['status_code'] == 401, result_login
    assert result_login['phrase'] == 'Unauthorized'
    assert result_login['detail'] == 'Incorrect username or password'


@pytest.mark.parametrize(
    ('username_dict', 'password_dict'),
    [
        ({'username': None}, {'password': 'doesnt_matter'}),
        ({'username': 'doesnt_matter'}, {'password': None}),
        ({'username': None}, {'password': None}),
    ],
    ids=[
        'missing username',
        'missing password',
        'missing username and password',
    ],
)
def test_login_for_access_token_credentials_missing(
    username_dict: Optional[dict], password_dict: Optional[dict], api_client: TestClient
):
    # ARRANGE
    url = '/token'
    form_data = {**username_dict, **password_dict}

    # ACT
    response_login = api_client.post(url=url, data=form_data)
    result_login = response_login.json()

    # ASSERT
    assert response_login.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, result_login
    assert result_login == {'detail': _build_detail(username_dict, password_dict)}


@pytest.mark.parametrize('by_header', [False, True], ids=['using HttpOnly cookie', 'using Authorization header'])
def test_authentication_methods(by_header: bool, login_user: LoginUserMaker, api_client: TestClient):
    # ARRANGE
    url = '/me'
    logout_url = '/logout'
    headers = None

    response_login = login_user()

    if by_header:
        result_login = response_login.json()
        api_client.post(url=logout_url)  # deleting HttpOnly cookie to test if authorization by header works also
        headers = {'Authorization': f'Bearer {result_login["access_token"]}'}

    # ACT
    response_me = api_client.get(url=url, headers=headers)
    result_me = response_me.json()

    # ASSERT
    assert response_me.status_code == status.HTTP_200_OK, result_me
