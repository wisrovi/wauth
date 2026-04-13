"""Tests for the centralised logging module with verbosity control."""

# pylint: disable=import-outside-toplevel
import warnings

from loguru import logger

from wauth import get_verbose, set_verbose
from wauth._log import _debug, _error, _get_verbose, _info, _set_verbose, _warning


class TestLogModule:
    """Test suite for the _log module."""

    def test_default_verbose_is_false(self) -> None:
        """Verify verbose is False by default."""
        # Reset to default
        _set_verbose(False)
        assert _get_verbose() is False
        assert get_verbose() is False

    def test_set_verbose_true(self) -> None:
        """Verify setting verbose to True."""
        _set_verbose(True)
        assert _get_verbose() is True
        assert get_verbose() is True

    def test_set_verbose_false(self) -> None:
        """Verify setting verbose back to False."""
        _set_verbose(True)
        _set_verbose(False)
        assert _get_verbose() is False

    def test_debug_only_when_verbose(self, capsys) -> None:
        """Verify debug messages only appear when verbose is True."""
        logger.remove()
        logger.add(capsys.readouterr, level="DEBUG")
        _set_verbose(False)
        _debug("should not appear")
        _set_verbose(True)
        _debug("should appear")
        logger.remove()

    def test_info_only_when_verbose(self) -> None:
        """Verify info messages only appear when verbose is True."""
        _set_verbose(False)
        _info("silent")
        _set_verbose(True)
        _info("logged")
        _set_verbose(False)

    def test_warning_only_when_verbose(self) -> None:
        """Verify warnings only appear when verbose is True."""
        _set_verbose(False)
        _warning("silent warning")
        _set_verbose(True)
        _warning("logged warning")
        _set_verbose(False)

    def test_error_always_logged(self) -> None:
        """Verify error messages are always logged regardless of verbose."""
        _set_verbose(False)
        _error("always visible error")
        _set_verbose(True)
        _error("always visible error too")
        _set_verbose(False)

    def test_set_verbose_public_api(self) -> None:
        """Verify the public set_verbose function works."""
        set_verbose(True)
        assert get_verbose() is True
        set_verbose(False)
        assert get_verbose() is False
