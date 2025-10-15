# Flame Game Loop AI Integration

**Purpose:** Deep dive into integrating AI with Flame's game loop without blocking  
**Audience:** Advanced Flame developers, game engineers  
**Status:** ✅ Complete  
**Related:** ← 60-flame-ai-integration-patterns.md | 61-flame-ai-components.md

---

## What This Document Covers

**Deep technical implementation details:**
- Flame game loop architecture
- Update cycle with AI (60 FPS critical)
- Render cycle considerations
- Performance profiling and optimization
- Memory management with AI
- Threading and isolates
- Advanced patterns

**This is an advanced guide** - assumes familiarity with Flame and game loops.

---

## Table of Contents

1. [Flame Game Loop Architecture](#flame-game-loop-architecture)
2. [Update Cycle with AI](#update-cycle-with-ai)
3. [Render Cycle Optimization](#render-cycle-optimization)
4. [Performance Profiling](#performance-profiling)
5. [Memory Management](#memory-management)
6. [Advanced Patterns](#advanced-patterns)
7. [Production Checklist](#production-checklist)

---

## Flame Game Loop Architecture

### The Game Loop

```dart
/// Flame's game loop (simplified)
class GameLoop {
  void tick(double dt) {
    // 1. Update all components
    _updateComponents(dt);  // Must complete in < 16ms for 60 FPS
    
    // 2. Render all components
    _renderComponents();    // Must complete in < 16ms for 60 FPS
  }
}
```

**Critical Constraint:** Total time for update + render < 16.67ms (60 FPS)

### AI Integration Challenge

```dart
// ❌ BAD - Blocks for 2-5 seconds
void update(double dt) {
  final dialogue = await _aiService.generateDialogue();  // BLOCKS LOOP!
  _showDialogue(dialogue);
}

// ✅ GOOD - Non-blocking
void update(double dt) {
  // Check if async AI completed (doesn't block)
  if (_dialogueFuture != null) {
    _checkIfReady();  // Quick check, doesn't block
  }
}
```

---

## Update Cycle with AI

### Pattern 1: State Machine Approach

```dart
class AIAwareComponent extends PositionComponent {
  AIState _state = AIState.idle;
  Future<DialogueResponse>? _pendingRequest;
  DialogueResponse? _result;
  
  @override
  void update(double dt) {
    super.update(dt);
    
    // State machine (non-blocking)
    switch (_state) {
      case AIState.idle:
        // Waiting for trigger
        break;
      
      case AIState.requesting:
        // Check if future completed (non-blocking)
        _checkFutureStatus();
        break;
      
      case AIState.processing:
        // Process result
        _processResult(dt);
        break;
      
      case AIState.displaying:
        // Display animation
        _updateDisplay(dt);
        break;
    }
  }
  
  void _checkFutureStatus() {
    // Non-blocking future check
    _pendingRequest!.then((result) {
      _result = result;
      _state = AIState.processing;
    }).catchError((error) {
      _state = AIState.error;
    });
  }
  
  void _processResult(double dt) {
    // Process result (quick, in update loop)
    if (_result != null) {
      _prepareDisplay(_result!);
      _state = AIState.displaying;
    }
  }
  
  void _updateDisplay(double dt) {
    // Animate display (smooth, frame-by-frame)
    _animationProgress += dt * _animationSpeed;
    // ... update visual state
  }
}

enum AIState {
  idle,
  requesting,
  processing,
  displaying,
  error,
}
```

### Pattern 2: Event-Driven Approach

```dart
class EventDrivenAIComponent extends PositionComponent {
  final StreamController<AIEvent> _eventStream = StreamController();
  StreamSubscription? _subscription;
  
  @override
  void onMount() {
    super.onMount();
    
    // Subscribe to AI events
    _subscription = _eventStream.stream.listen(_handleAIEvent);
  }
  
  @override
  void update(double dt) {
    super.update(dt);
    
    // Update loop stays clean and fast
    _updateVisuals(dt);
  }
  
  void _handleAIEvent(AIEvent event) {
    // Handle AI results asynchronously
    switch (event.type) {
      case AIEventType.dialogueReady:
        _showDialogue(event.dialogue);
        break;
      case AIEventType.evolutionComplete:
        _applyEvolution(event.evolution);
        break;
      case AIEventType.error:
        _showError(event.error);
        break;
    }
  }
  
  void requestDialogue() {
    // Trigger async request (returns immediately)
    _aiService.generateDialogue(cardId).then((dialogue) {
      _eventStream.add(AIEvent(
        type: AIEventType.dialogueReady,
        dialogue: dialogue,
      ));
    });
  }
  
  @override
  void onRemove() {
    _subscription?.cancel();
    _eventStream.close();
    super.onRemove();
  }
}
```

### Measuring Update Performance

```dart
class PerformanceMonitoredComponent extends PositionComponent {
  final List<double> _updateTimes = [];
  
  @override
  void update(double dt) {
    final stopwatch = Stopwatch()..start();
    
    super.update(dt);
    _updateLogic(dt);
    
    stopwatch.stop();
    _updateTimes.add(stopwatch.elapsedMicroseconds / 1000);  // Convert to ms
    
    // Keep last 60 frames (1 second at 60 FPS)
    if (_updateTimes.length > 60) {
      _updateTimes.removeAt(0);
    }
    
    // Warn if update too slow
    if (stopwatch.elapsedMilliseconds > 8) {  // Half of 16ms budget
      AppLogger.performance(
        'Slow update: ${stopwatch.elapsedMilliseconds}ms',
        stopwatch.elapsed,
      );
    }
  }
  
  double get averageUpdateTime {
    if (_updateTimes.isEmpty) return 0;
    return _updateTimes.reduce((a, b) => a + b) / _updateTimes.length;
  }
  
  double get maxUpdateTime {
    if (_updateTimes.isEmpty) return 0;
    return _updateTimes.reduce((a, b) => a > b ? a : b);
  }
}
```

---

## Render Cycle Optimization

### Conditional Rendering

```dart
class OptimizedAIComponent extends PositionComponent {
  bool _needsRedraw = false;
  
  @override
  void update(double dt) {
    super.update(dt);
    
    // AI result arrived - mark for redraw
    if (_stateChanged) {
      _needsRedraw = true;
    }
  }
  
  @override
  void render(Canvas canvas) {
    if (!_needsRedraw) {
      return;  // Skip render if nothing changed
    }
    
    super.render(canvas);
    _renderAIContent(canvas);
    
    _needsRedraw = false;
  }
}
```

### Layer Caching

```dart
class LayeredAIComponent extends PositionComponent {
  ui.Image? _cachedBackground;
  ui.Image? _cachedDialogue;
  
  @override
  void render(Canvas canvas) {
    // Render cached background (static)
    if (_cachedBackground != null) {
      canvas.drawImage(_cachedBackground!, Offset.zero, Paint());
    }
    
    // Render dialogue layer (changes frequently)
    _renderDialogue(canvas);
  }
  
  Future<void> _cacheBackground() async {
    // Render background to image once
    final recorder = ui.PictureRecorder();
    final canvas = Canvas(recorder);
    
    _renderBackgroundToCanvas(canvas);
    
    final picture = recorder.endRecording();
    _cachedBackground = await picture.toImage(300, 200);
  }
}
```

---

## Performance Profiling

### Built-in Flame Profiler

```dart
// Enable performance overlay
class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    // Enable FPS counter and performance stats
    debugMode = true;
  }
}
```

### Custom AI Performance Tracking

```dart
class AIPerformanceTracker {
  final List<AIMetric> _metrics = [];
  
  void trackRequest({
    required String operation,
    required Duration duration,
    required bool cached,
    required bool success,
  }) {
    _metrics.add(AIMetric(
      operation: operation,
      duration: duration,
      cached: cached,
      success: success,
      timestamp: DateTime.now(),
    ));
    
    // Keep last 100 metrics
    if (_metrics.length > 100) {
      _metrics.removeAt(0);
    }
    
    // Log slow operations
    if (duration.inMilliseconds > 3000) {
      AppLogger.performance('Slow AI operation: $operation', duration);
    }
  }
  
  PerformanceReport get report {
    final successful = _metrics.where((m) => m.success);
    final cached = _metrics.where((m) => m.cached);
    
    return PerformanceReport(
      totalRequests: _metrics.length,
      successRate: successful.length / _metrics.length,
      cacheHitRate: cached.length / _metrics.length,
      avgDuration: successful.isEmpty
          ? Duration.zero
          : Duration(
              milliseconds: successful
                  .map((m) => m.duration.inMilliseconds)
                  .reduce((a, b) => a + b) ~/
                  successful.length,
            ),
    );
  }
}

class AIMetric {
  final String operation;
  final Duration duration;
  final bool cached;
  final bool success;
  final DateTime timestamp;
  
  AIMetric({
    required this.operation,
    required this.duration,
    required this.cached,
    required this.success,
    required this.timestamp,
  });
}

class PerformanceReport {
  final int totalRequests;
  final double successRate;
  final double cacheHitRate;
  final Duration avgDuration;
  
  PerformanceReport({
    required this.totalRequests,
    required this.successRate,
    required this.cacheHitRate,
    required this.avgDuration,
  });
  
  @override
  String toString() {
    return 'AI Performance: $totalRequests requests, '
        '${(successRate * 100).toStringAsFixed(1)}% success, '
        '${(cacheHitRate * 100).toStringAsFixed(1)}% cached, '
        '${avgDuration.inMilliseconds}ms avg';
  }
}
```

---

## Memory Management

### Disposing AI Resources

```dart
class ProperlyDisposedAIComponent extends PositionComponent {
  late final AIRepository _repository;
  StreamSubscription? _subscription;
  Timer? _refreshTimer;
  
  @override
  void onRemove() {
    // Cancel any pending operations
    _subscription?.cancel();
    _refreshTimer?.cancel();
    
    // Clear caches
    _repository.clearLocalCache();
    
    super.onRemove();
  }
}
```

### Memory Leak Prevention

```dart
class LeakFreeAIComponent extends PositionComponent {
  // ❌ BAD - Creates memory leak
  void badExample() {
    _aiService.generateDialogue(cardId).then((dialogue) {
      // If component removed before this completes,
      // this callback still holds reference to component
      _showDialogue(dialogue);  // LEAK!
    });
  }
  
  // ✅ GOOD - Checks if still mounted
  void goodExample() {
    _aiService.generateDialogue(cardId).then((dialogue) {
      if (isMounted) {  // Check if still in game tree
        _showDialogue(dialogue);
      }
    });
  }
}
```

### Monitoring Memory Usage

```dart
class MemoryMonitor {
  Future<void> logMemoryUsage() async {
    final info = await DeviceInfoPlugin().androidInfo;
    
    // Track memory usage
    final memInfo = info.totalMemory;
    
    AppLogger.info('Memory usage: ${memInfo ~/ (1024 * 1024)} MB');
  }
}
```

---

## Advanced Patterns

### Pattern 1: Compute Isolates for Heavy AI

```dart
/// Use isolates for CPU-intensive AI operations
Future<DialogueResponse> generateWithIsolate(String prompt) async {
  return await compute(_generateDialogue, prompt);
}

/// Top-level function for isolate
DialogueResponse _generateDialogue(String prompt) {
  // CPU-intensive processing
  // Runs in separate isolate (doesn't block main thread)
  return DialogueResponse(/* ... */);
}
```

### Pattern 2: Background Generation

```dart
class BackgroundAIGenerator extends Component {
  Timer? _generationTimer;
  
  @override
  void onMount() {
    super.onMount();
    
    // Generate AI content in background (low priority)
    _generationTimer = Timer.periodic(Duration(seconds: 10), (_) {
      _generateBackground();
    });
  }
  
  void _generateBackground() {
    // Generate content for likely next interactions
    // Low priority, can be cancelled anytime
    _aiService.generateDialogue(
      cardId: _predictNextCard(),
      priority: Priority.low,
    ).then((dialogue) {
      // Cache silently
      _cache.put(_predictNextCard(), dialogue);
    }).catchError((e) {
      // Silent failure OK for background generation
    });
  }
  
  @override
  void onRemove() {
    _generationTimer?.cancel();
    super.onRemove();
  }
}
```

### Pattern 3: Progressive Enhancement

```dart
class ProgressiveAIComponent extends PositionComponent {
  @override
  Future<void> onLoad() async {
    // Show cached content immediately
    final cached = await _cache.get(cardId);
    if (cached != null) {
      _showDialogue(cached);
    }
    
    // Enhance with fresh AI in background
    _aiService.generateDialogue(cardId).then((fresh) {
      if (fresh != cached) {
        // Smoothly transition to fresh content
        _transitionToFreshContent(fresh);
      }
    });
  }
}
```

### Pattern 4: Request Coalescing

```dart
class RequestCoalescer {
  final Map<String, Future<DialogueResponse>> _pendingRequests = {};
  
  Future<DialogueResponse> getDialogue(String cardId) {
    // Check if request already in flight
    if (_pendingRequests.containsKey(cardId)) {
      // Return existing future (share result)
      return _pendingRequests[cardId]!;
    }
    
    // Start new request
    final future = _aiService.generateDialogue(cardId);
    _pendingRequests[cardId] = future;
    
    // Clean up when complete
    future.whenComplete(() {
      _pendingRequests.remove(cardId);
    });
    
    return future;
  }
}
```

---

## Production Checklist

### Performance Validation

```markdown
Before shipping:

## Update Loop
- [ ] No AI calls in update() method
- [ ] Update time < 8ms (p95)
- [ ] No frame drops during AI operations
- [ ] State transitions smooth

## Render Loop
- [ ] Render time < 8ms (p95)
- [ ] No unnecessary redraws
- [ ] Layer caching used where appropriate
- [ ] 60 FPS maintained during AI operations

## Memory
- [ ] No memory leaks (checked with DevTools)
- [ ] Proper dispose of AI resources
- [ ] Futures cancelled when components removed
- [ ] Cache size limited and monitored

## AI Integration
- [ ] All AI operations non-blocking
- [ ] Loading states visible to user
- [ ] Error states handled gracefully
- [ ] Fallback content available
- [ ] Cache hit rate > 70%

## Profiling
- [ ] Profiled on low-end devices
- [ ] No performance degradation over time
- [ ] Memory usage stable
- [ ] Battery drain acceptable (< 10% per 30 min)
```

### Testing Strategy

```dart
// Integration test
testWidgets('AI component doesn\'t block game loop', (tester) async {
  final game = MyGame();
  await tester.pumpWidget(GameWidget(game: game));
  
  // Trigger AI request
  final component = game.findByKey<AIComponent>(Key('test_component'));
  component.requestDialogue();
  
  // Game loop should continue
  for (int i = 0; i < 60; i++) {  // 60 frames = 1 second at 60 FPS
    await tester.pump(Duration(milliseconds: 16));
    
    // Verify FPS maintained
    expect(game.currentFps, greaterThan(55));  // Allow small variance
  }
  
  // AI result should eventually arrive
  await tester.pumpAndSettle();
  expect(component.hasDialogue, isTrue);
});
```

---

## Related Documentation

- **60-flame-ai-integration-patterns.md** - Architectural patterns
- **61-flame-ai-components.md** - Component library
- **52-local-cache-implementation.md** - Caching for performance

---

**Status:** ✅ Complete Advanced Guide  
**Critical:** Update + Render must complete < 16.67ms for 60 FPS  
**Target:** 0 frame drops during AI operations


