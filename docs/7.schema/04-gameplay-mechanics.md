# Gameplay Mechanics Schema

**Schema Version**: 1.0.0  
**Last Updated**: 2025-10-13  
**Dependencies**: `01-core-types.md`, `02-card-system.md`, `03-character-system.md`

---

## Overview

Defines resources, turn structure, meters, decision-making, success calculations, and core gameplay loops.

---

## 1. Resources

### Core Resource Types

```typescript
/**
 * All player resources (defined in detail)
 */
interface PlayerResources {
  // Primary resources
  energy: ResourceState<Energy>;
  money: MoneyState;
  social_capital: SocialCapitalState;
  time: TimeState;
  
  // Secondary resources
  comfort: ResourceState<RangedInt<0, 10>>;
  success_momentum: ResourceState<RangedInt<0, 10>>;
  
  // Derived states
  resource_pressure: ResourcePressure;
  at_risk_resources: string[];
}

/**
 * Generic resource state
 */
interface ResourceState<T> {
  current: T;
  maximum: T;
  minimum: T;
  
  // Regeneration
  regeneration_rate?: number;
  regeneration_interval?: Duration;
  next_regeneration?: GameTime;
  
  // Modifiers
  temporary_modifiers: ResourceModifier[];
  permanent_modifiers: ResourceModifier[];
  
  // State
  depleted: boolean;
  critical_low: boolean;
  critical_high: boolean;
}

interface ResourceModifier {
  modifier_id: string;
  source: string;
  modifier_type: "additive" | "multiplicative";
  value: number;
  duration?: Duration;
  expires_at?: GameTime;
  reason: string;
}
```

### Energy System

```typescript
/**
 * Energy resource (primary gameplay resource)
 */
interface EnergyState extends ResourceState<Energy> {
  current: Energy;
  maximum: 8;                       // Base max
  per_turn_regen: 3;                // Regenerates 3 per turn
  
  // Energy-specific
  exhaustion_level: RangedInt<0, 5>; // Cumulative exhaustion
  last_full_rest: GameTime;
  turns_since_rest: number;
  
  // Effects
  low_energy_threshold: 2;
  low_energy_effects: LowResourceEffect[];
}

interface LowResourceEffect {
  effect_type: string;
  description: string;
  gameplay_impact: string;
  triggers_at: number;
}
```

### Money System

```typescript
/**
 * Money resource
 */
interface MoneyState {
  current: MoneyAmount;             // In cents
  currency: "USD" | "generic";
  
  // Income & expenses
  weekly_income: MoneyAmount;
  weekly_expenses: MoneyAmount;
  net_weekly: number;               // Can be negative
  
  // Tracking
  income_sources: IncomeSource[];
  expense_categories: ExpenseCategory[];
  
  // State
  in_debt: boolean;
  debt_amount?: MoneyAmount;
  weeks_until_broke: number | null; // Null if solvent
  
  // Constraints
  can_borrow: boolean;
  max_debt?: MoneyAmount;
}

interface IncomeSource {
  source_id: string;
  source_name: string;
  amount_per_week: MoneyAmount;
  reliable: boolean;
  can_lose: boolean;
  tied_to_card?: CardID;
}

interface ExpenseCategory {
  category: "rent" | "bills" | "food" | "transport" | "debt" | "other";
  amount_per_week: MoneyAmount;
  mandatory: boolean;
  can_reduce: boolean;
  skip_consequences?: string;
}
```

### Social Capital System

```typescript
/**
 * Social capital per NPC
 */
interface SocialCapitalState {
  capital_by_npc: Record<NPCID, SocialCapitalEntry>;
  total_social_capital: number;     // Sum across all NPCs
  average_social_capital: number;
}

interface SocialCapitalEntry {
  npc_id: NPCID;
  current: SocialCapital;           // -10 to +10
  maximum: 10;
  minimum: -10;
  
  // Earning & spending
  earn_rate: number;                // Per positive interaction
  spend_rate: number;               // Per request
  
  // Recovery
  decay_rate: number;               // If not interacting
  weeks_since_interaction: number;
  
  // State
  overdrawn: boolean;               // Negative balance
  at_capacity: boolean;             // At +10
  needs_maintenance: boolean;       // Been a while
}
```

### Time System

```typescript
/**
 * Time budget
 */
interface TimeState {
  // Weekly time budget
  total_weekly_hours: 168;          // 24 * 7
  sleep_hours: number;              // 49-63 typical (7-9 per day)
  work_hours: number;               // 40-60 typical
  obligation_hours: number;
  discretionary_hours: number;
  
  // Current turn
  current_turn_hours: number;       // Hours left this turn
  max_turn_hours: number;           // Typically 6 hours per turn
  
  // Allocation
  committed_activities: TimeCommitment[];
  scheduled_events: GameTime[];
  
  // Pressure
  overcommitted: boolean;
  time_pressure_level: Intensity;
  conflicts: TimeConflict[];
}

interface TimeCommitment {
  commitment_id: string;
  activity: CardID;
  hours_per_week: number;
  flexible: boolean;
  can_skip: boolean;
  skip_consequences?: string[];
}

interface TimeConflict {
  conflict_id: string;
  conflicting_activities: CardID[];
  resolution_options: string[];
  forced_choice: boolean;
}
```

---

## 2. Meters

### Meter System

```typescript
/**
 * All four meters (0-10 scale)
 */
interface Meters {
  physical: MeterState;
  mental: MeterState;
  social: MeterState;
  emotional: MeterState;
}

/**
 * Individual meter state
 */
interface MeterState {
  meter_id: "physical" | "mental" | "social" | "emotional";
  current: Meter;                   // 0-10
  maximum: 10;
  minimum: 0;
  
  // Ideal range
  ideal_min: 4;
  ideal_max: 7;
  balanced: boolean;                // Within ideal range
  
  // Critical states
  critical_low: boolean;            // < 2
  critical_high: boolean;           // > 8
  
  // Tracking
  history: MeterSnapshot[];
  weeks_in_critical: number;
  weeks_balanced: number;
  
  // Changes
  pending_changes: MeterChange[];
  projected_value: Meter;           // After pending changes
}

interface MeterSnapshot {
  week: Week;
  value: Meter;
  emotional_state_at_time: EmotionalState;
}

interface MeterChange {
  change_id: string;
  source: CardID | "system";
  delta: number;                    // -10 to +10
  reason: string;
  applied_at?: GameTime;
  temporary: boolean;
  duration?: Duration;
}

/**
 * Meter balance analysis
 */
interface MeterBalance {
  all_balanced: boolean;
  balanced_count: number;
  imbalanced_meters: string[];
  
  // Spread
  highest_meter: "physical" | "mental" | "social" | "emotional";
  lowest_meter: "physical" | "mental" | "social" | "emotional";
  spread: number;                   // Highest - lowest
  
  // Crisis risk
  crisis_risk_level: Intensity;     // 0-10
  crisis_triggers: CrisisTrigger[];
  
  // Breakthrough potential
  breakthrough_possible: boolean;
  weeks_until_breakthrough?: number;
}

interface CrisisTrigger {
  trigger_type: "meter_critical" | "spread_extreme" | "neglect" | "accumulated_stress";
  meter_involved?: string;
  threshold: number;
  current_value: number;
  weeks_until_trigger?: number;
}
```

### Meter Mechanics

```typescript
/**
 * Meter modification rules
 */
interface MeterModificationRules {
  // Caps
  absolute_minimum: 0;
  absolute_maximum: 10;
  
  // Soft caps (require escalating cost)
  soft_minimum: 1;
  soft_maximum: 9;
  
  // Regeneration
  natural_drift_to: 5;              // Meters drift toward 5 if untouched
  drift_rate: 0.5;                  // Per week
  
  // Neglect penalties
  neglect_threshold_weeks: 2;
  neglect_penalty_per_week: -1;
  
  // Recovery
  recovery_difficulty_below_3: "hard";
  recovery_difficulty_above_8: "hard";
  balanced_range_easy_to_maintain: [4, 7];
}

/**
 * Meter effects on gameplay
 */
interface MeterEffects {
  meter: "physical" | "mental" | "social" | "emotional";
  
  // At different values
  effects_by_range: MeterRangeEffect[];
  
  // Impact on other systems
  affects_card_appeal: boolean;
  affects_success_chance: boolean;
  affects_relationships: boolean;
  affects_emotional_state: boolean;
}

interface MeterRangeEffect {
  range: [number, number];          // [min, max] inclusive
  range_name: string;
  description: string;
  gameplay_effects: string[];
  
  // Examples
  card_appeal_modifiers?: Record<CardCategory, number>;
  success_chance_modifier?: number;
  energy_cost_modifier?: number;
}

/**
 * Example: Physical meter effects
 */
const PHYSICAL_METER_EFFECTS: MeterRangeEffect[] = [
  {
    range: [0, 1],
    range_name: "Critical - Illness/Injury",
    description: "Severe physical distress. Cannot ignore.",
    gameplay_effects: [
      "Forced crisis event",
      "All activities cost +2 energy",
      "Success chances -40%",
      "Physical activities impossible"
    ]
  },
  {
    range: [2, 3],
    range_name: "Poor - Run Down",
    description: "Noticeably unwell. Affecting daily function.",
    gameplay_effects: [
      "Physical activities cost +1 energy",
      "Success chances -20%",
      "Exhaustion accumulates faster",
      "Sleep/rest cards +200% appeal"
    ]
  },
  {
    range: [4, 7],
    range_name: "Balanced - Healthy",
    description: "Feeling good. No significant physical issues.",
    gameplay_effects: [
      "Normal gameplay",
      "Can engage in all activities",
      "No modifiers"
    ]
  },
  {
    range: [8, 9],
    range_name: "Excellent - Peak Condition",
    description: "In great shape. High physical energy.",
    gameplay_effects: [
      "Physical activities cost -1 energy",
      "Physical success chances +15%",
      "Breakthrough potential if all meters high"
    ]
  },
  {
    range: [10, 10],
    range_name: "Extreme - Obsessive",
    description: "Unhealthily focused on physical perfection.",
    gameplay_effects: [
      "Compulsive exercise cards appear",
      "Other meters suffer (-1 per week)",
      "Risk of injury",
      "Relationships comment on obsession"
    ]
  }
];
```

---

## 3. Turn Structure

### Turn System

```typescript
/**
 * Current turn state
 */
interface TurnState {
  // Time
  current_time: GameTime;
  turn_type: "daily" | "weekly" | "seasonal";
  
  // Phase
  phase: TurnPhase;
  phase_started_at: ISO8601String;
  
  // Actions
  actions_taken: TurnAction[];
  actions_available: number;
  max_actions: number;
  
  // Cards
  current_hand: CardID[];
  cards_played_this_turn: CardID[];
  
  // State
  turn_locked: boolean;             // During resolution
  can_end_turn: boolean;
  must_resolve_before_end: CardID[];
  
  // Next turn
  queued_for_next_turn: QueuedAction[];
}

enum TurnPhase {
  Setup = "setup",                  // System draws hand
  Planning = "planning",            // Player views hand, plans
  Action = "action",                // Player takes actions
  Resolution = "resolution",        // Cards resolve
  Consolidation = "consolidation",  // Update meters, resources, etc
  Completion = "completion"         // Turn over, prep next
}

interface TurnAction {
  action_id: string;
  action_type: "play_card" | "skip" | "batch_process" | "end_turn";
  timestamp: ISO8601String;
  
  // Context
  card_id?: CardID;
  choice_made?: any;
  resources_spent: ResourceCost;
  
  // Outcome
  success: boolean;
  effects_applied: CardEffect[];
  unlocked_content: string[];
}

interface QueuedAction {
  queue_id: string;
  action: TurnAction;
  execute_at: GameTime;
  can_cancel: boolean;
}
```

### Turn Resolution

```typescript
/**
 * Turn resolution process
 */
interface TurnResolution {
  turn_id: string;
  resolving_turn: GameTime;
  
  // Steps
  resolution_steps: ResolutionStep[];
  current_step: number;
  
  // Results
  meters_changed: Record<string, number>;
  resources_changed: Record<string, number>;
  cards_updated: CardID[];
  relationships_changed: Record<NPCID, number>;
  
  // Events triggered
  events_triggered: TriggeredEvent[];
  
  // Next turn prep
  hand_for_next_turn: CardID[];
}

interface ResolutionStep {
  step_id: string;
  step_type: ResolutionStepType;
  description: string;
  
  // Execution
  execute_order: number;
  executed: boolean;
  result?: any;
}

enum ResolutionStepType {
  ResolveCardEffects = "resolve_card_effects",
  UpdateMeters = "update_meters",
  UpdateResources = "update_resources",
  ProcessRelationships = "process_relationships",
  CheckCrisisTriggers = "check_crisis_triggers",
  CheckBreakthroughTriggers = "check_breakthrough_triggers",
  ConsolidateMemories = "consolidate_memories",
  ProcessAspirations = "process_aspirations",
  DrawNextHand = "draw_next_hand",
  GenerateEvents = "generate_events"
}

interface TriggeredEvent {
  event_id: string;
  event_type: EventType;
  trigger_reason: string;
  card_generated?: CardID;
  forced: boolean;
  expires_at?: GameTime;
}
```

### Seasonal Turn (Every 12 Weeks)

```typescript
/**
 * Season turn (major checkpoint)
 */
interface SeasonTurn {
  season_id: SeasonID;
  season_number: number;
  
  // Timeframe
  start_week: Week;
  end_week: Week;
  weeks_duration: 12;
  
  // Retrospective
  season_summary: SeasonSummary;
  
  // Archive decision
  archive_candidates: CardID[];
  archive_limit: number;            // 3 for free, unlimited premium
  player_selections: CardID[];
  
  // Progression
  life_direction_shifts?: LifeDirection;
  major_events: EventSummary[];
  
  // Next season prep
  next_season_setup: SeasonSetup;
}

interface SeasonSummary {
  // Stats
  weeks_played: 12;
  total_cards_played: number;
  unique_cards_played: number;
  
  // Meters
  average_meters: Meters;
  meter_balance_score: Percentage;
  crises_experienced: number;
  breakthroughs_experienced: number;
  
  // Relationships
  new_relationships: NPCID[];
  deepened_relationships: NPCID[];
  lost_relationships: NPCID[];
  
  // Aspirations
  aspirations_completed: AspirationID[];
  aspirations_failed: AspirationID[];
  aspirations_ongoing: AspirationID[];
  
  // Fusions
  fusion_cards_created: number;
  legendary_fusions: FusionID[];
  
  // Memory
  most_memorable_weeks: Week[];
  emotional_journey: EmotionalState[];
  
  // Narrative
  story_arcs_completed: StoryArcID[];
  decisive_decisions_made: number;
  
  // Quality
  overall_season_quality: Percentage; // For book generation
}

interface SeasonSetup {
  season_number: number;
  
  // Continuing elements
  carried_forward_aspirations: AspirationID[];
  continuing_relationships: NPCID[];
  
  // New content
  new_cards_unlocked: CardID[];
  new_npcs_available: NPCID[];
  new_locations: LocationID[];
  
  // Configuration
  difficulty_adjustments: any;
  player_choices: any;
}

interface EventSummary {
  event_type: EventType;
  week: Week;
  description: string;
  emotional_weight: Intensity;
}
```

---

## 4. Success & Failure System

### Success Calculation

```typescript
/**
 * Success chance calculation
 */
interface SuccessCalculation {
  card_id: CardID;
  
  // Base chance
  base_chance: Probability;         // From card definition
  
  // Modifiers
  modifiers: SuccessModifier[];
  
  // Components
  personality_fit: number;          // -0.3 to +0.3
  skill_level: number;              // 0.0 to +0.25
  emotional_state: number;          // -0.2 to +0.2
  preparation: number;              // 0.0 to +0.15
  random: number;                   // -0.1 to +0.1
  
  // Final
  final_chance: Probability;        // 0.0-1.0, clamped
  display_chance: string;           // "Very Likely", "50/50", etc.
}

/**
 * Success modifier
 */
interface SuccessModifier {
  source: string;
  delta: number;
  reason: string;
  category: "personality" | "skill" | "emotional" | "preparation" | "random" | "other";
}

/**
 * Outcome types
 */
enum OutcomeType {
  CriticalSuccess = "critical_success",    // Rolled above 0.95
  Success = "success",                     // Rolled below success_chance
  PartialSuccess = "partial_success",      // Close but not quite
  Failure = "failure",                     // Rolled above success_chance
  CriticalFailure = "critical_failure"     // Rolled below 0.05
}

/**
 * Outcome result
 */
interface OutcomeResult {
  card_id: CardID;
  roll: number;                     // 0.0-1.0, the random roll
  success_chance: Probability;
  outcome: OutcomeType;
  
  // Effects
  effects_applied: CardEffect[];
  bonus_effects?: CardEffect[];     // For critical success
  reduced_effects?: CardEffect[];   // For partial/failure
  
  // Consequences
  meter_changes: Partial<Meters>;
  resource_changes: Partial<PlayerResources>;
  relationship_changes: Record<NPCID, number>;
  
  // Memory
  creates_memory: boolean;
  memory_emotional_weight: Intensity;
  
  // Narrative
  narrative_description: string;
}
```

### Difficulty System

```typescript
/**
 * Challenge difficulty
 */
interface ChallengeDifficulty {
  difficulty_level: Difficulty;
  
  // Success rates
  success_rate_low_skill: Probability;
  success_rate_medium_skill: Probability;
  success_rate_high_skill: Probability;
  success_rate_perfect_fit: Probability;
  
  // Consequences
  failure_severity: "mild" | "moderate" | "severe" | "catastrophic";
  
  // Scaling
  scales_with: string[];            // What affects difficulty
}

/**
 * Dynamic difficulty adjustment
 */
interface DifficultyAdjustment {
  enabled: boolean;
  
  // Triggers
  adjust_if_too_many_failures: number; // In a row
  adjust_if_too_many_successes: number;
  
  // Adjustments
  increase_success_chance_by: Percentage;
  decrease_success_chance_by: Percentage;
  
  // Limits
  min_success_chance: 0.1;          // Never below 10%
  max_success_chance: 0.95;         // Never above 95%
}
```

---

## 5. Locations

### Location System

```typescript
/**
 * Location definition
 */
interface Location {
  location_id: LocationID;
  name: string;
  location_type: LocationType;
  
  // Description
  description: string;
  atmosphere: string;
  sensory_details: string[];
  
  // Access
  unlocked: boolean;
  unlock_requirements?: CardRequirements;
  
  // NPCs
  frequent_npcs: NPCID[];
  npc_spawn_chances: Record<NPCID, Probability>;
  
  // Activities
  available_activities: CardID[];
  location_specific_activities: CardID[];
  
  // Properties
  privacy_level: Intensity;         // 1 = public, 10 = private
  comfort_level: Intensity;
  social_density: Intensity;        // How crowded
  
  // Time
  available_times: TimeOfDay[];
  
  // Costs
  entry_cost?: MoneyAmount;
  typical_activity_cost?: MoneyAmount;
}

/**
 * Location instance (player at location during turn)
 */
interface LocationInstance {
  location: LocationID;
  arrived_at: GameTime;
  
  // Present
  npcs_present: NPCID[];
  activities_available: CardID[];
  
  // Events
  random_event_chance: Probability;
  
  // Memory
  times_visited: number;
  memorable_moments: MemoryID[];
  
  // Atmosphere (can change)
  current_atmosphere: string;
}
```

---

## 6. Decision Making

### Decision Weight System

```typescript
/**
 * Decision context
 */
interface DecisionContext {
  decision_id: string;
  decision_type: "card_choice" | "dialogue_option" | "aspiration_commitment" | "crisis_response" | "life_direction";
  
  // Weight
  weight: DecisionWeight;
  time_limit?: Duration;
  
  // Options
  options: DecisionOption[];
  
  // Context
  emotional_state: EmotionalState;
  related_npcs: NPCID[];
  stakes: string;
  
  // Information
  information_complete: boolean;
  information_gaps: string[];
  
  // Pressure
  time_pressure: Intensity;
  social_pressure: Intensity;
  consequence_severity: Intensity;
}

interface DecisionOption {
  option_id: string;
  description: string;
  
  // Requirements
  requirements?: CardRequirements;
  available: boolean;
  
  // Predicted outcomes
  predicted_effects: CardEffect[];
  success_chance?: SuccessChance;
  risk_level: Intensity;
  
  // Alignment
  personality_alignment: number;    // How well it fits personality
  emotional_alignment: number;      // How well it fits emotional state
  
  // Consequences
  immediate_consequences: string[];
  long_term_consequences: string[];
  relationship_impacts: Record<NPCID, string>;
  
  // Regret potential
  regret_risk: Intensity;           // How likely to regret
}

/**
 * Decision result
 */
interface DecisionResult {
  decision_id: string;
  option_chosen: string;
  chosen_at: GameTime;
  
  // Time taken
  time_to_decide: Duration;
  rushed: boolean;
  
  // Outcome
  immediate_outcome: OutcomeResult;
  
  // Tracking
  logged_as: "trivial" | "minor" | "significant" | "life_defining";
  creates_memory: boolean;
  memory_id?: MemoryID;
  
  // Future reference
  can_affect_future: boolean;
  narrative_significance: Intensity;
}
```

---

## Notes for LLM Analysis

When validating gameplay mechanics schemas:

1. **Resource Ranges**: Energy 0-8, Meters 0-10, Social Capital -10 to +10
2. **Time Consistency**: Turns are 1-3, days 1-7, weeks increment
3. **Success Chances**: Always 0.0-1.0, never negative or >1.0
4. **Meter Balance**: Critical low <2, critical high >8, balanced 4-7
5. **Turn Phases**: Follow sequence: setup → planning → action → resolution → consolidation → completion
6. **Resource Costs**: All costs use ResourceCost interface
7. **Location Access**: Check unlock requirements reference valid cards
8. **Decision Weights**: Map to appropriate time limits

**Cross-schema dependencies**:
- CardID from card-system
- NPCID from character-system
- EmotionalState from emotional-system
- StoryArcID from narrative-system
- All effects must be valid CardEffect types
- Success modifiers must sum correctly
- Meter effects must be consistent with emotional-system

