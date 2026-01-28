"""
Parallel execution for TestAgent - run AI tests concurrently.

Inspired by pytest-xdist for speed optimization.
"""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Optional, Callable, Any


@dataclass
class ParallelConfig:
    """Configuration for parallel execution."""
    workers: int = 0  # 0 = auto (CPU count)
    
    def __post_init__(self):
        if self.workers == 0:
            self.workers = os.cpu_count() or 4


class ParallelRunner:
    """
    Run AI tests in parallel using thread pool.
    
    Uses ThreadPoolExecutor for I/O-bound LLM calls.
    
    Example:
        >>> runner = ParallelRunner(workers=4)
        >>> results = runner.run(tests)
    """
    
    def __init__(self, workers: Optional[int] = None):
        """
        Initialize parallel runner.
        
        Args:
            workers: Number of worker threads. None = auto (CPU count).
        """
        self.workers = workers or os.cpu_count() or 4
    
    def run(
        self,
        tasks: List[Callable[[], Any]],
        timeout: Optional[float] = None,
    ) -> List[Any]:
        """
        Run tasks in parallel.
        
        Args:
            tasks: List of callable tasks
            timeout: Optional timeout per task in seconds
            
        Returns:
            List of results in order
        """
        results = [None] * len(tasks)
        
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            # Submit all tasks
            future_to_index = {
                executor.submit(task): i
                for i, task in enumerate(tasks)
            }
            
            # Collect results
            for future in as_completed(future_to_index, timeout=timeout):
                index = future_to_index[future]
                try:
                    results[index] = future.result()
                except Exception as e:
                    results[index] = e
        
        return results
    
    def map(
        self,
        func: Callable[[Any], Any],
        items: List[Any],
        timeout: Optional[float] = None,
    ) -> List[Any]:
        """
        Apply function to items in parallel.
        
        Args:
            func: Function to apply
            items: Items to process
            timeout: Optional timeout per item
            
        Returns:
            List of results in order
        """
        tasks = [lambda item=item: func(item) for item in items]
        return self.run(tasks, timeout=timeout)


def run_parallel(
    tasks: List[Callable[[], Any]],
    workers: Optional[int] = None,
    timeout: Optional[float] = None,
) -> List[Any]:
    """
    Convenience function to run tasks in parallel.
    
    Args:
        tasks: List of callable tasks
        workers: Number of workers (None = auto)
        timeout: Optional timeout per task
        
    Returns:
        List of results
    """
    runner = ParallelRunner(workers=workers)
    return runner.run(tasks, timeout=timeout)


__all__ = ['ParallelRunner', 'ParallelConfig', 'run_parallel']
