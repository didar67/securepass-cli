"""
Main entry point of the Password Tool application.
Handles startup orchestration and delegates execution to CLI.
"""

import sys
from script import cli


def main():
    """Main entry function — orchestrates CLI execution."""
    cli.start_app()


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        sys.exit(1)
