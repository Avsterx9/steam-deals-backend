from fastapi import APIRouter

from steam_deals.core import schemas
from fastapi.security import OAuth2PasswordBearer

main_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/token')


@main_router.get('/', response_model=schemas.Index, description='base `/` endpoint with API details')
async def index():
    return schemas.Index()
