"""Tests for the CryptoEngine module.

Covers encryption, decryption, key generation, error handling,
and exception-based failures for the :mod:`wauth.core` module.
"""

import base64

from loguru import logger

from wauth.core import CryptoEngine
from wauth.exceptions import DecryptionError


class TestCryptoEngine:
    """Test suite for the CryptoEngine class."""

    def test_engine_initialization(self) -> None:
        """Verify that the engine initializes with a valid Fernet key."""
        engine = CryptoEngine()
        assert engine._key is not None
        assert len(engine._key) > 0
        decoded = base64.urlsafe_b64decode(engine._key)
        assert len(decoded) == 32
        logger.info("CryptoEngine initialized with valid 32-byte key")

    def test_engine_with_custom_key(self) -> None:
        """Verify that a custom key is properly derived."""
        engine = CryptoEngine(custom_key="my-custom-key")
        assert engine._key is not None
        decoded = base64.urlsafe_b64decode(engine._key)
        assert len(decoded) == 32
        logger.info("CryptoEngine initialized with custom key")

    def test_custom_key_is_deterministic(self) -> None:
        """Verify that the same custom key produces the same encryption."""
        engine1 = CryptoEngine(custom_key="test-key")
        engine2 = CryptoEngine(custom_key="test-key")
        data = b"secret"
        token1 = engine1.encrypt(data)
        decrypted = engine2.decrypt(token1)
        assert decrypted == data
        logger.info("Custom key is deterministic across instances")

    def test_encrypt_decrypt_roundtrip(self) -> None:
        """Verify that encrypted data can be decrypted correctly."""
        engine = CryptoEngine()
        original = b"my-secret-data"
        encrypted = engine.encrypt(original)
        assert isinstance(encrypted, str)
        decrypted = engine.decrypt(encrypted)
        assert decrypted == original
        logger.info("Encrypt/decrypt roundtrip successful")

    def test_encrypt_produces_different_ciphertext(self) -> None:
        """Verify that encrypting the same data twice produces different tokens."""
        engine = CryptoEngine()
        data = b"test-data"
        token1 = engine.encrypt(data)
        token2 = engine.encrypt(data)
        assert token1 != token2
        logger.info("Same plaintext produces different ciphertext (expected)")

    def test_decrypt_invalid_token_raises_error(self) -> None:
        """Verify that decrypting an invalid token raises DecryptionError."""
        engine = CryptoEngine()
        invalid_token = "not-a-valid-fernet-token"
        try:
            engine.decrypt(invalid_token)
            assert False, "Expected DecryptionError"
        except DecryptionError:
            logger.info("Invalid token correctly raises DecryptionError")

    def test_decrypt_tampered_token_raises_error(self) -> None:
        """Verify that tampered tokens raise DecryptionError."""
        engine = CryptoEngine()
        original = b"secret"
        token = engine.encrypt(original)
        tampered = token[:-5] + "XXXXX"
        try:
            engine.decrypt(tampered)
            assert False, "Expected DecryptionError"
        except DecryptionError:
            logger.info("Tampered token correctly raises DecryptionError")

    def test_decrypt_wrong_key_raises_error(self) -> None:
        """Verify that decrypting with a different key raises DecryptionError."""
        engine1 = CryptoEngine(custom_key="key-one")
        engine2 = CryptoEngine(custom_key="key-two")
        token = engine1.encrypt(b"secret")
        try:
            engine2.decrypt(token)
            assert False, "Expected DecryptionError"
        except DecryptionError:
            logger.info("Wrong key correctly raises DecryptionError")

    def test_encrypt_empty_bytes(self) -> None:
        """Verify encryption handles empty bytes correctly."""
        engine = CryptoEngine()
        encrypted = engine.encrypt(b"")
        decrypted = engine.decrypt(encrypted)
        assert decrypted == b""
        logger.info("Empty bytes encryption/decryption successful")

    def test_encrypt_unicode_data(self) -> None:
        """Verify encryption handles unicode data."""
        engine = CryptoEngine()
        data = "こんにちは世界".encode("utf-8")
        encrypted = engine.encrypt(data)
        decrypted = engine.decrypt(encrypted)
        assert decrypted == data
        logger.info("Unicode data encryption/decryption successful")

    def test_encrypt_large_data(self) -> None:
        """Verify encryption handles larger payloads."""
        engine = CryptoEngine()
        data = b"A" * 10000
        encrypted = engine.encrypt(data)
        decrypted = engine.decrypt(encrypted)
        assert decrypted == data
        logger.info("Large data encryption/decryption successful")

    def test_encrypt_returns_string_type(self) -> None:
        """Verify that encrypt returns a str, not bytes."""
        engine = CryptoEngine()
        result = engine.encrypt(b"test")
        assert isinstance(result, str)

    def test_decrypt_returns_bytes_type(self) -> None:
        """Verify that decrypt returns bytes."""
        engine = CryptoEngine()
        token = engine.encrypt(b"test")
        result = engine.decrypt(token)
        assert isinstance(result, bytes)
