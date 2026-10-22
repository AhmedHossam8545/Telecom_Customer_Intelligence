"""PostgreSQL helpers. Credentials come from environment variables only."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.config import PROJECT_ROOT, get_settings

ANALYTICS_DIR = PROJECT_ROOT / "sql" / "analytics"


def get_engine() -> Engine:
    return create_engine(get_settings().postgres_url, pool_pre_ping=True)


@contextmanager
def db_connection() -> Iterator:
    engine = get_engine()
    with engine.connect() as connection:
        yield connection


def read_sql_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run_sql_file(path: Path) -> pd.DataFrame:
    sql = read_sql_file(path)
    with db_connection() as connection:
        return pd.read_sql_query(text(sql), connection)


def list_analytics_files() -> list[Path]:
    return sorted(ANALYTICS_DIR.glob("[0-9][0-9]_*.sql"))
