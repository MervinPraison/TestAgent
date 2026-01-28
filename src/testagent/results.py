"""
Result classes for TestAgent.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class TestResult:
    """
    Result of an AI test.
    
    Attributes:
        score: Score from 0-10
        passed: Whether the test passed
        reasoning: Explanation of the score
        criteria: The criteria used for evaluation
        expected: The expected output (if any)
        output: The actual output tested
        duration: Time taken for the test in seconds
        start: Start time (epoch seconds)
        stop: Stop time (epoch seconds)
    """
    score: float
    passed: bool
    reasoning: str
    criteria: Optional[str] = None
    expected: Optional[str] = None
    output: Optional[str] = None
    duration: float = 0.0
    start: float = 0.0
    stop: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "score": self.score,
            "passed": self.passed,
            "reasoning": self.reasoning,
            "criteria": self.criteria,
            "expected": self.expected,
            "output": self.output,
            "duration": self.duration,
            "start": self.start,
            "stop": self.stop,
            "metadata": self.metadata,
        }
    
    def __bool__(self) -> bool:
        """Allow using result in boolean context."""
        return self.passed
    
    def __repr__(self) -> str:
        status = "✅ PASSED" if self.passed else "❌ FAILED"
        duration_str = f", {self.duration:.2f}s" if self.duration > 0 else ""
        return f"TestResult({status}, score={self.score}/10{duration_str})"


__all__ = ['TestResult']
