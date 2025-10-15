# Validation Rules & Consistency Checks

**Schema Version**: 1.0.0  
**Last Updated**: 2025-10-13  
**Dependencies**: All previous schemas

---

## Overview

Defines comprehensive validation rules, consistency checks, cross-schema validation, and automated quality assurance for the entire Unwritten system.

---

## 1. Core Type Validation

### ID Format Validation

```typescript
/**
 * Validate entity ID formats
 */
interface IDValidationRules {
  // Pattern matching
  card_id_pattern: /^card_[a-z0-9_]+$/;
  npc_id_pattern: /^npc_[a-z0-9_]+$/;
  player_id_pattern: /^player_[a-z0-9_]+$/;
  season_id_pattern: /^season_\d+$/;
  arc_id_pattern: /^arc_[a-z0-9_]+$/;
  location_id_pattern: /^loc_[a-z0-9_]+$/;
  skill_id_pattern: /^skill_[a-z0-9_]+$/;
  
  // Uniqueness
  all_ids_must_be_unique: true;
  no_duplicate_ids_across_types: false; // card_001 and npc_001 is OK
  
  // Case sensitivity
  ids_are_case_sensitive: true;
  prefer_lowercase: true;
}

/**
 * Validate numeric ranges
 */
interface NumericRangeValidation {
  meters: {
    min: 0;
    max: 10;
    type: "integer";
  };
  
  personality_traits: {
    min: 1.0;
    max: 5.0;
    type: "float";
    precision: 1; // One decimal place
  };
  
  trust: {
    min: 0.0;
    max: 1.0;
    type: "float";
    precision: 2;
  };
  
  social_capital: {
    min: -10;
    max: 10;
    type: "integer";
  };
  
  percentage: {
    min: 0.0;
    max: 1.0;
    type: "float";
  };
  
  intensity: {
    min: 1;
    max: 10;
    type: "integer";
  };
}
```

### Temporal Validation

```typescript
/**
 * Time-related validation rules
 */
interface TemporalValidationRules {
  // Week numbers
  weeks_are_positive: true;
  weeks_increment_sequentially: true;
  no_time_travel: true;
  
  // Day of week
  day_of_week_range: [1, 7];
  day_of_week_names_match_numbers: true;
  
  // Turn of day
  turn_of_day_range: [1, 3];
  turns_increment_within_day: true;
  
  // Game time
  game_time_always_complete: true;  // Must have week, day, turn
  game_time_never_null: true;
  
  // ISO8601
  timestamps_are_valid_iso8601: true;
  timestamps_have_timezone: true;
  
  // Chronology
  events_in_chronological_order: true;
  later_events_have_later_timestamps: true;
  created_at_before_updated_at: true;
}
```

---

## 2. Card System Validation

### Card Structure Validation

```typescript
/**
 * Card validation rules
 */
interface CardValidationRules {
  // Required fields
  required_fields: ["card_id", "title", "tier", "category", "state"];
  
  // Tier consistency
  tier_matches_category: {
    "Foundation": [CardTier.Foundation],
    "life_direction": [CardTier.Foundation],
    "phase_transition": [CardTier.Foundation],
    "major_aspiration": [CardTier.Aspiration],
    // ... etc
  };
  
  // Evolution
  evolution_level_range: [0, 5];
  evolved_cards_have_parent: true;
  parent_card_exists: true;
  
  // State transitions
  valid_state_transitions: {
    "locked": ["available"],
    "available": ["in_hand", "playing"],
    "in_hand": ["playing", "available"],
    "playing": ["available", "cooldown", "exhausted"],
    "cooldown": ["available"],
    "exhausted": ["archived"],
    "archived": []
  };
  
  // Resource costs
  costs_never_negative: true;
  energy_cost_range: [0, 8];
  time_cost_range: [0, 24];
  
  // Effects
  all_effect_types_defined: true;
  effect_targets_exist: true;
  effect_values_in_valid_ranges: true;
}

/**
 * Fusion validation
 */
interface FusionValidationRules {
  // Source cards
  fusion_requires_2_plus_cards: true;
  source_cards_exist: true;
  source_cards_played_together: boolean; // Context-dependent
  
  // Rarity
  fusion_rarity_never_lower_than_sources: true;
  legendary_fusions_require_special_conditions: true;
  
  // Uniqueness
  fusion_result_is_unique_to_player: true;
  fusion_id_globally_unique: true;
  
  // Properties
  fusion_card_has_origin_story: true;
  fusion_inherits_some_properties: true;
}
```

---

## 3. Character System Validation

### Personality Validation

```typescript
/**
 * Personality system validation
 */
interface PersonalityValidationRules {
  // OCEAN ranges
  all_traits_in_range: [1.0, 5.0];
  traits_to_one_decimal: true;
  
  // Evolution
  personality_changes_gradual: {
    max_change_per_week: 0.1;
    max_change_per_event: 0.5;
  };
  
  personality_changes_have_triggers: true;
  triggers_are_documented: true;
  
  // Consistency
  baseline_personality_never_null: true;
  snapshots_in_chronological_order: true;
  
  // Compatibility
  compatibility_scores_between_0_and_1: true;
}

/**
 * Relationship validation
 */
interface RelationshipValidationRules {
  // Core metrics
  trust_range: [0.0, 1.0];
  social_capital_range: [-10, 10];
  
  // Level consistency
  relationship_level_matches_trust: {
    [RelationshipLevel.Stranger]: [0.0, 0.2],
    [RelationshipLevel.Acquaintance]: [0.2, 0.4],
    [RelationshipLevel.Friend]: [0.4, 0.6],
    [RelationshipLevel.CloseFriend]: [0.6, 0.8],
    [RelationshipLevel.BestFriend]: [0.8, 0.95],
    [RelationshipLevel.Soulmate]: [0.95, 1.0]
  };
  
  // History
  first_met_before_last_interaction: true;
  interaction_count_matches_history: true;
  
  // Mutual consistency
  if_a_knows_b_then_b_knows_a: true;
  relationships_are_bidirectional: true;
  
  // Snapshots
  snapshots_show_progression: true;
  trust_changes_are_reasonable: {
    max_increase_per_interaction: 0.3;
    max_decrease_per_interaction: -0.5;
  };
}

/**
 * NPC memory validation
 */
interface MemoryValidationRules {
  // Tier capacity
  short_term_max: 10;
  medium_term_max: 30;
  long_term_max: 100;
  
  // Consolidation
  memories_consolidate_upward_only: true;
  higher_tier_memories_more_significant: true;
  
  // Timeline
  memories_in_chronological_order: true;
  memory_week_valid: true;
  
  // Emotional weight
  emotional_weight_range: [1, 10];
  long_term_memories_min_weight: 5;
  
  // References
  linked_memories_exist: true;
  character_references_exist: true;
}
```

---

## 4. Gameplay Mechanics Validation

### Resource Validation

```typescript
/**
 * Resource system validation
 */
interface ResourceValidationRules {
  // Energy
  energy_never_negative: true;
  energy_max: 8;
  energy_regen_per_turn: 3;
  
  // Money
  money_in_cents: true;
  money_can_be_negative_if_in_debt: true;
  debt_has_reasonable_limit: true;
  
  // Time
  weekly_hours_total: 168;
  time_allocations_sum_to_168: true;
  discretionary_hours_non_negative: true;
  
  // Meters
  all_meters_0_to_10: true;
  meters_are_integers: true;
  
  // Social capital
  social_capital_per_npc_range: [-10, 10];
  npc_exists_for_social_capital_entry: true;
}

/**
 * Turn system validation
 */
interface TurnValidationRules {
  // Turn sequence
  turns_1_2_3_per_day: true;
  days_1_through_7: true;
  weeks_increment_after_day_7: true;
  
  // Phase sequence
  turn_phases_in_order: true;
  cannot_skip_phases: true;
  
  // Actions
  actions_taken_during_action_phase: true;
  max_actions_enforced: true;
  
  // Hand
  hand_size_within_limits: true;
  cards_in_hand_exist: true;
  cards_in_hand_are_available: true;
}
```

---

## 5. Narrative System Validation

### Story Arc Validation

```typescript
/**
 * Story arc validation rules
 */
interface StoryArcValidationRules {
  // Structure
  arcs_have_at_least_one_phase: true;
  phases_in_sequential_order: true;
  phase_week_ranges_non_overlapping: true;
  
  // Status
  active_arcs_within_current_week: true;
  completed_arcs_have_end_week: true;
  failed_arcs_have_failure_reason: true;
  
  // NPCs
  all_referenced_npcs_exist: true;
  primary_npcs_appear_in_arc: true;
  
  // Decisive decisions
  decisive_decisions_are_life_defining_weight: true;
  decisive_decisions_create_memories: true;
  choices_have_consequences: true;
  
  // Completion
  success_variations_require_completed_phases: true;
  failure_conditions_are_mutually_exclusive_with_success: true;
}

/**
 * Memory validation
 */
interface NarrativeMemoryValidationRules {
  // Required fields
  memory_has_week_and_location: true;
  memory_has_emotional_state: true;
  
  // Significance
  emotional_weight_range: [1, 10];
  narrative_significance_range: [1, 10];
  
  // Characters
  all_characters_present_exist: true;
  pov_character_is_valid: true;
  
  // Timeline
  memory_week_within_season: true;
  memories_chronological_within_season: true;
  
  // Sensory
  sensory_snapshot_has_at_least_2_senses: true;
  
  // References
  related_arc_exists_if_specified: true;
  decisive_decision_exists_if_specified: true;
}

/**
 * Timeline validation
 */
interface TimelineValidationRules {
  // Chronology
  events_in_chronological_order: true;
  no_duplicate_events_same_week: false; // Multiple events per week OK
  
  // Density
  dramatic_density_reasonable: {
    max_decisive_decisions_per_season: 8;
    max_crises_per_season: 4;
  };
  
  // Seeds and payoffs
  planted_seeds_eventually_pay_off: true;
  foreshadowing_pays_off_within_reasonable_time: {
    max_weeks_until_payoff: 20;
  };
  
  // Arc timing
  arcs_start_before_they_end: true;
  arc_duration_reasonable: {
    min_weeks: 4;
    max_weeks: 60;
  };
}
```

---

## 6. Emotional System Validation

### Emotional State Validation

```typescript
/**
 * Emotional system validation
 */
interface EmotionalStateValidationRules {
  // States
  emotional_state_is_one_of_20: true;
  state_belongs_to_correct_quadrant: true;
  
  // Coordinates
  energy_level_range: [-1, 1];
  valence_range: [-1, 1];
  
  // Transitions
  transitions_reference_valid_states: true;
  transition_probabilities_between_0_and_1: true;
  natural_transitions_make_sense: true;
  
  // Duration
  time_in_state_non_negative: true;
  volatile_states_change_more_frequently: true;
  stable_states_persist_longer: true;
  
  // Mood filters
  all_card_categories_have_modifiers: true;
  modifiers_are_multiplicative: {
    min: 0.1;
    max: 5.0;
  };
}

/**
 * Emotional journey validation
 */
interface EmotionalJourneyValidationRules {
  // History
  state_history_chronological: true;
  state_durations_sum_correctly: true;
  
  // Variety
  variety_score_between_0_and_1: true;
  
  // Quality
  narrative_arc_requires_turning_points: true;
  trajectory_consistent_with_events: true;
  
  // Beats
  emotional_beats_tied_to_events: true;
  beat_intensity_range: [1, 10];
  peaks_and_lows_identified: true;
}
```

---

## 7. AI Integration Validation

### AI Inference Validation

```typescript
/**
 * AI system validation rules
 */
interface AIValidationRules {
  // Performance
  inference_time_under_50ms: true;
  target_inference_time: 15; // milliseconds
  
  // Battery
  battery_cost_tracked: true;
  battery_optimization_enabled: true;
  
  // Quality
  confidence_scores_between_0_and_1: true;
  low_confidence_triggers_fallback: {
    threshold: 0.7;
  };
  
  // Context
  all_required_context_provided: true;
  context_references_valid_entities: true;
  
  // Results
  personality_predictions_in_valid_ranges: true;
  sentiment_scores_between_minus_1_and_1: true;
  generated_dialogue_not_empty: true;
  
  // Fallback
  fallback_always_available: true;
  fallback_produces_valid_results: true;
}
```

---

## 8. Archive & Persistence Validation

### Archive Validation

```typescript
/**
 * Archive system validation
 */
interface ArchiveValidationRules {
  // Season archive
  season_archive_has_summary: true;
  archived_cards_within_tier_limits: true;
  free_tier_max_3_cards: true;
  premium_tier_unlimited_cards: true;
  
  // Content
  all_archived_cards_exist: true;
  all_archived_memories_exist: true;
  all_archived_relationships_exist: true;
  
  // Quality
  season_quality_scores_between_0_and_1: true;
  
  // Book
  if_book_generated_has_metadata: true;
  book_word_count_matches_tier: {
    free: [3000, 5000],
    premium: [12000, 15000]
  };
  
  // Timestamps
  archived_at_after_season_end: true;
}

/**
 * Save system validation
 */
interface SaveValidationRules {
  // Completeness
  save_has_all_required_sections: true;
  save_has_version_info: true;
  
  // Consistency
  player_state_consistent: true;
  card_states_match_deck: true;
  npc_states_match_relationships: true;
  
  // Timeline
  save_timestamp_valid: true;
  game_time_valid: true;
  
  // Size
  save_file_within_reasonable_size: {
    max_mb: 50;
  };
  
  // Compression
  if_compressed_can_decompress: true;
}
```

---

## 9. Monetization Validation

### Monetization Validation

```typescript
/**
 * Monetization system validation
 */
interface MonetizationValidationRules {
  // Essence
  essence_balance_never_negative: true;
  essence_transactions_sum_correctly: true;
  essence_never_expires: true;
  
  // Subscription
  active_subscription_has_valid_dates: true;
  subscription_benefits_granted: true;
  subscription_end_after_start: true;
  
  // Tiers
  tier_capabilities_consistent: true;
  free_tier_gets_25_daily_essence: true;
  premium_tier_has_active_subscription: true;
  
  // Packs
  owned_packs_have_purchase_date: true;
  pack_content_unlocked_after_purchase: true;
  
  // Pricing
  all_prices_positive: true;
  essence_costs_within_reasonable_range: true;
  
  // Entitlements
  entitlements_match_purchases: true;
  premium_content_gated_correctly: true;
}
```

---

## 10. Novel Generation Validation

### Novel Generation Validation

```typescript
/**
 * Novel generation validation rules
 */
interface NovelGenerationValidationRules {
  // Master context
  master_context_complete: true;
  all_established_facts_valid: true;
  character_registry_complete: true;
  no_contradictory_facts: true;
  
  // Chapter packet
  chapter_has_all_required_sections: true;
  pov_perspectives_complete: true;
  scenes_have_structure: true;
  
  // Continuity
  facts_never_contradicted: true;
  character_voices_consistent: true;
  timeline_coherent: true;
  relationship_states_consistent: true;
  
  // Quality
  word_count_matches_target: {
    tolerance_percentage: 0.1; // Within 10%
  };
  
  sensory_details_present: true;
  at_least_3_senses_per_scene: true;
  
  show_dont_tell_ratio: {
    min_showing: 0.7; // 70% showing vs telling
  };
  
  // Technique
  micro_tension_in_every_paragraph: true;
  interiority_present: true;
  dialogue_has_subtext: true;
  
  // Structure
  scenes_have_6_elements: true; // Anchor, action, reaction, complication, decision, tension
  chapter_has_hook_ending: true;
  
  // Callbacks
  planted_callbacks_tracked: true;
  paid_off_callbacks_reference_valid_seeds: true;
  
  // Book assembly
  chapters_in_order: true;
  chapter_numbers_sequential: true;
  total_word_count_sum_of_chapters: true;
}
```

---

## 11. Cross-Schema Validation

### Entity Reference Validation

```typescript
/**
 * Cross-schema reference validation
 */
interface CrossSchemaValidationRules {
  // Card references
  cards_referenced_in_gameplay_exist_in_card_system: true;
  card_effects_reference_valid_meters: true;
  card_requirements_reference_valid_resources: true;
  
  // Character references
  npcs_referenced_in_narrative_exist_in_character_system: true;
  npc_personalities_in_valid_ranges: true;
  npc_relationships_bidirectional: true;
  
  // Location references
  locations_in_memories_exist_in_gameplay: true;
  location_activities_exist_in_card_system: true;
  
  // Arc references
  arcs_in_timeline_exist_in_narrative_system: true;
  arc_cards_exist_in_card_system: true;
  arc_npcs_exist_in_character_system: true;
  
  // Memory references
  memories_reference_valid_cards: true;
  memories_reference_valid_npcs: true;
  memories_reference_valid_locations: true;
  
  // Archive references
  archived_content_exists_in_source_systems: true;
  
  // Novel references
  novel_facts_consistent_with_game_state: true;
  novel_characters_match_npc_profiles: true;
  novel_timeline_matches_game_timeline: true;
}

/**
 * Data consistency validation
 */
interface DataConsistencyValidation {
  // Temporal consistency
  all_dates_valid: true;
  created_before_updated: true;
  events_chronological: true;
  
  // Numerical consistency
  all_ranges_respected: true;
  sums_add_up: true;
  percentages_between_0_and_1: true;
  
  // Relationship consistency
  parent_child_relationships_valid: true;
  circular_references_detected: false;
  orphaned_records_detected: false;
  
  // State consistency
  state_transitions_valid: true;
  mutually_exclusive_states_enforced: true;
  
  // Enum consistency
  all_enum_values_valid: true;
  string_enums_case_consistent: true;
}
```

---

## 12. Validation Execution

### Validation Framework

```typescript
/**
 * Validation execution
 */
interface ValidationExecution {
  // When to validate
  validate_on_load: boolean;
  validate_on_save: boolean;
  validate_on_mutation: boolean;
  validate_before_generation: boolean;
  
  // What to validate
  validate_all_schemas: boolean;
  validate_cross_references: boolean;
  validate_data_integrity: boolean;
  
  // Error handling
  fail_fast_on_critical_errors: boolean;
  collect_all_errors: boolean;
  
  // Performance
  async_validation: boolean;
  cache_validation_results: boolean;
  validation_timeout_ms: number;
}

/**
 * Validation result
 */
interface ValidationResult {
  valid: boolean;
  timestamp: ISO8601String;
  duration_ms: number;
  
  // Issues
  critical_errors: ValidationError[];
  errors: ValidationError[];
  warnings: ValidationWarning[];
  info: ValidationInfo[];
  
  // Statistics
  total_checks_run: number;
  checks_passed: number;
  checks_failed: number;
  
  // By schema
  results_by_schema: Record<string, SchemaValidationResult>;
}

interface ValidationError {
  error_id: string;
  severity: "critical" | "error";
  schema: string;
  rule: string;
  message: string;
  location: string;
  value_found: any;
  value_expected: any;
  fix_suggestion: string;
}

interface ValidationWarning {
  warning_id: string;
  severity: "warning";
  schema: string;
  rule: string;
  message: string;
  location: string;
  suggestion: string;
}
```

---

## Notes for LLM Analysis

When using this schema to validate Unwritten data:

1. **Start with Core Types**: Validate IDs, ranges, enums first
2. **Entity Existence**: Verify all referenced entities exist
3. **Cross-References**: Check bidirectional relationships
4. **Timeline Coherence**: Events in chronological order
5. **State Consistency**: Valid state transitions
6. **Numerical Ranges**: All values within defined limits
7. **Enum Values**: All enum references valid
8. **Completeness**: Required fields present
9. **Contradictions**: No contradictory facts/states
10. **Quality Metrics**: Scores in valid ranges

**Validation Priority**:
1. **Critical**: Data integrity, no contradictions, entity existence
2. **High**: Timeline coherence, relationship consistency, state validity
3. **Medium**: Quality metrics, optional fields, warnings
4. **Low**: Optimization hints, style suggestions, info messages

**Automated Checks**:
- Run validation on every save
- Run before book generation
- Run after AI content generation
- Run periodically on loaded game state
- Cache results for performance
- Report issues to developers for fixes

This validation schema ensures that all data across the entire Unwritten system remains consistent, coherent, and contradiction-free.

