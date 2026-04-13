"""Create encrypted secrets for the pipeline example.

This script stores secrets using a custom encryption key that will be
shared across multiple pipeline runs.

Usage:
    python create_secret.py

See example.py for the full pipeline demonstration.
"""

import os
from pathlib import Path

from wauth import WAuth

DB_PATH = "wauth2.db"


def create_secrets() -> None:
    """Store example secrets in an encrypted vault."""
    custom_key = "my-very-secure-key"
    auth = WAuth(db_path=DB_PATH, custom_key=custom_key)

    REAL_PASSWORD = "mysecretpassword123"

    auth.set("USER_1", REAL_PASSWORD)
    print(f"Secret stored for key: USER_1")


def main() -> None:
    """Main entry point."""
    create_secrets()

    if os.path.exists(DB_PATH):
        print(f"Vault created: {Path(DB_PATH).absolute()}")


if __name__ == "__main__":
    main()
