# Advanced Examples

Advanced usage patterns for TestAgent.

## Parametrized Testing

```python
from testagent import mark, param

@mark.parametrize("prompt, expected_type", [
    ("Hello", "greeting"),
    ("What is 2+2?", "question"),
    param("Calculate 5*5", "command", id="math_command"),
])
def test_prompt_classification(prompt, expected_type):
    result = classify_prompt(prompt)
    return result == expected_type
```

## Fixtures with Setup/Teardown

```python
from testagent import fixture

@fixture
def database():
    """Setup database, yield, then cleanup."""
    db = create_database()
    yield db
    db.cleanup()

@fixture(scope="session")
def api_client():
    """Session-scoped fixture - created once."""
    return APIClient(api_key=os.environ["API_KEY"])
```

## Parallel Testing

```python
from testagent import run_parallel

# Run multiple tests concurrently
tests = [
    ("output1", {"criteria": "is correct"}),
    ("output2", {"criteria": "is helpful"}),
    ("output3", {"expected": "4"}),
]

results = run_parallel(tests)
for result in results:
    print(f"Score: {result.score}")
```

## Custom Configuration

```python
from testagent import TestAgent, TestConfig

# Create custom tester
tester = TestAgent(config=TestConfig(
    model="gpt-4",
    threshold=8.0,
    temperature=0.0,
    cache_enabled=True,
))

result = tester.run("output", criteria="is excellent")
```

## Async Testing

```python
import asyncio
from testagent import TestAgent

async def test_async():
    tester = TestAgent()
    result = await tester.run_async(
        "Hello world",
        criteria="is a greeting"
    )
    return result

result = asyncio.run(test_async())
```

## Conditional Skipping

```python
from testagent import mark
import sys
import os

@mark.skipif(
    sys.platform == 'win32',
    reason="Unix only"
)
def test_unix_feature():
    pass

@mark.skipif(
    "CI" not in os.environ,
    reason="CI only"
)
def test_ci_feature():
    pass
```

## Expected Failures

```python
from testagent import mark

@mark.xfail(reason="Known bug #123")
def test_known_bug():
    # This test is expected to fail
    assert False

@mark.xfail(reason="Should pass", strict=True)
def test_strict_xfail():
    # If this passes, test fails
    pass
```

## Caching for Speed

```python
from testagent import TestAgentCache, CacheKey

cache = TestAgentCache()

# Check cache before expensive test
key = CacheKey(
    output="test output",
    criteria="is correct",
    model="gpt-4o-mini"
)

cached = cache.get(key)
if cached:
    print("Using cached result")
else:
    result = test("test output", criteria="is correct")
    cache.set(key, result)
```

## CI/CD Integration

```bash
#!/bin/bash
# run_tests.sh

# Run tests with duration reporting
testagent run tests/ --durations=10 -v

# Exit with appropriate code
exit $?
```

```yaml
# .github/workflows/test.yml
name: Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install testagent
      - run: testagent run tests/ -v
```
