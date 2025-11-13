"""
Application entrypoint. Orchestrates initial setup (config load) and
delegates execution to CLI/service layer. Keeps main.py minimal.
"""

import sys
from script import cli
from script.config_loader import load_config, ConfigLoadError
from core.exceptions import AppError

def main() -> None:
    """
    Load configuration and start CLI handler.

    Any heavy logic is delegated to modules; main remains orchestration-only.
    """
    try:
        config = load_config()
        cli.start_app(config=config)
        sys.exit(0)

    except (ConfigLoadError, AppError) as e:
        print(f"[ERROR] {e}")
        sys.exit(2)

    except Exception as e:
        print(f"[FATAL] Unexpected system error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        # Last-resort error output; actual modules should log via logger
        print(f"FATAL: Unhandled exception: {e}")
        sys.exit(1)
