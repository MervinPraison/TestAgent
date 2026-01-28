"""
Protocols for TestAgent - extending praisonaiagents protocols.

TestAgent provides its own protocol layer that wraps praisonaiagents,
making it the world's easiest AI testing interface.
"""

from typing import Protocol, runtime_checkable, Optional, Dict, Any


@runtime_checkable
class TestResultProtocol(Protocol):
    """
    Protocol for test results.
    
    Minimal interface for any AI test result.
    """
    score: float
    passed: bool
    reasoning: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        ...


@runtime_checkable
class TestProtocol(Protocol):
    """
    Protocol for AI tests.
    
    Defines the interface for testing anything with AI.
    
    Example:
        >>> class MyTest:
        ...     def run(self, output, criteria="is correct"):
        ...         return TestResult(score=9.0, passed=True, reasoning="Good")
        >>> 
        >>> tester: TestProtocol = MyTest()
        >>> result = tester.run("Hello world", criteria="is a greeting")
    """
    
    def run(
        self,
        output: str,
        expected: Optional[str] = None,
        criteria: Optional[str] = None,
        **kwargs: Any,
    ) -> TestResultProtocol:
        """
        Run an AI test on the output.
        
        Args:
            output: The output to test
            expected: Optional expected output for comparison
            criteria: Optional custom criteria for evaluation
            **kwargs: Additional arguments
            
        Returns:
            A TestResultProtocol with score, passed, and reasoning
        """
        ...
    
    async def run_async(
        self,
        output: str,
        expected: Optional[str] = None,
        criteria: Optional[str] = None,
        **kwargs: Any,
    ) -> TestResultProtocol:
        """Run an AI test asynchronously."""
        ...


@runtime_checkable
class JudgeModuleProtocol(Protocol):
    """
    Protocol for judge modules (accuracy, criteria, code, api, etc.).
    
    Each judge module specializes in a specific type of testing.
    """
    name: str
    description: str
    
    def judge(
        self,
        output: str,
        **kwargs: Any,
    ) -> TestResultProtocol:
        """Judge the output."""
        ...


__all__ = [
    'TestResultProtocol',
    'TestProtocol',
    'JudgeModuleProtocol',
]
