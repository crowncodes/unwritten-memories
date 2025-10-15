# State Management Architecture

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete

---

## Overview

Unwritten uses **Riverpod 3.x** for state management, manually integrated with Flame game engine. This guide covers provider patterns, code generation, and Flame integration.

**Why Riverpod 3.x:** Latest features, compile-time safety, better performance than 2.x

**Why Manual Flame Integration:** flame_riverpod requires Riverpod 2.x (incompatible)

---

## Riverpod 3.x Fundamentals

### Setup

**pubspec.yaml:**
```yaml
dependencies:
  flutter_riverpod: ^3.0.3
  riverpod_annotation: ^3.0.0

dev_dependencies:
  riverpod_generator: ^3.0.0
  build_runner: ^2.4.0
```

**Generate Code:**
```bash
flutter pub run build_runner watch --delete-conflicting-outputs
```

### Provider Types

| Type | Use Case | Example |
|------|----------|---------|
| **Provider** | Static/computed data | Config, constants |
| **StateProvider** | Simple mutable state | Counter, toggle |
| **StateNotifierProvider** | Complex state logic | Game state, card hand |
| **AsyncNotifierProvider** | Async operations | API calls, data loading |
| **FutureProvider** | One-time async data | Initial data fetch |
| **StreamProvider** | Real-time updates | WebSocket, Firebase |

---

## Code Generation Patterns

### AsyncNotifierProvider (Recommended)

**Use for:** Most feature state (async operations common)

```dart
// features/cards/presentation/providers/card_providers.dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'card_providers.g.dart';

@riverpod
class CardNotifier extends _$CardNotifier {
  @override
  FutureOr<List<Card>> build() async {
    // Initial state (async loading)
    return await _loadCards();
  }
  
  Future<void> playCard(String cardId) async {
    state = const AsyncValue.loading();
    
    try {
      final result = await ref.read(playCardUseCaseProvider).call(cardId);
      
      result.fold(
        (failure) => state = AsyncValue.error(failure, StackTrace.current),
        (updatedCards) => state = AsyncValue.data(updatedCards),
      );
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }
  
  Future<List<Card>> _loadCards() async {
    final result = await ref.read(getCardsUseCaseProvider).call();
    return result.fold(
      (failure) => throw failure,
      (cards) => cards,
    );
  }
}
```

**Generated Code:**
```dart
// card_providers.g.dart (auto-generated)
final cardNotifierProvider =
    AsyncNotifierProvider<CardNotifier, List<Card>>(() {
  return CardNotifier();
});
```

### StateNotifierProvider (Simple State)

**Use for:** Synchronous state changes

```dart
@riverpod
class GameTurnNotifier extends _$GameTurnNotifier {
  @override
  int build() => 1; // Initial turn
  
  void nextTurn() {
    state = state + 1;
  }
  
  void resetTurn() {
    state = 1;
  }
}
```

### Provider (Computed Values)

**Use for:** Derived state (selectors)

```dart
@riverpod
int availableActions(AvailableActionsRef ref) {
  final resources = ref.watch(resourcesProvider);
  final cards = ref.watch(cardNotifierProvider);
  
  // Computed: how many cards can player afford?
  return cards.when(
    data: (cards) => cards.where((c) => c.cost <= resources.actions).length,
    loading: () => 0,
    error: (_, __) => 0,
  );
}
```

---

## Flame + Riverpod Manual Integration

### Pattern 1: Provider in GameWidget

**Problem:** Flame game needs access to Riverpod state

**Solution:** Pass state via GameWidget constructor

```dart
// features/game/presentation/screens/game_screen.dart
class GameScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final gameState = ref.watch(gameStateProvider);
    final cards = ref.watch(cardNotifierProvider);
    
    return Scaffold(
      body: Stack(
        children: [
          // Flame game (pass state as constructor args)
          GameWidget(
            game: UnwrittenGame(
              initialState: gameState,
              cards: cards.value ?? [],
              onCardPlay: (cardId) {
                // Callback to Riverpod
                ref.read(cardNotifierProvider.notifier).playCard(cardId);
              },
              onTurnEnd: () {
                ref.read(gameTurnNotifierProvider.notifier).nextTurn();
              },
            ),
          ),
          
          // Flutter UI overlays
          Positioned(
            top: 16,
            child: ResourcesBar(),
          ),
        ],
      ),
    );
  }
}
```

### Pattern 2: Reactive Game Updates

**Problem:** Game needs to react to provider changes

**Solution:** Listen to providers and update game

```dart
class GameScreen extends ConsumerWidget {
  final UnwrittenGame _game = UnwrittenGame();
  
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Listen to state changes
    ref.listen(gameStateProvider, (previous, next) {
      // Update game when state changes
      _game.updateState(next);
    });
    
    ref.listen(cardNotifierProvider, (previous, next) {
      next.whenData((cards) {
        _game.updateCards(cards);
      });
    });
    
    return GameWidget(game: _game);
  }
}
```

### Pattern 3: Callback-Based Communication

**Problem:** Flame component needs to trigger Riverpod action

**Solution:** Pass callbacks from ConsumerWidget

```dart
// Flame component
class CardGameComponent extends PositionComponent {
  final void Function(String cardId) onCardPlay;
  
  CardGameComponent({required this.onCardPlay});
  
  void _handleCardTap(String cardId) {
    onCardPlay(cardId); // Trigger Riverpod action
  }
}

// In GameWidget setup
GameWidget(
  game: UnwrittenGame(
    onCardPlay: (cardId) {
      ref.read(cardNotifierProvider.notifier).playCard(cardId);
    },
  ),
)
```

---

## Provider Organization

### By Feature

```dart
// features/cards/presentation/providers/card_providers.dart
@riverpod
class CardNotifier extends _$CardNotifier { }

@riverpod
class CardHandNotifier extends _$CardHandNotifier { }

@riverpod
int cardCount(CardCountRef ref) => // ...

// features/game/presentation/providers/game_providers.dart
@riverpod
class GameStateNotifier extends _$GameStateNotifier { }

@riverpod
class ResourcesNotifier extends _$ResourcesNotifier { }
```

### Dependencies Between Providers

```dart
@riverpod
class GameStateNotifier extends _$GameStateNotifier {
  @override
  GameState build() {
    // Depend on other providers
    final cards = ref.watch(cardNotifierProvider);
    final resources = ref.watch(resourcesNotifierProvider);
    
    return GameState(
      cards: cards.value ?? [],
      resources: resources,
    );
  }
}
```

---

## Error Handling

### AsyncValue Pattern

```dart
// In provider
state = const AsyncValue.loading();

try {
  final result = await _fetchData();
  state = AsyncValue.data(result);
} catch (error, stackTrace) {
  state = AsyncValue.error(error, stackTrace);
}

// In UI
ref.watch(cardNotifierProvider).when(
  data: (cards) => CardListWidget(cards),
  loading: () => CircularProgressIndicator(),
  error: (error, stack) => ErrorWidget(error),
)
```

### Either Pattern (with fpdart)

```dart
// In provider
final result = await ref.read(getCardsUseCaseProvider).call();

result.fold(
  (failure) {
    // Handle failure
    state = AsyncValue.error(failure, StackTrace.current);
    _showError(failure.message);
  },
  (cards) {
    // Handle success
    state = AsyncValue.data(cards);
  },
);
```

---

## Optimistic UI Updates

### Pattern

**Goal:** Instant feedback while server validates

```dart
@riverpod
class CardNotifier extends _$CardNotifier {
  Future<void> playCard(String cardId) async {
    // 1. Get current state
    final currentCards = state.value ?? [];
    
    // 2. Optimistic update (instant)
    final optimisticCards = currentCards
        .where((c) => c.id != cardId)
        .toList();
    state = AsyncValue.data(optimisticCards);
    
    // 3. Server validation (background)
    try {
      final result = await ref.read(playCardUseCaseProvider).call(cardId);
      
      result.fold(
        (failure) {
          // 4a. Rollback on failure
          state = AsyncValue.data(currentCards);
          _showError(failure.message);
        },
        (serverCards) {
          // 4b. Apply server state
          state = AsyncValue.data(serverCards);
        },
      );
    } catch (e) {
      // Rollback on exception
      state = AsyncValue.data(currentCards);
    }
  }
}
```

**Benefits:**
- ✅ Instant UI feedback (<1ms)
- ✅ Server validates in background
- ✅ Rollback if server disagrees
- ✅ Feels native, not networked

---

## Testing Providers

### Unit Testing

```dart
// test/features/cards/presentation/providers/card_providers_test.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('CardNotifier', () {
    late ProviderContainer container;
    
    setUp(() {
      container = ProviderContainer();
    });
    
    tearDown(() {
      container.dispose();
    });
    
    test('initial state is loading', () {
      final provider = container.read(cardNotifierProvider);
      expect(provider, const AsyncValue<List<Card>>.loading());
    });
    
    test('playCard removes card optimistically', () async {
      // Setup
      final notifier = container.read(cardNotifierProvider.notifier);
      await container.read(cardNotifierProvider.future);
      
      // Act
      await notifier.playCard('card-1');
      
      // Assert
      final state = container.read(cardNotifierProvider).value!;
      expect(state.any((c) => c.id == 'card-1'), false);
    });
  });
}
```

### Widget Testing with Providers

```dart
testWidgets('CardWidget uses provider data', (tester) async {
  await tester.pumpWidget(
    ProviderScope(
      overrides: [
        cardNotifierProvider.overrideWith(() {
          return MockCardNotifier();
        }),
      ],
      child: MaterialApp(
        home: CardWidget(),
      ),
    ),
  );
  
  expect(find.text('Card Title'), findsOneWidget);
});
```

---

## Performance Optimization

### Auto-Dispose Providers

**Problem:** Providers stay in memory even when not used

**Solution:** Use `@riverpod` (auto-disposes by default)

```dart
// Auto-disposes when no longer watched
@riverpod
FutureOr<List<Card>> cards(CardsRef ref) async {
  return await _fetchCards();
}

// To keep alive
@Riverpod(keepAlive: true)
FutureOr<AppConfig> appConfig(AppConfigRef ref) async {
  return await _loadConfig();
}
```

### Select (Reduce Rebuilds)

**Problem:** Widget rebuilds on every provider change

**Solution:** Use `select` to watch specific field

```dart
// ❌ BAD: Rebuilds on any gameState change
final gameState = ref.watch(gameStateProvider);

// ✅ GOOD: Rebuilds only when turn changes
final turn = ref.watch(gameStateProvider.select((state) => state.turn));
```

### Family Providers (Cache by Parameter)

```dart
@riverpod
FutureOr<Card> card(CardRef ref, String cardId) async {
  return await _fetchCard(cardId);
}

// Usage: Each cardId has its own provider instance
final card1 = ref.watch(cardProvider('card-1'));
final card2 = ref.watch(cardProvider('card-2'));
```

---

## Common Patterns

### Loading State

```dart
Consumer(
  builder: (context, ref, child) {
    return ref.watch(cardNotifierProvider).when(
      data: (cards) => CardListView(cards),
      loading: () => Center(child: CircularProgressIndicator()),
      error: (error, stack) => ErrorView(error),
    );
  },
)
```

### Pagination

```dart
@riverpod
class CardsNotifier extends _$CardsNotifier {
  int _page = 1;
  
  @override
  FutureOr<List<Card>> build() async {
    return await _fetchPage(1);
  }
  
  Future<void> loadMore() async {
    final currentCards = state.value ?? [];
    _page++;
    final nextCards = await _fetchPage(_page);
    state = AsyncValue.data([...currentCards, ...nextCards]);
  }
}
```

### Debouncing

```dart
@riverpod
class SearchNotifier extends _$SearchNotifier {
  Timer? _debounce;
  
  @override
  FutureOr<List<Card>> build() => [];
  
  void search(String query) {
    _debounce?.cancel();
    _debounce = Timer(Duration(milliseconds: 300), () async {
      final results = await _searchCards(query);
      state = AsyncValue.data(results);
    });
  }
}
```

---

## Related Documentation

- **50-architecture-overview.md** - Architecture decisions
- **51-project-structure-guide.md** - Provider organization
- **61-riverpod-integration.md** - Detailed Riverpod guide
- **67-testing-strategy.md** - Testing providers

---

## Quick Reference

### Provider Cheat Sheet

```dart
// Static data
@riverpod
AppConfig config(ConfigRef ref) => AppConfig();

// Async data
@riverpod
FutureOr<User> user(UserRef ref) async => await _fetchUser();

// Mutable state
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;
  void increment() => state++;
}

// Watch provider
final value = ref.watch(counterProvider);

// Read once (no rebuild)
final value = ref.read(counterProvider);

// Listen to changes
ref.listen(counterProvider, (prev, next) {
  print('Changed from $prev to $next');
});
```

---

**Status:** ✅ State Management Complete  
**Pattern:** Riverpod 3.x + Manual Flame Integration  
**Performance:** Optimistic UI + Auto-Dispose

