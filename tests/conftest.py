import os
from typing import Final
from typing import Protocol

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from steam_deals.config import ENV_SWITCHER
from steam_deals.config import settings
from steam_deals.core import schemas
from steam_deals.core.db.base_class import Base
from steam_deals.core.db.session import get_db
from steam_deals.v1.api import add_cors_middleware
from steam_deals.v1.api import app

API_BASE_URL: Final[str] = '/api/v1'


@pytest.fixture(name='_set_test_settings', scope='session', autouse=True)
def _fixture_set_test_settings() -> None:
    os.environ[ENV_SWITCHER] = "testing"
    settings.reload()


@pytest.fixture(name='_session')
def _fixture_session() -> Session:
    engine = create_engine(settings.DATABASE_URL, connect_args={'check_same_thread': False})

    Base.metadata.create_all(bind=engine)
    SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # pylint: disable=invalid-name

    yield SessionTesting()

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(name='api_client')
def fixture_api_client(_session: Session) -> TestClient:
    # because middleware gets variables from `steam_deals.config.settings` and is actually added when the
    # `from steam_deals.v1.api import app` is done - has to be added again after settings.reload()
    add_cors_middleware(app)

    def _get_db_override():
        return _session

    app.dependency_overrides[get_db] = _get_db_override
    return TestClient(app)


class IndexResponseMaker(Protocol):
    def __call__(self, version: str) -> schemas.Index:
        pass


@pytest.fixture(name='index_response')
def fixture_index_response() -> IndexResponseMaker:  # remove err: "'Index' object is not callable" when type-hinting
    def _index_response(version: str) -> schemas.Index:
        return schemas.Index(version=version)

    return _index_response
