# Local Storage with Hive

**Package:** `hive ^2.2.3`  
**Status:** ✅ UP TO DATE  
**Flame Integration:** Complete

---

## Overview

Fast, lightweight key-value database for Unwritten, providing local storage for game saves, player progress, card collections, and cached data. Pure Dart implementation with no native dependencies.

## Why Hive?

- ✅ **Fast**: 10x faster than SharedPreferences, faster than SQLite
- ✅ **Lightweight**: < 1.5MB, no native dependencies
- ✅ **Type-Safe**: Strongly typed with code generation
- ✅ **Cross-Platform**: Mobile, desktop, and web
- ✅ **Encrypted**: Built-in AES-256 encryption
- ✅ **Lazy Loading**: Load data only when needed
- ✅ **60 FPS Safe**: Non-blocking async operations

---

## Installation

### Package Setup

```yaml
dependencies:
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  
dev_dependencies:
  hive_generator: ^2.0.1
  build_runner: ^2.4.12
```

### Generate Code

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

---

## Initialization

### App Startup

```dart
import 'package:hive_flutter/hive_flutter.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Hive
  await Hive.initFlutter();
  
  // Register type adapters
  Hive.registerAdapter(CardModelAdapter());
  Hive.registerAdapter(GameStateAdapter());
  Hive.registerAdapter(UserProgressAdapter());
  Hive.registerAdapter(RelationshipModelAdapter());
  Hive.registerAdapter(PersonalityTraitsAdapter());
  
  // Open boxes
  await Hive.openBox<CardModel>('cards');
  await Hive.openBox<GameState>('game_state');
  await Hive.openBox<UserProgress>('user_progress');
  await Hive.openBox('settings');
  
  AppLogger.info('Hive initialized', data: {
    'boxes_opened': Hive.box('settings').isOpen,
  });
  
  runApp(const ProviderScope(child: UnwrittenApp()));
}
```

---

## Type Adapters

### Create Model with Hive Annotations

```dart
import 'package:hive/hive.dart';

part 'card_model.g.dart';

@HiveType(typeId: 0)
class CardModel extends HiveObject {
  @HiveField(0)
  final String id;
  
  @HiveField(1)
  final String title;
  
  @HiveField(2)
  final String description;
  
  @HiveField(3)
  final CardType type;
  
  @HiveField(4)
  final Map<String, double> costs;
  
  @HiveField(5)
  final List<String> tags;
  
  @HiveField(6)
  final DateTime? acquiredAt;
  
  CardModel({
    required this.id,
    required this.title,
    required this.description,
    required this.type,
    required this.costs,
    required this.tags,
    this.acquiredAt,
  });
}

// Enum adapter
@HiveType(typeId: 1)
enum CardType {
  @HiveField(0)
  activity,
  
  @HiveField(1)
  relationship,
  
  @HiveField(2)
  place,
  
  @HiveField(3)
  event,
}
```

### Type ID Registry

**Important:** Each model needs a unique typeId (0-223)

```dart
// Type ID Registry for Unwritten
// 0: CardModel
// 1: CardType enum
// 2: GameState
// 3: UserProgress
// 4: RelationshipModel
// 5: PersonalityTraits
// 6: LifeMeters
// 7: Resources
// 8: TimelineState
// ... reserve 9-20 for future game models
```

---

## Basic Operations

### CRUD Operations

```dart
// Get box
final cardsBox = Hive.box<CardModel>('cards');

// Create/Update
await cardsBox.put('card_001', card);

// Read single
final card = cardsBox.get('card_001');

// Read all
final allCards = cardsBox.values.toList();

// Read with default
final card = cardsBox.get('card_999', defaultValue: defaultCard);

// Check exists
final exists = cardsBox.containsKey('card_001');

// Delete
await cardsBox.delete('card_001');

// Clear all
await cardsBox.clear();

// Count
final count = cardsBox.length;
```

### Lazy Boxes (For Large Data)

```dart
// Open lazy box (loads data on-demand)
final scenesBox = await Hive.openLazyBox<SceneData>('scenes');

// Get data (async)
final scene = await scenesBox.get('scene_001');

// Put data
await scenesBox.put('scene_001', sceneData);
```

---

## Unwritten Storage Services

### Game Save Service

```dart
@riverpod
class GameSaveService extends _$GameSaveService {
  late Box<GameState> _gameBox;
  
  @override
  Future<void> build() async {
    _gameBox = Hive.box<GameState>('game_state');
  }
  
  /// Save current game state
  Future<void> saveGame(GameState state) async {
    try {
      await _gameBox.put('current', state);
      
      AppLogger.info('Game saved', data: {
        'week': state.currentWeek,
        'day': state.currentDay,
        'cards_in_hand': state.hand.length,
      });
    } catch (e, stack) {
      AppLogger.error('Failed to save game', e, stack);
      throw SaveGameException('Could not save game: $e');
    }
  }
  
  /// Load saved game
  Future<GameState?> loadGame() async {
    try {
      final state = _gameBox.get('current');
      
      if (state != null) {
        AppLogger.info('Game loaded', data: {
          'week': state.currentWeek,
          'day': state.currentDay,
        });
      }
      
      return state;
    } catch (e, stack) {
      AppLogger.error('Failed to load game', e, stack);
      return null;
    }
  }
  
  /// Create autosave slot
  Future<void> autoSave(GameState state) async {
    await _gameBox.put('autosave', state);
    await _gameBox.put('autosave_timestamp', DateTime.now().toIso8601String());
  }
  
  /// List all save slots
  List<SaveSlot> listSaves() {
    final saves = <SaveSlot>[];
    
    for (final key in _gameBox.keys) {
      final state = _gameBox.get(key);
      if (state != null) {
        saves.add(SaveSlot(
          id: key.toString(),
          state: state,
          savedAt: state.lastSavedAt,
        ));
      }
    }
    
    return saves..sort((a, b) => b.savedAt.compareTo(a.savedAt));
  }
  
  /// Delete save slot
  Future<void> deleteSave(String slotId) async {
    await _gameBox.delete(slotId);
    AppLogger.info('Save deleted', data: {'slot': slotId});
  }
}
```

### Card Collection Service

```dart
@riverpod
class CardCollectionService extends _$CardCollectionService {
  late Box<CardModel> _cardsBox;
  
  @override
  Future<void> build() async {
    _cardsBox = Hive.box<CardModel>('cards');
  }
  
  /// Add card to collection
  Future<void> addCard(CardModel card) async {
    final cardWithTimestamp = card.copyWith(
      acquiredAt: DateTime.now(),
    );
    
    await _cardsBox.put(card.id, cardWithTimestamp);
    
    AppLogger.info('Card added to collection', data: {
      'id': card.id,
      'title': card.title,
    });
  }
  
  /// Get all owned cards
  List<CardModel> getOwnedCards() {
    return _cardsBox.values.toList()
      ..sort((a, b) => (b.acquiredAt ?? DateTime.now())
          .compareTo(a.acquiredAt ?? DateTime.now()));
  }
  
  /// Get cards by type
  List<CardModel> getCardsByType(CardType type) {
    return _cardsBox.values
        .where((card) => card.type == type)
        .toList();
  }
  
  /// Check if card is owned
  bool hasCard(String cardId) {
    return _cardsBox.containsKey(cardId);
  }
  
  /// Get collection stats
  CollectionStats getStats() {
    final cards = _cardsBox.values.toList();
    
    return CollectionStats(
      total: cards.length,
      byType: {
        CardType.activity: cards.where((c) => c.type == CardType.activity).length,
        CardType.relationship: cards.where((c) => c.type == CardType.relationship).length,
        CardType.place: cards.where((c) => c.type == CardType.place).length,
        CardType.event: cards.where((c) => c.type == CardType.event).length,
      },
      recentAcquisitions: cards
          .where((c) => c.acquiredAt != null)
          .where((c) => c.acquiredAt!.isAfter(
              DateTime.now().subtract(Duration(days: 7))))
          .length,
    );
  }
}
```

### Settings Service

```dart
@riverpod
class SettingsService extends _$SettingsService {
  late Box _settingsBox;
  
  @override
  Future<void> build() async {
    _settingsBox = Hive.box('settings');
  }
  
  // Audio settings
  bool get musicEnabled => _settingsBox.get('music_enabled', defaultValue: true);
  set musicEnabled(bool value) => _settingsBox.put('music_enabled', value);
  
  double get musicVolume => _settingsBox.get('music_volume', defaultValue: 0.3);
  set musicVolume(double value) => _settingsBox.put('music_volume', value);
  
  bool get sfxEnabled => _settingsBox.get('sfx_enabled', defaultValue: true);
  set sfxEnabled(bool value) => _settingsBox.put('sfx_enabled', value);
  
  double get sfxVolume => _settingsBox.get('sfx_volume', defaultValue: 0.7);
  set sfxVolume(double value) => _settingsBox.put('sfx_volume', value);
  
  // Haptics
  bool get hapticsEnabled => _settingsBox.get('haptics_enabled', defaultValue: true);
  set hapticsEnabled(bool value) => _settingsBox.put('haptics_enabled', value);
  
  // Graphics
  bool get highQuality => _settingsBox.get('high_quality', defaultValue: true);
  set highQuality(bool value) => _settingsBox.put('high_quality', value);
  
  // AI
  bool get aiEnabled => _settingsBox.get('ai_enabled', defaultValue: true);
  set aiEnabled(bool value) => _settingsBox.put('ai_enabled', value);
  
  // Theme
  String get theme => _settingsBox.get('theme', defaultValue: 'dark');
  set theme(String value) => _settingsBox.put('theme', value);
  
  // Export all settings
  Map<String, dynamic> exportSettings() {
    return _settingsBox.toMap();
  }
  
  // Import settings
  Future<void> importSettings(Map<String, dynamic> settings) async {
    await _settingsBox.putAll(settings);
  }
}
```

---

## Flame Integration

### Save Game State from Flame

```dart
class GameWorld extends Component with HasGameRef {
  final WidgetRef ref;
  
  GameWorld({required this.ref});
  
  Future<void> saveGameState() async {
    // Collect game state from Flame components
    final cardComponents = children.whereType<CardComponent>();
    final cards = cardComponents.map((c) => c.card).toList();
    
    final gameState = GameState(
      currentWeek: _currentWeek,
      currentDay: _currentDay,
      hand: cards,
      resources: _resources,
      relationships: _relationships,
      lastSavedAt: DateTime.now(),
    );
    
    // Save to Hive
    final saveService = ref.read(gameSaveServiceProvider.notifier);
    await saveService.saveGame(gameState);
    
    // Visual feedback
    add(SaveIconComponent()
      ..position = Vector2(game.size.x - 50, 20)
      ..add(FadeEffect.fadeOut(
        EffectController(duration: 1.0),
      )));
  }
  
  Future<void> loadGameState() async {
    final saveService = ref.read(gameSaveServiceProvider.notifier);
    final state = await saveService.loadGame();
    
    if (state != null) {
      // Restore game state to Flame components
      _currentWeek = state.currentWeek;
      _currentDay = state.currentDay;
      _resources = state.resources;
      _relationships = state.relationships;
      
      // Recreate card components
      removeAll(children.whereType<CardComponent>());
      for (final card in state.hand) {
        add(CardComponent(card: card, ref: ref));
      }
      
      AppLogger.info('Game state loaded into Flame world');
    }
  }
}
```

### Auto-Save Timer Component

```dart
class AutoSaveComponent extends Component with HasGameRef {
  final WidgetRef ref;
  Timer? _autoSaveTimer;
  
  AutoSaveComponent({required this.ref});
  
  @override
  void onMount() {
    super.onMount();
    
    // Auto-save every 2 minutes
    _autoSaveTimer = Timer.periodic(
      Duration(minutes: 2),
      (_) => _performAutoSave(),
    );
  }
  
  Future<void> _performAutoSave() async {
    final gameWorld = findParent<GameWorld>();
    if (gameWorld != null) {
      await gameWorld.saveGameState();
      
      AppLogger.info('Auto-save completed');
      
      // Show subtle notification
      add(TextComponent(
        text: 'Game Saved',
        position: Vector2(game.size.x / 2, 20),
      )..add(RemoveEffect(delay: 2.0)));
    }
  }
  
  @override
  void onRemove() {
    _autoSaveTimer?.cancel();
    super.onRemove();
  }
}
```

---

## Performance Optimization

### Box Compaction

```dart
Future<void> compactDatabase() async {
  final boxes = [
    Hive.box<GameState>('game_state'),
    Hive.box<CardModel>('cards'),
    Hive.box<UserProgress>('user_progress'),
  ];
  
  for (final box in boxes) {
    await box.compact();
  }
  
  AppLogger.info('Database compacted');
}

// Schedule compaction weekly
void scheduleCompaction() {
  final settingsBox = Hive.box('settings');
  final lastCompaction = settingsBox.get('last_compaction');
  
  if (lastCompaction == null || 
      DateTime.parse(lastCompaction).isBefore(
        DateTime.now().subtract(Duration(days: 7))
      )) {
    compactDatabase();
    settingsBox.put('last_compaction', DateTime.now().toIso8601String());
  }
}
```

### Lazy Loading Pattern

```dart
class LazyCardLoader {
  late LazyBox<CardModel> _cardsBox;
  final Map<String, CardModel> _cache = {};
  
  Future<void> initialize() async {
    _cardsBox = await Hive.openLazyBox<CardModel>('all_cards');
  }
  
  Future<CardModel?> getCard(String id) async {
    // Check cache first
    if (_cache.containsKey(id)) {
      return _cache[id];
    }
    
    // Load from lazy box
    final card = await _cardsBox.get(id);
    
    // Add to cache (LRU eviction)
    if (card != null) {
      if (_cache.length >= 50) {
        _cache.remove(_cache.keys.first);
      }
      _cache[id] = card;
    }
    
    return card;
  }
}
```

---

## Encrypted Storage

### Secure User Data

```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'dart:convert';

class SecureStorageService {
  static const _secureStorage = FlutterSecureStorage();
  
  static Future<void> initializeEncryptedBox() async {
    // Get or generate encryption key
    var encryptionKeyString = await _secureStorage.read(key: 'hive_key');
    
    if (encryptionKeyString == null) {
      final encryptionKey = Hive.generateSecureKey();
      encryptionKeyString = base64UrlEncode(encryptionKey);
      await _secureStorage.write(
        key: 'hive_key',
        value: encryptionKeyString,
      );
    }
    
    final encryptionKey = base64Url.decode(encryptionKeyString);
    
    // Open encrypted box
    await Hive.openBox(
      'user_data',
      encryptionCipher: HiveAesCipher(encryptionKey),
    );
    
    AppLogger.info('Encrypted storage initialized');
  }
  
  // Store sensitive user data
  static Future<void> storeUserEmail(String email) async {
    final box = Hive.box('user_data');
    await box.put('email', email);
  }
  
  static String? getUserEmail() {
    final box = Hive.box('user_data');
    return box.get('email');
  }
}
```

---

## Data Migration

### Schema Versioning

```dart
class DatabaseMigration {
  static const int currentVersion = 2;
  
  static Future<void> migrate() async {
    final settingsBox = Hive.box('settings');
    final dbVersion = settingsBox.get('db_version', defaultValue: 1);
    
    if (dbVersion < currentVersion) {
      AppLogger.info('Migrating database', data: {
        'from': dbVersion,
        'to': currentVersion,
      });
      
      for (int version = dbVersion + 1; version <= currentVersion; version++) {
        await _migrateToVersion(version);
      }
      
      await settingsBox.put('db_version', currentVersion);
    }
  }
  
  static Future<void> _migrateToVersion(int version) async {
    switch (version) {
      case 2:
        await _migrateToV2();
        break;
      // Add more versions as needed
    }
  }
  
  static Future<void> _migrateToV2() async {
    // Example: Add new field to existing cards
    final cardsBox = Hive.box<CardModel>('cards');
    
    for (final key in cardsBox.keys) {
      final card = cardsBox.get(key);
      if (card != null) {
        // Update card with new field
        final updatedCard = card.copyWith(
          acquiredAt: DateTime.now(), // New field in v2
        );
        await cardsBox.put(key, updatedCard);
      }
    }
    
    AppLogger.info('Migrated to database v2');
  }
}
```

---

## Best Practices

1. **Close Boxes**: Close boxes on app termination
   ```dart
   @override
   void dispose() {
     Hive.close();
     super.dispose();
   }
   ```

2. **Unique Type IDs**: Use unique typeIds for each adapter (0-223)

3. **Box Names**: Use descriptive, unique names

4. **Compact Regularly**: Schedule compaction weekly

5. **Lazy Loading**: Use lazy boxes for large datasets (> 10,000 items)

6. **Limit Box Size**: Keep boxes < 10,000 items each

7. **Feature-Based Boxes**: Separate boxes per feature, not one giant box

8. **Migrations**: Handle schema changes with versioned migrations

9. **Encryption**: Use encrypted boxes for sensitive data

10. **Error Handling**: Always handle box operation errors gracefully

---

## Testing

### Unit Tests

```dart
void main() {
  setUpAll(() async {
    // Use temporary directory for tests
    final tempDir = await getTemporaryDirectory();
    Hive.init(tempDir.path);
    
    Hive.registerAdapter(CardModelAdapter());
  });
  
  tearDownAll(() async {
    await Hive.close();
    await Hive.deleteFromDisk();
  });
  
  group('GameSaveService', () {
    late Box<GameState> gameBox;
    late GameSaveService service;
    
    setUp(() async {
      gameBox = await Hive.openBox<GameState>('game_state_test');
      service = GameSaveService();
    });
    
    tearDown(() async {
      await gameBox.clear();
      await gameBox.close();
    });
    
    test('Save and load game state', () async {
      final state = GameState(
        currentWeek: 5,
        currentDay: 3,
        hand: [],
      );
      
      await service.saveGame(state);
      final loaded = await service.loadGame();
      
      expect(loaded, isNotNull);
      expect(loaded!.currentWeek, 5);
      expect(loaded.currentDay, 3);
    });
    
    test('Auto-save creates separate slot', () async {
      final state = GameState(currentWeek: 1, currentDay: 1, hand: []);
      
      await service.saveGame(state);
      await service.autoSave(state.copyWith(currentWeek: 2));
      
      final saves = service.listSaves();
      expect(saves.length, 2);
    });
  });
}
```

---

## Troubleshooting

### Box Already Open

**Solution:**
```dart
Box<T> getBox<T>(String name) {
  if (Hive.isBoxOpen(name)) {
    return Hive.box<T>(name);
  } else {
    return await Hive.openBox<T>(name);
  }
}
```

### Type Adapter Not Registered

**Solution:**
```dart
// Ensure adapter is registered before opening box
if (!Hive.isAdapterRegistered(0)) {
  Hive.registerAdapter(CardModelAdapter());
}
```

### Corrupted Box

**Solution:**
```dart
Future<void> recoverBox<T>(String name) async {
  try {
    await Hive.openBox<T>(name);
  } catch (e) {
    // Delete corrupted box
    await Hive.deleteBoxFromDisk(name);
    // Recreate box
    await Hive.openBox<T>(name);
  }
}
```

---

## Resources

### Official Documentation
- **Hive Docs**: https://docs.hivedb.dev/
- **GitHub**: https://github.com/isar/hive
- **Examples**: https://github.com/isar/hive/tree/master/hive/example

### Alternatives
- **Isar**: By same author, more features but larger
- **SharedPreferences**: Simpler but slower
- **SQLite (sqflite)**: Relational database, more complex

---

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Package Version:** hive ^2.2.3  
**Master Spec Reference:** `docs/master_flutter_flame_spec_v_1_0.md`


