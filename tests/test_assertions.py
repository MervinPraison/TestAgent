"""
Tests for TestAgent assertion helpers (approx, raises, warns).

Inspired by pytest's python_api.py, raises.py, and recwarn.py.
"""

import pytest
import warnings


class TestApprox:
    """Test approx() function for approximate comparisons."""
    
    def test_approx_basic(self):
        """Test basic approximate comparison."""
        from testagent.assertions import approx
        
        assert 0.1 + 0.2 == approx(0.3)
    
    def test_approx_with_rel_tolerance(self):
        """Test approx with relative tolerance."""
        from testagent.assertions import approx
        
        assert 100.0 == approx(99.0, rel=0.02)  # 2% tolerance
        assert 100.0 != approx(99.0, rel=0.005)  # 0.5% tolerance
    
    def test_approx_with_abs_tolerance(self):
        """Test approx with absolute tolerance."""
        from testagent.assertions import approx
        
        assert 0.1 == approx(0.11, abs=0.02)
        assert 0.1 != approx(0.11, abs=0.005)
    
    def test_approx_list(self):
        """Test approx with list of values."""
        from testagent.assertions import approx
        
        assert [0.1, 0.2, 0.3] == approx([0.1, 0.2, 0.3])
    
    def test_approx_dict(self):
        """Test approx with dict of values."""
        from testagent.assertions import approx
        
        assert {"a": 0.1, "b": 0.2} == approx({"a": 0.1, "b": 0.2})
    
    def test_approx_repr(self):
        """Test approx string representation."""
        from testagent.assertions import approx
        
        a = approx(1.0)
        assert "approx" in repr(a)
    
    def test_approx_score(self):
        """Test approx for AI test scores."""
        from testagent.assertions import approx
        
        # AI scores are typically 0-10 floats
        assert 7.5 == approx(7.5, abs=0.1)
        assert 8.0 == approx(7.9, abs=0.2)


class TestRaises:
    """Test raises() context manager."""
    
    def test_raises_basic(self):
        """Test basic exception raising."""
        from testagent.assertions import raises
        
        with raises(ValueError):
            raise ValueError("test error")
    
    def test_raises_wrong_exception(self):
        """Test raises with wrong exception type."""
        from testagent.assertions import raises
        
        with pytest.raises(AssertionError):
            with raises(ValueError):
                raise TypeError("wrong type")
    
    def test_raises_no_exception(self):
        """Test raises when no exception is raised."""
        from testagent.assertions import raises
        
        with pytest.raises(AssertionError):
            with raises(ValueError):
                pass  # No exception raised
    
    def test_raises_match(self):
        """Test raises with message matching."""
        from testagent.assertions import raises
        
        with raises(ValueError, match="test"):
            raise ValueError("this is a test error")
    
    def test_raises_match_fails(self):
        """Test raises when match fails."""
        from testagent.assertions import raises
        
        with pytest.raises(AssertionError):
            with raises(ValueError, match="not found"):
                raise ValueError("different message")
    
    def test_raises_excinfo(self):
        """Test raises returns exception info."""
        from testagent.assertions import raises
        
        with raises(ValueError) as excinfo:
            raise ValueError("test message")
        
        assert "test message" in str(excinfo.value)


class TestWarns:
    """Test warns() context manager."""
    
    def test_warns_basic(self):
        """Test basic warning capture."""
        from testagent.assertions import warns
        
        with warns(UserWarning):
            warnings.warn("test warning", UserWarning)
    
    def test_warns_wrong_type(self):
        """Test warns with wrong warning type."""
        from testagent.assertions import warns
        
        with pytest.raises(AssertionError):
            with warns(DeprecationWarning):
                warnings.warn("test", UserWarning)
    
    def test_warns_no_warning(self):
        """Test warns when no warning is issued."""
        from testagent.assertions import warns
        
        with pytest.raises(AssertionError):
            with warns(UserWarning):
                pass  # No warning
    
    def test_warns_match(self):
        """Test warns with message matching."""
        from testagent.assertions import warns
        
        with warns(UserWarning, match="test"):
            warnings.warn("this is a test warning", UserWarning)


class TestDeprecatedCall:
    """Test deprecated_call() context manager."""
    
    def test_deprecated_call_basic(self):
        """Test deprecated_call captures deprecation warnings."""
        from testagent.assertions import deprecated_call
        
        with deprecated_call():
            warnings.warn("deprecated", DeprecationWarning)
    
    def test_deprecated_call_pending(self):
        """Test deprecated_call captures pending deprecation."""
        from testagent.assertions import deprecated_call
        
        with deprecated_call():
            warnings.warn("pending", PendingDeprecationWarning)
    
    def test_deprecated_call_future(self):
        """Test deprecated_call captures future warnings."""
        from testagent.assertions import deprecated_call
        
        with deprecated_call():
            warnings.warn("future", FutureWarning)
