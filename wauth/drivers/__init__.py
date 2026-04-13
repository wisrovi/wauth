"""Driver abstraction layer for secret retrieval sources.

Provides a factory pattern that prioritizes Docker secrets when running
inside a container, falling back to the local encrypted vault otherwise.
"""

from .._log import _debug, _error, _info, _warning

from .docker import DockerDriver
from .local import LocalDriver


class DriverFactory:
    """Factory for managing secret drivers (local and Docker).

    Automatically selects the appropriate driver based on the
    runtime environment.
    """

    def __init__(self) -> None:
        self.local: LocalDriver = LocalDriver()
        self.docker: DockerDriver = DockerDriver()
        _debug("DriverFactory initialized")

    def get_value(self, key: str) -> str | None:
        """Retrieve a secret value, trying Docker first if in a container.

        Args:
            key: Unique identifier for the secret.

        Returns:
            The secret value if found, or ``None``.
        """
        if self.docker.is_docker():
            val = self.docker.get_secret(key)
            if val:
                _debug(f"Secret retrieved from Docker: key='{key}'")
                return val
            _debug("Docker secret not found, falling back to local vault")
        return self.local.get_secret(key)

    def set_value(self, key: str, value: str, is_file: bool = False) -> None:
        """Store a secret using the local encrypted vault.

        Writing is always directed to the local driver since the vault
        is the persistent store.

        Args:
            key: Unique identifier for the secret.
            value: Secret value or file path if ``is_file`` is True.
            is_file: Whether the value represents a file path.
        """
        if is_file:
            self.local.set_file(key, value)
        else:
            self.local.set_secret(key, value)
