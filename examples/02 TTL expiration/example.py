"""Example: secrets with time-to-live (TTL).

Demonstrates how to store secrets that automatically expire after
a specified number of seconds.
"""

import os
import time

from wauth import WAuth


def main() -> None:
    """Run the TTL example."""
    db_path = "example_ttl.db"
    auth = WAuth(db_path=db_path)

    # ── Secret with 1-second TTL ──
    auth.set("SESSION_TOKEN", "abc-123-def", ttl=1.0)
    token = auth.get("SESSION_TOKEN")
    assert token == "abc-123-def"
    print("✅ Token retrieved before expiration:", token)

    # Wait for expiration
    print("⏳ Waiting 1.5 seconds for TTL expiration...")
    time.sleep(1.5)

    token = auth.get("SESSION_TOKEN")
    assert token is None
    print("✅ Token correctly expired (returned None)")

    # ── Secret without TTL (permanent) ──
    auth.set("API_KEY", "sk-permanent")
    print("⏳ Waiting 1.5 seconds...")
    time.sleep(1.5)

    key = auth.get("API_KEY")
    assert key == "sk-permanent"
    print("✅ Permanent secret still available after wait:", key)

    # Clean up
    auth.delete("API_KEY")
    if os.path.exists(db_path):
        os.remove(db_path)


if __name__ == "__main__":
    main()
