from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


class DBConnector:

    def __init__(
        self,
        url: str,
        pool_size: int,
        max_overflow: int,
        echo: bool,
    ) -> None:

        self.engine = create_async_engine(
            url=url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            echo=echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_connector = DBConnector(
    url=settings.postgres.get_url,
    pool_size=settings.postgres.pool_size,
    max_overflow=settings.postgres.max_overflow,
    echo=settings.postgres.echo,
)
