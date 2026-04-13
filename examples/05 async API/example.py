"""Example: async API usage.

Demonstrates the async methods for non-blocking secret operations
in async/await codebases (FastAPI, aiohttp, etc.).
"""

import asyncio
import os

from wauth import WAuth


async def main() -> None:
    """Run the async API example."""
    db_path = "example_async.db"
    auth = WAuth(db_path=db_path)
    # Clear any leftover data
    for k in auth.list_keys():
        auth.delete(k)

    # ── Async set and get ──
    print("🔄 Using async_set and async_get...")
    await auth.async_set("API_KEY", "async-secret-value")
    value = await auth.async_get("API_KEY")
    assert value == "async-secret-value"
    print(f"✅ Retrieved: {value}")

    # ── Async operations in a loop ──
    print("\n🔄 Setting multiple secrets concurrently...")
    tasks = [
        auth.async_set("KEY_1", "value_1"),
        auth.async_set("KEY_2", "value_2"),
        auth.async_set("KEY_3", "value_3"),
    ]
    await asyncio.gather(*tasks)
    print("✅ All secrets set concurrently")

    # ── Async list keys ──
    keys = auth.list_keys()
    print(f"\n📋 Vault keys: {keys}")

    # ── Async delete ──
    print("\n🔄 Deleting keys asynchronously...")
    await auth.async_delete("API_KEY")
    await auth.async_delete("KEY_1")
    await auth.async_delete("KEY_2")
    await auth.async_delete("KEY_3")
    assert auth.list_keys() == []
    print("✅ All keys deleted")

    # ── Async backup and restore ──
    auth.set("BACKUP_ME", "important-data")
    backup_file = "async_backup.wauth"
    print(f"\n🔄 Async backup to {backup_file}...")
    path = await auth.async_backup(backup_file)
    print(f"✅ Backup created at: {path}")

    auth.delete("BACKUP_ME")
    count = await auth.async_restore(backup_file)
    print(f"✅ Restored {count} secrets")

    assert auth.get("BACKUP_ME") == "important-data"

    # Clean up
    auth.delete("BACKUP_ME")
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(backup_file):
        os.remove(backup_file)


if __name__ == "__main__":
    asyncio.run(main())
