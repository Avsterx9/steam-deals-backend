from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from steam_deals.config import settings
from steam_deals.core import authentication
from steam_deals.core import schemas
from steam_deals.core.db.session import get_db

main_router = APIRouter()


@main_router.get('/', response_model=schemas.Index, description='base `/` endpoint with API details')
async def index():
    return schemas.Index()


@main_router.post('/token', response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authentication.authenticate_user(db=db, username=form_data.username, password=form_data.password)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}
