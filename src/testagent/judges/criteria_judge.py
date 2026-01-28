"""
Criteria Judge - Evaluate output against custom criteria.
"""

from typing import Optional, Any
from ..results import TestResult
from ..config import get_config


class CriteriaJudge:
    """
    Judge for criteria-based testing.
    
    Example:
        >>> judge = CriteriaJudge()
        >>> result = judge.judge("Hello!", criteria="is a friendly greeting")
        >>> assert result.passed
    """
    
    name = "criteria"
    description = "Evaluate output against custom criteria"
    
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
        criteria: str,
        **kwargs: Any,
    ) -> TestResult:
        """
        Judge output against criteria.
        
        Args:
            output: The output to evaluate
            criteria: The criteria to evaluate against
            
        Returns:
            TestResult with criteria evaluation
        """
        judge = self._get_judge()
        result = judge.run(output=output, criteria=criteria, **kwargs)
        
        return TestResult(
            score=result.score,
            passed=result.passed,
            reasoning=result.reasoning,
            criteria=criteria,
            output=output,
        )


__all__ = ['CriteriaJudge']
