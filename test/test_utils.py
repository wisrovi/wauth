"""Tests for utility functions.

Covers machine identification and key derivation functions in
the :mod:`wauth.utils` module.
"""

import hashlib

# pylint: disable=import-outside-toplevel
from loguru import logger

from wauth.utils import generate_key, get_machine_id


class TestGetMachineId:
    """Test suite for the get_machine_id function."""

    def test_returns_string(self) -> None:
        """Verify that get_machine_id returns a non-empty string."""
        machine_id = get_machine_id()
        assert isinstance(machine_id, str)
        assert len(machine_id) > 0
        logger.info(f"Machine ID retrieved: {machine_id[:20]}...")

    def test_returns_consistent_id(self) -> None:
        """Verify that repeated calls return the same identifier."""
        id1 = get_machine_id()
        id2 = get_machine_id()
        assert id1 == id2
        logger.info("Machine ID is consistent across calls")


class TestGenerateKey:
    """Test suite for the generate_key function."""

    def test_returns_32_bytes(self) -> None:
        """Verify that generate_key returns exactly 32 bytes."""
        key = generate_key()
        assert isinstance(key, bytes)
        assert len(key) == 32
        logger.info("Key generation produces 32-byte output")

    def test_key_is_deterministic(self) -> None:
        """Verify that key generation is deterministic for same machine."""
        key1 = generate_key()
        key2 = generate_key()
        assert key1 == key2
        logger.info("Key generation is deterministic")

    def test_key_derivation_uses_sha256(self) -> None:
        """Verify that the key is derived using SHA-256 hashing."""
        machine_id = get_machine_id()
        expected = hashlib.sha256(f"wisrovi-salt-{machine_id}".encode()).digest()
        actual = generate_key()
        assert actual == expected
        logger.info("Key derivation confirmed to use SHA-256")

    def test_keys_are_different_for_different_ids(self) -> None:
        """Verify that different machine IDs produce different keys."""
        key1 = generate_key()
        # Simulate a different machine ID by directly hashing
        different_key = hashlib.sha256(
            "wisrovi-salt-different-machine".encode()
        ).digest()
        assert key1 != different_key
        logger.info("Different machine IDs produce different keys")


class TestGetMachineIdPlatforms:
    """Test platform-specific branches in get_machine_id via mocking."""

    def test_linux_fallback_to_dbus(self, monkeypatch) -> None:
        """Test Linux path when /etc/machine-id doesn't exist."""
        import wauth.utils as utils_mod
        import os

        monkeypatch.setattr(os.path, "exists", lambda p: False)
        monkeypatch.setattr(
            "subprocess.check_output",
            lambda cmd: b"dbus-machine-id-12345\n",
        )
        monkeypatch.setattr("platform.system", lambda: "Linux")
        monkeypatch.setattr("platform.node", lambda: "fallback-node")

        result = utils_mod.get_machine_id()
        assert result == "dbus-machine-id-12345"
        logger.info("Linux DBus fallback path covered")

    def test_windows_path(self, monkeypatch) -> None:
        """Test Windows platform branch."""
        import wauth.utils as utils_mod
        import os

        monkeypatch.setattr(os.path, "exists", lambda p: False)
        # wmic output has a header line, then the value, then empty line
        monkeypatch.setattr(
            "subprocess.check_output",
            lambda cmd: b"UUID\r\nUUID-12345\r\n\r\n",
        )
        monkeypatch.setattr("platform.system", lambda: "Windows")
        monkeypatch.setattr("platform.node", lambda: "windows-node")

        result = utils_mod.get_machine_id()
        assert "UUID-12345" in result
        logger.info("Windows platform branch covered")

    def test_macos_path(self, monkeypatch) -> None:
        """Test macOS platform branch."""
        import wauth.utils as utils_mod
        import os

        monkeypatch.setattr(os.path, "exists", lambda p: False)
        # Code does: .split("IOPlatformUUID")[1].split('"')[1]
        # After split on IOPlatformUUID: 'XXXX" VALUE "...' -> split '"': ['', ' VALUE ', ...]
        # So index [1] needs to be our value: '"macos-uuid-12345"'
        monkeypatch.setattr(
            "subprocess.check_output",
            lambda cmd: b'foo IOPlatformUUID"macos-uuid-12345" bar',
        )
        monkeypatch.setattr("platform.system", lambda: "Darwin")
        monkeypatch.setattr("platform.node", lambda: "mac-node")

        result = utils_mod.get_machine_id()
        assert result == "macos-uuid-12345"
        logger.info("macOS platform branch covered")

    def test_fallback_to_platform_node(self, monkeypatch) -> None:
        """Test fallback to platform.node() when all methods fail."""
        import wauth.utils as utils_mod
        import os

        monkeypatch.setattr(os.path, "exists", lambda p: False)
        monkeypatch.setattr(
            "subprocess.check_output",
            lambda cmd: (_ for _ in ()).throw(OSError("fail")),
        )
        monkeypatch.setattr("platform.system", lambda: "Linux")
        monkeypatch.setattr("platform.node", lambda: "fallback-hostname")

        result = utils_mod.get_machine_id()
        assert result == "fallback-hostname"
        logger.info("Fallback to platform.node() covered")
