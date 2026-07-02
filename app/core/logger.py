"""
Centralized logging configuration for ProdPilot AI.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ======================================================
# Paths
# ======================================================

BASE_DIR = Path(__file__).resolve().parents[2]

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "prodpilot.log"

# ======================================================
# Formatter
# ======================================================

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

formatter = logging.Formatter(LOG_FORMAT)

# ======================================================
# Root Logger
# ======================================================

logger = logging.getLogger("prodpilot")

if not logger.handlers:

    logger.setLevel(logging.INFO)

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Rotating File
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """
    Return a child logger.
    """

    return logger.getChild(name)