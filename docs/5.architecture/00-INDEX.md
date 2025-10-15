# Architecture Documentation Index

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete

---

## Overview

Complete architecture documentation for Unwritten, a Flutter + Flame narrative card game. This folder contains 22 numbered documents (50-70) covering architecture, Flame engine, package integrations, testing, and implementation reference.

**Pattern:** I/O FLIP (Google I/O 2023) - Proven at scale  
**Stack:** Flutter 3.27+ | Flame 1.20+ | Dart Frog | Firebase | Riverpod 3.x

---

## Quick Navigation

### 🎯 New to the Project?

**Start here:**
1. Read `50-architecture-overview.md` (architecture decisions)
2. Read `51-project-structure-guide.md` (folder structure)
3. Follow `52-development-environment-setup.md` (setup)
4. Study `55-flame-engine-fundamentals.md` (Flame basics)
5. Review `56-card-physics-animations.md` (I/O FLIP physics)

### 🔥 Flame Developer?

**Flame-specific docs:**
- `55-flame-engine-fundamentals.md` - Core concepts
- `56-card-physics-animations.md` - I/O FLIP drag physics
- `57-component-architecture.md` - Component patterns
- `58-camera-viewport-systems.md` - Camera control
- `59-performance-optimization-flame.md` - 60 FPS optimization

### 📦 Integration Work?

**Package-specific docs:**
- `60-package-integration-overview.md` - All packages
- `61-riverpod-integration.md` - Riverpod 3.x
- `62-flame-integration.md` - Flame setup
- `63-audio-haptics-integration.md` - Audio & haptics
- `64-storage-persistence-integration.md` - Hive storage
- `65-networking-integration.md` - Dio HTTP client
- `66-ai-ml-integration.md` - TensorFlow Lite

### 🧪 Testing & Quality?

**Testing docs:**
- `67-testing-strategy.md` - Unit, widget, integration tests
- `68-performance-monitoring.md` - DevTools & monitoring
- `69-code-quality-standards.md` - Linting & standards

---

## Complete Document List

### Core Architecture (50-54)

| # | Document | Purpose | Status |
|---|----------|---------|--------|
| **50** | `architecture-overview.md` | Architecture decisions, I/O FLIP patterns, tech stack | ✅ |
| **51** | `project-structure-guide.md` | Complete folder structure, Clean Architecture | ✅ |
| **52** | `development-environment-setup.md` | Setup guide, dependencies, platform config | ✅ |
| **53** | `state-management-architecture.md` | Riverpod 3.x patterns, Flame integration | ✅ |
| **54** | `build-configuration-deployment.md` | Build flavors, CI/CD, Firebase/Cloud Run | ✅ |

### Flame Engine (55-59)

| # | Document | Purpose | Status |
|---|----------|---------|--------|
| **55** | `flame-engine-fundamentals.md` | FlameGame lifecycle, component system, game loop | ✅ |
| **56** | `card-physics-animations.md` | I/O FLIP drag physics, momentum, drop zones | ✅ |
| **57** | `component-architecture.md` | Component hierarchy, lifecycle, communication | ✅ |
| **58** | `camera-viewport-systems.md` | Camera control, coordinate transformation | ✅ |
| **59** | `performance-optimization-flame.md` | Sprite atlases, pooling, 60 FPS optimization | ✅ |

### Package Integrations (60-66)

| # | Document | Purpose | Status |
|---|----------|---------|--------|
| **60** | `package-integration-overview.md` | All packages, versions, compatibility matrix | ✅ |
| **61** | `riverpod-integration.md` | Riverpod 3.x setup, code generation | ✅ |
| **62** | `flame-integration.md` | Flame package setup, GameWidget | ✅ |
| **63** | `audio-haptics-integration.md` | audioplayers + vibration services | ✅ |
| **64** | `storage-persistence-integration.md` | Hive local storage, type adapters | ✅ |
| **65** | `networking-integration.md` | Dio HTTP client, API setup | ✅ |
| **66** | `ai-ml-integration.md` | TensorFlow Lite on-device AI | ✅ |

### Testing & Quality (67-69)

| # | Document | Purpose | Status |
|---|----------|---------|--------|
| **67** | `testing-strategy.md` | Unit, widget, integration tests | ✅ |
| **68** | `performance-monitoring.md` | DevTools, FPS monitoring, battery tracking | ✅ |
| **69** | `code-quality-standards.md` | Linter rules, documentation, git standards | ✅ |

### Implementation Bridge (70)

| # | Document | Purpose | Status |
|---|----------|---------|--------|
| **70** | `implementation-reference.md` | Bridge to app/docs/ implementation details | ✅ |

---

## Implementation Reference

For detailed implementation documentation, see:
- **[70-implementation-reference.md](./70-implementation-reference.md)** - Bridge to app implementation docs
- **`app/docs/packages/`** - Comprehensive package reference with examples
- **`app/docs/SETUP.md`** - Flutter app quick setup guide
- **`app/docs/ARCHITECTURE.md`** - Deep dive into I/O FLIP architecture
- **`app/docs/CARD_DRAG_INTERACTION_FEATURE.md`** - Card system implementation details

**Documentation Philosophy:**
- **Architecture Docs** (this folder) - Planning, patterns, and high-level design
- **Implementation Docs** (`app/docs/`) - Code examples, package usage, and setup

---

## Reading Paths by Role

### For Flutter Developers (New to Flame)

```
50 (Architecture Overview)
  ↓
51 (Project Structure)
  ↓
52 (Environment Setup)
  ↓
55 (Flame Fundamentals)
  ↓
56 (Card Physics)
  ↓
53 (Riverpod State Management)
  ↓
60-66 (Package Integrations as needed)
```

### For Flame Developers (New to Project)

```
55 (Flame Fundamentals)
  ↓
56 (Card Physics - I/O FLIP patterns)
  ↓
57 (Component Architecture)
  ↓
59 (Performance Optimization)
  ↓
50 (Architecture Overview)
  ↓
51 (Project Structure)
```

### For Backend Developers (Dart Frog)

```
50 (Architecture Overview - Backend section)
  ↓
54 (Build & Deployment - Cloud Run)
  ↓
65 (Networking - API client)
  ↓
51 (Project Structure - Shared packages)
```

### For QA/Testing

```
67 (Testing Strategy)
  ↓
68 (Performance Monitoring)
  ↓
69 (Code Quality Standards)
  ↓
50 (Architecture Overview)
```

---

## Key Decisions

### ADR-001: Flame from Day 1

**Decision:** Use Flame game engine from project start  
**Rationale:** Code structure fundamentally different, migration cost 2-3 weeks  
**See:** `50-architecture-overview.md` ADR-001

### ADR-002: Riverpod 3.x Manual Integration

**Decision:** Use Riverpod 3.x, manually integrate with Flame  
**Rationale:** Latest features, flame_riverpod incompatible  
**See:** `50-architecture-overview.md` ADR-002

### ADR-003: Backend-Authoritative Model

**Decision:** Server validates all critical operations  
**Rationale:** Training data collection, prevent cheating  
**See:** `50-architecture-overview.md` ADR-003

### ADR-004: Dart Frog Backend

**Decision:** Use Dart Frog instead of Node.js frameworks  
**Rationale:** Full-stack Dart, shared packages, type safety  
**See:** `50-architecture-overview.md` ADR-004

---

## Performance Targets

| Metric | Target | Doc |
|--------|--------|-----|
| **Frame Rate** | 60 FPS stable | 59, 68 |
| **Frame Time** | < 16ms | 59, 68 |
| **Memory Usage** | < 200MB | 59 |
| **App Size** | < 50MB | 54 |
| **Battery Drain** | < 10% per 30min | 59, 68 |

---

## Technology Stack

### Frontend

| Technology | Version | Doc |
|------------|---------|-----|
| Flutter | 3.27+ | 52 |
| Flame | 1.20+ | 55, 62 |
| Riverpod | 3.0+ | 53, 61 |
| Hive | 2.2+ | 64 |
| audioplayers | 6.1+ | 63 |
| vibration | 2.0+ | 63 |

### Backend

| Technology | Version | Doc |
|------------|---------|-----|
| Dart Frog | Latest | 50, 54 |
| Firebase Firestore | Latest | 50, 54 |
| Firebase Auth | Latest | 50, 54 |
| Cloud Run | Latest | 54 |

### Future (Phase 5+)

| Technology | Version | Doc |
|------------|---------|-----|
| TensorFlow Lite | 2.x | 66 |
| Custom Shaders | GLSL | 62 |

---

## Related Documentation

### Within This Project

- **`docs/master_truths_canonical_spec_v_1_2.md`** - Canonical rules
- **`docs/1.concept/`** - Design philosophy
- **`docs/2.gameplay/`** - Implementation specs
- **`docs/3.ai/`** - AI architecture
- **`docs/CANONICAL-DECISIONS-LOG.md`** - All decisions

### External References

- **I/O FLIP GitHub:** https://github.com/flutter/io_flip
- **I/O FLIP Blog:** https://flutter.dev/flip
- **Flame Docs:** https://docs.flame-engine.org/
- **Riverpod Docs:** https://riverpod.dev/
- **Firebase Docs:** https://firebase.google.com/docs
- **Dart Frog Docs:** https://dartfrog.vgv.dev/

---

## Document Status Tracking

### Completion Status

- ✅ **Core Architecture (50-54):** 5/5 complete
- ✅ **Flame Engine (55-59):** 5/5 complete
- ✅ **Package Integrations (60-66):** 7/7 complete
- ✅ **Testing & Quality (67-69):** 3/3 complete
- ✅ **Index (00):** 1/1 complete

**Total:** 21/21 documents complete (100%)

### Last Updated

All documents updated: **October 14, 2025**

### Compliance

All documents compliant with **Master Truths v1.2**

---

## Migration Notes

### From Old Documentation

All previous unnumbered documentation archived to:
- `docs/_archive/2025-10-14-architecture/`

See `ARCHIVE_README.md` in archive folder for migration map.

### Key Changes

1. ✅ Numbered documentation (50-69 series)
2. ✅ Consistent structure across all docs
3. ✅ Clear reading paths by role
4. ✅ Latest package versions (Flutter 3.27+, Flame 1.20+)
5. ✅ Comprehensive cross-references
6. ✅ I/O FLIP patterns documented

---

## Frequently Asked Questions

### Why Flame from day 1?

**Answer:** Code structure fundamentally different. Migration would cost 2-3 weeks. See `50-architecture-overview.md` ADR-001.

### Can I use flame_riverpod?

**Answer:** No, flame_riverpod requires Riverpod 2.x. We use Riverpod 3.x with manual integration. See `53-state-management-architecture.md`.

### How do I add a new package?

**Answer:** Add to `pubspec.yaml`, document in appropriate 60-66 doc, update `60-package-integration-overview.md`.

### Where are the old docs?

**Answer:** Archived in `docs/_archive/2025-10-14-architecture/` with migration map.

---

## Contributing to Documentation

### When to Update These Docs

Update documentation when:
- Architecture patterns change
- New packages added
- Breaking changes introduced
- Performance targets updated
- I/O FLIP patterns evolve

### How to Update

1. Update the specific numbered doc (50-69)
2. Update "Last Updated" date
3. Update this index if new doc added
4. Update cross-references
5. Update `CANONICAL-DECISIONS-LOG.md` if decision changed

### Documentation Standards

Each document must have:
- ✅ Header (title, date, compliance, status)
- ✅ Overview section
- ✅ Code examples (complete, runnable)
- ✅ Related documentation links
- ✅ Quick reference section
- ✅ Status indicator

---

## Getting Help

### For Architecture Questions

1. Check this index for relevant doc
2. Read the specific numbered doc
3. Check related docs in cross-references
4. Review I/O FLIP GitHub for patterns
5. Ask in #architecture channel

### For Implementation Questions

1. Check implementation doc (51-66)
2. Review code examples in docs
3. Check I/O FLIP for reference implementation
4. Review Master Truths v1.2 for rules
5. Ask in #development channel

---

## Success Criteria

This documentation is successful when:

- ✅ New developers onboard in < 1 day
- ✅ All architecture decisions documented
- ✅ Clear path from concept to implementation
- ✅ I/O FLIP patterns properly adopted
- ✅ Performance targets clearly defined
- ✅ Testing strategy comprehensive
- ✅ Package integrations complete
- ✅ 100% document completion

**Current Status:** ✅ All criteria met

---

## Maintenance Schedule

### Weekly
- Review for outdated content
- Update package versions if changed
- Check external links

### Monthly
- Verify I/O FLIP patterns still current
- Update performance benchmarks
- Review and consolidate feedback

### Quarterly
- Major documentation review
- Architecture pattern updates
- Technology stack evaluation

---

**Status:** ✅ Architecture Documentation Complete  
**Total Documents:** 21 (50-69 + 00-INDEX)  
**Completion:** 100%  
**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2

---

## Quick Command Reference

```bash
# Setup
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs

# Run
flutter run --flavor development -t lib/main_development.dart

# Test
flutter test
flutter analyze
dart format .

# Build
flutter build apk --flavor production -t lib/main_production.dart --release

# Deploy
firebase deploy --only hosting:production
./scripts/deploy_backend.sh production
```

---

**Welcome to Unwritten Architecture Documentation!**  
Start with `50-architecture-overview.md` and follow your role's reading path.

