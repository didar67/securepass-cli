"""
Handles command-line interface for Password Tool.
Provides structured subcommands (generate, open) for end users.
"""

import argparse
import sys
from typing import Optional
from script.commands import cmd_generate, cmd_open_records
from script.config_loader import Config
from utils.helpers import ensure_dir


def start_app(config: Optional[Config] = None) -> None:
    """
    Initialize and run the Password Tool CLI interface.

    Args:
        config (Optional[Config]): Loaded configuration object (YAML-based).
    """
    parser = argparse.ArgumentParser(
        prog="password_tool",
        description="Secure Password Generator & Saver CLI",
        epilog="Example: python main.py generate --level personal --length 16",
    )

    # Define subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a secure password")
    generate_parser.add_argument(
        "--level", "-l",
        type=str,
        required=True,
        help="Specify password category (e.g., personal, work, finance)",
    )
    generate_parser.add_argument(
        "--length", "-n",
        type=int,
        default=12,
        help="Password length (default: 12)",
    )
    generate_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview password without saving to file",
    )

    # Open command
    subparsers.add_parser("open", help="Open the saved password record file")

    # Parse CLI args
    args = parser.parse_args()

    try:
        if args.command == "generate":
            from pathlib import Path
            ensure_dir(Path("records"))  # ensures directory exists
            pwd = cmd_generate(
                level=args.level,
                length=args.length,
                config=config,
                dry_run=args.dry_run,
            )
            print(f"Generated password for [{args.level}]: {pwd}")

        elif args.command == "open":
            cmd_open_records(config=config)

        else:
            parser.print_help()

    except Exception as exc:
        print(f"[ERROR] CLI execution failed: {exc}")
        sys.exit(1)
