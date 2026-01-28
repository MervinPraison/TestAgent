# TestAgent

**The world's easiest way to test anything using AI.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

TestAgent is a simple, pytest-like AI testing framework powered by [PraisonAI Agents](https://github.com/MervinPraison/PraisonAI).

## Installation

```bash
# Using uv (recommended)
uv add testagent

# Using pip
pip install testagent
```

## Quick Start

### One Line Test

```python
from testagent import test

result = test("The capital of France is Paris", criteria="factually correct")
assert result.passed
```

### Accuracy Testing

```python
from testagent import accuracy

result = accuracy("4", expected="4")
assert result.score >= 9.0
```

### Criteria Testing

```python
from testagent import criteria

result = criteria("Hello, how can I help you?", criteria="is a friendly greeting")
assert result.passed
```

## CLI Usage

```bash
# Basic test
testagent "The capital of France is Paris" --criteria "factually correct"

# Accuracy test
testagent accuracy "4" --expected "4"

# Criteria test
testagent criteria "Hello world" --criteria "is a greeting"

# With options
testagent "Output to test" --criteria "is correct" --threshold 8.0 --verbose
```

## pytest-like Features

TestAgent replicates pytest's speed, robustness, and power:

### Test Discovery

```bash
# Discover tests without running (like pytest --collect-only)
testagent collect tests/
testagent collect . --pattern "test_*.py"
```

### Caching (100x Speedup)

```bash
# Cache is enabled by default - identical tests skip LLM calls
testagent "test output" --criteria "is correct"  # First run: LLM call
testagent "test output" --criteria "is correct"  # Second run: cached!

# Cache management
testagent cache-stats    # Show cache statistics
testagent cache-clear    # Clear the cache
```

### Parallel Execution

```python
from testagent import run_parallel, ParallelRunner

# Run multiple tests in parallel (I/O-bound LLM calls)
runner = ParallelRunner(workers=4)
results = runner.map(lambda x: test(x, criteria="is correct"), outputs)
```

### Timing & Performance

```python
from testagent import Instant, Duration

start = Instant()
# ... run tests ...
duration = start.elapsed()
print(f"Tests completed in {duration}")  # "Tests completed in 1.23s"
```

### Test Outcomes (skip, fail, xfail)

```python
from testagent import skip, fail, xfail, importorskip

# Skip a test
skip("Not implemented yet")

# Fail explicitly
fail("This should not happen")

# Expected failure
xfail("Known bug #123")

# Skip if module not available
np = importorskip("numpy")
```

### Conditional Markers

```python
from testagent import mark
import sys

@mark.skipif(sys.platform == 'win32', reason="Not supported on Windows")
def test_unix_only():
    pass

@mark.xfail(reason="Known bug #123", strict=False)
def test_known_bug():
    pass
```

### Run Command with Durations

```bash
# Run tests with duration reporting
testagent run tests/ --durations=5

# Run with fail-fast
testagent run tests/ -x

# Verbose mode
testagent run tests/ -v
```

### Assertion Helpers

```python
from testagent import approx, raises, warns, deprecated_call

# Approximate comparisons (essential for AI scores)
assert result.score == approx(7.5, abs=0.5)
assert 0.1 + 0.2 == approx(0.3)
assert [0.1, 0.2] == approx([0.1, 0.2])

# Exception testing
with raises(ValueError, match="invalid"):
    raise ValueError("invalid input")

# Warning testing
with warns(UserWarning):
    warnings.warn("test", UserWarning)

# Deprecation testing
with deprecated_call():
    warnings.warn("deprecated", DeprecationWarning)
```

### Parametrize (Data-Driven Testing)

```python
from testagent import mark, param

# Test with multiple inputs
@mark.parametrize("x, y, expected", [
    (1, 2, 3),
    (4, 5, 9),
    param(10, 20, 30, id="large_numbers"),
])
def test_add(x, y, expected):
    assert x + y == expected

# Single argument
@mark.parametrize("prompt", [
    "Hello",
    "What is AI?",
    "Explain quantum computing",
])
def test_ai_responses(prompt):
    result = get_ai_response(prompt)
    assert len(result) > 0
```

### Fixtures

```python
from testagent import fixture

@fixture
def ai_client():
    """Create an AI client for testing."""
    return AIClient()

@fixture(scope="session")
def expensive_resource():
    """Session-scoped fixture - created once."""
    resource = create_expensive_resource()
    yield resource
    resource.cleanup()
```

## Pytest-like Decorators

```python
from testagent import mark

@mark.criteria("output is helpful and accurate")
def test_helpfulness():
    return "Hello! I'm here to help you with any questions."

@mark.accuracy(expected="4")
def test_math():
    return "4"
```

## Judge Modules

TestAgent includes specialized judges for different testing scenarios:

```python
from testagent.judges import (
    AccuracyJudge,   # Compare output to expected
    CriteriaJudge,   # Evaluate against criteria
    CodeJudge,       # Evaluate code quality
    APIJudge,        # Test API responses
    SafetyJudge,     # Detect harmful content
)

# Code quality testing
code_judge = CodeJudge()
result = code_judge.judge(
    "def add(a, b): return a + b",
    criteria="correct implementation"
)

# API response testing
api_judge = APIJudge()
result = api_judge.judge(
    '{"status": "ok", "data": [1, 2, 3]}',
    expected_fields=["status", "data"]
)

# Safety testing
safety_judge = SafetyJudge()
result = safety_judge.judge("Hello, how can I help you?")
assert result.passed  # Safe content
```

## Configuration

```python
from testagent import TestConfig, TestAgent

# Custom configuration
config = TestConfig(
    model="gpt-4o",           # LLM model
    threshold=8.0,            # Pass threshold (1-10)
    temperature=0.1,          # LLM temperature
    verbose=True,             # Verbose output
)

tester = TestAgent(config=config)
result = tester.run("Test output", criteria="is correct")
```

## Environment Variables

```bash
export AITEST_MODEL="gpt-4o-mini"      # Default model
export OPENAI_API_KEY="sk-..."         # OpenAI API key
```

## Custom Judges

Register your own judges:

```python
from testagent import add_judge, get_judge

class MyCustomJudge:
    def run(self, output, **kwargs):
        from testagent import TestResult
        return TestResult(
            score=10.0,
            passed=True,
            reasoning="Custom evaluation"
        )

add_judge("custom", MyCustomJudge)

# Use it
judge = get_judge("custom")()
result = judge.run("test output")
```

## API Reference

### Core Functions

| Function | Description |
|----------|-------------|
| `test(output, criteria=None, expected=None)` | Test any output |
| `accuracy(output, expected)` | Compare to expected output |
| `criteria(output, criteria)` | Evaluate against criteria |

### Classes

| Class | Description |
|-------|-------------|
| `TestAgent` | Main testing class |
| `TestResult` | Test result with score, passed, reasoning |
| `TestConfig` | Configuration options |

### Decorators

| Decorator | Description |
|-----------|-------------|
| `@mark.criteria(criteria)` | Mark test with criteria |
| `@mark.accuracy(expected)` | Mark test for accuracy |
| `@mark.skip(reason)` | Skip a test |

## How It Works

TestAgent wraps [PraisonAI Agents](https://github.com/MervinPraison/PraisonAI) evaluation framework, providing:

1. **Simple API** - One function to test anything
2. **Protocol-driven** - Extends `JudgeProtocol` for compatibility
3. **Multiple judges** - Specialized testing for different scenarios
4. **CLI support** - Test from command line
5. **pytest integration** - Use familiar decorator syntax

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please read our contributing guidelines first.

## Links

- [PraisonAI](https://github.com/MervinPraison/PraisonAI)
- [Documentation](https://docs.praison.ai)
