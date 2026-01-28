"""
Timing utilities for TestAgent - inspired by pytest's timing.py.

Provides precise timing for test execution and duration reporting.
"""

from __future__ import annotations

import dataclasses
from datetime import datetime, timezone
from time import perf_counter, time as time_func


@dataclasses.dataclass(frozen=True)
class Instant:
    """
    Represents an instant in time.
    
    Used to measure duration of test execution.
    Inspired by Rust's std::time::Instant and pytest's timing.Instant.
    """
    
    # Creation time using time.time() for actual timestamps
    time: float = dataclasses.field(default_factory=lambda: time_func(), init=False)
    
    # Performance counter for precise elapsed time measurement
    perf_count: float = dataclasses.field(default_factory=lambda: perf_counter(), init=False)
    
    def elapsed(self) -> Duration:
        """Measure duration since this Instant was created."""
        return Duration(start=self, stop=Instant())
    
    def as_utc(self) -> datetime:
        """Get this instant as UTC datetime."""
        return datetime.fromtimestamp(self.time, timezone.utc)


@dataclasses.dataclass(frozen=True)
class Duration:
    """
    A span of time measured by Instant.elapsed().
    
    Example:
        >>> start = Instant()
        >>> # ... do work ...
        >>> duration = start.elapsed()
        >>> print(f"Took {duration.seconds:.3f}s")
    """
    
    start: Instant
    stop: Instant
    
    @property
    def seconds(self) -> float:
        """Elapsed time in seconds using performance counter."""
        return self.stop.perf_count - self.start.perf_count
    
    @property
    def milliseconds(self) -> float:
        """Elapsed time in milliseconds."""
        return self.seconds * 1000
    
    def __str__(self) -> str:
        if self.seconds < 0.001:
            return f"{self.seconds * 1000000:.0f}μs"
        elif self.seconds < 1.0:
            return f"{self.milliseconds:.2f}ms"
        else:
            return f"{self.seconds:.2f}s"


def format_duration(seconds: float) -> str:
    """
    Format duration for display.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Human-readable duration string
    """
    if seconds < 0.001:
        return f"{seconds * 1000000:.0f}μs"
    elif seconds < 1.0:
        return f"{seconds * 1000:.2f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"


__all__ = ['Instant', 'Duration', 'format_duration', 'perf_counter', 'time_func']
