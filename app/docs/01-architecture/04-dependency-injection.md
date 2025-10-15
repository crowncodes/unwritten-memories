# Dependency Injection with Riverpod

**Status:** ✅ Implemented  
**Package:** `flutter_riverpod ^2.6.1` + `riverpod_generator ^2.6.2`  
**Pattern:** Code Generation + Provider Composition

---

## Overview

Unwritten uses **Riverpod** for dependency injection and state management. Riverpod provides compile-time safety, automatic disposal, and powerful provider composition. We use **code generation** with `riverpod_generator` for type-safe, boilerplate-free DI.

## Why Riverpod?

- ✅ **Compile-time safety**: Catch errors before runtime
- ✅ **No BuildContext**: Access providers anywhere (including Flame)
- ✅ **Automatic disposal**: No memory leaks
- ✅ **Testability**: Easy to mock and override
- ✅ **Provider composition**: Providers depend on other providers
- ✅ **Flame integration**: Perfect for game development

---

## Setup

### 1. Dependencies

```yaml
dependencies:
  flutter_riverpod: ^2.6.1
  riverpod_annotation: ^2.6.1

dev_dependencies:
  riverpod_generator: ^2.6.2
  build_runner: ^2.4.12
  riverpod_lint: ^2.6.1
  custom_lint: ^0.7.0
```

### 2. Main App Initialization

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Hive
  await Hive.initFlutter();
  
  runApp(
    const ProviderScope(  // ← Required root widget
      child: UnwrittenApp(),
    ),
  );
}
```

### 3. Code Generation

```bash
# Watch for changes (recommended during development)
flutter pub run build_runner watch --delete-conflicting-outputs

# One-time build
flutter pub run build_runner build --delete-conflicting-outputs
```

---

## Provider Types

### 1. Provider (Immutable, Sync)

**Use for:** Constants, computed values, singletons

```dart
@riverpod
AppConstants appConstants(AppConstantsRef ref) {
  return const AppConstants(
    maxHandSize: 7,
    maxEnergy: 3,
    startingResources: {'energy': 3, 'time': 168},
  );
}

// Usage
final constants = ref.watch(appConstantsProvider);
```

### 2. FutureProvider (Async, Immutable)

**Use for:** One-time async operations, initialization

```dart
@riverpod
Future<List<CardEntity>> initialCards(InitialCardsRef ref) async {
  final repository = ref.watch(cardRepositoryProvider);
  return await repository.getStartingCards();
}

// Usage in widget
final cardsAsync = ref.watch(initialCardsProvider);
return cardsAsync.when(
  data: (cards) => CardGrid(cards: cards),
  loading: () => CircularProgressIndicator(),
  error: (error, stack) => ErrorWidget(error),
);
```

### 3. StreamProvider (Reactive Streams)

**Use for:** Real-time updates, Firebase streams

```dart
@riverpod
Stream<GameStateEntity> gameStateStream(GameStateStreamRef ref) {
  final repository = ref.watch(gameStateRepositoryProvider);
  return repository.watchGameState();  // Hive box stream
}

// Usage
final gameStateAsync = ref.watch(gameStateStreamProvider);
```

### 4. StateNotifier / NotifierProvider (Mutable State)

**Use for:** Complex state management, game logic

```dart
@riverpod
class GameState extends _$GameState {
  @override
  GameStateEntity build() {
    return GameStateEntity.initial();
  }
  
  void advanceTurn() {
    state = state.copyWith(turn: state.turn + 1);
  }
  
  void advancePhase(Phase newPhase) {
    state = state.copyWith(currentPhase: newPhase);
  }
  
  Future<void> playCard(CardEntity card) async {
    // Validate resources
    if (!card.canPlay(state.resources)) {
      throw InsufficientResourcesError();
    }
    
    // Apply card effects
    final updatedResources = _applyCardCosts(state.resources, card);
    state = state.copyWith(
      resources: updatedResources,
      hand: state.hand.where((c) => c.id != card.id).toList(),
    );
    
    // Save to repository
    final repository = ref.read(gameStateRepositoryProvider);
    await repository.save(state);
  }
  
  ResourcesEntity _applyCardCosts(ResourcesEntity resources, CardEntity card) {
    var updated = resources;
    for (final cost in card.costs.entries) {
      updated = updated.reduceResource(cost.key, cost.value);
    }
    return updated;
  }
}

// Usage
final gameState = ref.watch(gameStateProvider);
ref.read(gameStateProvider.notifier).advanceTurn();
```

### 5. AsyncNotifier (Async State Management)

**Use for:** State that requires async initialization

```dart
@riverpod
class CardCollection extends _$CardCollection {
  @override
  Future<List<CardEntity>> build() async {
    // Async initialization
    final repository = ref.watch(cardRepositoryProvider);
    return await repository.getAllCards();
  }
  
  Future<void> addCard(CardEntity card) async {
    // Optimistic update
    state = AsyncValue.data([...state.value!, card]);
    
    try {
      final repository = ref.read(cardRepositoryProvider);
      await repository.addCard(card);
    } catch (e, stack) {
      // Rollback on error
      state = AsyncValue.error(e, stack);
    }
  }
  
  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final repository = ref.read(cardRepositoryProvider);
      return await repository.getAllCards();
    });
  }
}
```

---

## Dependency Hierarchy

### Complete DI Structure

```dart
// ========================================
// Data Layer Providers
// ========================================

// Data Sources
@riverpod
CardLocalDataSource cardLocalDataSource(CardLocalDataSourceRef ref) {
  final box = Hive.box<CardModel>('cards');
  return CardLocalDataSource(box);
}

@riverpod
GameStateLocalDataSource gameStateLocalDataSource(
  GameStateLocalDataSourceRef ref,
) {
  final box = Hive.box<GameStateModel>('game_state');
  return GameStateLocalDataSource(box);
}

// Repositories (Implementation)
@riverpod
CardRepository cardRepository(CardRepositoryRef ref) {
  return CardRepositoryImpl(
    ref.watch(cardLocalDataSourceProvider),
  );
}

@riverpod
GameStateRepository gameStateRepository(GameStateRepositoryRef ref) {
  return GameStateRepositoryImpl(
    ref.watch(gameStateLocalDataSourceProvider),
  );
}

// ========================================
// Domain Layer Providers
// ========================================

// Use Cases
@riverpod
GetAvailableCardsUseCase getAvailableCardsUseCase(
  GetAvailableCardsUseCaseRef ref,
) {
  return GetAvailableCardsUseCase(
    ref.watch(cardRepositoryProvider),
  );
}

@riverpod
PlayCardUseCase playCardUseCase(PlayCardUseCaseRef ref) {
  return PlayCardUseCase(
    ref.watch(cardRepositoryProvider),
    ref.watch(gameStateRepositoryProvider),
  );
}

@riverpod
AdvanceTurnUseCase advanceTurnUseCase(AdvanceTurnUseCaseRef ref) {
  return AdvanceTurnUseCase(
    ref.watch(gameStateRepositoryProvider),
  );
}

// ========================================
// Presentation Layer Providers
// ========================================

// State Notifiers
@riverpod
class GameState extends _$GameState {
  @override
  GameStateEntity build() => GameStateEntity.initial();
  
  Future<void> loadGame() async {
    final loadUseCase = ref.read(loadGameUseCaseProvider);
    final result = await loadUseCase.execute();
    result.fold(
      onSuccess: (gameState) => state = gameState,
      onError: (_) => state = GameStateEntity.initial(),
    );
  }
  
  Future<void> advanceTurn() async {
    final useCase = ref.read(advanceTurnUseCaseProvider);
    await useCase.execute();
    state = state.copyWith(turn: state.turn + 1);
  }
}

@riverpod
class CardHand extends _$CardHand {
  @override
  List<CardEntity> build() {
    // Listen to game state for hand updates
    return ref.watch(gameStateProvider.select((state) => state.hand));
  }
  
  Future<void> playCard(CardEntity card) async {
    final playCardUseCase = ref.read(playCardUseCaseProvider);
    await playCardUseCase.execute(card);
    
    // Refresh game state
    ref.invalidate(gameStateProvider);
  }
}

// Derived State (Computed Values)
@riverpod
bool canPlayCard(CanPlayCardRef ref, CardEntity card) {
  final gameState = ref.watch(gameStateProvider);
  return card.canPlay(gameState.resources);
}

@riverpod
int availableEnergy(AvailableEnergyRef ref) {
  return ref.watch(
    gameStateProvider.select((state) => state.resources.energy),
  );
}
```

---

## Flame Integration

### Passing WidgetRef to Flame Game

```dart
class UnwrittenGame extends FlameGame with HasCollisionDetection {
  final WidgetRef ref;
  
  UnwrittenGame({required this.ref});
  
  @override
  Future<void> onLoad() async {
    // Access providers directly from game
    final gameState = ref.read(gameStateProvider);
    final cards = await ref.read(initialCardsProvider.future);
    
    // Create world with ref
    world = GameWorld(ref: ref);
    camera = CameraComponent.withFixedResolution(
      width: 1920,
      height: 1080,
      world: world,
    );
  }
}

// Usage in GameWidget
class GameBoardScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: GameWidget(
        game: UnwrittenGame(ref: ref),  // ← Pass ref to game
      ),
    );
  }
}
```

### Accessing Providers from Flame Components

```dart
class CardComponent extends SpriteAnimationGroupComponent 
    with TapCallbacks, DragCallbacks {
  final CardEntity card;
  final WidgetRef ref;
  
  CardComponent({
    required this.card,
    required this.ref,
  });
  
  @override
  Future<void> onLoad() async {
    // Access providers
    final canPlay = ref.read(canPlayCardProvider(card));
    
    if (canPlay) {
      current = CardState.playable;
    } else {
      current = CardState.disabled;
    }
  }
  
  @override
  void onTapUp(TapUpEvent event) async {
    // Use state notifier
    try {
      await ref.read(cardHandProvider.notifier).playCard(card);
      
      // Success animation
      add(CardPlayEffect());
      removeFromParent();
    } catch (e) {
      // Error feedback
      add(ErrorShakeEffect());
    }
  }
  
  @override
  void update(double dt) {
    super.update(dt);
    
    // Reactive updates from providers
    final canPlay = ref.read(canPlayCardProvider(card));
    if (canPlay && current != CardState.playable) {
      current = CardState.playable;
    } else if (!canPlay && current != CardState.disabled) {
      current = CardState.disabled;
    }
  }
}

// Game World with Providers
class GameWorld extends Component {
  final WidgetRef ref;
  
  GameWorld({required this.ref});
  
  @override
  Future<void> onLoad() async {
    // Listen to game state changes
    ref.listen<GameStateEntity>(gameStateProvider, (previous, next) {
      if (previous?.turn != next.turn) {
        _onTurnChanged(next.turn);
      }
    });
    
    // Create initial components from state
    final gameState = ref.read(gameStateProvider);
    for (final card in gameState.hand) {
      add(CardComponent(card: card, ref: ref));
    }
  }
  
  void _onTurnChanged(int newTurn) {
    // Refresh hand
    removeAll(children.whereType<CardComponent>());
    
    final hand = ref.read(cardHandProvider);
    for (final card in hand) {
      add(CardComponent(card: card, ref: ref));
    }
  }
}
```

---

## Advanced Patterns

### 1. Provider Families (Parameterized Providers)

```dart
@riverpod
Future<CardEntity?> cardById(CardByIdRef ref, String id) async {
  final repository = ref.watch(cardRepositoryProvider);
  return await repository.getCardById(id);
}

// Usage
final card = ref.watch(cardByIdProvider('card_001'));
```

### 2. Provider Modifiers

```dart
// Select specific parts of state
final energy = ref.watch(
  gameStateProvider.select((state) => state.resources.energy),
);

// Only rebuilds when energy changes, not entire game state!

// Auto-dispose (clean up when no longer used)
@riverpod
Future<List<CardEntity>> temporaryCards(TemporaryCardsRef ref) async {
  ref.keepAlive();  // Or ref.onDispose(() { /* cleanup */ });
  return await ref.watch(cardRepositoryProvider).getTemporaryCards();
}
```

### 3. Provider Composition

```dart
@riverpod
Future<GameSummary> gameSummary(GameSummaryRef ref) async {
  // Compose multiple providers
  final gameState = ref.watch(gameStateProvider);
  final cards = await ref.watch(cardCollectionProvider.future);
  final relationships = await ref.watch(relationshipsProvider.future);
  
  return GameSummary(
    currentWeek: gameState.currentWeek,
    cardsCollected: cards.length,
    friendships: relationships.where((r) => r.trust > 50).length,
  );
}
```

### 4. Async Initialization Pattern

```dart
// Ensure services are initialized before app starts
@riverpod
Future<void> appInitialization(AppInitializationRef ref) async {
  // Initialize in sequence
  await ref.watch(hiveInitializationProvider.future);
  await ref.watch(firebaseInitializationProvider.future);
  await ref.watch(audioServiceProvider.future);
  
  AppLogger.info('App initialization complete');
}

// In main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  final container = ProviderContainer();
  await container.read(appInitializationProvider.future);
  
  runApp(
    UnrestrictedProviderScope(
      container: container,
      child: const UnwrittenApp(),
    ),
  );
}
```

---

## Testing with Riverpod

### Unit Testing Use Cases

```dart
void main() {
  test('PlayCardUseCase reduces resources correctly', () async {
    // Create mock repository
    final mockRepository = MockGameStateRepository();
    when(() => mockRepository.getCurrentState()).thenAnswer(
      (_) async => GameStateEntity(resources: ResourcesEntity(energy: 3)),
    );
    
    // Create use case with mock
    final useCase = PlayCardUseCase(mockRepository);
    
    // Test
    final card = CardEntity(costs: {'energy': 2});
    await useCase.execute(card);
    
    // Verify
    verify(() => mockRepository.updateState(any(
      that: predicate<GameStateEntity>(
        (state) => state.resources.energy == 1,
      ),
    ))).called(1);
  });
}
```

### Widget Testing with Providers

```dart
void main() {
  testWidgets('Card displays correctly', (tester) async {
    // Create test provider scope with overrides
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          cardByIdProvider('test').overrideWith((ref, id) async {
            return CardEntity(
              id: 'test',
              title: 'Test Card',
              costs: {'energy': 2},
            );
          }),
        ],
        child: MaterialApp(
          home: CardDetailScreen(cardId: 'test'),
        ),
      ),
    );
    
    await tester.pumpAndSettle();
    
    expect(find.text('Test Card'), findsOneWidget);
    expect(find.text('Energy: 2'), findsOneWidget);
  });
}
```

### Integration Testing

```dart
void main() {
  testWidgets('Playing card updates game state', (tester) async {
    final container = ProviderContainer(
      overrides: [
        // Use real implementations but with test data
        cardLocalDataSourceProvider.overrideWith((ref) {
          return CardLocalDataSource(testHiveBox);
        }),
      ],
    );
    
    await tester.pumpWidget(
      UnrestrictedProviderScope(
        container: container,
        child: const MaterialApp(home: GameBoardScreen()),
      ),
    );
    
    // Interact with UI
    await tester.tap(find.byType(CardComponent).first);
    await tester.pumpAndSettle();
    
    // Verify state changed
    final gameState = container.read(gameStateProvider);
    expect(gameState.hand.length, 6);  // Card removed from hand
  });
}
```

---

## Best Practices

### ✅ DO

1. **Use code generation**
   ```dart
   @riverpod  // ← Always use this
   MyService myService(MyServiceRef ref) {
     return MyService();
   }
   ```

2. **Keep providers pure**
   ```dart
   @riverpod
   CardRepository cardRepository(CardRepositoryRef ref) {
     return CardRepositoryImpl(ref.watch(dataSourceProvider));
     // No side effects, no async operations here!
   }
   ```

3. **Use `.select()` for performance**
   ```dart
   final energy = ref.watch(
     gameStateProvider.select((s) => s.resources.energy),
   );
   ```

4. **Dispose resources**
   ```dart
   @riverpod
   class MyNotifier extends _$MyNotifier {
     StreamSubscription? _subscription;
     
     @override
     void dispose() {
       _subscription?.cancel();
       super.dispose();
     }
   }
   ```

5. **Test with overrides**
   ```dart
   ProviderScope(
     overrides: [
       myProvider.overrideWithValue(mockValue),
     ],
     child: MyWidget(),
   );
   ```

### ❌ DON'T

1. **Don't use BuildContext in providers**
   ```dart
   @riverpod
   MyService myService(MyServiceRef ref) {
     // ❌ No context here!
     return MyService();
   }
   ```

2. **Don't mutate state directly**
   ```dart
   class GameState extends _$GameState {
     void badUpdate() {
       state.turn = 5;  // ❌ Don't mutate directly!
       state = state.copyWith(turn: 5);  // ✅ Use copyWith
     }
   }
   ```

3. **Don't create circular dependencies**
   ```dart
   @riverpod
   A a(ARef ref) => A(ref.watch(bProvider));  // Depends on B
   
   @riverpod
   B b(BRef ref) => B(ref.watch(aProvider));  // Depends on A
   // ❌ Circular dependency!
   ```

4. **Don't forget to run code generation**
   ```bash
   # Always run after adding/modifying @riverpod providers
   flutter pub run build_runner build --delete-conflicting-outputs
   ```

---

## Resources

### Related Documentation
- [Clean Architecture Layers](./02-clean-architecture-layers.md)
- [Feature Organization](./03-feature-organization.md)
- [Riverpod Setup](../03-state-management/01-riverpod-setup.md)
- [Flame-Riverpod Integration](../02-flame-engine/10-flame-riverpod-integration.md)

### Official Documentation
- [Riverpod](https://riverpod.dev/)
- [Riverpod Generator](https://pub.dev/packages/riverpod_generator)
- [Testing with Riverpod](https://riverpod.dev/docs/essentials/testing)

---

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Master Spec Reference:** `docs/master_flutter_flame_spec_v_1_0.md`

