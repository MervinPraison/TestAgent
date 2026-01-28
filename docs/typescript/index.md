# TypeScript SDK

The TypeScript SDK (`aitestagent`) provides the same powerful AI testing capabilities as the Python package, optimized for Node.js and TypeScript projects.

## Installation

```bash
npm install aitestagent
```

## Quick Start

```typescript
import { test, accuracy, criteria } from 'aitestagent';

// Simple test with custom criteria
const result = await test("Hello, world!", {
  criteria: "is a friendly greeting"
});

console.log(result.passed);  // true/false
console.log(result.score);   // 1-10
console.log(result.reasoning);
```

## Features

- **Simple API** - Just `test()`, `accuracy()`, and `criteria()`
- **LLM-as-Judge** - Powered by PraisonAI's Judge implementation
- **CLI Tool** - Test from command line with `aitestagent`
- **TypeScript First** - Full type definitions included
- **Caching** - Built-in result caching for faster iteration

## Next Steps

- [API Reference](api.md) - Complete API documentation
- [CLI Usage](cli.md) - Command line interface
- [Examples](examples.md) - Code examples and patterns
