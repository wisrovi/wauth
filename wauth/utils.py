"""Platform utilities for machine identification and key derivation."""

import hashlib
import os
import platform
import subprocess

from ._log import _debug, _error, _info, _warning


def get_machine_id() -> str:
    """Retrieve a unique machine identifier in a cross-platform way.

    Attempts platform-specific methods in the following order:

    - **Linux**: Reads ``/etc/machine-id`` or ``/var/lib/dbus/machine-id``.
    - **Windows**: Queries ``wmic csproduct get uuid``.
    - **macOS**: Extracts ``IOPlatformUUID`` from ``ioreg``.

    Falls back to ``platform.node()`` (hostname) if all methods fail.

    Returns:
        A string representing the machine ID.
    """
    system = platform.system()
    _debug(f"Detecting machine ID on platform: {system}")
    try:
        if system == "Linux":
            if os.path.exists("/etc/machine-id"):
                with open("/etc/machine-id", encoding="utf-8") as f:
                    machine_id = f.read().strip()
                    _debug("Machine ID read from /etc/machine-id")
                    return machine_id
            _debug("/etc/machine-id not found, trying DBus fallback")
            machine_id = (
                subprocess.check_output(["cat", "/var/lib/dbus/machine-id"])
                .decode()
                .strip()
            )
            _debug("Machine ID read from /var/lib/dbus/machine-id")
            return machine_id
        if system == "Windows":
            machine_id = (
                subprocess.check_output(["wmic", "csproduct", "get", "uuid"])
                .decode()
                .split("\n")[1]
                .strip()
            )
            _debug("Machine ID retrieved via wmic")
            return machine_id
        if system == "Darwin":  # macOS
            machine_id = (
                subprocess.check_output(
                    ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"]
                )
                .decode()
                .split("IOPlatformUUID")[1]
                .split('"')[1]
            )
            _debug("Machine ID retrieved via ioreg")
            return machine_id
    except Exception as exc:  # noqa: BLE001, pylint: disable=broad-exception-caught
        _warning(f"Platform-specific machine ID detection failed: {exc}")

    _warning("Falling back to hostname as machine ID")
    return platform.node()


def generate_key() -> bytes:
    """Derive a 32-byte key for AES-256 encryption.

    The key is derived by hashing a salted machine identifier with SHA-256,
    producing a deterministic 32-byte output suitable for Fernet.

    Returns:
        A 32-byte key derived from the machine ID.
    """
    machine_id = get_machine_id()
    key = hashlib.sha256(f"wisrovi-salt-{machine_id}".encode()).digest()
    _debug("Derived 32-byte encryption key from machine ID")
    return key
