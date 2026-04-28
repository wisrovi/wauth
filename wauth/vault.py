"""Persistent storage layer for encrypted secrets using wsqlite."""

import os
from typing import Optional, Tuple

from ._log import _debug, _error, _info, _warning
from pydantic import BaseModel, Field
from wsqlite import WSQLite

from .exceptions import KeyNotFoundError, VaultError


class SecretModel(BaseModel):
    """Pydantic model representing a stored secret.

    Attributes:
        key: Primary key — unique name of the secret.
        value: Encrypted ciphertext of the secret.
        type: Secret type, either ``"text"`` or ``"file"``.
        created_at: Unix timestamp when the secret was first stored.
        updated_at: Unix timestamp of the last modification.
        ttl: Optional time-to-live in seconds. ``None`` means no expiration.
    """

    key: str = Field(..., description="Primary Key - Unique name of the secret")
    value: str = Field(..., description="Encrypted ciphertext value")
    type: str = Field(default="text", description="Secret type: 'text' or 'file'")
    created_at: float = Field(default=0.0, description="Unix timestamp of creation")
    updated_at: float = Field(default=0.0, description="Unix timestamp of last update")
    ttl: Optional[float] = Field(default=None, description="Time-to-live in seconds")


class Vault:
    """Encrypted secret storage backed by a SQLite database.

    Args:
        db_path: Path to the SQLite database file.
            Defaults to ``~/.wisrovi/wauth.db``.
    """

    def __init__(self, db_path: str = "~/.wisrovi/wauth.db") -> None:
        self.db_path: str = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        self.db: WSQLite = WSQLite(SecretModel, self.db_path)
        _debug(f"Vault initialized at {self.db_path}")

    def _timestamp(self) -> float:
        """Return the current Unix timestamp.

        Returns:
            Current time as a float (seconds since epoch).
        """
        # pylint: disable=import-outside-toplevel
        import time

        return time.time()

    def save(
        self,
        key: str,
        encrypted_value: str,
        val_type: str = "text",
        ttl: Optional[float] = None,
    ) -> None:
        """Save or update an encrypted secret in the vault.

        Uses ``INSERT OR REPLACE`` semantics to upsert the secret
        by key. Timestamps are automatically managed.

        Args:
            key: Unique identifier for the secret.
            encrypted_value: Fernet-encrypted ciphertext string.
            val_type: Secret type — ``"text"`` or ``"file"``.
            ttl: Optional time-to-live in seconds.
        """
        # pylint: disable=import-outside-toplevel
        import time

        now = self._timestamp()
        secret = SecretModel(
            key=key,
            value=encrypted_value,
            type=val_type,
            created_at=now,
            updated_at=now,
            ttl=ttl,
        )
        table = self.db.table_name
        fields = ", ".join(secret.model_dump().keys())
        placeholders = ", ".join(["?" for _ in secret.model_dump()])
        values = tuple(secret.model_dump().values())
        query = f"INSERT OR REPLACE INTO {table} ({fields}) VALUES ({placeholders})"  # nosec B608
        try:
            self.db._execute(query, values)  # pylint: disable=protected-access
            _debug(f"Secret saved: key='{key}', type='{val_type}'")
        except Exception as exc:
            _error(f"Failed to save secret '{key}': {exc}")
            raise VaultError(f"Failed to save secret '{key}': {exc}") from exc

    def get(self, key: str) -> Tuple[Optional[str], Optional[str]]:
        """Retrieve an encrypted secret by its key.

        Args:
            key: Unique identifier for the secret.

        Returns:
            A tuple of ``(encrypted_value, type)``.
            Returns ``(None, None)`` if the key does not exist.
        """
        try:
            result = self.db.get_by_field(key=key)
        except Exception as exc:
            _error(f"Vault error retrieving key '{key}': {exc}")
            raise VaultError(f"Failed to retrieve key '{key}': {exc}") from exc

        if not result:
            _debug(f"Key not found: '{key}'")
            return (None, None)

        secret_data = result[0]

        # Check TTL expiration
        if secret_data.ttl is not None and secret_data.ttl > 0:
            # pylint: disable=import-outside-toplevel
            import time

            if time.time() - secret_data.updated_at > secret_data.ttl:
                _warning(f"Secret expired: key='{key}'")
                self.delete(key)
                return (None, None)

        _debug(f"Secret retrieved: key='{key}', type='{secret_data.type}'")
        return (secret_data.value, secret_data.type)

    def delete(self, key: str) -> None:
        """Delete a secret from the vault.

        Args:
            key: Unique identifier for the secret to remove.

        Raises:
            KeyNotFoundError: If the key does not exist.
            VaultError: If the delete operation fails.
        """
        table = self.db.table_name
        query = f"DELETE FROM {table} WHERE key = ?"  # nosec B608
        try:
            rowcount = self.db._execute(query, (key,))  # pylint: disable=protected-access
            if rowcount == 0:
                raise KeyNotFoundError(f"Key not found: '{key}'")
            _debug(f"Secret deleted: key='{key}'")
        except KeyNotFoundError:
            raise
        except Exception as exc:
            _error(f"Failed to delete key '{key}': {exc}")
            raise VaultError(f"Failed to delete key '{key}': {exc}") from exc

    def list_keys(self) -> list[str]:
        """List all secret keys stored in the vault.

        Returns:
            A list of all key names.
        """
        table = self.db.table_name
        query = f"SELECT key FROM {table}"  # nosec B608
        try:
            rows = self.db._execute(query)  # pylint: disable=protected-access
            keys = [row[0] for row in rows]
            _debug(f"Listed {len(keys)} keys in vault")
            return keys
        except Exception as exc:
            _error(f"Failed to list keys: {exc}")
            raise VaultError(f"Failed to list keys: {exc}") from exc

    def count(self) -> int:
        """Return the number of secrets stored in the vault.

        Returns:
            Total number of secrets.
        """
        table = self.db.table_name
        query = f"SELECT COUNT(*) FROM {table}"  # nosec B608
        try:
            result = self.db._execute(query)  # pylint: disable=protected-access
            count: int = result[0][0] if result else 0
            _debug(f"Vault contains {count} secrets")
            return count
        except Exception as exc:
            _error(f"Failed to count secrets: {exc}")
            raise VaultError(f"Failed to count secrets: {exc}") from exc
