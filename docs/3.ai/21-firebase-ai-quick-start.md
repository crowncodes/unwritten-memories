# Firebase AI Flutter Quick Start Guide

## Overview

This is a practical quick start guide for using the `firebase_ai` Flutter package (version 3.4.0+) in the Unwritten project.

**Official Resources**:
- [Package Documentation](https://pub.dev/documentation/firebase_ai/latest/)
- [pub.dev Package](https://pub.dev/packages/firebase_ai)
- [Firebase AI Logic Documentation](https://firebase.google.com/docs/ai-logic)

## Installation

### 1. Add Dependency

Update `app/pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # Firebase
  firebase_core: ^3.11.0
  firebase_ai: ^3.4.0  # Latest version
  firebase_app_check: ^0.3.0  # Critical for security!
```

Run:
```bash
cd app
flutter pub get
```

### 2. Initialize Firebase

If not already done, initialize Firebase in `lib/main.dart`:

```dart
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_app_check/firebase_app_check.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  
  // CRITICAL: Enable App Check to prevent API abuse
  await FirebaseAppCheck.instance.activate(
    androidProvider: AndroidProvider.playIntegrity,
    appleProvider: AppleProvider.appAttest,
    webProvider: ReCaptchaV3Provider('your-recaptcha-site-key'),
  );
  
  runApp(const MyApp());
}
```

⚠️ **Important**: Always enable App Check before deploying to production!

## Basic Usage

### Simple Text Generation

```dart
import 'package:firebase_ai/firebase_ai.dart';

class SimpleAIExample extends StatelessWidget {
  Future<String> generateText() async {
    // Create a model instance
    final model = FirebaseAI.googleAI().generativeModel(
      model: 'gemini-2.5-flash',
    );
    
    // Generate content
    final prompt = [Content.text('Write a short greeting for a mysterious character')];
    final response = await model.generateContent(prompt);
    
    return response.text ?? 'No response generated';
  }
  
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<String>(
      future: generateText(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return CircularProgressIndicator();
        }
        
        if (snapshot.hasError) {
          return Text('Error: ${snapshot.error}');
        }
        
        return Text(snapshot.data ?? 'No data');
      },
    );
  }
}
```

### Streaming Text Generation

For better UX, stream responses as they're generated:

```dart
import 'package:firebase_ai/firebase_ai.dart';

class StreamingAIExample extends StatefulWidget {
  @override
  State<StreamingAIExample> createState() => _StreamingAIExampleState();
}

class _StreamingAIExampleState extends State<StreamingAIExample> {
  final _buffer = StringBuffer();
  bool _isGenerating = false;
  
  Future<void> _generateStreaming() async {
    setState(() {
      _isGenerating = true;
      _buffer.clear();
    });
    
    try {
      final model = FirebaseAI.googleAI().generativeModel(
        model: 'gemini-2.5-flash',
      );
      
      final prompt = [Content.text('Tell me a short story about a magic card')];
      final stream = model.generateContentStream(prompt);
      
      await for (final chunk in stream) {
        if (chunk.text != null) {
          setState(() {
            _buffer.write(chunk.text);
          });
        }
      }
    } catch (e) {
      // Handle error
      print('Error: $e');
    } finally {
      setState(() {
        _isGenerating = false;
      });
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ElevatedButton(
          onPressed: _isGenerating ? null : _generateStreaming,
          child: Text('Generate Story'),
        ),
        SizedBox(height: 16),
        Text(_buffer.toString()),
        if (_isGenerating) LinearProgressIndicator(),
      ],
    );
  }
}
```

## Service Pattern for Unwritten

### Create a Reusable Service

Create `lib/shared/services/firebase_ai_service.dart`:

```dart
import 'package:firebase_ai/firebase_ai.dart';

/// Service for Firebase AI Logic integration.
/// 
/// Provides dialogue generation, image analysis, and other AI features
/// using Google's Gemini models directly from the Flutter app.
class FirebaseAIService {
  late final GenerativeModel _textModel;
  late final GenerativeModel _visionModel;
  
  FirebaseAIService() {
    // Initialize models
    _textModel = FirebaseAI.googleAI().generativeModel(
      model: 'gemini-2.5-flash',
    );
    
    _visionModel = FirebaseAI.googleAI().generativeModel(
      model: 'gemini-2.0-flash-exp',  // Vision-capable model
    );
  }
  
  /// Generates dialogue for a card interaction.
  Future<String> generateDialogue({
    required String cardName,
    required String context,
    required Map<String, double> personalityTraits,
  }) async {
    final prompt = _buildDialoguePrompt(cardName, context, personalityTraits);
    
    try {
      final content = [Content.text(prompt)];
      final response = await _textModel.generateContent(content);
      
      return response.text ?? 'Hello...';
    } catch (e) {
      print('Error generating dialogue: $e');
      return _getFallbackDialogue(cardName);
    }
  }
  
  /// Generates dialogue with streaming for progressive display.
  Stream<String> generateDialogueStream({
    required String cardName,
    required String context,
  }) async* {
    final prompt = _buildDialoguePrompt(cardName, context, {});
    
    try {
      final content = [Content.text(prompt)];
      final stream = _textModel.generateContentStream(content);
      
      await for (final chunk in stream) {
        if (chunk.text != null) {
          yield chunk.text!;
        }
      }
    } catch (e) {
      print('Error streaming dialogue: $e');
      yield _getFallbackDialogue(cardName);
    }
  }
  
  /// Analyzes an image (e.g., card artwork).
  Future<String> analyzeImage(Uint8List imageBytes) async {
    try {
      final prompt = [
        Content.multi([
          DataPart('image/jpeg', imageBytes),
          TextPart('Describe this character\'s personality based on their appearance.'),
        ]),
      ];
      
      final response = await _visionModel.generateContent(prompt);
      return response.text ?? 'Could not analyze image';
    } catch (e) {
      print('Error analyzing image: $e');
      return 'Image analysis unavailable';
    }
  }
  
  String _buildDialoguePrompt(
    String cardName,
    String context,
    Map<String, double> traits,
  ) {
    return '''
You are generating dialogue for a character named "$cardName" in a narrative card game.

Context: $context

Generate a short, engaging dialogue (1-2 sentences) that fits the character and situation.
''';
  }
  
  String _getFallbackDialogue(String cardName) {
    return 'Hello, traveler. I am $cardName.';
  }
}
```

### Use with Riverpod Provider

If using Riverpod for state management:

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Provider for the service
final firebaseAIServiceProvider = Provider<FirebaseAIService>((ref) {
  return FirebaseAIService();
});

// Provider for dialogue generation
final dialogueProvider = FutureProvider.family<String, DialogueRequest>(
  (ref, request) async {
    final service = ref.read(firebaseAIServiceProvider);
    return await service.generateDialogue(
      cardName: request.cardName,
      context: request.context,
      personalityTraits: request.traits,
    );
  },
);

// Usage in widget
class DialogueWidget extends ConsumerWidget {
  final DialogueRequest request;
  
  const DialogueWidget({required this.request});
  
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final dialogue = ref.watch(dialogueProvider(request));
    
    return dialogue.when(
      data: (text) => Text(text),
      loading: () => CircularProgressIndicator(),
      error: (error, stack) => Text('Error: $error'),
    );
  }
}
```

## Chat Conversations

For multi-turn conversations:

```dart
class ChatService {
  late final ChatSession _session;
  
  void startChat({required String characterPersonality}) {
    final model = FirebaseAI.googleAI().generativeModel(
      model: 'gemini-2.5-flash',
    );
    
    _session = model.startChat(
      systemInstruction: Content.system('''
You are roleplaying as a character with this personality: $characterPersonality

Respond in character with 1-2 sentences. Be consistent with your personality.
'''),
    );
  }
  
  Future<String> sendMessage(String message) async {
    try {
      final response = await _session.sendMessage(
        Content.text(message),
      );
      return response.text ?? '';
    } catch (e) {
      print('Error sending message: $e');
      return 'I don\'t know what to say...';
    }
  }
  
  Stream<String> sendMessageStream(String message) async* {
    try {
      final stream = _session.sendMessageStream(
        Content.text(message),
      );
      
      await for (final chunk in stream) {
        if (chunk.text != null) {
          yield chunk.text!;
        }
      }
    } catch (e) {
      print('Error streaming message: $e');
      yield 'I don\'t know what to say...';
    }
  }
}
```

## Configuration Options

### Generation Config

Customize model behavior:

```dart
final model = FirebaseAI.googleAI().generativeModel(
  model: 'gemini-2.5-flash',
);

final response = await model.generateContent(
  [Content.text('Generate dialogue')],
  generationConfig: GenerationConfig(
    temperature: 0.7,        // Creativity (0.0-1.0)
    maxOutputTokens: 500,    // Max response length
    topK: 40,                // Sampling parameter
    topP: 0.95,              // Sampling parameter
    stopSequences: ['\n\n'], // Stop generation at these
    responseMimeType: 'application/json', // For structured output
  ),
);
```

### Safety Settings

Control content filtering:

```dart
final response = await model.generateContent(
  [Content.text('Generate dialogue')],
  safetySettings: [
    SafetySetting(
      category: HarmCategory.harassment,
      threshold: HarmBlockThreshold.medium,
    ),
    SafetySetting(
      category: HarmCategory.hateSpeech,
      threshold: HarmBlockThreshold.medium,
    ),
  ],
);
```

## Error Handling

### Robust Error Handling

```dart
class RobustFirebaseAIService {
  Future<String> generateDialogue(String prompt) async {
    final model = FirebaseAI.googleAI().generativeModel(
      model: 'gemini-2.5-flash',
    );
    
    try {
      final response = await model.generateContent([Content.text(prompt)])
        .timeout(
          Duration(seconds: 30),
          onTimeout: () => throw TimeoutException('Generation timeout'),
        );
      
      if (response.text == null || response.text!.isEmpty) {
        throw Exception('Empty response from model');
      }
      
      return response.text!;
      
    } on TimeoutException catch (e) {
      print('Timeout: $e');
      return _getFallbackDialogue();
      
    } on SocketException catch (e) {
      print('Network error: $e');
      return _getCachedDialogue() ?? _getFallbackDialogue();
      
    } on FormatException catch (e) {
      print('Invalid response format: $e');
      return _getFallbackDialogue();
      
    } catch (e) {
      print('Unexpected error: $e');
      return _getFallbackDialogue();
    }
  }
  
  String _getFallbackDialogue() {
    return 'Hello, traveler...';
  }
  
  String? _getCachedDialogue() {
    // TODO: Implement cache lookup
    return null;
  }
}
```

## Performance Best Practices

### 1. Caching

```dart
class CachedFirebaseAIService {
  final _cache = <String, String>{};
  
  Future<String> generateDialogue(String cardId, String context) async {
    final key = '$cardId:${context.hashCode}';
    
    // Check cache
    if (_cache.containsKey(key)) {
      return _cache[key]!;
    }
    
    // Generate
    final response = await _generateDialogue(cardId, context);
    
    // Cache result
    _cache[key] = response;
    
    return response;
  }
  
  Future<String> _generateDialogue(String cardId, String context) async {
    // Actual generation logic
    throw UnimplementedError();
  }
}
```

### 2. Request Coalescing

```dart
class CoalescedAIService {
  final _pending = <String, Future<String>>{};
  
  Future<String> generateDialogue(String prompt) async {
    // If already generating this prompt, return existing future
    if (_pending.containsKey(prompt)) {
      return _pending[prompt]!;
    }
    
    // Create new request
    final future = _actuallyGenerate(prompt);
    _pending[prompt] = future;
    
    try {
      return await future;
    } finally {
      _pending.remove(prompt);
    }
  }
  
  Future<String> _actuallyGenerate(String prompt) async {
    // Actual generation
    throw UnimplementedError();
  }
}
```

### 3. Progressive Enhancement

Show cached/simple content first, then update with AI:

```dart
class ProgressiveAIWidget extends StatefulWidget {
  final String cardId;
  
  const ProgressiveAIWidget({required this.cardId});
  
  @override
  State<ProgressiveAIWidget> createState() => _ProgressiveAIWidgetState();
}

class _ProgressiveAIWidgetState extends State<ProgressiveAIWidget> {
  String _dialogue = 'Loading...';
  
  @override
  void initState() {
    super.initState();
    _loadDialogue();
  }
  
  Future<void> _loadDialogue() async {
    // 1. Show cached immediately
    final cached = await _getCached(widget.cardId);
    if (cached != null) {
      setState(() => _dialogue = cached);
    }
    
    // 2. Generate fresh in background
    final fresh = await _generateFresh(widget.cardId);
    setState(() => _dialogue = fresh);
    
    // 3. Update cache
    await _updateCache(widget.cardId, fresh);
  }
  
  Future<String?> _getCached(String cardId) async {
    // TODO: Implement
    return null;
  }
  
  Future<String> _generateFresh(String cardId) async {
    // TODO: Implement
    return 'Fresh dialogue...';
  }
  
  Future<void> _updateCache(String cardId, String dialogue) async {
    // TODO: Implement
  }
  
  @override
  Widget build(BuildContext context) {
    return Text(_dialogue);
  }
}
```

## Testing

### Unit Tests

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';

void main() {
  group('FirebaseAIService', () {
    late FirebaseAIService service;
    
    setUp(() {
      service = FirebaseAIService();
    });
    
    test('generates dialogue', () async {
      final result = await service.generateDialogue(
        cardName: 'Test Character',
        context: 'Test context',
        personalityTraits: {},
      );
      
      expect(result, isNotEmpty);
    });
    
    test('handles errors gracefully', () async {
      // Test error handling
      final result = await service.generateDialogue(
        cardName: '',
        context: '',
        personalityTraits: {},
      );
      
      expect(result, isNotEmpty); // Should return fallback
    });
  });
}
```

### Widget Tests

```dart
testWidgets('displays generated dialogue', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: DialogueWidget(
        request: DialogueRequest(
          cardName: 'Test',
          context: 'Test context',
        ),
      ),
    ),
  );
  
  // Should show loading indicator
  expect(find.byType(CircularProgressIndicator), findsOneWidget);
  
  // Wait for generation
  await tester.pumpAndSettle(Duration(seconds: 3));
  
  // Should show dialogue
  expect(find.byType(Text), findsOneWidget);
});
```

## Common Issues & Solutions

### Issue 1: App Check Not Configured

**Error**: "App Check verification failed"

**Solution**:
```dart
// Ensure App Check is activated before any AI calls
await FirebaseAppCheck.instance.activate(
  androidProvider: AndroidProvider.playIntegrity,
  appleProvider: AppleProvider.appAttest,
);
```

### Issue 2: Response is null

**Error**: `response.text` returns null

**Solution**:
```dart
final response = await model.generateContent(prompt);
final text = response.text ?? 'Default fallback text';
```

### Issue 3: Quota Exceeded

**Error**: "Quota exceeded for quota metric..."

**Solution**:
- Enable App Check to prevent abuse
- Implement rate limiting
- Cache aggressively
- Set budget alerts in Google Cloud Console

### Issue 4: Slow Response Times

**Problem**: Takes > 3 seconds to generate

**Solution**:
```dart
// Use streaming for better UX
final stream = model.generateContentStream(prompt);
await for (final chunk in stream) {
  // Display partial response immediately
  updateUI(chunk.text);
}
```

## Production Checklist

Before deploying:

- [ ] App Check enabled and configured
- [ ] Error handling implemented
- [ ] Fallback dialogue system in place
- [ ] Caching implemented (memory + disk)
- [ ] Request timeout configured (30s)
- [ ] Budget alerts set in Google Cloud Console
- [ ] Rate limiting implemented (per user)
- [ ] Analytics tracking added
- [ ] Integration tests passing
- [ ] Tested on real devices (Android + iOS)

## Cost Monitoring

### Track Usage

```dart
class MonitoredFirebaseAIService {
  final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;
  
  Future<String> generateDialogue(String prompt) async {
    final stopwatch = Stopwatch()..start();
    
    try {
      final model = FirebaseAI.googleAI().generativeModel(
        model: 'gemini-2.5-flash',
      );
      
      final response = await model.generateContent([Content.text(prompt)]);
      
      // Log success
      await _analytics.logEvent(
        name: 'ai_generation_success',
        parameters: {
          'duration_ms': stopwatch.elapsedMilliseconds,
          'prompt_length': prompt.length,
          'response_length': response.text?.length ?? 0,
          'model': 'gemini-2.5-flash',
        },
      );
      
      return response.text ?? '';
      
    } catch (e) {
      // Log failure
      await _analytics.logEvent(
        name: 'ai_generation_failure',
        parameters: {
          'duration_ms': stopwatch.elapsedMilliseconds,
          'error': e.toString(),
        },
      );
      
      rethrow;
    }
  }
}
```

## Next Steps

1. **Read**: [Firebase AI Logic Integration Guide](./firebase_ai_logic_integration_guide.md) for comprehensive documentation
2. **Compare**: [AI Approach Comparison](./ai_approach_comparison.md) to decide between Firebase AI Logic and Genkit
3. **Implement**: Start with simple dialogue generation
4. **Test**: Verify App Check is working
5. **Monitor**: Track usage and costs in Firebase Console

## Related Documentation

- [Firebase AI Logic Integration Guide](./firebase_ai_logic_integration_guide.md) - Complete guide
- [AI Approach Comparison](./ai_approach_comparison.md) - Compare TFLite, Firebase AI Logic, and Genkit
- [Genkit Integration Guide](./genkit_integration_guide.md) - Backend alternative
- [Official Firebase AI Docs](https://firebase.google.com/docs/ai-logic)
- [Package Documentation](https://pub.dev/documentation/firebase_ai/latest/)

## External Resources

- **Package**: [pub.dev/packages/firebase_ai](https://pub.dev/packages/firebase_ai)
- **Documentation**: [pub.dev/documentation/firebase_ai/latest/](https://pub.dev/documentation/firebase_ai/latest/)
- **Firebase AI Logic**: [firebase.google.com/docs/ai-logic](https://firebase.google.com/docs/ai-logic)
- **App Check Setup**: [firebase.google.com/docs/app-check](https://firebase.google.com/docs/app-check)

---

**Package Version**: firebase_ai ^3.4.0  
**Last Updated**: October 15, 2025  
**Maintainer**: Unwritten AI Team

**Ready to implement?** Start with the simple text generation example above and gradually add more features!

