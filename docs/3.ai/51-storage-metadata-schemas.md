# AI Output Metadata Schemas

**Purpose:** Complete schema definitions for all AI-generated content types  
**Audience:** Backend engineers, mobile developers  
**Status:** ✅ Complete  
**Related:** ← 50-ai-output-storage-system.md | → 52-local-cache-implementation.md

---

## What This Document Contains

**Complete metadata schemas for:**
1. Dialogue metadata
2. Image metadata
3. Video metadata
4. Audio/music stem metadata
5. Common fields across all types

**Use these schemas for:**
- Firestore document structure
- Local cache models (Hive, Dart classes)
- API request/response models
- Analytics and reporting

---

## Table of Contents

1. [Common Fields](#common-fields)
2. [Dialogue Metadata](#dialogue-metadata)
3. [Image Metadata](#image-metadata)
4. [Video Metadata](#video-metadata)
5. [Audio Stem Metadata](#audio-stem-metadata)
6. [Dart Model Classes](#dart-model-classes)
7. [Firestore Examples](#firestore-examples)

---

## Common Fields

### Fields Present in All AI Output Types

```typescript
interface CommonAIMetadata {
  // Identity
  id: string;                          // Unique identifier
  user_id: string;                     // Owner user ID
  content_type: ContentType;            // "dialogue" | "image" | "video" | "audio"
  
  // Generation metadata
  generated_at: Timestamp;              // When generated
  model: string;                        // AI model used ("gemini-2.5-flash" | "gemini-2.5-pro" | "imagen-3" | "veo" | "lyria")
  model_version: string;                // Model version (for tracking)
  
  // Performance metrics
  latency_ms: number;                   // Generation time in milliseconds
  cost_usd: number;                     // Generation cost in USD
  
  // Caching
  cached: boolean;                      // Whether this is in cache
  cache_hit_count: number;              // Times retrieved from cache
  last_accessed: Timestamp;             // Last access time
  
  // Quality and feedback
  quality_score?: number;               // Automated quality score (0.0-1.0)
  user_feedback?: "liked" | "disliked" | "reported" | null; // User rating
  
  // Versioning
  version: number;                      // Schema version (for migrations)
}

type ContentType = "dialogue" | "image" | "video" | "audio";
```

---

## Dialogue Metadata

### Complete Schema

```typescript
interface DialogueMetadata extends CommonAIMetadata {
  content_type: "dialogue";
  
  // Content
  text: string;                         // The actual dialogue text
  text_length: number;                  // Character count
  
  // Context
  card_id: string;                      // Card this dialogue is for
  card_name: string;                    // Card name (denormalized)
  interaction_id: string;               // Interaction identifier
  interaction_type: InteractionType;    // Type of interaction
  
  // Personality context (OCEAN traits)
  personality_traits: {
    openness: number;                   // 0.0 - 1.0
    conscientiousness: number;          // 0.0 - 1.0
    extraversion: number;               // 0.0 - 1.0
    agreeableness: number;              // 0.0 - 1.0
    neuroticism: number;                // 0.0 - 1.0
  };
  
  // Relationship context
  relationship_level: number;           // 1-5 (card level)
  trust_score: number;                  // 0.0 - 1.0
  friendship_score: number;             // 0.0 - 1.0
  
  // Generation details
  prompt_template: string;              // Template used (from 11-prompt-templates-library.md)
  context_length: number;               // Input tokens
  output_length: number;                // Output tokens
  
  // Memory and consistency
  memory_ids: string[];                 // Referenced memory IDs
  canonical_fact_ids: string[];         // Referenced canonical facts
  
  // Validation
  passed_validation: boolean;           // Passed quality checks
  cliche_score?: number;                // Cliché detection score (lower = better)
  consistency_score?: number;           // Consistency with past (higher = better)
  
  // Master Truths v1.2 compliance
  urgency_level?: number;               // 1x, 2x, 3x, 5x (crisis)
  emotional_capacity?: number;          // 0-10 scale
  response_authenticity?: number;       // 0.0-1.0 (authenticity score)
}

type InteractionType = 
  | "greeting"
  | "conversation"
  | "crisis"
  | "romantic"
  | "conflict"
  | "evolution"
  | "memory";
```

### Firestore Document Example

```javascript
// Firestore: ai_outputs/{user_id}/dialogues/{card_id}_{interaction_id}
{
  // Common fields
  id: "card_123_interaction_456",
  user_id: "user_abc123",
  content_type: "dialogue",
  generated_at: Timestamp(2025, 10, 15, 10, 30, 0),
  model: "gemini-2.5-flash",
  model_version: "2.5.20251001",
  latency_ms: 2847,
  cost_usd: 0.0000825,
  cached: true,
  cache_hit_count: 3,
  last_accessed: Timestamp(2025, 10, 15, 14, 20, 0),
  quality_score: 0.87,
  user_feedback: "liked",
  version: 1,
  
  // Dialogue-specific
  text: "I understand how you feel. When I was younger, I struggled with similar doubts...",
  text_length: 142,
  card_id: "card_123",
  card_name: "Elena Rivers",
  interaction_id: "interaction_456",
  interaction_type: "conversation",
  personality_traits: {
    openness: 0.75,
    conscientiousness: 0.60,
    extraversion: 0.80,
    agreeableness: 0.70,
    neuroticism: 0.45
  },
  relationship_level: 3,
  trust_score: 0.72,
  friendship_score: 0.68,
  prompt_template: "conversation_deep_bond",
  context_length: 487,
  output_length: 156,
  memory_ids: ["mem_001", "mem_045"],
  canonical_fact_ids: ["fact_012"],
  passed_validation: true,
  cliche_score: 0.12,
  consistency_score: 0.91,
  urgency_level: 1,
  emotional_capacity: 7.2,
  response_authenticity: 0.89
}
```

---

## Image Metadata

### Complete Schema

```typescript
interface ImageMetadata extends CommonAIMetadata {
  content_type: "image";
  
  // Storage
  storage_path: string;                 // Cloud Storage path
  local_path?: string;                  // Local cache path (optional)
  
  // Content
  card_id?: string;                     // Card this image is for (if applicable)
  type: ImageType;                      // Image type
  
  // Technical details
  dimensions: {
    width: number;                      // Pixels
    height: number;                     // Pixels
  };
  format: ImageFormat;                  // "webp" | "png" | "jpg"
  size_bytes: number;                   // File size
  
  // Generation details
  prompt: string;                       // Text prompt used (may be truncated)
  prompt_hash: string;                  // Hash for deduplication
  negative_prompt?: string;             // Negative prompt (if used)
  
  // Image-specific settings
  style?: string;                       // Art style ("portrait" | "anime" | "realistic")
  seed?: number;                        // Generation seed (for reproducibility)
  
  // SDK change note
  sdk: "google-ai" | "vertex-ai";       // Which SDK was used (see doc 80)
  
  // Usage
  download_count: number;               // Times downloaded
  view_count: number;                   // Times displayed
}

type ImageType = 
  | "card_portrait"
  | "card_action"
  | "card_evolution"
  | "scene_background"
  | "item"
  | "custom";

type ImageFormat = "webp" | "png" | "jpg";
```

### Firestore Document Example

```javascript
// Firestore: ai_outputs/{user_id}/images/{card_id}_{type}
{
  // Common fields
  id: "card_123_portrait",
  user_id: "user_abc123",
  content_type: "image",
  generated_at: Timestamp(2025, 10, 10, 15, 45, 0),
  model: "imagen-3",
  model_version: "3.0.20251001",
  latency_ms: 15234,
  cost_usd: 0.04,
  cached: true,
  cache_hit_count: 12,
  last_accessed: Timestamp(2025, 10, 15, 14, 20, 0),
  quality_score: 0.92,
  user_feedback: null,
  version: 1,
  
  // Image-specific
  storage_path: "users/user_abc123/ai_generated/images/card_123_portrait.webp",
  local_path: "/data/cache/card_123_portrait.webp",
  card_id: "card_123",
  type: "card_portrait",
  dimensions: {
    width: 1024,
    height: 1024
  },
  format: "webp",
  size_bytes: 87352,
  prompt: "Portrait of a young woman with auburn hair, confident expression, modern casual clothing...",
  prompt_hash: "a3f5e8c2d1b9",
  negative_prompt: "blurry, low quality, distorted",
  style: "realistic",
  seed: 42,
  sdk: "google-ai",
  download_count: 12,
  view_count: 45
}
```

---

## Video Metadata

### Complete Schema

```typescript
interface VideoMetadata extends CommonAIMetadata {
  content_type: "video";
  
  // Storage
  storage_path: string;                 // Cloud Storage path
  local_path?: string;                  // Local cache path
  thumbnail_path?: string;              // Thumbnail image path
  
  // Content
  scene_id: string;                     // Scene identifier
  type: VideoType;                      // Video type
  
  // Technical details
  duration_sec: number;                 // Duration in seconds
  dimensions: {
    width: number;                      // Pixels
    height: number;                     // Pixels
  };
  fps: number;                          // Frames per second
  format: VideoFormat;                  // "mp4" | "webm"
  size_bytes: number;                   // File size
  codec: string;                        // Video codec ("h264" | "vp9")
  
  // Generation details
  prompt: string;                       // Text prompt
  prompt_hash: string;                  // For deduplication
  keyframes?: string[];                 // Keyframe descriptions
  
  // Video-specific settings
  style?: string;                       // Visual style
  seed?: number;                        // Generation seed
  
  // Usage
  play_count: number;                   // Times played
  completion_rate?: number;             // % watched (average)
}

type VideoType = 
  | "card_evolution"
  | "story_cutscene"
  | "tutorial"
  | "custom";

type VideoFormat = "mp4" | "webm";
```

### Firestore Document Example

```javascript
// Firestore: ai_outputs/{user_id}/videos/{scene_id}
{
  // Common fields
  id: "evolution_3_to_4",
  user_id: "user_abc123",
  content_type: "video",
  generated_at: Timestamp(2025, 10, 12, 18, 20, 0),
  model: "veo",
  model_version: "1.0.20251001",
  latency_ms: 45678,
  cost_usd: 0.20,
  cached: true,
  cache_hit_count: 2,
  last_accessed: Timestamp(2025, 10, 15, 10, 15, 0),
  quality_score: 0.88,
  user_feedback: null,
  version: 1,
  
  // Video-specific
  storage_path: "users/user_abc123/ai_generated/videos/evolution_3_to_4.mp4",
  local_path: "/data/cache/evolution_3_to_4.mp4",
  thumbnail_path: "users/user_abc123/ai_generated/videos/evolution_3_to_4_thumb.webp",
  scene_id: "evolution_3_to_4",
  type: "card_evolution",
  duration_sec: 5.2,
  dimensions: {
    width: 1920,
    height: 1080
  },
  fps: 30,
  format: "mp4",
  size_bytes: 1245600,
  codec: "h264",
  prompt: "Card evolution animation from level 3 to level 4, character gaining confidence...",
  prompt_hash: "b8d4f2a1c9e7",
  keyframes: [
    "Opening: character at level 3",
    "Middle: transformation sequence",
    "End: character at level 4"
  ],
  style: "anime",
  seed: 123,
  play_count: 2,
  completion_rate: 0.95
}
```

---

## Audio Stem Metadata

### Complete Schema

```typescript
interface AudioStemMetadata extends CommonAIMetadata {
  content_type: "audio";
  
  // Storage
  storage_path: string;                 // Cloud Storage path
  local_path?: string;                  // Local cache path
  
  // Content
  stem_id: string;                      // Unique stem identifier
  stem_type: StemType;                  // Type of audio stem
  
  // Technical details
  duration_sec: number;                 // Duration in seconds
  format: AudioFormat;                  // "opus" | "mp3" | "wav"
  size_bytes: number;                   // File size
  sample_rate: number;                  // Hz (48000 typical)
  bitrate: number;                      // kbps
  
  // Musical properties
  mood: Mood;                           // Musical mood
  tempo: number;                        // BPM (beats per minute)
  key?: string;                         // Musical key ("C major", "A minor", etc.)
  time_signature?: string;              // "4/4", "3/4", etc.
  
  // Generation details
  prompt: string;                       // Text prompt
  prompt_hash: string;                  // For deduplication
  
  // Composition context
  scene_context?: string;               // Game scene this is for
  emotional_intensity?: number;         // 0.0-1.0
  
  // Usage
  play_count: number;                   // Times played
  loop_count?: number;                  // Times looped
  
  // Multi-stem coordination
  stem_group_id?: string;               // Group ID if part of multi-stem composition
  sibling_stem_ids?: string[];          // Other stems in same group
}

type StemType = 
  | "bass"
  | "drums"
  | "melody"
  | "harmony"
  | "ambient"
  | "percussion"
  | "vocals";

type AudioFormat = "opus" | "mp3" | "wav";

type Mood = 
  | "calm"
  | "tense"
  | "joyful"
  | "sad"
  | "mysterious"
  | "epic"
  | "romantic"
  | "energetic";
```

### Firestore Document Example

```javascript
// Firestore: ai_outputs/{user_id}/audio/music_stems/{stem_id}
{
  // Common fields
  id: "stem_bass_001",
  user_id: "user_abc123",
  content_type: "audio",
  generated_at: Timestamp(2025, 10, 11, 12, 0, 0),
  model: "lyria",
  model_version: "1.0.20251001",
  latency_ms: 45000,
  cost_usd: 0.10,
  cached: true,
  cache_hit_count: 5,
  last_accessed: Timestamp(2025, 10, 15, 16, 30, 0),
  quality_score: 0.85,
  user_feedback: null,
  version: 1,
  
  // Audio-specific
  storage_path: "users/user_abc123/ai_generated/audio/stems/bass_stem_001.opus",
  local_path: "/data/cache/bass_stem_001.opus",
  stem_id: "stem_bass_001",
  stem_type: "bass",
  duration_sec: 30.0,
  format: "opus",
  size_bytes: 245600,
  sample_rate: 48000,
  bitrate: 64,
  mood: "calm",
  tempo: 120,
  key: "C major",
  time_signature: "4/4",
  prompt: "Calm bass line for contemplative scene, warm and mellow",
  prompt_hash: "c7f3a9e2d5b1",
  scene_context: "card_conversation",
  emotional_intensity: 0.4,
  play_count: 5,
  loop_count: 15,
  stem_group_id: "composition_001",
  sibling_stem_ids: ["stem_drums_001", "stem_melody_001", "stem_ambient_001"]
}
```

---

## Dart Model Classes

### Base AI Output Model

```dart
// lib/features/ai/data/models/ai_output_model.dart
import 'package:cloud_firestore/cloud_firestore.dart';

abstract class AIOutputModel {
  final String id;
  final String userId;
  final String contentType;
  final DateTime generatedAt;
  final String model;
  final String modelVersion;
  final int latencyMs;
  final double costUsd;
  final bool cached;
  final int cacheHitCount;
  final DateTime lastAccessed;
  final double? qualityScore;
  final String? userFeedback;
  final int version;
  
  AIOutputModel({
    required this.id,
    required this.userId,
    required this.contentType,
    required this.generatedAt,
    required this.model,
    required this.modelVersion,
    required this.latencyMs,
    required this.costUsd,
    required this.cached,
    required this.cacheHitCount,
    required this.lastAccessed,
    this.qualityScore,
    this.userFeedback,
    this.version = 1,
  });
  
  Map<String, dynamic> toJson();
  Map<String, dynamic> toFirestore();
}
```

### Dialogue Model

```dart
// lib/features/ai/data/models/dialogue_model.dart
class DialogueModel extends AIOutputModel {
  final String text;
  final int textLength;
  final String cardId;
  final String cardName;
  final String interactionId;
  final String interactionType;
  final Map<String, double> personalityTraits;
  final int relationshipLevel;
  final double trustScore;
  final double friendshipScore;
  final String promptTemplate;
  final int contextLength;
  final int outputLength;
  final List<String> memoryIds;
  final List<String> canonicalFactIds;
  final bool passedValidation;
  final double? clicheScore;
  final double? consistencyScore;
  final int? urgencyLevel;
  final double? emotionalCapacity;
  final double? responseAuthenticity;
  
  DialogueModel({
    required super.id,
    required super.userId,
    required super.generatedAt,
    required super.model,
    required super.modelVersion,
    required super.latencyMs,
    required super.costUsd,
    required super.cached,
    required super.cacheHitCount,
    required super.lastAccessed,
    required this.text,
    required this.textLength,
    required this.cardId,
    required this.cardName,
    required this.interactionId,
    required this.interactionType,
    required this.personalityTraits,
    required this.relationshipLevel,
    required this.trustScore,
    required this.friendshipScore,
    required this.promptTemplate,
    required this.contextLength,
    required this.outputLength,
    required this.memoryIds,
    required this.canonicalFactIds,
    required this.passedValidation,
    super.qualityScore,
    super.userFeedback,
    this.clicheScore,
    this.consistencyScore,
    this.urgencyLevel,
    this.emotionalCapacity,
    this.responseAuthenticity,
  }) : super(contentType: 'dialogue');
  
  factory DialogueModel.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return DialogueModel(
      id: doc.id,
      userId: data['user_id'],
      generatedAt: (data['generated_at'] as Timestamp).toDate(),
      model: data['model'],
      modelVersion: data['model_version'],
      latencyMs: data['latency_ms'],
      costUsd: data['cost_usd'].toDouble(),
      cached: data['cached'],
      cacheHitCount: data['cache_hit_count'],
      lastAccessed: (data['last_accessed'] as Timestamp).toDate(),
      text: data['text'],
      textLength: data['text_length'],
      cardId: data['card_id'],
      cardName: data['card_name'],
      interactionId: data['interaction_id'],
      interactionType: data['interaction_type'],
      personalityTraits: Map<String, double>.from(data['personality_traits']),
      relationshipLevel: data['relationship_level'],
      trustScore: data['trust_score'].toDouble(),
      friendshipScore: data['friendship_score'].toDouble(),
      promptTemplate: data['prompt_template'],
      contextLength: data['context_length'],
      outputLength: data['output_length'],
      memoryIds: List<String>.from(data['memory_ids']),
      canonicalFactIds: List<String>.from(data['canonical_fact_ids']),
      passedValidation: data['passed_validation'],
      qualityScore: data['quality_score']?.toDouble(),
      userFeedback: data['user_feedback'],
      clicheScore: data['cliche_score']?.toDouble(),
      consistencyScore: data['consistency_score']?.toDouble(),
      urgencyLevel: data['urgency_level'],
      emotionalCapacity: data['emotional_capacity']?.toDouble(),
      responseAuthenticity: data['response_authenticity']?.toDouble(),
    );
  }
  
  @override
  Map<String, dynamic> toFirestore() {
    return {
      'user_id': userId,
      'content_type': contentType,
      'generated_at': Timestamp.fromDate(generatedAt),
      'model': model,
      'model_version': modelVersion,
      'latency_ms': latencyMs,
      'cost_usd': costUsd,
      'cached': cached,
      'cache_hit_count': cacheHitCount,
      'last_accessed': Timestamp.fromDate(lastAccessed),
      'quality_score': qualityScore,
      'user_feedback': userFeedback,
      'version': version,
      'text': text,
      'text_length': textLength,
      'card_id': cardId,
      'card_name': cardName,
      'interaction_id': interactionId,
      'interaction_type': interactionType,
      'personality_traits': personalityTraits,
      'relationship_level': relationshipLevel,
      'trust_score': trustScore,
      'friendship_score': friendshipScore,
      'prompt_template': promptTemplate,
      'context_length': contextLength,
      'output_length': outputLength,
      'memory_ids': memoryIds,
      'canonical_fact_ids': canonicalFactIds,
      'passed_validation': passedValidation,
      'cliche_score': clicheScore,
      'consistency_score': consistencyScore,
      'urgency_level': urgencyLevel,
      'emotional_capacity': emotionalCapacity,
      'response_authenticity': responseAuthenticity,
    };
  }
  
  @override
  Map<String, dynamic> toJson() {
    return toFirestore()..addAll({
      'generated_at': generatedAt.toIso8601String(),
      'last_accessed': lastAccessed.toIso8601String(),
    });
  }
}
```

---

## Firestore Examples

### Query Examples

```dart
// Get all dialogues for a specific card
Future<List<DialogueModel>> getCardDialogues(String userId, String cardId) async {
  final snapshot = await FirebaseFirestore.instance
      .collection('ai_outputs')
      .doc(userId)
      .collection('dialogues')
      .where('card_id', isEqualTo: cardId)
      .orderBy('generated_at', descending: true)
      .limit(50)
      .get();
  
  return snapshot.docs
      .map((doc) => DialogueModel.fromFirestore(doc))
      .toList();
}

// Get most expensive generations (for cost analysis)
Future<List<AIOutputModel>> getMostExpensiveGenerations(String userId) async {
  final snapshot = await FirebaseFirestore.instance
      .collection('ai_outputs')
      .doc(userId)
      .collection('dialogues')
      .orderBy('cost_usd', descending: true)
      .limit(10)
      .get();
  
  return snapshot.docs
      .map((doc) => DialogueModel.fromFirestore(doc))
      .toList();
}

// Get cache hit statistics
Future<Map<String, dynamic>> getCacheStats(String userId) async {
  final snapshot = await FirebaseFirestore.instance
      .collection('ai_outputs')
      .doc(userId)
      .collection('dialogues')
      .get();
  
  int totalItems = snapshot.docs.length;
  int cachedItems = snapshot.docs.where((doc) => doc.data()['cached'] == true).length;
  double totalCost = snapshot.docs.fold(0.0, (sum, doc) => sum + doc.data()['cost_usd']);
  
  return {
    'total_items': totalItems,
    'cached_items': cachedItems,
    'cache_rate': cachedItems / totalItems,
    'total_cost_usd': totalCost,
  };
}
```

---

## Related Documentation

- **50-ai-output-storage-system.md** - Complete storage architecture
- **52-local-cache-implementation.md** - Local caching implementation
- **53-cloud-storage-integration.md** - Firebase integration
- **02-technology-stack.md** - Models and pricing
- **80-image-generation-sdk-change.md** - Image generation SDK notes

---

**Status:** ✅ Complete  
**Version:** 1.0  
**Last Updated:** October 2025


