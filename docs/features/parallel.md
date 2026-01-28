# Parallel Execution

Run tests concurrently for faster execution.

```mermaid
graph TB
    subgraph "Parallel Execution"
        A[Tests] --> B[ParallelRunner]
        B --> C[Worker 1]
        B --> D[Worker 2]
        B --> E[Worker N]
        C --> F[Results]
        D --> F
        E --> F
    end
    
    classDef input fill:#6366F1,stroke:#7C90A0,color:#fff
    classDef runner fill:#F59E0B,stroke:#7C90A0,color:#fff
    classDef output fill:#10B981,stroke:#7C90A0,color:#fff
    
    class A input
    class B,C,D,E runner
    class F output
```

## Quick Start

```python
from testagent import run_parallel

results = run_parallel([
    ("output1", {"criteria": "is correct"}),
    ("output2", {"criteria": "is helpful"}),
    ("output3", {"expected": "4"}),
])

for result in results:
    print(f"{result.passed}: {result.score}")
```

## ParallelRunner Class

```python
from testagent import ParallelRunner

runner = ParallelRunner(max_workers=4)

tests = [
    {"output": "Hello", "criteria": "is a greeting"},
    {"output": "4", "expected": "4"},
]

results = runner.run(tests)
```

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `max_workers` | `int` | `4` | Maximum concurrent workers |

## Thread Safety

TestAgent is thread-safe by default:

- Each test runs in isolation
- No shared mutable state
- Results are collected safely

## Best Practices

!!! tip "When to Use Parallel"
    - Many independent tests
    - Tests with similar duration
    - CI/CD pipelines

!!! warning "When Not to Use"
    - Tests with shared resources
    - Rate-limited APIs
    - Sequential dependencies
