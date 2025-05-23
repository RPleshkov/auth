import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base
from app.models.mixins import CreatedAtMixin


if TYPE_CHECKING:
    from app.models import User


class Token(Base, CreatedAtMixin):

    __tablename__ = "tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    jti: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, index=True)

    user: Mapped["User"] = relationship(back_populates="tokens")
