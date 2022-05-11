from typing import List

from sqlalchemy.orm import Session

from steam_deals.core import models
from steam_deals.core import schemas


def create_follow(db: Session, follow: schemas.FollowIn) -> models.Follow:
    db_follow = models.Follow(
        username=follow.username,
        steam_appid=follow.steam_appid,
        price_target=follow.price_target,
        notification=follow.notification,
    )

    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow


def update_follow(db: Session, follow: schemas.FollowIn) -> models.Follow:
    db_follow = get_follow_by_username_and_app_id(db=db, username=follow.username, app_id=follow.steam_appid)

    for var, value in vars(follow).items():
        if value is not None:
            setattr(db_follow, var, value)

    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow


def create_or_update_follow(db: Session, follow: schemas.FollowIn) -> models.Follow:
    db_follow = get_follow_by_username_and_app_id(db=db, username=follow.username, app_id=follow.steam_appid)
    return update_follow(db=db, follow=follow) if db_follow else create_follow(db=db, follow=follow)


def get_follow_by_username_and_app_id(db: Session, username: str, app_id: int) -> models.Follow:
    return db.query(models.Follow).get((username, app_id))


def get_follows_by_app_id(db: Session, app_id: int) -> List[models.Follow]:
    return db.query(models.Follow).filter(models.Follow.steam_appid == app_id).all()


def get_follows_by_username(db: Session, username: str) -> List[models.Follow]:
    return db.query(models.Follow).filter(models.Follow.username == username).all()
