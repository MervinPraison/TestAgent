"""
Judge registry for TestAgent.

Allows registering custom judges for different testing scenarios.
"""

from typing import Dict, Type, Optional


# Global judge registry
_JUDGE_REGISTRY: Dict[str, Type] = {}


def add_judge(name: str, judge_class: Type) -> None:
    """
    Register a custom judge.
    
    Args:
        name: Name for the judge
        judge_class: Judge class implementing TestProtocol
        
    Example:
        >>> class MyJudge:
        ...     def run(self, output, **kwargs):
        ...         return TestResult(score=10.0, passed=True, reasoning="Perfect")
        >>> add_judge("my_judge", MyJudge)
    """
    _JUDGE_REGISTRY[name.lower()] = judge_class


def get_judge(name: str) -> Optional[Type]:
    """
    Get a registered judge by name.
    
    Args:
        name: Name of the judge
        
    Returns:
        Judge class or None if not found
    """
    return _JUDGE_REGISTRY.get(name.lower())


def list_judges() -> list:
    """
    List all registered judges.
    
    Returns:
        List of judge names
    """
    return list(_JUDGE_REGISTRY.keys())


def remove_judge(name: str) -> bool:
    """
    Remove a registered judge.
    
    Args:
        name: Name of the judge to remove
        
    Returns:
        True if removed, False if not found
    """
    if name.lower() in _JUDGE_REGISTRY:
        del _JUDGE_REGISTRY[name.lower()]
        return True
    return False


__all__ = ['add_judge', 'get_judge', 'list_judges', 'remove_judge']
