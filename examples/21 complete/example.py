"""Example 21: Comprehensive Vault Lifecycle Management.

This example demonstrates the full lifecycle of a WAuth vault, including:
1. Initialization with a custom key.
2. Storing various types of secrets (strings and files).
3. Creating an encrypted backup of the entire vault.
4. Restoring the vault from a backup using a configuration file.
5. Verifying the integrity of restored data.
"""

import os
from typing import List

from wauth import WAuth

# Constants for the example
DB_PATH: str = "example_complete.db"
BACKUP_FILE: str = "vault_backup.wauth"
CONFIG_FILE: str = "wauth_config.toml"
DEMO_FILE: str = "demo.txt"
CUSTOM_KEY: str = "master-key-example-2024"


def setup_files() -> None:
    """Prepare environment files for the example."""
    if not os.path.exists(DEMO_FILE):
        with open(DEMO_FILE, "w", encoding="utf-8") as f:
            f.write("This is a demo file content for secret storage.")

    # Create a simple config file for the restoration phase
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(f'db_path = "{DB_PATH}"\n')
        f.write(f'custom_key = "{CUSTOM_KEY}"\n')


def main() -> None:
    """Run the complete lifecycle example."""
    setup_files()

    # 1. Initialize WAuth with a specific database and custom key
    print("── Step 1: Initialization & Storage ──")
    auth = WAuth(db_path=DB_PATH, custom_key=CUSTOM_KEY)

    # 2. Store different types of secrets
    auth.set("REDIS_URL", "redis://localhost:6379")
    auth.set_file("LICENSE_CERT", DEMO_FILE)
    auth.set("DEBUG_MODE", "enabled")
    print("   ✅ Secrets and files stored successfully\n")

    # 3. List current keys
    print("📋 Current keys in vault:")
    keys: List[str] = auth.list_keys()
    for key in sorted(keys):
        print(f"   - {key}")
    print()

    # 4. Create an encrypted backup
    print("── Step 2: Backup Process ──")
    backup_path: str = auth.backup(BACKUP_FILE)
    print(f"   ✅ Backup created at: {backup_path}\n")

    # 5. Clear current vault (simulating data loss or migration)
    for key in keys:
        auth.delete(key)
    print("   ⚠️ Vault cleared for restoration demo\n")

    # 6. Restore from backup using a TOML configuration
    print("── Step 3: Restoration ──")
    # New instance using config file
    auth_restored = WAuth(config_path=CONFIG_FILE)
    restored_count: int = auth_restored.restore(backup_path)
    print(f"   ✅ Successfully restored {restored_count} secrets\n")

    # 7. Final Verification
    print("── Step 4: Verification ──")
    restored_keys: List[str] = auth_restored.list_keys()
    for key in sorted(restored_keys):
        value = auth_restored.get(key)
        # Handle file-type secrets which return bytes
        display_val = value.decode("utf-8") if isinstance(value, bytes) else value
        print(f"   - {key}: {display_val[:50]}...")

    # Cleanup example files
    print("\n🧹 Cleaning up example files...")
    for f in [DB_PATH, BACKUP_FILE, CONFIG_FILE, DEMO_FILE]:
        if os.path.exists(f):
            os.remove(f)
    print("   ✅ Cleanup complete")


if __name__ == "__main__":
    main()
