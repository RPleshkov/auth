import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData
from app.core.config import settings


class Base(DeclarativeBase):

    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.postgres.naming_convention,
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4()
    )
