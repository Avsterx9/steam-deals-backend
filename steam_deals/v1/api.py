from fastapi import FastAPI
from steam_deals.v1.routers import main_router

app = FastAPI()

app.include_router(main_router)
