# Flame-Riverpod Integration

**Note:** `flame_riverpod` package has version conflicts. Use manual integration patterns.

## Manual Integration Pattern

### HasGameReference with Riverpod

```dart
class CardComponent extends PositionComponent 
    with HasGameReference<UnwrittenGame> {
  
  late final WidgetRef ref;
  
  @override
  Future<void> onLoad() async {
    // Get WidgetRef from game
    ref = game.ref;
    
    // Watch providers
    _watchGameState();
  }
  
  void _watchGameState() {
    ref.listen<GameState>(
      gameStateProvider,
      (previous, next) {
        _onGameStateChange(previous, next);
      },
    );
  }
  
  void _onGameStateChange(GameState? previous, GameState next) {
    // React to state changes
    if (next.currentPhase != previous?.currentPhase) {
      _updateForPhase(next.currentPhase);
    }
  }
}
```

### Game with Riverpod Reference

```dart
class UnwrittenGame extends FlameGame {
  late final WidgetRef ref;
  
  UnwrittenGame(this.ref);
  
  @override
  Future<void> onLoad() async {
    // Access providers
    final gameState = ref.read(gameStateProvider);
    
    // Setup based on state
    _setupForState(gameState);
  }
  
  void playCard(CardComponent card) {
    // Update state via notifier
    ref.read(gameStateProvider.notifier).playCard(card.cardData);
  }
}
```

### GameWidget with Riverpod

```dart
class GameScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return GameWidget(
      game: UnwrittenGame(ref),
      overlayBuilderMap: {
        'hud': (context, game) => GameHUD(ref: ref),
      },
    );
  }
}
```

## Reactive Component Updates

```dart
class ReactiveCard extends PositionComponent 
    with HasGameReference<UnwrittenGame> {
  
  @override
  void update(double dt) {
    // Read current state each frame
    final gameState = game.ref.read(gameStateProvider);
    
    // Update based on state
    if (gameState.isPlayerTurn) {
      _enableInteraction();
    } else {
      _disableInteraction();
    }
    
    super.update(dt);
  }
}
```

## Provider Access from Components

```dart
class CardHand extends PositionComponent with HasGameReference<UnwrittenGame> {
  void drawCard() {
    // Read notifier
    final notifier = game.ref.read(gameStateProvider.notifier);
    notifier.drawCard();
    
    // Get new card data
    final newCard = game.ref.read(gameStateProvider).hand.last;
    
    // Create component
    add(CardComponent(newCard));
  }
}
```

## UI Overlay with Game Integration

```dart
class GameHUD extends ConsumerWidget {
  final UnwrittenGame game;
  
  const GameHUD({required this.game});
  
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final gameState = ref.watch(gameStateProvider);
    
    return Stack(
      children: [
        // Resource display
        Positioned(
          top: 20,
          right: 20,
          child: ResourceDisplay(
            energy: gameState.resources.energy,
          ),
        ),
        
        // Turn counter
        Positioned(
          top: 20,
          left: 20,
          child: Text('Turn ${gameState.currentTurn}'),
        ),
        
        // End turn button
        Positioned(
          bottom: 20,
          right: 20,
          child: EndTurnButton(
            onPressed: () {
              game.endTurn();
              ref.read(gameStateProvider.notifier).endTurn();
            },
          ),
        ),
      ],
    );
  }
}
```

---

**Previous:** [Performance Optimization](./09-performance-optimization.md)  
**Index:** [Flame Engine Index](./00-INDEX.md)  
**Related:** `../03-state-management/`


