# Basic Examples

Simple examples to get started with TestAgent.

## Testing AI Outputs

```python
from testagent import test

# Test factual correctness
result = test(
    "The capital of France is Paris",
    criteria="factually correct"
)
print(f"Passed: {result.passed}, Score: {result.score}")
```

## Accuracy Testing

```python
from testagent import accuracy

# Compare output to expected
result = accuracy("4", expected="4")
assert result.passed
```

## Criteria Testing

```python
from testagent import criteria

# Test against custom criteria
result = criteria(
    "Hello! How can I help you today?",
    criteria="is a friendly greeting"
)
assert result.passed
```

## Using Decorators

```python
from testagent import mark

@mark.criteria("output is helpful")
def test_helpfulness():
    return "I'm here to help!"

@mark.accuracy(expected="4")
def test_math():
    return "4"
```

## CLI Examples

```bash
# Basic test
testagent "Hello world" --criteria "is a greeting"

# Accuracy test
testagent accuracy "4" --expected "4"

# Criteria test
testagent criteria "Paris" --criteria "is a city name"

# With verbose output
testagent "Hello" -c "is a greeting" -v
```

## Assertions

```python
from testagent import approx, raises

# Approximate comparison
assert result.score == approx(7.5, abs=0.5)

# Exception testing
with raises(ValueError):
    raise ValueError("test")
```

## Skip and XFail

```python
from testagent import mark, skip, importorskip

@mark.skip(reason="Not ready")
def test_future():
    pass

def test_optional():
    np = importorskip("numpy")
    # Use numpy
```
