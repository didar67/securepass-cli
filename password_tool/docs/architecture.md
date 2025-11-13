# System Architecture — Password Tool

## Folder Structure

```bash
password_tool/
├── config/
│   └── config.yaml                # Default configuration (YAML)
├── core/
│   ├── logger.py                  # Centralized structured logging
│   └── exceptions.py              # Custom error definitions
├── script/
│   ├── cli.py                     # CLI command parser
│   ├── commands.py                # Command execution wrapper
│   ├── service.py                 # Password generation & save logic
│   └── config_loader.py           # YAML → Pydantic config loader
├── utils/
│   └── helpers.py                 # Helper utilities (safe I/O, timestamp)
├── tests/
│   ├── test_logger.py             # Logger module test
│   ├── test_cli.py                # CLI behavior test
│   └── test_service.py            # Password generator test
├── docs/
│   ├── README.md                  # Project documentation
│   └── architecture.md            # Architecture explanation
├── main.py                        # CLI entry point
├── requirements.txt               # Dependency list
├── .gitignore                     # Git ignore rules
└── LICENSE                        # License information
```

---

## Core Workflow

### 🔹 1. CLI Entry (`main.py` → `script/cli.py`)

* Initializes CLI parser using `argparse`.
* Supports `generate` and `open` subcommands.
* Passes parsed arguments to command functions in `commands.py`.

### 🔹 2. Command Execution (`script/commands.py`)

* For `generate`: calls `service.generate_secure_password()` and optionally `service.save_password_record()`.
* For `open`: calls `service.reveal_password_file()`.
* Uses `config_loader` to load YAML configurations.

### 🔹 3. Password Generation (`script/service.py`)

* Creates cryptographically secure passwords using `secrets.choice()`.
* Supports symbol, digit, and uppercase toggles.
* Saves generated passwords with timestamps.
* Mock-safe for test coverage.

### 🔹 4. Logging System (`core/logger.py`)

* Uses `RotatingFileHandler` for log rotation.
* Logs are stored in `/logs/app.log` and `/logs/error.log`.
* Ensures all modules can access unified logger.

### 🔹 5. Configuration Loader (`script/config_loader.py`)

* Loads settings from YAML file.
* Validates via `Pydantic` model.
* Exposes attributes like storage folder and filename.

### 🔹 6. Helpers (`utils/helpers.py`)

* Provides common functions such as directory creation, safe file append, and timestamp utilities.

### 🔹 7. Unit Tests (`tests/`)

* Each core component is covered by unit tests.
* Mocking used for file and subprocess dependencies.
* Achieved >85% coverage using `pytest-cov`.

---

## Data Flow Diagram

```
┌────────────┐
│  User CLI  │
└──────┬─────┘
       │
       ▼
┌────────────┐    ┌───────────────┐
│  CLI Parser│───▶│ Command Layer │
└────────────┘    └──────┬────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Service Logic│
                  └──────┬───────┘
                         │
                         ▼
                 ┌──────────────┐
                 │ File System  │
                 └──────────────┘
```

---

## Design Principles

| Principle                  | Description                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------- |
| **Modularity**             | Each component (CLI, Service, Logger, Config) is independent and testable.         |
| **Separation of Concerns** | CLI handles user interaction, Service handles logic, Logger handles observability. |
| **Extensibility**          | Future subcommands or encryption support can be added easily.                      |
| **Reliability**            | Errors are handled with custom exceptions and logs.                                |

---

## Summary

This architecture ensures:

* Robust and secure password management.
* Clear separation of CLI, logic, and utility layers.
* Full test coverage and maintainability.
* Ready for CI/CD, containerization, and DevOps pipelines.
