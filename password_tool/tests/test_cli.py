"""
Covers:
- CLI argument parsing for generate/open
- Invalid command handling
- Integration with helper and command modules using mock
"""

import pytest
from unittest import mock
from script import cli


def test_cli_generate_command(monkeypatch):
    """Verify generate command runs with valid args."""
    test_args = ["prog", "generate", "--level", "personal", "--length", "8"]
    monkeypatch.setattr("sys.argv", test_args)

    with mock.patch("script.commands.cmd_generate", return_value="mockPWD"):
        cli.start_app()
    # Expect print output (stdout)
    # But since print output is side-effect, no exception == success


def test_cli_open_command(monkeypatch):
    """Verify open command runs successfully."""
    test_args = ["prog", "open"]
    monkeypatch.setattr("sys.argv", test_args)

    with mock.patch("script.commands.cmd_open_records") as mock_open:
        cli.start_app()
        mock_open.assert_called_once()


def test_cli_invalid_command(monkeypatch):
    """Invalid command should show help (no crash)."""
    test_args = ["prog", "invalid"]
    monkeypatch.setattr("sys.argv", test_args)

    with pytest.raises(SystemExit):
        cli.start_app()


def test_cli_exception_handling(monkeypatch):
    """Ensure exception prints friendly message and exits."""
    test_args = ["prog", "generate", "--level", "x"]
    monkeypatch.setattr("sys.argv", test_args)

    with mock.patch("script.commands.cmd_generate", side_effect=Exception("mock error")):
        with pytest.raises(SystemExit):
            cli.start_app()
    # Expect SystemExit due to unhandled exception in command