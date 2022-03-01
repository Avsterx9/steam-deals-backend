from fastapi import FastAPI
from nwta.v1.routers import main_router

app = FastAPI()

app.include_router(main_router)
