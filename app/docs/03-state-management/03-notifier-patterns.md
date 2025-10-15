# StateNotifier Patterns

**Status:** ✅ Implemented  
**Package:** `riverpod ^2.6.1` with code generation  
**Purpose:** Advanced state management patterns for complex game logic

---

## Overview

StateNotifiers are Riverpod's solution for managing mutable state that changes over time. This document covers advanced patterns, best practices, and common use cases in Unwritten's game architecture.

## When to Use StateNotifier vs. AsyncNotifier

### Use StateNotifier When:
- ✅ State is synchronous (changes immediately)
- ✅ State has simple dependencies
- ✅ No async initialization required
- ✅ Examples: UI state, simple counters, toggles

### Use AsyncNotifier When:
- ✅ State requires async initialization (loading from DB)
- ✅ State depends on async operations
- ✅ Need to handle loading/error states
- ✅ Examples: User data, game saves, API responses

---

## Basic StateNotifier Pattern

### Simple Counter Example

```dart
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;  // Initial state
  
  void increment() => state++;
  void decrement() => state--;
  void reset() => state = 0;
}

// Usage
final count = ref.watch(counterProvider);
ref.read(counterProvider.notifier).increment();
```

### Game Turn Counter

```dart
@riverpod
class TurnCounter extends _$TurnCounter {
  @override
  int build() {
    // Initialize from game state
    return ref.watch(
      gameStateProvider.select((state) => state.currentTurn),
    );
  }
  
  void advance() {
    state++;
    _saveTurn();
  }
  
  void _saveTurn() {
    final gameState = ref.read(gameStateProvider);
    ref.read(gameStateProvider.notifier).state = 
        gameState.copyWith(currentTurn: state);
  }
}
```

---

## Complex State Management

### Entity State Pattern

```dart
// State class
@freezed
class CardCollectionState with _$CardCollectionState {
  const factory CardCollectionState({
    required List<CardEntity> cards,
    required bool isLoading,
    String? error,
    @Default('') String searchQuery,
    @Default(CardFilter.all) CardFilter currentFilter,
    @Default(CardSort.nameAsc) CardSort currentSort,
  }) = _CardCollectionState;
  
  factory CardCollectionState.initial() => const CardCollectionState(
    cards: [],
    isLoading: true,
  );
}

// StateNotifier
@riverpod
class CardCollection extends _$CardCollection {
  @override
  CardCollectionState build() {
    _loadCards();
    return CardCollectionState.initial();
  }
  
  Future<void> _loadCards() async {
    state = state.copyWith(isLoading: true, error: null);
    
    try {
      final repository = ref.read(cardRepositoryProvider);
      final cards = await repository.getAllCards();
      
      state = state.copyWith(
        cards: cards,
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }
  
  // ===================
  // Search & Filter
  // ===================
  
  void search(String query) {
    state = state.copyWith(searchQuery: query);
  }
  
  void setFilter(CardFilter filter) {
    state = state.copyWith(currentFilter: filter);
  }
  
  void setSort(CardSort sort) {
    state = state.copyWith(currentSort: sort);
  }
  
  // ===================
  // Computed Lists
  // ===================
  
  List<CardEntity> get filteredCards {
    var cards = state.cards;
    
    // Apply search
    if (state.searchQuery.isNotEmpty) {
      cards = cards.where((card) {
        return card.title.toLowerCase().contains(
          state.searchQuery.toLowerCase(),
        );
      }).toList();
    }
    
    // Apply filter
    switch (state.currentFilter) {
      case CardFilter.all:
        break;
      case CardFilter.owned:
        cards = cards.where((c) => c.isOwned).toList();
        break;
      case CardFilter.unowned:
        cards = cards.where((c) => !c.isOwned).toList();
        break;
      case CardFilter.activity:
        cards = cards.where((c) => c.type == CardType.activity).toList();
        break;
      case CardFilter.relationship:
        cards = cards.where((c) => c.type == CardType.relationship).toList();
        break;
    }
    
    // Apply sort
    switch (state.currentSort) {
      case CardSort.nameAsc:
        cards.sort((a, b) => a.title.compareTo(b.title));
        break;
      case CardSort.nameDesc:
        cards.sort((a, b) => b.title.compareTo(a.title));
        break;
      case CardSort.rarityAsc:
        cards.sort((a, b) => a.rarity.index.compareTo(b.rarity.index));
        break;
      case CardSort.rarityDesc:
        cards.sort((a, b) => b.rarity.index.compareTo(a.rarity.index));
        break;
    }
    
    return cards;
  }
}

// Usage with derived state
final filteredCards = ref.watch(
  cardCollectionProvider.select((state) => state.filteredCards),
);
```

---

## Async State Patterns

### AsyncNotifier with Error Handling

```dart
@riverpod
class UserProfile extends _$UserProfile {
  @override
  Future<UserEntity> build() async {
    return await _loadProfile();
  }
  
  Future<UserEntity> _loadProfile() async {
    final repository = ref.watch(userRepositoryProvider);
    
    try {
      return await repository.getCurrentUser();
    } catch (e, stack) {
      AppLogger.error('Failed to load user profile', e, stack);
      throw ProfileLoadException('Could not load profile');
    }
  }
  
  // ===================
  // Update Methods
  // ===================
  
  Future<void> updateName(String newName) async {
    // Optimistic update
    final current = state.value;
    if (current != null) {
      state = AsyncValue.data(current.copyWith(name: newName));
    }
    
    try {
      final repository = ref.read(userRepositoryProvider);
      await repository.updateName(newName);
    } catch (e, stack) {
      // Rollback on error
      state = AsyncValue.error(e, stack);
      await refresh();  // Reload from server
    }
  }
  
  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() => _loadProfile());
  }
}

// Usage in widget
final profileAsync = ref.watch(userProfileProvider);
return profileAsync.when(
  data: (profile) => Text(profile.name),
  loading: () => CircularProgressIndicator(),
  error: (error, stack) => ErrorWidget(error),
);
```

### AsyncNotifier with Refresh Control

```dart
@riverpod
class GameLeaderboard extends _$GameLeaderboard {
  @override
  Future<List<LeaderboardEntry>> build() async {
    // Auto-refresh every 5 minutes
    ref.cacheFor(const Duration(minutes: 5));
    return await _fetchLeaderboard();
  }
  
  Future<List<LeaderboardEntry>> _fetchLeaderboard() async {
    final repository = ref.watch(leaderboardRepositoryProvider);
    return await repository.getTopPlayers(limit: 100);
  }
  
  Future<void> forceRefresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() => _fetchLeaderboard());
  }
}

// Extension for cache control
extension CacheForExtension on Ref {
  void cacheFor(Duration duration) {
    final link = keepAlive();
    Timer(duration, () => link.close());
  }
}
```

---

## Multi-State Coordination

### Coordinating Multiple Notifiers

```dart
@riverpod
class GameSession extends _$GameSession {
  @override
  GameSessionState build() => GameSessionState.initial();
  
  Future<void> startNewGame() async {
    state = state.copyWith(isInitializing: true);
    
    try {
      // Initialize game state
      await ref.read(gameStateProvider.notifier).newGame();
      
      // Reset card hand
      await ref.read(cardHandProvider.notifier).drawInitialHand();
      
      // Reset relationships
      await ref.read(relationshipsProvider.notifier).resetAll();
      
      // Reset life meters
      ref.read(lifeMetersProvider.notifier).resetToDefault();
      
      state = state.copyWith(
        isInitializing: false,
        isActive: true,
      );
      
      AppLogger.info('New game started');
    } catch (e, stack) {
      AppLogger.error('Failed to start game', e, stack);
      state = state.copyWith(
        isInitializing: false,
        error: e.toString(),
      );
    }
  }
  
  Future<void> endGame() async {
    // Save final state
    await ref.read(gameStateProvider.notifier).saveGame();
    
    // Show game over screen
    state = state.copyWith(isActive: false, isGameOver: true);
  }
}
```

### Event-Based Coordination

```dart
// Event bus pattern
@riverpod
EventBus eventBus(EventBusRef ref) => EventBus();

// Listener pattern
@riverpod
class TurnEventListener extends _$TurnEventListener {
  @override
  void build() {
    ref.listen(
      eventBusProvider,
      (previous, eventBus) {
        eventBus.on<TurnAdvancedEvent>().listen(_onTurnAdvanced);
      },
    );
  }
  
  void _onTurnAdvanced(TurnAdvancedEvent event) {
    // Apply turn-based decay
    ref.read(lifeMetersProvider.notifier).applyTurnDecay();
    ref.read(relationshipsProvider.notifier).applyTurnDecay();
    
    // Check win/loss conditions
    _checkGameConditions();
  }
  
  void _checkGameConditions() {
    final lifeMeters = ref.read(lifeMetersProvider);
    
    if (lifeMeters.lowestMeter < 10) {
      // Game over
      ref.read(gameSessionProvider.notifier).endGame();
    }
  }
}
```

---

## Performance Patterns

### Debounced Updates

```dart
@riverpod
class SearchQuery extends _$SearchQuery {
  Timer? _debounceTimer;
  
  @override
  String build() => '';
  
  void update(String query) {
    // Cancel previous timer
    _debounceTimer?.cancel();
    
    // Update local state immediately (for UI)
    state = query;
    
    // Debounce the actual search
    _debounceTimer = Timer(const Duration(milliseconds: 300), () {
      _performSearch(query);
    });
  }
  
  void _performSearch(String query) {
    ref.read(cardCollectionProvider.notifier).search(query);
  }
  
  @override
  void dispose() {
    _debounceTimer?.cancel();
    super.dispose();
  }
}
```

### Batch Updates

```dart
@riverpod
class BatchResourceUpdate extends _$BatchResourceUpdate {
  final List<ResourceChange> _pendingChanges = [];
  Timer? _batchTimer;
  
  @override
  void build() {
    // Nothing to initialize
  }
  
  void queueChange(ResourceChange change) {
    _pendingChanges.add(change);
    
    // Start batch timer if not already running
    _batchTimer ??= Timer(const Duration(milliseconds: 100), _applyBatch);
  }
  
  void _applyBatch() {
    if (_pendingChanges.isEmpty) return;
    
    // Aggregate all changes
    final aggregated = <String, double>{};
    for (final change in _pendingChanges) {
      aggregated[change.resourceType] = 
          (aggregated[change.resourceType] ?? 0) + change.amount;
    }
    
    // Apply once
    for (final entry in aggregated.entries) {
      ref.read(resourcesProvider.notifier).modify(
        entry.key,
        entry.value,
      );
    }
    
    _pendingChanges.clear();
    _batchTimer = null;
  }
}
```

### Memoized Computations

```dart
@riverpod
class ExpensiveCalculation extends _$ExpensiveCalculation {
  final _cache = <String, double>{};
  
  @override
  void build() {}
  
  double calculate(String input) {
    // Check cache first
    if (_cache.containsKey(input)) {
      return _cache[input]!;
    }
    
    // Expensive calculation
    final result = _performExpensiveCalculation(input);
    
    // Cache result
    _cache[input] = result;
    
    // Limit cache size
    if (_cache.length > 100) {
      _cache.remove(_cache.keys.first);
    }
    
    return result;
  }
  
  double _performExpensiveCalculation(String input) {
    // Simulate expensive operation
    return input.codeUnits.fold(0.0, (sum, code) => sum + code / 1000);
  }
}
```

---

## Undo/Redo Pattern

### History-Based State Management

```dart
@riverpod
class UndoableGameState extends _$UndoableGameState {
  final List<GameStateEntity> _history = [];
  int _currentIndex = -1;
  
  @override
  GameStateEntity build() {
    final initial = GameStateEntity.initial();
    _history.add(initial);
    _currentIndex = 0;
    return initial;
  }
  
  void updateState(GameStateEntity newState) {
    // Remove any "future" history
    _history.removeRange(_currentIndex + 1, _history.length);
    
    // Add new state
    _history.add(newState);
    _currentIndex++;
    
    // Limit history size
    if (_history.length > 50) {
      _history.removeAt(0);
      _currentIndex--;
    }
    
    state = newState;
  }
  
  bool get canUndo => _currentIndex > 0;
  bool get canRedo => _currentIndex < _history.length - 1;
  
  void undo() {
    if (!canUndo) return;
    _currentIndex--;
    state = _history[_currentIndex];
  }
  
  void redo() {
    if (!canRedo) return;
    _currentIndex++;
    state = _history[_currentIndex];
  }
}
```

---

## Testing Patterns

### Testing StateNotifiers

```dart
void main() {
  group('CardCollection StateNotifier', () {
    late ProviderContainer container;
    late MockCardRepository mockRepository;
    
    setUp(() {
      mockRepository = MockCardRepository();
      
      container = ProviderContainer(
        overrides: [
          cardRepositoryProvider.overrideWithValue(mockRepository),
        ],
      );
    });
    
    tearDown(() {
      container.dispose();
    });
    
    test('loads cards on initialization', () async {
      // Arrange
      final testCards = [
        CardEntity(id: '1', title: 'Test Card'),
      ];
      when(() => mockRepository.getAllCards())
          .thenAnswer((_) async => testCards);
      
      // Act
      final notifier = container.read(cardCollectionProvider.notifier);
      await container.read(cardCollectionProvider.future);
      
      // Assert
      final state = container.read(cardCollectionProvider).value!;
      expect(state.cards, testCards);
      expect(state.isLoading, false);
    });
    
    test('search filters cards correctly', () async {
      // Arrange
      final testCards = [
        CardEntity(id: '1', title: 'Study at Library'),
        CardEntity(id: '2', title: 'Coffee with Friend'),
      ];
      when(() => mockRepository.getAllCards())
          .thenAnswer((_) async => testCards);
      
      await container.read(cardCollectionProvider.future);
      
      // Act
      container.read(cardCollectionProvider.notifier).search('Study');
      
      // Assert
      final filtered = container.read(
        cardCollectionProvider.select((state) => state.filteredCards),
      );
      expect(filtered.length, 1);
      expect(filtered.first.title, 'Study at Library');
    });
  });
}
```

### Testing Async State

```dart
test('optimistic update with rollback', () async {
  // Arrange
  final initialProfile = UserEntity(id: '1', name: 'Alice');
  when(() => mockRepository.getCurrentUser())
      .thenAnswer((_) async => initialProfile);
  
  await container.read(userProfileProvider.future);
  
  // Mock update failure
  when(() => mockRepository.updateName(any()))
      .thenThrow(Exception('Network error'));
  
  // Act
  final notifier = container.read(userProfileProvider.notifier);
  try {
    await notifier.updateName('Bob');
  } catch (_) {}
  
  // Wait for rollback
  await container.read(userProfileProvider.future);
  
  // Assert - name should be rolled back
  final profile = container.read(userProfileProvider).value!;
  expect(profile.name, 'Alice');
});
```

---

## Common Pitfalls

### ❌ DON'T: Mutate State Directly

```dart
// ❌ BAD
void addCard(CardEntity card) {
  state.cards.add(card);  // Mutating state directly!
}

// ✅ GOOD
void addCard(CardEntity card) {
  state = state.copyWith(
    cards: [...state.cards, card],
  );
}
```

### ❌ DON'T: Create Circular Dependencies

```dart
// ❌ BAD
@riverpod
class A extends _$A {
  @override
  void build() {
    ref.watch(bProvider);  // A depends on B
  }
}

@riverpod
class B extends _$B {
  @override
  void build() {
    ref.watch(aProvider);  // B depends on A - CIRCULAR!
  }
}
```

### ❌ DON'T: Forget to Dispose

```dart
// ❌ BAD
@riverpod
class MyNotifier extends _$MyNotifier {
  final StreamController _controller = StreamController();
  
  // No dispose method - memory leak!
}

// ✅ GOOD
@riverpod
class MyNotifier extends _$MyNotifier {
  final StreamController _controller = StreamController();
  
  @override
  void dispose() {
    _controller.close();
    super.dispose();
  }
}
```

### ❌ DON'T: Block the UI Thread

```dart
// ❌ BAD
void processLargeData() {
  final result = _expensiveSync Computation();  // Blocks UI!
  state = result;
}

// ✅ GOOD
Future<void> processLargeData() async {
  final result = await compute(_expensiveComputation, data);
  state = result;
}
```

---

## Advanced Patterns

### State Machine Pattern

```dart
enum GamePhase {
  loading,
  menu,
  playing,
  paused,
  gameOver,
}

@riverpod
class GamePhaseManager extends _$GamePhaseManager {
  @override
  GamePhase build() => GamePhase.loading;
  
  void transition(GamePhase newPhase) {
    // Validate transitions
    if (!_canTransition(state, newPhase)) {
      AppLogger.error('Invalid phase transition: $state -> $newPhase');
      return;
    }
    
    // Exit current phase
    _onExitPhase(state);
    
    // Enter new phase
    state = newPhase;
    _onEnterPhase(newPhase);
  }
  
  bool _canTransition(GamePhase from, GamePhase to) {
    switch (from) {
      case GamePhase.loading:
        return to == GamePhase.menu;
      case GamePhase.menu:
        return to == GamePhase.playing;
      case GamePhase.playing:
        return to == GamePhase.paused || to == GamePhase.gameOver;
      case GamePhase.paused:
        return to == GamePhase.playing || to == GamePhase.menu;
      case GamePhase.gameOver:
        return to == GamePhase.menu;
    }
  }
  
  void _onExitPhase(GamePhase phase) {
    switch (phase) {
      case GamePhase.playing:
        ref.read(gameStateProvider.notifier).saveGame();
        break;
      // ... other cleanup
    }
  }
  
  void _onEnterPhase(GamePhase phase) {
    switch (phase) {
      case GamePhase.playing:
        ref.read(gameStateProvider.notifier).resumeGame();
        break;
      // ... other setup
    }
  }
}
```

---

## Resources

### Related Documentation
- [Riverpod Setup](./01-riverpod-setup.md)
- [Game State Providers](./02-game-state-providers.md)
- [Dependency Injection](../01-architecture/04-dependency-injection.md)

### Official Documentation
- [Riverpod StateNotifier](https://riverpod.dev/docs/concepts/providers#statenotifierprovider)
- [Riverpod AsyncNotifier](https://riverpod.dev/docs/providers/notifier_provider#asyncnotifierprovider)
- [Testing with Riverpod](https://riverpod.dev/docs/essentials/testing)

---

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Master Spec Reference:** `docs/master_flutter_flame_spec_v_1_0.md`

