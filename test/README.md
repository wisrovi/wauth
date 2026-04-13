# WAuth Test Suite

Comprehensive test suite with **98% coverage** and **Pylint score 9.98/10**.

## Test Files

| File | Module Tested | Tests | Coverage |
|------|--------------|-------|----------|
| [`test_wauth.py`](test_wauth.py) | `WAuth` class, functional API | 15 | 100% |
| [`test_core.py`](test_core.py) | `CryptoEngine` | 10 | 89% |
| [`test_vault.py`](test_vault.py) | `SecretModel`, `Vault` | 12 | 100% |
| [`test_utils.py`](test_utils.py) | `get_machine_id`, `generate_key` | 10 | 97% |
| [`test_drivers.py`](test_drivers.py) | `LocalDriver`, `DockerDriver`, `DriverFactory` | 16 | 95-100% |
| [`conftest.py`](conftest.py) | Shared fixtures | — | — |

## Test Quality Standards

- **Pylint**: ≥ 9.5 per module (achieved: 9.98/10 overall)
- **Docstrings**: Google Style on all test classes and methods
- **Type Hints**: Complete on all test functions
- **Logging**: Uses `loguru.logger` instead of `print()`
- **Isolation**: Every test uses `tmp_path` fixture for database isolation
- **Cleanup**: Automatic DB file cleanup via `autouse` fixture

## Running Tests

```bash
# Run all tests with coverage
pytest test/ -v --cov=wauth --cov-report=term-missing

# Run specific test module
pytest test/test_core.py -v

# Run with Pylint check
pylint test/ --disable=import-error,no-member,no-name-in-module
```

## Coverage Breakdown

```
Name                        Cover   Missing
wauth/__init__.py           100%    —
wauth/core.py                89%    TYPE_CHECKING block (non-runtime)
wauth/drivers/__init__.py    95%    Branch optimization
wauth/drivers/docker.py     100%    —
wauth/drivers/local.py      100%    —
wauth/utils.py               97%    Platform-specific branch
wauth/vault.py              100%    —
--------------------------------------------
TOTAL                        98%
```
