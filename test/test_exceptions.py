"""Tests for the exception hierarchy.

Verifies that all custom exceptions inherit from the correct base
class and can be caught at different levels of the hierarchy.
"""

import pytest
from loguru import logger

from wauth.exceptions import (
    BackupError,
    ConfigurationError,
    DecryptionError,
    KeyNotFoundError,
    RestoreError,
    RotationError,
    VaultError,
    WAuthError,
)


class TestExceptionHierarchy:
    """Verify the inheritance structure of WAuth exceptions."""

    def test_all_exceptions_inherit_from_wauth_error(self) -> None:
        """Verify every custom exception is a subclass of WAuthError."""
        subclasses = [
            KeyNotFoundError,
            DecryptionError,
            VaultError,
            BackupError,
            RestoreError,
            RotationError,
            ConfigurationError,
        ]
        for exc_class in subclasses:
            assert issubclass(exc_class, WAuthError), (
                f"{exc_class.__name__} does not inherit WAuthError"
            )
        logger.info("All exceptions inherit from WAuthError")

    def test_wauth_error_is_exception(self) -> None:
        """Verify WAuthError inherits from Exception."""
        assert issubclass(WAuthError, Exception)
        logger.info("WAuthError is an Exception subclass")

    def test_can_catch_all_with_wauth_error(self) -> None:
        """Verify that catching WAuthError catches any subclass."""
        for exc_class in [
            KeyNotFoundError,
            DecryptionError,
            VaultError,
        ]:
            try:
                raise exc_class("test message")
            except WAuthError:
                pass
        logger.info("Catching WAuthError catches all subclasses")


class TestIndividualExceptions:
    """Test each exception type individually."""

    def test_key_not_found_error(self) -> None:
        """Verify KeyNotFoundError can be raised and caught."""
        with pytest.raises(KeyNotFoundError):
            raise KeyNotFoundError("Key 'X' not found")
        logger.info("KeyNotFoundError works correctly")

    def test_decryption_error(self) -> None:
        """Verify DecryptionError can be raised and caught."""
        with pytest.raises(DecryptionError):
            raise DecryptionError("Wrong key")
        logger.info("DecryptionError works correctly")

    def test_vault_error(self) -> None:
        """Verify VaultError can be raised and caught."""
        with pytest.raises(VaultError):
            raise VaultError("Database error")
        logger.info("VaultError works correctly")

    def test_backup_error(self) -> None:
        """Verify BackupError can be raised and caught."""
        with pytest.raises(BackupError):
            raise BackupError("IO error during backup")
        logger.info("BackupError works correctly")

    def test_restore_error(self) -> None:
        """Verify RestoreError can be raised and caught."""
        with pytest.raises(RestoreError):
            raise RestoreError("Corrupted backup file")
        logger.info("RestoreError works correctly")

    def test_rotation_error(self) -> None:
        """Verify RotationError can be raised and caught."""
        with pytest.raises(RotationError):
            raise RotationError("Failed to re-encrypt")
        logger.info("RotationError works correctly")

    def test_configuration_error(self) -> None:
        """Verify ConfigurationError can be raised and caught."""
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Invalid TOML")
        logger.info("ConfigurationError works correctly")

    def test_exception_message_preserved(self) -> None:
        """Verify that exception messages are preserved."""
        msg = "Custom error message"
        exc = DecryptionError(msg)
        assert msg in str(exc)
        logger.info("Exception message preserved")
