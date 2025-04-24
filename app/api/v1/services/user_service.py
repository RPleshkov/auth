from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.user import UserCreate
from app.api.v1.utils.password import hash_password
from app.models import User


class UserService:

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, email: str) -> User | None:
        stmt = select(User).where(User.email == email.lower())
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def create_user(
        cls,
        session: AsyncSession,
        user_in: UserCreate,
    ):
        email = user_in.email.lower()

        user = await cls.get_user_by_email(session=session, email=email)

        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )

        name = user_in.name
        password = hash_password(user_in.password)

        user = User(name=name, email=email, password=password)
        session.add(user)
        await session.commit()
        return user
