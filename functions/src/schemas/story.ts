import { z } from 'genkit';

export const OCEANSchema = z.object({
  openness: z.number().min(0).max(5),
  conscientiousness: z.number().min(0).max(5),
  extraversion: z.number().min(0).max(5),
  agreeableness: z.number().min(0).max(5),
  neuroticism: z.number().min(0).max(5),
});

export const PlayerMetersSchema = z.object({
  physical: z.number().min(0).max(10).default(6),
  mental: z.number().min(0).max(10).default(6),
  social: z.number().min(0).max(10).default(6),
  emotional: z.number().min(0).max(10).default(6),
});

export const StorySeedSchema = z.object({
  aspiration_id: z.string(),
  season_length_weeks: z.enum(["12", "24", "36"]).transform((v) => Number(v)).or(z.number().int().min(12).max(36)),
  start_location_id: z.string().describe('e.g., "apartment"'),
  start_career: z.string().describe('short label, e.g., "junior_designer"'),
  backstory_hint: z.string().optional().describe('one-liner seed'),
  player_profile: z.object({
    ocean: OCEANSchema,
    capacity: z.number().min(0).max(10).default(6.0),
    meters: PlayerMetersSchema.optional(),
  }),
});

export const StoryInputSchema = z.object({
  seed: StorySeedSchema,
  schemaVersion: z.string().default('1.0'),
});

export const StoryWorldSchema = z.object({
  starting_location: z.object({
    id: z.string(),
    enriched_description: z.string(),
    signature_elements: z.array(z.string()).default([]),
    image_prompt: z.string(),
  }),
  starting_career: z.object({
    id: z.string(),
    description: z.string(),
  }),
  backstory: z.object({
    summary: z.string(),
    motivating_memory: z.string().optional(),
  }),
});

export const ArcPlanSchema = z.object({
  season_length_weeks: z.number(),
  three_act: z.object({
    act1_weeks: z.tuple([z.number(), z.number()]),
    act2_weeks: z.tuple([z.number(), z.number()]),
    act3_weeks: z.tuple([z.number(), z.number()]),
  }),
  decisive_decisions: z.array(z.object({
    id: z.string(),
    title: z.string(),
    window_weeks: z.tuple([z.number(), z.number()]),
    foreshadowing_weeks_before: z.array(z.number()).default([4,2,1]),
  })).min(1),
});

export const EventsPlanSchema = z.object({
  initial_weeks: z.array(z.object({
    week: z.number(),
    event_types: z.array(z.string()),
  })),
  tension_hooks_schedule: z.array(z.number()).optional(),
  mystery_threads: z.array(z.object({ id: z.string(), type: z.string(), planted_week: z.number() })).optional(),
});

export const MemorySeedSchema = z.object({
  title: z.string(),
  emotional_weight: z.number().min(0).max(10),
  tags: z.array(z.string()).default([]),
});

export const StoryOutputSchema = z.object({
  world: StoryWorldSchema,
  arc_plan: ArcPlanSchema,
  events_plan: EventsPlanSchema,
  memory_seeds: z.array(MemorySeedSchema).default([]),
  model: z.string(),
  modelVersion: z.string().optional(),
  version: z.string().default('1.0'),
  tier: z.string().default('free'),
  prompt_hash: z.string(),
  generation_time_ms: z.number(),
});

export type StoryInput = z.infer<typeof StoryInputSchema>;
export type StoryOutput = z.infer<typeof StoryOutputSchema>;




