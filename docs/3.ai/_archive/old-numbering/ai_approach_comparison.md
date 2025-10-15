# AI Approach Comparison: TFLite vs Firebase AI Logic vs Genkit

## Overview

Unwritten can leverage **three different AI approaches**, each with distinct advantages. This guide helps you choose the right approach for each feature.

## The Three Approaches

### 1. TensorFlow Lite (On-Device)
**What**: Run pre-trained models directly on the user's device  
**Where**: Inside the Flutter app  
**Models**: Custom .tflite files

### 2. Firebase AI Logic (Client SDK)
**What**: Call Google's Gemini API directly from Flutter app  
**Where**: Client → Google AI (no backend needed)  
**Models**: Gemini 2.5 Flash, Gemini Vision, Imagen

### 3. Genkit (Backend Service)
**What**: Build custom AI workflows with Python backend  
**Where**: Client → Your Backend → Google AI  
**Models**: Any AI provider (Gemini, OpenAI, Anthropic, etc.)

## Quick Decision Tree

```
Need AI feature?
    │
    ├─→ Is it fast & fixed? (< 20ms, unchanging logic)
    │      └─→ TFLite ✓
    │
    ├─→ Is it simple & direct? (Quick prototype, MVP)
    │      └─→ Firebase AI Logic ✓
    │
    └─→ Is it complex? (Multi-step, tools, RAG, sensitive data)
           └─→ Genkit Backend ✓
```

## Detailed Comparison

### Performance

| Metric | TFLite | Firebase AI Logic | Genkit |
|--------|--------|------------------|---------|
| **Latency** | 5-15ms | 800-2000ms | 800-1500ms |
| **Throughput** | Instant | Depends on network | Depends on network |
| **Offline** | ✅ Yes | ❌ No | ❌ No |
| **Battery Impact** | Minimal | Low (network only) | Low (network only) |
| **Scalability** | Device-limited | Excellent | Excellent |

### Development

| Aspect | TFLite | Firebase AI Logic | Genkit |
|--------|--------|------------------|---------|
| **Setup Time** | 4-8 hours | 1-2 hours | 4-6 hours |
| **Complexity** | Medium-High | Low | High |
| **Maintenance** | Low (stable models) | Very Low | Medium |
| **Flexibility** | Low (fixed models) | Medium | High |
| **Debugging** | Moderate | Easy | Moderate-Hard |
| **Testing** | Unit + Integration | Easy | Full stack needed |

### Cost

| Cost Type | TFLite | Firebase AI Logic | Genkit |
|-----------|--------|------------------|---------|
| **Development** | High (model training) | Low | Medium |
| **API Calls** | $0 | $0.075-0.30 per 1M tokens | $0.075-0.30 per 1M tokens |
| **Infrastructure** | $0 | $0 | $10-50/month (Cloud Run) |
| **Per 1K Users/Month** | $0 | $5-20 | $5-30 |
| **Scaling** | Free | Linear with usage | Cheaper at scale |

### Security & Privacy

| Concern | TFLite | Firebase AI Logic | Genkit |
|---------|--------|------------------|---------|
| **Data Privacy** | ✅ All on-device | ⚠️ Sent to Google | ⚠️ Sent to Google |
| **API Key Security** | N/A | ⚠️ Client-side (use App Check!) | ✅ Server-side |
| **Abuse Prevention** | N/A | App Check required | Custom auth |
| **Compliance** | ✅ Easiest | Moderate | Moderate |
| **User Data** | Never leaves device | Sent for processing | Sent for processing |

## Feature-by-Feature Recommendations

### Personality Inference
**Requirement**: Analyze card data → Big 5 personality traits (0.0-1.0)  
**Need**: Fast (< 20ms), offline, fixed model

| Approach | Rating | Reasoning |
|----------|--------|-----------|
| **TFLite** | ⭐⭐⭐⭐⭐ | **BEST** - Instant, offline, privacy-preserving |
| Firebase AI Logic | ⭐⭐ | Too slow, unnecessary network call |
| Genkit | ⭐ | Massive overkill, adds latency |

**Recommendation**: **TFLite** ✓

---

### Sentiment Analysis
**Requirement**: Classify text → positive/neutral/negative  
**Need**: Fast (< 10ms), simple classification

| Approach | Rating | Reasoning |
|----------|--------|-----------|
| **TFLite** | ⭐⭐⭐⭐⭐ | **BEST** - Instant, simple model |
| Firebase AI Logic | ⭐⭐ | Works but slower than needed |
| Genkit | ⭐ | Overkill |

**Recommendation**: **TFLite** ✓

---

### Simple Dialogue Generation (MVP)
**Requirement**: Generate 1-3 sentence dialogue for card  
**Need**: Quick to implement, good quality, can iterate

| Approach | Rating | Reasoning |
|----------|--------|-----------|
| TFLite | ⭐⭐ | Would need trained model (time-consuming) |
| **Firebase AI Logic** | ⭐⭐⭐⭐⭐ | **BEST** - Fast to implement, good quality |
| Genkit | ⭐⭐⭐ | Better quality but more complex |

**Recommendation**: **Firebase AI Logic** ✓ (MVP), Genkit (Production)

---

### Rich Dialogue Generation (Production)
**Requirement**: Generate dialogue with context, history, personality  
**Need**: High quality, consistent, with fallbacks

| Approach | Rating | Reasoning |
|----------|--------|-----------|
| TFLite | ⭐ | Not feasible for creative text |
| Firebase AI Logic | ⭐⭐⭐ | Good but limited control |
| **Genkit** | ⭐⭐⭐⭐⭐ | **BEST** - Full control, workflows, caching |

**Recommendation**: **Genkit Backend** ✓

---

### Story Progression
**Requirement**: Generate next story beat based on choices  
**Need**: Context-aware, consistent, uses game state

| Approach | Rating | Reasoning |
|----------|--------|-----------|
| TFLite | ❌ | Not possible |
| Firebase AI Logic | ⭐⭐ | Can work but limited game state access |
| **Genkit** | ⭐⭐⭐⭐⭐ | **BEST** - Tool calling, RAG, full control |

**Recommendation**: **Genkit Backend** ✓

---

### Image Analysis (Card Artwork)
**Requirement**: Analyze uploaded image → personality traits  
**Need**: Vision model, good accuracy

| Approach | Rating | Reasoning |
|----------|--------|-----------|
| TFLite | ⭐⭐ | Possible but limited |
| **Firebase AI Logic** | ⭐⭐⭐⭐⭐ | **BEST** - Gemini Vision, easy to implement |
| Genkit | ⭐⭐⭐⭐ | Works well but more complex |

**Recommendation**: **Firebase AI Logic** ✓

---

### Multi-Turn Conversations
**Requirement**: Chat with character maintaining context  
**Need**: Session management, context, personality consistency

| Approach | Rating | Reasoning |
|----------|--------|-----------|
| TFLite | ❌ | Not feasible |
| Firebase AI Logic | ⭐⭐⭐⭐ | Built-in chat API, good for simple chat |
| **Genkit** | ⭐⭐⭐⭐⭐ | **BEST** - Better control, server-side state |

**Recommendation**: **Firebase AI Logic** ✓ (MVP), **Genkit** ✓ (Production)

---

### Player-Specific Narratives (RAG)
**Requirement**: Generate story using player's past interactions  
**Need**: Vector search, embeddings, context retrieval

| Approach | Rating | Reasoning |
|----------|--------|-----------|
| TFLite | ❌ | Not possible |
| Firebase AI Logic | ⭐⭐ | No built-in RAG support |
| **Genkit** | ⭐⭐⭐⭐⭐ | **BEST** - Full RAG support, embedders, retrievers |

**Recommendation**: **Genkit Backend** ✓

## Architecture Recommendations by Phase

### Phase 1: MVP (Weeks 1-8)

```
┌──────────────────────────────────────────┐
│         Flutter App (MVP)                │
│                                          │
│  TFLite → Personality, Sentiment        │
│  Firebase AI Logic → Simple Dialogue     │
│                                          │
└──────────────────────────────────────────┘
```

**Why**:
- ✅ Fastest to implement
- ✅ No backend to build
- ✅ Good enough for MVP
- ✅ Low maintenance

**Cost**: ~$5-10/month for 100 users

---

### Phase 2: Growth (Weeks 9-16)

```
┌──────────────────────────────────────────┐
│      Flutter App (Production)            │
│                                          │
│  TFLite → Fast inference                │
│  Firebase AI Logic → Simple features     │
│  Genkit Backend → Complex workflows      │
│                                          │
└──────────────────────────────────────────┘
```

**Why**:
- ✅ Best of both worlds
- ✅ Scale simple features (Firebase AI)
- ✅ Complex features well-controlled (Genkit)
- ✅ Can optimize costs with backend caching

**Cost**: ~$20-50/month for 1,000 users

---

### Phase 3: Scale (Week 17+)

```
┌──────────────────────────────────────────┐
│      Flutter App (At Scale)              │
│                                          │
│  TFLite → All fast inference            │
│  Genkit Backend → Most AI features       │
│  Firebase AI Logic → User-facing tools   │
│    (e.g., image upload analysis)        │
│                                          │
└──────────────────────────────────────────┘
```

**Why**:
- ✅ Genkit provides best cost control at scale
- ✅ Firebase AI Logic for features where client-side makes sense
- ✅ TFLite for all latency-critical operations

**Cost**: ~$150-300/month for 10,000 users (with optimization)

## Implementation Strategies

### Strategy 1: Progressive Enhancement (Recommended)

**Week 1-4: Start Simple**
```dart
class AIService {
  final TFLiteService _tflite;
  final FirebaseAIService _firebaseAI;
  
  // Use what's easiest to implement
  Future<Dialogue> generateDialogue(Card card) async {
    final personality = await _tflite.inferPersonality(card);
    return await _firebaseAI.generateDialogue(personality);
  }
}
```

**Week 5-8: Add Complexity**
```dart
class AIService {
  final TFLiteService _tflite;
  final FirebaseAIService _firebaseAI;
  final GenkitService? _genkit;  // Optional Genkit
  
  Future<Dialogue> generateDialogue(Card card, {bool complex = false}) async {
    final personality = await _tflite.inferPersonality(card);
    
    if (complex && _genkit != null) {
      return await _genkit.generateRichDialogue(personality);
    }
    
    return await _firebaseAI.generateDialogue(personality);
  }
}
```

**Week 9+: Optimize**
- Move complex features to Genkit
- Keep simple features on Firebase AI Logic
- Aggressive caching

---

### Strategy 2: Feature Flags

```dart
class AIService {
  final FeatureFlagService _flags;
  
  Future<Dialogue> generateDialogue(Card card) async {
    final useGenkit = await _flags.isEnabled('genkit_dialogue');
    
    if (useGenkit) {
      return await _genkitService.generateDialogue(card);
    } else {
      return await _firebaseAIService.generateDialogue(card);
    }
  }
}
```

**Benefits**:
- A/B test approaches
- Gradual rollout
- Easy rollback

---

### Strategy 3: Complexity-Based Routing

```dart
class AIService {
  Future<Dialogue> generateDialogue({
    required Card card,
    required GameContext context,
  }) async {
    final complexity = _assessComplexity(context);
    
    switch (complexity) {
      case Complexity.simple:
        // Quick greeting, no context
        return await _firebaseAI.generateSimple(card);
        
      case Complexity.moderate:
        // Context-aware dialogue
        return await _firebaseAI.generateWithContext(card, context);
        
      case Complexity.complex:
        // Multi-turn, RAG, tools
        return await _genkit.generateRichDialogue(card, context);
    }
  }
  
  Complexity _assessComplexity(GameContext context) {
    if (context.conversationHistory.isEmpty) {
      return Complexity.simple;
    } else if (context.conversationHistory.length < 5) {
      return Complexity.moderate;
    } else {
      return Complexity.complex;
    }
  }
}
```

## Common Pitfalls & Solutions

### Pitfall 1: Using Firebase AI Logic Without App Check

**Problem**: API abuse, quota exhaustion, high costs

**Solution**:
```dart
// ALWAYS enable App Check with Firebase AI Logic
await FirebaseAppCheck.instance.activate(
  androidProvider: AndroidProvider.playIntegrity,
  appleProvider: AppleProvider.appAttest,
);
```

---

### Pitfall 2: Not Caching Firebase AI Logic Responses

**Problem**: Every tap = new API call = high costs

**Solution**:
```dart
class CachedAIService {
  final _cache = <String, DialogueResponse>{};
  
  Future<DialogueResponse> generateDialogue(Card card) async {
    final key = card.id;
    
    if (_cache.containsKey(key)) {
      return _cache[key]!;
    }
    
    final response = await _firebaseAI.generateDialogue(card);
    _cache[key] = response;
    return response;
  }
}
```

---

### Pitfall 3: Using Genkit for Simple Features

**Problem**: Over-engineering, unnecessary complexity

**Solution**: Use Firebase AI Logic for simple features, Genkit for complex ones

---

### Pitfall 4: Using TFLite for Creative Text

**Problem**: TFLite models for text generation are huge and complex

**Solution**: TFLite for classification/regression, Firebase AI Logic or Genkit for generation

---

### Pitfall 5: Not Having Fallbacks

**Problem**: Network errors break the game

**Solution**:
```dart
Future<DialogueResponse> generateDialogue(Card card) async {
  try {
    // Try Firebase AI Logic
    return await _firebaseAI.generateDialogue(card);
  } on SocketException {
    // Fallback to cache
    return await _cache.get(card.id) ?? _getRuleBasedDialogue(card);
  } catch (e) {
    // Final fallback
    return _getRuleBasedDialogue(card);
  }
}
```

## Cost Comparison Example

**Scenario**: 1,000 active users, 50 dialogues per user per month

### Option 1: TFLite + Firebase AI Logic

| Item | Cost |
|------|------|
| TFLite | $0 (on-device) |
| Firebase AI Logic API | $3.50 |
| Infrastructure | $0 |
| **Total** | **$3.50/month** |

**Pros**: Simplest, lowest cost  
**Cons**: Less control, harder to optimize at scale

### Option 2: TFLite + Genkit

| Item | Cost |
|------|------|
| TFLite | $0 (on-device) |
| Genkit API calls | $3.50 |
| Cloud Run | $10 |
| **Total** | **$13.50/month** |

**Pros**: Better control, easier to optimize  
**Cons**: More complex, higher initial cost

### Option 3: Triple Hybrid (TFLite + Firebase AI Logic + Genkit)

| Item | Cost |
|------|------|
| TFLite | $0 (on-device) |
| Firebase AI Logic (25% of calls) | $0.88 |
| Genkit (75% of calls) | $2.62 |
| Cloud Run | $10 |
| **Total** | **$13.50/month** |

**Pros**: Best of both worlds  
**Cons**: Most complex architecture

**At 10,000 users**:
- Option 1: $35/month
- Option 2: $60/month (but with caching: ~$40/month)
- Option 3: $55/month (optimized)

## Decision Checklist

Use this checklist to decide which approach for each feature:

### ✅ Use TFLite If:
- [ ] Need < 20ms latency
- [ ] Must work offline
- [ ] Classification or regression task
- [ ] Model is < 50MB
- [ ] Privacy is critical
- [ ] Don't need frequent model updates

### ✅ Use Firebase AI Logic If:
- [ ] Need AI quickly (MVP, prototype)
- [ ] Simple, direct AI features
- [ ] No backend expertise
- [ ] Low-to-moderate API usage expected
- [ ] Can use App Check for security
- [ ] Don't need server-side logic

### ✅ Use Genkit Backend If:
- [ ] Complex multi-step workflows
- [ ] Need tool calling with game state
- [ ] Want RAG for consistency
- [ ] High-volume production app
- [ ] Need server-side caching
- [ ] API key security is critical
- [ ] Have backend development resources

## FAQ

### Q: Can I use all three?

**A**: Yes! Most production apps should use a hybrid approach:
- TFLite for fast inference
- Firebase AI Logic for simple features
- Genkit for complex workflows

### Q: Which is fastest to implement?

**A**: Firebase AI Logic (1-2 hours for basic setup)

### Q: Which is cheapest at scale?

**A**: Genkit (with server-side caching and optimization)

### Q: Which is most secure?

**A**: TFLite (all on-device) > Genkit (server-side API keys) > Firebase AI Logic (client-side with App Check)

### Q: Can I migrate from Firebase AI Logic to Genkit later?

**A**: Yes! Design your repository pattern to abstract the implementation:

```dart
abstract class AIRepository {
  Future<DialogueResponse> generateDialogue(Card card);
}

class FirebaseAIRepositoryImpl implements AIRepository {
  // Firebase AI Logic implementation
}

class GenkitRepositoryImpl implements AIRepository {
  // Genkit implementation
}
```

Switch implementations without changing app code.

### Q: What about OpenAI or Anthropic?

**A**: 
- **Firebase AI Logic**: Only supports Gemini/Imagen
- **Genkit**: Supports any provider (Gemini, OpenAI, Anthropic, etc.)
- **TFLite**: Any model you can convert

## Recommended Learning Path

### Week 1: Start with Firebase AI Logic
1. Read: [Firebase AI Logic Integration Guide](./firebase_ai_logic_integration_guide.md)
2. Implement: Simple dialogue generation
3. Deploy: Test with App Check enabled
4. Result: Working AI features in 1-2 days

### Week 2-4: Add TFLite
1. Read: [TensorFlow Lite Integration](./tensorflow_lite_integration.md)
2. Implement: Personality and sentiment inference
3. Test: Verify < 20ms latency
4. Result: Hybrid fast + creative AI

### Week 5-8: Evaluate Genkit (If Needed)
1. Read: [Genkit Integration Guide](./genkit_integration_guide.md)
2. Implement: One complex feature as proof of concept
3. Compare: Firebase AI Logic vs Genkit for your use case
4. Decide: Migrate complex features or stay with Firebase AI

## Related Documentation

- [Firebase AI Logic Integration Guide](./firebase_ai_logic_integration_guide.md) - Complete Firebase AI Logic guide
- [Genkit Integration Guide](./genkit_integration_guide.md) - Complete Genkit guide
- [Genkit Quick Reference](./genkit_quick_reference.md) - Genkit cheat sheet
- [TensorFlow Lite Integration](./tensorflow_lite_integration.md) - TFLite guide
- [AI Architecture](../5.architecture/genkit_architecture.md) - Overall AI architecture

---

**Document Version**: 1.0  
**Last Updated**: October 15, 2025  
**Maintainer**: Unwritten AI Team

**Need help deciding?** Start with Firebase AI Logic for MVP, evaluate Genkit when you have 1,000+ active users or need complex workflows.

