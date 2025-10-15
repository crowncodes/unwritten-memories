# Genkit Integration Guide for Unwritten

## Overview

This guide explains how to integrate Firebase Genkit into the Unwritten Flutter application to enhance AI capabilities through a Python backend service. Genkit provides a comprehensive framework for building AI-powered workflows, managing model interactions, and deploying scalable AI services.

## What is Genkit?

Firebase Genkit is a framework designed to facilitate the development of AI-powered applications by providing:

- **Unified AI Model Interface**: Work with multiple AI providers (Google Generative AI, OpenAI, Anthropic, etc.)
- **Workflow Management**: Define complex AI workflows (flows) with pre/post-processing
- **Tool Calling**: Enable AI models to interact with external functions and APIs
- **RAG Support**: Retrieval-Augmented Generation for context-aware responses
- **Developer Tools**: Local UI for testing and debugging AI workflows
- **Production-Ready Deployment**: Built-in support for Cloud Run and other platforms

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Flutter App (Unwritten)                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  AI Features (lib/features/ai/)                      │   │
│  │  - Card personality inference (TFLite - on-device)   │   │
│  │  - Dialogue generation (Genkit backend)             │   │
│  │  - Story progression (Genkit backend)               │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS/WebSocket
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Genkit Python Backend Service                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  AI Flows                                            │   │
│  │  - dialogue_generation_flow                         │   │
│  │  - story_progression_flow                           │   │
│  │  - character_interaction_flow                       │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Tools (External Functions)                          │   │
│  │  - fetch_card_data                                   │   │
│  │  - check_relationship_status                         │   │
│  │  - get_story_context                                │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  RAG Components (Optional)                           │   │
│  │  - Story context retriever                          │   │
│  │  - Character memory embedder                        │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           Google Generative AI / Other Providers             │
│              (Gemini 2.5 Flash, etc.)                       │
└─────────────────────────────────────────────────────────────┘
```

## Why Use Genkit with Unwritten?

### Hybrid Approach: TFLite + Genkit

**On-Device (TFLite - Current Implementation)**:
- ✅ Fast personality trait inference (< 15ms)
- ✅ No network latency
- ✅ Works offline
- ✅ Privacy-preserving
- ❌ Limited model complexity
- ❌ Fixed models (requires app update to change)

**Cloud-Based (Genkit Backend - New Addition)**:
- ✅ Powerful language models for dialogue/narrative
- ✅ Easy to update and improve
- ✅ Access to latest AI capabilities
- ✅ Complex reasoning and creativity
- ❌ Requires network connection
- ❌ Potential latency
- ❌ Cost per API call

### Recommended Split

| Feature | Implementation |
|---------|---------------|
| Personality inference (Big 5 traits) | **TFLite** (on-device) |
| Sentiment analysis | **TFLite** (on-device) |
| Relationship scoring | **TFLite** (on-device) |
| Dynamic dialogue generation | **Genkit** (backend) |
| Story narrative generation | **Genkit** (backend) |
| Complex character interactions | **Genkit** (backend) |
| Multi-turn conversations | **Genkit** (backend) |

## Installation & Setup

### 1. Backend Setup (Python + Genkit)

#### Install Dependencies

```bash
# Install Genkit CLI (Node.js required)
npm install -g genkit-cli

# Create Python virtual environment
python -m venv genkit-env
source genkit-env/bin/activate  # On Windows: genkit-env\Scripts\activate

# Install Genkit Python SDK
pip install genkit google-genkit-ai
```

#### Project Structure

Create a new backend service directory:

```
unwritten-backend/
├── main.py                    # Entry point
├── flows/
│   ├── __init__.py
│   ├── dialogue_flow.py      # Dialogue generation
│   ├── story_flow.py         # Story progression
│   └── character_flow.py     # Character interactions
├── tools/
│   ├── __init__.py
│   ├── game_tools.py         # Game state tools
│   └── data_tools.py         # Data retrieval tools
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration
├── requirements.txt
└── Dockerfile                # For deployment
```

### 2. Flutter App Configuration

#### Add HTTP Package

Update `app/pubspec.yaml`:

```yaml
dependencies:
  # ... existing dependencies
  http: ^1.2.0
  web_socket_channel: ^2.4.0  # For real-time features (optional)
```

#### Create Genkit Service Client

Create `lib/shared/services/genkit_service.dart`:

```dart
/// Service for interacting with Genkit backend.
/// 
/// Handles communication with the Python Genkit service
/// for AI-powered dialogue and narrative generation.
/// 
/// Performance: 
/// - Average latency: 800-1500ms (includes model inference)
/// - Implements caching to reduce API calls
/// - Falls back to rule-based system on failure
class GenkitService {
  static const String _baseUrl = 'https://your-cloud-run-url';
  final http.Client _client;
  
  GenkitService({http.Client? client}) 
      : _client = client ?? http.Client();
  
  /// Generates dialogue for a character interaction.
  /// 
  /// Uses the backend's dialogue_generation_flow.
  /// Caches responses for common interactions.
  Future<DialogueResponse> generateDialogue({
    required String cardId,
    required String context,
    required Map<String, double> personalityTraits,
  }) async {
    final stopwatch = Stopwatch()..start();
    
    try {
      final response = await _client.post(
        Uri.parse('$_baseUrl/dialogue'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'cardId': cardId,
          'context': context,
          'personalityTraits': personalityTraits,
        }),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        
        AppLogger.ai('Dialogue generated', metrics: {
          'duration_ms': stopwatch.elapsedMilliseconds,
          'card_id': cardId,
        });
        
        return DialogueResponse.fromJson(data);
      } else {
        throw GenkitException('Failed to generate dialogue: ${response.statusCode}');
      }
    } catch (e, stack) {
      AppLogger.error('Dialogue generation failed', e, stack);
      // Fallback to rule-based system
      return _generateFallbackDialogue(cardId, context);
    }
  }
  
  /// Fallback dialogue generation using rule-based system.
  DialogueResponse _generateFallbackDialogue(String cardId, String context) {
    // Implementation of rule-based fallback
    return DialogueResponse(
      text: _getRuleBasedDialogue(cardId, context),
      isFallback: true,
    );
  }
  
  void dispose() {
    _client.close();
  }
}
```

## Developer Tools

### Genkit CLI Commands

```bash
# Start Developer UI with your backend
genkit start -- python3 main.py

# Open in browser automatically
genkit start -o -- python3 main.py

# Run a specific flow (backend must be running)
genkit flow:run dialogue_generation_flow

# Evaluate a flow
genkit eval:flow dialogue_generation_flow

# View help
genkit --help
```

### Developer UI Features

The Genkit Developer UI (runs on `http://localhost:4000`) provides:

- **Flow Testing**: Test AI workflows interactively
- **Model Testing**: Try different models and parameters
- **Prompt Management**: Edit and test prompts in real-time
- **Trace Inspection**: View detailed execution traces
- **Performance Metrics**: Monitor latency and token usage

**Recommended Workflow**:
1. Start the Developer UI: `genkit start -o -- python3 main.py`
2. Test flows with sample inputs
3. Inspect traces to identify performance bottlenecks
4. Iterate on prompts and configurations
5. Run evaluations before deployment

## Core Features

### 1. AI Models (`ai.generate()`)

#### Basic Usage

```python
from genkit import ai
from genkit_google_genai import googleAI

# Configure AI with Google Generative AI
ai.configure(
    plugins=[googleAI()],
    model=googleAI.model('gemini-2.5-flash')  # Default model
)

# Generate content
response = await ai.generate("Generate a mysterious dialogue for a character meeting")
```

#### With Structured Output

```python
from pydantic import BaseModel

class DialogueOutput(BaseModel):
    text: str
    emotion: str
    tone: str

response = await ai.generate(
    prompt="Generate dialogue for meeting a mysterious character",
    output_schema=DialogueOutput
)

# Access structured data
dialogue = response.output  # Type: DialogueOutput
print(dialogue.text)
print(dialogue.emotion)
```

#### Multimodal Input (Optional)

If you want to analyze card artwork:

```python
from genkit.ai import Part

result = await ai.generate(
    prompt=[
        Part(media={'url': 'https://your-cdn.com/card-image.jpg'}),
        Part(text='Describe the personality this character might have based on their appearance.'),
    ],
)
```

### 2. Flows (Workflows)

Flows encapsulate complete AI workflows with input validation, pre/post-processing, and error handling.

#### Define a Dialogue Flow

Create `flows/dialogue_flow.py`:

```python
from genkit import flow
from pydantic import BaseModel
from typing import Dict

class DialogueInput(BaseModel):
    card_id: str
    context: str
    personality_traits: Dict[str, float]
    previous_interactions: int = 0

class DialogueOutput(BaseModel):
    text: str
    emotion: str
    tone: str
    suggested_responses: list[str]

@flow
async def dialogue_generation_flow(input: DialogueInput) -> DialogueOutput:
    """
    Generates contextual dialogue for card interactions.
    
    Takes personality traits from TFLite inference and generates
    appropriate dialogue based on game context.
    
    Performance: 800-1200ms average latency
    """
    
    # Pre-processing: Build context from personality traits
    personality_desc = build_personality_description(input.personality_traits)
    
    # Build prompt with context
    prompt = f"""
    You are generating dialogue for a character in a narrative card game.
    
    Character Personality:
    {personality_desc}
    
    Game Context:
    {input.context}
    
    Previous Interactions: {input.previous_interactions}
    
    Generate appropriate dialogue that:
    - Reflects the character's personality traits
    - Fits the current game context
    - Feels natural and engaging
    - Includes emotion and tone markers
    - Suggests 3 player response options
    
    Output as JSON with: text, emotion, tone, suggested_responses
    """
    
    # Generate with model
    response = await ai.generate(
        prompt=prompt,
        output_schema=DialogueOutput
    )
    
    return response.output

def build_personality_description(traits: Dict[str, float]) -> str:
    """Convert Big 5 traits to natural language description."""
    # Implementation based on trait values
    descriptions = []
    
    if traits.get('openness', 0.5) > 0.7:
        descriptions.append("highly creative and open to new experiences")
    
    if traits.get('extraversion', 0.5) > 0.7:
        descriptions.append("outgoing and energetic")
    elif traits.get('extraversion', 0.5) < 0.3:
        descriptions.append("reserved and introspective")
    
    # ... more trait descriptions
    
    return ", ".join(descriptions)
```

### 3. Tool Calling

Enable AI models to call external functions during generation.

#### Define Tools

Create `tools/game_tools.py`:

```python
from genkit import tool

@tool
async def fetch_card_data(card_id: str) -> dict:
    """
    Retrieves card data from the game database.
    
    Used by AI to access card information during dialogue generation.
    """
    # Query your database/API
    card = await get_card_from_db(card_id)
    
    return {
        'name': card.name,
        'rarity': card.rarity,
        'backstory': card.backstory,
        'abilities': card.abilities,
    }

@tool
async def check_relationship_status(player_id: str, card_id: str) -> dict:
    """
    Checks the relationship level between player and card.
    
    Returns relationship score and history.
    """
    relationship = await get_relationship(player_id, card_id)
    
    return {
        'level': relationship.level,
        'score': relationship.score,
        'interactions': relationship.total_interactions,
        'memorable_moments': relationship.key_events[:3],
    }

@tool
async def get_story_context(player_id: str) -> dict:
    """
    Retrieves current story state and progress.
    
    Provides context about player's journey.
    """
    story_state = await get_player_story_state(player_id)
    
    return {
        'current_chapter': story_state.chapter,
        'completed_arcs': story_state.completed_arcs,
        'active_quests': story_state.active_quests,
        'story_flags': story_state.flags,
    }
```

#### Use Tools in Flows

```python
@flow
async def character_interaction_flow(input: InteractionInput) -> InteractionOutput:
    """
    Handles complex character interactions with access to game state.
    
    Uses tools to fetch relevant data during generation.
    """
    
    # Define tools for this flow
    tools = [fetch_card_data, check_relationship_status, get_story_context]
    
    prompt = f"""
    Generate a character interaction based on the current game state.
    Use the available tools to fetch necessary information.
    
    Player ID: {input.player_id}
    Card ID: {input.card_id}
    Interaction Type: {input.interaction_type}
    """
    
    response = await ai.generate(
        prompt=prompt,
        tools=tools,
        output_schema=InteractionOutput
    )
    
    return response.output
```

### 4. Retrieval-Augmented Generation (RAG)

RAG enhances responses by retrieving relevant information from external sources.

#### Setup RAG Components

Create `rag/story_retriever.py`:

```python
from genkit import retriever, embedder, indexer
from genkit_google_genai import googleAI

# Configure embedder for vector search
@embedder
def story_embedder():
    return googleAI.embedder('text-embedding-004')

# Define retriever for story context
@retriever
async def story_context_retriever(query: str) -> list[dict]:
    """
    Retrieves relevant story context based on semantic search.
    
    Used to provide consistent narrative across interactions.
    """
    # Embed the query
    query_embedding = await story_embedder().embed(query)
    
    # Search vector database (e.g., Pinecone, Chroma)
    results = await vector_db.search(
        embedding=query_embedding,
        top_k=5
    )
    
    return [
        {
            'content': doc.content,
            'metadata': doc.metadata,
            'relevance': doc.score,
        }
        for doc in results
    ]

# Define indexer for storing story content
@indexer
async def story_indexer(documents: list[dict]):
    """
    Indexes story content for RAG retrieval.
    
    Run this when adding new story content.
    """
    for doc in documents:
        # Generate embedding
        embedding = await story_embedder().embed(doc['content'])
        
        # Store in vector database
        await vector_db.upsert(
            id=doc['id'],
            embedding=embedding,
            content=doc['content'],
            metadata=doc['metadata'],
        )
```

#### Use RAG in Flows

```python
@flow
async def story_progression_flow(input: StoryInput) -> StoryOutput:
    """
    Generates story progression with consistent narrative context.
    
    Uses RAG to maintain story coherence across sessions.
    """
    
    # Retrieve relevant story context
    context_docs = await story_context_retriever(
        query=f"Story context for {input.player_id} at chapter {input.current_chapter}"
    )
    
    # Build context string
    context = "\n".join([doc['content'] for doc in context_docs])
    
    prompt = f"""
    Continue the story based on the following context:
    
    Previous Story Context:
    {context}
    
    Current Situation:
    {input.current_situation}
    
    Player Choices:
    {input.recent_choices}
    
    Generate the next story beat that:
    - Maintains narrative consistency
    - Responds to player choices
    - Advances the plot meaningfully
    - Creates emotional engagement
    """
    
    response = await ai.generate(
        prompt=prompt,
        output_schema=StoryOutput
    )
    
    return response.output
```

## Deployment

### Deploy to Google Cloud Run

#### 1. Create Dockerfile

Create `Dockerfile` in your backend directory:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Cloud Run uses PORT env variable)
ENV PORT=8080
EXPOSE 8080

# Run the application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
```

#### 2. Deploy to Cloud Run

```bash
# Authenticate with Google Cloud
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy unwritten-ai-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 60s \
  --min-instances 0 \
  --max-instances 10
```

#### 3. Update Flutter App Configuration

After deployment, update your Flutter app with the Cloud Run URL:

Create `lib/core/constants/api_config.dart`:

```dart
/// API configuration for Genkit backend service.
class ApiConfig {
  // Use environment variables for different builds
  static const String genkitBaseUrl = String.fromEnvironment(
    'GENKIT_BASE_URL',
    defaultValue: 'https://unwritten-ai-backend-xxxxx.run.app',
  );
  
  static const Duration requestTimeout = Duration(seconds: 30);
  static const int maxRetries = 2;
}
```

Build with environment variable:

```bash
flutter build apk --dart-define=GENKIT_BASE_URL=https://your-actual-url.run.app
```

## Integration Patterns

### Pattern 1: Enhanced Dialogue System

```dart
// lib/features/ai/data/repositories/ai_repository_impl.dart

class AIRepositoryImpl implements AIRepository {
  final AIService _tfliteService;  // Existing TFLite service
  final GenkitService _genkitService;  // New Genkit service
  final CacheService _cache;
  
  @override
  Future<DialogueResponse> generateDialogue({
    required Card card,
    required GameContext context,
  }) async {
    // Step 1: Use TFLite for fast personality inference (on-device)
    final personality = await _tfliteService.inferPersonality(card);
    
    AppLogger.ai('Personality inferred', metrics: {
      'card_id': card.id,
      'openness': personality.openness,
      'extraversion': personality.extraversion,
    });
    
    // Step 2: Check cache for similar dialogue
    final cacheKey = '${card.id}_${context.hashCode}';
    final cached = await _cache.get(cacheKey);
    if (cached != null) {
      return cached;
    }
    
    // Step 3: Use Genkit for creative dialogue generation (backend)
    try {
      final response = await _genkitService.generateDialogue(
        cardId: card.id,
        context: context.toString(),
        personalityTraits: personality.toMap(),
      );
      
      // Cache the result
      await _cache.set(cacheKey, response, duration: Duration(hours: 1));
      
      return response;
    } catch (e) {
      // Fallback to rule-based system
      AppLogger.error('Genkit dialogue failed, using fallback', e);
      return _generateRuleBasedDialogue(card, personality, context);
    }
  }
}
```

### Pattern 2: Battery-Aware AI

```dart
/// Battery-aware AI service that adapts based on device state.
/// 
/// Reduces Genkit API calls when battery is low.
class BatteryAwareAIService {
  final GenkitService _genkitService;
  final AIService _tfliteService;
  final Battery _battery;
  
  Future<DialogueResponse> generateDialogue({
    required Card card,
    required GameContext context,
  }) async {
    final batteryLevel = await _battery.batteryLevel;
    final batteryState = await _battery.batteryState;
    
    // Use on-device only when battery is low or charging unavailable
    if (batteryLevel < 20 && batteryState != BatteryState.charging) {
      AppLogger.performance(
        'Low battery: using on-device inference only',
        Duration.zero,
      );
      return _tfliteService.generateSimpleDialogue(card, context);
    }
    
    // Use Genkit for rich dialogue when battery is sufficient
    return _genkitService.generateDialogue(
      cardId: card.id,
      context: context.toString(),
      personalityTraits: await _tfliteService.inferPersonality(card).then((p) => p.toMap()),
    );
  }
}
```

### Pattern 3: Offline-First with Sync

```dart
/// Offline-first AI service with background sync.
/// 
/// Queues Genkit requests when offline and syncs when connected.
class OfflineFirstAIService {
  final GenkitService _genkitService;
  final LocalStorageService _storage;
  final ConnectivityService _connectivity;
  
  Future<DialogueResponse> generateDialogue({
    required Card card,
    required GameContext context,
  }) async {
    final isOnline = await _connectivity.isConnected;
    
    if (!isOnline) {
      // Use cached or rule-based responses
      return _getCachedOrRuleBasedDialogue(card, context);
    }
    
    try {
      // Try online generation
      final response = await _genkitService.generateDialogue(
        cardId: card.id,
        context: context.toString(),
        personalityTraits: {},
      );
      
      // Cache for offline use
      await _storage.cacheDialogue(card.id, context, response);
      
      return response;
    } catch (e) {
      // Network error: queue for later retry
      await _queueForRetry(card, context);
      return _getCachedOrRuleBasedDialogue(card, context);
    }
  }
  
  /// Background sync for queued requests
  Future<void> syncQueuedRequests() async {
    final queued = await _storage.getQueuedRequests();
    
    for (final request in queued) {
      try {
        await _genkitService.generateDialogue(
          cardId: request.cardId,
          context: request.context,
          personalityTraits: request.traits,
        );
        await _storage.removeFromQueue(request.id);
      } catch (e) {
        AppLogger.error('Failed to sync queued request', e);
      }
    }
  }
}
```

## Performance Optimization

### 1. Request Batching

```python
# Backend: flows/batch_flow.py

@flow
async def batch_dialogue_flow(input: BatchDialogueInput) -> BatchDialogueOutput:
    """
    Generates multiple dialogues in a single request.
    
    Reduces network overhead by batching requests.
    """
    
    results = []
    
    # Generate all dialogues in parallel
    tasks = [
        generate_single_dialogue(item)
        for item in input.items
    ]
    
    results = await asyncio.gather(*tasks)
    
    return BatchDialogueOutput(dialogues=results)
```

```dart
// Flutter: Batch multiple requests
final responses = await _genkitService.generateBatchDialogues(
  requests: [
    DialogueRequest(cardId: 'card1', context: 'context1'),
    DialogueRequest(cardId: 'card2', context: 'context2'),
    DialogueRequest(cardId: 'card3', context: 'context3'),
  ],
);
```

### 2. Response Streaming

For long narrative generation, use streaming:

```python
# Backend: Enable streaming
@flow
async def story_streaming_flow(input: StoryInput):
    """Generates story with streaming for progressive display."""
    
    async for chunk in ai.generate_stream(prompt=build_prompt(input)):
        yield chunk
```

```dart
// Flutter: Handle streaming responses
Stream<String> streamStory(StoryRequest request) async* {
  final response = await _client.send(
    http.Request('POST', Uri.parse('$_baseUrl/story/stream'))
      ..headers.addAll({'Content-Type': 'application/json'})
      ..body = jsonEncode(request.toJson()),
  );
  
  await for (final chunk in response.stream.transform(utf8.decoder)) {
    yield chunk;
  }
}
```

### 3. Caching Strategy

```dart
/// Multi-level caching for AI responses.
/// 
/// - Memory cache: Fast access for recent requests
/// - Disk cache: Persistent storage for offline use
/// - Network: Fresh generation from Genkit
class AIResponseCache {
  final MemoryCache _memory;
  final DiskCache _disk;
  
  Future<DialogueResponse?> get(String key) async {
    // Try memory first
    var cached = _memory.get(key);
    if (cached != null) {
      AppLogger.performance('Memory cache hit', Duration.zero);
      return cached;
    }
    
    // Try disk
    cached = await _disk.get(key);
    if (cached != null) {
      AppLogger.performance('Disk cache hit', Duration.zero);
      // Promote to memory
      _memory.set(key, cached);
      return cached;
    }
    
    return null;
  }
  
  Future<void> set(String key, DialogueResponse response) async {
    _memory.set(key, response);
    await _disk.set(key, response);
  }
}
```

## Monitoring & Analytics

### Backend Monitoring

```python
# Enable Genkit telemetry
from genkit import telemetry

telemetry.configure(
    export_to='cloud_monitoring',  # Google Cloud Monitoring
    log_level='INFO',
)

# Track custom metrics
@flow
async def monitored_dialogue_flow(input: DialogueInput) -> DialogueOutput:
    with telemetry.span('dialogue_generation') as span:
        span.set_attribute('card_id', input.card_id)
        span.set_attribute('has_context', bool(input.context))
        
        result = await generate_dialogue(input)
        
        span.set_attribute('response_length', len(result.text))
        span.set_attribute('emotion', result.emotion)
        
        return result
```

### Flutter Monitoring

```dart
/// Track AI service performance
class AIAnalytics {
  static void trackDialogueGeneration({
    required Duration duration,
    required bool fromCache,
    required bool success,
  }) {
    FirebaseAnalytics.instance.logEvent(
      name: 'ai_dialogue_generated',
      parameters: {
        'duration_ms': duration.inMilliseconds,
        'from_cache': fromCache,
        'success': success,
      },
    );
    
    // Log performance warning if slow
    if (duration.inMilliseconds > 2000) {
      AppLogger.performance(
        'Slow dialogue generation',
        duration,
      );
    }
  }
}
```

## Error Handling

### Backend Error Handling

```python
from genkit import flow
from genkit.errors import GenkitError

class DialogueGenerationError(GenkitError):
    """Custom error for dialogue generation failures."""
    pass

@flow
async def safe_dialogue_flow(input: DialogueInput) -> DialogueOutput:
    """
    Dialogue flow with comprehensive error handling.
    """
    
    try:
        # Validate input
        if not input.card_id:
            raise ValueError("card_id is required")
        
        if not input.personality_traits:
            raise ValueError("personality_traits are required")
        
        # Generate dialogue
        result = await generate_dialogue(input)
        
        # Validate output
        if not result.text or len(result.text) < 10:
            raise DialogueGenerationError("Generated dialogue too short")
        
        return result
        
    except ValueError as e:
        # Input validation errors
        raise DialogueGenerationError(f"Invalid input: {e}")
        
    except TimeoutError:
        # Model timeout
        raise DialogueGenerationError("Model inference timeout")
        
    except Exception as e:
        # Unexpected errors
        raise DialogueGenerationError(f"Unexpected error: {e}")
```

### Flutter Error Handling

```dart
class GenkitException implements Exception {
  final String message;
  final int? statusCode;
  final dynamic originalError;
  
  GenkitException(this.message, {this.statusCode, this.originalError});
  
  @override
  String toString() => 'GenkitException: $message';
}

extension GenkitServiceErrors on GenkitService {
  Future<T> handleErrors<T>(Future<T> Function() operation) async {
    try {
      return await operation();
    } on SocketException {
      throw GenkitException('Network connection failed');
    } on TimeoutException {
      throw GenkitException('Request timeout');
    } on FormatException {
      throw GenkitException('Invalid response format');
    } on http.ClientException catch (e) {
      throw GenkitException('HTTP client error: $e');
    } catch (e) {
      throw GenkitException('Unexpected error: $e', originalError: e);
    }
  }
}
```

## Testing

### Backend Testing

```python
# tests/test_dialogue_flow.py

import pytest
from flows.dialogue_flow import dialogue_generation_flow, DialogueInput

@pytest.mark.asyncio
async def test_dialogue_generation():
    """Test dialogue generation with valid input."""
    
    input_data = DialogueInput(
        card_id='test_card_1',
        context='Player meets character for first time',
        personality_traits={
            'openness': 0.8,
            'extraversion': 0.6,
            'agreeableness': 0.7,
            'conscientiousness': 0.5,
            'neuroticism': 0.3,
        },
        previous_interactions=0,
    )
    
    result = await dialogue_generation_flow(input_data)
    
    assert result.text
    assert len(result.text) > 20
    assert result.emotion in ['happy', 'neutral', 'curious', 'mysterious']
    assert len(result.suggested_responses) == 3

@pytest.mark.asyncio
async def test_dialogue_with_high_extraversion():
    """Test that high extraversion produces energetic dialogue."""
    
    input_data = DialogueInput(
        card_id='test_card_2',
        context='Casual conversation',
        personality_traits={'extraversion': 0.9},
    )
    
    result = await dialogue_generation_flow(input_data)
    
    # Verify energetic tone
    assert result.tone in ['energetic', 'enthusiastic', 'outgoing']
```

### Flutter Testing

```dart
// test/shared/services/genkit_service_test.dart

void main() {
  group('GenkitService', () {
    late GenkitService service;
    late MockHttpClient mockClient;
    
    setUp(() {
      mockClient = MockHttpClient();
      service = GenkitService(client: mockClient);
    });
    
    test('generateDialogue returns valid response', () async {
      // Arrange
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response(
        jsonEncode({
          'text': 'Hello, traveler!',
          'emotion': 'friendly',
          'tone': 'welcoming',
          'suggested_responses': ['Hello', 'Who are you?', 'Leave'],
        }),
        200,
      ));
      
      // Act
      final response = await service.generateDialogue(
        cardId: 'card_1',
        context: 'First meeting',
        personalityTraits: {'extraversion': 0.8},
      );
      
      // Assert
      expect(response.text, equals('Hello, traveler!'));
      expect(response.emotion, equals('friendly'));
      expect(response.suggestedResponses, hasLength(3));
    });
    
    test('generateDialogue handles network error gracefully', () async {
      // Arrange
      when(() => mockClient.post(any(), headers: any(named: 'headers'), body: any(named: 'body')))
        .thenThrow(SocketException('Network unreachable'));
      
      // Act
      final response = await service.generateDialogue(
        cardId: 'card_1',
        context: 'Test',
        personalityTraits: {},
      );
      
      // Assert
      expect(response.isFallback, isTrue);
    });
  });
}
```

## Cost Management

### Estimating Costs

Google Generative AI (Gemini 2.5 Flash) pricing:
- **Input**: $0.075 per 1M tokens
- **Output**: $0.30 per 1M tokens

**Example calculation for Unwritten**:
- Average dialogue input: ~500 tokens
- Average dialogue output: ~200 tokens
- Cost per dialogue: ~$0.00007

**Monthly estimates** (1000 active users):
- 50 dialogues per user per month
- Total: 50,000 dialogues
- Cost: ~$3.50/month

### Cost Optimization Strategies

```python
# 1. Use caching to reduce API calls
from genkit import cache

@flow
@cache(ttl=3600)  # Cache for 1 hour
async def cached_dialogue_flow(input: DialogueInput) -> DialogueOutput:
    return await generate_dialogue(input)

# 2. Use cheaper models for simple tasks
@flow
async def smart_routing_flow(input: DialogueInput) -> DialogueOutput:
    """Routes to appropriate model based on complexity."""
    
    complexity = assess_complexity(input)
    
    if complexity == 'simple':
        # Use faster, cheaper model
        return await ai.generate(
            prompt=build_prompt(input),
            model='gemini-2.0-flash-lite',  # Cheaper
        )
    else:
        # Use more capable model
        return await ai.generate(
            prompt=build_prompt(input),
            model='gemini-2.5-flash',
        )

# 3. Implement rate limiting
from genkit import rate_limit

@flow
@rate_limit(max_calls=100, per_seconds=60)  # 100 calls/minute
async def rate_limited_flow(input: DialogueInput) -> DialogueOutput:
    return await generate_dialogue(input)
```

## Security Best Practices

### 1. API Authentication

```python
# Backend: Require API key
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key for backend access."""
    
    if x_api_key != os.environ.get('EXPECTED_API_KEY'):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return x_api_key

@app.post('/dialogue')
async def generate_dialogue(
    request: DialogueRequest,
    api_key: str = Depends(verify_api_key),
):
    # Process request
    pass
```

```dart
// Flutter: Include API key in requests
class GenkitService {
  static const String _apiKey = String.fromEnvironment('GENKIT_API_KEY');
  
  Future<DialogueResponse> generateDialogue(...) async {
    final response = await _client.post(
      Uri.parse('$_baseUrl/dialogue'),
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': _apiKey,
      },
      body: jsonEncode(data),
    );
    // ...
  }
}
```

### 2. Input Validation

```python
from pydantic import BaseModel, validator

class DialogueInput(BaseModel):
    card_id: str
    context: str
    personality_traits: Dict[str, float]
    
    @validator('card_id')
    def validate_card_id(cls, v):
        if not v or len(v) > 100:
            raise ValueError('Invalid card_id')
        return v
    
    @validator('context')
    def validate_context(cls, v):
        if len(v) > 5000:  # Prevent abuse
            raise ValueError('Context too long')
        return v
    
    @validator('personality_traits')
    def validate_traits(cls, v):
        valid_traits = {'openness', 'extraversion', 'agreeableness', 'conscientiousness', 'neuroticism'}
        if not all(k in valid_traits for k in v.keys()):
            raise ValueError('Invalid personality trait')
        if not all(0.0 <= val <= 1.0 for val in v.values()):
            raise ValueError('Trait values must be between 0 and 1')
        return v
```

### 3. Data Privacy

```python
# Never log sensitive data
@flow
async def privacy_aware_flow(input: DialogueInput) -> DialogueOutput:
    # Log without sensitive info
    logger.info(f"Generating dialogue for card_id={input.card_id}")
    # DON'T log: user IDs, personal context, etc.
    
    result = await generate_dialogue(input)
    
    return result
```

## Migration Path from TFLite Only

### Phase 1: Add Genkit for Non-Critical Features (Week 1-2)

1. Deploy basic Genkit backend
2. Integrate for non-critical dialogue only
3. Keep TFLite as primary system
4. Monitor performance and costs

### Phase 2: A/B Testing (Week 3-4)

1. Implement feature flags
2. Route 10% of users to Genkit-enhanced dialogues
3. Compare metrics:
   - User engagement
   - Dialogue quality ratings
   - App performance
   - Battery impact

### Phase 3: Gradual Rollout (Week 5-8)

1. Increase Genkit usage based on positive metrics
2. Optimize caching and performance
3. Implement cost controls
4. Add offline fallbacks

### Phase 4: Full Production (Week 9+)

1. Genkit for complex narratives
2. TFLite for fast personality inference
3. Hybrid system optimized for performance and quality

## Troubleshooting

### Common Issues

#### Issue 1: High Latency

**Symptoms**: Dialogue generation takes > 3 seconds

**Solutions**:
- Enable response caching
- Use faster model (gemini-flash-8b)
- Implement request batching
- Add loading states in UI

#### Issue 2: Backend Timeout

**Symptoms**: Requests timeout before completion

**Solutions**:
```python
# Increase timeout in Cloud Run
gcloud run services update unwritten-ai-backend \
  --timeout=60s \
  --request-timeout=60s
```

```dart
// Increase client timeout
final client = http.Client();
final response = await client.post(
  uri,
  headers: headers,
  body: body,
).timeout(Duration(seconds: 45));
```

#### Issue 3: High Costs

**Symptoms**: API costs exceed budget

**Solutions**:
- Implement aggressive caching
- Use rate limiting
- Switch to cheaper models for simple requests
- Implement user quotas

#### Issue 4: Inconsistent Responses

**Symptoms**: AI generates different responses for same input

**Solutions**:
```python
# Use temperature=0 for deterministic output
response = await ai.generate(
    prompt=prompt,
    config={'temperature': 0.0}
)

# Or use caching with longer TTL
@cache(ttl=86400)  # 24 hours
async def consistent_dialogue_flow(input):
    # ...
```

## Next Steps

1. **Set up Development Environment**:
   - Install Genkit CLI
   - Create Python backend project
   - Configure Google Generative AI

2. **Implement First Flow**:
   - Start with simple dialogue generation
   - Test in Developer UI
   - Integrate with Flutter app (development)

3. **Deploy to Cloud Run**:
   - Create Dockerfile
   - Deploy to staging environment
   - Test end-to-end integration

4. **Monitor and Iterate**:
   - Set up monitoring
   - Track performance metrics
   - Gather user feedback
   - Optimize based on data

## Additional Resources

- [Genkit Python Documentation](https://genkit.dev/docs/?lang=python)
- [Google Generative AI Models](https://ai.google.dev/models)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Flutter HTTP Package](https://pub.dev/packages/http)
- [Unwritten AI Architecture](../5.architecture/ai_architecture.md)

## Related Documentation

- [TensorFlow Lite Integration](./tensorflow_lite_integration.md)
- [AI Model Architecture](./ai_model_architecture.md)
- [Performance Optimization](../5.architecture/performance_optimization.md)
- [Testing AI Features](../../app/test/README.md)

---

**Document Version**: 1.0  
**Last Updated**: October 15, 2025  
**Maintainer**: Unwritten AI Team

