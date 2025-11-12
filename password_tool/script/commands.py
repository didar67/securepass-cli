"""
Thin adapter functions that CLI calls to perform actions.

Keeps CLI and business logic decoupled for easier testing and reuse.
"""

from __future__ import annotations
from typing import Optional
import logging

from script.service import (
    generate_secure_password,
    save_password_record,
    reveal_password_file,
)
from script.config_loader import Config

logger = logging.getLogger("password_tool")


def cmd_generate(level: str, length: int, config: Optional[Config] = None,
                 dry_run: bool = False) -> str:
    """
    Generate a password and optionally save it.

    Args:
        level: label/category for password
        length: desired password length
        config: optional config
        dry_run: if True, do not persist

    Returns:
        str: generated password
    """
    pwd = generate_secure_password(length=length)
    logger.debug("cmd_generate: generated password for %s", level)

    # Save record (or dry-run)
    save_password_record(level, pwd, config=config, dry_run=dry_run)

    # For CLI we return the password so the caller may print/copy
    return pwd


def cmd_open_records(config: Optional[Config] = None) -> None:
    """
    Command to open the password records file.
    """
    try:
        reveal_password_file(config)
    except FileNotFoundError:
        logger.warning("No password records found to open.")
