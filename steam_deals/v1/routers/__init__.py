from fastapi import APIRouter

main_router = APIRouter()


@main_router.get("/")
async def index():
    return {
        'description': 'This is a steam-deals project API',
        'message': 'For documentation please refer to /docs endpoint',
    }
