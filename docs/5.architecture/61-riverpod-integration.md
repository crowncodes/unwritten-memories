# Riverpod Integration

**Last Updated:** October 14, 2025  
**Status:** ✅ Complete

---

## Setup

```yaml
dependencies:
  flutter_riverpod: ^3.0.3
  riverpod_annotation: ^3.0.0

dev_dependencies:
  riverpod_generator: ^3.0.0
  build_runner: ^2.4.0
```

```bash
flutter pub get
flutter pub run build_runner watch
```

---

## Provider Template

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'providers.g.dart';

@riverpod
class MyNotifier extends _$MyNotifier {
  @override
  FutureOr<MyState> build() async {
    return await _loadData();
  }
  
  Future<void> updateData() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      return await _updateData();
    });
  }
}
```

---

## Usage

```dart
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(myNotifierProvider);
    
    return state.when(
      data: (data) => Text(data.toString()),
      loading: () => CircularProgressIndicator(),
      error: (err, stack) => Text('Error: $err'),
    );
  }
}
```

---

## Related Documentation

- **53-state-management-architecture.md** - Full Riverpod patterns

---

**Status:** ✅ Riverpod Integration Complete

