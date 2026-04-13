# WAuth Core Library

Machine-locked encrypted secret management built on Fernet (AES-128-CBC) and SQLite.

**Version:** 1.6.0 LTS  
**Pylint Score:** 9.95/10  
**Test Coverage:** 98%

## Modules

| Module | Description | Coverage |
|--------|-------------|----------|
| [`__init__.py`](#) | Main `WAuth` class, functional API, async methods, backup/restore | 97% |
| [`core.py`](#) | `CryptoEngine` — Fernet encryption/decryption with custom key support | 94% |
| [`vault.py`](#) | `SecretModel` (Pydantic) and `Vault` (SQLite + TTL + delete) | 100% |
| [`utils.py`](#) | Cross-platform machine ID detection and SHA-256 key derivation | 98% |
| [`exceptions.py`](#) | Custom exception hierarchy (`WAuthError` base) | 100% |
| [`deprecation.py`](#) | `@deprecated` decorator and `warn_deprecated()` helper | 100% |
| [`drivers/`](drivers/) | Driver abstraction layer (Local and Docker) | 88-100% |

## Design Principles

- **Machine-Locked Security**: Keys derived from unique machine identifiers
- **Zero Configuration**: Works out of the box with sensible defaults
- **Type Safe**: Full type hints and Pydantic validation
- **Well Documented**: Google Style Docstrings on every public member
- **Structured Logging**: Full `loguru` integration for diagnostics
- **Explicit Exceptions**: No silent failures — every error is raised
