# Hive - Local Database

**Current Project Version**: ^2.2.3  
**Latest Available Version**: ^2.2.3  
**Recommendation**: ✅ UP TO DATE

---

## Overview

Hive is a lightweight and blazing fast key-value database written in pure Dart. Perfect for mobile apps, it's ideal for local storage, caching, and offline-first architectures.

## Key Features

- **Fast**: Faster than SharedPreferences and SQLite
- **Lightweight**: No native dependencies
- **Strongly Typed**: Type-safe boxes with code generation
- **Cross-Platform**: Works on mobile, desktop, and web
- **Encrypted**: Built-in AES-256 encryption
- **Lazy Loading**: Load data only when needed
- **No Native Dependencies**: Pure Dart implementation

## Installation

```yaml
dependencies:
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  
dev_dependencies:
  hive_generator: ^2.0.1
  build_runner: ^2.4.9
```

## Basic Usage

### Initialize Hive

```dart
import 'package:hive_flutter/hive_flutter.dart';

void main() async {
  await Hive.initFlutter();
  
  // Register adapters
  Hive.registerAdapter(CardModelAdapter());
  Hive.registerAdapter(GameStateAdapter());
  
  // Open boxes
  await Hive.openBox<CardModel>('cards');
  await Hive.openBox<GameState>('gameState');
  
  runApp(MyApp());
}
```

### Create Type Adapter

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
  final Map<String, double> costs;
  
  CardModel({
    required this.id,
    required this.title,
    required this.costs,
  });
}
```

### CRUD Operations

```dart
// Get box
final box = Hive.box<CardModel>('cards');

// Create/Update
await box.put('card_001', card);

// Read
final card = box.get('card_001');

// Read all
final allCards = box.values.toList();

// Delete
await box.delete('card_001');

// Clear all
await box.clear();
```

### Lazy Boxes (Large Data)

```dart
// Open lazy box (loads data on-demand)
final lazyBox = await Hive.openLazyBox<LargeData>('largeData');

// Get data (async)
final data = await lazyBox.get('key');
```

### Encrypted Boxes

```dart
import 'package:hive/hive.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

// Generate encryption key
final secureStorage = FlutterSecureStorage();
var encryptionKey = await secureStorage.read(key: 'hive_key');
if (encryptionKey == null) {
  final key = Hive.generateSecureKey();
  await secureStorage.write(
    key: 'hive_key',
    value: base64UrlEncode(key),
  );
}

// Open encrypted box
final encryptedBox = await Hive.openBox(
  'secure',
  encryptionCipher: HiveAesCipher(key),
);
```

## Best Practices

1. **Close Boxes**: Close boxes when app terminates
```dart
@override
void dispose() {
  Hive.close();
  super.dispose();
}
```

2. **Type IDs**: Use unique typeIds for each adapter (0-223)

3. **Box Names**: Use descriptive, unique box names

4. **Compact Boxes**: Periodically compact boxes to reclaim space
```dart
await box.compact();
```

5. **Migrations**: Handle schema changes carefully
```dart
if (box.get('version') != currentVersion) {
  // Migrate data
  await migrateData(box);
  await box.put('version', currentVersion);
}
```

## Performance Tips

- Use lazy boxes for large datasets
- Limit box size (< 10,000 items per box)
- Use compaction to reduce file size
- Consider box per feature (not one giant box)
- Avoid frequent opens/closes

## Common Use Cases

### Settings Storage
```dart
final settings = await Hive.openBox('settings');
await settings.put('theme', 'dark');
final theme = settings.get('theme', defaultValue: 'light');
```

### User Progress
```dart
final progress = await Hive.openBox<UserProgress>('progress');
await progress.put('current', userProgress);
```

### Cache API Responses
```dart
final cache = await Hive.openBox<String>('apiCache');
await cache.put('user_${userId}', jsonEncode(user));
```

## Resources

- **Official Documentation**: https://docs.hivedb.dev/
- **GitHub Repository**: https://github.com/isar/hive
- **Examples**: https://github.com/isar/hive/tree/master/hive/example
- **Migration Guide**: https://docs.hivedb.dev/#/migration/from_shared_preferences

## Alternatives

- **Isar**: By same author, more features but larger
- **SharedPreferences**: Simpler but slower
- **SQLite (sqflite)**: Relational database, more complex

---

**Last Updated**: October 14, 2025  
**Update Priority**: None (already latest)

