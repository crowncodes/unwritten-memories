# Flame - Game Engine

**Current Project Version**: ^1.20.0  
**Latest Available Version**: ^1.32.0 (Released: August 30, 2025)  
**Recommendation**: ⚠️ UPDATE RECOMMENDED

---

## Overview

Flame is a minimalist Flutter game engine that provides a set of modular components to build 2D games. It offers features like a game loop, component system, input handling, and physics integration.

## What's New in 1.32.0

- Refactored `MutableRSTransform` from `flame_tiled` into core
- Added `renderLine` helper to canvas extensions
- Performance improvements for component systems
- Enhanced collision detection algorithms
- Better integration with Flutter 3.16.0

## Installation

```yaml
dependencies:
  flame: ^1.32.0
```

## Key Features

- **Component System**: Modular architecture with `PositionComponent`, `SpriteComponent`, etc.
- **Game Loop**: 60 FPS optimized game loop with fixed timestep support
- **Input Handling**: `TapCallbacks`, `DragCallbacks`, `HoverCallbacks` mixins
- **Effects System**: Built-in animation effects (`MoveEffect`, `ScaleEffect`, `RotateEffect`, etc.)
- **Collision Detection**: Hitbox-based collision system
- **Camera System**: Advanced camera with viewport and world support
- **Particle System**: Flexible particle effects
- **Sprite Rendering**: Efficient sprite and sprite sheet rendering

## Core Components

### Game Class
```dart
class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    // Initialize game components
  }
  
  @override
  void update(double dt) {
    super.update(dt);
    // Game logic updates
  }
}
```

### PositionComponent
```dart
class MyComponent extends PositionComponent with TapCallbacks {
  @override
  Future<void> onLoad() async {
    size = Vector2(100, 100);
    position = Vector2(50, 50);
  }
}
```

## Performance Targets

- 60 FPS on mid-range devices
- < 16ms frame time
- Efficient memory usage with component pooling
- Minimal GC pressure

## Resources

- **Official Documentation**: https://docs.flame-engine.org/latest/
- **GitHub Repository**: https://github.com/flame-engine/flame
- **Release Notes**: https://github.com/flame-engine/flame/releases
- **Examples**: https://examples.flame-engine.org/
- **Discord Community**: https://discord.com/invite/pxrBmy4

## Migration Notes (1.20.0 → 1.32.0)

- Check for breaking changes in component system
- Review any custom renderers for canvas API changes
- Test collision detection if using hitboxes
- Update any flame_tiled usage (MutableRSTransform moved to core)

## Related Packages

- `flame_audio`: Audio support for Flame games
- `flame_forge2d`: Box2D physics integration
- `flame_tiled`: Tiled map editor integration
- `flame_svg`: SVG rendering support

---

**Last Updated**: October 14, 2025  
**Update Priority**: Medium (significant improvements available)

