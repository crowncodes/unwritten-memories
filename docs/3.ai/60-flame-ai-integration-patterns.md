# Flame AI Integration Patterns

**Purpose:** Architectural patterns for integrating AI in Flame game loop without blocking  
**Audience:** Flame developers, game engineers, mobile developers  
**Status:** ✅ Complete  
**Related:** ← 50-ai-output-storage-system.md | → 61-flame-ai-components.md | 62-flame-game-loop-ai.md

---

## What This Document Covers

This document provides **complete architectural patterns** for integrating AI into Flame game components. You'll learn:
- How to call AI without blocking the game loop (60 FPS critical)
- Non-blocking async patterns for AI requests
- Component design for AI-aware game objects
- Queue management for multiple AI requests
- Loading states and visual feedback
- Pre-loading and predictive strategies
- Error handling in game context

**Why This Matters:**
- **Game loop must run at 60 FPS** - AI cannot block
- AI latency is 2-10 seconds - needs async handling
- Poor integration = stuttering, freezing, bad UX
- Good patterns = smooth gameplay with invisible AI

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [Non-Blocking Async Patterns](#non-blocking-async-patterns)
3. [AI-Aware Component Design](#ai-aware-component-design)
4. [Request Queue Management](#request-queue-management)
5. [Loading States](#loading-states)
6. [Pre-Loading Strategies](#pre-loading-strategies)
7. [Error Handling](#error-handling)
8. [Performance Optimization](#performance-optimization)
9. [Integration Examples](#integration-examples)

---

## Core Principles

### Rule #1: NEVER Block the Game Loop

```dart
// ❌ BAD - Blocks game loop
class BadCardComponent extends PositionComponent {
  @override
  void update(double dt) {
    super.update(dt);
    
    // NEVER DO THIS - blocks for 2-5 seconds!
    final dialogue = await _aiService.generateDialogue(); // ❌ await in update()
    _showDialogue(dialogue);
  }
}

// ✅ GOOD - Async request, non-blocking
class GoodCardComponent extends PositionComponent {
  Future<String>? _dialogueFuture;
  String? _currentDialogue;
  
  @override
  void update(double dt) {
    super.update(dt);
    
    // Check if future completed (non-blocking)
    if (_dialogueFuture != null) {
      _checkDialogueReady();
    }
  }
  
  void _requestDialogue() {
    // Start async request (returns immediately)
    _dialogueFuture = _aiService.generateDialogue();
  }
  
  void _checkDialogueReady() {
    // Non-blocking check
    _dialogueFuture!.then((dialogue) {
      _currentDialogue = dialogue;
      _dialogueFuture = null;
    }).catchError((error) {
      AppLogger.error('Dialogue generation failed', error);
      _dialogueFuture = null;
    });
  }
}
```

### Rule #2: Show Loading States

```dart
// Users need feedback during AI generation
class CardWithLoadingState extends PositionComponent {
  AIState _aiState = AIState.idle;
  
  void _requestDialogue() {
    _aiState = AIState.loading;  // Show loading indicator
    
    _aiService.generateDialogue().then((dialogue) {
      _aiState = AIState.ready;
      _currentDialogue = dialogue;
    }).catchError((error) {
      _aiState = AIState.error;
    });
  }
  
  @override
  void render(Canvas canvas) {
    super.render(canvas);
    
    switch (_aiState) {
      case AIState.loading:
        _renderLoadingSpinner(canvas);
        break;
      case AIState.ready:
        _renderDialogue(canvas);
        break;
      case AIState.error:
        _renderErrorMessage(canvas);
        break;
      case AIState.idle:
        break;
    }
  }
}

enum AIState { idle, loading, ready, error }
```

### Rule #3: Pre-Load Predictable Content

```dart
// Pre-load likely next dialogues
class PredictiveCardComponent extends PositionComponent {
  @override
  void onMount() {
    super.onMount();
    
    // Pre-load greeting when card mounts (before user clicks)
    _preloadDialogue('greeting');
  }
  
  void _preloadDialogue(String type) {
    // Non-blocking pre-load
    _aiService.getDialogue(cardId: id, type: type).then((dialogue) {
      // Cached for instant access when needed
      AppLogger.info('Pre-loaded $type dialogue');
    }).catchError((error) {
      // Silently fail pre-load
      AppLogger.info('Pre-load failed for $type');
    });
  }
}
```

### Rule #4: Degrade Gracefully

```dart
// Always have fallback content
class RobustCardComponent extends PositionComponent {
  Future<String> _getDialogue() async {
    try {
      // Try AI-generated
      return await _aiService.generateDialogue(cardId: id);
    } catch (e) {
      AppLogger.error('AI failed, using fallback', e);
      
      // Fallback to cached or rule-based
      return _getFallbackDialogue();
    }
  }
  
  String _getFallbackDialogue() {
    // Use cached previous dialogue or generic response
    return _cache.get(id) ?? "Hello! How are you?";
  }
}
```

---

## Non-Blocking Async Patterns

### Pattern 1: Future with State Tracking

**Use when:** Single AI request per interaction

```dart
class AIFutureComponent extends PositionComponent {
  Future<DialogueResponse>? _pendingRequest;
  DialogueResponse? _result;
  bool _isLoading = false;
  
  void requestAIContent() {
    if (_isLoading) return; // Prevent duplicate requests
    
    _isLoading = true;
    _pendingRequest = _aiService.generateDialogue(cardId: id);
    
    // Handle completion (doesn't block)
    _pendingRequest!.then((response) {
      _result = response;
      _isLoading = false;
      _pendingRequest = null;
      _onAIContentReady();
    }).catchError((error) {
      _isLoading = false;
      _pendingRequest = null;
      _onAIContentError(error);
    });
  }
  
  @override
  void update(double dt) {
    super.update(dt);
    // Update proceeds normally - not blocked!
  }
  
  void _onAIContentReady() {
    // Trigger animation, show dialogue, etc.
  }
  
  void _onAIContentError(dynamic error) {
    // Show error state or fallback
  }
}
```

### Pattern 2: Stream for Progressive Updates

**Use when:** Streaming AI responses (character-by-character)

```dart
class AIStreamComponent extends PositionComponent {
  StreamSubscription<String>? _streamSubscription;
  String _accumulatedText = '';
  
  void requestStreamingDialogue() {
    // Start streaming response
    final stream = _aiService.generateDialogueStream(cardId: id);
    
    _streamSubscription = stream.listen(
      (chunk) {
        // Update text incrementally (smooth reveal)
        _accumulatedText += chunk;
        _onTextUpdate();
      },
      onError: (error) {
        AppLogger.error('Streaming failed', error);
        _onStreamError(error);
      },
      onDone: () {
        _onStreamComplete();
      },
    );
  }
  
  void _onTextUpdate() {
    // Re-render with new text
    // Game loop continues uninterrupted!
  }
  
  @override
  void onRemove() {
    _streamSubscription?.cancel();
    super.onRemove();
  }
}
```

### Pattern 3: Completer for Manual Control

**Use when:** Complex coordination needed

```dart
class AICompleterComponent extends PositionComponent {
  final Completer<DialogueResponse> _completer = Completer();
  
  void requestAIContent() {
    _aiService.generateDialogue(cardId: id).then((response) {
      if (!_completer.isCompleted) {
        _completer.complete(response);
      }
    }).catchError((error) {
      if (!_completer.isCompleted) {
        _completer.completeError(error);
      }
    });
  }
  
  Future<void> waitForAI() async {
    // Can await this in async methods (NOT in update())
    return await _completer.future;
  }
  
  void cancelRequest() {
    if (!_completer.isCompleted) {
      _completer.completeError('Cancelled');
    }
  }
}
```

---

## AI-Aware Component Design

### Base AI Component

```dart
// lib/features/game/presentation/components/ai_aware_component.dart
import 'package:flame/components.dart';

/// Base class for components that use AI
abstract class AIAwareComponent extends PositionComponent {
  AIState get aiState => _aiState;
  AIState _aiState = AIState.idle;
  
  Future<T>? _pendingRequest;
  T? _currentResult;
  
  /// Start an AI request (non-blocking)
  @protected
  void requestAI<T>(Future<T> request, {
    required void Function(T) onSuccess,
    void Function(dynamic)? onError,
  }) {
    if (_aiState == AIState.loading) {
      AppLogger.info('AI request already in progress');
      return;
    }
    
    _aiState = AIState.loading;
    onLoadingStart();
    
    request.then((result) {
      _currentResult = result as T?;
      _aiState = AIState.ready;
      onLoadingEnd();
      onSuccess(result);
    }).catchError((error) {
      _aiState = AIState.error;
      onLoadingEnd();
      if (onError != null) {
        onError(error);
      } else {
        _handleDefaultError(error);
      }
    });
  }
  
  /// Called when AI request starts
  @protected
  void onLoadingStart() {
    // Override to show loading indicator
  }
  
  /// Called when AI request completes (success or error)
  @protected
  void onLoadingEnd() {
    // Override to hide loading indicator
  }
  
  void _handleDefaultError(dynamic error) {
    AppLogger.error('AI request failed', error);
    // Show default error state
  }
  
  /// Cancel pending AI request
  void cancelAIRequest() {
    if (_aiState == AIState.loading) {
      _pendingRequest = null;
      _aiState = AIState.idle;
      onLoadingEnd();
    }
  }
}

enum AIState {
  idle,       // No AI request
  loading,    // AI request in progress
  ready,      // AI result available
  error,      // AI request failed
}
```

### AI Dialogue Component

**See:** `61-flame-ai-components.md` for complete implementation

```dart
class AIDialogueComponent extends AIAwareComponent {
  final String cardId;
  final AIService _aiService;
  
  String? _currentDialogue;
  late TextBoxComponent _textBox;
  late SpriteComponent _loadingSpinner;
  
  AIDialogueComponent({
    required this.cardId,
    required AIService aiService,
  }) : _aiService = aiService;
  
  @override
  Future<void> onLoad() async {
    // Setup text box
    _textBox = TextBoxComponent(
      text: '',
      textRenderer: TextPaint(/* ... */),
    );
    add(_textBox);
    
    // Setup loading spinner
    _loadingSpinner = SpriteComponent(/* ... */);
    _loadingSpinner.opacity = 0.0;
    add(_loadingSpinner);
  }
  
  /// Request new dialogue
  void generateDialogue({required Map<String, dynamic> context}) {
    requestAI<String>(
      _aiService.generateDialogue(cardId: cardId, context: context),
      onSuccess: (dialogue) {
        _currentDialogue = dialogue;
        _showDialogue(dialogue);
      },
      onError: (error) {
        _showErrorDialogue();
      },
    );
  }
  
  @override
  void onLoadingStart() {
    // Show loading spinner
    _loadingSpinner.opacity = 1.0;
    _textBox.text = 'Thinking...';
  }
  
  @override
  void onLoadingEnd() {
    // Hide loading spinner
    _loadingSpinner.opacity = 0.0;
  }
  
  void _showDialogue(String dialogue) {
    // Animate text reveal (character by character)
    _animateTextReveal(dialogue);
  }
  
  void _animateTextReveal(String fullText) {
    // Reveal text progressively (doesn't block game loop)
    int currentIndex = 0;
    final timer = Timer.periodic(Duration(milliseconds: 30), (timer) {
      if (currentIndex < fullText.length) {
        _textBox.text = fullText.substring(0, currentIndex + 1);
        currentIndex++;
      } else {
        timer.cancel();
      }
    });
  }
  
  void _showErrorDialogue() {
    _textBox.text = '[Unable to generate dialogue]';
  }
}
```

---

## Request Queue Management

### AI Request Queue

**Use when:** Multiple AI requests need ordering/priority

```dart
// lib/core/services/ai_request_queue.dart
class AIRequestQueue {
  final List<AIRequest> _queue = [];
  bool _processing = false;
  int _maxConcurrent = 3;
  int _activeRequests = 0;
  
  /// Add request to queue
  Future<T> enqueue<T>(AIRequest<T> request) {
    final completer = Completer<T>();
    _queue.add(request..completer = completer);
    
    _processQueue();
    
    return completer.future;
  }
  
  /// Process queue (respects concurrency limit)
  Future<void> _processQueue() async {
    if (_processing) return;
    _processing = true;
    
    while (_queue.isNotEmpty && _activeRequests < _maxConcurrent) {
      final request = _queue.removeAt(0);
      _activeRequests++;
      
      // Execute request (non-blocking)
      _executeRequest(request);
    }
    
    _processing = false;
  }
  
  Future<void> _executeRequest(AIRequest request) async {
    try {
      final result = await request.execute();
      request.completer.complete(result);
    } catch (error) {
      request.completer.completeError(error);
    } finally {
      _activeRequests--;
      _processQueue(); // Process next in queue
    }
  }
  
  /// Cancel all pending requests
  void cancelAll() {
    for (final request in _queue) {
      request.completer.completeError('Cancelled');
    }
    _queue.clear();
  }
}

class AIRequest<T> {
  final String id;
  final AIRequestPriority priority;
  final Future<T> Function() execute;
  late Completer<T> completer;
  
  AIRequest({
    required this.id,
    required this.execute,
    this.priority = AIRequestPriority.normal,
  });
}

enum AIRequestPriority {
  low,      // Pre-fetch, background
  normal,   // Regular interactions
  high,     // User-initiated
  critical, // Game-breaking if fails
}
```

### Priority Queue Component

```dart
class PriorityAIComponent extends AIAwareComponent {
  final AIRequestQueue _queue = AIRequestQueue();
  
  void requestCriticalDialogue() {
    final request = AIRequest(
      id: 'critical_dialogue',
      priority: AIRequestPriority.critical,
      execute: () => _aiService.generateDialogue(cardId: id),
    );
    
    _queue.enqueue(request).then((dialogue) {
      _showDialogue(dialogue);
    });
  }
  
  void prefetchBackgroundDialogue() {
    final request = AIRequest(
      id: 'bg_dialogue',
      priority: AIRequestPriority.low,
      execute: () => _aiService.generateDialogue(cardId: id),
    );
    
    _queue.enqueue(request).then((dialogue) {
      // Cache silently
      _cache.put(id, dialogue);
    });
  }
}
```

---

## Loading States

### Loading Indicator Component

```dart
// lib/features/game/presentation/components/ai_loading_indicator.dart
class AILoadingIndicator extends PositionComponent {
  late SpriteAnimationComponent _spinner;
  late TextComponent _loadingText;
  double _elapsedTime = 0;
  
  @override
  Future<void> onLoad() async {
    // Animated spinner
    _spinner = SpriteAnimationComponent(
      animation: /* rotating animation */,
      size: Vector2.all(32),
    );
    add(_spinner);
    
    // "Generating..." text
    _loadingText = TextComponent(
      text: 'Generating...',
      textRenderer: TextPaint(/* ... */),
    );
    add(_loadingText);
  }
  
  @override
  void update(double dt) {
    super.update(dt);
    
    _elapsedTime += dt;
    
    // Update text based on elapsed time
    if (_elapsedTime < 2.0) {
      _loadingText.text = 'Thinking...';
    } else if (_elapsedTime < 5.0) {
      _loadingText.text = 'Almost ready...';
    } else {
      _loadingText.text = 'Just a moment...';
    }
  }
  
  /// Show loading indicator
  void show() {
    opacity = 1.0;
    _elapsedTime = 0;
  }
  
  /// Hide loading indicator
  void hide() {
    opacity = 0.0;
  }
}
```

---

## Pre-Loading Strategies

### Pattern 1: On-Mount Pre-Load

```dart
class PreloadingCardComponent extends PositionComponent {
  @override
  void onMount() {
    super.onMount();
    
    // Pre-load greeting dialogue when card appears
    _prefetchDialogue('greeting');
    
    // Pre-load card image
    _prefetchImage();
  }
  
  void _prefetchDialogue(String type) {
    _aiService.getDialogue(cardId: id, type: type).then((dialogue) {
      AppLogger.info('Pre-loaded $type');
    }).catchError((e) {
      // Silent failure OK for pre-load
    });
  }
}
```

### Pattern 2: Predictive Pre-Load

```dart
class PredictivePreloader {
  final AIService _aiService;
  
  /// Pre-load based on player behavior prediction
  void preloadLikelyNext({
    required String currentCardId,
    required List<String> likelyNextCards,
  }) {
    for (final nextCardId in likelyNextCards) {
      // Non-blocking pre-load
      unawaited(
        _aiService.getDialogue(cardId: nextCardId, type: 'greeting')
      );
    }
  }
  
  /// Pre-load during idle time
  void preloadDuringIdle(List<String> cardIds) {
    // Wait for idle period
    Future.delayed(Duration(seconds: 2), () {
      for (final cardId in cardIds) {
        unawaited(_aiService.getDialogue(cardId: cardId, type: 'greeting'));
      }
    });
  }
}
```

---

## Error Handling

### Graceful Error Component

```dart
class RobustAIComponent extends AIAwareComponent {
  int _retryCount = 0;
  static const int MAX_RETRIES = 3;
  
  void requestWithRetry() {
    requestAI<String>(
      _aiService.generateDialogue(cardId: id),
      onSuccess: (dialogue) {
        _retryCount = 0; // Reset on success
        _showDialogue(dialogue);
      },
      onError: (error) {
        _handleErrorWithRetry(error);
      },
    );
  }
  
  void _handleErrorWithRetry(dynamic error) {
    if (_retryCount < MAX_RETRIES) {
      _retryCount++;
      AppLogger.info('Retrying AI request (attempt $_retryCount)');
      
      // Exponential backoff
      Future.delayed(Duration(seconds: 2 << _retryCount), () {
        requestWithRetry();
      });
    } else {
      // Max retries exceeded - show fallback
      _showFallbackContent();
    }
  }
  
  void _showFallbackContent() {
    _showDialogue(_getFallbackDialogue());
  }
  
  String _getFallbackDialogue() {
    return _cache.get(id) ?? "Hello!";
  }
}
```

---

## Performance Optimization

### Optimization Checklist

✅ **Non-Blocking:** All AI requests use async patterns
✅ **Loading States:** Users see feedback during generation
✅ **Pre-Loading:** Likely content loaded before needed
✅ **Caching:** Results cached aggressively (80%+ hit rate)
✅ **Queue Management:** Multiple requests don't overwhelm system
✅ **Error Handling:** Graceful degradation with fallbacks
✅ **Cancellation:** Requests can be cancelled if no longer needed

### Performance Monitoring

```dart
class AIPerformanceMonitor {
  int totalRequests = 0;
  int cacheHits = 0;
  int errors = 0;
  Duration totalLatency = Duration.zero;
  
  void recordRequest({
    required bool cached,
    required Duration latency,
    required bool success,
  }) {
    totalRequests++;
    
    if (cached) {
      cacheHits++;
    }
    
    if (!success) {
      errors++;
    }
    
    totalLatency += latency;
    
    // Log metrics periodically
    if (totalRequests % 100 == 0) {
      _logMetrics();
    }
  }
  
  void _logMetrics() {
    final avgLatency = totalLatency.inMilliseconds / totalRequests;
    final cacheRate = cacheHits / totalRequests;
    final errorRate = errors / totalRequests;
    
    AppLogger.performance('AI Performance', Duration(milliseconds: avgLatency.toInt()));
    AppLogger.ai('AI Metrics', metrics: {
      'cache_rate': cacheRate,
      'error_rate': errorRate,
      'avg_latency_ms': avgLatency,
    });
  }
}
```

---

## Integration Examples

### Complete Card Component Example

**See:** `61-flame-ai-components.md` for more examples

```dart
// lib/features/game/presentation/components/interactive_card.dart
class InteractiveCard extends AIAwareComponent with TapCallbacks {
  final String cardId;
  final AIService _aiService;
  final AIRepository _repository;
  
  late AIDialogueComponent _dialogueBox;
  late AILoadingIndicator _loadingIndicator;
  
  InteractiveCard({
    required this.cardId,
    required AIService aiService,
    required AIRepository repository,
  }) : _aiService = aiService,
       _repository = repository;
  
  @override
  Future<void> onLoad() async {
    // Setup dialogue box
    _dialogueBox = AIDialogueComponent(
      cardId: cardId,
      aiService: _aiService,
    );
    add(_dialogueBox);
    
    // Setup loading indicator
    _loadingIndicator = AILoadingIndicator();
    add(_loadingIndicator);
    
    // Pre-load greeting
    _prefetchGreeting();
  }
  
  @override
  void onTapDown(TapDownEvent event) {
    // User tapped - request dialogue
    _requestDialogue();
  }
  
  void _prefetchGreeting() {
    // Pre-load in background (non-blocking)
    _repository.getDialogue(
      cardId: cardId,
      interactionId: 'greeting',
    ).then((dialogue) {
      AppLogger.info('Pre-loaded greeting for $cardId');
    }).catchError((e) {
      // Silent failure OK
    });
  }
  
  void _requestDialogue() {
    _loadingIndicator.show();
    
    _repository.getDialogue(
      cardId: cardId,
      interactionId: _generateInteractionId(),
    ).then((dialogue) {
      _loadingIndicator.hide();
      _dialogueBox.showDialogue(dialogue);
    }).catchError((error) {
      _loadingIndicator.hide();
      _dialogueBox.showError();
    });
  }
  
  String _generateInteractionId() {
    return 'interaction_${DateTime.now().millisecondsSinceEpoch}';
  }
}
```

---

## Related Documentation

- **61-flame-ai-components.md** - Complete component library with examples
- **62-flame-game-loop-ai.md** - Deep dive into game loop integration
- **50-ai-output-storage-system.md** - AI output storage and caching
- **40-hybrid-cloud-local-system.md** - Cloud-local AI routing

---

**Status:** ✅ Complete  
**Implementation:** See 61-flame-ai-components.md for complete component implementations  
**Critical Rule:** NEVER await AI in update() - use async patterns


