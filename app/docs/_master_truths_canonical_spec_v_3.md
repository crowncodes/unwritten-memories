# Master Truths — Canonical Spec (v3.0)

> **Purpose**: Single source of truth for the V3 architecture - DNA → Template → Instance, Core Simulation Engines, Just-in-Time generation, and anti-gamification mandate. Every implementation **must** comply with this specification.

**Major Version Change:**
- **v3.0** (2025-10-17): Complete architectural overhaul to DNA → Template → Instance paradigm with Core Simulation Engines (ENGINE_PERSONALITY, ENGINE_CAPACITY, ENGINE_MEMORY, ENGINE_WRITERS_ROOM); introduced Just-in-Time instantiation via Contextually Filtered Pool; established Tiered Generation Strategy (T1/T2/T3); enforced anti-gamification mandate with qualitative assessment; deprecated all deterministic calculation formulas in favor of emergent outcomes; removed Essence/subscription-gated AI quality

**Previous Versions:**
- v1.2 (2025-10-14): Added emotional authenticity and novel-quality systems (now integrated into ENGINE_CAPACITY and ENGINE_WRITERS_ROOM)
- v1.1 (2025-10-13): Season length selection and relationship levels
- v1.0: Base canonical specifications

---

## 0) Game Vision & V3 Architecture

**Unwritten** is a life simulation where **every card is generated on-demand** from Master Templates, creating truly unique playthroughs through sophisticated AI-powered narrative emergence.

### The Three-Layer Architecture

```
L1: GAMEPLAY DNA (The Concepts)
    ↓ implements
L2: MASTER TEMPLATES (The Archetypes) [~300 designed]
    ↓ instantiates via context
L3: CONTEXTUAL INSTANCES (The Cards/Events) [infinite unique]
```

**Core Principle:** Unwritten does not use static decks. Cards are **Contextual Instances (L3)** generated Just-in-Time from **Master Templates (L2)** based on **Gameplay DNA (L1)** concepts and current game state.

### The Four Core Simulation Engines

**ENGINE_PERSONALITY (OCEAN Model)**
- Defines how characters perceive and respond to the world
- Traits: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
- Each trait: 0.0-1.0 continuous scale
- Acts as perceptual filter: same objective event, different subjective experience
- Modifies costs, outcomes, available options

**ENGINE_CAPACITY (Emotional Bandwidth)**
- Tracks emotional resilience: 0.0-10.0 continuous scale
- Default: 5.0 (baseline human)
- Slow-moving resource (changes over days/weeks, not turns)
- Gates perception (can't see what you're too overwhelmed to notice)
- Limits support ability: Can provide up to (Capacity + 2) level of support
- Creates authentic limitations: "I want to help, but I'm drowning myself"

**ENGINE_MEMORY (The Archive)**
- Permanent record of all played instances
- Vector DB for semantic pattern detection
- Graph DB for relationship/location associations
- Powers Memory Resonance (callbacks to emotionally significant moments)
- Enables evolution assessment (comfort patterns, reciprocity, etc.)
- Feeds Novel Generation at season end

**ENGINE_WRITERS_ROOM (The AI Director)**
- Six specialized flows: Pacing, Narrative Arc, Character State, The Critic, Director (Synthesizer), Analyst
- Assesses qualitative progression readiness (NOT numerical thresholds)
- Generates L3 Instances via Tiered Strategy
- Detects evolution opportunities through semantic analysis
- Maintains narrative tension and pacing
- Validates novel-quality thresholds

### Just-in-Time Instantiation

**The Contextually Filtered Pool (CFP):**
- Dynamic weighted probability list of Master Template IDs
- NOT a deck of cards - a probability distribution
- Updates incrementally when affected variables change
- Typical size: 50-200 templates at any given moment
- Weighted draw produces 7-card hand

**Generation Flow:**
1. CFP identifies which templates are contextually appropriate
2. Weighted draw selects template based on probabilities
3. Template + context → L3 Instance via Tiered Generation
4. Instance appears in hand (art generated asynchronously)

### Tiered Generation Strategy

**Tier 1 (Local / The Weaver):**
- Execution: On-device, local template fill
- Latency: < 100ms (instant)
- Cost: $0
- Use for: Routine, low-variance activities
- Example: "Work on Current Project"

**Tier 2 (EWR-Light / Enriched):**
- Execution: Server-side, optimized EWR call
- Latency: 1-3 seconds (masked by predictive pre-fetching)
- Cost: ~$0.003 per generation (~500 tokens)
- Use for: Social, creative, contextual activities
- Example: "Coffee with Sarah at Café Luna" (unique narrative each time)

**Tier 3 (EWR-Heavy / Narrative Direction):**
- Execution: Server-side, full semantic analysis
- Latency: 5-10 seconds (Narrative Interlude experience)
- Cost: ~$0.020 per generation (~2000 tokens)
- Use for: Major events, evolutions, fusions
- Example: Relationship breakthrough, card evolution

**Season Novel:**
- Execution: Server-side, Archive query + narrative generation
- Latency: 30-60 seconds
- Output: 2000-5000 word coherent story
- Triggers: Season completion

### Anti-Gamification Mandate

> **IF YOU CAN WRITE A WALKTHROUGH THAT SAYS "DO X 16 TIMES TO UNLOCK Y," YOU'VE FAILED.**

**Forbidden Patterns:**
- Fixed numerical thresholds for evolution ("meet 8 times")
- Deterministic formulas that can be optimized
- Grinding mechanisms where repetition without meaning works
- "Score" systems that can be farmed

**Required Patterns:**
- Qualitative assessment by ENGINE_WRITERS_ROOM
- Context-dependent timing (personality, capacity, situation matter)
- Semantic pattern detection via Vector DB
- "Interaction count is correlation, not causation"

### Monetization (V3)

**Expansion Packs:**
- Add new Master Templates (L2), not static cards
- Templates multiply value: 50 new templates = exponential narrative possibilities
- Never gate AI quality, narrative depth, or core features

**Subscriptions (Optional, cosmetic/convenience only):**
- Plus: Unlimited lifetime archives, priority generation queue
- Ultimate: Early access to expansion packs, special art styles

**Forbidden:**
- Essence tokens or AI generation limits
- Quality gating (T1 vs T3) based on payment
- Competitive advantages
- FOMO mechanics

---

## 1) Canonical Vocabulary & Nomenclature (V3)

### The Three-Layer Architecture

**L1: GAMEPLAY DNA (The Concepts)**
- Definition: Immutable, abstract building blocks
- Purpose: Defines boundaries and logic of simulation
- Count: 7 Strands
- Nature: Categories, not content
- Examples: "The Psyche", "Volitional Actions", "Catalytic Events"

**L2: MASTER TEMPLATES (The Archetypes)**
- Definition: Specific implementations of DNA concepts
- Purpose: Provides rules for generating infinite L3 instances
- Count: ~300 designed archetypes
- Nature: JSON specifications with generation rules
- Examples: `ACT_Connect_Informal_Social`, `EVT_Relationship_Crisis`

**L3: CONTEXTUAL INSTANCES (The Cards/Events)**
- Definition: Unique, moment-specific cards generated at runtime
- Purpose: Playable content with narrative texture
- Count: Infinite (procedurally generated)
- Nature: Output of Template + Context via EWR
- Examples: "Coffee with Sarah at Café Luna" (unique each playthrough)

### The Seven DNA Strands

| Strand | Name | Concept | Manifests As |
|--------|------|---------|--------------|
| **1** | The Psyche | Internal mental/emotional states | State Cards (passive modifiers) |
| **2** | Volitional Actions | Intentional activities character chooses | Action Cards (7-card hand) |
| **3** | Catalytic Events | External forces that disrupt/accelerate | System-triggered Situation Cards |
| **4** | Narrative Structure | Core motivation shaping life story | Life Directions, Aspirations |
| **5** | Social Connection | Relationships and interpersonal dynamics | NPCs (Graph DB entities) |
| **6** | Spatial Awareness | Physical locations and their meaning | Locations (Graph DB entities) |
| **7** | Progression & Artifacts | Skills, items, perks, growth | System Cards (persistent elements) |

### The Four Core Engines

**ENGINE_PERSONALITY**
- OCEAN traits: 0.0-1.0 per trait
- Acts as perceptual filter
- Modifies costs, outcomes, narrative tone

**ENGINE_CAPACITY**
- Emotional bandwidth: 0.0-10.0
- Default: 5.0 (baseline)
- Support rule: Can provide up to (Capacity + 2) level support

**ENGINE_MEMORY**
- Archive: Permanent event storage
- Vector DB: Semantic pattern detection
- Graph DB: Relationship/location networks

**ENGINE_WRITERS_ROOM**
- Six flows: Pacing, Arc, Character State, Critic, Director, Analyst
- Qualitative assessment authority
- Narrative generation orchestrator

### Time & Structure

**Turn Structure:**
- 3 turns per day (Morning / Afternoon / Evening)
- 7 days per week
- Time advances fluidly based on activity duration (not rigid phases)

**Season Structure:**
- **12 weeks (Standard)**: Focused single-goal arc
- **24 weeks (Extended)**: Complex multi-path arc
- **36 weeks (Epic)**: Transformational saga arc
- Player selects at season start
- Follows 3-act structure: Setup → Escalation → Resolution

### Relationships

**Levels: 0-5** (discrete stages)
- Level 0: Not Met (tracked internally, display as "Not Met")
- Level 1: Stranger (0-5 interactions)
- Level 2: Acquaintance (6-15 interactions)
- Level 3: Friend (16-30 interactions)
- Level 4: Close Friend (31-75 interactions)
- Level 5: Soulmate/Best Friend (76+ interactions)

**⚠️ V3 Critical Change:**
- Interaction counts are **indicators**, NOT determinants
- ENGINE_WRITERS_ROOM must assess **Journey Beats** for level-up
- High compatibility: May reach Level 3 in 10 interactions
- Low compatibility: May never reach Level 3 despite 50 interactions

**Trust: 0.0-1.0** (continuous, internal)

**Journey Beats (Required for Progression):**
- **Connection Moment** (Acquaintance → Friend)
- **Vulnerability Moment** (Friend → Close Friend)
- **Crisis Support Moment** (Close Friend → Soulmate)

**Display Format:** "Level 3 (Trust 0.62)"

### Emotional States

**Canonical Names:**
- CURIOUS, MOTIVATED, CONFIDENT, GRATEFUL
- EXHAUSTED, OVERWHELMED, ANXIOUS, VULNERABLE
- INSPIRED, DETERMINED, PEACEFUL

**Capacity-Driven:**
- States emerge from ENGINE_CAPACITY thresholds
- Capacity < 3.0 → OVERWHELMED or EXHAUSTED
- Capacity > 8.0 → CONFIDENT or INSPIRED

### Resources

**Primary Resources:**
- **Time**: Fluid progression (hours, not slots)
- **Energy**: Daily budget (typically 10 points, varies by state)
- **Money**: Liquid currency for costs
- **Emotional Capacity**: 0.0-10.0 (gates perception and support)

**NOT Resources:**
- Skills (0-10 mastery system, separate from resources)
- Perks (behavioral rewards, not currencies)
- Relationship Trust (quality metric, not spendable)

---

## 2) The Contextually Filtered Pool (CFP)

### Definition

The CFP is a **dynamic weighted probability distribution** of Master Template IDs, NOT a physical deck of cards.

### Structure

```javascript
{
  templates: [
    {
      id: "ACT_Connect_Informal_Social",
      base_probability: 0.15,
      current_weight: 0.28,  // After modifiers
      modifiers_active: ["weekend", "LONELY_state", "neglected_relationship"]
    },
    // ... 50-200 templates currently viable
  ],
  total_probability_mass: 1.0  // Always normalized
}
```

### Update Strategy

**Incremental Only:**
- When emotional state changes → Update only templates with emotional_state modifiers (15-30 templates, < 5ms)
- When time category changes → Update only templates with temporal modifiers (40-60 templates, < 8ms)
- When relationship interaction → Update only templates referencing that NPC (10-20 templates, < 3ms)

**Never:**
- Full CFP recalculation every turn
- Update templates unaffected by the specific change

### Probability Modifiers

**Structure in Template:**
```json
"probability_modifiers": {
  "emotional_states": {
    "CURIOUS": "+30%",
    "LONELY": "+40%",
    "EXHAUSTED": "-50%"
  },
  "temporal": {
    "weekend": "+25%",
    "friday_evening": "+40%"
  },
  "personality": {
    "extraversion_high": "+25%",
    "extraversion_low": "-15%"
  },
  "context": {
    "neglected_relationship": "+60%",
    "aspiration_pressure_high": "-20%"
  }
}
```

### Hand Generation

**7-Card Hand Composition:**
- 1-2 Obligation cards (auto-appear based on schedule)
- 5-6 Contextual actions (weighted draw from CFP)

**Diversity Rules:**
- No duplicate templates in single hand
- At least 1 social option (if NPCs available)
- At least 1 aspiration-related (if active aspiration)
- Balance high/low energy activities

### Predictive Pre-Fetching

**Trigger:** Hand size drops to 4 cards

**Process:**
1. Client requests CFP update from server
2. Server recalculates affected templates incrementally
3. Server performs weighted draw (3-4 templates)
4. Server instantiates via Tier 1 or Tier 2 (batched)
5. Instances sent to client buffer
6. When player plays next card → instant replenishment from buffer

**Target:** > 95% buffer hit rate (< 5% "Drawing..." moments)

---

## 3) Evolution System (V3 Qualitative Assessment)

### Evolution Stages

**Generic → Personalized → Cherished**

Each stage represents a **transformative change**, not incremental improvement.

### Generic Stage (Initial)

**Source:** Fresh instantiation from Master Template

**Example:** "Coffee with a Friend"

**Properties:**
- Generic placeholder name
- Standard mechanics
- No memory resonance
- Discardable

### Personalized Stage (Established Familiarity)

**Trigger:** ENGINE_WRITERS_ROOM detects **familiarity pattern**

**Assessment Criteria (Qualitative):**
- Consistency of connection (not count, but quality)
- Emotional reciprocity established
- Comfort level reached between parties
- Personality compatibility demonstrated
- Natural rhythm developed

**Timing Examples:**
- High compatibility: 2-3 interactions
- Neutral compatibility: 15-20 interactions
- Low compatibility: May never happen

**⚠️ Forbidden:** `if (interaction_count >= 8) { evolve(); }`

**✅ Required:** `if (ENGINE_WRITERS_ROOM.detects_familiarity_pattern()) { evolve(); }`

**Example:** "Coffee with Sarah"

**Properties:**
- NPC name attached
- Minor mechanical tweaks (-0.5 Energy cost)
- Beginning of memory resonance
- Cannot be discarded

### Cherished Stage (Transformative Moment)

**Trigger:** ENGINE_WRITERS_ROOM detects **deep emotional bond + transformative moment**

**Assessment Criteria (Qualitative):**
- Breakthrough outcome occurred during instance
- Journey Beat achieved (Vulnerability or Crisis Support)
- Emotional significance evident in both parties
- Memory resonance potential high
- Relationship reached new depth

**Required Conditions:**
- Qualitative moment (NOT "X times")
- Both emotionally present (ENGINE_CAPACITY check)
- Bond depth sufficient (assessed, not scored)

**Examples of Transformative Moments:**
- Vulnerability shared that deepened trust
- Decision made together affecting life path
- Support given during crisis proving bond
- Revelation experienced changing perspective

**Timing:** One profound conversation at 3 AM can trigger. Twenty surface meetings won't.

**Example:** "Tuesday Afternoons at Café Luna"

**Properties:**
- Fully unique name
- Significant mechanical evolution (-1 Energy, +0.3 Capacity restore)
- High memory resonance (triggers flashbacks)
- Cannot be discarded
- Golden visual frame
- Appears in Season Novel as chapter-level scene

### Evolution Assessment Method

**Vector DB Query:**
```javascript
ENGINE_WRITERS_ROOM.assess_evolution({
  interaction_history: VECTOR_DB.query("interactions_with_npc"),
  quality_indicators: ["emotional_depth", "reciprocity", "consistency"],
  transformative_moments: MEMORY.query("vulnerability_shared"),
  personality_compatibility: calculate_compatibility(char, npc),
  current_receptivity: [char.capacity, npc.capacity]
})
```

**Output:** Boolean (qualifies for evolution) + rationale

---

## 4) Journey Beats (Required for Relationship Progression)

### Core Principle

> **Relationships CANNOT progress without qualitative Journey Beats. Forced interaction without emotional presence = stalled progression.**

### The Three Primary Beats

**Connection Moment (Acquaintance → Friend)**
- Sharing personal information
- Discovering unexpected common ground
- Choosing to be present in meaningful conversation
- **Requires:** Both emotionally available (Capacity > 4.0)

**Vulnerability Moment (Friend → Close Friend)**
- One person shares deep fear, shame, or pain
- Other person responds with empathy
- **Requires:** Supporter Capacity + 2 > vulnerability level
- Emotional risk taken and honored

**Crisis Support Moment (Close Friend → Soulmate)**
- One person faces major crisis
- Other person shows up significantly
- **Requires:** Capacity + 2 rule satisfied
- Relationship proves depth through adversity

### Additional Beat Types

- **Shared Joy Moment**: Celebrating success together
- **Conflict Resolution Moment**: Fighting and repairing
- **Sacrifice Moment**: Choosing other over self-interest

### Implementation

**Journey Beat Detection:**
- ENGINE_WRITERS_ROOM identifies when beat occurred during interaction
- Archives beat in MEMORY with metadata
- Marks relationship as "beat achieved"
- Level-up check: Interaction threshold AND beat(s) achieved

**Example:**
```javascript
{
  relationship_progression: {
    current_level: 2,  // Acquaintance
    interactions: 12,
    journey_beats_achieved: ["connection_moment"],
    ready_for_level_up: true  // Has interactions AND beat
  }
}
```

---

## 5) State Cards (DNA Strand 1: The Psyche)

### Definition

State Cards are **passive modifiers**, NOT playable cards in the hand.

### Generation

**Hybrid: Procedural Trigger + AI Instantiation**

**Step 1 - Detection (Procedural):**
- ENGINE_CAPACITY: `capacity < 3.0 for 2 weeks` → trigger `STATE_Burnout`
- ENGINE_PERSONALITY: `high_neuroticism + major_stressor` → trigger `STATE_Anxious`
- Event resolution: `breakup_event` → trigger `STATE_Heartbroken`

**Step 2 - Instantiation (AI):**
- Tier 2 or 3 depending on complexity
- EWR generates specific manifestation with context
- Output: Unique State Card with narrative flavor

### Display

**Character State Panel (Separate from Hand):**
- Top of screen or sidebar
- Different visual style (darker, no action button)
- Hover for details and resolution conditions
- Max 3-5 state cards active

**Example Display:**
```
┌─ CHARACTER STATE ───────────┐
│ 😰 OVERWHELMED              │
│    +50% Energy costs         │
│    -20% Success rates        │
│                              │
│ 💔 HEARTBROKEN (8 days)     │
│    -2 Capacity              │
│    Filters out party cards   │
└──────────────────────────────┘
```

### Stacking

Multiple State Cards multiply effects:
```
Base action: 3 Energy
+ OVERWHELMED: +50% → 4.5 Energy
+ EXHAUSTED: +67% → 7.5 Energy
= Final cost: 8 Energy (rounded)
```

---

## 6) The Narrative Interlude (Embracing Tier 3 Latency)

### Purpose

Transform technical constraint (5-10s latency) into thematic feature.

### When Triggered

- Major Catalytic Event (DNA Strand 3)
- Card Evolution (Generic → Personalized → Cherished)
- Fusion opportunity detected
- Life Direction milestone
- Season climax/resolution

### Visual Design

**NOT a loading screen. A diegetic, thematic pause.**

**Elements:**
- Gentle fade from game board
- Stylized memory web animation (connecting dots)
- Reflective text: "A realization dawns...", "This is a moment you'll remember..."
- Serif typography, literary aesthetic
- Ambient, contemplative music

**Duration:** 5-10 seconds (actual EWR-Heavy processing time)

**Player Psychology:**
- Signals: "Something significant is happening"
- Builds anticipation before major moment
- Fits game's introspective, literary theme
- Feels intentional, NOT broken

### Frequency

**Target:** 2-4 times per session (30-60 min play)

**Too Frequent:** Would disrupt flow
**Too Rare:** Would lose dramatic impact

**Reserve for genuinely significant moments.**

---

## 7) Master Template Structure (L2)

### Minimum Required Fields

Every Master Template MUST include:

```json
{
  "meta": {
    "id": "ACT_Connect_Informal_Social",
    "dna_strand": "strand_2_volition",
    "tier": "routine",
    "version": "1.0.0"
  },
  
  "cfp_rules": {
    "base_probability": 0.15,
    "required_conditions": [...],
    "blocking_conditions": [...],
    "probability_modifiers": {...},
    "optimization_notes": {
      "update_frequency": "Only when affected variables change",
      "affected_by": [...]
    }
  },
  
  "instantiation": {
    "tier": 2,  // 1, 2, or 3
    "required_context": [...],
    "prompt_framework": {...},
    "cost_optimization": {...}
  },
  
  "costs": {
    "base": {...},
    "personality_modifiers": {...},
    "contextual_modifiers": {...}
  },
  
  "outcomes": {
    "success_spectrum": [...],
    "failure_spectrum": [...]
  },
  
  "evolution": {
    "stages": ["generic", "personalized", "cherished"],
    "generic_to_personalized": {
      "assessment_method": {
        "engine": "ENGINE_WRITERS_ROOM",
        "process": "Semantic analysis via Vector DB",
        "evaluates": [...]
      }
    }
  }
}
```

### Anti-Gamification Compliance

**Every template MUST:**
- Use ENGINE_WRITERS_ROOM for evolution assessment
- Define qualitative criteria (personality, capacity, context)
- Show timing variability in examples
- Explicitly state "cannot be forced through repetition"
- Include "forbidden_pattern" and "correct_pattern" examples

**Templates that include fixed numerical thresholds will be REJECTED.**

---

## 8) Canonical Constants (V3)

### Time & Structure

- Season lengths: **12w (Standard)** | **24w (Extended)** | **36w (Epic)**
- Turns per day: **3** (fluid time progression within each)
- Days per week: **7**

### Generation Tiers

- **Tier 1 latency:** < 100ms (instant)
- **Tier 2 latency:** 1-3s (masked by pre-fetch, target > 95% buffer hit rate)
- **Tier 3 latency:** 5-10s (Narrative Interlude)

### Generation Costs (Estimated)

- **Tier 1:** $0 (local)
- **Tier 2:** ~$0.003 per generation (~500 token budget)
- **Tier 3:** ~$0.020 per generation (~2000 token budget)

### Relationships

- **Levels:** 0-5 (0 = Not Met)
- **Trust:** 0.0-1.0 (continuous)
- **Journey Beats:** Required for level-up (interactions alone insufficient)

### Emotional Capacity (ENGINE_CAPACITY)

- **Scale:** 0.0-10.0 (continuous)
- **Default:** 5.0 (baseline human)
- **Low threshold:** < 5.0 (shows limitations)
- **High threshold:** ≥ 8.0 (full support available)
- **Crisis threshold:** ≤ 1.0 (cannot provide support)
- **Support rule:** Can provide up to (Capacity + 2) level support

### Personality (ENGINE_PERSONALITY)

- **Traits:** Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
- **Scale:** 0.0-1.0 per trait (continuous)

### CFP Performance

- **Update latency target:** < 10ms per incremental update
- **Typical templates affected:** 10-60 depending on change type
- **Hand replenishment target:** 0ms perceived (from buffer)
- **Pre-fetch success rate target:** > 95%

### Quality Thresholds

- **Narrative Quality Score:** ≥ 0.7 (Tier 2/3 generations)
- **Emotional Authenticity:** ≥ 0.7 (capacity constraints respected)
- **Sensory Detail:** ≥ 0.7 (grounded, specific)
- **Contextual Reference:** ≥ 0.6 (reflects game state)

---

## 9) Forbidden Patterns (V3 Enforcement)

### In Templates

**❌ FORBIDDEN:**
```json
"evolution": {
  "trigger": "played_8_times",
  "conditions": ["interaction_count >= 8"]
}
```

**✅ REQUIRED:**
```json
"evolution": {
  "assessment_method": {
    "engine": "ENGINE_WRITERS_ROOM",
    "process": "Semantic analysis of interaction history",
    "evaluates": ["comfort_pattern", "reciprocity", "compatibility"]
  },
  "timing_note": "May happen after 3 interactions (compatible) or never (incompatible)"
}
```

### In Code

**❌ FORBIDDEN:**
```dart
if (interactionCount >= 16 && trustLevel > 0.6) {
  evolveToPersonalized();
}
```

**✅ REQUIRED:**
```dart
final assessment = await ENGINE_WRITERS_ROOM.assessEvolution(
  interactionHistory: VECTOR_DB.query("interactions_with_$npcId"),
  qualityIndicators: ["emotional_depth", "reciprocity"],
  personalityCompatibility: calculateCompatibility(char, npc),
);

if (assessment.qualifiesForEvolution) {
  evolveToPersonalized(rationale: assessment.rationale);
}
```

### In Outcomes

**❌ FORBIDDEN:**
```dart
final impact = baseImpact * urgencyMultiplier * trustModifier;
return FixedOutcome(trustChange: impact);
```

**✅ REQUIRED:**
```dart
final outcome = await ENGINE_WRITERS_ROOM.determineOutcome(
  template: template,
  context: currentGameState,
  tier: template.instantiation.tier,
);

return EmergentOutcome(
  narrative: outcome.generatedNarrative,
  effects: outcome.calculatedEffects,
  rationale: outcome.assessmentRationale,
);
```

---

## 10) Deprecated Systems (V3)

### From V1.2 - NO LONGER VALID

**Deterministic Formulas:**
- ❌ NPC Response Calculator (`Response_Impact = Base × Urgency × Trust...`)
- ❌ Fixed progression thresholds
- ❌ Hardcoded `PlayerActionTypes`

**Monetization:**
- ❌ Essence tokens
- ❌ AI generation limits
- ❌ Subscription-gated quality (T1 vs T3 based on payment)

**Task-Specific AI:**
- ❌ `generateNPCDialogue()` (replaced by unified instantiation)
- ❌ `generateCardEvolution()` (replaced by unified instantiation)
- ❌ Specialized response types

**Rigid Structure:**
- ❌ Morning/Afternoon/Evening as discrete phases with slots
- ❌ Pre-generated static deck
- ❌ Fixed 3-act checkpoints

### V3 Replacements

**Unified Instantiation:**
- ✅ `instantiateTemplate(L2Template, GameContext)` via ENGINE_WRITERS_ROOM
- ✅ Tiered generation strategy (T1/T2/T3)

**Emergent Outcomes:**
- ✅ Outcome spectrums defined in templates
- ✅ ENGINE_WRITERS_ROOM determines appropriate tier
- ✅ Context-dependent effects

**Fluid Structure:**
- ✅ Time advances based on activity duration
- ✅ Just-in-Time hand generation from CFP
- ✅ Adaptive pacing (AI decides zoom vs montage)

---

## 11) Implementation Requirements (V3)

### Core Systems to Build

**1. CFP Engine**
- Incremental update logic
- Weighted probability distribution
- Hand generation with diversity rules
- Performance target: < 10ms per update

**2. EWR Service**
- Unified `instantiateTemplate()` method
- Tier routing (T1 local, T2/T3 server)
- Batch generation for pre-fetching
- Quality validation

**3. Memory Systems**
- Vector DB integration for semantic search
- Graph DB for relationships/locations
- Archive storage with metadata
- Memory Resonance queries

**4. Pre-Fetch System**
- Buffer management (3-4 cards)
- Trigger at hand size = 4
- Target: > 95% hit rate
- Fallback to T1 if buffer empty

**5. Evolution Assessment**
- Vector DB pattern detection
- ENGINE_WRITERS_ROOM qualitative evaluation
- Journey Beat tracking
- Compatibility calculation

### Data Models Required

**L2_MasterTemplate**
```dart
class L2_MasterTemplate {
  final String id;
  final DNAStrand dnaStrand;
  final CFPRules cfpRules;
  final InstantiationRules instantiation;
  final CostStructure costs;
  final OutcomeSpectrums outcomes;
  final EvolutionRules evolution;
}
```

**L3_ContextualInstance**
```dart
class L3_ContextualInstance {
  final String instanceId;
  final String templateId;
  final String title;
  final String description;
  final InstanceCosts costs;
  final EvolutionStage evolutionStage;
  final String artUrl;
  final GenerationMetadata metadata;
}
```

**GameContext**
```dart
class GameContext {
  final CharacterState character;
  final Map<String, NPCState> npcs;
  final List<StateCard> activeStates;
  final DateTime currentTime;
  final List<Aspiration> activeAspirations;
  final MemoryArchive archive;
}
```

### Services Required

**EWR_Service** (replaces FirebaseAIService)
- `instantiateTemplate()`
- `assessEvolution()`
- `determineOutcome()`
- `generateSeasonNovel()`

**CFP_Service**
- `updateCFP(changeType, changeData)`
- `drawHand()`
- `calculateWeights()`

**Memory_Service**
- `storeInteraction()`
- `queryPatterns()`
- `calculateResonance()`

**PreFetch_Service**
- `triggerPreFetch()`
- `getFromBuffer()`
- `monitorHitRate()`

---

## 12) Validation & Quality Assurance

### Template Validation Checklist

Before implementation, every template must pass:

- [ ] Anti-gamification checker (no fixed thresholds)
- [ ] CFP simulation (balance check across 20+ game states)
- [ ] Evolution integrity testing (Grinder/Natural/Incompatibility)
- [ ] Narrative quality scoring (10+ generated instances, avg ≥ 0.7)
- [ ] Cost projection (monthly cost acceptable)
- [ ] Production readiness (all required fields populated)

### Runtime Quality Validation

Every Tier 2/3 generation must validate:

- [ ] Narrative Quality Score ≥ 0.7
- [ ] Emotional Authenticity ≥ 0.7 (capacity constraints respected)
- [ ] Sensory Detail ≥ 0.7 (grounded, specific)
- [ ] Contextual Reference ≥ 0.6 (reflects game state)

**If validation fails:**
- Tier 2 → retry with Tier 3
- Tier 3 → flag for review, use fallback

### Performance Monitoring

Track and alert on:

- CFP update latency (target < 10ms)
- Pre-fetch buffer hit rate (target > 95%)
- Tier 2 generation latency (target 1-3s)
- Tier 3 generation latency (target 5-10s)
- Hand staleness index (target < 0.30)

---

## 13) V3 Compliance Checklist

Use this checklist for all new code, templates, and documentation:

**Architecture:**
- [ ] Uses three-layer architecture (DNA → Template → Instance)
- [ ] References correct layer (L1/L2/L3)
- [ ] Master Templates (L2) defined as JSON with generation rules
- [ ] Contextual Instances (L3) generated Just-in-Time

**Core Engines:**
- [ ] ENGINE_PERSONALITY used for perceptual filtering
- [ ] ENGINE_CAPACITY used for support limits and perception gates
- [ ] ENGINE_MEMORY used for pattern detection and resonance
- [ ] ENGINE_WRITERS_ROOM used for qualitative assessment

**CFP & Generation:**
- [ ] CFP treated as probability distribution, not deck
- [ ] Incremental updates only (no full recalculation)
- [ ] Appropriate tier selected (T1/T2/T3)
- [ ] Pre-fetching strategy implemented for T2

**Anti-Gamification:**
- [ ] No fixed numerical thresholds for evolution
- [ ] Qualitative assessment by ENGINE_WRITERS_ROOM
- [ ] Timing variability documented
- [ ] "Cannot be forced" explicitly stated

**Journey Beats:**
- [ ] Relationships require Journey Beats for level-up
- [ ] Interactions alone insufficient
- [ ] Beat types defined and tracked

**Forbidden Patterns:**
- [ ] No deterministic formulas (replaced by emergent outcomes)
- [ ] No Essence tokens or AI generation limits
- [ ] No hardcoded action types
- [ ] No rigid phase slots

**Scales & Vocabulary:**
- [ ] Relationships: 0-5 levels, 0.0-1.0 trust
- [ ] Capacity: 0.0-10.0 scale
- [ ] Personality: 0.0-1.0 per OCEAN trait
- [ ] Season: 12/24/36 weeks (player choice)
- [ ] Time: Fluid progression (hours, not slots)

**Quality:**
- [ ] Narrative Quality ≥ 0.7
- [ ] Emotional Authenticity ≥ 0.7
- [ ] Template validated via checklist
- [ ] Performance targets met

**This document cites:** Master Truths v3.0

---

## 14) Versioning & Change Process

### Version Numbering

**MAJOR.MINOR.PATCH**
- MAJOR: Architectural paradigm shift (e.g., 2.x → 3.0)
- MINOR: Significant feature additions
- PATCH: Clarifications, corrections, small additions

### Change Proposal (CP)

Required fields:
- **Title**: Clear, concise description
- **Rationale**: Why is this change needed?
- **Impacted Sections**: Which sections change?
- **Breaking Changes**: What becomes invalid?
- **Migration Plan**: How to update existing code/templates
- **Owner**: Who is responsible?
- **Target Release**: When will this be implemented?

### Approval Process

**Requires sign-off from:**
1. Product (vision alignment)
2. Systems/Engineering (feasibility)
3. Design (gameplay impact)

**Merge only after all three approve.**

---

## 15) Document Metadata

**Document Version:** v3.0  
**Last Updated:** October 17, 2025  
**Major Changes:** Complete architectural overhaul to DNA → Template → Instance paradigm; introduced Core Simulation Engines (ENGINE_PERSONALITY, ENGINE_CAPACITY, ENGINE_MEMORY, ENGINE_WRITERS_ROOM); established Just-in-Time instantiation via Contextually Filtered Pool; implemented Tiered Generation Strategy (T1/T2/T3); enforced anti-gamification mandate; deprecated all V1.2 deterministic systems; removed Essence/subscription-gated quality

**Supersedes:** master_truths_canonical_spec_v_1_2.md

**Authoritative References:**
- `app/docs/00-master-concept/00-INDEX.md` - Document hierarchy
- `app/docs/00-master-concept/08-template-spec.md` - Master Template JSON schema
- `app/docs/00-master-concept/09-turn-structure.md` - CFP and generation mechanics
- `app/docs/00-master-concept/10-validating-template-design.md` - Quality assurance framework

---

**This is the V3 foundation. Every line of code, every template, every design decision must trace back to these principles.**

**Let's build something extraordinary.**

