# Unwritten App Documentation - Overview

**🎯 Quick Navigation**

## Documentation Structure

This documentation follows a numbered structure aligned with [`docs/master_flutter_flame_spec_v_1_0.md`](../../docs/master_flutter_flame_spec_v_1_0.md) - our authoritative source.

### Core Documentation Sections

1. **[00-overview/](.)** - Project overview, quick start, performance targets
2. **[01-architecture/](../01-architecture/)** - Project structure, Clean Architecture, feature organization
3. **[02-flame-engine/](../02-flame-engine/)** - Complete Flame implementation guide (Components, Animation, Effects, Input)
4. **[03-state-management/](../03-state-management/)** - Riverpod patterns for game state
5. **[04-audio-visuals/](../04-audio-visuals/)** - Audio system, music, SFX, haptics, visual effects
6. **[05-performance/](../05-performance/)** - 60 FPS guidelines, profiling, optimization
7. **[06-integration/](../06-integration/)** - Firebase, AI inference, local storage

### Package-Specific Documentation

- [audioplayers.md](../audioplayers.md) - Audio package with Flame integration
- [flame.md](../flame.md) - Flame quick reference
- [flutter_riverpod.md](../flutter_riverpod.md) - Riverpod with game state examples
- [vibration.md](../vibration.md) - Haptic feedback patterns
- [hive.md](../hive.md) - Local data persistence
- [tflite_flutter.md](../tflite_flutter.md) - AI inference
- [See all package docs →](../README.packages.md)

### Central Documentation Reference

- **[Master Flutter/Flame Spec](../../docs/master_flutter_flame_spec_v_1_0.md)** - Authoritative technical guide
- **[Visual Generation](../../docs/4.visual/)** - Asset creation and artistic direction
- **[AI Systems](../../docs/3.ai/)** - AI architecture and inference
- **[Gameplay](../../docs/2.gameplay/)** - Game design and mechanics

## 🎮 What is Unwritten?

AI-powered card-based narrative game built with Flutter and Flame. Players navigate life decisions through card gameplay while an on-device AI models personality, generates dynamic dialogue, and adapts the story.

### Core Technology

- **Framework:** Flutter 3.24+ with Dart 3.x
- **Game Engine:** Flame 1.32+ (Unity-like feel, 60 FPS target)
- **ML Inference:** TensorFlow Lite (on-device)
- **State Management:** Riverpod (Flutter-native, not Redux)
- **Audio:** audioplayers + just_audio
- **Storage:** Hive (local data) + Firebase (cloud sync)

### Performance Targets

| Metric | Target | Critical |
|--------|--------|----------|
| **FPS** | 60 stable | ✓ |
| **Frame Time** | < 16.67ms | ✓ |
| **AI Inference** | < 15ms | ✓ |
| **Memory** | < 200MB | ✓ |
| **Battery** | < 10%/30min | ✓ |
| **App Size** | < 50MB (no assets) | ✓ |

## 🚀 Quick Start Paths

### I'm New to Flame
1. Read [Master Flame Spec](../../docs/master_flutter_flame_spec_v_1_0.md) (Lines 1-100)
2. Study [Component System](../02-flame-engine/01-component-system.md)
3. Explore [Sprite Animation](../02-flame-engine/03-sprite-animation-system.md)
4. Try [Example: Basic Card](../CARD_INTERACTION_GUIDE.md)

### I'm Building Features
1. Check [Architecture](../01-architecture/01-project-structure.md) for structure
2. Review [Performance Guidelines](../05-performance/01-60fps-guidelines.md)
3. Follow [Feature Organization](../01-architecture/03-feature-organization.md)
4. Integrate [State Management](../03-state-management/02-game-state-providers.md)

### I'm Optimizing Performance
1. Review [Performance Targets](./02-performance-targets.md)
2. Study [Flame Optimization](../02-flame-engine/09-performance-optimization.md)
3. Check [Memory Management](../05-performance/02-memory-management.md)
4. Use [Profiling Tools](../05-performance/04-profiling-tools.md)

### I'm Debugging Issues
1. Check linter: `flutter analyze`
2. Run tests: `flutter test`
3. Profile: DevTools → Performance tab
4. See [Common Issues](../TROUBLESHOOTING.md) (if exists)

## 📋 This Section

- **[01-quick-start.md](./01-quick-start.md)** - Setup, run, and first build
- **[02-performance-targets.md](./02-performance-targets.md)** - Detailed performance metrics and monitoring
- **[03-architecture-principles.md](./03-architecture-principles.md)** - Core architectural decisions

## 🎯 Philosophy

**Battery life and performance are PRIMARY metrics.** Every decision prioritizes:
1. 60 FPS gameplay
2. Premium Unity-level feel
3. On-device AI with <15ms inference
4. Minimal battery impact

---

**Last Updated:** October 15, 2025  
**Flutter Version:** 3.24.0+  
**Flame Version:** 1.32.0


