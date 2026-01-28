"""
Code Judge - Evaluate code quality and correctness.
"""

from typing import Optional, Any
from ..results import TestResult
from ..config import get_config


class CodeJudge:
    """
    Judge for code quality testing.
    
    Example:
        >>> judge = CodeJudge()
        >>> result = judge.judge("def add(a, b): return a + b", criteria="correct implementation")
        >>> assert result.passed
    """
    
    name = "code"
    description = "Evaluate code quality and correctness"
    
    DEFAULT_CRITERIA = """
    Evaluate the code for:
    1. Correctness - Does it work as intended?
    2. Readability - Is it easy to understand?
    3. Best practices - Does it follow coding standards?
    4. No bugs - Are there any obvious errors?
    """
    
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
        code: str,
        criteria: Optional[str] = None,
        language: str = "python",
        **kwargs: Any,
    ) -> TestResult:
        """
        Judge code quality.
        
        Args:
            code: The code to evaluate
            criteria: Optional custom criteria (uses default if not provided)
            language: Programming language (default: python)
            
        Returns:
            TestResult with code quality evaluation
        """
        judge = self._get_judge()
        
        eval_criteria = criteria or self.DEFAULT_CRITERIA
        prompt = f"Language: {language}\n\nCode:\n```{language}\n{code}\n```\n\nCriteria: {eval_criteria}"
        
        result = judge.run(output=prompt, criteria=eval_criteria, **kwargs)
        
        return TestResult(
            score=result.score,
            passed=result.passed,
            reasoning=result.reasoning,
            criteria=eval_criteria,
            output=code,
            metadata={"language": language},
        )


__all__ = ['CodeJudge']
