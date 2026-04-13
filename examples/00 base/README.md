# Base Example

Demonstrates the fundamental WAuth workflow.

## What This Example Shows

1. **Initialization**: Creating a `WAuth` instance with a custom database path
2. **Storing Secrets**: Using `auth.set()` to store an encrypted text secret
3. **Retrieving Secrets**: Using `auth.get()` to decrypt and retrieve the secret
4. **Cleanup**: Removing the demo database file after use

## Running

```bash
python example.py
# Output: Retrieved token: 7483920:ABC-DEF-GHI
```

## Code Quality

- **Pylint**: 10.00/10
- **Type Hints**: Complete
- **Docstrings**: Google Style
- **PEP 8**: Compliant
