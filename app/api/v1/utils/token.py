from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

import jwt

from app.core.config import settings
from app.models import User, Token
from sqlalchemy.ext.asyncio import AsyncSession


class TokenManager:

    ACCESS_TOKEN = "access"
    REFRESH_TOKEN = "refresh"

    def __init__(
        self,
        private_key: str,
        public_key: str,
        algorithm: str,
        access_token_expire_minutes: int,
        refresh_token_expire_days: int,
    ):
        self.private_key = private_key
        self.public_key = public_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def _update_iat_and_exp(self, payload: dict[str, Any]) -> None:
        self.iat = datetime.now(timezone.utc)
        token_type = payload["type"]
        if token_type == self.ACCESS_TOKEN:
            self.exp = self.iat + timedelta(minutes=self.access_token_expire_minutes)
        elif token_type == self.REFRESH_TOKEN:
            self.exp = self.iat + timedelta(days=self.refresh_token_expire_days)

    def _generate_jti(self):
        self.jti = uuid4()

    def encode_jwt(self, payload: dict[str, Any]) -> str:
        to_encode = payload.copy()

        self._update_iat_and_exp(to_encode)
        self._generate_jti()

        to_encode.update(jti=self.jti, iat=self.iat, exp=self.exp)
        token = jwt.encode(
            payload=payload, key=self.private_key, algorithm=self.algorithm
        )
        return token

    def decode_jwt(self, token: str) -> dict[str, Any]:
        payload = jwt.decode(
            jwt=token,
            key=self.public_key,
            algorithms=[self.algorithm],
        )
        return payload

    def create_access_token(self, user: User) -> str:
        payload = {
            "type": self.ACCESS_TOKEN,
            "user_id": str(user.id),
            "sub": user.email,
        }
        return self.encode_jwt(payload)

    async def create_refresh_token(self, session: AsyncSession, user: User) -> str:
        payload = {
            "type": self.REFRESH_TOKEN,
            "user_id": str(user.id),
            "sub": user.email,
        }

        token = self.encode_jwt(payload)
        session.add(
            Token(
                user_id=user.id,
                jti=self.jti,
                created_at=self.iat,
                expires_at=self.exp,
            )
        )
        await session.commit()
        return token


token_manager = TokenManager(
    private_key=settings.security.private_key.read_text(),
    public_key=settings.security.public_key.read_text(),
    algorithm=settings.security.jwt.algorithm,
    access_token_expire_minutes=settings.security.jwt.access_token_expire_minutes,
    refresh_token_expire_days=settings.security.jwt.refresh_token_expire_days,
)
