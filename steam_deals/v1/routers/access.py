from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

from steam_deals.config import settings, templates
from steam_deals.core import authentication, schemas, verification
from steam_deals.core.authentication import get_current_active_user
from steam_deals.core.db import crud
from steam_deals.core.db.session import get_db
from steam_deals.core.exception import HTTPException
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
    user: schemas.UserDetailed = Depends(get_current_active_user),
):
    # pylint: disable=unused-argument
    # REASON: `current_user` argument is need to properly check if user is already authenticated

    response = StatusResponse(detail='Cookie with access_token has been removed')
    response.set_cookie(key='access_token', httponly=True, samesite='strict', max_age=0)
    return response


@access_router.get('/sendVerificationMail', response_model=schemas.StatusResponse)
async def send_email_with_verification_token(user: schemas.UserDetailed = Depends(get_current_active_user)):
    await verification.send_verification_email(user=user)
    return StatusResponse(detail=f'Email with verification token has been sent to {user.email}.')


@access_router.get('/verify', response_model=schemas.StatusResponse)
async def verify_by_token_sent_to_email(request: Request, token: str, db: Session = Depends(get_db)):
    user = verification.verify_email_token(db=db, token=token)

    if user.verified:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f'User with username `{user.username}` is already verified!'
        )

    user.verified = True
    crud.users.update_user(db=db, user=user)

    return templates.TemplateResponse(name='verified.html', context={'request': request, 'username': user.username})
