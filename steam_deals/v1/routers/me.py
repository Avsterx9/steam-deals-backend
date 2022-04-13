from fastapi import APIRouter, Depends
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from steam_deals.core import schemas
from steam_deals.core.authentication import get_current_active_user, get_current_verified_user
from steam_deals.core.utils import create_status_responses

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
async def read_info_about_logged_user(user: schemas.UserDetailed = Depends(get_current_active_user)):
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
async def read_info_about_logged_user_if_verified(user: schemas.UserDetailed = Depends(get_current_verified_user)):
    return user
