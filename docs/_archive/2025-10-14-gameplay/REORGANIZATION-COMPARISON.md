# Original Plan vs. Reassessed Plan - Visual Comparison

## The Fundamental Difference

### ❌ ORIGINAL PLAN (FLAWED)
```
docs/1.concept/          docs/2.gameplay/
(Design Philosophy)      (Duplicate Philosophy + Some Details)
     ↓                           ↓
  470 cards               470 cards again
  Card evolution          Card evolution again  
  Fusion philosophy       Fusion philosophy again
  Turn structure          Turn structure again
```
**Problem:** Duplication creates maintenance burden and version drift.

---

### ✅ REASSESSED PLAN (CORRECT)
```
docs/master_truths_canonical_spec_v_1.md
(Canonical Constants & Rules - AUTHORITY)
                ↓ referenced by ↓
     ┌──────────────────────┬──────────────────────┐
     ↓                      ↓                      ↓
docs/1.concept/      docs/2.gameplay/      Implementation
(WHY & WHAT)         (HOW & EXACT)         (Code)
     ↓                      ↓                      ↓
Philosophy         Implementation        Features
Design Goals       Formulas & Math       Systems
Player Journey     Complete Catalogs     Content
Examples           Templates             Database
```

**Relationship:**
- **master_truths** = Single source of truth for constants
- **1.concept/** = "Here's WHY we do it this way" (references master_truths)
- **2.gameplay/** = "Here's EXACTLY HOW to do it" (complies with master_truths, references 1.concept/ for philosophy)
- **Implementation** = Code that follows 2.gameplay/ specs

---

## Document Purpose Comparison

| Aspect | 1.concept/ | 2.gameplay/ |
|--------|-----------|-------------|
| **Purpose** | Design philosophy | Implementation specs |
| **Audience** | Designers, writers, stakeholders | Developers, content creators |
| **Length** | 500-1000 lines | 1500-3000 lines (reference material) |
| **Style** | Narrative, examples | Technical, tables, formulas |
| **Content** | "Cards evolve based on player choices" | "Evolution triggers: 5+ interactions + trust > 0.4 + context match" |
| **Completeness** | Representative examples | Exhaustive catalogs |
| **Changes** | Evolves with design | Stable specifications |

---

## Example: Card Evolution Documentation

### In 1.concept/12-card-evolution.md (CURRENT - GOOD)
```markdown
## Evolution Philosophy

Cards don't just level up—they **remember**. Each evolution 
captures a specific moment from YOUR playthrough.

### Example:
Sarah Anderson evolves from Level 1 (Stranger) to Level 2 
(Acquaintance) after your first real conversation...

[Continues with philosophy, design goals, player experience]
```
**Purpose:** Explain WHY and create vision
**Length:** ~650 lines

---

### In 2.gameplay/ (SHOULD BE)
```markdown
## Card Evolution Implementation Specification

**References:** 
- Design philosophy: `1.concept/12-card-evolution.md`
- Master truths: v1.0.0, Relationship Levels 0-5

### Evolution Trigger Formula

```javascript
function canEvolve(card, gameState) {
  const requirements = EVOLUTION_REQUIREMENTS[card.currentLevel];
  
  return (
    card.interactionCount >= requirements.minInteractions &&
    card.trust >= requirements.minTrust &&
    card.daysSinceLastEvolution >= requirements.cooldownDays &&
    meetsContextRequirements(card, gameState)
  );
}

const EVOLUTION_REQUIREMENTS = {
  0: { // Not met → Stranger (Level 1)
    minInteractions: 1,
    minTrust: 0.0,
    cooldownDays: 0,
    context: "first_meeting"
  },
  1: { // Stranger → Acquaintance (Level 2)
    minInteractions: 5,
    minTrust: 0.2,
    cooldownDays: 7,
    context: "meaningful_conversation"
  },
  // ... continues for all levels
};
```

### All 50 Base Character Evolution Paths
| Character | Level 1 Trigger | Level 2 Trigger | Special Requirements |
|-----------|-----------------|-----------------|---------------------|
| Sarah Anderson | First coffee meetup | 5 interactions + bookstore visit | Must have cultural interests |
| Marcus Rivera | Gym introduction | 3 workouts together | Must have fitness skill |
| ... (all 50 characters) ... |

### AI Generation Prompt Template

```
[SYSTEM]
Character: {character_name}
Current Level: {current_level} → {target_level}
Interaction Count: {count}
Trust Level: {trust_score}
Recent Context: {last_5_interactions}

[TASK]
Generate evolved card with:
1. New memory (50-100 words)
2. Personality shift (OCEAN adjustments, max ±0.3)
3. One new detail revealed
4. Unlock 1-2 new activities
5. Portrait update description

[CONSTRAINTS]
- Must reference at least 1 previous memory
- Personality shift must be psychologically consistent
- New detail must connect to previous interactions
- No contradictions with canonical facts
```
**Purpose:** Exact implementation specifications
**Length:** ~2000 lines (complete reference)

---

## What Gets Preserved vs. Reorganized

### ✅ PRESERVE (From current 2.gameplay/)

#### From `Gameplay Turns.md`:
```
EXACT BUDGETS:
- Energy: 8/day weekday, 11/day weekend
- Time: 168h/week total, ~48h flexible after obligations
- Money: Weekly income - weekly expenses
- Social Capital: Earned at +1 per meaningful interaction
- Comfort Zone: Depleted by risky activities, regenerates slowly
- Success Probability: Modified by skills, emotional state, resources

WEEKDAY STRUCTURE:
Morning (6am-12pm): 3 Energy, Obligations priority
Afternoon (12pm-6pm): 3 Energy, Main activities
Evening (6pm-12am): 2 Energy, Social/rest
```
→ Goes to: `11-turn-economy-implementation.md`

#### From `narrative-arc-system.md`:
```
DECISIVE DECISION TEMPLATE:

{
  "id": "sarah_bookshop_investment",
  "title": "Sarah's Dream",
  "trigger": {
    "character": "sarah_anderson",
    "relationship_level": 3,
    "trust": 0.65,
    "context": "business_plan_revealed",
    "week_range": [25, 35]
  },
  "preconditions": [
    "sarah_level_3_or_higher",
    "bookstore_visits >= 3",
    "savings >= 15000",
    "career_stability == true"
  ],
  "foreshadowing": [
    {week: -12, event: "sarah_mentions_grandmother"},
    {week: -8, event: "sarah_shows_business_notes"},
    {week: -4, event: "sarah_finds_location"},
    {week: -1, event: "sarah_asks_to_talk"}
  ],
  "options": [
    {
      "choice": "invest_full",
      "cost": {money: 25000, career: "quit_job"},
      "immediate": ["+0.3 sarah_trust", "new_career: entrepreneur"],
      "long_term": ["business_partner_arc", "financial_risk_arc"],
      "success_prob": 0.65
    },
    {
      "choice": "invest_partial",
      "cost": {money: 10000},
      "immediate": ["+0.15 sarah_trust", "keep_job"],
      "long_term": ["side_business_arc", "time_pressure_arc"],
      "success_prob": 0.75
    },
    {
      "choice": "support_emotionally",
      "cost": {time: "weekly_help"},
      "immediate": ["+0.05 sarah_trust"],
      "long_term": ["supporter_role_arc"],
      "success_prob": 0.85
    },
    {
      "choice": "decline",
      "cost": null,
      "immediate": ["-0.2 sarah_trust", "relationship_strain"],
      "long_term": ["distant_friend_arc", "regret_path"],
      "success_prob": 1.0
    }
  ],
  "success_path": {
    "weeks": [8, 20, 32, 45],
    "milestones": ["lease_signed", "renovation", "inventory", "opening"],
    "fusion_unlocks": ["bookshop_partner_legendary"]
  },
  "failure_path": {
    "weeks": [12, 28],
    "outcomes": ["financial_loss", "relationship_recovery_arc"],
    "learning": ["+business_skill_intuition"]
  }
}
```
→ Goes to: `30-decisive-decision-templates.md` with 20+ complete examples

#### From `fusion_trees_doc.md`:
```
LEGENDARY FUSION CHAIN: "The Bookshop Opening"

STEP 1: Level 2 Unlock (Week 12)
[Sarah Level 1] + [Bookstore Visit] + [EXCITED emotion]
→ "The Bookshop Dream" (Quest Card)
Requirements: 
  - Trust >= 0.35
  - EXCITED or CURIOUS emotion
  - Location: Bookstore or Café

STEP 2: Planning Phase (Weeks 13-25)
["Bookshop Dream"] + [Business Planning Activity] (×5)
→ "Detailed Business Plan" (Resource Card)
Requirements:
  - Business skill >= 2
  - Time investment: 5 activities × 2h each
  - Sarah trust >= 0.5

STEP 3: Commitment (Week 28)
["Business Plan"] + [Your Savings $25k] + [Sarah's Inheritance $15k]
→ "Signed Lease" (Major Milestone)
Requirements:
  - Sarah trust >= 0.65
  - Savings >= $25,000
  - Decisive decision: "invest_full"

STEP 4: Building Phase (Weeks 29-44)
["Signed Lease"] + [Renovation Activities] (×10) + [Sarah Level 4]
→ "Bookshop Ready to Open" (Pre-Legendary)
Requirements:
  - Time: 15 weeks minimum
  - Money: $15,000 additional
  - Skills: Business 4, Sarah trust >= 0.85

STEP 5: LEGENDARY CLIMAX (Week 45)
["Bookshop Ready"] + [Opening Day Event] + [All Friends Invited]
→ "THE BOOKSHOP OPENING" (LEGENDARY CARD)
Requirements:
  - All previous steps completed
  - At least 3 Level 3+ relationships present
  - Success roll >= 0.65
Effects:
  - New career: Bookshop co-owner
  - Sarah relationship: 1.0 (max)
  - Income: $2,000/month base
  - Achievement: "Dream Builder"
  - Archive moment: Major
```
→ Goes to: `22-fusion-recipe-book.md` with 100+ complete chains

---

### ❌ REMOVE (Duplicated Philosophy)

From `unified-card-system.md`:
```
"Cards in Unwritten are not just mechanics—they're memories. 
Each card represents a moment, a person, a place that matters 
to your character's story..."
```
→ Already in `1.concept/11-card-system-basics.md` - DELETE

From `unified-narrative-structure.md`:
```
"Unwritten uses a season-based structure where each season is 
a complete story arc. This creates natural stopping points 
and allows players to..."
```
→ Already in `1.concept/15-progression-phases.md` - DELETE

---

## Critical Contradictions to Resolve FIRST

### 🚨 CONTRADICTION 1: Season Length

| Source | Says |
|--------|------|
| **master_truths v1.0** | Season = **12 weeks default**, Extended 24/36 |
| **1.concept/15-progression-phases.md** | Season = **12-100 weeks variable** |
| **2.gameplay/unified-gameplay-flow.md** | Mentions both fixed and variable |

**Impact:** 
- Architecture decisions (memory systems scale differently)
- Novel generation (chapters per season)
- Content planning (how much content per season?)
- Player expectations (commitment level)

**Resolution Options:**
1. **Use master_truths (12/24/36 fixed):**
   - Update 1.concept/15 to remove variable length
   - Document in 40-season-length-calculation.md
   - Season complexity affects DENSITY not LENGTH
   
2. **Use concept docs (12-100 variable):**
   - Update master_truths to allow variable
   - Document formula for length calculation
   - Season complexity extends duration

**Recommendation:** Option 1 (fixed lengths) because:
- Easier to balance content
- Clearer player commitment
- Simpler memory architecture
- Can achieve same narrative flexibility through:
  - Multi-season arcs (single aspiration across 2-3 seasons)
  - Extended mode for complex stories (24/36 weeks)
  - Season density (routine batching vs. granular days)

---

### 🚨 CONTRADICTION 2: Relationship Levels

| Source | Says |
|--------|------|
| **master_truths v1.0** | Levels **0-5** (6 levels) |
| **1.concept/13-ai-personality-system.md** | Level 1 = Stranger (implies 1-5, 5 levels) |
| **1.concept/11-card-system-basics.md** | Lists 5 levels: Stranger, Acquaintance, Friend, Close Friend, Soulmate |

**Impact:**
- UI display ("Level 0" vs. "Not Met")
- Progression curve (5 steps vs. 6 steps)
- Fusion requirements (trust + level gating)
- Archive statistics

**Resolution Options:**
1. **Use 0-5 (6 levels):**
   - Level 0 = "Not Met" (never interacted)
   - Level 1 = "Stranger" (met, minimal interaction)
   - Level 2-5 as currently described
   - Update concept docs

2. **Use 1-5 (5 levels):**
   - No Level 0 (all NPCs start at Level 1 once met)
   - Level 1 = "Stranger"
   - Update master_truths

**Recommendation:** Option 1 (0-5, six levels) because:
- Level 0 useful for tracking "never met this NPC"
- Enables "first meeting" special mechanics
- Cleaner database (NULL vs. 0 vs. 1)
- More progression granularity
- Update 1.concept/13 to show:
  ```
  Level 0: Not Met (base state)
  Level 1: Stranger (first meeting - 5 interactions)
  Level 2: Acquaintance (6-15 interactions)
  Level 3: Friend (16-30 interactions)
  Level 4: Close Friend (31-75 interactions)
  Level 5: Soulmate/Best Friend (76+ interactions)
  ```

---

### ✅ NO CONTRADICTION: Turn Structure

| Source | Says |
|--------|------|
| **master_truths v1.0** | **3 turns/day** (Morning/Afternoon/Evening) |
| **1.concept/21-turn-structure.md** | **3 turns/day** (Morning/Afternoon/Evening) |
| **2.gameplay/Gameplay Turns.md** | **3 turns/day** (Morning/Afternoon/Evening) |

**Status:** ✅ **ALIGNED** - No changes needed

---

## Recommended Resolution Process

### Step 1: Create Canonical Decisions Document
```markdown
# Canonical Decisions - October 2025

## Decision 1: Season Length (RESOLVED)
**Date:** 2025-10-13
**Decision:** Fixed lengths (12/24/36 weeks)
**Rationale:** Balancing, player commitment, memory architecture
**Updates Required:**
- [ ] Update 1.concept/15-progression-phases.md
- [ ] Create 2.gameplay/40-season-length-calculation.md
- [ ] Update master_truths v1.0 → v1.1 (clarify, not change)

## Decision 2: Relationship Levels (RESOLVED)
**Date:** 2025-10-13
**Decision:** Use 0-5 (6 levels including "Not Met")
**Rationale:** Database clarity, first-meeting mechanics, progression curve
**Updates Required:**
- [ ] Update 1.concept/13-ai-personality-system.md (add Level 0)
- [ ] Update 1.concept/11-card-system-basics.md (clarify)
- [ ] Create 2.gameplay/44-relationship-progression-spec.md
- [ ] Update master_truths v1.0 → v1.1 (clarify)
```

---

### Step 2: Update Master Truths (v1.0 → v1.1)

**Changes:**
```diff
- Season length (default): 12 weeks (Extended: 24/36)
+ Season length: 12 weeks (default), 24 weeks (Extended), 36 weeks (Epic)
+ Note: Variable length removed; complexity affects density not duration

- Relationship Levels: 0–5 (discrete stages)
+ Relationship Levels: 0–5 (0=Not Met, 1=Stranger, 2=Acquaintance, 3=Friend, 4=Close Friend, 5=Soulmate)
+ Display: "Level X" for 1-5; "Not Met" for 0; never show "Level 0"
```

---

### Step 3: Update Concept Docs
- 1.concept/15-progression-phases.md → Remove variable 12-100 weeks
- 1.concept/13-ai-personality-system.md → Add Level 0 explanation
- 1.concept/11-card-system-basics.md → Clarify 0-5 display

---

### Step 4: Create 2.gameplay/ Structure
- Follow reassessed plan structure
- Preserve all implementation details
- Reference concept docs, don't duplicate
- Comply with master_truths v1.1

---

## Summary: The Correct Path Forward

**ORIGINAL PLAN:**
- ❌ Duplicate 1.concept/ in 2.gameplay/
- ❌ Lose implementation details
- ❌ Create maintenance burden

**REASSESSED PLAN:**
- ✅ Preserve ALL implementation specs
- ✅ Remove philosophy duplication
- ✅ Resolve contradictions FIRST
- ✅ Create clear document hierarchy:
  - master_truths = Authority
  - 1.concept/ = Philosophy (WHY)
  - 2.gameplay/ = Specifications (HOW)
  - Implementation = Code

**NEXT ACTIONS:**
1. Get approval on reassessment
2. Resolve season length → Fixed 12/24/36
3. Resolve relationship levels → 0-5 (six levels)
4. Update master_truths v1.0 → v1.1
5. Create 00-INDEX.md for 2.gameplay/
6. Migrate content preserving ALL details
7. Expand incomplete sections
8. Compliance check

This approach preserves all valuable content while creating a sustainable documentation structure.

