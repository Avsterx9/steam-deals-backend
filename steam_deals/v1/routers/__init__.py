from fastapi import APIRouter

from steam_deals.core import schemas
from steam_deals.v1.routers.access import access_router
from steam_deals.v1.routers.me import me_router
from steam_deals.v1.routers.users import users_router

main_router = APIRouter()  # need for defining tags order
index_router = APIRouter()


@index_router.get('/', response_model=schemas.Index, description='base `/` endpoint with API details', tags=['index'])
async def index():
    return schemas.Index()


main_router.include_router(index_router)
main_router.include_router(access_router)
main_router.include_router(me_router)
main_router.include_router(users_router)
