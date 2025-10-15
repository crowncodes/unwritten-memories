# Game Loop & Lifecycle

**Reference:** `docs/master_flutter_flame_spec_v_1_0.md` (Lines 50-88)

## Overview

Unwritten's game loop is built on FlameGame with sophisticated World/Camera architecture, optimized for 60 FPS performance. This document covers the complete game structure, update loop, and lifecycle management.

## FlameGame Structure

### Basic Game Setup

```dart
class UnwrittenGame extends FlameGame 
    with HasCollisionDetection, TapCallbacks, DragCallbacks {
  
  // Game references (singleton pattern)
  late final AudioManager audioManager;
  late final HapticFeedback hapticFeedback;
  late final GameStateNotifier gameState;
  
  @override
  Color backgroundColor() => const Color(0xFF1A1A1A);
  
  @override
  Future<void> onLoad() async {
    // Initialize services
    audioManager = AudioManager();
    hapticFeedback = HapticFeedback();
    
    // Setup world and camera
    await _setupWorldAndCamera();
    
    // Load initial components
    await _loadGameComponents();
    
    AppLogger.info('UnwrittenGame initialized');
  }
  
  Future<void> _setupWorldAndCamera() async {
    final world = World();
    
    // Fixed resolution camera for consistent layout
    final camera = CameraComponent.withFixedResolution(
      world: world,
      width: 1920,
      height: 1080,
    );
    
    camera.viewport = FixedResolutionViewport(
      resolution: Vector2(1920, 1080),
    );
    camera.viewfinder.anchor = Anchor.center;
    
    await addAll([world, camera]);
  }
  
  Future<void> _loadGameComponents() async {
    // Add component hierarchy
    await world.addAll([
      BackgroundLayer(priority: -100),
      GameBoardLayer(priority: 0),
      CardHandLayer(priority: 50),
      UIOverlayLayer(priority: 100),
      DebugOverlay(priority: 1000),
    ]);
  }
}
```

## Component Hierarchy

### Layered Architecture

Unwritten uses a priority-based layer system:

```dart
// Layer priorities (lower renders first/behind)
const PRIORITY_BACKGROUND = -100;
const PRIORITY_BOARD = 0;
const PRIORITY_CARDS = 50;
const PRIORITY_UI = 100;
const PRIORITY_DEBUG = 1000;

class BackgroundLayer extends PositionComponent {
  @override
  int get priority => PRIORITY_BACKGROUND;
  
  @override
  Future<void> onLoad() async {
    // Background visuals, parallax, ambiance
    add(ParallaxBackground());
    add(AmbientParticles());
  }
}

class GameBoardLayer extends PositionComponent {
  @override
  int get priority => PRIORITY_BOARD;
  
  @override
  Future<void> onLoad() async {
    // Game board, zones, placement areas
    add(CardPlayZone());
    add(CharacterPortrait());
  }
}

class CardHandLayer extends PositionComponent {
  @override
  int get priority => PRIORITY_CARDS;
  
  @override
  Future<void> onLoad() async {
    // Player's card hand
    add(CardHand());
  }
}

class UIOverlayLayer extends PositionComponent {
  @override
  int get priority => PRIORITY_UI;
  
  @override
  Future<void> onLoad() async {
    // HUD, buttons, overlays
    add(ResourceDisplay());
    add(TurnCounter());
  }
}
```

## Custom Update Loop

### Game Update Cycle

Override `update()` for custom game logic:

```dart
class UnwrittenGame extends FlameGame {
  // Performance tracking
  final _performanceMonitor = PerformanceMonitor();
  double _accumulatedTime = 0;
  
  @override
  void update(double dt) {
    _performanceMonitor.startFrame();
    
    // Call parent update (updates all components)
    super.update(dt);
    
    // Custom game state updates
    _updateGameState(dt);
    
    // Performance monitoring
    _handlePerformanceMetrics(dt);
    
    _performanceMonitor.endFrame();
  }
  
  void _updateGameState(double dt) {
    _accumulatedTime += dt;
    
    // Update game state at fixed intervals
    if (_accumulatedTime >= 1.0) {
      gameState.incrementPlayTime();
      _accumulatedTime = 0;
    }
    
    // Check win/loss conditions
    if (gameState.shouldCheckEndConditions) {
      _checkGameEnd();
    }
  }
  
  void _handlePerformanceMetrics(double dt) {
    final frameTime = _performanceMonitor.lastFrameTime;
    
    // Log performance issues
    if (frameTime > 16.67) {  // 60 FPS = 16.67ms per frame
      AppLogger.performance('Slow frame detected', {
        'frame_time_ms': frameTime,
        'component_count': children.length,
      });
    }
    
    // Trigger optimization if needed
    if (_performanceMonitor.averageFrameTime > 16.67) {
      _optimizePerformance();
    }
  }
  
  void _optimizePerformance() {
    // Reduce particle count
    final particles = world.query<ParticleSystemComponent>();
    if (particles.length > 10) {
      particles.skip(10).forEach((p) => p.removeFromParent());
    }
    
    // Cull off-screen components
    _cullOffScreenComponents();
  }
}
```

### Fixed Timestep Updates

For physics or consistent gameplay:

```dart
class PhysicsGame extends FlameGame {
  static const fixedDeltaTime = 1 / 60;  // 60 updates per second
  double _accumulator = 0;
  
  @override
  void update(double dt) {
    _accumulator += dt;
    
    // Update at fixed intervals
    while (_accumulator >= fixedDeltaTime) {
      _fixedUpdate(fixedDeltaTime);
      _accumulator -= fixedDeltaTime;
    }
    
    // Render at variable rate
    super.update(dt);
  }
  
  void _fixedUpdate(double dt) {
    // Physics, game logic that needs consistent timing
    gameState.update(dt);
  }
}
```

## Lifecycle Management

### Game Lifecycle Hooks

```dart
class UnwrittenGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    // ✅ One-time initialization
    await _loadAssets();
    await _initializeServices();
    await _setupGame();
  }
  
  @override
  void onMount() {
    // ✅ Called when game is mounted
    // Resume audio, animations
    audioManager.resume();
  }
  
  @override
  void onRemove() {
    // ✅ Called before game is removed
    // Cleanup resources
    audioManager.dispose();
    hapticFeedback.dispose();
    super.onRemove();
  }
  
  @override
  void onGameResize(Vector2 size) {
    // ✅ Handle screen size changes
    super.onGameResize(size);
    
    // Update responsive elements
    _updateResponsiveLayout(size);
  }
  
  void pauseEngine() {
    // Pause game loop
    paused = true;
    audioManager.pauseAll();
  }
  
  void resumeEngine() {
    // Resume game loop
    paused = false;
    audioManager.resumeAll();
  }
}
```

### App Lifecycle Integration

Connect to Flutter's app lifecycle:

```dart
class UnwrittenGameWidget extends StatefulWidget {
  @override
  State<UnwrittenGameWidget> createState() => _UnwrittenGameWidgetState();
}

class _UnwrittenGameWidgetState extends State<UnwrittenGameWidget>
    with WidgetsBindingObserver {
  late final UnwrittenGame _game;
  
  @override
  void initState() {
    super.initState();
    _game = UnwrittenGame();
    WidgetsBinding.instance.addObserver(this);
  }
  
  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }
  
  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    switch (state) {
      case AppLifecycleState.paused:
        _game.pauseEngine();
        _game.audioManager.pauseAll();
      case AppLifecycleState.resumed:
        _game.resumeEngine();
        _game.audioManager.resumeAll();
      case AppLifecycleState.inactive:
        // Save state
        _game.saveGameState();
      case AppLifecycleState.detached:
        // Final cleanup
        _game.dispose();
      case AppLifecycleState.hidden:
        break;
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return GameWidget(game: _game);
  }
}
```

## World & Camera Setup

### Multi-Camera Configuration

```dart
class UnwrittenGame extends FlameGame {
  late CameraComponent mainCamera;
  late CameraComponent uiCamera;
  
  @override
  Future<void> onLoad() async {
    final gameWorld = World();
    final uiWorld = World();
    
    // Main game camera (follows action)
    mainCamera = CameraComponent.withFixedResolution(
      world: gameWorld,
      width: 1920,
      height: 1080,
    )..viewport = FixedResolutionViewport(
        resolution: Vector2(1920, 1080),
      );
    
    // UI camera (static, always visible)
    uiCamera = CameraComponent(
      world: uiWorld,
      viewport: MaxViewport(),
    );
    
    await addAll([
      gameWorld,
      uiWorld,
      mainCamera,
      uiCamera,
    ]);
  }
}
```

### Responsive Viewport

```dart
class ResponsiveGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    final world = World();
    final camera = CameraComponent(world: world);
    
    // Responsive viewport
    camera.viewport = FixedResolutionViewport(
      resolution: Vector2(1920, 1080),
    )..clip = false;  // Allow overflow if needed
    
    await addAll([world, camera]);
  }
  
  @override
  void onGameResize(Vector2 size) {
    super.onGameResize(size);
    
    // Adjust camera based on aspect ratio
    final aspectRatio = size.x / size.y;
    if (aspectRatio < 0.75) {
      // Portrait: adjust width
      camera.viewport = FixedResolutionViewport(
        resolution: Vector2(1080, 1920),
      );
    } else {
      // Landscape: standard
      camera.viewport = FixedResolutionViewport(
        resolution: Vector2(1920, 1080),
      );
    }
  }
}
```

## Performance Metrics Tracking

### Built-in Performance Monitor

```dart
class PerformanceMonitor {
  final _frameTimes = <double>[];
  final _maxSamples = 60;
  double _lastFrameTime = 0;
  Stopwatch? _frameStopwatch;
  
  void startFrame() {
    _frameStopwatch = Stopwatch()..start();
  }
  
  void endFrame() {
    _frameStopwatch?.stop();
    _lastFrameTime = _frameStopwatch!.elapsedMilliseconds.toDouble();
    
    _frameTimes.add(_lastFrameTime);
    if (_frameTimes.length > _maxSamples) {
      _frameTimes.removeAt(0);
    }
  }
  
  double get lastFrameTime => _lastFrameTime;
  
  double get averageFrameTime {
    if (_frameTimes.isEmpty) return 0;
    return _frameTimes.reduce((a, b) => a + b) / _frameTimes.length;
  }
  
  double get currentFps => 1000 / _lastFrameTime;
  
  double get averageFps => 1000 / averageFrameTime;
  
  bool get isRunningSmooth => averageFps >= 55;  // 55+ FPS = smooth
}
```

### Debug Overlay

```dart
class DebugOverlay extends PositionComponent {
  final PerformanceMonitor monitor;
  late TextComponent fpsText;
  late TextComponent componentCountText;
  
  DebugOverlay(this.monitor);
  
  @override
  Future<void> onLoad() async {
    fpsText = TextComponent(
      position: Vector2(10, 10),
      textRenderer: TextPaint(
        style: const TextStyle(
          color: Colors.green,
          fontSize: 16,
          fontFamily: 'monospace',
        ),
      ),
    );
    
    componentCountText = TextComponent(
      position: Vector2(10, 30),
      textRenderer: fpsText.textRenderer,
    );
    
    addAll([fpsText, componentCountText]);
  }
  
  @override
  void update(double dt) {
    super.update(dt);
    
    // Update debug info
    fpsText.text = 'FPS: ${monitor.currentFps.toStringAsFixed(1)}';
    
    final componentCount = parent!.children.length;
    componentCountText.text = 'Components: $componentCount';
    
    // Color code FPS
    if (monitor.currentFps < 55) {
      fpsText.textRenderer = TextPaint(
        style: const TextStyle(color: Colors.red, fontSize: 16),
      );
    } else {
      fpsText.textRenderer = TextPaint(
        style: const TextStyle(color: Colors.green, fontSize: 16),
      );
    }
  }
}
```

## Best Practices

### Initialization Order

```dart
class UnwrittenGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    // 1. Load critical assets first
    await images.loadAll(['background.png', 'cards.png']);
    
    // 2. Initialize services (no async dependencies)
    audioManager = AudioManager();
    hapticFeedback = HapticFeedback();
    
    // 3. Setup world and camera
    await _setupWorldAndCamera();
    
    // 4. Load game components (can use services now)
    await _loadGameComponents();
    
    // 5. Start background processes
    _startPerformanceMonitoring();
  }
}
```

### Resource Management

```dart
class UnwrittenGame extends FlameGame {
  final List<StreamSubscription> _subscriptions = [];
  
  @override
  Future<void> onLoad() async {
    // Track subscriptions for cleanup
    _subscriptions.add(
      gameState.stream.listen(_onStateChange),
    );
  }
  
  @override
  void onRemove() {
    // Clean up all subscriptions
    for (final sub in _subscriptions) {
      sub.cancel();
    }
    _subscriptions.clear();
    
    // Dispose services
    audioManager.dispose();
    hapticFeedback.dispose();
    
    super.onRemove();
  }
}
```

### Update Loop Optimization

```dart
class OptimizedGame extends FlameGame {
  bool _needsUpdate = true;
  
  @override
  void update(double dt) {
    // Skip expensive operations when paused
    if (paused) {
      // Only update critical UI
      _updateCriticalUI(dt);
      return;
    }
    
    // Guard frequent updates
    if (_needsUpdate) {
      _performExpensiveUpdate();
      _needsUpdate = false;
    }
    
    super.update(dt);
  }
  
  void markNeedsUpdate() {
    _needsUpdate = true;
  }
}
```

---

**Next:** [Sprite Animation System](./03-sprite-animation-system.md)  
**Previous:** [Component System](./01-component-system.md)  
**Related:** [Performance Optimization](./09-performance-optimization.md)


