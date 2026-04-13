"""Performance benchmarks for WAuth.

Measures encryption/decryption throughput, secret storage latency,
and key rotation performance across various payload sizes.

Run with:
    python benchmarks/performance.py
"""

import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wauth import WAuth
from wauth.core import CryptoEngine


def benchmark_encrypt(sizes: list[int], iterations: int = 100) -> dict[int, float]:
    """Benchmark encryption speed across payload sizes.

    Args:
        sizes: List of payload sizes in bytes.
        iterations: Number of iterations per size.

    Returns:
        Dict mapping payload size to average time per operation (ms).
    """
    engine = CryptoEngine()
    results: dict[int, float] = {}

    for size in sizes:
        data = b"A" * size
        start = time.perf_counter()
        for _ in range(iterations):
            engine.encrypt(data)
        elapsed = time.perf_counter() - start
        avg_ms = (elapsed / iterations) * 1000
        results[size] = avg_ms
        print(f"  Encrypt {size:>6}B: {avg_ms:.4f} ms avg ({iterations} iterations)")

    return results


def benchmark_decrypt(sizes: list[int], iterations: int = 100) -> dict[int, float]:
    """Benchmark decryption speed across payload sizes.

    Args:
        sizes: List of payload sizes in bytes.
        iterations: Number of iterations per size.

    Returns:
        Dict mapping payload size to average time per operation (ms).
    """
    engine = CryptoEngine()
    results: dict[int, float] = {}

    for size in sizes:
        data = b"A" * size
        token = engine.encrypt(data)
        start = time.perf_counter()
        for _ in range(iterations):
            engine.decrypt(token)
        elapsed = time.perf_counter() - start
        avg_ms = (elapsed / iterations) * 1000
        results[size] = avg_ms
        print(f"  Decrypt {size:>6}B: {avg_ms:.4f} ms avg ({iterations} iterations)")

    return results


def benchmark_secret_lifecycle(count: int = 1000) -> dict[str, float]:
    """Benchmark full secret lifecycle (set + get + delete).

    Args:
        count: Number of secrets to create.

    Returns:
        Dict with set_ms, get_ms, delete_ms averages.
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        auth = WAuth(db_path=db_path)

        # Benchmark set
        start = time.perf_counter()
        for i in range(count):
            auth.set(f"BENCH_KEY_{i}", f"value_{i}")
        set_ms = ((time.perf_counter() - start) / count) * 1000

        # Benchmark get
        start = time.perf_counter()
        for i in range(count):
            auth.get(f"BENCH_KEY_{i}")
        get_ms = ((time.perf_counter() - start) / count) * 1000

        # Benchmark delete
        start = time.perf_counter()
        for i in range(count):
            auth.delete(f"BENCH_KEY_{i}")
        delete_ms = ((time.perf_counter() - start) / count) * 1000

        print(f"  set():    {set_ms:.4f} ms avg ({count} operations)")
        print(f"  get():    {get_ms:.4f} ms avg ({count} operations)")
        print(f"  delete(): {delete_ms:.4f} ms avg ({count} operations)")

        return {"set_ms": set_ms, "get_ms": get_ms, "delete_ms": delete_ms}
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def benchmark_key_rotation(count: int = 100) -> float:
    """Benchmark key rotation performance.

    Args:
        count: Number of secrets to rotate.

    Returns:
        Total time for rotation in milliseconds.
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        auth = WAuth(db_path=db_path)
        for i in range(count):
            auth.set(f"ROT_KEY_{i}", f"value_{i}")

        start = time.perf_counter()
        results = auth.rotate_key("new-benchmark-key")
        elapsed = (time.perf_counter() - start) * 1000

        success = sum(1 for v in results.values() if v)
        print(f"  Rotate {count} keys: {elapsed:.2f} ms total ({success}/{count} succeeded)")

        return elapsed
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def main() -> None:
    """Run all benchmarks."""
    print("=" * 60)
    print("  WAuth Performance Benchmarks")
    print("=" * 60)

    print("\n--- Encryption ---")
    benchmark_encrypt([16, 64, 256, 1024, 4096, 16384])

    print("\n--- Decryption ---")
    benchmark_decrypt([16, 64, 256, 1024, 4096, 16384])

    print("\n--- Secret Lifecycle (1000 operations) ---")
    benchmark_secret_lifecycle(1000)

    print("\n--- Key Rotation (100 keys) ---")
    benchmark_key_rotation(100)

    print("\n" + "=" * 60)
    print("  Benchmarks complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
