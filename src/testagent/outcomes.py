"""
Outcome exceptions and functions for TestAgent.

Inspired by pytest's outcomes.py for robust test control flow.

Example:
    >>> from testagent import skip, fail, xfail, importorskip
    >>> 
    >>> # Skip a test
    >>> skip("Not implemented yet")
    >>> 
    >>> # Fail explicitly
    >>> fail("This should not happen")
    >>> 
    >>> # Expected failure
    >>> xfail("Known bug #123")
    >>> 
    >>> # Skip if module not available
    >>> np = importorskip("numpy")
"""

from __future__ import annotations

import sys
from typing import Any, NoReturn, ClassVar


class OutcomeException(BaseException):
    """
    Base exception for test outcomes.
    
    Inherits from BaseException to avoid being caught by generic
    except Exception handlers.
    """
    
    def __init__(self, msg: str | None = None) -> None:
        if msg is not None and not isinstance(msg, str):
            raise TypeError(
                f"{type(self).__name__} expected string as 'msg' parameter, "
                f"got '{type(msg).__name__}' instead."
            )
        super().__init__(msg)
        self.msg = msg or ""
    
    def __repr__(self) -> str:
        if self.msg:
            return self.msg
        return f"<{self.__class__.__name__} instance>"
    
    __str__ = __repr__


class Skipped(OutcomeException):
    """
    Exception raised when a test is skipped.
    
    Example:
        >>> raise Skipped("Not implemented yet")
    """
    __module__ = "builtins"


class Failed(OutcomeException):
    """
    Exception raised when a test fails explicitly.
    
    Example:
        >>> raise Failed("Assertion failed")
    """
    __module__ = "builtins"


class XFailed(Failed):
    """
    Exception raised for expected failures.
    
    Example:
        >>> raise XFailed("Known bug")
    """
    pass


class _Skip:
    """
    Skip an executing test with the given reason.
    
    Example:
        >>> skip("Not implemented yet")
    """
    
    Exception: ClassVar[type[Skipped]] = Skipped
    
    def __call__(self, reason: str = "") -> NoReturn:
        raise Skipped(msg=reason)


skip: _Skip = _Skip()


class _Fail:
    """
    Explicitly fail an executing test with the given reason.
    
    Example:
        >>> fail("This should not happen")
    """
    
    Exception: ClassVar[type[Failed]] = Failed
    
    def __call__(self, reason: str = "") -> NoReturn:
        raise Failed(msg=reason)


fail: _Fail = _Fail()


class _XFail:
    """
    Mark an executing test as an expected failure.
    
    Example:
        >>> xfail("Known bug #123")
    """
    
    Exception: ClassVar[type[XFailed]] = XFailed
    
    def __call__(self, reason: str = "") -> NoReturn:
        raise XFailed(msg=reason)


xfail: _XFail = _XFail()


def importorskip(
    modname: str,
    minversion: str | None = None,
    reason: str | None = None,
) -> Any:
    """
    Import and return the requested module, or skip the test if unavailable.
    
    Args:
        modname: The name of the module to import
        minversion: If given, the module's __version__ must be at least this
        reason: Custom reason for the skip message
        
    Returns:
        The imported module
        
    Raises:
        Skipped: If the module cannot be imported
        
    Example:
        >>> np = importorskip("numpy")
        >>> pd = importorskip("pandas", minversion="1.0.0")
    """
    import importlib
    import warnings
    
    # Validate module name
    compile(modname, "", "eval")
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        try:
            importlib.import_module(modname)
        except ImportError as exc:
            if reason is None:
                reason = f"could not import {modname!r}: {exc}"
            raise Skipped(reason)
    
    mod = sys.modules[modname]
    
    if minversion is None:
        return mod
    
    verattr = getattr(mod, "__version__", None)
    if verattr is not None:
        # Lazy import to avoid dependency
        try:
            from packaging.version import Version
            if Version(verattr) < Version(minversion):
                raise Skipped(
                    f"module {modname!r} has __version__ {verattr!r}, "
                    f"required is: {minversion!r}"
                )
        except ImportError:
            # packaging not available, do simple string comparison
            if verattr < minversion:
                raise Skipped(
                    f"module {modname!r} has __version__ {verattr!r}, "
                    f"required is: {minversion!r}"
                )
    
    return mod


__all__ = [
    'OutcomeException',
    'Skipped',
    'Failed',
    'XFailed',
    'skip',
    'fail',
    'xfail',
    'importorskip',
]
