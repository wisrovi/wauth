"""Example: exception handling.

Demonstrates the structured exception hierarchy and how to handle
each type of error appropriately.
"""

import os

from wauth import WAuth
from wauth.core import CryptoEngine
from wauth.exceptions import (
    DecryptionError,
    KeyNotFoundError,
    VaultError,
    WAuthError,
)


def demo_decryption_error() -> None:
    """Show how DecryptionError is raised on wrong key."""
    engine = CryptoEngine(custom_key="correct-key")
    encrypted = engine.encrypt(b"secret message")

    # Try to decrypt with wrong key
    wrong_engine = CryptoEngine(custom_key="wrong-key")
    try:
        wrong_engine.decrypt(encrypted)
    except DecryptionError as exc:
        print(f"✅ DecryptionError caught: {exc}")


def demo_key_not_found() -> None:
    """Show how KeyNotFoundError is raised on missing keys."""
    db_path = "example_exceptions.db"
    auth = WAuth(db_path=db_path)

    try:
        auth.delete("NONEXISTENT_KEY")
    except WAuthError as exc:
        print(f"✅ WAuthError caught: {exc}")

    # Clean up
    if os.path.exists(db_path):
        os.remove(db_path)


def demo_hierarchy() -> None:
    """Show that all exceptions inherit from WAuthError."""
    from wauth.exceptions import (
        BackupError,
        ConfigurationError,
        RestoreError,
        RotationError,
    )

    exceptions = [
        DecryptionError("test"),
        KeyNotFoundError("test"),
        VaultError("test"),
        BackupError("test"),
        RestoreError("test"),
        RotationError("test"),
        ConfigurationError("test"),
    ]

    for exc in exceptions:
        assert isinstance(exc, WAuthError)
    print(f"✅ All {len(exceptions)} exception types inherit from WAuthError")


def main() -> None:
    """Run the exception handling example."""
    print("── Decryption Error ──")
    demo_decryption_error()

    print("\n── Key Not Found ──")
    demo_key_not_found()

    print("\n── Exception Hierarchy ──")
    demo_hierarchy()


if __name__ == "__main__":
    main()
