# Performance Optimization (Flame)

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete

---

## Performance Targets

| Metric | Target | Critical |
|--------|--------|----------|
| Frame Rate | 60 FPS | Yes |
| Frame Time | < 16ms | Yes |
| Memory | < 200MB | Yes |
| Battery | < 10% per 30min | Yes |

---

## Sprite Atlases

### Problem

```dart
// ❌ BAD: Individual sprites (50 draw calls)
for (final card in cards) {
  await images.load('cards/${card.id}.png');
}
```

### Solution

```dart
// ✅ GOOD: Sprite atlas (1 draw call)
final atlas = await images.load('cards_atlas.png');
final spriteSheet = SpriteSheet(
  image: atlas,
  srcSize: Vector2(200, 300),
);
```

---

## Component Pooling

### Implementation

```dart
class CardPool {
  final List<CardComponent> _pool = [];
  
  CardComponent get() {
    return _pool.isNotEmpty ? _pool.removeLast() : CardComponent();
  }
  
  void release(CardComponent card) {
    card.removeFromParent();
    _pool.add(card);
  }
}
```

---

## Draw Call Reduction

### Batching

```dart
// Use sprite batching
final batch = SpriteBatch(atlas);
batch.add(position: Vector2(100, 100), source: Rect.fromLTWH(0, 0, 200, 300));
batch.add(position: Vector2(320, 100), source: Rect.fromLTWH(200, 0, 200, 300));
batch.render(canvas); // 1 draw call for multiple sprites
```

---

## Memory Management

### Dispose Resources

```dart
@override
void onRemove() {
  // Clean up
  sprite.image?.dispose();
  super.onRemove();
}
```

### Limit Active Components

```dart
// Remove off-screen components
@override
void update(double dt) {
  if (!isVisible()) {
    removeFromParent();
  }
}
```

---

## Profiling

### Enable Performance Overlay

```dart
MaterialApp(
  showPerformanceOverlay: true,
  // ...
)
```

### DevTools

```bash
flutter run --profile
# Open DevTools
flutter pub global run devtools
```

---

## Related Documentation

- **55-flame-engine-fundamentals.md** - Flame basics
- **68-performance-monitoring.md** - Monitoring tools

---

**Status:** ✅ Performance Optimization Complete  
**Target:** 60 FPS Stable

