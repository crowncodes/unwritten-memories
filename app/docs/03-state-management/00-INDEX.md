# State Management Documentation Index

## Overview

Unwritten uses **Riverpod** for type-safe, compile-time state management integrated with Flame game components.

## Documentation Files

1. **01-riverpod-setup.md** - Riverpod configuration and patterns
2. **02-game-state-providers.md** - Game state, card state, resource providers
3. **03-notifier-patterns.md** - StateNotifier patterns for game logic

## Quick Reference

### Game State Provider

```dart
final gameStateProvider = StateNotifierProvider<GameStateNotifier, GameState>((ref) {
  return GameStateNotifier();
});

// Usage in widget
class GameScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final gameState = ref.watch(gameStateProvider);
    return Text('Turn ${gameState.currentTurn}');
  }
}
```

### Flame Integration

```dart
class CardComponent extends PositionComponent 
    with HasGameReference<UnwrittenGame> {
  
  @override
  Future<void> onLoad() async {
    // Access providers via game reference
    final gameState = game.ref.read(gameStateProvider);
  }
}
```

---

**Related:** [Flame-Riverpod Integration](../02-flame-engine/10-flame-riverpod-integration.md), [flutter_riverpod.md](../flutter_riverpod.md)


