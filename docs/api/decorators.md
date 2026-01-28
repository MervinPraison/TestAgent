# Decorators API Reference

Decorators for AI testing.

## mark.criteria()

```python
def criteria(criteria: str, threshold: float = 7.0)
```

Mark test with evaluation criteria.

**Example:**

```python
from testagent import mark

@mark.criteria("output is helpful")
def test_helpfulness():
    return "Hello!"
```

---

## mark.accuracy()

```python
def accuracy(expected: str, threshold: float = 7.0)
```

Mark test for accuracy comparison.

**Example:**

```python
@mark.accuracy(expected="4")
def test_math():
    return "4"
```

---

## mark.skip()

```python
def skip(reason: str = "")
```

Skip a test.

**Example:**

```python
@mark.skip(reason="Not implemented")
def test_future():
    pass
```

---

## mark.skipif()

```python
def skipif(condition: bool, *, reason: str)
```

Conditional skip.

**Example:**

```python
@mark.skipif(sys.platform == 'win32', reason="Unix only")
def test_unix():
    pass
```

---

## mark.xfail()

```python
def xfail(reason: str = "", *, strict: bool = False)
```

Expected failure.

**Example:**

```python
@mark.xfail(reason="Known bug")
def test_bug():
    assert False
```

---

## mark.parametrize()

```python
def parametrize(argnames: str, argvalues: list)
```

Data-driven testing.

**Example:**

```python
@mark.parametrize("x, y", [(1, 2), (3, 4)])
def test_add(x, y):
    return x + y
```

---

## param()

```python
def param(*values, marks=(), id: str | None = None) -> ParameterSet
```

Create parameter set with ID.

**Example:**

```python
@mark.parametrize("x", [
    param(1, id="one"),
    param(2, id="two"),
])
def test_func(x):
    pass
```

---

## fixture()

```python
def fixture(func: Callable = None, *, scope: str = "function")
```

Create a test fixture.

**Scopes:** `function`, `class`, `module`, `session`

**Example:**

```python
from testagent import fixture

@fixture
def client():
    return Client()

@fixture(scope="session")
def database():
    db = create_db()
    yield db
    db.close()
```
