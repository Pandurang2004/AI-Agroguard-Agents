# core/logger.py

import logging
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler

# Log file location
LOG_FILE = "agroguard.log"

# Logging format
FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

def get_logger(name: str = "AgroGuard"):
    """
    Creates and returns a logger instance that logs to both
    console (pretty) and a file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # ---- Console Handler (Rich output) ----
    console_handler = RichHandler(markup=True)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(FORMAT))

    # ---- File Handler (Rotating) ----
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(FORMAT))

    # Avoid duplicate handlers if already added
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
