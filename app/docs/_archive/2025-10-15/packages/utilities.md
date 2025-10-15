# Utility Packages Reference

This document covers multiple utility packages used in Unwritten.

---

## UUID - Unique Identifier Generator

**Current Version**: ^4.4.0  
**Latest Version**: ^4.5.0  
**Recommendation**: ⚠️ UPDATE AVAILABLE

### Overview
Generates RFC4122 (v1, v4, v5, v6, v7, v8) UUIDs with crypto-strong random number generator.

### Installation
```yaml
dependencies:
  uuid: ^4.5.0
```

### Usage
```dart
import 'package:uuid/uuid.dart';

const uuid = Uuid();

// Generate v4 UUID (random)
final id = uuid.v4();  // '110ec58a-a0f2-4ac4-8393-c866d813b8d1'

// Generate v1 UUID (time-based)
final timeId = uuid.v1();

// Generate v5 UUID (namespace-based, SHA-1)
final namespaceId = uuid.v5(Uuid.NAMESPACE_URL, 'example.com');
```

### Unwritten Usage
```dart
// Card IDs
final cardId = uuid.v4();
final card = CardModel(id: cardId, ...);

// Session IDs
final sessionId = uuid.v4();

// Transaction IDs
final transactionId = uuid.v4();
```

### Resources
- **Pub.dev**: https://pub.dev/packages/uuid
- **GitHub**: https://github.com/Daegalus/dart-uuid

---

## Intl - Internationalization

**Current Version**: ^0.20.2  
**Latest Version**: ^0.20.2  
**Recommendation**: ✅ UP TO DATE

### Overview
Provides internationalization and localization facilities including message translation, number formatting, date formatting, and bidirectional text.

### Installation
```yaml
dependencies:
  intl: ^0.20.2
```

### Usage
```dart
import 'package:intl/intl.dart';

// Date formatting
final formatter = DateFormat('yyyy-MM-dd');
print(formatter.format(DateTime.now())); // '2025-10-14'

// Number formatting
final numberFormat = NumberFormat.currency(symbol: '\$');
print(numberFormat.format(1234.56)); // '$1,234.56'

// Relative time
final relative = DateFormat.yMMMd().format(date);
```

### Unwritten Usage
```dart
// Game time display
final timeFormat = DateFormat.Hm(); // '14:30'
final dateFormat = DateFormat.yMMMd(); // 'Oct 14, 2025'

// Resource display
final currencyFormat = NumberFormat.compact();
print(currencyFormat.format(1500)); // '1.5K'

// Card costs
final costFormat = NumberFormat.decimalPattern();
print('Energy: ${costFormat.format(card.costs['energy'])}');
```

### Resources
- **Pub.dev**: https://pub.dev/packages/intl
- **Documentation**: https://pub.dev/documentation/intl/latest/

---

## Equatable - Value Equality

**Current Version**: ^2.0.5  
**Latest Version**: ^2.0.7  
**Recommendation**: ⚠️ UPDATE AVAILABLE

### Overview
Simplifies value equality in Dart by overriding `==` and `hashCode` for you based on a list of properties.

### Installation
```yaml
dependencies:
  equatable: ^2.0.7
```

### Usage
```dart
import 'package:equatable/equatable.dart';

class CardModel extends Equatable {
  final String id;
  final String title;
  final CardType type;
  
  const CardModel({
    required this.id,
    required this.title,
    required this.type,
  });
  
  @override
  List<Object?> get props => [id, title, type];
}

// Now CardModel instances compare by value
final card1 = CardModel(id: '1', title: 'Coffee', type: CardType.activity);
final card2 = CardModel(id: '1', title: 'Coffee', type: CardType.activity);

print(card1 == card2); // true (same values)
print(card1.hashCode == card2.hashCode); // true
```

### With Collections
```dart
class GameState extends Equatable {
  final List<CardModel> hand;
  final int turnNumber;
  
  const GameState({
    required this.hand,
    required this.turnNumber,
  });
  
  @override
  List<Object?> get props => [hand, turnNumber];
  
  @override
  bool get stringify => true; // Better toString()
}
```

### Unwritten Models
All data models should extend `Equatable`:
- `CardModel`
- `GameState`
- `RelationshipModel`
- `UserProgress`
- etc.

### Resources
- **Pub.dev**: https://pub.dev/packages/equatable
- **GitHub**: https://github.com/felangel/equatable

---

## Async - Asynchronous Utilities

**Current Version**: ^2.11.0  
**Latest Version**: ^2.11.0  
**Recommendation**: ✅ UP TO DATE

### Overview
Utility functions and classes for working with asynchronous operations.

### Installation
```yaml
dependencies:
  async: ^2.11.0
```

### Key Features

#### StreamQueue
```dart
import 'package:async/async.dart';

final queue = StreamQueue(myStream);
final first = await queue.next;
final second = await queue.next;
```

#### CancelableOperation
```dart
import 'package:async/async.dart';

CancelableOperation<String>? _currentOperation;

Future<void> fetchData() async {
  // Cancel previous operation
  await _currentOperation?.cancel();
  
  _currentOperation = CancelableOperation.fromFuture(
    _performFetch(),
    onCancel: () => print('Cancelled'),
  );
  
  try {
    final result = await _currentOperation!.value;
    print(result);
  } catch (e) {
    if (e is! CancelledException) rethrow;
  }
}
```

#### Result
```dart
import 'package:async/async.dart';

Result<int> divide(int a, int b) {
  if (b == 0) {
    return Result.error('Division by zero');
  }
  return Result.value(a ~/ b);
}

final result = divide(10, 2);
if (result.isValue) {
  print(result.asValue!.value); // 5
} else {
  print(result.asError!.error);
}
```

### Unwritten Usage
```dart
// AI Service with cancellation
class AIService {
  CancelableOperation<AIResponse>? _currentInference;
  
  Future<AIResponse> predict(AIRequest request) async {
    await _currentInference?.cancel();
    
    _currentInference = CancelableOperation.fromFuture(
      _runInference(request),
    );
    
    return await _currentInference!.value;
  }
  
  void dispose() {
    _currentInference?.cancel();
  }
}
```

### Resources
- **Pub.dev**: https://pub.dev/packages/async
- **API Docs**: https://pub.dev/documentation/async/latest/

---

## Path Provider - File System Paths

**Current Version**: ^2.1.3  
**Latest Version**: ^2.1.4  
**Recommendation**: ⚠️ UPDATE AVAILABLE

### Overview
Finds commonly used locations on the filesystem. Supports Android, iOS, Linux, macOS, Windows.

### Installation
```yaml
dependencies:
  path_provider: ^2.1.4
```

### Usage
```dart
import 'package:path_provider/path_provider.dart';
import 'dart:io';

// Get app documents directory
final directory = await getApplicationDocumentsDirectory();
print(directory.path);

// Get temporary directory
final tempDir = await getTemporaryDirectory();

// Get app support directory
final appDir = await getApplicationSupportDirectory();
```

### Unwritten Usage
```dart
// Initialize Hive with path_provider
import 'package:hive_flutter/hive_flutter.dart';
import 'package:path_provider/path_provider.dart';

Future<void> initializeStorage() async {
  final appDir = await getApplicationDocumentsDirectory();
  await Hive.init(appDir.path);
  
  // Open boxes
  await Hive.openBox<CardModel>('cards');
}
```

### Resources
- **Pub.dev**: https://pub.dev/packages/path_provider
- **Platform Paths**: Different per platform (see documentation)

---

**Last Updated**: October 14, 2025  
**Packages Covered**: uuid, intl, equatable, async, path_provider

