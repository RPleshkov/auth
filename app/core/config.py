from dataclasses import dataclass, field
from pathlib import Path

from environs import Env
from pydantic import PostgresDsn

env = Env()
env.read_env()


def convention() -> dict[str, str]:
    return {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


@dataclass(frozen=True, repr=False)
class PostgresConfig:

    host: str = env("POSTGRES_HOST")
    port: int = env.int("POSTGRES_PORT")
    db_name: str = env("POSTGRES_DB_NAME")
    username: str = env("POSTGRES_USERNAME")
    password: str = env("POSTGRES_PASSWORD")

    pool_size: int = 50
    max_overflow: int = 10
    echo: bool = False

    naming_convention: dict[str, str] = field(default_factory=convention)

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


CERTS_PATH = Path(__file__).parent / "certs"


@dataclass
class JWTConfig:
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7


@dataclass(frozen=True, repr=False)
class SecurityConfig:
    jwt: JWTConfig
    private_key: Path = CERTS_PATH / "private.pem"
    public_key: Path = CERTS_PATH / "public.pem"


@dataclass
class Config:

    postgres: PostgresConfig
    security: SecurityConfig

    api_v1_prefix: str = "/api/v1"


settings = Config(
    postgres=PostgresConfig(),
    security=SecurityConfig(
        jwt=JWTConfig(),
    ),
)
