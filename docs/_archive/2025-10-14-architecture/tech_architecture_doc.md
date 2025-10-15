# Unwritten: Technical Architecture - Card Evolution System

## Table of Contents
1. [System Architecture Overview](#system-architecture-overview)
2. [Database Schema](#database-schema)
3. [State Management](#state-management)
4. [AI Integration Layer](#ai-integration-layer)
5. [Real-Time Evolution Pipeline](#real-time-evolution-pipeline)
6. [Caching & Performance](#caching-performance)
7. [Offline Capability](#offline-capability)
8. [Synchronization System](#synchronization-system)
9. [Mobile-Specific Optimizations](#mobile-specific-optimizations)
10. [Security & Data Protection](#security-data-protection)
11. [Analytics & Telemetry](#analytics-telemetry)
12. [Scalability Architecture](#scalability-architecture)

---

## System Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MOBILE CLIENT                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│  │  Presentation  │  │  Game Logic    │  │   Local AI   │  │
│  │     Layer      │  │     Layer      │  │    Engine    │  │
│  │   (Unity UI)   │  │   (C# Core)    │  │  (ML Model)  │  │
│  └────────┬───────┘  └────────┬───────┘  └──────┬───────┘  │
│           │                   │                   │          │
│           └───────────┬───────┴───────────────────┘          │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │           State Management & Cache Layer             │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │  │
│  │  │  Card Store  │  │  NPC Store   │  │  Memory   │ │  │
│  │  │   (Redux)    │  │   (Redux)    │  │   Cache   │ │  │
│  │  └──────────────┘  └──────────────┘  └───────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │              Local Storage Layer                      │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │  │
│  │  │   SQLite     │  │   IndexedDB  │  │   Files   │ │  │
│  │  │  (Structured)│  │   (Blobs)    │  │  (Media)  │ │  │
│  │  └──────────────┘  └──────────────┘  └───────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                      │
└───────────────────────┼──────────────────────────────────────┘
                        │
                        │ Network Layer (REST/GraphQL)
                        │
┌───────────────────────▼──────────────────────────────────────┐
│                      BACKEND SERVICES                         │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   API        │  │   Cloud AI   │  │   Image Gen      │  │
│  │  Gateway     │  │   Service    │  │    Service       │  │
│  │ (Node.js)    │  │  (Python)    │  │   (Python)       │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                  │                    │            │
│  ┌──────▼──────────────────▼────────────────────▼─────────┐ │
│  │              Message Queue (Redis)                      │ │
│  └─────────────────────────────────────────────────────────┘ │
│         │                  │                    │            │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌────────▼─────────┐ │
│  │  PostgreSQL  │  │    Redis     │  │   Object Store   │ │
│  │  (Primary)   │  │   (Cache)    │  │   (S3/Images)    │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Technology Stack

```javascript
const TECH_STACK = {
  
  mobile_client: {
    engine: 'Unity 2023.3 LTS',
    language: 'C#',
    ui_framework: 'Unity UI Toolkit',
    state_management: 'Redux-like pattern (custom)',
    local_database: 'SQLite',
    local_storage: 'PlayerPrefs + File System',
    networking: 'Unity WebRequest / gRPC',
    
    ai_integration: {
      ios: 'Core ML + MLX Framework',
      android: 'TensorFlow Lite'
    }
  },
  
  backend: {
    api_server: 'Node.js + Express',
    ai_service: 'Python + FastAPI',
    image_service: 'Python + FastAPI',
    
    databases: {
      primary: 'PostgreSQL 15',
      cache: 'Redis 7',
      object_storage: 'AWS S3 / Google Cloud Storage'
    },
    
    message_queue: 'Redis + Bull Queue',
    
    ai_models: {
      text: 'Claude Sonnet 4 API',
      image: 'Stable Diffusion XL',
      local: 'Phi-3-mini (quantized)'
    }
  },
  
  infrastructure: {
    hosting: 'AWS / Google Cloud',
    cdn: 'CloudFlare',
    monitoring: 'Datadog / New Relic',
    analytics: 'Mixpanel + Custom',
    crash_reporting: 'Sentry'
  }
};
```

---

## Database Schema

### SQLite Schema (Local/Client)

```sql
-- CARDS TABLE (All card types: Character, Activity, Location, Resource)
CREATE TABLE cards (
    id TEXT PRIMARY KEY,
    card_type TEXT NOT NULL, -- 'character', 'activity', 'location', 'resource'
    
    -- Core Data
    name TEXT NOT NULL,
    description TEXT,
    level INTEGER DEFAULT 1,
    
    -- JSON fields for flexibility
    personality_traits TEXT, -- JSON: {openness: 3.5, ...}
    visual_details TEXT,     -- JSON: [{type: 'scarf', added_week: 4}, ...]
    stats TEXT,              -- JSON: {health: 5, energy: 8, ...}
    
    -- Metadata
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    last_interaction INTEGER,
    interaction_count INTEGER DEFAULT 0,
    
    -- State flags
    is_favorited BOOLEAN DEFAULT 0,
    is_archived BOOLEAN DEFAULT 0,
    tier TEXT DEFAULT 'base', -- 'base', 'evolved', 'fusion', 'legendary'
    
    -- Sync
    sync_status TEXT DEFAULT 'synced', -- 'synced', 'pending', 'conflict'
    server_version INTEGER DEFAULT 0,
    
    -- Search optimization
    search_text TEXT -- Concatenated searchable text
);

CREATE INDEX idx_cards_type ON cards(card_type);
CREATE INDEX idx_cards_level ON cards(level);
CREATE INDEX idx_cards_updated ON cards(updated_at);
CREATE INDEX idx_cards_sync ON cards(sync_status);
CREATE VIRTUAL TABLE cards_fts USING fts5(name, description, search_text);


-- MEMORIES TABLE (Relationship memories)
CREATE TABLE memories (
    id TEXT PRIMARY KEY,
    card_id TEXT NOT NULL,
    
    -- Memory content
    description TEXT NOT NULL,
    emotional_tone TEXT, -- 'joyful', 'vulnerable', 'exciting'
    significance REAL NOT NULL, -- 0.0-1.0
    
    -- Context
    activity_id TEXT, -- What activity generated this
    location_id TEXT, -- Where it happened
    other_characters TEXT, -- JSON array of other NPCs present
    
    -- Temporal data
    created_at INTEGER NOT NULL,
    game_week INTEGER NOT NULL,
    memory_tier INTEGER NOT NULL, -- 1-4 (trivial to defining)
    
    -- Fading
    fade_time INTEGER, -- When memory fades (NULL = permanent)
    weight REAL DEFAULT 1.0, -- Decays over time for non-permanent
    
    FOREIGN KEY(card_id) REFERENCES cards(id) ON DELETE CASCADE
);

CREATE INDEX idx_memories_card ON memories(card_id);
CREATE INDEX idx_memories_significance ON memories(significance);
CREATE INDEX idx_memories_created ON memories(created_at);


-- FUSION_HISTORY (Track card combinations)
CREATE TABLE fusion_history (
    id TEXT PRIMARY KEY,
    
    -- Input cards
    input_cards TEXT NOT NULL, -- JSON array of card IDs
    
    -- Output
    output_card_id TEXT NOT NULL,
    fusion_type TEXT NOT NULL, -- 'simple', 'complex', 'legendary'
    
    -- Generation metadata
    generated_by TEXT, -- 'local_ai', 'cloud_ai', 'template'
    generation_time INTEGER, -- Milliseconds
    
    -- Context
    player_state TEXT, -- JSON of player emotional/physical state
    world_context TEXT, -- JSON of time, weather, etc.
    
    created_at INTEGER NOT NULL,
    
    FOREIGN KEY(output_card_id) REFERENCES cards(id) ON DELETE CASCADE
);

CREATE INDEX idx_fusion_output ON fusion_history(output_card_id);


-- PLAYER_STATE (Current game state)
CREATE TABLE player_state (
    id INTEGER PRIMARY KEY CHECK (id = 1), -- Singleton
    
    -- Stats
    physical_stat REAL DEFAULT 5.0,
    mental_stat REAL DEFAULT 5.0,
    social_stat REAL DEFAULT 5.0,
    emotional_stat REAL DEFAULT 5.0,
    
    -- Resources
    money REAL DEFAULT 0,
    energy INTEGER DEFAULT 10,
    
    -- Progression
    game_day INTEGER DEFAULT 1,
    game_week INTEGER DEFAULT 1,
    
    -- Current context
    current_location TEXT,
    current_time TEXT, -- JSON: {hour, minute, day_of_week}
    current_season TEXT,
    
    -- Metadata
    playthrough_id TEXT NOT NULL,
    started_at INTEGER NOT NULL,
    last_played INTEGER NOT NULL,
    total_playtime INTEGER DEFAULT 0, -- Seconds
    
    -- Settings
    user_tier TEXT DEFAULT 'free', -- 'free', 'premium'
    settings TEXT -- JSON of user preferences
);


-- RELATIONSHIP_GRAPH (Tracks relationships between NPCs)
CREATE TABLE relationships (
    id TEXT PRIMARY KEY,
    character_a_id TEXT NOT NULL,
    character_b_id TEXT NOT NULL,
    
    -- Relationship data
    relationship_type TEXT, -- 'friends', 'family', 'romantic', 'professional'
    strength REAL DEFAULT 0.5, -- 0.0-1.0
    
    -- History
    first_met_week INTEGER,
    last_interaction_week INTEGER,
    interaction_count INTEGER DEFAULT 0,
    
    -- Player involvement
    player_introduced BOOLEAN DEFAULT 0,
    player_mediated_conflicts INTEGER DEFAULT 0,
    
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    
    FOREIGN KEY(character_a_id) REFERENCES cards(id) ON DELETE CASCADE,
    FOREIGN KEY(character_b_id) REFERENCES cards(id) ON DELETE CASCADE,
    
    UNIQUE(character_a_id, character_b_id)
);

CREATE INDEX idx_relationships_chars ON relationships(character_a_id, character_b_id);


-- EVOLUTION_QUEUE (Pending AI generations)
CREATE TABLE evolution_queue (
    id TEXT PRIMARY KEY,
    card_id TEXT NOT NULL,
    
    -- Evolution context
    evolution_type TEXT NOT NULL, -- 'level_up', 'fusion', 'crisis'
    context_data TEXT NOT NULL, -- JSON with all context
    priority INTEGER DEFAULT 5, -- 1-10, higher = more urgent
    
    -- Processing
    status TEXT DEFAULT 'pending', -- 'pending', 'processing', 'complete', 'failed'
    assigned_to TEXT, -- 'local_ai', 'cloud_ai', 'template'
    
    -- Retry logic
    attempt_count INTEGER DEFAULT 0,
    last_attempt INTEGER,
    error_message TEXT,
    
    created_at INTEGER NOT NULL,
    completed_at INTEGER,
    
    FOREIGN KEY(card_id) REFERENCES cards(id) ON DELETE CASCADE
);

CREATE INDEX idx_evolution_status ON evolution_queue(status);
CREATE INDEX idx_evolution_priority ON evolution_queue(priority DESC);


-- CACHE_STORE (AI generation cache)
CREATE TABLE cache_store (
    id TEXT PRIMARY KEY, -- Hash of input context
    cache_type TEXT NOT NULL, -- 'text_generation', 'image_generation'
    
    -- Input
    input_hash TEXT NOT NULL,
    input_data TEXT, -- JSON of inputs
    
    -- Output
    output_data TEXT NOT NULL, -- JSON or blob reference
    
    -- Metadata
    hit_count INTEGER DEFAULT 0,
    last_accessed INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    expires_at INTEGER, -- NULL = never expires
    
    -- Size tracking
    size_bytes INTEGER,
    
    UNIQUE(input_hash, cache_type)
);

CREATE INDEX idx_cache_hash ON cache_store(input_hash);
CREATE INDEX idx_cache_accessed ON cache_store(last_accessed);


-- ANALYTICS_EVENTS (Local analytics before sync)
CREATE TABLE analytics_events (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    event_data TEXT NOT NULL, -- JSON
    
    created_at INTEGER NOT NULL,
    synced BOOLEAN DEFAULT 0
);

CREATE INDEX idx_analytics_synced ON analytics_events(synced);
```

### PostgreSQL Schema (Server/Backend)

```sql
-- USERS (Player accounts)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Auth
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    
    -- Profile
    username VARCHAR(50) UNIQUE,
    display_name VARCHAR(100),
    
    -- Subscription
    tier VARCHAR(20) DEFAULT 'free', -- 'free', 'premium'
    subscription_id VARCHAR(100),
    subscription_starts_at TIMESTAMP,
    subscription_ends_at TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    last_sync TIMESTAMP,
    
    -- Stats
    total_playtime INTEGER DEFAULT 0, -- Seconds
    playthroughs_completed INTEGER DEFAULT 0,
    
    -- Settings
    settings JSONB DEFAULT '{}'
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_tier ON users(tier);


-- PLAYTHROUGHS (Game saves)
CREATE TABLE playthroughs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Playthrough metadata
    name VARCHAR(100),
    game_day INTEGER DEFAULT 1,
    game_week INTEGER DEFAULT 1,
    
    -- State
    is_active BOOLEAN DEFAULT TRUE,
    is_completed BOOLEAN DEFAULT FALSE,
    completion_type VARCHAR(50), -- 'natural_end', 'player_choice', 'failure'
    
    -- Timestamps
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    last_played TIMESTAMP DEFAULT NOW(),
    
    -- Sync
    last_sync_at TIMESTAMP,
    sync_version INTEGER DEFAULT 0,
    
    -- Archived playthrough data (if completed)
    archived_data JSONB
);

CREATE INDEX idx_playthroughs_user ON playthroughs(user_id);
CREATE INDEX idx_playthroughs_active ON playthroughs(user_id, is_active);


-- CARDS_SYNC (Synced card data)
CREATE TABLE cards_sync (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    playthrough_id UUID NOT NULL REFERENCES playthroughs(id) ON DELETE CASCADE,
    
    -- Card data (mirrors client schema)
    card_type VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    level INTEGER DEFAULT 1,
    
    -- JSON fields
    personality_traits JSONB,
    visual_details JSONB,
    stats JSONB,
    
    -- Generated content cache
    generated_text TEXT,
    generated_image_url TEXT,
    
    -- Sync metadata
    client_id VARCHAR(100) UNIQUE, -- Client-side UUID
    version INTEGER DEFAULT 1,
    last_modified TIMESTAMP DEFAULT NOW(),
    
    -- Premium features
    custom_portrait_generated BOOLEAN DEFAULT FALSE,
    lora_model_id VARCHAR(100)
);

CREATE INDEX idx_cards_playthrough ON cards_sync(playthrough_id);
CREATE INDEX idx_cards_client_id ON cards_sync(client_id);


-- AI_GENERATION_QUEUE (Server-side generation queue)
CREATE TABLE ai_generation_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    playthrough_id UUID REFERENCES playthroughs(id),
    
    -- Request
    generation_type VARCHAR(50) NOT NULL, -- 'text', 'image', 'fusion'
    input_data JSONB NOT NULL,
    priority INTEGER DEFAULT 5,
    
    -- Processing
    status VARCHAR(20) DEFAULT 'pending',
    assigned_worker VARCHAR(100),
    
    -- Output
    output_data JSONB,
    generation_time INTEGER, -- Milliseconds
    
    -- Cost tracking
    estimated_cost DECIMAL(10, 4),
    actual_cost DECIMAL(10, 4),
    
    -- Retry
    attempt_count INTEGER DEFAULT 0,
    error_message TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_generation_status ON ai_generation_queue(status);
CREATE INDEX idx_generation_user ON ai_generation_queue(user_id);
CREATE INDEX idx_generation_priority ON ai_generation_queue(priority DESC, created_at ASC);


-- AI_GENERATION_CACHE (Server-side cache)
CREATE TABLE ai_generation_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Cache key
    input_hash VARCHAR(64) UNIQUE NOT NULL,
    generation_type VARCHAR(50) NOT NULL,
    
    -- Cached data
    output_data JSONB NOT NULL,
    output_url TEXT, -- For images/media
    
    -- Usage stats
    hit_count INTEGER DEFAULT 0,
    total_cost_saved DECIMAL(10, 2) DEFAULT 0,
    
    -- Lifecycle
    created_at TIMESTAMP DEFAULT NOW(),
    last_accessed TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    
    -- Size
    size_bytes INTEGER
);

CREATE INDEX idx_cache_input_hash ON ai_generation_cache(input_hash);
CREATE INDEX idx_cache_type ON ai_generation_cache(generation_type);


-- ANALYTICS_EVENTS (Server-side analytics)
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    playthrough_id UUID REFERENCES playthroughs(id),
    
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    
    -- Context
    client_version VARCHAR(20),
    platform VARCHAR(20), -- 'ios', 'android'
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_analytics_user ON analytics_events(user_id);
CREATE INDEX idx_analytics_type ON analytics_events(event_type);
CREATE INDEX idx_analytics_created ON analytics_events(created_at DESC);

-- Partition by month for performance
CREATE TABLE analytics_events_y2025m01 PARTITION OF analytics_events
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```

---

## State Management

### Redux-Like State Architecture

```csharp
// Unity C# State Management

public class GameState
{
    // Singleton instance
    private static GameState _instance;
    public static GameState Instance => _instance ?? (_instance = new GameState());
    
    // State stores
    public CardStore Cards { get; private set; }
    public NPCStore NPCs { get; private set; }
    public PlayerStore Player { get; private set; }
    public MemoryStore Memories { get; private set; }
    public UIStore UI { get; private set; }
    
    // Event system for reactive updates
    public event Action<StateChange> OnStateChanged;
    
    private GameState()
    {
        Cards = new CardStore();
        NPCs = new NPCStore();
        Player = new PlayerStore();
        Memories = new MemoryStore();
        UI = new UIStore();
    }
    
    // Dispatch actions to update state
    public void Dispatch(IAction action)
    {
        var changes = new List<StateChange>();
        
        // Route action to appropriate reducer
        if (action is CardAction cardAction)
        {
            var change = Cards.Reduce(cardAction);
            if (change != null) changes.Add(change);
        }
        else if (action is NPCAction npcAction)
        {
            var change = NPCs.Reduce(npcAction);
            if (change != null) changes.Add(change);
        }
        // ... other action types
        
        // Notify subscribers of changes
        foreach (var change in changes)
        {
            OnStateChanged?.Invoke(change);
        }
        
        // Persist to local database
        PersistenceManager.Instance.SaveChanges(changes);
        
        // Queue for sync if online
        if (NetworkManager.Instance.IsOnline)
        {
            SyncManager.Instance.QueueSync(changes);
        }
    }
}

// Example: Card Store
public class CardStore
{
    private Dictionary<string, Card> _cards = new Dictionary<string, Card>();
    
    public Card GetCard(string id)
    {
        return _cards.TryGetValue(id, out var card) ? card : null;
    }
    
    public IEnumerable<Card> GetAllCards()
    {
        return _cards.Values;
    }
    
    public StateChange Reduce(CardAction action)
    {
        switch (action)
        {
            case CreateCardAction create:
                return HandleCreate(create);
                
            case UpdateCardAction update:
                return HandleUpdate(update);
                
            case EvolveCardAction evolve:
                return HandleEvolve(evolve);
                
            case FuseCardsAction fuse:
                return HandleFusion(fuse);
                
            default:
                return null;
        }
    }
    
    private StateChange HandleEvolve(EvolveCardAction action)
    {
        var card = GetCard(action.CardId);
        if (card == null) return null;
        
        // Update card with evolution data
        card.Level = action.NewLevel;
        card.Description = action.NewDescription;
        card.PersonalityTraits = action.NewPersonalityTraits;
        card.VisualDetails.AddRange(action.NewVisualDetails);
        card.UpdatedAt = DateTime.Now;
        
        _cards[action.CardId] = card;
        
        return new StateChange
        {
            Type = StateChangeType.CardEvolved,
            AffectedId = action.CardId,
            OldState = action.OldCard,
            NewState = card
        };
    }
}

// Actions
public interface IAction { }

public class EvolveCardAction : IAction
{
    public string CardId { get; set; }
    public int NewLevel { get; set; }
    public string NewDescription { get; set; }
    public PersonalityTraits NewPersonalityTraits { get; set; }
    public List<VisualDetail> NewVisualDetails { get; set; }
    public Card OldCard { get; set; } // For undo/sync
}

public class FuseCardsAction : IAction
{
    public List<string> InputCardIds { get; set; }
    public Card OutputCard { get; set; }
    public FusionType FusionType { get; set; }
}
```

### Reactive UI Binding

```csharp
// UI components subscribe to state changes

public class CharacterCardUI : MonoBehaviour
{
    private string _cardId;
    private Card _currentCard;
    
    void OnEnable()
    {
        // Subscribe to state changes
        GameState.Instance.OnStateChanged += HandleStateChange;
    }
    
    void OnDisable()
    {
        GameState.Instance.OnStateChanged -= HandleStateChange;
    }
    
    public void Initialize(string cardId)
    {
        _cardId = cardId;
        RefreshCard();
    }
    
    private void HandleStateChange(StateChange change)
    {
        // Only update if this card changed
        if (change.AffectedId == _cardId)
        {
            RefreshCard();
        }
    }
    
    private void RefreshCard()
    {
        _currentCard = GameState.Instance.Cards.GetCard(_cardId);
        
        // Update UI elements
        nameText.text = _currentCard.Name;
        descriptionText.text = _currentCard.Description;
        levelText.text = $"Level {_currentCard.Level}";
        
        // Update personality bars
        UpdatePersonalityBars(_currentCard.PersonalityTraits);
        
        // Update visual details
        UpdatePortrait(_currentCard.VisualDetails);
        
        // Animate changes
        AnimateCardUpdate();
    }
}
```

---

## AI Integration Layer

### AI Service Manager

```csharp
public class AIServiceManager : MonoBehaviour
{
    private static AIServiceManager _instance;
    public static AIServiceManager Instance => _instance;
    
    // AI engines
    private LocalAIEngine _localAI;
    private CloudAIClient _cloudAI;
    
    // Configuration
    private UserTier _userTier;
    
    void Awake()
    {
        _instance = this;
        
        // Initialize AI engines
        _localAI = new LocalAIEngine();
        _cloudAI = new CloudAIClient();
        
        // Load user tier
        _userTier = GameState.Instance.Player.Tier;
    }
    
    public async Task<CardEvolution> GenerateEvolution(
        Card card, 
        InteractionContext context
    )
    {
        // Determine routing
        var route = DetermineRoute(card, context);
        
        switch (route)
        {
            case AIRoute.LocalImmediate:
                return await GenerateLocal(card, context);
                
            case AIRoute.CloudWithFallback:
                return await GenerateCloudWithFallback(card, context);
                
            case AIRoute.PremiumPrecached:
                return await GetPrecachedEvolution(card);
                
            case AIRoute.Template:
                return GenerateFromTemplate(card, context);
                
            default:
                return await GenerateLocal(card, context);
        }
    }
    
    private AIRoute DetermineRoute(Card card, InteractionContext context)
    {
        // Check cache first
        if (EvolutionCache.HasCached(card.Id, context))
        {
            return AIRoute.PremiumPrecached;
        }
        
        // Calculate importance
        var importance = CalculateImportance(card, context);
        
        if (_userTier == UserTier.Premium)
        {
            if (importance > 0.7)
            {
                return AIRoute.CloudWithFallback;
            }
            else if (importance > 0.3)
            {
                return AIRoute.LocalImmediate;
            }
            else
            {
                return AIRoute.Template;
            }
        }
        else // Free tier
        {
            if (importance > 0.5)
            {
                return AIRoute.LocalImmediate;
            }
            else
            {
                return AIRoute.Template;
            }
        }
    }
    
    private async Task<CardEvolution> GenerateLocal(
        Card card, 
        InteractionContext context
    )
    {
        var startTime = DateTime.Now;
        
        // Multi-step local generation
        var chain = new LocalEvolutionChain(_localAI);
        var evolution = await chain.GenerateEvolution(card, context);
        
        var duration = (DateTime.Now - startTime).TotalMilliseconds;
        
        // Track analytics
        AnalyticsManager.Instance.TrackEvent("evolution_generated", new {
            route = "local",
            duration_ms = duration,
            card_level = card.Level,
            importance = CalculateImportance(card, context)
        });
        
        return evolution;
    }
    
    private async Task<CardEvolution> GenerateCloudWithFallback(
        Card card,
        InteractionContext context
    )
    {
        // Show local version immediately
        var localEvolution = await GenerateLocal(card, context);
        
        // Apply local evolution to UI
        ApplyEvolutionToCard(card, localEvolution);
        
        // Generate cloud version in background
        StartCoroutine(EnhanceWithCloud(card, context, localEvolution));
        
        return localEvolution;
    }
    
    private IEnumerator EnhanceWithCloud(
        Card card,
        InteractionContext context,
        CardEvolution localEvolution
    )
    {
        // Wait for cloud generation
        var cloudTask = _cloudAI.GenerateEnhanced(card, context);
        
        while (!cloudTask.IsCompleted)
        {
            yield return null;
        }
        
        if (cloudTask.IsCompletedSuccessfully)
        {
            var cloudEvolution = cloudTask.Result;
            
            // Smoothly transition to cloud version
            TransitionToEnhancedEvolution(card, localEvolution, cloudEvolution);
        }
    }
}
```

### Local AI Engine Implementation

```csharp
public class LocalAIEngine
{
    private MLModel _textModel;
    private Tokenizer _tokenizer;
    
    public LocalAIEngine()
    {
        // Load quantized model
        #if UNITY_IOS
            _textModel = CoreMLModel.Load("phi3_mini_q4");
        #elif UNITY_ANDROID
            _textModel = TFLiteModel.Load("phi3_mini_q4.tflite");
        #endif
        
        _tokenizer = new Tokenizer();
    }
    
    public async Task<string> Generate(string prompt, int maxTokens = 100)
    {
        // Encode prompt
        var tokens = _tokenizer.Encode(prompt);
        
        // Generate on device
        var output = await _textModel.GenerateAsync(
            input: tokens,
            maxTokens: maxTokens,
            temperature: 0.7f
        );
        
        // Decode output
        return _tokenizer.Decode(output);
    }
    
    public async Task<MemoryDescription> GenerateMemory(
        string template,
        Dictionary<string, string> variables
    )
    {
        // Fill template with variables
        var prompt = FillTemplate(template, variables);
        
        // Add instruction
        var fullPrompt = $@"
            Complete this memory description (20-40 words):
            {prompt}
            
            Memory:
        ";
        
        var result = await Generate(fullPrompt, maxTokens: 60);
        
        return new MemoryDescription
        {
            Text = result.Trim(),
            GeneratedBy = "local_ai",
            GenerationTime = /* tracked */
        };
    }
}
```

### Cloud AI Client

```csharp
public class CloudAIClient
{
    private HttpClient _httpClient;
    private string _apiUrl;
    
    public CloudAIClient()
    {
        _httpClient = new HttpClient();
        _apiUrl = "https://api.unwritten.game";
    }
    
    public async Task<CardEvolution> GenerateEnhanced(
        Card card,
        InteractionContext context
    )
    {
        var request = new EvolutionRequest
        {
            CardId = card.Id,
            CurrentState = card.ToJson(),
            Context = context.ToJson(),
            UserId = PlayerPrefs.GetString("user_id"),
            PlaythroughId = GameState.Instance.Player.PlaythroughId
        };
        
        var response = await _httpClient.PostAsJsonAsync(
            $"{_apiUrl}/v1/evolution/generate",
            request
        );
        
        if (!response.IsSuccessStatusCode)
        {
            throw new AIGenerationException("Cloud generation failed");
        }
        
        var result = await response.Content.ReadAsAsync<EvolutionResponse>();
        
        return result.Evolution;
    }
    
    public async Task<byte[]> GeneratePortrait(
        Card card,
        string prompt
    )
    {
        var request = new ImageGenerationRequest
        {
            CardId = card.Id,
            Prompt = prompt,
            LoraModelId = card.LoraModelId,
            Resolution = "1024x1024",
            Quality = "high"
        };
        
        var response = await _httpClient.PostAsJsonAsync(
            $"{_apiUrl}/v1/image/generate",
            request
        );
        
        var result = await response.Content.ReadAsAsync<ImageGenerationResponse>();
        
        // Download image
        var imageBytes = await _httpClient.GetByteArrayAsync(result.ImageUrl);
        
        return imageBytes;
    }
}
```

---

## Real-Time Evolution Pipeline

### Evolution Queue System

```csharp
public class EvolutionQueueManager : MonoBehaviour
{
    private Queue<EvolutionTask> _pendingQueue = new Queue<EvolutionTask>();
    private List<EvolutionTask> _processingQueue = new List<EvolutionTask>();
    
    private int _maxConcurrent = 3;
    
    public void QueueEvolution(Card card, InteractionContext context, int priority = 5)
    {
        var task = new EvolutionTask
        {
            Id = Guid.NewGuid().ToString(),
            CardId = card.Id,
            Context = context,
            Priority = priority,
            QueuedAt = DateTime.Now,
            Status = EvolutionStatus.Pending
        };
        
        // Save to local database
        DatabaseManager.Instance.InsertEvolutionTask(task);
        
        // Add to memory queue
        _pendingQueue.Enqueue(task);
        
        // Try to process immediately
        ProcessQueue();
    }
    
    private void ProcessQueue()
    {
        // Process tasks until max concurrent reached
        while (_processingQueue.Count < _maxConcurrent && _pendingQueue.Count > 0)
        {
            var task = _pendingQueue.Dequeue();
            
            _processingQueue.Add(task);
            task.Status = EvolutionStatus.Processing;
            
            StartCoroutine(ProcessEvolutionTask(task));
        }
    }
    
    private IEnumerator ProcessEvolutionTask(EvolutionTask task)
    {
        var card = GameState.Instance.Cards.GetCard(task.CardId);
        
        // Generate evolution
        var evolutionTask = AIServiceManager.Instance.GenerateEvolution(
            card, 
            task.Context
        );
        
        while (!evolutionTask.IsCompleted)
        {
            yield return null;
        }
        
        if (evolutionTask.IsCompletedSuccessfully)
        {
            var evolution = evolutionTask.Result;
            
            // Apply evolution to card
            ApplyEvolution(card, evolution);
            
            task.Status = EvolutionStatus.Complete;
            task.CompletedAt = DateTime.Now;
        }
        else
        {
            task.Status = EvolutionStatus.Failed;
            task.ErrorMessage = evolutionTask.Exception?.Message;
            task.AttemptCount++;
            
            // Retry if under max attempts
            if (task.AttemptCount < 3)
            {
                _pendingQueue.Enqueue(task);
            }
        }
        
        // Remove from processing
        _processingQueue.Remove(task);
        
        // Update database
        DatabaseManager.Instance.UpdateEvolutionTask(task);
        
        // Process next task
        ProcessQueue();
    }
    
    private void ApplyEvolution(Card card, CardEvolution evolution)
    {
        // Dispatch action to update state
        GameState.Instance.Dispatch(new EvolveCardAction
        {
            CardId = card.Id,
            NewLevel = evolution.NewLevel,
            NewDescription = evolution.Description,
            NewPersonalityTraits = evolution.PersonalityTraits,
            NewVisualDetails = evolution.VisualDetails,
            OldCard = card.Clone()
        });
        
        // Show evolution animation
        UIManager.Instance.ShowEvolutionAnimation(card, evolution);
        
        // Track analytics
        AnalyticsManager.Instance.TrackEvent("card_evolved", new {
            card_id = card.Id,
            old_level = card.Level,
            new_level = evolution.NewLevel,
            evolution_type = evolution.Type
        });
    }
}
```

### Predictive Pre-Generation

```csharp
public class PredictiveGenerator : MonoBehaviour
{
    private Dictionary<string, float> _interactionProbabilities = new Dictionary<string, float>();
    
    void Update()
    {
        // Only run during idle time
        if (!IsPlayerIdle()) return;
        
        // Predict next likely interactions
        var predictions = PredictNextInteractions();
        
        // Pre-generate for top predictions
        foreach (var prediction in predictions.Take(5))
        {
            PreGenerateIfNeeded(prediction);
        }
    }
    
    private List<InteractionPrediction> PredictNextInteractions()
    {
        var predictions = new List<InteractionPrediction>();
        
        var player = GameState.Instance.Player;
        var location = player.CurrentLocation;
        
        // Get NPCs near player
        var nearbyNPCs = GetNearbyNPCs(player.Position, radius: 50f);
        
        foreach (var npc in nearbyNPCs)
        {
            var probability = CalculateInteractionProbability(player, npc);
            
            predictions.Add(new InteractionPrediction
            {
                NPCId = npc.Id,
                Probability = probability,
                EstimatedContext = EstimateContext(player, npc)
            });
        }
        
        // Sort by probability
        return predictions.OrderByDescending(p => p.Probability).ToList();
    }
    
    private float CalculateInteractionProbability(Player player, NPC npc)
    {
        var probability = 0f;
        
        // Distance factor
        var distance = Vector3.Distance(player.Position, npc.Position);
        probability += Mathf.Clamp01(1f - (distance / 50f)) * 0.3f;
        
        // Relationship level factor
        probability += (npc.RelationshipLevel / 5f) * 0.3f;
        
        // Time since last interaction
        var hoursSinceLastInteraction = (DateTime.Now - npc.LastInteraction).TotalHours;
        if (hoursSinceLastInteraction > 24)
        {
            probability += 0.2f; // Due for interaction
        }
        
        // Player pattern matching
        var playerHistory = GetPlayerInteractionHistory();
        if (playerHistory.FrequentlyInteractsWith(npc.Id))
        {
            probability += 0.2f;
        }
        
        return Mathf.Clamp01(probability);
    }
    
    private void PreGenerateIfNeeded(InteractionPrediction prediction)
    {
        var cacheKey = GenerateCacheKey(prediction);
        
        // Check if already cached
        if (EvolutionCache.HasCached(cacheKey)) return;
        
        // Check if already queued
        if (IsAlreadyQueued(prediction.NPCId)) return;
        
        // Queue for background generation
        var npc = GameState.Instance.NPCs.GetNPC(prediction.NPCId);
        
        BackgroundGenerator.Instance.QueueGeneration(
            npc,
            prediction.EstimatedContext,
            priority: (int)(prediction.Probability * 10)
        );
    }
}
```

---

## Caching & Performance

### Multi-Layer Cache System

```csharp
public class EvolutionCache : MonoBehaviour
{
    // Layer 1: Memory cache (fast, limited size)
    private LRUCache<string, CardEvolution> _memoryCache = new LRUCache<string, CardEvolution>(100);
    
    // Layer 2: Disk cache (slower, larger size)
    private DiskCache _diskCache = new DiskCache("evolution_cache");
    
    // Layer 3: Cloud cache (for premium users)
    private CloudCacheClient _cloudCache = new CloudCacheClient();
    
    public async Task<CardEvolution> GetCached(string cacheKey)
    {
        // Try memory cache first
        if (_memoryCache.TryGet(cacheKey, out var cached))
        {
            AnalyticsManager.Instance.TrackCacheHit("memory");
            return cached;
        }
        
        // Try disk cache
        var diskCached = await _diskCache.GetAsync<CardEvolution>(cacheKey);
        if (diskCached != null)
        {
            // Promote to memory cache
            _memoryCache.Add(cacheKey, diskCached);
            
            AnalyticsManager.Instance.TrackCacheHit("disk");
            return diskCached;
        }
        
        // Try cloud cache (premium only)
        if (GameState.Instance.Player.Tier == UserTier.Premium)
        {
            var cloudCached = await _cloudCache.GetAsync<CardEvolution>(cacheKey);
            if (cloudCached != null)
            {
                // Promote to memory and disk
                _memoryCache.Add(cacheKey, cloudCached);
                await _diskCache.SetAsync(cacheKey, cloudCached);
                
                AnalyticsManager.Instance.TrackCacheHit("cloud");
                return cloudCached;
            }
        }
        
        // Cache miss
        AnalyticsManager.Instance.TrackCacheMiss();
        return null;
    }
    
    public async Task SetCached(string cacheKey, CardEvolution evolution)
    {
        // Add to all cache layers
        _memoryCache.Add(cacheKey, evolution);
        
        await _diskCache.SetAsync(cacheKey, evolution);
        
        if (GameState.Instance.Player.Tier == UserTier.Premium)
        {
            await _cloudCache.SetAsync(cacheKey, evolution);
        }
    }
    
    public void InvalidateCache(string cardId)
    {
        // Remove all cached evolutions for this card
        var keysToRemove = _memoryCache.Keys
            .Where(k => k.StartsWith(cardId))
            .ToList();
        
        foreach (var key in keysToRemove)
        {
            _memoryCache.Remove(key);
            _diskCache.Delete(key);
        }
    }
}

// LRU Cache implementation
public class LRUCache<TKey, TValue>
{
    private readonly int _capacity;
    private readonly Dictionary<TKey, LinkedListNode<CacheItem>> _cache;
    private readonly LinkedList<CacheItem> _lruList;
    
    public LRUCache(int capacity)
    {
        _capacity = capacity;
        _cache = new Dictionary<TKey, LinkedListNode<CacheItem>>(capacity);
        _lruList = new LinkedList<CacheItem>();
    }
    
    public bool TryGet(TKey key, out TValue value)
    {
        if (_cache.TryGetValue(key, out var node))
        {
            // Move to front (most recently used)
            _lruList.Remove(node);
            _lruList.AddFirst(node);
            
            value = node.Value.Value;
            return true;
        }
        
        value = default;
        return false;
    }
    
    public void Add(TKey key, TValue value)
    {
        // Remove if already exists
        if (_cache.TryGetValue(key, out var existingNode))
        {
            _lruList.Remove(existingNode);
            _cache.Remove(key);
        }
        
        // Add to front
        var item = new CacheItem { Key = key, Value = value };
        var node = _lruList.AddFirst(item);
        _cache[key] = node;
        
        // Evict if over capacity
        if (_cache.Count > _capacity)
        {
            var lru = _lruList.Last;
            _lruList.RemoveLast();
            _cache.Remove(lru.Value.Key);
        }
    }
    
    private class CacheItem
    {
        public TKey Key { get; set; }
        public TValue Value { get; set; }
    }
}
```

---

## Offline Capability

### Offline-First Architecture

```csharp
public class OfflineManager : MonoBehaviour
{
    private bool _isOnline = false;
    private Queue<SyncOperation> _pendingSync = new Queue<SyncOperation>();
    
    void Start()
    {
        // Check network status
        CheckNetworkStatus();
        
        // Subscribe to network changes
        Application.internetReachabilityChanged += OnNetworkStatusChanged;
        
        // Load pending sync operations
        LoadPendingSync();
    }
    
    private void OnNetworkStatusChanged(NetworkReachability status)
    {
        var wasOnline = _isOnline;
        _isOnline = status != NetworkReachability.NotReachable;
        
        if (!wasOnline && _isOnline)
        {
            // Just came online, sync pending operations
            StartCoroutine(SyncPendingOperations());
        }
    }
    
    public void RecordOperation(SyncOperation operation)
    {
        // Save to pending queue
        _pendingSync.Enqueue(operation);
        
        // Persist to database
        DatabaseManager.Instance.InsertPendingSync(operation);
        
        // Try to sync immediately if online
        if (_isOnline)
        {
            StartCoroutine(SyncOperation(operation));
        }
    }
    
    private IEnumerator SyncPendingOperations()
    {
        while (_pendingSync.Count > 0)
        {
            var operation = _pendingSync.Dequeue();
            
            yield return SyncOperation(operation);
        }
    }
    
    private IEnumerator SyncOperation(SyncOperation operation)
    {
        var syncTask = SyncManager.Instance.Sync(operation);
        
        while (!syncTask.IsCompleted)
        {
            yield return null;
        }
        
        if (syncTask.IsCompletedSuccessfully)
        {
            // Remove from pending
            DatabaseManager.Instance.DeletePendingSync(operation.Id);
        }
        else
        {
            // Keep in queue, will retry later
            _pendingSync.Enqueue(operation);
        }
    }
}
```

### Conflict Resolution

```csharp
public class ConflictResolver
{
    public ResolvedState ResolveConflict(
        CardState localState,
        CardState serverState
    )
    {
        // Last-write-wins for most fields
        var resolved = serverState.Version > localState.Version 
            ? serverState 
            : localState;
        
        // But merge certain fields
        resolved.InteractionCount = Math.Max(
            localState.InteractionCount,
            serverState.InteractionCount
        );
        
        // Merge memories (union of both)
        resolved.Memories = MergeMemories(
            localState.Memories,
            serverState.Memories
        );
        
        // Merge visual details (union, no duplicates)
        resolved.VisualDetails = MergeVisualDetails(
            localState.VisualDetails,
            serverState.VisualDetails
        );
        
        // Increment version
        resolved.Version = Math.Max(localState.Version, serverState.Version) + 1;
        
        return new ResolvedState
        {
            State = resolved,
            ConflictsFound = IdentifyConflicts(localState, serverState),
            ResolutionStrategy = "merge"
        };
    }
    
    private List<Memory> MergeMemories(
        List<Memory> local,
        List<Memory> server
    )
    {
        // Combine both lists
        var merged = new List<Memory>(local);
        
        // Add server memories not in local
        foreach (var serverMemory in server)
        {
            if (!merged.Any(m => m.Id == serverMemory.Id))
            {
                merged.Add(serverMemory);
            }
        }
        
        // Sort by significance and recency
        return merged
            .OrderByDescending(m => m.Significance)
            .ThenByDescending(m => m.CreatedAt)
            .ToList();
    }
}
```

---

## Synchronization System

### Sync Strategy: Eventual Consistency

```csharp
public class SyncManager : MonoBehaviour
{
    private static SyncManager _instance;
    public static SyncManager Instance => _instance;
    
    private Queue<SyncOperation> _syncQueue = new Queue<SyncOperation>();
    private bool _isSyncing = false;
    
    // Sync configuration
    private const int MAX_BATCH_SIZE = 50;
    private const int SYNC_INTERVAL_SECONDS = 30;
    
    void Awake()
    {
        _instance = this;
    }
    
    void Start()
    {
        // Start periodic sync
        InvokeRepeating(nameof(PeriodicSync), SYNC_INTERVAL_SECONDS, SYNC_INTERVAL_SECONDS);
        
        // Sync on app pause/resume
        Application.focusChanged += OnApplicationFocusChanged;
    }
    
    private void OnApplicationFocusChanged(bool hasFocus)
    {
        if (!hasFocus)
        {
            // App going to background, sync immediately
            StartCoroutine(SyncNow());
        }
        else
        {
            // App coming to foreground, pull latest
            StartCoroutine(PullLatestData());
        }
    }
    
    public void QueueSync(StateChange change)
    {
        var operation = new SyncOperation
        {
            Id = Guid.NewGuid().ToString(),
            Type = GetSyncType(change),
            EntityId = change.AffectedId,
            Data = SerializeChange(change),
            Timestamp = DateTime.UtcNow,
            Status = SyncStatus.Pending,
            Priority = CalculatePriority(change)
        };
        
        _syncQueue.Enqueue(operation);
        
        // Persist to database
        DatabaseManager.Instance.InsertSyncOperation(operation);
    }
    
    private void PeriodicSync()
    {
        if (!NetworkManager.Instance.IsOnline) return;
        if (_isSyncing) return;
        
        StartCoroutine(SyncNow());
    }
    
    private IEnumerator SyncNow()
    {
        _isSyncing = true;
        
        // Batch operations
        var batch = new List<SyncOperation>();
        
        while (_syncQueue.Count > 0 && batch.Count < MAX_BATCH_SIZE)
        {
            batch.Add(_syncQueue.Dequeue());
        }
        
        if (batch.Count == 0)
        {
            _isSyncing = false;
            yield break;
        }
        
        // Send to server
        var syncRequest = new SyncRequest
        {
            UserId = PlayerPrefs.GetString("user_id"),
            PlaythroughId = GameState.Instance.Player.PlaythroughId,
            Operations = batch,
            ClientVersion = Application.version,
            LastSyncVersion = GetLastSyncVersion()
        };
        
        var syncTask = SendSyncRequest(syncRequest);
        
        while (!syncTask.IsCompleted)
        {
            yield return null;
        }
        
        if (syncTask.IsCompletedSuccessfully)
        {
            var response = syncTask.Result;
            
            // Handle conflicts
            if (response.Conflicts.Count > 0)
            {
                ResolveConflicts(response.Conflicts);
            }
            
            // Apply server updates
            ApplyServerUpdates(response.ServerUpdates);
            
            // Mark operations as synced
            foreach (var operation in batch)
            {
                DatabaseManager.Instance.MarkOperationSynced(operation.Id);
            }
            
            // Update sync version
            SetLastSyncVersion(response.NewSyncVersion);
        }
        else
        {
            // Sync failed, re-queue operations
            foreach (var operation in batch)
            {
                _syncQueue.Enqueue(operation);
            }
        }
        
        _isSyncing = false;
        
        // If more operations, sync again
        if (_syncQueue.Count > 0)
        {
            yield return new WaitForSeconds(1);
            StartCoroutine(SyncNow());
        }
    }
    
    private async Task<SyncResponse> SendSyncRequest(SyncRequest request)
    {
        var httpClient = new HttpClient();
        
        var response = await httpClient.PostAsJsonAsync(
            "https://api.unwritten.game/v1/sync",
            request
        );
        
        response.EnsureSuccessStatusCode();
        
        return await response.Content.ReadAsAsync<SyncResponse>();
    }
    
    private void ResolveConflicts(List<Conflict> conflicts)
    {
        var resolver = new ConflictResolver();
        
        foreach (var conflict in conflicts)
        {
            var localState = GetLocalState(conflict.EntityId);
            var serverState = conflict.ServerState;
            
            var resolved = resolver.ResolveConflict(localState, serverState);
            
            // Apply resolved state
            ApplyResolvedState(resolved);
            
            // Track conflict resolution
            AnalyticsManager.Instance.TrackEvent("sync_conflict_resolved", new {
                entity_id = conflict.EntityId,
                strategy = resolved.ResolutionStrategy
            });
        }
    }
    
    private void ApplyServerUpdates(List<ServerUpdate> updates)
    {
        foreach (var update in updates)
        {
            switch (update.Type)
            {
                case UpdateType.CardUpdated:
                    UpdateCardFromServer(update);
                    break;
                    
                case UpdateType.MemoryAdded:
                    AddMemoryFromServer(update);
                    break;
                    
                case UpdateType.EvolutionCompleted:
                    ApplyEvolutionFromServer(update);
                    break;
            }
        }
    }
}
```

### Delta Sync Optimization

```csharp
public class DeltaSyncManager
{
    // Only sync what changed, not entire objects
    
    public SyncDelta GenerateDelta(Card oldCard, Card newCard)
    {
        var delta = new SyncDelta
        {
            EntityId = newCard.Id,
            EntityType = "card",
            Changes = new Dictionary<string, object>()
        };
        
        // Compare fields
        if (oldCard.Name != newCard.Name)
        {
            delta.Changes["name"] = newCard.Name;
        }
        
        if (oldCard.Description != newCard.Description)
        {
            delta.Changes["description"] = newCard.Description;
        }
        
        if (oldCard.Level != newCard.Level)
        {
            delta.Changes["level"] = newCard.Level;
        }
        
        // Compare complex objects
        if (!PersonalityTraitsEqual(oldCard.PersonalityTraits, newCard.PersonalityTraits))
        {
            delta.Changes["personality_traits"] = newCard.PersonalityTraits;
        }
        
        // Compare visual details
        var newDetails = newCard.VisualDetails
            .Where(d => !oldCard.VisualDetails.Any(od => od.Type == d.Type))
            .ToList();
        
        if (newDetails.Count > 0)
        {
            delta.Changes["visual_details_added"] = newDetails;
        }
        
        return delta;
    }
    
    public Card ApplyDelta(Card existingCard, SyncDelta delta)
    {
        var updated = existingCard.Clone();
        
        foreach (var change in delta.Changes)
        {
            switch (change.Key)
            {
                case "name":
                    updated.Name = (string)change.Value;
                    break;
                    
                case "description":
                    updated.Description = (string)change.Value;
                    break;
                    
                case "level":
                    updated.Level = (int)change.Value;
                    break;
                    
                case "personality_traits":
                    updated.PersonalityTraits = (PersonalityTraits)change.Value;
                    break;
                    
                case "visual_details_added":
                    var newDetails = (List<VisualDetail>)change.Value;
                    updated.VisualDetails.AddRange(newDetails);
                    break;
            }
        }
        
        return updated;
    }
}
```

### Optimistic UI Updates

```csharp
public class OptimisticUpdateManager
{
    // Apply changes immediately to UI, rollback if sync fails
    
    private Dictionary<string, object> _optimisticUpdates = new Dictionary<string, object>();
    
    public void ApplyOptimisticUpdate(string entityId, object newState)
    {
        // Save current state for potential rollback
        var currentState = GetCurrentState(entityId);
        _optimisticUpdates[entityId] = currentState;
        
        // Apply new state immediately
        ApplyState(entityId, newState);
        
        // UI updates instantly, player sees change
    }
    
    public void ConfirmUpdate(string entityId)
    {
        // Server confirmed, remove from optimistic updates
        _optimisticUpdates.Remove(entityId);
    }
    
    public void RollbackUpdate(string entityId)
    {
        // Server rejected, rollback to previous state
        if (_optimisticUpdates.TryGetValue(entityId, out var previousState))
        {
            ApplyState(entityId, previousState);
            _optimisticUpdates.Remove(entityId);
            
            // Show user feedback
            UIManager.Instance.ShowToast("Update failed, changes reverted");
        }
    }
}
```

---

## Mobile-Specific Optimizations

### Memory Management

```csharp
public class MobileMemoryManager : MonoBehaviour
{
    private const int TARGET_MEMORY_MB = 300; // 300MB budget
    
    private int _currentMemoryUsage = 0;
    
    void Start()
    {
        // Monitor memory usage
        InvokeRepeating(nameof(CheckMemoryUsage), 5f, 5f);
    }
    
    private void CheckMemoryUsage()
    {
        _currentMemoryUsage = (int)(Profiler.GetTotalAllocatedMemoryLong() / 1024 / 1024);
        
        if (_currentMemoryUsage > TARGET_MEMORY_MB)
        {
            // Aggressive cleanup
            PerformMemoryCleanup();
        }
        else if (_currentMemoryUsage > TARGET_MEMORY_MB * 0.8)
        {
            // Gentle cleanup
            PerformGentleCleanup();
        }
    }
    
    private void PerformMemoryCleanup()
    {
        Debug.Log($"Memory at {_currentMemoryUsage}MB, performing cleanup");
        
        // 1. Clear texture cache
        TextureCache.Instance.ClearLRU(50); // Keep only 50 most recent
        
        // 2. Unload unused card assets
        CardAssetManager.Instance.UnloadInactive();
        
        // 3. Clear old memories from cache
        MemoryCache.Instance.ClearOldest(100);
        
        // 4. Clear evolution cache
        EvolutionCache.Instance.ClearLowPriority();
        
        // 5. Unity's garbage collection
        Resources.UnloadUnusedAssets();
        GC.Collect();
        
        Debug.Log($"After cleanup: {Profiler.GetTotalAllocatedMemoryLong() / 1024 / 1024}MB");
    }
    
    private void PerformGentleCleanup()
    {
        // Less aggressive, just trim caches
        TextureCache.Instance.ClearLRU(75);
        MemoryCache.Instance.ClearOldest(50);
    }
    
    void OnApplicationPause(bool pauseStatus)
    {
        if (pauseStatus)
        {
            // App going to background, aggressive cleanup
            PerformMemoryCleanup();
        }
    }
}
```

### Battery Optimization

```csharp
public class BatteryOptimizer : MonoBehaviour
{
    private bool _lowPowerMode = false;
    
    void Start()
    {
        // Check battery level
        InvokeRepeating(nameof(CheckBatteryLevel), 0f, 30f);
    }
    
    private void CheckBatteryLevel()
    {
        var batteryLevel = SystemInfo.batteryLevel;
        
        if (batteryLevel < 0.2f && !_lowPowerMode)
        {
            // Battery low, enable power saving
            EnableLowPowerMode();
        }
        else if (batteryLevel > 0.5f && _lowPowerMode)
        {
            // Battery recovered, disable power saving
            DisableLowPowerMode();
        }
    }
    
    private void EnableLowPowerMode()
    {
        _lowPowerMode = true;
        
        Debug.Log("Low power mode enabled");
        
        // Reduce frame rate
        Application.targetFrameRate = 30;
        
        // Disable expensive effects
        VisualEffectsManager.Instance.SetQuality(VisualQuality.Low);
        
        // Reduce AI processing
        AIServiceManager.Instance.SetMode(AIMode.PowerSaving);
        
        // Disable background generation
        BackgroundGenerator.Instance.Pause();
        
        // Reduce update frequency
        CardUpdateManager.Instance.SetUpdateInterval(1f); // Once per second instead of every frame
        
        // Show notification to user
        UIManager.Instance.ShowToast("Battery saver mode enabled");
    }
    
    private void DisableLowPowerMode()
    {
        _lowPowerMode = false;
        
        Debug.Log("Low power mode disabled");
        
        Application.targetFrameRate = 60;
        VisualEffectsManager.Instance.SetQuality(VisualQuality.High);
        AIServiceManager.Instance.SetMode(AIMode.Normal);
        BackgroundGenerator.Instance.Resume();
        CardUpdateManager.Instance.SetUpdateInterval(0f);
    }
}
```

### Network Optimization

```csharp
public class NetworkOptimizer : MonoBehaviour
{
    private bool _isOnWiFi = false;
    private bool _isMetered = false;
    
    void Start()
    {
        CheckNetworkType();
        
        // Re-check periodically
        InvokeRepeating(nameof(CheckNetworkType), 0f, 10f);
    }
    
    private void CheckNetworkType()
    {
        var reachability = Application.internetReachability;
        
        _isOnWiFi = reachability == NetworkReachability.ReachableViaLocalAreaNetwork;
        _isMetered = reachability == NetworkReachability.ReachableViaCarrierDataNetwork;
        
        // Adjust behavior based on network type
        if (_isOnWiFi)
        {
            // Unrestricted
            EnableFullNetworkFeatures();
        }
        else if (_isMetered)
        {
            // Conservative
            EnableMeteredNetworkFeatures();
        }
        else
        {
            // Offline
            EnableOfflineFeatures();
        }
    }
    
    private void EnableMeteredNetworkFeatures()
    {
        // Reduce image quality
        ImageDownloader.Instance.SetQuality(ImageQuality.Compressed);
        
        // Batch sync operations more aggressively
        SyncManager.Instance.SetBatchSize(100); // Larger batches, fewer requests
        
        // Disable automatic portrait downloads
        PortraitDownloader.Instance.SetMode(DownloadMode.Manual);
        
        // Compress sync data
        SyncManager.Instance.EnableCompression(true);
        
        Debug.Log("Metered network detected, reducing data usage");
    }
    
    private void EnableFullNetworkFeatures()
    {
        ImageDownloader.Instance.SetQuality(ImageQuality.Full);
        SyncManager.Instance.SetBatchSize(50);
        PortraitDownloader.Instance.SetMode(DownloadMode.Automatic);
        SyncManager.Instance.EnableCompression(false);
    }
}
```

### Asset Streaming

```csharp
public class AssetStreamingManager : MonoBehaviour
{
    // Load assets on-demand, not all at once
    
    private Dictionary<string, AssetBundle> _loadedBundles = new Dictionary<string, AssetBundle>();
    
    public async Task<T> LoadAsset<T>(string assetPath) where T : Object
    {
        var bundleName = GetBundleForAsset(assetPath);
        
        // Load bundle if not already loaded
        if (!_loadedBundles.ContainsKey(bundleName))
        {
            await LoadBundle(bundleName);
        }
        
        // Load asset from bundle
        var bundle = _loadedBundles[bundleName];
        var asset = bundle.LoadAsset<T>(assetPath);
        
        return asset;
    }
    
    private async Task LoadBundle(string bundleName)
    {
        var bundlePath = $"{Application.persistentDataPath}/bundles/{bundleName}";
        
        // Check if bundle exists locally
        if (!File.Exists(bundlePath))
        {
            // Download from CDN
            await DownloadBundle(bundleName);
        }
        
        // Load bundle
        var bundleLoadRequest = AssetBundle.LoadFromFileAsync(bundlePath);
        
        while (!bundleLoadRequest.isDone)
        {
            await Task.Yield();
        }
        
        _loadedBundles[bundleName] = bundleLoadRequest.assetBundle;
    }
    
    private async Task DownloadBundle(string bundleName)
    {
        var url = $"https://cdn.unwritten.game/bundles/{bundleName}";
        var downloadPath = $"{Application.persistentDataPath}/bundles/{bundleName}";
        
        using (var www = UnityWebRequest.Get(url))
        {
            var operation = www.SendWebRequest();
            
            while (!operation.isDone)
            {
                // Show download progress
                UpdateDownloadProgress(bundleName, www.downloadProgress);
                await Task.Yield();
            }
            
            if (www.result == UnityWebRequest.Result.Success)
            {
                File.WriteAllBytes(downloadPath, www.downloadHandler.data);
            }
        }
    }
    
    public void UnloadBundle(string bundleName)
    {
        if (_loadedBundles.TryGetValue(bundleName, out var bundle))
        {
            bundle.Unload(false); // Keep assets loaded
            _loadedBundles.Remove(bundleName);
        }
    }
    
    void OnLowMemory()
    {
        // Unload unused bundles
        var unusedBundles = _loadedBundles
            .Where(kvp => !IsBundleInUse(kvp.Key))
            .Select(kvp => kvp.Key)
            .ToList();
        
        foreach (var bundleName in unusedBundles)
        {
            UnloadBundle(bundleName);
        }
    }
}
```

### Touch Input Optimization

```csharp
public class TouchInputManager : MonoBehaviour
{
    // Optimize for mobile touch input
    
    private const float SWIPE_THRESHOLD = 50f;
    private const float TAP_TIMEOUT = 0.3f;
    
    private Vector2 _touchStartPos;
    private float _touchStartTime;
    
    void Update()
    {
        if (Input.touchCount > 0)
        {
            HandleTouch(Input.GetTouch(0));
        }
    }
    
    private void HandleTouch(Touch touch)
    {
        switch (touch.phase)
        {
            case TouchPhase.Began:
                _touchStartPos = touch.position;
                _touchStartTime = Time.time;
                break;
                
            case TouchPhase.Ended:
                var touchDuration = Time.time - _touchStartTime;
                var touchDelta = touch.position - _touchStartPos;
                
                if (touchDuration < TAP_TIMEOUT && touchDelta.magnitude < 10f)
                {
                    // Tap
                    HandleTap(touch.position);
                }
                else if (touchDelta.magnitude > SWIPE_THRESHOLD)
                {
                    // Swipe
                    HandleSwipe(touchDelta);
                }
                break;
        }
    }
    
    private void HandleTap(Vector2 position)
    {
        // Raycast to see what was tapped
        var ray = Camera.main.ScreenPointToRay(position);
        
        if (Physics.Raycast(ray, out var hit))
        {
            var tappable = hit.collider.GetComponent<ITappable>();
            tappable?.OnTap();
        }
    }
    
    private void HandleSwipe(Vector2 delta)
    {
        // Determine swipe direction
        var direction = GetSwipeDirection(delta);
        
        // For card interactions (Reigns-style)
        if (CardInteractionManager.Instance.IsCardActive())
        {
            CardInteractionManager.Instance.HandleSwipe(direction);
        }
    }
    
    private SwipeDirection GetSwipeDirection(Vector2 delta)
    {
        var angle = Mathf.Atan2(delta.y, delta.x) * Mathf.Rad2Deg;
        
        if (angle > -45f && angle <= 45f) return SwipeDirection.Right;
        if (angle > 45f && angle <= 135f) return SwipeDirection.Up;
        if (angle > 135f || angle <= -135f) return SwipeDirection.Left;
        return SwipeDirection.Down;
    }
}
```

---

## Security & Data Protection

### Data Encryption

```csharp
public class EncryptionManager
{
    private readonly string _encryptionKey;
    
    public EncryptionManager()
    {
        // Generate or retrieve encryption key
        _encryptionKey = GetOrCreateEncryptionKey();
    }
    
    private string GetOrCreateEncryptionKey()
    {
        const string keyPrefKey = "encryption_key";
        
        if (PlayerPrefs.HasKey(keyPrefKey))
        {
            return PlayerPrefs.GetString(keyPrefKey);
        }
        
        // Generate new key
        var key = GenerateRandomKey(32);
        PlayerPrefs.SetString(keyPrefKey, key);
        PlayerPrefs.Save();
        
        return key;
    }
    
    public string Encrypt(string plainText)
    {
        if (string.IsNullOrEmpty(plainText))
            return plainText;
        
        using (var aes = Aes.Create())
        {
            aes.Key = Encoding.UTF8.GetBytes(_encryptionKey);
            aes.GenerateIV();
            
            var encryptor = aes.CreateEncryptor(aes.Key, aes.IV);
            
            using (var msEncrypt = new MemoryStream())
            {
                // Write IV to beginning of stream
                msEncrypt.Write(aes.IV, 0, aes.IV.Length);
                
                using (var csEncrypt = new CryptoStream(msEncrypt, encryptor, CryptoStreamMode.Write))
                using (var swEncrypt = new StreamWriter(csEncrypt))
                {
                    swEncrypt.Write(plainText);
                }
                
                return Convert.ToBase64String(msEncrypt.ToArray());
            }
        }
    }
    
    public string Decrypt(string cipherText)
    {
        if (string.IsNullOrEmpty(cipherText))
            return cipherText;
        
        var buffer = Convert.FromBase64String(cipherText);
        
        using (var aes = Aes.Create())
        {
            aes.Key = Encoding.UTF8.GetBytes(_encryptionKey);
            
            // Extract IV from beginning of buffer
            var iv = new byte[aes.IV.Length];
            Array.Copy(buffer, 0, iv, 0, iv.Length);
            aes.IV = iv;
            
            var decryptor = aes.CreateDecryptor(aes.Key, aes.IV);
            
            using (var msDecrypt = new MemoryStream(buffer, iv.Length, buffer.Length - iv.Length))
            using (var csDecrypt = new CryptoStream(msDecrypt, decryptor, CryptoStreamMode.Read))
            using (var srDecrypt = new StreamReader(csDecrypt))
            {
                return srDecrypt.ReadToEnd();
            }
        }
    }
    
    private string GenerateRandomKey(int length)
    {
        const string chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        var random = new System.Random();
        return new string(Enumerable.Repeat(chars, length)
            .Select(s => s[random.Next(s.Length)]).ToArray());
    }
}

// Usage in database manager
public class SecureDatabaseManager : DatabaseManager
{
    private EncryptionManager _encryption = new EncryptionManager();
    
    public override void SaveCard(Card card)
    {
        // Encrypt sensitive data before saving
        var encryptedDescription = _encryption.Encrypt(card.Description);
        var encryptedMemories = _encryption.Encrypt(JsonConvert.SerializeObject(card.Memories));
        
        // Save to database
        var sql = @"
            INSERT INTO cards (id, name, description, memories, ...)
            VALUES (@id, @name, @description, @memories, ...)
        ";
        
        ExecuteNonQuery(sql, new {
            id = card.Id,
            name = card.Name,
            description = encryptedDescription,
            memories = encryptedMemories
        });
    }
    
    public override Card LoadCard(string id)
    {
        var card = base.LoadCard(id);
        
        // Decrypt sensitive data
        card.Description = _encryption.Decrypt(card.Description);
        
        var memoriesJson = _encryption.Decrypt(card.MemoriesJson);
        card.Memories = JsonConvert.DeserializeObject<List<Memory>>(memoriesJson);
        
        return card;
    }
}
```

### API Security

```csharp
public class SecureAPIClient
{
    private readonly string _apiUrl;
    private readonly string _apiKey;
    private string _accessToken;
    private string _refreshToken;
    
    public SecureAPIClient(string apiUrl)
    {
        _apiUrl = apiUrl;
        _apiKey = GetAPIKey(); // Obfuscated in build
    }
    
    public async Task<T> AuthenticatedRequest<T>(
        string endpoint, 
        HttpMethod method, 
        object data = null
    )
    {
        // Ensure we have valid access token
        await EnsureAuthenticated();
        
        using (var client = new HttpClient())
        {
            // Add authentication header
            client.DefaultRequestHeaders.Authorization = 
                new AuthenticationHeaderValue("Bearer", _accessToken);
            
            // Add API key
            client.DefaultRequestHeaders.Add("X-API-Key", _apiKey);
            
            // Add request signature
            var signature = GenerateRequestSignature(endpoint, method, data);
            client.DefaultRequestHeaders.Add("X-Request-Signature", signature);
            
            HttpResponseMessage response;
            
            if (method == HttpMethod.Get)
            {
                response = await client.GetAsync($"{_apiUrl}{endpoint}");
            }
            else if (method == HttpMethod.Post)
            {
                var content = new StringContent(
                    JsonConvert.SerializeObject(data),
                    Encoding.UTF8,
                    "application/json"
                );
                response = await client.PostAsync($"{_apiUrl}{endpoint}", content);
            }
            else
            {
                throw new NotSupportedException($"Method {method} not supported");
            }
            
            // Check for token expiration
            if (response.StatusCode == System.Net.HttpStatusCode.Unauthorized)
            {
                // Refresh token and retry
                await RefreshAccessToken();
                return await AuthenticatedRequest<T>(endpoint, method, data);
            }
            
            response.EnsureSuccessStatusCode();
            
            var responseContent = await response.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<T>(responseContent);
        }
    }
    
    private string GenerateRequestSignature(string endpoint, HttpMethod method, object data)
    {
        // Generate HMAC signature to prevent tampering
        var message = $"{method}:{endpoint}:{JsonConvert.SerializeObject(data ?? "")}";
        
        using (var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(_apiKey)))
        {
            var hash = hmac.ComputeHash(Encoding.UTF8.GetBytes(message));
            return Convert.ToBase64String(hash);
        }
    }
    
    private async Task EnsureAuthenticated()
    {
        if (string.IsNullOrEmpty(_accessToken))
        {
            await Login();
        }
        else if (IsTokenExpired(_accessToken))
        {
            await RefreshAccessToken();
        }
    }
    
    private async Task RefreshAccessToken()
    {
        using (var client = new HttpClient())
        {
            var request = new RefreshTokenRequest
            {
                RefreshToken = _refreshToken
            };
            
            var response = await client.PostAsJsonAsync(
                $"{_apiUrl}/auth/refresh",
                request
            );
            
            if (!response.IsSuccessStatusCode)
            {
                // Refresh token invalid, need to login again
                await Login();
                return;
            }
            
            var result = await response.Content.ReadAsAsync<TokenResponse>();
            
            _accessToken = result.AccessToken;
            _refreshToken = result.RefreshToken;
            
            // Save tokens securely
            SaveTokensSecurely();
        }
    }
}
```

### Anti-Cheat Measures

```csharp
public class AntiCheatManager : MonoBehaviour
{
    // Detect tampering and cheating
    
    private float _lastChecksum;
    private int _checkInterval = 0;
    
    void Start()
    {
        // Initial checksum
        _lastChecksum = CalculateGameStateChecksum();
        
        // Periodic integrity checks
        InvokeRepeating(nameof(PerformIntegrityCheck), 30f, 30f);
    }
    
    void Update()
    {
        _checkInterval++;
        
        // Lightweight checks every frame
        if (_checkInterval % 60 == 0)
        {
            CheckTimeManipulation();
        }
        
        if (_checkInterval % 300 == 0)
        {
            CheckMemoryTampering();
        }
    }
    
    private void PerformIntegrityCheck()
    {
        var currentChecksum = CalculateGameStateChecksum();
        
        // Compare with expected checksum
        var expectedChecksum = CalculateExpectedChecksum();
        
        if (Math.Abs(currentChecksum - expectedChecksum) > 0.001f)
        {
            // State has been tampered with
            HandleTampering("Game state checksum mismatch");
        }
        
        _lastChecksum = currentChecksum;
    }
    
    private float CalculateGameStateChecksum()
    {
        var player = GameState.Instance.Player;
        
        // Calculate checksum from critical values
        var checksum = 0f;
        checksum += player.PhysicalStat * 1.1f;
        checksum += player.MentalStat * 1.2f;
        checksum += player.SocialStat * 1.3f;
        checksum += player.EmotionalStat * 1.4f;
        checksum += (float)player.Money * 0.001f;
        checksum += player.GameDay * 2.5f;
        
        return checksum;
    }
    
    private void CheckTimeManipulation()
    {
        // Check if system time was changed
        var serverTime = GetServerTime();
        var localTime = DateTime.UtcNow;
        
        var timeDelta = Math.Abs((serverTime - localTime).TotalSeconds);
        
        if (timeDelta > 300) // 5 minutes difference
        {
            HandleTampering("Time manipulation detected");
        }
    }
    
    private void CheckMemoryTampering()
    {
        // Validate critical values are within reasonable bounds
        var player = GameState.Instance.Player;
        
        if (player.PhysicalStat < 0 || player.PhysicalStat > 10)
        {
            HandleTampering("Invalid stat value");
        }
        
        if (player.Money < 0 || player.Money > 999999999)
        {
            HandleTampering("Invalid money value");
        }
        
        // Check for impossible progression
        if (player.GameDay < 1 || player.GameDay > 10000)
        {
            HandleTampering("Invalid game day");
        }
    }
    
    private void HandleTampering(string reason)
    {
        Debug.LogError($"Tampering detected: {reason}");
        
        // Log to server
        AnalyticsManager.Instance.TrackEvent("anti_cheat_triggered", new {
            reason = reason,
            user_id = PlayerPrefs.GetString("user_id"),
            timestamp = DateTime.UtcNow
        });
        
        // For now, just log. In production, could:
        // - Flag account for review
        // - Reset to last known good state
        // - Temporarily disable online features
        // - Show warning to user
    }
}
```

---

## Analytics & Telemetry

### Analytics Manager

```csharp
public class AnalyticsManager : MonoBehaviour
{
    private static AnalyticsManager _instance;
    public static AnalyticsManager Instance => _instance;
    
    private Queue<AnalyticsEvent> _eventQueue = new Queue<AnalyticsEvent>();
    
    void Awake()
    {
        _instance = this;
    }
    
    void Start()
    {
        // Periodic flush to server
        InvokeRepeating(nameof(FlushEvents), 30f, 30f);
    }
    
    public void TrackEvent(string eventType, object properties = null)
    {
        var analyticsEvent = new AnalyticsEvent
        {
            Id = Guid.NewGuid().ToString(),
            EventType = eventType,
            Properties = properties != null ? JsonConvert.SerializeObject(properties) : "{}",
            Timestamp = DateTime.UtcNow,
            SessionId = GetSessionId(),
            UserId = GetUserId(),
            Platform = Application.platform.ToString(),
            AppVersion = Application.version
        };
        
        // Save to local database
        DatabaseManager.Instance.InsertAnalyticsEvent(analyticsEvent);
        
        // Add to queue for sending
        _eventQueue.Enqueue(analyticsEvent);
        
        // Debug log
        Debug.Log($"Analytics: {eventType} - {properties}");
    }
    
    private void FlushEvents()
    {
        if (_eventQueue.Count == 0) return;
        if (!NetworkManager.Instance.IsOnline) return;
        
        var batch = new List<AnalyticsEvent>();
        
        while (_eventQueue.Count > 0 && batch.Count < 100)
        {
            batch.Add(_eventQueue.Dequeue());
        }
        
        StartCoroutine(SendEventBatch(batch));
    }
    
    private IEnumerator SendEventBatch(List<AnalyticsEvent> events)
    {
        var request = new AnalyticsBatchRequest
        {
            Events = events
        };
        
        var httpClient = new HttpClient();
        var sendTask = httpClient.PostAsJsonAsync(
            "https://api.unwritten.game/v1/analytics",
            request
        );
        
        while (!sendTask.IsCompleted)
        {
            yield return null;
        }
        
        if (sendTask.IsCompletedSuccessfully)
        {
            // Mark as sent in database
            foreach (var analyticsEvent in events)
            {
                DatabaseManager.Instance.MarkAnalyticsEventSent(analyticsEvent.Id);
            }
        }
        else
        {
            // Failed to send, re-queue
            foreach (var analyticsEvent in events)
            {
                _eventQueue.Enqueue(analyticsEvent);
            }
        }
    }
    
    // Specific tracking methods
    
    public void TrackCardEvolution(Card card, int oldLevel, int newLevel)
    {
        TrackEvent("card_evolved", new {
            card_id = card.Id,
            card_type = card.CardType,
            old_level = oldLevel,
            new_level = newLevel,
            game_day = GameState.Instance.Player.GameDay
        });
    }
    
    public void TrackCardFusion(List<string> inputCardIds, string outputCardId, string fusionType)
    {
        TrackEvent("card_fusion", new {
            input_cards = inputCardIds,
            output_card = outputCardId,
            fusion_type = fusionType
        });
    }
    
    public void TrackAIGeneration(string route, int durationMs, float importance)
    {
        TrackEvent("ai_generation", new {
            route = route,
            duration_ms = durationMs,
            importance = importance
        });
    }
    
    public void TrackScreenView(string screenName)
    {
        TrackEvent("screen_view", new {
            screen_name = screenName
        });
    }
    
    public void TrackPurchase(string productId, decimal price, string currency)
    {
        TrackEvent("purchase", new {
            product_id = productId,
            price = price,
            currency = currency
        });
    }
}
```

### Key Metrics to Track

```csharp
public class MetricsTracker : MonoBehaviour
{
    // Track important game metrics
    
    void Start()
    {
        // Session start
        AnalyticsManager.Instance.TrackEvent("session_start", new {
            session_id = GetSessionId(),
            user_tier = GameState.Instance.Player.Tier
        });
        
        // Track key milestones
        TrackKeyMilestones();
    }
    
    private void TrackKeyMilestones()
    {
        var player = GameState.Instance.Player;
        
        // First card evolution
        if (player.TotalCardEvolutions == 1)
        {
            AnalyticsManager.Instance.TrackEvent("milestone_first_evolution");
        }
        
        // First Level 5 card
        var level5Cards = GameState.Instance.Cards.GetAllCards()
            .Count(c => c.Level >= 5);
        
        if (level5Cards == 1)
        {
            AnalyticsManager.Instance.TrackEvent("milestone_first_legendary");
        }
        
        // Played 7 days
        if (player.TotalPlayDays == 7)
        {
            AnalyticsManager.Instance.TrackEvent("milestone_week_played");
        }
    }
    
    void OnApplicationQuit()
    {
        // Track session end
        AnalyticsManager.Instance.TrackEvent("session_end", new {
            session_duration = Time.time,
            cards_evolved = GetSessionCardEvolutions(),
            interactions = GetSessionInteractions()
        });
        
        // Flush remaining events
        AnalyticsManager.Instance.FlushEvents();
    }
}
```

### A/B Testing Framework

```csharp
public class ABTestManager : MonoBehaviour
{
    private Dictionary<string, string> _activeTests = new Dictionary<string, string>();
    
    void Start()
    {
        // Fetch active A/B tests from server
        StartCoroutine(FetchABTests());
    }
    
    private IEnumerator FetchABTests()
    {
        var httpClient = new HttpClient();
        var fetchTask = httpClient.GetAsync(
            "https://api.unwritten.game/v1/ab-tests"
        );
        
        while (!fetchTask.IsCompleted)
        {
            yield return null;
        }
        
        if (fetchTask.IsCompletedSuccessfully)
        {
            var response = fetchTask.Result;
            var tests = await response.Content.ReadAsAsync<ABTestResponse>();
            
            foreach (var test in tests.ActiveTests)
            {
                var variant = AssignVariant(test);
                _activeTests[test.TestId] = variant;
                
                // Track assignment
                AnalyticsManager.Instance.TrackEvent("ab_test_assigned", new {
                    test_id = test.TestId,
                    variant = variant
                });
            }
        }
    }
    
    private string AssignVariant(ABTest test)
    {
        var userId = GetUserId();
        var hash = GetConsistentHash(userId + test.TestId);
        
        // Deterministic assignment based on user ID
        var variants = test.Variants;
        var index = hash % variants.Count;
        
        return variants[index];
    }
    
    public string GetVariant(string testId)
    {
        return _activeTests.TryGetValue(testId, out var variant) 
            ? variant 
            : "control";
    }
    
    public bool IsVariant(string testId, string variantName)
    {
        return GetVariant(testId) == variantName;
    }
    
    // Usage examples:
    public void ShowOnboardingFlow()
    {
        if (ABTestManager.Instance.IsVariant("onboarding_v2", "test"))
        {
            ShowNewOnboarding();
        }
        else
        {
            ShowOriginalOnboarding();
        }
    }
    
    public float GetEvolutionSpeed()
    {
        var variant = ABTestManager.Instance.GetVariant("evolution_speed");
        
        return variant switch
        {
            "fast" => 1.5f,
            "slow" => 0.75f,
            _ => 1.0f
        };
    }
}
```

---

## Scalability Architecture

### Backend Scalability

```python
# Python backend service with horizontal scaling

from fastapi import FastAPI, BackgroundTasks
from redis import Redis
from typing import List
import asyncio

app = FastAPI()
redis_client = Redis(host='redis', port=6379)

# Worker pool for AI generation
class AIWorkerPool:
    def __init__(self, num_workers=10):
        self.num_workers = num_workers
        self.workers = []
        
    async def start(self):
        for i in range(self.num_workers):
            worker = AIWorker(worker_id=i)
            self.workers.append(worker)
            asyncio.create_task(worker.run())
    
    async def submit_job(self, job: AIGenerationJob):
        # Add to Redis queue
        await redis_client.lpush('ai_generation_queue', job.to_json())

class AIWorker:
    def __init__(self, worker_id: int):
        self.worker_id = worker_id
        self.is_running = True
        
    async def run(self):
        while self.is_running:
            # Pop job from queue (blocking)
            job_data = await redis_client.brpop('ai_generation_queue', timeout=1)
            
            if job_data:
                job = AIGenerationJob.from_json(job_data[1])
                
                try:
                    result = await self.process_job(job)
                    
                    # Save result to database
                    await save_generation_result(job.id, result)
                    
                    # Notify client via WebSocket or push notification
                    await notify_client(job.user_id, result)
                    
                except Exception as e:
                    # Handle error, retry if needed
                    await handle_job_error(job, e)
    
    async def process_job(self, job: AIGenerationJob):
        if job.generation_type == 'text':
            return await generate_text(job)
        elif job.generation_type == 'image':
            return await generate_image(job)

# API endpoints
@app.post("/v1/evolution/generate")
async def generate_evolution(
    request: EvolutionRequest,
    background_tasks: BackgroundTasks
):
    # Create job
    job = AIGenerationJob(
        user_id=request.user_id,
        generation_type='text',
        input_data=request.to_dict()
    )
    
    # Submit to worker pool
    await worker_pool.submit_job(job)
    
    # Return immediately (async processing)
    return {
        "status": "processing",
        "job_id": job.id,
        "estimated_time": 5
    }

@app.get("/v1/evolution/{job_id}/status")
async def get_job_status(job_id: str):
    # Check job status
    result = await get_generation_result(job_id)
    
    if result:
        return {
            "status": "complete",
            "result": result
        }
    else:
        return {
            "status": "processing"
        }

# Load balancing
if __name__ == "__main__":
    import uvicorn
    
    # Start worker pool
    worker_pool = AIWorkerPool(num_workers=10)
    asyncio.run(worker_pool.start())
    
    # Start server (behind nginx load balancer)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=4  # Multiple processes
    )
```

### Database Scaling

```sql
-- Partitioning strategy for analytics

-- Partition by time (monthly)
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY,
    user_id UUID,
    event_type VARCHAR(100),
    event_data JSONB,
    created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Create partitions for each month
CREATE TABLE analytics_events_2025_01 
    PARTITION OF analytics_events
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE analytics_events_2025_02 
    PARTITION OF analytics_events
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- Automatic partition management
CREATE OR REPLACE FUNCTION create_next_partition()
RETURNS void AS $
DECLARE
    next_month DATE;
    partition_name TEXT;
BEGIN
    next_month := date_trunc('month', CURRENT_DATE + INTERVAL '1 month');
    partition_name := 'analytics_events_' || to_char(next_month, 'YYYY_MM');
    
    EXECUTE format('
        CREATE TABLE IF NOT EXISTS %I
        PARTITION OF analytics_events
        FOR VALUES FROM (%L) TO (%L)',
        partition_name,
        next_month,
        next_month + INTERVAL '1 month'
    );
END;
$ LANGUAGE plpgsql;

-- Sharding strategy for user data

-- Shard by user_id hash
CREATE EXTENSION postgres_fdw;

-- Define shards
CREATE SERVER shard_1
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host 'db-shard-1.internal', port '5432', dbname 'unwritten');

CREATE SERVER shard_2
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host 'db-shard-2.internal', port '5432', dbname 'unwritten');

-- Create foreign tables
CREATE FOREIGN TABLE users_shard_1 (
    id UUID,
    email VARCHAR(255),
    ...
) SERVER shard_1 OPTIONS (table_name 'users');

CREATE FOREIGN TABLE users_shard_2 (
    id UUID,
    email VARCHAR(255),
    ...
) SERVER shard_2 OPTIONS (table_name 'users');

-- Routing logic (in application)
def get_shard_for_user(user_id: UUID) -> str:
    shard_count = 2
    shard_num = hash(str(user_id)) % shard_count
    return f"shard_{shard_num + 1}"
```

### CDN Strategy

```javascript
// Asset delivery via CDN

const CDN_CONFIG = {
    base_url: 'https://cdn.unwritten.game',
    
    // Asset types and their CDN paths
    paths: {
        portraits: '/portraits',
        card_assets: '/cards',
        bundles: '/bundles',
        static: '/static'
    },
    
    // Regional endpoints for lower latency
    regions: {
        'us-east': 'https://us-east.cdn.unwritten.game',
        'us-west': 'https://us-west.cdn.unwritten.game',
        'eu': 'https://eu.cdn.unwritten.game',
        'asia': 'https://asia.cdn.unwritten.game'
    }
};

class CDNManager {
    getAssetURL(assetPath, assetType) {
        // Detect user's region
        const region = this.detectRegion();
        
        // Use regional CDN endpoint
        const baseURL = CDN_CONFIG.regions[region] || CDN_CONFIG.base_url;
        const typePath = CDN_CONFIG.paths[assetType];
        
        return `${baseURL}${typePath}/${assetPath}`;
    }
    
    detectRegion() {
        // Could use geolocation API or server hint
        // For now, simple heuristic
        const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        
        if (timezone.startsWith('America/')) {
            return timezone.includes('Los_Angeles') || timezone.includes('Phoenix') 
                ? 'us-west' 
                : 'us-east';
        } else if (timezone.startsWith('Europe/')) {
            return 'eu';
        } else if (timezone.startsWith('Asia/')) {
            return 'asia';
        }
        
        return 'us-east'; // Default
    }
}
```

### Caching Strategy

```
┌─────────────────────────────────────────┐
│         CLIENT REQUEST                   │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│     CDN CACHE (CloudFlare)              │
│     • Static assets: 1 year             │
│     • Images: 1 month                   │
│     • API responses: 5 minutes          │
└─────────────┬───────────────────────────┘
              │ Cache miss
              ▼
┌─────────────────────────────────────────┐
│     LOAD BALANCER (nginx)               │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│     REDIS CACHE LAYER                   │
│     • AI generations: 1 hour            │
│     • User sessions: 24 hours           │
│     • Hot data: Variable TTL            │
└─────────────┬───────────────────────────┘
              │ Cache miss
              ▼
┌─────────────────────────────────────────┐
│     APPLICATION SERVER                   │
│     • Generate/fetch data               │
│     • Update caches                     │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│     DATABASE (PostgreSQL)               │
│     • Primary data store                │
└─────────────────────────────────────────┘
```

---

## Performance Benchmarks & Targets

### Target Metrics

```javascript
const PERFORMANCE_TARGETS = {
    
    // Client-side performance
    client: {
        app_launch_time: '< 3 seconds',
        card_render_time: '< 100ms',
        ui_response_time: '< 16ms (60 FPS)',
        memory_usage: '< 300MB',
        battery_drain: '< 10% per hour',
        
        ai_generation: {
            local_simple: '< 200ms',
            local_complex: '< 1000ms',
            cloud_perceived: '< 500ms (with UX tricks)'
        },
        
        sync_time: '< 2 seconds',
        offline_capable: true
    },
    
    // Server-side performance
    server: {
        api_response_time: {
            p50: '< 100ms',
            p95: '< 500ms',
            p99: '< 1000ms'
        },
        
        ai_generation_time: {
            text_simple: '< 2 seconds',
            text_complex: '< 5 seconds',
            image: '< 20 seconds'
        },
        
        throughput: {
            requests_per_second: '> 10,000',
            concurrent_users: '> 100,000',
            ai_generations_per_minute: '> 1,000'
        },
        
        availability: {
            uptime: '> 99.9%',
            error_rate: '< 0.1%'
        }
    },
    
    // Database performance
    database: {
        query_time: {
            simple_reads: '< 10ms',
            complex_reads: '< 100ms',
            writes: '< 50ms'
        },
        
        cache_hit_rate: '> 90%',
        connection_pool: '1000 connections'
    }
};
```

### Monitoring & Alerting

```python
# Server-side monitoring with Prometheus

from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics
api_requests = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

api_latency = Histogram(
    'api_request_duration_seconds',
    'API request latency',
    ['method', 'endpoint']
)

ai_generation_time = Histogram(
    'ai_generation_duration_seconds',
    'AI generation time',
    ['generation_type']
)

active_users = Gauge(
    'active_users',
    'Number of active users'
)

# Middleware to track metrics
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    # Record metrics
    duration = time.time() - start_time
    
    api_requests.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    api_latency.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response

# Alert rules (Prometheus AlertManager)
"""
groups:
- name: api_performance
  rules:
  - alert: HighAPILatency
    expr: api_request_duration_seconds{quantile="0.95"} > 1
    for: 5m
    annotations:
      summary: "High API latency detected"
      
  - alert: HighErrorRate
    expr: rate(api_requests_total{status=~"5.."}[5m]) > 0.01
    for: 5m
    annotations:
      summary: "High error rate detected"
"""
```

---

## Disaster Recovery & Backup

### Backup Strategy

```bash
#!/bin/bash
# Automated backup script

# Full database backup daily
pg_dump -h $DB_HOST -U $DB_USER unwritten | gzip > /backups/unwritten_$(date +%Y%m%d).sql.gz

# Upload to S3 with versioning
aws s3 cp /backups/unwritten_$(date +%Y%m%d).sql.gz s3://unwritten-backups/database/

# Incremental WAL archiving (continuous)
# PostgreSQL configured with:
# archive_mode = on
# archive_command = 'aws s3 cp %p s3://unwritten-wal-archive/%f'

# Backup retention: 30 days full, 90 days WAL
```

### Disaster Recovery Plan

```markdown
# Disaster Recovery Runbook

## RTO (Recovery Time Objective): 1 hour
## RPO (Recovery Point Objective): 5 minutes

### Scenario 1: Database Failure

1. Detect failure (automated monitoring alerts)
2. Failover to hot standby replica (automatic, < 30 seconds)
3. Verify data integrity
4. Update DNS to point to new primary
5. Restore WAL from archive if needed
6. Investigate and fix original primary

### Scenario 2: Complete Data Center Failure

1. Activate disaster recovery data center
2. Restore latest database backup to DR environment
3. Apply WAL archives up to failure point
4. Update DNS to point to DR environment
5. Scale up capacity as needed
6. Monitor for issues

### Scenario 3: Data Corruption

1. Identify corruption point (timestamp)
2. Restore from backup prior to corruption
3. Apply WAL up to corruption point
4. Manually fix corrupted records if possible
5. Communicate with affected users
6. Implement prevention measures

### Testing

- Monthly: Backup restoration test
- Quarterly: Full DR drill
- Annually: Complete disaster simulation
```

---

## Conclusion

This technical architecture provides:

1. **Scalable Foundation**
   - Horizontal scaling for backend services
   - Database sharding and partitioning
   - CDN distribution for global reach
   - Efficient caching at multiple layers

2. **Mobile-Optimized Performance**
   - Memory management < 300MB
   - Battery optimization < 10% drain/hour
   - Offline-first architecture
   - Smart asset streaming

3. **Robust Security**
   - End-to-end encryption
   - Secure API authentication
   - Anti-cheat measures
   - Data protection compliance

4. **Production-Ready Operations**
   - Comprehensive monitoring
   - Automated alerting
   - Disaster recovery
   - A/B testing framework

5. **Cost-Effective Design**
   - Aggressive caching reduces API costs
   - Hybrid local/cloud AI reduces compute costs
   - Efficient sync minimizes bandwidth
   - Scalable infrastructure optimizes hosting costs

**This architecture supports:**
- 100,000+ concurrent users
- 1,000+ AI generations per minute
- 99.9% uptime
- Sub-second response times
- Global availability

**Ready for production deployment.**

---

**Documents Complete:**
1. ✅ Card Combination Trees & Fusion System
2. ✅ AI Prompt Engineering for Character Evolution
3. ✅ Technical Architecture for Card Evolution System

**Next Documents Available:**
4. Specific Scenarios and Fusion Card Outcomes
5. Achievement/Unlock Progression System