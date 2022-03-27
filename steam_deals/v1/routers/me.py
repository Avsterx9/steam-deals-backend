from fastapi import APIRouter, Depends

from steam_deals.core import authentication
from steam_deals.core import schemas

me_router = APIRouter()


@me_router.get('/me', response_model=schemas.User, tags=['me'])
async def read_me(current_active_user: schemas.User = Depends(authentication.get_current_active_user)):
    return current_active_user
