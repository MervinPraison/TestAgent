"""
Core TestAgent functionality - the world's easiest AI testing.

This module provides the main test functions that wrap praisonaiagents.
"""

from typing import Optional, Any
from .results import TestResult
from .config import TestConfig, get_config


class TestAgent:
    """
    Main TestAgent class for running AI-powered tests.
    
    Wraps praisonaiagents Judge for the simplest possible API.
    
    Example:
        >>> tester = TestAgent()
        >>> result = tester.run("Hello world", criteria="is a greeting")
        >>> assert result.passed
    """
    
    def __init__(self, config: Optional[TestConfig] = None):
        """
        Initialize TestAgent.
        
        Args:
            config: Optional configuration. Uses global config if not provided.
        """
        self.config = config or get_config()
        self._judge = None
    
    def _get_judge(self):
        """Lazy load the judge from praisonaiagents."""
        if self._judge is None:
            try:
                from praisonaiagents.eval import Judge
                self._judge = Judge(
                    model=self.config.model,
                    temperature=self.config.temperature,
                    threshold=self.config.threshold,
                )
            except ImportError:
                raise ImportError(
                    "praisonaiagents is required. Install with: pip install praisonaiagents"
                )
        return self._judge
    
    def run(
        self,
        output: str,
        expected: Optional[str] = None,
        criteria: Optional[str] = None,
        **kwargs: Any,
    ) -> TestResult:
        """
        Run an AI test on the output.
        
        Args:
            output: The output to test
            expected: Optional expected output for comparison
            criteria: Optional custom criteria for evaluation
            **kwargs: Additional arguments passed to judge
            
        Returns:
            TestResult with score, passed, and reasoning
        """
        judge = self._get_judge()
        
        # Use praisonaiagents Judge
        result = judge.run(
            output=output,
            expected=expected,
            criteria=criteria,
            **kwargs,
        )
        
        # Convert to TestResult
        return TestResult(
            score=result.score,
            passed=result.passed,
            reasoning=result.reasoning,
            criteria=criteria,
            expected=expected,
            output=output,
        )
    
    async def run_async(
        self,
        output: str,
        expected: Optional[str] = None,
        criteria: Optional[str] = None,
        **kwargs: Any,
    ) -> TestResult:
        """Run an AI test asynchronously."""
        judge = self._get_judge()
        
        result = await judge.run_async(
            output=output,
            expected=expected,
            criteria=criteria,
            **kwargs,
        )
        
        return TestResult(
            score=result.score,
            passed=result.passed,
            reasoning=result.reasoning,
            criteria=criteria,
            expected=expected,
            output=output,
        )


# Global TestAgent instance for simple API
_default_tester: Optional[TestAgent] = None


def _get_tester() -> TestAgent:
    """Get the global default tester."""
    global _default_tester
    if _default_tester is None:
        _default_tester = TestAgent()
    return _default_tester


def test(
    output: str,
    expected: Optional[str] = None,
    criteria: Optional[str] = None,
    **kwargs: Any,
) -> TestResult:
    """
    Test any output using AI.
    
    The simplest possible API for AI testing.
    
    Args:
        output: The output to test
        expected: Optional expected output for comparison
        criteria: Optional custom criteria (default: "is correct and complete")
        **kwargs: Additional arguments
        
    Returns:
        TestResult with score, passed, and reasoning
        
    Example:
        >>> result = test("The capital of France is Paris", criteria="factually correct")
        >>> assert result.passed
        
        >>> result = test("4", expected="4")  # Accuracy test
        >>> assert result.score >= 9.0
    """
    if criteria is None and expected is None:
        criteria = "is correct and complete"
    
    return _get_tester().run(output, expected=expected, criteria=criteria, **kwargs)


def accuracy(
    output: str,
    expected: str,
    **kwargs: Any,
) -> TestResult:
    """
    Test output accuracy against expected output.
    
    Args:
        output: The actual output
        expected: The expected output
        **kwargs: Additional arguments
        
    Returns:
        TestResult with accuracy score
        
    Example:
        >>> result = accuracy("4", expected="4")
        >>> assert result.passed
    """
    return _get_tester().run(output, expected=expected, **kwargs)


def criteria(
    output: str,
    criteria: str,
    **kwargs: Any,
) -> TestResult:
    """
    Test output against custom criteria.
    
    Args:
        output: The output to test
        criteria: The criteria to evaluate against
        **kwargs: Additional arguments
        
    Returns:
        TestResult with criteria evaluation
        
    Example:
        >>> result = criteria("Hello world!", criteria="is a friendly greeting")
        >>> assert result.passed
    """
    return _get_tester().run(output, criteria=criteria, **kwargs)


__all__ = ['TestAgent', 'test', 'accuracy', 'criteria']
