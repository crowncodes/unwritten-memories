# Component Architecture

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete

---

## Overview

Flame's component system provides a hierarchy for organizing game objects, managing lifecycle, and enabling composition patterns.

---

## Component Hierarchy

### Tree Structure

```
FlameGame (root)
  └── World
      ├── Component A
      │   ├── Child A1
      │   └── Child A2
      │       └── Grandchild
      └── Component B
```

### Example

```dart
class UnwrittenGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    world.add(BackgroundComponent());
    world.add(CardHandComponent(
      children: [
        CardComponent(card: card1),
        CardComponent(card: card2),
      ],
    ));
  }
}
```

---

## Component Lifecycle

### Lifecycle Methods

```dart
class MyComponent extends PositionComponent {
  // 1. Constructor
  MyComponent() {
    print('Constructor called');
  }
  
  // 2. onLoad (async initialization)
  @override
  Future<void> onLoad() async {
    await super.onLoad();
    print('onLoad: Load assets here');
  }
  
  // 3. onMount (added to game tree)
  @override
  void onMount() {
    super.onMount();
    print('onMount: Component added to game');
  }
  
  // 4. update (every frame)
  @override
  void update(double dt) {
    super.update(dt);
    print('update: Called every frame');
  }
  
  // 5. render (every frame)
  @override
  void render(Canvas canvas) {
    super.render(canvas);
    print('render: Draw to canvas');
  }
  
  // 6. onRemove (removed from tree)
  @override
  void onRemove() {
    print('onRemove: Cleanup here');
    super.onRemove();
  }
}
```

---

## Component Communication

### Parent-Child Communication

```dart
// Parent accessing child
class ParentComponent extends Component {
  late ChildComponent child;
  
  @override
  Future<void> onLoad() async {
    child = ChildComponent();
    add(child);
  }
  
  void notifyChild() {
    child.doSomething();
  }
}

// Child accessing parent
class ChildComponent extends Component {
  void accessParent() {
    if (parent is ParentComponent) {
      (parent as ParentComponent).parentMethod();
    }
  }
}
```

### Event System

```dart
// Define event
class CardPlayedEvent {
  final String cardId;
  CardPlayedEvent(this.cardId);
}

// Dispatch event
void playCard(String cardId) {
  game.propagateToChildren((component) {
    if (component is EventListener<CardPlayedEvent>) {
      component.onEvent(CardPlayedEvent(cardId));
    }
    return true; // Continue propagation
  });
}

// Listen for event
class ListenerComponent extends Component 
    implements EventListener<CardPlayedEvent> {
  
  @override
  void onEvent(CardPlayedEvent event) {
    print('Card played: ${event.cardId}');
  }
}
```

---

## Composition Patterns

### Mixin-Based Composition

```dart
class InteractiveCard extends PositionComponent
    with DragCallbacks, TapCallbacks, HoverCallbacks {
  // Combines drag, tap, and hover behaviors
}
```

### Component-Based Composition

```dart
class ComplexCard extends PositionComponent {
  @override
  Future<void> onLoad() async {
    // Add sprite
    add(SpriteComponent(/* ... */));
    
    // Add text
    add(TextComponent(/* ... */));
    
    // Add particle effects
    add(ParticleSystemComponent(/* ... */));
    
    // Add health bar
    add(HealthBarComponent(/* ... */));
  }
}
```

---

## Custom Components

### Template

```dart
class CustomComponent extends PositionComponent with HasGameRef {
  // State
  double health = 100;
  
  // Dependencies
  late SpriteComponent sprite;
  
  CustomComponent({
    required Vector2 position,
    required Vector2 size,
  }) : super(position: position, size: size, anchor: Anchor.center);
  
  @override
  Future<void> onLoad() async {
    await super.onLoad();
    
    // Initialize sprite
    final spriteImage = await gameRef.loadSprite('custom.png');
    sprite = SpriteComponent(sprite: spriteImage, size: size);
    add(sprite);
  }
  
  @override
  void update(double dt) {
    super.update(dt);
    // Update logic
  }
  
  void takeDamage(double amount) {
    health -= amount;
    if (health <= 0) {
      removeFromParent();
    }
  }
}
```

---

## Component Pooling

```dart
class ComponentPool<T extends Component> {
  final List<T> _pool = [];
  final T Function() _creator;
  
  ComponentPool(this._creator);
  
  T acquire() {
    if (_pool.isNotEmpty) {
      return _pool.removeLast();
    }
    return _creator();
  }
  
  void release(T component) {
    component.removeFromParent();
    _pool.add(component);
  }
}

// Usage
final cardPool = ComponentPool<CardComponent>(() => CardComponent());
final card = cardPool.acquire();
// ... use card ...
cardPool.release(card);
```

---

## Related Documentation

- **55-flame-engine-fundamentals.md** - Flame basics
- **56-card-physics-animations.md** - Physics implementation
- **59-performance-optimization-flame.md** - Performance

---

**Status:** ✅ Component Architecture Complete

