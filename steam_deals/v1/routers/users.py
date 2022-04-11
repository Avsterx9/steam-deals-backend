from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from steam_deals.core import schemas, verification
from steam_deals.core.db import crud
from steam_deals.core.db.session import get_db
from steam_deals.core.exception import HTTPException

users_router = APIRouter()


@users_router.post('/users', response_model=schemas.UserDetailed, tags=['users'])
async def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    if crud.users.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=f'Email `{user.email}` is already taken')
    if crud.users.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=f'Username `{user.username}` is already taken')

    user = crud.users.create_user(db=db, user=user)
    await verification.verify_user(db=db, user=user)
    return user


@users_router.get('/users/{username}', response_model=schemas.UserPublic, tags=['users'])
def read_user(username: str, db: Session = Depends(get_db)):
    user = crud.users.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'User with username `{username}` was not found')
    return user


@users_router.get('/users', response_model=List[schemas.UserPublic], tags=['users'])
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
    users = crud.get_users_with_filtering(db, params=params, skip=skip, limit=limit)

    if not users:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'No users with given params: {params}')

    return users
