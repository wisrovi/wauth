"""Example: Docker secrets integration.

Demonstrates how WAuth reads Docker secrets when running inside a
container, with automatic fallback to the local vault.
"""

import os
import tempfile

from wauth import WAuth
from wauth.drivers import DriverFactory


def main() -> None:
    """Run the Docker secrets example."""
    print("── Docker Driver ──")

    # ── Simulate Docker secrets locally ──
    secrets_dir = tempfile.mkdtemp()
    db_password = os.path.join(secrets_dir, "db_password")
    api_key = os.path.join(secrets_dir, "api_key")

    with open(db_password, "w", encoding="utf-8") as f:
        f.write("super-secret-db-pass\n")
    with open(api_key, "w", encoding="utf-8") as f:
        f.write("sk-api-key-12345\n")

    # Create DockerDriver pointing to our temp directory
    from wauth.drivers.docker import DockerDriver

    docker_driver = DockerDriver(secrets_path=secrets_dir)

    # Read Docker secrets
    db_pass = docker_driver.get_secret("db_password")
    print(f"✅ Docker secret (db_password): {db_pass}")

    api = docker_driver.get_secret("api_key")
    print(f"✅ Docker secret (api_key): {api}")

    # Missing Docker secret returns None
    missing = docker_driver.get_secret("nonexistent")
    assert missing is None
    print(f"✅ Missing Docker secret returns None: {missing}")

    # ── DriverFactory (auto-detect) ──
    print("\n── DriverFactory ──")
    factory = DriverFactory()

    # Outside Docker, it falls back to local vault
    is_docker = factory.docker.is_docker()
    print(f"Running inside Docker container: {is_docker}")

    # Set a value via local vault
    db_path = "example_docker.db"
    auth = WAuth(db_path=db_path)
    auth.set("LOCAL_SECRET", "local-value")

    # Get via factory (falls back to local since we're not in Docker)
    value = factory.get_value("LOCAL_SECRET")
    print(f"✅ Factory get_value (local fallback): {value}")

    # Clean up
    os.remove(db_password)
    os.remove(api_key)
    os.rmdir(secrets_dir)
    if os.path.exists(db_path):
        os.remove(db_path)


if __name__ == "__main__":
    main()
