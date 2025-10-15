# Unwritten Project Structure Guide

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete

---

## Overview

Unwritten follows **Clean Architecture** with **Feature-First Organization**, combining Flutter widgets and Flame game components in a scalable, maintainable structure.

**Pattern Source:** I/O FLIP + Very Good Ventures best practices

---

## Complete Directory Structure

```
unwritten/
├── app/                                  # Flutter application
│   ├── lib/
│   │   ├── main.dart                    # App entry point
│   │   │
│   │   ├── core/                        # Shared across all features
│   │   │   ├── constants/
│   │   │   │   └── game_constants.dart # From Master Truths v1.2
│   │   │   ├── config/
│   │   │   │   ├── environment.dart    # Dev/staging/prod
│   │   │   │   └── firebase_options.dart
│   │   │   ├── errors/
│   │   │   │   ├── exceptions.dart
│   │   │   │   └── failures.dart
│   │   │   ├── utils/
│   │   │   │   ├── app_logger.dart     # Structured logging
│   │   │   │   └── extensions.dart
│   │   │   └── performance/
│   │   │       ├── frame_monitor.dart
│   │   │       └── memory_monitor.dart
│   │   │
│   │   ├── features/                    # Feature modules
│   │   │   │
│   │   │   ├── cards/                   # Card system
│   │   │   │   ├── data/
│   │   │   │   │   ├── models/
│   │   │   │   │   │   ├── card_model.dart
│   │   │   │   │   │   └── card_type.dart
│   │   │   │   │   ├── repositories/
│   │   │   │   │   │   ├── card_repository.dart      # Interface
│   │   │   │   │   │   └── card_repository_impl.dart # Implementation
│   │   │   │   │   └── datasources/
│   │   │   │   │       ├── card_local_datasource.dart
│   │   │   │   │       └── card_remote_datasource.dart
│   │   │   │   ├── domain/
│   │   │   │   │   ├── entities/
│   │   │   │   │   │   └── card.dart              # Business entity
│   │   │   │   │   ├── repositories/
│   │   │   │   │   │   └── card_repository.dart # Interface
│   │   │   │   │   └── usecases/
│   │   │   │   │       ├── get_cards_usecase.dart
│   │   │   │   │       └── play_card_usecase.dart
│   │   │   │   └── presentation/
│   │   │   │       ├── components/           # Flame components
│   │   │   │       │   ├── card_game_component.dart
│   │   │   │       │   └── drop_zone_component.dart
│   │   │   │       ├── widgets/              # Flutter widgets
│   │   │   │       │   ├── card_widget.dart
│   │   │   │       │   └── card_hand_widget.dart
│   │   │   │       └── providers/
│   │   │   │           └── card_providers.dart # Riverpod
│   │   │   │
│   │   │   ├── game/                    # Game loop and state
│   │   │   │   ├── data/
│   │   │   │   │   ├── models/
│   │   │   │   │   │   ├── game_state_model.dart
│   │   │   │   │   │   ├── resources_model.dart
│   │   │   │   │   │   └── turn_phase.dart
│   │   │   │   │   └── repositories/
│   │   │   │   │       └── game_repository_impl.dart
│   │   │   │   ├── domain/
│   │   │   │   │   ├── entities/
│   │   │   │   │   ├── repositories/
│   │   │   │   │   └── usecases/
│   │   │   │   └── presentation/
│   │   │   │       ├── components/           # Flame components
│   │   │   │       │   ├── unwritten_game_world.dart  # Main game
│   │   │   │       │   ├── card_animation_effects.dart
│   │   │   │       │   └── ui_overlay_component.dart
│   │   │   │       ├── screens/
│   │   │   │       │   └── game_screen.dart
│   │   │   │       └── providers/
│   │   │   │           └── game_state_providers.dart
│   │   │   │
│   │   │   ├── ai/                      # AI/ML features
│   │   │   │   ├── data/
│   │   │   │   │   ├── models/
│   │   │   │   │   │   ├── personality_profile.dart
│   │   │   │   │   │   └── ai_response.dart
│   │   │   │   │   ├── datasources/
│   │   │   │   │   │   ├── ai_remote_datasource.dart   # Cloud AI
│   │   │   │   │   │   └── ai_local_datasource.dart    # TFLite
│   │   │   │   │   └── repositories/
│   │   │   │   │       └── ai_repository_impl.dart
│   │   │   │   ├── domain/
│   │   │   │   │   ├── entities/
│   │   │   │   │   ├── repositories/
│   │   │   │   │   └── usecases/
│   │   │   │   │       ├── generate_dialogue_usecase.dart
│   │   │   │   │       └── analyze_personality_usecase.dart
│   │   │   │   └── presentation/
│   │   │   │       └── providers/
│   │   │   │           └── ai_providers.dart
│   │   │   │
│   │   │   └── relationships/           # NPC relationships
│   │   │       ├── data/
│   │   │       │   ├── models/
│   │   │       │   │   └── relationship_model.dart
│   │   │       │   └── repositories/
│   │   │       ├── domain/
│   │   │       │   ├── entities/
│   │   │       │   ├── repositories/
│   │   │       │   └── usecases/
│   │   │       └── presentation/
│   │   │           ├── widgets/
│   │   │           └── providers/
│   │   │
│   │   └── shared/                      # Shared across features
│   │       ├── services/
│   │       │   ├── audio_service.dart
│   │       │   ├── haptic_service.dart
│   │       │   ├── storage_service.dart
│   │       │   └── analytics_service.dart
│   │       ├── widgets/
│   │       │   ├── resources_bar.dart
│   │       │   ├── turn_indicator.dart
│   │       │   └── custom_button.dart
│   │       └── extensions/
│   │           ├── context_extensions.dart
│   │           └── datetime_extensions.dart
│   │
│   ├── assets/
│   │   ├── audio/
│   │   │   ├── music/
│   │   │   │   └── game_theme.mp3
│   │   │   └── sfx/
│   │   │       ├── card_hover.mp3
│   │   │       ├── card_play.mp3
│   │   │       └── card_draw.mp3
│   │   ├── images/
│   │   │   ├── cards/
│   │   │   ├── backgrounds/
│   │   │   ├── effects/
│   │   │   └── ui/
│   │   ├── models/              # TensorFlow Lite models
│   │   │   ├── personality.tflite
│   │   │   └── sentiment.tflite
│   │   ├── data/
│   │   │   └── cards.json
│   │   └── shaders/
│   │       └── holographic.frag
│   │
│   ├── test/
│   │   ├── core/
│   │   ├── features/
│   │   │   ├── cards/
│   │   │   │   ├── data/
│   │   │   │   ├── domain/
│   │   │   │   └── presentation/
│   │   │   └── game/
│   │   ├── helpers/
│   │   │   └── test_helpers.dart
│   │   └── integration/
│   │       └── game_flow_test.dart
│   │
│   ├── pubspec.yaml
│   ├── analysis_options.yaml
│   └── README.md
│
├── backend/                             # Dart Frog backend
│   ├── routes/
│   │   ├── index.dart
│   │   ├── game/
│   │   │   ├── play_card.dart
│   │   │   ├── advance_turn.dart
│   │   │   └── get_state.dart
│   │   └── ai/
│   │       └── generate_dialogue.dart
│   ├── services/
│   │   ├── ai_service.dart
│   │   ├── firestore_service.dart
│   │   └── training_data_service.dart
│   ├── middleware/
│   │   ├── auth_middleware.dart
│   │   └── logging_middleware.dart
│   ├── main.dart
│   ├── pubspec.yaml
│   └── Dockerfile
│
├── packages/                            # Shared packages
│   ├── game_logic/
│   │   ├── lib/
│   │   │   ├── game_logic.dart
│   │   │   └── src/
│   │   │       ├── calculators/
│   │   │       │   ├── relationship_calculator.dart
│   │   │       │   └── success_probability.dart
│   │   │       ├── models/
│   │   │       │   ├── card.dart
│   │   │       │   ├── game_state.dart
│   │   │       │   └── relationship.dart
│   │   │       └── validators/
│   │   │           └── card_play_validator.dart
│   │   ├── test/
│   │   └── pubspec.yaml
│   │
│   └── data_models/
│       ├── lib/
│       │   ├── data_models.dart
│       │   └── src/
│       │       ├── card_model.dart
│       │       ├── game_state_model.dart
│       │       └── relationship_model.dart
│       ├── test/
│       └── pubspec.yaml
│
├── docs/                                # Documentation
│   ├── master_truths_canonical_spec_v_1_2.md
│   ├── 1.concept/
│   ├── 2.gameplay/
│   ├── 3.ai/
│   ├── 5.architecture/                  # This folder
│   └── _archive/
│
└── scripts/                             # Utility scripts
    ├── setup_environment.sh
    └── deploy.sh
```

---

## File Naming Conventions

### Dart Files

**Format:** `lowercase_with_underscores.dart` (snake_case)

```dart
// ✅ CORRECT
card_model.dart
game_state_providers.dart
relationship_calculator.dart

// ❌ WRONG
CardModel.dart
gameStateProviders.dart
RelationshipCalculator.dart
```

### Test Files

**Format:** `[filename]_test.dart`

```dart
// ✅ CORRECT
card_model_test.dart
game_state_providers_test.dart

// ❌ WRONG
test_card_model.dart
card_model.test.dart
```

### Component Files (Flame)

**Suffix:** `_component.dart`

```dart
// ✅ CORRECT - Flame components
card_game_component.dart
drop_zone_component.dart
ui_overlay_component.dart

// ✅ CORRECT - Flutter widgets
card_widget.dart
card_hand_widget.dart
```

### Service Files

**Suffix:** `_service.dart`

```dart
// ✅ CORRECT
audio_service.dart
ai_service.dart
storage_service.dart
```

---

## Clean Architecture Layers

### Layer 1: Data (Outermost)

**Responsibility:** External interfaces (APIs, databases, files)

**Contains:**
- Models (data representation)
- Repositories (implementation)
- Data sources (remote, local)

**Example:**
```dart
// data/models/card_model.dart
class CardModel {
  final String id;
  final String title;
  // ...
  
  factory CardModel.fromJson(Map<String, dynamic> json) => // ...
  Map<String, dynamic> toJson() => // ...
}

// data/datasources/card_remote_datasource.dart
class CardRemoteDataSource {
  Future<List<CardModel>> fetchCards() async {
    // Call backend API
  }
}

// data/repositories/card_repository_impl.dart
class CardRepositoryImpl implements CardRepository {
  final CardRemoteDataSource remoteDataSource;
  final CardLocalDataSource localDataSource;
  
  @override
  Future<Either<Failure, List<Card>>> getCards() async {
    // Try remote, fallback to local
  }
}
```

### Layer 2: Domain (Core Business Logic)

**Responsibility:** Business rules (pure Dart, no Flutter)

**Contains:**
- Entities (business objects)
- Repository interfaces
- Use cases (business operations)

**Example:**
```dart
// domain/entities/card.dart
class Card {
  final String id;
  final String title;
  // Pure business object (no fromJson/toJson)
}

// domain/repositories/card_repository.dart
abstract class CardRepository {
  Future<Either<Failure, List<Card>>> getCards();
  Future<Either<Failure, void>> playCard(String cardId);
}

// domain/usecases/play_card_usecase.dart
class PlayCardUseCase {
  final CardRepository repository;
  
  Future<Either<Failure, void>> call(String cardId) async {
    // Business logic: validate, check resources, etc.
    return repository.playCard(cardId);
  }
}
```

### Layer 3: Presentation (UI & State)

**Responsibility:** UI rendering and state management

**Contains:**
- Components (Flame)
- Widgets (Flutter)
- Providers (Riverpod)
- Screens

**Example:**
```dart
// presentation/components/card_game_component.dart (Flame)
class CardGameComponent extends PositionComponent with DragCallbacks {
  @override
  void update(double dt) {
    // Flame game loop
  }
  
  @override
  void render(Canvas canvas) {
    // Flame rendering
  }
}

// presentation/widgets/card_widget.dart (Flutter)
class CardWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(/* Flutter UI */);
  }
}

// presentation/providers/card_providers.dart (Riverpod)
@riverpod
class CardNotifier extends _$CardNotifier {
  @override
  List<Card> build() => [];
  
  Future<void> loadCards() async {
    // Load from use case
  }
}
```

---

## Feature-First Organization

### Why Feature-First?

**Problem with Layer-First:**
```
lib/
├── models/         # All models together (hard to find)
├── repositories/   # All repos together
├── usecases/       # All usecases together
└── widgets/        # All widgets together
```

**Solution with Feature-First:**
```
lib/features/
├── cards/          # Everything about cards
│   ├── data/
│   ├── domain/
│   └── presentation/
└── game/           # Everything about game
    ├── data/
    ├── domain/
    └── presentation/
```

**Benefits:**
- ✅ Easy to find related code
- ✅ Features are independent
- ✅ Can work on features in parallel
- ✅ Can delete entire features
- ✅ Clear ownership

### When to Create a New Feature

**Create feature when:**
- ✅ Has its own data models
- ✅ Has its own business logic
- ✅ Has its own UI
- ✅ Relatively independent

**Examples:**
- `cards/` - Card system
- `game/` - Game loop
- `ai/` - AI/ML
- `relationships/` - NPC relationships

**Don't create feature for:**
- ❌ Single widget (put in shared/)
- ❌ Utility function (put in core/)
- ❌ Shared service (put in shared/)

---

## Flame Component Structure

### Game World Structure

```dart
// game/presentation/components/unwritten_game_world.dart
class UnwrittenGameWorld extends FlameGame {
  late final CameraComponent camera;
  late final World world;
  
  @override
  Future<void> onLoad() async {
    // Setup camera
    camera = CameraComponent.withFixedResolution(
      width: 1920,
      height: 1080,
    );
    
    // Setup world
    world = World();
    
    // Add components
    world.add(CardGameComponent(...));
    world.add(DropZoneComponent(...));
  }
}
```

### Component Hierarchy

```
UnwrittenGameWorld (FlameGame)
  └── World
      ├── CameraComponent
      ├── CardGameComponent × N
      │   ├── SpriteComponent (card art)
      │   ├── TextComponent (card title)
      │   └── Effects
      ├── DropZoneComponent × N
      │   └── RectangleComponent (highlight)
      └── UIOverlayComponent
```

**See:** `55-flame-engine-fundamentals.md` for Flame basics

---

## Package Structure (Shared Logic)

### game_logic Package

**Purpose:** Business logic shared between client and server

**Structure:**
```
packages/game_logic/
├── lib/
│   ├── game_logic.dart          # Public API
│   └── src/
│       ├── calculators/         # Formulas from Master Truths
│       │   ├── relationship_calculator.dart
│       │   └── success_probability.dart
│       ├── models/              # Core models
│       │   ├── card.dart
│       │   └── game_state.dart
│       └── validators/          # Business rules
│           └── card_play_validator.dart
├── test/
│   └── calculators/
│       └── relationship_calculator_test.dart
└── pubspec.yaml
```

**Usage:**
```dart
// In Flutter app
import 'package:game_logic/game_logic.dart';

// In Dart Frog backend
import 'package:game_logic/game_logic.dart';

// Same code, same behavior
```

**See:** `50-architecture-overview.md` for shared package rationale

---

## File Organization Best Practices

### 1. Maximum File Size

**Rule:** Max 300 lines per file

**Why:**
- Easier to navigate
- Forces good separation
- Faster reviews

**How to split:**
```dart
// Too large (500 lines)
game_state_providers.dart

// Split into:
game_state_provider.dart       // Main state (150 lines)
game_actions_provider.dart     // Actions (100 lines)
game_selectors_provider.dart   // Selectors (100 lines)
```

### 2. Barrel Exports

**Pattern:** Each feature has `[feature].dart` that exports all public APIs

```dart
// features/cards/cards.dart
export 'data/models/card_model.dart';
export 'data/models/card_type.dart';
export 'domain/entities/card.dart';
export 'domain/repositories/card_repository.dart';
export 'presentation/widgets/card_widget.dart';
export 'presentation/providers/card_providers.dart';

// Don't export private implementation
// export 'data/repositories/card_repository_impl.dart'; // ❌
```

**Usage:**
```dart
// ✅ Clean
import 'package:unwritten/features/cards/cards.dart';

// ❌ Messy
import 'package:unwritten/features/cards/data/models/card_model.dart';
import 'package:unwritten/features/cards/domain/entities/card.dart';
import 'package:unwritten/features/cards/presentation/widgets/card_widget.dart';
```

### 3. One Class Per File

**Rule:** One public class per file (except small helpers)

```dart
// ✅ CORRECT
// card_model.dart
class CardModel { }

// card_type.dart
enum CardType { }

// ❌ WRONG
// card.dart
class CardModel { }
enum CardType { }
class CardStats { }
```

---

## Related Documentation

- **50-architecture-overview.md** - Architecture decisions
- **52-development-environment-setup.md** - Setup guide
- **53-state-management-architecture.md** - Riverpod patterns
- **55-flame-engine-fundamentals.md** - Flame structure
- **60-package-integration-overview.md** - Package organization

---

## Quick Reference

### Where Do I Put...?

| Type | Location | Example |
|------|----------|---------|
| **Game constant** | `core/constants/` | `game_constants.dart` |
| **Utility function** | `core/utils/` | `date_formatter.dart` |
| **Shared widget** | `shared/widgets/` | `custom_button.dart` |
| **Shared service** | `shared/services/` | `audio_service.dart` |
| **Feature model** | `features/[feature]/data/models/` | `card_model.dart` |
| **Feature entity** | `features/[feature]/domain/entities/` | `card.dart` |
| **Flame component** | `features/[feature]/presentation/components/` | `card_game_component.dart` |
| **Flutter widget** | `features/[feature]/presentation/widgets/` | `card_widget.dart` |
| **Riverpod provider** | `features/[feature]/presentation/providers/` | `card_providers.dart` |
| **Test file** | `test/[mirror structure]/` | `card_model_test.dart` |

---

**Status:** ✅ Structure Complete  
**Next:** Follow this structure for all new code  
**Compliance:** Clean Architecture + Feature-First

