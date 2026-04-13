"""Example: security best practices.

Demonstrates recommended patterns for using WAuth securely in
production applications.
"""

import os

from wauth import WAuth
from wauth.exceptions import DecryptionError, KeyNotFoundError


def main() -> None:
    """Run the security best practices example."""
    db_path = "example_security.db"

    print("── Security Best Practices ──\n")

    # ── 1. Always use a custom key for portability ──
    print("1️⃣  Use custom encryption key for portability")
    auth = WAuth(
        db_path=db_path,
        custom_key="my-secure-key-from-env-or-vault",
    )
    print("   ✅ Custom key set (load from env vars or secret manager)\n")

    # ── 2. Store secrets with TTL for temporary data ──
    print("2️⃣  Use TTL for temporary credentials")
    auth.set("SESSION_TOKEN", "temp-token", ttl=3600)
    auth.set("API_KEY", "permanent-key")  # No TTL = permanent
    print("   ✅ Session token set with 1-hour TTL")
    print("   ✅ API key set as permanent\n")

    # ── 3. Handle exceptions explicitly ──
    print("3️⃣  Handle exceptions explicitly")
    try:
        value = auth.get("SESSION_TOKEN")
        print(f"   ✅ Retrieved: {value}")
    except DecryptionError:
        print("   ❌ Decryption failed — key mismatch or corruption")

    try:
        auth.delete("NONEXISTENT")
    except KeyNotFoundError:
        print("   ⚠️  Key not found — handled gracefully\n")

    # ── 4. Back up before key rotation ──
    print("4️⃣  Always backup before rotating keys")
    backup_path = auth.backup("security_backup.wauth")
    print(f"   ✅ Backup created: {backup_path}")

    # Rotate key
    results = auth.rotate_key("new-secure-key-2024")
    print(f"   ✅ Key rotated: {results}\n")

    # ── 5. Verify backup restore works ──
    print("5️⃣  Test backup restore")
    count = auth.restore(backup_path)
    print(f"   ✅ Restored {count} secrets from backup\n")

    # ── 6. Clean up: delete sensitive data when done ──
    print("6️⃣  Delete secrets when no longer needed")
    auth.delete("SESSION_TOKEN")
    print("   ✅ Temporary token deleted")

    # Clean up
    for key in auth.list_keys():
        auth.delete(key)
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(backup_path):
        os.remove(backup_path)


if __name__ == "__main__":
    main()
