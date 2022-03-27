from typing import Protocol

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from steam_deals.config import settings
from steam_deals.core import schemas
from steam_deals.core.db.base_class import Base
from steam_deals.core.db.session import get_db
from steam_deals.v1.api import app


@pytest.fixture(scope='session', autouse=True)
def _set_test_settings() -> None:
    settings.configure(ENV_FOR_DYNACONF='testing')


@pytest.fixture()
def _session() -> Session:
    engine = create_engine(settings.DATABASE_URL, connect_args={'check_same_thread': False})

    Base.metadata.create_all(bind=engine)
    SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # pylint: disable=invalid-name

    yield SessionTesting()

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def api_client(_session) -> TestClient:
    def _get_db_override():
        return _session

    app.dependency_overrides[get_db] = _get_db_override
    return TestClient(app)


class IndexResponseMaker(Protocol):
    def __call__(self, version: str) -> schemas.Index:
        pass


@pytest.fixture()
def index_response() -> IndexResponseMaker:  # remove err: "'Index' object is not callable" when type-hinting 'Index'
    def _index_response(version: str) -> schemas.Index:
        return schemas.Index(version=version)

    return _index_response
