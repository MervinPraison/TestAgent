# API Reference

Complete API reference for the aitestagent TypeScript SDK.

## Core Functions

### test(output, options)

The main testing function that evaluates any output using AI.

```typescript
import { test } from 'aitestagent';

const result = await test("The capital of France is Paris", {
  criteria: "factually correct",
  threshold: 7.0,
  model: "gpt-4"
});
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `output` | `string` | The output to evaluate |
| `options.expected` | `string?` | Expected output for accuracy comparison |
| `options.criteria` | `string?` | Custom criteria for evaluation |
| `options.threshold` | `number?` | Pass threshold 1-10 (default: 7.0) |
| `options.model` | `string?` | LLM model to use |

**Returns:** `Promise<TestResult>`

---

### accuracy(output, expected, threshold?)

Compare output against expected value.

```typescript
import { accuracy } from 'aitestagent';

const result = await accuracy("4", "4");
console.log(result.passed); // true
```

---

### criteria(output, criteria, threshold?)

Evaluate output against custom criteria.

```typescript
import { criteria } from 'aitestagent';

const result = await criteria("Hello!", "is a friendly greeting");
console.log(result.passed); // true
```

---

## Types

### TestResult

```typescript
interface TestResult {
  passed: boolean;      // Whether the test passed
  score: number;        // Score from 1-10
  reasoning: string;    // LLM's reasoning
  suggestions: string[]; // Improvement suggestions
}
```

### TestOptions

```typescript
interface TestOptions {
  expected?: string;   // Expected output
  criteria?: string;   // Custom criteria
  threshold?: number;  // Pass threshold (1-10)
  model?: string;      // LLM model
}
```

---

## Re-exports

The SDK also re-exports the underlying Judge from praisonai for advanced usage:

```typescript
import { Judge, JudgeConfig, JudgeResult } from 'aitestagent';

const judge = new Judge({ threshold: 8.0 });
const result = await judge.run({
  output: "test output",
  criteria: "is correct"
});
```
