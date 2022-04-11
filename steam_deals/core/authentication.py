from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from steam_deals.config import settings
from steam_deals.core import schemas, security
from steam_deals.core.db import crud
from steam_deals.core.db.session import get_db
from steam_deals.core.exception import CREDENTIALS_VALIDATION_EXCEPTION, HTTPException
from steam_deals.core.security import OAuth2PasswordBearerWithCookie

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl='/token')


def authenticate_user(db: Session, username: str, password: str) -> schemas.UserInDb:
    user = crud.users.get_user_by_username(db, username=username) or crud.users.get_user_by_email(db, email=username)
    if not user or not security.verify_password(plain_password=password, hashed_password=user.hashed_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    data = data.copy()

    expires = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=30)
    data.update({'exp': expires})
    encoded_jwt = jwt.encode(claims=data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> schemas.UserInDb:
    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = payload.get('sub')
        if username is None:
            raise CREDENTIALS_VALIDATION_EXCEPTION
    except JWTError as exception:
        raise CREDENTIALS_VALIDATION_EXCEPTION from exception

    user = crud.users.get_user_by_username(db, username=username)
    if user is None:
        raise CREDENTIALS_VALIDATION_EXCEPTION
    return user


async def get_current_active_user(user: schemas.UserInDb = Depends(get_current_user)) -> schemas.UserInDb:
    if user.disabled:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f'User with username `{user.username}` is inactive!'
        )
    return user


async def get_current_verified_user(user: schemas.UserInDb = Depends(get_current_active_user)) -> schemas.UserInDb:
    if not user.verified:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f'User with username `{user.username}` is not verified!'
        )
    return user
