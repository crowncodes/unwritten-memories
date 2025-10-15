# Camera & Viewport Systems

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete

---

## Overview

Camera systems in Flame control what players see, handle viewport scaling, and manage coordinate transformations.

---

## Camera Setup

### Fixed Resolution (Recommended)

```dart
@override
Future<void> onLoad() async {
  camera = CameraComponent.withFixedResolution(
    width: 1920,
    height: 1080,
  );
  camera.viewfinder.anchor = Anchor.topLeft;
}
```

**Benefits:**
- Consistent gameplay across devices
- Predictable physics
- Easier development

### Responsive Resolution

```dart
@override
Future<void> onLoad() async {
  camera = CameraComponent();
  camera.viewfinder.visibleGameSize = Vector2(1920, 1080);
}
```

---

## Coordinate Transformation

### Screen to World

```dart
final screenPosition = event.position;
final worldPosition = camera.viewfinder.globalToLocal(screenPosition);
```

### World to Screen

```dart
final worldPosition = component.position;
final screenPosition = camera.viewfinder.localToGlobal(worldPosition);
```

---

## Camera Movement

### Follow Target

```dart
camera.follow(playerComponent);
camera.setBounds(Rectangle.fromLTWH(0, 0, 3840, 2160));
```

### Smooth Following

```dart
camera.follow(
  playerComponent,
  maxSpeed: 200,
  verticalOnly: false,
  horizontalOnly: false,
);
```

---

## Screen Shake

```dart
class CameraShake extends Effect with EffectTarget<CameraComponent> {
  final double intensity;
  final Vector2 originalPosition;
  
  CameraShake({
    required this.intensity,
    required EffectController controller,
  }) : originalPosition = Vector2.zero(),
       super(controller);
  
  @override
  void onStart() {
    originalPosition.setFrom(target.viewfinder.position);
  }
  
  @override
  void apply(double progress) {
    final shake = Vector2.random() * intensity * (1 - progress);
    target.viewfinder.position = originalPosition + shake;
  }
}

// Usage
game.camera.add(CameraShake(
  intensity: 20,
  controller: EffectController(duration: 0.5),
));
```

---

## Related Documentation

- **55-flame-engine-fundamentals.md** - Flame basics
- **56-card-physics-animations.md** - Physics
- **59-performance-optimization-flame.md** - Performance

---

**Status:** ✅ Camera Systems Complete

