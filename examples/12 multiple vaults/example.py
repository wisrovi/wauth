"""Example: multiple isolated vaults.

Demonstrates how to use separate WAuth instances with different
databases and encryption keys for different purposes (dev, staging, prod).
"""

import os

from wauth import WAuth


def main() -> None:
    """Run the multiple vaults example."""
    print("── Multiple Isolated Vaults ──\n")

    # ── Development vault ──
    dev_auth = WAuth(
        db_path="vault_dev.db",
        custom_key="dev-key-2024",
    )
    dev_auth.set("DATABASE_URL", "postgresql://localhost:5432/dev_db")
    dev_auth.set("DEBUG", "true")
    print("🟢 Development vault:")
    print(f"   DATABASE_URL: {dev_auth.get('DATABASE_URL')}")
    print(f"   DEBUG: {dev_auth.get('DEBUG')}")

    # ── Production vault ──
    prod_auth = WAuth(
        db_path="vault_prod.db",
        custom_key="prod-key-2024",
    )
    prod_auth.set("DATABASE_URL", "postgresql://prod-server:5432/prod_db")
    prod_auth.set("DEBUG", "false")
    print("\n🔴 Production vault:")
    print(f"   DATABASE_URL: {prod_auth.get('DATABASE_URL')}")
    print(f"   DEBUG: {prod_auth.get('DEBUG')}")

    # ── Cross-vault isolation proof ──
    print("\n── Cross-Vault Isolation ──")
    dev_url = dev_auth.get("DATABASE_URL")
    prod_url = prod_auth.get("DATABASE_URL")
    assert dev_url != prod_url
    print(f"✅ Dev and prod DATABASE_URL are different:")
    print(f"   Dev:  {dev_url}")
    print(f"   Prod: {prod_url}")

    # Even with same key name, data is isolated
    assert dev_auth.get("DATABASE_URL") == "postgresql://localhost:5432/dev_db"
    assert prod_auth.get("DATABASE_URL") == "postgresql://prod-server:5432/prod_db"

    # ── List keys per vault ──
    print(f"\n📋 Dev keys: {dev_auth.list_keys()}")
    print(f"📋 Prod keys: {prod_auth.list_keys()}")

    # Clean up
    for auth, db in [(dev_auth, "vault_dev.db"), (prod_auth, "vault_prod.db")]:
        for key in auth.list_keys():
            auth.delete(key)
        if os.path.exists(db):
            os.remove(db)


if __name__ == "__main__":
    main()
