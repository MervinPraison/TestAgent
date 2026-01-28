"""
Tests for TestAgent core functionality.

TDD: These tests define the expected behavior.
"""

from unittest.mock import Mock, patch


class TestImports:
    """Test that all imports work correctly."""
    
    def test_import_testagent(self):
        """Test basic import."""
        import testagent
        assert hasattr(testagent, '__version__')
    
    def test_import_test_function(self):
        """Test importing test function."""
        from testagent import test
        assert callable(test)
    
    def test_import_accuracy(self):
        """Test importing accuracy function."""
        from testagent import accuracy
        assert callable(accuracy)
    
    def test_import_criteria(self):
        """Test importing criteria function."""
        from testagent import criteria
        assert callable(criteria)
    
    def test_import_testagent_class(self):
        """Test importing TestAgent class."""
        from testagent import TestAgent
        assert TestAgent is not None
    
    def test_import_test_result(self):
        """Test importing TestResult."""
        from testagent import TestResult
        assert TestResult is not None
    
    def test_import_test_config(self):
        """Test importing TestConfig."""
        from testagent import TestConfig
        assert TestConfig is not None
    
    def test_import_mark(self):
        """Test importing mark decorator."""
        from testagent import mark
        assert hasattr(mark, 'criteria')
        assert hasattr(mark, 'accuracy')


class TestTestResult:
    """Test TestResult class."""
    
    def test_create_result(self):
        """Test creating a TestResult."""
        from testagent.results import TestResult
        
        result = TestResult(
            score=8.0,
            passed=True,
            reasoning="Good output"
        )
        
        assert result.score == 8.0
        assert result.passed is True
        assert result.reasoning == "Good output"
    
    def test_result_to_dict(self):
        """Test converting result to dict."""
        from testagent.results import TestResult
        
        result = TestResult(
            score=8.0,
            passed=True,
            reasoning="Good"
        )
        
        d = result.to_dict()
        assert d['score'] == 8.0
        assert d['passed'] is True
        assert d['reasoning'] == "Good"
    
    def test_result_bool(self):
        """Test using result in boolean context."""
        from testagent.results import TestResult
        
        passed = TestResult(score=8.0, passed=True, reasoning="Good")
        failed = TestResult(score=3.0, passed=False, reasoning="Bad")
        
        assert bool(passed) is True
        assert bool(failed) is False
    
    def test_result_repr(self):
        """Test result string representation."""
        from testagent.results import TestResult
        
        result = TestResult(score=8.0, passed=True, reasoning="Good")
        assert "PASSED" in repr(result)
        assert "8.0" in repr(result)


class TestTestConfig:
    """Test TestConfig class."""
    
    def test_default_config(self):
        """Test default configuration."""
        from testagent.config import TestConfig
        
        config = TestConfig()
        assert config.threshold == 7.0
        assert config.temperature == 0.1
        assert config.verbose is False
    
    def test_custom_config(self):
        """Test custom configuration."""
        from testagent.config import TestConfig
        
        config = TestConfig(
            model="gpt-4o",
            threshold=8.0,
            verbose=True
        )
        
        assert config.model == "gpt-4o"
        assert config.threshold == 8.0
        assert config.verbose is True


class TestProtocols:
    """Test protocol definitions."""
    
    def test_test_result_protocol(self):
        """Test TestResultProtocol is runtime checkable."""
        from testagent.protocols import TestResultProtocol
        from testagent.results import TestResult
        
        result = TestResult(score=8.0, passed=True, reasoning="Good")
        assert isinstance(result, TestResultProtocol)
    
    def test_test_protocol_exists(self):
        """Test TestProtocol exists."""
        from testagent.protocols import TestProtocol
        assert TestProtocol is not None


class TestRegistry:
    """Test judge registry."""
    
    def test_add_judge(self):
        """Test adding a judge."""
        from testagent.registry import add_judge, get_judge, remove_judge
        
        class MockJudge:
            pass
        
        add_judge("mock", MockJudge)
        assert get_judge("mock") is MockJudge
        
        # Cleanup
        remove_judge("mock")
    
    def test_list_judges(self):
        """Test listing judges."""
        from testagent.registry import add_judge, list_judges, remove_judge
        
        class MockJudge:
            pass
        
        add_judge("test_judge", MockJudge)
        judges = list_judges()
        assert "test_judge" in judges
        
        # Cleanup
        remove_judge("test_judge")
    
    def test_remove_judge(self):
        """Test removing a judge."""
        from testagent.registry import add_judge, get_judge, remove_judge
        
        class MockJudge:
            pass
        
        add_judge("to_remove", MockJudge)
        assert remove_judge("to_remove") is True
        assert get_judge("to_remove") is None
        assert remove_judge("nonexistent") is False


class TestDecorators:
    """Test decorator functionality."""
    
    def test_mark_criteria_exists(self):
        """Test mark.criteria decorator exists."""
        from testagent.decorators import mark
        
        assert hasattr(mark, 'criteria')
        assert callable(mark.criteria)
    
    def test_mark_accuracy_exists(self):
        """Test mark.accuracy decorator exists."""
        from testagent.decorators import mark
        
        assert hasattr(mark, 'accuracy')
        assert callable(mark.accuracy)
    
    def test_mark_skip_exists(self):
        """Test mark.skip decorator exists."""
        from testagent.decorators import mark
        
        assert hasattr(mark, 'skip')
        assert callable(mark.skip)


class TestJudgeModules:
    """Test judge modules."""
    
    def test_accuracy_judge_exists(self):
        """Test AccuracyJudge exists."""
        from testagent.judges import AccuracyJudge
        assert AccuracyJudge is not None
    
    def test_criteria_judge_exists(self):
        """Test CriteriaJudge exists."""
        from testagent.judges import CriteriaJudge
        assert CriteriaJudge is not None
    
    def test_code_judge_exists(self):
        """Test CodeJudge exists."""
        from testagent.judges import CodeJudge
        assert CodeJudge is not None
    
    def test_api_judge_exists(self):
        """Test APIJudge exists."""
        from testagent.judges import APIJudge
        assert APIJudge is not None
    
    def test_safety_judge_exists(self):
        """Test SafetyJudge exists."""
        from testagent.judges import SafetyJudge
        assert SafetyJudge is not None


class TestTestAgentClass:
    """Test TestAgent class with mocked praisonaiagents."""
    
    def test_testagent_init(self):
        """Test TestAgent initialization."""
        from testagent.core import TestAgent
        from testagent.config import TestConfig
        
        config = TestConfig(model="test-model")
        tester = TestAgent(config=config)
        
        assert tester.config.model == "test-model"
    
    @patch('testagent.core.TestAgent._get_judge')
    def test_testagent_run(self, mock_get_judge):
        """Test TestAgent.run with mocked judge."""
        from testagent.core import TestAgent
        from testagent.results import TestResult
        
        # Mock the judge
        mock_judge = Mock()
        mock_result = Mock()
        mock_result.score = 8.0
        mock_result.passed = True
        mock_result.reasoning = "Good output"
        mock_judge.run.return_value = mock_result
        mock_get_judge.return_value = mock_judge
        
        tester = TestAgent()
        result = tester.run("Hello world", criteria="is a greeting")
        
        assert isinstance(result, TestResult)
        assert result.score == 8.0
        assert result.passed is True


class TestCoreFunctions:
    """Test core functions with mocked backend."""
    
    @patch('testagent.core._get_tester')
    def test_test_function(self, mock_get_tester):
        """Test the test() function."""
        from testagent.core import test
        from testagent.results import TestResult
        
        # Mock the tester
        mock_tester = Mock()
        mock_tester.run.return_value = TestResult(
            score=8.0, passed=True, reasoning="Good"
        )
        mock_get_tester.return_value = mock_tester
        
        result = test("Hello world", criteria="is a greeting")
        
        assert result.passed is True
        mock_tester.run.assert_called_once()
    
    @patch('testagent.core._get_tester')
    def test_accuracy_function(self, mock_get_tester):
        """Test the accuracy() function."""
        from testagent.core import accuracy
        from testagent.results import TestResult
        
        mock_tester = Mock()
        mock_tester.run.return_value = TestResult(
            score=10.0, passed=True, reasoning="Exact match"
        )
        mock_get_tester.return_value = mock_tester
        
        result = accuracy("4", expected="4")
        
        assert result.passed is True
    
    @patch('testagent.core._get_tester')
    def test_criteria_function(self, mock_get_tester):
        """Test the criteria() function."""
        from testagent.core import criteria
        from testagent.results import TestResult
        
        mock_tester = Mock()
        mock_tester.run.return_value = TestResult(
            score=9.0, passed=True, reasoning="Meets criteria"
        )
        mock_get_tester.return_value = mock_tester
        
        result = criteria("Hello!", criteria="is friendly")
        
        assert result.passed is True
