from fastapi import APIRouter

from app.api.v1.auth_router import router as auth_router
from app.api.v1.user_router import router as user_router
from app.core.config import settings

api_router = APIRouter(prefix=settings.api_v1_prefix)
api_router.include_router(auth_router)
api_router.include_router(user_router)
