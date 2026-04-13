"""Tests for the deprecation utilities.

Verifies that the ``@deprecated`` decorator and ``warn_deprecated``
helper emit proper warnings and log messages.
"""

import warnings

# pylint: disable=import-outside-toplevel
from loguru import logger

from wauth.deprecation import deprecated, warn_deprecated


class TestDeprecatedDecorator:
    """Test suite for the @deprecated decorator."""

    def test_decorator_emits_warning(self) -> None:
        """Verify that calling a decorated function emits a warning."""
        @deprecated(since="1.6.0", removal="2.0.0", replacement="new_func")
        def old_func() -> str:
            return "old"

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = old_func()
            assert result == "old"
            assert len(caught) == 1
            assert issubclass(caught[0].category, DeprecationWarning)
            assert "1.6.0" in str(caught[0].message)
            assert "new_func" in str(caught[0].message)
        logger.info("Deprecated decorator emits warning on first call")

    def test_decorator_only_warns_once(self) -> None:
        """Verify that the warning is only emitted once per function."""
        @deprecated(since="1.6.0", removal="2.0.0")
        def once_func() -> int:
            return 42

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            once_func()
            once_func()
            once_func()
            assert len(caught) == 1
        logger.info("Deprecated decorator warns only once")

    def test_decorator_without_replacement(self) -> None:
        """Verify decorator works without a replacement name."""
        @deprecated(since="1.7.0", removal="3.0.0")
        def removed_func() -> None:
            pass

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            removed_func()
            msg = str(caught[0].message)
            assert "instead" not in msg
        logger.info("Deprecated decorator works without replacement")

    def test_decorator_with_reason(self) -> None:
        """Verify decorator includes the reason in the warning."""
        @deprecated(
            since="1.6.0",
            removal="2.0.0",
            replacement="new_api",
            reason="Performance improved.",
        )
        def reason_func() -> None:
            pass

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            reason_func()
            msg = str(caught[0].message)
            assert "Performance improved" in msg
        logger.info("Deprecated decorator includes reason")


class TestWarnDeprecated:
    """Test suite for the warn_deprecated helper function."""

    def test_warn_deprecated_emits_warning(self) -> None:
        """Verify warn_deprecated emits a DeprecationWarning."""
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            warn_deprecated("old_param", "1.6.0", "2.0.0", "new_param")
            assert len(caught) == 1
            assert issubclass(caught[0].category, DeprecationWarning)
        logger.info("warn_deprecated emits DeprecationWarning")

    def test_warn_deprecated_without_replacement(self) -> None:
        """Verify warn_deprecated works without a replacement."""
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            warn_deprecated("legacy_mode", "1.6.0", "2.0.0")
            msg = str(caught[0].message)
            assert "legacy_mode" in msg
            assert "2.0.0" in msg
        logger.info("warn_deprecated works without replacement")
