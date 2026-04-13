"""Pytest configuration and shared fixtures for wauth tests.

Provides temporary database paths, cleanup utilities, and common
fixtures used across all test modules.
"""

import os
from pathlib import Path
from typing import Generator

import pytest
from loguru import logger


@pytest.fixture(name="tmp_db_path")
def fixture_tmp_db_path(tmp_path: Path) -> str:
    """Provide a temporary database path for test isolation.

    Args:
        tmp_path: Pytest-built-in temporary directory fixture.

    Returns:
        Absolute path to a temporary SQLite database file.
    """
    db_file = tmp_path / "test_wauth.db"
    logger.debug(f"Temporary DB path: {db_file}")
    return str(db_file)


@pytest.fixture(name="clean_env")
def fixture_clean_env() -> Generator[None, None, None]:
    """Ensure a clean environment with no interfering variables.

    Yields:
        None — environment is restored after test.
    """
    logger.debug("Cleaning environment for test isolation")
    yield
    logger.debug("Restoring environment after test")


@pytest.fixture(autouse=True)
def cleanup_db_files(tmp_db_path: str) -> Generator[None, None, None]:
    """Automatically clean up any leftover database files after each test.

    Args:
        tmp_db_path: Path to the temporary database file.

    Yields:
        None — cleanup occurs after test completion.
    """
    yield
    if os.path.exists(tmp_db_path):
        logger.debug(f"Cleaning up: {tmp_db_path}")
        try:
            os.remove(tmp_db_path)
        except OSError:
            pass
