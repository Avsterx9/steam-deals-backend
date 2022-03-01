from fastapi.testclient import TestClient

import pytest

from nwta.v1.api import app


@pytest.fixture(scope="function")
def api_client():
    return TestClient(app)
