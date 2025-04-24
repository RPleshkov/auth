from fastapi import APIRouter, status

from app.api.v1.deps import SessionDep
from app.api.v1.schemas.user import UserCreate, UserPublic
from app.api.v1.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(session: SessionDep, user_in: UserCreate):
    return await UserService.create_user(session=session, user_in=user_in)
