# Code Generation Packages Reference

This document covers all code generation packages used in Unwritten.

---

## Freezed - Immutable Data Classes

**Current Version**: freezed ^2.5.2, freezed_annotation ^2.4.1  
**Latest Version**: freezed ^2.5.7, freezed_annotation ^2.4.4  
**Recommendation**: ⚠️ UPDATE AVAILABLE

### Overview
Code generator for data classes with immutability, unions/sealed classes, and copyWith.

### Installation
```yaml
dependencies:
  freezed_annotation: ^2.4.4
  
dev_dependencies:
  freezed: ^2.5.7
  build_runner: ^2.4.12
```

### Usage
```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'game_state.freezed.dart';

@freezed
class GameState with _$GameState {
  const factory GameState({
    required List<CardModel> hand,
    required int turnNumber,
    required ResourcesModel resources,
    @Default(false) bool isLoading,
  }) = _GameState;
  
  // Add custom methods
  const GameState._();
  
  bool get canPlayCard => resources.energy >= 1 && hand.isNotEmpty;
}

// Generate code
// flutter pub run build_runner build
```

### Features

#### CopyWith
```dart
final newState = state.copyWith(
  turnNumber: state.turnNumber + 1,
  isLoading: false,
);
```

#### Unions/Sealed Classes
```dart
@freezed
class AIResult with _$AIResult {
  const factory AIResult.success(AIResponse response) = Success;
  const factory AIResult.loading() = Loading;
  const factory AIResult.error(String message) = Error;
}

// Pattern matching
result.when(
  success: (response) => Text(response.text),
  loading: () => CircularProgressIndicator(),
  error: (msg) => Text('Error: $msg'),
);
```

#### With JSON
```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'card_model.freezed.dart';
part 'card_model.g.dart';

@freezed
class CardModel with _$CardModel {
  const factory CardModel({
    required String id,
    required String title,
    required CardType type,
  }) = _CardModel;
  
  factory CardModel.fromJson(Map<String, dynamic> json) =>
      _$CardModelFromJson(json);
}
```

### Best Practices
1. Use `@Default()` for optional fields with defaults
2. Add `const CardModel._();` for custom methods
3. Use unions for state management
4. Always run build_runner after changes

### Resources
- **Pub.dev**: https://pub.dev/packages/freezed
- **Documentation**: https://pub.dev/packages/freezed#usage
- **GitHub**: https://github.com/rrousselGit/freezed

---

## JSON Serialization

**Current Version**: json_annotation ^4.9.0, json_serializable ^6.8.0  
**Latest Version**: json_annotation ^4.9.0, json_serializable ^6.9.0  
**Recommendation**: ⚠️ MINOR UPDATE AVAILABLE

### Overview
Generates JSON serialization/deserialization code at compile time.

### Installation
```yaml
dependencies:
  json_annotation: ^4.9.0
  
dev_dependencies:
  json_serializable: ^6.9.0
  build_runner: ^2.4.12
```

### Usage
```dart
import 'package:json_annotation/json_annotation.dart';

part 'card_model.g.dart';

@JsonSerializable()
class CardModel {
  final String id;
  final String title;
  
  @JsonKey(name: 'card_type')
  final CardType type;
  
  @JsonKey(defaultValue: {})
  final Map<String, double> costs;
  
  @JsonKey(includeIfNull: false)
  final String? description;
  
  CardModel({
    required this.id,
    required this.title,
    required this.type,
    required this.costs,
    this.description,
  });
  
  factory CardModel.fromJson(Map<String, dynamic> json) =>
      _$CardModelFromJson(json);
  
  Map<String, dynamic> toJson() => _$CardModelToJson(this);
}

// Generate code
// flutter pub run build_runner build
```

### Advanced Features

#### Custom Converters
```dart
class TimestampConverter implements JsonConverter<DateTime, int> {
  const TimestampConverter();
  
  @override
  DateTime fromJson(int timestamp) =>
      DateTime.fromMillisecondsSinceEpoch(timestamp);
  
  @override
  int toJson(DateTime date) => date.millisecondsSinceEpoch;
}

@JsonSerializable()
class Event {
  @TimestampConverter()
  final DateTime createdAt;
  
  Event(this.createdAt);
}
```

#### Enum Serialization
```dart
@JsonEnum(valueField: 'value')
enum CardType {
  activity('activity'),
  relationship('relationship'),
  place('place');
  
  final String value;
  const CardType(this.value);
}
```

### Best Practices
1. Use `@JsonKey()` for field customization
2. Create custom converters for complex types
3. Use `explicitToJson: true` for nested objects
4. Set `fieldRename: FieldRename.snake` for consistency

### Resources
- **Pub.dev**: https://pub.dev/packages/json_serializable
- **Documentation**: https://pub.dev/packages/json_serializable#readme

---

## Build Runner - Code Generation

**Current Version**: ^2.4.9  
**Latest Version**: ^2.4.12  
**Recommendation**: ⚠️ UPDATE AVAILABLE

### Overview
A build system for Dart that powers code generation.

### Installation
```yaml
dev_dependencies:
  build_runner: ^2.4.12
```

### Commands

#### One-time Build
```bash
# Generate all code
flutter pub run build_runner build

# Delete conflicting outputs
flutter pub run build_runner build --delete-conflicting-outputs
```

#### Watch Mode
```bash
# Continuous generation
flutter pub run build_runner watch

# With cleanup
flutter pub run build_runner watch --delete-conflicting-outputs
```

#### Clean
```bash
# Remove generated files
flutter pub run build_runner clean
```

### Unwritten Build Script
```bash
# scripts/generate.sh
#!/bin/bash

echo "Cleaning previous build..."
flutter pub run build_runner clean

echo "Generating code..."
flutter pub run build_runner build --delete-conflicting-outputs

echo "Done!"
```

### Best Practices
1. Run build_runner after model changes
2. Use watch mode during development
3. Clean before important builds
4. Add generated files to `.gitignore`
5. Run once before running tests

### Resources
- **Pub.dev**: https://pub.dev/packages/build_runner
- **Documentation**: https://pub.dev/packages/build_runner#usage

---

## Riverpod Generator

**Current Version**: ^3.0.0-dev.11  
**Latest Version**: ^3.0.3  
**Recommendation**: ⚠️ UPDATE TO STABLE

### Overview
Code generator for Riverpod providers using annotations.

### Installation
```yaml
dependencies:
  riverpod_annotation: ^3.0.3
  
dev_dependencies:
  riverpod_generator: ^3.0.3
  build_runner: ^2.4.12
```

### Usage
```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'game_providers.g.dart';

@riverpod
class GameState extends _$GameState {
  @override
  Future<GameModel> build() async {
    return await loadGame();
  }
  
  Future<void> playCard(CardModel card) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final newGame = await _gameService.playCard(card);
      return newGame;
    });
  }
}

// Usage in widgets
class GameScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final gameState = ref.watch(gameStateProvider);
    
    return gameState.when(
      data: (game) => GameView(game: game),
      loading: () => LoadingScreen(),
      error: (err, stack) => ErrorScreen(error: err),
    );
  }
}
```

### Provider Types
```dart
// Simple provider
@riverpod
String greeting(GreetingRef ref) => 'Hello';

// Async provider
@riverpod
Future<User> user(UserRef ref, String id) async {
  return await fetchUser(id);
}

// Stream provider
@riverpod
Stream<List<Event>> events(EventsRef ref) {
  return eventStream;
}

// Class-based provider (stateful)
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;
  
  void increment() => state++;
}
```

### Resources
- **Pub.dev**: https://pub.dev/packages/riverpod_generator
- **Documentation**: https://riverpod.dev/docs/concepts/about_code_generation

---

## Hive Generator

**Current Version**: ^2.0.1  
**Latest Version**: ^2.0.1  
**Recommendation**: ✅ UP TO DATE

### Overview
Generates TypeAdapters for Hive data classes.

### Installation
```yaml
dependencies:
  hive: ^2.2.3
  
dev_dependencies:
  hive_generator: ^2.0.1
  build_runner: ^2.4.12
```

### Usage
```dart
import 'package:hive/hive.dart';

part 'card_model.g.dart';

@HiveType(typeId: 0)
class CardModel {
  @HiveField(0)
  final String id;
  
  @HiveField(1)
  final String title;
  
  @HiveField(2)
  final CardType type;
  
  CardModel({
    required this.id,
    required this.title,
    required this.type,
  });
}

// Register adapter
Hive.registerAdapter(CardModelAdapter());
```

### Type IDs
- Assign unique typeId (0-223) to each model
- Keep a registry to avoid conflicts

```dart
// Type ID Registry
// 0: CardModel
// 1: GameState
// 2: UserProgress
// 3: RelationshipModel
```

### Resources
- **Pub.dev**: https://pub.dev/packages/hive_generator
- **Hive Docs**: https://docs.hivedb.dev/#/custom-objects/type_adapters

---

**Last Updated**: October 14, 2025  
**Packages Covered**: freezed, json_serializable, build_runner, riverpod_generator, hive_generator

