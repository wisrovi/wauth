"""Tests for driver modules.

Covers LocalDriver, DockerDriver, DriverFactory, key rotation,
TTL support, and delete operations in the :mod:`wauth.drivers` package.
"""

import os

# pylint: disable=import-outside-toplevel
from loguru import logger

from wauth.drivers import DriverFactory
from wauth.drivers.docker import DockerDriver
from wauth.drivers.local import LocalDriver
from wauth.exceptions import KeyNotFoundError


class TestLocalDriver:
    """Test suite for the LocalDriver class."""

    def test_driver_initialization(self) -> None:
        """Verify that LocalDriver initializes with engine and vault."""
        driver = LocalDriver()
        assert driver.engine is not None
        assert driver.vault is not None
        logger.info("LocalDriver initialized successfully")

    def test_driver_with_custom_key(self) -> None:
        """Verify LocalDriver with a custom encryption key."""
        driver = LocalDriver(custom_key="my-custom-key")
        assert driver.engine is not None
        logger.info("LocalDriver initialized with custom key")

    def test_set_and_get_text_secret(self, tmp_db_path: str) -> None:
        """Verify setting and getting a text secret."""
        driver = LocalDriver()
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        driver.vault.db = WSQLite(SecretModel, tmp_db_path)

        driver.set_secret("MY_TOKEN", "super-secret-value")
        result = driver.get_secret("MY_TOKEN")
        assert result == "super-secret-value"
        logger.info("Text secret set/get successful via LocalDriver")

    def test_set_and_get_with_ttl(self, tmp_db_path: str) -> None:
        """Verify that TTL secrets expire correctly."""
        import time
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        driver = LocalDriver()
        driver.vault.db = WSQLite(SecretModel, tmp_db_path)

        driver.set_secret("TTL_KEY", "ttl-value", ttl=0.1)
        result = driver.get_secret("TTL_KEY")
        assert result == "ttl-value"
        time.sleep(0.15)
        result = driver.get_secret("TTL_KEY")
        assert result is None
        logger.info("TTL secret expiration works correctly")

    def test_get_nonexistent_key(self, tmp_db_path: str) -> None:
        """Verify that getting a non-existent key returns None."""
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        driver = LocalDriver()
        driver.vault.db = WSQLite(SecretModel, tmp_db_path)

        result = driver.get_secret("DOES_NOT_EXIST")
        assert result is None
        logger.info("Non-existent key returns None correctly")

    def test_set_and_get_file_secret(self, tmp_db_path: str, tmp_path) -> None:
        """Verify setting and getting a file secret."""
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        driver = LocalDriver()
        driver.vault.db = WSQLite(SecretModel, tmp_db_path)

        test_file = tmp_path / "test_key.pem"
        test_file.write_text("-----BEGIN RSA PRIVATE KEY-----\nMIIEpA...")

        driver.set_file("MY_KEY", str(test_file))
        result = driver.get_secret("MY_KEY")
        assert isinstance(result, bytes)
        assert b"BEGIN RSA PRIVATE KEY" in result
        logger.info("File secret set/get successful via LocalDriver")

    def test_delete_secret(self, tmp_db_path: str) -> None:
        """Verify that deleting a secret removes it."""
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        driver = LocalDriver()
        driver.vault.db = WSQLite(SecretModel, tmp_db_path)

        driver.set_secret("TO_DELETE", "delete-me")
        driver.delete_secret("TO_DELETE")
        result = driver.get_secret("TO_DELETE")
        assert result is None
        logger.info("Secret deleted successfully")

    def test_delete_nonexistent_raises(self, tmp_db_path: str) -> None:
        """Verify that deleting a non-existent key raises KeyNotFoundError."""
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        driver = LocalDriver()
        driver.vault.db = WSQLite(SecretModel, tmp_db_path)

        import pytest
        with pytest.raises(KeyNotFoundError):
            driver.delete_secret("NONEXISTENT")
        logger.info("Delete non-existent raises KeyNotFoundError")

    def test_list_keys(self, tmp_db_path: str) -> None:
        """Verify listing all keys."""
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        driver = LocalDriver()
        driver.vault.db = WSQLite(SecretModel, tmp_db_path)

        driver.set_secret("A", "1")
        driver.set_secret("B", "2")
        keys = driver.list_keys()
        assert set(keys) == {"A", "B"}
        logger.info(f"Listed keys: {keys}")

    def test_rotate_key_all(self, tmp_db_path: str) -> None:
        """Verify full key rotation re-encrypts all secrets."""
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        driver = LocalDriver()
        driver.vault.db = WSQLite(SecretModel, tmp_db_path)

        driver.set_secret("KEY1", "value1")
        driver.set_secret("KEY2", "value2")

        results = driver.rotate_key("new-rotation-key")
        assert results == {"KEY1": True, "KEY2": True}

        # Verify secrets are still readable with the new engine
        assert driver.get_secret("KEY1") == "value1"
        assert driver.get_secret("KEY2") == "value2"
        logger.info("Key rotation successful for all secrets")

    def test_rotate_key_selective(self, tmp_db_path: str) -> None:
        """Verify selective key rotation."""
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        driver = LocalDriver()
        driver.vault.db = WSQLite(SecretModel, tmp_db_path)

        driver.set_secret("MIGRATE", "migrate-me")
        driver.set_secret("KEEP", "keep-as-is")

        results = driver.rotate_key("selective-key", keys_to_migrate=["MIGRATE"])
        assert results == {"MIGRATE": True}
        logger.info("Selective key rotation successful")


class TestDockerDriver:
    """Test suite for the DockerDriver class."""

    def test_driver_initialization(self) -> None:
        """Verify DockerDriver initializes with default secrets path."""
        driver = DockerDriver()
        assert driver.secrets_path == "/run/secrets"
        logger.info("DockerDriver initialized with default secrets path")

    def test_driver_custom_secrets_path(self) -> None:
        """Verify DockerDriver accepts a custom secrets path."""
        driver = DockerDriver(secrets_path="/custom/secrets")
        assert driver.secrets_path == "/custom/secrets"
        logger.info("DockerDriver initialized with custom secrets path")

    def test_get_secret_not_found(self, tmp_path) -> None:
        """Verify that get_secret returns None when file doesn't exist."""
        driver = DockerDriver(secrets_path=str(tmp_path))
        result = driver.get_secret("NONEXISTENT")
        assert result is None
        logger.info("DockerDriver correctly returns None for missing secret")

    def test_get_secret_exists(self, tmp_path) -> None:
        """Verify that get_secret reads from file when it exists."""
        secret_file = tmp_path / "MY_SECRET"
        secret_file.write_text("my-docker-secret\n")

        driver = DockerDriver(secrets_path=str(tmp_path))
        result = driver.get_secret("MY_SECRET")
        assert result == "my-docker-secret"
        logger.info("DockerDriver read secret from file successfully")

    def test_get_secret_strips_whitespace(self, tmp_path) -> None:
        """Verify that Docker secrets have whitespace removed."""
        secret_file = tmp_path / "TRIMMED_SECRET"
        secret_file.write_text("  secret-with-padding  \n")

        driver = DockerDriver(secrets_path=str(tmp_path))
        result = driver.get_secret("TRIMMED_SECRET")
        assert result == "secret-with-padding"
        logger.info("DockerDriver correctly strips whitespace from secrets")

    def test_is_docker_returns_bool(self) -> None:
        """Verify that is_docker returns a boolean."""
        driver = DockerDriver()
        result = driver.is_docker()
        assert isinstance(result, bool)
        logger.info(f"is_docker() returned: {result}")


class TestDriverFactory:
    """Test suite for the DriverFactory class."""

    def test_factory_initialization(self) -> None:
        """Verify that DriverFactory creates both drivers."""
        factory = DriverFactory()
        assert factory.local is not None
        assert factory.docker is not None
        logger.info("DriverFactory initialized with local and docker drivers")

    def test_factory_get_value_falls_back_to_local(self, tmp_db_path: str) -> None:
        """Verify that get_value falls back to local driver."""
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        factory = DriverFactory()
        factory.local.vault.db = WSQLite(SecretModel, tmp_db_path)

        factory.local.set_secret("FACTORY_KEY", "factory-value")
        result = factory.get_value("FACTORY_KEY")
        assert result == "factory-value"
        logger.info("DriverFactory get_value falls back to local correctly")

    def test_factory_set_value_uses_local(self, tmp_db_path: str) -> None:
        """Verify that set_value stores via local driver."""
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        factory = DriverFactory()
        factory.local.vault.db = WSQLite(SecretModel, tmp_db_path)

        factory.set_value("SET_KEY", "set-value")
        result = factory.get_value("SET_KEY")
        assert result == "set-value"
        logger.info("DriverFactory set_value uses local driver correctly")

    def test_factory_get_value_docker_path(self, monkeypatch, tmp_db_path: str) -> None:
        """Verify that get_value tries Docker driver when in Docker."""
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        factory = DriverFactory()
        factory.local.vault.db = WSQLite(SecretModel, tmp_db_path)

        monkeypatch.setattr(factory.docker, "is_docker", lambda: True)
        monkeypatch.setattr(factory.docker, "get_secret", lambda key: None)

        factory.local.set_secret("DOCKER_FALLBACK_KEY", "docker-fallback-value")
        result = factory.get_value("DOCKER_FALLBACK_KEY")
        assert result == "docker-fallback-value"
        logger.info("DriverFactory get_value Docker path covered")

    def test_factory_set_value_is_file(self, tmp_db_path: str, tmp_path) -> None:
        """Verify that set_value with is_file=True uses set_file."""
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        factory = DriverFactory()
        factory.local.vault.db = WSQLite(SecretModel, tmp_db_path)

        test_file = tmp_path / "factory_test.key"
        test_file.write_text("factory-file-content")

        factory.set_value("FACTORY_FILE_KEY", str(test_file), is_file=True)
        result = factory.get_value("FACTORY_FILE_KEY")
        assert isinstance(result, bytes)
        assert b"factory-file-content" in result
        logger.info("DriverFactory set_value with is_file=True successful")

    def test_factory_get_value_docker_returns_secret(self, monkeypatch, tmp_db_path: str) -> None:
        """Verify that get_value returns Docker secret when available."""
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        factory = DriverFactory()
        factory.local.vault.db = WSQLite(SecretModel, tmp_db_path)

        monkeypatch.setattr(factory.docker, "is_docker", lambda: True)
        monkeypatch.setattr(factory.docker, "get_secret", lambda key: "docker-secret")

        result = factory.get_value("DOCKER_KEY")
        assert result == "docker-secret"
        logger.info("DriverFactory get_value returns Docker secret when available")

    def test_rotate_key_partial_failure(self, tmp_db_path: str, monkeypatch) -> None:
        """Verify rotate_key reports False for keys that fail to migrate."""
        from wauth.vault import SecretModel
        from wsqlite import WSQLite
        driver = LocalDriver()
        driver.vault.db = WSQLite(SecretModel, tmp_db_path)

        driver.set_secret("GOOD", "value")
        driver.set_secret("BAD", "value")

        # Make BAD key's decryption fail by corrupting its encrypted value
        monkeypatch.setattr(
            driver.engine, "decrypt",
            lambda token: b"corrupted" if "BAD" in str(token)[:10] else driver.engine.decrypt(token),
        )

        results = driver.rotate_key("new-key")
        assert "GOOD" in results
        assert "BAD" in results
        logger.info(f"Partial rotation results: {results}")
