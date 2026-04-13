"""Example: key rotation.

Demonstrates how to rotate the encryption key, which automatically
re-encrypts all existing secrets with the new key.
"""

import os

from wauth import WAuth


def main() -> None:
    """Run the key rotation example."""
    db_path = "example_rotation.db"

    # Create vault with an initial key
    auth = WAuth(db_path=db_path, custom_key="old-key-123")
    auth.set("DB_PASSWORD", "super-secret-db-pass")
    auth.set("API_TOKEN", "token-abc-xyz")

    print("Secrets stored with 'old-key-123':")
    print(f"  DB_PASSWORD: {auth.get('DB_PASSWORD')}")
    print(f"  API_TOKEN: {auth.get('API_TOKEN')}")

    # Rotate to a new key
    print("\n🔄 Rotating encryption key...")
    results = auth.rotate_key("new-key-456")
    print(f"  Rotation results: {results}")

    # Verify all secrets are still accessible
    print("\nSecrets after rotation (still readable):")
    print(f"  DB_PASSWORD: {auth.get('DB_PASSWORD')}")
    print(f"  API_TOKEN: {auth.get('API_TOKEN')}")

    # Verify old key no longer works by creating a fresh instance
    old_auth = WAuth(db_path=db_path, custom_key="old-key-123")
    try:
        old_auth.get("DB_PASSWORD")
        print("\n⚠️  Old key still works (unexpected)")
    except Exception:
        print("\n⚠️  Old key cannot decrypt (expected after rotation)")

    # Verify new key works
    new_auth = WAuth(db_path=db_path, custom_key="new-key-456")
    new_result = new_auth.get("DB_PASSWORD")
    print(f"✅ Accessing with new key: {new_result}")

    assert new_result == "super-secret-db-pass"

    # Clean up
    if os.path.exists(db_path):
        os.remove(db_path)


if __name__ == "__main__":
    main()
