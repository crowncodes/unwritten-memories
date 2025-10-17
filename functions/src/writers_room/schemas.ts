import { z } from 'genkit';

// Shared enums
export const TensionLevelSchema = z.enum([
  'SERENE',
  'INTRIGUE',
  'CONCERN',
  'PRESSURE',
  'URGENT',
  'CRITICAL',
  'CLIMACTIC',
]);

export const PacingRecommendationSchema = z.enum([
  'INJECT_INTRIGUE',
  'PROVIDE_RESPITE',
  'MAINTAIN_ESCALATION',
]);

export const ArcRecommendationSchema = z.enum([
  'ESTABLISH_STAKES',
  'GENERATE_COMPLICATION',
  'TRIGGER_DECISIVE_MOMENT',
  'RESOLVE_AND_REFLECT',
]);

export const CharacterRecommendationSchema = z.enum([
  'READY_FOR_CHALLENGE',
  'PROTECT_FROM_CRISIS',
  'NEEDS_INTERVENTION',
  'NEEDS_A_WIN',
]);

export const CriticRecommendationSchema = z.enum([
  'INJECT_SURPRISE',
  'ESCALATE_PERSONAL_STAKES',
  'INTRODUCE_CONTRAST',
  'ACTIVATE_DORMANT_RELATIONSHIP',
]);

// Inputs
export const SpecialistPlayerSchema = z.object({
  ocean: z.object({
    openness: z.number().min(0).max(5),
    conscientiousness: z.number().min(0).max(5),
    extraversion: z.number().min(0).max(5),
    agreeableness: z.number().min(0).max(5),
    neuroticism: z.number().min(0).max(5),
  }),
  capacity: z.number().min(0).max(10),
});

export const SpecialistInputSchema = z.object({
  seasonWeek: z.number().int().min(1).optional(),
  arcPosition: z.object({ currentAct: z.number().int().min(1).max(3) }).optional(),
  recentEvents: z.array(z.object({ id: z.string(), type: z.string(), week: z.number().int() })).default([]),
  player: SpecialistPlayerSchema,
  activeStates: z.array(z.string()).default([]),
  pacingHistory: z.array(TensionLevelSchema).default([]),
  aspirationStatus: z.object({ id: z.string().optional(), progress: z.number().min(0).max(100).optional() }).partial().optional(),
  retrievalTags: z.array(z.string()).default([]),
});

// Outputs
export const PacingRecSchema = z.object({
  recommendation: PacingRecommendationSchema,
  targetTension: TensionLevelSchema,
  rationale: z.string().min(1),
});

export const ArcRecSchema = z.object({
  recommendation: ArcRecommendationSchema,
  beatsNeeded: z.array(z.string()).default([]),
  rationale: z.string().min(1),
});

export const CharacterRecSchema = z.object({
  recommendation: CharacterRecommendationSchema,
  constraints: z.object({ maxIntensity: z.string().optional(), lockTypes: z.array(z.string()).default([]) }).default({}),
  rationale: z.string().min(1),
});

export const CriticRecSchema = z.object({
  recommendation: CriticRecommendationSchema,
  notes: z.array(z.string()).default([]),
});

export const ChoicesFrameworkSchema = z.object({
  axis: z.string(),
  no_right_answer: z.boolean().default(true),
  consequences_significant: z.boolean().default(true),
  options: z.array(z.object({
    type: z.string(),
    personality_alignment: z.string().optional(),
    consequences: z.string().optional(),
  })).default([]),
});

export const DirectorBriefSchema = z.object({
  event_type: z.string(),
  primary_emotion: z.string(),
  narrative_beat: z.string(),
  setup: z.object({
    trigger: z.string(),
    initial_tone: z.string(),
    reveal: z.string().optional(),
  }),
  twist: z.object({
    timing: z.string().optional(),
    revelation: z.string().optional(),
    deadline: z.string().optional(),
  }).partial().optional(),
  choices_framework: ChoicesFrameworkSchema,
  capacity_impact: z.object({ immediate: z.number().optional(), after_twist_revealed: z.number().optional(), net: z.number().optional() }).partial().default({}),
  thematic_tags: z.array(z.string()).default([]),
});

export const AnalystMetadataSchema = z.object({
  themes_expressed: z.array(z.string()).default([]),
  character_arc_notes: z.object({ pattern_identified: z.string().optional(), trait_reinforced: z.string().optional(), potential_arc: z.string().optional(), character_growth: z.string().optional() }).partial().default({}),
  symbolic_elements: z.array(z.object({ symbol: z.string(), interpretation: z.string() })).default([]),
  relationship_dynamics: z.object({
    sarah_relationship_status: z.string().optional(),
    sarah_emotional_state: z.string().optional(),
    future_hooks: z.array(z.string()).optional(),
  }).partial().default({}),
  narrative_callbacks: z.array(z.object({ callback_to: z.string(), relationship: z.string().optional() })).default([]),
  future_query_tags: z.array(z.string()).default([]),
});

export type SpecialistInput = z.infer<typeof SpecialistInputSchema>;
export type PacingRec = z.infer<typeof PacingRecSchema>;
export type ArcRec = z.infer<typeof ArcRecSchema>;
export type CharacterRec = z.infer<typeof CharacterRecSchema>;
export type CriticRec = z.infer<typeof CriticRecSchema>;
export type DirectorBrief = z.infer<typeof DirectorBriefSchema>;
export type AnalystMetadata = z.infer<typeof AnalystMetadataSchema>;


