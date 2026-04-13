"""Example: backup and restore.

Demonstrates how to export all secrets to a backup file and
restore them later.
"""

import os

from wauth import WAuth


def main() -> None:
    """Run the backup/restore example."""
    db_path = "example_backup.db"
    backup_file = "vault_backup.wauth"
    auth = WAuth(db_path=db_path)

    # Store some secrets
    auth.set("DATABASE_URL", "postgresql://localhost:5432/myapp")
    auth.set("REDIS_URL", "redis://localhost:6379")
    auth.set_file("TLS_CERT", __file__)

    print(f"📋 Vault contains {len(auth.list_keys())} secrets:")
    for key in auth.list_keys():
        print(f"   - {key}")

    # ── Create backup ──
    backup_path = auth.backup(backup_file)
    print(f"\n💾 Backup created at: {backup_path}")

    # Simulate a disaster — delete all secrets
    print("\n🗑️  Simulating disaster — deleting all secrets...")
    for key in auth.list_keys():
        auth.delete(key)
    print(f"   Vault now empty: {auth.list_keys()}")

    # ── Restore from backup ──
    print(f"\n🔄 Restoring from {backup_path}...")
    count = auth.restore(backup_path)
    print(f"   Restored {count} secrets")

    # Verify
    print(f"\n✅ Vault restored with {len(auth.list_keys())} secrets:")
    for key in auth.list_keys():
        print(f"   - {key}")

    assert auth.get("DATABASE_URL") == "postgresql://localhost:5432/myapp"

    # Clean up
    for key in auth.list_keys():
        auth.delete(key)
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(backup_file):
        os.remove(backup_file)


if __name__ == "__main__":
    main()
