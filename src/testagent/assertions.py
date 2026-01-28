"""
Assertion helpers for TestAgent - pytest-like assertion utilities.

Inspired by pytest's python_api.py, raises.py, and recwarn.py.

Example:
    >>> from testagent import approx, raises, warns
    >>> 
    >>> # Approximate comparisons
    >>> assert 0.1 + 0.2 == approx(0.3)
    >>> assert result.score == approx(7.5, abs=0.5)
    >>> 
    >>> # Exception testing
    >>> with raises(ValueError, match="invalid"):
    ...     raise ValueError("invalid input")
    >>> 
    >>> # Warning testing
    >>> with warns(DeprecationWarning):
    ...     warnings.warn("deprecated", DeprecationWarning)
"""

from __future__ import annotations

import re
import warnings
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Generator, Type, Pattern


# ============================================================================
# approx() - Approximate comparisons
# ============================================================================

@dataclass
class ApproxScalar:
    """Approximate comparison for a single scalar value."""
    
    expected: float
    rel: float | None = None
    abs: float | None = None
    
    def __eq__(self, actual: Any) -> bool:
        if not isinstance(actual, (int, float)):
            return False
        
        # Default tolerances (same as pytest)
        rel_tol = self.rel if self.rel is not None else 1e-6
        abs_tol = self.abs if self.abs is not None else 1e-12
        
        # If only abs is specified, don't use rel
        if self.abs is not None and self.rel is None:
            return abs(self.expected - actual) <= abs_tol
        
        # If only rel is specified, don't use abs
        if self.rel is not None and self.abs is None:
            return abs(self.expected - actual) <= rel_tol * abs(self.expected)
        
        # Both or neither: use either tolerance
        return (
            abs(self.expected - actual) <= abs_tol or
            abs(self.expected - actual) <= rel_tol * abs(self.expected)
        )
    
    def __ne__(self, actual: Any) -> bool:
        return not self.__eq__(actual)
    
    def __repr__(self) -> str:
        parts = [f"{self.expected}"]
        if self.rel is not None:
            parts.append(f"rel={self.rel}")
        if self.abs is not None:
            parts.append(f"abs={self.abs}")
        return f"approx({', '.join(parts)})"


class ApproxSequence:
    """Approximate comparison for sequences."""
    
    def __init__(self, expected: list | tuple, rel: float | None = None, abs: float | None = None):
        self.expected = expected
        self.rel = rel
        self.abs = abs
    
    def __eq__(self, actual: Any) -> bool:
        if not isinstance(actual, (list, tuple)):
            return False
        if len(actual) != len(self.expected):
            return False
        
        for a, e in zip(actual, self.expected):
            if ApproxScalar(e, rel=self.rel, abs=self.abs) != a:
                return False
        return True
    
    def __ne__(self, actual: Any) -> bool:
        return not self.__eq__(actual)
    
    def __repr__(self) -> str:
        return f"approx({self.expected!r})"


class ApproxMapping:
    """Approximate comparison for mappings (dicts)."""
    
    def __init__(self, expected: dict, rel: float | None = None, abs: float | None = None):
        self.expected = expected
        self.rel = rel
        self.abs = abs
    
    def __eq__(self, actual: Any) -> bool:
        if not isinstance(actual, dict):
            return False
        if actual.keys() != self.expected.keys():
            return False
        
        for key in self.expected:
            if ApproxScalar(self.expected[key], rel=self.rel, abs=self.abs) != actual[key]:
                return False
        return True
    
    def __ne__(self, actual: Any) -> bool:
        return not self.__eq__(actual)
    
    def __repr__(self) -> str:
        return f"approx({self.expected!r})"


def approx(
    expected: float | list | tuple | dict,
    rel: float | None = None,
    abs: float | None = None,
) -> ApproxScalar | ApproxSequence | ApproxMapping:
    """
    Assert that two numbers (or sequences of numbers) are approximately equal.
    
    Args:
        expected: The expected value
        rel: Relative tolerance (default: 1e-6)
        abs: Absolute tolerance (default: 1e-12)
        
    Returns:
        An Approx object that can be compared with ==
        
    Example:
        >>> assert 0.1 + 0.2 == approx(0.3)
        >>> assert result.score == approx(7.5, abs=0.5)
        >>> assert [0.1, 0.2] == approx([0.1, 0.2])
    """
    if isinstance(expected, dict):
        return ApproxMapping(expected, rel=rel, abs=abs)
    elif isinstance(expected, (list, tuple)):
        return ApproxSequence(expected, rel=rel, abs=abs)
    else:
        return ApproxScalar(expected, rel=rel, abs=abs)


# ============================================================================
# raises() - Exception testing
# ============================================================================

@dataclass
class ExceptionInfo:
    """Information about a raised exception."""
    
    type: Type[BaseException]
    value: BaseException
    
    def __str__(self) -> str:
        return str(self.value)


@contextmanager
def raises(
    expected_exception: Type[BaseException] | tuple[Type[BaseException], ...],
    *,
    match: str | Pattern[str] | None = None,
) -> Generator[ExceptionInfo, None, None]:
    """
    Assert that a block of code raises an expected exception.
    
    Args:
        expected_exception: The expected exception type(s)
        match: Optional regex pattern to match against the exception message
        
    Yields:
        ExceptionInfo object with details about the raised exception
        
    Example:
        >>> with raises(ValueError):
        ...     raise ValueError("test")
        >>> 
        >>> with raises(ValueError, match="invalid"):
        ...     raise ValueError("invalid input")
    """
    excinfo = ExceptionInfo(type=Exception, value=Exception())
    
    try:
        yield excinfo
    except expected_exception as e:
        excinfo.type = type(e)
        excinfo.value = e
        
        # Check match pattern if provided
        if match is not None:
            pattern = match if isinstance(match, Pattern) else re.compile(match)
            if not pattern.search(str(e)):
                raise AssertionError(
                    f"Exception message '{e}' does not match pattern '{match}'"
                )
        return
    except BaseException as e:
        raise AssertionError(
            f"Expected {expected_exception}, but got {type(e).__name__}: {e}"
        )
    
    # No exception was raised
    raise AssertionError(
        f"Expected {expected_exception} to be raised, but no exception was raised"
    )


# ============================================================================
# warns() - Warning testing
# ============================================================================

@contextmanager
def warns(
    expected_warning: Type[Warning] | tuple[Type[Warning], ...],
    *,
    match: str | Pattern[str] | None = None,
) -> Generator[list[warnings.WarningMessage], None, None]:
    """
    Assert that a block of code issues an expected warning.
    
    Args:
        expected_warning: The expected warning type(s)
        match: Optional regex pattern to match against the warning message
        
    Yields:
        List of captured warning messages
        
    Example:
        >>> with warns(UserWarning):
        ...     warnings.warn("test", UserWarning)
        >>> 
        >>> with warns(DeprecationWarning, match="deprecated"):
        ...     warnings.warn("deprecated feature", DeprecationWarning)
    """
    with warnings.catch_warnings(record=True) as warning_list:
        warnings.simplefilter("always")
        yield warning_list
    
    # Check that at least one warning of the expected type was issued
    matching_warnings = [
        w for w in warning_list
        if issubclass(w.category, expected_warning)
    ]
    
    if not matching_warnings:
        raise AssertionError(
            f"Expected {expected_warning} to be issued, but no matching warning was found. "
            f"Warnings issued: {[w.category.__name__ for w in warning_list]}"
        )
    
    # Check match pattern if provided
    if match is not None:
        pattern = match if isinstance(match, Pattern) else re.compile(match)
        if not any(pattern.search(str(w.message)) for w in matching_warnings):
            raise AssertionError(
                f"No warning message matches pattern '{match}'. "
                f"Messages: {[str(w.message) for w in matching_warnings]}"
            )


@contextmanager
def deprecated_call(
    *,
    match: str | Pattern[str] | None = None,
) -> Generator[list[warnings.WarningMessage], None, None]:
    """
    Assert that a block of code issues a deprecation warning.
    
    Captures DeprecationWarning, PendingDeprecationWarning, and FutureWarning.
    
    Args:
        match: Optional regex pattern to match against the warning message
        
    Yields:
        List of captured warning messages
        
    Example:
        >>> with deprecated_call():
        ...     warnings.warn("deprecated", DeprecationWarning)
    """
    with warns(
        (DeprecationWarning, PendingDeprecationWarning, FutureWarning),
        match=match,
    ) as warning_list:
        yield warning_list


__all__ = [
    'approx',
    'ApproxScalar',
    'ApproxSequence',
    'ApproxMapping',
    'raises',
    'ExceptionInfo',
    'warns',
    'deprecated_call',
]
