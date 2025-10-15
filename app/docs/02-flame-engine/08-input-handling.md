# Input Handling

**Reference:** `docs/master_flutter_flame_spec_v_1_0.md` (Lines 368-456)

## Overview

Flame provides sophisticated input mixins for tap, drag, and hover interactions. These are essential for responsive card controls with multi-touch support and gesture recognition.

## Tap Callbacks

### Basic Tap Handling

```dart
class TappableCard extends PositionComponent with TapCallbacks {
  @override
  void onTapDown(TapDownEvent event) {
    // Called when tap starts
    game.audioManager.playSfx('tap');
    game.hapticFeedback.lightImpact();
    
    add(ScaleEffect.by(Vector2.all(0.95), EffectController(duration: 0.1)));
  }
  
  @override
  void onTapUp(TapDownEvent event) {
    // Called when tap releases
    add(ScaleEffect.to(Vector2.all(1.0), EffectController(duration: 0.1)));
  }
  
  @override
  void onTapCancel(TapCancelEvent event) {
    // Called if tap is cancelled (e.g., drag starts)
    add(ScaleEffect.to(Vector2.all(1.0), EffectController(duration: 0.1)));
  }
}
```

### Tap vs Long Press

```dart
class CardWithLongPress extends PositionComponent with TapCallbacks {
  DateTime? _tapDownTime;
  static const longPressDuration = Duration(milliseconds: 500);
  
  @override
  void onTapDown(TapDownEvent event) {
    _tapDownTime = DateTime.now();
    
    // Check for long press after delay
    Future.delayed(longPressDuration, () {
      if (_tapDownTime != null) {
        _onLongPress();
      }
    });
  }
  
  @override
  void onTapUp(TapUpEvent event) {
    final duration = DateTime.now().difference(_tapDownTime!);
    _tapDownTime = null;
    
    if (duration < longPressDuration) {
      _onShortTap();
    }
  }
  
  void _onShortTap() {
    // Quick tap: select card
    game.selectCard(this);
  }
  
  void _onLongPress() {
    // Long press: show card details
    game.showCardDetails(this);
  }
}
```

## Drag Callbacks

### Basic Dragging

```dart
class DraggableCard extends PositionComponent with DragCallbacks {
  Vector2? _dragStartPosition;
  int _originalPriority = 0;
  
  @override
  void onDragStart(DragStartEvent event) {
    _dragStartPosition = position.clone();
    _originalPriority = priority;
    
    // Bring to front
    priority = 1000;
    
    // Visual feedback
    add(ScaleEffect.to(Vector2.all(1.2), EffectController(duration: 0.2)));
    game.audioManager.playSfx('card_pickup');
  }
  
  @override
  void onDragUpdate(DragUpdateEvent event) {
    // Move card with finger/mouse
    position += event.delta;
  }
  
  @override
  void onDragEnd(DragEndEvent event) {
    // Check if dropped in valid zone
    if (_isInValidDropZone()) {
      _playCard();
    } else {
      _returnToHand();
    }
    
    priority = _originalPriority;
  }
  
  void _returnToHand() {
    add(MoveEffect.to(
      _dragStartPosition!,
      EffectController(duration: 0.3, curve: Curves.easeOut),
    ));
    add(ScaleEffect.to(Vector2.all(1.0), EffectController(duration: 0.2)));
  }
  
  bool _isInValidDropZone() {
    final dropZone = game.findByKey(ComponentKey.named('drop_zone'))!;
    return dropZone.containsPoint(position);
  }
}
```

### Drag with Constraints

```dart
class ConstrainedDraggable extends PositionComponent with DragCallbacks {
  final Rect dragBounds;
  
  ConstrainedDraggable(this.dragBounds);
  
  @override
  void onDragUpdate(DragUpdateEvent event) {
    // Calculate new position
    final newPosition = position + event.delta;
    
    // Clamp to bounds
    position = Vector2(
      newPosition.x.clamp(dragBounds.left, dragBounds.right),
      newPosition.y.clamp(dragBounds.top, dragBounds.bottom),
    );
  }
}
```

## Hover Callbacks

### Hover Effects

```dart
class HoverableCard extends PositionComponent with HoverCallbacks {
  bool _isHovered = false;
  
  @override
  void onHoverEnter() {
    _isHovered = true;
    
    // Visual feedback
    add(CombinedEffect([
      ScaleEffect.to(Vector2.all(1.15), EffectController(duration: 0.2)),
      MoveEffect.by(Vector2(0, -10), EffectController(duration: 0.2)),
    ]));
    
    // Show glow
    add(ColorEffect(
      Colors.yellow,
      EffectController(duration: 0.2),
      opacityTo: 0.3,
    ));
    
    game.hapticFeedback.selectionClick();
  }
  
  @override
  void onHoverExit() {
    _isHovered = false;
    
    // Return to normal
    add(CombinedEffect([
      ScaleEffect.to(Vector2.all(1.0), EffectController(duration: 0.2)),
      MoveEffect.to(
        _originalPosition,
        EffectController(duration: 0.2),
      ),
    ]));
    
    // Remove glow
    removeAll(children.query<ColorEffect>());
  }
}
```

## Multi-Touch Support

### Simultaneous Touch Handling

```dart
class MultiTouchGame extends FlameGame with MultiTouchTapDetector {
  final Map<int, Vector2> _activeTouches = {};
  
  @override
  void onTapDown(int pointerId, TapDownInfo info) {
    _activeTouches[pointerId] = info.eventPosition.global;
    
    // Handle multiple simultaneous taps
    if (_activeTouches.length > 1) {
      _handleMultiTouch();
    }
  }
  
  @override
  void onTapUp(int pointerId, TapUpInfo info) {
    _activeTouches.remove(pointerId);
  }
  
  void _handleMultiTouch() {
    // Two-finger pinch/zoom
    if (_activeTouches.length == 2) {
      final touches = _activeTouches.values.toList();
      final distance = (touches[0] - touches[1]).length;
      _handlePinchZoom(distance);
    }
  }
}
```

## Gesture Recognition

### Swipe Detection

```dart
class SwipeableCard extends PositionComponent with DragCallbacks {
  Vector2? _swipeStart;
  DateTime? _swipeStartTime;
  
  static const swipeVelocityThreshold = 500.0;  // pixels per second
  static const swipeDistanceThreshold = 50.0;
  
  @override
  void onDragStart(DragStartEvent event) {
    _swipeStart = position.clone();
    _swipeStartTime = DateTime.now();
  }
  
  @override
  void onDragEnd(DragEndEvent event) {
    if (_swipeStart == null || _swipeStartTime == null) return;
    
    final swipeDistance = (position - _swipeStart!).length;
    final swipeDuration = DateTime.now().difference(_swipeStartTime!);
    final velocity = swipeDistance / (swipeDuration.inMilliseconds / 1000);
    
    if (velocity > swipeVelocityThreshold && 
        swipeDistance > swipeDistanceThreshold) {
      _handleSwipe(position - _swipeStart!);
    } else {
      _returnToStart();
    }
  }
  
  void _handleSwipe(Vector2 swipeVector) {
    // Determine swipe direction
    final angle = swipeVector.angleToSigned(Vector2(1, 0));
    
    if (angle.abs() < math.pi / 4) {
      _onSwipeRight();
    } else if (angle.abs() > 3 * math.pi / 4) {
      _onSwipeLeft();
    } else if (angle > 0) {
      _onSwipeDown();
    } else {
      _onSwipeUp();
    }
  }
  
  void _onSwipeRight() {
    // Discard card right
    add(CombinedEffect([
      MoveEffect.by(Vector2(500, 0), EffectController(duration: 0.3)),
      OpacityEffect.fadeOut(EffectController(duration: 0.3)),
      RemoveEffect(),
    ]));
  }
}
```

### Double Tap Detection

```dart
class DoubleTappableCard extends PositionComponent with TapCallbacks {
  DateTime? _lastTapTime;
  static const doubleTapWindow = Duration(milliseconds: 300);
  
  @override
  void onTapDown(TapDownEvent event) {
    final now = DateTime.now();
    
    if (_lastTapTime != null && 
        now.difference(_lastTapTime!) < doubleTapWindow) {
      _onDoubleTap();
      _lastTapTime = null;
    } else {
      _lastTapTime = now;
    }
  }
  
  void _onDoubleTap() {
    // Play card immediately on double tap
    game.playCard(this);
  }
}
```

## Input Prediction

### Anticipatory Feedback

```dart
class PredictiveCard extends PositionComponent with DragCallbacks {
  Vector2? _dragVelocity;
  Vector2? _lastPosition;
  DateTime? _lastUpdateTime;
  
  @override
  void onDragUpdate(DragUpdateEvent event) {
    final now = DateTime.now();
    
    if (_lastPosition != null && _lastUpdateTime != null) {
      // Calculate velocity
      final deltaPosition = position - _lastPosition!;
      final deltaTime = now.difference(_lastUpdateTime!).inMilliseconds / 1000;
      _dragVelocity = deltaPosition / deltaTime;
      
      // Show predicted drop zone
      _showPredictedTarget();
    }
    
    _lastPosition = position.clone();
    _lastUpdateTime = now;
    
    position += event.delta;
  }
  
  void _showPredictedTarget() {
    if (_dragVelocity == null) return;
    
    // Project where card will land
    final predictedPosition = position + (_dragVelocity! * 0.5);
    
    // Highlight predicted zone
    game.highlightDropZone(predictedPosition);
  }
}
```

## Performance Optimization

### Input Throttling

```dart
class ThrottledInput extends PositionComponent with DragCallbacks {
  DateTime? _lastUpdateTime;
  static const updateInterval = Duration(milliseconds: 16);  // ~60 FPS
  
  @override
  void onDragUpdate(DragUpdateEvent event) {
    final now = DateTime.now();
    
    // Throttle updates to 60 FPS
    if (_lastUpdateTime != null &&
        now.difference(_lastUpdateTime!) < updateInterval) {
      return;
    }
    
    _lastUpdateTime = now;
    position += event.delta;
  }
}
```

### Hitbox Optimization

```dart
class OptimizedClickable extends PositionComponent 
    with TapCallbacks, HasCollisionDetection {
  
  @override
  Future<void> onLoad() async {
    // Use hitbox for more accurate click detection
    add(RectangleHitbox()
      ..collisionType = CollisionType.passive  // Only receives input
    );
  }
  
  @override
  bool containsLocalPoint(Vector2 point) {
    // Custom containment logic for complex shapes
    return _isPointInCardArea(point);
  }
  
  bool _isPointInCardArea(Vector2 point) {
    // Custom shape detection (e.g., rounded corners)
    final rect = size.toRect();
    final cornerRadius = 12.0;
    
    // Check if point is in rounded rectangle
    return _isInRoundedRect(point, rect, cornerRadius);
  }
}
```

## Complete Card Interaction Example

```dart
class FullyInteractiveCard extends PositionComponent 
    with TapCallbacks, DragCallbacks, HoverCallbacks {
  
  CardState _state = CardState.idle;
  Vector2? _dragStart;
  
  // Hover
  @override
  void onHoverEnter() {
    if (_state == CardState.idle) {
      _state = CardState.hover;
      add(EffectLibrary.cardHover());
    }
  }
  
  @override
  void onHoverExit() {
    if (_state == CardState.hover) {
      _state = CardState.idle;
      add(EffectLibrary.cardIdle());
    }
  }
  
  // Tap
  @override
  void onTapDown(TapDownEvent event) {
    game.hapticFeedback.lightImpact();
  }
  
  @override
  void onTapUp(TapUpEvent event) {
    if (_state == CardState.hover) {
      _onCardSelected();
    }
  }
  
  // Drag
  @override
  void onDragStart(DragStartEvent event) {
    _state = CardState.dragging;
    _dragStart = position.clone();
    priority = 1000;
    
    add(ScaleEffect.to(Vector2.all(1.3), EffectController(duration: 0.2)));
    game.audioManager.playSfx('card_pickup');
  }
  
  @override
  void onDragUpdate(DragUpdateEvent event) {
    position += event.delta;
    game.checkDropZones(position);
  }
  
  @override
  void onDragEnd(DragEndEvent event) {
    if (game.isInValidDropZone(position)) {
      _playCard();
    } else {
      _returnToHand();
    }
  }
  
  void _onCardSelected() {
    game.selectCard(this);
  }
  
  void _playCard() {
    _state = CardState.playing;
    game.playCard(this);
  }
  
  void _returnToHand() {
    _state = CardState.returning;
    add(CombinedEffect([
      MoveEffect.to(_dragStart!, EffectController(duration: 0.3)),
      ScaleEffect.to(Vector2.all(1.0), EffectController(duration: 0.2)),
    ], onComplete: () {
      _state = CardState.idle;
      priority = 0;
    }));
  }
}
```

---

**Next:** [Performance Optimization](./09-performance-optimization.md)  
**Previous:** [Effects System](./05-effects-system.md)  
**Related:** [Component System](./01-component-system.md), [Collision Detection](./07-collision-detection.md)


