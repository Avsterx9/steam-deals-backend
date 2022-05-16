from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_409_CONFLICT

from steam_deals.core import schemas
from steam_deals.core import verification
from steam_deals.core.db import crud
from steam_deals.core.db.session import get_db
from steam_deals.core.exception import HTTPException
from steam_deals.core.utils import create_status_responses

users_router = APIRouter()


@users_router.post(
    path='/users',
    response_model=schemas.UserDetailed,
    tags=['users'],
    description='Used to create a `new` user.',
    responses=create_status_responses(
        {HTTP_409_CONFLICT: 'When the given `username` / `email address` is already taken.'}
    ),
)
async def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    if crud.users.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=f'Email `{user.email}` is already taken')
    if crud.users.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=f'Username `{user.username}` is already taken')

    user = crud.users.create_user(db=db, user=user)
    await verification.verify_user(db=db, user=user)
    return user


@users_router.get(
    path='/users/{username}',
    response_model=schemas.UserPublic,
    tags=['users'],
    description='Get info about the registered user with the provided `username`.',
    responses=create_status_responses({HTTP_404_NOT_FOUND: 'When a user with the given username was `not found`.'}),
)
def read_user(username: str, db: Session = Depends(get_db)):
    user = crud.users.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'User with username `{username}` was not found')
    return user


@users_router.get(
    '/users',
    response_model=List[schemas.UserPublic],
    tags=['users'],
    description='Get info about `all` registered users.',
    responses=create_status_responses({HTTP_404_NOT_FOUND: 'When `no user` with the given parameters was found.'}),
)
def read_users(
    skip: int = 0,
    limit: int = 100,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    disabled: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    # pylint: disable=unused-argument, too-many-arguments
    # REASON: the unused parameters are captured indirectly via `locals()` for automatic filtering

    params = locals().copy()
    params.pop('skip')
    params.pop('limit')
    params.pop('db')

    params = {key: value for key, value in params.items() if value is not None}
    users = crud.users.get_users_with_filtering(db, params=params, skip=skip, limit=limit)

    if not users:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'No users with given params: {params}')

    return users
