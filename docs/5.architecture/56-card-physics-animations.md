# Card Physics & Animations

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete  
**Source:** I/O FLIP (Google I/O 2023)

---

## Overview

Complete breakdown of I/O FLIP's momentum-based card drag physics and how to implement it in Unwritten for a Unity-like game feel.

**Key Features:**
- Velocity-based dragging
- Momentum on release (throw physics)
- Friction and deceleration
- Snap-back animations
- Drop zone detection

---

## Physics Constants

### From I/O FLIP Analysis

```dart
// features/cards/presentation/components/card_physics_config.dart
class CardPhysicsConfig {
  // Friction coefficient (energy retention per frame)
  static const double friction = 0.95; // Loses 5% velocity per frame
  
  // Throw multiplier (amplify release velocity)
  static const double throwMultiplier = 1.8;
  
  // Snap-back speed (pixels per second)
  static const double snapBackSpeed = 1200.0;
  
  // Minimum velocity threshold (stop below this)
  static const double minVelocity = 1.0;
  
  // Bounce coefficient (energy retention on collision)
  static const double bounceCoefficient = 0.5; // Loses 50% on bounce
  
  // Drop zone detection (AABB tolerance)
  static const double dropZoneTolerance = 20.0;
  
  // Hover scale (card grows on hover)
  static const double hoverScale = 1.1;
  
  // Hover animation duration
  static const double hoverDuration = 0.2;
}
```

---

## Drag Physics Implementation

### Complete CardGameComponent

```dart
// features/cards/presentation/components/card_game_component.dart
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/effects.dart';
import 'package:flutter/material.dart';
import 'dart:math';

class CardGameComponent extends PositionComponent 
    with DragCallbacks, TapCallbacks, HoverCallbacks, HasGameRef {
  
  final Card card;
  final void Function(String cardId) onPlay;
  
  // Physics state
  Vector2 velocity = Vector2.zero();
  Vector2 acceleration = Vector2.zero();
  Vector2 startPosition = Vector2.zero();
  Vector2 dragStartPosition = Vector2.zero();
  Vector2 lastPosition = Vector2.zero();
  double lastUpdateTime = 0;
  
  // Drag state
  bool isDragging = false;
  bool isHovering = false;
  bool isAnimating = false;
  
  // Sprite components
  late SpriteComponent cardSprite;
  late TextComponent titleText;
  
  CardGameComponent({
    required this.card,
    required this.onPlay,
    Vector2? position,
  }) : super(
    position: position ?? Vector2.zero(),
    size: Vector2(200, 300),
    anchor: Anchor.bottomCenter, // I/O FLIP: pivot at bottom-middle
  );
  
  @override
  Future<void> onLoad() async {
    await super.onLoad();
    
    // Load card sprite
    final sprite = await gameRef.loadSprite('cards/${card.id}.png');
    cardSprite = SpriteComponent(
      sprite: sprite,
      size: size,
      anchor: Anchor.topLeft,
    );
    add(cardSprite);
    
    // Add title
    titleText = TextComponent(
      text: card.title,
      position: Vector2(size.x / 2, 20),
      anchor: Anchor.topCenter,
      textRenderer: TextPaint(
        style: const TextStyle(
          color: Colors.white,
          fontSize: 18,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
    add(titleText);
    
    // Store initial position
    startPosition = position.clone();
    lastPosition = position.clone();
  }
  
  @override
  void update(double dt) {
    super.update(dt);
    
    if (!isDragging && !isAnimating) {
      // Apply velocity (momentum)
      position += velocity * dt;
      
      // Apply friction
      velocity *= CardPhysicsConfig.friction;
      
      // Stop if velocity too small
      if (velocity.length < CardPhysicsConfig.minVelocity) {
        velocity.setZero();
      }
      
      // Check bounds collision
      _checkBoundsCollision();
    }
    
    lastPosition = position.clone();
    lastUpdateTime = dt;
  }
  
  @override
  void onDragStart(DragStartEvent event) {
    isDragging = true;
    isAnimating = false;
    velocity.setZero();
    dragStartPosition = position.clone();
    lastPosition = position.clone();
    
    // Bring to front
    priority = 100;
    
    // Play haptic feedback
    HapticFeedback.lightImpact();
    
    // Play sound
    AudioService.playSfx('card_grab');
    
    // Remove any active effects
    removeWhere((component) => component is Effect);
  }
  
  @override
  void onDragUpdate(DragUpdateEvent event) {
    // Move card
    position += event.localDelta;
    
    // Calculate velocity (for momentum)
    if (event.dt > 0) {
      velocity = event.localDelta / event.dt;
    }
  }
  
  @override
  void onDragEnd(DragEndEvent event) {
    isDragging = false;
    priority = 0;
    
    // Apply throw multiplier (I/O FLIP pattern)
    velocity *= CardPhysicsConfig.throwMultiplier;
    
    // Check if dropped on drop zone
    final dropZone = _findDropZone();
    if (dropZone != null) {
      _playCard(dropZone);
    } else {
      _snapBack();
    }
    
    // Play release sound
    AudioService.playSfx('card_release');
  }
  
  @override
  void onHoverEnter() {
    if (!isDragging) {
      isHovering = true;
      
      // Grow card (I/O FLIP pattern)
      add(ScaleEffect.to(
        Vector2.all(CardPhysicsConfig.hoverScale),
        EffectController(
          duration: CardPhysicsConfig.hoverDuration,
          curve: Curves.easeOut,
        ),
      ));
      
      // Lift up slightly
      add(MoveEffect.by(
        Vector2(0, -10),
        EffectController(
          duration: CardPhysicsConfig.hoverDuration,
          curve: Curves.easeOut,
        ),
      ));
      
      HapticFeedback.selectionClick();
    }
  }
  
  @override
  void onHoverExit() {
    if (isHovering) {
      isHovering = false;
      
      // Shrink back
      add(ScaleEffect.to(
        Vector2.all(1.0),
        EffectController(
          duration: CardPhysicsConfig.hoverDuration,
          curve: Curves.easeIn,
        ),
      ));
      
      // Lower back
      add(MoveEffect.by(
        Vector2(0, 10),
        EffectController(
          duration: CardPhysicsConfig.hoverDuration,
          curve: Curves.easeIn,
        ),
      ));
    }
  }
  
  // Snap back to start position with momentum
  void _snapBack() {
    isAnimating = true;
    
    // Calculate direction and distance
    final direction = (startPosition - position).normalized();
    final distance = position.distanceTo(startPosition);
    
    // Set velocity for smooth return
    velocity = direction * CardPhysicsConfig.snapBackSpeed;
    
    // Or use effect for more control
    add(MoveEffect.to(
      startPosition,
      EffectController(
        duration: min(distance / CardPhysicsConfig.snapBackSpeed, 0.5),
        curve: Curves.easeOut,
      ),
      onComplete: () {
        isAnimating = false;
        velocity.setZero();
      },
    ));
    
    HapticFeedback.mediumImpact();
    AudioService.playSfx('card_snapback');
  }
  
  // Find drop zone under card
  DropZoneComponent? _findDropZone() {
    final zones = gameRef.world.children.whereType<DropZoneComponent>();
    
    for (final zone in zones) {
      // AABB collision detection
      if (_isOverlapping(zone)) {
        return zone;
      }
    }
    
    return null;
  }
  
  bool _isOverlapping(DropZoneComponent zone) {
    final cardRect = toRect();
    final zoneRect = zone.toRect();
    
    // Check overlap with tolerance
    return cardRect.overlaps(zoneRect.inflate(
      CardPhysicsConfig.dropZoneTolerance,
    ));
  }
  
  // Play card on drop zone
  void _playCard(DropZoneComponent zone) {
    isAnimating = true;
    
    // Animate to zone center
    add(MoveEffect.to(
      zone.position,
      EffectController(duration: 0.3, curve: Curves.easeOut),
      onComplete: () {
        // Trigger callback (to Riverpod)
        onPlay(card.id);
        
        // Remove card with fade effect
        add(OpacityEffect.fadeOut(
          EffectController(duration: 0.2),
          onComplete: () => removeFromParent(),
        ));
      },
    ));
    
    // Scale down
    add(ScaleEffect.to(
      Vector2.all(0.8),
      EffectController(duration: 0.3, curve: Curves.easeOut),
    ));
    
    HapticFeedback.heavyImpact();
    AudioService.playSfx('card_play');
  }
  
  // Bounce off screen bounds
  void _checkBoundsCollision() {
    final worldBounds = gameRef.camera.visibleWorldRect;
    
    // Left/right bounds
    if (position.x < worldBounds.left) {
      position.x = worldBounds.left;
      velocity.x *= -CardPhysicsConfig.bounceCoefficient;
      HapticFeedback.lightImpact();
    } else if (position.x > worldBounds.right) {
      position.x = worldBounds.right;
      velocity.x *= -CardPhysicsConfig.bounceCoefficient;
      HapticFeedback.lightImpact();
    }
    
    // Top/bottom bounds
    if (position.y < worldBounds.top) {
      position.y = worldBounds.top;
      velocity.y *= -CardPhysicsConfig.bounceCoefficient;
      HapticFeedback.lightImpact();
    } else if (position.y > worldBounds.bottom) {
      position.y = worldBounds.bottom;
      velocity.y *= -CardPhysicsConfig.bounceCoefficient;
      HapticFeedback.lightImpact();
    }
  }
}
```

---

## Drop Zone Component

```dart
// features/cards/presentation/components/drop_zone_component.dart
enum DropZoneType { play, discard }

class DropZoneComponent extends RectangleComponent with HasGameRef {
  final DropZoneType type;
  bool isHighlighted = false;
  
  DropZoneComponent({
    required this.type,
    required Vector2 position,
    required Vector2 size,
  }) : super(
    position: position,
    size: size,
    anchor: Anchor.center,
    paint: Paint()
      ..color = Colors.blue.withOpacity(0.3)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 4,
  );
  
  @override
  void update(double dt) {
    super.update(dt);
    
    // Check if any card is over this zone
    final cardsOver = gameRef.world.children
        .whereType<CardGameComponent>()
        .where((card) => card.isDragging && _isCardOver(card))
        .isNotEmpty;
    
    if (cardsOver && !isHighlighted) {
      _highlight();
    } else if (!cardsOver && isHighlighted) {
      _unhighlight();
    }
  }
  
  bool _isCardOver(CardGameComponent card) {
    return toRect().overlaps(card.toRect());
  }
  
  void _highlight() {
    isHighlighted = true;
    paint.color = Colors.green.withOpacity(0.5);
    add(ScaleEffect.to(
      Vector2.all(1.1),
      EffectController(duration: 0.2, curve: Curves.easeOut),
    ));
    HapticFeedback.selectionClick();
  }
  
  void _unhighlight() {
    isHighlighted = false;
    paint.color = Colors.blue.withOpacity(0.3);
    add(ScaleEffect.to(
      Vector2.all(1.0),
      EffectController(duration: 0.2, curve: Curves.easeIn),
    ));
  }
}
```

---

## Animation Effects Library

### Particle Effects

```dart
// features/cards/presentation/components/card_effects.dart
import 'package:flame/particles.dart';

class CardEffects {
  // Play sparkles when card played
  static ParticleSystemComponent playSparkles(Vector2 position) {
    return ParticleSystemComponent(
      particle: Particle.generate(
        count: 20,
        lifespan: 0.5,
        generator: (i) => AcceleratedParticle(
          speed: Vector2.random() * 200,
          acceleration: Vector2(0, 400),
          child: CircleParticle(
            radius: 3,
            paint: Paint()..color = Colors.yellow.withOpacity(0.8),
          ),
        ),
      ),
      position: position,
    );
  }
  
  // Hover glow effect
  static Component hoverGlow() {
    return CircleComponent(
      radius: 150,
      paint: Paint()
        ..color = Colors.white.withOpacity(0.2)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 30),
      anchor: Anchor.center,
    );
  }
}
```

### Shake Effect

```dart
class ShakeEffect extends Effect with EffectTarget<PositionComponent> {
  final double intensity;
  final Vector2 originalPosition;
  
  ShakeEffect({
    required this.intensity,
    required EffectController controller,
  }) : originalPosition = Vector2.zero(),
       super(controller);
  
  @override
  void onStart() {
    super.onStart();
    originalPosition.setFrom(target.position);
  }
  
  @override
  void apply(double progress) {
    final shake = Vector2.random() * intensity * (1 - progress);
    target.position = originalPosition + shake;
  }
}

// Usage
card.add(ShakeEffect(
  intensity: 10,
  controller: EffectController(duration: 0.3),
));
```

---

## Performance Tips

### 1. Component Pooling

```dart
class CardPool {
  final List<CardGameComponent> _available = [];
  
  CardGameComponent get(Card card, void Function(String) onPlay) {
    if (_available.isNotEmpty) {
      final component = _available.removeLast();
      component.card = card;
      component.onPlay = onPlay;
      return component;
    }
    return CardGameComponent(card: card, onPlay: onPlay);
  }
  
  void release(CardGameComponent component) {
    component.removeFromParent();
    _available.add(component);
  }
}
```

### 2. Sprite Atlas

```dart
// Load all cards as sprite atlas
final atlas = await gameRef.images.load('cards_atlas.png');
final spriteSheet = SpriteSheet(
  image: atlas,
  srcSize: Vector2(200, 300),
);

// Get sprite by index (much faster)
final cardSprite = spriteSheet.getSprite(row, col);
```

### 3. Limit Active Effects

```dart
@override
void onDragStart(DragStartEvent event) {
  // Remove previous effects before adding new
  removeWhere((component) => component is Effect);
  
  // Now add new effect
  add(ScaleEffect.to(/* ... */));
}
```

---

## Related Documentation

- **55-flame-engine-fundamentals.md** - Flame basics
- **57-component-architecture.md** - Component patterns
- **59-performance-optimization-flame.md** - Optimization
- **63-audio-haptics-integration.md** - Audio/haptic feedback

---

## Quick Reference

### Physics Formula

```
velocity = dragDelta / deltaTime
position = position + (velocity * deltaTime * throwMultiplier)
velocity = velocity * friction
```

### Key Constants

```dart
friction = 0.95           // 5% loss per frame
throwMultiplier = 1.8     // Amplify release
snapBackSpeed = 1200      // pixels/second
minVelocity = 1.0         // Stop threshold
bounceCoefficient = 0.5   // 50% bounce
```

---

**Status:** ✅ Card Physics Complete  
**Source:** I/O FLIP Reference Implementation  
**Feel:** Unity-like Momentum Physics

