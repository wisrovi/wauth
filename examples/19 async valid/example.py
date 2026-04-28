"""Example 19: Using async_valid() for async secret verification."""

import asyncio
from wauth import WAuth

DB_PATH_DISK = "example_async_valid.db"

async def verify_credentials(username: str, password: str) -> bool:
    """Verify user credentials using async_valid()."""
    auth = WAuth(db_path=DB_PATH_DISK)
    
    # Check if password matches stored value
    return await auth.async_valid(f"USER_{username}", password)

async def main() -> None:
    """Run the async valid() example."""
    auth = WAuth(db_path=DB_PATH_DISK)

    # Setup: Store user passwords (done once)
    auth.set("USER_alice", "alice-secret-123")
    auth.set("USER_bob", "bob-secret-456")
    print("User secrets stored")

    # Simulate login attempts
    test_cases = [
        ("alice", "alice-secret-123", True),
        ("alice", "wrong-password", False),
        ("bob", "bob-secret-456", True),
        ("charlie", "any-password", False),  # User doesn't exist
    ]

    for username, password, expected in test_cases:
        result = await verify_credentials(username, password)
        status = "✓ VALID" if result else "✗ INVALID"
        print(f"Login {username}: {status} (expected: {'VALID' if expected else 'INVALID'})")

    # Cleanup
    import os
    if os.path.exists(DB_PATH_DISK):
        os.remove(DB_PATH_DISK)

if __name__ == "__main__":
    asyncio.run(main())
