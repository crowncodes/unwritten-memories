import crypto from 'node:crypto';
import { z } from 'genkit';
import { LifebondContext } from '../context/contextTypes';

export type Step<TIn, TOut> = (input: TIn, ctx: LifebondContext) => Promise<TOut>;

export const normalizeInputStep: Step<unknown, unknown> = async (input) => input;

export const assembleContextStep: Step<unknown, LifebondContext> = async (_input, ctx) => ctx;

export function hashPrompt(prompt: string): string {
  return crypto.createHash('sha256').update(prompt).digest('hex').slice(0, 16);
}

export const dedupeByPromptHashStep: Step<{ prompt: string }, { prompt: string; promptHash: string }> = async ({ prompt }) => {
  const promptHash = hashPrompt(prompt);
  return { prompt, promptHash };
};

export const validateStep = <T>(schema: z.ZodType<T>): Step<T, T> => {
  return async (input) => schema.parse(input);
};

export interface PersistResult {
  id?: string;
  path?: string;
}

export const persistStep: Step<{ data: unknown }, PersistResult> = async () => {
  // Placeholder: actual Firestore/Storage writes implemented per domain flows
  return {};
};

export interface EvaluationFeedback {
  scores?: Record<string, number>;
  suggestions?: string[];
}

export const evaluateStep: Step<{ outputText?: string; prompt?: string }, EvaluationFeedback> = async () => {
  // Placeholder evaluator; replace with Genkit evaluator plugins
  return { scores: { clarity: 0.8 }, suggestions: [] };
};

export interface TelemetryRecord {
  operation: string;
  durationMs: number;
  model?: string;
  tier?: string;
}

export const telemetryStep: Step<TelemetryRecord, void> = async () => {
  return;
};




