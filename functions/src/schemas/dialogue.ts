import { z } from 'genkit';

export const DialogueInputSchema = z.object({
  card_id: z.string(),
  interaction_id: z.string(),
  prompt: z.string().min(4),
  schemaVersion: z.string().default('1.0'),
});

export const DialogueOutputSchema = z.object({
  text: z.string(),
  model: z.string(),
  modelVersion: z.string().optional(),
  version: z.string().default('1.0'),
  tier: z.string().default('free'),
  prompt_hash: z.string(),
  generation_time_ms: z.number(),
});

export type DialogueInput = z.infer<typeof DialogueInputSchema>;
export type DialogueOutput = z.infer<typeof DialogueOutputSchema>;


