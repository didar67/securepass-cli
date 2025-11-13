# Password Tool — Secure Password Generator & Manager

## Overview

Password Tool is a **secure, modular, and testable CLI application** designed to generate and manage encrypted passwords efficiently. Built with **Python, logging, unit testing, and CLI automation**, it’s structured for scalability, DevOps readiness, and professional production use.

---

## Features

* **CLI-based operations** (`generate`, `open`)
* **Configurable password generation** (symbols, digits, case, exclusions)
* **Secure file-based storage** with timestamp records
* **Structured logging system** (console + rotating file)
* **Extensive unit test coverage** (>85%) using `pytest`
* **Cross-platform compatibility** (Windows, macOS, Linux)

---

## Setup Instructions

### Prerequisites

* Python ≥ 3.9
* Git installed

### Installation Steps

```bash
# Clone repository
git clone https://github.com/<your-username>/password_tool.git
cd password_tool

# Create virtual environment
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt
```

---

## CLI Usage

### Generate Password

```bash
python main.py generate --level personal --length 16
```

**Options:**

| Flag        | Description                     | Example            |
| ----------- | ------------------------------- | ------------------ |
| `--level`   | Category of password            | `personal`, `work` |
| `--length`  | Password length                 | `--length 16`      |
| `--dry-run` | Preview password without saving | `--dry-run`        |

### Open Password Records

```bash
python main.py open
```

Opens the saved record file using system default application.

---

## Folder Structure

```bash
password_tool/
├── config/              # YAML config
├── core/                # Logger & Exception handling
├── script/              # CLI, Services, Config Loader
├── utils/               # Helper utilities
├── tests/               # Unit tests
├── docs/                # Documentation
├── main.py              # Entry point
└── requirements.txt     # Dependencies
```

---

## Logging System

* Console + Rotating File Logging (`app.log`, `error.log`)
* Format: `timestamp | level | module | message`
* Max size: 5MB per file (3 backups retained)

Example:

```
2025-11-13 19:45:02 | INFO     | password_tool | Generated secure password
```

---

## Testing

Run unit tests with:

```bash
pytest --maxfail=1 --disable-warnings -q
```

Generate coverage report:

```bash
pytest --cov=script --cov=core --cov=utils tests/
```

Expected coverage ≥ **85%**

---

## Tech Stack

| Component     | Technology                    |
| ------------- | ----------------------------- |
| Language      | Python 3.11                   |
| CLI Framework | argparse                      |
| Logging       | logging + RotatingFileHandler |
| Testing       | pytest, unittest.mock         |
| Config        | YAML (via Pydantic)           |

---

## Author

**Didarul Islam** — *Cloud DevOps & Automation Engineer (in progress)*
Passionate about creating efficient, testable, and scalable automation tools.

---

## License

Licensed under the **MIT License** — see [LICENSE](../LICENSE) for details.
