# Archive - Superseded 2.gameplay/ Documents

**Date Archived:** October 14, 2025  
**Reason:** Content migrated to numbered implementation spec files (00-82)  
**Status:** Historical reference only - DO NOT USE for implementation

---

## What's Here

This archive contains 20 documents from the October 13, 2025 reorganization and earlier development:

### 📊 Session Progress Documents (6 files)
Temporary tracking documents from October 13, 2025 session showing implementation progress.

**See:** `2025-10-13-session/`

### 📋 Reorganization Planning (5 files)
Planning documents created during the `2.gameplay/` reorganization process.

**See:** `reorganization-planning/`

### 📚 Source Documents - Migrated (9 files)
Original content documents whose content has been extracted and migrated to numbered specs.

**See:** `source-docs-migrated/`

### 🔗 Unified Docs - Dissolved (4 files)
"Unified" documents that mixed philosophy and implementation. Philosophy moved to `1.concept/`, implementation distributed to numbered specs.

**See:** `unified-docs-dissolved/`

---

## Why Were These Archived?

**Problem:** These documents mixed:
1. Philosophy (WHY) with implementation (HOW)
2. Progress tracking with permanent specifications
3. Multiple systems in single large files

**Solution:** Reorganization into:
- **`docs/1.concept/`** - Design philosophy (WHY & WHAT)
- **`docs/2.gameplay/`** - Implementation specs (HOW & EXACT)
- **Numbered spec files** - Each system in dedicated file

---

## Where Did the Content Go?

### Session/Progress Documents → Nowhere
These were **temporary tracking documents**. Their content was superseded by the completed specs they tracked.

### Reorganization Documents → Nowhere
These were **planning artifacts**. The reorganization is complete, structure is now standard.

### Source Documents → Numbered Specs

| Old File | New Location(s) | Status |
|----------|----------------|--------|
| `Base Cards.md` | `20-base-card-catalog.md` | ✅ Migrated |
| `Categories.md` | `20-base-card-catalog.md` + `70-complete-game-flow-diagram.md` | ✅ Migrated |
| `fusion_trees_doc.md` | `22-card-fusion-system.md` + `23-fusion-type-specifications.md` | ✅ Migrated |
| `Gameplay Turns.md` | `11-turn-economy-implementation.md` + `71-daily-turn-flow-detailed.md` + `72-weekly-cycle-implementation.md` | ✅ Migrated |
| `narrative-arc-system.md` | `30-decisive-decision-templates.md` + `31-narrative-arc-scaffolding.md` + `32-event-generation-rules.md` | ✅ Migrated |
| `Packs.md` | `50-expansion-pack-specifications.md` | ✅ Migrated |
| `Expansions.md` | `50-expansion-pack-specifications.md` (pack families) | ✅ Migrated |

### Unified Documents → Philosophy + Implementation Split

| Old File | Philosophy → | Implementation → |
|----------|--------------|------------------|
| `unified-card-system.md` | `1.concept/11-card-system-basics.md` | `20-base-card-catalog.md`, `21-card-evolution-mechanics.md`, `22-card-fusion-system.md`, `23-fusion-type-specifications.md` |
| `unified-narrative-structure.md` | `1.concept/15-progression-phases.md` | `30-decisive-decision-templates.md`, `31-narrative-arc-scaffolding.md`, `32-event-generation-rules.md`, `73-season-flow-implementation.md` |
| `unified-content-expansion.md` | `1.concept/17-monetization-model.md` | `50-expansion-pack-specifications.md` |
| `unified-gameplay-flow.md` | `1.concept/21-turn-structure.md` | `71-daily-turn-flow-detailed.md`, `72-weekly-cycle-implementation.md`, `73-season-flow-implementation.md` |

---

## Can I Still Read These?

**Yes!** They're archived, not deleted. However:

⚠️ **DO NOT use for implementation** - Content may be outdated or superseded  
✅ **DO use for historical reference** - Understanding how systems evolved  
✅ **DO use for context** - Seeing what decisions were made and why

**For implementation, always use:**
- **`docs/master_truths_canonical_spec_v_1_2.md`** - Canonical authority
- **`docs/1.concept/`** - Design philosophy
- **`docs/2.gameplay/00-82`** - Implementation specs

---

## Archive Structure

```
_ARCHIVE/
├── README.md (this file)
├── ARCHIVAL-ANALYSIS-2025-10-14.md (detailed analysis)
│
├── 2025-10-13-session/
│   ├── README.md
│   ├── COMPLETE-SESSION-SUMMARY-2025-10-13.md
│   ├── CURRENT-SESSION-SUMMARY.md
│   ├── FINAL-SESSION-SUMMARY.md
│   ├── IMPLEMENTATION-PROGRESS-2025-10-13.md
│   ├── SESSION-PROGRESS-2025-10-13.md
│   └── CARD-SYSTEM-COMPLETE-2025-10-13.md
│
├── reorganization-planning/
│   ├── README.md
│   ├── REORGANIZATION-PLAN.md
│   ├── REORGANIZATION-REASSESSMENT.md
│   ├── REORGANIZATION-COMPARISON.md
│   ├── REORGANIZATION-SUMMARY.md
│   └── SEASON-FLOW-CLARIFICATION-2025-10-13.md
│
├── source-docs-migrated/
│   ├── README.md
│   ├── Base-Cards.md
│   ├── Categories.md
│   ├── fusion_trees_doc.md
│   ├── Gameplay-Turns.md
│   ├── narrative-arc-system.md
│   ├── Packs.md
│   └── Expansions.md
│
└── unified-docs-dissolved/
    ├── README.md
    ├── unified-card-system.md
    ├── unified-narrative-structure.md
    ├── unified-content-expansion.md
    └── unified-gameplay-flow.md
```

---

## Questions?

**"I need information from an archived doc"**  
→ Find the migration target in the table above and use the new spec instead.

**"The new spec is missing something from the archive"**  
→ File an issue in `CANONICAL-DECISIONS-LOG.md` - we may have missed content during migration.

**"Why not just delete these?"**  
→ Historical context is valuable. These show how the system evolved and document decision rationale.

**"Can I reference these in new docs?"**  
→ No. Reference the new numbered specs or `1.concept/` docs instead.

---

**Last Updated:** October 14, 2025  
**See:** `ARCHIVAL-ANALYSIS-2025-10-14.md` for detailed analysis

