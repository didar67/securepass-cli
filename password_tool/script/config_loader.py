"""
Load and validate YAML configuration for password_tool.

Uses PyYAML to parse config file and Pydantic v2 for typed validation.
Provides a simple `load_config()` function returning a validated Config model.

Design goals:
- Clear error messages for missing/invalid config
- Minimal side-effects (pure loader)
- Easy to mock in tests
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
import yaml
from pydantic import BaseModel, Field, ValidationError

CONFIG_DEFAULT_PATH = Path("config") / "config.yaml"


class LoggingConfig(BaseModel):
    log_dir: str = Field(..., description="Directory for log files")
    log_file: str = Field(..., description="Primary log file name")
    error_log_file: str = Field(..., description="Error-only log file name")
    level: str = Field("INFO", description="Default logging level")
    rotate_max_bytes: int = Field(5 * 1024 * 1024, description="Max bytes before rotation")
    rotate_backup_count: int = Field(3, description="Backup count for rotated logs")


class PasswordConfig(BaseModel):
    default_length: int = Field(12, description="Default password length")
    min_length: int = Field(6, description="Minimum allowed length")
    max_length: int = Field(64, description="Maximum allowed length")
    storage_folder: str = Field("generated_passwords", description="Folder to store passwords")
    storage_file: str = Field("password_records.txt", description="Filename for stored passwords")


class AppConfig(BaseModel):
    name: str = Field("password_tool")
    version: str = Field("0.1.0")


class Config(BaseModel):
    logging: LoggingConfig
    password: PasswordConfig
    app: AppConfig


class ConfigLoadError(RuntimeError):
    """Raised when configuration cannot be loaded or validated."""


def _read_yaml(path: Path) -> dict[str, Any]:
    """
    Read YAML file and return parsed dictionary.

    Raises:
        FileNotFoundError: if path does not exist.
        yaml.YAMLError: for YAML parsing errors.
    """
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with path.open("r", encoding="utf-8") as fh:
        try:
            data = yaml.safe_load(fh) or {}
            return data
        except yaml.YAMLError as exc:
            raise exc


def load_config(path: Path | str | None = None) -> Config:
    """
    Load and validate configuration.

    Args:
        path: Optional path to the YAML config file. Defaults to config/config.yaml.

    Returns:
        Config: Validated configuration object.

    Raises:
        ConfigLoadError: If file missing, invalid YAML, or validation fails.
    """
    cfg_path = Path(path) if path else CONFIG_DEFAULT_PATH

    try:
        raw = _read_yaml(cfg_path)
    except FileNotFoundError as exc:
        raise ConfigLoadError(str(exc)) from exc
    except yaml.YAMLError as exc:
        raise ConfigLoadError(f"Invalid YAML in config file: {exc}") from exc

    try:
        config = Config.model_validate(raw)  # Pydantic v2 API
        return config
    except ValidationError as exc:
        # Provide readable message about which fields failed
        raise ConfigLoadError(f"Config validation error: {exc}") from exc
