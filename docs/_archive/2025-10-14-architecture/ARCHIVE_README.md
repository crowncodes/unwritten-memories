# Architecture Documentation Archive

**Archive Date:** October 14, 2025  
**Reason:** Restructured to numbered documentation (50-69 series)  
**New Location:** `docs/5.architecture/`

---

## What Happened?

The architecture documentation was restructured from unnumbered files to a numbered series (50-69) following the established pattern used in:
- `docs/1.concept/` (10-22 series)
- `docs/2.gameplay/` (10-82 series)  
- `docs/3.architecture/` (30-39 series)

This archive preserves all original documentation for historical reference.

---

## Document Migration Map

### Core Architecture

| Old Document | New Document | Notes |
|--------------|--------------|-------|
| ARCHITECTURE-README.md | 00-INDEX.md | Now includes all navigation |
| tech_architecture_doc.md | 50-architecture-overview.md | Consolidated with I/O FLIP analysis |
| FLUTTER-PROJECT-SETUP.md | 51-project-structure-guide.md<br>52-development-environment-setup.md | Split into structure and setup |
| IMPLEMENTATION-PLAN-MVP.md | 50-architecture-overview.md<br>54-build-configuration-deployment.md | Integrated into overview and deployment |
| README.md | 00-INDEX.md | Replaced by comprehensive index |

### Flame Engine

| Old Document | New Document | Notes |
|--------------|--------------|-------|
| CARD-DRAG-PHYSICS-GUIDE.md | 56-card-physics-animations.md | Focused on I/O FLIP physics |
| IO-FLIP-ARCHITECTURE-ANALYSIS.md | 50-architecture-overview.md<br>55-flame-engine-fundamentals.md<br>62-flame-integration.md | Distributed across multiple docs |

### Guides

| Old Document | New Document | Notes |
|--------------|--------------|-------|
| QUICK-START-DEVELOPER-GUIDE.md | 00-INDEX.md<br>52-development-environment-setup.md | Integrated into index and setup |
| IMPLEMENTATION-DELIVERABLES-SUMMARY.md | 00-INDEX.md | Now part of index with document status |

### Miscellaneous

| Old Document | New Document | Notes |
|--------------|--------------|-------|
| b0d2d175.md | (various) | Content distributed as needed |

---

## New Documentation Structure

### Complete Series (50-69)

**Core Architecture (50-54):**
- 50-architecture-overview.md
- 51-project-structure-guide.md
- 52-development-environment-setup.md
- 53-state-management-architecture.md
- 54-build-configuration-deployment.md

**Flame Engine (55-59):**
- 55-flame-engine-fundamentals.md
- 56-card-physics-animations.md
- 57-component-architecture.md
- 58-camera-viewport-systems.md
- 59-performance-optimization-flame.md

**Package Integrations (60-66):**
- 60-package-integration-overview.md
- 61-riverpod-integration.md
- 62-flame-integration.md
- 63-audio-haptics-integration.md
- 64-storage-persistence-integration.md
- 65-networking-integration.md
- 66-ai-ml-integration.md

**Testing & Quality (67-69):**
- 67-testing-strategy.md
- 68-performance-monitoring.md
- 69-code-quality-standards.md

**Index:**
- 00-INDEX.md

---

## Why the Restructure?

### Problems with Old Structure
1. **No clear navigation** - Hard to find specific topics
2. **Inconsistent numbering** - Some numbered, most not
3. **Overlapping content** - Same topics in multiple docs
4. **No reading paths** - Unclear what to read when
5. **Not aligned** - Different pattern from concept/gameplay/AI docs

### Benefits of New Structure
1. ✅ **Clear navigation** - 00-INDEX.md with reading paths
2. ✅ **Consistent numbering** - 50-69 series matches other folders
3. ✅ **Single responsibility** - Each doc covers one topic
4. ✅ **Reading paths by role** - Flutter dev, Flame dev, Integration, etc.
5. ✅ **Aligned patterns** - Follows 1.concept/, 2.gameplay/, 3.ai/ structure

---

## How to Use This Archive

### If You Need Old Content

1. **Find the old doc** in this folder
2. **Check migration map** above for new location
3. **Read new doc** for updated content
4. **Reference old doc** only if content missing

### If You Find Missing Content

If something from these archived docs is missing in the new structure:

1. Check the migration map to confirm which new doc should contain it
2. Review the new doc thoroughly
3. If truly missing, file an issue referencing:
   - Old document name
   - Specific section/content
   - Suggested new location

---

## Archive Retention

These files are preserved for:
- **Historical reference**
- **Content verification**
- **Migration audit**
- **Fallback if needed**

**Do not delete** - Disk space is cheap, knowledge is expensive.

---

## Questions?

See `docs/5.architecture/00-INDEX.md` for:
- Complete new documentation
- Reading paths by role
- Quick navigation
- Document status

---

**Last Updated:** October 14, 2025  
**Status:** Archive Complete  
**New Docs:** All 21 numbered docs created

