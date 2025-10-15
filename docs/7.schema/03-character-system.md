# Character System Schema

**Schema Version**: 1.0.0  
**Last Updated**: 2025-10-13  
**Dependencies**: `01-core-types.md`

---

## Overview

Defines all data structures for NPCs, player character, personality modeling, relationships, memory systems, and behavioral patterns.

---

## 1. Core Character Types

### Base Character Interface

```typescript
/**
 * Base character properties (Player & NPCs)
 */
interface BaseCharacter {
  character_id: string;             // PlayerID or NPCID
  character_type: "player" | "npc";
  
  // Identity
  name: string;
  age?: number;
  pronouns?: string[];
  
  // Personality
  personality: PersonalityTraits;
  personality_history: PersonalitySnapshot[];
  
  // State
  current_emotional_state: EmotionalState;
  current_location?: LocationID;
  
  // Relationships
  relationships: Record<string, Relationship>;
  
  // Metadata
  created_at: ISO8601String;
  first_appearance?: Week;
  schema_version: SemanticVersion;
}

/**
 * Personality snapshot at a point in time
 */
interface PersonalitySnapshot {
  week: Week;
  personality: PersonalityTraits;
  notable_change?: string;
  trigger?: string;
}
```

### Player Character

```typescript
/**
 * Player character - the protagonist
 */
interface PlayerCharacter extends BaseCharacter {
  character_id: PlayerID;
  character_type: "player";
  
  // Game state
  current_week: Week;
  current_day: DayOfWeek;
  current_turn: TurnOfDay;
  
  // Resources
  resources: PlayerResources;
  meters: Meters;
  
  // Progression
  life_direction: LifeDirection;
  active_aspirations: AspirationID[];
  completed_aspirations: AspirationID[];
  skills: Record<SkillID, SkillLevel>;
  perks: CardID[];
  
  // History
  total_cards_played: number;
  weeks_played: number;
  lifetime_number: number;          // Which lifetime (1, 2, 3...)
  previous_lifetimes?: PlayerLifetimeSummary[];
  
  // Preferences (player choices)
  preferences: PlayerPreferences;
}

interface SkillLevel {
  skill_id: SkillID;
  level: RangedInt<1, 10>;
  experience_points: number;
  xp_to_next_level: number;
}

interface PlayerPreferences {
  // Gameplay
  routine_batch_processing: boolean;
  auto_resolve_trivial: boolean;
  show_probabilities: boolean;
  
  // Content
  preferred_content_packs: PackID[];
  hidden_content_warnings: string[];
  
  // Narrative
  preferred_pov_style: "second_person" | "first_person";
  chapter_length_preference: "short" | "medium" | "long";
}

interface PlayerLifetimeSummary {
  lifetime_number: number;
  character_name: string;
  weeks_played: number;
  seasons_completed: number;
  final_age: number;
  ending_type: string;
  memorable_moments: string[];
}
```

### NPC Character

```typescript
/**
 * Non-player character
 */
interface NPCCharacter extends BaseCharacter {
  character_id: NPCID;
  character_type: "npc";
  
  // Core identity
  npc_profile: NPCProfile;
  
  // Behavior
  behavior_patterns: BehaviorPattern[];
  voice_profile: VoiceProfile;
  
  // Memory
  memory_system: NPCMemorySystem;
  
  // Relationship context
  primary_relationship_id?: string; // Player character ID
  relationship_level: RelationshipLevel;
  
  // Story role
  story_role: StoryRole;
  arc_involvement: Record<StoryArcID, ArcInvolvement>;
  
  // Appearance tracking
  first_met: Week;
  last_interaction: Week;
  total_interactions: number;
  
  // Generation
  ai_generated: boolean;
  generation_context?: AIContext;
  pack_source?: PackID;
}

/**
 * NPC profile - core character definition
 */
interface NPCProfile {
  // Background
  occupation?: string;
  background_summary: string;
  
  // Core traits
  surface_trait: string;            // How they appear
  deeper_truth: string;             // What drives them
  contradiction: string;            // Internal conflict
  wound: string;                    // Formative pain
  desire: string;                   // What they want
  fear: string;                     // What terrifies them
  
  // Physical identity
  visual_identity: VisualIdentity;
  
  // Archetype
  archetype?: CharacterArchetype;
}

interface VisualIdentity {
  key_features: string[];           // ["Freckles", "cerulean scarf"]
  recurring_behaviors: string[];    // ["Traces coffee rim when nervous"]
  sensory_associations: string[];   // ["Smells like coffee and vanilla"]
  age_range?: string;               // "mid-20s"
  style?: string;                   // "Casual artistic"
}

enum CharacterArchetype {
  Mentor = "mentor",
  Friend = "friend",
  Lover = "lover",
  Rival = "rival",
  Catalyst = "catalyst",
  Mirror = "mirror",
  Antagonist = "antagonist",
  Supporting = "supporting"
}

/**
 * Story role in current season
 */
interface StoryRole {
  role_type: StoryRoleType;
  importance: "main" | "supporting" | "minor" | "background";
  narrative_function: string;
  can_be_romance: boolean;
  can_be_antagonist: boolean;
}

enum StoryRoleType {
  Protagonist = "protagonist",      // Player only
  MajorCharacter = "major_character",
  SupportingCharacter = "supporting_character",
  RecurringCharacter = "recurring_character",
  MinorCharacter = "minor_character"
}

interface ArcInvolvement {
  arc_id: StoryArcID;
  role_in_arc: string;
  involvement_level: Intensity;     // 1-10
  key_moments: Week[];
}
```

---

## 2. Personality System

### OCEAN Model (Big 5)

```typescript
/**
 * Big 5 personality traits (defined in core-types, detailed here)
 */
interface PersonalityTraits {
  openness: Personality;            // 1.0-5.0
  conscientiousness: Personality;
  extraversion: Personality;
  agreeableness: Personality;
  neuroticism: Personality;
}

/**
 * Personality trait interpretations
 */
interface PersonalityInterpretation {
  trait: keyof PersonalityTraits;
  value: Personality;
  interpretation: TraitInterpretation;
}

interface TraitInterpretation {
  level: "very_low" | "low" | "moderate" | "high" | "very_high";
  behavioral_indicators: string[];
  affects_gameplay: string[];
  affects_relationships: string[];
}

/**
 * Openness interpretations
 */
const OPENNESS_INTERPRETATIONS: Record<string, TraitInterpretation> = {
  very_low: {
    level: "very_low",
    behavioral_indicators: [
      "Strongly prefers routine",
      "Uncomfortable with novelty",
      "Practical, concrete thinking",
      "Resistant to change"
    ],
    affects_gameplay: [
      "Exploration cards -70% appeal",
      "Routine formation after 2 repetitions",
      "Breaking routines costs +2 Emotional"
    ],
    affects_relationships: [
      "Bonds slowly with new people",
      "Values predictability in relationships",
      "Uncomfortable with abstract conversations"
    ]
  },
  // ... other levels
  very_high: {
    level: "very_high",
    behavioral_indicators: [
      "Craves novelty and variety",
      "Abstract, creative thinking",
      "Comfortable with uncertainty",
      "Curious about everything"
    ],
    affects_gameplay: [
      "Exploration cards +220% appeal",
      "Routine formation resisted (5+ repetitions needed)",
      "Breaking routines costs -1 Emotional"
    ],
    affects_relationships: [
      "Forms connections quickly",
      "Enjoys diverse social circles",
      "Deep philosophical conversations"
    ]
  }
};

/**
 * Personality evolution
 */
interface PersonalityEvolution {
  character_id: string;
  changes: PersonalityChange[];
}

interface PersonalityChange {
  change_id: string;
  occurred_at: GameTime;
  trait_affected: keyof PersonalityTraits;
  old_value: Personality;
  new_value: Personality;
  delta: number;
  trigger: PersonalityTrigger;
  permanent: boolean;
}

interface PersonalityTrigger {
  trigger_type: "single_event" | "accumulated_behavior" | "relationship" | "crisis";
  trigger_description: string;
  emotional_weight: Intensity;
  cards_involved?: CardID[];
}

/**
 * Personality compatibility
 */
interface PersonalityCompatibility {
  character_a_id: string;
  character_b_id: string;
  compatibility_score: Percentage;  // 0.0-1.0
  trait_alignments: TraitAlignment[];
  friction_points: string[];
  synergy_points: string[];
}

interface TraitAlignment {
  trait: keyof PersonalityTraits;
  a_value: Personality;
  b_value: Personality;
  difference: number;
  alignment: "aligned" | "complementary" | "neutral" | "conflicting";
}
```

---

## 3. Relationship System

### Core Relationship Structure

```typescript
/**
 * Relationship between two characters
 */
interface Relationship {
  relationship_id: string;
  from_character_id: string;
  to_character_id: string;
  
  // Core metrics
  trust: Trust;                     // 0.0-1.0
  attraction?: Trust;               // 0.0-1.0 (if applicable)
  social_capital: SocialCapital;    // -10 to +10
  
  // Classification
  relationship_type: RelationshipType;
  relationship_level: RelationshipLevel;
  
  // History
  first_met: Week;
  last_interaction: Week;
  total_interactions: number;
  
  // Evolution
  relationship_history: RelationshipSnapshot[];
  key_moments: RelationshipMoment[];
  
  // Current state
  current_dynamic: string;          // "Supportive but worried"
  unresolved_tensions: string[];
  shared_secrets: string[];
  
  // Trajectory
  trajectory: "improving" | "stable" | "declining" | "complicated";
}

enum RelationshipLevel {
  Stranger = 0,                     // Trust 0.0-0.2
  Acquaintance = 1,                 // Trust 0.2-0.4
  Friend = 2,                       // Trust 0.4-0.6
  CloseFriend = 3,                  // Trust 0.6-0.8
  BestFriend = 4,                   // Trust 0.8-0.95
  Soulmate = 5                      // Trust 0.95-1.0
}

/**
 * Relationship snapshot
 */
interface RelationshipSnapshot {
  week: Week;
  trust: Trust;
  attraction?: Trust;
  relationship_level: RelationshipLevel;
  current_dynamic: string;
  notable_event?: string;
}

/**
 * Relationship moment (key event)
 */
interface RelationshipMoment {
  moment_id: string;
  occurred_at: GameTime;
  moment_type: RelationshipMomentType;
  description: string;
  
  // Impact
  trust_delta: number;
  attraction_delta?: number;
  emotional_weight: Intensity;
  
  // Memory
  creates_memory: boolean;
  memory_id?: MemoryID;
  
  // Context
  cards_involved: CardID[];
  location?: LocationID;
  witnesses?: string[];
}

enum RelationshipMomentType {
  FirstMeeting = "first_meeting",
  VulnerabilityShared = "vulnerability_shared",
  ConflictResolved = "conflict_resolved",
  ConflictUnresolved = "conflict_unresolved",
  BoundarySet = "boundary_set",
  SupportGiven = "support_given",
  SupportReceived = "support_received",
  BetrayalOccurred = "betrayal_occurred",
  TrustRestored = "trust_restored",
  LevelUp = "level_up",
  LevelDown = "level_down"
}
```

### Relationship Dynamics

```typescript
/**
 * Dynamic relationship state
 */
interface RelationshipDynamic {
  relationship_id: string;
  
  // Current vibe
  primary_dynamic: string;          // "Supportive mentor"
  secondary_dynamics: string[];     // ["Occasionally competitive", "Mutually inspiring"]
  
  // Emotional tone
  emotional_tenor: "warm" | "neutral" | "tense" | "complicated";
  
  // Interaction patterns
  interaction_frequency: Frequency;
  typical_activities: CardCategory[];
  conversation_depth_typical: ConversationDepth;
  
  // Power dynamics
  power_balance: "equal" | "from_has_more" | "to_has_more";
  who_initiates_more: "from" | "to" | "balanced";
  
  // Evolution potential
  can_deepen_further: boolean;
  can_become_romantic: boolean;
  at_risk_of_ending: boolean;
  stagnant: boolean;
}

/**
 * Relationship health
 */
interface RelationshipHealth {
  relationship_id: string;
  
  // Health score
  health_score: Percentage;         // 0.0-1.0
  health_status: "thriving" | "healthy" | "strained" | "critical" | "ended";
  
  // Contributing factors
  positive_factors: HealthFactor[];
  negative_factors: HealthFactor[];
  
  // Needs
  needs_attention: boolean;
  weeks_since_interaction: number;
  neglect_level: Intensity;         // 0-10
  
  // Risk
  at_risk_of_crisis: boolean;
  risk_factors: string[];
}

interface HealthFactor {
  factor: string;
  impact: number;                   // -1.0 to +1.0
  description: string;
}
```

---

## 4. NPC Memory System

### Memory Architecture

```typescript
/**
 * NPC memory system - three-tier
 */
interface NPCMemorySystem {
  npc_id: NPCID;
  
  // Three tiers
  short_term: ShortTermMemory;
  medium_term: MediumTermMemory;
  long_term: LongTermMemory;
  
  // Processing
  consolidation_schedule: ConsolidationSchedule;
  memory_capacity: MemoryCapacity;
}

/**
 * Short-term memory (24 hours)
 */
interface ShortTermMemory {
  memories: Memory[];
  max_capacity: number;             // 5-10 memories
  retention_duration: Duration;     // 1 day
  
  // Auto-consolidation
  consolidates_to_medium_if: ConsolidationCriteria;
}

/**
 * Medium-term memory (1-4 weeks)
 */
interface MediumTermMemory {
  memories: Memory[];
  max_capacity: number;             // 15-30 memories
  retention_duration: Duration;     // 1-4 weeks
  
  // Auto-consolidation
  consolidates_to_long_if: ConsolidationCriteria;
  fades_if: FadingCriteria;
}

/**
 * Long-term memory (permanent)
 */
interface LongTermMemory {
  memories: Memory[];
  max_capacity: number;             // 50-100 significant memories
  permanent: boolean;
  
  // Organization
  indexed_by: {
    emotional_weight: Record<Intensity, MemoryID[]>;
    other_character: Record<string, MemoryID[]>;
    location: Record<LocationID, MemoryID[]>;
    week: Record<Week, MemoryID[]>;
  };
}

/**
 * Individual memory
 */
interface Memory {
  memory_id: MemoryID;
  created_at: GameTime;
  
  // Content
  event_type: string;
  description: string;
  other_characters: string[];
  location?: LocationID;
  
  // Emotional content
  emotion_at_time: EmotionalState;
  emotional_valence: number;        // -1.0 to +1.0 (negative to positive)
  emotional_weight: Intensity;      // 1-10
  
  // Memory properties
  vividness: Percentage;            // How clear/detailed
  accuracy: Percentage;             // How accurate (can be distorted)
  importance: Intensity;
  
  // Consolidation
  tier: "short" | "medium" | "long";
  consolidation_count: number;      // How many times reinforced
  last_accessed: GameTime;
  
  // Tags
  tags: string[];
  linked_memories: MemoryID[];
  
  // Effects personality
  personality_impact?: Partial<PersonalityTraits>;
  unlocks?: string[];
}

/**
 * Memory consolidation criteria
 */
interface ConsolidationCriteria {
  min_emotional_weight: Intensity;
  min_access_count: number;
  involves_important_character: boolean;
  relates_to_core_traits: boolean;
}

interface FadingCriteria {
  weeks_without_access: number;
  low_emotional_weight: boolean;
  contradicted_by_newer_memory: boolean;
}

/**
 * Memory consolidation schedule
 */
interface ConsolidationSchedule {
  short_to_medium: {
    frequency: Duration;            // Every 24 hours
    last_run: ISO8601String;
    next_run: ISO8601String;
  };
  medium_to_long: {
    frequency: Duration;            // Every week
    last_run: ISO8601String;
    next_run: ISO8601String;
  };
}

interface MemoryCapacity {
  short_term_capacity: number;
  medium_term_capacity: number;
  long_term_capacity: number;
  total_memories: number;
  memory_pressure: Percentage;      // How full
}
```

### Memory Operations

```typescript
/**
 * Create memory operation
 */
interface CreateMemoryOperation {
  operation_type: "create";
  npc_id: NPCID;
  memory_data: Partial<Memory>;
  tier: "short" | "medium" | "long";
}

/**
 * Consolidate memory operation
 */
interface ConsolidateMemoryOperation {
  operation_type: "consolidate";
  memory_id: MemoryID;
  from_tier: "short" | "medium";
  to_tier: "medium" | "long";
  reason: string;
}

/**
 * Recall memory operation
 */
interface RecallMemoryOperation {
  operation_type: "recall";
  npc_id: NPCID;
  query: MemoryQuery;
  results: Memory[];
}

interface MemoryQuery {
  query_type: "by_character" | "by_emotion" | "by_location" | "by_week" | "by_tags" | "recent";
  filters: Record<string, any>;
  limit?: number;
  min_emotional_weight?: Intensity;
}

/**
 * Update memory operation (memories can be reinterpreted)
 */
interface UpdateMemoryOperation {
  operation_type: "update";
  memory_id: MemoryID;
  changes: Partial<Memory>;
  reason: string;                   // Why memory is being updated
  
  // Distortion tracking
  original_values?: Partial<Memory>;
  distortion_type?: "enhancement" | "suppression" | "reinterpretation";
}
```

---

## 5. Behavioral Patterns

### Behavior System

```typescript
/**
 * NPC behavior pattern
 */
interface BehaviorPattern {
  pattern_id: string;
  pattern_name: string;
  pattern_type: BehaviorPatternType;
  
  // Trigger
  triggers: BehaviorTrigger[];
  
  // Actions
  typical_actions: BehaviorAction[];
  
  // Personality link
  driven_by_trait: keyof PersonalityTraits;
  intensity_factor: number;         // How strongly trait expresses
}

enum BehaviorPatternType {
  Initiative = "initiative",        // NPC initiates contact
  Response = "response",            // How NPC responds
  Avoidance = "avoidance",          // What NPC avoids
  Seeking = "seeking",              // What NPC seeks
  Habit = "habit",                  // Recurring behavior
  Stress = "stress"                 // Behavior under stress
}

interface BehaviorTrigger {
  trigger_type: string;
  condition: string;
  threshold?: number;
  frequency?: Frequency;
}

interface BehaviorAction {
  action_type: "card_generation" | "dialogue" | "relationship_change" | "state_change";
  action_details: any;
  probability: Probability;
}

/**
 * NPC agency - how NPCs act autonomously
 */
interface NPCAgency {
  npc_id: NPCID;
  
  // Initiative
  initiative_level: Intensity;      // 1-10, how proactive
  reaches_out_frequency: Frequency;
  
  // Awareness
  notices: NPCAwareness;
  
  // Needs
  current_needs: NPCNeed[];
  
  // Boundaries
  boundaries: NPCBoundary[];
}

interface NPCAwareness {
  player_stress_level: boolean;
  player_major_life_events: boolean;
  time_since_last_interaction: boolean;
  player_career_situation: boolean;
  player_other_relationships: boolean;
}

interface NPCNeed {
  need_type: "connection" | "support" | "space" | "validation" | "help";
  intensity: Intensity;
  expressed_how: string[];
  if_unmet_consequence: string;
}

interface NPCBoundary {
  boundary_type: "emotional" | "time" | "topic" | "physical";
  description: string;
  if_violated_reaction: string;
  can_change_over_time: boolean;
}
```

---

## 6. Voice & Dialogue

### Voice Profile

```typescript
/**
 * Character voice profile (for dialogue generation)
 */
interface VoiceProfile {
  character_id: string;
  
  // Speaking patterns
  speech_patterns: SpeechPattern[];
  vocabulary_level: "simple" | "moderate" | "sophisticated" | "mixed";
  typical_sentence_length: "short" | "medium" | "long" | "varied";
  
  // Thought patterns (for POV)
  internal_monologue_style: string;
  metaphor_preference: string;
  
  // Emotional expression
  how_expresses_emotion: string;
  what_suppresses: string;
  tells_when_lying: string[];
  
  // Unique markers
  verbal_tics: string[];
  behavioral_tics: string[];
  catchphrases?: string[];
  
  // Differentiation
  distinct_from_other_povs: string;
  
  // Examples
  example_phrases: string[];
  example_internal_thoughts: string[];
}

interface SpeechPattern {
  pattern: string;
  condition: string;                // When this pattern appears
  examples: string[];
}

/**
 * Dialogue generation context
 */
interface DialogueContext {
  speaking_character: string;
  listening_characters: string[];
  
  // Situational
  location: LocationID;
  emotional_state: EmotionalState;
  conversation_depth: ConversationDepth;
  
  // Relationship
  relationship_state: Record<string, Relationship>;
  
  // History
  recent_topics: string[];
  unresolved_topics: string[];
  
  // Intent
  speaker_intent: SpeakerIntent;
  
  // Constraints
  character_voice: VoiceProfile;
  topic_restrictions: string[];
}

interface SpeakerIntent {
  primary_goal: "inform" | "persuade" | "connect" | "deflect" | "confront" | "support";
  subtext?: string;                 // What they're really saying
  desired_outcome: string;
}
```

---

## 7. Character Creation & Generation

### Character Creation (Player)

```typescript
/**
 * Character creation data
 */
interface CharacterCreation {
  creation_id: string;
  player_id: PlayerID;
  
  // Basic info
  name: string;
  pronouns: string[];
  
  // Personality selection
  personality_method: "quiz" | "manual" | "random";
  personality_result: PersonalityTraits;
  
  // Starting conditions
  starting_age: number;
  starting_location: LocationID;
  starting_life_direction?: LifeDirection;
  
  // Preferences
  content_preferences: ContentPreferences;
  difficulty_preferences: DifficultyPreferences;
  
  // Validation
  valid: boolean;
  validation_errors: string[];
}

interface ContentPreferences {
  preferred_themes: string[];
  avoided_themes: string[];
  romance_content: "yes" | "no" | "optional";
  intensity_level: "light" | "moderate" | "intense";
}

interface DifficultyPreferences {
  resource_scarcity: "easy" | "balanced" | "challenging";
  relationship_difficulty: "easy" | "balanced" | "challenging";
  crisis_frequency: "rare" | "moderate" | "frequent";
  success_chances: "generous" | "balanced" | "realistic";
}
```

### NPC Generation

```typescript
/**
 * NPC generation request
 */
interface NPCGenerationRequest {
  request_id: string;
  generation_method: "ai" | "template" | "pack";
  
  // Context
  player_context: {
    personality: PersonalityTraits;
    life_direction: LifeDirection;
    current_week: Week;
    emotional_state: EmotionalState;
  };
  
  // Constraints
  archetype?: CharacterArchetype;
  relationship_potential: "high" | "medium" | "low";
  story_role: StoryRoleType;
  
  // Requirements
  must_have_traits?: Partial<PersonalityTraits>;
  must_fit_location?: LocationID;
  must_fit_theme?: string;
  
  // Diversity
  ensure_diversity: boolean;
  existing_npc_ids: NPCID[];
}

/**
 * NPC generation result
 */
interface NPCGenerationResult {
  npc_id: NPCID;
  npc_data: NPCCharacter;
  
  // Generation metadata
  generated_by: "ai" | "template" | "pack";
  ai_model?: string;
  generation_prompt?: string;
  
  // Validation
  meets_requirements: boolean;
  compatibility_score: Percentage;
  
  // Assets
  portrait_generated: boolean;
  portrait_url?: URL;
  voice_generated: boolean;
  
  // Review
  requires_human_review: boolean;
  quality_score: number;
}
```

---

## Notes for LLM Analysis

When validating character system schemas:

1. **ID Formats**: All character IDs match PlayerID or NPCID patterns
2. **Personality Ranges**: All OCEAN traits 1.0-5.0
3. **Trust Ranges**: All trust/attraction values 0.0-1.0
4. **Relationship Levels**: Map correctly to trust thresholds
5. **Memory Tiers**: Proper consolidation between short/medium/long
6. **Behavior Triggers**: Link to actual game events/states
7. **Voice Profiles**: Ensure uniqueness across NPCs
8. **Generation Context**: References valid game state

**Cross-schema dependencies**:
- PlayerResources from gameplay-mechanics
- EmotionalState from emotional-system
- LocationID from gameplay-mechanics
- CardID from card-system
- StoryArcID from narrative-system
- Memory consolidation affects novel-generation POV data

