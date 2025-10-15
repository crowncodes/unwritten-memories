# Unwritten 2.gameplay/ Reorganization - REASSESSMENT

## The Real Problem

After reviewing `master_truths_canonical_spec_v_1.md` and the existing `1.concept/` documentation, I realize the original reorganization plan was **fundamentally flawed**.

---

## What Each Documentation Layer Should Be

### 📘 `docs/1.concept/` (DESIGN PHILOSOPHY)
**Purpose:** High-level "WHAT and WHY"
- Game vision and pillars
- Core systems explained conceptually
- Player experience goals
- Design principles and philosophy
- **Audience:** Game designers, writers, stakeholders, new team members

**Characteristics:**
- Explains the "why" behind decisions
- Describes player emotional journey
- Uses examples and stories
- ~500-1000 lines per doc
- References other concept docs

---

### 📕 `docs/master_truths_canonical_spec_v_1.md` (CANONICAL RULES)
**Purpose:** Single source of truth for constants and rules
- Canonical vocabulary and scales
- Exact numbers that must be followed
- Change control process
- Compliance requirements
- **Audience:** All team members (authority document)

**Characteristics:**
- Authoritative constants
- Version controlled
- Requires sign-off to change
- Referenced by all other docs
- Minimal prose, maximum clarity

---

### 📗 `docs/2.gameplay/` (IMPLEMENTATION SPECS)
**Purpose:** Detailed "HOW and EXACT IMPLEMENTATION"
- Exact formulas and calculations
- Complete data tables and catalogs
- Step-by-step system flows
- Templates and scaffolding
- Content specifications
- **Audience:** Developers, content designers, implementers

**Characteristics:**
- Implementation-ready details
- Exact numbers and formulas
- Complete catalogs (all 470 cards listed)
- Technical diagrams and flows
- Recipe books and templates
- Can be 1500-2000+ lines (reference material)
- References 1.concept/ for "why" but focuses on "exactly how"

---

## The Actual Gap Analysis

### ❌ What's Wrong With Current 2.gameplay/

**Problem 1: Redundancy**
- `unified-card-system.md` (1,874 lines) re-explains card philosophy already in `11-card-system-basics.md`
- `unified-narrative-structure.md` (1,254 lines) re-explains narrative philosophy already in multiple concept docs
- Creates maintenance burden and version drift

**Problem 2: Missing Structure**
- No index/navigation
- Overlapping content across files
- Hard to find implementation details
- No clear "where do I look for X?"

**Problem 3: Contradictions**
- `master_truths` says seasons = **12 weeks default** (24/36 extended)
- `1.concept/15-progression-phases.md` says **12-100 weeks variable**
- These need reconciliation

---

### ✅ What's RIGHT With Current 2.gameplay/

The following IMPLEMENTATION DETAILS should be preserved and enhanced:

#### From `Gameplay Turns.md`:
- **6 resource types with exact budgets**
- **168-hour weekly time model** with 48 flexible hours
- **Social Capital** as spendable relationship currency
- **Weekday/weekend turn cadence** with specific energy allocations
- **Event mix percentages** (routine vs. social vs. narrative)

#### From `narrative-arc-system.md`:
- **Decisive-decision scaffolding:**
  - Templates with triggers
  - Preconditions and requirements
  - Foreshadowing beats
  - Option payloads (immediate + long-term consequences)
  - Success/failure paths
- **Implementation-ready decision templates**

#### From `fusion_trees_doc.md`:
- **5 fusion types fully specified:**
  - Simple (2-card) with examples
  - Complex (3-card) with requirements
  - Chain fusion progressions
  - Legendary fusion sequences (5+ steps)
  - Conditional fusions with context gates
- **Multi-level fusion trees** with exact progression paths
- **Example: Character + Activity evolving through 5 levels**

#### From `Packs.md`:
- **Fully scoped expansion packs:**
  - City Explorer: 60 cards breakdown
  - Metro Transit system mechanics
  - High-Rise Living mechanics
  - Urban Reputation system
  - Complete NPC lists per pack
  - New systems introduced per pack

#### From `Categories.md`:
- **Complete Card Flow Diagram** (Life Direction → week cadence → events → season end → phase transition)
- **Visual flow of entire game loop**
- **Integration diagram showing how systems connect**

#### From `Expansions.md`:
- **Broad expansion taxonomy:**
  - Career & Ambition packs
  - Relationship & Social packs
  - Mind & Growth packs
  - Lifestyle & Environment packs
  - Culture & Language packs
  - Meta & Fantasy packs
  - Utility packs
  - Art & Aesthetic packs
- **Content pipeline for future expansions**

#### From `Base Cards.md`:
- **Catalog of 470+ base cards with category distribution**
- **Confirmation of card counts per type**

---

## What 2.gameplay/ Should ACTUALLY Contain

### Proposed Structure (Implementation Reference Library)

```
docs/2.gameplay/
├── 00-INDEX.md                              ← Navigation hub
│
├─────────────────────────────────────────────
│ CORE SYSTEMS (Implementation Details)
├─────────────────────────────────────────────
├── 10-resource-economy-spec.md              ← 6 resources, exact budgets, formulas
├── 11-turn-economy-implementation.md        ← 168h model, turn structure, batching
├── 12-success-probability-formulas.md       ← Exact math for success chances
├── 13-meter-effects-tables.md               ← What happens at each threshold
├── 14-emotional-state-mechanics.md          ← 20 states, filtering rules, transitions
│
├─────────────────────────────────────────────
│ CARD SYSTEMS (Complete Catalogs & Recipes)
├─────────────────────────────────────────────
├── 20-base-card-catalog.md                  ← All 470 cards listed with stats
├── 21-card-evolution-recipes.md             ← Evolution triggers, templates, AI prompts
├── 22-fusion-recipe-book.md                 ← Complete fusion trees with requirements
├── 23-fusion-type-specifications.md         ← 5 fusion types, exact mechanics
├── 24-card-generation-guidelines.md         ← AI generation templates for cards
│
├─────────────────────────────────────────────
│ NARRATIVE SYSTEMS (Templates & Scaffolding)
├─────────────────────────────────────────────
├── 30-decisive-decision-templates.md        ← Complete scaffolding with preconditions
├── 31-narrative-arc-scaffolding.md          ← 3-act season structure implementation
├── 32-event-generation-rules.md             ← Event mix, frequency, triggers
├── 33-dialogue-generation-templates.md      ← Context-aware dialogue generation
├── 34-novel-generation-pipeline.md          ← Season → chapter conversion process
│
├─────────────────────────────────────────────
│ PROGRESSION SYSTEMS (Exact Mechanics)
├─────────────────────────────────────────────
├── 40-season-length-calculation.md          ← Formula for 12/24/36 week seasons
├── 41-phase-transition-mechanics.md         ← Triggers, thresholds, transitions
├── 42-aspiration-goal-trees.md              ← 90 aspirations with requirements
├── 43-skill-progression-tables.md           ← 30+ skills, Level 1-10 requirements
├── 44-relationship-progression-spec.md      ← Levels 0-5, trust 0.0-1.0, thresholds
│
├─────────────────────────────────────────────
│ CONTENT EXPANSION (Pack Specifications)
├─────────────────────────────────────────────
├── 50-expansion-pack-specs.md               ← All 12+ packs with full breakdowns
├── 51-pack-city-explorer.md                 ← 60-card breakdown, new systems
├── 52-pack-nature-adventure.md              ← Complete specification
├── 53-pack-career-ambition.md               ← Complete specification
├── 54-pack-relationship-depth.md            ← Complete specification
├── 55-future-content-roadmap.md             ← Planned expansions beyond launch
│
├─────────────────────────────────────────────
│ VISUAL SYSTEMS (Asset Specifications)
├─────────────────────────────────────────────
├── 60-card-art-specifications.md            ← Art requirements per card type
├── 61-art-style-pack-specs.md               ← 10 art packs with visual examples
├── 62-animation-specifications.md           ← Holo cards, particle effects
├── 63-ui-flow-diagrams.md                   ← Complete UI flows with screenshots
│
├─────────────────────────────────────────────
│ INTEGRATION & FLOWS (System Connections)
├─────────────────────────────────────────────
├── 70-complete-game-flow-diagram.md         ← End-to-end player journey
├── 71-daily-turn-flow-detailed.md           ← Moment-to-moment implementation
├── 72-weekly-cycle-implementation.md        ← Week structure, end-of-week processing
├── 73-season-flow-implementation.md         ← Act I → II → III mechanics
├── 74-multi-season-continuity-spec.md       ← Tier 1-4 context management
│
└── 80-master-truths-compliance.md           ← How gameplay docs comply with canonical spec
```

---

## Key Principles for 2.gameplay/

### 1. **NO Philosophy Duplication**
- Don't re-explain "why cards evolve" (that's in 1.concept/12-card-evolution.md)
- DO provide exact evolution triggers, formulas, and AI prompt templates
- Reference concept docs with: `See 1.concept/12-card-evolution.md for design philosophy`

### 2. **Implementation-Ready Detail**
- Exact numbers, not ranges
- Complete formulas, not descriptions
- Full catalogs, not summaries
- Step-by-step flows, not overviews

### 3. **Master Truths Compliance**
- Every doc must cite compliance with master_truths
- Use canonical constants (reference by name, don't hardcode)
- Note any deviations with rationale

### 4. **Developer-Focused**
- Someone should be able to implement from these docs
- Include pseudocode where helpful
- Provide worked examples with exact numbers
- Link to JSON schemas in 1.concept/18-json-contracts.md

### 5. **Content Designer-Focused**
- Complete card catalogs (all 470 base cards listed)
- Fusion recipe book (all major fusions documented)
- Pack specifications (every card in every pack)
- Event templates (copy-pasteable templates)

---

## What to Do With Current Files

### Files to PRESERVE (with cleanup):

**✅ Gameplay Turns.md → 11-turn-economy-implementation.md**
- Keep: 6 resource types, 168h weekly model, exact budgets
- Remove: Philosophy already in 21-turn-structure.md
- Add: Pseudocode for turn resolution
- Compliance: Verify 3 turns/day matches master_truths

**✅ narrative-arc-system.md → 30-decisive-decision-templates.md**
- Keep: Complete decision template with preconditions
- Remove: Narrative philosophy (already in concept docs)
- Add: 20+ example templates with all fields filled
- Enhance: Failure path scaffolding

**✅ fusion_trees_doc.md → 22-fusion-recipe-book.md + 23-fusion-type-specifications.md**
- Split: Types (5 fusion types with mechanics) vs. Recipes (specific fusion trees)
- Keep: All multi-level examples
- Add: More fusion trees (100+ documented fusions)
- Enhance: Exact probability formulas

**✅ Packs.md → 50-expansion-pack-specs.md + 51-56 (individual pack specs)**
- Keep: All 60-card breakdowns
- Expand: Create individual files for each major pack
- Add: New system mechanics per pack (Metro Transit, etc.)
- Add: Integration notes (how pack content triggers)

**✅ Categories.md → 70-complete-game-flow-diagram.md**
- Keep: Complete card flow diagram
- Enhance: Add more integration diagrams
- Add: System connection maps

**✅ Expansions.md → 55-future-content-roadmap.md**
- Keep: Broad expansion taxonomy
- Add: Priority order and dependencies
- Add: Content pipeline process

**✅ Base Cards.md → 20-base-card-catalog.md**
- Keep: Card count confirmation
- MASSIVELY EXPAND: List all 470 cards with:
  - Name, type, rarity
  - Base stats and costs
  - Evolution potential
  - Combination possibilities
  - Pack source (base vs. premium)

### Files to DISSOLVE (merge into appropriate spec docs):

**❌ unified-card-system.md**
- Philosophy → Already in 1.concept/11-card-system-basics.md
- Implementation details → Distribute to:
  - 20-base-card-catalog.md (card lists)
  - 21-card-evolution-recipes.md (evolution mechanics)
  - 12-success-probability-formulas.md (success formulas)

**❌ unified-narrative-structure.md**
- Philosophy → Already in 1.concept/15-progression-phases.md, 16-archive-persistence.md
- Implementation details → Distribute to:
  - 31-narrative-arc-scaffolding.md (3-act implementation)
  - 32-event-generation-rules.md (event triggers)
  - 34-novel-generation-pipeline.md (book generation process)

**❌ unified-content-expansion.md**
- Philosophy → Already in 1.concept/17-monetization-model.md
- Implementation details → Distribute to:
  - 50-expansion-pack-specs.md (pack breakdowns)
  - 55-future-content-roadmap.md (roadmap)

**❌ unified-gameplay-flow.md**
- Philosophy → Already in 1.concept/21-turn-structure.md
- Implementation details → Distribute to:
  - 71-daily-turn-flow-detailed.md (turn mechanics)
  - 72-weekly-cycle-implementation.md (week structure)
  - 73-season-flow-implementation.md (season mechanics)

---

## Critical Contradictions to Resolve

### 🚨 Season Length: 12 vs. 12-100 weeks

**master_truths says:**
```
Season length (default): 12 weeks (Extended: 24/36)
```

**1.concept/15-progression-phases.md says:**
```
12-100 weeks variable based on complexity
```

**Resolution Needed:**
1. Which is canonical?
2. If variable length, update master_truths
3. If fixed 12/24/36, update concept docs
4. Document in 40-season-length-calculation.md

---

### 🚨 Relationship Levels: 0-5 vs. 1-5

**master_truths says:**
```
Relationship Levels: 0–5 (discrete stages)
```

**1.concept/13-ai-personality-system.md says:**
```
Level 1 → 2: Stranger → Acquaintance
Level 2 → 3: Acquaintance → Friend
[Implies 1-5, not 0-5]
```

**Resolution Needed:**
1. Clarify: Is Level 0 "Not Met" or is Level 1 "Stranger"?
2. Update either master_truths or concept docs
3. Document in 44-relationship-progression-spec.md

---

### 🚨 Turn Structure: 3 per day

**master_truths says:**
```
3 turns/day (Morning / Afternoon / Evening)
```

**This is consistent** across docs. ✅

---

## Recommended Action Plan

### Phase 1: Reconcile Contradictions (FIRST!)
1. ✅ Resolve season length (12 fixed vs. variable)
2. ✅ Resolve relationship levels (0-5 vs. 1-5)
3. ✅ Update master_truths OR concept docs to match
4. ✅ Document decisions in change log

### Phase 2: Create 00-INDEX.md for 2.gameplay/
- Navigation hub
- "Where do I find X?" quick reference
- Relationship to 1.concept/ explained
- Compliance with master_truths noted

### Phase 3: Extract Implementation Details
- Go through each "unified" doc
- Extract implementation specs (formulas, numbers, catalogs)
- Place in appropriate new spec files
- Remove philosophy duplication

### Phase 4: Expand Catalogs & Recipe Books
- Complete 470-card catalog
- Complete fusion recipe book (100+ fusions)
- Complete pack specifications (all 12+ packs)
- Complete templates (decisions, events, dialogue)

### Phase 5: Create Integration Docs
- System flow diagrams
- Daily/weekly/season flows
- Multi-season continuity mechanics
- Complete game loop documentation

### Phase 6: Compliance Check
- Every file cites master_truths version
- Every file has compliance checklist
- Every file references concept docs where appropriate
- No contradictions remain

---

## Success Criteria

**Good 2.gameplay/ documentation means:**

✅ A developer can implement resource economy from 10-resource-economy-spec.md
✅ A content designer can create new cards from 20-base-card-catalog.md + templates
✅ A systems designer can add new fusion from 22-fusion-recipe-book.md
✅ A narrative designer can create events from 30-decisive-decision-templates.md
✅ An AI engineer can generate content from 24-card-generation-guidelines.md
✅ Anyone can find implementation details quickly via 00-INDEX.md
✅ No duplication of philosophy from 1.concept/
✅ All specs comply with master_truths canonical constants
✅ All contradictions resolved and documented

---

## The Bottom Line

**You were right to be concerned.** The original reorganization plan would have:
- ❌ Lost detailed implementation specs (resource economy, decision templates, fusion trees, pack specs)
- ❌ Duplicated philosophy already in 1.concept/
- ❌ Created maintenance burden

**The correct approach is:**
- ✅ Preserve ALL implementation details from current docs
- ✅ Organize them clearly by system
- ✅ Remove philosophy duplication (reference concept docs instead)
- ✅ Expand incomplete sections (full card catalog, more fusion recipes)
- ✅ Resolve contradictions with master_truths
- ✅ Make docs implementation-ready for developers and designers

**2.gameplay/ should be a REFERENCE LIBRARY and IMPLEMENTATION GUIDE, not a duplicate concept explanation.**

---

## Next Steps

1. **Get approval** on this reassessment
2. **Resolve contradictions** (season length, relationship levels)
3. **Create 00-INDEX.md** with new structure
4. **Migrate content** file by file (preserve all implementation details)
5. **Expand incomplete** sections (full catalogs, recipes)
6. **Compliance check** everything against master_truths
7. **Integration pass** (ensure all systems connect)

This will take longer but will result in MUCH better documentation that actually serves its purpose: giving implementers the exact specifications they need to build the game.

