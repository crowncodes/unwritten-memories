# AI Implementation Phases

**Purpose:** Phased implementation strategy from development to production  
**Audience:** All team members, product managers, engineers  
**Status:** ✅ Active Strategy  
**Related:** ← 01-ai-strategy-overview.md | → 04-ai-approach-comparison.md | 20-firebase-ai-integration.md | 30-genkit-architecture.md

---

## Current Implementation Strategy

**Development (Now - Weeks 1-8):** Firebase AI Logic for rapid content generation  
**Production (Target - Weeks 9-24):** Genkit backend as primary architecture  
**Current State:** 1 AI Studio cloud function (audio generation)

---

## Table of Contents

1. [Strategy Overview](#strategy-overview)
2. [Phase 1: Development & Content Generation](#phase-1-development--content-generation-weeks-1-8)
3. [Phase 2: Genkit Backend Development](#phase-2-genkit-backend-development-weeks-9-16)
4. [Phase 3: Migration](#phase-3-migration-weeks-17-24)
5. [Phase 4: Production](#phase-4-production-week-25)
6. [Feature Flags](#feature-flags)
7. [Success Metrics](#success-metrics)
8. [Risk Mitigation](#risk-mitigation)

---

## Strategy Overview

### Why This Phased Approach?

```
Week 1-8 (NOW):         Use Firebase AI Logic
                        ↓
                        • Generate training data FAST
                        • Populate game with content
                        • Test personality models with real content
                        • Rapid iteration on prompts

Week 9-16 (BUILD):      Build Genkit Backend Properly
                        ↓
                        • Production-ready architecture
                        • Complex flows (dialogue, story, evolution)
                        • RAG for story consistency
                        • Tool calling for game state integration

Week 17-24 (MIGRATE):   Gradual Migration
                        ↓
                        • Run both systems in parallel
                        • Feature-by-feature rollout
                        • Compare outputs and performance
                        • Ensure quality maintained

Week 25+ (PRODUCTION):  Genkit as Primary
                        ↓
                        • Genkit handles all AI features
                        • Firebase AI as fallback (optional)
                        • Monitor costs and performance
                        • Scale confidently
```

### Key Principle: Build Right from the Start

**We're NOT building a prototype Genkit to replace later.** We're building the production Genkit properly from week 9-16, while using Firebase AI as a temporary development tool.

---

## Phase 1: Development & Content Generation (Weeks 1-8)

### Objective
Use Firebase AI Logic to rapidly generate content and populate the game while building Genkit backend.

### What Firebase AI is Used For

#### Primary Use Cases:
1. **Training Data Generation**
   - Generate 1000+ dialogue examples
   - Create personality-trait-driven responses
   - Build card evolution examples
   - Test prompt templates at scale

2. **Game Content Population**
   - Generate card descriptions (200+ unique cards)
   - Create initial NPC dialogues
   - Populate story branches
   - Generate memory events

3. **Prompt Iteration**
   - Fast feedback loop (2-5 seconds per generation)
   - Test different prompt approaches
   - Validate OCEAN trait behavioral mapping
   - Refine templates based on output quality

4. **Model Testing**
   - Test Gemini Flash 2.5 performance
   - Test Gemini 2.5 Pro for complex scenarios
   - Benchmark costs and latency
   - Validate memory systems

### Implementation (Week 1-2)

#### Step 1: Firebase AI SDK Setup (2-4 hours)

**See:** `21-firebase-ai-quick-start.md` for complete setup

```dart
// lib/core/services/dev_ai_service.dart
import 'package:firebase_ai/firebase_ai.dart';

/// Development AI service using Firebase AI Logic
/// 
/// ⚠️ FOR DEVELOPMENT ONLY - Will be replaced by Genkit
class DevAIService {
  late final GenerativeModel _flashModel;
  late final GenerativeModel _proModel;
  
  DevAIService() {
    // Gemini Flash 2.5 for fast iterations
    _flashModel = FirebaseAI.googleAI().generativeModel(
      model: 'gemini-2.5-flash',
    );
    
    // Gemini 2.5 Pro for complex scenarios
    _proModel = FirebaseAI.googleAI().generativeModel(
      model: 'gemini-2.5-pro',
    );
  }
  
  /// Generate dialogue for development/testing
  Future<String> generateDevDialogue({
    required String cardName,
    required String context,
    required Map<String, double> personalityTraits,
  }) async {
    final prompt = _buildDialoguePrompt(cardName, context, personalityTraits);
    
    final response = await _flashModel.generateContent([
      Content.text(prompt),
    ]);
    
    return response.text ?? '';
  }
  
  /// Generate card description
  Future<String> generateCardDescription({
    required String cardName,
    required String archetype,
    required Map<String, double> oceanTraits,
  }) async {
    // Similar pattern...
  }
  
  String _buildDialoguePrompt(String name, String context, Map<String, double> traits) {
    // Use templates from 11-prompt-templates-library.md
    return '''
You are generating dialogue for $name in Unwritten.

OCEAN Traits:
- Openness: ${traits['openness']}
- Conscientiousness: ${traits['conscientiousness']}
- Extraversion: ${traits['extraversion']}
- Agreeableness: ${traits['agreeableness']}
- Neuroticism: ${traits['neuroticism']}

Context: $context

Generate natural, personality-consistent dialogue.
''';
  }
}
```

#### Step 2: Content Generation Scripts (Week 2)

```dart
// lib/dev_tools/content_generator.dart
import 'package:unwritten/core/services/dev_ai_service.dart';

/// Script to bulk-generate content for development
class ContentGenerator {
  final DevAIService _aiService;
  
  ContentGenerator(this._aiService);
  
  /// Generate 200 card descriptions
  Future<void> generateAllCardDescriptions() async {
    final cards = await _loadCardTemplates();
    
    for (final card in cards) {
      final description = await _aiService.generateCardDescription(
        cardName: card.name,
        archetype: card.archetype,
        oceanTraits: card.traits,
      );
      
      await _saveCardDescription(card.id, description);
      
      // Log progress
      AppLogger.info('Generated description for ${card.name}');
    }
  }
  
  /// Generate dialogue examples for training
  Future<void> generateTrainingDialogues() async {
    // Generate 1000+ examples for model training
    // ...
  }
}
```

### Development Workflow (Week 3-8)

```
Day-to-Day:
1. Run content generation scripts
2. Review generated content quality
3. Refine prompts based on output
4. Store good examples as training data
5. Populate game with content
6. Test gameplay with AI-generated content

Parallel Work:
- Frontend: Use generated content to build UI
- Backend: Start Genkit architecture (Phase 2)
- AI Team: Refine prompt templates
```

### Critical Notes for Phase 1

⚠️ **This is Development Only**
- Firebase AI is NOT for production
- No complex caching (simple is fine)
- No advanced error handling (basic try-catch OK)
- Focus on SPEED of content generation

✅ **What to Save**
- All generated training data
- Prompt templates that work well
- OCEAN trait → output quality correlations
- Cost/latency benchmarks

🔄 **What Will Change**
- Replace DevAIService with Genkit client
- Keep all the content generated
- Keep all the prompt templates (move to Genkit)

---

## Phase 2: Genkit Backend Development (Weeks 9-16)

### Objective
Build production-ready Genkit backend with Unwritten-specific architecture.

### Genkit Architecture for Unwritten

**See:** `30-genkit-architecture.md` for complete architecture

#### Backend Service Structure

```
unwritten-genkit-backend/
├── main.py                          # FastAPI app + Genkit config
├── flows/
│   ├── dialogue_generation_flow.py  # OCEAN-aware dialogue
│   ├── card_evolution_flow.py       # Level progression
│   ├── story_progression_flow.py    # Choice-based narrative
│   ├── relationship_calc_flow.py    # Trust/friendship mechanics
│   └── memory_generation_flow.py    # Event memory creation
├── tools/
│   ├── firestore_tools.py          # Game state access
│   ├── card_data_tools.py          # Card information retrieval
│   ├── player_history_tools.py     # Player interaction history
│   └── world_state_tools.py        # Global game state
├── rag/
│   ├── story_context.py            # Story consistency retrieval
│   ├── canonical_facts.py          # Canonical fact enforcement
│   └── character_memory.py         # Character memory retrieval
├── config/
│   ├── models.py                   # Pydantic models
│   └── settings.py                 # Environment config
├── requirements.txt
├── Dockerfile
└── README.md
```

### Core Flows Implementation (Week 9-12)

#### 1. Dialogue Generation Flow

**See:** `31-genkit-integration-guide.md` for implementation details

```python
# flows/dialogue_generation_flow.py
from genkit import flow, ai
from config.models import DialogueInput, DialogueOutput
from tools.card_data_tools import fetch_card_data
from tools.player_history_tools import fetch_player_interactions

@flow
async def dialogue_generation_flow(input: DialogueInput) -> DialogueOutput:
    """
    Generate OCEAN-aware dialogue for card interactions.
    
    This is the production replacement for DevAIService.generateDevDialogue()
    """
    # Fetch card data using tools
    card_data = await fetch_card_data(input.card_id)
    
    # Fetch player history for context
    history = await fetch_player_interactions(
        player_id=input.player_id,
        card_id=input.card_id,
        limit=5
    )
    
    # Build comprehensive prompt (use templates from 11-prompt-templates-library.md)
    prompt = f"""
You are generating dialogue for {card_data.name} in Unwritten.

OCEAN Personality Traits:
- Openness: {card_data.traits.openness:.2f}
- Conscientiousness: {card_data.traits.conscientiousness:.2f}
- Extraversion: {card_data.traits.extraversion:.2f}
- Agreeableness: {card_data.traits.agreeableness:.2f}
- Neuroticism: {card_data.traits.neuroticism:.2f}

Current Context:
{input.context}

Recent Interactions:
{_format_history(history)}

Generate natural, personality-consistent dialogue.
"""
    
    # Use Gemini 2.5 Flash (fast and cheap)
    response = await ai.generate(
        model='gemini-2.5-flash',
        prompt=prompt,
        output_schema=DialogueOutput,
    )
    
    return response.output
```

#### 2. Card Evolution Flow

```python
# flows/card_evolution_flow.py
@flow
async def card_evolution_flow(input: CardEvolutionInput) -> CardEvolutionOutput:
    """
    Handle card level progression (1→2, 2→3, 3→4, 4→5).
    
    Uses templates from 11-prompt-templates-library.md
    """
    # Fetch card current state
    card = await fetch_card_data(input.card_id)
    
    # Fetch all interactions for this evolution
    interactions = await fetch_player_interactions(
        player_id=input.player_id,
        card_id=input.card_id,
        since_level=card.current_level
    )
    
    # Use appropriate template based on level
    template = _get_evolution_template(
        current_level=card.current_level,
        target_level=card.current_level + 1
    )
    
    prompt = template.format(
        name=card.name,
        traits=card.traits,
        interactions=interactions,
        # ... more context
    )
    
    # Use Gemini 2.5 Pro for complex evolution
    response = await ai.generate(
        model='gemini-2.5-pro',
        prompt=prompt,
        output_schema=CardEvolutionOutput,
    )
    
    return response.output
```

### RAG Implementation (Week 13-14)

**Purpose:** Ensure story consistency across 3000+ weeks

```python
# rag/story_context.py
from genkit import embed, rag

# Initialize embedder
embedder = embed.google('text-embedding-004')

# Story context retrieval
async def retrieve_story_context(query: str) -> List[StoryEvent]:
    """
    Retrieve relevant story context for consistency.
    
    Searches past 3000 weeks of player history for relevant events.
    """
    # Embed query
    query_embedding = await embedder.embed(query)
    
    # Search Firestore vector collection
    results = await firestore_vector_search(
        collection='story_events',
        embedding=query_embedding,
        limit=10,
        threshold=0.7  # Similarity threshold
    )
    
    return results
```

### Tool Integration (Week 15-16)

**Tools allow Genkit to access game state**

```python
# tools/firestore_tools.py
from genkit import tool

@tool
async def fetch_card_data(card_id: str) -> dict:
    """
    Retrieve complete card data from Firestore.
    
    Returns personality traits, current level, relationship stats, etc.
    """
    doc = await firestore.collection('cards').document(card_id).get()
    return doc.to_dict()

@tool
async def update_relationship_score(
    player_id: str,
    card_id: str,
    delta: float
) -> dict:
    """
    Update trust/friendship score based on AI-determined impact.
    """
    # Update Firestore
    # Return new score
```

### Deployment to Cloud Run (Week 16)

**See:** `31-genkit-integration-guide.md` for complete deployment guide

```bash
# Deploy to Google Cloud Run
gcloud run deploy unwritten-genkit-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_AI_API_KEY=${GOOGLE_AI_API_KEY}

# Output:
# Service URL: https://unwritten-genkit-backend-xxx.run.app
```

### Flutter Client Integration (Week 16)

```dart
// lib/core/services/genkit_ai_service.dart
class GenkitAIService {
  static const String _baseUrl = 'https://unwritten-genkit-backend-xxx.run.app';
  final http.Client _client;
  
  GenkitAIService({http.Client? client}) 
      : _client = client ?? http.Client();
  
  /// Generate dialogue using Genkit backend
  Future<DialogueResponse> generateDialogue({
    required String cardId,
    required String playerId,
    required String context,
  }) async {
    final response = await _client.post(
      Uri.parse('$_baseUrl/dialogue_generation_flow'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'card_id': cardId,
        'player_id': playerId,
        'context': context,
      }),
    );
    
    if (response.statusCode == 200) {
      return DialogueResponse.fromJson(jsonDecode(response.body));
    } else {
      throw AIException('Genkit generation failed: ${response.statusCode}');
    }
  }
}
```

### Phase 2 Success Criteria

- [ ] Genkit backend deployed to Cloud Run
- [ ] All 5 core flows implemented (dialogue, evolution, story, relationship, memory)
- [ ] RAG system operational with story context
- [ ] Tools integrated (Firestore access, game state)
- [ ] Flutter client can call Genkit backend
- [ ] Performance tested (< 3 seconds per generation)
- [ ] Cost validated ($2-2.50/player/month achievable)

---

## Phase 3: Migration (Weeks 17-24)

### Objective
Gradually migrate from Firebase AI Logic to Genkit without disrupting players.

### Migration Strategy

#### Week 17-18: Parallel Running

**Run both systems side-by-side for comparison**

```dart
// lib/core/services/ai_service_manager.dart
class AIServiceManager {
  final DevAIService _devAI;         // Firebase AI Logic
  final GenkitAIService _genkitAI;   // Genkit backend
  final RemoteConfig _config;
  
  /// Generate dialogue using BOTH systems for comparison
  Future<DialogueResponse> generateDialogueWithComparison({
    required String cardId,
    required String playerId,
    required String context,
  }) async {
    // Run both in parallel
    final results = await Future.wait([
      _devAI.generateDevDialogue(/* params */),
      _genkitAI.generateDialogue(/* params */),
    ]);
    
    final devResult = results[0];
    final genkitResult = results[1];
    
    // Log comparison
    AppLogger.ai('Comparison', metrics: {
      'dev_length': devResult.length,
      'genkit_length': genkitResult.length,
      'dev_latency_ms': /* track */,
      'genkit_latency_ms': /* track */,
    });
    
    // Return dev result for now (players still see Firebase AI)
    return devResult;
  }
}
```

**Comparison Metrics:**
- Output quality (human review sample)
- Latency (should be similar)
- Cost (Genkit should be similar or better)
- Error rates

#### Week 19-21: Gradual Rollout

**Use feature flags to control which system is used**

```dart
// lib/core/services/ai_service_router.dart
class AIServiceRouter {
  final DevAIService _devAI;
  final GenkitAIService _genkitAI;
  final RemoteConfig _config;
  
  Future<DialogueResponse> generateDialogue({
    required String cardId,
    required String playerId,
    required String context,
  }) async {
    // Check feature flag
    final useGenkit = await _config.getBool('use_genkit_for_dialogue');
    final rolloutPercentage = await _config.getDouble('genkit_rollout_percentage');
    
    // Gradual rollout by user ID hash
    final userHash = _hashUserId(playerId);
    final useGenkitForUser = (userHash % 100) < rolloutPercentage;
    
    if (useGenkit && useGenkitForUser) {
      try {
        return await _genkitAI.generateDialogue(/* params */);
      } catch (e) {
        AppLogger.error('Genkit failed, falling back to dev AI', e);
        return await _devAI.generateDevDialogue(/* params */);
      }
    } else {
      return await _devAI.generateDevDialogue(/* params */);
    }
  }
}
```

**Rollout Schedule:**
- Week 19: 10% of users on Genkit
- Week 20: 50% of users on Genkit
- Week 21: 100% of users on Genkit

**Monitoring:**
- Dashboard with real-time metrics
- Alert if error rate > 1%
- Alert if latency > 5 seconds (p95)
- Cost tracking per approach

#### Week 22-24: Complete Migration

**Switch all features to Genkit**

```dart
// lib/core/services/ai_service.dart
class AIService {
  final GenkitAIService _genkit;
  final DevAIService _fallback;  // Keep as fallback
  
  Future<DialogueResponse> generateDialogue({
    required String cardId,
    required String playerId,
    required String context,
  }) async {
    try {
      // Primary: Genkit
      return await _genkit.generateDialogue(/* params */);
    } catch (e, stack) {
      AppLogger.error('Genkit failed, using fallback', e, stack);
      
      // Fallback: Firebase AI Logic (offline scenarios)
      return await _fallback.generateDevDialogue(/* params */);
    }
  }
}
```

### Rollback Plan

**If issues arise, roll back using feature flags:**

```dart
// Remote Config
{
  "use_genkit_for_dialogue": false,  // Flip to false to roll back
  "genkit_rollout_percentage": 0.0   // Set to 0 to roll back
}
```

**Rollback Triggers:**
- Error rate > 5%
- Latency p95 > 8 seconds
- Cost > $3.50/player/month
- Quality degradation (user complaints)

### Phase 3 Success Criteria

- [ ] Both systems run in parallel successfully (Week 17-18)
- [ ] Genkit quality matches or exceeds Firebase AI (comparative analysis)
- [ ] Rollout to 100% users without incidents (Week 19-21)
- [ ] All features migrated to Genkit (Week 22-24)
- [ ] Fallback system tested and working
- [ ] Cost and performance targets met

---

## Phase 4: Production (Week 25+)

### Objective
Run Genkit as primary system with monitoring and optimization.

### Production Architecture

```
Player (Flutter App)
        ↓
GenkitAIService (HTTP client)
        ↓
Cloud Run (Genkit Backend)
        ├→ Gemini 2.5 Flash (fast generations)
        ├→ Gemini 2.5 Pro (complex generations)
        ├→ Firestore (game state via tools)
        └→ RAG (story consistency)
        
Fallback Path (offline):
DevAIService → Firebase AI Logic → Gemini (direct)
```

### Monitoring Dashboard

**Key Metrics:**
- Requests per minute
- Latency (p50, p95, p99)
- Error rate
- Cost per player per day
- Model usage (Flash vs Pro percentage)
- Quality scores (automated + human review)

**Alerts:**
- Error rate > 2% (warning), > 5% (critical)
- Latency p95 > 5s (warning), > 10s (critical)
- Cost per player > $3.00/month (warning), > $4.00/month (critical)

### Optimization Strategies

**See:** `71-cost-performance-targets.md` for complete optimization guide

1. **Caching** (80% hit rate target)
   - Cache common dialogue responses
   - Cache card evolution outcomes
   - TTL: 24 hours for dynamic content, 7 days for static

2. **Smart Model Selection**
   - Use Flash for simple dialogues (80% of requests)
   - Use Pro only for complex scenarios (20% of requests)
   - Auto-select based on complexity score

3. **Request Batching**
   - Batch multiple AI requests in single flow
   - Reduce Cloud Run cold starts

4. **Pre-Generation**
   - Pre-generate likely player choices
   - Pre-compute evolution dialogues for active cards

### Cost Monitoring

**Target:** $2.00 - $2.50 per player per month

**Breakdown:**
- Gemini Flash calls: $1.50/month (70% of generations)
- Gemini Pro calls: $0.75/month (20% of generations)
- Cloud Run hosting: $0.25/month
- Caching savings: -$0.50/month

**Monthly Review:**
- Analyze cost trends
- Optimize expensive flows
- Adjust caching strategy
- Fine-tune model selection

### Phase 4 Success Criteria

- [ ] 99.9% uptime
- [ ] Latency p95 < 3 seconds
- [ ] Cost per player $2.00-2.50/month
- [ ] Error rate < 1%
- [ ] Quality maintained or improved
- [ ] Monitoring dashboard operational
- [ ] Cost alerts configured

---

## Feature Flags

### Remote Config Setup

```dart
// lib/core/config/feature_flags.dart
class FeatureFlags {
  static const String USE_GENKIT = 'use_genkit_for_dialogue';
  static const String GENKIT_ROLLOUT_PERCENTAGE = 'genkit_rollout_percentage';
  static const String USE_GENKIT_FOR_EVOLUTION = 'use_genkit_for_evolution';
  static const String USE_GENKIT_FOR_STORY = 'use_genkit_for_story';
}
```

### Flag States by Phase

| Phase | Dialogue | Evolution | Story | Rollout % |
|-------|----------|-----------|-------|-----------|
| **Phase 1 (Dev)** | false | false | false | 0% |
| **Phase 2 (Build)** | false | false | false | 0% |
| **Phase 3 Week 17-18** | true | false | false | 0% (parallel only) |
| **Phase 3 Week 19** | true | false | false | 10% |
| **Phase 3 Week 20** | true | false | false | 50% |
| **Phase 3 Week 21** | true | true | false | 100% |
| **Phase 3 Week 22** | true | true | true | 100% |
| **Phase 4 (Prod)** | true | true | true | 100% |

---

## Success Metrics

### Phase 1 Success (Week 1-8)
- ✅ Firebase AI SDK integrated
- ✅ 200+ card descriptions generated
- ✅ 1000+ training dialogues created
- ✅ Prompt templates validated
- ✅ Cost benchmarks established ($0.01-0.02 per generation)

### Phase 2 Success (Week 9-16)
- ✅ Genkit backend deployed to Cloud Run
- ✅ 5 core flows operational
- ✅ RAG system working
- ✅ Tools integrated with Firestore
- ✅ Flutter client tested
- ✅ Performance validated (< 3s latency)

### Phase 3 Success (Week 17-24)
- ✅ Parallel comparison completed
- ✅ Quality parity confirmed
- ✅ 100% rollout successful
- ✅ Zero rollbacks required
- ✅ Cost targets met

### Phase 4 Success (Week 25+)
- ✅ 99.9% uptime achieved
- ✅ Cost per player $2-2.50/month
- ✅ Latency p95 < 3 seconds
- ✅ Error rate < 1%
- ✅ Quality maintained

---

## Risk Mitigation

### Risk 1: Genkit Development Takes Longer Than Expected

**Mitigation:**
- Keep using Firebase AI for development (no blocker)
- Extend Phase 1 as needed
- Genkit quality > Genkit speed

**Fallback:**
- If Genkit significantly delayed (>4 weeks), consider Firebase AI for MVP
- Re-evaluate timeline quarterly

### Risk 2: Quality Degradation During Migration

**Mitigation:**
- Comparative analysis before rollout
- Gradual rollout with monitoring
- Instant rollback via feature flags
- Keep Firebase AI as fallback

**Detection:**
- Automated quality scoring
- User feedback monitoring
- A/B testing results

### Risk 3: Cost Overruns

**Mitigation:**
- Extensive caching (80% hit rate)
- Smart model selection (Flash vs Pro)
- Pre-generation for likely scenarios
- Rate limiting per player

**Monitoring:**
- Daily cost alerts
- Per-player cost tracking
- Monthly cost reviews

### Risk 4: Cloud Run Downtime

**Mitigation:**
- Multi-region deployment
- Firebase AI Logic as fallback
- Cached responses for offline
- Graceful degradation

**SLA Target:** 99.9% uptime (43 minutes downtime/month acceptable)

---

## Related Documentation

- **01-ai-strategy-overview.md** - High-level AI strategy and constraints
- **04-ai-approach-comparison.md** - Why Firebase AI vs Genkit vs TFLite
- **20-firebase-ai-integration.md** - Complete Firebase AI reference
- **21-firebase-ai-quick-start.md** - 30-minute Firebase AI setup
- **30-genkit-architecture.md** - Unwritten-specific Genkit design
- **31-genkit-integration-guide.md** - Complete Genkit implementation
- **34-migration-firebase-to-genkit.md** - Detailed migration guide
- **71-cost-performance-targets.md** - Cost optimization strategies

---

**Implementation Status:** 📝 Planning Complete - Ready for Phase 1
**Timeline:** 24 weeks (6 months) from development to production
**Next Step:** Begin Phase 1 - Firebase AI SDK integration (Week 1)


