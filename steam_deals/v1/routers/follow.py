import logging
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.status import HTTP_403_FORBIDDEN
from starlette.status import HTTP_404_NOT_FOUND

from steam_deals.core import apps
from steam_deals.core import schemas
from steam_deals.core.authentication import get_current_verified_user
from steam_deals.core.db import crud
from steam_deals.core.db.session import get_db
from steam_deals.core.exception import HTTPException
from steam_deals.core.utils import create_status_responses

log = logging.getLogger('steam_deals')

follows_router = APIRouter()


@follows_router.put(
    path='/follows/{app_id}',
    tags=['follows'],
    description='Follow app specified by `app_id`. When there is no `price_target`, the notification will not be sent.',
    responses=create_status_responses(
        {
            HTTP_401_UNAUTHORIZED: 'Problem with the `JWT token` (user does not exist / token invalid).',
            HTTP_403_FORBIDDEN: 'When a user is `inactive` or `not verified`.',
            HTTP_404_NOT_FOUND: 'When `no app` with the given `app_id` was found.',
        }
    ),
)
def follow_app(
    app_id: int,
    price_target: Optional[float] = None,
    notification: Optional[bool] = None,
    db: Session = Depends(get_db),
    user: schemas.UserDetailed = Depends(get_current_verified_user),
):
    # pylint: disable=unused-argument

    app = crud.apps.get_app_by_app_id(db=db, app_id=app_id)

    if not app:
        app_schema = apps.get_base_app(app_id=app_id)

        if not app_schema:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'App with app_id {app_id} was not found.')

        app = crud.apps.create_app(db=db, app=app_schema)

    follow_schema = schemas.FollowBase(
        username=user.username,
        steam_appid=app.steam_appid,
        price_target=price_target,
        notification=notification,
    )

    return crud.follows.create_or_update_follow(db=db, follow=follow_schema)
