"""Tests for the Vault and SecretModel modules.

Covers Pydantic model validation, CRUD operations, TTL, listing,
counting, and persistence for the :mod:`wauth.vault` module.
"""

# pylint: disable=import-outside-toplevel
import time

import pytest
from loguru import logger

from wauth.exceptions import KeyNotFoundError, VaultError
from wauth.vault import SecretModel, Vault


class TestSecretModel:
    """Test suite for the SecretModel Pydantic model."""

    def test_model_creation_defaults(self) -> None:
        """Verify default values for SecretModel."""
        secret = SecretModel(key="MY_KEY", value="encrypted-value")
        assert secret.key == "MY_KEY"
        assert secret.value == "encrypted-value"
        assert secret.type == "text"
        assert secret.created_at == 0.0
        assert secret.updated_at == 0.0
        assert secret.ttl is None
        logger.info("SecretModel created with all defaults")

    def test_model_creation_with_file_type(self) -> None:
        """Verify explicit file type assignment."""
        secret = SecretModel(key="MY_KEY", value="encrypted-value", type="file")
        assert secret.type == "file"
        logger.info("SecretModel created with type='file'")

    def test_model_with_ttl(self) -> None:
        """Verify TTL can be set on the model."""
        secret = SecretModel(
            key="EXPIRING_KEY", value="enc", ttl=3600.0
        )
        assert secret.ttl == 3600.0
        logger.info("SecretModel created with TTL=3600")

    def test_model_validation_error_missing_key(self) -> None:
        """Verify that missing required fields raise validation errors."""
        with pytest.raises(Exception):  # noqa: PT011
            SecretModel(value="encrypted-value")  # type: ignore[call-arg]
        logger.info("Missing key correctly raises validation error")

    def test_model_validation_error_missing_value(self) -> None:
        """Verify that missing value field raises validation error."""
        with pytest.raises(Exception):  # noqa: PT011
            SecretModel(key="MY_KEY")  # type: ignore[call-arg]
        logger.info("Missing value correctly raises validation error")

    def test_model_dump(self) -> None:
        """Verify model serialization to dictionary."""
        secret = SecretModel(
            key="API_KEY", value="enc-123", type="text",
            created_at=100.0, updated_at=200.0,
        )
        dumped = secret.model_dump()
        assert dumped["key"] == "API_KEY"
        assert dumped["value"] == "enc-123"
        assert dumped["type"] == "text"
        logger.info("SecretModel serialization successful")


class TestVault:
    """Test suite for the Vault storage class."""

    def test_vault_initialization(self, tmp_db_path: str) -> None:
        """Verify vault initializes and creates the database directory."""
        vault = Vault(db_path=tmp_db_path)
        assert vault.db_path == tmp_db_path
        assert vault.db is not None
        logger.info("Vault initialized successfully")

    def test_vault_expands_user_path(self) -> None:
        """Verify that user home path expansion works."""
        vault = Vault(db_path="~/test_vault.db")
        assert "~" not in vault.db_path
        assert vault.db_path.startswith("/")
        logger.info(f"User path expanded to: {vault.db_path}")

    def test_save_and_get_text_secret(self, tmp_db_path: str) -> None:
        """Verify saving and retrieving a text secret."""
        vault = Vault(db_path=tmp_db_path)
        vault.save("TEST_KEY", "encrypted-value-123", "text")
        value, v_type = vault.get("TEST_KEY")
        assert value == "encrypted-value-123"
        assert v_type == "text"
        logger.info("Text secret save/get successful")

    def test_save_and_get_file_secret(self, tmp_db_path: str) -> None:
        """Verify saving and retrieving a file secret."""
        vault = Vault(db_path=tmp_db_path)
        vault.save("FILE_KEY", "encrypted-file-data", "file")
        value, v_type = vault.get("FILE_KEY")
        assert value == "encrypted-file-data"
        assert v_type == "file"
        logger.info("File secret save/get successful")

    def test_get_nonexistent_key(self, tmp_db_path: str) -> None:
        """Verify that getting a non-existent key returns (None, None)."""
        vault = Vault(db_path=tmp_db_path)
        value, v_type = vault.get("DOES_NOT_EXIST")
        assert value is None
        assert v_type is None
        logger.info("Non-existent key correctly returns (None, None)")

    def test_upsert_replaces_existing_key(self, tmp_db_path: str) -> None:
        """Verify that saving the same key updates the value."""
        vault = Vault(db_path=tmp_db_path)
        vault.save("MY_KEY", "first-value", "text")
        vault.save("MY_KEY", "updated-value", "text")
        value, v_type = vault.get("MY_KEY")
        assert value == "updated-value"
        assert v_type == "text"
        logger.info("Key upsert successful")

    def test_multiple_keys_coexist(self, tmp_db_path: str) -> None:
        """Verify that multiple keys can be stored independently."""
        vault = Vault(db_path=tmp_db_path)
        vault.save("KEY1", "value1", "text")
        vault.save("KEY2", "value2", "file")
        val1, type1 = vault.get("KEY1")
        val2, type2 = vault.get("KEY2")
        assert val1 == "value1" and type1 == "text"
        assert val2 == "value2" and type2 == "file"
        logger.info("Multiple keys stored independently")

    def test_delete_existing_key(self, tmp_db_path: str) -> None:
        """Verify that deleting a key removes it from the vault."""
        vault = Vault(db_path=tmp_db_path)
        vault.save("TO_DELETE", "encrypted", "text")
        vault.delete("TO_DELETE")
        value, v_type = vault.get("TO_DELETE")
        assert value is None and v_type is None
        logger.info("Key deleted successfully")

    def test_delete_nonexistent_key_raises(self, tmp_db_path: str) -> None:
        """Verify that deleting a non-existent key raises KeyNotFoundError."""
        vault = Vault(db_path=tmp_db_path)
        with pytest.raises(KeyNotFoundError):
            vault.delete("NONEXISTENT")
        logger.info("Delete non-existent key raises KeyNotFoundError")

    def test_list_keys(self, tmp_db_path: str) -> None:
        """Verify that list_keys returns all stored key names."""
        vault = Vault(db_path=tmp_db_path)
        vault.save("A", "v1", "text")
        vault.save("B", "v2", "text")
        vault.save("C", "v3", "text")
        keys = vault.list_keys()
        assert set(keys) == {"A", "B", "C"}
        logger.info(f"Listed keys: {keys}")

    def test_count(self, tmp_db_path: str) -> None:
        """Verify that count returns the correct number of secrets."""
        vault = Vault(db_path=tmp_db_path)
        assert vault.count() == 0
        vault.save("K1", "v1", "text")
        vault.save("K2", "v2", "text")
        assert vault.count() == 2
        logger.info("Vault count is correct")

    def test_vault_with_special_characters(self, tmp_db_path: str) -> None:
        """Verify handling of special characters in keys and values."""
        vault = Vault(db_path=tmp_db_path)
        vault.save("KEY-WITH-DASH", "value:with/special=chars", "text")
        value, v_type = vault.get("KEY-WITH-DASH")
        assert value == "value:with/special=chars"
        assert v_type == "text"
        logger.info("Special characters handled correctly")

    def test_ttl_expiration(self, tmp_db_path: str) -> None:
        """Verify that expired secrets return (None, None)."""
        import time
        vault = Vault(db_path=tmp_db_path)
        vault.save("EXPIRED_KEY", "encrypted", "text", ttl=0.05)
        time.sleep(0.1)
        value, v_type = vault.get("EXPIRED_KEY")
        assert value is None
        assert v_type is None
        logger.info("Expired secret correctly returns (None, None)")

    def test_save_triggers_vault_error(self, tmp_db_path: str, monkeypatch) -> None:
        """Verify that save raises VaultError on database failure."""
        vault = Vault(db_path=tmp_db_path)
        # Force the context manager to raise
        monkeypatch.setattr(
            vault.db,
            "_get_connection",
            lambda: (_ for _ in ()).throw(OSError("disk full")),
        )
        with pytest.raises(VaultError):
            vault.save("FAIL_KEY", "value", "text")
        logger.info("VaultError raised on save failure")

    def test_get_triggers_vault_error(self, tmp_db_path: str, monkeypatch) -> None:
        """Verify that get raises VaultError on database failure."""
        vault = Vault(db_path=tmp_db_path)
        monkeypatch.setattr(
            vault.db,
            "_get_connection",
            lambda: (_ for _ in ()).throw(OSError("disk full")),
        )
        # get_by_field uses db internally — mock it
        monkeypatch.setattr(vault.db, "get_by_field", lambda **kw: (_ for _ in ()).throw(OSError("fail")))
        with pytest.raises(VaultError):
            vault.get("ANY_KEY")
        logger.info("VaultError raised on get failure")

    def test_delete_triggers_vault_error(self, tmp_db_path: str, monkeypatch) -> None:
        """Verify that delete raises VaultError on database failure."""
        vault = Vault(db_path=tmp_db_path)
        monkeypatch.setattr(
            vault.db,
            "_get_connection",
            lambda: (_ for _ in ()).throw(OSError("disk full")),
        )
        with pytest.raises(VaultError):
            vault.delete("ANY_KEY")
        logger.info("VaultError raised on delete failure")

    def test_list_keys_triggers_vault_error(self, tmp_db_path: str, monkeypatch) -> None:
        """Verify that list_keys raises VaultError on database failure."""
        vault = Vault(db_path=tmp_db_path)
        monkeypatch.setattr(
            vault.db,
            "_get_connection",
            lambda: (_ for _ in ()).throw(OSError("disk full")),
        )
        with pytest.raises(VaultError):
            vault.list_keys()
        logger.info("VaultError raised on list_keys failure")

    def test_count_triggers_vault_error(self, tmp_db_path: str, monkeypatch) -> None:
        """Verify that count raises VaultError on database failure."""
        vault = Vault(db_path=tmp_db_path)
        monkeypatch.setattr(
            vault.db,
            "_get_connection",
            lambda: (_ for _ in ()).throw(OSError("disk full")),
        )
        with pytest.raises(VaultError):
            vault.count()
        logger.info("VaultError raised on count failure")
