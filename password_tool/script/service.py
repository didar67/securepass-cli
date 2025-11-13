"""
Core password generation and storage service.

This module exposes pure functions that perform:
 - secure password generation
 - saving password records to disk
 - revealing/opening the record file in an OS-appropriate way

All functions are designed to be testable and to log important events.
"""

from __future__ import annotations
from typing import Optional
import string
import secrets
import logging
import os
import sys
import subprocess
from pathlib import Path
from core.exceptions import PasswordError, FileAccessError
from script.config_loader import Config  # Pydantic model from Step 4
from utils.helpers import safe_append_text, timestamp_now, ensure_dir

logger = logging.getLogger("password_tool")


def generate_secure_password(length: int = 12, use_upper: bool = True,
                             use_digits: bool = True, use_symbols: bool = True,
                             exclude_similar: bool = False) -> str:
    """
    Generate a cryptographically secure random password.

    Args:
        length (int): desired password length (>=1)
        use_upper (bool): include uppercase letters
        use_digits (bool): include digits
        use_symbols (bool): include punctuation/symbols
        exclude_similar (bool): exclude confusing chars like 'l', 'I', '1', '0', 'O'

    Returns:
        str: generated password

    Raises:
        ValueError: if length is not a positive integer or no charset available
    """
    if not isinstance(length, int) or length <= 0:
        raise ValueError("length must be a positive integer")

    base = list(string.ascii_lowercase)
    if use_upper:
        base += list(string.ascii_uppercase)
    if use_digits:
        base += list(string.digits)
    if use_symbols:
        base += list(string.punctuation)

    if exclude_similar:
        similar = set("lI1O0")
        base = [c for c in base if c not in similar]

    if not base:
        raise ValueError("Character set is empty. Enable at least one category.")

    # Use secrets.choice for cryptographic randomness
    password = "".join(secrets.choice(base) for _ in range(length))

    logger.info("Generated secure password (length=%d)", length)
    return password


def get_password_file_path(config: Optional[Config] = None) -> Path:
    """
    Compute the Path for storing the password records using config defaults.

    Args:
        config: Optional validated Config object.

    Returns:
        Path: path to password record file
    """
    if config:
        folder = Path(config.password.storage_folder)
        filename = config.password.storage_file
    else:
        folder = Path("generated_passwords")
        filename = "password_records.txt"

    ensure_dir(folder)
    return folder / filename


def save_password(level: str, password: str, file_path: str) -> None:
    """
    Save generated password securely to the given file path.
    """
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"{level}: {password}\n")
    except PermissionError as e:
        raise FileAccessError(f"Permission denied while saving: {e}")
    except FileNotFoundError as e:
        raise FileAccessError(f"Directory not found: {e}")
    except Exception as e:
        raise PasswordError(f"Unexpected error during save: {e}")


def save_password_record(level: str, password: str, config: Optional[Config] = None,
                         dry_run: bool = False) -> Path:
    """
    Save the password record (timestamp | level | password) to the configured file.

    Args:
        level (str): category/label for the password (e.g., 'gmail', 'work')
        password (str): the generated password
        config: Optional Config for storage location
        dry_run (bool): if True, do not write to disk; just log intent

    Returns:
        Path: path to the file where record would be written

    Raises:
        PermissionError: if file cannot be written
        OSError: for other IO errors
    """
    target = get_password_file_path(config)
    timestamp = timestamp_now()
    line = f"{timestamp} | {level}: {password}"

    if dry_run:
        logger.info("Dry-run enabled. Skipping write to %s", target)
        logger.debug("Dry-run content: %s", line)
        return target

    try:
        safe_append_text(target, [line])
        logger.info("Saved password for '%s' to %s", level, target)
        return target
    except PermissionError as exc:
        logger.error("Permission denied when saving password: %s", exc)
        raise
    except OSError as exc:
        logger.exception("Unexpected IO error while saving password: %s", exc)
        raise


def reveal_password_file(config: Optional[Config] = None) -> None:
    """
    Open the password record file with the system default application.

    Supports Windows (os.startfile), macOS (open) and Linux (xdg-open).

    Args:
        config: Optional Config used to locate the file

    Raises:
        FileNotFoundError: if file does not exist
        OSError: if opener command fails
    """
    path = get_password_file_path(config)
    if not path.exists():
        logger.warning("Password file not found: %s", path)
        raise FileNotFoundError(f"Password file not found: {path}")

    try:
        if os.name == "nt":  # Windows
            os.startfile(str(path))
        else:
            # macOS: 'open', Linux: 'xdg-open'
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.run([opener, str(path)], check=False)
        logger.info("Opened password file: %s", path)
    except Exception as exc:
        logger.exception("Failed to open password file: %s", exc)
        raise
