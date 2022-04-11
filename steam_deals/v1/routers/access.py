from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from steam_deals.config import settings
from steam_deals.core import authentication, schemas
from steam_deals.core.db.session import get_db
from steam_deals.core.utils import StatusResponse

access_router = APIRouter()


@access_router.post('/token', response_model=schemas.Token)
async def login_for_access_token(
    response: Response, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authentication.authenticate_user(db=db, username=form_data.username, password=form_data.password)

    expires_secs = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    expires_delta = timedelta(seconds=expires_secs)

    access_token = authentication.create_access_token(data={'sub': user.username}, expires_delta=expires_delta)
    response.set_cookie(
        key='access_token', value=f'Bearer {access_token}', httponly=True, samesite='strict', max_age=expires_secs
    )
    return schemas.Token(access_token=access_token, expires_in=expires_secs)


@access_router.post('/logout', response_model=schemas.StatusResponse)
async def logout_to_remove_http_only_cookie(
    current_user: schemas.User = Depends(authentication.get_current_active_user),
):
    # pylint: disable=unused-argument
    # REASON: `current_user` argument is need to properly check if user is already authenticated

    response = StatusResponse(detail='Cookie with access_token has been removed')
    response.set_cookie(key='access_token', httponly=True, samesite='strict', max_age=0)
    return response
