from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from steam_deals.config import settings, VERSION
from steam_deals.core.exception import HTTPException
from steam_deals.v1.routers import main_router
from steam_deals.v1.routers.me import me_router
from steam_deals.v1.routers.users import users_router

app = FastAPI(
    title=settings.PROJECT_TITLE,
    description=settings.PROJECT_DESC,
    version=VERSION,
    contact={
        'name': 'steam-deals',
        'url': 'https://gitlab.com/rafit/steam-deals-backend',
    },
    license_info={
        'name': 'MIT License',
        'url': 'https://opensource.org/licenses/MIT',
    },
)


def add_cors_middleware(app_: Starlette):
    if settings.get('ALLOW_ORIGINS', None):
        app_.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOW_ORIGINS,
            allow_credentials=settings.get('ALLOW_CREDENTIALS', True),
            allow_methods=settings.get('ALLOW_METHODS', ['*']),
            allow_headers=settings.get('ALLOW_HEADERS', ['*']),
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exception: HTTPException):
    # pylint: disable=unused-argument
    # REASON: to properly add exception handler we must include `request` and `exception` parameters

    return JSONResponse(
        status_code=exception.status_code,
        headers=exception.headers,
        content={'status_code': exception.status_code, 'phrase': exception.phrase, 'detail': exception.detail},
    )


app.include_router(main_router)
app.include_router(users_router)
app.include_router(me_router)

add_cors_middleware(app)
