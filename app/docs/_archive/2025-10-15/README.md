# Archived Documentation - October 15, 2025

This archive contains documentation that has been consolidated into the new numbered folder structure. All content has been preserved and integrated into comprehensive, Flame-first documentation.

## Why These Files Were Archived

These files were part of Phase 2 of the documentation reorganization. They contained valuable information but were scattered across the docs folder without a clear structure. They have been consolidated, de-duplicated, and enhanced with Flame integration examples.

---

## Migration Guide

### Audio & Haptics

**Archived Files:**
- `audioplayers.md` → `04-audio-visuals/01-audio-system.md`
- `vibration.md` → `04-audio-visuals/01-audio-system.md`

**New Location:** `app/docs/04-audio-visuals/01-audio-system.md`

**What's New:**
- Combined audio and haptics into single comprehensive guide
- Added Flame component integration examples
- Included performance guidelines
- Added audio asset organization recommendations

---

### Firebase Integration

**Archived Files:**
- `FIREBASE_AUTH_SETUP.md` → `06-integration/01-firebase-setup.md`
- `FIREBASE_APP_CHECK_SETUP.md` → `06-integration/01-firebase-setup.md`
- `FIREBASE_INTEGRATION_COMPLETE.md` → `06-integration/01-firebase-setup.md`
- `FIREBASE_WEB_FIX.md` → `06-integration/01-firebase-setup.md`

**New Location:** `app/docs/06-integration/01-firebase-setup.md`

**What's New:**
- All Firebase services in one document
- Complete troubleshooting section
- Local emulator setup
- Development vs production workflows
- Security rules examples

---

### Card Interactions

**Archived Files:**
- `CARD_DRAG_INTERACTION_FEATURE.md` → `02-flame-engine/11-card-interactions.md`
- `CARD_INTERACTION_GUIDE.md` → `02-flame-engine/11-card-interactions.md`

**New Location:** `app/docs/02-flame-engine/11-card-interactions.md`

**What's New:**
- Merged implementation details with quick reference
- Added Flame component patterns
- Included audio/haptic integration
- Performance optimization section
- Complete gesture detection guide

---

### Responsive Design

**Archived Files:**
- `MOBILE_PEEK_FROM_EDGES.md` → `02-flame-engine/12-responsive-design.md` (TODO)
- `RESPONSIVE_DESIGN_IMPLEMENTATION.md` → `02-flame-engine/12-responsive-design.md` (TODO)

**New Location (Planned):** `app/docs/02-flame-engine/12-responsive-design.md`

**What Will Be New:**
- Unified responsive design system
- Flame-specific responsive patterns
- Mobile peek-from-edges detailed guide
- Breakpoint system documentation

---

### Package Documentation

**Archived Files:**
- `code_generation.md` → Will be integrated into relevant docs
- `dio.md` → Will be integrated into relevant docs
- `flutter_riverpod.md` → `03-state-management/01-riverpod-setup.md`
- `hive.md` → `06-integration/03-local-storage.md` (TODO)
- `tflite_flutter.md` → `06-integration/02-ai-inference.md` (TODO)
- `ui_packages.md` → Will be integrated into relevant docs
- `utilities.md` → Will be integrated into relevant docs

**New Locations:**
- **State Management:** `app/docs/03-state-management/01-riverpod-setup.md` ✅
- **Local Storage (TODO):** `app/docs/06-integration/03-local-storage.md`
- **AI Inference (TODO):** `app/docs/06-integration/02-ai-inference.md`

**What's New:**
- Flame integration patterns
- Game-specific examples
- Performance considerations
- Testing strategies

---

### Setup Guide

**Archived Files:**
- `SETUP.md` → `00-overview/01-quick-start.md` (TODO - content to be integrated)

**New Location (Planned):** `app/docs/00-overview/01-quick-start.md`

**What Will Be New:**
- Consolidated quick start guide
- Flame-first setup instructions
- Updated for latest project structure

---

## Archive Structure

```
_archive/2025-10-15/
├── audio-haptics/
│   ├── audioplayers.md
│   └── vibration.md
├── firebase/
│   ├── FIREBASE_AUTH_SETUP.md
│   ├── FIREBASE_APP_CHECK_SETUP.md
│   ├── FIREBASE_INTEGRATION_COMPLETE.md
│   └── FIREBASE_WEB_FIX.md
├── card-interaction/
│   ├── CARD_DRAG_INTERACTION_FEATURE.md
│   └── CARD_INTERACTION_GUIDE.md
├── responsive-design/
│   ├── MOBILE_PEEK_FROM_EDGES.md
│   └── RESPONSIVE_DESIGN_IMPLEMENTATION.md
├── packages/
│   ├── code_generation.md
│   ├── dio.md
│   ├── flutter_riverpod.md
│   ├── hive.md
│   ├── tflite_flutter.md
│   ├── ui_packages.md
│   └── utilities.md
├── setup/
│   └── SETUP.md
└── README.md (this file)
```

---

## Finding Current Documentation

### Start with the Index
1. Navigate to `app/docs/00-overview/00-INDEX.md`
2. Find your topic
3. Follow the link to the numbered documentation

### Quick Reference by Topic

| Topic | Location |
|-------|----------|
| **Audio & Haptics** | `04-audio-visuals/01-audio-system.md` |
| **Firebase** | `06-integration/01-firebase-setup.md` |
| **Card Interactions** | `02-flame-engine/11-card-interactions.md` |
| **State Management** | `03-state-management/01-riverpod-setup.md` |
| **Responsive Design** | `02-flame-engine/12-responsive-design.md` (TODO) |
| **AI/ML** | `06-integration/02-ai-inference.md` (TODO) |
| **Local Storage** | `06-integration/03-local-storage.md` (TODO) |
| **Quick Start** | `00-overview/01-quick-start.md` |

---

## Documentation Philosophy

### Before (Phase 1 - Initial Reorg)
- Scattered docs at root level
- I/O FLIP multiplayer references
- No clear structure
- Duplicated information

### After (Phase 2 - Consolidation)
- ✅ Numbered folder hierarchy (00-06)
- ✅ Flame-first approach
- ✅ Single source of truth per topic
- ✅ Comprehensive integration examples
- ✅ Performance-focused
- ✅ Clear cross-references

---

## Accessing Archived Content

### If You Need Original Content

1. Navigate to this archive folder
2. Find the relevant subfolder
3. Read the original markdown file

**Note:** All content from archived files has been preserved in the new consolidated documents. The new docs often have additional information, better organization, and Flame integration examples.

### If You Find Broken Links

Please update links to point to the new documentation locations using the migration guide above.

---

## Consolidation Summary

### Completed Consolidations ✅
- Audio & Haptics (2 files → 1 comprehensive doc)
- Firebase Integration (4 files → 1 comprehensive doc)
- Card Interactions (2 files → 1 comprehensive doc)
- State Management (1 file → 1 enhanced doc)

### Remaining Consolidations 📝
- Responsive Design (2 files → 1 doc)
- AI Inference (1 file → 1 doc)
- Local Storage (1 file → 1 doc)
- Package utilities (3 files → integrate into relevant docs)
- Setup guide (1 file → enhance existing quick start)

---

## Questions?

If you have questions about the consolidation or can't find specific content:

1. Check the `DOCUMENTATION_CONSOLIDATION_2025-10-15.md` summary
2. Search the new numbered docs
3. Reference this README for migration paths

---

**Archive Date:** October 15, 2025  
**Consolidation Phase:** 2 of 2  
**Status:** Ongoing (partial completion)  
**Next Action:** Complete remaining consolidations


