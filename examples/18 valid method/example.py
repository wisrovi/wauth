"""Example 18: Using valid() method for secure secret verification.

This example demonstrates how to verify secrets without exposing them.
"""

from wauth import WAuth

DB_PATH_DISK = "example_valid.db"

def main() -> None:
    """Run the valid() method example."""
    auth = WAuth(db_path=DB_PATH_DISK)

    # Store a secret (setup - typically done once, outside of source code)
    REAL_TOKEN = "7483920:ABC-DEF-GHI"
    auth.set("TELEGRAM_TOKEN", REAL_TOKEN)
    print("Secret stored successfully")

    # UNSAFE: Using get() exposes the secret in your code
    # token = auth.get("TELEGRAM_TOKEN")  # DON'T DO THIS in production
    # print(f"Retrieved token: {token}")  # Secret is now in memory/logs

    # SAFE: Using valid() never exposes the secret
    user_input = input("Enter your Telegram token: ")
    if auth.valid("TELEGRAM_TOKEN", user_input):
        print("✓ Token is VALID - access granted")
    else:
        print("✗ Token is INVALID - access denied")

    # The secret never leaves the wauth library
    print("\nSecurity note: The secret was never exposed in this process")

    # Cleanup
    import os
    if os.path.exists(DB_PATH_DISK):
        os.remove(DB_PATH_DISK)

if __name__ == "__main__":
    main()
