# Narrative System Schema

**Schema Version**: 1.0.0  
**Last Updated**: 2025-10-13  
**Dependencies**: `01-core-types.md`, `02-card-system.md`, `03-character-system.md`, `04-gameplay-mechanics.md`

---

## Overview

Defines story arcs, narrative structure, decisive decisions, memory formation, timeline management, and seasonal progression for compelling storytelling.

---

## 1. Story Arc System

### Core Story Arc Structure

```typescript
/**
 * Story arc - multi-phase narrative thread
 */
interface StoryArc {
  arc_id: StoryArcID;
  title: string;
  category: StoryArcCategory;
  
  // Structure
  phases: ArcPhase[];
  current_phase: number;
  
  // State
  status: ArcStatus;
  started_at: Week;
  last_activity: Week;
  
  // Participants
  primary_npcs: NPCID[];
  secondary_npcs: NPCID[];
  locations: LocationID[];
  
  // Progression
  progress_percentage: Percentage;  // 0.0-1.0
  weeks_active: number;
  weeks_neglected: number;
  
  // Outcomes
  failure_conditions: FailureCondition[];
  success_variations: SuccessVariation[];
  
  // Integration
  conflicts_with: StoryArcID[];    // Concurrent arcs with conflicts
  builds_on: StoryArcID[];         // Previous arcs this extends
  
  // Metadata
  emotional_theme: string;
  narrative_weight: Intensity;      // 1-10
  can_fail: boolean;
  player_initiated: boolean;
  pack_source?: PackID;
  
  schema_version: SemanticVersion;
}

enum StoryArcCategory {
  Career = "career",
  Relationship = "relationship",
  Personal = "personal",
  Creative = "creative",
  Family = "family",
  Health = "health",
  Financial = "financial",
  Spiritual = "spiritual",
  Community = "community",
  Adventure = "adventure"
}

enum ArcStatus {
  Dormant = "dormant",              // Not yet started
  Active = "active",                // Currently progressing
  Neglected = "neglected",          // Active but ignored
  AtRisk = "at_risk",               // About to fail
  Succeeded = "succeeded",          // Completed successfully
  Failed = "failed",                // Failed or abandoned
  Archived = "archived"             // Completed and archived
}
```

### Arc Phase Structure

```typescript
/**
 * Phase within story arc
 */
interface ArcPhase {
  phase_id: string;
  phase_number: number;
  title: string;
  
  // Timing
  week_range: [Week, Week];
  duration_weeks: number;
  
  // Entry
  trigger_requirements: PhraseTrigger[];
  automatically_enters: boolean;
  
  // Goals
  goals: PhaseGoal[];
  optional_goals: PhaseGoal[];
  
  // Content
  cards_unlocked: CardID[];
  generated_cards: CardID[];
  
  // Tension
  tension_description: string;
  emotional_tone: EmotionalState[];
  
  // Decisive decision
  decisive_decision?: DecisiveDecision;
  
  // Crisis
  crisis_risk?: CrisisRisk;
  
  // Progression
  completion_criteria: CompletionCriteria;
  completion_status: "not_started" | "in_progress" | "complete" | "failed";
}

interface PhraseTrigger {
  trigger_type: "phase_complete" | "card_played" | "relationship_level" | "time_passed" | "event_occurred";
  requirement: any;
  met: boolean;
}

interface PhaseGoal {
  goal_id: string;
  description: string;
  measurable: boolean;
  current_progress: number;
  target_progress: number;
  completed: boolean;
}

interface CrisisRisk {
  risk_type: CrisisTriggerType;
  probability: Probability;
  triggers_if: string;
  can_be_avoided: boolean;
}
```

### Decisive Decisions

```typescript
/**
 * Major life-defining decision
 */
interface DecisiveDecision {
  decision_id: string;
  card_id: CardID;                  // The card that presents decision
  arc_id: StoryArcID;
  
  // Framing
  title: string;
  description: string;
  stakes_description: string;
  
  // Timing
  appears_at_week: Week;
  foreshadowed_at?: Week[];
  time_limit?: Duration;
  
  // Weight
  decision_weight: DecisionWeight.LifeDefining;
  
  // Conflict
  same_day_conflict?: CardID;
  mutually_exclusive_arcs?: StoryArcID[];
  
  // Options
  choices: DecisiveChoice[];
  
  // Dramatic structure
  internal_conflict: string;
  external_pressure: string;
  emotional_stakes: string;
  
  // Permanence
  irreversible: boolean;
  can_revisit_later: boolean;
  
  // Memory
  always_creates_memory: true;
  memory_emotional_weight: RangedInt<8, 10>; // Always high
}

/**
 * Choice within decisive decision
 */
interface DecisiveChoice {
  choice_id: string;
  choice_name: string;
  description: string;
  
  // Arc impact
  arc_progression: "advance" | "maintain" | "terminate" | "fork";
  unlocks_phases?: number[];
  ends_arc?: boolean;
  starts_new_arc?: StoryArcID;
  
  // Immediate outcomes
  immediate_positive: string[];
  immediate_negative: string[];
  
  // Long-term outcomes
  longterm_positive: string[];
  longterm_negative: string[];
  
  // Effects
  effects: CardEffect[];
  meter_changes: Partial<Meters>;
  relationship_impacts: Record<NPCID, number>;
  
  // Resources
  costs: ResourceCost;
  
  // Personality
  personality_alignment: Partial<PersonalityTraits>;
  regret_risk: Intensity;
  
  // Success
  requires_success_roll: boolean;
  success_chance?: SuccessChance;
  
  // Memory
  memory_interpretation: string;   // How this is remembered
}
```

### Arc Failure & Success

```typescript
/**
 * Arc failure condition
 */
interface FailureCondition {
  condition_id: string;
  condition_type: "decisive_choice" | "neglect" | "crisis" | "prerequisite_failed";
  
  // Trigger
  triggers_if: string;
  threshold?: number;
  grace_period?: Duration;
  
  // Result
  arc_terminates: boolean;
  partial_recovery_possible: boolean;
  
  // Consequences
  consequences: ArcConsequence[];
  
  // Memory
  creates_memory: boolean;
  memory_type: "regret" | "failure" | "lesson_learned";
  memory_title: string;
}

/**
 * Arc success variation
 */
interface SuccessVariation {
  variation_id: string;
  path_name: string;
  description: string;
  
  // Conditions
  achieved_if: string;
  requires_phases: number[];
  requires_choices: string[];
  
  // Rewards
  fusion_card?: FusionID;
  unlocked_content: string[];
  skill_improvements: Record<SkillID, number>;
  
  // Impact
  ending_impact: string;
  quality_tier: "satisfying" | "good" | "great" | "perfect";
  
  // Future
  enables_future_arcs: StoryArcID[];
  affects_future_seasons: string[];
}

interface ArcConsequence {
  consequence_type: "meter_change" | "relationship_change" | "unlock" | "lock" | "emotional_state";
  description: string;
  permanent: boolean;
  severity: Intensity;
}
```

---

## 2. Memory & Timeline

### Memory Formation

```typescript
/**
 * Narrative memory (player perspective, for book generation)
 */
interface NarrativeMemory {
  memory_id: MemoryID;
  memory_type: MemoryType;
  
  // When
  occurred_at: GameTime;
  week_number: Week;
  season_number: number;
  
  // What
  title: string;
  description: string;
  event_summary: string;
  
  // Who
  player_emotional_state: EmotionalState;
  characters_present: NPCID[];
  character_perspectives: Record<NPCID, NPCPerspective>;
  
  // Where
  location: LocationID;
  location_atmosphere: string;
  
  // Why significant
  narrative_significance: Intensity; // 1-10
  emotional_weight: Intensity;       // 1-10
  turning_point: boolean;
  
  // Sensory details
  sensory_snapshot: SensorySnapshot;
  
  // Context
  related_arc: StoryArcID;
  arc_phase?: number;
  decisive_decision?: DecisiveDecision;
  
  // Cards involved
  cards_played: CardID[];
  outcome: OutcomeType;
  
  // Relationships
  relationship_impacts: Record<NPCID, RelationshipMoment>;
  
  // Future impact
  referenced_later: Week[];
  callbacks: CallbackReference[];
  
  // Book generation
  chapter_candidate: boolean;
  pov_character: string;            // Who narrates this memory
  literary_techniques: string[];    // Techniques to use when writing
  
  schema_version: SemanticVersion;
}

interface NPCPerspective {
  npc_id: NPCID;
  
  // Their view
  how_they_saw_event: string;
  what_they_felt: EmotionalState;
  what_they_thought: string;        // Internal monologue
  what_they_noticed: string[];
  
  // Memory in their system
  their_memory_id?: MemoryID;
  their_memory_tier: "short" | "medium" | "long";
  
  // Differences from player perspective
  perspective_differences: string[];
}

interface SensorySnapshot {
  visual: string[];                 // What was seen
  auditory: string[];               // What was heard
  tactile: string[];                // What was felt
  olfactory: string[];              // What was smelled
  gustatory: string[];              // What was tasted
  emotional_sense: string;          // The "feeling" of the moment
}

interface CallbackReference {
  callback_id: string;
  appears_in_week: Week;
  callback_type: "echo" | "contrast" | "resolution" | "parallel";
  description: string;
}
```

### Timeline Management

```typescript
/**
 * Game timeline
 */
interface GameTimeline {
  player_id: PlayerID;
  lifetime_number: number;
  
  // Current state
  current_week: Week;
  total_weeks_played: number;
  current_season: number;
  weeks_in_season: number;
  
  // History
  key_events: TimelineEvent[];
  decisive_decisions: Week[];
  crises: Week[];
  breakthroughs: Week[];
  
  // Arcs
  active_arcs: StoryArcID[];
  completed_arcs: StoryArcID[];
  failed_arcs: StoryArcID[];
  
  // Memories
  total_memories: number;
  memorable_weeks: Week[];
  
  // Quality metrics
  dramatic_density: Percentage;     // How much drama per week
  emotional_variety: number;        // How many different emotional states
  relationship_depth: number;       // Average relationship quality
  
  // Future planning
  planted_seeds: PlantedSeed[];
  foreshadowed_events: ForeshadowedEvent[];
}

interface TimelineEvent {
  event_id: string;
  week: Week;
  event_type: EventType;
  title: string;
  description: string;
  significance: Intensity;
  creates_memory: boolean;
  memory_id?: MemoryID;
}

interface PlantedSeed {
  seed_id: string;
  planted_at: Week;
  seed_type: "foreshadowing" | "setup" | "callback_target" | "character_intro";
  description: string;
  pays_off_at?: Week;
  paid_off: boolean;
}

interface ForeshadowedEvent {
  event_id: string;
  foreshadowed_at: Week[];
  will_occur_at: Week;
  event_description: string;
  foreshadowing_method: string[];
}
```

---

## 3. Season Structure

### Season Definition

```typescript
/**
 * Season - complete story arc (12-100 weeks)
 */
interface Season {
  season_id: SeasonID;
  season_number: number;
  title: string;
  
  // Timeframe
  start_week: Week;
  end_week: Week;
  weeks_duration: number;           // 12-100, typically 12-48
  
  // Three-act structure
  act_structure: ActStructure;
  
  // Arcs
  primary_arc: StoryArcID;
  secondary_arcs: StoryArcID[];
  
  // Theme
  season_theme: string;
  emotional_journey: EmotionalJourney;
  
  // Quality
  dramatic_quality: Percentage;     // How compelling the season was
  emotional_resonance: Percentage;
  character_growth: Percentage;
  
  // Ending
  ending_type: SeasonEndingType;
  climax_week: Week;
  resolution_quality: "incomplete" | "satisfying" | "powerful" | "perfect";
  
  // Persistence
  archived_cards: CardID[];
  memorable_moments: MemoryID[];
  key_decisions: DecisiveDecision[];
  
  // Book generation
  generates_book: boolean;
  estimated_chapters: number;
  book_quality: "free_tier" | "premium_tier";
  
  schema_version: SemanticVersion;
}

/**
 * Three-act structure within season
 */
interface ActStructure {
  act_1: Act;
  act_2: Act;
  act_3: Act;
}

interface Act {
  act_number: 1 | 2 | 3;
  title: string;
  
  // Timeframe
  week_range: [Week, Week];
  
  // Narrative function
  function: string;                 // "Discovery", "Pursuit", "Crisis"
  stakes: "low" | "moderate" | "high";
  
  // Content
  major_events: TimelineEvent[];
  arc_phases_active: number[];
  
  // Emotional arc
  dominant_emotions: EmotionalState[];
  emotional_trajectory: "rising" | "falling" | "oscillating";
}

enum SeasonEndingType {
  Cliffhanger = "cliffhanger",      // Continues to next season
  Resolution = "resolution",         // Complete but room for more
  Bittersweet = "bittersweet",      // Mixed success/failure
  Triumph = "triumph",              // Major success
  Tragedy = "tragedy",              // Major failure
  Transformation = "transformation", // Character fundamentally changed
  PlayerChoice = "player_choice"    // Player decided ending
}

interface EmotionalJourney {
  starting_state: EmotionalState;
  journey_beats: EmotionalBeat[];
  ending_state: EmotionalState;
  
  // Arc
  follows_arc: boolean;             // Clear emotional progression
  peak_emotion_week: Week;
  lowest_emotion_week: Week;
  
  // Variety
  states_experienced: EmotionalState[];
  total_transitions: number;
  
  // Quality
  authentic: boolean;               // Feels real, not random
  earned: boolean;                  // Changes feel earned
}

interface EmotionalBeat {
  week: Week;
  state: EmotionalState;
  trigger: string;
  intensity: Intensity;
  narrative_purpose: string;
}
```

### Season Archive

```typescript
/**
 * Season archive data (for persistence across lifetimes)
 */
interface SeasonArchive {
  season_id: SeasonID;
  player_id: PlayerID;
  
  // Summary
  season_summary: SeasonSummary;    // From gameplay-mechanics
  
  // Preserved content
  archived_cards: MemoryCard[];
  archived_relationships: ArchivedRelationship[];
  archived_personality: PersonalitySnapshot;
  
  // Achievements
  aspirations_completed: AspirationID[];
  fusion_cards_created: FusionCard[];
  skills_mastered: SkillID[];
  
  // Narrative
  key_moments: NarrativeMemory[];
  decisive_decisions_made: DecisiveDecision[];
  story_arcs_completed: StoryArc[];
  
  // Book
  book_generated: boolean;
  book_data?: GeneratedBook;
  
  // Metadata
  archived_at: ISO8601String;
  free_tier_slots_used: number;
  premium_tier: boolean;
  
  schema_version: SemanticVersion;
}

interface ArchivedRelationship {
  npc_id: NPCID;
  final_trust: Trust;
  final_level: RelationshipLevel;
  relationship_summary: string;
  memorable_moments: RelationshipMoment[];
  continues_to_next_season: boolean;
}

interface GeneratedBook {
  book_id: string;
  title: string;
  chapters: GeneratedChapter[];
  word_count: number;
  generation_quality: "free" | "premium";
  generated_at: ISO8601String;
  
  // Metadata
  genre_tags: string[];
  content_warnings: string[];
  reading_time_minutes: number;
}

interface GeneratedChapter {
  chapter_number: number;
  title: string;
  pov_character: string;
  source_memories: MemoryID[];
  word_count: number;
  excerpt: string;                  // First 200 words
}
```

---

## 4. Continuity & Consistency

### Continuity Tracking

```typescript
/**
 * Continuity system (prevents contradictions)
 */
interface ContinuityTracker {
  player_id: PlayerID;
  
  // Established facts
  established_facts: EstablishedFact[];
  
  // Character consistency
  character_states: Record<string, CharacterState>;
  
  // World state
  world_state: WorldState;
  
  // Relationships
  relationship_history: Record<string, RelationshipHistory>;
  
  // Validation
  validates_against_history: boolean;
  contradiction_checks_enabled: boolean;
}

interface EstablishedFact {
  fact_id: string;
  fact_type: "character_trait" | "event" | "relationship" | "world_state" | "decision";
  
  // Content
  description: string;
  established_at: Week;
  
  // Immutability
  immutable: boolean;
  can_evolve: boolean;
  
  // References
  referenced_in_memories: MemoryID[];
  affects_future_content: boolean;
  
  // Validation
  must_be_consistent_with: string[];
}

interface CharacterState {
  character_id: string;
  
  // Personality (with evolution)
  baseline_personality: PersonalityTraits;
  current_personality: PersonalityTraits;
  personality_evolution: PersonalityChange[];
  
  // Core identity (immutable)
  core_traits: string[];
  voice_characteristics: string[];
  
  // Current state
  current_emotional_state: EmotionalState;
  current_location?: LocationID;
  current_activities: CardID[];
  
  // Knowledge
  knows_about: string[];
  unaware_of: string[];
}

interface WorldState {
  current_week: Week;
  season_number: number;
  
  // World facts
  locations_exist: LocationID[];
  npcs_known: NPCID[];
  events_occurred: string[];
  
  // Player state
  player_occupation: string;
  player_living_situation: string;
  player_financial_state: "struggling" | "stable" | "comfortable" | "wealthy";
  
  // Season-specific
  ongoing_situations: string[];
  unresolved_conflicts: string[];
}

interface RelationshipHistory {
  relationship_id: string;
  
  // Timeline
  first_met: Week;
  milestones: RelationshipMoment[];
  current_status: Relationship;
  
  // Knowledge
  shared_secrets: string[];
  unresolved_issues: string[];
  
  // Consistency
  established_dynamics: string[];
  cannot_contradict: string[];
}
```

### Narrative Coherence Rules

```typescript
/**
 * Rules for maintaining narrative coherence
 */
interface NarrativeCoherenceRules {
  // Character consistency
  characters_dont_forget_major_events: boolean;
  personality_changes_are_gradual: boolean;
  relationships_evolve_logically: boolean;
  
  // Causality
  effects_have_causes: boolean;
  setup_payoff_tracking: boolean;
  decisions_have_consequences: boolean;
  
  // Timeline
  events_in_chronological_order: boolean;
  time_passage_feels_realistic: boolean;
  seasonal_changes_reflected: boolean;
  
  // Emotional
  emotional_changes_are_motivated: boolean;
  crisis_has_buildup: boolean;
  triumph_is_earned: boolean;
  
  // Thematic
  themes_are_consistent: boolean;
  callbacks_reference_real_events: boolean;
  foreshadowing_pays_off: boolean;
}
```

---

## Notes for LLM Analysis

When validating narrative system schemas:

1. **Arc Phases**: Phase numbers sequential, week ranges non-overlapping
2. **Decisive Decisions**: Always LifeDefining weight, creates memory
3. **Timeline**: Events in chronological order, no time paradoxes
4. **Memory References**: All memory_ids must exist
5. **Character Consistency**: Personality changes tracked with triggers
6. **Relationship History**: Trust levels consistent with moments
7. **Season Structure**: Acts cover full season, no gaps
8. **Continuity**: Established facts never contradicted

**Cross-schema dependencies**:
- CardID from card-system (all cards referenced must exist)
- NPCID from character-system (all NPCs must be defined)
- EmotionalState from emotional-system (all states valid)
- LocationID from gameplay-mechanics (all locations exist)
- PersonalityTraits from character-system (all in valid ranges)
- Memory formation affects novel-generation chapter data
- Timeline events must respect gameplay turn structure
- Arc progression must respect season boundaries

