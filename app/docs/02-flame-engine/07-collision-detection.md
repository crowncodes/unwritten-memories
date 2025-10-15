# Collision Detection

**Reference:** `docs/master_flutter_flame_spec_v_1_0.md` (Lines 457-536)

## Basic Collision Setup

```dart
class CollisionGame extends FlameGame with HasCollisionDetection {
  // Collision detection enabled
}

class CollisionCard extends PositionComponent 
    with CollisionCallbacks, HasGameReference<CollisionGame> {
  
  @override
  Future<void> onLoad() async {
    // Add hitbox
    add(RectangleHitbox());
  }
  
  @override
  void onCollision(Set<Vector2> intersectionPoints, PositionComponent other) {
    if (other is DropZone) {
      // Card collided with drop zone
      _highlightDropZone(other);
    }
  }
  
  @override
  void onCollisionEnd(PositionComponent other) {
    if (other is DropZone) {
      _unhighlightDropZone(other);
    }
  }
}
```

## Hitbox Types

```dart
class CardWithHitbox extends PositionComponent with CollisionCallbacks {
  @override
  Future<void> onLoad() async {
    // Rectangle hitbox
    add(RectangleHitbox());
    
    // Circle hitbox
    add(CircleHitbox(radius: 60));
    
    // Polygon hitbox (custom shape)
    add(PolygonHitbox([
      Vector2(0, 0),
      Vector2(120, 0),
      Vector2(120, 168),
      Vector2(0, 168),
    ]));
    
    // Composite hitbox (multiple shapes)
    add(CompositeHitbox([
      CircleHitbox(radius: 30, position: Vector2(60, 40)),
      RectangleHitbox(size: Vector2(80, 100), position: Vector2(20, 60)),
    ]));
  }
}
```

## Collision Types

```dart
class CollisionTypes extends PositionComponent with CollisionCallbacks {
  @override
  Future<void> onLoad() async {
    final hitbox = RectangleHitbox();
    
    // Active: Can collide with others
    hitbox.collisionType = CollisionType.active;
    
    // Passive: Only receives collisions
    hitbox.collisionType = CollisionType.passive;
    
    // Inactive: No collisions
    hitbox.collisionType = CollisionType.inactive;
    
    add(hitbox);
  }
}
```

## Raycast for Drop Detection

```dart
class DropDetection extends Component with HasGameReference<CollisionGame> {
  bool isOverDropZone(Vector2 position) {
    // Cast ray from position
    final result = game.collisionDetection.raycast(
      Ray2(origin: position, direction: Vector2(0, 1)),
    );
    
    if (result != null) {
      return result.hitbox?.parent is DropZone;
    }
    
    return false;
  }
}
```

---

**Next:** [Input Handling](./08-input-handling.md)  
**Previous:** [Camera & Viewport](./06-camera-viewport.md)


