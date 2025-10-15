# Cloud Storage Integration

**Purpose:** Firebase Cloud Storage and Firestore integration for AI outputs  
**Audience:** Backend engineers, mobile developers  
**Status:** ✅ Complete  
**Related:** ← 50-ai-output-storage-system.md | 51-storage-metadata-schemas.md | 52-local-cache-implementation.md

---

## What This Document Covers

**Complete Firebase integration:**
- Firestore setup for metadata
- Cloud Storage setup for assets
- Security rules
- Upload/download patterns
- Background sync service
- Batch operations
- Error handling and retries
- Cost optimization

---

## Table of Contents

1. [Firebase Setup](#firebase-setup)
2. [Firestore Integration](#firestore-integration)
3. [Cloud Storage Integration](#cloud-storage-integration)
4. [Security Rules](#security-rules)
5. [Sync Service](#sync-service)
6. [Error Handling](#error-handling)
7. [Cost Optimization](#cost-optimization)
8. [Complete Example](#complete-example)

---

## Firebase Setup

### Dependencies

```yaml
# app/pubspec.yaml
dependencies:
  firebase_core: ^3.11.0
  cloud_firestore: ^5.5.0
  firebase_storage: ^12.3.4
  firebase_app_check: ^0.3.0  # CRITICAL for security
```

### Initialization

```dart
// lib/main.dart
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_app_check/firebase_app_check.dart';
import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  
  // CRITICAL: Enable App Check
  await FirebaseAppCheck.instance.activate(
    androidProvider: AndroidProvider.playIntegrity,
    appleProvider: AppleProvider.appAttest,
  );
  
  runApp(const MyApp());
}
```

---

## Firestore Integration

### Service Implementation

```dart
// lib/features/ai/data/services/firestore_ai_service.dart
import 'package:cloud_firestore/cloud_firestore.dart';

class FirestoreAIService {
  final FirebaseFirestore _firestore;
  final String _userId;
  
  FirestoreAIService({
    required String userId,
    FirebaseFirestore? firestore,
  })  : _userId = userId,
        _firestore = firestore ?? FirebaseFirestore.instance;
  
  /// Save dialogue metadata to Firestore
  Future<void> saveDialogue({
    required String cardId,
    required String interactionId,
    required String text,
    required Map<String, double> personalityTraits,
    required String model,
    required int latencyMs,
    required double costUsd,
  }) async {
    final docId = '${cardId}_$interactionId';
    
    await _firestore
        .collection('ai_outputs')
        .doc(_userId)
        .collection('dialogues')
        .doc(docId)
        .set({
      'card_id': cardId,
      'interaction_id': interactionId,
      'text': text,
      'generated_at': FieldValue.serverTimestamp(),
      'model': model,
      'model_version': _getModelVersion(model),
      'latency_ms': latencyMs,
      'cost_usd': costUsd,
      'personality_traits': personalityTraits,
      'cached': true,  // Now cached locally
      'cache_hit_count': 0,
      'last_accessed': FieldValue.serverTimestamp(),
      'version': 1,
    });
    
    AppLogger.info('Saved dialogue to Firestore: $docId');
  }
  
  /// Get dialogue from Firestore
  Future<DialogueModel?> getDialogue(
    String cardId,
    String interactionId,
  ) async {
    final docId = '${cardId}_$interactionId';
    
    final doc = await _firestore
        .collection('ai_outputs')
        .doc(_userId)
        .collection('dialogues')
        .doc(docId)
        .get();
    
    if (!doc.exists) {
      return null;
    }
    
    // Update access statistics
    await doc.reference.update({
      'cache_hit_count': FieldValue.increment(1),
      'last_accessed': FieldValue.serverTimestamp(),
    });
    
    return DialogueModel.fromFirestore(doc);
  }
  
  /// Batch save multiple dialogues
  Future<void> batchSaveDialogues(List<DialogueModel> dialogues) async {
    final batch = _firestore.batch();
    
    for (final dialogue in dialogues) {
      final ref = _firestore
          .collection('ai_outputs')
          .doc(_userId)
          .collection('dialogues')
          .doc(dialogue.id);
      
      batch.set(ref, dialogue.toFirestore());
    }
    
    await batch.commit();
    AppLogger.info('Batch saved ${dialogues.length} dialogues');
  }
  
  /// Get cost analytics
  Future<Map<String, dynamic>> getCostAnalytics() async {
    final snapshot = await _firestore
        .collection('ai_outputs')
        .doc(_userId)
        .collection('dialogues')
        .get();
    
    final docs = snapshot.docs;
    final totalCost = docs.fold<double>(
      0.0,
      (sum, doc) => sum + (doc.data()['cost_usd'] as num).toDouble(),
    );
    
    final cachedDocs = docs.where((doc) => doc.data()['cached'] == true);
    final cacheRate = docs.isEmpty ? 0.0 : cachedDocs.length / docs.length;
    
    return {
      'total_generations': docs.length,
      'total_cost_usd': totalCost,
      'cache_rate': cacheRate,
      'avg_cost_per_generation': docs.isEmpty ? 0.0 : totalCost / docs.length,
    };
  }
  
  String _getModelVersion(String model) {
    // Map model names to versions
    return {
      'gemini-2.5-flash': '2.5.20251001',
      'gemini-2.5-pro': '2.5.20251001',
    }[model] ?? 'unknown';
  }
}
```

---

## Cloud Storage Integration

### Upload Service

```dart
// lib/features/ai/data/services/cloud_storage_ai_service.dart
import 'package:firebase_storage/firebase_storage.dart';
import 'dart:typed_data';

class CloudStorageAIService {
  final FirebaseStorage _storage;
  final String _userId;
  
  CloudStorageAIService({
    required String userId,
    FirebaseStorage? storage,
  })  : _userId = userId,
        _storage = storage ?? FirebaseStorage.instance;
  
  /// Upload image to Cloud Storage
  Future<String> uploadImage({
    required String cardId,
    required String imageType,  // "portrait" | "action" | "evolution"
    required Uint8List imageBytes,
  }) async {
    final path = 'users/$_userId/ai_generated/images/${cardId}_$imageType.webp';
    final ref = _storage.ref().child(path);
    
    // Upload with metadata
    final metadata = SettableMetadata(
      contentType: 'image/webp',
      customMetadata: {
        'card_id': cardId,
        'image_type': imageType,
        'generated_at': DateTime.now().toIso8601String(),
      },
    );
    
    final task = ref.putData(imageBytes, metadata);
    
    // Monitor upload progress
    task.snapshotEvents.listen((snapshot) {
      final progress = snapshot.bytesTransferred / snapshot.totalBytes;
      AppLogger.info('Upload progress: ${(progress * 100).toStringAsFixed(1)}%');
    });
    
    await task;
    
    AppLogger.info('Uploaded image: $path');
    return path;
  }
  
  /// Download image from Cloud Storage
  Future<Uint8List> downloadImage(String path) async {
    final ref = _storage.ref().child(path);
    
    // Get download URL (cached for 1 hour)
    final url = await ref.getDownloadURL();
    
    // Download data
    final data = await ref.getData();
    
    if (data == null) {
      throw Exception('Failed to download image: $path');
    }
    
    AppLogger.info('Downloaded image: $path (${data.length} bytes)');
    return data;
  }
  
  /// Upload video to Cloud Storage
  Future<String> uploadVideo({
    required String sceneId,
    required Uint8List videoBytes,
  }) async {
    final path = 'users/$_userId/ai_generated/videos/$sceneId.mp4';
    final ref = _storage.ref().child(path);
    
    final metadata = SettableMetadata(
      contentType: 'video/mp4',
      customMetadata: {
        'scene_id': sceneId,
        'generated_at': DateTime.now().toIso8601String(),
      },
    );
    
    await ref.putData(videoBytes, metadata);
    
    AppLogger.info('Uploaded video: $path');
    return path;
  }
  
  /// Upload audio stem to Cloud Storage
  Future<String> uploadAudioStem({
    required String stemId,
    required String stemType,  // "bass" | "drums" | "melody" | etc
    required Uint8List audioBytes,
  }) async {
    final path = 'users/$_userId/ai_generated/audio/stems/${stemType}_$stemId.opus';
    final ref = _storage.ref().child(path);
    
    final metadata = SettableMetadata(
      contentType: 'audio/opus',
      customMetadata: {
        'stem_id': stemId,
        'stem_type': stemType,
        'generated_at': DateTime.now().toIso8601String(),
      },
    );
    
    await ref.putData(audioBytes, metadata);
    
    AppLogger.info('Uploaded audio stem: $path');
    return path;
  }
  
  /// Delete file from Cloud Storage
  Future<void> delete(String path) async {
    final ref = _storage.ref().child(path);
    await ref.delete();
    AppLogger.info('Deleted: $path');
  }
  
  /// Get storage usage for user
  Future<int> getStorageUsage() async {
    final ref = _storage.ref().child('users/$_userId/ai_generated');
    
    int totalBytes = 0;
    
    // List all files recursively
    final result = await ref.listAll();
    
    for (final item in result.items) {
      final metadata = await item.getMetadata();
      totalBytes += metadata.size ?? 0;
    }
    
    AppLogger.info('Storage usage: ${(totalBytes / 1024 / 1024).toStringAsFixed(2)} MB');
    return totalBytes;
  }
}
```

---

## Security Rules

### Firestore Security Rules

```javascript
// firestore.rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Helper functions
    function isAuthenticated() {
      return request.auth != null;
    }
    
    function isOwner(userId) {
      return isAuthenticated() && request.auth.uid == userId;
    }
    
    // AI outputs - users can only access their own
    match /ai_outputs/{userId}/{document=**} {
      allow read: if isOwner(userId);
      allow write: if isOwner(userId) && 
                    request.resource.size < 1000000;  // 1MB limit per doc
    }
    
    // Cards (read-only for players)
    match /cards/{cardId} {
      allow read: if isAuthenticated();
      allow write: if false;  // Only admin can write
    }
    
    // Player data
    match /players/{userId} {
      allow read: if isOwner(userId);
      allow write: if isOwner(userId);
      
      // Sub-collections
      match /{document=**} {
        allow read: if isOwner(userId);
        allow write: if isOwner(userId);
      }
    }
  }
}
```

### Cloud Storage Security Rules

```javascript
// storage.rules
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    
    // Helper functions
    function isAuthenticated() {
      return request.auth != null;
    }
    
    function isOwner(userId) {
      return isAuthenticated() && request.auth.uid == userId;
    }
    
    function isValidSize() {
      return request.resource.size < 5 * 1024 * 1024;  // 5MB limit
    }
    
    function isValidImageType() {
      return request.resource.contentType.matches('image/.*');
    }
    
    function isValidVideoType() {
      return request.resource.contentType == 'video/mp4';
    }
    
    function isValidAudioType() {
      return request.resource.contentType.matches('audio/.*');
    }
    
    // AI generated content - users can only access their own
    match /users/{userId}/ai_generated/{allPaths=**} {
      // Read: owner only
      allow read: if isOwner(userId);
      
      // Write: owner only, with size and type checks
      allow write: if isOwner(userId) && 
                     isValidSize() &&
                     (isValidImageType() || isValidVideoType() || isValidAudioType());
    }
  }
}
```

---

## Sync Service

### Background Sync

```dart
// lib/core/sync/ai_output_sync_service.dart
import 'dart:collection';

class AIOutputSyncService {
  final FirestoreAIService _firestoreService;
  final CloudStorageAIService _storageService;
  
  final Queue<SyncTask> _syncQueue = Queue();
  bool _syncing = false;
  
  AIOutputSyncService({
    required FirestoreAIService firestoreService,
    required CloudStorageAIService storageService,
  })  : _firestoreService = firestoreService,
        _storageService = storageService;
  
  /// Queue item for sync
  void queueForSync(SyncTask task) {
    _syncQueue.add(task);
    AppLogger.info('Queued for sync: ${task.id} (queue size: ${_syncQueue.length})');
    
    // Start processing if not already syncing
    _processSyncQueue();
  }
  
  /// Process sync queue
  Future<void> _processSyncQueue() async {
    if (_syncing || _syncQueue.isEmpty) return;
    
    _syncing = true;
    
    while (_syncQueue.isNotEmpty) {
      final task = _syncQueue.removeFirst();
      
      try {
        await task.execute(
          firestoreService: _firestoreService,
          storageService: _storageService,
        );
        
        AppLogger.info('Synced: ${task.id}');
      } catch (e, stack) {
        AppLogger.error('Sync failed: ${task.id}', e, stack);
        
        // Re-queue with exponential backoff
        if (task.retryCount < 3) {
          await Future.delayed(Duration(seconds: 2 << task.retryCount));
          _syncQueue.add(task.incrementRetry());
        } else {
          AppLogger.error('Sync failed after 3 retries: ${task.id}', e);
        }
      }
    }
    
    _syncing = false;
  }
  
  /// Force sync all pending items
  Future<void> syncAll() async {
    while (_syncQueue.isNotEmpty) {
      await _processSyncQueue();
    }
  }
  
  /// Get sync statistics
  SyncStats get stats => SyncStats(
    queueSize: _syncQueue.length,
    isSyncing: _syncing,
  );
}

abstract class SyncTask {
  final String id;
  final int retryCount;
  
  SyncTask({required this.id, this.retryCount = 0});
  
  Future<void> execute({
    required FirestoreAIService firestoreService,
    required CloudStorageAIService storageService,
  });
  
  SyncTask incrementRetry();
}

class DialogueSyncTask extends SyncTask {
  final DialogueModel dialogue;
  
  DialogueSyncTask({
    required this.dialogue,
    super.retryCount,
  }) : super(id: dialogue.id);
  
  @override
  Future<void> execute({
    required FirestoreAIService firestoreService,
    required CloudStorageAIService storageService,
  }) async {
    await firestoreService.saveDialogue(
      cardId: dialogue.cardId,
      interactionId: dialogue.interactionId,
      text: dialogue.text,
      personalityTraits: dialogue.personalityTraits,
      model: dialogue.model,
      latencyMs: dialogue.latencyMs,
      costUsd: dialogue.costUsd,
    );
  }
  
  @override
  SyncTask incrementRetry() => DialogueSyncTask(
        dialogue: dialogue,
        retryCount: retryCount + 1,
      );
}

class ImageSyncTask extends SyncTask {
  final String cardId;
  final String imageType;
  final Uint8List imageBytes;
  
  ImageSyncTask({
    required this.cardId,
    required this.imageType,
    required this.imageBytes,
    super.retryCount,
  }) : super(id: '${cardId}_$imageType');
  
  @override
  Future<void> execute({
    required FirestoreAIService firestoreService,
    required CloudStorageAIService storageService,
  }) async {
    await storageService.uploadImage(
      cardId: cardId,
      imageType: imageType,
      imageBytes: imageBytes,
    );
  }
  
  @override
  SyncTask incrementRetry() => ImageSyncTask(
        cardId: cardId,
        imageType: imageType,
        imageBytes: imageBytes,
        retryCount: retryCount + 1,
      );
}

class SyncStats {
  final int queueSize;
  final bool isSyncing;
  
  SyncStats({required this.queueSize, required this.isSyncing});
}
```

---

## Error Handling

### Retry Logic

```dart
/// Retry with exponential backoff
Future<T> retryWithBackoff<T>({
  required Future<T> Function() operation,
  int maxRetries = 3,
  Duration initialDelay = const Duration(seconds: 1),
}) async {
  int attempt = 0;
  
  while (true) {
    try {
      return await operation();
    } catch (e) {
      attempt++;
      
      if (attempt >= maxRetries) {
        rethrow;
      }
      
      final delay = initialDelay * (1 << attempt);  // Exponential backoff
      AppLogger.info('Retry attempt $attempt after ${delay.inSeconds}s');
      await Future.delayed(delay);
    }
  }
}

// Usage
final result = await retryWithBackoff(
  operation: () => _firestoreService.saveDialogue(...),
  maxRetries: 3,
);
```

---

## Cost Optimization

### Batch Operations

```dart
/// Batch multiple Firestore writes to save costs
Future<void> batchSync(List<DialogueModel> dialogues) async {
  // Firestore batch write (cheaper than individual writes)
  await _firestoreService.batchSaveDialogues(dialogues);
  
  // Cost: 1 write operation for up to 500 documents
  // vs. N write operations for N individual writes
}
```

### Conditional Uploads

```dart
/// Only upload if not already exists
Future<void> uploadIfNotExists(String path, Uint8List data) async {
  try {
    // Check if exists
    await _storage.ref().child(path).getMetadata();
    AppLogger.info('File already exists, skipping upload: $path');
  } on FirebaseException catch (e) {
    if (e.code == 'object-not-found') {
      // Doesn't exist, upload
      await _storage.ref().child(path).putData(data);
    } else {
      rethrow;
    }
  }
}
```

---

## Complete Example

### Full Integration Service

```dart
// lib/features/ai/data/repositories/cloud_ai_repository.dart
class CloudAIRepository {
  final FirestoreAIService _firestore;
  final CloudStorageAIService _storage;
  final AIOutputSyncService _sync;
  final HiveCache _cache;
  
  CloudAIRepository({
    required FirestoreAIService firestore,
    required CloudStorageAIService storage,
    required AIOutputSyncService sync,
    required HiveCache cache,
  })  : _firestore = firestore,
        _storage = storage,
        _sync = sync,
        _cache = cache;
  
  /// Save dialogue (local first, sync later)
  Future<void> saveDialogue(DialogueModel dialogue) async {
    // Save to local cache immediately
    await _cache.put(
      dialogue.id,
      CachedAIOutput(
        id: dialogue.id,
        contentType: 'dialogue',
        content: dialogue.text,
        cachedAt: DateTime.now(),
        expiresAt: DateTime.now().add(CacheTTL.dialogue),
        metadata: dialogue.toJson(),
      ),
    );
    
    // Queue for background sync to Firestore
    _sync.queueForSync(DialogueSyncTask(dialogue: dialogue));
  }
  
  /// Get dialogue (cloud fallback)
  Future<String?> getDialogue(String cardId, String interactionId) async {
    final id = '${cardId}_$interactionId';
    
    // Try local cache first
    final cached = await _cache.get(id);
    if (cached != null) {
      return cached.content;
    }
    
    // Fallback to Firestore
    final cloud = await _firestore.getDialogue(cardId, interactionId);
    if (cloud != null) {
      // Cache for next time
      await _cache.put(
        id,
        CachedAIOutput(
          id: id,
          contentType: 'dialogue',
          content: cloud.text,
          cachedAt: DateTime.now(),
          expiresAt: DateTime.now().add(CacheTTL.dialogue),
          metadata: {},
        ),
      );
      
      return cloud.text;
    }
    
    return null;
  }
}
```

---

## Related Documentation

- **50-ai-output-storage-system.md** - Overall storage architecture
- **51-storage-metadata-schemas.md** - Data schemas
- **52-local-cache-implementation.md** - Local caching
- **02-technology-stack.md** - Firebase costs and pricing

---

**Status:** ✅ Complete Implementation Guide  
**Critical:** App Check MUST be enabled for security  
**Cost Target:** $0.06/GB Firestore + $0.026/GB Cloud Storage


