from contextvars import ContextVar
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from steam_deals.config import settings

connect_args = {"connect_args": {"check_same_thread": False}} if settings.DATABASE_URL.startswith('sqlite') else {}

engine = create_engine(url=settings.DATABASE_URL, **connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_session: ContextVar[Session] = ContextVar('db_session')
