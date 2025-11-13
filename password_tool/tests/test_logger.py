"""
Covers:
- Log directory creation
- Log rotation handler configuration
- Error log handler addition
- Logging initialization and level setup
"""

import os
import logging
import pytest
from unittest import mock
from core.logger import setup_logger


@pytest.fixture
def mock_log_dir(tmp_path):
    """Fixture for temporary log directory"""
    return tmp_path


def test_logger_creates_log_directory(mock_log_dir):
    """Ensure logger creates directory if not exists."""
    with mock.patch("os.makedirs") as mock_make_dir:
        setup_logger(str(mock_log_dir))
        mock_make_dir.assert_called_once_with(str(mock_log_dir), exist_ok=True)


def test_logger_returns_valid_instance(mock_log_dir):
    """Logger should return a valid logging.Logger instance."""
    logger_instance = setup_logger(str(mock_log_dir))
    assert isinstance(logger_instance, logging.Logger)
    assert logger_instance.name == "password_tool"


def test_logger_handlers_and_levels(mock_log_dir):
    """Verify all handlers and log levels are properly configured."""
    log = setup_logger(str(mock_log_dir))
    handler_types = [type(h).__name__ for h in log.handlers]
    assert "RotatingFileHandler" in handler_types
    assert "StreamHandler" in handler_types
    assert log.level == logging.DEBUG


def test_logger_writes_log_file(mock_log_dir):
    """Ensure logger writes logs to file successfully."""
    log = setup_logger(str(mock_log_dir))
    log.info("Test message written to file")
    files = os.listdir(mock_log_dir)
    assert any(f.endswith(".log") for f in files)
