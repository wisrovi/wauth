# WAuth Benchmarks

Performance benchmarks for encryption, decryption, secret lifecycle, and key rotation.

## Running Benchmarks

```bash
python benchmarks/performance.py
```

## What's Measured

| Benchmark | Description |
|-----------|-------------|
| **Encryption** | Time to encrypt payloads from 16B to 16KB |
| **Decryption** | Time to decrypt corresponding tokens |
| **Secret Lifecycle** | Average time for set/get/delete across 1000 operations |
| **Key Rotation** | Total time to rotate key for 100 secrets |

## Output Format

Results are printed to stdout in tabular format with averages in milliseconds.
