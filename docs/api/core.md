# Core API Reference

Core functions and classes for AI testing.

## Functions

### test()

```python
def test(
    output: str,
    expected: Optional[str] = None,
    criteria: Optional[str] = None,
    **kwargs: Any,
) -> TestResult
```

Test any output using AI.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `output` | `str` | - | The output to test |
| `expected` | `str` | `None` | Expected output for comparison |
| `criteria` | `str` | `None` | Custom evaluation criteria |

**Returns:** `TestResult`

**Example:**

```python
from testagent import test

result = test("Paris", criteria="is a city name")
assert result.passed
```

---

### accuracy()

```python
def accuracy(
    output: str,
    expected: str,
    **kwargs: Any,
) -> TestResult
```

Test output accuracy against expected value.

**Example:**

```python
from testagent import accuracy

result = accuracy("4", expected="4")
```

---

### criteria()

```python
def criteria(
    output: str,
    criteria: str,
    **kwargs: Any,
) -> TestResult
```

Test output against custom criteria.

**Example:**

```python
from testagent import criteria

result = criteria("Hello!", criteria="is a greeting")
```

---

## Classes

### TestAgent

Main class for AI testing with configuration.

```python
class TestAgent:
    def __init__(self, config: Optional[TestConfig] = None)
    def run(self, output: str, expected: str = None, criteria: str = None) -> TestResult
    async def run_async(self, output: str, expected: str = None, criteria: str = None) -> TestResult
```

**Example:**

```python
from testagent import TestAgent, TestConfig

tester = TestAgent(config=TestConfig(model="gpt-4"))
result = tester.run("output", criteria="is correct")
```

---

### TestResult

Result of an AI test.

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Score from 0 to 10 |
| `passed` | `bool` | True if score ≥ threshold |
| `reasoning` | `str` | AI's explanation |
| `criteria` | `str` | Criteria used |
| `expected` | `str` | Expected output |
| `output` | `str` | Tested output |
| `duration` | `float` | Test duration |

---

### TestConfig

Configuration for AI testing.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `model` | `str` | `"gpt-4o-mini"` | LLM model |
| `threshold` | `float` | `7.0` | Pass threshold |
| `temperature` | `float` | `0.0` | LLM temperature |
| `verbose` | `bool` | `False` | Verbose output |
| `cache_enabled` | `bool` | `True` | Enable caching |
