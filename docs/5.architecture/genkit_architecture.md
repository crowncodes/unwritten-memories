# Genkit + TFLite Hybrid Architecture

## Overview

Unwritten uses a hybrid AI architecture that combines on-device TensorFlow Lite inference with cloud-based Genkit services to deliver fast, intelligent, and creative AI experiences while maintaining battery efficiency and offline capability.

## Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                         Flutter App (Unwritten)                    │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                     Presentation Layer                        │ │
│  │  (lib/features/*/presentation/)                              │ │
│  │                                                              │ │
│  │  ├─ CardInteractionScreen                                   │ │
│  │  ├─ DialogueWidget                                          │ │
│  │  └─ StoryProgressionScreen                                  │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                              │                                     │
│                              ▼                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                      Domain Layer                            │ │
│  │  (lib/features/*/domain/)                                    │ │
│  │                                                              │ │
│  │  ├─ AIRepository (interface)                                │ │
│  │  ├─ DialogueUseCase                                         │ │
│  │  └─ StoryProgressionUseCase                                 │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                              │                                     │
│                              ▼                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                      Data Layer                              │ │
│  │  (lib/features/*/data/)                                      │ │
│  │                                                              │ │
│  │  ├─ AIRepositoryImpl                                        │ │
│  │  │   ├─ TFLiteService (fast, on-device)                    │ │
│  │  │   └─ GenkitService (creative, cloud)                    │ │
│  │  │                                                          │ │
│  │  ├─ CacheService                                            │ │
│  │  └─ BatteryMonitorService                                   │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                              │                                     │
└──────────────────────────────┼─────────────────────────────────────┘
                               │
                ┌──────────────┴───────────────┐
                │                              │
                ▼                              ▼
┌───────────────────────────┐   ┌────────────────────────────────┐
│   TFLite Models           │   │   Network Layer                │
│   (On-Device)             │   │                                │
│                           │   │   HTTP Client + WebSocket      │
│  ├─ personality.tflite    │   │   ├─ Request batching         │
│  ├─ sentiment.tflite      │   │   ├─ Retry logic              │
│  └─ relationship.tflite   │   │   └─ Error handling           │
└───────────────────────────┘   └────────────────────────────────┘
                                               │
                                               ▼
                                ┌──────────────────────────────────┐
                                │   Genkit Python Backend          │
                                │   (Cloud Run)                    │
                                │                                  │
                                │  ┌─────────────────────────────┐│
                                │  │  API Layer (FastAPI/Flask)  ││
                                │  │  ├─ /dialogue               ││
                                │  │  ├─ /story                  ││
                                │  │  └─ /character              ││
                                │  └─────────────────────────────┘│
                                │               │                  │
                                │               ▼                  │
                                │  ┌─────────────────────────────┐│
                                │  │  Genkit Flows               ││
                                │  │  ├─ dialogue_generation     ││
                                │  │  ├─ story_progression       ││
                                │  │  └─ character_interaction   ││
                                │  └─────────────────────────────┘│
                                │               │                  │
                                │               ▼                  │
                                │  ┌─────────────────────────────┐│
                                │  │  Tools & RAG                ││
                                │  │  ├─ fetch_card_data         ││
                                │  │  ├─ story_retriever         ││
                                │  │  └─ relationship_checker    ││
                                │  └─────────────────────────────┘│
                                └──────────────────────────────────┘
                                               │
                                               ▼
                                ┌──────────────────────────────────┐
                                │   Google Generative AI           │
                                │   (Gemini Models)                │
                                │                                  │
                                │  ├─ gemini-2.5-flash             │
                                │  ├─ gemini-2.0-flash-lite        │
                                │  └─ text-embedding-004           │
                                └──────────────────────────────────┘
```

## Decision Flow: When to Use Each Service

```
                    ┌─────────────────────────────┐
                    │  AI Operation Required      │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │  Is it personality/         │
                    │  sentiment inference?       │
                    └─────────────┬───────────────┘
                                  │
                     ┌────────────┼────────────┐
                     │ YES                     │ NO
                     ▼                         ▼
        ┌────────────────────────┐  ┌─────────────────────────┐
        │  Use TFLite            │  │  Check Battery Level     │
        │  (on-device)           │  └───────────┬─────────────┘
        │                        │              │
        │  • < 15ms latency      │              ▼
        │  • Works offline       │  ┌─────────────────────────┐
        │  • No network cost     │  │  Battery < 20% AND      │
        │  • Privacy preserved   │  │  Not charging?          │
        └────────────────────────┘  └───────────┬─────────────┘
                                                │
                                   ┌────────────┼────────────┐
                                   │ YES                     │ NO
                                   ▼                         ▼
                      ┌────────────────────────┐  ┌─────────────────────────┐
                      │  Check Cache           │  │  Check Network          │
                      └──────────┬─────────────┘  └───────────┬─────────────┘
                                 │                            │
                                 ▼                            ▼
                      ┌────────────────────────┐  ┌─────────────────────────┐
                      │  Cache Hit?            │  │  Online?                │
                      └──────────┬─────────────┘  └───────────┬─────────────┘
                                 │                            │
                    ┌────────────┼────────────┐  ┌────────────┼────────────┐
                    │ YES                     │  │ YES                     │ NO
                    ▼                         ▼  ▼                         ▼
       ┌────────────────────┐  ┌──────────────────────┐  ┌────────────────────┐
       │  Return Cached     │  │  Use Genkit Backend  │  │  Use Fallback      │
       │  Response          │  │                      │  │  (Rule-based)      │
       └────────────────────┘  │  • Rich dialogue     │  └────────────────────┘
                               │  • Creative story    │
                               │  • Context-aware     │
                               │  • 800-1500ms        │
                               └──────────────────────┘
```

## Component Responsibilities

### Flutter App (Client)

#### TFLiteService
**Purpose**: Fast, on-device AI inference for real-time operations

**Responsibilities**:
- Personality trait inference (Big 5 model)
- Sentiment analysis (positive/neutral/negative)
- Relationship score calculation
- Battery-efficient operations

**Performance Targets**:
- Inference: < 15ms
- Memory: < 50MB
- Battery impact: Negligible

**Example Usage**:
```dart
final personality = await tfliteService.inferPersonality(cardData);
// Returns: {openness: 0.8, extraversion: 0.6, ...}
```

#### GenkitService
**Purpose**: Rich, cloud-based AI for creative and complex tasks

**Responsibilities**:
- Dynamic dialogue generation
- Story narrative creation
- Complex character interactions
- Context-aware responses
- Multi-turn conversations

**Performance Targets**:
- Latency: < 1500ms (p95)
- Cache hit rate: > 60%
- Error rate: < 1%

**Example Usage**:
```dart
final dialogue = await genkitService.generateDialogue(
  cardId: 'card_123',
  context: 'First meeting in tavern',
  personalityTraits: personality,
);
// Returns: {text: "...", emotion: "curious", tone: "friendly"}
```

#### AIRepositoryImpl
**Purpose**: Orchestrate TFLite and Genkit services

**Responsibilities**:
- Route operations to appropriate service
- Implement caching strategy
- Handle fallbacks and errors
- Monitor battery state
- Track performance metrics

**Decision Logic**:
```dart
Future<DialogueResponse> generateDialogue(...) async {
  // 1. Fast inference (TFLite)
  final personality = await _tfliteService.inferPersonality(card);
  
  // 2. Check cache
  final cached = await _cache.get(key);
  if (cached != null) return cached;
  
  // 3. Check battery
  if (await _battery.level < 20 && !await _battery.isCharging) {
    return _generateSimpleDialogue(card, personality);
  }
  
  // 4. Use Genkit for rich dialogue
  try {
    final response = await _genkitService.generateDialogue(...);
    await _cache.set(key, response);
    return response;
  } catch (e) {
    // 5. Fallback to rule-based
    return _generateFallbackDialogue(card, personality);
  }
}
```

### Genkit Backend (Server)

#### API Layer
**Purpose**: HTTP/WebSocket interface for Flutter app

**Responsibilities**:
- Request validation
- Authentication
- Rate limiting
- Response formatting
- Error handling

**Endpoints**:
```python
POST /dialogue          # Generate dialogue
POST /story             # Progress story
POST /character         # Character interaction
POST /batch             # Batch operations
GET  /health           # Health check
```

#### Genkit Flows
**Purpose**: AI workflow orchestration

**Responsibilities**:
- Input validation with Pydantic
- Pre/post-processing
- Model interaction
- Tool calling
- RAG integration
- Error handling
- Logging/telemetry

**Example Flow**:
```python
@flow
async def dialogue_generation_flow(input: DialogueInput) -> DialogueOutput:
    # 1. Validate input
    validate_input(input)
    
    # 2. Pre-process
    context = build_context(input)
    
    # 3. Generate with AI
    response = await ai.generate(
        prompt=build_prompt(context),
        tools=[fetch_card_data, check_relationship],
        output_schema=DialogueOutput
    )
    
    # 4. Post-process
    final_output = enhance_output(response.output)
    
    # 5. Log metrics
    log_metrics(input, final_output)
    
    return final_output
```

#### Tools
**Purpose**: Extend AI capabilities with external functions

**Responsibilities**:
- Fetch game data
- Check relationship status
- Retrieve story context
- Access player history
- Query databases

**Example Tool**:
```python
@tool
async def fetch_card_data(card_id: str) -> dict:
    """Retrieves card information from database."""
    card = await db.cards.find_one({'id': card_id})
    return {
        'name': card.name,
        'backstory': card.backstory,
        'traits': card.personality_traits,
    }
```

#### RAG Components
**Purpose**: Enhance responses with retrieved context

**Responsibilities**:
- Embed content for vector search
- Index story content
- Retrieve relevant context
- Maintain narrative consistency

**Example RAG Flow**:
```python
@flow
async def rag_story_flow(input: StoryInput) -> StoryOutput:
    # 1. Retrieve relevant context
    context_docs = await story_retriever(input.query)
    
    # 2. Build augmented prompt
    prompt = f"""
    Story Context:
    {format_context(context_docs)}
    
    Current Situation:
    {input.situation}
    
    Generate next story beat...
    """
    
    # 3. Generate with context
    response = await ai.generate(prompt)
    
    return response.output
```

## Data Flow Examples

### Example 1: First Card Interaction

```
User taps on card
      │
      ▼
[Flutter] CardInteractionScreen
      │
      ▼
[Flutter] DialogueUseCase.generate()
      │
      ▼
[Flutter] AIRepositoryImpl.generateDialogue()
      │
      ├─────────────────────────────────┐
      │                                 │
      ▼                                 ▼
[TFLite] inferPersonality()    [Cache] check(key)
   • Input: card_data              │
   • Output: traits (8ms)          ▼
   • {openness: 0.8, ...}       Cache miss
      │                                 │
      └─────────────┬───────────────────┘
                    ▼
           [Network] Check connectivity
                    │
                    ▼ (online)
           [GenkitService] generateDialogue()
                    │
                    ▼
    [HTTP POST] https://backend-url/dialogue
      {
        cardId: "card_123",
        context: "First meeting",
        personalityTraits: {openness: 0.8, ...}
      }
                    │
                    ▼
    [Backend] POST /dialogue handler
                    │
                    ▼
    [Genkit] dialogue_generation_flow()
      │
      ├─ Validate input
      ├─ Build context
      ├─ Call tools (fetch_card_data)
      ├─ Generate with Gemini 2.5 Flash
      └─ Return structured output
                    │
                    ▼
    [Response] {
      text: "Greetings, traveler...",
      emotion: "curious",
      tone: "friendly",
      suggestedResponses: ["Hello", "Who are you?", ...]
    }
                    │
                    ▼
    [Flutter] Cache response
                    │
                    ▼
    [Flutter] Display dialogue in UI
```

### Example 2: Low Battery Mode

```
User taps on card (battery: 15%)
      │
      ▼
[Flutter] AIRepositoryImpl.generateDialogue()
      │
      ├─ Check battery: 15% (LOW)
      ├─ Check charging: false
      │
      ▼
[Decision] Use on-device only
      │
      ├─────────────────────────────────┐
      │                                 │
      ▼                                 ▼
[TFLite] inferPersonality()    [Cache] check(key)
   (8ms)                              │
      │                               ▼
      │                          Cache hit
      │                               │
      └───────────┬───────────────────┘
                  ▼
    [Flutter] _generateSimpleDialogue()
      • Use personality traits
      • Apply rule-based templates
      • Fast, no network
                  │
                  ▼
    [Response] {
      text: "Hello! [generated from rules]",
      emotion: "friendly",
      isFallback: true
    }
                  │
                  ▼
    [Flutter] Display dialogue in UI
```

### Example 3: Offline Mode

```
User taps on card (no network)
      │
      ▼
[Flutter] AIRepositoryImpl.generateDialogue()
      │
      ├─ Check battery: OK
      │
      ▼
[Cache] check(key)
      │
      ├─ Cache hit
      │
      ▼
[Flutter] Return cached response (instant)
      │
      ▼
[UI] Display dialogue
```

## Scaling Strategy

### Current Phase (MVP - 100-1K users)

```
Flutter App ──────► Single Cloud Run Instance
                    (1 vCPU, 2GB RAM)
                    ├─ Genkit flows
                    └─ Google Generative AI
```

**Cost**: ~$3-30/month  
**Latency**: 800-1500ms  
**Availability**: 99.5%

### Growth Phase (1K-10K users)

```
Flutter App ──────► Cloud Run (autoscaling)
                    (1-5 instances)
                    ├─ Genkit flows
                    ├─ Redis cache
                    └─ Google Generative AI
                    
                    + Cloud Load Balancer
                    + Cloud CDN (caching)
```

**Cost**: ~$35-200/month  
**Latency**: 600-1200ms (with CDN)  
**Availability**: 99.9%

### Scale Phase (10K-100K users)

```
Flutter App ──────► Global Load Balancer
                    │
                    ├─ Cloud Run (US) - 5-20 instances
                    ├─ Cloud Run (EU) - 3-10 instances
                    └─ Cloud Run (ASIA) - 3-10 instances
                    
                    Each region:
                    ├─ Genkit flows
                    ├─ Redis cluster (caching)
                    ├─ Firestore (state)
                    └─ Google Generative AI
                    
                    + Cloud CDN (edge caching)
                    + Cloud Armor (DDoS protection)
```

**Cost**: ~$350-2000/month  
**Latency**: 400-800ms (regional)  
**Availability**: 99.95%

## Performance Optimization Strategies

### 1. Multi-Level Caching

```
Request → Memory Cache (LRU, 100 items) → 5ms
              ↓ miss
          Disk Cache (Hive, 1000 items) → 20ms
              ↓ miss
          CDN Cache (Cloud CDN) → 100ms
              ↓ miss
          Backend Cache (Redis) → 200ms
              ↓ miss
          Generate (Genkit + Gemini) → 1200ms
```

**Cache Invalidation Strategy**:
- Memory: LRU, 15 min TTL
- Disk: 24 hour TTL
- CDN: 6 hour TTL
- Backend: 1 hour TTL

### 2. Request Batching

```dart
// Instead of 10 sequential requests (10 x 1200ms = 12s)
for (var card in cards) {
  await generateDialogue(card);
}

// Batch into single request (1 x 1500ms = 1.5s)
final responses = await generateBatchDialogues(cards);
```

**Savings**: 8x faster, 10x cheaper

### 3. Smart Model Routing

```python
@flow
async def smart_dialogue_flow(input: DialogueInput) -> DialogueOutput:
    # Assess complexity
    complexity = assess_complexity(input)
    
    if complexity == 'simple':
        # Fast, cheap model
        return await generate_with_model('gemini-2.0-flash-lite')
    elif complexity == 'medium':
        # Balanced model
        return await generate_with_model('gemini-2.5-flash')
    else:
        # Most capable model
        return await generate_with_model('gemini-2.5-pro')
```

**Benefits**:
- 30% cost reduction
- 20% latency improvement
- Same quality for users

### 4. Progressive Enhancement

```dart
Future<DialogueResponse> generateDialogue() async {
  // 1. Show cached/simple response immediately
  final quick = await _getQuickResponse();
  _streamController.add(quick);
  
  // 2. Generate rich response in background
  final rich = await _genkitService.generateDialogue();
  
  // 3. Update UI with rich response
  _streamController.add(rich);
}
```

**User Experience**:
- Instant feedback (< 50ms)
- Progressive enhancement
- Perceived latency: near-zero

## Security Architecture

### Authentication Flow

```
[Flutter] Request with API key
    │
    ▼
[Cloud Run] API Gateway
    │
    ├─ Validate API key
    ├─ Check rate limits
    └─ Verify request signature
    │
    ▼
[Genkit] Process request
    │
    ▼
[Response] Encrypted (HTTPS)
```

### Security Measures

1. **API Authentication**:
   - API keys stored in Flutter secure storage
   - Keys rotated every 90 days
   - Different keys for dev/staging/prod

2. **Rate Limiting**:
   - Per-user: 100 requests/minute
   - Per-IP: 1000 requests/minute
   - Backend: 10,000 requests/minute

3. **Input Validation**:
   - Pydantic models for type safety
   - Max input size: 5000 characters
   - Sanitize all user inputs

4. **Data Privacy**:
   - No PII logged
   - No chat history stored server-side
   - GDPR/CCPA compliant

## Monitoring & Observability

### Key Metrics

**Client-Side (Firebase Analytics)**:
```dart
- ai_dialogue_generated (success rate, latency)
- cache_hit_rate (memory, disk, network)
- battery_impact (per session)
- error_rate (by type)
- fallback_usage (frequency)
```

**Server-Side (Cloud Monitoring)**:
```python
- request_count (per endpoint)
- latency (p50, p95, p99)
- error_rate (4xx, 5xx)
- token_usage (input, output)
- cost_per_request
```

### Alerting Rules

```
Alert: High Error Rate
  Condition: error_rate > 5% for 5 minutes
  Action: PagerDuty alert
  
Alert: High Latency
  Condition: p95_latency > 3000ms for 10 minutes
  Action: Email + Slack
  
Alert: High Costs
  Condition: daily_cost > $50
  Action: Email + Disable non-critical features
```

### Observability Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│  Unwritten AI Service Dashboard                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Requests/min:  1,234  ▲ +12%                               │
│  Avg Latency:   847ms  ▼ -5%                                │
│  Error Rate:    0.3%   ▼ -0.1%                              │
│  Cost/day:      $12.45 ▲ +$1.20                             │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ Cache Hit Rate  │  │ Model Usage     │                  │
│  │                 │  │                 │                  │
│  │  Memory:  67%   │  │  Flash:  85%    │                  │
│  │  Disk:    45%   │  │  Lite:   15%    │                  │
│  │  Network: 12%   │  │                 │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
│  Recent Errors:                                             │
│  - Timeout (2): /dialogue - 3s limit exceeded               │
│  - 429 (1): Rate limit hit for user_123                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Disaster Recovery

### Failure Scenarios

#### Scenario 1: Genkit Backend Down

```
[Flutter] Request to backend
    │
    ▼
[Network] Connection failed
    │
    ▼
[AIRepository] Catch error
    │
    ├─ Try cache
    │     │
    │     ▼ (hit)
    │  Return cached
    │     │
    │     ▼ (miss)
    ├─ Use TFLite + rules
    │
    ▼
[User] Still has experience (degraded)
```

**Recovery Time**: Instant (automatic fallback)  
**User Impact**: Reduced dialogue creativity

#### Scenario 2: API Rate Limit Exceeded

```
[Flutter] Too many requests
    │
    ▼
[Backend] 429 Too Many Requests
    │
    ▼
[AIRepository] Implement backoff
    │
    ├─ Wait with exponential backoff
    ├─ Use cached responses
    └─ Queue non-critical requests
    │
    ▼
[User] Core features work, rate-limited features queued
```

**Recovery Time**: 1-60 seconds  
**User Impact**: Slight delay for new dialogues

#### Scenario 3: Model Provider Outage (Google AI)

```
[Backend] Model request fails
    │
    ▼
[Genkit] Retry with backoff (3 attempts)
    │
    ▼ (all failed)
[Backend] Switch to fallback model
    │
    └─ Use cached templates
    └─ Use rule-based generation
    │
    ▼
[User] Degraded but functional
```

**Recovery Time**: Automatic  
**User Impact**: Less creative responses temporarily

## Migration Strategy

### Phase 1: Setup (Week 1)
- [ ] Create Genkit backend project
- [ ] Deploy to Cloud Run (staging)
- [ ] Add GenkitService to Flutter app
- [ ] Implement basic dialogue flow
- [ ] Test end-to-end integration

### Phase 2: Feature Flag Rollout (Week 2-3)
- [ ] Add feature flag: `enable_genkit`
- [ ] Route 1% of users to Genkit
- [ ] Monitor metrics closely
- [ ] Increase to 5% if stable
- [ ] Increase to 25% if positive

### Phase 3: Optimization (Week 4-5)
- [ ] Implement caching strategy
- [ ] Add batch request support
- [ ] Optimize prompts for latency
- [ ] Configure CDN caching
- [ ] Add monitoring dashboards

### Phase 4: Full Rollout (Week 6+)
- [ ] Increase to 100% of users
- [ ] Monitor costs and performance
- [ ] Optimize based on real usage
- [ ] Add advanced features (RAG, tools)
- [ ] Scale infrastructure as needed

## Testing Strategy

### Unit Tests

```dart
// Flutter: Test AIRepository routing logic
test('uses TFLite for personality inference', () async {
  final result = await aiRepository.inferPersonality(card);
  verify(() => tfliteService.inferPersonality(any())).called(1);
  verifyNever(() => genkitService.inferPersonality(any()));
});

test('uses Genkit for dialogue generation', () async {
  final result = await aiRepository.generateDialogue(card, context);
  verify(() => genkitService.generateDialogue(any())).called(1);
});
```

```python
# Backend: Test flows
async def test_dialogue_flow():
    input_data = DialogueInput(
        card_id='test_card',
        context='Test context',
        personality_traits={'openness': 0.8},
    )
    
    result = await dialogue_generation_flow(input_data)
    
    assert result.text
    assert result.emotion in VALID_EMOTIONS
    assert len(result.suggested_responses) == 3
```

### Integration Tests

```dart
// Test end-to-end with test backend
testWidgets('generates dialogue and displays in UI', (tester) async {
  await tester.pumpWidget(app);
  await tester.tap(find.byType(CardWidget));
  await tester.pumpAndSettle();
  
  expect(find.text('Hello, traveler!'), findsOneWidget);
});
```

### Load Tests

```python
# Backend load testing with Locust
class AIServiceUser(HttpUser):
    @task
    def generate_dialogue(self):
        self.client.post('/dialogue', json={
            'cardId': 'test_card',
            'context': 'Test context',
            'personalityTraits': {'extraversion': 0.8},
        })

# Run: locust -f load_test.py --users 100 --spawn-rate 10
```

## Cost Breakdown (Example)

### Monthly Cost Projection (1000 Users)

| Component | Usage | Cost |
|-----------|-------|------|
| **Cloud Run** | 100,000 requests | $2.00 |
| **Gemini API** | 50,000 dialogues | $3.50 |
| **Cloud CDN** | 1TB transfer | $8.00 |
| **Redis Cache** | 1GB memory | $5.00 |
| **Firestore** | 500k reads/writes | $1.50 |
| **Monitoring** | Standard tier | $3.00 |
| **Total** | | **$23.00** |

**With Caching Optimization**: ~$15/month (35% reduction)

### Cost Optimization Checklist

- [x] Enable aggressive caching (60%+ hit rate)
- [x] Use batch requests where possible
- [x] Implement smart model routing
- [x] Set request timeouts (prevent hanging)
- [x] Monitor and alert on cost spikes
- [ ] Consider reserved capacity (if scale justifies)
- [ ] Optimize prompt length (fewer tokens)
- [ ] Use cheaper models for simple tasks

## Future Enhancements

### Short Term (Q1 2026)

1. **Streaming Responses**: Progressive display for long narratives
2. **Advanced RAG**: Semantic search for story consistency
3. **Multi-Language**: Support for localized dialogues
4. **Voice Integration**: Text-to-speech for dialogues

### Medium Term (Q2-Q3 2026)

1. **Multi-Agent System**: Multiple AI characters interacting
2. **Fine-Tuned Models**: Custom models for Unwritten's style
3. **Edge Deployment**: On-device LLMs for premium users
4. **Predictive Pre-Loading**: Generate likely dialogues in advance

### Long Term (Q4 2026+)

1. **Fully Personalized**: AI learns from each player's style
2. **Real-Time Collaboration**: Multiplayer AI experiences
3. **Advanced Reasoning**: Complex puzzle and mystery solving
4. **Emotional Intelligence**: Detect and respond to player emotions

## Related Documentation

- [Genkit Integration Guide](../3.ai/genkit_integration_guide.md)
- [Genkit Quick Reference](../3.ai/genkit_quick_reference.md)
- [TFLite Integration](../3.ai/tensorflow_lite_integration.md)
- [Performance Optimization](./performance_optimization.md)

---

**Document Version**: 1.0  
**Last Updated**: October 15, 2025  
**Maintained By**: Unwritten AI Team

