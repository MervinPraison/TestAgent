# Timing

Precise timing utilities for test performance measurement.

```mermaid
graph LR
    subgraph "Timing Classes"
        A[Instant] --> B[Start time]
        A --> C[elapsed]
        D[Duration] --> E[seconds]
        D --> F[milliseconds]
    end
    
    classDef class fill:#6366F1,stroke:#7C90A0,color:#fff
    classDef method fill:#10B981,stroke:#7C90A0,color:#fff
    
    class A,D class
    class B,C,E,F method
```

## Instant

Capture a point in time:

```python
from testagent import Instant

start = Instant()

# ... do work ...

elapsed = start.elapsed()
print(f"Took {elapsed}")  # "0.123s"
```

## Duration

Represent a time duration:

```python
from testagent import Duration

duration = Duration(seconds=1.5)

print(duration.seconds)      # 1.5
print(duration.milliseconds) # 1500.0
print(str(duration))         # "1.500s"
```

## CLI Duration Reporting

Show slowest tests:

```bash
# Show 5 slowest tests
testagent run tests/ --durations=5

# Show all durations
testagent run tests/ --durations=0

# Minimum duration to show
testagent run tests/ --durations=10 --durations-min=0.01
```

Output:
```
= slowest 5 durations =
  0.1234s tests/test_ai.py::test_complex
  0.0567s tests/test_ai.py::test_simple
  0.0234s tests/test_basic.py::test_hello
```

## TestResult Timing

Results include timing information:

```python
from testagent import test

result = test("output", criteria="is correct")

print(f"Duration: {result.duration}s")
print(f"Started: {result.start}")
print(f"Stopped: {result.stop}")
```
