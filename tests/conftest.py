from fastapi.testclient import TestClient

import pytest

from steam_deals.v1.api import app


@pytest.fixture(scope="function")
def api_client():
    return TestClient(app)
