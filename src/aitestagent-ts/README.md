# aitestagent

> The world's easiest way to test anything using AI

[![npm version](https://badge.fury.io/js/aitestagent.svg)](https://www.npmjs.com/package/aitestagent)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, AI-powered testing library that uses LLM-as-judge to evaluate outputs. Built on top of [PraisonAI](https://www.npmjs.com/package/praisonai).

## Installation

```bash
npm install aitestagent
```

## Quick Start

```typescript
import { test, accuracy, criteria } from 'aitestagent';

// Test with custom criteria
const result = await test("Hello, world!", {
  criteria: "is a friendly greeting"
});
console.log(result.passed);  // true
console.log(result.score);   // 9

// Accuracy test
const acc = await accuracy("Paris", "Paris, France");
console.log(acc.passed);     // true

// Criteria test
const crit = await criteria("Hello!", "is polite and welcoming");
console.log(crit.score);     // 8
```

## Features

### 🎯 Simple Test Function

```typescript
import { test } from 'aitestagent';

const result = await test("The capital of France is Paris", {
  criteria: "is factually correct",
  threshold: 7.0,    // Pass threshold (1-10)
  model: "gpt-4"     // Optional: specify model
});
```

### ✅ Accuracy Testing

Compare outputs against expected values:

```typescript
import { accuracy } from 'aitestagent';

const result = await accuracy("4", "4");
// { passed: true, score: 10, reasoning: "..." }
```

### 📋 Criteria-Based Testing

Evaluate against custom criteria:

```typescript
import { criteria } from 'aitestagent';

const result = await criteria(
  "Thank you for your patience!",
  "is polite and professional"
);
// { passed: true, score: 9, reasoning: "..." }
```

### 🔧 CLI Tool

```bash
# Test with criteria
aitestagent "Hello world" -c "is a greeting"

# Accuracy test
aitestagent "4" -e "4"

# With custom threshold
aitestagent "Hello" -c "is friendly" -t 8.0
```

### 📊 Test Results

All functions return a `TestResult`:

```typescript
interface TestResult {
  passed: boolean;       // Did it pass the threshold?
  score: number;         // Score from 1-10
  reasoning: string;     // LLM's explanation
  suggestions: string[]; // Improvement suggestions
}
```

## Integration Examples

### With Vitest

```typescript
import { describe, it, expect } from 'vitest';
import { criteria } from 'aitestagent';

describe('Chatbot', () => {
  it('responds politely', async () => {
    const response = await chatbot.respond("Hi");
    const result = await criteria(response, "is friendly");
    expect(result.passed).toBe(true);
  }, 30000);
});
```

### With Jest

```typescript
import { accuracy } from 'aitestagent';

test('calculator adds correctly', async () => {
  const result = await accuracy(add(2, 2).toString(), "4");
  expect(result.score).toBeGreaterThanOrEqual(9);
}, 30000);
```

## Advanced Usage

Access the underlying Judge for more control:

```typescript
import { Judge } from 'aitestagent';

const judge = new Judge({ 
  threshold: 8.0,
  model: "gpt-4"
});

const result = await judge.run({
  output: "test output",
  criteria: "is correct and complete"
});
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key (required) |

## API Reference

### test(output, options)

Main testing function.

| Parameter | Type | Description |
|-----------|------|-------------|
| `output` | `string` | Output to evaluate |
| `options.expected` | `string?` | Expected output |
| `options.criteria` | `string?` | Evaluation criteria |
| `options.threshold` | `number?` | Pass threshold (default: 7.0) |
| `options.model` | `string?` | LLM model to use |

### accuracy(output, expected, threshold?)

Shorthand for accuracy testing.

### criteria(output, criteria, threshold?)

Shorthand for criteria-based testing.

## License

MIT © [Mervin Praison](https://github.com/mervinpraison)

## Links

- [Documentation](https://mervinpraison.github.io/TestAgent/typescript/)
- [GitHub](https://github.com/MervinPraison/TestAgent)
- [PraisonAI](https://www.npmjs.com/package/praisonai)
