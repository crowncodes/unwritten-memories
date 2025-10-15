# Firebase AI Logic Integration Guide for Unwritten

## Overview

**Firebase AI Logic** is Firebase's client SDK for building AI-powered mobile and web apps using Google's Gemini and Imagen models. It provides a simpler, direct alternative to setting up a separate backend service while still leveraging powerful AI capabilities.

**Source**: [Firebase AI Logic Documentation](https://firebase.google.com/docs/ai-logic/get-started?platform=web&authuser=0&_gl=1*v7itu3*_ga*MTYwNjExNTUxMy4xNzYwNDc3NDYw*_ga_CW55HF8NVT*czE3NjA0OTY2NDIkbzIkZzEkdDE3NjA1MDI4NDYkajUzJGwwJGgw&api=dev#add-sdk)

## Firebase AI Logic vs Genkit vs TFLite

Understanding when to use each approach is crucial for optimal architecture:

### Three Approaches Compared

| Feature | TFLite (On-Device) | Firebase AI Logic (Client SDK) | Genkit (Backend Service) |
|---------|-------------------|-------------------------------|-------------------------|
| **Location** | Device | Device → Cloud | Server → Cloud |
| **Latency** | < 15ms | 500-2000ms | 800-1500ms |
| **Network Required** | ❌ No | ✅ Yes | ✅ Yes |
| **API Key Exposure** | N/A | ⚠️ Client-side | ✅ Server-side (secure) |
| **Model Flexibility** | ❌ Fixed | ✅ Full Gemini API | ✅ Full API + custom flows |
| **Cost** | Free (device) | Per API call | Per API call |
| **Complexity** | Low | Low | Medium-High |
| **Use Case** | Fast inference | Quick AI features | Complex workflows |
| **App Size** | +5-10MB | +1MB | 0 (backend) |
| **Battery Impact** | Minimal | Minimal (network only) | Minimal (network only) |
| **Updates** | Requires app update | Auto (model updates) | Auto (backend updates) |
| **Caching** | Manual | Built-in (App Check) | Custom |
| **Abuse Prevention** | N/A | App Check | Custom auth |

### Decision Matrix for Unwritten

```
┌─────────────────────────────────────────────────────────────┐
│                    When to Use What?                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Fast, Fixed Inference (< 20ms):                           │
│  ✓ Personality traits                                      │
│  ✓ Sentiment analysis          → TFLite (On-Device)       │
│  ✓ Relationship scoring                                    │
│                                                             │
│  Quick AI Features (Prototype/MVP):                         │
│  ✓ Simple dialogue generation                              │
│  ✓ Card descriptions           → Firebase AI Logic         │
│  ✓ Image analysis              (Client SDK)                │
│  ✓ Quick prototyping                                       │
│                                                             │
│  Complex AI Workflows (Production):                         │
│  ✓ Multi-step dialogue                                     │
│  ✓ Story progression           → Genkit                    │
│  ✓ Tool calling                (Backend Service)           │
│  ✓ RAG with game state                                    │
│  ✓ Secure API keys                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## What is Firebase AI Logic?

Firebase AI Logic is a **client-side SDK** that allows you to call Gemini and Imagen models directly from your Flutter, iOS, Android, or web app without building a custom backend.

### Key Features

1. **Direct Model Access**: Call Gemini and Imagen models from client code
2. **Multimodal Support**: Text, images, video, audio, and PDFs
3. **Streaming**: Real-time response streaming
4. **Built-in Security**: App Check integration to prevent abuse
5. **Simple Setup**: Just a few lines of code to get started
6. **No Backend Required**: API calls go directly from client to Google AI
7. **Automatic Updates**: Models improve without app updates

### Supported Capabilities

- **Text Generation**: Generate text from text prompts
- **Chat**: Multi-turn conversations with context
- **Image Analysis**: Analyze images with Gemini Vision
- **Image Generation**: Generate images with Gemini or Imagen
- **Image Editing**: Edit images with Imagen
- **Video Analysis**: Analyze video content
- **Audio Analysis**: Process audio input
- **PDF Analysis**: Extract information from PDFs
- **Structured Output**: Generate JSON responses
- **Function Calling**: Connect to external tools
- **Code Execution**: Run code within prompts
- **Grounding**: Use Google Search for up-to-date info

## Architecture with Firebase AI Logic

### Option 1: Hybrid TFLite + Firebase AI Logic (Simpler)

```
┌────────────────────────────────────────────────────────────┐
│                Flutter App (Unwritten)                     │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  TFLite Service (On-Device)                          │ │
│  │  • Personality inference (< 15ms)                    │ │
│  │  • Sentiment analysis (< 10ms)                       │ │
│  │  • Relationship scoring                              │ │
│  └──────────────────────────────────────────────────────┘ │
│                              │                             │
│                              ▼                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Firebase AI Logic Service                           │ │
│  │  • Dialogue generation (800-1500ms)                  │ │
│  │  • Story narratives                                  │ │
│  │  • Image analysis (card art)                         │ │
│  └──────────────────────────────────────────────────────┘ │
│                              │                             │
└──────────────────────────────┼─────────────────────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │  Google Gemini API           │
                │  (via Firebase AI Logic)     │
                └──────────────────────────────┘
```

**Pros**:
- ✅ No backend to maintain
- ✅ Simple architecture
- ✅ Quick to implement
- ✅ Built-in abuse prevention (App Check)
- ✅ Automatic model updates

**Cons**:
- ⚠️ API keys in client app (use App Check!)
- ⚠️ Less control over requests
- ⚠️ Harder to implement complex workflows
- ⚠️ Direct costs per user request

### Option 2: Triple Hybrid (TFLite + Firebase AI Logic + Genkit)

```
┌────────────────────────────────────────────────────────────┐
│                Flutter App (Unwritten)                     │
│                                                            │
│  TFLite → Fast inference (personality, sentiment)          │
│      ↓                                                     │
│  Firebase AI Logic → Quick features (card descriptions)    │
│      ↓                                                     │
│  Genkit Backend → Complex workflows (story progression)    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Use Case**: Start with Firebase AI Logic for MVP, migrate complex features to Genkit for production.

## Installation & Setup

### Step 1: Prerequisites

Ensure you have:
- ✅ Firebase project created
- ✅ Blaze (pay-as-you-go) pricing plan
- ✅ Gemini API enabled
- ✅ Flutter app connected to Firebase

### Step 2: Enable Required APIs

In Google Cloud Console:
1. Enable **Generative Language API** (for Gemini)
2. Enable **Vertex AI API** (optional, for Vertex AI backend)

### Step 3: Add Flutter Dependencies

Update `app/pubspec.yaml`:

```yaml
dependencies:
  # ... existing dependencies
  firebase_core: ^3.11.0
  firebase_ai: ^0.1.0  # Firebase AI Logic SDK
```

Run:
```bash
cd app
flutter pub get
```

### Step 4: Initialize Firebase

If not already done, initialize Firebase in your app:

```dart
// lib/main.dart
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  
  runApp(MyApp());
}
```

### Step 5: Set Up App Check (Important!)

**Critical**: Firebase AI Logic exposes API calls from client. Use App Check to prevent abuse.

```dart
// lib/main.dart
import 'package:firebase_app_check/firebase_app_check.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  
  // Enable App Check to prevent API abuse
  await FirebaseAppCheck.instance.activate(
    androidProvider: AndroidProvider.playIntegrity,
    appleProvider: AppleProvider.appAttest,
    webProvider: ReCaptchaV3Provider('your-recaptcha-site-key'),
  );
  
  runApp(MyApp());
}
```

**Important**: See [App Check documentation](https://firebase.google.com/docs/app-check) for setup details.

## Basic Usage

### Text Generation

Create `lib/shared/services/firebase_ai_service.dart`:

```dart
import 'package:firebase_ai/firebase_ai.dart';
import '../utils/app_logger.dart';

/// Service for Firebase AI Logic integration.
/// 
/// Provides direct access to Gemini models for AI features
/// without requiring a separate backend service.
/// 
/// Performance:
/// - Average latency: 800-1500ms
/// - Requires network connection
/// - Uses App Check for abuse prevention
class FirebaseAIService {
  late final GenerativeModel _model;
  
  FirebaseAIService() {
    // Initialize with Google AI backend (uses Gemini Developer API)
    _model = FirebaseAI.googleAI().generativeModel(
      model: 'gemini-2.5-flash',
    );
  }
  
  /// Generates text from a prompt.
  /// 
  /// Example:
  /// ```dart
  /// final text = await service.generateText(
  ///   'Write a mysterious dialogue for a character'
  /// );
  /// ```
  Future<String> generateText(String prompt) async {
    final stopwatch = Stopwatch()..start();
    
    try {
      final content = [Content.text(prompt)];
      final response = await _model.generateContent(content);
      
      AppLogger.ai('Text generated', metrics: {
        'duration_ms': stopwatch.elapsedMilliseconds,
        'prompt_length': prompt.length,
      });
      
      return response.text ?? '';
    } catch (e, stack) {
      AppLogger.error('Text generation failed', e, stack);
      rethrow;
    }
  }
  
  /// Generates text with streaming for progressive display.
  /// 
  /// Example:
  /// ```dart
  /// await for (final chunk in service.generateTextStream(prompt)) {
  ///   print(chunk);
  /// }
  /// ```
  Stream<String> generateTextStream(String prompt) async* {
    try {
      final content = [Content.text(prompt)];
      final stream = _model.generateContentStream(content);
      
      await for (final chunk in stream) {
        if (chunk.text != null) {
          yield chunk.text!;
        }
      }
    } catch (e, stack) {
      AppLogger.error('Streaming text generation failed', e, stack);
      rethrow;
    }
  }
}
```

### Dialogue Generation with Firebase AI Logic

Create `lib/features/ai/data/services/firebase_dialogue_service.dart`:

```dart
import 'package:firebase_ai/firebase_ai.dart';
import '../../../../shared/utils/app_logger.dart';
import '../../domain/entities/dialogue_response.dart';

/// Generates dialogue using Firebase AI Logic.
/// 
/// Simpler alternative to Genkit backend for basic dialogue.
class FirebaseDialogueService {
  final GenerativeModel _model;
  
  FirebaseDialogueService()
      : _model = FirebaseAI.googleAI().generativeModel(
          model: 'gemini-2.5-flash',
        );
  
  /// Generates dialogue for card interaction.
  /// 
  /// Uses personality traits from TFLite to guide generation.
  Future<DialogueResponse> generateDialogue({
    required String cardId,
    required String context,
    required Map<String, double> personalityTraits,
    int previousInteractions = 0,
  }) async {
    final stopwatch = Stopwatch()..start();
    
    try {
      // Build personality description
      final personalityDesc = _buildPersonalityDescription(personalityTraits);
      
      // Build prompt
      final prompt = '''
You are generating dialogue for a character in Unwritten, a narrative card game.

CHARACTER PERSONALITY:
$personalityDesc

GAME CONTEXT:
$context

INTERACTION HISTORY:
${previousInteractions == 0 ? 'First meeting' : 'Met $previousInteractions times before'}

Generate authentic dialogue (1-3 sentences) that reflects the character's personality.
Also provide the character's emotion (e.g., curious, friendly, mysterious) and tone (e.g., warm, enigmatic).

Format as JSON:
{
  "text": "dialogue here",
  "emotion": "emotion here",
  "tone": "tone here"
}
''';

      // Configure model for JSON output
      final content = [Content.text(prompt)];
      final response = await _model.generateContent(
        content,
        generationConfig: GenerationConfig(
          temperature: 0.7,
          maxOutputTokens: 500,
          responseMimeType: 'application/json',
        ),
      );
      
      // Parse JSON response
      final jsonText = response.text ?? '{}';
      final data = jsonDecode(jsonText) as Map<String, dynamic>;
      
      AppLogger.ai('Dialogue generated', metrics: {
        'duration_ms': stopwatch.elapsedMilliseconds,
        'card_id': cardId,
        'interactions': previousInteractions,
      });
      
      return DialogueResponse(
        text: data['text'] as String? ?? 'Hello...',
        emotion: data['emotion'] as String? ?? 'neutral',
        tone: data['tone'] as String? ?? 'normal',
        suggestedResponses: [], // Not included in simple prompt
      );
    } catch (e, stack) {
      AppLogger.error('Firebase dialogue generation failed', e, stack);
      rethrow;
    }
  }
  
  String _buildPersonalityDescription(Map<String, double> traits) {
    final descriptions = <String>[];
    
    final openness = traits['openness'] ?? 0.5;
    if (openness > 0.7) {
      descriptions.add('creative and open to new experiences');
    } else if (openness < 0.3) {
      descriptions.add('conventional and traditional');
    }
    
    final extraversion = traits['extraversion'] ?? 0.5;
    if (extraversion > 0.7) {
      descriptions.add('outgoing and energetic');
    } else if (extraversion < 0.3) {
      descriptions.add('reserved and introspective');
    }
    
    return descriptions.join(', ');
  }
}
```

### Multi-Turn Chat

For conversations with context:

```dart
import 'package:firebase_ai/firebase_ai.dart';

/// Manages multi-turn conversations with characters.
class ChatService {
  final GenerativeModel _model;
  ChatSession? _currentSession;
  
  ChatService()
      : _model = FirebaseAI.googleAI().generativeModel(
          model: 'gemini-2.5-flash',
        );
  
  /// Starts a new chat session with system instructions.
  void startChat({
    required String characterPersonality,
    required String gameContext,
  }) {
    _currentSession = _model.startChat(
      systemInstruction: Content.system('''
You are roleplaying as a character in Unwritten, a narrative card game.

Your personality: $characterPersonality
Current context: $gameContext

Respond in character with 1-3 sentences. Be consistent with your personality.
'''),
    );
  }
  
  /// Sends a message in the current chat.
  Future<String> sendMessage(String message) async {
    if (_currentSession == null) {
      throw StateError('No active chat session. Call startChat() first.');
    }
    
    try {
      final response = await _currentSession!.sendMessage(
        Content.text(message),
      );
      
      return response.text ?? '';
    } catch (e, stack) {
      AppLogger.error('Chat message failed', e, stack);
      rethrow;
    }
  }
  
  /// Sends a message with streaming response.
  Stream<String> sendMessageStream(String message) async* {
    if (_currentSession == null) {
      throw StateError('No active chat session. Call startChat() first.');
    }
    
    try {
      final stream = _currentSession!.sendMessageStream(
        Content.text(message),
      );
      
      await for (final chunk in stream) {
        if (chunk.text != null) {
          yield chunk.text!;
        }
      }
    } catch (e, stack) {
      AppLogger.error('Chat stream failed', e, stack);
      rethrow;
    }
  }
  
  /// Ends the current chat session.
  void endChat() {
    _currentSession = null;
  }
}
```

### Image Analysis (Gemini Vision)

Analyze card artwork or player-uploaded images:

```dart
import 'package:firebase_ai/firebase_ai.dart';
import 'dart:io';

/// Analyzes images using Gemini Vision.
class ImageAnalysisService {
  final GenerativeModel _model;
  
  ImageAnalysisService()
      : _model = FirebaseAI.googleAI().generativeModel(
          model: 'gemini-2.0-flash-exp',  // Vision-capable model
        );
  
  /// Analyzes a card's artwork to describe personality.
  /// 
  /// Example use case: Let players upload custom card images.
  Future<String> analyzeCardArtwork(File imageFile) async {
    try {
      // Read image bytes
      final bytes = await imageFile.readAsBytes();
      
      // Create multimodal prompt
      final prompt = [
        Content.multi([
          DataPart('image/jpeg', bytes),
          TextPart('''
Analyze this character artwork and describe:
1. The character's apparent personality traits
2. Their emotional state
3. What kind of story role they might have

Keep it brief (2-3 sentences).
'''),
        ]),
      ];
      
      final response = await _model.generateContent(prompt);
      
      return response.text ?? 'Could not analyze image.';
    } catch (e, stack) {
      AppLogger.error('Image analysis failed', e, stack);
      rethrow;
    }
  }
  
  /// Analyzes multiple images (e.g., card collection).
  Future<List<String>> analyzeMultipleImages(
    List<File> images,
  ) async {
    final results = <String>[];
    
    for (final image in images) {
      try {
        final result = await analyzeCardArtwork(image);
        results.add(result);
      } catch (e) {
        results.add('Analysis failed for this image.');
      }
    }
    
    return results;
  }
}
```

### Function Calling

Connect Gemini to your game state:

```dart
import 'package:firebase_ai/firebase_ai.dart';

/// Service with function calling to access game state.
class AIGameService {
  final GenerativeModel _model;
  
  AIGameService()
      : _model = FirebaseAI.googleAI().generativeModel(
          model: 'gemini-2.5-flash',
          tools: [
            Tool(functionDeclarations: [
              // Define functions the AI can call
              FunctionDeclaration(
                name: 'get_card_data',
                description: 'Retrieves information about a specific card',
                parameters: Schema(
                  SchemaType.object,
                  properties: {
                    'card_id': Schema(
                      SchemaType.string,
                      description: 'The unique ID of the card',
                    ),
                  },
                  requiredProperties: ['card_id'],
                ),
              ),
              FunctionDeclaration(
                name: 'get_relationship_score',
                description: 'Gets the relationship score between player and card',
                parameters: Schema(
                  SchemaType.object,
                  properties: {
                    'player_id': Schema(SchemaType.string),
                    'card_id': Schema(SchemaType.string),
                  },
                  requiredProperties: ['player_id', 'card_id'],
                ),
              ),
            ]),
          ],
        );
  
  /// Generates context-aware dialogue using function calling.
  Future<String> generateContextAwareDialogue({
    required String playerId,
    required String cardId,
    required String situation,
  }) async {
    final prompt = '''
Generate dialogue for this situation: $situation

Use the available functions to check:
1. The card's data and personality
2. The current relationship between player and card

Then generate appropriate dialogue based on this information.
''';
    
    var response = await _model.generateContent([Content.text(prompt)]);
    
    // Handle function calls
    while (response.functionCalls.isNotEmpty) {
      final functionCall = response.functionCalls.first;
      final functionResponse = await _handleFunctionCall(
        functionCall,
        playerId: playerId,
        cardId: cardId,
      );
      
      // Send function result back to model
      response = await _model.generateContent([
        Content.model([
          ...response.candidates.first.content.parts,
        ]),
        Content.functionResponse(
          functionCall.name,
          functionResponse,
        ),
      ]);
    }
    
    return response.text ?? '';
  }
  
  Future<Map<String, Object?>> _handleFunctionCall(
    FunctionCall call, {
    required String playerId,
    required String cardId,
  }) async {
    switch (call.name) {
      case 'get_card_data':
        final id = call.args['card_id'] as String;
        final card = await _getCardFromDatabase(id);
        return {
          'name': card.name,
          'personality': card.personalityTraits,
          'backstory': card.backstory,
        };
        
      case 'get_relationship_score':
        final pId = call.args['player_id'] as String;
        final cId = call.args['card_id'] as String;
        final relationship = await _getRelationship(pId, cId);
        return {
          'score': relationship.score,
          'level': relationship.level,
          'interactions': relationship.totalInteractions,
        };
        
      default:
        return {'error': 'Unknown function'};
    }
  }
  
  // Mock implementations - replace with real database calls
  Future<CardData> _getCardFromDatabase(String id) async {
    // TODO: Implement actual database query
    throw UnimplementedError();
  }
  
  Future<RelationshipData> _getRelationship(String playerId, String cardId) async {
    // TODO: Implement actual relationship query
    throw UnimplementedError();
  }
}
```

## Integration Patterns

### Pattern 1: Progressive Enhancement (Start Simple)

```dart
/// AIRepository that starts with Firebase AI Logic, 
/// can migrate to Genkit later.
class AIRepositoryImpl implements AIRepository {
  final AIService _tfliteService;
  final FirebaseDialogueService _firebaseAI;
  final CacheService _cache;
  
  @override
  Future<DialogueResponse> generateDialogue({
    required Card card,
    required GameContext context,
  }) async {
    // 1. Fast personality inference (TFLite - on device)
    final personality = await _tfliteService.inferPersonality(card);
    
    // 2. Check cache
    final cached = await _cache.get('dialogue_${card.id}');
    if (cached != null) {
      return cached;
    }
    
    // 3. Generate with Firebase AI Logic (simple, no backend)
    try {
      final response = await _firebaseAI.generateDialogue(
        cardId: card.id,
        context: context.description,
        personalityTraits: personality.toMap(),
      );
      
      // Cache result
      await _cache.set('dialogue_${card.id}', response);
      
      return response;
    } catch (e) {
      // Fallback to rule-based
      return _generateFallbackDialogue(card, personality);
    }
  }
}
```

**Migration Path**:
1. **Week 1-4**: Implement with Firebase AI Logic
2. **Week 5-8**: Prototype works, gather feedback
3. **Week 9+**: If needed, migrate complex features to Genkit backend

### Pattern 2: Feature Flag (A/B Testing)

```dart
/// Toggle between Firebase AI Logic and Genkit based on feature flag.
class AIRepositoryImpl implements AIRepository {
  final FirebaseDialogueService _firebaseAI;
  final GenkitService _genkit;
  final FeatureFlagService _flags;
  
  @override
  Future<DialogueResponse> generateDialogue({
    required Card card,
    required GameContext context,
  }) async {
    final useGenkit = await _flags.isEnabled('use_genkit_backend');
    
    if (useGenkit) {
      // Use Genkit for more complex workflows
      return await _genkit.generateDialogue(
        cardId: card.id,
        context: context.description,
        personalityTraits: {},
      );
    } else {
      // Use Firebase AI Logic for simpler approach
      return await _firebaseAI.generateDialogue(
        cardId: card.id,
        context: context.description,
        personalityTraits: {},
      );
    }
  }
}
```

### Pattern 3: Hybrid by Complexity

```dart
/// Use Firebase AI Logic for simple features, 
/// Genkit for complex workflows.
class AIRepositoryImpl implements AIRepository {
  final FirebaseDialogueService _firebaseAI;
  final GenkitService _genkit;
  
  @override
  Future<DialogueResponse> generateSimpleDialogue(Card card) async {
    // Simple greeting: use Firebase AI Logic (faster to implement)
    return await _firebaseAI.generateDialogue(
      cardId: card.id,
      context: 'Casual greeting',
      personalityTraits: {},
    );
  }
  
  @override
  Future<StoryResponse> generateStoryProgression({
    required List<Card> activeCards,
    required GameState state,
    required List<PlayerChoice> recentChoices,
  }) async {
    // Complex story: use Genkit backend (better control, RAG, tools)
    return await _genkit.generateStoryProgression(
      cards: activeCards,
      gameState: state,
      choices: recentChoices,
    );
  }
}
```

## Security Best Practices

### 1. Always Use App Check

**Critical**: Firebase AI Logic makes API calls from the client. Use App Check to prevent abuse.

```dart
// main.dart
await FirebaseAppCheck.instance.activate(
  androidProvider: AndroidProvider.playIntegrity,
  appleProvider: AppleProvider.appAttest,
  webProvider: ReCaptchaV3Provider('your-site-key'),
);
```

**Why This Matters**:
- Without App Check: Anyone can call your Firebase AI Logic endpoints
- With App Check: Only verified app instances can make calls
- Protects against: API key theft, quota exhaustion, abuse

### 2. Set Up Budget Alerts

In Google Cloud Console:
1. Go to **Billing** > **Budgets & alerts**
2. Create budget alert for Gemini API
3. Set threshold (e.g., $50/month)
4. Enable notifications

### 3. Implement Rate Limiting

```dart
/// Rate limiter for Firebase AI Logic calls.
class RateLimitedAIService {
  final FirebaseDialogueService _service;
  final Map<String, DateTime> _lastCallTime = {};
  final Duration _minInterval = Duration(seconds: 2);
  
  Future<DialogueResponse> generateDialogue({
    required String cardId,
    required String context,
    required Map<String, double> personalityTraits,
  }) async {
    final now = DateTime.now();
    final lastCall = _lastCallTime[cardId];
    
    // Enforce minimum interval between calls for same card
    if (lastCall != null) {
      final elapsed = now.difference(lastCall);
      if (elapsed < _minInterval) {
        throw RateLimitException(
          'Please wait ${_minInterval.inSeconds - elapsed.inSeconds} seconds',
        );
      }
    }
    
    _lastCallTime[cardId] = now;
    
    return await _service.generateDialogue(
      cardId: cardId,
      context: context,
      personalityTraits: personalityTraits,
    );
  }
}
```

### 4. Don't Expose Sensitive Data in Prompts

```dart
// ❌ BAD - Exposes user email
final prompt = 'Generate dialogue for user ${user.email}';

// ✅ GOOD - Only sends game-relevant data
final prompt = 'Generate dialogue for card interaction #${interaction.id}';
```

## Performance Optimization

### 1. Caching Strategy

```dart
/// Multi-tier caching for Firebase AI Logic responses.
class CachedFirebaseAIService {
  final FirebaseDialogueService _service;
  final MemoryCache _memory = MemoryCache(maxSize: 50);
  final HiveCache _disk;
  
  Future<DialogueResponse> generateDialogue({
    required String cardId,
    required String context,
    required Map<String, double> traits,
  }) async {
    final key = _buildKey(cardId, context, traits);
    
    // Try memory cache
    var cached = _memory.get(key);
    if (cached != null) return cached;
    
    // Try disk cache
    cached = await _disk.get(key);
    if (cached != null) {
      _memory.set(key, cached);
      return cached;
    }
    
    // Generate new
    final response = await _service.generateDialogue(
      cardId: cardId,
      context: context,
      personalityTraits: traits,
    );
    
    // Cache at both levels
    _memory.set(key, response);
    await _disk.set(key, response, ttl: Duration(hours: 24));
    
    return response;
  }
  
  String _buildKey(String cardId, String context, Map<String, double> traits) {
    return '$cardId:${context.hashCode}:${traits.hashCode}';
  }
}
```

### 2. Streaming for Better UX

```dart
/// Shows partial responses as they stream in.
class StreamingDialogueWidget extends StatefulWidget {
  final String cardId;
  
  const StreamingDialogueWidget({required this.cardId});
  
  @override
  State<StreamingDialogueWidget> createState() => _State();
}

class _State extends State<StreamingDialogueWidget> {
  final _buffer = StringBuffer();
  
  @override
  Widget build(BuildContext context) {
    return StreamBuilder<String>(
      stream: _generateDialogueStream(),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          _buffer.write(snapshot.data);
        }
        
        return Text(
          _buffer.toString(),
          style: TextStyle(fontSize: 16),
        );
      },
    );
  }
  
  Stream<String> _generateDialogueStream() {
    final service = FirebaseDialogueService();
    return service.generateTextStream(
      'Generate mysterious dialogue for ${widget.cardId}',
    );
  }
}
```

### 3. Request Coalescing

```dart
/// Prevents duplicate requests for the same dialogue.
class CoalescedAIService {
  final Map<String, Future<DialogueResponse>> _pending = {};
  
  Future<DialogueResponse> generateDialogue({
    required String cardId,
    required String context,
  }) async {
    final key = '$cardId:$context';
    
    // If request already in flight, return existing future
    if (_pending.containsKey(key)) {
      AppLogger.performance('Coalesced duplicate request', Duration.zero);
      return _pending[key]!;
    }
    
    // Create new request
    final future = _actuallyGenerateDialogue(cardId, context);
    _pending[key] = future;
    
    try {
      return await future;
    } finally {
      _pending.remove(key);
    }
  }
  
  Future<DialogueResponse> _actuallyGenerateDialogue(
    String cardId,
    String context,
  ) async {
    // Actual implementation
    throw UnimplementedError();
  }
}
```

## Cost Management

### Cost Comparison

**Firebase AI Logic** (direct from client):
- Uses same Gemini API pricing
- No server costs
- Potential for higher usage (direct access)

**Genkit Backend**:
- Same Gemini API pricing
- Server costs (Cloud Run)
- Better control over usage

**Cost Per 1,000 Dialogues** (Gemini 2.5 Flash):

| Item | Firebase AI Logic | Genkit Backend |
|------|------------------|----------------|
| Gemini API calls | $0.07 | $0.07 |
| Server costs | $0 | $0.10 |
| **Total** | **$0.07** | **$0.17** |

**However**:
- Firebase AI Logic may have higher usage (easier to call)
- Genkit can implement server-side caching, batching
- With optimization, Genkit can be cheaper at scale

### Cost Optimization

```dart
/// Implements smart caching to reduce API calls.
class CostOptimizedAIService {
  final FirebaseDialogueService _service;
  final CacheService _cache;
  final int maxCallsPerUserPerHour = 50;
  
  Future<DialogueResponse> generateDialogue({
    required String userId,
    required String cardId,
    required String context,
  }) async {
    // 1. Check if user exceeded quota
    final userCalls = await _getUserCallCount(userId);
    if (userCalls >= maxCallsPerUserPerHour) {
      // Return cached or fallback instead
      return await _getCachedOrFallback(cardId, context);
    }
    
    // 2. Check cache first (80% hit rate = 80% cost savings)
    final cached = await _cache.get('$cardId:$context');
    if (cached != null) {
      return cached;
    }
    
    // 3. Generate and cache
    final response = await _service.generateDialogue(
      cardId: cardId,
      context: context,
      personalityTraits: {},
    );
    
    // Cache for 24 hours
    await _cache.set(
      '$cardId:$context',
      response,
      ttl: Duration(hours: 24),
    );
    
    // Increment user's call count
    await _incrementUserCallCount(userId);
    
    return response;
  }
  
  Future<int> _getUserCallCount(String userId) async {
    // TODO: Implement with Firestore or local storage
    throw UnimplementedError();
  }
  
  Future<void> _incrementUserCallCount(String userId) async {
    // TODO: Implement
    throw UnimplementedError();
  }
  
  Future<DialogueResponse> _getCachedOrFallback(
    String cardId,
    String context,
  ) async {
    // TODO: Implement
    throw UnimplementedError();
  }
}
```

## Monitoring & Analytics

### Track API Usage

```dart
/// Tracks Firebase AI Logic usage metrics.
class AIAnalytics {
  static void trackGeneration({
    required String featureType,
    required Duration duration,
    required bool fromCache,
    required int tokensUsed,
  }) {
    FirebaseAnalytics.instance.logEvent(
      name: 'ai_generation',
      parameters: {
        'feature_type': featureType,
        'duration_ms': duration.inMilliseconds,
        'from_cache': fromCache,
        'tokens_used': tokensUsed,
        'timestamp': DateTime.now().toIso8601String(),
      },
    );
    
    // Log to Cloud Monitoring for cost tracking
    if (!fromCache) {
      _logApiCall(featureType, tokensUsed);
    }
  }
  
  static void _logApiCall(String featureType, int tokens) {
    // Estimate cost (Gemini 2.5 Flash pricing)
    final inputCost = (tokens * 0.075) / 1000000;  // $0.075 per 1M tokens
    final outputCost = (tokens * 0.30) / 1000000;   // $0.30 per 1M tokens
    final totalCost = inputCost + outputCost;
    
    AppLogger.info('API call cost estimate', data: {
      'feature': featureType,
      'tokens': tokens,
      'cost_usd': totalCost,
    });
  }
}
```

### Monitor Costs in Firebase Console

1. Go to **Firebase Console** > **Usage and billing**
2. View Gemini API usage
3. Set up budget alerts

## Testing

### Unit Tests

```dart
// test/services/firebase_ai_service_test.dart

void main() {
  group('FirebaseAIService', () {
    late FirebaseAIService service;
    
    setUp(() {
      service = FirebaseAIService();
    });
    
    test('generates text from prompt', () async {
      final result = await service.generateText('Hello');
      
      expect(result, isNotEmpty);
    });
    
    test('handles errors gracefully', () async {
      // Test with invalid input
      expect(
        () => service.generateText(''),
        throwsA(isA<Exception>()),
      );
    });
  });
}
```

### Integration Tests

```dart
// integration_test/firebase_ai_test.dart

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  
  testWidgets('generates dialogue end-to-end', (tester) async {
    await tester.pumpWidget(MyApp());
    
    // Navigate to card interaction
    await tester.tap(find.byType(CardWidget).first);
    await tester.pumpAndSettle();
    
    // Tap generate dialogue button
    await tester.tap(find.text('Generate Dialogue'));
    
    // Wait for response (with timeout)
    await tester.pumpAndSettle(timeout: Duration(seconds: 5));
    
    // Verify dialogue appears
    expect(find.byType(DialogueText), findsOneWidget);
  });
}
```

## Migration from Google AI Client SDK

If you're currently using `google_generative_ai` package:

### Before (Google AI Client SDK)

```dart
import 'package:google_generative_ai/google_generative_ai.dart';

final model = GenerativeModel(
  model: 'gemini-2.5-flash',
  apiKey: 'YOUR_API_KEY',  // ⚠️ Exposed in client!
);

final response = await model.generateContent([
  Content.text('Generate dialogue')
]);
```

### After (Firebase AI Logic)

```dart
import 'package:firebase_ai/firebase_ai.dart';

// No API key in code! Uses Firebase App Check
final model = FirebaseAI.googleAI().generativeModel(
  model: 'gemini-2.5-flash',
);

final response = await model.generateContent([
  Content.text('Generate dialogue')
]);
```

**Benefits**:
- ✅ No API key in client code
- ✅ Built-in App Check integration
- ✅ Automatic abuse prevention
- ✅ Usage tracking in Firebase Console

## Recommendations for Unwritten

### MVP Phase (Weeks 1-8): Firebase AI Logic Only

**Recommended Approach**:
```
TFLite (on-device) + Firebase AI Logic (client SDK)
```

**Why**:
- ✅ Fastest to implement
- ✅ No backend to build/maintain
- ✅ Built-in security with App Check
- ✅ Perfect for prototyping and MVP

**Implement**:
1. Personality inference → TFLite
2. Simple dialogues → Firebase AI Logic
3. Card descriptions → Firebase AI Logic
4. Image analysis → Firebase AI Logic (Gemini Vision)

### Growth Phase (Weeks 9-16): Add Genkit Backend

**When to migrate to Genkit**:
- API costs > $50/month (better control needed)
- Need complex multi-step workflows
- Want RAG for story consistency
- Need server-side caching
- Require tool calling with sensitive data

**Hybrid Approach**:
```
TFLite (personality) 
  → Firebase AI Logic (simple features)
  → Genkit Backend (complex workflows)
```

### Production Phase (Week 17+): Optimize

**Final Architecture**:
- **TFLite**: All fast inference (< 20ms)
- **Firebase AI Logic**: Player-facing simple features
- **Genkit Backend**: Complex workflows, admin tools, analytics

## Comparison Summary

### Firebase AI Logic

**Best For**:
- ✅ Quick prototypes and MVPs
- ✅ Simple AI features
- ✅ Small teams without backend expertise
- ✅ Apps with low API usage

**Not Ideal For**:
- ❌ Complex multi-step workflows
- ❌ High-volume production apps (costly)
- ❌ Features requiring server-side logic
- ❌ RAG with large context

### Genkit Backend

**Best For**:
- ✅ Production apps with scale
- ✅ Complex AI workflows
- ✅ Features requiring tool calling
- ✅ Apps needing server-side caching
- ✅ Teams with backend resources

**Not Ideal For**:
- ❌ Quick prototypes (overhead)
- ❌ Very simple use cases
- ❌ Teams without backend expertise

### Recommended Strategy

```
Start → Firebase AI Logic (Weeks 1-8)
         ↓ If successful
      Hybrid (Weeks 9-16)
         ↓ At scale
      Mostly Genkit + Firebase AI Logic for client features
```

## Related Documentation

- [Genkit Integration Guide](./genkit_integration_guide.md) - Full backend approach
- [Genkit Quick Reference](./genkit_quick_reference.md) - Genkit cheat sheet
- [Genkit Architecture](../5.architecture/genkit_architecture.md) - Architecture decisions
- [TensorFlow Lite Integration](./tensorflow_lite_integration.md) - On-device inference
- [Firebase AI Logic Official Docs](https://firebase.google.com/docs/ai-logic/get-started)

## External Resources

- [Firebase AI Logic Documentation](https://firebase.google.com/docs/ai-logic)
- [Gemini API Models](https://ai.google.dev/models/gemini)
- [Firebase App Check](https://firebase.google.com/docs/app-check)
- [Google AI Studio](https://aistudio.google.com)

---

**Document Version**: 1.0  
**Last Updated**: October 15, 2025  
**Maintainer**: Unwritten AI Team

