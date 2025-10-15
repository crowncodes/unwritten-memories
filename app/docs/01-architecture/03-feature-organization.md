# Feature Organization

**Status:** ✅ Implemented  
**Flame Integration:** Complete  
**Pattern:** Feature-Based Modules

---

## Overview

Unwritten organizes code by **feature** rather than by layer or file type. Each feature is a self-contained module with its own data, domain, and presentation layers. This makes the codebase scalable, testable, and easy to navigate.

## Feature-Based vs. Layer-Based

### ❌ Layer-Based (Old Approach)

```
lib/
├── models/
│   ├── card_model.dart
│   ├── game_state_model.dart
│   ├── relationship_model.dart
│   └── resource_model.dart
├── repositories/
│   ├── card_repository.dart
│   ├── game_state_repository.dart
│   └── relationship_repository.dart
├── screens/
│   ├── game_board_screen.dart
│   ├── card_collection_screen.dart
│   └── relationship_screen.dart
└── widgets/
    ├── card_widget.dart
    ├── resource_widget.dart
    └── relationship_widget.dart
```

**Problems:**
- 🔴 Hard to find related files
- 🔴 Features spread across multiple folders
- 🔴 Difficult to delete/refactor features
- 🔴 Tight coupling between unrelated features

### ✅ Feature-Based (Unwritten Approach)

```
lib/
├── features/
│   ├── cards/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   ├── game/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   └── relationships/
│       ├── data/
│       ├── domain/
│       └── presentation/
├── core/          # Shared utilities
└── shared/        # Shared widgets/services
```

**Benefits:**
- ✅ All feature code in one place
- ✅ Easy to navigate and understand
- ✅ Independent, loosely coupled features
- ✅ Easy to delete/refactor entire features

---

## Feature Structure Template

Every feature follows this structure:

```
features/feature_name/
├── data/
│   ├── models/
│   │   └── feature_model.dart          # DTOs with serialization
│   ├── repositories/
│   │   └── feature_repository_impl.dart # Repository implementation
│   └── datasources/
│       ├── feature_local_datasource.dart   # Local storage
│       └── feature_remote_datasource.dart  # API/Firebase
│
├── domain/
│   ├── entities/
│   │   └── feature_entity.dart         # Core business objects
│   ├── repositories/
│   │   └── feature_repository.dart     # Repository interface
│   └── usecases/
│       ├── get_feature_data.dart       # Use case 1
│       └── update_feature.dart         # Use case 2
│
└── presentation/
    ├── screens/
    │   └── feature_screen.dart         # Flutter screen
    ├── widgets/
    │   └── feature_widget.dart         # Flutter widgets
    ├── components/
    │   └── feature_component.dart      # Flame components
    └── providers/
        └── feature_provider.dart       # Riverpod state
```

---

## Unwritten Features

### 1. Cards Feature

**Purpose:** Card management, collection, evolution, and gameplay

```
features/cards/
├── data/
│   ├── models/
│   │   ├── card_model.dart
│   │   ├── card_model.g.dart         # Generated
│   │   └── card_effect_model.dart
│   ├── repositories/
│   │   └── card_repository_impl.dart
│   └── datasources/
│       ├── card_local_datasource.dart    # Hive storage
│       └── card_remote_datasource.dart   # Firebase (future)
│
├── domain/
│   ├── entities/
│   │   ├── card_entity.dart
│   │   ├── card_type.dart
│   │   ├── card_effect.dart
│   │   └── card_rarity.dart
│   ├── repositories/
│   │   └── card_repository.dart
│   └── usecases/
│       ├── get_available_cards.dart
│       ├── get_card_by_id.dart
│       ├── play_card.dart
│       ├── evolve_card.dart
│       └── unlock_card.dart
│
└── presentation/
    ├── screens/
    │   ├── card_collection_screen.dart
    │   └── card_detail_screen.dart
    ├── widgets/
    │   ├── card_tile_widget.dart
    │   ├── card_grid_widget.dart
    │   └── card_filter_widget.dart
    ├── components/                    # Flame components
    │   ├── card_component.dart
    │   ├── card_hand_component.dart
    │   ├── card_play_effect.dart
    │   └── card_draw_animation.dart
    └── providers/
        ├── card_collection_provider.dart
        ├── card_hand_provider.dart
        └── card_state_provider.dart
```

**Key Use Cases:**
- Get available cards
- Play card (check resources, apply effects)
- Evolve card (combine/upgrade)
- Unlock new cards

---

### 2. Game Feature

**Purpose:** Core game loop, turn management, state persistence

```
features/game/
├── data/
│   ├── models/
│   │   ├── game_state_model.dart
│   │   ├── resources_model.dart
│   │   └── timeline_model.dart
│   ├── repositories/
│   │   └── game_state_repository_impl.dart
│   └── datasources/
│       └── game_state_local_datasource.dart
│
├── domain/
│   ├── entities/
│   │   ├── game_state_entity.dart
│   │   ├── resources_entity.dart
│   │   ├── timeline_entity.dart
│   │   └── phase.dart
│   ├── repositories/
│   │   └── game_state_repository.dart
│   └── usecases/
│       ├── initialize_game.dart
│       ├── advance_turn.dart
│       ├── advance_phase.dart
│       ├── save_game.dart
│       └── load_game.dart
│
└── presentation/
    ├── screens/
    │   ├── game_board_screen.dart
    │   └── main_menu_screen.dart
    ├── widgets/
    │   ├── clusters/                  # UI overlays
    │   │   ├── resource_cluster.dart
    │   │   ├── timeline_cluster.dart
    │   │   └── life_meters_cluster.dart
    │   └── phase_selector_widget.dart
    ├── components/                    # Flame game world
    │   ├── unwritten_game_world.dart
    │   ├── background_component.dart
    │   ├── drop_zone_component.dart
    │   └── turn_indicator_component.dart
    └── providers/
        ├── game_state_provider.dart
        ├── resources_provider.dart
        └── turn_provider.dart
```

**Key Use Cases:**
- Initialize new game
- Advance turn/phase
- Save/load game state
- Calculate resource changes

---

### 3. Relationships Feature

**Purpose:** NPC relationships, trust, dialogue

```
features/relationships/
├── data/
│   ├── models/
│   │   ├── relationship_model.dart
│   │   └── npc_model.dart
│   ├── repositories/
│   │   └── relationship_repository_impl.dart
│   └── datasources/
│       └── relationship_local_datasource.dart
│
├── domain/
│   ├── entities/
│   │   ├── relationship_entity.dart
│   │   ├── npc_entity.dart
│   │   └── trust_level.dart
│   ├── repositories/
│   │   └── relationship_repository.dart
│   └── usecases/
│       ├── get_relationships.dart
│       ├── update_relationship.dart
│       ├── trigger_dialogue.dart
│       └── check_trust_threshold.dart
│
└── presentation/
    ├── screens/
    │   └── relationships_screen.dart
    ├── widgets/
    │   ├── relationship_tile.dart
    │   └── trust_meter.dart
    ├── components/
    │   ├── npc_component.dart
    │   └── dialogue_bubble_component.dart
    └── providers/
        └── relationships_provider.dart
```

---

### 4. AI Feature

**Purpose:** On-device AI inference for personality, sentiment, and dialogue

```
features/ai/
├── data/
│   ├── models/
│   │   ├── personality_traits_model.dart
│   │   └── sentiment_score_model.dart
│   ├── repositories/
│   │   └── ai_repository_impl.dart
│   └── datasources/
│       ├── ai_local_datasource.dart      # TFLite models
│       └── ai_cache_datasource.dart      # Inference cache
│
├── domain/
│   ├── entities/
│   │   ├── personality_traits_entity.dart
│   │   ├── sentiment_score_entity.dart
│   │   └── ai_response_entity.dart
│   ├── repositories/
│   │   └── ai_repository.dart
│   └── usecases/
│       ├── predict_personality.dart
│       ├── analyze_sentiment.dart
│       └── generate_dialogue.dart
│
└── presentation/
    └── providers/
        ├── personality_provider.dart
        └── ai_inference_provider.dart
```

---

### 5. Music Feature

**Purpose:** Adaptive background music, emotional scoring

```
features/music/
├── data/
│   ├── models/
│   │   ├── music_track_model.dart
│   │   └── emotional_state_model.dart
│   └── repositories/
│       └── music_repository_impl.dart
│
├── domain/
│   ├── entities/
│   │   ├── music_track_entity.dart
│   │   └── emotional_state_entity.dart
│   ├── repositories/
│   │   └── music_repository.dart
│   └── usecases/
│       ├── select_adaptive_track.dart
│       └── blend_tracks.dart
│
└── presentation/
    └── services/
        └── music_engine_service.dart
```

---

## Shared Code

### Core (Framework-Level Utilities)

```
core/
├── constants/
│   ├── app_constants.dart
│   ├── game_constants.dart
│   └── responsive_breakpoints.dart
├── errors/
│   ├── exceptions.dart
│   └── failures.dart
├── utils/
│   ├── logger.dart
│   ├── result.dart
│   └── validators.dart
└── performance/
    ├── performance_monitor.dart
    └── memory_tracker.dart
```

**Rules for `core/`:**
- ✅ Framework-level, reusable across ALL features
- ✅ No feature-specific code
- ✅ Pure Dart utilities
- ❌ No UI components
- ❌ No business logic

---

### Shared (Reusable UI & Services)

```
shared/
├── widgets/
│   ├── custom_button.dart
│   ├── loading_overlay.dart
│   └── error_dialog.dart
├── services/
│   ├── firebase_service.dart
│   ├── audio_service.dart
│   └── analytics_service.dart
└── theme/
    ├── app_theme.dart
    └── colors.dart
```

**Rules for `shared/`:**
- ✅ Reusable UI components used by multiple features
- ✅ Global services (Firebase, Analytics)
- ✅ Theme and styling
- ❌ Feature-specific widgets (those go in the feature)

---

## Feature Communication

Features should be **loosely coupled**. They communicate through:

### 1. Domain Events

```dart
// In game feature
class TurnAdvancedEvent {
  final int newTurn;
  final DateTime timestamp;
  
  TurnAdvancedEvent(this.newTurn, this.timestamp);
}

// Event bus
final eventBusProvider = Provider((ref) => EventBus());

// Publish event
ref.read(eventBusProvider).fire(TurnAdvancedEvent(5, DateTime.now()));

// Subscribe from relationships feature
ref.listen(turnAdvancedEventProvider, (_, event) {
  // Update relationship decay
});
```

### 2. Shared Providers

```dart
// Game state is shared across features
@riverpod
class GameState extends _$GameState {
  @override
  GameStateEntity build() => GameStateEntity.initial();
  
  void advanceTurn() {
    state = state.copyWith(turn: state.turn + 1);
  }
}

// Cards feature can watch game state
final canPlayCard = ref.watch(
  gameStateProvider.select((state) => state.resources.energy >= 2),
);
```

### 3. Use Case Composition

```dart
// High-level use case that coordinates multiple features
class PlayCardAndUpdateRelationshipsUseCase {
  final PlayCardUseCase _playCard;
  final UpdateRelationshipUseCase _updateRelationship;
  
  PlayCardAndUpdateRelationshipsUseCase(
    this._playCard,
    this._updateRelationship,
  );
  
  Future<Result<void>> execute(CardEntity card, NpcEntity npc) async {
    // Play card (cards feature)
    final playResult = await _playCard.execute(card);
    if (playResult.isError) return playResult;
    
    // Update relationship (relationships feature)
    final relationshipImpact = card.getRelationshipImpact(npc);
    await _updateRelationship.execute(npc, relationshipImpact);
    
    return Result.success(null);
  }
}
```

---

## Feature Dependencies

### Dependency Graph

```
┌──────────┐
│   Game   │
│ (Central)│
└────┬─────┘
     │
     ├──────► Cards      (Game depends on Cards)
     ├──────► Relationships
     ├──────► AI
     └──────► Music
```

**Rules:**
- ✅ Central feature (Game) can depend on other features
- ❌ Leaf features (Cards, Relationships) should NOT depend on each other
- ✅ All features can depend on Core and Shared

### Managing Dependencies

```dart
// ✅ GOOD: Game feature uses Cards feature
class GameStateNotifier extends StateNotifier<GameState> {
  final PlayCardUseCase _playCard;  // From cards feature
  
  Future<void> handleCardPlay(CardEntity card) async {
    await _playCard.execute(card);
    _advanceTurn();
  }
}

// ❌ BAD: Cards feature depends on Relationships feature
class CardComponent extends Component {
  void onPlay() {
    // ❌ Don't do this!
    ref.read(relationshipsProvider).updateTrust(npc, card);
  }
}

// ✅ GOOD: Use events or composition at a higher level
class CardComponent extends Component {
  void onPlay() {
    // Emit event, let game feature coordinate
    ref.read(eventBusProvider).fire(CardPlayedEvent(card));
  }
}
```

---

## Creating a New Feature

### Step-by-Step Guide

1. **Create folder structure**
   ```bash
   mkdir -p features/new_feature/{data/{models,repositories,datasources},domain/{entities,repositories,usecases},presentation/{screens,widgets,components,providers}}
   ```

2. **Define domain entities**
   ```dart
   // features/new_feature/domain/entities/new_entity.dart
   class NewEntity {
     final String id;
     final String name;
     
     NewEntity({required this.id, required this.name});
   }
   ```

3. **Create repository interface**
   ```dart
   // features/new_feature/domain/repositories/new_repository.dart
   abstract class NewRepository {
     Future<List<NewEntity>> getAll();
     Future<void> save(NewEntity entity);
   }
   ```

4. **Implement data layer**
   ```dart
   // features/new_feature/data/models/new_model.dart
   class NewModel {
     final String id;
     final String name;
     
     NewEntity toEntity() => NewEntity(id: id, name: name);
     factory NewModel.fromEntity(NewEntity entity) => 
         NewModel(id: entity.id, name: entity.name);
   }
   
   // features/new_feature/data/repositories/new_repository_impl.dart
   class NewRepositoryImpl implements NewRepository {
     final NewLocalDataSource _localDataSource;
     
     NewRepositoryImpl(this._localDataSource);
     
     @override
     Future<List<NewEntity>> getAll() async {
       final models = await _localDataSource.getAll();
       return models.map((m) => m.toEntity()).toList();
     }
   }
   ```

5. **Create use cases**
   ```dart
   // features/new_feature/domain/usecases/get_all_items.dart
   class GetAllItemsUseCase {
     final NewRepository _repository;
     
     GetAllItemsUseCase(this._repository);
     
     Future<Result<List<NewEntity>>> execute() async {
       try {
         final items = await _repository.getAll();
         return Result.success(items);
       } catch (e) {
         return Result.error(Exception('Failed to load items: $e'));
       }
     }
   }
   ```

6. **Set up providers**
   ```dart
   // features/new_feature/presentation/providers/new_provider.dart
   @riverpod
   NewRepository newRepository(NewRepositoryRef ref) {
     return NewRepositoryImpl(
       ref.watch(newLocalDataSourceProvider),
     );
   }
   
   @riverpod
   GetAllItemsUseCase getAllItemsUseCase(GetAllItemsUseCaseRef ref) {
     return GetAllItemsUseCase(
       ref.watch(newRepositoryProvider),
     );
   }
   
   @riverpod
   class NewItems extends _$NewItems {
     @override
     Future<List<NewEntity>> build() async {
       final useCase = ref.read(getAllItemsUseCaseProvider);
       final result = await useCase.execute();
       return result.fold(
         onSuccess: (items) => items,
         onError: (_) => [],
       );
     }
   }
   ```

7. **Create UI**
   ```dart
   // features/new_feature/presentation/screens/new_screen.dart
   class NewScreen extends ConsumerWidget {
     @override
     Widget build(BuildContext context, WidgetRef ref) {
       final items = ref.watch(newItemsProvider);
       
       return items.when(
         data: (data) => ListView.builder(
           itemCount: data.length,
           itemBuilder: (context, index) => ListTile(
             title: Text(data[index].name),
           ),
         ),
         loading: () => CircularProgressIndicator(),
         error: (error, stack) => Text('Error: $error'),
       );
     }
   }
   ```

8. **Add barrel export** (optional)
   ```dart
   // features/new_feature/new_feature.dart
   export 'domain/entities/new_entity.dart';
   export 'domain/repositories/new_repository.dart';
   export 'domain/usecases/get_all_items.dart';
   export 'presentation/providers/new_provider.dart';
   export 'presentation/screens/new_screen.dart';
   ```

---

## Best Practices

### ✅ DO

1. **Keep features independent**
   - Each feature should work in isolation
   - Minimize cross-feature dependencies

2. **Use domain events for coordination**
   - Features communicate via events, not direct calls
   - Loose coupling through event bus

3. **Follow folder structure**
   - Consistent structure makes navigation easy
   - New developers can find code quickly

4. **Test features in isolation**
   - Each feature has its own test folder
   - Integration tests at the app level

5. **Document feature boundaries**
   - Clear README in each feature folder
   - Document public API (exported entities, use cases)

### ❌ DON'T

1. **Don't create circular dependencies**
   - Feature A → Feature B → Feature A (BAD!)
   - Use events or a coordinator pattern

2. **Don't put everything in `shared/`**
   - Only truly reusable components belong there
   - Feature-specific code stays in the feature

3. **Don't bypass layers**
   - Always go through domain layer
   - No direct data access from presentation

4. **Don't create "god features"**
   - Keep features focused on a single responsibility
   - Split large features into sub-features

---

## Resources

### Related Documentation
- [Project Structure](./01-project-structure.md)
- [Clean Architecture Layers](./02-clean-architecture-layers.md)
- [Dependency Injection](./04-dependency-injection.md)

### External Resources
- [Feature-Driven Development](https://en.wikipedia.org/wiki/Feature-driven_development)
- [Package by Feature, not Layer](https://phauer.com/2020/package-by-feature/)

---

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Master Spec Reference:** `docs/master_flutter_flame_spec_v_1_0.md`

