"""WAuth - Local encrypted secret management library.

Provides a simple interface to store and retrieve secrets encrypted
with Fernet (AES-256), backed by a SQLite database via wsqlite.

Example:
    >>> from wauth import WAuth
    >>> auth = WAuth()
    >>> auth.set("API_KEY", "secret-value")
    >>> auth.get("API_KEY")
    'secret-value'
"""

# pylint: disable=redefined-builtin
# 'set' and 'get' are intentional convenience names for the functional API

import asyncio
import json
import os
import tomllib
from pathlib import Path
from typing import Any, Optional

from wsqlite import WSQLite

from ._log import (
    _debug,
    _error,
    _get_verbose,
    _info,
    _set_verbose,
    _warning,
)
from .core import CryptoEngine
from .deprecation import deprecated
from .drivers.local import LocalDriver
from .exceptions import BackupError, ConfigurationError, RestoreError, WAuthError
from .vault import SecretModel, Vault

__all__ = [
    "WAuth",
    "CryptoEngine",
    "LocalDriver",
    "SecretModel",
    "Vault",
    "set",
    "set_file",
    "get",
    "delete",
    "list_keys",
    "WAuthError",
    "set_verbose",
    "get_verbose",
]

# Version info for LTS tracking
__version__ = "0.3.2"
__lts__ = True

# Global verbosity: when False, suppress all loguru output from wauth

def set_verbose(enabled: bool) -> None:
    """Enable or disable loguru output across the entire WAuth library.

    When verbose is ``False`` (the default), all debug, info, and warning
    messages are suppressed. Errors are always logged.

    Args:
        enabled: Whether to enable verbose logging.
    """
    _set_verbose(enabled)


def get_verbose() -> bool:
    """Return the current verbose state.

    Returns:
        ``True`` if verbose logging is enabled.
    """
    return _get_verbose()


class WAuth:
    """Main interface for managing encrypted secrets.

    Provides methods for storing, retrieving, deleting, rotating,
    backing up, and restoring encrypted secrets.

    Args:
        db_path: Path to the SQLite database file.
            Defaults to ``~/.wisrovi/wauth.db``.
        custom_key: Optional custom encryption key string.
        config_path: Optional path to a TOML configuration file.
        verbose: When ``True``, emit debug/info/warning logs via loguru.
            Defaults to ``False``.

    Example:
        >>> auth = WAuth()
        >>> auth.set("MY_KEY", "my-secret")
        >>> value = auth.get("MY_KEY")
    """

    def __init__(
        self,
        db_path: str = "~/.wisrovi/wauth.db",
        custom_key: Optional[str] = None,
        config_path: Optional[str] = None,
        verbose: bool = False,
    ) -> None:
        _set_verbose(verbose)
        resolved_db: str = db_path
        resolved_key: Optional[str] = custom_key

        if config_path:
            config = self._load_config(config_path)
            resolved_db = config.get("db_path", resolved_db)
            resolved_key = config.get("custom_key", resolved_key)

        self._driver = LocalDriver(custom_key=resolved_key)
        if resolved_db != "~/.wisrovi/wauth.db":
            self._driver.vault.db = WSQLite(SecretModel, resolved_db)
        _info(f"WAuth initialized with db='{resolved_db}'")

    @staticmethod
    def _load_config(config_path: str) -> dict[str, Any]:
        """Load configuration from a TOML file.

        Args:
            config_path: Path to the TOML configuration file.

        Returns:
            Configuration dictionary.

        Raises:
            ConfigurationError: If the file cannot be read or parsed.
        """
        path = Path(config_path)
        if not path.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")
        try:
            with open(path, "rb") as f:
                config = tomllib.load(f)
            wauth_section = config.get("wauth", config)
            _debug(f"Configuration loaded from {config_path}")
            return wauth_section
        except Exception as exc:  # noqa: BLE001
            raise ConfigurationError(f"Failed to parse config: {exc}") from exc

    def set(self, key: str, value: str, ttl: Optional[float] = None) -> None:
        """Store an encrypted text secret.

        Args:
            key: Unique identifier for the secret.
            value: Plaintext value to encrypt and store.
            ttl: Optional time-to-live in seconds. ``None`` means no
                expiration.
        """
        self._driver.set_secret(key, value, ttl=ttl)

    def set_file(self, key: str, path: str, ttl: Optional[float] = None) -> None:
        """Store an encrypted file (e.g., .pem, .key).

        Args:
            key: Unique identifier for the file secret.
            path: Filesystem path to the file to encrypt and store.
            ttl: Optional time-to-live in seconds.
        """
        self._driver.set_file(key, path, ttl=ttl)

    def get(self, key: str) -> str | bytes | None:
        """Retrieve a decrypted secret.

        Args:
            key: Unique identifier for the secret.

        Returns:
            Decrypted secret as ``str`` for text type or ``bytes`` for
            file type. Returns ``None`` if the key does not exist.
        """
        return self._driver.get_secret(key)

    def delete(self, key: str) -> None:
        """Delete a secret from the vault.

        Args:
            key: Unique identifier for the secret to remove.

        Raises:
            WAuthError: If the key does not exist.
        """
        self._driver.delete_secret(key)

    def list_keys(self) -> list[str]:
        """List all secret keys stored in the vault.

        Returns:
            A list of all key names.
        """
        return self._driver.list_keys()

    def rotate_key(self, new_custom_key: str) -> dict[str, bool]:
        """Rotate the encryption key and re-encrypt all existing secrets.

        Decrypts every secret with the current key, then re-encrypts
        and stores them with the new key. The internal engine is
        swapped only if all migrations succeed.

        Args:
            new_custom_key: The new custom key to use for encryption.

        Returns:
            A dict mapping each key to ``True`` (success) or ``False``
            (failure).
        """
        return self._driver.rotate_key(new_custom_key)

    def backup(self, output_path: str) -> str:
        """Export all secrets to an encrypted backup file.

        Creates a JSON file containing all secret keys and their
        encrypted values (still encrypted — the backup itself is not
        decrypted).

        Args:
            output_path: Destination path for the backup file.

        Returns:
            The absolute path of the created backup file.

        Raises:
            BackupError: If the export fails.
        """
        try:
            # pylint: disable=import-outside-toplevel
            import time

            keys = self.list_keys()
            secrets: dict[str, dict[str, Any]] = {}
            for key in keys:
                encrypted, v_type = self._driver.vault.get(key)
                if encrypted:
                    secrets[key] = {"value": encrypted, "type": v_type}

            backup_data = {
                "version": __version__,
                "timestamp": time.time(),
                "secrets": secrets,
            }
            abs_path = os.path.abspath(output_path)
            with open(abs_path, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=2)
            _info(f"Backup created: {abs_path} ({len(secrets)} secrets)")
            return abs_path
        except Exception as exc:  # noqa: BLE001
            _error(f"Backup failed: {exc}")
            raise BackupError(f"Failed to create backup: {exc}") from exc

    def restore(self, backup_path: str) -> int:
        """Restore secrets from an encrypted backup file.

        Reads a backup file created by :meth:`backup` and re-stores
        all encrypted secrets into the current vault.

        Args:
            backup_path: Path to the backup file.

        Returns:
            The number of secrets restored.

        Raises:
            RestoreError: If the file cannot be read or parsed.
        """
        try:
            path = Path(backup_path)
            if not path.exists():
                raise RestoreError(f"Backup file not found: {backup_path}")
            with open(path, encoding="utf-8") as f:
                backup_data = json.load(f)
            secrets = backup_data.get("secrets", {})
            count = 0
            for key, data in secrets.items():
                self._driver.vault.save(key, data["value"], data["type"])
                count += 1
            _info(f"Restored {count} secrets from {backup_path}")
            return count
        except (RestoreError, KeyError):
            raise
        except Exception as exc:  # noqa: BLE001
            _error(f"Restore failed: {exc}")
            raise RestoreError(f"Failed to restore backup: {exc}") from exc

    # ─── Async support ────────────────────────────────────────────────

    async def async_set(self, key: str, value: str, ttl: Optional[float] = None) -> None:
        """Async variant of :meth:`set`.

        Runs the synchronous ``set`` in a thread pool to avoid blocking
        the event loop during I/O-bound database writes.

        Args:
            key: Unique identifier for the secret.
            value: Plaintext value to encrypt and store.
            ttl: Optional time-to-live in seconds.
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.set, key, value, ttl)

    async def async_get(self, key: str) -> str | bytes | None:
        """Async variant of :meth:`get`.

        Args:
            key: Unique identifier for the secret.

        Returns:
            Decrypted secret or ``None``.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.get, key)

    async def async_delete(self, key: str) -> None:
        """Async variant of :meth:`delete`.

        Args:
            key: Unique identifier for the secret to remove.
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.delete, key)

    async def async_backup(self, output_path: str) -> str:
        """Async variant of :meth:`backup`.

        Args:
            output_path: Destination path for the backup file.

        Returns:
            Absolute path of the created backup file.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.backup, output_path)

    async def async_restore(self, backup_path: str) -> int:
        """Async variant of :meth:`restore`.

        Args:
            backup_path: Path to the backup file.

        Returns:
            Number of secrets restored.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.restore, backup_path)


# Functional API for convenience
_driver = LocalDriver()


def set(key: str, value: str, ttl: Optional[float] = None) -> None:
    """Store an encrypted text secret (functional API).

    Args:
        key: Unique identifier for the secret.
        value: Plaintext value to encrypt and store.
        ttl: Optional time-to-live in seconds.
    """
    _driver.set_secret(key, value, ttl=ttl)


def set_file(key: str, path: str, ttl: Optional[float] = None) -> None:
    """Store an encrypted file (functional API).

    Args:
        key: Unique identifier for the file secret.
        path: Filesystem path to the file to encrypt and store.
        ttl: Optional time-to-live in seconds.
    """
    _driver.set_file(key, path, ttl=ttl)


def get(key: str) -> str | bytes | None:
    """Retrieve a decrypted secret (functional API).

    Args:
        key: Unique identifier for the secret.

    Returns:
        Decrypted secret as ``str`` for text type or ``bytes`` for
        file type. Returns ``None`` if the key does not exist.
    """
    return _driver.get_secret(key)


def delete(key: str) -> None:
    """Delete a secret (functional API).

    Args:
        key: Unique identifier for the secret to remove.

    Raises:
        WAuthError: If the key does not exist.
    """
    _driver.delete_secret(key)


def list_keys() -> list[str]:
    """List all secret keys (functional API).

    Returns:
        A list of all key names.
    """
    return _driver.list_keys()
