# Storage & Persistence Integration

**Last Updated:** October 14, 2025  
**Status:** ✅ Complete

---

## Setup

```yaml
dependencies:
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  path_provider: ^2.1.0
```

---

## Initialization

```dart
import 'package:hive_flutter/hive_flutter.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Hive.initFlutter();
  
  // Register adapters
  Hive.registerAdapter(CardAdapter());
  Hive.registerAdapter(GameStateAdapter());
  
  // Open boxes
  await Hive.openBox<Card>('cards');
  await Hive.openBox('settings');
  
  runApp(MyApp());
}
```

---

## Storage Service

```dart
class StorageService {
  static final _cardsBox = Hive.box<Card>('cards');
  static final _settingsBox = Hive.box('settings');
  
  // Save card
  static Future<void> saveCard(Card card) async {
    await _cardsBox.put(card.id, card);
  }
  
  // Get card
  static Card? getCard(String id) {
    return _cardsBox.get(id);
  }
  
  // Get all cards
  static List<Card> getAllCards() {
    return _cardsBox.values.toList();
  }
  
  // Save setting
  static Future<void> saveSetting(String key, dynamic value) async {
    await _settingsBox.put(key, value);
  }
  
  // Get setting
  static T? getSetting<T>(String key) {
    return _settingsBox.get(key) as T?;
  }
}
```

---

## Type Adapter

```dart
class CardAdapter extends TypeAdapter<Card> {
  @override
  final int typeId = 0;
  
  @override
  Card read(BinaryReader reader) {
    return Card(
      id: reader.readString(),
      title: reader.readString(),
      // ...
    );
  }
  
  @override
  void write(BinaryWriter writer, Card obj) {
    writer.writeString(obj.id);
    writer.writeString(obj.title);
    // ...
  }
}
```

---

**Status:** ✅ Storage Integration Complete

