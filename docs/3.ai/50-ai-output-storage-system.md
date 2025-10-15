# AI Output Storage System

**Purpose:** Complete architecture for storing and retrieving all AI-generated content  
**Audience:** Backend engineers, mobile developers, system architects  
**Status:** ✅ Complete Architecture  
**Related:** ← 40-hybrid-cloud-local-system.md | → 51-storage-metadata-schemas.md | 52-local-cache-implementation.md | 53-cloud-storage-integration.md

---

## What This Document Covers

This document provides the **complete storage architecture** for all AI-generated content in Unwritten. You'll learn:
- Storage strategy for all content types (text, images, video, audio/music stems)
- Firebase Cloud architecture (Firestore + Cloud Storage)
- Local caching system (memory + Hive)
- Efficient retrieval patterns
- Sync strategies
- Offline-first design
- Cost optimization through caching

**Why This Matters:**
- AI generations are expensive - cache aggressively
- Users expect instant responses - local cache critical
- Offline gameplay requires cached content
- Proper storage enables analytics and improvement

---

## Table of Contents

1. [Storage Architecture Overview](#storage-architecture-overview)
2. [Content Types](#content-types)
3. [Firebase Cloud Storage](#firebase-cloud-storage)
4. [Local Cache Strategy](#local-cache-strategy)
5. [Retrieval Patterns](#retrieval-patterns)
6. [Sync Strategies](#sync-strategies)
7. [Offline-First Design](#offline-first-design)
8. [Cost Optimization](#cost-optimization)
9. [Implementation Examples](#implementation-examples)
10. [Monitoring & Analytics](#monitoring--analytics)

---

## Storage Architecture Overview

### Three-Tier Storage System

```
┌─────────────────────────────────────────────────┐
│          TIER 1: Memory Cache                   │
│  • Instant access (< 1ms)                       │
│  • Most recently used (MRU) items               │
│  • 10-20MB capacity                             │
│  • Cleared on app restart                       │
└─────────────────────────────────────────────────┘
              ↓ Cache miss
┌─────────────────────────────────────────────────┐
│          TIER 2: Local Disk Cache (Hive)       │
│  • Fast access (1-5ms)                          │
│  • Persistent across restarts                   │
│  • 50-100MB capacity                            │
│  • TTL-based eviction                           │
└─────────────────────────────────────────────────┘
              ↓ Cache miss
┌─────────────────────────────────────────────────┐
│          TIER 3: Firebase Cloud                 │
│  • Network access (100-500ms)                   │
│  • Unlimited capacity                           │
│  • Persistent forever                           │
│  • Synced across devices                        │
│  • Firestore (metadata) + Storage (assets)      │
└─────────────────────────────────────────────────┘
              ↓ Cloud miss
┌─────────────────────────────────────────────────┐
│          Generate New (AI)                      │
│  • 2-10 seconds latency                         │
│  • $0.01-0.10 cost                              │
│  • Cache result in all tiers                    │
└─────────────────────────────────────────────────┘
```

### Key Principles

1. **Offline-First** - App works without network
2. **Cache Aggressively** - AI is expensive, storage is cheap
3. **Cascade Retrieval** - Memory → Disk → Cloud → Generate
4. **Smart Eviction** - TTL + LRU based on content type
5. **Background Sync** - Upload to cloud asynchronously
6. **Pre-Fetch** - Predictive loading for likely interactions

---

## Content Types

### 1. Text Content (Dialogues, Descriptions)

**Characteristics:**
- Small size (100-500 bytes typical)
- High frequency (multiple per session)
- Fast generation (2-5 seconds)
- Low cost ($0.00008 per generation)

**Storage Strategy:**
- Memory cache: Last 50 dialogues
- Disk cache: Last 500 dialogues (TTL: 7 days)
- Cloud: All dialogues (forever)

**Typical Volume:**
- Per player per day: 20-50 dialogues
- Per player per month: 600-1500 dialogues
- Storage per player: ~50KB text/month

### 2. Images (Card Art, Portraits)

**Characteristics:**
- Medium size (50-200KB per image, WebP compressed)
- Low frequency (occasional, mostly pre-generated)
- Slow generation (10-20 seconds)
- Higher cost ($0.04 per image)

**Storage Strategy:**
- Memory cache: Currently visible images only (5-10 images)
- Disk cache: Frequently used cards (50 images, TTL: 30 days)
- Cloud: All images (forever)

**Typical Volume:**
- Per player per month: 2-5 new images
- Storage per player: 200KB-1MB images/month

### 3. Video (Evolution Animations, Story Cutscenes)

**Characteristics:**
- Large size (500KB-2MB per video, compressed)
- Very low frequency (rare, special moments)
- Very slow generation (30-60 seconds)
- High cost ($0.10-0.50 per video, estimated)

**Storage Strategy:**
- Memory cache: Currently playing video only
- Disk cache: Recent videos (10 videos, TTL: 14 days)
- Cloud: All videos (forever)

**Typical Volume:**
- Per player per month: 1-3 videos
- Storage per player: 1-3MB videos/month

### 4. Audio / Music Stems

**Characteristics:**
- Medium size (100-300KB per stem, Opus compressed)
- Low frequency (background music, occasional)
- Slow generation (30-60 seconds)
- Medium cost ($0.10 per stem, estimated)

**Storage Strategy:**
- Memory cache: Currently playing stems (2-3 active)
- Disk cache: Frequently used stems (20 stems, TTL: 30 days)
- Cloud: All stems (forever)

**Typical Volume:**
- Per player per month: 3-5 new stems
- Storage per player: 500KB-1.5MB audio/month

---

## Firebase Cloud Storage

### Firestore Structure (Metadata)

```javascript
// Firestore Database Structure

// Collection: ai_outputs
ai_outputs/
  {user_id}/
    // Sub-collection: dialogues
    dialogues/
      {card_id}_{interaction_id}/
        - card_id: string
        - interaction_id: string
        - text: string (the dialogue content)
        - generated_at: timestamp
        - model: string ("gemini-2.5-flash" | "gemini-2.5-pro")
        - cost_usd: number (0.00008)
        - latency_ms: number (2500)
        - personality_traits: map
            - openness: number (0.75)
            - conscientiousness: number (0.60)
            - extraversion: number (0.80)
            - agreeableness: number (0.70)
            - neuroticism: number (0.45)
        - context_length: number (tokens)
        - output_length: number (tokens)
        - cached: boolean (false initially)
        - cache_hit_count: number (0)
        - quality_score: number (0.85, optional)
        - user_feedback: string ("liked" | "disliked" | null)
    
    // Sub-collection: images
    images/
      {card_id}_{type}/
        - card_id: string
        - type: string ("portrait" | "action" | "evolution")
        - storage_path: string ("users/{user_id}/ai_generated/images/card_123_portrait.webp")
        - generated_at: timestamp
        - model: string ("imagen-3")
        - cost_usd: number (0.04)
        - latency_ms: number (15000)
        - dimensions: map
            - width: number (1024)
            - height: number (1024)
        - format: string ("webp")
        - size_bytes: number (87352)
        - prompt: string (truncated)
        - cached: boolean
        - download_count: number
    
    // Sub-collection: videos
    videos/
      {scene_id}/
        - scene_id: string
        - type: string ("evolution" | "cutscene" | "story")
        - storage_path: string
        - generated_at: timestamp
        - model: string ("veo" | "custom")
        - cost_usd: number
        - latency_ms: number
        - duration_sec: number (5.2)
        - dimensions: map
        - format: string ("mp4")
        - size_bytes: number
        - prompt: string (truncated)
        - cached: boolean
        - play_count: number
    
    // Sub-collection: audio
    audio/
      music_stems/
        {stem_id}/
          - stem_id: string
          - stem_type: string ("bass" | "drums" | "melody" | "harmony" | "ambient")
          - storage_path: string
          - generated_at: timestamp
          - model: string ("lyria")
          - cost_usd: number (0.10)
          - latency_ms: number (45000)
          - duration_sec: number (30.0)
          - format: string ("opus")
          - size_bytes: number (245600)
          - prompt: string (truncated)
          - mood: string ("calm" | "tense" | "joyful")
          - tempo: number (120)
          - cached: boolean
          - play_count: number
```

### Cloud Storage Structure (Assets)

```
// Firebase Cloud Storage Structure

users/
  {user_id}/
    ai_generated/
      images/
        card_123_portrait.webp         (87KB)
        card_123_action.webp           (92KB)
        card_456_evolution.webp        (105KB)
      
      videos/
        evolution_3_to_4.mp4           (1.2MB)
        story_cutscene_001.mp4         (1.8MB)
      
      audio/
        stems/
          bass_stem_001.opus           (120KB)
          drums_stem_001.opus          (95KB)
          melody_stem_001.opus         (180KB)
          harmony_stem_001.opus        (150KB)
          ambient_stem_001.opus        (200KB)
```

### Security Rules

```javascript
// Firestore Security Rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // AI outputs - users can only access their own
    match /ai_outputs/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}

// Cloud Storage Security Rules
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // AI generated content - users can only access their own
    match /users/{userId}/{allPaths=**} {
      allow read: if request.auth != null && request.auth.uid == userId;
      allow write: if request.auth != null && request.auth.uid == userId
                   && request.resource.size < 5 * 1024 * 1024; // 5MB limit
    }
  }
}
```

**See:** `53-cloud-storage-integration.md` for complete Firebase setup

---

## Local Cache Strategy

### Memory Cache (Tier 1)

**Implementation:** Dart Map (in-memory)

```dart
// lib/core/cache/memory_cache.dart
class MemoryCache<T> {
  final int _maxSize;
  final Map<String, _CacheEntry<T>> _cache = {};
  final List<String> _accessOrder = []; // LRU tracking
  
  MemoryCache({int maxSize = 50}) : _maxSize = maxSize;
  
  T? get(String key) {
    final entry = _cache[key];
    if (entry == null) return null;
    
    // Update access order (move to end = most recent)
    _accessOrder.remove(key);
    _accessOrder.add(key);
    
    return entry.value;
  }
  
  void put(String key, T value) {
    // Remove least recently used if at capacity
    if (_cache.length >= _maxSize) {
      final lruKey = _accessOrder.removeAt(0);
      _cache.remove(lruKey);
    }
    
    _cache[key] = _CacheEntry(value, DateTime.now());
    _accessOrder.add(key);
  }
  
  void clear() {
    _cache.clear();
    _accessOrder.clear();
  }
}

class _CacheEntry<T> {
  final T value;
  final DateTime cachedAt;
  
  _CacheEntry(this.value, this.cachedAt);
}
```

### Disk Cache (Tier 2)

**Implementation:** Hive (NoSQL local database)

```dart
// lib/core/cache/hive_cache.dart
import 'package:hive/hive.dart';

@HiveType(typeId: 1)
class CachedAIOutput extends HiveObject {
  @HiveField(0)
  final String id;
  
  @HiveField(1)
  final String contentType; // "dialogue" | "image" | "video" | "audio"
  
  @HiveField(2)
  final String content; // Text content or storage path
  
  @HiveField(3)
  final DateTime cachedAt;
  
  @HiveField(4)
  final DateTime expiresAt; // TTL
  
  @HiveField(5)
  final Map<String, dynamic> metadata;
  
  CachedAIOutput({
    required this.id,
    required this.contentType,
    required this.content,
    required this.cachedAt,
    required this.expiresAt,
    required this.metadata,
  });
  
  bool get isExpired => DateTime.now().isAfter(expiresAt);
}

class HiveCache {
  late Box<CachedAIOutput> _box;
  
  Future<void> initialize() async {
    await Hive.initFlutter();
    Hive.registerAdapter(CachedAIOutputAdapter());
    _box = await Hive.openBox<CachedAIOutput>('ai_outputs');
    
    // Clean expired entries on startup
    await _cleanExpired();
  }
  
  Future<CachedAIOutput?> get(String key) async {
    final entry = _box.get(key);
    if (entry == null) return null;
    
    if (entry.isExpired) {
      await _box.delete(key);
      return null;
    }
    
    return entry;
  }
  
  Future<void> put(String key, CachedAIOutput value) async {
    await _box.put(key, value);
    
    // Check capacity (max 500 entries)
    if (_box.length > 500) {
      await _evictOldest();
    }
  }
  
  Future<void> _cleanExpired() async {
    final expiredKeys = _box.values
        .where((entry) => entry.isExpired)
        .map((entry) => entry.id)
        .toList();
    
    await _box.deleteAll(expiredKeys);
    
    AppLogger.info('Cleaned ${expiredKeys.length} expired cache entries');
  }
  
  Future<void> _evictOldest() async {
    // Evict oldest 50 entries
    final entries = _box.values.toList()
      ..sort((a, b) => a.cachedAt.compareTo(b.cachedAt));
    
    final toEvict = entries.take(50).map((e) => e.id).toList();
    await _box.deleteAll(toEvict);
  }
}
```

**See:** `52-local-cache-implementation.md` for complete implementation

### TTL Configuration by Content Type

```dart
class CacheTTL {
  // Text content
  static const Duration dialogue = Duration(days: 7);
  static const Duration cardDescription = Duration(days: 30);
  
  // Images
  static const Duration cardImage = Duration(days: 30);
  static const Duration temporaryImage = Duration(days: 7);
  
  // Video
  static const Duration video = Duration(days: 14);
  
  // Audio
  static const Duration musicStem = Duration(days: 30);
  static const Duration ambientAudio = Duration(days: 14);
}
```

---

## Retrieval Patterns

### Cascade Retrieval Pattern

**The standard pattern for fetching any AI content:**

```dart
// lib/core/services/ai_output_repository.dart
class AIOutputRepository {
  final MemoryCache<String> _memoryCache;
  final HiveCache _diskCache;
  final FirestoreService _firestore;
  final CloudStorageService _storage;
  final AIService _aiService;
  
  /// Cascade retrieval: Memory → Disk → Cloud → Generate
  Future<String> getDialogue({
    required String cardId,
    required String interactionId,
    required Map<String, double> context,
  }) async {
    final key = '${cardId}_$interactionId';
    
    // TIER 1: Memory cache (< 1ms)
    final memoryResult = _memoryCache.get(key);
    if (memoryResult != null) {
      AppLogger.performance('Cache hit: memory', Duration(microseconds: 100));
      return memoryResult;
    }
    
    // TIER 2: Disk cache (1-5ms)
    final diskResult = await _diskCache.get(key);
    if (diskResult != null && !diskResult.isExpired) {
      // Promote to memory cache
      _memoryCache.put(key, diskResult.content);
      AppLogger.performance('Cache hit: disk', Duration(milliseconds: 2));
      return diskResult.content;
    }
    
    // TIER 3: Cloud (Firestore + Storage) (100-500ms)
    try {
      final cloudResult = await _firestore.getDialogue(cardId, interactionId);
      if (cloudResult != null) {
        // Promote to disk and memory
        await _cacheDialogue(key, cloudResult.text);
        AppLogger.performance('Cache hit: cloud', Duration(milliseconds: 250));
        return cloudResult.text;
      }
    } catch (e) {
      AppLogger.error('Cloud fetch failed', e);
    }
    
    // TIER 4: Generate new (2-10 seconds)
    final stopwatch = Stopwatch()..start();
    final generated = await _aiService.generateDialogue(
      cardId: cardId,
      context: context,
    );
    stopwatch.stop();
    
    // Cache in all tiers
    await _cacheDialogue(key, generated);
    
    // Upload to cloud asynchronously
    _uploadToCloud(cardId, interactionId, generated, context);
    
    AppLogger.performance('Generated new dialogue', stopwatch.elapsed);
    return generated;
  }
  
  Future<void> _cacheDialogue(String key, String dialogue) async {
    // Memory cache
    _memoryCache.put(key, dialogue);
    
    // Disk cache
    await _diskCache.put(
      key,
      CachedAIOutput(
        id: key,
        contentType: 'dialogue',
        content: dialogue,
        cachedAt: DateTime.now(),
        expiresAt: DateTime.now().add(CacheTTL.dialogue),
        metadata: {},
      ),
    );
  }
  
  Future<void> _uploadToCloud(
    String cardId,
    String interactionId,
    String dialogue,
    Map<String, double> context,
  ) async {
    // Non-blocking upload
    unawaited(
      _firestore.saveDialogue(
        cardId: cardId,
        interactionId: interactionId,
        dialogue: dialogue,
        metadata: context,
      )
    );
  }
}
```

### Pre-Fetch Pattern

**Predictively load content before it's needed:**

```dart
class PredictivePrefetcher {
  final AIOutputRepository _repository;
  
  /// Pre-fetch likely next dialogues
  Future<void> prefetchLikelyDialogues({
    required String currentCardId,
    required List<String> likelyNextCards,
  }) async {
    // Pre-fetch in background (non-blocking)
    for (final nextCardId in likelyNextCards) {
      unawaited(
        _repository.getDialogue(
          cardId: nextCardId,
          interactionId: 'greeting',
          context: {},
        ).catchError((e) {
          // Silently fail pre-fetch
          AppLogger.info('Pre-fetch failed for $nextCardId');
        }),
      );
    }
  }
}
```

---

## Sync Strategies

### Background Upload Strategy

**All locally generated content uploads to cloud in background:**

```dart
class BackgroundSyncService {
  final Queue<SyncTask> _syncQueue = Queue();
  bool _syncing = false;
  
  /// Add item to sync queue
  void queueForSync(SyncTask task) {
    _syncQueue.add(task);
    _processSyncQueue();
  }
  
  Future<void> _processSyncQueue() async {
    if (_syncing || _syncQueue.isEmpty) return;
    
    _syncing = true;
    
    while (_syncQueue.isNotEmpty) {
      final task = _syncQueue.removeFirst();
      
      try {
        await task.execute();
        AppLogger.info('Synced: ${task.description}');
      } catch (e) {
        AppLogger.error('Sync failed: ${task.description}', e);
        
        // Re-queue with exponential backoff
        if (task.retryCount < 3) {
          await Future.delayed(Duration(seconds: 2 << task.retryCount));
          _syncQueue.add(task.incrementRetry());
        }
      }
    }
    
    _syncing = false;
  }
  
  /// Force sync all pending items (on app background)
  Future<void> syncAll() async {
    while (_syncQueue.isNotEmpty) {
      await _processSyncQueue();
    }
  }
}
```

### Download on Demand

**Download assets from cloud only when needed:**

```dart
Future<Uint8List> getImage(String imagePath) async {
  // Check local cache first
  final cached = await _localImageCache.get(imagePath);
  if (cached != null) return cached;
  
  // Download from Cloud Storage
  final bytes = await _cloudStorage.download(imagePath);
  
  // Cache locally
  await _localImageCache.put(imagePath, bytes);
  
  return bytes;
}
```

---

## Offline-First Design

### Offline Capabilities

**What works offline:**
- ✅ Recently cached dialogues (last 500)
- ✅ Cached card images (frequently used)
- ✅ Cached music stems (recent)
- ✅ Local AI predictions (TFLite)

**What requires connection:**
- ❌ New AI generations
- ❌ First-time asset downloads
- ❌ Cloud sync

### Graceful Degradation

```dart
Future<String> getDialogue({required String cardId}) async {
  try {
    return await _getDialogueWithNetwork(cardId);
  } on SocketException {
    // Offline - use cached or local fallback
    final cached = await _getCachedDialogue(cardId);
    if (cached != null) return cached;
    
    // Last resort: rule-based fallback
    return _getRuleBasedDialogue(cardId);
  }
}
```

---

## Cost Optimization

### Cache Hit Rate Targets

| Content Type | Target Hit Rate | Savings |
|--------------|----------------|---------|
| **Dialogue** | 60-70% | $0.50/player/month |
| **Images** | 90%+ | $0.30/player/month |
| **Video** | 80%+ | $0.20/player/month |
| **Audio** | 85%+ | $0.15/player/month |

### Cost Calculation

```
Without Caching:
1000 dialogues/month × $0.00008 = $0.08
100 images/month × $0.04 = $4.00
10 videos/month × $0.20 = $2.00
Total: $6.08/player/month

With 70% Cache Hit Rate:
300 dialogues generated × $0.00008 = $0.024
10 images generated × $0.04 = $0.40
3 videos generated × $0.20 = $0.60
Total: $1.02/player/month

Savings: $5.06/player/month (83% reduction)
```

**See:** `71-cost-performance-targets.md` for detailed optimization strategies

---

## Implementation Examples

### Complete Service Example

```dart
// lib/features/ai/data/repositories/dialogue_repository.dart
class DialogueRepository {
  final MemoryCache<String> _memoryCache;
  final HiveCache _diskCache;
  final FirebaseFirestore _firestore;
  final AIService _aiService;
  
  /// Get dialogue with full cascade retrieval
  Future<DialogueResponse> getDialogue({
    required String cardId,
    required String interactionId,
  }) async {
    final key = '${cardId}_$interactionId';
    
    // Try memory cache
    final memoryCached = _memoryCache.get(key);
    if (memoryCached != null) {
      return DialogueResponse.fromJson(jsonDecode(memoryCached));
    }
    
    // Try disk cache
    final diskCached = await _diskCache.get(key);
    if (diskCached != null) {
      _memoryCache.put(key, diskCached.content);
      return DialogueResponse.fromJson(jsonDecode(diskCached.content));
    }
    
    // Try cloud
    final cloudDoc = await _firestore
        .collection('ai_outputs')
        .doc(_userId)
        .collection('dialogues')
        .doc(key)
        .get();
    
    if (cloudDoc.exists) {
      final response = DialogueResponse.fromFirestore(cloudDoc);
      await _cacheDialogue(key, response);
      return response;
    }
    
    // Generate new
    final generated = await _aiService.generateDialogue(cardId: cardId);
    await _cacheDialogue(key, generated);
    _uploadToFirestore(key, generated);
    
    return generated;
  }
  
  Future<void> _cacheDialogue(String key, DialogueResponse response) async {
    final json = jsonEncode(response.toJson());
    _memoryCache.put(key, json);
    await _diskCache.put(
      key,
      CachedAIOutput(
        id: key,
        contentType: 'dialogue',
        content: json,
        cachedAt: DateTime.now(),
        expiresAt: DateTime.now().add(CacheTTL.dialogue),
        metadata: {},
      ),
    );
  }
  
  Future<void> _uploadToFirestore(String key, DialogueResponse response) async {
    unawaited(
      _firestore
          .collection('ai_outputs')
          .doc(_userId)
          .collection('dialogues')
          .doc(key)
          .set(response.toFirestore()),
    );
  }
}
```

---

## Monitoring & Analytics

### Key Metrics to Track

```dart
class CacheMetrics {
  int memoryHits = 0;
  int diskHits = 0;
  int cloudHits = 0;
  int misses = 0;
  
  double get hitRate => (memoryHits + diskHits + cloudHits) / totalRequests;
  double get memoryHitRate => memoryHits / totalRequests;
  double get diskHitRate => diskHits / totalRequests;
  double get cloudHitRate => cloudHits / totalRequests;
  
  int get totalRequests => memoryHits + diskHits + cloudHits + misses;
  
  double get costSavings {
    // Each hit saves $0.00008 (average generation cost)
    final hits = memoryHits + diskHits + cloudHits;
    return hits * 0.00008;
  }
}
```

### Analytics Events

```dart
// Track cache performance
analytics.logEvent(
  name: 'cache_performance',
  parameters: {
    'hit_rate': metrics.hitRate,
    'memory_hit_rate': metrics.memoryHitRate,
    'cost_savings_usd': metrics.costSavings,
  },
);
```

---

## Related Documentation

- **40-hybrid-cloud-local-system.md** - Cloud-local routing and integration
- **51-storage-metadata-schemas.md** - Complete schema definitions
- **52-local-cache-implementation.md** - Hive cache implementation details
- **53-cloud-storage-integration.md** - Firebase setup and configuration
- **71-cost-performance-targets.md** - Cost optimization strategies

---

**Status:** ✅ Complete Architecture  
**Implementation:** See sub-documents (51-53) for detailed implementation  
**Next Steps:** Implement three-tier caching system with cascade retrieval


