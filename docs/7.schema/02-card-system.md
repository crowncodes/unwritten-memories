# Card System Schema

**Schema Version**: 1.0.0  
**Last Updated**: 2025-10-13  
**Dependencies**: `01-core-types.md`

---

## Overview

Defines all data structures for the Unwritten card system including the 7-tier taxonomy, card evolution, fusion, and hand management.

---

## 1. Base Card Structure

### Core Card Interface

```typescript
/**
 * Base card that all other cards extend
 */
interface BaseCard {
  // Identity
  card_id: CardID;
  title: string;
  description: string;
  
  // Classification
  tier: CardTier;
  category: CardCategory;
  subcategory?: string;
  rarity: CardRarity;
  
  // State
  state: CardState;
  evolution_level: number;        // 0 = base, 1-5 = evolved levels
  uses: number;                   // How many times played
  
  // Costs & Requirements
  costs: ResourceCost;
  requirements?: CardRequirements;
  
  // Effects
  effects: CardEffect[];
  success_chance?: SuccessChance;
  
  // Metadata
  tags: string[];
  unlocked_at?: Week;
  first_played_at?: GameTime;
  pack_id?: PackID;               // If from expansion pack
  
  // Relationships
  parent_card_id?: CardID;        // For evolved/fusion cards
  generated_from_aspiration?: AspirationID;
  
  // Versioning
  schema_version: SemanticVersion;
  created_at: ISO8601String;
  updated_at: ISO8601String;
}

/**
 * Card categories
 */
type CardCategory =
  | "life_direction"
  | "phase_transition"
  | "major_aspiration"
  | "minor_aspiration"
  | "routine"
  | "obligation"
  | "scheduled_event"
  | "milestone"
  | "repeatable_quest"
  | "social_activity"
  | "solo_activity"
  | "exploration"
  | "challenge"
  | "npc_initiated"
  | "random_event"
  | "crisis"
  | "breakthrough"
  | "skill"
  | "item"
  | "perk"
  | "memory";

/**
 * Card state
 */
enum CardState {
  Locked = "locked",              // Not yet unlocked
  Available = "available",        // Can be played
  InHand = "in_hand",            // Currently in player's hand
  Playing = "playing",           // Being resolved
  Cooldown = "cooldown",         // Temporarily unavailable
  Exhausted = "exhausted",       // Used up (one-time cards)
  Archived = "archived"          // Stored in archive
}
```

### Card Requirements

```typescript
/**
 * Requirements to play a card
 */
interface CardRequirements {
  // Resource requirements
  min_energy?: Energy;
  min_money?: MoneyAmount;
  min_time_available?: number;   // Hours
  
  // Stat requirements
  min_meters?: Partial<Meters>;
  min_skills?: Record<SkillID, number>;
  
  // State requirements
  required_emotional_states?: EmotionalState[];
  forbidden_emotional_states?: EmotionalState[];
  
  // Relationship requirements
  required_npc_trust?: Record<NPCID, Trust>;
  required_npc_present?: NPCID[];
  
  // World state requirements
  required_location?: LocationID;
  required_time_of_day?: TimeOfDay[];
  required_day_of_week?: DayOfWeek[];
  
  // Progression requirements
  min_week?: Week;
  max_week?: Week;
  required_cards_played?: CardID[];
  required_aspirations_active?: AspirationID[];
  
  // Other requirements
  required_packs?: PackID[];
  required_tier?: "free" | "premium";
}
```

### Card Effects

```typescript
/**
 * Effect that occurs when card is played
 */
interface CardEffect {
  effect_id: string;
  type: CardEffectType;
  target: EffectTarget;
  value: EffectValue;
  duration?: Duration;
  conditions?: EffectCondition[];
}

enum CardEffectType {
  // Meter effects
  ModifyMeter = "modify_meter",
  RestoreMeter = "restore_meter",
  DrainMeter = "drain_meter",
  
  // Resource effects
  ModifyMoney = "modify_money",
  ModifyEnergy = "modify_energy",
  ModifySocialCapital = "modify_social_capital",
  
  // Relationship effects
  ModifyTrust = "modify_trust",
  ModifyAttraction = "modify_attraction",
  
  // State effects
  ChangeEmotionalState = "change_emotional_state",
  ApplyBuff = "apply_buff",
  ApplyDebuff = "apply_debuff",
  
  // Progression effects
  UnlockCard = "unlock_card",
  UnlockLocation = "unlock_location",
  UnlockNPC = "unlock_npc",
  ProgressAspiration = "progress_aspiration",
  
  // Personality effects
  ShiftPersonality = "shift_personality",
  ImproveSkill = "improve_skill",
  
  // Narrative effects
  TriggerEvent = "trigger_event",
  CreateMemory = "create_memory",
  StartStoryArc = "start_story_arc"
}

interface EffectTarget {
  type: "player" | "npc" | "world" | "aspiration" | "card";
  target_id?: string;              // Specific NPC/card/etc
}

type EffectValue = 
  | number 
  | string 
  | { min: number; max: number } 
  | Record<string, any>;

interface EffectCondition {
  type: "meter_above" | "meter_below" | "has_skill" | "npc_present" | "emotional_state";
  value: any;
  required: boolean;
}
```

---

## 2. Tier-Specific Card Types

### Tier 1: Foundation Cards

```typescript
/**
 * Life Direction Card (Tier 1A)
 */
interface LifeDirectionCard extends BaseCard {
  tier: CardTier.Foundation;
  category: "life_direction";
  
  // Life direction properties
  direction_name: LifeDirection;
  deck_composition_shifts: DeckCompositionShift[];
  unlocked_aspirations: AspirationID[];
  unlocked_locations: LocationID[];
  unlocked_npcs: NPCID[];
  personality_compatibility: PersonalityCompatibility;
  commitment_duration: Duration;    // Typically 12-48 weeks
}

type LifeDirection =
  | "pursue_creative_fulfillment"
  | "achieve_financial_security"
  | "seek_deep_relationships"
  | "find_personal_freedom"
  | "build_family_legacy"
  | "master_a_craft"
  | "make_social_impact"
  | "discover_who_you_are"
  | "balance_everything";

interface DeckCompositionShift {
  card_category: CardCategory;
  weight_multiplier: number;        // 0.5 = half as common, 2.0 = twice as common
  reason: string;
}

interface PersonalityCompatibility {
  compatible_traits: Partial<PersonalityTraits>;
  difficulty_modifiers: {
    high_neuroticism?: number;
    low_openness?: number;
    // etc
  };
}

/**
 * Phase Transition Card (Tier 1B)
 */
interface PhaseTransitionCard extends BaseCard {
  tier: CardTier.Foundation;
  category: "phase_transition";
  
  // Crisis properties
  transition_type: PhaseTransitionType;
  trigger_conditions: TransitionTrigger[];
  mandatory: boolean;               // Cannot skip
  life_direction_choices: LifeDirection[];
  consequences: PhaseConsequence[];
}

type PhaseTransitionType =
  | "major_breakup"
  | "career_devastation"
  | "health_crisis"
  | "loss_of_loved_one"
  | "financial_catastrophe"
  | "achievement_peak"
  | "existential_crisis"
  | "unexpected_opportunity";

interface TransitionTrigger {
  condition: string;
  threshold?: number;
  duration?: Duration;
}

interface PhaseConsequence {
  type: "aspiration_cancel" | "relationship_shift" | "deck_reset" | "personality_shift";
  details: any;
  reversible: boolean;
}
```

### Tier 2: Aspiration Cards

```typescript
/**
 * Major Aspiration Card (Tier 2A)
 */
interface MajorAspirationCard extends BaseCard {
  tier: CardTier.Aspiration;
  category: "major_aspiration";
  
  // Aspiration properties
  aspiration_id: AspirationID;
  duration: Duration;               // 8-16 weeks typical
  difficulty: Difficulty;
  success_rate: Probability;
  
  // Requirements
  requirements_list: AspriationRequirement[];
  generated_quest_cards: CardID[]; // Dynamically generated
  
  // Milestones
  milestones: MilestoneDefinition[];
  
  // Outcomes
  success_rewards: AspirationReward;
  failure_consequences: AspirationFailure;
  can_fail: boolean;
  max_simultaneous: number;         // Max active at once (typically 2)
}

type Difficulty = "easy" | "moderate" | "hard" | "very_hard" | "extreme";

interface AspriationRequirement {
  requirement_id: string;
  description: string;
  completion_criteria: CompletionCriteria;
  optional: boolean;
}

interface CompletionCriteria {
  type: "play_card_n_times" | "reach_value" | "time_passes" | "event_occurs";
  target_value?: number;
  card_ids?: CardID[];
  event_type?: EventType;
}

interface MilestoneDefinition {
  milestone_id: string;
  title: string;
  week_target: Week;
  requirements: string[];
  generates_card: boolean;
  card_template?: CardID;
}

interface AspirationReward {
  fusion_card?: FusionID;
  meter_changes: Partial<Meters>;
  skill_improvements: Record<SkillID, number>;
  unlocked_cards: CardID[];
  unlocked_npcs: NPCID[];
  memory_weight: Intensity;
}

interface AspirationFailure {
  meter_penalty: Partial<Meters>;
  emotional_impact: EmotionalState;
  relationship_impacts: Record<NPCID, number>;
  resources_lost: ResourceCost;
  creates_memory: boolean;
}

/**
 * Minor Aspiration Card (Tier 2B)
 */
interface MinorAspirationCard extends Omit<MajorAspirationCard, 'tier' | 'category'> {
  tier: CardTier.Aspiration;
  category: "minor_aspiration";
  
  // Simplified for minor aspirations
  duration: Duration;               // 4-12 weeks
  success_rate: Probability;        // 60-85% (more achievable)
  low_stakes: boolean;              // Failure = minor disappointment
}
```

### Tier 3: Structure Cards

```typescript
/**
 * Routine Card (Tier 3A)
 */
interface RoutineCard extends BaseCard {
  tier: CardTier.Structure;
  category: "routine";
  
  // Routine properties
  original_card_id: CardID;         // The activity that became routine
  times_performed: number;          // How many times repeated
  established_week: Week;           // When it became routine
  
  // Routine behavior
  auto_resolve: boolean;            // Can be batch-processed
  batch_duration?: Duration;        // "This week" or "Next 3 days"
  
  // Breaking routine
  break_cost: ResourceCost;         // Cost to break routine
  personality_resistance: {         // How hard to break based on personality
    high_conscientiousness: number;
    low_openness: number;
  };
  
  // Evolution stages
  evolution_stage: RoutineEvolutionStage;
}

enum RoutineEvolutionStage {
  Emerging = 1,        // Uses 1-5
  Established = 2,     // Uses 6-15
  Tradition = 3,       // Uses 16-30
  Legendary = 4        // Uses 31+
}

/**
 * Obligation Card (Tier 3B)
 */
interface ObligationCard extends BaseCard {
  tier: CardTier.Structure;
  category: "obligation";
  
  // Obligation properties
  obligation_type: ObligationType;
  frequency: Frequency;
  mandatory: boolean;               // Cannot skip without consequences
  
  // Requirements
  minimum_allocation: ResourceCost;
  quality_tiers: QualityTier[];
  
  // Skip consequences
  skip_consequences: ObligationConsequence[];
}

type ObligationType = 
  | "work_hours" 
  | "rent_payment" 
  | "bills" 
  | "sleep" 
  | "meals" 
  | "family_obligation";

interface Frequency {
  interval: "daily" | "weekly" | "monthly";
  occurrences_per_interval: number;
}

interface QualityTier {
  tier_name: string;                // "Minimum Viable", "Good Work", "Excellence"
  resources_required: ResourceCost;
  outcomes: CardEffect[];
}

interface ObligationConsequence {
  consequence_type: "meter_penalty" | "relationship_damage" | "resource_loss" | "crisis_trigger";
  severity: Intensity;
  description: string;
}

/**
 * Scheduled Event Card (Tier 3C)
 */
interface ScheduledEventCard extends BaseCard {
  tier: CardTier.Structure;
  category: "scheduled_event";
  
  // Event properties
  scheduled_time: GameTime;
  rsvp_status: "accepted" | "declined" | "maybe" | "pending";
  commitment_locked: boolean;       // Can't cancel without cost
  
  // Event details
  location: LocationID;
  attendees: NPCID[];
  duration: Duration;
  
  // Cancellation
  cancellation_cost: CancellationCost;
}

interface CancellationCost extends ResourceCost {
  relationship_penalty: Record<NPCID, number>;
  reputation_impact: string;
  guilt_level: Intensity;
}
```

### Tier 4: Quest Chain Cards

```typescript
/**
 * Milestone Card (Tier 4A)
 */
interface MilestoneCard extends BaseCard {
  tier: CardTier.Quest;
  category: "milestone";
  
  // Milestone properties
  parent_aspiration: AspirationID;
  milestone_number: number;         // e.g., 3 of 5
  week_target: Week;
  
  // Readiness
  readiness_criteria: ReadinessCriteria;
  success_chance: SuccessChance;
  
  // Outcome branches
  success_outcome: MilestoneOutcome;
  partial_success_outcome?: MilestoneOutcome;
  failure_outcome: MilestoneOutcome;
  
  // Dramatic weight
  is_climax: boolean;               // Is this the aspiration climax?
  emotional_weight: Intensity;
}

interface ReadinessCriteria {
  required_progress: {
    quest_cards_completed: number;
    weeks_progressed: number;
    skills_acquired: Record<SkillID, number>;
  };
  current_status: "ready" | "not_ready" | "overdue";
}

interface MilestoneOutcome {
  arc_progression: "advance" | "maintain" | "regress" | "terminate";
  emotional_state_shift: EmotionalState;
  unlocked_cards?: CardID[];
  generates_memory: boolean;
}

/**
 * Repeatable Quest Card (Tier 4B)
 */
interface RepeatableQuestCard extends BaseCard {
  tier: CardTier.Quest;
  category: "repeatable_quest";
  
  // Repeatable properties
  parent_aspiration: AspirationID;
  times_completed: number;
  progress_per_completion: number;  // % toward aspiration
  
  // Routine conversion
  becomes_routine_after: number;    // After 3 weeks typically
  routine_card_id?: CardID;         // If converted to routine
  
  // Variance
  success_variance: {
    min_progress: number;
    max_progress: number;
    difficulty_factors: string[];
  };
}
```

### Tier 5: Activity Cards

```typescript
/**
 * Social Activity Card (Tier 5A)
 */
interface SocialActivityCard extends BaseCard {
  tier: CardTier.Activity;
  category: "social_activity";
  
  // Social properties
  participants: NPCID[];
  activity_type: SocialActivityType;
  intimacy_level: Intensity;        // 1 = casual, 10 = deeply personal
  
  // Conversation
  conversation_depth: ConversationDepth;
  dialogue_options: DialogueOption[];
  
  // Fusion opportunities
  fusion_conditions: FusionCondition[];
  
  // Evolution
  evolution_tracking: {
    times_with_this_npc: Record<NPCID, number>;
    landmark_moments: LandmarkMoment[];
  };
}

type SocialActivityType = 
  | "one_on_one" 
  | "group" 
  | "family" 
  | "romantic" 
  | "professional";

enum ConversationDepth {
  Surface = 1,        // "How's it going?"
  Pleasant = 2,       // Safe, comfortable topics
  Meaningful = 3,     // Sharing real thoughts
  Vulnerable = 4,     // Opening up deeply
  Transformative = 5  // Life-changing conversation
}

interface DialogueOption {
  option_id: string;
  text: string;
  depth: ConversationDepth;
  risk_level: Intensity;
  potential_outcomes: DialogueOutcome[];
}

interface DialogueOutcome {
  outcome_type: "bond_deepens" | "conflict" | "revelation" | "friendship_level_up";
  relationship_delta: number;
  trust_delta: number;
  attraction_delta?: number;
  unlocks?: string[];
}

interface LandmarkMoment {
  week: Week;
  description: string;
  significance: string;
  emotional_weight: Intensity;
}

/**
 * Solo Activity Card (Tier 5B)
 */
interface SoloActivityCard extends BaseCard {
  tier: CardTier.Activity;
  category: "solo_activity";
  
  // Solo properties
  activity_type: SoloActivityType;
  restoration_type: "physical" | "mental" | "emotional" | "practical";
  
  // Self-care vs development
  purpose: "restore" | "develop" | "maintain" | "explore";
  
  // Personality alignment
  personality_fit: Partial<PersonalityTraits>;
  introvert_appeal: number;         // Higher for introverts
}

type SoloActivityType =
  | "physical_exercise"
  | "reading"
  | "creative_work"
  | "meditation"
  | "journaling"
  | "skill_practice"
  | "entertainment"
  | "rest";

/**
 * Exploration Card (Tier 5C)
 */
interface ExplorationCard extends BaseCard {
  tier: CardTier.Activity;
  category: "exploration";
  
  // Exploration properties
  novelty_level: Intensity;         // How new/unfamiliar
  openness_requirement: Personality; // Min openness for comfort
  
  // Discovery potential
  unlockable_content: UnlockableContent[];
  new_npc_chance: Probability;
  new_location_chance: Probability;
  
  // Risk
  comfort_risk: RangedInt<0, 5>;
  social_anxiety_factor: number;
}

interface UnlockableContent {
  content_type: "npc" | "location" | "activity" | "story_arc";
  content_id: string;
  unlock_chance: Probability;
  requirements?: CardRequirements;
}

/**
 * Challenge Card (Tier 5D)
 */
interface ChallengeCard extends BaseCard {
  tier: CardTier.Activity;
  category: "challenge";
  
  // Challenge properties
  risk_level: Intensity;
  personality_fit: Personality;     // How well aligned with personality
  success_chance: SuccessChance;
  
  // Outside comfort zone
  comfort_stretch: RangedInt<1, 5>; // How far outside comfort
  
  // High risk, high reward
  success_rewards: ChallengeReward;
  failure_consequences: ChallengeFailure;
  disaster_chance: Probability;     // Chance of catastrophic failure
}

interface ChallengeReward {
  personality_growth: Partial<PersonalityTraits>;
  emotional_boost: number;
  skill_improvements: Record<SkillID, number>;
  unlocked_confidence: string[];
  creates_landmark_memory: boolean;
}

interface ChallengeFailure {
  emotional_cost: number;
  recovery_time: Duration;
  lesson_learned?: string;
  still_gains_courage_points: boolean;
}
```

### Tier 6: Event Cards

```typescript
/**
 * NPC-Initiated Card (Tier 6A)
 */
interface NPCInitiatedCard extends BaseCard {
  tier: CardTier.Event;
  category: "npc_initiated";
  
  // NPC properties
  initiating_npc: NPCID;
  request_type: NPCRequestType;
  urgency: "immediate" | "soon" | "flexible";
  
  // Relationship context
  relationship_test: boolean;       // Is this testing the relationship?
  social_capital_cost: SocialCapital;
  
  // Conflicts
  conflicts_with?: CardID[];        // Other scheduled cards
  
  // Response options
  response_options: NPCResponseOption[];
}

type NPCRequestType =
  | "help_request"
  | "invitation"
  | "confrontation"
  | "revelation"
  | "crisis_support";

interface NPCResponseOption {
  option_id: string;
  response_type: "accept" | "decline" | "negotiate" | "defer";
  relationship_impact: number;
  trust_impact: number;
  consequences: string[];
}

/**
 * Random Event Card (Tier 6B)
 */
interface RandomEventCard extends BaseCard {
  tier: CardTier.Event;
  category: "random_event";
  
  // Random event properties
  event_type: RandomEventType;
  spawn_chance: Probability;        // 5-10% per turn typical
  time_sensitive: boolean;
  expiration: Duration;
  
  // Chaos factor
  disruption_level: Intensity;
  opportunity_vs_disruption: "opportunity" | "disruption" | "choice";
  
  // Narrative seed
  story_seed: boolean;              // Can start new storyline
}

type RandomEventType =
  | "opportunity"
  | "disruption"
  | "choice"
  | "discovery";

/**
 * Crisis Card (Tier 6C)
 */
interface CrisisCard extends BaseCard {
  tier: CardTier.Event;
  category: "crisis";
  
  // Crisis properties
  trigger_type: CrisisTriggerType;
  severity: Intensity;
  forced: boolean;                  // Cannot skip
  
  // Cause
  caused_by: CrisisCause;
  
  // Resolution
  resolution_options: CrisisResolution[];
  recovery_path: RecoveryPath;
  
  // Long-term impact
  permanent_effects: CardEffect[];
  may_trigger_phase_transition: boolean;
}

type CrisisTriggerType =
  | "meter_critical_low"
  | "meter_critical_high"
  | "neglect_accumulated"
  | "relationship_breakdown"
  | "financial_collapse"
  | "health_emergency";

interface CrisisCause {
  meters: Partial<Meters>;
  weeks_of_neglect?: number;
  triggering_event?: CardID;
  warning_signs_missed: string[];
}

interface CrisisResolution {
  resolution_id: string;
  approach: string;
  success_chance: Probability;
  short_term_cost: ResourceCost;
  long_term_benefit: string;
}

interface RecoveryPath {
  min_duration: Duration;
  recovery_milestones: string[];
  support_needed: NPCID[];
}

/**
 * Breakthrough Card (Tier 6D)
 */
interface BreakthroughCard extends BaseCard {
  tier: CardTier.Event;
  category: "breakthrough";
  
  // Breakthrough properties
  trigger_conditions: BreakthroughTrigger;
  rarity: "rare";                   // Breakthroughs are always rare
  
  // Rewards
  breakthrough_type: BreakthroughType;
  benefits: BreakthroughBenefit[];
  
  // Flow state
  flow_duration: Duration;
  enhanced_performance: Record<string, number>;
}

type BreakthroughType =
  | "flow_state"
  | "balanced"
  | "peak_performance"
  | "revelation"
  | "mastery";

interface BreakthroughTrigger {
  meters_balanced: boolean;         // All meters 5-7
  duration_maintained: Duration;    // How long balanced
  no_crisis_for: Duration;
}

interface BreakthroughBenefit {
  benefit_type: "success_boost" | "energy_reduction" | "unlock" | "fusion";
  value: any;
  duration: Duration;
}
```

### Tier 7: System Cards

```typescript
/**
 * Skill Card (Tier 7A)
 */
interface SkillCard extends BaseCard {
  tier: CardTier.System;
  category: "skill";
  
  // Skill properties
  skill_id: SkillID;
  skill_name: string;
  skill_level: RangedInt<1, 10>;
  
  // Progression
  experience_points: number;
  xp_to_next_level: number;
  unlocked_by: string;              // What action unlocked it
  times_practiced: number;
  
  // Effects
  current_effects: SkillEffect[];
  level_up_rewards: SkillLevelReward[];
  
  // Application
  applies_to_cards: CardCategory[];
  success_chance_bonus: Percentage;
}

interface SkillEffect {
  effect_description: string;
  applies_when: string;
  bonus_value: number;
}

interface SkillLevelReward {
  at_level: number;
  unlocks: string[];
  bonus_effects: CardEffect[];
}

/**
 * Item/Possession Card (Tier 7B)
 */
interface ItemCard extends BaseCard {
  tier: CardTier.System;
  category: "item";
  
  // Item properties
  item_type: ItemType;
  purchase_cost: MoneyAmount;
  monthly_cost?: MoneyAmount;       // Ongoing costs
  
  // Benefits
  passive_bonuses: CardEffect[];
  unlocked_activities: CardID[];
  
  // Fusion potential
  enables_fusions: FusionID[];
  
  // Lifecycle
  depreciates: boolean;
  sell_value?: MoneyAmount;
  can_lose: boolean;
}

type ItemType =
  | "transportation"
  | "equipment"
  | "access"
  | "collectible";

/**
 * Perk/Trait Card (Tier 7C)
 */
interface PerkCard extends BaseCard {
  tier: CardTier.System;
  category: "perk";
  
  // Perk properties
  perk_type: "positive" | "negative";
  earned_by: string;                // How was it earned
  
  // Effects
  persistent_effects: CardEffect[];
  personality_marker: boolean;      // Reflects personality
  
  // Story impact
  affects_npc_dialogue: boolean;
  affects_ai_generation: boolean;
  
  // Removal
  permanent: boolean;
  removal_requirements?: string[];
}

/**
 * Memory Card (Tier 7D)
 */
interface MemoryCard extends BaseCard {
  tier: CardTier.System;
  category: "memory";
  
  // Memory properties
  memory_id: MemoryID;
  memory_type: MemoryType;
  emotional_weight: Intensity;      // 1-10
  
  // Content
  event_week: Week;
  description: string;
  characters_present: NPCID[];
  location: LocationID;
  
  // Sensory
  sensory_details: SensorySnapshot;
  
  // Fusion
  fusion_result?: FusionID;
  cards_involved: CardID[];
  
  // Archive
  archive_significance: ArchiveSignificance;
  appears_in_book: boolean;
  book_chapter?: number;
  
  // View-only
  readonly: true;                   // Cannot be played, only viewed
}

type MemoryType =
  | "landmark"
  | "turning_point"
  | "peak_moment"
  | "failure"
  | "fusion"
  | "relationship_milestone"
  | "achievement";

enum ArchiveSignificance {
  Minor = 1,
  Significant = 2,
  Major = 3,
  Climax = 4,
  Legendary = 5
}
```

---

## 3. Card Evolution System

### Evolution Tracking

```typescript
/**
 * Card evolution state
 */
interface CardEvolution {
  card_id: CardID;
  base_card_id: CardID;             // Original template
  evolution_level: number;          // 0-5
  evolution_history: EvolutionEvent[];
  
  // Personalization
  ai_generated_content: AIGeneratedContent;
  player_specific: boolean;
  unique_to_playthrough: boolean;
}

interface EvolutionEvent {
  event_id: string;
  occurred_at: GameTime;
  trigger: EvolutionTrigger;
  changes: EvolutionChange[];
}

interface EvolutionTrigger {
  trigger_type: "usage_count" | "relationship_milestone" | "time_passed" | "event_occurred";
  threshold?: number;
  context: string;
}

interface EvolutionChange {
  property: string;
  old_value: any;
  new_value: any;
  reason: string;
}

/**
 * AI-generated personalization
 */
interface AIGeneratedContent {
  generated_at: ISO8601String;
  ai_model: string;
  context_used: AIContext;
  
  // Generated content
  personalized_title?: string;
  personalized_description?: string;
  personalized_image?: URL;
  personalized_dialogue?: string[];
  
  // Validation
  approved: boolean;
  human_reviewed: boolean;
}

interface AIContext {
  player_personality: PersonalityTraits;
  player_emotional_state: EmotionalState;
  player_life_direction: LifeDirection;
  relationship_context: Record<NPCID, Trust>;
  interaction_history: string[];
}
```

### Evolution Templates

```typescript
/**
 * Evolution stage definition
 */
interface EvolutionStage {
  stage_number: number;
  stage_name: string;
  unlock_threshold: EvolutionThreshold;
  
  // Changes at this stage
  title_template: string;
  description_template: string;
  effect_bonuses: CardEffect[];
  new_properties: Record<string, any>;
  
  // AI generation params
  ai_generation_prompt?: string;
}

interface EvolutionThreshold {
  uses_min?: number;
  relationship_level_min?: number;
  weeks_known_min?: number;
  combined_criteria?: EvolutionThreshold[];
}

/**
 * Example: Character card evolution stages
 */
const CHARACTER_EVOLUTION_STAGES: EvolutionStage[] = [
  {
    stage_number: 1,
    stage_name: "First Meeting",
    unlock_threshold: { uses_min: 1 },
    title_template: "{name}",
    description_template: "You just met {name}. {initial_impression}",
    effect_bonuses: [],
    new_properties: {}
  },
  {
    stage_number: 2,
    stage_name: "Acquaintance",
    unlock_threshold: { uses_min: 3 },
    title_template: "{name}",
    description_template: "{name}, {occupation}. {personality_glimpse}",
    effect_bonuses: [],
    new_properties: { conversation_depth: 2 }
  },
  {
    stage_number: 3,
    stage_name: "Friend",
    unlock_threshold: { uses_min: 10, relationship_level_min: 0.6 },
    title_template: "{name} (Friend)",
    description_template: "{name} trusts you. {shared_history}",
    effect_bonuses: [
      { type: "unlock_card", target: { type: "card" }, value: "deep_conversation" }
    ],
    new_properties: { conversation_depth: 4 }
  }
  // ... stages 4-5
];
```

---

## 4. Fusion System

### Fusion Structure

```typescript
/**
 * Fusion card - created by combining cards
 */
interface FusionCard extends BaseCard {
  // Fusion metadata
  fusion_id: FusionID;
  fusion_type: FusionType;
  rarity: CardRarity;               // Based on complexity
  
  // Source cards
  source_cards: CardID[];
  fusion_conditions_met: FusionCondition[];
  
  // Fusion properties
  fusion_result_type: FusionResultType;
  symbolic_meaning: string;
  narrative_significance: string;
  
  // Effects
  combined_effects: CardEffect[];
  bonus_effects: CardEffect[];      // Beyond sum of parts
  
  // Memory
  origin_story: FusionOriginStory;
  creates_permanent_memory: boolean;
  
  // State
  permanent: boolean;               // Cannot be unfused
  appears_in_deck: boolean;
}

type FusionType =
  | "simple_2card"
  | "complex_3card"
  | "legendary_4plus"
  | "temporal"                      // Time-based
  | "compound";                     // Fusion of fusions

type FusionResultType =
  | "personalized_memory"
  | "colored_interaction"
  | "signature_experience"
  | "mastery_variant"
  | "perfect_moment"
  | "life_integration"
  | "group_dynamic"
  | "life_defining";

/**
 * Fusion conditions
 */
interface FusionCondition {
  condition_id: string;
  condition_type: FusionConditionType;
  requirement: any;
  met: boolean;
}

enum FusionConditionType {
  CardsPlayedTogether = "cards_played_together",
  RepetitionCount = "repetition_count",
  EmotionalStateMatch = "emotional_state_match",
  RelationshipLevel = "relationship_level",
  MilestoneAchieved = "milestone_achieved",
  TemporalAlignment = "temporal_alignment",
  ContextualMatch = "contextual_match"
}

/**
 * Fusion origin story
 */
interface FusionOriginStory {
  when_created: GameTime;
  how_created: string;
  why_significant: string;
  emotional_moment: string;
  participants: NPCID[];
}
```

### Fusion Templates

```typescript
/**
 * Fusion template - defines possible fusions
 */
interface FusionTemplate {
  template_id: string;
  template_name: string;
  
  // Requirements
  required_card_categories: CardCategory[];
  required_card_count: number;
  additional_conditions: FusionCondition[];
  
  // Result
  result_fusion_type: FusionResultType;
  result_rarity: CardRarity;
  
  // AI generation
  ai_generation_params: {
    prompt_template: string;
    context_requirements: string[];
    personalization_level: "low" | "medium" | "high";
  };
}

/**
 * Example fusion templates
 */
const FUSION_TEMPLATES: FusionTemplate[] = [
  {
    template_id: "fusion_character_location",
    template_name: "Character + Location = Ritual",
    required_card_categories: ["social_activity", "solo_activity"],
    required_card_count: 2,
    additional_conditions: [
      { 
        condition_type: FusionConditionType.RepetitionCount, 
        requirement: 5,
        met: false
      }
    ],
    result_fusion_type: "signature_experience",
    result_rarity: "common",
    ai_generation_params: {
      prompt_template: "Create a ritual/routine name for {character} + {location} after {count} visits",
      context_requirements: ["character_personality", "location_atmosphere"],
      personalization_level: "medium"
    }
  },
  // ... more templates
];
```

---

## 5. Hand & Deck Management

### Hand Structure

```typescript
/**
 * Player's current hand of cards
 */
interface PlayerHand {
  hand_id: string;
  game_time: GameTime;
  
  // Cards
  cards: CardID[];
  max_hand_size: number;            // Typically 8
  
  // Draw context
  drawn_for_emotional_state: EmotionalState;
  draw_filters_applied: DrawFilter[];
  
  // State
  locked: boolean;                  // During card resolution
  expires_at?: GameTime;            // When hand refreshes
}

/**
 * Deck composition at a point in time
 */
interface DeckState {
  total_cards: number;
  available_cards: CardID[];
  locked_cards: CardID[];           // Not yet unlocked
  exhausted_cards: CardID[];        // One-time cards used
  cooldown_cards: CardID[];         // Temporarily unavailable
  
  // Composition
  cards_by_tier: Record<CardTier, CardID[]>;
  cards_by_category: Record<CardCategory, CardID[]>;
  cards_by_rarity: Record<CardRarity, CardID[]>;
  
  // Stats
  total_cards_ever: number;
  total_evolved: number;
  total_fusions: number;
}
```

### Card Drawing System

```typescript
/**
 * Card draw algorithm parameters
 */
interface DrawParameters {
  hand_size: number;
  emotional_state: EmotionalState;
  personality_filters: PersonalityTraits;
  life_direction_weights: DeckCompositionShift[];
  active_aspirations: AspirationID[];
  time_context: GameTime;
  
  // Constraints
  min_obligations: number;          // Must include obligations
  max_repetition: number;           // Don't draw same card too often
  force_include?: CardID[];         // Must include these
  exclude?: CardID[];               // Cannot include these
}

/**
 * Draw filter applied
 */
interface DrawFilter {
  filter_type: DrawFilterType;
  weight_multiplier: number;
  reason: string;
  applies_to_categories: CardCategory[];
}

enum DrawFilterType {
  EmotionalStateAppeal = "emotional_state_appeal",
  PersonalityAlignment = "personality_alignment",
  LifeDirectionWeight = "life_direction_weight",
  AspirationGenerated = "aspiration_generated",
  ProgressionGated = "progression_gated",
  PackOwnership = "pack_ownership"
}

/**
 * Card appeal calculation
 */
interface CardAppeal {
  card_id: CardID;
  base_appeal: number;              // 0.0-1.0
  emotional_state_modifier: number; // -0.5 to +2.0
  personality_modifier: number;     // -0.3 to +0.3
  life_direction_modifier: number;  // 0.5 to 3.0
  final_appeal: number;
  draw_probability: Probability;
}
```

---

## Notes for LLM Analysis

When validating card system schemas:

1. **ID Consistency**: All `card_id` fields match pattern from core-types
2. **Tier Hierarchy**: Card tiers 1-7 properly categorized
3. **Effect Types**: All `CardEffectType` values are defined in enum
4. **Resource Costs**: Use `ResourceCost` interface from core-types
5. **Time References**: Use `GameTime` or `Week` consistently
6. **Relationships**: NPC IDs reference character system
7. **Evolution**: Evolution levels 0-5, proper triggers defined
8. **Fusion**: Source cards must exist, conditions properly defined
9. **Enums**: All enum values used in cards are defined
10. **Requirements**: Card requirements use proper types from core-types

**Cross-schema dependencies**:
- NPCs referenced must exist in character-system
- Locations referenced must exist in gameplay-mechanics
- Skills referenced must have definitions
- Aspirations generate quest cards properly
- Memory cards link to archive-persistence
- Fusion conditions validated against gameplay state

