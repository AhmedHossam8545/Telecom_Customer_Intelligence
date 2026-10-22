"""Shared logging setup for ingestion, ETL, and later pipelines."""

from __future__ import annotations

import logging
from pathlib import Path

from src.config import PROJECT_ROOT, get_settings


def configure_logging(name: str = "telecom") -> logging.Logger:
    settings = get_settings()
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(settings.log_level.upper())
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    file_handler = logging.FileHandler(log_dir / "pipeline.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
