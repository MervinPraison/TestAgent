"""
TestAgent - The world's easiest way to test anything using AI.

Simple, pytest-like AI testing framework powered by praisonaiagents.

Usage:
    >>> from testagent import test
    >>> result = test("The capital of France is Paris", criteria="factually correct")
    >>> assert result.passed
    
    >>> from testagent import accuracy, criteria
    >>> result = accuracy("4", expected="4")  # Compare outputs
    >>> result = criteria("Hello world", criteria="greeting is friendly")

CLI:
    $ testagent "The output is correct" --criteria "factually accurate"
    $ testagent accuracy "4" --expected "4"
"""

__version__ = "0.1.0"
__all__ = [
    # Core functions
    "test",
    "accuracy",
    "criteria",
    # Protocols
    "TestProtocol",
    "TestResultProtocol",
    # Classes
    "TestAgent",
    "TestResult",
    "TestConfig",
    # Decorators
    "mark",
    # Registry
    "add_judge",
    "get_judge",
    "list_judges",
    # Caching
    "TestAgentCache",
    "CacheKey",
    # Timing
    "Instant",
    "Duration",
    # Collection
    "Collector",
    "collect",
    # Parallel
    "ParallelRunner",
    "run_parallel",
    # Outcomes
    "skip",
    "fail",
    "xfail",
    "importorskip",
    "Skipped",
    "Failed",
    "XFailed",
    # Assertions
    "approx",
    "raises",
    "warns",
    "deprecated_call",
    # Parametrize & Fixtures
    "param",
    "ParameterSet",
    "fixture",
]

# Lazy imports for zero performance impact
_LAZY_IMPORTS = {
    "test": ("core", "test"),
    "accuracy": ("core", "accuracy"),
    "criteria": ("core", "criteria"),
    "TestProtocol": ("protocols", "TestProtocol"),
    "TestResultProtocol": ("protocols", "TestResultProtocol"),
    "TestAgent": ("core", "TestAgent"),
    "TestResult": ("results", "TestResult"),
    "TestConfig": ("config", "TestConfig"),
    "mark": ("decorators", "mark"),
    "add_judge": ("registry", "add_judge"),
    "get_judge": ("registry", "get_judge"),
    "list_judges": ("registry", "list_judges"),
    # Caching
    "TestAgentCache": ("cache", "TestAgentCache"),
    "CacheKey": ("cache", "CacheKey"),
    # Timing
    "Instant": ("timing", "Instant"),
    "Duration": ("timing", "Duration"),
    # Collection
    "Collector": ("collector", "Collector"),
    "collect": ("collector", "collect"),
    # Parallel
    "ParallelRunner": ("parallel", "ParallelRunner"),
    "run_parallel": ("parallel", "run_parallel"),
    # Outcomes
    "skip": ("outcomes", "skip"),
    "fail": ("outcomes", "fail"),
    "xfail": ("outcomes", "xfail"),
    "importorskip": ("outcomes", "importorskip"),
    "Skipped": ("outcomes", "Skipped"),
    "Failed": ("outcomes", "Failed"),
    "XFailed": ("outcomes", "XFailed"),
    # Assertions
    "approx": ("assertions", "approx"),
    "raises": ("assertions", "raises"),
    "warns": ("assertions", "warns"),
    "deprecated_call": ("assertions", "deprecated_call"),
    # Parametrize & Fixtures
    "param": ("decorators", "param"),
    "ParameterSet": ("decorators", "ParameterSet"),
    "fixture": ("decorators", "fixture"),
}


def __getattr__(name: str):
    """Lazy import mechanism for zero-cost imports when not used."""
    if name in _LAZY_IMPORTS:
        module_name, attr_name = _LAZY_IMPORTS[name]
        import importlib
        module = importlib.import_module(f".{module_name}", __name__)
        return getattr(module, attr_name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    """Return list of available attributes for tab completion."""
    return __all__
