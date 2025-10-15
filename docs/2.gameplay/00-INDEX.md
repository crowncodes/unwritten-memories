# Unwritten Gameplay Documentation - Implementation Specifications

**Last Updated:** October 14, 2025  
**Compliance:** master_truths v1.2 (Canonical Spec)  
**Purpose:** Implementation-ready specifications for developers and content designers

---

## Documentation Hierarchy

```
docs/
├── master_truths_canonical_spec_v_1_2.md (v1.2)
│   └── AUTHORITY - Single source of truth for constants and rules
│
├── 1.concept/ (Design Philosophy)
│   └── WHY & WHAT - Game vision, player experience, design principles
│
└── 2.gameplay/ (Implementation Specs) ← YOU ARE HERE
    └── HOW & EXACT - Formulas, catalogs, templates, exact mechanics
```

**Relationship Between Layers:**
- **master_truths v1.2** = Canonical constants and rules (what's allowed) + Emotional Authenticity & Novel-Quality systems
- **1.concept/** = Philosophy ("why cards evolve" - player experience goals)
- **2.gameplay/** = Implementation ("exact evolution triggers at trust > 0.4" - developer specs)

**Rule:** 2.gameplay/ docs REFERENCE 1.concept/ for philosophy, never duplicate it.

---

## Quick Navigation

### "Where do I find...?"

**"How do I implement the resource economy?"**  
→ `10-resource-economy-spec.md` (6 resources, exact budgets, formulas)

**"What are the exact evolution triggers?"**  
→ `21-card-evolution-recipes.md` (all triggers with pseudocode)

**"How do I create a decisive decision?"**  
→ `30-decisive-decision-templates.md` (20+ complete examples)

**"What fusion recipes exist?"**  
→ `22-fusion-recipe-book.md` (100+ documented fusions)

**"What cards are in each expansion pack?"**  
→ `50-expansion-pack-specs.md` + `51-56-pack-*.md` (complete breakdowns)

**"How does turn resolution work?"**  
→ `71-daily-turn-flow-detailed.md` (step-by-step implementation)

---

## 🆕 Emotional Authenticity Integration (01-03) - Cross-System Enhancement

**NEW - October 14, 2025**

```
01-emotional-authenticity.md        Master plan for OCEAN + memory + context integration
02-system-by-system-enhancement.md  Detailed enhancement specs for each document
03-integrated-example.md            Complete scenario showing all systems working together
```

**Purpose:** These documents provide the master plan for integrating "real consequences, real behavior, real emotions, and real reactions" across ALL gameplay systems. Every system should query OCEAN traits, memories, environmental context, and parallel life circumstances to create emotionally authentic, novel-worthy experiences.

**Key Innovations:**
- Memory Echo System (past experiences trigger current states)
- Circumstance Stacking (multiple stressors compound)
- Emotional Capacity Gating (limited bandwidth affects options)
- Personality-Based Perception (same situation = different tension)
- NPC Observational Awareness (characters notice player state)
- Pattern Recognition & Breaking (track decision patterns across time)
- Environmental Context (weather, season, time affect mood)
- Emotional Journey Tracking (cards evolve based on significance)

**Read These If:**
- You're implementing any gameplay system
- You want to understand how systems integrate
- You need to ensure emotional authenticity
- You're generating novel content

**Implementation Timeline:** 10 weeks, 4 phases (see master plan)

---

## Document Organization

### Core Systems (10s) - Resource & Economy Implementation
```
10-resource-economy-spec.md          6 resources, exact budgets, scarcity formulas
11-turn-economy-implementation.md    168h weekly model, 3 turns/day, batching rules
12-success-probability-formulas.md   Exact math for success chances
13-meter-effects-tables.md           What happens at each meter threshold
14-emotional-state-mechanics.md      20 states, filtering rules, state transitions
```

**Key Deliverable:** Developers can implement resource systems directly from these specs.

---

### Card Systems (20s) - Complete Catalogs & Evolution
```
20-base-card-catalog.md              ALL 470 cards listed with stats
21-card-evolution-mechanics.md       Evolution triggers, requirements, AI templates
22-card-fusion-system.md             Complete fusion system with mechanics
23-fusion-type-specifications.md     5 fusion types with exact mechanics
24-card-generation-guidelines.md     AI generation templates for new cards
25-legendary-fusion-narratives.md    Epic 40-100 week fusion examples (Bookshop Saga, Found Family)
```

**Key Deliverable:** Content designers can create cards and fusions using these catalogs and templates. File 25 provides inspirational narrative examples of legendary fusion sequences.

---

### Narrative Systems (30s) - Templates & Scaffolding
```
30-decisive-decision-templates.md    Complete scaffolding with 20+ examples
31-narrative-arc-scaffolding.md      3-act season structure implementation
32-event-generation-rules.md         Event mix, frequency, triggers
33-dialogue-generation-templates.md  Context-aware dialogue with AI prompts
34-novel-generation-pipeline.md      Season → chapter conversion process
35-tension-maintenance-system.md     [NEW] Hook points, mystery threads, micro-cliffhangers
36-stakes-escalation-mechanics.md    [NEW] Consequence chains, dramatic neglect consequences
37-dramatic-irony-system.md          [ENHANCED] NPC perspectives, oblivious dialogue, memory callbacks, trait consequences
38-emotional-memory-tracking.md      [NEW] Emotional echoes, multi-season memory persistence
```

**Key Deliverable:** Narrative designers can author events and decisions with complete context. NEW docs (35-38) enable novel-quality tension, stakes, and emotional continuity.

---

### Progression Systems (40s) - Exact Mechanics
```
40-season-structure-spec.md          12/24/36 week options, pacing per length
41-phase-transition-mechanics.md     Triggers, thresholds, unlock progression
42-aspiration-goal-trees.md          90 aspirations with requirements
43-skill-progression-tables.md       30+ skills, Level 1-10 requirements
44-relationship-progression-spec.md  Levels 0-5, trust thresholds, interaction counts
```

**Key Deliverable:** Systems designers can implement progression using exact thresholds.

---

### Content Expansion (50s) - Pack Specifications
```
50-expansion-pack-specs.md           Overview of all 12+ packs
51-pack-city-explorer.md             60-card breakdown, Metro Transit system
52-pack-nature-adventure.md          40-card breakdown, wilderness mechanics
53-pack-career-ambition.md           50-card breakdown, career progression
54-pack-relationship-depth.md        50-card breakdown, advanced relationships
55-future-content-roadmap.md         Planned expansions beyond launch
```

**Key Deliverable:** Content teams can build packs following these specifications.

---

### Visual Systems (60s) - Asset Specifications
```
60-card-art-specifications.md        Art requirements per card type, resolutions
61-art-style-pack-specs.md           10 art packs with visual guidelines
62-animation-specifications.md       Holo cards, particle effects, loops
63-ui-flow-diagrams.md               Complete UI flows, state machines
```

**Key Deliverable:** Artists and UI developers have exact asset requirements.

---

### Integration & Flows (70s) - System Connections
```
70-complete-game-flow-diagram.md     End-to-end player journey with all systems
71-daily-turn-flow-detailed.md       Moment-to-moment implementation
72-weekly-cycle-implementation.md    Week structure, end-of-week processing
73-season-flow-implementation.md     Act I → II → III mechanics, climax systems
74-multi-season-continuity-spec.md   Tier 1-4 context management, compression
```

**Key Deliverable:** Integration engineers understand how systems connect.

---

### Compliance & Reference (80s)
```
80-master-truths-compliance.md       How gameplay specs align with canonical rules
81-implementation-glossary.md        Technical terms and their exact definitions
82-pseudocode-conventions.md         How to read code snippets in this documentation
```

---

## Reading Paths by Role

### For Game Developers
**Start Here:** 10 → 11 → 71 → 72  
**Then:** 20 → 21 → 70  
**Purpose:** Understand core loops, then expand to full systems

### For Content Designers
**Start Here:** 20 → 21 → 22 → 25  
**Then:** 30 → 31 → 32  
**Purpose:** Learn card creation, then narrative authoring. File 25 shows inspiring examples of epic narrative arcs.

### For Systems Designers
**Start Here:** 10 → 12 → 40 → 41  
**Then:** 70 → 74  
**Purpose:** Understand progression and balance

### For AI Engineers
**Start Here:** 21 → 24 → 33 → 34  
**Then:** 74  
**Purpose:** AI generation templates and context management

### For Artists & Animators
**Start Here:** 60 → 61 → 62  
**Then:** 20 (for card types)  
**Purpose:** Asset requirements and specifications

### For QA & Testers
**Start Here:** 70 → 71 → 80  
**Then:** All 10s-40s  
**Purpose:** Understand complete flows, then test individual systems

---

## Implementation Priorities

### Alpha (Core Loop)
**Must Have:** 10, 11, 20, 21, 71, 72  
**Why:** Basic gameplay loop functional

### Beta (Full Systems)
**Must Have:** 12, 13, 14, 22, 30, 31, 40, 41, 44, 70, 73  
**Why:** Complete core experience

### Launch (Polish & Content)
**Must Have:** All 20s-40s, 50, 60, 61, 74  
**Why:** Full content library, visual polish

### Post-Launch (Expansion)
**Must Have:** 51-55, 62, 63  
**Why:** Ongoing content and features

---

## Canonical Compliance

### All 2.gameplay/ Documents Must:
- [ ] Cite master_truths v1.2 at top
- [ ] Use canonical constants (12/24/36w seasons, Levels 0-5, Capacity 0-10, etc.)
- [ ] Reference 1.concept/ docs for philosophy (don't duplicate)
- [ ] Include worked examples with exact numbers
- [ ] Provide pseudocode or formulas where applicable
- [ ] Note any deviations with rationale
- [ ] Respect emotional capacity constraints (0-10 scale)
- [ ] Apply tension injection frequency guidelines
- [ ] Meet novel-quality thresholds (≥ 0.7)

### Compliance Checklist (from master_truths v1.2):
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
- [ ] **Emotional capacity constraints respected (0-10 scale; support rule: capacity + 2)**
- [ ] **Tension injection frequency followed (Level 1-2: 1 in 3; Level 3-4: 1 in 2; Level 5: nearly every)**
- [ ] **Dramatic irony mechanics used when knowledge gaps exist (score ≥ 0.6)**
- [ ] **Memory resonance factors applied to recall (weights: 0.7-0.95)**
- [ ] **Novel-quality thresholds met (≥ 0.7 overall; authenticity ≥ 0.7; tension ≥ 0.6; hooks ≥ 0.6)**
- [ ] This doc cites **Truths v1.2** at the top

---

## Current Status

### ✅ Completed
- master_truths v1.2 (canonical spec with Emotional Authenticity & Novel-Quality systems)
- Emotional authenticity integration docs (01-03)
- 1.concept/ docs all compliant
- CANONICAL-DECISIONS-LOG.md (decision tracking)
- This index (navigation hub)

### 🚧 In Progress
- Extracting implementation details from existing unified docs
- Creating numbered spec files (10-82)
- Migrating content while preserving ALL details

### ⏳ Pending
- Complete all 10s-80s files
- Deprecate unified-*.md files (archive, don't delete)
- Cross-reference check (all internal links work)
- Final compliance audit

---

## Migration from Old Structure

### Old Files → New Files Mapping

**`Gameplay Turns.md` →**
- `11-turn-economy-implementation.md` (168h model, 6 resources)
- `71-daily-turn-flow-detailed.md` (moment-to-moment)
- `72-weekly-cycle-implementation.md` (week structure)

**`narrative-arc-system.md` →**
- `30-decisive-decision-templates.md` (decision scaffolding)
- `31-narrative-arc-scaffolding.md` (3-act structure)
- `73-season-flow-implementation.md` (season mechanics)

**`fusion_trees_doc.md` →**
- `22-card-fusion-system.md` (complete fusion mechanics)
- `23-fusion-type-specifications.md` (5 fusion types)
- `25-legendary-fusion-narratives.md` (Bookshop Saga, Found Family examples)

**`Packs.md` →**
- `50-expansion-pack-specs.md` (overview)
- `51-56-pack-*.md` (individual pack specs)

**`Categories.md` →**
- `70-complete-game-flow-diagram.md` (card flow diagrams)

**`Base Cards.md` →**
- `20-base-card-catalog.md` (expanded with ALL 470 cards)

**`Expansions.md` →**
- `55-future-content-roadmap.md` (expansion taxonomy)

**`unified-card-system.md` → DISSOLVED**
- Philosophy → Already in 1.concept/11-card-system-basics.md
- Implementation → Distributed to 20, 21, 22, 23

**`unified-narrative-structure.md` → DISSOLVED**
- Philosophy → Already in 1.concept/15-progression-phases.md
- Implementation → Distributed to 30, 31, 32, 73

**`unified-content-expansion.md` → DISSOLVED**
- Philosophy → Already in 1.concept/17-monetization-model.md
- Implementation → Distributed to 50, 51-56

**`unified-gameplay-flow.md` → DISSOLVED**
- Philosophy → Already in 1.concept/21-turn-structure.md
- Implementation → Distributed to 71, 72, 73

---

## Maintenance Notes

### When Adding New Docs:
1. Follow numbering scheme (10s, 20s, etc.)
2. Add to this index
3. Include master_truths v1.1 compliance
4. Cross-reference 1.concept/ where appropriate
5. Use pseudocode conventions (see 82)
6. Include worked examples

### When Updating Constants:
1. Update master_truths first (with change proposal)
2. Update CANONICAL-DECISIONS-LOG.md
3. Search and update all 2.gameplay/ references
4. Update 1.concept/ if philosophy affected
5. Document migration path

### Quarterly Review:
- Verify all cross-references work
- Check for drift from master_truths
- Update status sections
- Archive deprecated content

---

## Questions?

**"Where's the philosophy explanation?"**  
→ See 1.concept/ docs. 2.gameplay/ focuses on implementation.

**"Why so many files?"**  
→ Large reference catalogs (470 cards, 100+ fusions) need dedicated files. Better than 3000-line monoliths.

**"Can I just read one file?"**  
→ Yes! Each file is self-contained with cross-references. Use the role-based reading paths above.

**"This contradicts 1.concept/!"**  
→ That's a bug. 2.gameplay/ must align with 1.concept/ philosophy. File an issue in CANONICAL-DECISIONS-LOG.md.

**"The master_truths says X, but this says Y"**  
→ master_truths wins. Update this file and document in CANONICAL-DECISIONS-LOG.md.

---

## Related Documentation

- **Canonical Authority:** `docs/master_truths_canonical_spec_v_1_2.md` (v1.2)
- **Design Philosophy:** `docs/1.concept/00-INDEX.md`
- **Decision Log:** `docs/CANONICAL-DECISIONS-LOG.md`
- **Update Summaries:**
  - `docs/UPDATE-SUMMARY-2025-10-13.md` (v1.1 compliance)
  - `docs/AI-NOVEL-QUALITY-ENHANCEMENTS-COMPLETE-2025-10-14.md` (AI enhancements for novel-quality)
  - `docs/MASTER-TRUTHS-V1.2-CHANGES-SUMMARY.md` (v1.1 → v1.2 changes)
  - `docs/IMPLEMENTATION-COMPLETE-NOVEL-ENHANCEMENTS-2025-10-14.md` (Novel generation integration)
- **Change Proposals:** `docs/CHANGE-PROPOSAL-EMOTIONAL-AUTHENTICITY-CANON.md`
- **Enhancement Plans:** `docs/2.gameplay/01-emotional-authenticity.md`

---

**This index will be updated as files are created and migrated.**  
**Last Major Update:** October 14, 2025 (Master Truths v1.2 + Emotional Authenticity & Novel-Quality systems integrated)

