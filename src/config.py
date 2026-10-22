"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    if value is not None and value.strip() == "":
        return default
    return value


@dataclass(frozen=True)
class Settings:
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_sslmode: str
    log_level: str

    @property
    def postgres_url(self) -> str:
        user = quote_plus(self.postgres_user)
        password = quote_plus(self.postgres_password)
        return (
            f"postgresql+psycopg2://{user}:{password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
            f"?sslmode={self.postgres_sslmode}"
        )


def get_settings() -> Settings:
    host = _env("POSTGRES_HOST", "localhost") or "localhost"
    default_ssl = "require" if "supabase" in host.lower() else "prefer"
    return Settings(
        postgres_host=host,
        postgres_port=int(_env("POSTGRES_PORT", "5432") or "5432"),
        postgres_db=_env("POSTGRES_DB", "telecom_intelligence") or "telecom_intelligence",
        postgres_user=_env("POSTGRES_USER", "telecom") or "telecom",
        postgres_password=_env("POSTGRES_PASSWORD", "change_me") or "change_me",
        postgres_sslmode=_env("POSTGRES_SSLMODE", default_ssl) or default_ssl,
        log_level=_env("LOG_LEVEL", "INFO") or "INFO",
    )
