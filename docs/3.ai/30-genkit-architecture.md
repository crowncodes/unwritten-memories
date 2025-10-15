# Genkit Architecture for Unwritten

**Purpose:** Unwritten-specific Genkit implementation (not generic tutorial)  
**Audience:** Backend engineers building the production AI system  
**Status:** ✅ Complete Architecture  
**Related:** ← 03-implementation-phases.md | → 31-genkit-integration-guide.md | 34-migration-firebase-to-genkit.md

---

## What This Document Covers

This is **NOT a generic Genkit tutorial** - this is Unwritten's specific production architecture.

**You'll learn:**
- Unwritten-specific flows (dialogue, evolution, story, relationship)
- Custom tools for game state integration
- RAG implementation for 3000+ week continuity
- Backend service structure tailored to Unwritten
- Deployment configuration for Cloud Run
- Cost optimization specific to our use case

**See `31-genkit-integration-guide.md` for generic Genkit reference.**

---

## Table of Contents

1. [Unwritten-Specific Requirements](#unwritten-specific-requirements)
2. [Backend Service Structure](#backend-service-structure)
3. [Core Flows](#core-flows)
4. [Custom Tools](#custom-tools)
5. [RAG Implementation](#rag-implementation)
6. [Model Selection Strategy](#model-selection-strategy)
7. [Deployment Configuration](#deployment-configuration)
8. [Cost Optimization](#cost-optimization)
9. [Monitoring & Analytics](#monitoring--analytics)

---

## Unwritten-Specific Requirements

### What Makes Unwritten Unique

**Game-Specific Challenges:**
1. **Multi-Lifetime Continuity** - 3000+ weeks of player history
2. **OCEAN Personality System** - 5-dimensional personality for every NPC
3. **Dynamic Card Evolution** - Characters evolve through 5 levels
4. **Choice-Based Narrative** - Player choices affect story branches
5. **Relationship Mechanics** - Trust/friendship scores influence everything
6. **Memory Systems** - Characters remember past interactions
7. **Canonical Facts** - Story consistency across all generations
8. **Real-Time Gameplay** - Must integrate with Flame game loop
9. **Cost Constraints** - $2-2.50 per player per month target

### Why Genkit for Unwritten

✅ **Flow System** - Perfect for multi-step card evolution  
✅ **Tool Calling** - Access Firestore game state seamlessly  
✅ **RAG** - Maintain story consistency across 3000+ weeks  
✅ **Observability** - Built-in monitoring and debugging  
✅ **Structured Outputs** - Pydantic models for game data  
✅ **Cost Control** - Smart model selection (Flash vs Pro)

---

## Backend Service Structure

### Project Layout

```
unwritten-genkit-backend/
├── main.py                          # FastAPI + Genkit initialization
├── config/
│   ├── __init__.py
│   ├── settings.py                  # Environment variables
│   ├── models.py                    # Pydantic models
│   └── firebase.py                  # Firebase Admin SDK setup
├── flows/
│   ├── __init__.py
│   ├── dialogue_generation_flow.py  # OCEAN-aware dialogue
│   ├── card_evolution_flow.py       # Level progression (1→2, 2→3, etc.)
│   ├── story_progression_flow.py    # Choice-based narrative
│   ├── relationship_calc_flow.py    # Trust/friendship mechanics
│   ├── memory_generation_flow.py    # Event memory creation
│   └── crisis_response_flow.py      # Emergency/crisis handling
├── tools/
│   ├── __init__.py
│   ├── firestore_tools.py          # Game state CRUD operations
│   ├── card_data_tools.py          # Card information retrieval
│   ├── player_history_tools.py     # Player interaction history
│   ├── world_state_tools.py        # Global game state
│   └── relationship_tools.py       # Relationship score updates
├── rag/
│   ├── __init__.py
│   ├── story_context.py            # Story consistency retrieval
│   ├── canonical_facts.py          # Canonical fact enforcement
│   ├── character_memory.py         # Character memory retrieval
│   └── embeddings.py               # Embedding generation
├── utils/
│   ├── __init__.py
│   ├── prompt_templates.py         # Templates from doc 11
│   ├── validation.py               # Quality validation (from doc 13)
│   └── cost_tracking.py            # Cost monitoring
├── tests/
│   ├── test_flows.py
│   ├── test_tools.py
│   └── test_rag.py
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

### main.py - FastAPI + Genkit Setup

```python
# main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from genkit import genkit, ai
from genkit.plugins.google_genai import GoogleAI
from firebase_admin import initialize_app

# Initialize Firebase
initialize_app()

# Initialize Genkit
ai.configure(
    plugins=[GoogleAI()],
)

# Initialize FastAPI
app = FastAPI(
    title="Unwritten AI Backend",
    version="1.0.0",
)

# CORS for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import flows (registers them with Genkit)
from flows import (
    dialogue_generation_flow,
    card_evolution_flow,
    story_progression_flow,
    relationship_calc_flow,
    memory_generation_flow,
    crisis_response_flow,
)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "unwritten-ai-backend"}

# Start server
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

---

## Core Flows

### 1. Dialogue Generation Flow

**Purpose:** Generate OCEAN-aware dialogue for card interactions

```python
# flows/dialogue_generation_flow.py
from genkit import flow, ai
from pydantic import BaseModel
from typing import List, Dict
from tools.card_data_tools import fetch_card_data
from tools.player_history_tools import fetch_recent_interactions
from tools.relationship_tools import get_relationship_scores
from utils.prompt_templates import DIALOGUE_TEMPLATE

class DialogueInput(BaseModel):
    """Input for dialogue generation"""
    player_id: str
    card_id: str
    interaction_type: str  # "greeting" | "conversation" | "crisis"
    context: str  # Current game context
    player_choice: str | None = None  # If responding to player choice

class DialogueOutput(BaseModel):
    """Output from dialogue generation"""
    text: str
    emotional_tone: str
    trust_delta: float  # Change in trust score
    friendship_delta: float  # Change in friendship score
    memory_created: bool
    urgency_level: int  # 1x, 2x, 3x, 5x (Master Truths v1.2)

@flow(name="dialogue_generation_flow")
async def dialogue_generation_flow(input: DialogueInput) -> DialogueOutput:
    """
    Generate OCEAN-aware dialogue for card interactions.
    
    This flow:
    1. Fetches card data (personality traits, current level)
    2. Fetches player interaction history (last 10 interactions)
    3. Gets current relationship scores
    4. Builds comprehensive prompt with all context
    5. Generates dialogue using appropriate model (Flash vs Pro)
    6. Returns structured output with relationship impacts
    """
    
    # STEP 1: Fetch card data (uses tool)
    card_data = await fetch_card_data(input.card_id)
    
    # STEP 2: Fetch recent interactions (uses tool)
    recent_interactions = await fetch_recent_interactions(
        player_id=input.player_id,
        card_id=input.card_id,
        limit=10
    )
    
    # STEP 3: Get relationship scores (uses tool)
    relationship = await get_relationship_scores(
        player_id=input.player_id,
        card_id=input.card_id
    )
    
    # STEP 4: Build prompt from template (from doc 11)
    prompt = DIALOGUE_TEMPLATE.format(
        card_name=card_data["name"],
        card_level=card_data["level"],
        openness=card_data["personality"]["openness"],
        conscientiousness=card_data["personality"]["conscientiousness"],
        extraversion=card_data["personality"]["extraversion"],
        agreeableness=card_data["personality"]["agreeableness"],
        neuroticism=card_data["personality"]["neuroticism"],
        trust_score=relationship["trust"],
        friendship_score=relationship["friendship"],
        recent_interactions=_format_interactions(recent_interactions),
        current_context=input.context,
        player_choice=input.player_choice or "N/A",
    )
    
    # STEP 5: Select model based on complexity
    model = _select_model(input.interaction_type, card_data["level"])
    
    # STEP 6: Generate dialogue
    response = await ai.generate(
        model=model,
        prompt=prompt,
        output_schema=DialogueOutput,
    )
    
    return response.output

def _select_model(interaction_type: str, card_level: int) -> str:
    """
    Select appropriate model based on complexity.
    
    Flash 2.5: Simple interactions, levels 1-2
    Pro 2.5: Complex interactions, levels 3-5
    """
    if interaction_type == "crisis" or card_level >= 3:
        return "gemini-2.5-pro"
    return "gemini-2.5-flash"

def _format_interactions(interactions: List[Dict]) -> str:
    """Format interaction history for prompt"""
    return "\n".join([
        f"- {i['timestamp']}: {i['summary']}"
        for i in interactions
    ])
```

### 2. Card Evolution Flow

**Purpose:** Handle card level progression (1→2, 2→3, 3→4, 4→5)

```python
# flows/card_evolution_flow.py
from genkit import flow, ai
from pydantic import BaseModel
from typing import List, Dict
from tools.card_data_tools import fetch_card_data, update_card_level
from tools.player_history_tools import fetch_interactions_since_level
from utils.prompt_templates import get_evolution_template
from rag.story_context import retrieve_story_context

class CardEvolutionInput(BaseModel):
    player_id: str
    card_id: str
    trigger_event: str  # What triggered evolution

class CardEvolutionOutput(BaseModel):
    new_name: str | None  # Name might change
    new_description: str  # Updated description
    personality_shifts: Dict[str, float]  # OCEAN trait changes
    new_abilities: List[str]  # Unlocked abilities
    evolution_narrative: str  # Story of the evolution
    memory_milestone: str  # Key memory from this evolution

@flow(name="card_evolution_flow")
async def card_evolution_flow(input: CardEvolutionInput) -> CardEvolutionOutput:
    """
    Handle card level progression with story consistency.
    
    Uses RAG to ensure evolution is consistent with player history.
    """
    
    # Fetch current card state
    card_data = await fetch_card_data(input.card_id)
    current_level = card_data["level"]
    target_level = current_level + 1
    
    if target_level > 5:
        raise ValueError("Card already at max level")
    
    # Fetch all interactions since this level started
    interactions = await fetch_interactions_since_level(
        player_id=input.player_id,
        card_id=input.card_id,
        since_level=current_level
    )
    
    # Use RAG to retrieve relevant story context
    story_context = await retrieve_story_context(
        query=f"Evolution of {card_data['name']} from level {current_level} to {target_level}",
        player_id=input.player_id
    )
    
    # Get appropriate evolution template (from doc 11)
    template = get_evolution_template(current_level, target_level)
    
    # Build comprehensive prompt
    prompt = template.format(
        card_name=card_data["name"],
        current_level=current_level,
        target_level=target_level,
        personality_traits=card_data["personality"],
        interactions_summary=_summarize_interactions(interactions),
        story_context=story_context,
        trigger_event=input.trigger_event,
    )
    
    # Use Gemini Pro for complex evolution
    response = await ai.generate(
        model="gemini-2.5-pro",
        prompt=prompt,
        output_schema=CardEvolutionOutput,
    )
    
    # Update card in Firestore
    await update_card_level(
        card_id=input.card_id,
        new_level=target_level,
        evolution_data=response.output.dict()
    )
    
    return response.output
```

### 3. Story Progression Flow

**Purpose:** Generate choice-based narrative branches

```python
# flows/story_progression_flow.py
from genkit import flow, ai
from pydantic import BaseModel
from typing import List
from rag.canonical_facts import enforce_canonical_facts
from tools.world_state_tools import get_world_state, update_world_state

class StoryProgressionInput(BaseModel):
    player_id: str
    current_scene_id: str
    player_choice: str  # What player chose
    week_number: int  # Current game week (out of 3000+)

class StoryProgressionOutput(BaseModel):
    next_scene_id: str
    narrative_text: str
    consequences: List[str]  # What changed in the world
    unlocked_cards: List[str]  # New cards available
    relationship_impacts: Dict[str, float]  # Impact on various relationships

@flow(name="story_progression_flow")
async def story_progression_flow(input: StoryProgressionInput) -> StoryProgressionOutput:
    """
    Generate next story scene based on player choice.
    
    Uses RAG and canonical facts to maintain consistency.
    """
    
    # Get current world state
    world_state = await get_world_state(input.player_id)
    
    # Enforce canonical facts (from RAG)
    canonical_facts = await enforce_canonical_facts(
        scene_id=input.current_scene_id,
        player_id=input.player_id
    )
    
    # Build prompt with full context
    prompt = f"""
You are generating the next story scene in Unwritten.

Current Week: {input.week_number} / 3000
Current Scene: {input.current_scene_id}
Player Choice: {input.player_choice}

World State:
{world_state}

Canonical Facts (MUST maintain consistency):
{canonical_facts}

Generate the next scene, ensuring:
1. Consistency with canonical facts
2. Natural consequences of player choice
3. Engaging narrative that advances story
4. Appropriate relationship impacts
"""
    
    response = await ai.generate(
        model="gemini-2.5-pro",  # Complex narrative needs Pro
        prompt=prompt,
        output_schema=StoryProgressionOutput,
    )
    
    # Update world state
    await update_world_state(
        player_id=input.player_id,
        updates=response.output.consequences
    )
    
    return response.output
```

### 4. Relationship Calculation Flow

**Purpose:** Calculate trust/friendship impacts based on interactions

```python
# flows/relationship_calc_flow.py
from genkit import flow, ai
from pydantic import BaseModel
from utils.prompt_templates import RELATIONSHIP_IMPACT_TEMPLATE

class RelationshipCalcInput(BaseModel):
    card_id: str
    interaction_type: str
    player_action: str
    card_personality: Dict[str, float]  # OCEAN traits
    current_trust: float
    current_friendship: float

class RelationshipCalcOutput(BaseModel):
    trust_delta: float  # Change in trust (-1.0 to +1.0)
    friendship_delta: float  # Change in friendship (-1.0 to +1.0)
    reasoning: str  # Why these changes
    emotional_response: str  # How card feels about it

@flow(name="relationship_calc_flow")
async def relationship_calc_flow(input: RelationshipCalcInput) -> RelationshipCalcOutput:
    """
    Calculate relationship impact using OCEAN personality.
    
    Fast, uses Flash model.
    """
    
    prompt = RELATIONSHIP_IMPACT_TEMPLATE.format(
        interaction_type=input.interaction_type,
        player_action=input.player_action,
        openness=input.card_personality["openness"],
        conscientiousness=input.card_personality["conscientiousness"],
        extraversion=input.card_personality["extraversion"],
        agreeableness=input.card_personality["agreeableness"],
        neuroticism=input.card_personality["neuroticism"],
        current_trust=input.current_trust,
        current_friendship=input.current_friendship,
    )
    
    response = await ai.generate(
        model="gemini-2.5-flash",  # Simple calculation, use Flash
        prompt=prompt,
        output_schema=RelationshipCalcOutput,
    )
    
    return response.output
```

---

## Custom Tools

### Firestore Tools

```python
# tools/firestore_tools.py
from genkit import tool
from firebase_admin import firestore
from typing import Dict, List, Optional

db = firestore.client()

@tool
async def fetch_card_data(card_id: str) -> Dict:
    """
    Retrieve complete card data from Firestore.
    
    Returns personality traits, current level, relationship stats, etc.
    Used by: All flows that need card information.
    """
    doc = db.collection('cards').document(card_id).get()
    if not doc.exists:
        raise ValueError(f"Card {card_id} not found")
    return doc.to_dict()

@tool
async def update_relationship_score(
    player_id: str,
    card_id: str,
    trust_delta: float,
    friendship_delta: float
) -> Dict:
    """
    Update trust/friendship scores based on AI-determined impact.
    
    Used by: dialogue_generation_flow, relationship_calc_flow
    """
    ref = db.collection('players').document(player_id).collection('relationships').document(card_id)
    
    doc = ref.get()
    if doc.exists:
        current = doc.to_dict()
        new_trust = min(1.0, max(0.0, current['trust'] + trust_delta))
        new_friendship = min(1.0, max(0.0, current['friendship'] + friendship_delta))
    else:
        new_trust = 0.5 + trust_delta
        new_friendship = 0.5 + friendship_delta
    
    ref.set({
        'trust': new_trust,
        'friendship': new_friendship,
        'updated_at': firestore.SERVER_TIMESTAMP
    })
    
    return {'trust': new_trust, 'friendship': new_friendship}

@tool
async def fetch_player_interactions(
    player_id: str,
    card_id: str,
    limit: int = 10
) -> List[Dict]:
    """
    Retrieve recent player-card interactions.
    
    Used by: dialogue_generation_flow, card_evolution_flow
    """
    query = (db.collection('interactions')
        .where('player_id', '==', player_id)
        .where('card_id', '==', card_id)
        .order_by('timestamp', direction=firestore.Query.DESCENDING)
        .limit(limit))
    
    docs = query.stream()
    return [doc.to_dict() for doc in docs]

@tool
async def get_world_state(player_id: str) -> Dict:
    """
    Get current game world state for story consistency.
    
    Used by: story_progression_flow
    """
    doc = db.collection('players').document(player_id).collection('state').document('world').get()
    return doc.to_dict() if doc.exists else {}

@tool
async def update_world_state(player_id: str, updates: List[str]) -> None:
    """
    Update world state based on story progression.
    
    Used by: story_progression_flow
    """
    ref = db.collection('players').document(player_id).collection('state').document('world')
    
    current = ref.get().to_dict() if ref.get().exists else {}
    
    # Add updates to event log
    event_log = current.get('event_log', [])
    event_log.extend(updates)
    
    ref.set({
        'event_log': event_log,
        'updated_at': firestore.SERVER_TIMESTAMP
    }, merge=True)
```

---

## RAG Implementation

### Story Context Retrieval

```python
# rag/story_context.py
from genkit import embed
from firebase_admin import firestore
from typing import List, Dict

db = firestore.client()

# Initialize embedder
embedder = embed.text_embedder("text-embedding-004")

async def retrieve_story_context(
    query: str,
    player_id: str,
    limit: int = 5
) -> str:
    """
    Retrieve relevant story context for consistency.
    
    Searches past 3000 weeks of player history.
    Returns top 5 most relevant story events.
    """
    
    # Generate query embedding
    query_embedding = await embedder.embed(query)
    
    # Search Firestore vector collection
    # Note: Firestore vector search requires index
    results = await _vector_search(
        collection='story_events',
        player_id=player_id,
        embedding=query_embedding,
        limit=limit
    )
    
    # Format results
    context_text = "\n\n".join([
        f"Week {r['week']}: {r['description']}"
        for r in results
    ])
    
    return context_text

async def _vector_search(
    collection: str,
    player_id: str,
    embedding: List[float],
    limit: int
) -> List[Dict]:
    """
    Perform vector similarity search in Firestore.
    
    Requires Firestore vector index on embedding field.
    """
    # Firestore vector search implementation
    # This is a simplified example - actual implementation
    # depends on Firestore vector search setup
    
    query = (db.collection(collection)
        .where('player_id', '==', player_id)
        .limit(limit * 10))  # Over-fetch then re-rank
    
    docs = list(query.stream())
    
    # Calculate cosine similarity
    results = []
    for doc in docs:
        data = doc.to_dict()
        if 'embedding' in data:
            similarity = _cosine_similarity(embedding, data['embedding'])
            results.append({
                **data,
                'similarity': similarity
            })
    
    # Sort by similarity and return top results
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:limit]

def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    import numpy as np
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

### Canonical Facts Enforcement

```python
# rag/canonical_facts.py
from typing import List, Dict

async def enforce_canonical_facts(scene_id: str, player_id: str) -> str:
    """
    Retrieve and enforce canonical facts for story consistency.
    
    Canonical facts are immutable story points that must remain consistent.
    Example: "Elena's mother died when she was 10"
    """
    
    facts = await _fetch_canonical_facts(scene_id, player_id)
    
    facts_text = "CANONICAL FACTS (must remain consistent):\n"
    for fact in facts:
        facts_text += f"- {fact['description']}\n"
    
    return facts_text

async def _fetch_canonical_facts(scene_id: str, player_id: str) -> List[Dict]:
    """Fetch relevant canonical facts from Firestore"""
    from firebase_admin import firestore
    db = firestore.client()
    
    query = (db.collection('canonical_facts')
        .where('player_id', '==', player_id)
        .where('relevant_scenes', 'array_contains', scene_id))
    
    docs = query.stream()
    return [doc.to_dict() for doc in docs]
```

---

## Model Selection Strategy

### Complexity-Based Routing

```python
# config/model_selection.py
from typing import Literal

ModelType = Literal["gemini-2.5-flash", "gemini-2.5-pro"]

def select_model(
    interaction_type: str,
    card_level: int,
    context_size: int,
) -> ModelType:
    """
    Select appropriate Gemini model based on complexity.
    
    Flash 2.5: 80% of requests (fast, cheap)
    Pro 2.5: 20% of requests (complex, high quality)
    
    Target cost: $2-2.50/player/month
    """
    
    # Pro for complex scenarios
    if card_level >= 4:  # Deep bonds (level 4-5)
        return "gemini-2.5-pro"
    
    if interaction_type in ["crisis", "evolution", "story_branch"]:
        return "gemini-2.5-pro"
    
    if context_size > 1000:  # Large context
        return "gemini-2.5-pro"
    
    # Flash for everything else
    return "gemini-2.5-flash"
```

**Target Distribution:**
- Flash: 80% of requests (routine dialogues, level 1-2 interactions)
- Pro: 20% of requests (evolutions, crises, deep dialogues)

**Cost Breakdown:**
```
1000 requests/month:
- 800 Flash requests: $0.0000825 each = $0.066
- 200 Pro requests: $0.005 each = $1.00
Total: ~$1.07/player/month
```

---

## Deployment Configuration

### Docker file

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Environment
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Run with gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 60 main:app
```

### requirements.txt

```txt
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
gunicorn==21.2.0
genkit==0.5.0
google-genkit-ai==0.5.0
pydantic==2.5.0
firebase-admin==6.2.0
numpy==1.26.0
python-dotenv==1.0.0
```

### Cloud Run Deployment

```bash
# Deploy to Google Cloud Run
gcloud run deploy unwritten-genkit-backend \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 100 \
  --concurrency 80 \
  --timeout 60s \
  --set-env-vars GOOGLE_AI_API_KEY=${GOOGLE_AI_API_KEY}

# Output:
# Service URL: https://unwritten-genkit-backend-xxxxx.run.app
```

### Environment Variables

```bash
# .env.example
GOOGLE_AI_API_KEY=your_api_key_here
FIREBASE_PROJECT_ID=unwritten-prod
ENVIRONMENT=production
LOG_LEVEL=INFO
```

---

## Cost Optimization

### Caching Strategy

```python
# config/caching.py
from functools import lru_cache
import hashlib

class ResponseCache:
    """In-memory cache for common responses"""
    _cache = {}
    
    @classmethod
    def get(cls, key: str) -> str | None:
        return cls._cache.get(key)
    
    @classmethod
    def set(cls, key: str, value: str, ttl_seconds: int = 3600):
        cls._cache[key] = {
            'value': value,
            'expires_at': time.time() + ttl_seconds
        }
    
    @classmethod
    def _generate_key(cls, **kwargs) -> str:
        """Generate cache key from parameters"""
        content = str(sorted(kwargs.items()))
        return hashlib.md5(content.encode()).hexdigest()

# Use in flows
@flow(name="cached_dialogue_flow")
async def cached_dialogue_flow(input: DialogueInput) -> DialogueOutput:
    # Check cache first
    cache_key = ResponseCache._generate_key(
        card_id=input.card_id,
        interaction_type=input.interaction_type
    )
    
    cached = ResponseCache.get(cache_key)
    if cached:
        return DialogueOutput.parse_raw(cached)
    
    # Generate if not cached
    result = await dialogue_generation_flow(input)
    
    # Cache result
    ResponseCache.set(cache_key, result.json())
    
    return result
```

### Target Cost: $1.50-2.50/player/month

**Optimization Strategies:**
1. ✅ **Caching** - 60-70% hit rate saves $0.50/month
2. ✅ **Smart Model Selection** - Flash for 80% saves $0.40/month
3. ✅ **Local AI Routing** - TFLite for simple tasks saves $0.30/month
4. ✅ **Request Batching** - Reduce overhead saves $0.10/month

**See:** `71-cost-performance-targets.md` for complete optimization guide

---

## Monitoring & Analytics

### Genkit Telemetry

```python
# Genkit automatically tracks:
# - Flow execution times
# - Model usage (Flash vs Pro)
# - Error rates
# - Token usage

# View in Genkit Developer UI:
# genkit start -o -- python main.py
```

### Custom Metrics

```python
# utils/metrics.py
from prometheus_client import Counter, Histogram

# Custom metrics
flow_requests = Counter('unwritten_flow_requests_total', 'Flow requests', ['flow_name'])
flow_duration = Histogram('unwritten_flow_duration_seconds', 'Flow duration', ['flow_name'])
model_usage = Counter('unwritten_model_usage_total', 'Model usage', ['model'])
generation_cost = Counter('unwritten_generation_cost_usd', 'Generation cost')

# Track in flows
@flow(name="tracked_dialogue_flow")
async def tracked_dialogue_flow(input: DialogueInput) -> DialogueOutput:
    flow_requests.labels(flow_name="dialogue_generation").inc()
    
    with flow_duration.labels(flow_name="dialogue_generation").time():
        result = await dialogue_generation_flow(input)
    
    model_usage.labels(model="gemini-2.5-flash").inc()
    generation_cost.inc(0.0000825)
    
    return result
```

---

## Related Documentation

- **03-implementation-phases.md** - When and how to implement Genkit
- **31-genkit-integration-guide.md** - Generic Genkit reference and tutorial
- **34-migration-firebase-to-genkit.md** - Migration guide from Firebase AI
- **02-technology-stack.md** - Models and pricing
- **71-cost-performance-targets.md** - Cost optimization strategies

---

**Status:** ✅ Complete Architecture  
**Implementation:** Follow 03-implementation-phases.md for development timeline  
**Target:** Production-ready by Week 16 (Phase 2 complete)


