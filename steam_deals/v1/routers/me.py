import logging
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.status import HTTP_403_FORBIDDEN

from steam_deals.core import schemas
from steam_deals.core.authentication import get_current_active_user
from steam_deals.core.authentication import get_current_verified_user
from steam_deals.core.db import crud
from steam_deals.core.db.session import get_db
from steam_deals.core.utils import create_status_responses

log = logging.getLogger('steam_deals')

me_router = APIRouter()


@me_router.get(
    path='/me/info',
    response_model=schemas.UserDetailed,
    tags=['me'],
    description='Get information about the current `logged in` user.',
    responses=create_status_responses(
        {
            HTTP_401_UNAUTHORIZED: 'Problem with the `JWT token` (user does not exist / token invalid).',
            HTTP_403_FORBIDDEN: 'When a user is `inactive`.',
        },
    ),
)
def read_info_about_logged_user(user: schemas.UserDetailed = Depends(get_current_active_user)):
    return user


@me_router.get(
    path='/me/infoVerified',
    response_model=schemas.UserDetailed,
    tags=['me'],
    description='Get information about the current `logged in` user if he\'s `verified`.',
    responses=create_status_responses(
        {
            HTTP_401_UNAUTHORIZED: 'Problem with the `JWT token` (user does not exist / token invalid).',
            HTTP_403_FORBIDDEN: 'When a user is `inactive` or `not verified`.',
        },
    ),
)
def read_info_about_logged_user_if_verified(user: schemas.UserDetailed = Depends(get_current_verified_user)):
    return user


@me_router.get(
    path='/me/follows',
    response_model=List[schemas.FollowDetailed],
    tags=['me'],
    description='Get `all followed` apps by currently `logged in` user',
    responses=create_status_responses(
        {
            HTTP_401_UNAUTHORIZED: 'Problem with the `JWT token` (user does not exist / token invalid).',
            HTTP_403_FORBIDDEN: 'When a user is `inactive` or `not verified`.',
        },
    ),
)
def read_all_followed_apps_by_logged_in_user(
    db: Session = Depends(get_db), user: schemas.UserDetailed = Depends(get_current_verified_user)
):
    follows = crud.follows.get_follows_by_username(db=db, username=user.username)

    response = []
    for follow in follows:
        app = crud.apps.get_app_by_app_id(db=db, app_id=follow.steam_appid)

        app_dict = app.__dict__
        app_dict['developers'] = app_dict['developers'].split(', ')
        app_dict['publishers'] = app_dict['publishers'].split(', ')

        response.append(schemas.FollowDetailed(**follow.__dict__, app=app.__dict__))

    return response
