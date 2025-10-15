# Emotional System Schema

**Schema Version**: 1.0.0  
**Last Updated**: 2025-10-13  
**Dependencies**: `01-core-types.md`, `04-gameplay-mechanics.md`

---

## Overview

Defines the 20 emotional states, state transitions, mood filtering, emotional influence on gameplay, and emotional journey tracking.

---

## 1. Emotional States

### The 20 Core States

```typescript
/**
 * All 20 emotional states organized by quadrants
 */
enum EmotionalState {
  // ENERGIZING POSITIVE (High Energy + Positive Valence)
  MOTIVATED = "MOTIVATED",
  INSPIRED = "INSPIRED",
  EXCITED = "EXCITED",
  CONFIDENT = "CONFIDENT",
  
  // CALM POSITIVE (Low Energy + Positive Valence)
  CONTENT = "CONTENT",
  PEACEFUL = "PEACEFUL",
  GRATEFUL = "GRATEFUL",
  REFLECTIVE = "REFLECTIVE",
  
  // ENERGIZING NEGATIVE (High Energy + Negative Valence)
  FRUSTRATED = "FRUSTRATED",
  ANXIOUS = "ANXIOUS",
  RESTLESS = "RESTLESS",
  PASSIONATE = "PASSIONATE",
  
  // WITHDRAWING NEGATIVE (Low Energy + Negative Valence)
  MELANCHOLY = "MELANCHOLY",
  DISCOURAGED = "DISCOURAGED",
  NUMB = "NUMB",
  EXHAUSTED = "EXHAUSTED",
  
  // NEUTRAL / TRANSITIONAL
  CURIOUS = "CURIOUS",
  FOCUSED = "FOCUSED",
  BALANCED = "BALANCED",
  UNCERTAIN = "UNCERTAIN"
}

/**
 * Emotional quadrant classification
 */
enum EmotionalQuadrant {
  EnergizingPositive = "energizing_positive",
  CalmPositive = "calm_positive",
  EnergizingNegative = "energizing_negative",
  WithdrawingNegative = "withdrawing_negative",
  Neutral = "neutral"
}

/**
 * Emotional state properties
 */
interface EmotionalStateProperties {
  state: EmotionalState;
  quadrant: EmotionalQuadrant;
  
  // Coordinates
  energy_level: RangedFloat<-1, 1>;  // -1 = low, +1 = high
  valence: RangedFloat<-1, 1>;       // -1 = negative, +1 = positive
  
  // Description
  display_name: string;
  description: string;
  physical_manifestation: string[];
  thought_patterns: string[];
  
  // Gameplay effects
  card_appeal_modifiers: Record<CardCategory, number>;
  success_chance_modifier: number;
  energy_cost_modifier: number;
  social_interaction_modifier: number;
  
  // Duration tendencies
  typical_duration: Duration;
  stable: boolean;                  // Tends to persist
  volatile: boolean;                // Changes easily
  
  // Transitions
  natural_transitions_to: EmotionalState[];
  crisis_transitions_to: EmotionalState[];
  breakthrough_transitions_to: EmotionalState[];
}
```

### State Definitions

```typescript
/**
 * Complete emotional state definitions
 */
const EMOTIONAL_STATE_DEFINITIONS: Record<EmotionalState, EmotionalStateProperties> = {
  MOTIVATED: {
    state: EmotionalState.MOTIVATED,
    quadrant: EmotionalQuadrant.EnergizingPositive,
    energy_level: 0.7,
    valence: 0.6,
    display_name: "Motivated",
    description: "Driven to take action, ready to tackle challenges",
    physical_manifestation: [
      "Alert posture",
      "Quick movements",
      "Forward-leaning body language"
    ],
    thought_patterns: [
      "Let's do this",
      "I can make progress today",
      "One step at a time"
    ],
    card_appeal_modifiers: {
      social_activity: 1.2,
      solo_activity: 1.5,
      challenge: 1.8,
      routine: 1.1,
      exploration: 1.3
    },
    success_chance_modifier: 0.15,
    energy_cost_modifier: -1,
    social_interaction_modifier: 0.1,
    typical_duration: { hours: 4 },
    stable: false,
    volatile: true,
    natural_transitions_to: [
      EmotionalState.CONFIDENT,
      EmotionalState.FOCUSED,
      EmotionalState.FRUSTRATED
    ],
    crisis_transitions_to: [EmotionalState.ANXIOUS, EmotionalState.EXHAUSTED],
    breakthrough_transitions_to: [EmotionalState.INSPIRED, EmotionalState.CONFIDENT]
  },
  
  ANXIOUS: {
    state: EmotionalState.ANXIOUS,
    quadrant: EmotionalQuadrant.EnergizingNegative,
    energy_level: 0.6,
    valence: -0.7,
    display_name: "Anxious",
    description: "Worried, on edge, anticipating problems",
    physical_manifestation: [
      "Tense muscles",
      "Fidgeting",
      "Shallow breathing",
      "Racing heart"
    ],
    thought_patterns: [
      "What if something goes wrong?",
      "I'm not prepared",
      "Too many things could fail",
      "I should have..."
    ],
    card_appeal_modifiers: {
      social_activity: 0.5,
      solo_activity: 0.8,
      challenge: 0.3,
      routine: 1.4,
      exploration: 0.2
    },
    success_chance_modifier: -0.15,
    energy_cost_modifier: 2,
    social_interaction_modifier: -0.3,
    typical_duration: { hours: 6 },
    stable: false,
    volatile: true,
    natural_transitions_to: [
      EmotionalState.EXHAUSTED,
      EmotionalState.FOCUSED,
      EmotionalState.PEACEFUL
    ],
    crisis_transitions_to: [EmotionalState.NUMB, EmotionalState.MELANCHOLY],
    breakthrough_transitions_to: [EmotionalState.CONFIDENT, EmotionalState.PEACEFUL]
  },
  
  CONTENT: {
    state: EmotionalState.CONTENT,
    quadrant: EmotionalQuadrant.CalmPositive,
    energy_level: -0.3,
    valence: 0.7,
    display_name: "Content",
    description: "Satisfied, at peace with the present moment",
    physical_manifestation: [
      "Relaxed posture",
      "Gentle smile",
      "Slow, deep breathing"
    ],
    thought_patterns: [
      "This is nice",
      "I have enough",
      "Things are good right now"
    ],
    card_appeal_modifiers: {
      social_activity: 1.1,
      solo_activity: 1.2,
      challenge: 0.7,
      routine: 1.3,
      exploration: 0.8
    },
    success_chance_modifier: 0.05,
    energy_cost_modifier: 0,
    social_interaction_modifier: 0.2,
    typical_duration: { hours: 8 },
    stable: true,
    volatile: false,
    natural_transitions_to: [
      EmotionalState.PEACEFUL,
      EmotionalState.GRATEFUL,
      EmotionalState.REFLECTIVE
    ],
    crisis_transitions_to: [EmotionalState.UNCERTAIN, EmotionalState.ANXIOUS],
    breakthrough_transitions_to: [EmotionalState.GRATEFUL, EmotionalState.INSPIRED]
  },
  
  EXHAUSTED: {
    state: EmotionalState.EXHAUSTED,
    quadrant: EmotionalQuadrant.WithdrawingNegative,
    energy_level: -0.9,
    valence: -0.6,
    display_name: "Exhausted",
    description: "Depleted, running on empty, need rest",
    physical_manifestation: [
      "Slumped posture",
      "Heavy limbs",
      "Difficulty concentrating",
      "Physical fatigue"
    ],
    thought_patterns: [
      "I can't do this anymore",
      "I just need to rest",
      "Everything feels like too much"
    ],
    card_appeal_modifiers: {
      social_activity: 0.2,
      solo_activity: 0.4,
      challenge: 0.1,
      routine: 0.3,
      exploration: 0.1
    },
    success_chance_modifier: -0.25,
    energy_cost_modifier: 3,
    social_interaction_modifier: -0.5,
    typical_duration: { hours: 12 },
    stable: true,
    volatile: false,
    natural_transitions_to: [
      EmotionalState.NUMB,
      EmotionalState.CONTENT,
      EmotionalState.PEACEFUL
    ],
    crisis_transitions_to: [EmotionalState.NUMB, EmotionalState.MELANCHOLY],
    breakthrough_transitions_to: [EmotionalState.CONTENT, EmotionalState.GRATEFUL]
  },
  
  BALANCED: {
    state: EmotionalState.BALANCED,
    quadrant: EmotionalQuadrant.Neutral,
    energy_level: 0.0,
    valence: 0.0,
    display_name: "Balanced",
    description: "Emotionally centered, in equilibrium",
    physical_manifestation: [
      "Neutral posture",
      "Steady breathing",
      "Clear-eyed"
    ],
    thought_patterns: [
      "I'm okay",
      "Things are as they are",
      "I can handle what comes"
    ],
    card_appeal_modifiers: {
      social_activity: 1.0,
      solo_activity: 1.0,
      challenge: 1.0,
      routine: 1.0,
      exploration: 1.0
    },
    success_chance_modifier: 0.0,
    energy_cost_modifier: 0,
    social_interaction_modifier: 0.0,
    typical_duration: { days: 1 },
    stable: true,
    volatile: false,
    natural_transitions_to: [
      EmotionalState.CONTENT,
      EmotionalState.MOTIVATED,
      EmotionalState.CURIOUS
    ],
    crisis_transitions_to: [EmotionalState.ANXIOUS, EmotionalState.FRUSTRATED],
    breakthrough_transitions_to: [EmotionalState.INSPIRED, EmotionalState.GRATEFUL]
  }
  
  // ... Define all 20 states similarly
};
```

---

## 2. State Transitions

### Transition System

```typescript
/**
 * Emotional state transition
 */
interface EmotionalTransition {
  transition_id: string;
  from_state: EmotionalState;
  to_state: EmotionalState;
  
  // Trigger
  trigger: TransitionTrigger;
  
  // Probability
  base_probability: Probability;
  modified_probability: Probability;
  
  // Modifiers
  modifiers: TransitionModifier[];
  
  // Timing
  transition_speed: "instant" | "gradual" | "delayed";
  transition_duration?: Duration;
  
  // Requirements
  requires: TransitionRequirement[];
}

interface TransitionTrigger {
  trigger_type: TransitionTriggerType;
  source: string;                   // Card, event, time passage, etc.
  description: string;
  emotional_weight: Intensity;
}

enum TransitionTriggerType {
  CardOutcome = "card_outcome",
  MeterChange = "meter_change",
  TimePassage = "time_passage",
  Relationship Event = "relationship_event",
  Crisis = "crisis",
  Breakthrough = "breakthrough",
  DecisiveDecision = "decisive_decision",
  Natural = "natural",
  Random = "random"
}

interface TransitionModifier {
  source: string;
  delta: number;                    // +/- to probability
  reason: string;
}

interface TransitionRequirement {
  requirement_type: "meter_above" | "meter_below" | "resource_above" | "time_passed";
  value: any;
  met: boolean;
}
```

### Transition Rules

```typescript
/**
 * Transition rules between emotional states
 */
interface TransitionRules {
  // Natural drift
  natural_drift_enabled: boolean;
  drift_toward_balanced: boolean;
  drift_rate: Percentage;           // Per hour
  
  // Momentum
  state_momentum: boolean;          // Harder to leave stable states
  momentum_factor: number;
  
  // Volatility
  volatile_states_change_easily: boolean;
  stable_states_resist_change: boolean;
  
  // Meter influence
  meter_critical_forces_state: boolean;
  all_meters_balanced_enables_breakthrough: boolean;
  
  // Quadrant locking
  can_skip_across_quadrants: boolean;
  must_transition_through_neutral: boolean;
  
  // Limits
  max_transitions_per_turn: number;
  min_duration_in_state: Duration;
}

/**
 * Transition probability calculation
 */
interface TransitionProbabilityCalculation {
  from_state: EmotionalState;
  to_state: EmotionalState;
  trigger: TransitionTrigger;
  
  // Base
  base_probability: Probability;    // From state definition
  
  // Modifiers
  meter_modifier: number;
  personality_modifier: number;
  recent_events_modifier: number;
  time_in_state_modifier: number;
  
  // Final
  final_probability: Probability;
  will_transition: boolean;
}
```

---

## 3. Mood Filtering (Hand Generation)

### Mood-Based Card Appeal

```typescript
/**
 * How emotional state affects card appeal
 */
interface MoodFilter {
  current_state: EmotionalState;
  
  // Card appeal modifications
  category_modifiers: Record<CardCategory, number>;
  
  // Specific card modifiers
  card_specific_modifiers: Record<CardID, number>;
  
  // Filtered hand
  increases_appeal: CardCategory[];
  decreases_appeal: CardCategory[];
  blocks_entirely: CardCategory[];
  
  // Explanation
  player_visible_explanation: string;
}

/**
 * Example mood filters for different states
 */
const MOOD_FILTERS: Record<EmotionalState, MoodFilter> = {
  ANXIOUS: {
    current_state: EmotionalState.ANXIOUS,
    category_modifiers: {
      routine: 1.4,                 // +40% appeal
      obligation: 1.3,
      solo_activity: 0.8,
      social_activity: 0.5,         // -50% appeal
      exploration: 0.2,             // -80% appeal
      challenge: 0.3
    },
    card_specific_modifiers: {
      "card_meditation": 2.0,
      "card_journaling": 1.5,
      "card_party_invitation": 0.1
    },
    increases_appeal: ["routine", "obligation", "structured"],
    decreases_appeal: ["exploration", "challenge", "social"],
    blocks_entirely: [],
    player_visible_explanation: "Feeling anxious. Craving familiar routines and avoiding new situations."
  },
  
  MOTIVATED: {
    current_state: EmotionalState.MOTIVATED,
    category_modifiers: {
      challenge: 1.8,
      exploration: 1.3,
      solo_activity: 1.5,
      social_activity: 1.2,
      routine: 1.1,
      obligation: 0.9
    },
    card_specific_modifiers: {},
    increases_appeal: ["challenge", "activity", "progress"],
    decreases_appeal: ["rest", "passive"],
    blocks_entirely: [],
    player_visible_explanation: "Feeling motivated. Ready to take on challenges and make progress."
  },
  
  EXHAUSTED: {
    current_state: EmotionalState.EXHAUSTED,
    category_modifiers: {
      challenge: 0.1,
      exploration: 0.1,
      social_activity: 0.2,
      solo_activity: 0.4,
      obligation: 0.3,
      routine: 0.3
    },
    card_specific_modifiers: {
      "card_sleep": 5.0,
      "card_rest_day": 3.0,
      "card_netflix": 2.0
    },
    increases_appeal: ["rest", "passive", "low_energy"],
    decreases_appeal: ["active", "social", "demanding"],
    blocks_entirely: ["high_intensity_exercise"],
    player_visible_explanation: "Feeling exhausted. Need to rest and recharge."
  }
  
  // ... all 20 states
};
```

### Appeal Calculation

```typescript
/**
 * Card appeal with emotional state
 */
interface CardAppealCalculation {
  card_id: CardID;
  base_appeal: Probability;
  
  // Emotional modifier
  emotional_state: EmotionalState;
  emotional_modifier: number;
  
  // Other modifiers
  personality_modifier: number;
  life_direction_modifier: number;
  recent_play_modifier: number;
  
  // Final
  final_appeal: Probability;
  draw_weight: number;
  
  // Explanation
  why_appealing: string[];
  why_not_appealing: string[];
}
```

---

## 4. Emotional Journey Tracking

### Journey System

```typescript
/**
 * Player's emotional journey over time
 */
interface EmotionalJourney {
  player_id: PlayerID;
  
  // Current
  current_state: EmotionalState;
  time_in_state: Duration;
  
  // History
  state_history: EmotionalStateRecord[];
  transitions: EmotionalTransition[];
  
  // Patterns
  dominant_states: EmotionalState[];
  rare_states: EmotionalState[];
  typical_state_duration: Record<EmotionalState, Duration>;
  
  // Trajectory
  emotional_trajectory: EmotionalTrajectory;
  
  // Quality metrics
  variety_score: number;            // 0-1, how many states experienced
  stability_score: number;          // 0-1, how stable emotionally
  positivity_ratio: number;         // Positive states / Total states
  
  // Cycles
  identified_cycles: EmotionalCycle[];
  
  // Book generation
  narrative_emotional_arc: boolean; // Does it tell a story?
  arc_quality: Percentage;
}

interface EmotionalStateRecord {
  state: EmotionalState;
  entered_at: GameTime;
  exited_at?: GameTime;
  duration: Duration;
  trigger: string;
  notable_events_during: string[];
}

interface EmotionalTrajectory {
  trajectory_type: "improving" | "declining" | "stable" | "oscillating" | "narrative_arc";
  
  // Peaks and valleys
  highest_point: {
    week: Week;
    state: EmotionalState;
  };
  lowest_point: {
    week: Week;
    state: EmotionalState;
  };
  
  // Trend
  trend_direction: "up" | "down" | "flat";
  trend_strength: Percentage;
  
  // Narrative quality
  follows_story_arc: boolean;
  has_turning_points: boolean;
  resolution_satisfying: boolean;
}

interface EmotionalCycle {
  cycle_id: string;
  pattern: EmotionalState[];
  frequency: Duration;
  identified_at: Week;
  occurrences: number;
  trigger_pattern?: string;
}
```

### Emotional Beats (Narrative)

```typescript
/**
 * Emotional beat - significant emotional moment
 */
interface EmotionalBeat {
  beat_id: string;
  week: Week;
  
  // State
  state: EmotionalState;
  intensity: Intensity;
  
  // Context
  trigger: string;
  cards_involved: CardID[];
  npcs_involved: NPCID[];
  
  // Narrative function
  beat_type: EmotionalBeatType;
  narrative_purpose: string;
  
  // Position in arc
  position_in_season: Percentage;   // 0.0-1.0 through season
  position_in_act: "setup" | "conflict" | "climax" | "resolution";
  
  // Impact
  changes_trajectory: boolean;
  turning_point: boolean;
  
  // Book generation
  chapter_worthy: boolean;
  dramatic_weight: Intensity;
}

enum EmotionalBeatType {
  EmotionalPeak = "emotional_peak",
  EmotionalLow = "emotional_low",
  TurningPoint = "turning_point",
  Breakthrough = "breakthrough",
  Crisis = "crisis",
  Revelation = "revelation",
  Connection = "connection",
  Loss = "loss",
  Triumph = "triumph",
  Setback = "setback"
}
```

---

## 5. Crisis & Breakthrough States

### Crisis States

```typescript
/**
 * Crisis-related emotional states
 */
interface CrisisEmotionalState {
  crisis_id: string;
  
  // Progression
  pre_crisis_state: EmotionalState; // Before crisis
  crisis_state: EmotionalState;     // During crisis
  post_crisis_state?: EmotionalState; // After resolution
  
  // Intensity
  emotional_intensity: RangedInt<7, 10>; // Crises are intense
  
  // Duration
  crisis_duration: Duration;
  time_to_recover: Duration;
  
  // Impact
  permanent_emotional_scars: boolean;
  changes_baseline_state: boolean;
}

/**
 * Crisis triggers from emotional state
 */
const CRISIS_EMOTIONAL_TRIGGERS = {
  prolonged_exhaustion: {
    state: EmotionalState.EXHAUSTED,
    duration_threshold: { weeks: 3 },
    triggers: "burnout_crisis"
  },
  prolonged_anxious: {
    state: EmotionalState.ANXIOUS,
    duration_threshold: { weeks: 4 },
    triggers: "anxiety_crisis"
  },
  prolonged_melancholy: {
    state: EmotionalState.MELANCHOLY,
    duration_threshold: { weeks: 6 },
    triggers: "depression_crisis"
  }
};
```

### Breakthrough States

```typescript
/**
 * Breakthrough emotional requirements
 */
interface BreakthroughEmotionalRequirements {
  // All meters balanced (4-7)
  meters_balanced: boolean;
  
  // Positive emotional state
  required_states: EmotionalState[];
  current_state_positive: boolean;
  
  // Sustained duration
  duration_balanced: Duration;
  duration_threshold: Duration;     // Typically 2+ weeks
  
  // No recent crises
  weeks_since_crisis: number;
  min_weeks_since_crisis: 4;
  
  // Breakthrough eligible
  eligible: boolean;
  probability: Probability;
}

/**
 * Post-breakthrough emotional state
 */
interface BreakthroughEmotionalEffect {
  immediate_state: EmotionalState;  // INSPIRED, CONFIDENT, or GRATEFUL
  enhanced_duration: Duration;      // State lasts longer
  
  // Effects
  positive_momentum: boolean;
  success_boost: Percentage;
  energy_boost: number;
  
  // Duration
  breakthrough_window: Duration;    // 1-2 weeks of enhanced state
}
```

---

## 6. Personality-Emotion Interactions

### Emotional Tendencies by Personality

```typescript
/**
 * How personality affects emotional states
 */
interface PersonalityEmotionalTendencies {
  personality: PersonalityTraits;
  
  // State tendencies
  default_state: EmotionalState;
  common_states: EmotionalState[];
  rare_states: EmotionalState[];
  
  // Modifiers
  high_neuroticism: {
    more_prone_to: [EmotionalState.ANXIOUS, EmotionalState.MELANCHOLY],
    less_prone_to: [EmotionalState.PEACEFUL, EmotionalState.BALANCED],
    transition_modifier: 0.3        // Transitions 30% more likely to negative
  };
  
  high_extraversion: {
    more_prone_to: [EmotionalState.EXCITED, EmotionalState.MOTIVATED],
    less_prone_to: [EmotionalState.NUMB, EmotionalState.EXHAUSTED],
    social_recovery_bonus: 0.2
  };
  
  low_openness: {
    more_prone_to: [EmotionalState.CONTENT, EmotionalState.BALANCED],
    less_prone_to: [EmotionalState.INSPIRED, EmotionalState.CURIOUS],
    novelty_anxiety_risk: 0.3
  };
  
  // ... other traits
}

/**
 * Emotional resilience based on personality
 */
interface EmotionalResilience {
  personality: PersonalityTraits;
  
  // Recovery rates
  recovery_from_negative_states: Duration;
  maintenance_of_positive_states: Duration;
  
  // Crisis resistance
  crisis_threshold_modifier: number;
  crisis_recovery_speed_modifier: number;
  
  // Breakthrough potential
  breakthrough_probability_modifier: number;
}
```

---

## Notes for LLM Analysis

When validating emotional system schemas:

1. **State Count**: Exactly 20 emotional states defined
2. **Quadrants**: Each state assigned to correct quadrant
3. **Energy/Valence**: Coordinates in range [-1, 1]
4. **Transitions**: All natural_transitions_to reference valid states
5. **Modifiers**: Appeal modifiers are multiplicative (0.1-5.0 typical)
6. **Duration**: Typical durations reasonable (hours to days)
7. **Mood Filters**: All card categories have modifiers defined
8. **Journey Tracking**: State history chronological

**Cross-schema dependencies**:
- CardCategory from card-system (all categories defined)
- Meters from gameplay-mechanics (affects state transitions)
- PersonalityTraits from character-system (affects tendencies)
- Crisis/Breakthrough triggers link to gameplay-mechanics
- Emotional beats reference narrative-system timeline
- Hand generation uses card-system appeal calculations
- State changes logged in narrative-system memory

