# Core Types & Foundational Schemas

**Schema Version**: 1.0.0  
**Last Updated**: 2025-10-13  
**Dependencies**: None (foundation schema)

---

## Overview

This schema defines fundamental types used across all Unwritten systems. All other schemas depend on these core types.

---

## 1. Identifiers

### Entity ID Formats

```typescript
/**
 * Base type for all entity identifiers
 * Format: {entity_type}_{unique_identifier}
 */
type EntityID = string;

// Specific ID types
type CardID = string;           // "card_12847" | "card_uuid_abc123"
type NPCID = string;            // "npc_sarah_anderson" | "npc_001"
type PlayerID = string;         // "player_uuid_xyz789"
type SeasonID = string;         // "season_3" | "season_uuid_def456"
type StoryArcID = string;       // "arc_photography_dream"
type LocationID = string;       // "loc_cafe_luna"
type SkillID = string;          // "skill_cooking" | "skill_photography"
type AspirationID = string;     // "asp_marathon" | "asp_012"
type FusionID = string;         // "fusion_uuid_abc123"
type MemoryID = string;         // "mem_12847"
type PackID = string;           // "pack_creative_arts"

/**
 * ID Generation Convention:
 * 
 * Prefer semantic IDs for:
 * - Core NPCs: "npc_sarah_anderson"
 * - Locations: "loc_cafe_luna"
 * - Skills: "skill_cooking"
 * 
 * Use incremental for:
 * - Generic cards: "card_00123"
 * - Memories: "mem_12847"
 * - Seasons: "season_3"
 * 
 * Use UUIDs for:
 * - User-generated content
 * - Runtime-created entities
 * - Unique player instances
 */

/**
 * Validation regex patterns
 */
const ID_PATTERNS = {
  card: /^card_[a-z0-9_]+$/,
  npc: /^npc_[a-z0-9_]+$/,
  player: /^player_[a-z0-9_]+$/,
  season: /^season_\d+$/,
  arc: /^arc_[a-z0-9_]+$/,
  location: /^loc_[a-z0-9_]+$/,
  skill: /^skill_[a-z0-9_]+$/,
  aspiration: /^asp_[a-z0-9_]+$/,
  fusion: /^fusion_[a-z0-9_]+$/,
  memory: /^mem_\d+$/,
  pack: /^pack_[a-z0-9_]+$/
};
```

---

## 2. Time & Temporal Types

### Game Time

```typescript
/**
 * Week number (1-based)
 * Represents in-game progression
 */
type Week = number; // 1, 2, 3, ... 100+

/**
 * Day of week (1-7, Monday = 1)
 */
type DayOfWeek = 1 | 2 | 3 | 4 | 5 | 6 | 7;

/**
 * Turn within day (1-3)
 * 1 = Morning (6am-12pm)
 * 2 = Afternoon (12pm-6pm)
 * 3 = Evening (6pm-12am)
 */
type TurnOfDay = 1 | 2 | 3;

/**
 * Complete game time reference
 */
interface GameTime {
  week: Week;
  day: DayOfWeek;
  turn: TurnOfDay;
}

/**
 * Human-readable time strings
 */
type TimeOfDay = "morning" | "afternoon" | "evening" | "night";
type DayName = "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday" | "Saturday" | "Sunday";
type Season = "spring" | "summer" | "autumn" | "winter";

/**
 * Duration measurement
 */
interface Duration {
  weeks?: number;
  days?: number;
  hours?: number;
  minutes?: number;
}
```

### Real-World Time

```typescript
/**
 * ISO 8601 timestamp string
 * Example: "2025-10-13T14:30:00Z"
 */
type ISO8601String = string;

/**
 * Timestamp with timezone
 */
interface Timestamp {
  iso: ISO8601String;
  unix: number;          // Unix timestamp (seconds since epoch)
  timezone?: string;     // "America/New_York"
}

/**
 * Date range
 */
interface DateRange {
  start: ISO8601String;
  end: ISO8601String;
  duration_days: number;
}
```

---

## 3. Numeric Types & Ranges

### Basic Numeric Types

```typescript
/**
 * Percentage (0.0 to 1.0)
 * Example: 0.75 = 75%
 */
type Percentage = number; // 0.0 <= value <= 1.0

/**
 * Integer in range [min, max]
 */
type RangedInt<Min extends number, Max extends number> = number & { 
  __min: Min; 
  __max: Max; 
};

/**
 * Float in range [min, max]
 */
type RangedFloat<Min extends number, Max extends number> = number & { 
  __min: Min; 
  __max: Max; 
};

// Common ranges
type Meter = RangedInt<0, 10>;         // Meters are 0-10
type Personality = RangedFloat<1, 5>;  // OCEAN traits are 1.0-5.0
type Trust = RangedFloat<0, 1>;        // Trust/attraction are 0.0-1.0
type Intensity = RangedInt<1, 10>;     // Intensity levels are 1-10
type Priority = RangedInt<1, 10>;      // Priority values are 1-10
```

### Stat Types

```typescript
/**
 * Core game meters (0-10)
 */
interface Meters {
  physical: Meter;      // Physical health/energy
  mental: Meter;        // Mental health/focus
  social: Meter;        // Social connection/energy
  emotional: Meter;     // Emotional wellbeing
}

/**
 * Big 5 personality traits (1.0-5.0)
 */
interface PersonalityTraits {
  openness: Personality;           // 1.0 = Low, 5.0 = High
  conscientiousness: Personality;
  extraversion: Personality;
  agreeableness: Personality;
  neuroticism: Personality;
}

/**
 * Money amount (cents to avoid floating point issues)
 */
type MoneyAmount = number; // Stored as cents, display as dollars

/**
 * Energy points (regenerates per turn)
 */
type Energy = number; // 0-8 typical range

/**
 * Social capital (-10 to +10)
 */
type SocialCapital = RangedInt<-10, 10>;
```

---

## 4. Common Enums

### Core Game Enums

```typescript
/**
 * Card tier classification
 */
enum CardTier {
  Foundation = 1,      // Life Direction, Phase Transition
  Aspiration = 2,      // Major/Minor Aspirations
  Structure = 3,       // Routines, Obligations, Scheduled
  Quest = 4,           // Milestone, Repeatable Quest
  Activity = 5,        // Social, Solo, Exploration, Challenge
  Event = 6,           // NPC-Initiated, Random, Crisis, Breakthrough
  System = 7           // Skills, Items, Perks, Memory
}

/**
 * Card rarity
 */
enum CardRarity {
  Common = "common",         // 70%
  Uncommon = "uncommon",     // 20%
  Rare = "rare",             // 8%
  Legendary = "legendary"    // 2%
}

/**
 * Emotional states (20 total)
 */
enum EmotionalState {
  // Energizing Positive
  MOTIVATED = "MOTIVATED",
  INSPIRED = "INSPIRED",
  EXCITED = "EXCITED",
  CONFIDENT = "CONFIDENT",
  
  // Calm Positive
  CONTENT = "CONTENT",
  PEACEFUL = "PEACEFUL",
  GRATEFUL = "GRATEFUL",
  REFLECTIVE = "REFLECTIVE",
  
  // Energizing Negative
  FRUSTRATED = "FRUSTRATED",
  ANXIOUS = "ANXIOUS",
  RESTLESS = "RESTLESS",
  PASSIONATE = "PASSIONATE",
  
  // Withdrawing Negative
  MELANCHOLY = "MELANCHOLY",
  DISCOURAGED = "DISCOURAGED",
  NUMB = "NUMB",
  EXHAUSTED = "EXHAUSTED",
  
  // Neutral
  CURIOUS = "CURIOUS",
  FOCUSED = "FOCUSED",
  BALANCED = "BALANCED",
  UNCERTAIN = "UNCERTAIN"
}

/**
 * Decision weight tiers
 */
enum DecisionWeight {
  AutoResolve = 1,     // Trivial, auto-processed
  Quick = 2,           // Minor, 3-5 seconds
  Considered = 3,      // Significant, 30-60 seconds
  LifeDefining = 4     // Major, unlimited time
}

/**
 * Relationship types
 */
enum RelationshipType {
  Stranger = "stranger",
  Acquaintance = "acquaintance",
  Friend = "friend",
  CloseFriend = "close_friend",
  BestFriend = "best_friend",
  Partner = "partner",
  Family = "family",
  Enemy = "enemy",
  Rival = "rival"
}

/**
 * Event/Moment types
 */
enum EventType {
  DecisiveDecision = "decisive_decision",
  EmotionalPeak = "emotional_peak",
  EmotionalLow = "emotional_low",
  RelationshipMilestone = "relationship_milestone",
  Crisis = "crisis",
  Breakthrough = "breakthrough",
  FusionCreation = "fusion_creation",
  AspirationComplete = "aspiration_complete",
  AspirationFailed = "aspiration_failed"
}

/**
 * Location types
 */
enum LocationType {
  Home = "home",
  Work = "work",
  Social = "social",
  Commercial = "commercial",
  Recreation = "recreation",
  Nature = "nature",
  Cultural = "cultural",
  Transit = "transit"
}
```

---

## 5. Common Interfaces

### Result & Error Types

```typescript
/**
 * Standard result wrapper
 */
interface Result<T, E = Error> {
  success: boolean;
  data?: T;
  error?: E;
  metadata?: Record<string, any>;
}

/**
 * Validation result
 */
interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
}

interface ValidationError {
  field: string;
  message: string;
  code: string;
  severity: "error" | "critical";
}

interface ValidationWarning {
  field: string;
  message: string;
  code: string;
  severity: "warning" | "info";
}

/**
 * Game error types
 */
enum ErrorCode {
  InvalidID = "INVALID_ID",
  NotFound = "NOT_FOUND",
  InvalidState = "INVALID_STATE",
  InsufficientResources = "INSUFFICIENT_RESOURCES",
  InvalidChoice = "INVALID_CHOICE",
  SaveFailed = "SAVE_FAILED",
  LoadFailed = "LOAD_FAILED",
  NetworkError = "NETWORK_ERROR",
  AIInferenceError = "AI_INFERENCE_ERROR"
}

interface GameError {
  code: ErrorCode;
  message: string;
  context?: Record<string, any>;
  timestamp: ISO8601String;
  recoverable: boolean;
}
```

### Metadata & Tags

```typescript
/**
 * Generic metadata container
 */
interface Metadata {
  tags: string[];
  properties: Record<string, any>;
  created_at: ISO8601String;
  updated_at: ISO8601String;
  version: string;
}

/**
 * Tagging system
 */
interface Tag {
  id: string;
  name: string;
  category: string;
  color?: string;
}

/**
 * Search/filter criteria
 */
interface FilterCriteria {
  tags?: string[];
  properties?: Record<string, any>;
  date_range?: DateRange;
  min_value?: number;
  max_value?: number;
}
```

### Probability & Randomness

```typescript
/**
 * Probability value (0.0 to 1.0)
 */
type Probability = Percentage;

/**
 * Weighted option for random selection
 */
interface WeightedOption<T> {
  value: T;
  weight: number;        // Higher weight = more likely
  probability?: Probability; // Calculated from weights
}

/**
 * Random outcome with probabilities
 */
interface OutcomeDistribution<T> {
  options: WeightedOption<T>[];
  total_weight: number;
  seed?: number;         // For deterministic randomness
}

/**
 * Success/failure chance
 */
interface SuccessChance {
  base_chance: Probability;
  modifiers: SuccessModifier[];
  final_chance: Probability;
  rolls_required?: number; // For multi-roll checks
}

interface SuccessModifier {
  source: string;
  delta: number;         // +/- to add to base chance
  reason: string;
}
```

---

## 6. Resource Types

### Core Resources

```typescript
/**
 * Resource cost structure
 */
interface ResourceCost {
  energy?: Energy;
  time_hours?: number;
  money?: MoneyAmount;
  social_capital?: SocialCapital;
  comfort_risk?: RangedInt<0, 5>; // 0 = no risk, 5 = extreme
}

/**
 * Resource availability
 */
interface ResourceAvailability {
  current: number;
  maximum: number;
  regeneration_rate?: number;
  regeneration_interval?: Duration;
}

/**
 * Player resources state
 */
interface PlayerResources {
  energy: ResourceAvailability;
  money: MoneyAmount;
  social_capital: Record<NPCID, SocialCapital>;
  time_budget: {
    weekly_hours: number;
    discretionary_hours: number;
    committed_hours: number;
  };
}
```

---

## 7. Common Utility Types

### Optional & Nullable

```typescript
/**
 * Value that may be null or undefined
 */
type Optional<T> = T | null | undefined;

/**
 * Value that may be null
 */
type Nullable<T> = T | null;

/**
 * Partial with required fields
 */
type PartialExcept<T, K extends keyof T> = Partial<T> & Pick<T, K>;

/**
 * Make specific fields optional
 */
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;
```

### Array & Collection Types

```typescript
/**
 * Non-empty array
 */
type NonEmptyArray<T> = [T, ...T[]];

/**
 * Fixed-length array
 */
type FixedArray<T, N extends number> = N extends N 
  ? number extends N 
    ? T[] 
    : _FixedArrayType<T, N, []> 
  : never;
type _FixedArrayType<T, N extends number, R extends any[]> = R['length'] extends N 
  ? R 
  : _FixedArrayType<T, N, [T, ...R]>;

/**
 * Tuple types
 */
type Pair<T> = [T, T];
type Triple<T> = [T, T, T];

/**
 * Map with required keys
 */
type RequiredMap<K extends string | number | symbol, V> = Record<K, V>;
```

### String Types

```typescript
/**
 * Non-empty string
 */
type NonEmptyString = string & { __brand: "NonEmptyString" };

/**
 * URL string
 */
type URL = string & { __brand: "URL" };

/**
 * Email string
 */
type Email = string & { __brand: "Email" };

/**
 * JSON string
 */
type JSONString = string & { __brand: "JSON" };

/**
 * Localized string
 */
interface LocalizedString {
  en: string;
  es?: string;
  fr?: string;
  de?: string;
  ja?: string;
  zh?: string;
  [locale: string]: string | undefined;
}
```

---

## 8. Schema Versioning

### Version Structure

```typescript
/**
 * Semantic version string
 * Format: MAJOR.MINOR.PATCH
 */
type SemanticVersion = string; // "1.2.3"

/**
 * Schema version info
 */
interface SchemaVersion {
  version: SemanticVersion;
  last_updated: ISO8601String;
  breaking_changes_from?: SemanticVersion;
  migration_required?: boolean;
  changelog?: string[];
}

/**
 * Versioned entity
 */
interface Versioned {
  schema_version: SemanticVersion;
  data_version?: number;       // Incremental version for this entity
  created_at: ISO8601String;
  updated_at: ISO8601String;
  deprecated?: boolean;
  deprecation_message?: string;
}
```

---

## 9. Common Patterns

### Builder Pattern

```typescript
/**
 * Builder interface for complex objects
 */
interface Builder<T> {
  build(): T;
  validate(): ValidationResult;
  reset(): this;
}
```

### Observer Pattern

```typescript
/**
 * Event listener
 */
type EventListener<T = any> = (event: T) => void;

/**
 * Observable entity
 */
interface Observable<T> {
  subscribe(listener: EventListener<T>): UnsubscribeFn;
  unsubscribe(listener: EventListener<T>): void;
  notify(event: T): void;
}

type UnsubscribeFn = () => void;
```

### State Machine

```typescript
/**
 * State machine state
 */
interface State<T> {
  name: string;
  enter?: (context: T) => void;
  exit?: (context: T) => void;
  transitions: Record<string, string>; // event -> next state
}

/**
 * State machine
 */
interface StateMachine<T> {
  current_state: string;
  states: Record<string, State<T>>;
  transition(event: string, context: T): Result<string>;
}
```

---

## 10. Constants

### Game Constants

```typescript
/**
 * Game-wide constants
 */
const GAME_CONSTANTS = {
  // Time
  TURNS_PER_DAY: 3,
  DAYS_PER_WEEK: 7,
  WEEKS_PER_SEASON: 12,
  
  // Resources
  MAX_ENERGY_PER_TURN: 3,
  MAX_METER_VALUE: 10,
  MIN_METER_VALUE: 0,
  
  // Personality
  MIN_PERSONALITY_TRAIT: 1.0,
  MAX_PERSONALITY_TRAIT: 5.0,
  
  // Relationships
  MIN_TRUST: 0.0,
  MAX_TRUST: 1.0,
  
  // Cards
  DEFAULT_HAND_SIZE: 8,
  MAX_DECK_SIZE: 10000, // Practically unlimited
  
  // Archive
  FREE_TIER_ARCHIVE_SLOTS: 3,
  PREMIUM_ARCHIVE_SLOTS: Infinity
} as const;

/**
 * Balance constants (tunable)
 */
const BALANCE_CONSTANTS = {
  // Success chance components (weights)
  PERSONALITY_FIT_WEIGHT: 0.30,
  SKILL_LEVEL_WEIGHT: 0.25,
  EMOTIONAL_STATE_WEIGHT: 0.20,
  PREPARATION_WEIGHT: 0.15,
  RANDOM_WEIGHT: 0.10,
  
  // Crisis triggers
  CRISIS_METER_THRESHOLD: 2,
  BURNOUT_THRESHOLD: 15, // (high_meter - low_meter) + neglect_weeks
  
  // Relationship
  RELATIONSHIP_DECAY_RATE: -0.05, // Per week of no interaction
  RELATIONSHIP_GROWTH_CAP: 0.3,   // Max gain per interaction
  
  // Evolution
  MIN_PERSONALITY_SHIFT: 0.1,
  MAX_PERSONALITY_SHIFT: 0.5,
  
  // Fusion
  FUSION_COMMON_CHANCE: 0.70,
  FUSION_UNCOMMON_CHANCE: 0.20,
  FUSION_RARE_CHANCE: 0.08,
  FUSION_LEGENDARY_CHANCE: 0.02
} as const;
```

---

## Usage Examples

### Creating an ID

```typescript
// Semantic ID
const sarahID: NPCID = "npc_sarah_anderson";

// Incremental ID
const cardID: CardID = `card_${incrementalCounter.toString().padStart(5, '0')}`;

// UUID-based ID
const playerID: PlayerID = `player_${generateUUID()}`;
```

### Working with Time

```typescript
const currentTime: GameTime = {
  week: 28,
  day: 2, // Tuesday
  turn: 1 // Morning
};

const meetingTime: ISO8601String = "2025-10-13T14:30:00Z";
```

### Resource Costs

```typescript
const activityCost: ResourceCost = {
  energy: 2,
  time_hours: 1.5,
  money: 1200, // $12.00 stored as cents
  social_capital: -1 // Costs social capital
};
```

### Personality Check

```typescript
const sarah_personality: PersonalityTraits = {
  openness: 3.5,
  conscientiousness: 4.0,
  extraversion: 2.8,
  agreeableness: 3.9,
  neuroticism: 3.8
};

// Validate
function validatePersonality(p: PersonalityTraits): boolean {
  return Object.values(p).every(v => 
    v >= GAME_CONSTANTS.MIN_PERSONALITY_TRAIT && 
    v <= GAME_CONSTANTS.MAX_PERSONALITY_TRAIT
  );
}
```

---

## Validation Rules

### ID Validation

```typescript
function validateID(id: string, type: keyof typeof ID_PATTERNS): boolean {
  return ID_PATTERNS[type].test(id);
}
```

### Range Validation

```typescript
function validateRange<T extends number>(
  value: T, 
  min: number, 
  max: number
): boolean {
  return value >= min && value <= max;
}
```

### Required Fields

```typescript
function hasRequiredFields<T extends object>(
  obj: T, 
  required: (keyof T)[]
): boolean {
  return required.every(field => obj[field] !== undefined && obj[field] !== null);
}
```

---

## Notes for LLM Analysis

When analyzing schemas for consistency:

1. **ID References**: All `*_id` fields must match format in ID_PATTERNS
2. **Numeric Ranges**: All numbers with semantic meaning should use RangedInt/RangedFloat
3. **Time Fields**: Use GameTime for game time, ISO8601String for real-world time
4. **Enums**: Check that string values match enum definitions
5. **Resources**: All costs should use ResourceCost interface
6. **Versioning**: All persistent schemas should include SchemaVersion

**Cross-Schema Checks**:
- NPC IDs in character-system match pattern here
- Card IDs in card-system match pattern here
- Enum values used in other schemas match definitions here
- Timestamp fields use consistent format
- Range types respect min/max from GAME_CONSTANTS

