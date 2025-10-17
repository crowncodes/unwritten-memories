# Card System Architecture

**Document Status**: V3 Canonical Reference  
**Last Updated**: October 17, 2025  
**Authority Level**: Master Truth  
**Compliance**: Master Truths v3.0 (anti-gamification, qualitative evolution)

---

## 1. Core Philosophy: Templates, Not Cards

### The Paradigm Shift

**OLD THINKING (V1):**
- Create 500 static, predefined cards
- Each card is handwritten and fixed
- Expansions add more static cards

**NEW THINKING (V2):**
- Create ~300 Master Templates
- Templates are "DNA" or "schematics" for concepts
- Story Weaver instantiates unique cards from templates per playthrough
- Expansions add new templates = exponential narrative value

### Why This Matters

**Traditional Approach:**
- 500 cards = 500 possible experiences
- Player sees the same content every playthrough
- Limited replayability

**Template Approach:**
- 300 templates × contextual instantiation = infinite variations
- Every playthrough generates unique, personalized cards
- True infinite replayability

---

## 2. The Seven-Tier Structure

### Tier 1: Foundation (9 Cards)
**Life Direction Cards** - "The Why"

- Defines character's core motivation
- One active per lifetime
- Reshapes entire card pool composition
- Examples: `ld_financial_security`, `ld_discover_self`, `ld_creative_fulfillment`

**Key Properties:**
- Never drawn randomly
- Chosen during character creation
- Persists entire lifetime
- Filters all other card availability

---

### Tier 2: Quest (82 Cards)
**Aspiration Cards** - "The What"

- Season-defining goals (40 Major, 42 Minor templates)
- 3-5 active per season
- Each has structured milestone progression
- Examples: `asp_get_promotion_senior`, `asp_learn_spanish_basics`

**Key Properties:**
- Not drawn—displayed in dedicated Season Goals UI
- Progress tracked via milestone system
- Completion triggers major narrative beats
- Success/failure spectrum (not binary)

---

### Tier 3: Routine (20 Cards)
**Routine Cards** - "The Daily Rhythm"

- Weekly/monthly recurring activities
- Not drawn—auto-execute on schedule
- Low narrative weight but high authenticity value
- Examples: `rout_family_call_weekly`, `rout_meal_prep_sunday`

**Key Properties:**
- Background maintenance activities
- Generate minor "routine breach" events when skipped
- Can evolve into significant traditions
- Low time/energy cost

---

### Tier 4: Action (150 Cards)
**Activity Cards** - "The How"

- The core gameplay loop
- **7-card hand**, drawn from filtered pool
- Categorized by function (Social, Productive, Restorative, Challenge, Exploration)
- Examples: `act_coffee_with_friend`, `act_gym_workout`, `act_difficult_work_project`

**Key Properties:**
- **This is what the player does most**
- Time/Energy/Money costs vary widely
- Primary vector for card evolution
- Can become Routines or fuse into unique memories

---

### Tier 5: Catalyst (60 Cards)
**Situation Cards** - "The Unexpected"

- System-generated narrative events
- Not drawn—triggered by Story Weaver AI
- Present branching choices with consequences
- Examples: `evt_health_crisis`, `evt_unexpected_opportunity`, `evt_relationship_conflict`

**Key Properties:**
- Generated, not random
- Based on Writers Room analysis
- Major narrative turning points
- Require player choice/response

---

### Tier 6: System (70 Cards)
**Skills, Items, Perks** - "The Tools"

- Not drawn—persistent character elements
- **Skills** (30): `skill_cooking`, `skill_photography`
- **Items** (30): `item_laptop`, `item_professional_camera`
- **Perks** (10): `perk_resilient`, `perk_morning_person`

**Key Properties:**
- Passive modifiers or action unlocks
- Skills have 0-10 mastery progression
- Items can be lost/broken (narrative weight)
- Perks earned through sustained behavior

---

### Tier 7: Living World (80 Cards)
**Characters & Locations** - "The Who & Where"

- **Characters** (50 templates): NPCs with own lives and Capacity
- **Locations** (30 templates): Places that accrue meaning
- Examples: `char_mentor_professional`, `loc_favorite_cafe`

**Key Properties:**
- Start generic, become deeply personal
- Evolve through memory accumulation
- Characters have independent agency and limits
- Locations transform based on events experienced there

---

## 3. The Three Card Types

### Type 1: Action Cards
**"The Verbs of Life"**

**What They Are:**
- Player-initiated activities
- Drawn randomly from filtered pool
- **Always maintain 7-card hand**

**How They Work:**
1. End of turn: discard all unused cards
2. Draw new hand from contextually filtered pool
3. Pool shaped by: Life Direction, personality, current State Cards, time of day, NPCs available

**Evolution Vector:**
- Generic → Specific → Cherished
- `act_coffee_with_friend` → `Coffee with Sarah` → `Tuesday Afternoons at Café Luna`

---

### Type 2: Situation Cards
**"The Plot Twists"**

**What They Are:**
- AI-generated narrative events
- Not drawn—**triggered by Writers Room**
- Present meaningful choices with consequences

**How They Work:**
1. Writers Room analyzes game state
2. Identifies need for Crisis/Opportunity/Complication
3. Generates custom Situation Card
4. Player makes choice
5. Consequences update character state and available cards

**Generation Triggers:**
- Pacing Specialist: "Story is flat, inject intrigue"
- Arc Specialist: "Need complication for Act 2"
- Character Specialist: "Capacity critically low, needs intervention"
- The Critic: "Predictable, inject surprise"

---

### Type 3: State Cards
**"The Conditions"**

**What They Are:**
- Passive status effects
- System-generated, not drawn
- Displayed in dedicated UI panel

**Examples:**
- `STATE_OVERWHELMED`: +50% Energy cost, -20% success rate
- `STATE_GRIEVING`: Filters card pool toward restorative activities
- `STATE_INJURED`: Locks physical activities
- `STATE_DRAINED`: In Energy Debt, each action increases exhaustion

**How They Work:**
- Applied by events or threshold triggers
- Persist until resolved (time, events, or player actions)
- Stack multiplicatively (multiple states compound effects)
- Visible, persistent UI presence

---

## 4. Master Template Structure

### What a Template Contains

Every Master Template is a structured JSON schema with:

```json
{
  "template_id": "act_base_connect_socially",
  "tier": 4,
  "category": "social",
  
  "instantiation_rules": {
    "context_variables": ["character_age", "personality_extraversion", "current_relationships", "location_pool"],
    "generation_prompt": "Generate a social connection activity appropriate for [age], [personality], at [location]",
    "flavor_examples": ["Coffee meetup", "Dinner party", "Study group", "Book club"]
  },
  
  "base_mechanics": {
    "time_cost": {"min": 1.5, "max": 3.0, "unit": "hours"},
    "energy_cost": {"min": 1, "max": 2},
    "money_cost": {"min": 10, "max": 30, "currency": "USD"}
  },
  
  "personality_modifiers": {
    "high_extraversion": {"energy_cost": -0.5, "success_bonus": 0.2},
    "low_extraversion": {"energy_cost": +1.0, "success_penalty": 0.1}
  },
  
  "evolution": {
    "stages": ["generic", "personalized", "cherished"],
    "generic_to_personalized": {
      "assessment_method": {
        "engine": "ENGINE_WRITERS_ROOM",
        "process": "Semantic analysis via Vector DB",
        "evaluates": [
          "consistency_of_connection",
          "emotional_reciprocity",
          "comfort_pattern",
          "personality_compatibility"
        ]
      },
      "timing_note": "May happen after 2-3 interactions (high compatibility) or never (incompatible)"
    },
    "personalized_to_cherished": {
      "assessment_method": {
        "engine": "ENGINE_WRITERS_ROOM",
        "process": "Transformative moment detection",
        "evaluates": [
          "breakthrough_outcome_occurred",
          "journey_beat_achieved",
          "emotional_significance",
          "memory_resonance_potential"
        ]
      },
      "timing_note": "One profound moment can trigger; twenty surface meetings won't"
    }
  },
  
  "fusion_tags": ["routine_candidate", "social_bonding", "low_stakes"],
  
  "narrative_hooks": [
    "Opportunity for unexpected encounter",
    "Setting for vulnerable conversation",
    "Routine that can be disrupted for drama"
  ]
}
```

---

## 5. Card Filtering & Pool Management

### The Dynamic Pool System

**Players never see the full 300+ card templates**

The Story Weaver maintains a **Contextually Filtered Pool** that shapes what gets drawn:

#### Filter 1: Life Direction
- Active Life Direction sets baseline card frequencies
- `ld_creative_fulfillment`: +60% creative activities, -40% corporate activities
- `ld_discover_self`: +50% introspective/exploration, -30% relationship focus

#### Filter 2: Personality
- OCEAN traits boost/reduce card availability
- High Openness: +exploration, +creative, +risk-taking activities
- Low Conscientiousness: -long-term planning, -routine maintenance

#### Filter 3: Current State Cards
- `STATE_OVERWHELMED`: Filters toward restorative, filters out high-energy
- `STATE_GRIEVING`: Boosts introspective, reduces social
- `STATE_INSPIRED`: Increases creative opportunities

#### Filter 4: Contextual Availability
- Time of day: "Late Night" filters out work activities
- NPCs present: Social activities only available if NPCs are free
- Skills unlocked: Advanced activities gated by skill levels

#### Filter 5: Narrative Needs (Writers Room)
- Pacing Specialist can inject specific card types
- "Need intrigue" → boost exploration/risk activities
- "Need respite" → boost restorative activities

---

## 6. Card Evolution System

### The Three Evolution Stages

#### Stage 1: Generic Template Instance
**"A Coffee with a Friend"**
- Fresh instantiation from master template
- Generic placeholder name
- Standard mechanics
- No memory resonance

#### Stage 2: Personalized Instance
**"Coffee with Sarah"**
- **Trigger**: ENGINE_WRITERS_ROOM detects **familiarity pattern** (qualitative assessment)
- Assessment evaluates: consistency of connection, emotional reciprocity, comfort level, personality compatibility
- **Timing varies**: High compatibility may trigger after 2-3 interactions; low compatibility may never happen
- NPC's name permanently attached
- Minor mechanical tweaks based on that NPC's traits (-0.5 Energy cost)
- Beginning of memory resonance
- Cannot be discarded

#### Stage 3: Cherished Memory
**"Tuesday Afternoons at Café Luna"**
- **Trigger**: ENGINE_WRITERS_ROOM detects **deep emotional bond + transformative moment**
- Assessment evaluates: breakthrough outcome, Journey Beat achieved, emotional significance, memory resonance potential
- **Timing**: One profound 3 AM conversation can trigger; twenty surface meetings won't
- Fully unique card with custom name
- Significant mechanical evolution (-1 Energy, +0.3 Capacity restore)
- High memory resonance (triggers flashbacks, referenced in narration)
- Golden visual frame
- Can never be discarded
- Appears in Season Novel as chapter-level scene

### Evolution Requirements

**⚠️ V3 CRITICAL: No Fixed Numerical Thresholds**

Evolution requires **qualitative assessment by ENGINE_WRITERS_ROOM**, NOT repetition counts.

**❌ FORBIDDEN:** `if (interaction_count >= 8) { evolve(); }`

**✅ REQUIRED:** `if (ENGINE_WRITERS_ROOM.detects_familiarity_pattern()) { evolve(); }`

**Assessment Method:**
- Vector DB query of interaction history
- Semantic analysis of emotional depth, reciprocity, consistency
- Personality compatibility calculation
- Current receptivity check (both characters' Capacity)
- Transformative moment detection

**This prevents grindable relationships and ensures evolution emerges from authentic connection, not farming interactions.**

---

## 7. Card Fusion System

### What Is Fusion?

**When two separate cards merge into a unique, emergent memory.**

#### Example: The Breakup Mug

**Ingredients:**
- `item_coffee_mug` (a random item card)
- `evt_relationship_breakup` (a crisis event)

**Context:**
- The breakup happens while the character is holding the mug
- AI identifies symbolic opportunity

**Result:**
- `item_coffee_mug` transforms → `item_shattered_mug_memory`
- New card text: "The mug Sarah threw during the fight. You kept the pieces."
- Mechanical effect: -1 Capacity when in inventory (painful reminder)
- Memory resonance: Triggers flashback text when drawn or seen

### Fusion Detection: During Tier 3 High-Intensity Events Only

**Fusion Timing Clarification:**
```
Fusion Detection: During Tier 3 high-intensity events ONLY

When: Major Catalytic Event (breakup, death, profound realization)
How: EWR performs semantic resonance check via Vector DB
If threshold met: Narrative Interlude triggered
Process: Parallel processing (dialogue + EWR + art generation)
Output: New fused entity with unique symbolic meaning
```

Fusion is **AI-detected**, not player-initiated. The Story Weaver identifies opportunities based on:

1. **Narrative tags alignment** (e.g., both cards tagged with "vulnerability")
2. **Contextual co-occurrence** (both active during same scene)
3. **Emotional intensity** (high-stakes Tier 3 moment required)
4. **Symbolic potential** (AI recognizes metaphoric connection via Vector DB clustering)

### Why Fusion Matters

Fusion creates **emergent storytelling artifacts** that are:
- Totally unique to that playthrough
- Impossible to predict or plan
- Deeply personal and memorable
- Evidence of the AI's literary creativity

---

## 8. The Archive: Permanent Memory

### What Gets Archived

**Every played card is permanently recorded:**
- When it was played
- What the outcome was
- What the character was feeling (Capacity level)
- What was happening in their life (active State Cards, Aspirations)
- Narrative metadata (themes, symbolism, arc notes)

**When card resolves with memory_weight >= 5:**

**Primary Facet (Visible in Archive UI):**
  - Core emotional takeaway
  - 1-2 sentence summary
  - Weight: 5-10
  - Player sees this in day recaps and Archive queries

**Sensory Facets (Backend):**
  - 2-4 ambient details
  - Trigger conditions for future resonance
  - Weight: 2-5 each
  - Used by EWR to trigger memory recall via similar sensory cues

**Observational Facets (Backend):**
  - 1-3 intrigue hooks or mysteries
  - Tags for future event generation
  - Weight: 3-6 each
  - Reviewed during Weekly EWR Narrative Analysis for pattern detection

### Why the Archive Matters

**The Archive is not a trophy case—it's the game's long-term memory.**

It enables:

1. **Memory Resonance**: Future events reference past experiences
   - "This crisis reminds you of when..."
   - "Sarah's words echo what your mentor once said..."

2. **Novel Weaver**: End-of-life story generation
   - AI queries Archive to write coherent, thematically rich life story
   - Identifies patterns, turning points, character development

3. **Season Recaps**: Inter-season narrative bridges
   - "Last season, you learned..." transitions

4. **Dramatic Irony**: System tracks what character knows vs. player knows

### Archive Query System

The Story Weaver constantly queries the Archive using **Facet-based queries**:

```
"Find: Primary Facets where emotional_weight > 8"
"Find: All Observational Facets tagged 'secrecy' involving Sarah"
"Find: Sensory Facets matching 'golden afternoon light'"
"Find: All times character faced financial crisis"
"Find: All conversations with mentor about career doubt"
"Find: Patterns in how character handles conflict"
"Find: Themes of 'ambition vs. connection' in character's choices"
```

**Facet-Based Query Examples:**

```
Query: "Find: All Observational Facets from past 7 days"
Use: Weekly EWR Narrative Analysis for pattern detection

Query: "Find: Sensory Facets matching 'cafe' + 'afternoon'"
Use: Trigger memory resonance when similar sensory context occurs

Query: "Find: Primary Facets involving Sarah where weight > 7"
Use: Understand core relationship moments for future narrative
```

These queries inform narrative generation, making every new event feel connected to the character's history. Sensory Facets create "Proustian moments" where ambient details trigger emotional recall.

---

## 9. Critical Design Rules

### Rule 1: No Pure RNG
- Card draw is **filtered**, not random
- Situation Cards are **generated**, not pulled from deck
- Evolution is **earned**, not luck-based

### Rule 2: Every Card Can Matter
- Even a generic `act_gym_workout` can evolve
- Even a mundane `item_coffee_mug` can become a cherished artifact
- No "vendor trash" or "filler" cards

### Rule 3: Respect Player Investment
- Evolved cards can never be accidentally discarded
- Cherished memories persist across seasons
- The Archive is permanent and sacred

### Rule 4: Context Is Everything
- Same template instantiates differently per playthrough
- Same card plays differently based on character state
- Same NPC interaction has different options based on Capacity

### Rule 5: Authenticity Over Balance
- Cards don't need to be "balanced" mechanically
- Some choices are objectively worse—that's life
- Failure and loss are part of the narrative, not design flaws

---

## 10. Expansion Strategy

### How New Templates Add Value

**300 base templates + 50 expansion templates ≠ 350 total stories**

**It equals:**
- New fusion opportunities with all existing cards
- New evolution branches for existing archetypes
- New narrative threads the Writers Room can weave
- **Multiplicative, not additive value**

### Example: "Parenthood" Expansion

**Adds 50 new templates:**
- 15 Parenting Activity cards
- 10 Family Situation cards
- 5 Child Character archetypes
- 5 New Skills (Patience, First Aid, etc.)
- 15 New Aspirations

**Impacts all existing content:**
- Existing relationship cards gain "parenting together" evolution paths
- Existing career cards gain "work-life balance" tension mechanics
- Existing crisis events gain "how this affects the child" consequences
- Existing locations gain "family-friendly" transformation options

**Result: Exponential narrative expansion.**

---

## Conclusion

The card system is the **narrative DNA** of Unwritten. It's designed from the ground up for:

- **Infinite replayability** through procedural instantiation
- **Emotional authenticity** through context-aware filtering
- **Literary depth** through evolution and fusion
- **Player investment** through persistent memory

Every card is a potential memory. Every memory tells the story of a life truly lived.

