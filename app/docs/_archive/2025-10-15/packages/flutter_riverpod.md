# Flutter Riverpod - State Management

**Current Project Version**: ^3.0.3  
**Latest Available Version**: ^3.0.3  
**Recommendation**: ✅ UP TO DATE

---

## Overview

Riverpod is a reactive state management library for Flutter that is compile-safe, testable, and flexible. It's a complete rewrite of the Provider pattern without its limitations.

## Key Features

- **Compile-safe**: Catch errors at compile-time, not runtime
- **No BuildContext**: Access providers from anywhere
- **Testable**: Built with testability in mind
- **AsyncValue**: First-class support for loading/error states
- **Auto-dispose**: Automatic state disposal when no longer used
- **Family & AutoDispose**: Advanced modifiers for dynamic state
- **Code Generation**: Generate boilerplate with riverpod_generator

## Installation

```yaml
dependencies:
  flutter_riverpod: ^3.0.3
  riverpod_annotation: ^3.0.3
  
dev_dependencies:
  riverpod_generator: ^3.0.0-dev.11
  build_runner: ^2.4.9
```

## Core Concepts

### Provider Types

```dart
// Simple value provider
final counterProvider = StateProvider<int>((ref) => 0);

// Async provider
final userProvider = FutureProvider<User>((ref) async {
  return await fetchUser();
});

// StateNotifier provider (complex state)
final gameStateProvider = StateNotifierProvider<GameNotifier, GameState>(
  (ref) => GameNotifier(ref.read(aiServiceProvider)),
);
```

### Consumer Widget

```dart
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    
    return Text('Count: $count');
  }
}
```

### Code Generation

```dart
@riverpod
class GameState extends _$GameState {
  @override
  Future<GameModel> build() async {
    return await loadGame();
  }
  
  Future<void> playCard(CardModel card) async {
    // Update state
    state = AsyncValue.data(newGameState);
  }
}
```

## Best Practices

1. **Use ConsumerWidget**: Prefer `ConsumerWidget` over `Consumer` for better performance
2. **Watch vs Read vs Listen**:
   - `watch`: Rebuild when state changes
   - `read`: One-time read, no rebuild
   - `listen`: Side-effects without rebuild

3. **AsyncValue Handling**:
```dart
ref.watch(userProvider).when(
  data: (user) => Text(user.name),
  loading: () => CircularProgressIndicator(),
  error: (err, stack) => Text('Error: $err'),
);
```

4. **Provider Scope**: Always wrap app in `ProviderScope`
```dart
void main() {
  runApp(
    ProviderScope(
      child: MyApp(),
    ),
  );
}
```

## Performance Tips

- Use `.select()` to watch specific parts of state
- Leverage `family` for parameterized providers
- Use `autoDispose` for temporary state
- Avoid creating providers in build methods

## Resources

- **Official Documentation**: https://riverpod.dev/
- **GitHub Repository**: https://github.com/rrousselGit/riverpod
- **Examples**: https://riverpod.dev/docs/getting_started
- **Migration Guide**: https://riverpod.dev/docs/migration/from_provider

## Related Packages

- `riverpod_annotation`: Annotations for code generation
- `riverpod_generator`: Code generator for Riverpod
- `flutter_hooks`: React-like hooks for Flutter (works with Riverpod)
- `riverpod_lint`: Additional lint rules for Riverpod

---

**Last Updated**: October 14, 2025  
**Update Priority**: None (already latest)

