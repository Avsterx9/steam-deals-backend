from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from steam_deals.config import VERSION
from steam_deals.config import settings
from steam_deals.core.exception import HTTPException
from steam_deals.v1.routers import main_router

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
    docs_url='/api/v1/docs',
    redoc_url='/api/v1/redocs',
    openapi_url='/api/v1/openapi.json',
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


app.include_router(router=main_router, prefix='/api/v1')

add_cors_middleware(app)
