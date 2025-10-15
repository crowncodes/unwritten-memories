# Master Truths — Canonical Spec (v1.2)

> **Purpose**: Single source of truth for systems, vocabulary, and guardrails. Every new or updated doc **must** comply with this page or explicitly propose a change via the process below.

**Changelog:**
- **v1.2** (2025-10-14): Added Emotional Authenticity System (Section 16) and Novel-Quality Narrative Systems (Section 17); added NPC Response Framework to Section 11 (personality-driven responses with situational multipliers); updated Sections 2, 11, 13, and 15 to include emotional capacity, tension injection, memory resonance, and quality validation standards; enhanced Section 0 (Game Vision) with visual generation system details
- **v1.1** (2025-10-13): Clarified season length selection (12/24/36 weeks, player choice) and relationship levels (0-5 with Level 0 = "Not Met")
- **v1.0** (Initial): Base canonical specifications

---

## 0) Game Vision & Core Description

**Unwritten** is a sophisticated card-based life simulation game that combines AI-powered narrative generation with on-device visual synthesis to create deeply personalized, evolving stories. Each playthrough is a unique literary experience where player choices reshape both the narrative and the visual representation of their character's world.

### Core Game Loop

**Season Structure**: Players define a life goal (aspiration) and navigate 12, 24, or 36 weeks of decision-making across 3 turns per day (Morning/Afternoon/Evening). Each season follows a classic 3-act narrative structure:
- **Act I (SETUP)**: Establish goals, relationships, and foundations
- **Act II (CLIMAX)**: Face complications, escalating challenges, and decisive moments
- **Act III (RESOLUTION)**: Experience consequences, achieve closure, and witness transformation

**Card-Driven Gameplay**: Cards represent atomic units of a player's life—people, places, activities, aspirations, routines, and items. Players select cards each turn to progress toward goals, build relationships, develop skills, and navigate life's complexities. Cards are not static: they **evolve** based on player actions, relationship progression, and narrative context.

### AI-Powered Visual Generation

**On-Device TensorFlow Lite Models**: All visual generation happens locally for privacy, speed, and offline capability.

**Dynamic Visual Content**:
- **Character Portraits**: NPCs visually evolve as relationships deepen (Level 0-5 progression)
- **Location Art**: Places transform based on season, time of day, and narrative events
- **Card Visuals**: Every card generates contextually appropriate imagery reflecting current state
- **Emotional States**: Visual representation adapts to character emotional capacity and mood

**Context Integration**: Visual generation system integrates with:
- **Personality Modeling** (OCEAN traits): Character appearance reflects personality
- **Emotional State Tracking**: Capacity (0-10 scale) influences visual mood and expression
- **Relationship Progression**: Visual intimacy and detail increase with relationship levels
- **Narrative Tension**: Visual cues for mystery hooks, stakes escalation, and dramatic moments
- **Memory Resonance**: Visual callbacks to emotionally significant past events

### Card Evolution & Narrative Emergence

**Living Cards**: Cards transform through usage and context:
- **Relationship cards** evolve as trust (0.0-1.0) and level (0-5) progress
- **Activity cards** unlock new variants based on skill development and emotional growth
- **Location cards** change appearance based on season, weather, and story beats
- **Aspiration cards** morph as goals shift or crystallize

**Mid-Season Pivots**: Player choices can fundamentally redirect goals—what starts as "Get Promoted" may transform into "Start My Own Business" or "Realize Work Isn't Everything" based on authentic character development and relationship dynamics.

**Unique Season Archives**: At season's end, the player possesses a **completely unique deck** shaped by their specific choices, relationship paths, and emotional journey. No two playthroughs generate identical cards.

### Novel Generation System

**Literary Output**: Each completed season generates a **short novel** (novella-length) capturing the character's journey. The novel:
- Uses the evolved card deck as narrative anchors
- Incorporates relationship progression, emotional authenticity, and decisive moments
- Meets **novel-quality thresholds** (≥ 0.7 overall quality; ≥ 0.7 emotional authenticity)
- Reflects tension building, dramatic irony, and memory resonance systems
- Provides narrative closure while seeding future season possibilities

### Multi-Season Lifetimes

**Lifetime Progression**: Players can continue a character across **up to 8 seasons** (maximum), creating a multi-book saga:
- **Continuity**: Relationship levels, trust, NPC memories, and key outcomes persist
- **Consequences**: Decisive decisions from Season 1 ripple through Season 8
- **Character Growth**: Long-term emotional capacity development and personality evolution
- **Archive System**: Unlimited season archives (free tier); unlimited lifetime archives (Plus/Ultimate)

**Each Season = Self-Contained Arc**: While continuity persists, every season provides complete narrative closure. Players can end a character's story after any season without cliffhangers.

### Design Philosophy

**Player-First, Story-Deep**: 
- No predatory mechanics, FOMO, or anxiety farming
- Decisions pause time—players have space to reflect
- Battery life and performance are primary metrics (60 FPS, <15ms AI inference, <10% battery per 30min)
- On-device AI ensures privacy and offline play
- DLC adds narrative possibilities, never power or competitive advantage

**Emotional Authenticity Over Game Logic**:
- NPCs respond within realistic human limitations (emotional capacity constraints)
- No "perfect NPC" behaviors—characters at 2.5/10 capacity cannot provide 8/10 support
- Dramatic irony creates "yelling at screen" tension through knowledge gaps
- Memory resonance prioritizes emotional impact over recency

**Novel-Quality Narrative**:
- Tension injection framework maintains engagement ("one more week" pull)
- Mystery hooks, partial reveals, contradictions, and stakes escalation
- Literary dialogue over game-speak ("I want to help, but I'm drowning myself right now")
- Quality validation ensures every generation meets authorial standards

---

## 1) Core Principles
- **Player-first**: No predatory mechanics; decisions matter, not anxiety farming.
- **Stories with closure**: Each **Season** is a complete 3‑act arc; choices echo across seasons and lifetimes.
- **Additive content**: DLC adds possibilities, not power. No RNG/gacha. No pay-to-win.
- **Consistency over cleverness**: Terminology, scales, and UI states are canonical here.
- **Emotional authenticity**: Characters respond within realistic human limitations; no "perfect NPC" behaviors.

---

## 2) Canonical Vocabulary & Scales

**Time units**
- **Turn**: Three per day (Morning / Afternoon / Evening). 7 days per week.
- **Season**: **12, 24, or 36 weeks** (player selects at season start based on aspiration complexity and desired depth).
  - **Standard (12w)**: Focused single-goal arc
  - **Extended (24w)**: Complex multi-path arc
  - **Epic (36w)**: Transformational saga arc
  - Players can end seasons early if goals complete ahead of schedule.

**Relationships**
- **Levels**: **0–5** (discrete stages; 0 = "Not Met", tracked internally but never displayed as "Level 0").
  - Level 0: Not Met (never interacted)
  - Level 1: Stranger (0-5 interactions)
  - Level 2: Acquaintance (6-15 interactions)
  - Level 3: Friend (16-30 interactions)
  - Level 4: Close Friend (31-75 interactions)
  - Level 5: Soulmate/Best Friend (76+ interactions)
- **Trust**: **0.0–1.0** continuous meter under the hood.
- **Level-Up Requirements**: Both interaction count AND minimum trust threshold required.
- **Statuses** (post-level): *Life Partnership*, *Estranged*, etc. (Statuses are **not** new levels.)
- **Display**: "Level 3 (Trust 0.62)" — never "10/10", "Level 6", or "Level 0" (show "Not Met" instead).

**Emotional State Lexicon**
- Canonical names include **EXHAUSTED** and **OVERWHELMED**.
- Deprecated alias: **DRAINED → EXHAUSTED** (map in logic and copy).
- New emotions must either map to an existing canonical name or propose an addition.

**Emotional Systems** *(NEW v1.2)*
- **Emotional Capacity**: **0.0–10.0** continuous scale (internal tracking; show in UI context when relevant)
  - Default: 5.0 (baseline human)
  - Low capacity: < 5.0 (shows limitations)
  - High capacity: ≥ 8.0 (full support available)
  - Crisis: ≤ 1.0 (cannot provide support)
- **Support Level Needed**: **0.0–10.0** scale (assessed per interaction)
- **Display**: "Character Name (Capacity 2.5/10)" in UI overlays when relevant to decision context

**Narrative Tension** *(NEW v1.2)*
- **Tension Types**: mystery_hook | partial_reveal | contradiction | stakes_escalation
- **Hook Status**: planted | unresolved | payoff_due | resolved
- **Payoff Timeline**: 2-4 weeks | 5-8 weeks | season_end
- **Tension Score**: **0.0–1.0** (internal quality metric)

**Memory Resonance** *(NEW v1.2)*
- **Resonance Types**: same_emotion_different_context | opposite_emotion_growth | past_trauma_trigger | joy_sadness_contrast | growth_callback
- **Resonance Score**: **0.0–1.0** (affects memory recall priority)

---

## 3) Economy & Resources
- **Time**: Weekly budget model (target: ~168h total; internal planning may assume ~48h flexible).
- **Energy**: Daily/phase-limited; gates higher-effort actions.
- **Money**: Liquidity for purchases, travel, activities.
- **Social Capital**: Earned/spendable relationship currency that unlocks favors, intros, and opportunities.
- **Modifiers**: Emotional state, skills, items provide multipliers/thresholds but are not currencies.

Authoring note: If introducing new currencies, they **must** be approved and added here first.

---

## 4) Turn Structure & Pacing
- **Cadence**: 3 turns/day; weekdays favor routines/obligations; weekends favor exploration/social.
- **Batching & Automation**: Repeating routines can be batched or auto-resolved to reduce friction.
- **Decision Tiers**: Top-tier/Decisive decisions **pause time** in UI; deadlines are in‑world, not real‑time.
- **Event Mix**: Each day blends routine, opportunity, social, and narrative beats (use category weights).

Copy standard: Replace any "FOMO/decide now" language with **"Time is paused while you decide."**

---

## 5) Narrative Structure
- **Season (3‑act)**: Setup → Escalation/Complications → Resolution/Consequences.
- **Decisive-Decision Template**: Triggers, preconditions, foreshadowing beats, clear options with immediate and long‑range consequences; success/failure paths defined.
- **Continuity**: NPC memory, relationship levels/trust, key outcomes persist across seasons and lifetimes.
- **Tension Building** *(NEW v1.2)*: Use tension injection framework (Section 17) to maintain engagement and create "one more week" desire to continue.

---

## 6) Card System (Unified)
- **Purpose**: Cards are the atomic memory/content units.
- **Taxonomy** (top-level): Life Direction • Aspirations • Relationships • Activities • Routines/Obligations • Places • Items/Utilities (7 buckets).
- **Base Deck**: 470+ curated base cards.
- **Evolution**: Cards evolve through usage/context; evolution is authored (not random) and preserves identity.
- **Tension Metadata** *(NEW v1.2)*: Cards track tension_type, hook_description, payoff_timeline, and information_debt for narrative continuity.

---

## 7) Fusion System
- **Types**: Simple • Complex • Chain • Legendary • Conditional.
- **Rules**: Fusion outputs declare prerequisites, inputs, and carried-forward traits; maintain traceability.
- **Levels/Trust**: Do **not** introduce new relationship levels; fusion may unlock statuses or traits.

---

## 8) Progression & Phases
- **Phase ladder** (high level): Foundations → Expansion → Mastery (names may localize per domain).
- Gating uses **skill checks**, **trust thresholds**, and **resource minima** — never paywalls.

---

## 9) Archives, Continuity & Persistence
- **Free**: Unlimited **Season Archives**; **3 Lifetime Archives**.
- **Plus/Ultimate**: Unlimited **Lifetime Archives**.
- Archives preserve: deck state, relationships (levels/trust), decisive outcomes, unlocked systems, and key world flags.

---

## 10) Monetization (Canonical)
- **Essence Tokens**: Daily free grant (baseline 25/day) for AI-heavy actions; subscription tiers raise limits.
- **Packs (DLC)**: Permanent unlocks, no RNG.
  - **Standard**: **20–30** cards
  - **Deluxe**: **35–50** cards
  - **Mega**: **60–80** cards (large locale/discipline collections)
- **Art Style Packs**: Visual-only style changes; typical price point **$2.99**.
- **Subscriptions**: **Plus $14.99/mo**, **Ultimate $29.99/mo** (exact entitlements maintained in Pricing table).

Policy: No timers, streaks, or scarcity designed to induce anxiety; in‑world deadlines are narrative devices only.

---

## 11) AI Personality & NPC Behavior

- **Stable voices**: NPCs maintain personality, goals, and memory across sessions.
- **Knowledge boundaries**: POV access is limited to what the character would plausibly know.
- **Authoring knobs**: Traits, goals, secrets, and trust thresholds are explicit dials; random drift is disallowed.

### NPC Response Framework *(NEW v1.2)*

> **Core Truth**: Every NPC response to player actions/dialogue is determined by THEIR frame of reference, filtered through a prioritized hierarchy of factors.

**Hierarchy (Primary to Modifiers)**:

1. **Personality (OCEAN) — PRIMARY FILTER**
   - Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
   - Sets baseline response tendency
   - Example: Low-conscientiousness NPC typically doesn't care if you decline to help

2. **Situational Urgency — MULTIPLIER (can override personality)**
   - Current need level: routine | important | urgent | crisis
   - Multiplier range: **1x (routine) to 5x (crisis)**
   - Example: Same low-conscientiousness NPC in crisis NOW cares deeply if you decline
   - Crisis needs override base personality indifference

3. **Relationship History — MODIFIER**
   - Trust level (0.0-1.0)
   - Relationship level (0-5)
   - Past interactions and patterns
   - Shared memories with emotional resonance (Section 17)

4. **Current Emotional Capacity — CONSTRAINT**
   - Capacity level (0-10 scale)
   - Limits available response range regardless of desire
   - Low capacity prevents high-engagement responses even if personality/urgency warrant them

5. **Personal Goals & Aspirations — CONTEXT**
   - How action affects their active goals
   - Alignment or conflict with their life direction
   - Opportunity cost assessment

**Formula**:
```
Response_Impact = Base_Personality_Response 
                  × Situational_Urgency_Multiplier (1x-5x)
                  × Relationship_Trust_Modifier (0.5x-2x)
                  × Memory_Resonance_Factor (0.7x-0.95x if applicable)
                  ÷ Emotional_Capacity_Constraint (caps maximum response)
```

**Examples**:

| NPC Type | Situation | Player Declines Help | Impact |
|----------|-----------|---------------------|---------|
| Low Agreeableness | Routine favor | Mild annoyance | -0.5 trust |
| Low Agreeableness | Crisis need (5x) | Significant hurt/anger | -2.5 trust |
| High Agreeableness | Routine favor | Understanding | -0.1 trust |
| High Agreeableness | Crisis need (5x) | Devastated, questioning relationship | -3.0 trust |

**Key Principle**: Personality sets the *baseline*, but situational urgency can *amplify* or *override* that baseline. A typically disengaged NPC becomes highly engaged when desperate. A typically engaged NPC becomes even more impacted by rejection during crisis.

### Bidirectional Scoring *(NEW v1.2)*

> **Critical Rule**: This framework applies **BOTH DIRECTIONS** - NPC evaluating player actions AND player understanding NPC responses.

**When NPC Evaluates Player Actions:**

The same hierarchy applies when determining relationship impact of player choices:

```
Player_Action_Impact = NPC_Personality_Filter 
                      × NPC_Current_Urgency (1x-5x)
                      × Relationship_History (0.5x-2x)
                      × NPC_Capacity_Constraint
```

**Scoring Determinants:**

1. **NPC's Personality (Primary)**: How THEY interpret player action
   - High-agreeableness NPC: Forgiving, gives benefit of doubt
   - Low-agreeableness NPC: Harsh judgment, takes offense easily

2. **NPC's Current State (Multiplier)**: Their urgency amplifies impact
   - Routine context: Small impact
   - Crisis context: 5x impact (same action feels MUCH worse)

3. **Relationship History (Modifier)**: Trust affects interpretation
   - High trust: Assumes good intent, cushions negative actions
   - Low trust: Assumes bad intent, amplifies negative actions

4. **NPC's Capacity (Constraint)**: Affects how much they can process
   - High capacity: Can consider nuance, context, player's state
   - Low capacity: Black/white thinking, can't see complexity

**Example - Same Player Action, Different NPC States:**

```
PLAYER ACTION: Declines to help NPC move apartments

NPC State A (Low urgency, high capacity, high trust):
- Impact: -0.2 trust ("No worries, it's a lot to ask")
- NPC considers: Player might be busy, stressed, etc.

NPC State B (Crisis urgency, low capacity, medium trust):
- Impact: -1.8 trust ("I really needed you and you weren't there")
- NPC cannot process: Player's reasons, context, legitimate conflicts

Formula:
State A: -0.5 (base) × 1.0 (routine) × 1.5 (high trust) = -0.75 → -0.2 (high capacity softens)
State B: -0.5 (base) × 4.0 (crisis) × 1.0 (med trust) = -2.0 → -1.8 (low capacity hardens)
```

**Scoring Guide Requirements:**

Every interaction must calculate:
1. What is NPC's baseline response (OCEAN)?
2. What is current urgency multiplier (1x-5x)?
3. What is relationship trust modifier (0.5x-2x)?
4. What is NPC's capacity constraint (affects judgment quality)?
5. Are there memory resonance factors (past betrayals, past support)?

**DO NOT use fixed scoring tables**. Same action has different impacts based on NPC state.

**Emotional Capacity Constraints** *(NEW v1.2)*:
- NPCs track current emotional capacity (0-10 scale)
- Responses are **CONSTRAINED** by capacity:
  - Low capacity (< 5): Cannot provide full emotional support
  - Character at 2.5/10 capacity CANNOT act like 8/10 capacity
  - Must show authentic limitations: trying but failing, withdrawing, acknowledging inadequacy
- **Canonical Rule**: Character at X/10 capacity can provide UP TO (X + 2)/10 level of emotional support
- Capacity affected by: stress, exhaustion, trauma, active problems, time since rest
- Positive gameplay: Characters acknowledge limitations authentically ("I want to help, but I'm overwhelmed myself")

**Dramatic Irony Mechanics** *(NEW v1.2)*:
- **Knowledge Gaps**: Track what player knows vs. what character knows
- **Tension Opportunities**: When knowledge gap exists, create "yelling at screen" moments
- **Capacity-Limited Perception**: Low capacity characters MORE LIKELY to misread situations
- **Player Overlays**: UI shows "(You know this is wrong, but [Character] doesn't...)"
- **Three Response Types**:
  - Tone-deaf (character acts on incomplete information)
  - Well-intentioned but misguided (tries to help incorrectly)
  - Growth choice (acknowledges limitations honestly)

---

## 12) UX & Copy Standards
- **Decisions**: Show **paused time** affordance on decisive choices.
- **States**: Use canonical emotion names; show tooltips for mapped aliases.
- **Consistency**: Surface "Level X (Trust Y.Y)" for relationships; never show deprecated scales.
- **Accessibility**: Plain language; avoid purple prose in system text.
- **Capacity Context** *(NEW v1.2)*: When character capacity affects available responses, show context: "Sarah (Exhausted, Capacity 2.5/10)" in UI overlays.

---

## 13) Authoring Rules for New Docs

When you create or edit any spec:
1. **Declare Intent**: Is it canonical, proposed, or exploratory?
2. **Align Scales**: Relationship 0–5; Trust 0.0–1.0; Emotional Capacity 0.0-10.0; Season 12w (or mark as Extended 24/36).
3. **Economy Check**: Only Time/Energy/Money/Social Capital as currencies unless added here.
4. **Decision Tiering**: Paused-time for top-tier choices; no real-time urgency text.
5. **Pack Fit**: Classify as Standard/Deluxe/Mega; include card counts.
6. **Archive Policy**: Respect tier entitlements.
7. **Emotion Names**: Use canonical lexicon; map aliases.
8. **Fusion Rules**: Specify type, inputs, prerequisites, and traceability.
9. **NPC Response Framework** *(NEW v1.2)*: Apply hierarchy (OCEAN primary → Situational multiplier → Relationship/capacity modifiers).
10. **Capacity Constraints** *(NEW v1.2)*: Respect emotional capacity limitations in NPC responses.
11. **Tension Injection** *(NEW v1.2)*: Follow frequency guidelines (1 in 3 for Level 1-2, 1 in 2 for Level 3-4).
12. **Quality Standards** *(NEW v1.2)*: Meet novel-quality thresholds (≥ 0.7 overall).
13. **Numerical Grounding** *(NEW v1.2)*: Use qualitative anchors from `NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md` - every number must have derivation, anchor, and validation.

Every doc should end with a **Compliance Checklist** referencing these bullets.

### Critical Resource: Numerical Calibration

> **See `NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md` for complete grounding system**

All numerical assignments (trust impact, capacity values, meter changes, quality scores) MUST reference qualitative anchors. Never assign numbers arbitrarily - use the three-step process:

1. **ANCHOR**: Identify qualitative tier ("major harm", "struggling", etc.)
2. **CALCULATE**: Apply formulas with explicit factors
3. **VALIDATE**: Confirm narrative matches the number

**Example:**
```
❌ WRONG: "relationship_impact": -1.3 (no justification)

✅ CORRECT:
"relationship_impact": -1.3,
"calculation": "base -0.6 × personality 0.8 × urgency 3x = -1.44",
"tier": "MODERATE HARM (-0.8 to -1.2)",
"narrative": "That stung. I'm disappointed."
```

---

## 14) Versioning & Change Process
- **Versioning**: Semantic (MAJOR.MINOR.PATCH) for this Truths doc; cite version in downstream docs.
- **Change Proposal (CP)**: Title • Rationale • Impacted Sections • Backward‑compat notes • Migration plan • Owner • Target release.
- **Approval**: 1 Product + 1 Narrative + 1 Systems sign‑off. Merge only after all are green.

---

## 15) Canonical Constants (v1.2)

**Time & Structure**
- Season length options: **12 weeks (Standard)**, **24 weeks (Extended)**, **36 weeks (Epic)** (player choice at season start)
- Turns per day: **3** (Morning/Afternoon/Evening); Days per week: **7**
- Free daily Essence: **25** (subject to tiering)

**Relationships**
- Relationship Levels: **0–5** (0=Not Met, 1-5 displayed); Trust: **0.0–1.0** (continuous)
- Level-up requirements: **Interaction count + Trust threshold** (both required)

**Monetization**
- Pack sizes: **Standard 20–30**, **Deluxe 35–50**, **Mega 60–80**

**NPC Response Framework** *(NEW v1.2)*:
- Situational urgency multipliers: **1x (routine)** | **2x (important)** | **3x (urgent)** | **5x (crisis)**
- Relationship trust modifiers: **0.5x (low trust)** to **2x (high trust)**
- Response hierarchy: OCEAN (primary) → Urgency (multiplier) → Relationship → Capacity (constraint)
- Crisis override: **5x multiplier** can make typically disengaged NPCs highly engaged

**Emotional Capacity** *(NEW v1.2)*:
- Default capacity: **5.0** (baseline human)
- Low capacity threshold: **< 5.0** (shows limitations)
- High capacity threshold: **≥ 8.0** (full support available)
- Crisis capacity: **≤ 1.0** (cannot provide support)
- Support rule: Can provide up to **(capacity + 2)** level support
- Capacity factors: stress (-1 to -3), exhaustion (-1 to -3), trauma (-2 to -4), problems (-0.5 each)

**Tension Injection** *(NEW v1.2)*:
- Level 1-2 frequency: **1 in 3** evolutions
- Level 3-4 frequency: **1 in 2** evolutions
- Level 5 frequency: **Nearly every** evolution
- Crisis evolutions: **Always** include stakes escalation
- Payoff timelines: **2-4 weeks** | **5-8 weeks** | **season_end**

**Memory Resonance** *(NEW v1.2)*:
- Same emotion, different context: **0.8** weight
- Opposite emotion, growth opportunity: **0.9** weight
- Past trauma, current trigger: **0.95** weight
- Past joy, current sadness contrast: **0.85** weight
- Emotional growth callback: **0.7** weight

**Novel-Quality Thresholds** *(NEW v1.2)*:
- Emotional Authenticity: **≥ 0.7**
- Tension Building: **≥ 0.6**
- Dramatic Irony: **≥ 0.5** (when applicable)
- Hook Effectiveness: **≥ 0.6**
- Overall Novel-Quality: **≥ 0.7**

> Update this block anytime numbers change. Downstream docs must reference constants by name, not hardcode values.
> 
> **v1.2 Updates:** Added NPC Response Framework with situational urgency multipliers (1x-5x), emotional capacity system (0-10 scale), tension injection framework with frequency guidelines, memory resonance weights (0.7-0.95), and novel-quality validation thresholds (all ≥ 0.7)

---

## 16) Emotional Authenticity System *(NEW v1.2)*

**Purpose**: Ensure characters respond within realistic human limitations, creating authentic emotional experiences rather than "perfect NPC" behaviors.

### Emotional Capacity

**Scale**: **0.0–10.0** (continuous, internal tracking)
- **Display**: Show as context in UI overlays when relevant: "Exhausted (Capacity 2.5/10)"
- **Default**: 5.0 (baseline human capacity)

**Factors Affecting Capacity**:
| Factor | Impact | Recovery |
|--------|--------|----------|
| Major stressor | -1.0 to -3.0 per stressor | Resolution or time |
| Sleep deprivation | -0.5 to -2.0 | Rest/sleep |
| Recent trauma or crisis | -2.0 to -4.0 | Processing, support, time |
| Active problems | -0.5 per problem | Problem resolution |
| Physical exhaustion | -1.0 to -3.0 | Rest, self-care |
| Positive factors | +0.5 to +2.0 | Good news, support, wins |

### Capacity Levels & Limitations

**0-1/10 (Crisis Mode)**
- **Can provide**: Nothing (and that's okay), honesty about inability
- **Cannot provide**: Any emotional support, even practical help
- **Example**: "I'm sorry. I can't. I just... I can't right now. I'm so sorry."

**2-4/10 (Low Capacity)**
- **Can provide**: Acknowledgment ("I hear you"), physical presence, practical help (errands, not emotional labor), promise to help later
- **Cannot provide**: Emotional support, long conversations, problem-solving, advice
- **Example**: "I can see this is really hard for you. I'm honestly not in a place to help the way you need right now—I'm barely keeping it together myself. Can I check in tomorrow?"

**5-7/10 (Medium Capacity)**
- **Can provide**: Moderate emotional support, listening for 30-60 minutes, basic advice, encouragement, practical help
- **Cannot provide**: Hours of processing, deep psychological analysis, crisis-level intervention
- **Example**: "I'm here for you. I've got an hour before I need to handle some stuff, but let's talk. What's going on?"

**8-10/10 (High Capacity)**
- **Can provide**: Deep emotional support, active listening for hours, thoughtful advice, crisis intervention, multiple perspectives, patient explanation
- **Example**: "Tell me everything. I've got all night, and I'm all yours. What happened?"

### Canonical Rule

> **Support Constraint**: A character at X/10 capacity can provide UP TO (X + 2)/10 level of emotional support. Beyond this, responses must show authentic limitations.

**Examples**:
- Character at 2.5/10 capacity can provide ~4.5/10 support (trying but limited)
- Character at 8.5/10 capacity can provide 10/10 support (full processing)
- Character at 4.0/10 capacity can provide ~6.0/10 support (moderate help)

### Circumstance Stacking

Multiple stressors compound:
```
Base capacity: 8.0
- Job deadline: -2.0
- Family crisis: -3.0
- Money problems: -2.0
= Effective capacity: 1.0
```

At 1.0 capacity, character can only acknowledge problem, not process it.

### Implementation Requirements

- Track capacity per character per turn
- Gate dialogue options by current capacity
- Show capacity warnings in UI when mismatch exists
- Award authenticity bonus for acknowledging limitations
- Penalize generations that exceed capacity constraints

### UI Integration

**Context Overlay** (shown when capacity affects decision):
```
┌─────────────────────────────────┐
│ Sarah (Exhausted)               │
│ Emotional Capacity: 2.5/10      │
│                                 │
│ ⚠️ Sarah is struggling right    │
│    now and can't provide full   │
│    emotional support.           │
└─────────────────────────────────┘
```

**Dialogue Option Gating**:
- High-support options grayed out with tooltip: "Requires capacity ≥ 6.0 (Sarah's current: 2.5)"
- Available options show capacity-appropriate responses
- Growth options always available (acknowledging limitations)

---

## 17) Novel-Quality Narrative Systems *(NEW v1.2)*

**Purpose**: Create page-turner experiences that feel like literary fiction rather than typical game dialogue. Transform "I'll help you!" into "I want to help, but I'm drowning myself right now."

### Tension Injection Framework

**Frequency Guidelines**:
- **Level 1-2 relationships**: 1 in 3 evolutions includes tension hook
- **Level 3-4 relationships**: 1 in 2 evolutions includes tension
- **Level 5 relationships**: Nearly every evolution maintains tension
- **Crisis evolutions**: Always include stakes escalation

### Four Tension Types

#### 1. Mystery Hook
**Definition**: Character mentions something but doesn't elaborate; unexplained behavior change; reference to unseen events/people.

**Examples**:
- "Sarah mentions someone named 'David' then immediately changes subject, hands shake slightly"
- "You notice Mark's hands shake when certain topics come up"
- "Emily gets a phone call and her whole demeanor shifts"

**Payoff Timeline**: Typically 2-4 weeks

#### 2. Partial Reveal
**Definition**: Show effect without cause (or vice versa); create "information debt" - promise future explanation.

**Examples**:
- "Character's phone lights up: '15 missed calls from Mom'. Character goes pale, dismisses it"
- "You see packed boxes in character's apartment they don't mention"
- "Character has a fresh scar they deflect questions about"

**Payoff Timeline**: Typically 2-4 weeks

#### 3. Contradiction Moment
**Definition**: Character acts against established pattern; signals major life events happening off-screen.

**Examples**:
- "Reserved Sarah suddenly takes a big social risk, won't explain why"
- "Optimistic Mark seems defeated, won't explain why"
- "Reliable friend cancels last-minute, very unusual"

**Payoff Timeline**: Typically 5-8 weeks (deeper arc)

#### 4. Stakes Escalation
**Definition**: Add time pressure; introduce consequences for inaction; create "ticking clock" elements.

**Examples**:
- "If you don't help Sarah this week, she'll make major decision alone"
- "Character is considering moving away - 2 weeks to decide"
- "Relationship at crossroads - next interaction is critical"

**Payoff Timeline**: Immediate to 2-4 weeks

### Tension Metadata

Track per card/interaction:
```json
{
  "tension_type": "mystery_hook | partial_reveal | contradiction | stakes_escalation | none",
  "hook_description": "What was planted",
  "expected_payoff_timeline": "2-4 weeks | 5-8 weeks | season_end",
  "information_debt": ["Question 1", "Question 2"],
  "player_curiosity_score": 0.85,
  "connects_to_previous_hooks": ["hook_id_123"]
}
```

**Memory Types**:
- `TENSION_HOOK`: Stores planted hooks
- `HOOK_PAYOFF`: Stores resolutions

### Memory Emotional Resonance

**Purpose**: Prioritize memory recall based on emotional impact and resonance with current situation, not just recency.

**Five Resonance Factors** (with weights):

1. **Same Emotion, Different Context** (0.8 weight)
   - Both memories involve joy, but first was achievement, now is connection
   - Shows pattern in emotional life

2. **Opposite Emotion, Growth Opportunity** (0.9 weight)
   - Memory of sadness, current situation is joy - shows character growth
   - Powerful contrast moments

3. **Past Trauma, Current Trigger** (0.95 weight - highest)
   - Memory of breakup, current situation involves romantic risk
   - Authentic emotional callbacks that feel real

4. **Past Joy, Current Sadness Contrast** (0.85 weight)
   - Memory of happy time with friend, friend now distant
   - Creates poignant, literary moments

5. **Emotional Growth Callback** (0.7 weight)
   - Memory of struggling with emotion, now handling it better
   - Shows character development

**Implementation**:
```javascript
calculateMemoryResonance(memory, currentContext) {
  let resonance = 0;
  
  // Check each resonance type
  if (sameEmotionDifferentContext(memory, currentContext)) {
    resonance += 0.8;
  }
  
  if (oppositeEmotionGrowth(memory, currentContext)) {
    resonance += 0.9;
  }
  
  if (pastTraumaTrigger(memory, currentContext)) {
    resonance += 0.95;
  }
  
  if (pastJoyCurrentSadness(memory, currentContext)) {
    resonance += 0.85;
  }
  
  if (emotionalGrowthCallback(memory, currentContext)) {
    resonance += 0.7;
  }
  
  return Math.min(1.0, resonance);
}
```

### Dramatic Irony System

**Purpose**: Create "yelling at the screen" tension through knowledge gaps between player and character.

**Three Components**:

1. **Player Knowledge** (what player knows that character doesn't)
   - NPC secrets
   - Witnessed events character wasn't present for
   - Overheard conversations
   - Hidden information

2. **Character Knowledge** (what character knows that player doesn't)
   - Internal struggles not yet revealed
   - Secret information not shared
   - True feelings not expressed
   - Off-screen events

3. **Knowledge Gap Score** (0-1 scale)
   - Calculated based on magnitude and type of gap
   - Score ≥ 0.6: Use dramatic irony template
   - Creates tension opportunity

**Irony Types**:
- `character_oblivious_to_npc_truth`: Player knows NPC's secret, character doesn't
- `character_misinterprets_situation`: Player witnessed event, character has wrong interpretation
- `capacity_limited_perception`: Low capacity character misreads social cues

**Three Response Types**:

1. **Tone-Deaf Option** (character acts on incomplete information)
   - Most realistic when capacity < 4/10
   - Creates maximum tension
   - Negative relationship impact (-0.5 to -1.5)
   - Player overlay: "(You know this is wrong, but [Character] doesn't...)"

2. **Well-Intentioned but Misguided** (tries to help incorrectly)
   - Most realistic when capacity 4-6/10
   - Creates moderate tension
   - Minor relationship impact (-0.2 to -0.5)
   - Shows character limitations authentically

3. **Growth Choice** (acknowledges limitations)
   - Most realistic when capacity ≥ 7/10
   - Resolves tension positively
   - Positive relationship impact (+0.3 to +0.8)
   - Shows emotional maturity

### Quality Validation

Every AI generation validated against:

| Check | Threshold | Weight | Purpose |
|-------|-----------|--------|---------|
| Emotional Authenticity | ≥ 0.7 | 35% | Responses constrained by capacity |
| Tension Building | ≥ 0.6 | 30% | Mystery hooks, stakes, engagement |
| Dramatic Irony | ≥ 0.5 | 15% | Knowledge gap utilization (when applicable) |
| Hook Effectiveness | ≥ 0.6 | 20% | "One more week" engagement |

**Overall Novel-Quality Score**: ≥ 0.7 required

**Retry Logic**:
- If quality < threshold and not using best model → retry with better model
- If quality < threshold with best model → flag for review
- Analytics track: authenticity_score, tension_score, hook_score, overall_quality

---

### Compliance Checklist (paste into new docs)

- [ ] Uses canonical vocab & scales (Levels 0–5; Trust 0.0–1.0; Capacity 0.0-10.0; EXHAUSTED/OVERWHELMED)
- [ ] Season = 12/24/36w (player choice at season start); 3 turns/day
- [ ] Relationship Level 0 = "Not Met" (never displayed as "Level 0")
- [ ] Level-up requires BOTH interaction count AND trust threshold
- [ ] Currencies limited to Time/Energy/Money/Social Capital
- [ ] Decisive decisions pause time; copy avoids FOMO framing
- [ ] Packs classified (Standard/Deluxe/Mega) with counts
- [ ] Archive policy respected by tier
- [ ] Fusion type, inputs, prerequisites, outputs defined
- [ ] NPC personality/memory constraints respected
- [ ] **NPC Response Framework applied: OCEAN primary filter → Situational multiplier (1x-5x) → Relationship/capacity modifiers**
- [ ] **Emotional capacity constraints respected (0-10 scale; support rule: capacity + 2)**
- [ ] **Tension injection frequency followed (Level 1-2: 1 in 3; Level 3-4: 1 in 2; Level 5: nearly every)**
- [ ] **Dramatic irony mechanics used when knowledge gaps exist (score ≥ 0.6)**
- [ ] **Memory resonance factors applied to recall (weights: 0.7-0.95)**
- [ ] **Novel-quality thresholds met (≥ 0.7 overall; authenticity ≥ 0.7; tension ≥ 0.6; hooks ≥ 0.6)**
- [ ] This doc cites **Truths v1.2** at the top

---

**Document Version:** v1.2  
**Last Updated:** October 14, 2025  
**Major Changes:** Added Section 0 (Game Vision & Core Description) with AI-powered visual generation system details; added Sections 16 (Emotional Authenticity) and 17 (Novel-Quality Narratives); added NPC Response Framework to Section 11 (OCEAN-driven responses with situational multipliers); enhanced Sections 2, 11, 13, 15 with emotional capacity, tension, and quality standards

