"""
Handles command-line interface for Password Tool.
Uses argparse for structured, user-friendly CLI command management.
"""

import argparse
import sys
from utils.helpers import validate_length


def start_app():
    """
    Initializes and runs the Password Tool CLI interface.

    This function handles command parsing and triggers relevant
    functionality (generate, open, etc.) in the main workflow.
    """
    parser = argparse.ArgumentParser(
        prog="password_tool",
        description="Secure Password Generator & Saver CLI",
        epilog="Example: python main.py generate --level personal --length 16",
    )

    # Sub-commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command
    generate_parser = subparsers.add_parser(
        "generate", help="Generate a secure password"
    )
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

    # Open command
    subparsers.add_parser("open", help="Open the saved password file")

    # Parse arguments
    args = parser.parse_args()

    # Handle actions
    if args.command == "generate":
        if not validate_length(args.length):
            print("Invalid length: must be between 6 and 64")
            sys.exit(1)

        print(f"Generating password for level: {args.level}, length: {args.length}")
        # Placeholder: actual password generator logic will be connected later

    elif args.command == "open":
        print("Opening password record file...")
        # Placeholder for file reveal logic

    else:
        parser.print_help()
