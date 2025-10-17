import { z } from 'genkit';

export const MSVSchema = z.object({
  affect: z.object({ valence: z.number(), arousal: z.number(), tension: z.number(), agency: z.number() }),
  harmony: z.object({ brightness: z.number(), consonance: z.number(), cadentialDrive: z.number() }),
  temporal: z.object({ tempo: z.number(), regularity: z.number() }),
  orchestration: z.object({ sparsity: z.number(), weights: z.record(z.number()).optional() }),
  texture: z.object({ intimacy: z.number(), privacy: z.number().optional() }),
});

export const MusicInputSchema = z.object({
  msv: MSVSchema,
  cue_id: z.string().optional(),
  schemaVersion: z.string().default('1.0'),
});

export const MusicOutputSchema = z.object({
  prompt: z.string(),
  model: z.string(),
  version: z.string().default('1.0'),
  tier: z.string().default('free'),
  prompt_hash: z.string(),
  generation_time_ms: z.number(),
});

export type MusicInput = z.infer<typeof MusicInputSchema>;
export type MusicOutput = z.infer<typeof MusicOutputSchema>;


