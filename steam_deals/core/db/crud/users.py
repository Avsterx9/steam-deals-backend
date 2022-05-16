from datetime import datetime
from typing import List

import pytz
from sqlalchemy.orm import Session

from steam_deals.core import models
from steam_deals.core import schemas
from steam_deals.core import security
from steam_deals.core.schemas import UserDetailed


def create_user(db: Session, user: schemas.UserIn) -> models.User:
    hashed_password = security.get_password_hash(plain_password=user.password)
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


def update_user(db: Session, user: UserDetailed) -> models.User:
    db_user = get_user_by_username(db=db, username=user.username)

    for var, value in vars(user).items():
        if value is not None:
            setattr(db_user, var, value)

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


def get_users_with_filtering(db: Session, params: dict, skip: int = 0, limit: int = 100) -> List[models.User]:
    users = db.query(models.User)
    for key, value in params.items():
        if isinstance(value, str):
            users = users.filter(getattr(models.User, key).like(value))
            continue
        users = users.filter(getattr(models.User, key) == value)

    users = users.offset(skip).limit(limit)
    return users.all()
