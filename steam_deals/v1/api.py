from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from steam_deals.config import settings, VERSION
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
)

if settings.get('ALLOW_ORIGINS', None):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=settings.get('ALLOW_CREDENTIALS', True),
        allow_methods=settings.get('ALLOW_METHODS', ['*']),
        allow_headers=settings.get('ALLOW_HEADERS', ['*']),
    )

app.include_router(main_router)
