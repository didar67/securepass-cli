"""
Covers:
- Password generation (length, randomness, charset)
- File saving and reveal behavior
- Error handling for permission and missing file
"""

import os
import pytest
import string
from unittest import mock
from pathlib import Path
from script import service
from core.exceptions import PasswordError, FileAccessError


# -------------------------------
# 🔹 Password Generation Tests
# -------------------------------

def test_generate_password_length():
    """Generated password should have expected length."""
    pwd = service.generate_secure_password(length=16)
    assert len(pwd) == 16


def test_generate_password_randomness():
    """Two generated passwords should not be identical."""
    pwd1 = service.generate_secure_password(length=12)
    pwd2 = service.generate_secure_password(length=12)
    assert pwd1 != pwd2


def test_generate_password_with_symbols():
    """Generated password must include at least one symbol."""
    pwd = service.generate_secure_password(use_symbols=True)
    assert any(c in string.punctuation for c in pwd)


def test_generate_password_invalid_length():
    """Invalid length should raise ValueError."""
    with pytest.raises(ValueError):
        service.generate_secure_password(length=0)


def test_generate_password_empty_charset():
    """When all charsets disabled, ValueError should raise."""
    with pytest.raises(ValueError):
        service.generate_secure_password(
            use_upper=False, use_digits=False, use_symbols=False
        )


# -------------------------------
# 🔹 File Save Tests (Mocked IO)
# -------------------------------

@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_save_password_success(mock_open):
    """Password should save successfully with open()."""
    file_path = "test_file.txt"
    service.save_password("work", "secure123", file_path)
    mock_open.assert_called_once_with(file_path, "a", encoding="utf-8")
    mock_open().write.assert_called_once()


@mock.patch("builtins.open", side_effect=PermissionError("denied"))
def test_save_password_permission_error(mock_open):
    """PermissionError should raise FileAccessError."""
    with pytest.raises(FileAccessError):
        service.save_password("work", "pwd", "file.txt")


@mock.patch("builtins.open", side_effect=FileNotFoundError("missing"))
def test_save_password_file_not_found(mock_open):
    """FileNotFoundError should raise FileAccessError."""
    with pytest.raises(FileAccessError):
        service.save_password("bank", "123", "nonexistent.txt")


@mock.patch("builtins.open", side_effect=Exception("unknown error"))
def test_save_password_generic_exception(mock_open):
    """Unknown exception should raise PasswordError."""
    with pytest.raises(PasswordError):
        service.save_password("bank", "123", "file.txt")


# -------------------------------
# 🔹 Reveal Password File Tests
# -------------------------------

@mock.patch("pathlib.Path.exists", return_value=True)
@mock.patch("subprocess.run")
def test_reveal_password_file_linux(mock_run, mock_exists):
    """Should run xdg-open on Linux."""
    with mock.patch("os.name", "posix"), mock.patch("sys.platform", "linux"):
        service.reveal_password_file()
        mock_run.assert_called_once()


@mock.patch("os.startfile")
@mock.patch("pathlib.Path.exists", return_value=True)
def test_reveal_password_file_windows(mock_exists, mock_startfile):
    """Should use os.startfile on Windows."""
    with mock.patch("os.name", "nt"):
        service.reveal_password_file()
        mock_startfile.assert_called_once()


@mock.patch("pathlib.Path.exists", return_value=False)
def test_reveal_password_file_not_found(mock_exists):
    """Missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        service.reveal_password_file()


@mock.patch("pathlib.Path.exists", return_value=True)
@mock.patch("subprocess.run", side_effect=Exception("open failed"))
def test_reveal_password_file_error(mock_run, mock_exists):
    """Any subprocess error should propagate Exception."""
    with pytest.raises(Exception):
        service.reveal_password_file()
