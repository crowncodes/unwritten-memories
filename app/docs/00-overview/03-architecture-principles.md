# Architecture Principles

## Core Philosophy

**Performance First, Always.** Every architectural decision prioritizes 60 FPS, battery life, and premium user experience.

## Clean Architecture

Unwritten follows Clean Architecture with three layers:

### 1. Data Layer (`data/`)
- **Repository Implementations**
- **Data Sources** (local, remote, cache)
- **Data Models** (JSON serialization)

### 2. Domain Layer (`domain/`)
- **Entities** (business objects)
- **Use Cases** (business logic)
- **Repository Interfaces**

### 3. Presentation Layer (`presentation/`)
- **Screens** (Flutter widgets)
- **Widgets** (UI components)
- **Flame Components** (game visuals)
- **State Management** (Riverpod providers)

### Dependency Rule

Dependencies flow **inward**:
- Presentation → Domain → Data
- Never: Data → Domain → Presentation ❌

## Feature Organization

```
lib/features/cards/
├── data/
│   ├── models/
│   ├── repositories/
│   └── datasources/
├── domain/
│   ├── entities/
│   ├── usecases/
│   └── repositories/
└── presentation/
    ├── screens/
    ├── widgets/
    ├── components/  # Flame components
    └── providers/   # Riverpod state
```

Each feature is self-contained with minimal cross-feature dependencies.

## File Naming Conventions

- Files: `snake_case.dart`
- Classes: `PascalCase`
- Widgets: `widget_name_widget.dart`
- Models: `model_name.dart`
- Services: `service_name_service.dart`

## Code Organization Rules

### Maximum 300 Lines Per File

If file exceeds 300 lines:
1. Extract helper functions
2. Split into multiple files
3. Use barrel exports (`index.dart`)

### One Class Per File

```dart
// ✅ CORRECT
// card_component.dart
class CardComponent extends SpriteComponent { }

// ❌ WRONG
// multiple_classes.dart
class CardComponent extends SpriteComponent { }
class CardManager extends Component { }  // Should be separate file
```

### Barrel Exports

```dart
// lib/features/cards/presentation/components/index.dart
export 'card_component.dart';
export 'card_hand.dart';
export 'card_effect.dart';

// Usage
import 'package:app/features/cards/presentation/components/index.dart';
```

## State Management Philosophy

### Riverpod (Not Redux)

We use **Riverpod** for Flutter-native state management:

```dart
// Game state provider
final gameStateProvider = StateNotifierProvider<GameStateNotifier, GameState>((ref) {
  return GameStateNotifier();
});

// Usage in widget
class GameScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final gameState = ref.watch(gameStateProvider);
    return Text('Turn ${gameState.currentTurn}');
  }
}
```

### Why Riverpod?
- Type-safe
- Compile-time errors
- Flutter-native patterns
- Better testability
- No boilerplate

### Why Not Redux?
- Too much boilerplate
- Not Flutter-native
- Overkill for game state
- Poor performance (excessive rebuilds)

## Flame Integration

### Flame Components = Game Visuals

```dart
// Flame component for rendering
class CardComponent extends SpriteAnimationGroupComponent<CardState> {
  // Handles: rendering, animation, visual effects
}

// Flutter widget for UI overlay
class CardHUD extends ConsumerWidget {
  // Handles: buttons, text, UI elements
}
```

### Game Reference Pattern

```dart
class CardComponent extends PositionComponent 
    with HasGameReference<UnwrittenGame> {
  
  @override
  Future<void> onLoad() async {
    // Access game services
    game.audioManager.playSfx('card_draw');
    game.ref.read(gameStateProvider);  // Access Riverpod
  }
}
```

## Performance Guidelines

### Const Constructors

```dart
// ✅ CORRECT
const CardBorder({required this.width});

// ❌ WRONG
CardBorder({required this.width});  // Not const
```

### Async Operations

```dart
// ✅ CORRECT: Heavy work in isolate
final result = await compute(_parseJsonData, jsonString);

// ❌ WRONG: Blocking main thread
final result = jsonDecode(jsonString);  // Heavy operation
```

### Resource Disposal

```dart
class CardComponent extends PositionComponent {
  StreamSubscription? _subscription;
  
  @override
  Future<void> onLoad() async {
    _subscription = stream.listen(_onData);
  }
  
  @override
  void onRemove() {
    _subscription?.cancel();  // ✅ Always cleanup
    super.onRemove();
  }
}
```

## Testing Requirements

Every feature must have:

1. **Unit Tests:** Business logic (usecases)
2. **Widget Tests:** UI components
3. **Integration Tests:** Critical paths (card play flow)

Minimum coverage: 80% for critical features.

## Documentation Standards

### Public APIs Must Have Docs

```dart
/// Manages card interactions and animations.
/// 
/// Example:
/// ```dart
/// final manager = CardManager();
/// await manager.playCard(cardData);
/// ```
class CardManager {
  /// Plays the given card with animation.
  /// 
  /// Returns true if card was played successfully.
  Future<bool> playCard(CardData card) async { }
}
```

### No Docs on Private Members

```dart
// ✅ CORRECT: Public documented, private not
/// Public method with docs
void publicMethod() { }

void _privateMethod() { }  // No docs needed

// ❌ WRONG: Over-documenting private
/// Private helper  (unnecessary)
void _helper() { }
```

## Security & Privacy

### No Sensitive Data in Logs

```dart
// ✅ CORRECT
AppLogger.info('User progress saved', {
  'cards_collected': progress.cardsCollected,
});

// ❌ WRONG
print('Saving progress for ${user.email}');  // Exposed PII
```

---

**Previous:** [Performance Targets](./02-performance-targets.md)  
**Index:** [Overview Index](./00-INDEX.md)  
**Related:** [Project Structure](../01-architecture/01-project-structure.md)


