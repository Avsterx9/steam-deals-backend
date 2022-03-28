from fastapi import APIRouter

from steam_deals.core import schemas

main_router = APIRouter()


@main_router.get('/', response_model=schemas.Index, description='base `/` endpoint with API details')
async def index():
    return schemas.Index()
