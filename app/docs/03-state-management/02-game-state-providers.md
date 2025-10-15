# Game State Providers

**Status:** ✅ Implemented  
**Pattern:** StateNotifier + AsyncNotifier + Riverpod  
**Performance:** 60 FPS maintained

---

## Overview

Unwritten's game state is managed through a hierarchy of Riverpod providers. This document covers all game-related state providers, their relationships, and how they integrate with Flame components.

## State Architecture

```
┌─────────────────────────────────────────────┐
│           Game State Provider                │
│    (Central game state - turn, phase,       │
│     resources, hand, timeline)              │
└──────────────┬──────────────────────────────┘
               │
               ├──► Resources Provider
               ├──► Card Hand Provider
               ├──► Timeline Provider
               ├──► Life Meters Provider
               └──► Relationships Provider
```

---

## Core Game State Provider

### GameStateProvider

**Purpose:** Central source of truth for all game state

```dart
@riverpod
class GameState extends _$GameState {
  @override
  GameStateEntity build() {
    // Load saved game or create new
    _loadSavedGame();
    return GameStateEntity.initial();
  }
  
  Future<void> _loadSavedGame() async {
    final loadUseCase = ref.read(loadGameUseCaseProvider);
    final result = await loadUseCase.execute();
    
    result.fold(
      onSuccess: (savedState) {
        state = savedState;
        AppLogger.info('Game loaded', data: {
          'week': savedState.currentWeek,
          'day': savedState.currentDay,
        });
      },
      onError: (_) {
        state = GameStateEntity.initial();
        AppLogger.info('Starting new game');
      },
    );
  }
  
  // ===================
  // Turn Management
  // ===================
  
  Future<void> advanceTurn() async {
    final advanceTurnUseCase = ref.read(advanceTurnUseCaseProvider);
    final result = await advanceTurnUseCase.execute();
    
    result.fold(
      onSuccess: (newState) {
        state = newState;
        _triggerTurnEffects();
      },
      onError: (error) {
        AppLogger.error('Failed to advance turn', error);
      },
    );
  }
  
  void _triggerTurnEffects() {
    // Emit event for other systems
    ref.read(eventBusProvider).fire(
      TurnAdvancedEvent(state.currentWeek, state.currentDay),
    );
    
    // Resource regeneration
    _regenerateResources();
    
    // Relationship decay
    ref.read(relationshipsProvider.notifier).applyTurnDecay();
  }
  
  // ===================
  // Phase Management
  // ===================
  
  void advancePhase(Phase newPhase) {
    state = state.copyWith(currentPhase: newPhase);
    
    // Phase-specific effects
    switch (newPhase) {
      case Phase.morning:
        _onMorningPhase();
        break;
      case Phase.day:
        _onDayPhase();
        break;
      case Phase.night:
        _onNightPhase();
        break;
    }
  }
  
  void _onMorningPhase() {
    // Restore energy
    state = state.copyWith(
      resources: state.resources.copyWith(energy: 3),
    );
    
    // Draw cards
    ref.read(cardHandProvider.notifier).drawCards(5);
  }
  
  void _onDayPhase() {
    // Day-specific logic
  }
  
  void _onNightPhase() {
    // Auto-save
    _saveGame();
  }
  
  // ===================
  // Resource Management
  // ===================
  
  void _regenerateResources() {
    // Weekly resource reset
    if (state.currentDay == 1) {
      state = state.copyWith(
        resources: state.resources.copyWith(timeThisWeek: 168.0),
      );
    }
  }
  
  void spendResources(Map<String, double> costs) {
    var updatedResources = state.resources;
    
    for (final cost in costs.entries) {
      switch (cost.key) {
        case 'energy':
          updatedResources = updatedResources.copyWith(
            energy: updatedResources.energy - cost.value.toInt(),
          );
          break;
        case 'time':
          updatedResources = updatedResources.copyWith(
            timeThisWeek: updatedResources.timeThisWeek - cost.value,
          );
          break;
        case 'money':
          updatedResources = updatedResources.copyWith(
            money: updatedResources.money - cost.value,
          );
          break;
      }
    }
    
    state = state.copyWith(resources: updatedResources);
  }
  
  // ===================
  // Save/Load
  // ===================
  
  Future<void> _saveGame() async {
    final saveUseCase = ref.read(saveGameUseCaseProvider);
    await saveUseCase.execute(state);
  }
  
  Future<void> saveGameManual() async {
    await _saveGame();
    AppLogger.info('Game saved manually');
  }
}

// Usage in widgets
final gameState = ref.watch(gameStateProvider);
print('Week ${gameState.currentWeek}, Day ${gameState.currentDay}');

// Usage in Flame
final gameState = ref.read(gameStateProvider);
```

---

## Resources Provider

### ResourcesProvider

**Purpose:** Manage player resources (energy, time, money, social capital)

```dart
@riverpod
class Resources extends _$Resources {
  @override
  ResourcesEntity build() {
    // Derived from game state
    return ref.watch(gameStateProvider.select((state) => state.resources));
  }
  
  // ===================
  // Resource Checks
  // ===================
  
  bool canAfford(Map<String, double> costs) {
    final resources = state;
    
    for (final cost in costs.entries) {
      final available = _getResourceValue(cost.key);
      if (available < cost.value) {
        return false;
      }
    }
    
    return true;
  }
  
  double _getResourceValue(String resourceKey) {
    switch (resourceKey) {
      case 'energy':
        return state.energy.toDouble();
      case 'time':
        return state.timeThisWeek;
      case 'money':
        return state.money;
      case 'social':
        return state.socialCapital;
      default:
        return 0;
    }
  }
  
  // ===================
  // Resource Modifications
  // ===================
  
  void spend(Map<String, double> costs) {
    ref.read(gameStateProvider.notifier).spendResources(costs);
  }
  
  void earn(String resourceKey, double amount) {
    var updatedState = state;
    
    switch (resourceKey) {
      case 'money':
        updatedState = updatedState.copyWith(
          money: updatedState.money + amount,
        );
        break;
      case 'social':
        updatedState = updatedState.copyWith(
          socialCapital: updatedState.socialCapital + amount,
        );
        break;
    }
    
    // Update game state
    ref.read(gameStateProvider.notifier).state = 
        ref.read(gameStateProvider).copyWith(resources: updatedState);
  }
}

// Derived Providers
@riverpod
int availableEnergy(AvailableEnergyRef ref) {
  return ref.watch(resourcesProvider).energy;
}

@riverpod
double availableTime(AvailableTimeRef ref) {
  return ref.watch(resourcesProvider).timeThisWeek;
}

@riverpod
double availableMoney(AvailableMoneyRef ref) {
  return ref.watch(resourcesProvider).money;
}
```

---

## Card Hand Provider

### CardHandProvider

**Purpose:** Manage player's current hand of cards

```dart
@riverpod
class CardHand extends _$CardHand {
  @override
  List<CardEntity> build() {
    // Derived from game state
    return ref.watch(gameStateProvider.select((state) => state.hand));
  }
  
  // ===================
  // Card Management
  // ===================
  
  Future<void> drawCards(int count) async {
    final drawUseCase = ref.read(drawCardsUseCaseProvider);
    final result = await drawUseCase.execute(count);
    
    result.fold(
      onSuccess: (newCards) {
        final gameState = ref.read(gameStateProvider);
        ref.read(gameStateProvider.notifier).state = gameState.copyWith(
          hand: [...gameState.hand, ...newCards],
        );
      },
      onError: (error) {
        AppLogger.error('Failed to draw cards', error);
      },
    );
  }
  
  Future<void> playCard(CardEntity card) async {
    // Validate
    if (!_canPlayCard(card)) {
      throw InsufficientResourcesError();
    }
    
    // Play card use case
    final playCardUseCase = ref.read(playCardUseCaseProvider);
    final result = await playCardUseCase.execute(card);
    
    result.fold(
      onSuccess: (_) {
        // Remove from hand
        _removeCard(card);
        
        // Apply effects
        _applyCardEffects(card);
        
        // Log
        AppLogger.info('Card played', data: {
          'card_id': card.id,
          'card_title': card.title,
        });
      },
      onError: (error) {
        AppLogger.error('Failed to play card', error);
        throw error;
      },
    );
  }
  
  bool _canPlayCard(CardEntity card) {
    final resources = ref.read(resourcesProvider);
    return ref.read(resourcesProvider.notifier).canAfford(card.costs);
  }
  
  void _removeCard(CardEntity card) {
    final gameState = ref.read(gameStateProvider);
    ref.read(gameStateProvider.notifier).state = gameState.copyWith(
      hand: gameState.hand.where((c) => c.id != card.id).toList(),
    );
  }
  
  void _applyCardEffects(CardEntity card) {
    // Spend resources
    ref.read(resourcesProvider.notifier).spend(card.costs);
    
    // Apply card-specific effects
    for (final effect in card.effects) {
      _applyEffect(effect);
    }
  }
  
  void _applyEffect(Effect effect) {
    switch (effect.type) {
      case EffectType.modifyRelationship:
        ref.read(relationshipsProvider.notifier).modifyTrust(
          effect.targetNpc!,
          effect.value,
        );
        break;
      case EffectType.modifyLifeMeter:
        ref.read(lifeMetersProvider.notifier).modify(
          effect.meterType!,
          effect.value,
        );
        break;
      case EffectType.earnMoney:
        ref.read(resourcesProvider.notifier).earn('money', effect.value);
        break;
      // ... more effect types
    }
  }
  
  // ===================
  // Queries
  // ===================
  
  int get handSize => state.length;
  
  bool get isHandFull => handSize >= 7;
  
  List<CardEntity> get playableCards {
    return state.where((card) => _canPlayCard(card)).toList();
  }
}

// Derived Providers
@riverpod
bool canPlayCard(CanPlayCardRef ref, CardEntity card) {
  final resources = ref.watch(resourcesProvider);
  return ref.read(resourcesProvider.notifier).canAfford(card.costs);
}

@riverpod
int handSize(HandSizeRef ref) {
  return ref.watch(cardHandProvider).length;
}
```

---

## Timeline Provider

### TimelineProvider

**Purpose:** Track game timeline (week, day, phase, act structure)

```dart
@riverpod
class Timeline extends _$Timeline {
  @override
  TimelineEntity build() {
    final gameState = ref.watch(gameStateProvider);
    return TimelineEntity(
      currentWeek: gameState.currentWeek,
      currentDay: gameState.currentDay,
      currentPhase: gameState.currentPhase,
    );
  }
  
  // ===================
  // Act Structure
  // ===================
  
  int get currentAct {
    final week = state.currentWeek;
    if (week <= 6) return 1;   // Setup
    if (week <= 12) return 2;  // Rising Action
    if (week <= 18) return 3;  // Climax
    if (week <= 24) return 4;  // Falling Action
    return 5;                   // Resolution
  }
  
  String get currentActName {
    switch (currentAct) {
      case 1:
        return 'Act I: Setup';
      case 2:
        return 'Act II: Rising Action';
      case 3:
        return 'Act III: Climax';
      case 4:
        return 'Act IV: Falling Action';
      case 5:
        return 'Act V: Resolution';
      default:
        return 'Unknown Act';
    }
  }
  
  double get actProgress {
    final week = state.currentWeek;
    switch (currentAct) {
      case 1:
        return (week - 1) / 6;
      case 2:
        return (week - 7) / 6;
      case 3:
        return (week - 13) / 6;
      case 4:
        return (week - 19) / 6;
      case 5:
        return (week - 25) / 6;
      default:
        return 0;
    }
  }
  
  // ===================
  // Day/Week Tracking
  // ===================
  
  String get dayName {
    switch (state.currentDay) {
      case 1:
        return 'Monday';
      case 2:
        return 'Tuesday';
      case 3:
        return 'Wednesday';
      case 4:
        return 'Thursday';
      case 5:
        return 'Friday';
      case 6:
        return 'Saturday';
      case 7:
        return 'Sunday';
      default:
        return 'Unknown';
    }
  }
  
  bool get isWeekend => state.currentDay >= 6;
  
  bool get isWeekStart => state.currentDay == 1;
  
  // ===================
  // Phase Tracking
  // ===================
  
  String get phaseName => state.currentPhase.name.toUpperCase();
  
  bool get isMorning => state.currentPhase == Phase.morning;
  bool get isDay => state.currentPhase == Phase.day;
  bool get isNight => state.currentPhase == Phase.night;
}

// Derived Providers
@riverpod
int currentWeek(CurrentWeekRef ref) {
  return ref.watch(timelineProvider).currentWeek;
}

@riverpod
int currentDay(CurrentDayRef ref) {
  return ref.watch(timelineProvider).currentDay;
}

@riverpod
Phase currentPhase(CurrentPhaseRef ref) {
  return ref.watch(timelineProvider).currentPhase;
}
```

---

## Life Meters Provider

### LifeMetersProvider

**Purpose:** Track physical, mental, social, and emotional well-being

```dart
@riverpod
class LifeMeters extends _$LifeMeters {
  @override
  LifeMetersEntity build() {
    return ref.watch(gameStateProvider.select((state) => state.lifeMeters));
  }
  
  // ===================
  // Meter Modifications
  // ===================
  
  void modify(MeterType type, double amount) {
    var updated = state;
    
    switch (type) {
      case MeterType.physical:
        updated = updated.copyWith(
          physical: (updated.physical + amount).clamp(0, 100).toInt(),
        );
        break;
      case MeterType.mental:
        updated = updated.copyWith(
          mental: (updated.mental + amount).clamp(0, 100).toInt(),
        );
        break;
      case MeterType.social:
        updated = updated.copyWith(
          social: (updated.social + amount).clamp(0, 100).toInt(),
        );
        break;
      case MeterType.emotional:
        updated = updated.copyWith(
          emotional: (updated.emotional + amount).clamp(0, 100).toInt(),
        );
        break;
    }
    
    // Update game state
    final gameState = ref.read(gameStateProvider);
    ref.read(gameStateProvider.notifier).state = 
        gameState.copyWith(lifeMeters: updated);
    
    // Check for critical levels
    _checkCriticalLevels(updated);
  }
  
  void _checkCriticalLevels(LifeMetersEntity meters) {
    if (meters.physical < 20) {
      _triggerCriticalWarning('Physical health is dangerously low!');
    }
    if (meters.mental < 20) {
      _triggerCriticalWarning('Mental health needs attention!');
    }
    if (meters.social < 20) {
      _triggerCriticalWarning('You\'re becoming isolated!');
    }
    if (meters.emotional < 20) {
      _triggerCriticalWarning('Emotional well-being is suffering!');
    }
  }
  
  void _triggerCriticalWarning(String message) {
    ref.read(eventBusProvider).fire(CriticalWarningEvent(message));
  }
  
  // ===================
  // Turn-Based Decay
  // ===================
  
  void applyTurnDecay() {
    // Small decay each turn to encourage active play
    modify(MeterType.physical, -1);
    modify(MeterType.mental, -1);
    modify(MeterType.social, -1);
    modify(MeterType.emotional, -1);
  }
  
  // ===================
  // Queries
  // ===================
  
  bool get isHealthy {
    return state.physical > 50 &&
           state.mental > 50 &&
           state.social > 50 &&
           state.emotional > 50;
  }
  
  int get lowestMeter {
    return [
      state.physical,
      state.mental,
      state.social,
      state.emotional,
    ].reduce((a, b) => a < b ? a : b);
  }
  
  MeterType get criticalMeterType {
    final lowest = lowestMeter;
    if (state.physical == lowest) return MeterType.physical;
    if (state.mental == lowest) return MeterType.mental;
    if (state.social == lowest) return MeterType.social;
    return MeterType.emotional;
  }
}
```

---

## Relationships Provider

### RelationshipsProvider

**Purpose:** Manage NPC relationships and trust levels

```dart
@riverpod
class Relationships extends _$Relationships {
  @override
  Future<List<RelationshipEntity>> build() async {
    final repository = ref.watch(relationshipRepositoryProvider);
    return await repository.getAll();
  }
  
  // ===================
  // Trust Management
  // ===================
  
  Future<void> modifyTrust(String npcId, double amount) async {
    final relationships = state.value!;
    final index = relationships.indexWhere((r) => r.npcId == npcId);
    
    if (index == -1) {
      // Create new relationship
      final newRelationship = RelationshipEntity(
        npcId: npcId,
        trust: amount.clamp(0, 100),
      );
      state = AsyncValue.data([...relationships, newRelationship]);
    } else {
      // Update existing
      final updated = relationships[index].copyWith(
        trust: (relationships[index].trust + amount).clamp(0, 100),
      );
      state = AsyncValue.data([
        ...relationships.take(index),
        updated,
        ...relationships.skip(index + 1),
      ]);
    }
    
    // Persist to repository
    final repository = ref.read(relationshipRepositoryProvider);
    await repository.save(state.value!);
  }
  
  // ===================
  // Turn-Based Decay
  // ===================
  
  Future<void> applyTurnDecay() async {
    if (state.value == null) return;
    
    final updated = state.value!.map((r) {
      // Trust decays slowly over time
      return r.copyWith(
        trust: (r.trust - 0.5).clamp(0, 100),
      );
    }).toList();
    
    state = AsyncValue.data(updated);
    
    final repository = ref.read(relationshipRepositoryProvider);
    await repository.save(updated);
  }
  
  // ===================
  // Queries
  // ===================
  
  RelationshipEntity? getRelationshipByNpc(String npcId) {
    if (state.value == null) return null;
    try {
      return state.value!.firstWhere((r) => r.npcId == npcId);
    } catch (_) {
      return null;
    }
  }
  
  List<RelationshipEntity> get friends {
    if (state.value == null) return [];
    return state.value!.where((r) => r.trust >= 70).toList();
  }
  
  List<RelationshipEntity> get acquaintances {
    if (state.value == null) return [];
    return state.value!
        .where((r) => r.trust >= 30 && r.trust < 70)
        .toList();
  }
  
  int get friendCount => friends.length;
}

// Derived Providers
@riverpod
RelationshipEntity? relationshipWithNpc(
  RelationshipWithNpcRef ref,
  String npcId,
) {
  return ref.watch(relationshipsProvider.select((async) {
    return async.value?.firstWhere(
      (r) => r.npcId == npcId,
      orElse: () => RelationshipEntity.empty(npcId),
    );
  }));
}
```

---

## Flame Integration Patterns

### Using Game State in Flame Components

```dart
class CardComponent extends SpriteAnimationGroupComponent 
    with TapCallbacks, HasGameRef {
  final CardEntity card;
  final WidgetRef ref;
  
  CardComponent({required this.card, required this.ref});
  
  @override
  void update(double dt) {
    super.update(dt);
    
    // Reactive to game state
    final canPlay = ref.read(canPlayCardProvider(card));
    
    if (canPlay && current != CardState.playable) {
      current = CardState.playable;
      add(GlowEffect());
    } else if (!canPlay && current == CardState.playable) {
      current = CardState.disabled;
      remove(GlowEffect);
    }
  }
  
  @override
  void onTapUp(TapUpEvent event) async {
    try {
      await ref.read(cardHandProvider.notifier).playCard(card);
      
      // Success - remove from board
      add(CardPlayEffect());
      removeFromParent();
    } catch (e) {
      // Error feedback
      add(ErrorShakeEffect());
      AppLogger.error('Card play failed', e);
    }
  }
}
```

### Listening to State Changes in Flame

```dart
class GameWorld extends Component with HasGameRef {
  final WidgetRef ref;
  
  GameWorld({required this.ref});
  
  @override
  Future<void> onLoad() async {
    // Listen to turn changes
    ref.listen<GameStateEntity>(gameStateProvider, (previous, next) {
      if (previous?.currentTurn != next.currentTurn) {
        _onTurnChanged(next.currentTurn);
      }
      
      if (previous?.currentPhase != next.currentPhase) {
        _onPhaseChanged(next.currentPhase);
      }
    });
  }
  
  void _onTurnChanged(int newTurn) {
    // Refresh hand
    _refreshCardHand();
    
    // Play turn transition effect
    add(TurnTransitionEffect(newTurn));
  }
  
  void _onPhaseChanged(Phase newPhase) {
    // Update background lighting
    final background = children.whereType<BackgroundComponent>().first;
    background.updateForPhase(newPhase);
  }
  
  void _refreshCardHand() {
    final hand = ref.read(cardHandProvider);
    
    // Remove old cards
    removeAll(children.whereType<CardComponent>());
    
    // Add new cards
    for (var i = 0; i < hand.length; i++) {
      add(CardComponent(
        card: hand[i],
        ref: ref,
      )..position = _getCardPosition(i, hand.length));
    }
  }
}
```

---

## Performance Considerations

### Selective Watching

```dart
// ❌ BAD: Rebuilds on ANY game state change
final gameState = ref.watch(gameStateProvider);

// ✅ GOOD: Only rebuilds when energy changes
final energy = ref.watch(
  gameStateProvider.select((state) => state.resources.energy),
);
```

### Caching Expensive Computations

```dart
@riverpod
List<CardEntity> playableCards(PlayableCardsRef ref) {
  final hand = ref.watch(cardHandProvider);
  final resources = ref.watch(resourcesProvider);
  
  // Cached - only recomputes when hand or resources change
  return hand.where((card) {
    return ref.read(resourcesProvider.notifier).canAfford(card.costs);
  }).toList();
}
```

---

## Resources

### Related Documentation
- [Riverpod Setup](./01-riverpod-setup.md)
- [Notifier Patterns](./03-notifier-patterns.md)
- [Dependency Injection](../01-architecture/04-dependency-injection.md)
- [Flame-Riverpod Integration](../02-flame-engine/10-flame-riverpod-integration.md)

---

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Master Spec Reference:** `docs/master_flutter_flame_spec_v_1_0.md`

