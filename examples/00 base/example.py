"""Example demonstrating basic WAuth usage.

This example shows how to:
1. Initialize a WAuth instance with a custom database path.
2. Store an encrypted text secret.
3. Retrieve and decrypt the stored secret.
"""

import os

from wauth import WAuth


def main() -> None:
    """Run the basic WAuth example."""
    auth = WAuth(db_path="wauth.db")

    REAL_TOKEN = "7483920:ABC-DEF-GHI"  # Example token (not real)

    # Store an encrypted secret (automatic Fernet encryption)
    auth.set("TELEGRAM_TOKEN", REAL_TOKEN)

    # Retrieve and decrypt the secret (only works on this machine)
    token = auth.get("TELEGRAM_TOKEN")

    print(f"Retrieved token: {token}", "valid" if token == REAL_TOKEN else "invalid")

    # Clean up demo database
    if os.path.exists("demo.db"):
        os.remove("demo.db")


def main2() -> None:
    """Run the basic WAuth example with a custom encryption key."""
    custom_key = "my-very-secure-key"
    auth = WAuth(db_path="wauth2.db", custom_key=custom_key)

    REAL_TOKEN = "7483920:ABC-DEF-GHI"  # Example token (not real)

    # Store an encrypted secret (automatic Fernet encryption)
    auth.set("TELEGRAM_TOKEN", REAL_TOKEN)

    # Retrieve and decrypt the secret (only works on this machine with the same key)
    token = auth.get("TELEGRAM_TOKEN")

    print(
        f"Retrieved token with custom key: {token}",
        "valid" if token == REAL_TOKEN else "invalid",
    )


if __name__ == "__main__":
    main()
    main2()
