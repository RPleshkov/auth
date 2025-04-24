from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.token import TokenPair
from app.api.v1.services.user_service import UserService
from app.api.v1.utils.password import check_password
from app.api.v1.utils.token import token_manager


class AuthService:

    @classmethod
    async def login(cls, session: AsyncSession, email: str, password: str) -> TokenPair:

        user = await UserService.get_user_by_email(
            session=session,
            email=email,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not active",
            )

        access_token = token_manager.create_access_token(user)
        refresh_token = await token_manager.create_refresh_token(
            session=session, user=user
        )

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )
