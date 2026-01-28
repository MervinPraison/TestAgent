"""
API Judge - Test API responses.
"""

from typing import Optional, Any
from ..results import TestResult
from ..config import get_config


class APIJudge:
    """
    Judge for API response testing.
    
    Example:
        >>> judge = APIJudge()
        >>> result = judge.judge('{"status": "ok"}', criteria="valid JSON response")
        >>> assert result.passed
    """
    
    name = "api"
    description = "Test API responses"
    
    DEFAULT_CRITERIA = """
    Evaluate the API response for:
    1. Valid format - Is it valid JSON/XML?
    2. Correct structure - Does it have expected fields?
    3. Reasonable values - Are the values sensible?
    4. No errors - Is there no error indication?
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
        response: str,
        criteria: Optional[str] = None,
        expected_fields: Optional[list] = None,
        **kwargs: Any,
    ) -> TestResult:
        """
        Judge API response.
        
        Args:
            response: The API response to evaluate
            criteria: Optional custom criteria
            expected_fields: Optional list of expected fields
            
        Returns:
            TestResult with API evaluation
        """
        judge = self._get_judge()
        
        eval_criteria = criteria or self.DEFAULT_CRITERIA
        if expected_fields:
            eval_criteria += f"\n\nExpected fields: {', '.join(expected_fields)}"
        
        result = judge.run(output=response, criteria=eval_criteria, **kwargs)
        
        return TestResult(
            score=result.score,
            passed=result.passed,
            reasoning=result.reasoning,
            criteria=eval_criteria,
            output=response,
            metadata={"expected_fields": expected_fields},
        )


__all__ = ['APIJudge']
