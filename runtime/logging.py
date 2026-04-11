"""Project logging helpers."""
from __future__ import annotations

import logging
import os
from pathlib import Path

from config import AppConfig


def configure_logging(config: AppConfig) -> logging.Logger:
    log_dir = config.paths.logs_dir
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "abracapocus.log"

    logger = logging.getLogger("abracapocus")
    if logger.handlers:
        return logger

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
