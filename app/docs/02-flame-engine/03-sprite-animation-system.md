# Sprite Animation System

**Reference:** `docs/master_flutter_flame_spec_v_1_0.md` (Lines 90-153)

## Overview

Unwritten's card animation system uses Flame's SpriteAnimationGroupComponent for multi-state animations with frame-perfect event callbacks. This system handles card idle, hover, drag, and play states with smooth transitions.

## Multi-State Animation Management

### SpriteAnimationGroupComponent

The foundation for state-based animations:

```dart
enum CardState {
  idle,
  hover,
  dragging,
  playing,
  returning,
}

class AnimatedCard extends SpriteAnimationGroupComponent<CardState>
    with HasGameReference<UnwrittenGame>, TapCallbacks, DragCallbacks {
  
  final CardData cardData;
  
  AnimatedCard(this.cardData);
  
  @override
  Future<void> onLoad() async {
    // Load sprite sheet
    final spriteSheet = await game.images.load('cards/card_sheet.png');
    
    // Create animations for each state
    animations = {
      CardState.idle: await _createIdleAnimation(spriteSheet),
      CardState.hover: await _createHoverAnimation(spriteSheet),
      CardState.dragging: await _createDraggingAnimation(spriteSheet),
      CardState.playing: await _createPlayingAnimation(spriteSheet),
      CardState.returning: await _createReturningAnimation(spriteSheet),
    };
    
    // Set initial state
    current = CardState.idle;
    
    // Configure animation callbacks
    _setupAnimationCallbacks();
    
    size = Vector2(120, 168);
    anchor = Anchor.center;
  }
  
  Future<SpriteAnimation> _createIdleAnimation(Image spriteSheet) async {
    return SpriteAnimation.fromFrameData(
      spriteSheet,
      SpriteAnimationData.sequenced(
        amount: 8,           // 8 frames
        stepTime: 0.1,       // 100ms per frame
        textureSize: Vector2(128, 179),
        texturePosition: Vector2(0, 0),
        loop: true,
      ),
    );
  }
  
  Future<SpriteAnimation> _createHoverAnimation(Image spriteSheet) async {
    return SpriteAnimation.fromFrameData(
      spriteSheet,
      SpriteAnimationData.sequenced(
        amount: 6,
        stepTime: 0.08,      // Faster animation
        textureSize: Vector2(128, 179),
        texturePosition: Vector2(0, 179),  // Second row
        loop: true,
      ),
    );
  }
  
  Future<SpriteAnimation> _createPlayingAnimation(Image spriteSheet) async {
    return SpriteAnimation.fromFrameData(
      spriteSheet,
      SpriteAnimationData.sequenced(
        amount: 12,
        stepTime: 0.05,      // Fast dramatic animation
        textureSize: Vector2(128, 179),
        texturePosition: Vector2(0, 358),  // Third row
        loop: false,         // ✅ Non-looping, plays once
      ),
    );
  }
}
```

## Animation Event Callbacks

### Frame-Perfect Events

Use animation callbacks for synchronized game logic:

```dart
class AnimatedCard extends SpriteAnimationGroupComponent<CardState> {
  
  void _setupAnimationCallbacks() {
    // onComplete: Called when animation finishes (non-looping)
    animationTickers?[CardState.playing]?.onComplete = () {
      _onPlayAnimationComplete();
    };
    
    // onFrame: Called on specific frames
    animationTickers?[CardState.playing]?.onFrame = (frame) {
      if (frame == 6) {  // Halfway through animation
        _triggerCardEffect();
        game.audioManager.playSfx('card_impact');
      }
    };
    
    // onStart: Called when animation starts
    animationTickers?[CardState.hover]?.onStart = () {
      game.hapticFeedback.lightImpact();
    };
  }
  
  void _onPlayAnimationComplete() {
    // Animation finished, remove card
    removeFromParent();
    game.gameState.onCardPlayed(cardData);
  }
  
  void _triggerCardEffect() {
    // Add particle effect at key frame
    add(ParticleSystemComponent(
      particle: _createSparkleEffect(),
    ));
  }
}
```

### State Transitions with Callbacks

```dart
class AnimatedCard extends SpriteAnimationGroupComponent<CardState> {
  CardState? _previousState;
  
  void changeState(CardState newState) {
    if (current == newState) return;
    
    _previousState = current;
    current = newState;
    
    _onStateTransition(_previousState, newState);
  }
  
  void _onStateTransition(CardState? from, CardState? to) {
    // Handle state-specific logic
    switch (to) {
      case CardState.hover:
        add(ScaleEffect.to(
          Vector2.all(1.2),
          EffectController(duration: 0.2, curve: Curves.easeOut),
        ));
        priority = 100;  // Bring to front
        
      case CardState.dragging:
        game.audioManager.playSfx('card_pickup');
        priority = 1000;
        
      case CardState.playing:
        game.audioManager.playSfx('card_play');
        
      case CardState.idle:
        priority = 0;  // Return to normal layer
        scale = Vector2.all(1.0);
        
      default:
        break;
    }
  }
}
```

## Texture Packer Integration

### Optimized Sprite Sheets

Use texture packer for efficient sprite sheet management:

```dart
class CardSpriteAtlas {
  static late final Map<String, SpriteAnimation> animations;
  
  static Future<void> initialize(UnwrittenGame game) async {
    // Load atlas data (from Texture Packer export)
    final atlasData = await rootBundle.loadString('assets/cards/atlas.json');
    final atlasJson = jsonDecode(atlasData);
    
    // Load atlas image
    final atlasImage = await game.images.load('cards/atlas.png');
    
    // Create animations from atlas
    animations = {};
    
    for (final entry in atlasJson['frames'].entries) {
      final frameName = entry.key;
      final frameData = entry.value;
      
      animations[frameName] = await _createAnimationFromAtlas(
        atlasImage,
        frameData,
      );
    }
  }
  
  static Future<SpriteAnimation> _createAnimationFromAtlas(
    Image atlas,
    Map<String, dynamic> frameData,
  ) async {
    // Parse frame data
    final x = frameData['frame']['x'] as int;
    final y = frameData['frame']['y'] as int;
    final w = frameData['frame']['w'] as int;
    final h = frameData['frame']['h'] as int;
    
    return SpriteAnimation.fromFrameData(
      atlas,
      SpriteAnimationData.sequenced(
        amount: frameData['frames'] as int,
        stepTime: frameData['duration'] as double,
        textureSize: Vector2(w.toDouble(), h.toDouble()),
        texturePosition: Vector2(x.toDouble(), y.toDouble()),
      ),
    );
  }
  
  static SpriteAnimation getAnimation(String name) {
    return animations[name]!;
  }
}
```

### Usage with Atlas

```dart
class OptimizedCard extends SpriteAnimationGroupComponent<CardState> {
  @override
  Future<void> onLoad() async {
    // Use pre-loaded animations from atlas
    animations = {
      CardState.idle: CardSpriteAtlas.getAnimation('card_idle'),
      CardState.hover: CardSpriteAtlas.getAnimation('card_hover'),
      CardState.playing: CardSpriteAtlas.getAnimation('card_play'),
    };
    
    current = CardState.idle;
  }
}
```

## Dynamic Animation Speed

### Runtime Speed Modification

Adjust animation speed based on game state:

```dart
class DynamicCard extends SpriteAnimationGroupComponent<CardState> {
  double _animationSpeedMultiplier = 1.0;
  
  void setAnimationSpeed(double multiplier) {
    _animationSpeedMultiplier = multiplier;
    
    // Update all animation tickers
    for (final ticker in animationTickers?.values ?? []) {
      ticker.timeScale = multiplier;
    }
  }
  
  void enterSlowMotion() {
    setAnimationSpeed(0.3);  // 30% speed
  }
  
  void enterFastForward() {
    setAnimationSpeed(2.0);  // 200% speed
  }
  
  void resetSpeed() {
    setAnimationSpeed(1.0);
  }
  
  // Use for dramatic moments
  void playCardWithSlowMo() {
    enterSlowMotion();
    changeState(CardState.playing);
    
    // Return to normal speed after animation
    Future.delayed(const Duration(milliseconds: 400), resetSpeed);
  }
}
```

### State-Dependent Speed

```dart
class AdaptiveCard extends SpriteAnimationGroupComponent<CardState> {
  @override
  void update(double dt) {
    super.update(dt);
    
    // Adjust speed based on game state
    if (game.gameState.isBattlePhase) {
      setAnimationSpeed(1.5);  // Faster during battle
    } else if (game.gameState.isStoryPhase) {
      setAnimationSpeed(0.8);  // Slower during story
    }
  }
}
```

## Advanced Animation Techniques

### Animation Blending

Smooth transitions between states:

```dart
class BlendedCard extends SpriteAnimationGroupComponent<CardState> {
  double _blendDuration = 0.2;
  
  void transitionToState(CardState newState) {
    if (current == newState) return;
    
    // Create transition effect
    final currentOpacity = opacity;
    
    // Fade out current
    add(OpacityEffect.fadeOut(
      EffectController(duration: _blendDuration / 2),
      onComplete: () {
        // Change state at midpoint
        current = newState;
        
        // Fade in new
        add(OpacityEffect.to(
          currentOpacity,
          EffectController(duration: _blendDuration / 2),
        ));
      },
    ));
  }
}
```

### Synchronized Multi-Component Animation

```dart
class CardWithEffects extends PositionComponent {
  late SpriteAnimationGroupComponent<CardState> cardSprite;
  late SpriteAnimationComponent glowEffect;
  
  @override
  Future<void> onLoad() async {
    // Main card sprite
    cardSprite = await _createCardSprite();
    add(cardSprite);
    
    // Glow effect (separate animation, synchronized)
    glowEffect = await _createGlowEffect();
    glowEffect.opacity = 0;
    add(glowEffect);
  }
  
  void playCard() {
    // Synchronize multiple animations
    cardSprite.current = CardState.playing;
    
    // Sync glow with card animation
    glowEffect
      ..animation!.reset()
      ..opacity = 1.0;
    
    // Callbacks tied to main animation
    cardSprite.animationTickers?[CardState.playing]?.onFrame = (frame) {
      // Sync glow intensity with card animation
      glowEffect.opacity = _calculateGlowIntensity(frame);
    };
  }
  
  double _calculateGlowIntensity(int frame) {
    // Ramp up then down
    const peakFrame = 6;
    if (frame < peakFrame) {
      return frame / peakFrame;
    } else {
      return 1.0 - (frame - peakFrame) / peakFrame;
    }
  }
}
```

### Frame Interpolation

Create smoother animations with interpolated frames:

```dart
class SmoothCard extends SpriteAnimationGroupComponent<CardState> {
  @override
  void render(Canvas canvas) {
    // Enable anti-aliasing for smoother sprites
    canvas.save();
    canvas.scale(1.0);
    
    super.render(canvas);
    
    canvas.restore();
  }
  
  @override
  Future<void> onLoad() async {
    // Use higher frame rate for smoother animation
    animations = {
      CardState.idle: await SpriteAnimation.fromFrameData(
        await game.images.load('card_smooth.png'),
        SpriteAnimationData.sequenced(
          amount: 24,        // More frames = smoother
          stepTime: 0.042,   // ~24 FPS for animation
          textureSize: Vector2(128, 179),
        ),
      ),
    };
  }
}
```

## Performance Optimization

### Animation Pooling

Reuse animation objects:

```dart
class AnimationPool {
  final Map<String, Queue<SpriteAnimation>> _pools = {};
  
  void registerAnimation(String key, SpriteAnimation template) {
    _pools[key] = Queue<SpriteAnimation>();
    
    // Pre-populate with copies
    for (int i = 0; i < 10; i++) {
      _pools[key]!.add(_cloneAnimation(template));
    }
  }
  
  SpriteAnimation getAnimation(String key) {
    final pool = _pools[key];
    if (pool != null && pool.isNotEmpty) {
      return pool.removeFirst();
    }
    // Fallback: create new
    return _createNewAnimation(key);
  }
  
  void returnAnimation(String key, SpriteAnimation animation) {
    animation.reset();
    _pools[key]?.add(animation);
  }
}
```

### Conditional Animation Updates

Skip animation updates when off-screen:

```dart
class OptimizedCard extends SpriteAnimationGroupComponent<CardState> {
  @override
  void update(double dt) {
    // Skip animation update if not visible
    if (!isVisible || opacity <= 0) {
      return;
    }
    
    // Skip if off-screen
    final screenBounds = game.camera.visibleWorldRect;
    if (!screenBounds.containsPoint(absoluteCenter)) {
      return;
    }
    
    super.update(dt);
  }
}
```

### Sprite Sheet Best Practices

```dart
class EfficientCardLoader {
  // ✅ CORRECT: Load once, reuse
  static late final Image cardSpriteSheet;
  
  static Future<void> initialize(UnwrittenGame game) async {
    cardSpriteSheet = await game.images.load('cards/all_cards.png');
  }
  
  static SpriteAnimation createAnimation(int row, int frameCount) {
    // Reuse single sprite sheet
    return SpriteAnimation.fromFrameData(
      cardSpriteSheet,
      SpriteAnimationData.sequenced(
        amount: frameCount,
        stepTime: 0.1,
        textureSize: Vector2(128, 179),
        texturePosition: Vector2(0, row * 179.0),
      ),
    );
  }
}

// ❌ WRONG: Loading sprite sheet every time
class InefficientCard extends SpriteAnimationGroupComponent<CardState> {
  @override
  Future<void> onLoad() async {
    // Don't do this! Loading same image repeatedly
    final spriteSheet = await game.images.load('cards/all_cards.png');
  }
}
```

## Best Practices for Card Animations

### Animation State Machine

```dart
class CardAnimationController {
  final AnimatedCard card;
  CardState _currentState = CardState.idle;
  
  CardAnimationController(this.card);
  
  void transitionTo(CardState newState) {
    if (!_canTransition(_currentState, newState)) {
      AppLogger.warning('Invalid transition: $_currentState -> $newState');
      return;
    }
    
    _currentState = newState;
    card.changeState(newState);
  }
  
  bool _canTransition(CardState from, CardState to) {
    // Define valid transitions
    const validTransitions = {
      CardState.idle: {CardState.hover, CardState.playing},
      CardState.hover: {CardState.idle, CardState.dragging, CardState.playing},
      CardState.dragging: {CardState.hover, CardState.playing},
      CardState.playing: {}, // Terminal state
    };
    
    return validTransitions[from]?.contains(to) ?? false;
  }
}
```

### Memory-Efficient Animation Loading

```dart
class LazyCardAnimations {
  final Map<CardState, Future<SpriteAnimation>?> _animations = {};
  
  Future<SpriteAnimation> getAnimation(
    CardState state,
    UnwrittenGame game,
  ) async {
    // Lazy load animations only when needed
    _animations[state] ??= _loadAnimation(state, game);
    return await _animations[state]!;
  }
  
  Future<SpriteAnimation> _loadAnimation(
    CardState state,
    UnwrittenGame game,
  ) async {
    // Load only the specific animation
    return SpriteAnimation.fromFrameData(
      await game.images.load('cards/${state.name}.png'),
      SpriteAnimationData.sequenced(
        amount: _getFrameCount(state),
        stepTime: _getStepTime(state),
        textureSize: Vector2(128, 179),
      ),
    );
  }
}
```

---

**Next:** [Particle Effects](./04-particle-effects.md)  
**Previous:** [Game Loop & Lifecycle](./02-game-loop-lifecycle.md)  
**Related:** [Effects System](./05-effects-system.md), [Performance Optimization](./09-performance-optimization.md)


