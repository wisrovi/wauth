# WAuth Drivers

Pluggable driver architecture for secret retrieval from different sources.

## Drivers

| Driver | Description | Use Case |
|--------|-------------|----------|
| [`LocalDriver`](local.py) | Encrypted local storage via Fernet + SQLite | Development, single-node deployments |
| [`DockerDriver`](docker.py) | Read secrets from `/run/secrets` filesystem | Docker Swarm, Docker Compose |
| [`DriverFactory`](__init__.py) | Auto-selects the appropriate driver | Production environments |

## How It Works

The `DriverFactory` uses a priority-based approach:

1. **Docker Check**: If running inside a Docker container (`/.dockerenv` or `/proc/self/cgroup` exists), tries `DockerDriver` first.
2. **Fallback**: If Docker secret not found, falls back to `LocalDriver` encrypted vault.
3. **Write Path**: All writes always go through `LocalDriver` since the local vault is the persistent store.

## Quality

- **Pylint Score**: 10.00/10
- **Test Coverage**: 100% (docker.py, local.py), 95% (__init__.py)
- **Type Hints**: Complete
- **Docstrings**: Google Style, 100% coverage
