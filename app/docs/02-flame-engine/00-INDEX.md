# Flame Engine Documentation Index

**Master Reference:** `docs/master_flutter_flame_spec_v_1_0.md`

## 🎯 Overview

This folder contains comprehensive Flame engine documentation specifically tailored for Unwritten's card-based narrative game. All documentation is aligned with our master Flutter/Flame specification and focuses on achieving premium Unity-level game feel with 60 FPS performance.

## 📚 Documentation Structure

### Core Systems

1. **[Component System](./01-component-system.md)**
   - Complete component lifecycle (onLoad, onMount, onGameResize, onRemove)
   - Component keys and efficient retrieval
   - Priority-based Z-index rendering
   - Component communication patterns for card interactions

2. **[Game Loop & Lifecycle](./02-game-loop-lifecycle.md)**
   - FlameGame structure for Unwritten
   - World and camera setup
   - Component hierarchy (Background, Gameplay, UI layers)
   - Custom update loop extensions
   - Performance metrics tracking

3. **[Sprite Animation System](./03-sprite-animation-system.md)**
   - SpriteAnimationGroupComponent for card states
   - Multi-state animation management (idle, hover, drag, play)
   - Animation event callbacks (onComplete, onFrame)
   - Texture packer integration
   - Dynamic animation speed

### Visual Effects

4. **[Particle Effects](./04-particle-effects.md)**
   - Card play effects (sparkles, trails)
   - Particle composition patterns
   - GPU-accelerated rendering
   - Particle pooling for performance

5. **[Effects System](./05-effects-system.md)**
   - MoveEffect, ScaleEffect, RotateEffect, OpacityEffect
   - SequenceEffect and CombinedEffect chaining
   - Custom EffectController curves
   - Card animation patterns

6. **[Camera & Viewport](./06-camera-viewport.md)**
   - CameraComponent.withFixedResolution for responsive design
   - FixedResolutionViewport configuration
   - Camera follow and zoom effects
   - Multi-viewport for split UI

### Interaction & Collision

7. **[Collision Detection](./07-collision-detection.md)**
   - HasCollisionDetection mixin
   - RectangleHitbox for card boundaries
   - CompositeHitbox for complex shapes
   - Collision callbacks and raycast

8. **[Input Handling](./08-input-handling.md)**
   - TapCallbacks, DragCallbacks, HoverCallbacks
   - Multi-touch support
   - Gesture recognition patterns
   - Input prediction for responsiveness

### Optimization

9. **[Performance Optimization](./09-performance-optimization.md)**
   - Component pooling for cards
   - Sprite batching techniques
   - LOD systems and culling
   - Memory management strategies
   - 60 FPS targets and monitoring

10. **[Flame-Riverpod Integration](./10-flame-riverpod-integration.md)**
    - Manual integration patterns (flame_riverpod has version conflicts)
    - HasGameReference with Riverpod providers
    - Game state synchronization
    - Reactive component updates

11. **[Card Interactions](./11-card-interactions.md)**
    - Complete card drag system implementation
    - Tap, hover, and drag gesture handling
    - State-driven animations
    - Audio and haptic feedback

12. **[Responsive Design](./12-responsive-design.md)**
    - Fixed resolution viewport strategy
    - Breakpoint system for Flutter UI
    - Mobile peek-from-edges pattern
    - Tablet/desktop layouts

13. **[Unwritten Architecture](./13-unwritten-architecture.md)** ⭐
    - Complete game architecture overview
    - Coordinate system (1920×1080 logical space)
    - Component hierarchy and positioning
    - Integration patterns and best practices

## 🎯 Performance Targets

All Flame implementations must meet these targets:

| Metric | Target | Critical |
|--------|--------|----------|
| **FPS** | 60 stable | ✓ |
| **Frame Time** | < 16ms | ✓ |
| **AI Inference** | < 15ms | ✓ |
| **Memory** | < 200MB | ✓ |
| **Battery** | < 10%/30min | ✓ |

## 🔗 Related Documentation

- **Master Spec:** `../../docs/master_flutter_flame_spec_v_1_0.md` (Authoritative source)
- **Visual Generation:** `../../docs/4.visual/` (Asset creation and artistic direction)
- **Architecture:** `../01-architecture/` (Project structure and patterns)
- **State Management:** `../03-state-management/` (Riverpod integration)
- **Performance:** `../05-performance/` (Profiling and optimization)

## 🚀 Quick Start

For immediate implementation guidance:

1. **New to Flame?** Start with [Component System](./01-component-system.md)
2. **Building Cards?** See [Sprite Animation](./03-sprite-animation-system.md) and [Input Handling](./08-input-handling.md)
3. **Performance Issues?** Check [Performance Optimization](./09-performance-optimization.md)
4. **State Integration?** See [Flame-Riverpod Integration](./10-flame-riverpod-integration.md)

---

**Last Updated:** October 15, 2025  
**Flame Version:** 1.32.0  
**Flutter Version:** 3.24.0+


