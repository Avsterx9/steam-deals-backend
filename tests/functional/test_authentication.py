from typing import Optional

import pytest
from requests import Response
from starlette import status
from starlette.testclient import TestClient


def _build_detail(*args: Optional[dict]) -> list:
    detail = []
    for arg in args:
        key, value = list(arg.items())[0]
        if not value:
            detail.append({'loc': ['body', key], 'msg': 'field required', 'type': 'value_error.missing'})

    return detail


def test_login_for_access_token_successful(api_client: TestClient, register_user: Response):
    # ARRANGE
    url = '/token/'

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
    username: str, password: str, api_client: TestClient, register_user: Response
):
    # pylint: disable=unused-variable
    # REASON: `result_register` is used indirectly by pytest parametrize parameters

    # ARRANGE
    url = '/token'

    response_register = register_user
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
