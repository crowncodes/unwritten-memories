# Local Cache Implementation

**Purpose:** Complete implementation guide for Hive + memory caching system  
**Audience:** Mobile developers, Flutter engineers  
**Status:** ✅ Complete  
**Related:** ← 50-ai-output-storage-system.md | 51-storage-metadata-schemas.md | → 53-cloud-storage-integration.md

---

## What This Document Covers

**Complete implementation of local caching:**
- Memory cache (Tier 1) - Instant access
- Hive disk cache (Tier 2) - Persistent local storage
- TTL (Time-To-Live) strategies
- Eviction policies (LRU, size limits)
- Cache warming and pre-fetching
- Performance optimization
- Testing strategies

**Why This Matters:**
- 80%+ cache hit rate = 80% cost savings
- Instant response time (< 5ms)
- Offline-first gameplay
- Better user experience

---

## Table of Contents

1. [Memory Cache Implementation](#memory-cache-implementation)
2. [Hive Disk Cache Implementation](#hive-disk-cache-implementation)
3. [TTL Strategies](#ttl-strategies)
4. [Eviction Policies](#eviction-policies)
5. [Cache Warming](#cache-warming)
6. [Performance Optimization](#performance-optimization)
7. [Testing](#testing)
8. [Complete Example](#complete-example)

---

## Memory Cache Implementation

### Tier 1: In-Memory LRU Cache

```dart
// lib/core/cache/memory_cache.dart
import 'dart:collection';

/// In-memory cache with LRU eviction policy
/// 
/// Provides instant access (< 1ms) to recently used items.
/// Automatically evicts least recently used items when capacity reached.
class MemoryCache<T> {
  final int _maxSize;
  final Map<String, _CacheEntry<T>> _cache = {};
  final LinkedHashMap<String, DateTime> _accessOrder = LinkedHashMap();
  
  int _hits = 0;
  int _misses = 0;
  
  MemoryCache({int maxSize = 50}) : _maxSize = maxSize;
  
  /// Get item from cache
  /// 
  /// Returns null if not found. Updates access order (LRU).
  T? get(String key) {
    final entry = _cache[key];
    
    if (entry == null) {
      _misses++;
      return null;
    }
    
    // Check if expired
    if (entry.isExpired) {
      _cache.remove(key);
      _accessOrder.remove(key);
      _misses++;
      return null;
    }
    
    // Update access order (remove and re-add = move to end)
    _accessOrder.remove(key);
    _accessOrder[key] = DateTime.now();
    
    _hits++;
    return entry.value;
  }
  
  /// Put item into cache
  /// 
  /// If cache is full, evicts least recently used item.
  void put(String key, T value, {Duration? ttl}) {
    // Remove least recently used if at capacity
    if (_cache.length >= _maxSize && !_cache.containsKey(key)) {
      final lruKey = _accessOrder.keys.first;
      _cache.remove(lruKey);
      _accessOrder.remove(lruKey);
    }
    
    // Add new entry
    _cache[key] = _CacheEntry(
      value: value,
      cachedAt: DateTime.now(),
      expiresAt: ttl != null ? DateTime.now().add(ttl) : null,
    );
    
    // Update access order
    _accessOrder[key] = DateTime.now();
  }
  
  /// Remove item from cache
  void remove(String key) {
    _cache.remove(key);
    _accessOrder.remove(key);
  }
  
  /// Clear entire cache
  void clear() {
    _cache.clear();
    _accessOrder.clear();
    _hits = 0;
    _misses = 0;
  }
  
  /// Get cache statistics
  CacheStats get stats => CacheStats(
    size: _cache.length,
    maxSize: _maxSize,
    hits: _hits,
    misses: _misses,
    hitRate: _hits + _misses > 0 ? _hits / (_hits + _misses) : 0.0,
  );
  
  /// Remove expired entries
  void cleanup() {
    final now = DateTime.now();
    final expiredKeys = _cache.entries
        .where((e) => e.value.expiresAt != null && now.isAfter(e.value.expiresAt!))
        .map((e) => e.key)
        .toList();
    
    for (final key in expiredKeys) {
      _cache.remove(key);
      _accessOrder.remove(key);
    }
  }
}

class _CacheEntry<T> {
  final T value;
  final DateTime cachedAt;
  final DateTime? expiresAt;
  
  _CacheEntry({
    required this.value,
    required this.cachedAt,
    this.expiresAt,
  });
  
  bool get isExpired =>
      expiresAt != null && DateTime.now().isAfter(expiresAt!);
}

class CacheStats {
  final int size;
  final int maxSize;
  final int hits;
  final int misses;
  final double hitRate;
  
  CacheStats({
    required this.size,
    required this.maxSize,
    required this.hits,
    required this.misses,
    required this.hitRate,
  });
  
  @override
  String toString() {
    return 'CacheStats(size: $size/$maxSize, hits: $hits, misses: $misses, hitRate: ${(hitRate * 100).toStringAsFixed(1)}%)';
  }
}
```

### Usage Example

```dart
// Create memory cache for dialogues
final dialogueCache = MemoryCache<String>(maxSize: 50);

// Store dialogue with 1 hour TTL
dialogueCache.put(
  'card_123_greeting',
  'Hello! How are you today?',
  ttl: Duration(hours: 1),
);

// Retrieve dialogue
final dialogue = dialogueCache.get('card_123_greeting');
if (dialogue != null) {
  // Cache hit!
  showDialogue(dialogue);
}

// Check cache statistics
print(dialogueCache.stats);
// Output: CacheStats(size: 15/50, hits: 42, misses: 8, hitRate: 84.0%)
```

---

## Hive Disk Cache Implementation

### Tier 2: Persistent Disk Cache

```dart
// lib/core/cache/hive_cache.dart
import 'package:hive/hive.dart';
import 'package:hive_flutter/hive_flutter.dart';

part 'hive_cache.g.dart';  // Generated by hive_generator

/// Hive model for cached AI outputs
@HiveType(typeId: 1)
class CachedAIOutput extends HiveObject {
  @HiveField(0)
  final String id;
  
  @HiveField(1)
  final String contentType;  // "dialogue" | "image" | "video" | "audio"
  
  @HiveField(2)
  final String content;  // Text content or storage path
  
  @HiveField(3)
  final DateTime cachedAt;
  
  @HiveField(4)
  final DateTime expiresAt;  // TTL
  
  @HiveField(5)
  final Map<String, dynamic> metadata;
  
  @HiveField(6)
  int accessCount;  // For LRU eviction
  
  @HiveField(7)
  DateTime lastAccessedAt;
  
  CachedAIOutput({
    required this.id,
    required this.contentType,
    required this.content,
    required this.cachedAt,
    required this.expiresAt,
    required this.metadata,
    this.accessCount = 0,
    DateTime? lastAccessedAt,
  }) : lastAccessedAt = lastAccessedAt ?? DateTime.now();
  
  bool get isExpired => DateTime.now().isAfter(expiresAt);
}

/// Hive-based persistent cache
class HiveCache {
  late Box<CachedAIOutput> _box;
  final int _maxEntries;
  final String _boxName;
  
  HiveCache({
    int maxEntries = 500,
    String boxName = 'ai_outputs',
  })  : _maxEntries = maxEntries,
        _boxName = boxName;
  
  /// Initialize Hive cache
  Future<void> initialize() async {
    await Hive.initFlutter();
    
    // Register adapter
    if (!Hive.isAdapterRegistered(1)) {
      Hive.registerAdapter(CachedAIOutputAdapter());
    }
    
    // Open box
    _box = await Hive.openBox<CachedAIOutput>(_boxName);
    
    // Clean expired entries on startup
    await cleanExpired();
    
    AppLogger.info('Hive cache initialized: ${_box.length} entries');
  }
  
  /// Get item from cache
  Future<CachedAIOutput?> get(String key) async {
    final entry = _box.get(key);
    
    if (entry == null) {
      return null;
    }
    
    // Check if expired
    if (entry.isExpired) {
      await _box.delete(key);
      return null;
    }
    
    // Update access statistics
    entry.accessCount++;
    entry.lastAccessedAt = DateTime.now();
    await entry.save();  // Persist changes
    
    return entry;
  }
  
  /// Put item into cache
  Future<void> put(String key, CachedAIOutput value) async {
    // Check capacity
    if (_box.length >= _maxEntries && !_box.containsKey(key)) {
      await _evictOldest();
    }
    
    await _box.put(key, value);
  }
  
  /// Remove item from cache
  Future<void> remove(String key) async {
    await _box.delete(key);
  }
  
  /// Clear entire cache
  Future<void> clear() async {
    await _box.clear();
    AppLogger.info('Hive cache cleared');
  }
  
  /// Clean expired entries
  Future<int> cleanExpired() async {
    final expiredKeys = _box.values
        .where((entry) => entry.isExpired)
        .map((entry) => entry.id)
        .toList();
    
    await _box.deleteAll(expiredKeys);
    
    AppLogger.info('Cleaned ${expiredKeys.length} expired cache entries');
    return expiredKeys.length;
  }
  
  /// Evict oldest entries to make room
  Future<void> _evictOldest() async {
    // Sort by last accessed (oldest first)
    final entries = _box.values.toList()
      ..sort((a, b) => a.lastAccessedAt.compareTo(b.lastAccessedAt));
    
    // Evict oldest 10%
    final evictCount = (_maxEntries * 0.1).ceil();
    final toEvict = entries.take(evictCount).map((e) => e.id).toList();
    
    await _box.deleteAll(toEvict);
    
    AppLogger.info('Evicted $evictCount oldest cache entries');
  }
  
  /// Get cache statistics
  CacheStats get stats {
    final entries = _box.values.toList();
    final now = DateTime.now();
    
    return CacheStats(
      totalEntries: entries.length,
      expiredEntries: entries.where((e) => e.isExpired).length,
      totalSize: _estimateSize(entries),
      avgAccessCount: entries.isEmpty
          ? 0.0
          : entries.fold<int>(0, (sum, e) => sum + e.accessCount) / entries.length,
    );
  }
  
  int _estimateSize(List<CachedAIOutput> entries) {
    // Rough estimate of cache size in bytes
    return entries.fold<int>(
      0,
      (sum, entry) => sum + entry.content.length + 200, // 200 bytes overhead
    );
  }
  
  /// Compact database (reclaim space)
  Future<void> compact() async {
    await _box.compact();
    AppLogger.info('Hive cache compacted');
  }
}

class CacheStats {
  final int totalEntries;
  final int expiredEntries;
  final int totalSize;  // bytes
  final double avgAccessCount;
  
  CacheStats({
    required this.totalEntries,
    required this.expiredEntries,
    required this.totalSize,
    required this.avgAccessCount,
  });
  
  @override
  String toString() {
    return 'CacheStats(entries: $totalEntries, expired: $expiredEntries, size: ${(totalSize / 1024).toStringAsFixed(1)}KB, avgAccess: ${avgAccessCount.toStringAsFixed(1)})';
  }
}
```

### Usage Example

```dart
// Initialize Hive cache
final hiveCache = HiveCache(maxEntries: 500);
await hiveCache.initialize();

// Store dialogue
await hiveCache.put(
  'card_123_greeting',
  CachedAIOutput(
    id: 'card_123_greeting',
    contentType: 'dialogue',
    content: 'Hello! How are you today?',
    cachedAt: DateTime.now(),
    expiresAt: DateTime.now().add(Duration(days: 7)),
    metadata: {
      'card_id': 'card_123',
      'interaction_type': 'greeting',
    },
  ),
);

// Retrieve dialogue
final cached = await hiveCache.get('card_123_greeting');
if (cached != null) {
  showDialogue(cached.content);
}

// Clean expired entries (run periodically)
await hiveCache.cleanExpired();

// Check statistics
print(hiveCache.stats);
// Output: CacheStats(entries: 234, expired: 12, size: 45.3KB, avgAccess: 3.2)
```

---

## TTL Strategies

### Content-Type-Based TTL

```dart
// lib/core/cache/cache_ttl.dart
class CacheTTL {
  /// TTL durations by content type
  
  // Text content
  static const Duration dialogue = Duration(days: 7);
  static const Duration cardDescription = Duration(days: 30);
  static const Duration storyNarrative = Duration(days: 14);
  
  // Images
  static const Duration cardImage = Duration(days: 30);
  static const Duration temporaryImage = Duration(days: 7);
  
  // Video
  static const Duration evolutionVideo = Duration(days: 14);
  static const Duration cutsceneVideo = Duration(days: 14);
  
  // Audio
  static const Duration musicStem = Duration(days: 30);
  static const Duration ambientAudio = Duration(days: 14);
  
  /// Get TTL for content type
  static Duration getTTL(String contentType, {String? subType}) {
    switch (contentType) {
      case 'dialogue':
        return dialogue;
      case 'card_description':
        return cardDescription;
      case 'story':
        return storyNarrative;
      case 'image':
        return subType == 'temporary' ? temporaryImage : cardImage;
      case 'video':
        return evolutionVideo;
      case 'audio':
        return musicStem;
      default:
        return Duration(days: 7); // Default
    }
  }
}
```

### Dynamic TTL Based on Usage

```dart
/// Extend TTL for frequently accessed items
class AdaptiveTTL {
  static Duration calculateTTL(
    String contentType,
    int accessCount,
  ) {
    final baseTTL = CacheTTL.getTTL(contentType);
    
    // Extend TTL based on access frequency
    if (accessCount > 10) {
      return baseTTL * 2;  // Double TTL for popular items
    } else if (accessCount > 5) {
      return baseTTL * 1.5;  // 50% longer for moderately used
    }
    
    return baseTTL;
  }
}
```

---

## Eviction Policies

### Multi-Factor Eviction

```dart
/// Eviction policy considering multiple factors
class EvictionPolicy {
  /// Calculate eviction priority (higher = more likely to evict)
  static double calculateEvictionPriority(CachedAIOutput entry) {
    final now = DateTime.now();
    
    // Factor 1: Time since last access (0-1, higher = older)
    final hoursSinceAccess = now.difference(entry.lastAccessedAt).inHours;
    final accessFactor = (hoursSinceAccess / 168).clamp(0.0, 1.0);  // 168 hours = 1 week
    
    // Factor 2: Access frequency (0-1, higher = less accessed)
    final frequencyFactor = (1.0 / (entry.accessCount + 1)).clamp(0.0, 1.0);
    
    // Factor 3: Time to expiration (0-1, higher = closer to expiry)
    final hoursToExpiry = entry.expiresAt.difference(now).inHours;
    final expiryFactor = (1.0 - (hoursToExpiry / 168)).clamp(0.0, 1.0);
    
    // Weighted combination
    return (accessFactor * 0.4) + (frequencyFactor * 0.4) + (expiryFactor * 0.2);
  }
  
  /// Select entries to evict
  static List<String> selectForEviction(
    List<CachedAIOutput> entries,
    int evictCount,
  ) {
    // Calculate priority for each entry
    final prioritized = entries.map((entry) => MapEntry(
      entry.id,
      calculateEvictionPriority(entry),
    )).toList();
    
    // Sort by priority (highest first)
    prioritized.sort((a, b) => b.value.compareTo(a.value));
    
    // Return top eviction candidates
    return prioritized.take(evictCount).map((e) => e.key).toList();
  }
}
```

---

## Cache Warming

### Pre-Load Likely Content

```dart
// lib/core/cache/cache_warmer.dart
class CacheWarmer {
  final AIRepository _repository;
  final HiveCache _cache;
  
  CacheWarmer({
    required AIRepository repository,
    required HiveCache cache,
  })  : _repository = repository,
        _cache = cache;
  
  /// Warm cache with likely next interactions
  Future<void> warmCache({
    required String currentCardId,
    required List<String> likelyNextCards,
  }) async {
    // Pre-load greeting dialogues for likely next cards
    for (final cardId in likelyNextCards) {
      try {
        // Check if already cached
        final key = '${cardId}_greeting';
        final cached = await _cache.get(key);
        if (cached != null) continue;  // Already cached
        
        // Pre-fetch (non-blocking)
        unawaited(
          _repository.getDialogue(
            cardId: cardId,
            interactionId: 'greeting',
          ).then((dialogue) {
            AppLogger.info('Cache warmed: $key');
          }).catchError((e) {
            // Silent failure OK for cache warming
            AppLogger.info('Cache warm failed for $key');
          }),
        );
      } catch (e) {
        // Continue warming other cards
      }
    }
  }
  
  /// Warm cache during idle time
  Future<void> warmDuringIdle(List<String> cardIds) async {
    // Wait for idle period
    await Future.delayed(Duration(seconds: 2));
    
    for (final cardId in cardIds) {
      unawaited(
        _repository.getDialogue(
          cardId: cardId,
          interactionId: 'greeting',
        ),
      );
      
      // Small delay between requests
      await Future.delayed(Duration(milliseconds: 100));
    }
  }
}
```

---

## Performance Optimization

### Batch Operations

```dart
/// Batch cache operations for efficiency
class BatchCacheOperations {
  final HiveCache _cache;
  
  /// Put multiple items efficiently
  Future<void> putBatch(Map<String, CachedAIOutput> items) async {
    // Hive supports batch writes
    await _cache._box.putAll(items);
    AppLogger.info('Batch cached ${items.length} items');
  }
  
  /// Get multiple items efficiently
  Future<Map<String, CachedAIOutput?>> getBatch(List<String> keys) async {
    final results = <String, CachedAIOutput?>{};
    
    for (final key in keys) {
      results[key] = await _cache.get(key);
    }
    
    return results;
  }
}
```

### Background Maintenance

```dart
/// Background cache maintenance
class CacheMaintenanceService {
  final HiveCache _cache;
  Timer? _maintenanceTimer;
  
  /// Start periodic maintenance
  void startMaintenance() {
    // Run every hour
    _maintenanceTimer = Timer.periodic(Duration(hours: 1), (_) async {
      await _performMaintenance();
    });
  }
  
  Future<void> _performMaintenance() async {
    AppLogger.info('Starting cache maintenance');
    
    // Clean expired entries
    final expiredCount = await _cache.cleanExpired();
    
    // Compact if needed (weekly)
    final now = DateTime.now();
    if (now.weekday == DateTime.sunday && now.hour == 3) {
      await _cache.compact();
    }
    
    AppLogger.info('Cache maintenance complete: $expiredCount expired entries removed');
  }
  
  void stopMaintenance() {
    _maintenanceTimer?.cancel();
  }
}
```

---

## Testing

### Unit Tests

```dart
// test/core/cache/memory_cache_test.dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('MemoryCache', () {
    late MemoryCache<String> cache;
    
    setUp(() {
      cache = MemoryCache<String>(maxSize: 3);
    });
    
    test('stores and retrieves items', () {
      cache.put('key1', 'value1');
      expect(cache.get('key1'), 'value1');
    });
    
    test('evicts LRU when capacity reached', () {
      cache.put('key1', 'value1');
      cache.put('key2', 'value2');
      cache.put('key3', 'value3');
      
      // Access key1 to make it recently used
      cache.get('key1');
      
      // Add key4 - should evict key2 (least recently used)
      cache.put('key4', 'value4');
      
      expect(cache.get('key1'), 'value1');  // Still there
      expect(cache.get('key2'), null);      // Evicted
      expect(cache.get('key3'), 'value3');  // Still there
      expect(cache.get('key4'), 'value4');  // Newly added
    });
    
    test('respects TTL', () async {
      cache.put('key1', 'value1', ttl: Duration(milliseconds: 100));
      
      expect(cache.get('key1'), 'value1');
      
      await Future.delayed(Duration(milliseconds: 150));
      
      expect(cache.get('key1'), null);  // Expired
    });
    
    test('tracks hit rate', () {
      cache.put('key1', 'value1');
      
      cache.get('key1');  // Hit
      cache.get('key1');  // Hit
      cache.get('key2');  // Miss
      
      final stats = cache.stats;
      expect(stats.hits, 2);
      expect(stats.misses, 1);
      expect(stats.hitRate, closeTo(0.67, 0.01));
    });
  });
}
```

---

## Complete Example

### Integrated Cache System

```dart
// lib/core/cache/integrated_cache.dart
class IntegratedCache {
  final MemoryCache<String> _memoryCache;
  final HiveCache _hiveCache;
  
  IntegratedCache({
    required MemoryCache<String> memoryCache,
    required HiveCache hiveCache,
  })  : _memoryCache = memoryCache,
        _hiveCache = hiveCache;
  
  /// Get with cascade: Memory → Disk
  Future<String?> get(String key) async {
    // Try memory first (< 1ms)
    final memoryHit = _memoryCache.get(key);
    if (memoryHit != null) {
      return memoryHit;
    }
    
    // Try disk (1-5ms)
    final diskHit = await _hiveCache.get(key);
    if (diskHit != null) {
      // Promote to memory
      _memoryCache.put(key, diskHit.content);
      return diskHit.content;
    }
    
    return null;
  }
  
  /// Put in both caches
  Future<void> put(
    String key,
    String value, {
    required String contentType,
  }) async {
    final ttl = CacheTTL.getTTL(contentType);
    
    // Memory cache
    _memoryCache.put(key, value, ttl: ttl);
    
    // Disk cache
    await _hiveCache.put(
      key,
      CachedAIOutput(
        id: key,
        contentType: contentType,
        content: value,
        cachedAt: DateTime.now(),
        expiresAt: DateTime.now().add(ttl),
        metadata: {},
      ),
    );
  }
}
```

---

## Related Documentation

- **50-ai-output-storage-system.md** - Overall storage architecture
- **51-storage-metadata-schemas.md** - Data schemas
- **53-cloud-storage-integration.md** - Firebase integration
- **71-cost-performance-targets.md** - Performance targets

---

**Status:** ✅ Complete Implementation Guide  
**Target:** 80%+ cache hit rate, < 5ms access time  
**Key Metric:** Cost savings through aggressive caching


