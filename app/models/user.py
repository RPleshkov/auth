import uuid
from enum import Enum

from sqlalchemy.dialects.postgresql import BYTEA, CITEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base
from app.models.mixins import CreatedAtMixin, UpdatedAtMixin


class UserRole(Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


class User(Base, CreatedAtMixin, UpdatedAtMixin):

    __tablename__ = "users"

    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(CITEXT, unique=True, index=True)
    password: Mapped[bytes] = mapped_column(BYTEA)
    role: Mapped[UserRole] = mapped_column(default=UserRole.user)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
