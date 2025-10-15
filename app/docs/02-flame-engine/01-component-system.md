# Flame Component System

**Reference:** `docs/master_flutter_flame_spec_v_1_0.md` (Lines 1-48)

## Overview

The Flame Component System (FCS) is the sophisticated backbone of Unwritten's game architecture. It enables complex, hierarchical component management with a complete lifecycle system optimized for 60 FPS card game interactions.

## Component Lifecycle

### Complete Lifecycle Hooks

Every Flame component follows this lifecycle:

```dart
class CardComponent extends PositionComponent with TapCallbacks {
  @override
  Future<void> onLoad() async {
    // ✅ Called ONCE when component is first loaded
    // Use for: Asset loading, initialization, dependency resolution
    await super.onLoad();
    
    // Load card sprite
    final cardSprite = await Sprite.load('cards/base.png');
    add(SpriteComponent(sprite: cardSprite));
    
    // Initialize state
    size = Vector2(120, 168);
    anchor = Anchor.center;
  }
  
  @override
  void onMount() {
    // ✅ Called EVERY TIME component enters the tree
    // Use for: Reconnecting listeners, dynamic reconfiguration
    super.onMount();
    
    // Start animations when card appears
    add(ScaleEffect.to(Vector2.all(1.0), EffectController(duration: 0.3)));
  }
  
  @override
  void onGameResize(Vector2 size) {
    // ✅ Called when screen size changes (rotation, window resize)
    // Use for: Responsive positioning, layout adjustments
    super.onGameResize(size);
    
    // Reposition card based on new screen size
    position = size / 2;
  }
  
  @override
  void onParentResize(Vector2 size) {
    // ✅ Called when parent component resizes
    // Use for: Cascading size dependencies
    super.onParentResize(size);
  }
  
  @override
  void onRemove() {
    // ✅ Called before component is removed
    // Use for: Cleanup, resource deallocation
    _disposeResources();
    super.onRemove();
  }
  
  @override
  void onChildrenChanged(Component child, ChildrenChangeType type) {
    // ✅ Called when children are added/removed
    // Use for: Sophisticated parent-child management
    super.onChildrenChanged(child, type);
    
    if (type == ChildrenChangeType.added) {
      // React to new child
    }
  }
}
```

## Component Hierarchy & Priority

### Z-Index Rendering Order

Components render based on their `priority` value:

```dart
class GameBoardWorld extends World {
  @override
  Future<void> onLoad() async {
    await addAll([
      BackgroundLayer()..priority = -100,  // Renders first (behind)
      CardHandLayer()..priority = 0,       // Middle layer
      CardDragLayer()..priority = 50,      // Above hand
      UIOverlayLayer()..priority = 100,    // Renders last (front)
    ]);
  }
}
```

### Dynamic Priority Changes

Change rendering order at runtime:

```dart
class DraggableCard extends PositionComponent {
  void startDrag() {
    // Bring to front during drag
    changePriority(1000);
  }
  
  void endDrag() {
    // Return to original layer
    changePriority(0);
  }
  
  // For performance-critical bulk changes:
  void quickPriorityChange() {
    // Avoids immediate resort (batch with others)
    changePriorityWithoutResorting(50);
  }
}
```

## Component Keys & Retrieval

### Named Component Identification

Use component keys for efficient retrieval:

```dart
class CardHand extends PositionComponent {
  @override
  Future<void> onLoad() async {
    // Create cards with named keys
    for (int i = 0; i < 5; i++) {
      final card = CardComponent()
        ..key = ComponentKey.named('card_$i');
      add(card);
    }
  }
  
  void highlightCard(int index) {
    // Efficient retrieval by key
    final card = findByKey(ComponentKey.named('card_$index'));
    card?.add(GlowEffect());
  }
}
```

### Unique Keys for Dynamic Content

```dart
class CardFactory {
  static CardComponent create(String cardId) {
    return CardComponent()
      ..key = ComponentKey.unique()  // Guaranteed unique ID
      ..cardData = CardData.load(cardId);
  }
}
```

## Advanced Querying

### Type-Safe Component Queries

Use `query<T>()` for sophisticated filtering:

```dart
class GameManager extends Component with HasGameReference<MyGame> {
  void updateAllCards() {
    // Get all CardComponents
    final cards = query<CardComponent>();
    
    for (final card in cards) {
      card.updateState();
    }
  }
  
  void countActiveEffects() {
    // Get all active particle effects
    final particles = query<ParticleSystemComponent>();
    AppLogger.performance('Active particles', {'count': particles.length});
  }
  
  void cleanupOffscreenCards() {
    final cards = query<CardComponent>();
    final screenBounds = game.camera.visibleWorldRect;
    
    for (final card in cards) {
      if (!screenBounds.containsPoint(card.position)) {
        card.removeFromParent();
      }
    }
  }
}
```

### QueryableOrderedSet Operations

```dart
class CardManager extends Component {
  void batchCardOperation() {
    // Efficient batch operations
    final cardSet = QueryableOrderedSet<CardComponent>();
    
    // Add multiple cards
    cardSet.addAll(createCards());
    
    // Query and filter
    final visibleCards = cardSet.query<CardComponent>()
        .where((card) => card.isVisible)
        .toList();
    
    // Batch update
    for (final card in visibleCards) {
      card.animate();
    }
  }
}
```

## Visibility Optimization

### HasVisibility Mixin

Optimize show/hide without lifecycle overhead:

```dart
class OptimizedCard extends PositionComponent with HasVisibility {
  void hideWithoutRemoval() {
    // Performance-optimized hiding
    // No onRemove() called, no component tree modification
    isVisible = false;  // Just skips rendering
  }
  
  void showAgain() {
    isVisible = true;  // Starts rendering again
  }
  
  @override
  void render(Canvas canvas) {
    if (!isVisible) return;  // Automatically handled
    super.render(canvas);
  }
}
```

## Component Communication Patterns

### HasGameReference for Global Access

```dart
class CardComponent extends PositionComponent 
    with HasGameReference<UnwrittenGame>, TapCallbacks {
  
  @override
  void onTapDown(TapDownEvent event) {
    // Access game-level services
    game.audioManager.playSfx('card_tap');
    game.hapticFeedback.lightImpact();
    
    // Access game state
    if (game.gameState.canPlayCard(this)) {
      playCard();
    }
  }
  
  void playCard() {
    // Access other components via game reference
    final hand = game.findByKey(ComponentKey.named('card_hand'))!;
    hand.removeCard(this);
    
    // Trigger game state update
    game.playCard(this);
  }
}
```

### Stream-Based Communication

```dart
class CardHand extends PositionComponent {
  final _cardPlayedController = StreamController<CardComponent>.broadcast();
  
  Stream<CardComponent> get onCardPlayed => _cardPlayedController.stream;
  
  void playCard(CardComponent card) {
    _cardPlayedController.add(card);
    card.removeFromParent();
  }
  
  @override
  void onRemove() {
    _cardPlayedController.close();
    super.onRemove();
  }
}

class GameBoard extends PositionComponent {
  late CardHand hand;
  
  @override
  Future<void> onLoad() async {
    hand = CardHand();
    add(hand);
    
    // Listen to card events
    hand.onCardPlayed.listen((card) {
      // Animate card to board
      animateCardToBoard(card);
    });
  }
}
```

### Direct Component References

```dart
class GameManager extends Component with HasGameReference<UnwrittenGame> {
  late final CardHand hand;
  late final CardBoard board;
  late final UIOverlay ui;
  
  @override
  Future<void> onLoad() async {
    // Get references during initialization
    hand = game.findByKey(ComponentKey.named('hand'))! as CardHand;
    board = game.findByKey(ComponentKey.named('board'))! as CardBoard;
    ui = game.findByKey(ComponentKey.named('ui'))! as UIOverlay;
    
    // Set up cross-component communication
    hand.onCardPlayed.listen((card) {
      board.receiveCard(card);
      ui.updateCardCount(hand.cardCount);
    });
  }
}
```

## ComponentsNotifier Integration

### Automatic UI Updates

Connect Flame components to Flutter widgets:

```dart
class CardCounterWidget extends StatelessWidget {
  final UnwrittenGame game;
  
  const CardCounterWidget({required this.game});
  
  @override
  Widget build(BuildContext context) {
    return ComponentsNotifierBuilder<CardComponent>(
      notifier: game.componentsNotifier<CardComponent>(),
      builder: (context, components) {
        final cardCount = components.length;
        return Text('Cards: $cardCount');
      },
    );
  }
}
```

## Best Practices for Unwritten

### Component Organization

```dart
// ✅ CORRECT: Clear hierarchy, specific responsibilities
class CardHandComponent extends PositionComponent {
  final List<CardComponent> _cards = [];
  
  void addCard(CardComponent card) {
    _cards.add(card);
    add(card);
    _repositionCards();
  }
  
  void _repositionCards() {
    // Layout logic isolated to this component
  }
}

// ❌ WRONG: God component doing everything
class GameComponent extends PositionComponent {
  // Handles cards, UI, audio, state - too much!
}
```

### Resource Management

```dart
class CardComponent extends PositionComponent {
  StreamSubscription? _stateSubscription;
  
  @override
  Future<void> onLoad() async {
    // Subscribe to state changes
    _stateSubscription = gameState.stream.listen(_onStateChange);
  }
  
  @override
  void onRemove() {
    // ✅ ALWAYS clean up resources
    _stateSubscription?.cancel();
    _disposeAnimations();
    super.onRemove();
  }
}
```

### Performance Guidelines

```dart
class OptimizedCardComponent extends PositionComponent {
  @override
  Future<void> onLoad() async {
    // ✅ Load assets asynchronously
    final sprite = await Sprite.load('card.png');
    
    // ✅ Use const constructors where possible
    add(const CardBorderDecoration());
    
    // ✅ Pool frequently created components
    final particle = ParticlePool.instance.get();
    add(particle);
  }
  
  @override
  void update(double dt) {
    // ✅ Guard expensive operations
    if (!isVisible) return;
    
    // ✅ Batch operations
    if (_needsUpdate) {
      _batchUpdate();
      _needsUpdate = false;
    }
    
    super.update(dt);
  }
}
```

## Common Patterns for Card Games

### Card Pool Management

```dart
class CardPool extends Component {
  final Queue<CardComponent> _availableCards = Queue();
  final int _maxPoolSize = 100;
  
  CardComponent getCard() {
    if (_availableCards.isNotEmpty) {
      return _availableCards.removeFirst();
    }
    return CardComponent();  // Create new if pool empty
  }
  
  void returnCard(CardComponent card) {
    if (_availableCards.length < _maxPoolSize) {
      card.reset();
      _availableCards.add(card);
    }
  }
}
```

### State-Driven Component Updates

```dart
class StatefulCard extends PositionComponent {
  CardState _currentState = CardState.idle;
  
  set state(CardState newState) {
    if (_currentState == newState) return;
    
    _currentState = newState;
    _updateVisuals();
  }
  
  void _updateVisuals() {
    removeAll(children.query<Effect>());
    
    switch (_currentState) {
      case CardState.idle:
        scale = Vector2.all(1.0);
      case CardState.hover:
        add(ScaleEffect.to(Vector2.all(1.2), EffectController(duration: 0.2)));
      case CardState.dragging:
        priority = 1000;  // Bring to front
    }
  }
}
```

---

**Next:** [Game Loop & Lifecycle](./02-game-loop-lifecycle.md)  
**Related:** [Performance Optimization](./09-performance-optimization.md), [Input Handling](./08-input-handling.md)


