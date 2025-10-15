# Performance Optimization

**Reference:** `docs/master_flutter_flame_spec_v_1_0.md` (Lines 792-873)

## 60 FPS Target

Every optimization in Unwritten aims for stable 60 FPS (16.67ms per frame).

## Component Pooling

```dart
class CardPool {
  final Queue<CardComponent> _pool = Queue();
  final int maxSize = 50;
  
  CardComponent getCard() {
    if (_pool.isNotEmpty) {
      return _pool.removeFirst()..reset();
    }
    return CardComponent();
  }
  
  void returnCard(CardComponent card) {
    if (_pool.length < maxSize) {
      card.removeFromParent();
      _pool.add(card);
    }
  }
}
```

## Sprite Batching

```dart
class OptimizedCardRenderer {
  // ✅ CORRECT: Single sprite sheet, multiple cards
  static late final Image cardAtlas;
  
  static Future<void> initialize(FlameGame game) async {
    cardAtlas = await game.images.load('cards/atlas.png');
  }
  
  static SpriteComponent createCard(Vector2 atlasPosition) {
    // All cards use same atlas
    return SpriteComponent(
      sprite: Sprite(
        cardAtlas,
        srcPosition: atlasPosition,
        srcSize: Vector2(128, 179),
      ),
    );
  }
}
```

## Culling Off-Screen Components

```dart
class CullingSystem extends Component with HasGameReference<FlameGame> {
  @override
  void update(double dt) {
    final visibleRect = game.camera.visibleWorldRect;
    
    for (final card in game.world.query<CardComponent>()) {
      // Skip rendering if off-screen
      card.isVisible = visibleRect.overlaps(card.toRect());
    }
  }
}
```

## LOD (Level of Detail)

```dart
class LODCard extends PositionComponent {
  @override
  void update(double dt) {
    final distanceFromCamera = position.distanceTo(game.camera.position);
    
    if (distanceFromCamera > 500) {
      // Far away: low detail
      _renderLowDetail();
    } else if (distanceFromCamera > 200) {
      // Medium distance: medium detail
      _renderMediumDetail();
    } else {
      // Close: high detail
      _renderHighDetail();
    }
    
    super.update(dt);
  }
  
  void _renderLowDetail() {
    // Skip particles, use simple sprite
  }
  
  void _renderHighDetail() {
    // Full effects, animations, particles
  }
}
```

## Memory Management

```dart
class MemoryManager {
  void optimizeMemory() {
    // Remove unused components
    _removeOffScreenComponents();
    
    // Clear cached images not in use
    _clearUnusedAssets();
    
    // Force garbage collection (use sparingly!)
    // Only in extreme cases, let Dart handle GC
  }
  
  void _removeOffScreenComponents() {
    final visibleRect = game.camera.visibleWorldRect;
    
    for (final component in game.world.children) {
      if (component is PositionComponent) {
        final rect = component.toRect();
        if (!visibleRect.overlaps(rect)) {
          // Component far off-screen, consider removing
          if (_canRemove(component)) {
            component.removeFromParent();
          }
        }
      }
    }
  }
}
```

## Const Constructors

```dart
// ✅ CORRECT: Use const where possible
class CardBorder extends RectangleComponent {
  const CardBorder()
      : super(
          size: const Vector2(120, 168),
          paint: const PaintExtension.color(Colors.white),
        );
}

// ❌ WRONG: Creating new objects every time
class InefficientBorder extends RectangleComponent {
  InefficientBorder()
      : super(
          size: Vector2(120, 168),  // New object each time
          paint: Paint()..color = Colors.white,
        );
}
```

## Async Operations

```dart
class AsyncCardLoader {
  Future<void> loadCard(String cardId) async {
    // ✅ Use compute() for heavy operations
    final cardData = await compute(_parseCardData, cardId);
    
    // Apply on main thread
    _applyCardData(cardData);
  }
  
  static Map<String, dynamic> _parseCardData(String cardId) {
    // Heavy JSON parsing in isolate
    return jsonDecode(heavyJsonString);
  }
}
```

## Performance Monitoring

```dart
class PerformanceMonitor extends Component {
  final List<double> _frameTimes = [];
  Stopwatch? _frameStopwatch;
  
  @override
  void update(double dt) {
    _frameStopwatch?.stop();
    final frameTime = _frameStopwatch?.elapsedMilliseconds.toDouble() ?? 0;
    
    _frameTimes.add(frameTime);
    if (_frameTimes.length > 60) {
      _frameTimes.removeAt(0);
    }
    
    // Log if slow
    if (frameTime > 16.67) {
      AppLogger.performance('Slow frame', {
        'time_ms': frameTime,
        'target_ms': 16.67,
        'components': game.world.children.length,
      });
    }
    
    _frameStopwatch = Stopwatch()..start();
    super.update(dt);
  }
  
  double get averageFPS {
    if (_frameTimes.isEmpty) return 0;
    final avgFrameTime = _frameTimes.reduce((a, b) => a + b) / _frameTimes.length;
    return 1000 / avgFrameTime;
  }
}
```

## Best Practices Checklist

- ✅ Pool frequently created components (cards, particles)
- ✅ Use single sprite atlas for all cards
- ✅ Cull off-screen components
- ✅ Implement LOD for distant elements
- ✅ Use const constructors
- ✅ Limit active particles (< 100)
- ✅ Batch sprite rendering
- ✅ Async heavy operations with compute()
- ✅ Monitor frame times
- ✅ Target < 16.67ms per frame

---

**Next:** [Flame-Riverpod Integration](./10-flame-riverpod-integration.md)  
**Previous:** [Input Handling](./08-input-handling.md)  
**Related:** [Component System](./01-component-system.md)


