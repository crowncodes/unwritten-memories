# Camera & Viewport

**Reference:** `docs/master_flutter_flame_spec_v_1_0.md` (Lines 579-672)

## Fixed Resolution Camera

Essential for consistent card layouts across all devices:

```dart
class UnwrittenGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    final world = World();
    final camera = CameraComponent.withFixedResolution(
      world: world,
      width: 1920,  // Design width
      height: 1080, // Design height
    );
    
    camera.viewfinder.anchor = Anchor.center;
    await addAll([world, camera]);
  }
}
```

## Responsive Viewport Configuration

```dart
class ResponsiveGame extends FlameGame {
  @override
  void onGameResize(Vector2 size) {
    super.onGameResize(size);
    
    final aspectRatio = size.x / size.y;
    
    if (aspectRatio < 0.75) {
      // Portrait mobile
      camera.viewport = FixedResolutionViewport(
        resolution: Vector2(1080, 1920),
      );
    } else if (aspectRatio < 1.5) {
      // Tablet
      camera.viewport = FixedResolutionViewport(
        resolution: Vector2(1440, 1080),
      );
    } else {
      // Desktop/landscape
      camera.viewport = FixedResolutionViewport(
        resolution: Vector2(1920, 1080),
      );
    }
  }
}
```

## Camera Follow

```dart
class FollowingCamera extends Component {
  final PositionComponent target;
  
  FollowingCamera(this.target);
  
  void enableFollow() {
    game.camera.follow(target, maxSpeed: 200);
  }
  
  void smoothFollow() {
    game.camera.follow(
      target,
      maxSpeed: 100,
      snap: false,  // Smooth lerp following
    );
  }
}
```

## Camera Effects

```dart
class CameraEffects extends Component {
  void shake(double intensity) {
    game.camera.viewfinder.add(
      MoveEffect.by(
        Vector2.random() * intensity,
        EffectController(duration: 0.05),
      ),
    );
  }
  
  void zoomTo(double zoom) {
    game.camera.viewfinder.add(
      ScaleEffect.to(
        Vector2.all(zoom),
        EffectController(duration: 0.5, curve: Curves.easeInOut),
      ),
    );
  }
}
```

---

**Next:** [Collision Detection](./07-collision-detection.md)  
**Previous:** [Effects System](./05-effects-system.md)


