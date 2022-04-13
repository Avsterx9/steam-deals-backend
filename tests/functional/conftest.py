from typing import Protocol

import pytest
from requests import Response
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from steam_deals.core import schemas, verification
from steam_deals.core.db import crud
from tests.conftest import API_BASE_URL


@pytest.fixture(name='example_user', scope='session')
def fixture_example_user() -> dict:
    return {
        'username': 'johndoe',
        'email': 'john@doe.com',
        'password': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
    }


class RegisterUserMaker(Protocol):
    def __call__(self, verified: bool = True) -> Response:
        pass


@pytest.fixture(name='register_user')
def fixture_register_user(example_user: dict, api_client: TestClient, monkeypatch) -> RegisterUserMaker:
    def _register_user(verified: bool = True) -> Response:
        # ARRANGE
        url = f'{API_BASE_URL}/users'

        # make user verified or not - for tests, depending on the fixture parameter
        async def _verify_user(db: Session, user: schemas.UserDetailed):
            user.verified = verified
            crud.users.update_user(db=db, user=user)

        monkeypatch.setattr(verification, 'verify_user', _verify_user)

        # ACT
        response = api_client.post(url=url, json=example_user)
        result = response.json()

        # ASSERT
        assert response.status_code == status.HTTP_200_OK, result
        assert result['username'] == 'johndoe'
        assert result['email'] == 'john@doe.com'
        assert result['first_name'] == 'John'
        assert result['last_name'] == 'Doe'
        assert result['disabled'] is False
        assert result['admin'] is False
        assert result['verified'] is verified
        return response

    return _register_user


class LoginUserMaker(Protocol):
    def __call__(self, verified: bool = True) -> Response:
        pass


@pytest.fixture(name='login_user')
def fixture_login_user(register_user: RegisterUserMaker, api_client: TestClient) -> LoginUserMaker:
    def _login_user(verified: bool = True) -> Response:
        # ARRANGE
        url = f'{API_BASE_URL}/token'
        response_register = register_user(verified=verified)
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

    return _login_user
