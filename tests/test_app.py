from fastapi import status
import git
from starlette.testclient import TestClient

from steam_deals.config import settings
from tests.conftest import IndexResponseMaker


def test_if_test_settings():
    # settings.toml
    assert settings.ENV_FOR_DYNACONF == 'testing'
    assert settings.PORT == 5556
    assert settings.DATABASE_URL.startswith('sqlite')

    # .secrets.toml
    assert settings.SECRET_KEY == 'your_secret_key'


def test_api_connection(api_client: TestClient):
    # ACT
    response = api_client.get('/')

    # ASSERT
    assert response.status_code == status.HTTP_200_OK


def test_index(api_client: TestClient, index_response: IndexResponseMaker):
    # ARRANGE
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    # ACT
    response = api_client.get('/')
    result = response.json()

    # ASSERT
    assert response.status_code == status.HTTP_200_OK, result
    assert result in [index_response(version=sha), index_response(version='UNCOMMITTED')]


def test_cors_header(api_client: TestClient):
    # ARRANGE
    valid_origins = settings.ALLOW_ORIGINS
    invalid_origins = ['http://localhost:3201', 'http://localhost:4001']

    # ACT
    valid_responses = [api_client.get('/', headers={'Origin': origin}) for origin in valid_origins]
    invalid_responses = [api_client.get('/', headers={'Origin': origin}) for origin in invalid_origins]

    # ASSERT
    for response, origin in zip(valid_responses, valid_origins):
        assert response.headers.get('access-control-allow-origin') == origin

    for response in invalid_responses:
        assert response.headers.get('access-control-allow-origin') is None
