# Audio & Visuals Documentation Index

## Overview

Comprehensive audio system with music, SFX, haptic feedback, and visual effects for premium game feel.

## Documentation Files

1. **01-audio-system.md** - Audio architecture and managers
2. **02-music-manager.md** - Background music, adaptive audio
3. **03-sfx-pool.md** - Sound effects pooling and optimization
4. **04-haptic-feedback.md** - Tactile feedback patterns
5. **05-visual-effects.md** - Particles, shaders, post-processing

## Quick Reference

### Play Sound Effect

```dart
game.audioManager.playSfx('card_play');
```

### Play Music

```dart
game.audioManager.playMusic('background_theme', loop: true);
```

### Haptic Feedback

```dart
game.hapticFeedback.lightImpact();    // Subtle
game.hapticFeedback.mediumImpact();   // Card play
game.hapticFeedback.heavyImpact();    // Major event
```

---

**Related:** [audioplayers.md](../audioplayers.md), [vibration.md](../vibration.md), [Particle Effects](../02-flame-engine/04-particle-effects.md)


