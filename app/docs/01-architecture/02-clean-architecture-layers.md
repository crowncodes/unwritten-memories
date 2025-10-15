# Clean Architecture Layers

**Status:** ✅ Implemented  
**Flame Integration:** Complete  
**Reference:** Master Spec - Architecture Principles

---

## Overview

Unwritten follows **Clean Architecture** with three distinct layers: Data, Domain, and Presentation. This separation ensures testability, maintainability, and independence from external frameworks (including Flame).

## Architecture Layers

```
┌─────────────────────────────────────────────────┐
│         Presentation Layer (UI + Flame)         │
│  ┌─────────────┐  ┌──────────────────────────┐ │
│  │   Flutter   │  │    Flame Components      │ │
│  │   Widgets   │  │  (CardComponent, etc.)   │ │
│  └─────────────┘  └──────────────────────────┘ │
└────────────────────┬────────────────────────────┘
                     │
                     ↓ (depends on)
┌─────────────────────────────────────────────────┐
│              Domain Layer (Logic)                │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │
│  │ Entities │  │ Usecases │  │ Repositories │ │
│  │          │  │          │  │ (Interfaces) │ │
│  └──────────┘  └──────────┘  └──────────────┘ │
└────────────────────┬────────────────────────────┘
                     │
                     ↓ (depends on)
┌─────────────────────────────────────────────────┐
│             Data Layer (External)                │
│  ┌───────────┐  ┌──────────┐  ┌─────────────┐ │
│  │   Models  │  │  Repos   │  │ Datasources │ │
│  │ (DTOs)    │  │  (Impl)  │  │ (API/DB)    │ │
│  └───────────┘  └──────────┘  └─────────────┘ │
└─────────────────────────────────────────────────┘
```

**Key Principle:** Dependency flow is **always inward**. Outer layers depend on inner layers, never the reverse.

---

## Layer Responsibilities

### 1. Presentation Layer

**Purpose:** User interface and user interaction  
**Technologies:** Flutter Widgets + Flame Components  
**Dependencies:** Domain Layer only

**Contains:**
- Flutter screens and widgets
- Flame game components (cards, animations, particles)
- Riverpod providers for state management
- UI state (loading, error, success)
- View models / controllers

**Examples:**
```dart
// Flutter Widget
class GameBoardScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final gameState = ref.watch(gameStateProvider);
    return GameWidget(game: UnwrittenGame(ref: ref));
  }
}

// Flame Component
class CardComponent extends SpriteAnimationGroupComponent 
    with TapCallbacks, DragCallbacks {
  final CardEntity card;  // Domain entity
  
  CardComponent({required this.card});
  
  @override
  void onTapUp(TapUpEvent event) {
    // Call domain use case
    ref.read(playCardUseCaseProvider).execute(card);
  }
}
```

**Rules:**
- ✅ Can use domain entities and use cases
- ✅ Can contain UI-specific logic (animations, gestures)
- ❌ Cannot contain business logic
- ❌ Cannot access data layer directly
- ❌ Cannot import models or repositories

---

### 2. Domain Layer

**Purpose:** Business logic and rules  
**Technologies:** Pure Dart (no Flutter/Flame imports)  
**Dependencies:** None (pure, testable)

**Contains:**
- Entities (core business objects)
- Use cases (business operations)
- Repository interfaces (contracts)
- Domain errors and exceptions
- Business rules and validation

**Examples:**
```dart
// Entity
class CardEntity {
  final String id;
  final String title;
  final CardType type;
  final Map<String, double> costs;
  final List<Effect> effects;
  
  CardEntity({
    required this.id,
    required this.title,
    required this.type,
    required this.costs,
    required this.effects,
  });
  
  // Pure business logic
  bool canPlay(ResourcesEntity resources) {
    return costs.entries.every((cost) {
      final available = resources.getResource(cost.key);
      return available >= cost.value;
    });
  }
}

// Use Case
class PlayCardUseCase {
  final CardRepository _cardRepository;
  final GameStateRepository _gameStateRepository;
  
  PlayCardUseCase(this._cardRepository, this._gameStateRepository);
  
  Future<Result<void>> execute(CardEntity card) async {
    // Business logic
    final gameState = await _gameStateRepository.getCurrentState();
    
    if (!card.canPlay(gameState.resources)) {
      return Result.error(InsufficientResourcesError());
    }
    
    // Apply card effects
    final updatedState = _applyCardEffects(gameState, card);
    await _gameStateRepository.updateState(updatedState);
    
    return Result.success(null);
  }
}

// Repository Interface (contract)
abstract class CardRepository {
  Future<List<CardEntity>> getAvailableCards();
  Future<CardEntity?> getCardById(String id);
  Future<void> addCardToCollection(CardEntity card);
}
```

**Rules:**
- ✅ Pure Dart only (no external dependencies)
- ✅ 100% testable without mocks
- ✅ Contains all business rules
- ❌ No Flutter imports
- ❌ No Flame imports
- ❌ No platform-specific code

---

### 3. Data Layer

**Purpose:** External data access  
**Technologies:** HTTP, Database, Local Storage  
**Dependencies:** Domain Layer interfaces

**Contains:**
- Models (DTOs - Data Transfer Objects)
- Repository implementations
- Data sources (remote API, local DB)
- Mappers (Model ↔ Entity conversion)
- Caching logic

**Examples:**
```dart
// Model (DTO)
@HiveType(typeId: 0)
class CardModel extends HiveObject {
  @HiveField(0)
  final String id;
  
  @HiveField(1)
  final String title;
  
  @HiveField(2)
  final String type;  // Note: String, not enum
  
  @HiveField(3)
  final Map<String, double> costs;
  
  CardModel({
    required this.id,
    required this.title,
    required this.type,
    required this.costs,
  });
  
  // Mapper: Model → Entity
  CardEntity toEntity() {
    return CardEntity(
      id: id,
      title: title,
      type: CardType.values.firstWhere((t) => t.name == type),
      costs: costs,
      effects: [], // Parse from JSON
    );
  }
  
  // Mapper: Entity → Model
  factory CardModel.fromEntity(CardEntity entity) {
    return CardModel(
      id: entity.id,
      title: entity.title,
      type: entity.type.name,
      costs: entity.costs,
    );
  }
}

// Repository Implementation
class CardRepositoryImpl implements CardRepository {
  final CardLocalDataSource _localDataSource;
  final CardRemoteDataSource? _remoteDataSource;
  
  CardRepositoryImpl(this._localDataSource, [this._remoteDataSource]);
  
  @override
  Future<List<CardEntity>> getAvailableCards() async {
    try {
      // Try cache first
      final cachedModels = await _localDataSource.getCachedCards();
      if (cachedModels.isNotEmpty) {
        return cachedModels.map((m) => m.toEntity()).toList();
      }
      
      // Fallback to remote
      if (_remoteDataSource != null) {
        final remoteModels = await _remoteDataSource.fetchCards();
        await _localDataSource.cacheCards(remoteModels);
        return remoteModels.map((m) => m.toEntity()).toList();
      }
      
      return [];
    } catch (e) {
      throw DataException('Failed to load cards: $e');
    }
  }
}

// Data Source
class CardLocalDataSource {
  final Box<CardModel> _box;
  
  CardLocalDataSource(this._box);
  
  Future<List<CardModel>> getCachedCards() async {
    return _box.values.toList();
  }
  
  Future<void> cacheCards(List<CardModel> cards) async {
    for (final card in cards) {
      await _box.put(card.id, card);
    }
  }
}
```

**Rules:**
- ✅ Implements domain repository interfaces
- ✅ Handles external data (API, DB, files)
- ✅ Converts Models ↔ Entities
- ❌ No business logic (just data fetching/saving)
- ❌ No UI code

---

## Unwritten Feature Structure

### Card Feature Example

```
features/cards/
├── data/
│   ├── models/
│   │   └── card_model.dart           # DTO with JSON/Hive serialization
│   ├── repositories/
│   │   └── card_repository_impl.dart # Repository implementation
│   └── datasources/
│       ├── card_local_datasource.dart   # Hive database
│       └── card_remote_datasource.dart  # Firebase API
│
├── domain/
│   ├── entities/
│   │   ├── card_entity.dart          # Pure business object
│   │   └── card_type.dart            # Enums and value objects
│   ├── repositories/
│   │   └── card_repository.dart      # Repository interface
│   └── usecases/
│       ├── get_available_cards.dart  # Fetch cards
│       ├── play_card.dart            # Play card logic
│       └── evolve_card.dart          # Card evolution logic
│
└── presentation/
    ├── screens/
    │   └── card_collection_screen.dart  # Flutter screen
    ├── widgets/
    │   ├── card_tile_widget.dart        # Flutter card display
    │   └── card_detail_widget.dart      # Card detail modal
    ├── components/
    │   ├── card_component.dart          # Flame game card
    │   ├── card_hand_component.dart     # Flame card hand
    │   └── card_play_effect.dart        # Flame particle effect
    └── providers/
        ├── card_state_provider.dart     # Riverpod state
        └── card_collection_provider.dart # Collection state
```

---

## Dependency Injection with Riverpod

### Provider Structure

```dart
// Domain Layer - Use Case Provider
@riverpod
PlayCardUseCase playCardUseCase(PlayCardUseCaseRef ref) {
  return PlayCardUseCase(
    ref.watch(cardRepositoryProvider),
    ref.watch(gameStateRepositoryProvider),
  );
}

// Data Layer - Repository Provider
@riverpod
CardRepository cardRepository(CardRepositoryRef ref) {
  return CardRepositoryImpl(
    ref.watch(cardLocalDataSourceProvider),
    ref.watch(cardRemoteDataSourceProvider),
  );
}

// Data Layer - Data Source Provider
@riverpod
CardLocalDataSource cardLocalDataSource(CardLocalDataSourceRef ref) {
  final box = Hive.box<CardModel>('cards');
  return CardLocalDataSource(box);
}

// Presentation Layer - State Provider
@riverpod
class CardCollectionNotifier extends _$CardCollectionNotifier {
  @override
  Future<List<CardEntity>> build() async {
    final useCase = ref.read(getAvailableCardsUseCaseProvider);
    final result = await useCase.execute();
    return result.fold(
      onSuccess: (cards) => cards,
      onError: (_) => [],
    );
  }
  
  Future<void> playCard(CardEntity card) async {
    final useCase = ref.read(playCardUseCaseProvider);
    await useCase.execute(card);
    ref.invalidateSelf(); // Refresh collection
  }
}
```

---

## Flame Integration

### Connecting Flame to Clean Architecture

```dart
// Flame Component with Clean Architecture
class CardComponent extends SpriteAnimationGroupComponent 
    with TapCallbacks, HasGameRef {
  final CardEntity card;  // Domain entity
  final WidgetRef ref;    // Access to providers
  
  CardComponent({
    required this.card,
    required this.ref,
  });
  
  @override
  Future<void> onLoad() async {
    // Load sprite from entity data
    final spriteSheet = await game.images.load(card.spritePath);
    
    // Create animations from domain data
    animations = {
      CardState.idle: _createIdleAnimation(spriteSheet),
      CardState.hover: _createHoverAnimation(spriteSheet),
      CardState.play: _createPlayAnimation(spriteSheet),
    };
    
    current = CardState.idle;
  }
  
  @override
  void onTapUp(TapUpEvent event) async {
    // Call domain use case
    final playCardUseCase = ref.read(playCardUseCaseProvider);
    final result = await playCardUseCase.execute(card);
    
    result.fold(
      onSuccess: (_) {
        // Play success animation
        current = CardState.play;
        add(CardPlayEffect(card: card));
      },
      onError: (error) {
        // Show error feedback
        add(ErrorShakeEffect());
      },
    );
  }
}

// Game World with Repository Access
class GameWorld extends Component with HasGameRef {
  final WidgetRef ref;
  
  GameWorld({required this.ref});
  
  @override
  Future<void> onLoad() async {
    // Load initial cards from repository
    final cards = await ref.read(cardCollectionNotifierProvider.future);
    
    // Create Flame components from entities
    for (final card in cards) {
      add(CardComponent(card: card, ref: ref));
    }
  }
}
```

---

## Testing Strategy

### Domain Layer (Unit Tests - Fast)

```dart
void main() {
  group('PlayCardUseCase', () {
    late PlayCardUseCase useCase;
    late MockCardRepository cardRepository;
    late MockGameStateRepository gameStateRepository;
    
    setUp(() {
      cardRepository = MockCardRepository();
      gameStateRepository = MockGameStateRepository();
      useCase = PlayCardUseCase(cardRepository, gameStateRepository);
    });
    
    test('Should play card when resources are sufficient', () async {
      // Arrange
      final card = CardEntity(
        id: '1',
        costs: {'energy': 2.0},
        // ...
      );
      final gameState = GameStateEntity(
        resources: ResourcesEntity(energy: 3),
      );
      
      when(() => gameStateRepository.getCurrentState())
          .thenAnswer((_) async => gameState);
      
      // Act
      final result = await useCase.execute(card);
      
      // Assert
      expect(result.isSuccess, true);
      verify(() => gameStateRepository.updateState(any())).called(1);
    });
  });
}
```

### Presentation Layer (Widget Tests)

```dart
void main() {
  testWidgets('CardTile displays card information', (tester) async {
    final card = CardEntity(
      id: '1',
      title: 'Study at Library',
      type: CardType.activity,
      costs: {'energy': 2.0, 'time': 3.0},
    );
    
    await tester.pumpWidget(
      ProviderScope(
        child: MaterialApp(
          home: CardTileWidget(card: card),
        ),
      ),
    );
    
    expect(find.text('Study at Library'), findsOneWidget);
    expect(find.text('Energy: 2'), findsOneWidget);
  });
}
```

### Integration Tests (Flame + Riverpod)

```dart
void main() {
  testWidgets('Playing card updates game state', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        child: MaterialApp(
          home: GameWidget(
            game: UnwrittenGame(),
          ),
        ),
      ),
    );
    
    // Find card component
    final game = tester.widget<GameWidget>(find.byType(GameWidget)).game;
    final cardComponent = game.children.whereType<CardComponent>().first;
    
    // Simulate tap
    cardComponent.onTapUp(TapUpEvent());
    await tester.pumpAndSettle();
    
    // Verify game state updated
    // ...
  });
}
```

---

## Benefits of Clean Architecture

### 1. Testability
- ✅ Domain layer 100% testable without mocks
- ✅ No UI dependencies in business logic
- ✅ Fast unit tests (no Flutter engine)

### 2. Maintainability
- ✅ Changes in one layer don't affect others
- ✅ Easy to swap implementations (e.g., Firebase → local-only)
- ✅ Clear separation of concerns

### 3. Scalability
- ✅ Add new features without touching existing code
- ✅ Multiple UI implementations (Flutter, Flame, web)
- ✅ Parallel development (teams can work independently)

### 4. Flexibility
- ✅ Swap data sources (API → local DB)
- ✅ Change UI frameworks (Flutter → Flame)
- ✅ Platform-specific implementations

---

## Common Patterns

### Result Type

```dart
class Result<T> {
  final T? data;
  final Exception? error;
  
  Result.success(this.data) : error = null;
  Result.error(this.error) : data = null;
  
  bool get isSuccess => error == null;
  bool get isError => error != null;
  
  R fold<R>({
    required R Function(T data) onSuccess,
    required R Function(Exception error) onError,
  }) {
    if (isSuccess) {
      return onSuccess(data as T);
    } else {
      return onError(error!);
    }
  }
}
```

### Either Type (Alternative)

```dart
sealed class Either<L, R> {
  const Either();
}

class Left<L, R> extends Either<L, R> {
  final L value;
  const Left(this.value);
}

class Right<L, R> extends Either<L, R> {
  final R value;
  const Right(this.value);
}

// Usage
Either<Failure, List<CardEntity>> result = await repository.getCards();
```

---

## Anti-Patterns to Avoid

### ❌ DON'T: Skip layers

```dart
// BAD: Widget directly accessing data source
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final box = Hive.box<CardModel>('cards');  // ❌ Wrong layer!
    return ListView(
      children: box.values.map((card) => CardTile(card)).toList(),
    );
  }
}
```

### ❌ DON'T: Put business logic in presentation

```dart
// BAD: Game logic in Flame component
class CardComponent extends Component {
  void play() {
    // ❌ Business logic in presentation!
    if (resources.energy >= card.cost) {
      resources.energy -= card.cost;
      gameState.turn++;
    }
  }
}
```

### ❌ DON'T: Mix models and entities

```dart
// BAD: Using data model in domain layer
class PlayCardUseCase {
  Future<void> execute(CardModel card) async {  // ❌ Should be CardEntity!
    // ...
  }
}
```

### ✅ DO: Follow dependency flow

```dart
// GOOD: Clear layer separation
// Presentation → Domain → Data
class CardComponent extends Component {
  void play() {
    // ✅ Call use case (domain layer)
    ref.read(playCardUseCaseProvider).execute(card.toEntity());
  }
}
```

---

## Resources

### Related Documentation
- [Project Structure](./01-project-structure.md)
- [Feature Organization](./03-feature-organization.md)
- [Dependency Injection](./04-dependency-injection.md)
- [Flame-Riverpod Integration](../02-flame-engine/10-flame-riverpod-integration.md)

### External Resources
- [Clean Architecture (Robert C. Martin)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Flutter Clean Architecture](https://resocoder.com/flutter-clean-architecture-tdd/)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)

---

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Master Spec Reference:** `docs/master_flutter_flame_spec_v_1_0.md` (Architecture Principles)

