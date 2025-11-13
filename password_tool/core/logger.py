"""
Provides a centralized, rotating, and structured logging system.

This module ensures all logs are captured both on console and files,
following industry-grade formatting and handler configuration.
"""

import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger(log_dir: str = "logs", log_file: str = "app.log") -> logging.Logger:
    """
    Initialize and configure the application logger.

    Args:
        log_dir (str): Directory to store log files.
        log_file (str): Log file name.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("password_tool")

    # Prevent duplicate handlers if called multiple times
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        # File handler with rotation (max 5 MB, 3 backups)
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, log_file), maxBytes=5 * 1024 * 1024, backupCount=3
        )

        # Console handler for stdout
        console_handler = logging.StreamHandler()

        # Structured log format
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Optional: separate error file
        error_handler = RotatingFileHandler(
            os.path.join(log_dir, "error.log"), maxBytes=2 * 1024 * 1024, backupCount=2
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.addHandler(error_handler)

        logger.debug("Logger initialized successfully.")

    return logger
