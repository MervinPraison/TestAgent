/**
 * TestAgent - Simple AI testing with LLM-as-judge
 * Thin wrapper around praisonai-ts Judge
 */

import { Judge, type JudgeResult, type JudgeConfig } from 'praisonai';

export interface TestOptions {
    /** Expected output for accuracy comparison */
    expected?: string;
    /** Custom criteria for evaluation */
    criteria?: string;
    /** Threshold for pass/fail (1-10, default: 7.0) */
    threshold?: number;
    /** LLM model to use */
    model?: string;
}

export interface TestResult {
    /** Whether the test passed */
    passed: boolean;
    /** Score from 1-10 */
    score: number;
    /** LLM reasoning */
    reasoning: string;
    /** Improvement suggestions */
    suggestions: string[];
}

/**
 * Test an output using AI judge
 * 
 * @example
 * ```ts
 * import { test } from 'testagent';
 * 
 * // Simple accuracy test
 * const result = await test("Paris", { expected: "Paris, France" });
 * 
 * // Criteria-based test
 * const result = await test("Hello!", { criteria: "Response is friendly" });
 * ```
 */
export async function test(output: string, options: TestOptions = {}): Promise<TestResult> {
    const config: JudgeConfig = {
        threshold: options.threshold ?? 7.0,
        model: options.model,
    };

    const judge = new Judge(config);

    const result = await judge.run({
        output,
        expected: options.expected,
        criteria: options.criteria,
    });

    return {
        passed: result.passed,
        score: result.score,
        reasoning: result.reasoning,
        suggestions: result.suggestions,
    };
}

/**
 * Test for accuracy against expected output
 */
export async function accuracy(output: string, expected: string, threshold = 7.0): Promise<TestResult> {
    return test(output, { expected, threshold });
}

/**
 * Test against custom criteria
 */
export async function criteria(output: string, criteria: string, threshold = 7.0): Promise<TestResult> {
    return test(output, { criteria, threshold });
}
