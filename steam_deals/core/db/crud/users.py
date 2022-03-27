from datetime import datetime
from typing import List

import pytz
from sqlalchemy.orm import Session

from steam_deals.core import models, schemas


def create_user(db: Session, user: schemas.UserIn) -> models.User:
    hashed_password = user.password + 'fakehashed'
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        timestamp=datetime.now(pytz.utc).replace(tzinfo=None),
        first_name=user.first_name,
        last_name=user.last_name,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()
