# Unwritten 2.gameplay/ Reorganization - Visual Summary

## Before & After Comparison

### BEFORE (Current State - Chaotic)

```
docs/2.gameplay/
├── unified-card-system.md          (1,874 lines) 📚 MASSIVE
├── unified-narrative-structure.md  (1,254 lines) 📚 MASSIVE
├── unified-content-expansion.md    (870 lines)   📚 LARGE
├── unified-gameplay-flow.md        (1,161 lines) 📚 LARGE
├── Base Cards.md                   (25 lines)    📄
├── Categories.md                   (1,649 lines) 📚 MASSIVE
├── Expansions.md                   (182 lines)   📄
├── fusion_trees_doc.md             (1,509 lines) 📚 MASSIVE
├── Packs.md                        (614 lines)   📄
├── Gameplay Turns.md               (950 lines)   📄
└── narrative-arc-system.md         (1,391 lines) 📚 MASSIVE

Total: 11 files, ~11,479 lines
Problems: Overlap, contradictions, no index, hard to navigate
```

---

### AFTER (Target State - Organized)

```
docs/2.gameplay/
│
├── 00-INDEX.md                     📍 NAVIGATION HUB
│
├── 🎮 CORE SYSTEMS (10s)
│   ├── 10-resource-economy.md           ⚡ Energy, time, money, social capital
│   ├── 11-emotional-state-system.md     😊 20 states that drive gameplay
│   ├── 12-personality-integration.md    🧠 Big 5 affects gameplay
│   └── 13-success-probability.md        🎲 Success formula & modifiers
│
├── 🎴 CARD SYSTEMS (20s)
│   ├── 20-card-taxonomy.md              📊 7-tier organization
│   ├── 21-base-card-catalog.md          📚 470+ base cards listed
│   ├── 22-card-evolution.md             🌱 Base → Evolved → Legendary
│   ├── 23-fusion-system.md              💫 Fusion mechanics & trees
│   └── 24-card-generation-ai.md         🤖 AI personalization
│
├── ⏱️ TURN & FLOW (30s)
│   ├── 30-turn-structure.md             📅 Daily/weekly/seasonal turns
│   ├── 31-gameplay-flow.md              🎯 Pacing, batching, automation
│   ├── 32-decision-weight-system.md     ⚖️ 4-tier decisions
│   └── 33-hand-composition.md           🎴 Card drawing algorithm
│
├── 📖 NARRATIVE & STORY (40s)
│   ├── 40-narrative-arc-system.md       🎬 Multi-phase arcs
│   ├── 41-decisive-decisions.md         🚨 Decision templates
│   ├── 42-crisis-events.md              ⚠️ Crisis triggers
│   ├── 43-npc-behavior.md               👥 NPC agency
│   └── 44-memory-archive.md             💾 What gets remembered
│
├── 📈 PROGRESSION & SEASONS (50s)
│   ├── 50-season-structure.md           📆 12-week arc design
│   ├── 51-lifetime-progression.md       🌟 Multi-season continuity
│   ├── 52-phase-transitions.md          🔄 Life-changing events
│   └── 53-skill-development.md          📊 Skill trees & mastery
│
├── 📦 EXPANSION & CONTENT (60s)
│   ├── 60-pack-system-overview.md       🎁 How packs work
│   ├── 61-pack-catalog.md               📋 Complete pack specs
│   ├── 62-pack-integration.md           🔧 Technical integration
│   └── 63-content-roadmap.md            🗺️ Release schedule
│
├── 💰 ECONOMY & MONETIZATION (70s)
│   ├── 70-monetization-model.md         💎 V2 Essence token (canonical)
│   ├── 71-free-tier-spec.md             🎁 What free players get
│   ├── 72-subscription-tiers.md         ⭐ Plus/Ultimate benefits
│   └── 73-ethical-principles.md         ❤️ No dark patterns
│
└── 📦 _archive/                         🗄️ OLD FILES (reference only)
    └── [11 old files moved here]

Total: 29 files (28 numbered + 1 index), ~11,479 lines (same content, organized)
Benefits: Clear structure, no overlap, easy navigation, single source of truth
```

---

## Content Flow Map

### Where Content Went (Detailed Mapping)

```
unified-card-system.md (1,874 lines)
├─→ 20-card-taxonomy.md          (lines 11-1061)   7-tier system
├─→ 21-base-card-catalog.md      (lines 1544-1580) 470+ cards
├─→ 22-card-evolution.md         (lines 1194-1351) Evolution stages
├─→ 23-fusion-system.md          (lines 1353-1541) Fusion mechanics
├─→ 24-card-generation-ai.md     (lines 1304-1349) AI parameters
└─→ 33-hand-composition.md       (lines 1587-1828) Integration

unified-narrative-structure.md (1,254 lines)
├─→ 40-narrative-arc-system.md   (lines 57-181)    Multi-phase arcs
├─→ 41-decisive-decisions.md     (lines 183-268)   Decision templates
├─→ 42-crisis-events.md          (lines 270-352)   Crisis triggers
├─→ 43-npc-behavior.md           (lines 479-518)   NPC agency
├─→ 44-memory-archive.md         (lines 520-646)   Archive system
├─→ 12-personality-integration.md (lines 359-411)  OCEAN model
└─→ 50-season-structure.md       (lines 13-54)     Season model

unified-content-expansion.md (870 lines)
├─→ 60-pack-system-overview.md   (lines 13-80)     Pack philosophy
├─→ 61-pack-catalog.md           (lines 148-458)   Pack specs
├─→ 62-pack-integration.md       (lines 460-509)   Integration
├─→ 63-content-roadmap.md        (lines 716-751)   Release schedule
├─→ 70-monetization-model.md     (V2 update)       Essence tokens
└─→ 71-free-tier-spec.md         (lines 607-629)   Free tier

unified-gameplay-flow.md (1,161 lines)
├─→ 10-resource-economy.md       (lines 42-326)    6 resources
├─→ 11-emotional-state-system.md (lines 551-731)   20 states
├─→ 13-success-probability.md    (lines 272-325)   Success formula
├─→ 30-turn-structure.md         (lines 327-548)   Turn architecture
├─→ 31-gameplay-flow.md          (lines 851-1003)  Pacing systems
├─→ 32-decision-weight-system.md (lines 986-1054)  4-tier decisions
└─→ 33-hand-composition.md       (lines 938-963)   Priority system

Gameplay Turns.md (950 lines)
├─→ 10-resource-economy.md       (lines 1-450)     Turn economy
├─→ 13-success-probability.md    (lines 420-520)   Probability
└─→ 30-turn-structure.md         (lines 1-450)     Turn detail

narrative-arc-system.md (1,391 lines)
├─→ 40-narrative-arc-system.md   (lines 1-600)     Arc templates
├─→ 41-decisive-decisions.md     (lines 600-900)   Templates
└─→ 42-crisis-events.md          (lines 900-1100)  Crisis detail

fusion_trees_doc.md (1,509 lines)
├─→ 23-fusion-system.md          (full file)       Fusion trees
└─→ 22-card-evolution.md         (lines 1-300)     Evolution context

Categories.md (1,649 lines)
├─→ 20-card-taxonomy.md          (lines 1-200)     Overview
├─→ 21-base-card-catalog.md      (lines 200-1400)  Card lists
└─→ 33-hand-composition.md       (lines 1400-1649) Flow diagram

Packs.md (614 lines)
├─→ 60-pack-system-overview.md   (lines 1-150)     Overview
├─→ 61-pack-catalog.md           (full file)       Specs
└─→ 62-pack-integration.md       (lines 400-600)   Integration

Expansions.md (182 lines)
├─→ 61-pack-catalog.md           (broader taxonomy)
└─→ 63-content-roadmap.md        (future families)

Base Cards.md (25 lines)
└─→ 21-base-card-catalog.md      (merged)          Card catalog
```

---

## Reading Paths (How to Navigate)

### For Developers (Building the Game)

```
START HERE
    ↓
[00-INDEX.md] - Get the map
    ↓
UNDERSTAND RESOURCES
    ├─→ 10-resource-economy.md    (Energy, time, money, etc.)
    └─→ 11-emotional-state-system.md (20 states)
    ↓
UNDERSTAND CARDS
    ├─→ 20-card-taxonomy.md       (7 tiers)
    ├─→ 21-base-card-catalog.md   (470+ cards)
    ├─→ 22-card-evolution.md      (How cards evolve)
    └─→ 23-fusion-system.md       (Fusions)
    ↓
UNDERSTAND FLOW
    ├─→ 30-turn-structure.md      (Daily/weekly/seasonal)
    ├─→ 31-gameplay-flow.md       (Pacing)
    └─→ 33-hand-composition.md    (Card drawing)
    ↓
UNDERSTAND STORY
    ├─→ 40-narrative-arc-system.md (Story arcs)
    └─→ 50-season-structure.md    (12-week seasons)
    ↓
UNDERSTAND EXPANSION
    ├─→ 60-pack-system-overview.md (How packs work)
    └─→ 61-pack-catalog.md        (Pack specs)
    ↓
DONE - Start building!
```

### For Designers (Creating Content)

```
START HERE
    ↓
[00-INDEX.md] - Get the map
    ↓
UNDERSTAND CARDS
    ├─→ 20-card-taxonomy.md       (7 tiers)
    ├─→ 21-base-card-catalog.md   (470+ examples)
    ├─→ 22-card-evolution.md      (Evolution rules)
    └─→ 23-fusion-system.md       (Fusion possibilities)
    ↓
UNDERSTAND STORY
    ├─→ 40-narrative-arc-system.md (Arc structure)
    ├─→ 41-decisive-decisions.md   (Decision templates)
    └─→ 42-crisis-events.md       (Crisis design)
    ↓
UNDERSTAND PACKS
    ├─→ 60-pack-system-overview.md (How packs integrate)
    └─→ 61-pack-catalog.md        (Pack examples)
    ↓
CREATE CONTENT - Use templates!
```

### For Product/Business

```
START HERE
    ↓
[00-INDEX.md] - Get the map
    ↓
UNDERSTAND MONETIZATION
    ├─→ 70-monetization-model.md  (V2 Essence token)
    ├─→ 71-free-tier-spec.md      (What's free)
    └─→ 73-ethical-principles.md  (Our values)
    ↓
UNDERSTAND CONTENT
    ├─→ 60-pack-system-overview.md (Pack philosophy)
    ├─→ 61-pack-catalog.md        (Pack catalog)
    └─→ 63-content-roadmap.md     (Release schedule)
    ↓
UNDERSTAND SYSTEMS
    ├─→ 11-emotional-state-system.md (Core gameplay)
    └─→ 50-season-structure.md    (Progression)
    ↓
MAKE DECISIONS - Data-driven!
```

---

## Key Improvements

### ✅ Problem Solved: Overlap & Duplication

**BEFORE:** Card evolution appeared in 3 different files
- unified-card-system.md (lines 1194-1351)
- unified-narrative-structure.md (as part of NPC evolution)
- fusion_trees_doc.md (in context of fusion progression)

**AFTER:** Card evolution in ONE file
- 22-card-evolution.md (complete, definitive)
- Cross-referenced from 23-fusion-system.md and 43-npc-behavior.md

---

### ✅ Problem Solved: Contradictions

**BEFORE:** Different scales for relationships
- Some docs: "Level 1-5"
- Some docs: "MAX (10/10)"
- Some docs: "Level 6: Life Partnership"

**AFTER:** Canonical scale in all files
- 5 discrete levels (0-5)
- Trust meter 0.0-1.0 (continuous)
- Life Partnership = status flag, not Level 6
- Documented in 22-card-evolution.md, applied everywhere

---

### ✅ Problem Solved: No Clear Entry Point

**BEFORE:** Which file to read first?
- All 4 unified docs seemed equally important
- No index or guide

**AFTER:** Clear navigation
- 00-INDEX.md is the hub
- Reading paths for different roles
- Numbered progression (10s → 20s → 30s)
- "Quick Answers" section

---

### ✅ Problem Solved: Hidden Concrete Details

**BEFORE:** Turn economy buried in 950-line file
- Gameplay Turns.md had the specific budgets
- But mixed with other content
- Hard to find "How much energy per turn?"

**AFTER:** Resource budgets front & center
- 10-resource-economy.md has ALL resource specs
- Clear tables: Energy 3/3/2, Time 168h/week, etc.
- Easy to reference during implementation

---

### ✅ Problem Solved: Hard to Maintain

**BEFORE:** Change emotional state system
- Must update unified-gameplay-flow.md (lines 551-731)
- AND unified-card-system.md (lines 1587-1619)
- AND any examples in other docs
- Easy to miss one → contradiction

**AFTER:** Change in one place
- 11-emotional-state-system.md is the source of truth
- Other files cross-reference it
- Single edit propagates conceptually

---

## File Size Comparison

### BEFORE (4 massive files)
```
unified-card-system.md          1,874 lines 😰 TOO LARGE
unified-narrative-structure.md  1,254 lines 😰 TOO LARGE
unified-gameplay-flow.md        1,161 lines 😰 TOO LARGE
fusion_trees_doc.md             1,509 lines 😰 TOO LARGE
```

### AFTER (28 focused files)
```
10-resource-economy.md          ~400 lines  ✅ READABLE
11-emotional-state-system.md    ~500 lines  ✅ READABLE
20-card-taxonomy.md             ~600 lines  ✅ READABLE
21-base-card-catalog.md         ~800 lines  ✅ SEARCHABLE
23-fusion-system.md             ~700 lines  ✅ FOCUSED
30-turn-structure.md            ~400 lines  ✅ CLEAR
40-narrative-arc-system.md      ~500 lines  ✅ TEMPLATE
50-season-structure.md          ~400 lines  ✅ CONCISE
60-pack-system-overview.md      ~500 lines  ✅ COMPLETE
70-monetization-model.md        ~600 lines  ✅ CANONICAL

Average: ~500 lines per file
Max: ~800 lines (catalog)
Benefit: Easy to read in one sitting
```

---

## Benefits Summary

### For the Team

**Developers:**
- ✅ Know exactly where to find implementation details
- ✅ Smaller files = faster review in PRs
- ✅ Clear order to build systems (10s → 20s → 30s)
- ✅ No duplication = no confusion

**Designers:**
- ✅ Card catalog in one place (21)
- ✅ Templates for arcs, decisions, crises (40s)
- ✅ Pack specs organized (61)
- ✅ Examples abundant

**Product/Business:**
- ✅ Monetization canonical (70-73)
- ✅ Free tier clearly defined (71)
- ✅ Content roadmap visible (63)
- ✅ Ethical stance documented (73)

**Writers:**
- ✅ NPC behavior guidelines (43)
- ✅ Decision templates (41)
- ✅ Memory/archive rules (44)
- ✅ Narrative arc structure (40)

**QA/Testing:**
- ✅ Success formulas documented (13)
- ✅ Resource budgets clear (10)
- ✅ Crisis triggers defined (42)
- ✅ Testable specifications

### For Maintenance

- ✅ **Findability:** "Where's the turn structure?" → 30-turn-structure.md
- ✅ **Updatability:** One file to edit, not four
- ✅ **Version control:** Smaller diffs, clearer changes
- ✅ **Onboarding:** New team members follow reading paths
- ✅ **Reference:** Quick answers in index
- ✅ **Consistency:** Canonical decisions enforced

---

## Migration Status

### Phase Status

```
[✅] Phase 1: Setup (Index & Placeholders)
[ ] Phase 2: Core Systems (10-13)
[ ] Phase 3: Card Systems (20-24)
[ ] Phase 4: Turn & Flow (30-33)
[ ] Phase 5: Narrative & Story (40-44)
[ ] Phase 6: Progression & Seasons (50-53)
[ ] Phase 7: Expansion & Content (60-63)
[ ] Phase 8: Economy & Monetization (70-73)
[ ] Phase 9: Archive Old Files
[ ] Phase 10: Update Cross-References
[ ] Phase 11: Validation
```

### Canonicalization Status

```
Relationship Scale:
[ ] 22-card-evolution.md updated (MAX 10/10 → Trust 1.0, Level 5)
[ ] 23-fusion-system.md updated (Level 6 → Status flag)
[ ] All examples normalized to Levels 0-5

Archives:
[ ] 44-memory-archive.md updated (unlimited season, 3 lifetime)
[ ] 71-free-tier-spec.md updated

Emotional States:
[ ] 11-emotional-state-system.md (DRAINED → EXHAUSTED)
[ ] All references updated

Pack Sizes:
[ ] 60-pack-system-overview.md (Standard/Deluxe/Mega)
[ ] 61-pack-catalog.md (pricing updated)

Monetization:
[ ] 70-monetization-model.md (V2 Essence canonical)
[ ] Old "$4.99 Premium" retired

FOMO:
[ ] 31-gameplay-flow.md (tone adjusted)
[ ] 32-decision-weight-system.md (time pauses clarified)
[ ] 73-ethical-principles.md (policy clarified)
```

---

## Next Actions

1. **Review this summary** with team
2. **Approve reorganization plan** (REORGANIZATION-PLAN.md)
3. **Assign phase ownership** (who does what)
4. **Create feature branch** (`feature/reorganize-gameplay-docs`)
5. **Execute Phase 2** (Core Systems 10-13) as proof of concept
6. **Review & iterate** before continuing
7. **Complete remaining phases**
8. **Merge to main**

---

**Document Status:** Ready for team review  
**Related Documents:**
- REORGANIZATION-PLAN.md (detailed workflow)
- 00-INDEX.md (navigation hub)

**Timeline:** 18-24 hours total work  
**Can be parallelized:** Yes (different number ranges)  
**Breaking changes:** None (content preserved, just reorganized)

---

**Benefits in One Sentence:**
> Turn 11 chaotic, overlapping files into 28 focused, cross-referenced, canonical documents with clear navigation—making it 10x easier to find, maintain, and implement the game.

