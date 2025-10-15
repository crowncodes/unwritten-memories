# Flame - Game Engine Quick Reference

**Current Project Version**: ^1.20.0  
**Latest Available Version**: ^1.32.0 (Released: August 30, 2025)  
**Recommendation**: ⚠️ UPDATE RECOMMENDED

---

## 📚 Comprehensive Documentation

**→ See [02-flame-engine/](./02-flame-engine/00-INDEX.md) for complete Flame documentation**

This quick reference provides immediate guidance. For in-depth implementation details aligned with Unwritten's architecture, see the numbered documentation.

## Overview

Flame is Unwritten's game engine, providing Unity-level visual effects and 60 FPS performance. It powers all card animations, particle effects, and game visuals.

## Installation

```yaml
dependencies:
  flame: ^1.32.0  # Update from ^1.20.0
```

## Quick Start - Card Component

```dart
class CardComponent extends SpriteAnimationGroupComponent<CardState>
    with HasGameReference<UnwrittenGame>, TapCallbacks, DragCallbacks {
  
  @override
  Future<void> onLoad() async {
    // Load animations
    animations = {
      CardState.idle: await _createIdleAnimation(),
      CardState.hover: await _createHoverAnimation(),
    };
    
    current = CardState.idle;
    size = Vector2(120, 168);
    anchor = Anchor.center;
  }
  
  @override
  void onTapDown(TapDownEvent event) {
    current = CardState.hover;
    game.audioManager.playSfx('card_tap');
  }
  
  @override
  void onDragStart(DragStartEvent event) {
    priority = 1000;  // Bring to front
  }
  
  @override
  void onDragUpdate(DragUpdateEvent event) {
    position += event.delta;
  }
}
```

## Core Systems Reference

| System | Documentation | Use Case |
|--------|---------------|----------|
| **Components** | [01-component-system.md](./02-flame-engine/01-component-system.md) | Card lifecycle, hierarchy |
| **Game Loop** | [02-game-loop-lifecycle.md](./02-flame-engine/02-game-loop-lifecycle.md) | Update cycle, state management |
| **Animations** | [03-sprite-animation-system.md](./02-flame-engine/03-sprite-animation-system.md) | Card states, transitions |
| **Particles** | [04-particle-effects.md](./02-flame-engine/04-particle-effects.md) | Card play effects, sparkles |
| **Effects** | [05-effects-system.md](./02-flame-engine/05-effects-system.md) | Move, scale, rotate cards |
| **Camera** | [06-camera-viewport.md](./02-flame-engine/06-camera-viewport.md) | Responsive layout |
| **Collision** | [07-collision-detection.md](./02-flame-engine/07-collision-detection.md) | Drop zones, hitboxes |
| **Input** | [08-input-handling.md](./02-flame-engine/08-input-handling.md) | Tap, drag, hover |
| **Performance** | [09-performance-optimization.md](./02-flame-engine/09-performance-optimization.md) | 60 FPS optimization |
| **Riverpod** | [10-flame-riverpod-integration.md](./02-flame-engine/10-flame-riverpod-integration.md) | State management |

## Performance Requirements

- **60 FPS** stable gameplay
- **< 16.67ms** frame time
- **< 200** active components
- **< 100** active particles

See [Performance Targets](./00-overview/02-performance-targets.md) for details.

## Official Resources

- **Official Documentation**: https://docs.flame-engine.org/latest/
- **GitHub Repository**: https://github.com/flame-engine/flame
- **Examples**: https://examples.flame-engine.org/
- **Discord Community**: https://discord.com/invite/pxrBmy4

## Master Reference

**→ [`docs/master_flutter_flame_spec_v_1_0.md`](../../docs/master_flutter_flame_spec_v_1_0.md)**

This is the authoritative source for all Flame patterns in Unwritten. All app documentation derives from this master spec.

---

**Last Updated**: October 15, 2025  
**Next Steps**: Read [Component System](./02-flame-engine/01-component-system.md) for card implementation

