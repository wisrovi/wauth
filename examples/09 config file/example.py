"""Example: TOML configuration file.

Demonstrates how to configure WAuth via a TOML file instead of
passing parameters programmatically.
"""

import os
import tempfile
from pathlib import Path

from wauth import WAuth


def main() -> None:
    """Run the TOML configuration example."""
    db_path = "example_config.db"

    # ── Create a TOML config file ──
    config_file = Path("wauth_config.toml")
    config_content = f"""
[wauth]
db_path = "{db_path}"
custom_key = "config-based-key-2024"
"""
    config_file.write_text(config_content)
    print(f"📝 Created config file: {config_file}")

    # ── Initialize WAuth from config ──
    print("\n🔧 Initializing WAuth from config file...")
    auth = WAuth(config_path=str(config_file))

    # Store and retrieve
    auth.set("CONFIG_TEST", "configured-via-toml")
    value = auth.get("CONFIG_TEST")
    assert value == "configured-via-toml"
    print(f"✅ Retrieved: {value}")

    # ── Bad config handling ──
    print("\n⚠️  Testing bad config handling...")
    bad_config = Path("bad_config.toml")
    bad_config.write_text("this is {{{ not valid toml }}}")

    try:
        WAuth(config_path=str(bad_config))
    except Exception as exc:
        print(f"✅ Caught expected error: {type(exc).__name__}")

    # Clean up
    auth.delete("CONFIG_TEST")
    if os.path.exists(db_path):
        os.remove(db_path)
    config_file.unlink()
    bad_config.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
