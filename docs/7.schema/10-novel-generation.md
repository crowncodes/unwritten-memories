# Novel Generation Schema

**Schema Version**: 1.0.0  
**Last Updated**: 2025-10-13  
**Dependencies**: All previous schemas (comprehensive integration)

---

## Overview

Defines the complete data structures for generating premium literary-quality novels from player game data. Includes master story context, chapter generation packets, POV perspectives, literary technique guidance, and continuity tracking.

**Reference**: See `docs/6.monetization/novel-generation-data-structure.md` for detailed implementation guide and `docs/6.monetization/premium-novel-spec.md` for literary excellence principles.

---

## 1. Master Story Context

### Complete Story Context

```typescript
/**
 * Master context provided to LLM for every chapter generation
 */
interface MasterStoryContext {
  // Story identity
  story_metadata: StoryMetadata;
  
  // Immutable established facts
  established_facts: EstablishedFact[];
  
  // All characters
  character_registry: CharacterProfile[];
  
  // Story arcs
  story_arcs: StoryArcSummary[];
  
  // Previous chapters
  previous_chapters: ChapterSummary[];
  
  // Themes
  themes: Theme[];
  
  // World state
  world_facts: WorldFact[];
  
  // Recurring elements
  recurring_elements: RecurringElement[];
  
  schema_version: SemanticVersion;
}

interface StoryMetadata {
  title: string;
  subtitle?: string;
  season_number: number;
  
  // Style
  pov_style: "second_person" | "first_person" | "close_third";
  tone: string;                     // "hopeful_introspective_authentic"
  genre_tags: string[];
  
  // Timeframe
  time_span: {
    start_week: Week;
    end_week: Week;
    total_weeks: number;
    real_world_months: number;
  };
  
  // Quality
  generation_quality: "free" | "premium";
  word_count_target: number;
  chapter_count: number;
}
```

### Established Facts

```typescript
/**
 * Immutable truths that cannot be contradicted
 */
interface EstablishedFact {
  fact_id: string;
  fact: string;                     // "Sarah has a coffee shop in Pioneer Square"
  week_established: Week;
  chapter_established?: number;
  
  // Classification
  fact_type: "character_trait" | "relationship" | "world_state" | "event" | "decision_consequence";
  importance: "critical" | "significant" | "detail";
  
  // Immutability
  immutable: boolean;
  can_evolve: boolean;              // Can change over time but not contradict
  
  // References
  referenced_in_chapters: number[];
  affects_characters: string[];
  
  // Validation
  must_be_consistent_with: string[]; // Other fact IDs
}

/**
 * Example established facts
 */
const EXAMPLE_FACTS: EstablishedFact[] = [
  {
    fact_id: "fact_001",
    fact: "You quit your corporate job in Week 24 to pursue photography full-time",
    week_established: 24,
    chapter_established: 8,
    fact_type: "decision_consequence",
    importance: "critical",
    immutable: true,
    can_evolve: false,
    referenced_in_chapters: [8, 10, 12, 15],
    affects_characters: ["player", "npc_sarah_anderson"],
    must_be_consistent_with: ["fact_005", "fact_012"]
  },
  {
    fact_id: "fact_002",
    fact: "Sarah's coffee shop 'Luna Brew' has a vintage film camera collection on display",
    week_established: 4,
    chapter_established: 2,
    fact_type: "world_state",
    importance: "detail",
    immutable: true,
    can_evolve: false,
    referenced_in_chapters: [2, 7, 14],
    affects_characters: ["npc_sarah_anderson"],
    must_be_consistent_with: []
  }
];
```

### Character Profile (For Novel)

```typescript
/**
 * Character profile for novel generation
 */
interface CharacterProfile {
  character_id: string;
  name: string;
  role_in_story: "protagonist" | "major" | "supporting" | "minor";
  
  // Core identity (immutable)
  core_identity: {
    surface_trait: string;          // How they appear
    deeper_truth: string;           // What drives them
    contradiction: string;          // Internal conflict
    wound: string;                  // Formative pain
    desire: string;                 // What they want
    fear: string;                   // What terrifies them
  };
  
  // Voice (for POV chapters)
  voice_profile: VoiceProfile;
  
  // Personality evolution
  personality_timeline: PersonalitySnapshot[];
  
  // Arc
  character_arc: {
    starting_state: string;
    ending_state: string;
    key_turning_points: Week[];
    arc_type: "positive" | "negative" | "flat" | "complex";
  };
  
  // Relationships
  key_relationships: Record<string, RelationshipSnapshot[]>;
  
  // Appearance
  visual_identity: {
    key_features: string[];         // ["freckles across nose", "cerulean scarf"]
    recurring_behaviors: string[];  // ["traces coffee rim when nervous"]
    sensory_associations: string[]; // ["smells like coffee and vanilla"]
  };
}

/**
 * Voice profile for POV narration
 */
interface VoiceProfile {
  character_id: string;
  
  // Speech patterns
  typical_sentence_structure: "short" | "medium" | "long" | "varied";
  vocabulary_level: "simple" | "moderate" | "sophisticated" | "mixed";
  verbal_tics: string[];
  catchphrases?: string[];
  
  // Thought patterns (interiority)
  internal_monologue_style: string; // "analytical and self-aware"
  metaphor_preference: string;      // "camera/photography metaphors"
  how_they_process_emotion: string; // "intellectualize first, feel later"
  
  // Sensory focus
  dominant_sense: "visual" | "auditory" | "tactile" | "olfactory" | "emotional";
  
  // POV characteristics
  observational_style: string;      // "notices details others miss"
  blind_spots: string[];           // What they don't notice
  
  // Differentiation
  distinct_from_other_povs: string; // How this POV feels different
  
  // Examples
  example_internal_thoughts: string[];
  example_dialogue: string[];
  example_observations: string[];
}
```

### Story Arc Summary

```typescript
/**
 * Story arc summary for novel context
 */
interface StoryArcSummary {
  arc_id: StoryArcID;
  arc_name: string;
  category: StoryArcCategory;
  
  // Structure
  phases: ArcPhase[];
  current_phase?: number;
  
  // Timeline
  started_week: Week;
  ended_week?: Week;
  status: "active" | "completed" | "failed";
  
  // Dramatic structure
  emotional_theme: string;
  central_question: string;         // "Will you choose security or passion?"
  
  // Key moments
  decisive_decisions: Week[];
  crisis_points: Week[];
  breakthroughs: Week[];
  
  // Resolution
  outcome?: string;
  outcome_quality?: "satisfying" | "bittersweet" | "tragic" | "triumphant";
}

interface ArcPhase {
  phase_number: number;
  phase_name: string;
  weeks: [Week, Week];
  tension: string;
  goals: string[];
  key_events: string[];
}
```

### Theme Structure

```typescript
/**
 * Thematic elements
 */
interface Theme {
  theme_id: string;
  theme_name: string;                // "The Cost of Dreams"
  
  // Expression
  how_expressed: string[];           // Scenes that express this theme
  recurring_symbols: string[];       // Objects/images that represent it
  
  // Characters
  characters_embodying: string[];    // Which characters represent this
  character_perspectives: Record<string, string>; // How each character sees this theme
  
  // Arc
  theme_evolution: {
    opening_question: string;
    complicating_factors: string[];
    resolution: string;
  };
  
  // Subtlety
  never_state_directly: boolean;     // Always show, don't tell
  trust_reader_to_notice: boolean;
}
```

---

## 2. Chapter Generation Packet

### Complete Chapter Packet

```typescript
/**
 * Everything needed to generate one chapter
 */
interface ChapterGenerationPacket {
  // Identity
  chapter_metadata: ChapterMetadata;
  
  // Master context (continuity)
  master_context: MasterStoryContext;
  
  // This chapter's content
  chapter_narrative: ChapterNarrative;
  
  // POV data
  pov_perspectives: POVPerspective[];
  
  // Literary guidance
  technique_guidance: TechniqueGuidance;
  
  // Continuity
  continuity_anchors: ContinuityAnchors;
  
  // Foreshadowing
  foreshadowing: ForeshadowingHints[];
  
  // Quality target
  quality_target: "free" | "premium";
  
  schema_version: SemanticVersion;
}

interface ChapterMetadata {
  chapter_number: number;
  title: string;
  weeks_covered: Week[];
  
  // POV
  primary_pov: string;              // Character ID
  secondary_povs?: string[];        // If multi-POV chapter
  pov_switches?: POVSwitch[];
  
  // Structure
  act_placement: {
    act: 1 | 2 | 3;
    position_in_act: "early" | "middle" | "late";
    narrative_function: string;     // "Setup conflict", "Climax"
  };
  
  // Purpose
  chapter_purpose: string;
  emotional_arc: string;            // "Discouraged → Crisis → Determination"
  
  // Specs
  target_word_count: number;
  pacing: "fast" | "moderate" | "slow";
  sensory_emphasis: string[];       // Which senses to emphasize
}

interface POVSwitch {
  switch_at_word_count: number;
  from_character: string;
  to_character: string;
  transition_type: "scene_break" | "smooth" | "abrupt";
  reason: string;
}
```

### Chapter Narrative

```typescript
/**
 * The narrative content of this chapter
 */
interface ChapterNarrative {
  // Scenes
  scenes: Scene[];
  
  // Key moments
  decisive_moments: DecisiveMoment[];
  emotional_beats: EmotionalBeat[];
  
  // Conflict
  conflict_sources: ConflictSource[];
  tension_level: Intensity;
  
  // Relationships
  relationship_moments: RelationshipMoment[];
  
  // Stakes
  what_s_at_stake: string;
  urgency_level: Intensity;
}

interface Scene {
  scene_id: string;
  scene_purpose: string;
  
  // Structure
  anchor: string;                   // Opening orientation
  action: string[];                 // What happens
  reaction: string[];               // Character responses
  complication: string;             // What goes wrong/changes
  decision: string;                 // Choice made
  new_tension: string;              // What's unresolved
  
  // Setting
  location: string;
  time_of_day: TimeOfDay;
  atmosphere: string;
  sensory_details: SensorySnapshot;
  
  // Characters
  characters_present: string[];
  pov_character: string;
  
  // Content
  dialogue_beats: DialogueBeat[];
  action_beats: ActionBeat[];
  interiority_beats: InteriorityBeat[];
  
  // Pacing
  scene_pacing: "fast" | "moderate" | "slow";
  estimated_word_count: number;
}

interface DecisiveMoment {
  moment_id: string;
  week: Week;
  description: string;
  
  // Choice
  choice_made: string;
  alternatives_rejected: string[];
  
  // Weight
  emotional_weight: Intensity;
  narrative_significance: Intensity;
  irreversible: boolean;
  
  // Impact
  immediate_consequences: string[];
  future_implications: string[];
  
  // Presentation
  show_internal_debate: boolean;
  time_pressure: boolean;
  physical_manifestation: string;   // How choice shows in body
}
```

### POV Perspective

```typescript
/**
 * Complete POV perspective for a character
 */
interface POVPerspective {
  character_id: string;
  character_name: string;
  is_primary_pov: boolean;
  
  // Voice
  voice_profile: VoiceProfile;
  
  // State
  emotional_state: EmotionalState;
  physical_state: string;
  mental_state: string;
  
  // Knowledge
  knows_about: string[];
  unaware_of: string[];
  suspects_but_uncertain: string[];
  misunderstandings: string[];
  
  // Desires & Fears
  wants_this_chapter: string;
  fears_this_chapter: string;
  internal_conflict: string;
  
  // Relationships (their perspective)
  how_they_see_others: Record<string, string>;
  relationship_tensions: string[];
  
  // Memory
  memories_triggered: string[];
  what_reminds_them: string[];
  
  // Sensory focus
  what_they_notice: string[];
  what_they_miss: string[];
  dominant_sensory_impressions: SensorySnapshot;
}
```

---

## 3. Literary Technique Guidance

### Technique Instructions

```typescript
/**
 * Literary technique guidance for this chapter
 */
interface TechniqueGuidance {
  // Core principles
  show_dont_tell_examples: ShowDontTellExample[];
  
  // Tension
  tension_architecture: {
    micro_tension_every_paragraph: string[];
    macro_tension: string;
    unanswered_questions: string[];
  };
  
  // Character depth
  character_techniques: {
    interiority_moments: number;    // How many internal thought passages
    contradiction_to_show: string;  // Which contradiction to highlight
    subtext_in_dialogue: string[];
  };
  
  // Sensory
  sensory_requirements: {
    visual_details_per_scene: number;
    other_senses_ratio: Percentage;
    avoid_visual_only: boolean;
  };
  
  // Pacing
  pacing_guidance: {
    sentence_variation: "high" | "moderate" | "low";
    paragraph_length_target: string;
    white_space_usage: string;
    action_to_reflection_ratio: string;
  };
  
  // Subtext
  subtext_layers: SubtextLayer[];
  
  // Callbacks
  callbacks_to_plant: CallbackSeed[];
  callbacks_to_pay_off: CallbackPayoff[];
  
  // Opening & ending
  opening_technique: string;
  ending_hook: string;
}

interface ShowDontTellExample {
  dont_tell: string;                // "Sarah was nervous"
  show_instead: string[];           // ["traces coffee rim", "shifts weight"]
}

interface SubtextLayer {
  surface_level: string;            // What's said/done
  subtext_level: string;            // What's really meant
  how_to_convey: string;            // Technique to show subtext
}

interface CallbackSeed {
  callback_id: string;
  plant_in_this_chapter: string;    // Small detail to include
  will_pay_off_in_chapter: number;
  significance: string;
}

interface CallbackPayoff {
  callback_id: string;
  planted_in_chapter: number;
  original_detail: string;
  how_to_reference: string;
  emotional_resonance: string;
}
```

---

## 4. Continuity & Consistency

### Continuity Anchors

```typescript
/**
 * Anchors to maintain continuity
 */
interface ContinuityAnchors {
  // From previous chapter
  carry_forward: {
    unresolved_tension: string;
    emotional_state: EmotionalState;
    pending_consequences: string[];
    relationship_status: Record<string, string>;
  };
  
  // For next chapter
  setup_for_next: {
    plant_these_details: string[];
    foreshadow_events: string[];
    establish_facts: EstablishedFact[];
  };
  
  // Consistency checks
  must_reference: string[];         // Facts that must be acknowledged
  cannot_contradict: string[];      // Facts that cannot be changed
  character_voices_consistent: string[];
  
  // Timeline
  previous_chapter_ended: {
    week: Week;
    time_of_day: TimeOfDay;
    location: string;
  };
  this_chapter_starts: {
    week: Week;
    time_of_day: TimeOfDay;
    location: string;
    time_gap_explanation?: string;
  };
}
```

### Foreshadowing

```typescript
/**
 * Foreshadowing hints for future chapters
 */
interface ForeshadowingHints {
  foreshadow_id: string;
  pays_off_in_chapter: number;
  
  // What to foreshadow
  future_event: string;
  how_to_hint: string[];            // Subtle ways to suggest it
  
  // Technique
  foreshadowing_method: "dialogue_hint" | "object_placement" | "weather_mood" | "character_unease" | "symbolic";
  subtlety_level: "very_subtle" | "moderate" | "clear";
  
  // Validation
  must_not_be_obvious: boolean;
  reader_should_miss_first_time: boolean;
}
```

---

## 5. Generated Chapter Output

### Chapter Output Structure

```typescript
/**
 * Generated chapter output
 */
interface GeneratedChapter {
  generation_id: string;
  chapter_number: number;
  
  // Content
  title: string;
  content: string;                  // The actual prose
  word_count: number;
  
  // Metadata
  generated_at: ISO8601String;
  generation_model: string;
  generation_quality: "free" | "premium";
  
  // Structure
  scenes_included: string[];
  povs_used: string[];
  techniques_applied: string[];
  
  // Quality metrics
  quality_score: Percentage;
  consistency_score: Percentage;
  literary_technique_score: Percentage;
  
  // Validation
  passed_validation: boolean;
  validation_issues: ValidationIssue[];
  
  // Costs
  essence_cost: number;
  generation_time_seconds: number;
  
  // Tracking
  callbacks_planted: string[];
  callbacks_paid_off: string[];
  facts_established: EstablishedFact[];
  
  schema_version: SemanticVersion;
}

interface ValidationIssue {
  issue_type: "contradiction" | "voice_inconsistency" | "timeline_error" | "character_error" | "fact_error";
  severity: "critical" | "moderate" | "minor";
  description: string;
  location_in_text: string;
  suggested_fix: string;
}
```

---

## 6. Book Assembly

### Complete Book Structure

```typescript
/**
 * Assembled complete book
 */
interface AssembledBook {
  book_id: string;
  season_id: SeasonID;
  player_id: PlayerID;
  
  // Metadata
  title: string;
  subtitle?: string;
  author: string;                   // Player name or pseudonym
  
  // Content
  chapters: GeneratedChapter[];
  total_chapters: number;
  total_word_count: number;
  
  // Quality
  generation_quality: "free" | "premium";
  overall_quality_score: Percentage;
  
  // Structure
  act_breaks: number[];             // Chapter numbers where acts change
  
  // Front matter
  dedication?: string;
  epigraph?: string;
  
  // Generated elements
  generated_at: ISO8601String;
  generation_time_total_minutes: number;
  total_essence_cost: number;
  
  // Export formats
  available_formats: ("epub" | "pdf" | "mobi" | "txt")[];
  
  // Metadata for book
  genre_tags: string[];
  content_warnings: string[];
  reading_time_minutes: number;
  
  schema_version: SemanticVersion;
}
```

---

## Notes for LLM Analysis

When validating novel generation schemas:

1. **Master Context**: Always includes all established facts, character profiles, previous chapters
2. **Continuity**: Every fact ID must be unique, no contradictions allowed
3. **Voice Consistency**: Each character has distinct voice profile
4. **POV Switches**: Clearly marked with transition types
5. **Technique Guidance**: Specific, actionable instructions for literary quality
6. **Word Counts**: Free tier 3-5K words, premium tier 12-15K words
7. **Quality Scores**: Track consistency, literary technique, overall quality
8. **Callbacks**: Must track planted seeds and payoffs across chapters
9. **Foreshadowing**: Subtle hints that pay off later
10. **Sensory Balance**: Not just visual - all senses represented

**Cross-schema dependencies**:
- All game data from previous schemas feeds into MasterStoryContext
- CharacterProfile pulls from character-system (personality, relationships, memory)
- StoryArcSummary from narrative-system (arcs, decisions, timeline)
- EmotionalState from emotional-system (emotional journey tracking)
- Week and temporal data from gameplay-mechanics
- Quality tier from monetization-schema (free vs premium)
- Archive data from archive-persistence (season summaries)
- Theme extraction from narrative-system memory significance
- Sensory details from narrative-system SensorySnapshot
- Relationship evolution from character-system relationship history

