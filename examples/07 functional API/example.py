"""Example: functional API.

Demonstrates the module-level convenience functions that don't require
instantiating a class.
"""

import os
import tempfile

from wauth import delete, get, list_keys, set, set_file


def main() -> None:
    """Run the functional API example."""
    print("── Storing secrets without creating any object ──")

    # Store secrets
    set("DATABASE_URL", "postgresql://localhost:5432/app")
    set("REDIS_URL", "redis://localhost:6379")
    set("API_KEY", "sk-12345-abcde")

    # Retrieve
    db_url = get("DATABASE_URL")
    print(f"✅ DATABASE_URL: {db_url}")

    api_key = get("API_KEY")
    print(f"✅ API_KEY: {api_key}")

    # Missing key returns None
    missing = get("DOES_NOT_EXIST")
    assert missing is None
    print(f"✅ Missing key returns None: {missing}")

    # List all keys
    keys = list_keys()
    print(f"\n📋 All keys: {keys}")

    # Update a secret
    set("DATABASE_URL", "postgresql://production:5432/app")
    print(f"✅ Updated DATABASE_URL: {get('DATABASE_URL')}")

    # Delete a secret
    delete("REDIS_URL")
    print(f"✅ Deleted REDIS_URL, remaining: {list_keys()}")

    # Store a file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".pem", delete=False
    ) as f:
        f.write("-----BEGIN CERTIFICATE-----\ndata...")
        temp_path = f.name

    set_file("MY_CERT", temp_path)
    cert_data = get("MY_CERT")
    assert isinstance(cert_data, bytes)
    print(f"\n✅ File stored and retrieved: {cert_data[:40]}...")

    # Clean up
    for key in list_keys():
        delete(key)
    os.remove(temp_path)


if __name__ == "__main__":
    main()
