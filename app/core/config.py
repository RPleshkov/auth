from dataclasses import dataclass

from environs import Env
from pydantic import PostgresDsn

env = Env()
env.read_env()


@dataclass
class PostgresConfig:

    host: str = env("POSTGRES_HOST")
    port: int = env.int("POSTGRES_PORT")
    db_name: str = env("POSTGRES_DB_NAME")
    username: str = env("POSTGRES_USERNAME")
    password: str = env("POSTGRES_PASSWORD")

    pool_size: int = 50
    max_overflow: int = 10
    echo: bool = False

    @property
    def get_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                host=self.host,
                port=self.port,
                path=self.db_name,
                username=self.username,
                password=self.password,
            )
        )


@dataclass
class Config:

    postgres: PostgresConfig


settings = Config(
    postgres=PostgresConfig(),
)
