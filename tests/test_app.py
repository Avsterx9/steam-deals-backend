from fastapi import status

import git


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
