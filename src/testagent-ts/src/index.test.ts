import { describe, it, expect } from 'vitest';
import { test, accuracy, criteria } from './index.js';

describe('TestAgent', () => {
    it('should export test function', () => {
        expect(typeof test).toBe('function');
    });

    it('should export accuracy function', () => {
        expect(typeof accuracy).toBe('function');
    });

    it('should export criteria function', () => {
        expect(typeof criteria).toBe('function');
    });
});

describe('TestAgent with LLM', () => {
    it('should run accuracy test', async () => {
        const result = await accuracy('Paris', 'Paris, France');
        expect(result).toHaveProperty('passed');
        expect(result).toHaveProperty('score');
        expect(result).toHaveProperty('reasoning');
        expect(result.score).toBeGreaterThanOrEqual(1);
        expect(result.score).toBeLessThanOrEqual(10);
    }, 30000);

    it('should run criteria test', async () => {
        const result = await criteria('Hello, how can I help you?', 'Response is friendly and helpful');
        expect(result).toHaveProperty('passed');
        expect(result).toHaveProperty('score');
        expect(result.score).toBeGreaterThanOrEqual(1);
        expect(result.score).toBeLessThanOrEqual(10);
    }, 30000);
});
