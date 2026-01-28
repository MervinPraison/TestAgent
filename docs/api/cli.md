# CLI API Reference

Command-line interface for TestAgent.

## Commands

### testagent (main)

```bash
testagent OUTPUT [OPTIONS]
```

Test any output with AI.

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--criteria` | `-c` | `str` | - | Evaluation criteria |
| `--expected` | `-e` | `str` | - | Expected output |
| `--threshold` | `-t` | `float` | `7.0` | Pass threshold |
| `--model` | `-m` | `str` | - | LLM model |
| `--verbose` | `-v` | `bool` | `False` | Verbose output |
| `--json` | | `bool` | `False` | JSON output |

---

### testagent accuracy

```bash
testagent accuracy OUTPUT --expected EXPECTED [OPTIONS]
```

Test output accuracy.

---

### testagent criteria

```bash
testagent criteria OUTPUT --criteria CRITERIA [OPTIONS]
```

Test against criteria.

---

### testagent run

```bash
testagent run PATH [OPTIONS]
```

Run AI tests.

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--pattern` | `-p` | `str` | - | File pattern |
| `--durations` | | `int` | - | Show N slowest |
| `--durations-min` | | `float` | `0.005` | Min duration |
| `--exitfirst` | `-x` | `bool` | `False` | Exit on first failure |
| `--verbose` | `-v` | `bool` | `False` | Verbose output |

---

### testagent collect

```bash
testagent collect PATH [OPTIONS]
```

Discover tests without running.

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--pattern` | `-p` | `str` | File pattern |

---

### testagent cache-clear

```bash
testagent cache-clear
```

Clear the test cache.

---

### testagent cache-stats

```bash
testagent cache-stats
```

Show cache statistics.

---

### testagent version

```bash
testagent version
```

Show version.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | All tests passed |
| `1` | Some tests failed |
| `2` | Error occurred |
| `5` | No tests collected |
