# Particle Effects

**Reference:** `docs/master_flutter_flame_spec_v_1_0.md` (Lines 154-220)

## Overview

Flame's particle system enables GPU-accelerated visual effects for card plays, impacts, and ambient atmosphere. Unwritten uses particle composition for sparkles, trails, and magical effects that enhance the premium game feel.

## Particle System Basics

### Creating Simple Particles

```dart
class CardPlayEffect extends Component {
  Future<void> createSparkleEffect(Vector2 position) async {
    final sparkleParticle = CircleParticle(
      radius: 3.0,
      paint: Paint()..color = Colors.yellow.withOpacity(0.8),
    );
    
    add(ParticleSystemComponent(
      particle: sparkleParticle,
      position: position,
    ));
  }
}
```

### Particle Lifespan

```dart
// Particle that fades out over 2 seconds
final fadingParticle = CircleParticle(
  radius: 5.0,
  paint: Paint()..color = Colors.white,
  lifespan: 2.0,  // ✅ Auto-removes after 2 seconds
);
```

## Particle Composition

### ComputedParticle for Custom Rendering

Create custom particle behaviors:

```dart
class CardImpactEffect extends Component {
  Future<void> createImpact(Vector2 position) async {
    final impactParticle = ComputedParticle(
      renderer: (canvas, particle) {
        final progress = particle.progress;  // 0.0 to 1.0
        
        // Expanding ring effect
        final radius = 50 * progress;
        final opacity = 1.0 - progress;
        
        final paint = Paint()
          ..color = Colors.orange.withOpacity(opacity)
          ..style = PaintingStyle.stroke
          ..strokeWidth = 3.0;
        
        canvas.drawCircle(Offset.zero, radius, paint);
      },
      lifespan: 0.5,
    );
    
    add(ParticleSystemComponent(
      particle: impactParticle,
      position: position,
    ));
  }
}
```

### AcceleratedParticle for Physics

Add gravity and physics to particles:

```dart
class CardTrailEffect extends Component {
  Future<void> createTrail(Vector2 position) async {
    final trail = ComposedParticle(
      particles: [
        for (int i = 0; i < 20; i++)
          AcceleratedParticle(
            // Initial velocity (random directions)
            speed: Vector2.random() * 200,
            
            // Acceleration (gravity pulls down)
            acceleration: Vector2(0, 300),
            
            child: CircleParticle(
              radius: 2.0,
              paint: Paint()..color = Colors.blue.withOpacity(0.6),
            ),
            
            lifespan: 1.0,
          ),
      ],
    );
    
    add(ParticleSystemComponent(
      particle: trail,
      position: position,
    ));
  }
}
```

### MovingParticle for Linear Motion

Create particles that move from point A to B:

```dart
class CardDrawEffect extends Component {
  Future<void> createDrawEffect(Vector2 from, Vector2 to) async {
    final drawParticle = MovingParticle(
      from: Vector2.zero(),
      to: to - from,  // Relative to component position
      child: CircleParticle(
        radius: 4.0,
        paint: Paint()..color = Colors.white,
      ),
      lifespan: 0.3,
      curve: Curves.easeOut,  // Smooth deceleration
    );
    
    add(ParticleSystemComponent(
      particle: drawParticle,
      position: from,
    ));
  }
}
```

## Advanced Particle Effects

### Card Play Explosion

Comprehensive effect for card being played:

```dart
class CardPlayExplosion extends Component {
  Future<void> create(Vector2 position) async {
    final explosion = ComposedParticle(
      particles: [
        // Core flash
        ComputedParticle(
          renderer: (canvas, particle) {
            final progress = particle.progress;
            final radius = 60 * (1 - progress);
            final opacity = (1 - progress) * 0.8;
            
            final paint = Paint()
              ..color = Color.lerp(
                Colors.white,
                Colors.orange,
                progress,
              )!.withOpacity(opacity)
              ..maskFilter = const MaskFilter.blur(
                BlurStyle.normal,
                10,
              );
            
            canvas.drawCircle(Offset.zero, radius, paint);
          },
          lifespan: 0.3,
        ),
        
        // Sparkles (20 particles)
        for (int i = 0; i < 20; i++)
          AcceleratedParticle(
            speed: Vector2.random() * 300,
            acceleration: Vector2(0, 200),  // Gravity
            child: FadingParticle(
              from: 1.0,
              to: 0.0,
              child: ScalingParticle(
                from: 1.0,
                to: 0.0,
                child: CircleParticle(
                  radius: 3.0,
                  paint: Paint()..color = Colors.yellow,
                ),
              ),
            ),
            lifespan: 0.8,
          ),
        
        // Glow ring
        ComputedParticle(
          renderer: (canvas, particle) {
            final progress = particle.progress;
            final radius = 40 + (60 * progress);
            final opacity = 0.5 * (1 - progress);
            
            final paint = Paint()
              ..color = Colors.blue.withOpacity(opacity)
              ..style = PaintingStyle.stroke
              ..strokeWidth = 2.0
              ..maskFilter = const MaskFilter.blur(
                BlurStyle.normal,
                5,
              );
            
            canvas.drawCircle(Offset.zero, radius, paint);
          },
          lifespan: 0.6,
        ),
      ],
    );
    
    add(ParticleSystemComponent(
      particle: explosion,
      position: position,
    ));
  }
}
```

### Card Hover Shimmer

Subtle ambient effect for hovered cards:

```dart
class CardHoverShimmer extends Component {
  Future<void> create(Vector2 cardPosition, Vector2 cardSize) async {
    final shimmer = ComposedParticle(
      particles: [
        for (int i = 0; i < 5; i++)
          MovingParticle(
            from: Vector2(
              -cardSize.x / 2 + (Random().nextDouble() * cardSize.x),
              cardSize.y / 2,
            ),
            to: Vector2(
              -cardSize.x / 2 + (Random().nextDouble() * cardSize.x),
              -cardSize.y / 2,
            ),
            child: FadingParticle(
              from: 0.0,
              to: 0.6,
              child: CircleParticle(
                radius: 2.0,
                paint: Paint()
                  ..color = Colors.white
                  ..maskFilter = const MaskFilter.blur(
                    BlurStyle.normal,
                    3,
                  ),
              ),
            ),
            lifespan: 1.5,
            curve: Curves.easeInOut,
          ),
      ],
    );
    
    add(ParticleSystemComponent(
      particle: shimmer,
      position: cardPosition,
    ));
  }
}
```

## Particle Pooling for Performance

### Particle Pool Manager

```dart
class ParticlePool {
  final Queue<ParticleSystemComponent> _available = Queue();
  final int _maxPoolSize = 50;
  
  ParticleSystemComponent get() {
    if (_available.isNotEmpty) {
      return _available.removeFirst();
    }
    return ParticleSystemComponent(
      particle: CircleParticle(radius: 1),
    );
  }
  
  void release(ParticleSystemComponent component) {
    if (_available.length < _maxPoolSize) {
      component.particle = null;  // Clear particle
      _available.add(component);
    }
  }
}
```

### Using the Pool

```dart
class OptimizedEffects extends Component {
  final ParticlePool _pool = ParticlePool();
  
  void createEffect(Vector2 position, Particle particle) {
    final component = _pool.get()
      ..particle = particle
      ..position = position;
    
    add(component);
    
    // Return to pool after lifespan
    Future.delayed(
      Duration(milliseconds: (particle.lifespan * 1000).toInt()),
      () => _pool.release(component),
    );
  }
}
```

## GPU-Accelerated Rendering

### BlendMode for Visual Effects

```dart
class BlendModeParticles extends Component {
  Future<void> createGlowEffect(Vector2 position) async {
    // Screen blend mode for additive glow
    final glowParticle = ComputedParticle(
      renderer: (canvas, particle) {
        final paint = Paint()
          ..color = Colors.blue.withOpacity(0.8)
          ..blendMode = BlendMode.screen  // ✅ Additive blending
          ..maskFilter = const MaskFilter.blur(
            BlurStyle.normal,
            15,
          );
        
        canvas.drawCircle(Offset.zero, 20, paint);
      },
      lifespan: 1.0,
    );
    
    add(ParticleSystemComponent(
      particle: glowParticle,
      position: position,
    ));
  }
  
  Future<void> createFireEffect(Vector2 position) async {
    // Multiple blend mode for multiply effect
    final fireParticle = ComputedParticle(
      renderer: (canvas, particle) {
        final progress = particle.progress;
        
        final paint = Paint()
          ..color = Color.lerp(
            Colors.yellow,
            Colors.red,
            progress,
          )!.withOpacity(0.8)
          ..blendMode = BlendMode.plus  // ✅ Brighten effect
          ..maskFilter = const MaskFilter.blur(
            BlurStyle.normal,
            10,
          );
        
        canvas.drawCircle(
          Offset.zero,
          15 * (1 - progress),
          paint,
        );
      },
      lifespan: 0.5,
    );
    
    add(ParticleSystemComponent(
      particle: fireParticle,
      position: position,
    ));
  }
}
```

## Performance Best Practices

### Limit Active Particles

```dart
class ParticleManager extends Component with HasGameReference<UnwrittenGame> {
  static const maxParticles = 100;
  
  void createParticleEffect(Vector2 position, Particle particle) {
    // Count active particles
    final activeParticles = game.world.query<ParticleSystemComponent>();
    
    if (activeParticles.length >= maxParticles) {
      // Remove oldest particle
      activeParticles.first.removeFromParent();
    }
    
    add(ParticleSystemComponent(
      particle: particle,
      position: position,
    ));
  }
}
```

### Adaptive Particle Quality

```dart
class AdaptiveParticles extends Component {
  int _particleCount = 20;
  
  void adjustQuality(double fps) {
    if (fps < 55) {
      // Reduce particles if FPS drops
      _particleCount = max(5, _particleCount - 5);
      AppLogger.performance('Reduced particles', {'count': _particleCount});
    } else if (fps > 58 && _particleCount < 20) {
      // Increase particles if FPS is good
      _particleCount = min(20, _particleCount + 2);
    }
  }
  
  void createEffect(Vector2 position) {
    // Use current particle count
    final effect = ComposedParticle(
      particles: [
        for (int i = 0; i < _particleCount; i++)
          _createSingleParticle(),
      ],
    );
    
    add(ParticleSystemComponent(
      particle: effect,
      position: position,
    ));
  }
}
```

## Reusable Particle Recipes

### Create a Particle Library

```dart
class ParticleRecipes {
  // Sparkle burst
  static Particle sparkle({
    int count = 15,
    Color color = Colors.yellow,
    double intensity = 1.0,
  }) {
    return ComposedParticle(
      particles: [
        for (int i = 0; i < count; i++)
          AcceleratedParticle(
            speed: Vector2.random() * 200 * intensity,
            acceleration: Vector2(0, 300),
            child: FadingParticle(
              from: 1.0,
              to: 0.0,
              child: CircleParticle(
                radius: 2.0,
                paint: Paint()..color = color,
              ),
            ),
            lifespan: 0.8,
          ),
      ],
    );
  }
  
  // Glow ring
  static Particle glowRing({
    Color color = Colors.blue,
    double startRadius = 40,
    double endRadius = 100,
    double duration = 0.6,
  }) {
    return ComputedParticle(
      renderer: (canvas, particle) {
        final progress = particle.progress;
        final radius = startRadius + ((endRadius - startRadius) * progress);
        final opacity = 0.5 * (1 - progress);
        
        final paint = Paint()
          ..color = color.withOpacity(opacity)
          ..style = PaintingStyle.stroke
          ..strokeWidth = 2.0
          ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 5);
        
        canvas.drawCircle(Offset.zero, radius, paint);
      },
      lifespan: duration,
    );
  }
  
  // Trail effect
  static Particle trail({
    Color color = Colors.white,
    int particleCount = 10,
    double spread = 50,
  }) {
    return ComposedParticle(
      particles: [
        for (int i = 0; i < particleCount; i++)
          MovingParticle(
            from: Vector2.zero(),
            to: Vector2(
              (Random().nextDouble() - 0.5) * spread,
              (Random().nextDouble() - 0.5) * spread,
            ),
            child: FadingParticle(
              from: 0.8,
              to: 0.0,
              child: CircleParticle(
                radius: 3.0,
                paint: Paint()..color = color,
              ),
            ),
            lifespan: 0.5,
          ),
      ],
    );
  }
}

// Usage
class CardEffects extends Component {
  void playCard(Vector2 position) {
    add(ParticleSystemComponent(
      particle: ParticleRecipes.sparkle(
        count: 20,
        color: Colors.gold,
        intensity: 1.5,
      ),
      position: position,
    ));
    
    add(ParticleSystemComponent(
      particle: ParticleRecipes.glowRing(
        color: Colors.blue,
      ),
      position: position,
    ));
  }
}
```

---

**Next:** [Effects System](./05-effects-system.md)  
**Previous:** [Sprite Animation System](./03-sprite-animation-system.md)  
**Related:** [Performance Optimization](./09-performance-optimization.md)


