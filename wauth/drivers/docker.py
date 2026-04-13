"""Docker driver for reading container-injected secrets.

Reads secrets from the filesystem path used by Docker Swarm or
Docker Compose secret management (``/run/secrets`` by default).
"""

import os

from .._log import _debug, _error, _info, _warning


class DockerDriver:
    """Driver for reading secrets from a Docker container's filesystem.

    Docker injects secrets as files under ``/run/secrets``. This driver
    reads from that path when running inside a container.

    Note:
        This driver is **read-only**. Writing secrets is handled by
        :class:`LocalDriver`.

    Args:
        secrets_path: Base path where Docker secrets are mounted.
            Defaults to ``/run/secrets``.
    """

    def __init__(self, secrets_path: str = "/run/secrets") -> None:
        self.secrets_path: str = secrets_path
        _debug(f"DockerDriver initialized with secrets_path='{secrets_path}'")

    def get_secret(self, key: str) -> str | None:
        """Read a secret from the Docker secrets filesystem.

        Args:
            key: Name of the secret (corresponds to filename).

        Returns:
            Stripped secret content, or ``None`` if not found.
        """
        path = os.path.join(self.secrets_path, key)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                content = f.read().strip()
            _debug(f"Docker secret read: key='{key}'")
            return content
        _debug(f"Docker secret not found: key='{key}' at path='{path}'")
        return None

    def is_docker(self) -> bool:
        """Check if the process is running inside a Docker container.

        Returns:
            ``True`` if Docker indicators are present in the filesystem.
        """
        is_container = os.path.exists("/.dockerenv") or os.path.exists(
            "/proc/self/cgroup"
        )
        _debug(f"Docker container detection: {is_container}")
        return is_container
