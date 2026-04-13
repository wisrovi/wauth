"""Example: web application integration (FastAPI pattern).

Demonstrates how WAuth fits into a web application, managing
API keys, session tokens, and database credentials.
"""

import os
import time
from dataclasses import dataclass

from wauth import WAuth


@dataclass
class AppConfig:
    """Application configuration managed via WAuth."""

    database_url: str
    redis_url: str
    api_key: str
    debug: bool


def load_config(auth: WAuth) -> AppConfig:
    """Load application configuration from encrypted vault.

    Args:
        auth: WAuth instance.

    Returns:
        Application configuration object.
    """
    return AppConfig(
        database_url=auth.get("DATABASE_URL") or "",
        redis_url=auth.get("REDIS_URL") or "",
        api_key=auth.get("API_KEY") or "",
        debug=auth.get("DEBUG") == "true",
    )


def save_config(auth: WAuth, config: AppConfig) -> None:
    """Save application configuration to encrypted vault.

    Args:
        auth: WAuth instance.
        config: Configuration to encrypt and store.
    """
    auth.set("DATABASE_URL", config.database_url)
    auth.set("REDIS_URL", config.redis_url)
    auth.set("API_KEY", config.api_key)
    auth.set("DEBUG", str(config.debug).lower())


def main() -> None:
    """Run the web application integration example."""
    db_path = "example_webapp.db"
    auth = WAuth(db_path=db_path, custom_key="webapp-secret-key")

    print("── Web Application Configuration ──\n")

    # ── Save configuration ──
    print("📝 Saving application configuration...")
    config = AppConfig(
        database_url="postgresql://app_user:s3cret@db:5432/myapp",
        redis_url="redis://redis:6379/0",
        api_key="sk-webapp-2024-abcdef",
        debug=False,
    )
    save_config(auth, config)
    print("   ✅ Configuration encrypted and stored\n")

    # ── Load configuration ──
    print("📂 Loading application configuration...")
    loaded_config = load_config(auth)
    print(f"   DATABASE_URL: {loaded_config.database_url}")
    print(f"   REDIS_URL: {loaded_config.redis_url}")
    print(f"   API_KEY: {loaded_config.api_key}")
    print(f"   DEBUG: {loaded_config.debug}\n")

    # ── Session token management ──
    print("── Session Token Management ──")
    auth.set("session:user_123", "jwt-token-abc", ttl=1800)  # 30 min
    print("✅ Session token created with 30-min TTL")

    token = auth.get("session:user_123")
    assert token == "jwt-token-abc"
    print(f"✅ Session retrieved: {token}\n")

    # ── Rotate API key ──
    print("── API Key Rotation ──")
    old_key = auth.get("API_KEY")
    auth.set("API_KEY", "sk-webapp-2024-rotated")
    new_key = auth.get("API_KEY")
    print(f"   Old: {old_key}")
    print(f"   New: {new_key}")
    assert old_key != new_key
    print("   ✅ API key rotated\n")

    # ── List all secrets ──
    print(f"📋 Vault contains {len(auth.list_keys())} secrets:")
    for key in auth.list_keys():
        print(f"   - {key}")

    # Clean up
    for key in auth.list_keys():
        auth.delete(key)
    if os.path.exists(db_path):
        os.remove(db_path)


if __name__ == "__main__":
    main()
