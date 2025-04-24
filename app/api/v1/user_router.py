from fastapi import APIRouter
from app.api.v1.schemas.user import UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
async def register(user_in: UserCreate) -> UserPublic:
    pass
