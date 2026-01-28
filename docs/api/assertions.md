# Assertions API Reference

Assertion helpers for testing.

## approx()

```python
def approx(
    expected: float | list | tuple | dict,
    rel: float | None = None,
    abs: float | None = None,
) -> ApproxScalar | ApproxSequence | ApproxMapping
```

Approximate comparison for floating-point values.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `expected` | `float/list/dict` | - | Expected value |
| `rel` | `float` | `1e-6` | Relative tolerance |
| `abs` | `float` | `1e-12` | Absolute tolerance |

**Example:**

```python
from testagent import approx

assert 0.1 + 0.2 == approx(0.3)
assert result.score == approx(7.5, abs=0.5)
```

---

## raises()

```python
@contextmanager
def raises(
    expected_exception: Type[BaseException],
    *,
    match: str | Pattern[str] | None = None,
) -> Generator[ExceptionInfo, None, None]
```

Assert that code raises an exception.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `expected_exception` | `type` | Expected exception type |
| `match` | `str/Pattern` | Regex to match message |

**Example:**

```python
from testagent import raises

with raises(ValueError, match="invalid"):
    raise ValueError("invalid input")
```

---

## warns()

```python
@contextmanager
def warns(
    expected_warning: Type[Warning],
    *,
    match: str | Pattern[str] | None = None,
) -> Generator[list[WarningMessage], None, None]
```

Assert that code issues a warning.

**Example:**

```python
from testagent import warns
import warnings

with warns(UserWarning):
    warnings.warn("test", UserWarning)
```

---

## deprecated_call()

```python
@contextmanager
def deprecated_call(
    *,
    match: str | Pattern[str] | None = None,
) -> Generator[list[WarningMessage], None, None]
```

Assert deprecation warning is issued.

Captures: `DeprecationWarning`, `PendingDeprecationWarning`, `FutureWarning`

**Example:**

```python
from testagent import deprecated_call

with deprecated_call():
    warnings.warn("deprecated", DeprecationWarning)
```
