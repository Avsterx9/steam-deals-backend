from fastapi import FastAPI

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

app.include_router(main_router)
