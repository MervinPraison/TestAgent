"""
Tests for TestAgent outcomes module (skip, fail, xfail, importorskip).

Inspired by pytest's outcomes.py for robust test control flow.
"""

import pytest


class TestSkip:
    """Test skip() function."""
    
    def test_skip_raises_exception(self):
        """Test that skip() raises Skipped exception."""
        from testagent.outcomes import skip, Skipped
        
        with pytest.raises(Skipped) as exc_info:
            skip("test reason")
        
        assert exc_info.value.msg == "test reason"
    
    def test_skip_default_reason(self):
        """Test skip with no reason."""
        from testagent.outcomes import skip, Skipped
        
        with pytest.raises(Skipped) as exc_info:
            skip()
        
        assert exc_info.value.msg == ""
    
    def test_skipped_exception_str(self):
        """Test Skipped exception string representation."""
        from testagent.outcomes import Skipped
        
        exc = Skipped("my reason")
        assert str(exc) == "my reason"


class TestFail:
    """Test fail() function."""
    
    def test_fail_raises_exception(self):
        """Test that fail() raises Failed exception."""
        from testagent.outcomes import fail, Failed
        
        with pytest.raises(Failed) as exc_info:
            fail("test failure")
        
        assert exc_info.value.msg == "test failure"
    
    def test_fail_default_reason(self):
        """Test fail with no reason."""
        from testagent.outcomes import fail, Failed
        
        with pytest.raises(Failed) as exc_info:
            fail()
        
        assert exc_info.value.msg == ""


class TestXFail:
    """Test xfail() function."""
    
    def test_xfail_raises_exception(self):
        """Test that xfail() raises XFailed exception."""
        from testagent.outcomes import xfail, XFailed
        
        with pytest.raises(XFailed) as exc_info:
            xfail("expected to fail")
        
        assert exc_info.value.msg == "expected to fail"
    
    def test_xfail_default_reason(self):
        """Test xfail with no reason."""
        from testagent.outcomes import xfail, XFailed
        
        with pytest.raises(XFailed) as exc_info:
            xfail()
        
        assert exc_info.value.msg == ""


class TestImportOrSkip:
    """Test importorskip() function."""
    
    def test_importorskip_existing_module(self):
        """Test importing an existing module."""
        from testagent.outcomes import importorskip
        
        # os is always available
        mod = importorskip("os")
        import os
        assert mod is os
    
    def test_importorskip_missing_module(self):
        """Test importing a non-existent module."""
        from testagent.outcomes import importorskip, Skipped
        
        with pytest.raises(Skipped) as exc_info:
            importorskip("nonexistent_module_xyz123")
        
        assert "nonexistent_module_xyz123" in exc_info.value.msg
    
    def test_importorskip_custom_reason(self):
        """Test importorskip with custom reason."""
        from testagent.outcomes import importorskip, Skipped
        
        with pytest.raises(Skipped) as exc_info:
            importorskip("nonexistent_module", reason="Custom skip reason")
        
        assert "Custom skip reason" in exc_info.value.msg
    
    def test_importorskip_minversion(self):
        """Test importorskip with version check."""
        from testagent.outcomes import importorskip
        
        # sys has __version__ as None, so this should work
        mod = importorskip("sys")
        import sys
        assert mod is sys


class TestOutcomeExceptions:
    """Test outcome exception classes."""
    
    def test_skipped_is_base_exception(self):
        """Test Skipped inherits from BaseException."""
        from testagent.outcomes import Skipped, OutcomeException
        
        assert issubclass(Skipped, OutcomeException)
        assert issubclass(Skipped, BaseException)
    
    def test_failed_is_base_exception(self):
        """Test Failed inherits from BaseException."""
        from testagent.outcomes import Failed, OutcomeException
        
        assert issubclass(Failed, OutcomeException)
    
    def test_xfailed_is_failed(self):
        """Test XFailed inherits from Failed."""
        from testagent.outcomes import XFailed, Failed
        
        assert issubclass(XFailed, Failed)
