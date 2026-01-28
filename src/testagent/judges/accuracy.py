"""
Accuracy Judge - Compare output to expected output.
"""

from typing import Optional, Any
from ..results import TestResult
from ..config import get_config


class AccuracyJudge:
    """
    Judge for accuracy testing - compares output to expected output.
    
    Example:
        >>> judge = AccuracyJudge()
        >>> result = judge.judge("4", expected="4")
        >>> assert result.passed
    """
    
    name = "accuracy"
    description = "Compare output to expected output"
    
    def __init__(self, model: Optional[str] = None, threshold: float = 7.0):
        self.model = model or get_config().model
        self.threshold = threshold
        self._judge = None
    
    def _get_judge(self):
        if self._judge is None:
            try:
                from praisonaiagents.eval import Judge
                self._judge = Judge(model=self.model, threshold=self.threshold)
            except ImportError:
                raise ImportError("praisonaiagents required: pip install praisonaiagents")
        return self._judge
    
    def judge(
        self,
        output: str,
        expected: str,
        **kwargs: Any,
    ) -> TestResult:
        """
        Judge output accuracy against expected.
        
        Args:
            output: The actual output
            expected: The expected output
            
        Returns:
            TestResult with accuracy score
        """
        judge = self._get_judge()
        result = judge.run(output=output, expected=expected, **kwargs)
        
        return TestResult(
            score=result.score,
            passed=result.passed,
            reasoning=result.reasoning,
            expected=expected,
            output=output,
        )


__all__ = ['AccuracyJudge']
