#!/usr/bin/env node
/**
 * TestAgent CLI
 */

import { test } from './test.js';

async function main() {
    const args = process.argv.slice(2);

    if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
        console.log(`
testagent - AI-powered testing

Usage:
  testagent <output> [options]

Options:
  --expected, -e <text>    Expected output for accuracy test
  --criteria, -c <text>    Custom criteria for evaluation
  --threshold, -t <num>    Pass threshold (1-10, default: 7.0)
  --help, -h               Show this help

Examples:
  testagent "Paris" -e "Paris, France"
  testagent "Hello!" -c "Response is friendly"
`);
        process.exit(0);
    }

    const output = args[0];
    let expected: string | undefined;
    let criteria: string | undefined;
    let threshold = 7.0;

    for (let i = 1; i < args.length; i++) {
        const arg = args[i];
        if ((arg === '--expected' || arg === '-e') && args[i + 1]) {
            expected = args[++i];
        } else if ((arg === '--criteria' || arg === '-c') && args[i + 1]) {
            criteria = args[++i];
        } else if ((arg === '--threshold' || arg === '-t') && args[i + 1]) {
            threshold = parseFloat(args[++i]);
        }
    }

    try {
        const result = await test(output, { expected, criteria, threshold });

        const icon = result.passed ? '✅' : '❌';
        console.log(`${icon} Score: ${result.score}/10 (${result.passed ? 'PASSED' : 'FAILED'})`);
        console.log(`\nReasoning: ${result.reasoning}`);

        if (result.suggestions.length > 0) {
            console.log(`\nSuggestions:`);
            result.suggestions.forEach((s, i) => console.log(`  ${i + 1}. ${s}`));
        }

        process.exit(result.passed ? 0 : 1);
    } catch (error) {
        console.error('Error:', error instanceof Error ? error.message : error);
        process.exit(1);
    }
}

main();
