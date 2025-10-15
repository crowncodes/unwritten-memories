# AI Integration Schema

**Schema Version**: 1.0.0  
**Last Updated**: 2025-10-13  
**Dependencies**: `01-core-types.md`, `02-card-system.md`, `03-character-system.md`, `06-emotional-system.md`

---

## Overview

Defines AI personality modeling, inference requests/responses, dialogue generation, sentiment analysis, and on-device TensorFlow Lite integration.

---

## 1. AI Inference System

### Inference Request

```typescript
/**
 * AI inference request structure
 */
interface AIInferenceRequest {
  request_id: string;
  request_type: AIRequestType;
  timestamp: ISO8601String;
  
  // Context
  context: AIContext;
  
  // Input data
  input_data: AIInputData;
  
  // Configuration
  model_config: ModelConfig;
  
  // Performance
  max_inference_time_ms: number;   // 15ms target
  battery_aware: boolean;
  cache_enabled: boolean;
}

enum AIRequestType {
  PersonalityPrediction = "personality_prediction",
  SentimentAnalysis = "sentiment_analysis",
  DialogueGeneration = "dialogue_generation",
  RelationshipScoring = "relationship_scoring",
  CardPersonalization = "card_personalization",
  EmotionalStateDetection = "emotional_state_detection",
  SuccessChancePrediction = "success_chance_prediction"
}

/**
 * AI context (game state for inference)
 */
interface AIContext {
  // Player
  player_personality: PersonalityTraits;
  player_emotional_state: EmotionalState;
  player_life_direction?: LifeDirection;
  player_meters: Meters;
  
  // Relationship context (if applicable)
  npc_id?: NPCID;
  npc_personality?: PersonalityTraits;
  npc_emotional_state?: EmotionalState;
  relationship_level?: RelationshipLevel;
  relationship_trust?: Trust;
  
  // Interaction history
  recent_interactions: InteractionSummary[];
  conversation_history?: ConversationTurn[];
  
  // Temporal
  current_week: Week;
  time_of_day: TimeOfDay;
  
  // World state
  active_arcs: StoryArcID[];
  recent_major_events: string[];
}

interface InteractionSummary {
  week: Week;
  interaction_type: string;
  outcome: "positive" | "neutral" | "negative";
  emotional_weight: Intensity;
}

interface ConversationTurn {
  speaker: string;
  message: string;
  emotional_state: EmotionalState;
  depth: ConversationDepth;
}
```

### Inference Response

```typescript
/**
 * AI inference response structure
 */
interface AIInferenceResponse {
  request_id: string;
  response_type: AIRequestType;
  timestamp: ISO8601String;
  
  // Result
  result: AIResult;
  
  // Performance metrics
  inference_time_ms: number;
  battery_cost: number;             // Estimated mAh
  cache_hit: boolean;
  
  // Confidence
  confidence: Percentage;
  confidence_threshold_met: boolean;
  
  // Fallback
  used_fallback: boolean;           // Used rule-based system
  fallback_reason?: string;
  
  // Validation
  valid: boolean;
  validation_errors?: string[];
}

/**
 * AI result types
 */
type AIResult =
  | PersonalityPredictionResult
  | SentimentAnalysisResult
  | DialogueGenerationResult
  | RelationshipScoringResult
  | CardPersonalizationResult
  | EmotionalStateDetectionResult
  | SuccessChancePredictionResult;
```

---

## 2. Personality Modeling

### Personality Prediction

```typescript
/**
 * Personality prediction request
 */
interface PersonalityPredictionRequest extends AIInferenceRequest {
  request_type: AIRequestType.PersonalityPrediction;
  
  input_data: {
    // Observed behaviors
    card_play_history: CardPlayRecord[];
    decision_history: DecisionRecord[];
    relationship_patterns: RelationshipPattern[];
    
    // Current traits (for refinement)
    current_personality?: PersonalityTraits;
    
    // Prediction target
    target_character?: NPCID;       // If predicting NPC
  };
}

interface CardPlayRecord {
  card_id: CardID;
  card_category: CardCategory;
  emotional_state_at_play: EmotionalState;
  success: boolean;
  week: Week;
}

interface DecisionRecord {
  decision_type: DecisionWeight;
  chosen_option: string;
  rejected_options: string[];
  personality_alignment: number;
  week: Week;
}

interface RelationshipPattern {
  npc_id: NPCID;
  interaction_frequency: number;
  depth_preference: ConversationDepth;
  conflict_resolution_style: string;
}

/**
 * Personality prediction result
 */
interface PersonalityPredictionResult {
  // Predicted traits
  predicted_personality: PersonalityTraits;
  
  // Confidence per trait
  trait_confidence: Record<keyof PersonalityTraits, Percentage>;
  
  // Changes from baseline
  personality_delta?: Partial<PersonalityTraits>;
  
  // Behavioral indicators
  supporting_evidence: BehavioralEvidence[];
  
  // Consistency
  consistency_score: Percentage;    // How consistent behaviors are
  contradictions: string[];
}

interface BehavioralEvidence {
  trait: keyof PersonalityTraits;
  behavior: string;
  frequency: number;
  weight: Percentage;
}
```

### Personality Evolution Tracking

```typescript
/**
 * Track personality evolution over time
 */
interface PersonalityEvolutionTracking {
  character_id: string;
  
  // Baseline
  initial_personality: PersonalityTraits;
  established_at: Week;
  
  // Current
  current_personality: PersonalityTraits;
  
  // History
  snapshots: PersonalitySnapshot[];
  significant_changes: PersonalityChange[];
  
  // Trajectory
  evolution_trajectory: {
    openness_trend: "increasing" | "decreasing" | "stable";
    conscientiousness_trend: "increasing" | "decreasing" | "stable";
    extraversion_trend: "increasing" | "decreasing" | "stable";
    agreeableness_trend: "increasing" | "decreasing" | "stable";
    neuroticism_trend: "increasing" | "decreasing" | "stable";
  };
  
  // Prediction
  predicted_next_week: PersonalityTraits;
  prediction_confidence: Percentage;
}
```

---

## 3. Dialogue Generation

### Dialogue Generation Request

```typescript
/**
 * Dialogue generation request
 */
interface DialogueGenerationRequest extends AIInferenceRequest {
  request_type: AIRequestType.DialogueGeneration;
  
  input_data: {
    // Speaker
    speaking_character: string;
    character_voice: VoiceProfile;
    character_personality: PersonalityTraits;
    character_emotional_state: EmotionalState;
    
    // Listener
    listening_characters: string[];
    
    // Context
    conversation_context: ConversationContext;
    
    // Intent
    speaker_intent: SpeakerIntent;
    
    // Constraints
    max_length_words?: number;
    tone_requirements?: string[];
    topic_restrictions?: string[];
  };
}

interface ConversationContext {
  location: LocationID;
  conversation_depth: ConversationDepth;
  relationship_states: Record<string, Relationship>;
  recent_topics: string[];
  unresolved_tensions: string[];
  conversation_history: ConversationTurn[];
  narrative_moment?: string;        // "First meeting", "confession", etc.
}

/**
 * Dialogue generation result
 */
interface DialogueGenerationResult {
  // Generated dialogue
  dialogue: string;
  
  // Alternatives
  alternatives?: string[];
  
  // Metadata
  actual_word_count: number;
  tone_achieved: string[];
  voice_consistency_score: Percentage;
  
  // Subtext
  surface_meaning: string;
  deeper_meaning?: string;
  emotional_subtext?: string;
  
  // Effects
  predicted_relationship_impact: number;
  predicted_emotional_response: EmotionalState;
  
  // Quality
  naturalness_score: Percentage;
  character_voice_match: Percentage;
}
```

### Dialogue Validation

```typescript
/**
 * Validate generated dialogue
 */
interface DialogueValidation {
  dialogue: string;
  character_id: string;
  
  // Checks
  checks: DialogueCheck[];
  
  // Result
  valid: boolean;
  quality_score: Percentage;
  
  // Issues
  issues: DialogueIssue[];
  suggestions: string[];
}

interface DialogueCheck {
  check_type: "voice_consistency" | "personality_match" | "context_appropriate" | "no_contradictions";
  passed: boolean;
  score: Percentage;
  details: string;
}

interface DialogueIssue {
  issue_type: "voice_mismatch" | "out_of_character" | "contradiction" | "unnatural" | "inappropriate";
  severity: "minor" | "moderate" | "critical";
  description: string;
  suggestion: string;
}
```

---

## 4. Sentiment Analysis

### Sentiment Analysis Request

```typescript
/**
 * Sentiment analysis request
 */
interface SentimentAnalysisRequest extends AIInferenceRequest {
  request_type: AIRequestType.SentimentAnalysis;
  
  input_data: {
    // Text to analyze
    text: string;
    
    // Context
    speaker?: string;
    listener?: string;
    conversation_history?: ConversationTurn[];
    
    // Options
    analyze_subtext: boolean;
    detect_sarcasm: boolean;
    detect_emotional_state: boolean;
  };
}

/**
 * Sentiment analysis result
 */
interface SentimentAnalysisResult {
  // Overall sentiment
  sentiment: "positive" | "neutral" | "negative";
  sentiment_score: RangedFloat<-1, 1>; // -1 = very negative, +1 = very positive
  
  // Emotional state
  detected_emotional_state: EmotionalState;
  emotional_confidence: Percentage;
  
  // Detailed analysis
  valence: RangedFloat<-1, 1>;     // Positive/negative
  arousal: RangedFloat<-1, 1>;     // High/low energy
  
  // Specific emotions detected
  emotions: EmotionDetection[];
  
  // Subtext
  surface_sentiment: string;
  underlying_sentiment?: string;
  sarcasm_detected: boolean;
  
  // Tone
  tone: string[];                   // ["anxious", "hopeful", "uncertain"]
}

interface EmotionDetection {
  emotion: string;
  probability: Probability;
  intensity: Intensity;
  evidence: string[];               // Words/phrases that indicate this
}
```

---

## 5. Relationship Scoring

### Relationship Scoring Request

```typescript
/**
 * Relationship scoring request (predict relationship impact)
 */
interface RelationshipScoringRequest extends AIInferenceRequest {
  request_type: AIRequestType.RelationshipScoring;
  
  input_data: {
    // Relationship
    relationship: Relationship;
    
    // Proposed action
    action_type: "card_play" | "dialogue_choice" | "decision";
    action_details: any;
    
    // Personalities
    from_personality: PersonalityTraits;
    to_personality: PersonalityTraits;
    
    // Context
    relationship_history: RelationshipSnapshot[];
    recent_interactions: InteractionSummary[];
  };
}

/**
 * Relationship scoring result
 */
interface RelationshipScoringResult {
  // Predicted impact
  trust_delta: number;              // -1.0 to +1.0
  attraction_delta?: number;
  social_capital_delta: number;
  
  // Confidence
  prediction_confidence: Percentage;
  
  // Reasoning
  positive_factors: string[];
  negative_factors: string[];
  risk_factors: string[];
  
  // Outcomes
  likely_outcome: "strengthens" | "maintains" | "strains" | "damages" | "uncertain";
  relationship_level_change?: RelationshipLevel;
  
  // Alternatives
  alternative_actions: AlternativeAction[];
}

interface AlternativeAction {
  action_description: string;
  predicted_trust_delta: number;
  predicted_outcome: string;
  better_than_proposed: boolean;
}
```

---

## 6. Card Personalization

### Card Personalization Request

```typescript
/**
 * Card personalization request (AI-generated content)
 */
interface CardPersonalizationRequest extends AIInferenceRequest {
  request_type: AIRequestType.CardPersonalization;
  
  input_data: {
    // Base card
    base_card_id: CardID;
    base_card_template: BaseCard;
    
    // Personalization context
    player_context: {
      personality: PersonalityTraits;
      life_direction: LifeDirection;
      active_arcs: StoryArcID[];
      key_relationships: Record<NPCID, Relationship>;
    };
    
    // Customization level
    customization_type: "light" | "moderate" | "heavy";
    
    // Requirements
    maintain_gameplay_balance: boolean;
    preserve_card_type: boolean;
  };
}

/**
 * Card personalization result
 */
interface CardPersonalizationResult {
  // Personalized card
  personalized_card: AIGeneratedCard;
  
  // Changes
  changes_from_template: CardPersonalizationChange[];
  
  // Quality
  personalization_quality: Percentage;
  gameplay_balance_maintained: boolean;
  
  // Validation
  requires_review: boolean;
  validation_issues: string[];
}

interface AIGeneratedCard extends BaseCard {
  ai_generated: true;
  generation_context: AIContext;
  personalization_level: "light" | "moderate" | "heavy";
  
  // Generated content
  personalized_title?: string;
  personalized_description?: string;
  personalized_effects?: CardEffect[];
  personalized_image_prompt?: string;
}

interface CardPersonalizationChange {
  field: string;
  original_value: any;
  personalized_value: any;
  reason: string;
  personality_driven: boolean;
}
```

---

## 7. Model Management

### Model Configuration

```typescript
/**
 * TensorFlow Lite model configuration
 */
interface ModelConfig {
  model_id: string;
  model_name: string;
  model_version: string;
  
  // File
  model_path: string;
  model_size_mb: number;
  
  // Inference
  use_gpu_delegate: boolean;
  use_nnapi_delegate: boolean;
  num_threads: number;
  
  // Performance
  target_inference_time_ms: 15;
  max_inference_time_ms: 50;
  
  // Battery optimization
  battery_saver_mode: boolean;
  reduce_inference_frequency: boolean;
  cache_aggressively: boolean;
  
  // Fallback
  fallback_to_rules: boolean;
  fallback_threshold_ms: 30;
}

/**
 * Model registry
 */
interface ModelRegistry {
  models: Record<string, ModelInfo>;
  active_models: string[];
  cached_models: string[];
}

interface ModelInfo {
  model_id: string;
  model_type: AIRequestType;
  version: string;
  
  // Metadata
  description: string;
  input_shape: number[];
  output_shape: number[];
  
  // Performance
  average_inference_ms: number;
  average_battery_cost_mah: number;
  
  // Quality
  accuracy_benchmark: Percentage;
  last_validated: ISO8601String;
  
  // Lifecycle
  loaded: boolean;
  last_used: ISO8601String;
  use_count: number;
}
```

### Model Lifecycle

```typescript
/**
 * Model initialization
 */
interface ModelInitialization {
  model_id: string;
  
  // Loading
  load_start: ISO8601String;
  load_end?: ISO8601String;
  load_duration_ms?: number;
  
  // Validation
  model_validated: boolean;
  validation_tests_passed: number;
  validation_tests_failed: number;
  
  // Optimization
  gpu_delegate_available: boolean;
  gpu_delegate_loaded: boolean;
  optimization_level: "none" | "basic" | "aggressive";
  
  // Status
  status: "loading" | "ready" | "error";
  error?: GameError;
}

/**
 * Model disposal
 */
interface ModelDisposal {
  model_id: string;
  disposed_at: ISO8601String;
  reason: "app_close" | "memory_pressure" | "upgrade" | "error";
  
  // Cleanup
  memory_freed_mb: number;
  resources_released: string[];
}
```

---

## 8. Performance & Battery Optimization

### Performance Monitoring

```typescript
/**
 * AI performance metrics
 */
interface AIPerformanceMetrics {
  // Inference performance
  total_inferences: number;
  average_inference_ms: number;
  p95_inference_ms: number;
  p99_inference_ms: number;
  
  // Battery
  total_battery_cost_mah: number;
  battery_cost_per_inference: number;
  
  // Cache
  cache_hit_rate: Percentage;
  cache_size_mb: number;
  
  // Fallback usage
  fallback_rate: Percentage;
  fallback_reasons: Record<string, number>;
  
  // Quality
  average_confidence: Percentage;
  low_confidence_rate: Percentage;
  
  // Errors
  error_rate: Percentage;
  error_types: Record<string, number>;
}
```

### Battery-Aware Inference

```typescript
/**
 * Battery-aware inference strategy
 */
interface BatteryAwareStrategy {
  // Current battery
  current_battery_level: Percentage;
  
  // Thresholds
  low_battery_threshold: 0.20;      // 20%
  critical_battery_threshold: 0.10; // 10%
  
  // Adjustments
  adjustments: BatteryAdjustment[];
}

interface BatteryAdjustment {
  battery_level_range: [Percentage, Percentage];
  
  // Actions
  reduce_inference_frequency: boolean;
  increase_cache_usage: boolean;
  prefer_rule_based: boolean;
  reduce_model_quality: boolean;
  
  // Limits
  max_inferences_per_turn: number;
  max_battery_cost_per_turn_mah: number;
}

/**
 * Example battery modes
 */
const BATTERY_MODES = {
  normal: {
    battery_level_range: [0.50, 1.0],
    reduce_inference_frequency: false,
    increase_cache_usage: false,
    prefer_rule_based: false,
    max_inferences_per_turn: 10,
    max_battery_cost_per_turn_mah: 5
  },
  low_battery: {
    battery_level_range: [0.20, 0.50],
    reduce_inference_frequency: true,
    increase_cache_usage: true,
    prefer_rule_based: false,
    max_inferences_per_turn: 5,
    max_battery_cost_per_turn_mah: 2
  },
  critical_battery: {
    battery_level_range: [0.0, 0.20],
    reduce_inference_frequency: true,
    increase_cache_usage: true,
    prefer_rule_based: true,
    max_inferences_per_turn: 2,
    max_battery_cost_per_turn_mah: 0.5
  }
};
```

---

## Notes for LLM Analysis

When validating AI integration schemas:

1. **Inference Time**: Target 15ms, max 50ms for all inferences
2. **Battery Cost**: Monitor and optimize for <10% drain per 30min session
3. **Confidence Thresholds**: Fallback to rules if confidence <70%
4. **Personality Ranges**: All OCEAN predictions 1.0-5.0
5. **Sentiment Scores**: All valence/arousal in range [-1, 1]
6. **Model Versions**: Track versions for reproducibility
7. **Cache Validation**: Cached results expire after reasonable time
8. **Context Completeness**: All required context fields provided

**Cross-schema dependencies**:
- PersonalityTraits from character-system (must be in valid ranges)
- EmotionalState from emotional-system (all states valid)
- CardID from card-system (referenced cards exist)
- Relationship from character-system (trust in valid range)
- ConversationDepth from character-system (valid depth levels)
- VoiceProfile from character-system (consistent voice)
- AIContext references multiple schemas for complete picture
- Generated content must pass validation-rules consistency checks

