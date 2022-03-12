import os
from typing import Protocol

from fastapi.testclient import TestClient
import pytest

# This next line ensures tests uses its own database and settings environment
os.environ['FORCE_ENV_FOR_DYNACONF'] = 'testing'
# pylint: disable=wrong-import-position
# WARNING: Ensure imports from `steam_deals` comes after this line

from steam_deals.core import schemas  # noqa
from steam_deals.v1.api import app  # noqa


@pytest.fixture()
def api_client() -> TestClient:
    return TestClient(app)


class IndexResponseMaker(Protocol):
    def __call__(self, version: str) -> schemas.Index:
        pass


@pytest.fixture()
def index_response() -> IndexResponseMaker:
    def _index_response(version: str) -> schemas.Index:
        return schemas.Index(version=version)

    return _index_response
