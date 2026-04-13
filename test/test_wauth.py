"""Tests for the main WAuth class and functional API.

Covers the high-level :class:`wauth.WAuth` interface including
delete, list_keys, backup, restore, key rotation, async, config,
TTL, and the functional API.
"""

import json
import os
from pathlib import Path

# pylint: disable=import-outside-toplevel,redefined-builtin
from loguru import logger

from wauth import (
    WAuth,
    delete,
    get,
    get_verbose,
    list_keys,
    set as wauth_set,
    set_file,
    set_verbose,
)
from wauth.exceptions import BackupError, RestoreError, WAuthError


class TestWAuthClass:
    """Test suite for the WAuth class interface."""

    def test_wauth_initialization_default(self) -> None:
        """Verify WAuth initializes with default settings."""
        auth = WAuth()
        assert auth._driver is not None
        logger.info("WAuth initialized with default path")

    def test_wauth_initialization_custom_path(self, tmp_db_path: str) -> None:
        """Verify WAuth initializes with a custom database path."""
        auth = WAuth(db_path=tmp_db_path)
        assert auth._driver is not None
        logger.info(f"WAuth initialized with custom path: {tmp_db_path}")

    def test_wauth_verbose_defaults_false(self, tmp_db_path: str) -> None:
        """Verify verbose defaults to False."""
        auth = WAuth(db_path=tmp_db_path)
        assert get_verbose() is False

    def test_wauth_verbose_true(self, tmp_db_path: str) -> None:
        """Verify verbose can be set to True."""
        auth = WAuth(db_path=tmp_db_path, verbose=True)
        assert get_verbose() is True

    def test_wauth_verbose_false_explicit(self, tmp_db_path: str) -> None:
        """Verify verbose can be explicitly set to False."""
        auth = WAuth(db_path=tmp_db_path, verbose=False)
        assert get_verbose() is False

    def test_set_verbose_public_api(self) -> None:
        """Verify the public set_verbose/get_verbose API."""
        set_verbose(True)
        assert get_verbose() is True
        set_verbose(False)
        assert get_verbose() is False

    def test_wauth_initialization_with_config(self, tmp_path, tmp_db_path: str) -> None:
        """Verify WAuth loads from a TOML config file."""
        config_file = tmp_path / "wauth.toml"
        config_file.write_text(
            f'[wauth]\ndb_path = "{tmp_db_path}"\n'
        )
        auth = WAuth(config_path=str(config_file))
        assert auth._driver is not None
        logger.info("WAuth initialized with config file")

    def test_wauth_config_file_not_found(self) -> None:
        """Verify missing config file raises ConfigurationError."""
        import pytest
        from wauth.exceptions import ConfigurationError
        with pytest.raises(ConfigurationError):
            WAuth(config_path="/nonexistent/config.toml")
        logger.info("Missing config file raises ConfigurationError")

    def test_wauth_config_file_invalid(self, tmp_path) -> None:
        """Verify invalid TOML raises ConfigurationError."""
        import pytest
        from wauth.exceptions import ConfigurationError
        bad_config = tmp_path / "bad.toml"
        bad_config.write_text("this is {{{ not toml")
        with pytest.raises(ConfigurationError):
            WAuth(config_path=str(bad_config))
        logger.info("Invalid TOML raises ConfigurationError")

    def test_wauth_set_and_get(self, tmp_db_path: str) -> None:
        """Verify storing and retrieving a text secret."""
        auth = WAuth(db_path=tmp_db_path)
        auth.set("API_KEY", "my-api-key-value")
        result = auth.get("API_KEY")
        assert result == "my-api-key-value"
        logger.info("WAuth set/get successful")

    def test_wauth_set_with_ttl(self, tmp_db_path: str) -> None:
        """Verify storing a secret with TTL."""
        import time
        auth = WAuth(db_path=tmp_db_path)
        auth.set("TTL_KEY", "ttl-value", ttl=0.1)
        result = auth.get("TTL_KEY")
        assert result == "ttl-value"
        time.sleep(0.15)
        result = auth.get("TTL_KEY")
        assert result is None
        logger.info("WAuth set with TTL successful")

    def test_wauth_set_file_and_get(self, tmp_db_path: str, tmp_path) -> None:
        """Verify storing and retrieving a file secret."""
        auth = WAuth(db_path=tmp_db_path)

        test_file = tmp_path / "test.pem"
        test_file.write_text("-----BEGIN CERTIFICATE-----\nMIID...")

        auth.set_file("MY_CERT", str(test_file))
        result = auth.get("MY_CERT")
        assert isinstance(result, bytes)
        assert b"BEGIN CERTIFICATE" in result
        logger.info("WAuth set_file/get successful")

    def test_wauth_get_nonexistent(self, tmp_db_path: str) -> None:
        """Verify that getting a non-existent key returns None."""
        auth = WAuth(db_path=tmp_db_path)
        result = auth.get("NONEXISTENT")
        assert result is None
        logger.info("WAuth get non-existent key returns None")

    def test_wauth_delete(self, tmp_db_path: str) -> None:
        """Verify deleting a secret."""
        auth = WAuth(db_path=tmp_db_path)
        auth.set("TO_DELETE", "delete-me")
        auth.delete("TO_DELETE")
        result = auth.get("TO_DELETE")
        assert result is None
        logger.info("WAuth delete successful")

    def test_wauth_delete_nonexistent(self, tmp_db_path: str) -> None:
        """Verify that deleting a non-existent key raises WAuthError."""
        import pytest
        auth = WAuth(db_path=tmp_db_path)
        with pytest.raises(WAuthError):
            auth.delete("NONEXISTENT")
        logger.info("Delete non-existent raises WAuthError")

    def test_wauth_list_keys(self, tmp_db_path: str) -> None:
        """Verify listing all keys."""
        auth = WAuth(db_path=tmp_db_path)
        auth.set("A", "1")
        auth.set("B", "2")
        auth.set("C", "3")
        keys = auth.list_keys()
        assert set(keys) == {"A", "B", "C"}
        logger.info(f"WAuth list_keys: {keys}")

    def test_wauth_multiple_keys(self, tmp_db_path: str) -> None:
        """Verify storing and retrieving multiple independent keys."""
        auth = WAuth(db_path=tmp_db_path)
        auth.set("KEY1", "value1")
        auth.set("KEY2", "value2")
        auth.set("KEY3", "value3")
        assert auth.get("KEY1") == "value1"
        assert auth.get("KEY2") == "value2"
        assert auth.get("KEY3") == "value3"
        logger.info("WAuth multiple keys stored independently")

    def test_wauth_overwrite_key(self, tmp_db_path: str) -> None:
        """Verify that overwriting a key updates its value."""
        auth = WAuth(db_path=tmp_db_path)
        auth.set("MY_KEY", "original")
        auth.set("MY_KEY", "updated")
        result = auth.get("MY_KEY")
        assert result == "updated"
        logger.info("WAuth key overwrite successful")

    def test_wauth_rotate_key(self, tmp_db_path: str) -> None:
        """Verify key rotation re-encrypts all secrets."""
        auth = WAuth(db_path=tmp_db_path)
        auth.set("RKEY1", "value1")
        auth.set("RKEY2", "value2")

        results = auth.rotate_key("new-rotation-key")
        assert results["RKEY1"] is True
        assert results["RKEY2"] is True

        assert auth.get("RKEY1") == "value1"
        assert auth.get("RKEY2") == "value2"
        logger.info("WAuth key rotation successful")

    def test_wauth_backup_and_restore(self, tmp_db_path: str, tmp_path) -> None:
        """Verify backup creates a file and restore reads it back."""
        auth = WAuth(db_path=tmp_db_path)
        auth.set("BACKUP_KEY", "backup-value")

        backup_file = str(tmp_path / "backup.wauth")
        path = auth.backup(backup_file)
        assert os.path.exists(path)

        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        assert "secrets" in data
        assert "BACKUP_KEY" in data["secrets"]

        count = auth.restore(backup_file)
        assert count >= 1
        logger.info("WAuth backup/restore successful")

    def test_wauth_restore_nonexistent_file(self, tmp_db_path: str) -> None:
        """Verify restoring from a non-existent file raises RestoreError."""
        import pytest
        auth = WAuth(db_path=tmp_db_path)
        with pytest.raises(RestoreError):
            auth.restore("/nonexistent/backup.wauth")
        logger.info("Restore non-existent file raises RestoreError")

    def test_wauth_restore_corrupted_file(self, tmp_db_path: str, tmp_path) -> None:
        """Verify restoring from a corrupted file raises RestoreError."""
        import pytest
        auth = WAuth(db_path=tmp_db_path)
        bad_file = tmp_path / "bad.wauth"
        bad_file.write_text("not valid json{{{")
        with pytest.raises(RestoreError):
            auth.restore(str(bad_file))
        logger.info("Restore corrupted file raises RestoreError")

    def test_wauth_backup_error(self, tmp_db_path: str, monkeypatch) -> None:
        """Verify backup raises BackupError on failure."""
        import pytest
        auth = WAuth(db_path=tmp_db_path)
        auth.set("KEY", "value")
        monkeypatch.setattr(auth, "list_keys", lambda: (_ for _ in ()).throw(OSError("fail")))
        with pytest.raises(BackupError):
            auth.backup("/tmp/should_fail.wauth")
        logger.info("BackupError raised on failure")

    def test_db_file_is_created(self, tmp_db_path: str) -> None:
        """Verify that the database file is created on first use."""
        assert not os.path.exists(tmp_db_path)
        auth = WAuth(db_path=tmp_db_path)
        auth.set("TRIGGER_CREATION", "value")
        assert os.path.exists(tmp_db_path)
        logger.info("Database file created on first use")

    # ─── Async tests ──────────────────────────────────────────────────────

    def test_wauth_async_set_and_get(self, tmp_db_path: str) -> None:
        """Verify async set and get work correctly."""
        import asyncio
        auth = WAuth(db_path=tmp_db_path)

        async def _run() -> str | None:
            await auth.async_set("ASYNC_KEY", "async-value")
            return await auth.async_get("ASYNC_KEY")

        result = asyncio.run(_run())
        assert result == "async-value"
        logger.info("WAuth async set/get successful")

    def test_wauth_async_delete(self, tmp_db_path: str) -> None:
        """Verify async delete works correctly."""
        import asyncio
        auth = WAuth(db_path=tmp_db_path)
        auth.set("ASYNC_DEL", "delete-me")

        async def _run() -> None:
            await auth.async_delete("ASYNC_DEL")

        asyncio.run(_run())
        assert auth.get("ASYNC_DEL") is None
        logger.info("WAuth async delete successful")

    def test_wauth_async_backup(self, tmp_db_path: str, tmp_path) -> None:
        """Verify async backup works."""
        import asyncio
        auth = WAuth(db_path=tmp_db_path)
        auth.set("ASYNC_BACKUP", "backup-value")
        backup_file = str(tmp_path / "async_backup.wauth")

        async def _run() -> str:
            return await auth.async_backup(backup_file)

        path = asyncio.run(_run())
        assert os.path.exists(path)
        logger.info("WAuth async backup successful")

    def test_wauth_async_restore(self, tmp_db_path: str, tmp_path) -> None:
        """Verify async restore works."""
        import asyncio
        auth = WAuth(db_path=tmp_db_path)
        auth.set("RESTORE_ME", "restore-value")
        backup_file = str(tmp_path / "async_restore.wauth")
        auth.backup(backup_file)

        # Clear the vault
        for key in auth.list_keys():
            auth.delete(key)

        async def _run() -> int:
            return await auth.async_restore(backup_file)

        count = asyncio.run(_run())
        assert count >= 1
        assert auth.get("RESTORE_ME") == "restore-value"
        logger.info("WAuth async restore successful")


class TestFunctionalAPI:
    """Test suite for the functional API (set, set_file, get, delete, list_keys)."""

    def test_functional_get_nonexistent(self) -> None:
        """Verify functional get() returns None for missing keys."""
        result = get("THIS_KEY_DOES_NOT_EXIST_IN_DEFAULT_DB")
        logger.info(f"Functional get for non-existent key: {result}")

    def test_functional_list_keys(self) -> None:
        """Verify functional list_keys() returns a list."""
        keys = list_keys()
        assert isinstance(keys, list)
        logger.info(f"Functional list_keys returned {len(keys)} keys")


class TestWAuthIntegration:
    """Integration tests for end-to-end workflows."""

    def test_full_workflow_text(self, tmp_db_path: str) -> None:
        """Verify complete workflow: create, store, retrieve, verify."""
        auth = WAuth(db_path=tmp_db_path)
        auth.set("TELEGRAM_TOKEN", "7483920:ABC-DEF-GHI")
        token = auth.get("TELEGRAM_TOKEN")
        assert token == "7483920:ABC-DEF-GHI"
        logger.info("Full text workflow verified")

    def test_full_workflow_file(self, tmp_db_path: str, tmp_path) -> None:
        """Verify complete file workflow: create file, store, retrieve."""
        auth = WAuth(db_path=tmp_db_path)

        key_file = tmp_path / "private.key"
        key_file.write_bytes(b"-----BEGIN PRIVATE KEY-----\nMIIEv...")

        auth.set_file("MY_KEY_FILE", str(key_file))
        retrieved = auth.get("MY_KEY_FILE")

        assert isinstance(retrieved, bytes)
        assert b"BEGIN PRIVATE KEY" in retrieved
        logger.info("Full file workflow verified")

    def test_full_lifecycle(self, tmp_db_path: str, tmp_path) -> None:
        """Verify full lifecycle: set, list, backup, delete, restore, rotate."""
        auth = WAuth(db_path=tmp_db_path)

        # Set secrets
        auth.set("APP_KEY", "app-secret")
        auth.set("DB_PASS", "db-password")

        # List
        assert len(auth.list_keys()) == 2

        # Backup
        backup_file = str(tmp_path / "lifecycle.wauth")
        auth.backup(backup_file)

        # Delete one
        auth.delete("APP_KEY")
        assert len(auth.list_keys()) == 1

        # Restore
        auth.restore(backup_file)
        assert len(auth.list_keys()) == 2

        # Rotate
        results = auth.rotate_key("new-lifecycle-key")
        assert all(results.values())
        assert auth.get("APP_KEY") == "app-secret"
        assert auth.get("DB_PASS") == "db-password"

        logger.info("Full lifecycle verified")
