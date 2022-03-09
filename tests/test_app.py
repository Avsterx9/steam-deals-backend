from http import HTTPStatus


def test_index(api_client):
    # ACT
    response = api_client.get('/')
    result = response.json()
    # ASSERT
    assert response.status_code == HTTPStatus.OK
    assert result['description'] == "This is a steam-deals project API"
