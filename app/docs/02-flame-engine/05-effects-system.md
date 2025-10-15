# Effects System

**Reference:** `docs/master_flutter_flame_spec_v_1_0.md` (Lines 221-257)

## Overview

Flame's effects system provides built-in animations for move, scale, rotate, and opacity. These are essential for card animations, providing smooth, performant transitions without custom animation code.

## Built-in Effects

### MoveEffect - Card Movement

```dart
class MovingCard extends PositionComponent {
  void moveToPosition(Vector2 targetPosition) {
    add(MoveEffect.to(
      targetPosition,
      EffectController(duration: 0.5, curve: Curves.easeOut),
    ));
  }
  
  void moveBy(Vector2 offset) {
    add(MoveEffect.by(
      offset,
      EffectController(duration: 0.3),
    ));
  }
  
  // Card draw from deck
  void drawFromDeck(Vector2 deckPosition, Vector2 handPosition) {
    position = deckPosition;
    add(MoveEffect.to(
      handPosition,
      EffectController(duration: 0.6, curve: Curves.easeOutCubic),
    ));
  }
}
```

### ScaleEffect - Card Scaling

```dart
class ScalableCard extends PositionComponent {
  void scaleUp() {
    add(ScaleEffect.to(
      Vector2.all(1.5),
      EffectController(duration: 0.2, curve: Curves.easeOut),
    ));
  }
  
  void scaleDown() {
    add(ScaleEffect.to(
      Vector2.all(1.0),
      EffectController(duration: 0.2, curve: Curves.easeIn),
    ));
  }
  
  void scaleBy(double factor) {
    add(ScaleEffect.by(
      Vector2.all(factor),
      EffectController(duration: 0.15),
    ));
  }
  
  // Pulse effect for emphasis
  void pulse() {
    add(SequenceEffect([
      ScaleEffect.by(Vector2.all(1.1), EffectController(duration: 0.1)),
      ScaleEffect.by(Vector2.all(0.909), EffectController(duration: 0.1)),
    ]));
  }
}
```

### RotateEffect - Card Rotation

```dart
class RotatingCard extends PositionComponent {
  void rotateToAngle(double angleRadians) {
    add(RotateEffect.to(
      angleRadians,
      EffectController(duration: 0.3, curve: Curves.easeInOut),
    ));
  }
  
  void rotateBy(double deltaRadians) {
    add(RotateEffect.by(
      deltaRadians,
      EffectController(duration: 0.2),
    ));
  }
  
  // Spin effect
  void spin() {
    add(RotateEffect.by(
      2 * math.pi,  // Full rotation
      EffectController(duration: 0.5, curve: Curves.easeInOut),
    ));
  }
  
  // Fan layout rotation
  void rotateTo FanPosition(int cardIndex, int totalCards) {
    final angle = _calculateFanAngle(cardIndex, totalCards);
    add(RotateEffect.to(
      angle,
      EffectController(duration: 0.4, curve: Curves.easeOut),
    ));
  }
}
```

### OpacityEffect - Card Fade

```dart
class FadingCard extends PositionComponent {
  void fadeIn() {
    opacity = 0;
    add(OpacityEffect.fadeIn(
      EffectController(duration: 0.3),
    ));
  }
  
  void fadeOut() {
    add(OpacityEffect.fadeOut(
      EffectController(duration: 0.3),
    ));
  }
  
  void fadeTo(double targetOpacity) {
    add(OpacityEffect.to(
      targetOpacity,
      EffectController(duration: 0.2),
    ));
  }
  
  // Fade and remove
  void fadeOutAndRemove() {
    add(OpacityEffect.fadeOut(
      EffectController(duration: 0.5),
      onComplete: () => removeFromParent(),
    ));
  }
}
```

## Effect Chaining

### SequenceEffect - Sequential Animations

```dart
class AnimatedCard extends PositionComponent {
  void playCardSequence(Vector2 targetPosition) {
    add(SequenceEffect([
      // 1. Scale up
      ScaleEffect.to(
        Vector2.all(1.2),
        EffectController(duration: 0.2),
      ),
      // 2. Move to position
      MoveEffect.to(
        targetPosition,
        EffectController(duration: 0.4, curve: Curves.easeInOut),
      ),
      // 3. Scale down
      ScaleEffect.to(
        Vector2.all(1.0),
        EffectController(duration: 0.2),
      ),
      // 4. Flash
      OpacityEffect.to(
        0.5,
        EffectController(duration: 0.1),
      ),
      OpacityEffect.to(
        1.0,
        EffectController(duration: 0.1),
      ),
    ]));
  }
  
  void drawCardSequence() {
    add(SequenceEffect([
      OpacityEffect.fadeIn(EffectController(duration: 0.1)),
      ScaleEffect.to(Vector2.all(0.8), EffectController(duration: 0.1)),
      ScaleEffect.to(Vector2.all(1.0), EffectController(duration: 0.2)),
    ]));
  }
}
```

### CombinedEffect - Parallel Animations

```dart
class CardPlayEffect extends PositionComponent {
  void playCard(Vector2 targetPosition) {
    add(CombinedEffect([
      // All happen at same time
      MoveEffect.to(
        targetPosition,
        EffectController(duration: 0.5, curve: Curves.easeOut),
      ),
      ScaleEffect.to(
        Vector2.all(1.5),
        EffectController(duration: 0.5, curve: Curves.easeOut),
      ),
      RotateEffect.by(
        math.pi / 4,
        EffectController(duration: 0.5),
      ),
      OpacityEffect.to(
        0.8,
        EffectController(duration: 0.5),
      ),
    ]));
  }
}
```

## Custom EffectController

### Easing Curves

```dart
class CardWithEasing extends PositionComponent {
  void animateWithEasing() {
    // Elastic bounce
    add(ScaleEffect.to(
      Vector2.all(1.2),
      EffectController(
        duration: 0.5,
        curve: Curves.elasticOut,  // ✅ Bouncy effect
      ),
    ));
    
    // Smooth ease
    add(MoveEffect.to(
      Vector2(100, 100),
      EffectController(
        duration: 0.4,
        curve: Curves.easeInOutCubic,
      ),
    ));
    
    // Anticipation (starts slow, speeds up)
    add(ScaleEffect.to(
      Vector2.all(0.8),
      EffectController(
        duration: 0.3,
        curve: Curves.easeIn,
      ),
    ));
  }
}
```

### Infinite Effects

```dart
class FloatingCard extends PositionComponent {
  @override
  Future<void> onLoad() async {
    // Infinite float animation
    add(MoveEffect.by(
      Vector2(0, -10),
      EffectController(
        duration: 1.0,
        curve: Curves.easeInOut,
        infinite: true,
        alternate: true,  // ✅ Goes up, then down, repeat
      ),
    ));
  }
  
  void addRotation() {
    // Infinite gentle rotation
    add(RotateEffect.by(
      0.1,
      EffectController(
        duration: 2.0,
        infinite: true,
        alternate: true,
      ),
    ));
  }
}
```

### Delay and Repeating

```dart
class DelayedCard extends PositionComponent {
  void animateWithDelay() {
    add(SequenceEffect([
      // Wait 0.5 seconds
      MoveEffect.by(
        Vector2.zero(),
        EffectController(duration: 0.5),
      ),
      // Then animate
      ScaleEffect.to(
        Vector2.all(1.5),
        EffectController(duration: 0.3),
      ),
    ]));
  }
  
  void pulseRepeatedly() {
    add(SequenceEffect([
      ScaleEffect.by(Vector2.all(1.1), EffectController(duration: 0.2)),
      ScaleEffect.by(Vector2.all(0.909), EffectController(duration: 0.2)),
    ], repeatCount: 3));  // ✅ Repeat 3 times
  }
}
```

## Effect Callbacks

### onComplete Callback

```dart
class CardWithCallback extends PositionComponent {
  void moveAndCallback(Vector2 target) {
    add(MoveEffect.to(
      target,
      EffectController(duration: 0.5),
      onComplete: () {
        // Called when effect completes
        game.audioManager.playSfx('card_land');
        add(ParticleSystemComponent(
          particle: ParticleRecipes.sparkle(),
        ));
      },
    ));
  }
  
  void fadeOutAndRemove() {
    add(OpacityEffect.fadeOut(
      EffectController(duration: 0.5),
      onComplete: () {
        removeFromParent();
        game.onCardRemoved(this);
      },
    ));
  }
}
```

## RemoveEffect

### Auto-Remove After Animation

```dart
class TemporaryEffect extends PositionComponent {
  void playAndRemove() {
    add(SequenceEffect([
      // Animate
      ScaleEffect.to(Vector2.all(2.0), EffectController(duration: 0.3)),
      OpacityEffect.fadeOut(EffectController(duration: 0.2)),
      // Remove from tree
      RemoveEffect(),  // ✅ Removes component
    ]));
  }
}
```

## ColorEffect

### Tint and Color Transitions

```dart
class ColoredCard extends PositionComponent with HasPaint {
  void flashRed() {
    add(ColorEffect(
      Colors.red,
      EffectController(duration: 0.2),
      opacityFrom: 0.0,
      opacityTo: 0.5,
    ));
  }
  
  void transitionColor(Color targetColor) {
    add(ColorEffect(
      targetColor,
      EffectController(duration: 0.5, curve: Curves.easeInOut),
    ));
  }
  
  void pulseGlow() {
    add(SequenceEffect([
      ColorEffect(
        Colors.yellow,
        EffectController(duration: 0.3),
        opacityTo: 0.6,
      ),
      ColorEffect(
        Colors.white,
        EffectController(duration: 0.3),
        opacityTo: 0.0,
      ),
    ], repeatCount: 2));
  }
}
```

## Performance Optimization

### Effect Management

```dart
class OptimizedCard extends PositionComponent {
  void cleanupEffects() {
    // Remove all active effects
    removeAll(children.query<Effect>());
  }
  
  void replaceEffect(Effect newEffect) {
    // Remove old effects before adding new
    cleanupEffects();
    add(newEffect);
  }
  
  @override
  void update(double dt) {
    // Skip if too many effects (performance guard)
    final effectCount = children.query<Effect>().length;
    if (effectCount > 5) {
      AppLogger.warning('Too many effects on card', {'count': effectCount});
    }
    
    super.update(dt);
  }
}
```

### Reusable Effect Definitions

```dart
class EffectLibrary {
  static Effect cardHover() {
    return CombinedEffect([
      ScaleEffect.to(
        Vector2.all(1.2),
        EffectController(duration: 0.2, curve: Curves.easeOut),
      ),
      MoveEffect.by(
        Vector2(0, -10),
        EffectController(duration: 0.2, curve: Curves.easeOut),
      ),
    ]);
  }
  
  static Effect cardPlay() {
    return SequenceEffect([
      ScaleEffect.to(Vector2.all(1.3), EffectController(duration: 0.2)),
      OpacityEffect.fadeOut(EffectController(duration: 0.3)),
      RemoveEffect(),
    ]);
  }
  
  static Effect cardDraw() {
    return SequenceEffect([
      OpacityEffect.fadeIn(EffectController(duration: 0.1)),
      ScaleEffect.to(Vector2.all(0.9), EffectController(duration: 0.1)),
      ScaleEffect.to(Vector2.all(1.0), EffectController(duration: 0.2)),
    ]);
  }
}

// Usage
class Card extends PositionComponent {
  void hover() {
    add(EffectLibrary.cardHover());
  }
  
  void play() {
    add(EffectLibrary.cardPlay());
  }
}
```

## Complex Card Interactions

### Card Select → Hover → Play Flow

```dart
class InteractiveCard extends PositionComponent with TapCallbacks {
  CardState _state = CardState.idle;
  
  @override
  void onTapDown(TapDownEvent event) {
    if (_state == CardState.idle) {
      _transitionToHover();
    } else if (_state == CardState.hover) {
      _transitionToPlay();
    }
  }
  
  void _transitionToHover() {
    _state = CardState.hover;
    
    add(CombinedEffect([
      ScaleEffect.to(Vector2.all(2.5), EffectController(duration: 0.3)),
      MoveEffect.to(
        Vector2(game.size.x / 2, game.size.y / 2),
        EffectController(duration: 0.3, curve: Curves.easeOut),
      ),
    ]));
    
    priority = 1000;  // Bring to front
  }
  
  void _transitionToPlay() {
    _state = CardState.playing;
    
    add(SequenceEffect([
      ScaleEffect.to(Vector2.all(3.0), EffectController(duration: 0.2)),
      OpacityEffect.to(0.0, EffectController(duration: 0.3)),
      RemoveEffect(),
    ]));
    
    game.onCardPlayed(this);
  }
  
  void returnToHand(Vector2 handPosition) {
    _state = CardState.returning;
    
    add(CombinedEffect([
      ScaleEffect.to(Vector2.all(1.0), EffectController(duration: 0.3)),
      MoveEffect.to(
        handPosition,
        EffectController(duration: 0.3, curve: Curves.easeInOut),
      ),
    ], onComplete: () {
      _state = CardState.idle;
      priority = 0;
    }));
  }
}
```

---

**Next:** [Camera & Viewport](./06-camera-viewport.md)  
**Previous:** [Particle Effects](./04-particle-effects.md)  
**Related:** [Sprite Animation System](./03-sprite-animation-system.md)


