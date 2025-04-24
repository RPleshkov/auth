from fastapi import APIRouter
from app.api.v1.deps import SessionDep, RequestForm
from app.api.v1.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(session: SessionDep, form_data: RequestForm):
    return await AuthService.login(
        session=session,
        email=form_data.username,
        password=form_data.password,
    )
