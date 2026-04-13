"""Cryptographic engine for encrypting and decrypting data using Fernet."""

import base64
import hashlib
from typing import TYPE_CHECKING, Optional

from cryptography.fernet import Fernet
from ._log import _debug, _error, _info, _warning

from .exceptions import DecryptionError
from .utils import generate_key

if TYPE_CHECKING:
    pass


class CryptoEngine:
    """Handles encryption and decryption using Fernet (AES-128-CBC).

    The encryption key is derived from a machine-specific identifier,
    meaning data encrypted on one machine can only be decrypted on
    that same machine.

    Args:
        custom_key: Optional custom encryption key string. If provided,
            it is hashed with SHA-256 to produce a deterministic 32-byte
            key. If ``None``, the key is derived from the machine
            identifier.
    """

    def __init__(self, custom_key: Optional[str] = None) -> None:
        if custom_key is not None:
            raw_key: bytes = hashlib.sha256(custom_key.encode()).digest()
            _debug("CryptoEngine initialized with custom key")
        else:
            raw_key = generate_key()
            _debug("CryptoEngine initialized with machine-derived key")
        self._key: bytes = base64.urlsafe_b64encode(raw_key)
        self._fernet: Fernet = Fernet(self._key)

    def encrypt(self, data: bytes) -> str:
        """Encrypt raw bytes into a Fernet token.

        Args:
            data: Plaintext data to encrypt.

        Returns:
            Base64-encoded Fernet token as a string.
        """
        token: str = self._fernet.encrypt(data).decode()
        _debug(f"Encrypted {len(data)} bytes into Fernet token")
        return token

    def decrypt(self, token: str) -> bytes:
        """Decrypt a Fernet token back to raw bytes.

        Args:
            token: Base64-encoded Fernet token.

        Returns:
            Decrypted plaintext as bytes.

        Raises:
            DecryptionError: If the token is invalid, tampered, or
                encrypted with a different key.
        """
        try:
            result: bytes = self._fernet.decrypt(token.encode())
            _debug("Decrypted Fernet token successfully")
            return result
        except Exception as exc:  # noqa: BLE001, pylint: disable=broad-exception-caught
            _debug(f"Decryption failed: {exc}")
            raise DecryptionError(
                "Failed to decrypt token — wrong key or corrupted data"
            ) from exc
