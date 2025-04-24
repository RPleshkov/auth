from fastapi import FastAPI

from app.api import api_router

app = FastAPI(title="JWT Auth")


app.include_router(api_router)
