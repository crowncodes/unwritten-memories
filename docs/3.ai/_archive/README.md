# AI Documentation Archive

**Archived:** October 2025  
**Reason:** Documentation reorganization for clarity and consistency

---

## What's in This Archive

This archive contains documents that were superseded during the AI documentation reorganization.

### `old-numbering/`
Contains original numbered documents (30-39) before the complete reorganization. These are preserved for reference during the transition period.

**Original Structure:**
```
30-ai-architecture-overview.md
31-hybrid-cloud-local-system.md
32-prompt-engineering-principles.md
33-prompt-templates-library.md
34-context-memory-systems.md
35-consistency-coherence.md
36-local-model-training.md
37-model-deployment-optimization.md
37-training-data-quality-standards.md (duplicate number!)
38-latency-ux-strategies.md
39-cost-performance-targets.md
```

**New Location:**
- 30 → 01-ai-strategy-overview.md
- 31 → 40-hybrid-cloud-local-system.md
- 32 → 10-prompt-engineering-principles.md
- 33 → 11-prompt-templates-library.md
- 34 → 12-context-memory-systems.md
- 35 → 13-consistency-coherence.md
- 36 → 41-local-model-training.md
- 37 → 42-model-deployment-optimization.md
- 37 (duplicate) → 43-training-data-quality-standards.md
- 38 → 70-latency-ux-strategies.md
- 39 → 71-cost-performance-targets.md

### `meta-docs/`
Contains meta-documentation that became redundant after reorganization.

**Archived Documents:**
- `GENKIT_DOCUMENTATION_INDEX.md` - Navigation merged into main 00-INDEX.md
- `GENKIT_DOCUMENTATION_SUMMARY.md` - Content merged into README.md
- `AI_INTEGRATION_COMPLETE_SUMMARY.md` - Recommendations merged into README.md

**Why Archived:**
- Redundant with main navigation (00-INDEX.md)
- Redundant with README.md
- Meta-documents about other docs not needed post-reorganization

---

## Why This Reorganization?

### Problems with Old Structure:
1. ❌ **Confusing numbering** - Started at 30 (not 00)
2. ❌ **Duplicate numbers** - Two "37" documents
3. ❌ **No clear categories** - Everything mixed together
4. ❌ **Hard to navigate** - No logical grouping
5. ❌ **Separate Genkit navigation** - Fragmented documentation
6. ❌ **Unclear strategy** - Didn't clarify "Firebase AI now, Genkit later"

### New Structure Benefits:
1. ✅ **Clear categories** - Strategy (01-09), Prompts (10-19), Firebase (20-29), Genkit (30-39), Local (40-49), Storage (50-59), Flame (60-69), UX (70-79), Status (80-89)
2. ✅ **Consistent numbering** - No gaps, no duplicates, matches other doc folders
3. ✅ **Easy navigation** - Find anything in <30 seconds
4. ✅ **Clear strategy** - Implementation phases doc shows Firebase AI → Genkit path
5. ✅ **Complete coverage** - Added missing docs (storage system, Flame integration)
6. ✅ **Single navigation** - One 00-INDEX.md, one README.md

---

## When to Use Archived Docs

### Use Archived Docs If:
- You have bookmarks to old document names
- You're looking for historical context on decisions
- You need to see the "before" state of reorganization

### Use New Docs For:
- Everything else - new docs are updated and complete
- Current implementation work
- Learning the AI system

---

## Migration Map

See `DOCS_MIGRATION_MAP.md` in the root of `docs/3.ai/` for complete old → new document mapping.

---

**Archive Note:** These documents are preserved for historical reference. They may not be updated going forward. Always use the current documentation structure for active development.


