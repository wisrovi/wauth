"""Centralised logging with global verbosity control.

All wauth modules import logging helpers from here instead of
calling ``loguru.logger`` directly.  When verbosity is disabled
(the default), only ``_log_error`` messages are emitted.
"""

from loguru import logger as _raw_logger

# ── Global verbosity flag ─────────────────────────────────────────
_verbose: bool = False


def _set_verbose(enabled: bool) -> None:
    """Enable or disable non-error log output."""
    global _verbose  # noqa: PLW0603
    _verbose = enabled


def _get_verbose() -> bool:
    """Return the current verbose state."""
    return _verbose


# ── Convenience helpers ───────────────────────────────────────────

def _debug(msg: str) -> None:
    """Log at DEBUG level only when verbose is enabled."""
    if _verbose:
        _raw_logger.debug(msg)


def _info(msg: str) -> None:
    """Log at INFO level only when verbose is enabled."""
    if _verbose:
        _raw_logger.info(msg)


def _warning(msg: str) -> None:
    """Log at WARNING level only when verbose is enabled."""
    if _verbose:
        _raw_logger.warning(msg)


def _error(msg: str) -> None:
    """Log at ERROR level regardless of verbosity."""
    _raw_logger.error(msg)
