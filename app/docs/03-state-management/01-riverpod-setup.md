# Riverpod State Management

**Package:** `flutter_riverpod ^3.0.3`  
**Status:** ✅ UP TO DATE  
**Flame Integration:** Manual (see below)

---

## Overview

Riverpod is Unwritten's state management solution, providing compile-safe, testable, and reactive state management for game logic, UI, and data flow.

## Why Riverpod?

- ✅ **Compile-Safe**: Catch errors at compile-time, not runtime
- ✅ **No BuildContext**: Access providers from anywhere (including Flame components)
- ✅ **Testable**: Built with testing in mind
- ✅ **AsyncValue**: First-class loading/error states
- ✅ **Auto-Dispose**: Automatic memory management
- ✅ **Code Generation**: Reduce boilerplate with annotations

---

## Installation

```yaml
dependencies:
  flutter_riverpod: ^3.0.3
  riverpod_annotation: ^3.0.3
  
dev_dependencies:
  riverpod_generator: ^3.0.3
  build_runner: ^2.4.12
```

---

## Core Concepts

### Provider Types

```dart
// Simple value provider
final counterProvider = StateProvider<int>((ref) => 0);

// Async provider (Future)
final userProvider = FutureProvider<User>((ref) async {
  return await fetchUser();
});

// Stream provider
final eventsProvider = StreamProvider<List<Event>>((ref) {
  return eventStream;
});

// StateNotifier provider (complex state)
final gameStateProvider = StateNotifierProvider<GameNotifier, GameState>(
  (ref) => GameNotifier(ref.read(aiServiceProvider)),
);
```

### Consumer Widget

```dart
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    
    return Text('Count: $count');
  }
}
```

### Code Generation

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'game_providers.g.dart';

@riverpod
class GameState extends _$GameState {
  @override
  Future<GameModel> build() async {
    return await loadGame();
  }
  
  Future<void> playCard(CardModel card) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final newGame = await _gameService.playCard(card);
      return newGame;
    });
  }
}

// Usage in widgets
class GameScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final gameState = ref.watch(gameStateProvider);
    
    return gameState.when(
      data: (game) => GameView(game: game),
      loading: () => LoadingScreen(),
      error: (err, stack) => ErrorScreen(error: err),
    );
  }
}
```

---

## Generated Provider Types

```dart
// Simple provider
@riverpod
String greeting(GreetingRef ref) => 'Hello';

// Async provider
@riverpod
Future<User> user(UserRef ref, String id) async {
  return await fetchUser(id);
}

// Stream provider
@riverpod
Stream<List<Event>> events(EventsRef ref) {
  return eventStream;
}

// Class-based provider (stateful)
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;
  
  void increment() => state++;
  void decrement() => state--;
}
```

---

## Unwritten Game State

### Game State Provider

```dart
@riverpod
class GameState extends _$GameState {
  @override
  Future<GameData> build() async {
    // Load saved game or create new
    final savedGame = await ref.read(storageServiceProvider).loadGame();
    return savedGame ?? GameData.initial();
  }
  
  Future<void> playCard(CardModel card) async {
    state = const AsyncValue.loading();
    
    state = await AsyncValue.guard(() async {
      final currentGame = state.value!;
      
      // Validate card play
      if (!currentGame.canPlayCard(card)) {
        throw InvalidCardPlayException('Not enough resources');
      }
      
      // Update game state
      final newGame = currentGame.playCard(card);
      
      // Save game
      await ref.read(storageServiceProvider).saveGame(newGame);
      
      return newGame;
    });
  }
  
  Future<void> drawCard() async {
    state = await AsyncValue.guard(() async {
      final currentGame = state.value!;
      return currentGame.drawCard();
    });
  }
  
  Future<void> endTurn() async {
    state = await AsyncValue.guard(() async {
      final currentGame = state.value!;
      return currentGame.advanceTurn();
    });
  }
}
```

### Card Hand Provider

```dart
@riverpod
class CardHand extends _$CardHand {
  @override
  List<CardModel> build() {
    // Watch game state and extract hand
    final gameState = ref.watch(gameStateProvider);
    return gameState.maybeWhen(
      data: (game) => game.hand,
      orElse: () => [],
    );
  }
  
  void removeCard(CardModel card) {
    state = state.where((c) => c.id != card.id).toList();
  }
  
  void addCard(CardModel card) {
    state = [...state, card];
  }
}
```

### Resources Provider

```dart
@riverpod
class Resources extends _$Resources {
  @override
  ResourcesModel build() {
    final gameState = ref.watch(gameStateProvider);
    return gameState.maybeWhen(
      data: (game) => game.resources,
      orElse: () => ResourcesModel.empty(),
    );
  }
  
  bool canAfford(Map<String, double> costs) {
    return state.canAfford(costs);
  }
}
```

---

## Flame Integration

### Access Providers from Flame Components

Riverpod doesn't directly integrate with Flame, but you can access providers using a manual pattern:

#### Pattern 1: Provider Container Reference

```dart
class GameWorld extends FlameGame with HasGameRef {
  final ProviderContainer container;
  
  GameWorld({required this.container});
  
  @override
  Future<void> onLoad() async {
    // Read provider values
    final gameState = container.read(gameStateProvider);
    
    // Listen to provider changes
    container.listen(
      gameStateProvider,
      (previous, next) {
        // Update game components based on state
        _updateComponents(next);
      },
    );
  }
}

// In main.dart
final container = ProviderContainer();

runApp(
  UncontrolledProviderScope(
    container: container,
    child: GameWidget(
      game: GameWorld(container: container),
    ),
  ),
);
```

#### Pattern 2: Ref Passing

```dart
class CardComponent extends PositionComponent {
  final WidgetRef ref;
  
  CardComponent({required this.ref});
  
  @override
  void onTapUp(TapUpEvent event) {
    // Read providers
    final gameState = ref.read(gameStateProvider.notifier);
    gameState.playCard(card);
  }
}

// Create component with ref
class GameScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return GameWidget(
      game: GameWorld(
        onComponentCreate: (component) {
          if (component is CardComponent) {
            component.ref = ref;
          }
        },
      ),
    );
  }
}
```

#### Pattern 3: Event Bus

```dart
// For loose coupling
final gameEventBusProvider = Provider((ref) => GameEventBus());

class GameEventBus {
  final _controller = StreamController<GameEvent>.broadcast();
  
  Stream<GameEvent> get events => _controller.stream;
  
  void emit(GameEvent event) {
    _controller.add(event);
  }
}

// In Flame component
class CardComponent extends PositionComponent {
  final GameEventBus eventBus;
  
  CardComponent({required this.eventBus});
  
  @override
  void onTapUp(TapUpEvent event) {
    eventBus.emit(CardPlayedEvent(card));
  }
}

// In Riverpod provider
@riverpod
class GameState extends _$GameState {
  @override
  Future<GameData> build() async {
    final eventBus = ref.read(gameEventBusProvider);
    
    // Listen to game events
    eventBus.events.listen((event) {
      if (event is CardPlayedEvent) {
        playCard(event.card);
      }
    });
    
    return await loadGame();
  }
}
```

---

## Best Practices

### 1. Use ConsumerWidget

```dart
// ✅ GOOD
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final value = ref.watch(myProvider);
    return Text('$value');
  }
}

// ❌ BAD
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer((context, ref, child) {
      // Less efficient
    });
  }
}
```

### 2. Watch vs Read vs Listen

```dart
// watch - Rebuild when state changes
final value = ref.watch(myProvider);

// read - One-time read, no rebuild
final value = ref.read(myProvider);

// listen - Side-effects without rebuild
ref.listen(myProvider, (previous, next) {
  // Show snackbar, navigate, etc.
});
```

### 3. AsyncValue Handling

```dart
// ✅ GOOD - Handle all states
ref.watch(userProvider).when(
  data: (user) => Text(user.name),
  loading: () => CircularProgressIndicator(),
  error: (err, stack) => Text('Error: $err'),
);

// ❌ BAD - Crash on error
final user = ref.watch(userProvider).value!; // Will crash on error
```

### 4. Provider Scope

```dart
void main() {
  runApp(
    // Always wrap app in ProviderScope
    ProviderScope(
      child: MyApp(),
    ),
  );
}
```

---

## Performance Optimization

### 1. Select Specific Values

```dart
// ❌ BAD - Rebuilds on any game state change
final game = ref.watch(gameStateProvider);
final energy = game.value?.resources.energy ?? 0;

// ✅ GOOD - Only rebuilds when energy changes
final energy = ref.watch(
  gameStateProvider.select((state) => 
    state.value?.resources.energy ?? 0
  ),
);
```

### 2. Use Family for Parameterized Providers

```dart
@riverpod
Future<CardModel> card(CardRef ref, String id) async {
  return await fetchCard(id);
}

// Usage
final card = ref.watch(cardProvider('card_001'));
```

### 3. AutoDispose for Temporary State

```dart
@riverpod
class TemporaryState extends _$TemporaryState {
  @override
  int build() => 0;
  
  void increment() => state++;
}

// Automatically disposed when no longer used
```

---

## Testing

### Unit Test Providers

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('Counter increments', () {
    final container = ProviderContainer();
    
    expect(container.read(counterProvider), 0);
    
    container.read(counterProvider.notifier).increment();
    
    expect(container.read(counterProvider), 1);
    
    container.dispose();
  });
  
  test('Game state plays card', () async {
    final container = ProviderContainer(
      overrides: [
        storageServiceProvider.overrideWithValue(MockStorage()),
      ],
    );
    
    final gameState = container.read(gameStateProvider.notifier);
    await gameState.playCard(testCard);
    
    final state = container.read(gameStateProvider).value!;
    expect(state.hand.length, lessThan(5));
    
    container.dispose();
  });
}
```

### Widget Test with Providers

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Counter increments on tap', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        child: MaterialApp(
          home: CounterScreen(),
        ),
      ),
    );
    
    expect(find.text('0'), findsOneWidget);
    
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();
    
    expect(find.text('1'), findsOneWidget);
  });
}
```

---

## Code Generation

### Generate Providers

```bash
# One-time build
flutter pub run build_runner build --delete-conflicting-outputs

# Watch mode (auto-rebuild)
flutter pub run build_runner watch --delete-conflicting-outputs

# Clean and rebuild
flutter pub run build_runner clean
flutter pub run build_runner build --delete-conflicting-outputs
```

---

## Resources

### Official Documentation
- **Riverpod Docs**: https://riverpod.dev/
- **GitHub**: https://github.com/rrousselGit/riverpod
- **Migration Guide**: https://riverpod.dev/docs/migration/from_provider

### Related Packages
- `riverpod_annotation`: Annotations for code generation
- `riverpod_generator`: Code generator
- `flutter_hooks`: React-like hooks (optional)
- `riverpod_lint`: Additional lint rules

### Flame Integration
- [Flame Riverpod Integration](../02-flame-engine/10-flame-riverpod-integration.md)

---

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Master Spec Reference:** `docs/master_flutter_flame_spec_v_1_0.md`


