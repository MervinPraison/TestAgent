# Examples

Practical examples of using aitestagent in TypeScript projects.

## Basic Testing

### Test with Criteria

```typescript
import { test } from 'aitestagent';

async function validateChatResponse() {
  const response = await myChatbot.respond("Hello");
  
  const result = await test(response, {
    criteria: "is friendly, helpful, and appropriate"
  });
  
  if (!result.passed) {
    console.log("Failed:", result.reasoning);
  }
}
```

### Accuracy Testing

```typescript
import { accuracy } from 'aitestagent';

async function testMathFunction() {
  const answer = calculate(2, 2);
  
  const result = await accuracy(String(answer), "4");
  console.log(`Score: ${result.score}/10`);
}
```

---

## Integration with Test Frameworks

### With Vitest

```typescript
import { describe, it, expect } from 'vitest';
import { test, criteria } from 'aitestagent';

describe('Chatbot', () => {
  it('should give friendly responses', async () => {
    const response = await chatbot.respond("Hi");
    
    const result = await criteria(
      response, 
      "is friendly and welcoming"
    );
    
    expect(result.passed).toBe(true);
  }, 30000); // Increase timeout for LLM calls
});
```

### With Jest

```typescript
import { accuracy } from 'aitestagent';

describe('Calculator', () => {
  it('should add correctly', async () => {
    const result = await accuracy(
      calculator.add(2, 2).toString(),
      "4"
    );
    
    expect(result.score).toBeGreaterThanOrEqual(9);
  }, 30000);
});
```

---

## API Response Validation

```typescript
import { test } from 'aitestagent';

async function validateAPIResponse(response: any) {
  const result = await test(JSON.stringify(response), {
    criteria: `
      - Has status field
      - Contains data array
      - No error messages
    `
  });
  
  return result.passed;
}
```

---

## CI/CD Integration

```yaml
# .github/workflows/test.yml
name: AI Tests
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm install
      - run: npm test
    env:
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```
