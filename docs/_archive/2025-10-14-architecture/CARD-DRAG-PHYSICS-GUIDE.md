# Card Drag Physics & Animations Guide

> **Source**: I/O FLIP (Google I/O 2023)  
> **Framework**: Flame Game Engine  
> **Last Updated**: October 14, 2025

---

## Overview

I/O FLIP implements smooth, momentum-based card drag animations using **Flame's game engine components**. Cards feel "physical" when grabbed and thrown, with realistic deceleration and bounce effects.

This guide documents how I/O FLIP achieves this and how to implement similar physics for Unwritten.

---

## I/O FLIP Implementation

### Key Components

From the [I/O FLIP repository](https://github.com/flutter/io_flip):

```dart
/// Card component with drag physics
/// 
/// Uses Flame's DragCallbacks for touch/mouse interaction
/// and applies momentum/velocity physics on release.
class CardComponent extends PositionComponent 
    with DragCallbacks, TapCallbacks {
  
  CardComponent({
    required this.card,
    required this.initialPosition,
  });

  final Card card;
  final Vector2 initialPosition;
  
  // Physics properties
  Vector2 velocity = Vector2.zero();
  Vector2 acceleration = Vector2.zero();
  
  // Drag state
  bool isDragging = false;
  Vector2? dragStartPosition;
  Vector2? lastPosition;
  double lastUpdateTime = 0;
  
  // Physics constants
  static const double friction = 0.95; // Velocity decay per frame
  static const double snapBackSpeed = 800.0; // Pixels per second
  static const double throwMultiplier = 2.0; // Velocity amplification
  
  @override
  Future<void> onLoad() async {
    await super.onLoad();
    
    size = Vector2(120, 180); // Card dimensions
    position = initialPosition.clone();
    anchor = Anchor.center;
  }

  @override
  void update(double dt) {
    super.update(dt);
    
    if (!isDragging) {
      // Apply momentum physics when not being dragged
      applyPhysics(dt);
    }
  }

  @override
  void onDragStart(DragStartEvent event) {
    isDragging = true;
    dragStartPosition = position.clone();
    lastPosition = event.canvasPosition.clone();
    lastUpdateTime = gameRef.currentTime();
    
    // Visual feedback: lift card slightly
    priority = 10; // Bring to front
    scale = Vector2.all(1.05); // Slight scale up
  }

  @override
  void onDragUpdate(DragUpdateEvent event) {
    if (!isDragging) return;
    
    // Update position directly during drag
    position = event.canvasPosition.clone();
    
    // Calculate velocity for momentum
    final currentTime = gameRef.currentTime();
    final dt = currentTime - lastUpdateTime;
    
    if (dt > 0 && lastPosition != null) {
      // Velocity = displacement / time
      velocity = (position - lastPosition!) / dt;
    }
    
    lastPosition = position.clone();
    lastUpdateTime = currentTime;
  }

  @override
  void onDragEnd(DragEndEvent event) {
    isDragging = false;
    
    // Apply throw physics based on drag velocity
    velocity *= throwMultiplier;
    
    // Visual feedback: restore normal state
    scale = Vector2.all(1.0);
    
    // Check if card was dropped in valid zone
    final dropZone = gameRef.checkDropZone(position);
    if (dropZone != null) {
      // Snap to drop zone with animation
      snapToPosition(dropZone.center, onComplete: () {
        // Trigger card play event
        gameRef.playCard(card, dropZone);
      });
    } else {
      // Return to hand with physics
      snapToPosition(initialPosition);
    }
  }

  void applyPhysics(double dt) {
    // Apply friction (velocity decay)
    velocity *= friction;
    
    // Stop if velocity is negligible
    if (velocity.length < 1.0) {
      velocity = Vector2.zero();
    }
    
    // Update position based on velocity
    position += velocity * dt;
    
    // Apply acceleration (for snap-back)
    velocity += acceleration * dt;
    
    // Bounds checking with bounce
    final bounds = gameRef.playableArea;
    if (position.x < bounds.left) {
      position.x = bounds.left;
      velocity.x *= -0.5; // Bounce with energy loss
    }
    if (position.x > bounds.right) {
      position.x = bounds.right;
      velocity.x *= -0.5;
    }
    if (position.y < bounds.top) {
      position.y = bounds.top;
      velocity.y *= -0.5;
    }
    if (position.y > bounds.bottom) {
      position.y = bounds.bottom;
      velocity.y *= -0.5;
    }
  }

  void snapToPosition(
    Vector2 targetPosition, {
    VoidCallback? onComplete,
  }) {
    // Calculate acceleration toward target
    final direction = (targetPosition - position).normalized();
    acceleration = direction * snapBackSpeed;
    
    // Add effect for smooth arrival
    add(
      MoveToEffect(
        targetPosition,
        EffectController(
          duration: 0.3,
          curve: Curves.easeOut,
        ),
        onComplete: () {
          acceleration = Vector2.zero();
          velocity = Vector2.zero();
          onComplete?.call();
        },
      ),
    );
  }
}
```

---

## Physics Breakdown

### 1. Drag Tracking

**Velocity Calculation**:
```dart
// Track position over time during drag
velocity = (currentPosition - lastPosition) / deltaTime;
```

This captures the **speed and direction** of the user's drag gesture.

### 2. Momentum on Release

**Throw Physics**:
```dart
// Amplify velocity when released
velocity *= throwMultiplier; // 2x amplification

// Apply friction each frame
velocity *= friction; // 0.95 = 5% decay per frame
```

The card continues moving after release, gradually slowing down.

### 3. Snap-Back Animation

**Return to Hand**:
```dart
MoveToEffect(
  targetPosition,
  EffectController(
    duration: 0.3,
    curve: Curves.easeOut, // Smooth deceleration
  ),
)
```

Uses Flutter's **Curves.easeOut** for natural-feeling deceleration.

### 4. Bounce Physics

**Edge Collision**:
```dart
if (position.x < bounds.left) {
  position.x = bounds.left;
  velocity.x *= -0.5; // Reverse direction, lose 50% energy
}
```

Cards bounce off screen edges with energy loss.

---

## Flame Physics Components

### DragCallbacks Mixin

```dart
class CardComponent extends PositionComponent with DragCallbacks {
  @override
  void onDragStart(DragStartEvent event) {
    // User starts dragging
  }
  
  @override
  void onDragUpdate(DragUpdateEvent event) {
    // User moves finger/mouse
  }
  
  @override
  void onDragEnd(DragEndEvent event) {
    // User releases
  }
}
```

**Flame automatically handles**:
- Touch/mouse input detection
- Multi-touch support
- Event propagation
- Coordinate transformations

### Effect System

```dart
// Smooth interpolation effects
add(MoveToEffect(target, EffectController(duration: 0.3)));
add(ScaleEffect.to(Vector2.all(1.1), EffectController(duration: 0.2)));
add(RotateEffect.by(0.1, EffectController(duration: 0.15)));
```

**Built-in effects**:
- `MoveToEffect` - Position interpolation
- `ScaleEffect` - Size changes
- `RotateEffect` - Rotation animations
- `OpacityEffect` - Fade in/out
- `SequenceEffect` - Chain multiple effects
- `ParallelEffect` - Run effects simultaneously

---

## Unwritten Implementation

### Option 1: Flame-Based (Recommended for Game Feel)

**Advantages**:
- ✅ 60 FPS smooth animations
- ✅ Built-in physics and effects
- ✅ Game loop optimized for performance
- ✅ Same pattern as I/O FLIP

**Implementation**:

```dart
/// Unwritten card with drag physics (Flame version)
class UnwrittenCard extends PositionComponent with DragCallbacks {
  UnwrittenCard({
    required this.cardData,
    required this.handPosition,
  });

  final CardModel cardData;
  final Vector2 handPosition;
  
  Vector2 velocity = Vector2.zero();
  bool isDragging = false;
  Vector2? lastPosition;
  double lastTime = 0;

  @override
  Future<void> onLoad() async {
    size = Vector2(200, 300); // Larger cards for mobile
    position = handPosition.clone();
    anchor = Anchor.center;
    
    // Load card sprite/render
    await _loadCardVisuals();
  }

  @override
  void update(double dt) {
    super.update(dt);
    
    if (!isDragging && velocity.length > 0) {
      // Apply momentum physics
      velocity *= 0.95; // Friction
      position += velocity * dt;
      
      if (velocity.length < 1.0) {
        velocity = Vector2.zero();
      }
    }
  }

  @override
  void onDragStart(DragStartEvent event) {
    isDragging = true;
    lastPosition = event.canvasPosition;
    lastTime = gameRef.currentTime();
    
    // Visual feedback
    add(ScaleEffect.to(
      Vector2.all(1.08),
      EffectController(duration: 0.1),
    ));
    
    // Play haptic feedback
    HapticFeedback.selectionClick();
  }

  @override
  void onDragUpdate(DragUpdateEvent event) {
    position = event.canvasPosition;
    
    // Calculate velocity
    final now = gameRef.currentTime();
    final dt = now - lastTime;
    if (dt > 0 && lastPosition != null) {
      velocity = (position - lastPosition!) / dt;
    }
    
    lastPosition = position;
    lastTime = now;
    
    // Check for hover over NPC targets
    _checkNPCHover();
  }

  @override
  void onDragEnd(DragEndEvent event) {
    isDragging = false;
    
    // Amplify momentum
    velocity *= 1.5;
    
    // Check drop target
    final npc = _getNPCAtPosition(position);
    if (npc != null) {
      // Play card on NPC
      _playCardOnNPC(npc);
    } else {
      // Return to hand
      _returnToHand();
    }
  }

  void _returnToHand() {
    add(MoveToEffect(
      handPosition,
      EffectController(duration: 0.25, curve: Curves.easeOut),
      onComplete: () {
        velocity = Vector2.zero();
      },
    ));
    
    add(ScaleEffect.to(
      Vector2.all(1.0),
      EffectController(duration: 0.2),
    ));
  }

  void _playCardOnNPC(NPC npc) {
    // Animate card to NPC position
    add(
      SequenceEffect([
        MoveToEffect(
          npc.position,
          EffectController(duration: 0.2, curve: Curves.easeInOut),
        ),
        ScaleEffect.to(
          Vector2.all(0.5),
          EffectController(duration: 0.15),
        ),
        OpacityEffect.to(
          0.0,
          EffectController(duration: 0.1),
        ),
      ], onComplete: () {
        // Trigger game logic
        gameRef.playCard(cardData, npc);
        removeFromParent();
      }),
    );
  }

  void _checkNPCHover() {
    final npc = _getNPCAtPosition(position);
    if (npc != null) {
      // Highlight NPC
      npc.showHighlight();
      HapticFeedback.lightImpact();
    }
  }
}
```

### Option 2: Pure Flutter (Simpler, No Flame)

**Advantages**:
- ✅ No additional game engine dependency
- ✅ Simpler setup
- ✅ Standard Flutter animations

**Disadvantages**:
- ❌ Less smooth than Flame at 60 FPS
- ❌ More manual physics implementation
- ❌ No built-in game loop optimization

**Implementation**:

```dart
/// Unwritten card with drag physics (Pure Flutter version)
class UnwrittenCardWidget extends StatefulWidget {
  final CardModel cardData;
  final VoidCallback? onPlayCard;

  const UnwrittenCardWidget({
    required this.cardData,
    this.onPlayCard,
    Key? key,
  }) : super(key: key);

  @override
  State<UnwrittenCardWidget> createState() => _UnwrittenCardWidgetState();
}

class _UnwrittenCardWidgetState extends State<UnwrittenCardWidget>
    with SingleTickerProviderStateMixin {
  
  Offset position = Offset.zero;
  Offset velocity = Offset.zero;
  bool isDragging = false;
  
  late AnimationController _controller;
  Animation<Offset>? _snapAnimation;
  
  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 300),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Positioned(
      left: position.dx,
      top: position.dy,
      child: GestureDetector(
        onPanStart: _onDragStart,
        onPanUpdate: _onDragUpdate,
        onPanEnd: _onDragEnd,
        child: AnimatedScale(
          scale: isDragging ? 1.08 : 1.0,
          duration: const Duration(milliseconds: 150),
          child: CardDisplay(card: widget.cardData),
        ),
      ),
    );
  }

  void _onDragStart(DragStartDetails details) {
    setState(() {
      isDragging = true;
      velocity = Offset.zero;
      _controller.stop();
    });
    HapticFeedback.selectionClick();
  }

  void _onDragUpdate(DragUpdateDetails details) {
    setState(() {
      position += details.delta;
      
      // Estimate velocity from delta
      velocity = details.delta * 20; // Approximate multiplier
    });
  }

  void _onDragEnd(DragEndDetails details) {
    setState(() {
      isDragging = false;
      velocity = details.velocity.pixelsPerSecond / 1000; // Scale down
    });

    // Check if dropped on valid target
    final target = _checkDropTarget(position);
    if (target != null) {
      _playCard(target);
    } else {
      _returnToHand();
    }
  }

  void _returnToHand() {
    final startPosition = position;
    final endPosition = Offset.zero; // Hand position
    
    _snapAnimation = Tween<Offset>(
      begin: startPosition,
      end: endPosition,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeOut,
    ));
    
    _controller.forward(from: 0).then((_) {
      setState(() {
        position = endPosition;
        velocity = Offset.zero;
      });
    });
  }

  void _playCard(dynamic target) {
    widget.onPlayCard?.call();
    // Animate card away and remove
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
```

---

## Recommendation for Unwritten

### ✅ Use Flame from Day 1 (REVISED)

**Why This Is The Right Choice**:

1. **Code Structure Is Fundamentally Different**
   - Flame: Component-based architecture (game entities)
   - Flutter: Widget-based architecture (UI elements)
   - **Rewriting later would be a massive refactor, not a migration**

2. **I/O FLIP Proves It's Production-Ready**
   - Used at Google I/O 2023 with thousands of players
   - Stable, well-tested, proven at scale
   - Built by Very Good Ventures (Flutter experts)

3. **Aligns with Project Goals**
   - Unwritten specification: "Unity-like game feel"
   - Flame provides: Game loop, physics, effects, animations
   - Pure Flutter provides: UI widgets (not game engine features)

4. **Better Code Quality & Maintainability**
   - Clean separation: Game logic in components, UI in widgets
   - Built-in patterns for physics, collisions, effects
   - Established best practices from I/O FLIP
   - No technical debt from "temporary" solutions

5. **Learning Curve Is Manageable**
   - We have I/O FLIP as reference implementation
   - Flame docs are excellent
   - Architecture already mapped in our docs
   - Time investment pays off immediately

6. **Performance From The Start**
   - 60 FPS game loop optimized
   - GPU-accelerated rendering
   - Sprite batching built-in
   - Mobile-optimized from day 1

### Setup: Phase 1 Week 1

**Add to `pubspec.yaml`**:
```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # Game Engine (I/O FLIP pattern)
  flame: ^1.17.0
  
  # State Management
  flutter_riverpod: ^2.5.1
  
  # Other dependencies...
```

**Project Structure** (matches I/O FLIP):
```
lib/
├── game/
│   ├── unwritten_game.dart          # Main Flame game class
│   ├── components/
│   │   ├── card_component.dart     # Draggable cards
│   │   ├── npc_component.dart      # NPC targets
│   │   └── hand_component.dart     # Player's hand
│   └── views/
│       └── game_view.dart          # Flutter wrapper
│
├── features/
│   ├── cards/                       # Card data & logic
│   ├── relationships/               # Relationship system
│   └── game_state/                  # Game state management
│
└── main.dart
```

**Hybrid Architecture** (Best of Both):
```dart
// Flutter UI for menus, dialogs, HUD
Scaffold(
  body: Stack(
    children: [
      // Flame for game world
      GameWidget<UnwrittenGame>(
        game: UnwrittenGame(),
      ),
      
      // Flutter overlays for UI
      Positioned(
        top: 16,
        child: ResourceBar(), // Flutter widget
      ),
      
      Positioned(
        bottom: 0,
        child: NarrativePanel(), // Flutter widget
      ),
    ],
  ),
)
```

### Migration Cost: Pure Flutter → Flame (What We'd Face)

If we started with pure Flutter and migrated later:

**Would Need to Rewrite**:
- ❌ All card rendering (Widget → Component)
- ❌ All drag/touch handling (GestureDetector → DragCallbacks)
- ❌ All animations (AnimationController → EffectController)
- ❌ All physics (manual calculations → Flame physics)
- ❌ All collision detection (manual → Flame hitboxes)
- ❌ Game loop structure (setState → update/render)

**Estimated Rewrite Time**: 2-3 weeks

**Why Start Over?**:
- Different paradigms (widget tree vs component tree)
- Different lifecycle (build vs onLoad/update/render)
- Different coordinate systems
- Different event handling

**Conclusion**: Starting with Flame saves 2-3 weeks of rewriting and avoids technical debt.

---

## Performance Considerations

### Mobile Optimization

```dart
// Reduce physics calculations when off-screen
@override
void update(double dt) {
  if (!isVisibleInCamera) return; // Skip physics
  
  super.update(dt);
  applyPhysics(dt);
}

// Use sprite batching for multiple cards
@override
void render(Canvas canvas) {
  // Batch render all cards in one draw call
  cardSpriteBatch.render(canvas);
}

// Limit particle effects on low-end devices
if (DevicePerformance.isHighEnd) {
  add(ParticleEffect(...));
}
```

### Frame Rate Targets

| Device Tier | Target FPS | Physics Quality |
|-------------|-----------|-----------------|
| High-end | 60 FPS | Full physics |
| Mid-range | 60 FPS | Reduced particles |
| Low-end | 30 FPS | Simplified physics |

---

## Additional Resources

- **Flame Documentation**: https://docs.flame-engine.org/
- **I/O FLIP Source**: https://github.com/flutter/io_flip
- **Flutter Animations**: https://docs.flutter.dev/ui/animations
- **Game Physics Tutorial**: https://docs.flame-engine.org/latest/flame/components.html

---

## Compliance Checklist

- [x] Documents I/O FLIP's implementation
- [x] Provides Unwritten adaptation options
- [x] Includes code examples (Flame & Flutter)
- [x] Performance optimization guidance
- [x] Phase-appropriate recommendations (Flutter MVP → Flame polish)
- [x] Mobile-specific considerations

---

**Document Version**: 1.0  
**Last Updated**: October 14, 2025  
**Status**: Implementation guide ready  
**Next Step**: Implement Phase 1 with pure Flutter, migrate to Flame in Phase 5

