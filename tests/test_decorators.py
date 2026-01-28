"""
Tests for TestAgent decorators (mark.skipif, mark.xfail, etc.).
"""

import pytest


class TestMarkSkipif:
    """Test @mark.skipif decorator."""
    
    def test_skipif_true_condition(self):
        """Test skipif skips when condition is True."""
        from testagent import mark
        from testagent.outcomes import Skipped
        
        @mark.skipif(True, reason="Always skip")
        def test_func():
            return "should not run"
        
        with pytest.raises(Skipped) as exc_info:
            test_func()
        
        assert "Always skip" in exc_info.value.msg
    
    def test_skipif_false_condition(self):
        """Test skipif runs when condition is False."""
        from testagent import mark
        
        @mark.skipif(False, reason="Never skip")
        def test_func():
            return "ran successfully"
        
        result = test_func()
        assert result == "ran successfully"
    
    def test_skipif_metadata(self):
        """Test skipif stores metadata on function."""
        from testagent import mark
        
        @mark.skipif(True, reason="Test reason")
        def test_func():
            pass
        
        assert test_func._testagent_skipif is True
        assert test_func._testagent_skipif_reason == "Test reason"


class TestMarkXfail:
    """Test @mark.xfail decorator."""
    
    def test_xfail_failing_test(self):
        """Test xfail on a test that fails."""
        from testagent import mark
        from testagent.outcomes import XFailed
        
        @mark.xfail(reason="Known bug")
        def test_func():
            raise AssertionError("Expected failure")
        
        with pytest.raises(XFailed) as exc_info:
            test_func()
        
        assert "Known bug" in exc_info.value.msg
    
    def test_xfail_passing_test_non_strict(self):
        """Test xfail on a test that passes (non-strict)."""
        from testagent import mark
        
        @mark.xfail(reason="Known bug", strict=False)
        def test_func():
            return "passed unexpectedly"
        
        # Should not raise, just mark as xpass
        result = test_func()
        assert result == "passed unexpectedly"
        assert test_func._testagent_xpass is True
    
    def test_xfail_passing_test_strict(self):
        """Test xfail on a test that passes (strict mode)."""
        from testagent import mark
        
        @mark.xfail(reason="Known bug", strict=True)
        def test_func():
            return "passed unexpectedly"
        
        # Strict mode: passing is a failure
        with pytest.raises(AssertionError) as exc_info:
            test_func()
        
        assert "XPASS(strict)" in str(exc_info.value)
    
    def test_xfail_metadata(self):
        """Test xfail stores metadata on function."""
        from testagent import mark
        
        @mark.xfail(reason="Bug #123", strict=True)
        def test_func():
            pass
        
        assert test_func._testagent_xfail is True
        assert test_func._testagent_xfail_reason == "Bug #123"
        assert test_func._testagent_xfail_strict is True


class TestMarkSkip:
    """Test @mark.skip decorator."""
    
    def test_skip_always_skips(self):
        """Test skip always skips the test."""
        from testagent import mark
        from testagent.outcomes import Skipped
        
        @mark.skip(reason="Not implemented")
        def test_func():
            return "should not run"
        
        with pytest.raises(Skipped) as exc_info:
            test_func()
        
        assert "Not implemented" in exc_info.value.msg


class TestMarkCriteria:
    """Test @mark.criteria decorator exists."""
    
    def test_criteria_exists(self):
        """Test criteria decorator exists."""
        from testagent import mark
        
        assert hasattr(mark, 'criteria')
        assert callable(mark.criteria)


class TestMarkAccuracy:
    """Test @mark.accuracy decorator exists."""
    
    def test_accuracy_exists(self):
        """Test accuracy decorator exists."""
        from testagent import mark
        
        assert hasattr(mark, 'accuracy')
        assert callable(mark.accuracy)
