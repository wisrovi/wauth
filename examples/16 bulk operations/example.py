"""Example: bulk operations.

Demonstrates listing, counting, and batch-managing secrets in
a populated vault.
"""

import os

from wauth import WAuth


def main() -> None:
    """Run the bulk operations example."""
    db_path = "example_bulk.db"
    auth = WAuth(db_path=db_path)

    print("── Bulk Operations ──\n")

    # ── Populate vault ──
    print("📝 Populating vault with 10 secrets...")
    secrets = {
        "DB_PRIMARY": "postgresql://primary:5432/app",
        "DB_REPLICA": "postgresql://replica:5432/app",
        "REDIS_MAIN": "redis://redis:6379/0",
        "REDIS_CACHE": "redis://redis:6379/1",
        "API_EXTERNAL": "https://api.external.com/v1",
        "SMTP_HOST": "smtp.gmail.com",
        "SMTP_PORT": "587",
        "LOG_LEVEL": "INFO",
        "FEATURE_FLAG_A": "enabled",
        "FEATURE_FLAG_B": "disabled",
    }
    for key, value in secrets.items():
        auth.set(key, value)
    print(f"   ✅ Stored {len(secrets)} secrets\n")

    # ── Count secrets ──
    vault_count = auth._driver.vault.count()
    print(f"📊 Vault contains {vault_count} secrets\n")

    # ── List all keys ──
    keys = auth.list_keys()
    print(f"📋 All keys ({len(keys)} total):")
    for key in sorted(keys):
        value = auth.get(key)
        display = str(value)[:40] + "..." if len(str(value)) > 40 else value
        print(f"   {key}: {display}")

    # ── Filter keys by prefix ──
    print("\n🔍 Filtering by prefix:")
    db_keys = [k for k in auth.list_keys() if k.startswith("DB_")]
    redis_keys = [k for k in auth.list_keys() if k.startswith("REDIS_")]
    feature_keys = [k for k in auth.list_keys() if k.startswith("FEATURE_")]

    print(f"   DB keys: {db_keys}")
    print(f"   Redis keys: {redis_keys}")
    print(f"   Feature flags: {feature_keys}")

    # ── Bulk delete by prefix ──
    print("\n🗑️  Bulk deleting feature flags...")
    for key in feature_keys:
        auth.delete(key)
    print(f"   ✅ Deleted {len(feature_keys)} keys")
    print(f"   Remaining: {len(auth.list_keys())} secrets")

    # ── Bulk update ──
    print("\n🔄 Bulk updating all DB connection strings...")
    for key in db_keys:
        old_val = auth.get(key)
        new_val = old_val.replace("5432", "5433")
        auth.set(key, new_val)
        print(f"   Updated {key}: {old_val} → {new_val}")

    # Clean up
    for key in auth.list_keys():
        auth.delete(key)
    if os.path.exists(db_path):
        os.remove(db_path)


if __name__ == "__main__":
    main()
