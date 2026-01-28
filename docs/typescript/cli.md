# CLI Usage

The aitestagent CLI provides a simple way to test outputs directly from your terminal.

## Installation

```bash
npm install -g aitestagent
```

## Basic Usage

```bash
# Test with custom criteria
aitestagent "Hello, world!" -c "is a friendly greeting"

# Test accuracy against expected output
aitestagent "Paris" -e "Paris, France"

# With threshold
aitestagent "Hello!" -c "is friendly" -t 8.0
```

## Commands

### Test Output

```bash
aitestagent <output> [options]
```

**Options:**

| Flag | Description |
|------|-------------|
| `-e, --expected <text>` | Expected output for accuracy test |
| `-c, --criteria <text>` | Custom criteria for evaluation |
| `-t, --threshold <num>` | Pass threshold 1-10 (default: 7.0) |
| `-h, --help` | Show help |

## Examples

```bash
# Simple criteria test
aitestagent "The answer is 42" -c "provides a numerical answer"

# Accuracy comparison
aitestagent "4" -e "4"
# ✅ Score: 10/10 (PASSED)

# Stricter threshold
aitestagent "Hello" -c "is a complete greeting" -t 9.0
# ❌ Score: 6/10 (FAILED)
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Test passed |
| `1` | Test failed or error |

Use exit codes for CI/CD integration:

```bash
aitestagent "output" -c "is correct" && echo "Passed!" || echo "Failed!"
```
