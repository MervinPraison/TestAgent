# TestAgent Feature Specification

Feature mapping between Python and TypeScript implementations.

## Core API

| Feature | Python | TypeScript | Status |
|---------|--------|------------|--------|
| `test()` | `src/testagent/core.py` | `src/testagent-ts/src/test.ts` | ✅ |
| `accuracy()` | `src/testagent/core.py` | `src/testagent-ts/src/test.ts` | ✅ |
| `criteria()` | `src/testagent/core.py` | `src/testagent-ts/src/test.ts` | ✅ |

## Judge (via praisonai-ts)

| Feature | Python | TypeScript | Status |
|---------|--------|------------|--------|
| `Judge` | praisonaiagents.eval | praisonai-ts/eval | ✅ |
| `JudgeConfig` | praisonaiagents.eval | praisonai-ts/eval | ✅ |
| `JudgeResult` | praisonaiagents.eval | praisonai-ts/eval | ✅ |

## CLI

| Command | Python | TypeScript | Status |
|---------|--------|------------|--------|
| `aitestagent <output>` | ✅ | ✅ | ✅ |
| `--expected` | ✅ | ✅ | ✅ |
| `--criteria` | ✅ | ✅ | ✅ |
| `--threshold` | ✅ | ✅ | ✅ |
