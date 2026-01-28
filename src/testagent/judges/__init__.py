"""
Judge modules for TestAgent.

Each module specializes in a specific type of AI testing:
- accuracy: Compare output to expected output
- criteria: Evaluate against custom criteria
- code: Evaluate code quality and correctness
- api: Test API responses
- safety: Test for harmful content
"""

__all__ = [
    'AccuracyJudge',
    'CriteriaJudge',
    'CodeJudge',
    'APIJudge',
    'SafetyJudge',
]

# Lazy imports
_LAZY_IMPORTS = {
    'AccuracyJudge': ('accuracy', 'AccuracyJudge'),
    'CriteriaJudge': ('criteria_judge', 'CriteriaJudge'),
    'CodeJudge': ('code', 'CodeJudge'),
    'APIJudge': ('api', 'APIJudge'),
    'SafetyJudge': ('safety', 'SafetyJudge'),
}


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module_name, attr_name = _LAZY_IMPORTS[name]
        import importlib
        module = importlib.import_module(f".{module_name}", __name__)
        return getattr(module, attr_name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
