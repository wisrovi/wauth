"""Example: logging integration.

Demonstrates how to configure loguru for WAuth's built-in logging
and capture structured diagnostic output.
"""

import os
import sys

from loguru import logger

from wauth import WAuth


def main() -> None:
    """Run the logging example."""
    db_path = "example_logging.db"

    # ── Configure loguru ──
    # Remove default handler and set up custom logging
    logger.remove()

    # Log to console with INFO level
    logger.add(sys.stderr, level="DEBUG", format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")

    # ── Use WAuth (log output appears on stderr) ──
    print("── WAuth with DEBUG logging enabled ──\n")

    auth = WAuth(db_path=db_path)
    auth.set("LOGGED_KEY", "logged-value")
    value = auth.get("LOGGED_KEY")
    print(f"\n✅ Retrieved: {value}")

    auth.delete("LOGGED_KEY")
    if os.path.exists(db_path):
        os.remove(db_path)


if __name__ == "__main__":
    main()
