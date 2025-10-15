# Architecture Documentation

> **Canonical Reference**: Master Truths v1.2  
> **Purpose**: Index of all architecture and implementation documentation  
> **Last Updated**: October 14, 2025

---

## Quick Navigation

### 🚀 Getting Started
- **New Developer?** → Start with [Quick Start Developer Guide](QUICK-START-DEVELOPER-GUIDE.md)
- **Setting Up?** → Follow [Flutter Project Setup](FLUTTER-PROJECT-SETUP.md)
- **Understanding Vision?** → Read [Implementation Plan MVP](IMPLEMENTATION-PLAN-MVP.md)

### 📋 Current Phase: Foundation (Phase 1)
**Goal**: Set up Flutter project with Clean Architecture, basic UI, and card data models

**Priority Tasks**:
1. Project structure setup
2. Core data models (Card, GameState, Relationship)
3. Base card JSON with 50 starter cards
4. Basic UI framework

**Status**: In Progress  
**Timeline**: Weeks 1-4

---

## Document Index

### Implementation Guides

#### [IMPLEMENTATION-PLAN-MVP.md](IMPLEMENTATION-PLAN-MVP.md)
**Master implementation roadmap from foundation to beta**

- **Purpose**: Complete phase-by-phase plan focused on playable MVP
- **Scope**: 5 phases over 20 weeks
- **Focus**: Cloud-based AI, training data collection
- **When to Read**: Before starting any implementation work

**Key Sections**:
- Phase 1: Foundation (Weeks 1-4)
- Phase 2: Core Game Loop (Weeks 5-8)
- Phase 3: Cloud AI Integration (Weeks 9-12)
- Phase 4: Season Structure (Weeks 13-16)
- Phase 5: Polish & Beta Prep (Weeks 17-20)

**Status**: ✅ Complete, approved for implementation

---

#### [FLUTTER-PROJECT-SETUP.md](FLUTTER-PROJECT-SETUP.md)
**Step-by-step Flutter project initialization**

- **Purpose**: Technical setup guide with all commands and configurations
- **Scope**: Environment setup through first run
- **When to Read**: When setting up local dev environment

**Key Sections**:
- Prerequisites & environment setup
- Project structure creation
- Dependency configuration
- Code generation setup
- Verification steps

**Status**: ✅ Ready for use

---

#### [QUICK-START-DEVELOPER-GUIDE.md](QUICK-START-DEVELOPER-GUIDE.md)
**Fast onboarding for new developers**

- **Purpose**: Get contributing in < 30 minutes
- **Scope**: High-level overview + common tasks
- **When to Read**: First day on project

**Key Sections**:
- 5-minute architecture overview
- 10-minute project setup
- Essential reading list
- Common tasks & patterns
- Debugging tips

**Status**: ✅ Ready for use

---

## Architecture Principles

### Clean Architecture

Unwritten follows Clean Architecture with three layers:

```
┌─────────────────────────────────────┐
│        Presentation Layer           │
│  (UI, Widgets, Controllers)         │
│  - ConsumerWidget / StateNotifier   │
│  - Riverpod providers               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Domain Layer                │
│  (Business Logic, Use Cases)        │
│  - Entities                         │
│  - Use Cases                        │
│  - Repository Interfaces            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│          Data Layer                 │
│  (Models, Repositories, APIs)       │
│  - Models with JSON serialization   │
│  - Repository implementations       │
│  - Data sources (Hive, HTTP)        │
└─────────────────────────────────────┘
```

**Rules**:
- Presentation depends on Domain
- Domain depends on nothing (pure Dart)
- Data implements Domain interfaces
- Dependencies point inward

### State Management: Riverpod

**Pattern**: Provider + StateNotifier

```dart
// 1. Define state
class GameState {
  final int week;
  final ResourcesModel resources;
  // ...
}

// 2. Create controller
class GameController extends StateNotifier<GameState> {
  GameController() : super(GameState.initial());
  
  void advanceWeek() {
    state = state.copyWith(week: state.week + 1);
  }
}

// 3. Provide to UI
final gameStateProvider = StateNotifierProvider<GameController, GameState>((ref) {
  return GameController();
});

// 4. Consume in widget
class GameScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final gameState = ref.watch(gameStateProvider);
    return Text('Week ${gameState.week}');
  }
}
```

### File Organization

```
lib/
├── core/                          # Cross-cutting concerns
│   ├── constants/
│   │   └── game_constants.dart   # Canonical constants
│   ├── errors/
│   │   └── exceptions.dart       # Custom exceptions
│   └── utils/
│       └── app_logger.dart       # Structured logging
│
├── features/                      # Feature modules
│   ├── cards/
│   │   ├── data/
│   │   │   ├── models/           # JSON serializable models
│   │   │   └── repositories/     # Data access implementations
│   │   ├── domain/
│   │   │   ├── entities/         # Pure Dart entities
│   │   │   └── usecases/         # Business logic
│   │   └── presentation/
│   │       ├── controllers/      # StateNotifiers
│   │       ├── screens/          # Full screens
│   │       └── widgets/          # Reusable components
│   │
│   ├── game/                      # Game state, turns, seasons
│   │   └── [same structure]
│   │
│   └── relationships/             # NPC relationships
│       └── [same structure]
│
└── shared/                        # Shared across features
    ├── services/
    │   ├── ai_service.dart       # Cloud AI integration
    │   └── training_data_logger.dart
    └── widgets/
        └── common_widgets.dart
```

**Naming Conventions**:
- Files: `snake_case.dart`
- Classes: `PascalCase`
- Variables/functions: `camelCase`
- Constants: `camelCase` (not SCREAMING_SNAKE_CASE)

---

## Technology Stack

### Core Framework
| Component | Version | Purpose |
|-----------|---------|---------|
| Flutter | 3.24.0+ | Cross-platform UI framework |
| Dart | 3.5.0+ | Programming language |

### State Management
| Component | Version | Purpose |
|-----------|---------|---------|
| flutter_riverpod | 2.5.1+ | Provider-based state management |
| riverpod_annotation | 2.3.5+ | Code generation for providers |

### Data & Storage
| Component | Version | Purpose |
|-----------|---------|---------|
| hive | 2.2.3+ | Local key-value storage |
| hive_flutter | 1.1.0+ | Flutter bindings for Hive |
| path_provider | 2.1.3+ | Platform-specific directories |

### Networking
| Component | Version | Purpose |
|-----------|---------|---------|
| http | 1.2.1+ | HTTP client |
| dio | 5.4.3+ | Advanced HTTP client with interceptors |

### Utilities
| Component | Version | Purpose |
|-----------|---------|---------|
| uuid | 4.4.0+ | Unique ID generation |
| intl | 0.19.0+ | Internationalization |
| equatable | 2.0.5+ | Value equality |

### Code Generation
| Component | Version | Purpose |
|-----------|---------|---------|
| build_runner | 2.4.9+ | Code generation tool |
| freezed | 2.5.2+ | Immutable models |
| json_serializable | 6.8.0+ | JSON serialization |
| hive_generator | 2.0.1+ | Hive type adapters |

### UI
| Component | Version | Purpose |
|-----------|---------|---------|
| flutter_animate | 4.5.0+ | Declarative animations |
| google_fonts | 6.2.1+ | Typography |

---

## Development Workflow

### Daily Development

```bash
# 1. Pull latest changes
git pull origin main

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Run code generation (if needed)
flutter pub run build_runner watch

# 4. Develop with hot reload
flutter run
# Press 'r' for hot reload
# Press 'R' for hot restart

# 5. Run tests frequently
flutter test

# 6. Format and analyze before commit
dart format .
flutter analyze

# 7. Commit with conventional message
git commit -m "feat(cards): add card evolution system"

# 8. Push and create PR
git push origin feature/your-feature-name
```

### Code Review Process

**Before Submitting PR**:
- [ ] Code follows architecture guidelines
- [ ] Public APIs documented with `///` comments
- [ ] Uses `AppLogger` not `print()`
- [ ] References `GameConstants` not magic numbers
- [ ] Unit tests written and passing
- [ ] `flutter analyze` shows no errors
- [ ] `dart format .` applied
- [ ] PR description references Master Truths v1.2 sections

**PR Title Format**:
```
<type>(<scope>): <description>

Examples:
feat(cards): implement card evolution system
fix(game): resolve turn advance state bug
refactor(relationships): extract level calculator
docs(architecture): update implementation plan
test(cards): add card fusion tests
```

**PR Description Template**:
```markdown
## Changes
- Implemented X
- Fixed Y
- Updated Z

## Master Truths v1.2 Compliance
- Section 2: Relationship levels (0-5) ✅
- Section 11: NPC Response Framework ✅

## Testing
- Unit tests: 15 passing
- Widget tests: 3 passing
- Manual testing: Verified on Android emulator

## Screenshots
(if UI changes)
```

---

## Performance Targets

### MVP Targets (Phase 1-5)
| Metric | Target | Notes |
|--------|--------|-------|
| App Launch | < 3s | Cold start to playable |
| Turn Load | < 1s | Advance turn to new state |
| Card Play | < 2s | Play card to narrative display |
| AI Latency | < 3s | Cloud API round-trip |
| Memory Usage | < 200 MB | Average gameplay session |
| Battery Drain | < 5% | Per 30-minute session |
| Crash Rate | < 1% | Sessions with crash |

### Measurement

```dart
// Performance logging built-in
final stopwatch = Stopwatch()..start();
await operation();
stopwatch.stop();

AppLogger.performance('Operation name', stopwatch.elapsed);
// Only logs if > 16ms (one frame at 60fps)
```

---

## Testing Strategy

### Test Pyramid

```
       ╱╲        E2E Tests
      ╱  ╲       (Few, expensive)
     ╱────╲      
    ╱      ╲     Integration Tests
   ╱────────╲    (Some, moderate cost)
  ╱          ╲   
 ╱────────────╲  Unit Tests
╱──────────────╲ (Many, cheap)
```

### Test Coverage Goals
- **Unit Tests**: > 80% coverage
- **Widget Tests**: All reusable widgets
- **Integration Tests**: Critical paths (card play, turn advance, level up)
- **E2E Tests**: Full season completion (deferred to Phase 5)

### Running Tests

```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/features/cards/card_model_test.dart

# Run with coverage
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html

# Run integration tests
flutter test integration_test/
```

---

## Migration Path: Local AI (Post-MVP)

**Current (Phase 3)**: Cloud-based AI via OpenAI/Anthropic API  
**Future (Phase 6+)**: Hybrid cloud + on-device TensorFlow Lite

**Deferred Because**:
- MVP needs flexibility to iterate prompts
- Training data quality more important than latency initially
- TensorFlow Lite adds significant complexity
- Battery optimization premature at this stage

**Migration Plan** (Phase 6):
1. Train local models from collected training data
2. Implement TensorFlow Lite integration
3. Add battery-aware switching (cloud when low battery)
4. A/B test quality and performance
5. Gradually shift to local-first

**Code Impact**: Abstracted behind `AIService` interface, so minimal changes to consumers.

---

## Related Documentation

### Concept Documents
- `docs/1.concept/` - Game vision, card system, AI personality
- `docs/2.gameplay/` - Detailed mechanics, turn structure, seasons

### Schema Documents
- `docs/7.schema/base-card-schema-v1.md` - Card JSON specification
- `docs/7.schema/` - Data contracts and validation

### Master Truth
- `docs/master_truths_canonical_spec_v_1_2.md` - **Single source of truth**

---

## Frequently Asked Questions

### "Where do I start?"
Read [QUICK-START-DEVELOPER-GUIDE.md](QUICK-START-DEVELOPER-GUIDE.md) (10 minutes), then set up your environment with [FLUTTER-PROJECT-SETUP.md](FLUTTER-PROJECT-SETUP.md) (20 minutes).

### "What should I work on?"
Check [IMPLEMENTATION-PLAN-MVP.md](IMPLEMENTATION-PLAN-MVP.md) for current phase deliverables. Pick an unassigned task from Phase 1.

### "How do I reference canonical values?"
Use `GameConstants` class. Example: `GameConstants.relationshipLevelMax` instead of hardcoding `5`.

### "When do I use print() vs AppLogger?"
**Never use print()** in production code. Always use `AppLogger.info()`, `AppLogger.error()`, etc. Logs are automatically gated by debug mode.

### "How do I know if I'm following Clean Architecture?"
- Presentation layer imports domain layer ✅
- Domain layer imports nothing external ✅
- Data layer implements domain interfaces ✅
- Dependencies point inward ✅

### "What's the difference between Model and Entity?"
- **Entity**: Pure Dart class in domain layer (no JSON, no framework dependencies)
- **Model**: Data class with JSON serialization in data layer (can depend on packages)

### "Why Riverpod instead of Bloc or Redux?"
- Flutter-native (no external concepts like Redux patterns)
- Less boilerplate than Bloc
- Excellent testing support
- Compile-time safety
- Aligns with Flutter team's direction

### "When should I write integration tests?"
For **critical paths**: card playing, turn advancing, relationship leveling up, season completion. Not for every feature.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-14 | Initial architecture documentation |
| | | - Implementation Plan MVP |
| | | - Flutter Project Setup |
| | | - Quick Start Guide |

---

## Compliance Checklist

- [x] References Master Truths v1.2
- [x] Clean Architecture documented
- [x] Riverpod pattern explained
- [x] File naming conventions specified
- [x] This doc cites **Truths v1.2**

---

**Document Version**: 1.0  
**Last Updated**: October 14, 2025  
**Maintainer**: Architecture Team  
**Status**: Living document (update as architecture evolves)

