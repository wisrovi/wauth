"""Deprecation utilities for WAuth.

Provides a decorator and helper functions to mark deprecated APIs
with proper warnings, enabling graceful migration across versions.
"""

import functools
import warnings
from typing import Any, Callable, TypeVar

from ._log import _debug, _error, _info, _warning

T = TypeVar("T", bound=Callable[..., Any])


def deprecated(
    since: str,
    removal: str,
    replacement: str | None = None,
    reason: str = "",
) -> Callable[[T], T]:
    """Mark a function or method as deprecated.

    Emits a ``DeprecationWarning`` on first use and logs the deprecation
    via loguru.

    Args:
        since: Version when the deprecation was introduced (e.g., ``"1.6.0"``).
        removal: Version when the API will be removed (e.g., ``"2.0.0"``).
        replacement: Name of the replacement API, if any.
        reason: Additional explanation for the deprecation.

    Returns:
        Decorated function that emits a warning on invocation.

    Example:
        >>> @deprecated(since="1.6.0", removal="2.0.0", replacement="get_secret")
        ... def old_method():
        ...     pass
    """
    message = (
        f"Deprecated since v{since}. "
        f"Will be removed in v{removal}."
    )
    if replacement:
        message += f" Use ``{replacement}`` instead."
    if reason:
        message += f" {reason}"

    def decorator(func: T) -> T:
        warned: bool = False

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal warned
            if not warned:
                warnings.warn(message, DeprecationWarning, stacklevel=2)
                _warning(f"DEPRECATED: {func.__name__}() — {message}")
                warned = True
            return func(*args, **kwargs)

        # Expose the deprecation message for introspection
        wrapper.__deprecated_message__ = message  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]

    return decorator


def warn_deprecated(
    name: str,
    since: str,
    removal: str,
    replacement: str | None = None,
) -> None:
    """Emit a deprecation warning without a decorator.

    Useful for code paths that cannot be decorated (e.g., inside
    conditional branches).

    Args:
        name: Name of the deprecated element.
        since: Version when the deprecation was introduced.
        removal: Version when it will be removed.
        replacement: Name of the replacement, if any.
    """
    message = f"{name} is deprecated since v{since} and will be removed in v{removal}."
    if replacement:
        message += f" Use {replacement} instead."
    warnings.warn(message, DeprecationWarning, stacklevel=3)
    _warning(f"DEPRECATED: {message}")
