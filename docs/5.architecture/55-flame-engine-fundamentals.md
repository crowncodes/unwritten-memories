# Flame Engine Fundamentals

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete

---

## Overview

Flame is a 2D game engine built on Flutter. Unwritten uses Flame for smooth 60 FPS gameplay, physics-based card interactions, and Unity-like game feel.

**Why Flame:** Component-based architecture, built-in game loop, proven at scale (I/O FLIP)

**Version:** 1.20.0+

---

## Why Flame from Day 1?

### Code Structure Differences

**Flutter (Widget-based):**
```dart
class CardWidget extends StatefulWidget {
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onPanUpdate: (details) {
        // Manual update
        setState(() { /* ... */ });
      },
      child: Transform.translate(
        offset: position,
        child: Image.asset('card.png'),
      ),
    );
  }
}
```

**Flame (Component-based):**
```dart
class CardComponent extends PositionComponent with DragCallbacks {
  @override
  void update(double dt) {
    // Automatic game loop updates
    position += velocity * dt;
    velocity *= friction;
  }
  
  @override
  void render(Canvas canvas) {
    // Direct canvas rendering
    sprite.render(canvas);
  }
  
  @override
  void onDragUpdate(DragUpdateEvent event) {
    position += event.localDelta;
    velocity = event.localDelta / dt;
  }
}
```

**Key Differences:**
- ✅ Flame has automatic `update()` loop (no manual setState)
- ✅ Flame renders directly to canvas (faster)
- ✅ Flame has built-in physics (velocity, acceleration)
- ✅ Flame has component hierarchy (parent/child)

**Conclusion:** Starting with Flame avoids 2-3 weeks of migration work

**See:** `50-architecture-overview.md` ADR-001

---

## FlameGame Lifecycle

### Initialization Flow

```
FlameGame created
    ↓
onLoad() called
    ↓
Components added
    ↓
onMount() called on each component
    ↓
Game loop starts: update() → render() → repeat
```

### Main Game Class

```dart
// features/game/presentation/components/unwritten_game_world.dart
import 'package:flame/game.dart';

class UnwrittenGame extends FlameGame {
  // Game configuration
  static const double targetFPS = 60.0;
  static const double updateInterval = 1.0 / targetFPS; // 16.67ms
  
  // Game state (passed from Riverpod)
  final GameState initialState;
  final List<Card> cards;
  final void Function(String cardId) onCardPlay;
  
  UnwrittenGame({
    required this.initialState,
    required this.cards,
    required this.onCardPlay,
  });
  
  @override
  Future<void> onLoad() async {
    await super.onLoad();
    
    // Setup camera
    camera = CameraComponent.withFixedResolution(
      width: 1920,
      height: 1080,
    );
    camera.viewfinder.anchor = Anchor.topLeft;
    
    // Load assets
    await images.loadAll([
      'card_back.png',
      'card_frame.png',
      'drop_zone.png',
    ]);
    
    // Create world
    world.add(BackgroundComponent());
    
    // Create card components from state
    for (final card in cards) {
      world.add(CardGameComponent(
        card: card,
        onPlay: onCardPlay,
      ));
    }
    
    // Create drop zones
    world.add(DropZoneComponent(type: DropZoneType.play));
    world.add(DropZoneComponent(type: DropZoneType.discard));
  }
  
  @override
  void update(double dt) {
    super.update(dt);
    // Fixed timestep update (automatic for all components)
  }
  
  @override
  void render(Canvas canvas) {
    super.render(canvas);
    // Automatic rendering of all components
  }
  
  // Public methods for external updates (from Riverpod)
  void updateCards(List<Card> newCards) {
    // Remove old cards
    world.children.whereType<CardGameComponent>().forEach((c) => c.removeFromParent());
    
    // Add new cards
    for (final card in newCards) {
      world.add(CardGameComponent(card: card, onPlay: onCardPlay));
    }
  }
  
  void updateGameState(GameState newState) {
    // Update game state
    // ...
  }
}
```

---

## Component System

### Component Hierarchy

```
FlameGame
  └── World
      ├── BackgroundComponent
      ├── CardGameComponent (×N)
      │   ├── SpriteComponent (card art)
      │   ├── TextComponent (title)
      │   └── ParticleSystemComponent (effects)
      ├── DropZoneComponent (×2)
      └── UIOverlayComponent
```

### Base Component Class

```dart
import 'package:flame/components.dart';

class CardGameComponent extends PositionComponent 
    with DragCallbacks, TapCallbacks, HasGameRef<UnwrittenGame> {
  
  final Card card;
  final void Function(String) onPlay;
  
  // Physics state
  Vector2 velocity = Vector2.zero();
  Vector2 startPosition = Vector2.zero();
  
  CardGameComponent({
    required this.card,
    required this.onPlay,
  }) : super(
    size: Vector2(200, 300),
    anchor: Anchor.center,
  );
  
  @override
  Future<void> onLoad() async {
    await super.onLoad();
    
    // Load sprite
    final sprite = await gameRef.loadSprite('cards/${card.id}.png');
    add(SpriteComponent(sprite: sprite, size: size));
    
    // Add title text
    add(TextComponent(
      text: card.title,
      position: Vector2(size.x / 2, 20),
      anchor: Anchor.topCenter,
    ));
    
    startPosition = position.clone();
  }
  
  @override
  void update(double dt) {
    super.update(dt);
    
    // Apply physics (if not being dragged)
    if (!isDragging) {
      position += velocity * dt;
      velocity *= 0.95; // Friction
      
      // Stop if velocity too small
      if (velocity.length < 1.0) {
        velocity.setZero();
      }
    }
  }
  
  @override
  void render(Canvas canvas) {
    super.render(canvas);
    // Automatic rendering of child components
  }
  
  bool isDragging = false;
  
  @override
  void onDragStart(DragStartEvent event) {
    isDragging = true;
    priority = 100; // Bring to front
  }
  
  @override
  void onDragUpdate(DragUpdateEvent event) {
    position += event.localDelta;
    velocity = event.localDelta / event.dt; // Track velocity
  }
  
  @override
  void onDragEnd(DragEndEvent event) {
    isDragging = false;
    priority = 0;
    
    // Check if dropped on drop zone
    final dropZone = _findDropZone();
    if (dropZone != null) {
      onPlay(card.id); // Trigger Riverpod callback
    } else {
      // Snap back with momentum
      _snapBack();
    }
  }
  
  void _snapBack() {
    final direction = (startPosition - position).normalized();
    velocity = direction * 1200; // Fast snap back
  }
  
  DropZoneComponent? _findDropZone() {
    // Check collision with drop zones
    for (final zone in gameRef.world.children.whereType<DropZoneComponent>()) {
      if (zone.containsPoint(position)) {
        return zone;
      }
    }
    return null;
  }
}
```

---

## Game Loop

### Fixed Timestep (60 FPS)

```
Frame 1: update(0.0167s) → render()
Frame 2: update(0.0167s) → render()
Frame 3: update(0.0167s) → render()
...
```

**Automatic:** Flame handles game loop, you just implement `update()` and `render()`

**Benefits:**
- ✅ Consistent physics (independent of frame rate)
- ✅ Smooth animations (60 FPS)
- ✅ Easy to reason about (dt = delta time)

### Delta Time (dt)

```dart
@override
void update(double dt) {
  // dt ≈ 0.0167 seconds (60 FPS)
  // dt ≈ 0.0333 seconds (30 FPS)
  
  // Move with dt for frame-rate independence
  position += velocity * dt;
  
  // Without dt (❌ BAD):
  // position += velocity; // Faster on high FPS!
}
```

---

## World and Camera

### Camera Setup

```dart
@override
Future<void> onLoad() async {
  // Fixed resolution (scales to device)
  camera = CameraComponent.withFixedResolution(
    width: 1920,
    height: 1080,
  );
  
  // Or follow target
  camera = CameraComponent()
    ..follow(player)
    ..setBounds(Rectangle.fromLTWH(0, 0, 3840, 2160));
}
```

**Fixed Resolution Benefits:**
- ✅ Same gameplay on all devices
- ✅ Consistent physics
- ✅ Easier development

**See:** `58-camera-viewport-systems.md` for advanced usage

---

## Input Handling

### Mixins for Input

```dart
// Tap detection
class CardComponent extends PositionComponent with TapCallbacks {
  @override
  void onTapDown(TapDownEvent event) {
    print('Card tapped!');
  }
  
  @override
  void onTapUp(TapUpEvent event) {
    print('Card released!');
  }
}

// Drag detection
class CardComponent extends PositionComponent with DragCallbacks {
  @override
  void onDragStart(DragStartEvent event) { }
  @override
  void onDragUpdate(DragUpdateEvent event) { }
  @override
  void onDragEnd(DragEndEvent event) { }
}

// Hover (web/desktop)
class CardComponent extends PositionComponent with HoverCallbacks {
  @override
  void onHoverEnter() {
    scale = Vector2.all(1.1); // Grow on hover
  }
  
  @override
  void onHoverExit() {
    scale = Vector2.all(1.0);
  }
}
```

---

## Effects System

### Built-in Effects

```dart
// Move effect
component.add(MoveEffect.to(
  Vector2(400, 300),
  EffectController(duration: 0.5),
));

// Scale effect
component.add(ScaleEffect.to(
  Vector2.all(1.2),
  EffectController(duration: 0.3, curve: Curves.easeOut),
));

// Rotate effect
component.add(RotateEffect.to(
  pi / 4, // 45 degrees
  EffectController(duration: 0.5),
));

// Sequence multiple effects
component.add(SequenceEffect([
  ScaleEffect.to(Vector2.all(1.2), EffectController(duration: 0.2)),
  ScaleEffect.to(Vector2.all(1.0), EffectController(duration: 0.2)),
]));

// Composite effects (parallel)
component.add(MoveEffect.to(/* ... */)
  ..add(RotateEffect.to(/* ... */)));
```

**See:** `56-card-physics-animations.md` for detailed physics

---

## Asset Loading

### Images

```dart
@override
Future<void> onLoad() async {
  // Load single image
  await images.load('card.png');
  
  // Load multiple images
  await images.loadAll([
    'card_back.png',
    'card_frame.png',
    'background.png',
  ]);
  
  // Use sprite
  final sprite = await loadSprite('card.png');
  add(SpriteComponent(sprite: sprite));
}
```

### Sprite Sheets

```dart
final spriteSheet = SpriteSheet(
  image: await images.load('cards_atlas.png'),
  srcSize: Vector2(200, 300),
);

final cardSprite = spriteSheet.getSprite(0, 0); // Row 0, Column 0
```

### Audio (via audioplayers)

```dart
import 'package:audioplayers/audioplayers.dart';

class AudioService {
  static final AudioPlayer _player = AudioPlayer();
  
  static Future<void> playSfx(String sound) async {
    await _player.play(AssetSource('audio/sfx/$sound.mp3'));
  }
}

// In component
AudioService.playSfx('card_play');
```

**See:** `63-audio-haptics-integration.md` for full audio setup

---

## Coordinate Systems

### Screen Coordinates vs World Coordinates

```dart
// Screen coordinates (pixels)
// (0, 0) = top-left of screen
// (width, height) = bottom-right of screen

// World coordinates (game units)
// (0, 0) = based on camera anchor
// With camera.anchor = Anchor.topLeft: (0, 0) = top-left

// Convert screen to world
final worldPos = camera.viewfinder.globalToLocal(screenPos);

// Convert world to screen
final screenPos = camera.viewfinder.localToGlobal(worldPos);
```

---

## Common Patterns

### Pooling Components

```dart
class CardPool {
  final List<CardGameComponent> _pool = [];
  
  CardGameComponent acquire(Card card) {
    if (_pool.isNotEmpty) {
      final component = _pool.removeLast();
      component.card = card;
      return component;
    }
    return CardGameComponent(card: card);
  }
  
  void release(CardGameComponent component) {
    _pool.add(component);
  }
}
```

### Timers

```dart
class TimerComponent extends Component with HasGameRef {
  double _elapsed = 0;
  final double duration;
  final VoidCallback onComplete;
  
  @override
  void update(double dt) {
    _elapsed += dt;
    if (_elapsed >= duration) {
      onComplete();
      removeFromParent();
    }
  }
}
```

---

## Related Documentation

- **50-architecture-overview.md** - Why Flame from day 1
- **56-card-physics-animations.md** - I/O FLIP drag physics
- **57-component-architecture.md** - Component patterns
- **58-camera-viewport-systems.md** - Camera control
- **59-performance-optimization-flame.md** - Performance
- **62-flame-integration.md** - Package setup

---

## Quick Reference

### FlameGame Template

```dart
class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    // Setup camera
    camera = CameraComponent.withFixedResolution(width: 1920, height: 1080);
    
    // Load assets
    await images.loadAll(['sprite.png']);
    
    // Add components
    world.add(MyComponent());
  }
  
  @override
  void update(double dt) {
    super.update(dt);
    // Game logic
  }
}
```

### Component Template

```dart
class MyComponent extends PositionComponent with DragCallbacks {
  @override
  Future<void> onLoad() async {
    // Setup
  }
  
  @override
  void update(double dt) {
    // Update logic
  }
  
  @override
  void render(Canvas canvas) {
    super.render(canvas);
    // Custom rendering
  }
}
```

---

**Status:** ✅ Flame Fundamentals Complete  
**Next:** Study `56-card-physics-animations.md` for I/O FLIP patterns  
**Resources:** https://docs.flame-engine.org/

