"""
Custom exception classes for centralized error handling.
Defines structured exceptions with logging hooks.
"""

import logging

logger = logging.getLogger(__name__)

class AppError(Exception):
    """Base class for all custom application exceptions."""
    def __init__(self, message: str):
        super().__init__(message)
        logger.error(f"[AppError] {self.__class__.__name__}: {message}")

class ConfigError(AppError):
    """Raised when configuration loading or validation fails."""
    pass

class PasswordError(AppError):
    """Raised for password generation, validation, or saving errors."""
    pass

class FileAccessError(AppError):
    """Raised when reading/writing files encounters issues."""
    pass
