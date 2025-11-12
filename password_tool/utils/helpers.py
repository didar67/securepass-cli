"""
Common helper utilities for password_tool.

Provides filesystem helpers, timestamp formatting and safe file write.
All helpers are small, pure functions to make testing straightforward.
"""

from __future__ import annotations
from pathlib import Path
from typing import Iterable
import datetime
import os


def ensure_dir(path: Path) -> Path:
    """
    Ensure the given directory exists. Creates it if necessary.

    Args:
        path: Path object for the directory.

    Returns:
        Path: The same path object for chaining.

    Raises:
        PermissionError: If the directory cannot be created due to permissions.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def timestamp_now() -> str:
    """
    Return a human-friendly timestamp string suitable for logs and records.

    Format: YYYY-MM-DD HH:MM:SS

    Returns:
        str: formatted timestamp
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_append_text(file_path: Path | str, lines: Iterable[str]) -> None:
    """
    Append lines to a text file in a safe, cross-platform way.

    Creates parent directories if missing.

    Args:
        file_path: target file path
        lines: iterable of strings to append (no newline required)

    Raises:
        FileNotFoundError: if the parent dir cannot be created
        PermissionError: if file is not writable
        OSError: other filesystem related errors
    """
    path = Path(file_path)
    ensure_dir(path.parent)
    # Use newline handling explicitly
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        for line in lines:
            fh.write(f"{line}\n")
