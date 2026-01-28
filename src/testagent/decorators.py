"""
Decorators for TestAgent - pytest-like syntax for AI testing.

Example:
    >>> @testagent.mark.criteria("output is helpful")
    ... def test_helpfulness():
    ...     return "Hello, how can I help you?"
"""

from typing import Callable
from functools import wraps


class Mark:
    """
    Pytest-like mark decorator for AI tests.
    
    Example:
        >>> @mark.criteria("is a valid greeting")
        ... def test_greeting():
        ...     return "Hello world!"
        
        >>> @mark.accuracy(expected="4")
        ... def test_math():
        ...     return "4"
    """
    
    def criteria(self, criteria: str, threshold: float = 7.0):
        """
        Mark a test function with criteria.
        
        Args:
            criteria: The criteria to evaluate against
            threshold: Score threshold for passing (default: 7.0)
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                from .core import test
                output = func(*args, **kwargs)
                result = test(str(output), criteria=criteria)
                if result.score < threshold:
                    raise AssertionError(
                        f"AI test failed: {result.reasoning} (score: {result.score}/10)"
                    )
                return result
            
            # Store metadata for test discovery
            wrapper._testagent_criteria = criteria
            wrapper._testagent_threshold = threshold
            return wrapper
        return decorator
    
    def accuracy(self, expected: str, threshold: float = 7.0):
        """
        Mark a test function for accuracy testing.
        
        Args:
            expected: The expected output
            threshold: Score threshold for passing (default: 7.0)
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                from .core import accuracy
                output = func(*args, **kwargs)
                result = accuracy(str(output), expected=expected)
                if result.score < threshold:
                    raise AssertionError(
                        f"AI accuracy test failed: {result.reasoning} (score: {result.score}/10)"
                    )
                return result
            
            wrapper._testagent_expected = expected
            wrapper._testagent_threshold = threshold
            return wrapper
        return decorator
    
    def skip(self, reason: str = ""):
        """
        Skip an AI test.
        
        Args:
            reason: Reason for skipping
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                from .outcomes import skip as skip_fn
                skip_fn(reason or "AI test skipped")
            
            wrapper._testagent_skip = True
            wrapper._testagent_skip_reason = reason
            return wrapper
        return decorator
    
    def skipif(self, condition: bool, *, reason: str):
        """
        Skip an AI test if condition is true.
        
        Args:
            condition: Boolean condition to evaluate
            reason: Reason for skipping (required)
            
        Example:
            >>> @mark.skipif(sys.platform == 'win32', reason="Not supported on Windows")
            ... def test_unix_only():
            ...     pass
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                if condition:
                    from .outcomes import skip as skip_fn
                    skip_fn(reason)
                return func(*args, **kwargs)
            
            wrapper._testagent_skipif = True
            wrapper._testagent_skipif_condition = condition
            wrapper._testagent_skipif_reason = reason
            return wrapper
        return decorator
    
    def xfail(self, reason: str = "", *, strict: bool = False):
        """
        Mark a test as expected to fail.
        
        Args:
            reason: Reason for expected failure
            strict: If True, passing test is a failure
            
        Example:
            >>> @mark.xfail(reason="Known bug #123")
            ... def test_known_bug():
            ...     pass
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                from .outcomes import XFailed
                try:
                    result = func(*args, **kwargs)
                    # Test passed when expected to fail
                    if strict:
                        # Re-raise outside try block to avoid catching
                        pass
                    else:
                        # Mark as xpass (expected fail but passed)
                        wrapper._testagent_xpass = True
                        return result
                except (AssertionError, Exception):
                    # Test failed as expected
                    wrapper._testagent_xfail_triggered = True
                    raise XFailed(reason)
                
                # Strict mode: passing is a failure (raised outside try/except)
                if strict:
                    raise AssertionError(f"[XPASS(strict)] {reason}")
            
            wrapper._testagent_xfail = True
            wrapper._testagent_xfail_reason = reason
            wrapper._testagent_xfail_strict = strict
            return wrapper
        return decorator


    def parametrize(self, argnames: str, argvalues: list):
        """
        Parametrize a test function with multiple inputs.
        
        Args:
            argnames: Comma-separated string of argument names
            argvalues: List of values or param() objects
            
        Example:
            >>> @mark.parametrize("x, y", [(1, 2), (3, 4)])
            ... def test_add(x, y):
            ...     return x + y
        """
        # Parse argument names
        if isinstance(argnames, str):
            names = [n.strip() for n in argnames.split(",") if n.strip()]
        else:
            names = list(argnames)
        
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                results = []
                for values in argvalues:
                    # Handle ParameterSet objects
                    if hasattr(values, 'values'):
                        actual_values = values.values
                    elif len(names) == 1 and not isinstance(values, (list, tuple)):
                        actual_values = (values,)
                    else:
                        actual_values = values
                    
                    # Build kwargs for this iteration
                    call_kwargs = dict(zip(names, actual_values))
                    call_kwargs.update(kwargs)
                    
                    result = func(*args, **call_kwargs)
                    results.append(result)
                
                return results
            
            # Store metadata
            wrapper._testagent_parametrize = {
                'argnames': names,
                'argvalues': argvalues,
            }
            return wrapper
        return decorator


# Global mark instance
mark = Mark()


# ============================================================================
# ParameterSet - for param() function
# ============================================================================

class ParameterSet:
    """
    A set of parameter values with optional marks and ID.
    
    Example:
        >>> param(1, 2, id="test_case")
        >>> param(42, marks=mark.skip(reason="skip"))
    """
    
    def __init__(self, values: tuple, marks: tuple = (), id: str | None = None):
        self.values = values
        self.marks = marks
        self.id = id
    
    def __repr__(self) -> str:
        if self.id:
            return f"param({', '.join(map(repr, self.values))}, id={self.id!r})"
        return f"param({', '.join(map(repr, self.values))})"


def param(*values, marks=(), id: str | None = None) -> ParameterSet:
    """
    Create a parameter set for use with @mark.parametrize.
    
    Args:
        *values: The parameter values
        marks: Optional marks to apply
        id: Optional ID for the parameter set
        
    Returns:
        ParameterSet object
        
    Example:
        >>> @mark.parametrize("x", [
        ...     param(1, id="one"),
        ...     param(2, id="two"),
        ... ])
        ... def test_func(x):
        ...     pass
    """
    if not isinstance(marks, tuple):
        marks = (marks,)
    return ParameterSet(values, marks, id)


# ============================================================================
# fixture decorator
# ============================================================================

def fixture(func: Callable = None, *, scope: str = "function"):
    """
    Decorator to mark a function as a fixture.
    
    Args:
        func: The fixture function
        scope: Scope of the fixture ("function", "class", "module", "session")
        
    Example:
        >>> @fixture
        ... def my_fixture():
        ...     return "value"
        >>> 
        >>> @fixture(scope="session")
        ... def session_fixture():
        ...     return "session_value"
    """
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        
        wrapper._testagent_fixture = True
        wrapper._testagent_fixture_scope = scope
        return wrapper
    
    # Handle both @fixture and @fixture(scope="session")
    if func is not None:
        return decorator(func)
    return decorator


__all__ = ['mark', 'Mark', 'param', 'ParameterSet', 'fixture']
