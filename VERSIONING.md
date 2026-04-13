# Versioning Policy

WAuth follows [Semantic Versioning 2.0.0](https://semver.org/).

## Version Format

```
MAJOR.MINOR.PATCH
```

| Component | When to increment | Example |
|-----------|------------------|---------|
| **MAJOR** | Incompatible API changes | `1.x.x` → `2.0.0` |
| **MINOR** | Backwards-compatible features | `1.5.x` → `1.6.0` |
| **PATCH** | Backwards-compatible bug fixes | `1.6.0` → `1.6.1` |

## LTS Policy

- **Even minor versions** (1.6, 1.8, 2.0) are **LTS releases**
- LTS versions receive **security backports for 24 months**
- Non-LTS versions receive bug fixes for **6 months**
- The current LTS version is **1.6.0**

## Public API Stability

The following are considered the **stable public API**:

- `WAuth` class and all its methods
- Functional API: `set()`, `set_file()`, `get()`, `delete()`, `list_keys()`
- Exception classes in `wauth.exceptions`

Everything else (internal modules, private methods prefixed with `_`)
may change without notice.

## Deprecation Policy

- Deprecated APIs emit `DeprecationWarning` on first use
- Deprecated APIs are removed in the **next MAJOR** version
- Migration guides are published alongside deprecation notices

## Compatibility Matrix

| Python Version | Tested in CI | Officially Supported |
|---------------|-------------|---------------------|
| 3.9 | ✅ | ✅ |
| 3.10 | ✅ | ✅ |
| 3.11 | ✅ | ✅ |
| 3.12 | ✅ | ✅ |
| 3.13 | ✅ | ✅ |

| OS | CI Coverage | Supported |
|----|------------|-----------|
| Linux (Ubuntu) | ✅ | ✅ |
| macOS | Manual | ✅ |
| Windows | Manual | ✅ |

---

**Author:** William Rodríguez — wisrovi  
**LinkedIn:** https://es.linkedin.com/in/wisrovi-rodriguez
