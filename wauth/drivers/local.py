"""Local driver for encrypted secret storage.

Handles encryption/decryption of secrets and persistence via the Vault.
"""

import hmac

# pylint: disable=import-outside-toplevel
from typing import Optional

from .._log import _debug, _error, _info, _warning

from ..core import CryptoEngine
from ..vault import Vault


class LocalDriver:
    """Driver that stores secrets locally using Fernet encryption.

    Combines the cryptographic engine with the SQLite-backed vault
    for persistent, machine-locked secret storage.

    Args:
        custom_key: Optional custom encryption key string.
    """

    def __init__(self, custom_key: Optional[str] = None) -> None:
        self.engine: CryptoEngine = CryptoEngine(custom_key=custom_key)
        self.vault: Vault = Vault()
        _debug("LocalDriver initialized")

    def set_secret(
        self, key: str, value: str, ttl: Optional[float] = None
    ) -> None:
        """Encrypt and store a text secret.

        Args:
            key: Unique identifier for the secret.
            value: Plaintext value to encrypt.
            ttl: Optional time-to-live in seconds. ``None`` means no
                expiration.
        """
        encrypted = self.engine.encrypt(value.encode())
        self.vault.save(key, encrypted, "text", ttl=ttl)
        _info(f"Text secret stored: key='{key}'")

    def set_file(
        self, key: str, file_path: str, ttl: Optional[float] = None
    ) -> None:
        """Encrypt and store a file's contents.

        Args:
            key: Unique identifier for the file secret.
            file_path: Path to the file to encrypt and store.
            ttl: Optional time-to-live in seconds.
        """
        with open(file_path, "rb") as f:
            encrypted = self.engine.encrypt(f.read())
            self.vault.save(key, encrypted, "file", ttl=ttl)
        _info(f"File secret stored: key='{key}'")

    def get_secret(self, key: str) -> str | bytes | None:
        """Retrieve and decrypt a secret by its key.

        Args:
            key: Unique identifier for the secret.

        Returns:
            Decrypted secret as ``str`` for text type or ``bytes``
            for file type. Returns ``None`` if the key does not exist.
        """
        encrypted, v_type = self.vault.get(key)
        if not encrypted:
            _debug(f"Secret not found: key='{key}'")
            return None
        decrypted = self.engine.decrypt(encrypted)
        _debug(f"Secret decrypted: key='{key}', type='{v_type}'")
        return decrypted.decode() if v_type == "text" else decrypted

    def delete_secret(self, key: str) -> None:
        """Delete a secret from the vault.

        Args:
            key: Unique identifier for the secret to remove.

        Raises:
            KeyNotFoundError: If the key does not exist.
        """
        self.vault.delete(key)
        _info(f"Secret deleted: key='{key}'")

    def list_keys(self) -> list[str]:
        """List all secret keys stored in the vault.

        Returns:
            A list of all key names.
        """
        return self.vault.list_keys()

    def rotate_key(
        self, new_custom_key: str, keys_to_migrate: Optional[list[str]] = None
    ) -> dict[str, bool]:
        """Rotate the encryption key and re-encrypt existing secrets.

        Creates a new CryptoEngine with the provided key, decrypts all
        existing secrets with the current engine, and re-encrypts them
        with the new engine.

        Args:
            new_custom_key: The new custom key to use for encryption.
            keys_to_migrate: Specific keys to migrate. If ``None``, all
                keys in the vault are migrated.

        Returns:
            A dictionary mapping each key to a boolean indicating
            success (``True``) or failure (``False``).
        """
        new_engine = CryptoEngine(custom_key=new_custom_key)
        target_keys = keys_to_migrate or self.list_keys()
        results: dict[str, bool] = {}

        for secret_key in target_keys:
            try:
                encrypted, v_type = self.vault.get(secret_key)
                if not encrypted:
                    results[secret_key] = False
                    continue
                # Decrypt with old engine
                plaintext = self.engine.decrypt(encrypted)
                # Re-encrypt with new engine
                new_encrypted = new_engine.encrypt(plaintext)
                self.vault.save(secret_key, new_encrypted, v_type)
                results[secret_key] = True
                _info(f"Key migrated: '{secret_key}'")
            except Exception as exc:  # noqa: BLE001, pylint: disable=broad-exception-caught
                _error(f"Failed to migrate key '{secret_key}': {exc}")
                results[secret_key] = False

        if all(results.values()):
            # Swap the engine after successful migration
            self.engine = new_engine
            _info("Encryption key rotated successfully")
        else:
            _warning("Partial key rotation — some keys failed to migrate")

        return results

    def valid_secret(self, key: str, value_to_check: str) -> bool:
        """Verify if stored secret matches provided value without exposing it.

        Unlike get_secret(), this method never returns the decrypted secret.
        Uses constant-time comparison to prevent timing attacks.

        Args:
            key: Unique identifier for the secret.
            value_to_check: Plaintext value to compare against stored secret.

        Returns:
            True if values match, False otherwise (or if key doesn't exist).
        """
        encrypted, v_type = self.vault.get(key)
        if not encrypted or v_type != "text":
            _debug(f"Secret not found or not text: key='{key}'")
            return False
        try:
            decrypted = self.engine.decrypt(encrypted).decode()
            # Constant-time comparison to prevent timing attacks
            return hmac.compare_digest(decrypted, value_to_check)
        except Exception:  # noqa: BLE001, pylint: disable=broad-exception-caught
            _error(f"Failed to verify secret: key='{key}'")
            return False
