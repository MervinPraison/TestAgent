"""
Tests for TestAgent parallel execution.
"""

import time


class TestParallelConfig:
    """Test ParallelConfig class."""
    
    def test_config_default(self):
        """Test default config."""
        from testagent.parallel import ParallelConfig
        
        config = ParallelConfig()
        assert config.workers > 0
    
    def test_config_custom_workers(self):
        """Test custom worker count."""
        from testagent.parallel import ParallelConfig
        
        config = ParallelConfig(workers=8)
        assert config.workers == 8


class TestParallelRunner:
    """Test ParallelRunner class."""
    
    def test_runner_init(self):
        """Test runner initialization."""
        from testagent.parallel import ParallelRunner
        
        runner = ParallelRunner(workers=4)
        assert runner.workers == 4
    
    def test_runner_run_simple(self):
        """Test running simple tasks."""
        from testagent.parallel import ParallelRunner
        
        runner = ParallelRunner(workers=2)
        
        tasks = [
            lambda: 1,
            lambda: 2,
            lambda: 3,
        ]
        
        results = runner.run(tasks)
        
        assert results == [1, 2, 3]
    
    def test_runner_run_parallel_speedup(self):
        """Test that parallel execution is faster."""
        from testagent.parallel import ParallelRunner
        
        def slow_task(n):
            time.sleep(0.05)  # 50ms
            return n
        
        runner = ParallelRunner(workers=4)
        
        # Create tasks that would take 200ms sequentially
        tasks = [lambda i=i: slow_task(i) for i in range(4)]
        
        start = time.time()
        results = runner.run(tasks)
        duration = time.time() - start
        
        # Should complete in ~50ms (parallel) not 200ms (sequential)
        assert duration < 0.15  # Allow some overhead
        assert len(results) == 4
    
    def test_runner_map(self):
        """Test map function."""
        from testagent.parallel import ParallelRunner
        
        runner = ParallelRunner(workers=2)
        
        results = runner.map(lambda x: x * 2, [1, 2, 3, 4])
        
        assert results == [2, 4, 6, 8]
    
    def test_runner_handles_exceptions(self):
        """Test that exceptions are captured."""
        from testagent.parallel import ParallelRunner
        
        def failing_task():
            raise ValueError("test error")
        
        runner = ParallelRunner(workers=2)
        
        tasks = [
            lambda: 1,
            failing_task,
            lambda: 3,
        ]
        
        results = runner.run(tasks)
        
        assert results[0] == 1
        assert isinstance(results[1], ValueError)
        assert results[2] == 3


class TestRunParallel:
    """Test run_parallel convenience function."""
    
    def test_run_parallel(self):
        """Test run_parallel function."""
        from testagent.parallel import run_parallel
        
        tasks = [lambda: i for i in range(5)]
        results = run_parallel(tasks, workers=2)
        
        assert len(results) == 5
