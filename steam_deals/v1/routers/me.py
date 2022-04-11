from fastapi import APIRouter, Depends

from steam_deals.core import schemas
from steam_deals.core.authentication import get_current_active_user, get_current_verified_user

me_router = APIRouter()


@me_router.get('/me', response_model=schemas.UserDetailed, tags=['me'])
async def read_me(user: schemas.UserDetailed = Depends(get_current_active_user)):
    return user


@me_router.get('/meVerified', response_model=schemas.UserDetailed, tags=['me'])
async def read_me_verified(user: schemas.UserDetailed = Depends(get_current_verified_user)):
    return user
