# Migration Guide

## v1.5.x → v1.6.0 (LTS)

### Breaking Changes

#### 1. `CryptoEngine.decrypt()` now raises `DecryptionError`

**Before** (v1.5):
```python
result = engine.decrypt(token)
if result == b"":
    print("Decryption failed")  # Silent failure
```

**After** (v1.6):
```python
from wauth.exceptions import DecryptionError

try:
    result = engine.decrypt(token)
except DecryptionError:
    print("Decryption failed — wrong key or corrupted data")
```

**Migration**: Replace empty-byte checks with `try/except DecryptionError`.

#### 2. `WAuth` constructor accepts `config_path`

**Before** (v1.5):
```python
auth = WAuth(db_path="~/.wisrovi/wauth.db")
```

**After** (v1.6):
```python
# Option 1: Direct parameters (unchanged)
auth = WAuth(db_path="~/.wisrovi/wauth.db", custom_key="my-key")

# Option 2: From TOML config
auth = WAuth(config_path="~/.wauth.toml")
```

**Migration**: Existing code works unchanged. `config_path` is optional.

### New Features

#### Delete Secrets
```python
auth.delete("OLD_KEY")  # Removes the secret from the vault
```

#### List Keys
```python
keys = auth.list_keys()  # Returns ["KEY1", "KEY2", ...]
```

#### Key Rotation
```python
results = auth.rotate_key("new-encryption-key")
# {"KEY1": True, "KEY2": True}
```

#### TTL Support
```python
auth.set("TEMP_TOKEN", "value", ttl=3600)  # Expires in 1 hour
```

#### Backup & Restore
```python
auth.backup("backup.wauth")       # Export encrypted secrets
auth.restore("backup.wauth")      # Import from backup
```

#### Async Support
```python
await auth.async_set("KEY", "value")
value = await auth.async_get("KEY")
await auth.async_delete("KEY")
```

#### Custom Exceptions
```python
from wauth.exceptions import (
    WAuthError,
    KeyNotFoundError,
    DecryptionError,
    VaultError,
    BackupError,
    RestoreError,
    RotationError,
    ConfigurationError,
)
```

### Logging

WAuth now uses `loguru` internally. Configure logging in your application:

```python
from loguru import logger

# Set log level
logger.remove()
logger.add("wauth.log", level="DEBUG")
```

### Deprecations

None in v1.6.0 LTS. First deprecations expected in v1.7.x, removal
in v2.0.0.

---

## v1.4.x → v1.5.x

No breaking changes. Upgrade is drop-in compatible.

---

**Author:** William Rodríguez — wisrovi  
**LinkedIn:** https://es.linkedin.com/in/wisrovi-rodriguez
