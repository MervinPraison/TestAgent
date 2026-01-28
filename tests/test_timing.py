"""
Tests for TestAgent timing module.
"""

import time


class TestInstant:
    """Test Instant class."""
    
    def test_instant_creation(self):
        """Test creating an Instant."""
        from testagent.timing import Instant
        
        instant = Instant()
        assert instant.time > 0
        assert instant.perf_count > 0
    
    def test_instant_elapsed(self):
        """Test measuring elapsed time."""
        from testagent.timing import Instant
        
        start = Instant()
        time.sleep(0.01)  # 10ms
        duration = start.elapsed()
        
        assert duration.seconds >= 0.01
        assert duration.seconds < 0.1  # Should be less than 100ms
    
    def test_instant_as_utc(self):
        """Test converting to UTC datetime."""
        from testagent.timing import Instant
        from datetime import datetime, timezone
        
        instant = Instant()
        dt = instant.as_utc()
        
        assert dt.tzinfo == timezone.utc
        assert isinstance(dt, datetime)


class TestDuration:
    """Test Duration class."""
    
    def test_duration_seconds(self):
        """Test duration in seconds."""
        from testagent.timing import Instant, Duration
        
        start = Instant()
        time.sleep(0.01)
        stop = Instant()
        
        duration = Duration(start=start, stop=stop)
        assert duration.seconds >= 0.01
    
    def test_duration_milliseconds(self):
        """Test duration in milliseconds."""
        from testagent.timing import Instant, Duration
        
        start = Instant()
        time.sleep(0.01)
        stop = Instant()
        
        duration = Duration(start=start, stop=stop)
        assert duration.milliseconds >= 10.0
    
    def test_duration_str(self):
        """Test duration string representation."""
        from testagent.timing import Instant
        
        start = Instant()
        time.sleep(0.01)
        duration = start.elapsed()
        
        duration_str = str(duration)
        assert "ms" in duration_str or "s" in duration_str


class TestFormatDuration:
    """Test format_duration function."""
    
    def test_format_microseconds(self):
        """Test formatting microseconds."""
        from testagent.timing import format_duration
        
        result = format_duration(0.0001)  # 100μs
        assert "μs" in result
    
    def test_format_milliseconds(self):
        """Test formatting milliseconds."""
        from testagent.timing import format_duration
        
        result = format_duration(0.1)  # 100ms
        assert "ms" in result
    
    def test_format_seconds(self):
        """Test formatting seconds."""
        from testagent.timing import format_duration
        
        result = format_duration(5.5)  # 5.5s
        assert "s" in result
        assert "5.50" in result
    
    def test_format_minutes(self):
        """Test formatting minutes."""
        from testagent.timing import format_duration
        
        result = format_duration(90)  # 1m 30s
        assert "m" in result
