"""Custom exception hierarchy for WAuth.

Provides a structured hierarchy of exceptions that allow callers to
distinguish between different failure modes (key not found, decryption
failure, vault corruption, backup errors, etc.).
"""


class WAuthError(Exception):
    """Base exception for all WAuth-related errors.

    All custom exceptions inherit from this class, allowing callers to
    catch any WAuth-specific error with a single ``except`` clause.

    Example:
        >>> try:
        ...     auth.get("NONEXISTENT")
        ... except WAuthError as exc:
        ...     print(f"WAuth error: {exc}")
    """


class KeyNotFoundError(WAuthError):
    """Raised when a requested secret key does not exist in the vault.

    Example:
        >>> try:
        ...     value = auth.get("MISSING_KEY")
        ... except KeyNotFoundError:
        ...     print("Key not found")
    """


class DecryptionError(WAuthError):
    """Raised when decryption fails due to wrong key or corrupted data.

    This exception replaces the previous silent-failure behaviour that
    returned empty bytes (``b""``) on decryption errors.

    Example:
        >>> try:
        ...     engine.decrypt("invalid-token")
        ... except DecryptionError:
        ...     print("Cannot decrypt — wrong key or corrupted data")
    """


class VaultError(WAuthError):
    """Raised when a vault operation fails (database corruption, I/O error).

    Example:
        >>> try:
        ...     vault.save("KEY", "value")
        ... except VaultError:
        ...     print("Vault storage error")
    """


class BackupError(WAuthError):
    """Raised when a backup or export operation fails.

    Example:
        >>> try:
        ...     auth.backup("backup.wauth")
        ... except BackupError:
        ...     print("Backup failed")
    """


class RestoreError(WAuthError):
    """Raised when a restore or import operation fails.

    Example:
        >>> try:
        ...     auth.restore("backup.wauth")
        ... except RestoreError:
        ...     print("Restore failed")
    """


class RotationError(WAuthError):
    """Raised when a key or secret rotation operation fails.

    Example:
        >>> try:
        ...     auth.rotate_key()
        ... except RotationError:
        ...     print("Key rotation failed")
    """


class ConfigurationError(WAuthError):
    """Raised when configuration loading or validation fails.

    Example:
        >>> try:
        ...     auth = WAuth(config_path="bad.toml")
        ... except ConfigurationError:
        ...     print("Invalid configuration file")
    """
