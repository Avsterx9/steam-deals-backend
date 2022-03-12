from fastapi import status

import git

from steam_deals.config import settings


def test_connection(api_client):
    # ACT
    response = api_client.get('/')

    # ASSERT
    assert response.status_code == status.HTTP_200_OK


def test_index(api_client, index_response):
    # ARRANGE
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    # ACT
    response = api_client.get('/')
    result = response.json()

    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    assert result in [index_response(version=sha), index_response(version='UNCOMMITTED')]


def test_cors_header(api_client):
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
