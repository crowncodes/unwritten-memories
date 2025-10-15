# Unwritten Implementation Plan — MVP to Playable Loop

> **Canonical Reference**: Master Truths v1.2  
> **Purpose**: Phased implementation plan focused on getting a playable game loop with cloud AI and training data collection. Local AI optimization, advanced graphics, and cloud saves deferred to later phases.
>
> **Last Updated**: October 14, 2025

---

## Executive Summary

**Core Goal**: Build a playable game loop that generates high-quality training data from real gameplay, using cloud-based AI for flexibility and iteration speed.

**Architecture**: Adopts proven I/O FLIP patterns (Flutter + Dart Frog backend + Firebase), adapted for single-player narrative gameplay with AI generation.

**Philosophy**: 
- **Playable over perfect** - Get core loop working, then iterate
- **Full-stack Dart** - Flutter frontend + Dart Frog backend for code sharing
- **Backend-authoritative** - Server validates actions and generates AI content
- **Cloud AI first** - No on-device inference complexity in MVP
- **Training data focus** - Every interaction captured for model improvement
- **Defer optimization** - Graphics polish and local AI come after gameplay validation

**Timeline**: 20 weeks to playable MVP, 24 weeks to beta-ready

**Key Architecture Decision**: We adopt I/O FLIP's Dart Frog backend instead of direct client API calls. This provides:
1. **Shared game logic** between frontend/backend (like I/O FLIP's match_solver)
2. **Server authority** for validation and content generation
3. **Better scalability** with Cloud Run auto-scaling
4. **Centralized training data collection**
5. **Full-stack Dart** for code reuse and type safety

---

## Phase 1: Foundation (Weeks 1-4)

### Goal
Set up Flutter project with Clean Architecture, basic UI, and card data models. No AI yet.

### Deliverables

#### 1.1 Project Setup
```bash
unwritten/
├── lib/
│   ├── core/
│   │   ├── constants/
│   │   │   └── game_constants.dart
│   │   ├── errors/
│   │   │   └── exceptions.dart
│   │   └── utils/
│   │       └── app_logger.dart
│   ├── features/
│   │   ├── cards/
│   │   │   ├── data/
│   │   │   │   ├── models/
│   │   │   │   │   ├── card_model.dart
│   │   │   │   │   └── card_type.dart
│   │   │   │   └── repositories/
│   │   │   │       └── card_repository.dart
│   │   │   ├── domain/
│   │   │   │   ├── entities/
│   │   │   │   │   └── card.dart
│   │   │   │   └── usecases/
│   │   │   │       └── get_cards_usecase.dart
│   │   │   └── presentation/
│   │   │       ├── widgets/
│   │   │       │   └── card_widget.dart
│   │   │       └── screens/
│   │   │           └── card_hand_screen.dart
│   │   ├── game/
│   │   │   └── [similar structure]
│   │   └── relationships/
│   │       └── [similar structure]
│   └── shared/
│       ├── widgets/
│       └── services/
└── assets/
    ├── data/
    │   └── base_cards.json
    └── images/
        └── cards/
```

#### 1.2 Core Data Models

**Card Model** (`features/cards/data/models/card_model.dart`):
```dart
/// Card data model representing atomic game content.
/// 
/// Cards are the primary interaction units in Unwritten.
/// Each card has costs, effects, and evolution potential.
/// 
/// Example:
/// ```dart
/// final card = CardModel(
///   id: 'act_coffee_chat_001',
///   type: CardType.activity,
///   title: 'Coffee Chat',
///   description: 'Casual conversation over coffee',
///   costs: {'energy': 1.0, 'time': 1.0, 'money': 5.0},
///   effects: {'relationship_gain': 0.1},
/// );
/// ```
class CardModel {
  final String id;
  final CardType type;
  final String title;
  final String description;
  final Map<String, double> costs;
  final Map<String, double> effects;
  final int evolutionLevel;
  final List<String> fusionCompatibility;
  final Map<String, dynamic>? metadata;

  const CardModel({
    required this.id,
    required this.type,
    required this.title,
    required this.description,
    required this.costs,
    required this.effects,
    this.evolutionLevel = 0,
    this.fusionCompatibility = const [],
    this.metadata,
  });

  factory CardModel.fromJson(Map<String, dynamic> json) => CardModel(
    id: json['id'] as String,
    type: CardType.values.byName(json['type'] as String),
    title: json['title'] as String,
    description: json['description'] as String,
    costs: Map<String, double>.from(json['costs'] as Map),
    effects: Map<String, double>.from(json['effects'] as Map),
    evolutionLevel: json['evolution_level'] as int? ?? 0,
    fusionCompatibility: (json['fusion_compatibility'] as List?)?.cast<String>() ?? [],
    metadata: json['metadata'] as Map<String, dynamic>?,
  );

  Map<String, dynamic> toJson() => {
    'id': id,
    'type': type.name,
    'title': title,
    'description': description,
    'costs': costs,
    'effects': effects,
    'evolution_level': evolutionLevel,
    'fusion_compatibility': fusionCompatibility,
    'metadata': metadata,
  };
}

enum CardType {
  lifeDirection,
  aspiration,
  relationship,
  activity,
  routine,
  place,
  item,
}
```

**Game State Model** (`features/game/data/models/game_state_model.dart`):
```dart
/// Core game state tracking all gameplay data.
/// 
/// Represents the complete state of a player's current game,
/// including resources, relationships, time progression, and card deck.
class GameStateModel {
  final String playerId;
  final int currentWeek;
  final int currentDay;
  final TurnPhase currentTurn;
  final ResourcesModel resources;
  final Map<String, RelationshipModel> relationships;
  final List<String> deckCardIds;
  final List<String> handCardIds;
  final SeasonModel? activeSeason;
  final EmotionalStateModel emotionalState;

  const GameStateModel({
    required this.playerId,
    required this.currentWeek,
    required this.currentDay,
    required this.currentTurn,
    required this.resources,
    required this.relationships,
    required this.deckCardIds,
    required this.handCardIds,
    this.activeSeason,
    required this.emotionalState,
  });

  factory GameStateModel.initial(String playerId) => GameStateModel(
    playerId: playerId,
    currentWeek: 1,
    currentDay: 1,
    currentTurn: TurnPhase.morning,
    resources: ResourcesModel.initial(),
    relationships: {},
    deckCardIds: [],
    handCardIds: [],
    emotionalState: EmotionalStateModel.initial(),
  );
}

enum TurnPhase { morning, afternoon, evening }
```

**Relationship Model** (`features/relationships/data/models/relationship_model.dart`):
```dart
/// NPC relationship tracking.
/// 
/// Tracks relationship level (0-5), trust (0.0-1.0), and interaction history.
/// Level 0 = "Not Met" (never displayed as "Level 0").
class RelationshipModel {
  final String npcId;
  final int level; // 0-5 (0 = Not Met, internal only)
  final double trust; // 0.0-1.0
  final int interactionCount;
  final List<String> sharedMemoryIds;
  final DateTime? lastInteraction;

  const RelationshipModel({
    required this.npcId,
    required this.level,
    required this.trust,
    required this.interactionCount,
    this.sharedMemoryIds = const [],
    this.lastInteraction,
  });

  /// Display name for UI.
  /// Never shows "Level 0" - shows "Not Met" instead.
  String get displayLevel {
    if (level == 0) return 'Not Met';
    return 'Level $level';
  }

  /// Formatted display string: "Level 3 (Trust 0.62)"
  String get displayString => '$displayLevel (Trust ${trust.toStringAsFixed(2)})';
}
```

#### 1.3 Base Card JSON
Create `assets/data/base_cards.json` with ~50 starter cards:

```json
{
  "cards": [
    {
      "id": "act_coffee_chat_001",
      "type": "activity",
      "title": "Coffee Chat",
      "description": "Casual conversation over coffee",
      "costs": {"energy": 1.0, "time": 1.0, "money": 5.0},
      "effects": {"relationship_gain": 0.1},
      "evolution_level": 0,
      "fusion_compatibility": ["act_deep_talk_001", "place_cafe_001"],
      "metadata": {
        "category": "social",
        "intensity": "light"
      }
    },
    {
      "id": "act_deep_talk_001",
      "type": "activity",
      "title": "Deep Conversation",
      "description": "Meaningful heart-to-heart discussion",
      "costs": {"energy": 3.0, "time": 2.0},
      "effects": {"relationship_gain": 0.3, "trust_gain": 0.05},
      "evolution_level": 0,
      "fusion_compatibility": ["act_coffee_chat_001", "place_quiet_spot_001"],
      "metadata": {
        "category": "social",
        "intensity": "deep",
        "requires_relationship_level": 2
      }
    }
  ]
}
```

#### 1.4 Basic UI Framework
- Simple card hand display (static cards, no interaction yet)
- Resource bar (Energy, Time, Money display)
- Turn phase indicator
- Basic navigation

### Success Criteria
- ✅ Project compiles and runs on Android/iOS simulator
- ✅ Displays 5-10 cards in hand from JSON
- ✅ Shows mock resources (Energy: 10/10, Money: $100, etc.)
- ✅ Can advance turn phase (Morning → Afternoon → Evening → next day)
- ✅ Clean Architecture structure validated
- ✅ All files follow snake_case naming
- ✅ Code passes `flutter analyze` with no errors

### Key Files
- `lib/core/constants/game_constants.dart` - Canonical constants
- `lib/features/cards/data/models/card_model.dart` - Card data model
- `lib/features/game/data/models/game_state_model.dart` - Game state
- `assets/data/base_cards.json` - Card database

---

## Phase 2: Dart Frog Backend + Shared Packages (Weeks 5-8)

### Goal
Set up Dart Frog backend server with Firebase integration and shared game logic packages. Backend will handle validation and AI generation.

### Deliverables

#### 2.1 Dart Frog Project Setup

**Backend Structure**:
```bash
backend/
├── routes/
│   ├── index.dart              # GET / (health check)
│   ├── game/
│   │   ├── play_card.dart     # POST /game/play-card
│   │   ├── advance_turn.dart  # POST /game/advance-turn
│   │   └── state.dart         # GET /game/state
│   └── ai/
│       ├── generate_dialogue.dart  # POST /ai/generate-dialogue
│       └── evolve_card.dart        # POST /ai/evolve-card
│
├── middleware/
│   ├── auth_middleware.dart    # Firebase auth validation
│   └── logging_middleware.dart # Request logging
│
├── services/
│   ├── ai_service.dart         # OpenAI/Anthropic integration
│   ├── firestore_service.dart  # Firebase database
│   └── training_data_service.dart # Training data logging
│
├── main.dart
├── pubspec.yaml
└── Dockerfile
```

**Main Server** (`backend/main.dart`):
```dart
import 'dart:io';
import 'package:dart_frog/dart_frog.dart';
import 'package:game_logic/game_logic.dart';
import 'services/ai_service.dart';
import 'services/firestore_service.dart';
import 'services/training_data_service.dart';
import 'middleware/auth_middleware.dart';
import 'middleware/logging_middleware.dart';

Future<HttpServer> run(Handler handler, InternetAddress ip, int port) async {
  // Initialize services
  final aiService = OpenAIService(
    apiKey: Platform.environment['OPENAI_API_KEY']!,
  );
  
  final firestoreService = FirestoreService(
    projectId: Platform.environment['FIREBASE_PROJECT_ID']!,
  );
  
  final trainingDataService = TrainingDataService(firestoreService);
  
  // Inject services into request context
  final handler = Handler()
      .use(loggingMiddleware())
      .use(authMiddleware())
      .use(provider<AIService>((_) => aiService))
      .use(provider<FirestoreService>((_) => firestoreService))
      .use(provider<TrainingDataService>((_) => trainingDataService))
      .use(provider<GameLogic>((_) => GameLogic()));
  
  return serve(handler, ip, port);
}
```

#### 2.2 Shared Game Logic Package

**Package Structure**:
```bash
packages/game_logic/
├── lib/
│   ├── game_logic.dart         # Barrel export
│   ├── src/
│   │   ├── models/
│   │   │   ├── card.dart
│   │   │   ├── game_state.dart
│   │   │   └── relationship.dart
│   │   ├── calculators/
│   │   │   ├── relationship_calculator.dart
│   │   │   ├── resource_calculator.dart
│   │   │   └── progression_calculator.dart
│   │   └── validators/
│   │       ├── card_play_validator.dart
│   │       └── turn_validator.dart
│   └── game_logic.dart
├── test/
│   └── game_logic_test.dart
└── pubspec.yaml
```

**Relationship Calculator** (`packages/game_logic/lib/src/calculators/relationship_calculator.dart`):
```dart
/// Calculates relationship impacts using Master Truths v1.2 formulas.
/// 
/// Shared between Flutter client (for optimistic updates) and 
/// Dart Frog backend (for authoritative calculation).
class RelationshipCalculator {
  /// Calculates relationship impact from NPC response.
  /// 
  /// Formula: Base(OCEAN) × Urgency(1-5x) × Trust(0.5-2.0x) × Capacity
  RelationshipImpact calculate({
    required PersonalityProfile personality,
    required double emotionalCapacity,
    required double currentTrust,
    required UrgencyLevel urgency,
    required String playerAction,
  }) {
    // 1. PRIMARY FILTER: Personality baseline
    final baseResponse = _calculatePersonalityResponse(
      personality,
      playerAction,
    );
    
    // 2. MULTIPLIER: Urgency (1x-5x)
    final urgencyMultiplier = _getUrgencyMultiplier(urgency);
    
    // 3. MODIFIER: Trust (0.5x-2.0x)
    final trustModifier = _getTrustModifier(currentTrust);
    
    // 4. CONSTRAINT: Emotional capacity
    final capacityLimit = _applyCapacityConstraint(
      emotionalCapacity,
      baseResponse,
    );
    
    // Calculate final impact
    var relationshipDelta = baseResponse * urgencyMultiplier * trustModifier;
    relationshipDelta = relationshipDelta.clamp(
      -3.0,
      capacityLimit,
    );
    
    // Trust impact (smaller changes)
    var trustDelta = baseResponse * 0.1 * trustModifier;
    trustDelta = trustDelta.clamp(-0.5, 0.5);
    
    return RelationshipImpact(
      relationshipDelta: relationshipDelta,
      trustDelta: trustDelta,
      calculation: 'Base($baseResponse) × Urgency($urgencyMultiplier) '
          '× Trust($trustModifier) = $relationshipDelta',
    );
  }
  
  double _calculatePersonalityResponse(
    PersonalityProfile personality,
    String action,
  ) {
    // Simplified personality calculation
    // Full implementation would analyze action type
    return personality.agreeableness * 2.0 - 1.0; // -1.0 to 1.0
  }
  
  double _getUrgencyMultiplier(UrgencyLevel urgency) {
    switch (urgency) {
      case UrgencyLevel.routine:
        return 1.0;
      case UrgencyLevel.important:
        return 2.0;
      case UrgencyLevel.urgent:
        return 3.0;
      case UrgencyLevel.crisis:
        return 5.0;
    }
  }
  
  double _getTrustModifier(double trust) {
    if (trust < 0.3) return 0.5; // Low trust
    if (trust < 0.7) return 1.0; // Neutral trust
    return 2.0; // High trust
  }
  
  double _applyCapacityConstraint(double capacity, double baseResponse) {
    // Can provide up to (capacity + 2) / 10 level support
    return (capacity + 2.0) / 10.0 * 3.0; // Max 3.0 at capacity 10
  }
}
```

#### 2.3 Backend API Routes

**Play Card Route** (`backend/routes/game/play_card.dart`):
```dart
/// POST /game/play-card
/// 
/// Validates card play, applies costs/effects, triggers AI generation.
/// Returns updated game state and narrative.
Future<Response> onRequest(RequestContext context) async {
  try {
    // Parse request
    final json = await context.request.json() as Map<String, dynamic>;
    final userId = context.read<AuthenticatedUser>().uid;
    final cardId = json['card_id'] as String;
    final playContext = PlayContext.fromJson(json['context'] as Map<String, dynamic>);
    
    // Get services
    final gameLogic = context.read<GameLogic>();
    final firestoreService = context.read<FirestoreService>();
    final aiService = context.read<AIService>();
    final trainingDataService = context.read<TrainingDataService>();
    
    // Load current game state
    final gameState = await firestoreService.getGameState(userId);
    final card = await firestoreService.getCard(cardId);
    
    // Validate play using shared logic
    if (!gameLogic.canPlayCard(card, gameState)) {
      return Response.json(
        statusCode: HttpStatus.badRequest,
        body: {'error': 'Cannot play card: insufficient resources'},
      );
    }
    
    // Apply costs and effects (authoritative calculation)
    final updatedState = gameLogic.applyCardPlay(
      gameState,
      card,
      playContext,
    );
    
    // Generate AI narrative if NPC interaction
    String narrative;
    if (playContext.targetNpcId != null) {
      final npcResponse = await aiService.generateNPCResponse(
        NPCResponseRequest.fromGameState(updatedState, playContext),
      );
      
      narrative = npcResponse.dialogue;
      
      // Apply relationship impact (authoritative)
      final impact = gameLogic.relationshipCalculator.calculate(
        personality: npcResponse.personality,
        emotionalCapacity: npcResponse.emotionalCapacity,
        currentTrust: updatedState.relationships[playContext.targetNpcId]!.trust,
        urgency: playContext.urgency,
        playerAction: card.title,
      );
      
      updatedState = gameLogic.applyRelationshipImpact(
        updatedState,
        playContext.targetNpcId!,
        impact,
      );
      
      // Log training data
      await trainingDataService.logInteraction(
        userId: userId,
        type: 'npc_response',
        input: npcResponse.request.toJson(),
        output: npcResponse.toJson(),
      );
    } else {
      narrative = 'You ${card.title.toLowerCase()}. ${card.description}';
    }
    
    // Save updated state
    await firestoreService.saveGameState(userId, updatedState);
    
    return Response.json(body: {
      'success': true,
      'narrative': narrative,
      'game_state': updatedState.toJson(),
    });
    
  } catch (e, stack) {
    context.read<Logger>().severe('Play card failed', e, stack);
    return Response.json(
      statusCode: HttpStatus.internalServerError,
      body: {'error': 'Failed to play card'},
    );
  }
}
```

**AI Generation Route** (`backend/routes/ai/generate_dialogue.dart`):
```dart
/// POST /ai/generate-dialogue
/// 
/// Generates NPC dialogue using cloud AI (OpenAI/Anthropic).
/// Rate-limited by user tier.
Future<Response> onRequest(RequestContext context) async {
  try {
    final json = await context.request.json() as Map<String, dynamic>;
    final user = context.read<AuthenticatedUser>();
    final request = NPCResponseRequest.fromJson(json);
    
    // Check quota
    final quota = context.read<QuotaService>();
    if (!await quota.hasQuota(user.uid, user.tier)) {
      return Response.json(
        statusCode: HttpStatus.tooManyRequests,
        body: {'error': 'AI quota exceeded'},
      );
    }
    
    // Generate with AI
    final aiService = context.read<AIService>();
    final response = await aiService.generateNPCResponse(request);
    
    // Deduct quota
    await quota.deductQuota(user.uid);
    
    // Log training data
    await context.read<TrainingDataService>().logInteraction(
      userId: user.uid,
      type: 'npc_dialogue',
      input: request.toJson(),
      output: response.toJson(),
    );
    
    return Response.json(body: response.toJson());
    
  } catch (e) {
    return Response.json(
      statusCode: HttpStatus.internalServerError,
      body: {'error': 'AI generation failed: $e'},
    );
  }
}
```

#### 2.4 Firebase Integration

**Firestore Service** (`backend/services/firestore_service.dart`):
```dart
/// Firestore database service for game state persistence.
/// 
/// Handles all database operations with type-safe models.
class FirestoreService {
  final FirebaseFirestore _firestore;
  
  FirestoreService({required String projectId})
      : _firestore = FirebaseFirestore(projectId: projectId);
  
  /// Gets current game state for user.
  Future<GameState> getGameState(String userId) async {
    final doc = await _firestore
        .collection('game_states')
        .doc(userId)
        .get();
    
    if (!doc.exists) {
      return GameState.initial(userId);
    }
    
    return GameState.fromJson(doc.data()!);
  }
  
  /// Saves game state to Firestore.
  Future<void> saveGameState(String userId, GameState state) async {
    await _firestore
        .collection('game_states')
        .doc(userId)
        .set(state.toJson());
  }
  
  /// Gets card by ID.
  Future<Card> getCard(String cardId) async {
    final doc = await _firestore
        .collection('cards')
        .doc(cardId)
        .get();
    
    if (!doc.exists) {
      throw CardNotFoundException(cardId);
    }
    
    return Card.fromJson(doc.data()!);
  }
}
```

#### 2.5 Cloud Run Deployment

**Dockerfile** (`backend/Dockerfile`):
```dockerfile
FROM dart:stable AS build

WORKDIR /app

# Copy dependencies
COPY pubspec.* ./
RUN dart pub get

# Copy source
COPY . .

# Build production bundle
RUN dart pub global activate dart_frog_cli
RUN dart_frog build

# Runtime stage
FROM debian:bullseye-slim
RUN apt-get update && apt-get install -y ca-certificates

COPY --from=build /app/build /app
WORKDIR /app

EXPOSE 8080
CMD ["/app/bin/server"]
```

### Success Criteria
- ✅ Dart Frog backend compiles and runs locally
- ✅ Backend deployed to Cloud Run
- ✅ Shared `game_logic` package used by both frontend and backend
- ✅ Can call POST /game/play-card from Flutter app
- ✅ Backend validates card plays authoritatively
- ✅ Firebase integration working (Auth + Firestore)
- ✅ AI generation route functional with OpenAI
- ✅ Training data logged to Firestore

### Key Files
- `backend/main.dart` - Server entry point
- `backend/routes/game/play_card.dart` - Card play route
- `backend/routes/ai/generate_dialogue.dart` - AI generation
- `backend/services/firestore_service.dart` - Firebase integration
- `packages/game_logic/` - Shared logic package

---

## Phase 3: Core Game Loop (Weeks 9-12)

### Goal
Implement playable turn-based loop with card playing, resource management, and basic state persistence. Still no AI.

### Deliverables

#### 2.1 Card Play System

**Play Card Use Case** (`features/cards/domain/usecases/play_card_usecase.dart`):
```dart
/// Executes card play action with cost validation and effect application.
/// 
/// Validates resource costs, applies effects to game state,
/// and returns updated state with narrative outcome.
class PlayCardUsecase {
  final GameRepository _gameRepository;

  PlayCardUsecase(this._gameRepository);

  /// Plays a card in the current game context.
  /// 
  /// Throws [InsufficientResourcesException] if costs cannot be paid.
  /// Throws [InvalidCardPlayException] if card cannot be played.
  /// 
  /// Returns [CardPlayResult] with updated state and narrative.
  Future<CardPlayResult> execute(String cardId, PlayContext context) async {
    final gameState = await _gameRepository.getCurrentGameState();
    final card = await _gameRepository.getCard(cardId);

    // Validate can play
    if (!_canPlayCard(card, gameState)) {
      throw InvalidCardPlayException('Cannot play card: ${card.title}');
    }

    // Apply costs
    final updatedResources = _applyCosts(gameState.resources, card.costs);

    // Apply effects (no AI yet - simple deterministic effects)
    final updatedState = _applyEffects(
      gameState.copyWith(resources: updatedResources),
      card.effects,
      context,
    );

    // Generate simple narrative (template-based, no AI)
    final narrative = _generateNarrative(card, context);

    // Save state
    await _gameRepository.saveGameState(updatedState);

    AppLogger.info('Card played', data: {
      'card_id': cardId,
      'card_title': card.title,
      'turn': gameState.currentTurn.name,
    });

    return CardPlayResult(
      success: true,
      updatedState: updatedState,
      narrative: narrative,
    );
  }

  bool _canPlayCard(CardModel card, GameStateModel state) {
    // Check energy cost
    if (card.costs.containsKey('energy')) {
      if (state.resources.energy < card.costs['energy']!) {
        return false;
      }
    }

    // Check money cost
    if (card.costs.containsKey('money')) {
      if (state.resources.money < card.costs['money']!) {
        return false;
      }
    }

    // Check time cost
    if (card.costs.containsKey('time')) {
      if (state.resources.timeRemaining < card.costs['time']!) {
        return false;
      }
    }

    return true;
  }

  ResourcesModel _applyCosts(ResourcesModel resources, Map<String, double> costs) {
    return resources.copyWith(
      energy: resources.energy - (costs['energy'] ?? 0.0),
      money: resources.money - (costs['money'] ?? 0.0),
      timeRemaining: resources.timeRemaining - (costs['time'] ?? 0.0),
    );
  }

  GameStateModel _applyEffects(
    GameStateModel state,
    Map<String, double> effects,
    PlayContext context,
  ) {
    var updatedState = state;

    // Relationship gain
    if (effects.containsKey('relationship_gain') && context.targetNpcId != null) {
      final currentRel = state.relationships[context.targetNpcId];
      if (currentRel != null) {
        final updatedRel = _applyRelationshipGain(currentRel, effects['relationship_gain']!);
        final updatedRelationships = Map<String, RelationshipModel>.from(state.relationships);
        updatedRelationships[context.targetNpcId!] = updatedRel;
        updatedState = updatedState.copyWith(relationships: updatedRelationships);
      }
    }

    return updatedState;
  }

  String _generateNarrative(CardModel card, PlayContext context) {
    // Simple template-based narrative (no AI in Phase 2)
    if (context.targetNpcId != null) {
      return 'You ${card.title.toLowerCase()} with ${context.targetNpcName}. ${card.description}';
    }
    return 'You ${card.title.toLowerCase()}. ${card.description}';
  }
}
```

#### 2.2 Turn Management

**Turn Controller** (`features/game/presentation/controllers/turn_controller.dart`):
```dart
/// Manages turn-based game progression.
/// 
/// Handles turn phase advancement (Morning → Afternoon → Evening),
/// daily resource refresh, and turn-based event scheduling.
class TurnController extends StateNotifier<GameStateModel> {
  TurnController(this._gameRepository) : super(GameStateModel.initial('player_001'));

  final GameRepository _gameRepository;

  /// Advances to next turn phase.
  /// 
  /// Morning → Afternoon → Evening → Morning (next day).
  /// Refreshes resources at start of each day.
  Future<void> advanceTurn() async {
    var updatedState = state;

    switch (state.currentTurn) {
      case TurnPhase.morning:
        updatedState = state.copyWith(currentTurn: TurnPhase.afternoon);
        break;
      case TurnPhase.afternoon:
        updatedState = state.copyWith(currentTurn: TurnPhase.evening);
        break;
      case TurnPhase.evening:
        // Advance to next day
        updatedState = _advanceDay(state);
        break;
    }

    await _gameRepository.saveGameState(updatedState);
    state = updatedState;

    AppLogger.info('Turn advanced', data: {
      'week': updatedState.currentWeek,
      'day': updatedState.currentDay,
      'turn': updatedState.currentTurn.name,
    });
  }

  GameStateModel _advanceDay(GameStateModel currentState) {
    final newDay = currentState.currentDay + 1;
    final newWeek = newDay > 7 ? currentState.currentWeek + 1 : currentState.currentWeek;
    final adjustedDay = newDay > 7 ? 1 : newDay;

    return currentState.copyWith(
      currentDay: adjustedDay,
      currentWeek: newWeek,
      currentTurn: TurnPhase.morning,
      resources: _refreshDailyResources(currentState.resources),
    );
  }

  ResourcesModel _refreshDailyResources(ResourcesModel current) {
    return current.copyWith(
      energy: 10.0, // Full energy at start of day
      timeRemaining: 3.0, // 3 turns per day
    );
  }
}
```

#### 2.3 Local Storage with Hive

**Game Repository** (`features/game/data/repositories/game_repository_impl.dart`):
```dart
/// Local game state persistence using Hive.
/// 
/// Stores game state, card deck, and relationships locally.
/// No cloud sync in Phase 2.
class GameRepositoryImpl implements GameRepository {
  static const String GAME_STATE_BOX = 'game_state';
  static const String CARDS_BOX = 'cards';

  late Box<Map<dynamic, dynamic>> _gameStateBox;
  late Box<Map<dynamic, dynamic>> _cardsBox;

  /// Initializes Hive storage.
  /// 
  /// Must be called before any repository operations.
  Future<void> initialize() async {
    await Hive.initFlutter();
    _gameStateBox = await Hive.openBox(GAME_STATE_BOX);
    _cardsBox = await Hive.openBox(CARDS_BOX);

    AppLogger.info('Game repository initialized');
  }

  @override
  Future<GameStateModel> getCurrentGameState() async {
    final stateJson = _gameStateBox.get('current_game');
    if (stateJson == null) {
      return GameStateModel.initial('player_001');
    }
    return GameStateModel.fromJson(Map<String, dynamic>.from(stateJson));
  }

  @override
  Future<void> saveGameState(GameStateModel state) async {
    await _gameStateBox.put('current_game', state.toJson());
    AppLogger.info('Game state saved', data: {
      'week': state.currentWeek,
      'day': state.currentDay,
    });
  }

  @override
  Future<CardModel> getCard(String cardId) async {
    final cardJson = _cardsBox.get(cardId);
    if (cardJson == null) {
      throw CardNotFoundException('Card not found: $cardId');
    }
    return CardModel.fromJson(Map<String, dynamic>.from(cardJson));
  }
}
```

#### 2.4 Interactive UI

**Game Screen** (`features/game/presentation/screens/game_screen.dart`):
```dart
/// Main gameplay screen with card hand, resources, and turn controls.
/// 
/// Displays player's hand, current resources, and allows card playing.
class GameScreen extends ConsumerWidget {
  const GameScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final gameState = ref.watch(gameStateProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text('Week ${gameState.currentWeek} - Day ${gameState.currentDay}'),
        actions: [
          IconButton(
            icon: const Icon(Icons.save),
            onPressed: () => ref.read(gameStateProvider.notifier).saveGame(),
          ),
        ],
      ),
      body: Column(
        children: [
          // Resources bar
          ResourcesBar(resources: gameState.resources),

          // Turn phase indicator
          TurnPhaseIndicator(currentTurn: gameState.currentTurn),

          // Card hand
          Expanded(
            child: CardHandWidget(
              cardIds: gameState.handCardIds,
              onCardTapped: (cardId) => _playCard(ref, cardId),
            ),
          ),

          // Narrative display
          if (gameState.lastNarrative != null)
            NarrativePanel(narrative: gameState.lastNarrative!),

          // Turn controls
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: ElevatedButton(
              onPressed: () => ref.read(gameStateProvider.notifier).advanceTurn(),
              child: const Text('End Turn'),
            ),
          ),
        ],
      ),
    );
  }

  void _playCard(WidgetRef ref, String cardId) {
    ref.read(playCardUsecaseProvider).execute(
      cardId,
      PlayContext(targetNpcId: null), // No NPC targeting in Phase 2
    );
  }
}
```

### Success Criteria
- ✅ Can play cards from hand
- ✅ Resources deduct correctly when cards played
- ✅ Turn advances: Morning → Afternoon → Evening → next day
- ✅ Resources refresh each day
- ✅ Game state persists between app sessions
- ✅ Simple template-based narrative appears when card played
- ✅ Can play for 7 days (1 week) without crashes

### Key Files
- `features/cards/domain/usecases/play_card_usecase.dart`
- `features/game/presentation/controllers/turn_controller.dart`
- `features/game/data/repositories/game_repository_impl.dart`
- `features/game/presentation/screens/game_screen.dart`

---

## Phase 3: Cloud AI Integration (Weeks 9-12)

### Goal
Integrate cloud-based AI for card evolution, NPC responses, and narrative generation. Capture all interactions as training data.

### Deliverables

#### 3.1 Cloud AI Service

**AI Service Interface** (`shared/services/ai_service.dart`):
```dart
/// Cloud-based AI service for narrative generation and card evolution.
/// 
/// Uses OpenAI/Anthropic/Gemini API for flexible iteration.
/// All interactions logged for training data collection.
abstract class AIService {
  /// Generates NPC response to player action.
  /// 
  /// Returns AI-generated dialogue and relationship impact scores.
  /// Logs request/response for training data.
  Future<NPCResponseResult> generateNPCResponse(NPCResponseRequest request);

  /// Generates card evolution based on usage context.
  /// 
  /// Returns evolved card with updated description and effects.
  /// Logs evolution for training data.
  Future<CardEvolutionResult> evolveCard(CardEvolutionRequest request);

  /// Generates micro-narrative for card play.
  /// 
  /// Returns 2-3 sentence narrative describing action outcome.
  Future<MicroNarrativeResult> generateMicroNarrative(MicroNarrativeRequest request);
}

/// Cloud AI implementation using OpenAI API.
/// 
/// Configured via environment variables:
/// - OPENAI_API_KEY
/// - OPENAI_MODEL (default: gpt-4o-mini)
class OpenAIService implements AIService {
  final String _apiKey;
  final String _model;
  final TrainingDataLogger _trainingLogger;

  OpenAIService({
    required String apiKey,
    String model = 'gpt-4o-mini',
    required TrainingDataLogger trainingLogger,
  })  : _apiKey = apiKey,
        _model = model,
        _trainingLogger = trainingLogger;

  @override
  Future<NPCResponseResult> generateNPCResponse(NPCResponseRequest request) async {
    final stopwatch = Stopwatch()..start();

    try {
      final prompt = _buildNPCResponsePrompt(request);
      final response = await _callOpenAI(prompt);
      final parsed = _parseNPCResponse(response);

      stopwatch.stop();

      // Log for training data
      await _trainingLogger.logInteraction(TrainingDataEntry(
        timestamp: DateTime.now(),
        type: 'npc_response',
        input: request.toJson(),
        output: parsed.toJson(),
        metadata: {
          'model': _model,
          'latency_ms': stopwatch.elapsedMilliseconds,
        },
      ));

      AppLogger.ai('NPC response generated', metrics: {
        'npc_id': request.npcId,
        'latency_ms': stopwatch.elapsedMilliseconds,
      });

      return parsed;
    } catch (e, stack) {
      AppLogger.error('NPC response generation failed', e, stack);
      rethrow;
    }
  }

  String _buildNPCResponsePrompt(NPCResponseRequest request) {
    // Build prompt following canonical spec v1.2
    return '''
You are generating an NPC response in Unwritten, a narrative life simulation game.

NPC Profile:
- Name: ${request.npcName}
- Personality (OCEAN): O=${request.personality.openness}, C=${request.personality.conscientiousness}, E=${request.personality.extraversion}, A=${request.personality.agreeableness}, N=${request.personality.neuroticism}
- Current Emotional Capacity: ${request.emotionalCapacity}/10
- Relationship Level: ${request.relationshipLevel} (Trust: ${request.trust})

Situational Context:
- Urgency: ${request.urgency} (1x = routine, 5x = crisis)
- Player Action: ${request.playerAction}
- Recent History: ${request.recentHistory}

Response Framework (Master Truths v1.2):
1. PRIMARY FILTER: Personality (OCEAN) sets baseline response
2. MULTIPLIER: Situational urgency (${request.urgency}x) can override personality
3. MODIFIER: Relationship history (trust ${request.trust}) affects interpretation
4. CONSTRAINT: Emotional capacity (${request.emotionalCapacity}/10) limits response quality
   - Can provide up to (${request.emotionalCapacity} + 2)/10 level support
   - Must show authentic limitations if capacity is low

Generate:
1. Dialogue (2-3 sentences, authentic to capacity constraints)
2. Relationship impact (-3.0 to +3.0, calculated with formula from Master Truths)
3. Trust impact (-0.5 to +0.5)
4. Emotional authenticity score (0.0-1.0, must be ≥ 0.7)

Response JSON:
{
  "dialogue": "...",
  "relationship_impact": -1.3,
  "trust_impact": -0.2,
  "emotional_authenticity_score": 0.75,
  "calculation_notes": "base personality response × urgency multiplier × trust modifier"
}
''';
  }

  Future<String> _callOpenAI(String prompt) async {
    final response = await http.post(
      Uri.parse('https://api.openai.com/v1/chat/completions'),
      headers: {
        'Authorization': 'Bearer $_apiKey',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'model': _model,
        'messages': [
          {'role': 'system', 'content': 'You are a narrative generation system for Unwritten.'},
          {'role': 'user', 'content': prompt},
        ],
        'temperature': 0.8,
      }),
    );

    if (response.statusCode != 200) {
      throw AIServiceException('OpenAI API error: ${response.statusCode}');
    }

    final data = json.decode(response.body);
    return data['choices'][0]['message']['content'];
  }

  NPCResponseResult _parseNPCResponse(String response) {
    // Parse JSON response from AI
    final parsed = json.decode(response);
    return NPCResponseResult.fromJson(parsed);
  }
}
```

#### 3.2 Training Data Logger

**Training Data Logger** (`shared/services/training_data_logger.dart`):
```dart
/// Logs all AI interactions for training data collection.
/// 
/// Captures input prompts, AI outputs, player reactions,
/// and outcome quality scores for model training.
class TrainingDataLogger {
  final String _storageDir;
  final BatchWriter _batchWriter;

  TrainingDataLogger({
    required String storageDir,
  })  : _storageDir = storageDir,
        _batchWriter = BatchWriter(storageDir);

  /// Logs a single AI interaction.
  /// 
  /// Batches writes to avoid I/O bottlenecks.
  Future<void> logInteraction(TrainingDataEntry entry) async {
    await _batchWriter.write(entry);

    AppLogger.info('Training data logged', data: {
      'type': entry.type,
      'timestamp': entry.timestamp.toIso8601String(),
    });
  }

  /// Logs player feedback on AI generation quality.
  /// 
  /// Used to score training examples for quality filtering.
  Future<void> logPlayerFeedback(String interactionId, PlayerFeedback feedback) async {
    final entry = TrainingDataEntry(
      timestamp: DateTime.now(),
      type: 'player_feedback',
      input: {'interaction_id': interactionId},
      output: feedback.toJson(),
      metadata: {},
    );

    await _batchWriter.write(entry);
  }

  /// Exports all training data as JSONL for model fine-tuning.
  /// 
  /// Filters by quality scores and deduplicates.
  Future<File> exportTrainingData({
    DateTime? startDate,
    DateTime? endDate,
    double minQualityScore = 0.7,
  }) async {
    final entries = await _loadEntries(startDate, endDate);
    final filtered = entries.where((e) => e.qualityScore >= minQualityScore).toList();

    final outputFile = File('${_storageDir}/training_export_${DateTime.now().millisecondsSinceEpoch}.jsonl');
    final sink = outputFile.openWrite();

    for (final entry in filtered) {
      sink.writeln(json.encode(entry.toJson()));
    }

    await sink.close();

    AppLogger.info('Training data exported', data: {
      'total_entries': filtered.length,
      'output_file': outputFile.path,
    });

    return outputFile;
  }
}

class TrainingDataEntry {
  final DateTime timestamp;
  final String type; // 'npc_response', 'card_evolution', 'micro_narrative'
  final Map<String, dynamic> input;
  final Map<String, dynamic> output;
  final Map<String, dynamic> metadata;
  final double qualityScore; // 0.0-1.0, calculated from player engagement

  TrainingDataEntry({
    required this.timestamp,
    required this.type,
    required this.input,
    required this.output,
    required this.metadata,
    this.qualityScore = 0.5,
  });

  Map<String, dynamic> toJson() => {
    'timestamp': timestamp.toIso8601String(),
    'type': type,
    'input': input,
    'output': output,
    'metadata': metadata,
    'quality_score': qualityScore,
  };
}
```

#### 3.3 NPC System with AI

**NPC Response Request** (`features/relationships/domain/entities/npc_response_request.dart`):
```dart
/// Request data for AI-generated NPC response.
/// 
/// Contains all context needed for personality-driven response generation
/// following Master Truths v1.2 NPC Response Framework.
class NPCResponseRequest {
  final String npcId;
  final String npcName;
  final PersonalityProfile personality;
  final double emotionalCapacity; // 0.0-10.0
  final int relationshipLevel; // 0-5
  final double trust; // 0.0-1.0
  final UrgencyLevel urgency; // routine, important, urgent, crisis
  final String playerAction;
  final List<String> recentHistory;

  const NPCResponseRequest({
    required this.npcId,
    required this.npcName,
    required this.personality,
    required this.emotionalCapacity,
    required this.relationshipLevel,
    required this.trust,
    required this.urgency,
    required this.playerAction,
    this.recentHistory = const [],
  });

  Map<String, dynamic> toJson() => {
    'npc_id': npcId,
    'npc_name': npcName,
    'personality': personality.toJson(),
    'emotional_capacity': emotionalCapacity,
    'relationship_level': relationshipLevel,
    'trust': trust,
    'urgency': urgency.name,
    'player_action': playerAction,
    'recent_history': recentHistory,
  };
}

enum UrgencyLevel {
  routine, // 1x multiplier
  important, // 2x multiplier
  urgent, // 3x multiplier
  crisis, // 5x multiplier
}

class PersonalityProfile {
  final double openness; // 0.0-1.0
  final double conscientiousness; // 0.0-1.0
  final double extraversion; // 0.0-1.0
  final double agreeableness; // 0.0-1.0
  final double neuroticism; // 0.0-1.0

  const PersonalityProfile({
    required this.openness,
    required this.conscientiousness,
    required this.extraversion,
    required this.agreeableness,
    required this.neuroticism,
  });

  Map<String, dynamic> toJson() => {
    'openness': openness,
    'conscientiousness': conscientiousness,
    'extraversion': extraversion,
    'agreeableness': agreeableness,
    'neuroticism': neuroticism,
  };
}
```

#### 3.4 Card Evolution with AI

**Card Evolution Use Case** (`features/cards/domain/usecases/evolve_card_usecase.dart`):
```dart
/// Evolves cards based on usage context using AI generation.
/// 
/// Cards evolve after sufficient interactions, gaining personalized
/// descriptions and effects based on player's story.
class EvolveCardUsecase {
  final AIService _aiService;
  final CardRepository _cardRepository;

  EvolveCardUsecase(this._aiService, this._cardRepository);

  /// Attempts to evolve a card.
  /// 
  /// Returns evolved card if requirements met, null otherwise.
  Future<CardModel?> execute(String cardId) async {
    final card = await _cardRepository.getCard(cardId);
    final usageContext = await _cardRepository.getCardUsageContext(cardId);

    // Check evolution requirements
    if (!_canEvolve(card, usageContext)) {
      return null;
    }

    // Build AI request
    final request = CardEvolutionRequest(
      cardId: cardId,
      currentTitle: card.title,
      currentDescription: card.description,
      usageCount: usageContext.usageCount,
      associatedNPCs: usageContext.npcIds,
      emotionalContext: usageContext.dominantEmotions,
      playerChoices: usageContext.significantChoices,
    );

    // Generate evolution via AI
    final result = await _aiService.evolveCard(request);

    // Create evolved card
    final evolved = card.copyWith(
      title: result.evolvedTitle,
      description: result.evolvedDescription,
      effects: _mergeEffects(card.effects, result.newEffects),
      evolutionLevel: card.evolutionLevel + 1,
      metadata: {
        ...?card.metadata,
        'evolution_timestamp': DateTime.now().toIso8601String(),
        'evolution_context': result.evolutionNarrative,
      },
    );

    await _cardRepository.saveCard(evolved);

    AppLogger.info('Card evolved', data: {
      'card_id': cardId,
      'evolution_level': evolved.evolutionLevel,
    });

    return evolved;
  }

  bool _canEvolve(CardModel card, CardUsageContext context) {
    // Require at least 5 uses
    if (context.usageCount < 5) return false;

    // Require at least 2 associated NPCs
    if (context.npcIds.length < 2) return false;

    // Require significant player engagement
    if (context.significantChoices.isEmpty) return false;

    return true;
  }
}
```

### Success Criteria
- ✅ NPC dialogue generated via cloud AI
- ✅ NPC responses follow OCEAN personality + capacity constraints
- ✅ Card evolution works after 5+ uses
- ✅ All AI interactions logged to training data files
- ✅ Training data exportable as JSONL
- ✅ AI latency < 2 seconds (acceptable for MVP)
- ✅ Training data includes input context, AI output, and quality scores

### Key Files
- `shared/services/ai_service.dart` - Cloud AI interface
- `shared/services/training_data_logger.dart` - Training data capture
- `features/relationships/domain/usecases/generate_npc_response_usecase.dart`
- `features/cards/domain/usecases/evolve_card_usecase.dart`

---

## Phase 4: Season Structure & Progression (Weeks 13-16)

### Goal
Implement full season loop with aspiration tracking, relationship progression, and season completion.

### Deliverables

#### 4.1 Season Management

**Season Controller** (`features/game/presentation/controllers/season_controller.dart`):
```dart
/// Manages season lifecycle and progression tracking.
/// 
/// Seasons are 12/24/36 weeks with 3-act structure.
/// Tracks aspiration progress and triggers decisive moments.
class SeasonController extends StateNotifier<SeasonState> {
  SeasonController(this._gameRepository) : super(SeasonState.initial());

  final GameRepository _gameRepository;

  /// Starts a new season with player-selected aspiration and length.
  /// 
  /// Generates season plan with act structure and scheduled events.
  Future<void> startSeason({
    required Aspiration aspiration,
    required SeasonLength length,
  }) async {
    // Generate season plan
    final plan = await _generateSeasonPlan(aspiration, length);

    state = SeasonState(
      aspiration: aspiration,
      length: length,
      currentWeek: 1,
      actStructure: plan.actStructure,
      scheduledEvents: plan.events,
      decisiveMoments: plan.decisiveMoments,
      aspirationProgress: 0.0,
    );

    await _gameRepository.saveSeason(state);

    AppLogger.info('Season started', data: {
      'aspiration': aspiration.title,
      'length_weeks': length.weeks,
    });
  }

  /// Advances season by one week.
  /// 
  /// Checks for scheduled events, updates progression,
  /// and triggers decisive moments at key thresholds.
  Future<void> advanceWeek() async {
    final newWeek = state.currentWeek + 1;

    // Check for scheduled events
    final weekEvents = _getEventsForWeek(newWeek);

    // Update aspiration progress
    final progress = await _calculateProgress();

    // Check for decisive moments
    final decisiveMoment = _checkForDecisiveMoment(newWeek, progress);

    // Check for season completion
    if (_shouldEndSeason(newWeek, progress)) {
      await _triggerSeasonEnd();
      return;
    }

    state = state.copyWith(
      currentWeek: newWeek,
      weekEvents: weekEvents,
      aspirationProgress: progress,
      currentDecisiveMoment: decisiveMoment,
    );

    await _gameRepository.saveSeason(state);
  }

  Future<SeasonPlan> _generateSeasonPlan(Aspiration aspiration, SeasonLength length) async {
    // 3-act structure based on season length
    final act1End = (length.weeks * 0.25).round(); // Setup
    final act2End = (length.weeks * 0.75).round(); // Complications
    final act3End = length.weeks; // Resolution

    return SeasonPlan(
      actStructure: ActStructure(
        act1End: act1End,
        act2End: act2End,
        act3End: act3End,
      ),
      events: _scheduleSeasonEvents(aspiration, length),
      decisiveMoments: _scheduleDecisiveMoments(aspiration, length),
    );
  }

  bool _shouldEndSeason(int week, double progress) {
    // End season if:
    // 1. Reached max weeks
    if (week >= state.length.weeks) return true;

    // 2. Aspiration fully achieved early
    if (progress >= 1.0) return true;

    // 3. Critical failure condition met
    // TODO: Implement failure conditions

    return false;
  }
}

enum SeasonLength {
  standard(12),
  extended(24),
  epic(36);

  final int weeks;
  const SeasonLength(this.weeks);
}
```

#### 4.2 Aspiration Tracking

**Aspiration Progress Calculator** (`features/game/domain/services/aspiration_progress_calculator.dart`):
```dart
/// Calculates aspiration progress based on milestones and player actions.
/// 
/// Progress is 0.0-1.0 scale, calculated from weighted milestones.
class AspirationProgressCalculator {
  /// Calculates current progress toward aspiration goal.
  /// 
  /// Weighted by milestone importance and completion status.
  double calculate(Aspiration aspiration, GameStateModel gameState) {
    var totalProgress = 0.0;
    var totalWeight = 0.0;

    for (final milestone in aspiration.milestones) {
      final completed = _isMilestoneCompleted(milestone, gameState);
      if (completed) {
        totalProgress += milestone.weight;
      }
      totalWeight += milestone.weight;
    }

    return totalWeight > 0 ? totalProgress / totalWeight : 0.0;
  }

  bool _isMilestoneCompleted(Milestone milestone, GameStateModel gameState) {
    switch (milestone.type) {
      case MilestoneType.relationshipLevel:
        final rel = gameState.relationships[milestone.targetNpcId];
        return rel != null && rel.level >= milestone.targetValue;

      case MilestoneType.skillLevel:
        // TODO: Implement skill tracking
        return false;

      case MilestoneType.eventCompletion:
        // Check if specific event completed
        return gameState.completedEventIds.contains(milestone.eventId);

      case MilestoneType.resourceThreshold:
        // Check resource threshold met
        switch (milestone.resourceType) {
          case 'money':
            return gameState.resources.money >= milestone.targetValue;
          default:
            return false;
        }
    }
  }
}
```

#### 4.3 Relationship Progression

**Relationship Level Calculator** (`features/relationships/domain/services/relationship_level_calculator.dart`):
```dart
/// Calculates relationship level transitions.
/// 
/// Level up requires BOTH interaction count AND trust threshold.
/// Follows Master Truths v1.2 canonical scale (0-5).
class RelationshipLevelCalculator {
  /// Checks if relationship can level up.
  /// 
  /// Returns new level if requirements met, null otherwise.
  int? calculateLevelUp(RelationshipModel current) {
    if (current.level >= 5) return null; // Max level

    final requirements = _getLevelUpRequirements(current.level);

    // Both conditions required
    if (current.interactionCount >= requirements.interactionThreshold &&
        current.trust >= requirements.trustThreshold) {
      return current.level + 1;
    }

    return null;
  }

  LevelUpRequirements _getLevelUpRequirements(int currentLevel) {
    // Master Truths v1.2 canonical requirements
    switch (currentLevel) {
      case 0: // Not Met → Stranger
        return LevelUpRequirements(interactionThreshold: 1, trustThreshold: 0.0);
      case 1: // Stranger → Acquaintance
        return LevelUpRequirements(interactionThreshold: 6, trustThreshold: 0.2);
      case 2: // Acquaintance → Friend
        return LevelUpRequirements(interactionThreshold: 16, trustThreshold: 0.4);
      case 3: // Friend → Close Friend
        return LevelUpRequirements(interactionThreshold: 31, trustThreshold: 0.6);
      case 4: // Close Friend → Soulmate
        return LevelUpRequirements(interactionThreshold: 76, trustThreshold: 0.8);
      default:
        throw Exception('Invalid relationship level: $currentLevel');
    }
  }
}

class LevelUpRequirements {
  final int interactionThreshold;
  final double trustThreshold;

  LevelUpRequirements({
    required this.interactionThreshold,
    required this.trustThreshold,
  });
}
```

#### 4.4 Season Archive System

**Season Archive** (`features/game/domain/entities/season_archive.dart`):
```dart
/// Archived season data for persistence and novel generation.
/// 
/// Captures complete season story: relationships, events, decisive moments.
class SeasonArchive {
  final String archiveId;
  final String playerId;
  final Aspiration aspiration;
  final SeasonLength length;
  final int weeksCompleted;
  final double aspirationProgress;
  final Map<String, RelationshipModel> finalRelationships;
  final List<GameEvent> significantEvents;
  final List<DecisiveMoment> decisiveMoments;
  final DateTime startDate;
  final DateTime endDate;
  final SeasonOutcome outcome;

  const SeasonArchive({
    required this.archiveId,
    required this.playerId,
    required this.aspiration,
    required this.length,
    required this.weeksCompleted,
    required this.aspirationProgress,
    required this.finalRelationships,
    required this.significantEvents,
    required this.decisiveMoments,
    required this.startDate,
    required this.endDate,
    required this.outcome,
  });

  /// Generates summary for UI display.
  String get summary {
    final npcCount = finalRelationships.length;
    final eventCount = significantEvents.length;
    return '${aspiration.title} - ${length.weeks} weeks - $npcCount relationships - $eventCount key moments';
  }
}

enum SeasonOutcome {
  aspirationAchieved,
  partialSuccess,
  bittersweet,
  failure,
  earlyCompletion,
}
```

### Success Criteria
- ✅ Can start season with aspiration selection
- ✅ Season progresses week-by-week
- ✅ Aspiration progress calculated from milestones
- ✅ Relationships level up when thresholds met
- ✅ Season completes after 12/24/36 weeks or early completion
- ✅ Season archived with all key data
- ✅ Can start new season after previous ends
- ✅ Can view season archive list

### Key Files
- `features/game/presentation/controllers/season_controller.dart`
- `features/game/domain/services/aspiration_progress_calculator.dart`
- `features/relationships/domain/services/relationship_level_calculator.dart`
- `features/game/domain/entities/season_archive.dart`

---

## Phase 5: Polish & Beta Prep (Weeks 17-20)

### Goal
Polish UI, add onboarding, implement analytics, and prepare for beta testing.

### Deliverables

#### 5.1 Onboarding Flow
- Character creation screen
- Aspiration selection tutorial
- Card system tutorial
- First turn guided walkthrough

#### 5.2 UI/UX Polish
- Card animation when played
- Narrative text formatting improvements
- Relationship level-up celebrations
- Season completion screen with summary

#### 5.3 Analytics & Monitoring

**Analytics Service** (`shared/services/analytics_service.dart`):
```dart
/// Tracks player engagement and gameplay metrics.
/// 
/// Used to measure retention, feature usage, and quality validation.
class AnalyticsService {
  /// Tracks card play event.
  void trackCardPlayed(String cardId, CardType type) {
    _track('card_played', {
      'card_id': cardId,
      'card_type': type.name,
    });
  }

  /// Tracks relationship level up.
  void trackRelationshipLevelUp(String npcId, int newLevel) {
    _track('relationship_level_up', {
      'npc_id': npcId,
      'new_level': newLevel,
    });
  }

  /// Tracks season completion.
  void trackSeasonCompleted(SeasonOutcome outcome, int weeks, double progress) {
    _track('season_completed', {
      'outcome': outcome.name,
      'weeks': weeks,
      'progress': progress,
    });
  }

  /// Tracks AI quality scores.
  void trackAIQuality(String type, double score) {
    _track('ai_quality', {
      'type': type,
      'score': score,
    });
  }
}
```

#### 5.4 Error Handling & Recovery
- Graceful degradation when AI API unavailable
- Auto-save every 5 minutes
- Crash recovery from last save
- Network error UI feedback

#### 5.5 Beta Testing Preparation
- TestFlight/Play Store beta builds
- Feedback collection system
- Bug reporting tool
- Performance monitoring

### Success Criteria
- ✅ New players can complete onboarding in < 5 minutes
- ✅ UI animations smooth (60 FPS target)
- ✅ Analytics tracking all key events
- ✅ App recovers gracefully from crashes
- ✅ Beta builds deployable to testers
- ✅ Training data export working for fine-tuning

---

## Post-MVP Roadmap (Weeks 21+)

### Phase 6: Local AI Optimization
- TensorFlow Lite model integration
- On-device inference for simple interactions
- Battery-aware AI switching
- Model quantization (INT8/INT4)

### Phase 7: Advanced Features
- Card fusion system
- Multi-season continuity
- Lifetime archives
- Novel generation pipeline

### Phase 8: Visual Polish
- Custom card illustrations
- Art style packs
- Animated character portraits
- Visual effects for card plays

### Phase 9: Cloud Infrastructure
- Cloud save/sync
- Multiplayer features (future)
- Community card sharing
- Cross-platform progression

---

## Technical Stack Summary

| Component | Technology | Phase |
|-----------|-----------|-------|
| Framework | Flutter 3.x | Phase 1 |
| State Management | Riverpod 2.5+ | Phase 1 |
| Local Storage | Hive | Phase 2 |
| Cloud AI | OpenAI/Anthropic API | Phase 3 |
| Analytics | Firebase Analytics | Phase 5 |
| Crash Reporting | Sentry | Phase 5 |
| Local AI | TensorFlow Lite | Phase 6+ |
| Backend | Supabase/Firebase | Phase 9+ |

---

## Training Data Collection Strategy

### Data Points to Capture

**Every Card Play**:
- Card ID and type
- Game context (turn, week, season)
- Player resources before/after
- Target NPC (if applicable)
- Generated narrative
- Player engagement time (how long they read narrative)

**Every NPC Interaction**:
- NPC personality profile (OCEAN)
- Emotional capacity
- Relationship level and trust
- Player action/dialogue choice
- AI-generated response
- Relationship impact scores
- Player satisfaction signal (did they continue interaction?)

**Every Card Evolution**:
- Original card state
- Usage context (interactions, NPCs, emotions)
- AI-generated evolution
- Player usage of evolved card (validation)

**Season Completions**:
- Full season archive
- Aspiration progress
- Relationship final states
- Decisive moments chosen
- Outcome classification
- Player retention signal (did they start another season?)

### Export Format

Training data exported as JSONL with schema:

```json
{
  "timestamp": "2025-10-14T10:30:00Z",
  "type": "npc_response",
  "input": {
    "npc_id": "npc_sarah_001",
    "personality": {"openness": 0.8, "conscientiousness": 0.6, ...},
    "emotional_capacity": 4.5,
    "relationship_level": 3,
    "trust": 0.62,
    "urgency": "urgent",
    "player_action": "Declined to help with moving",
    "recent_history": [...]
  },
  "output": {
    "dialogue": "I... I really needed you there. I know you're busy, but this was important to me.",
    "relationship_impact": -1.8,
    "trust_impact": -0.3,
    "emotional_authenticity_score": 0.82
  },
  "player_feedback": {
    "read_time_seconds": 12,
    "continued_interaction": false,
    "session_length_after": 45
  },
  "quality_score": 0.85
}
```

---

## Performance Targets (MVP)

| Metric | Target | Measurement |
|--------|--------|-------------|
| App Launch Time | < 3 seconds | Cold start to playable |
| Turn Load Time | < 1 second | Advance turn to new state |
| Card Play Response | < 2 seconds | Play card to narrative display |
| AI Latency | < 3 seconds | Cloud API call round-trip |
| Memory Usage | < 200 MB | Average gameplay session |
| Battery Drain | < 5% | Per 30-minute session |
| Crash Rate | < 1% | Sessions with crash |

**Note**: These are MVP targets. Phase 6+ local AI optimization will improve latency and battery performance.

---

## Risk Mitigation

### Technical Risks

**Cloud API Dependency**
- **Risk**: OpenAI/API outages break gameplay
- **Mitigation**: Fallback to template-based responses; cache common responses
- **Timeline**: Phase 3

**Training Data Quality**
- **Risk**: Low-quality interactions poison training data
- **Mitigation**: Quality scoring system; manual review of exports
- **Timeline**: Phase 3-4

**State Management Complexity**
- **Risk**: Game state becomes inconsistent
- **Mitigation**: Comprehensive unit tests; immutable state patterns
- **Timeline**: Phase 1-2

### Product Risks

**Player Retention**
- **Risk**: Players churn before completing season
- **Mitigation**: Weekly engagement hooks; analytics tracking
- **Timeline**: Phase 4-5

**AI Response Quality**
- **Risk**: AI generates inappropriate or inconsistent content
- **Mitigation**: Content filtering; validation layers; quality thresholds
- **Timeline**: Phase 3

**Scope Creep**
- **Risk**: Feature bloat delays MVP
- **Mitigation**: Strict phase gate criteria; defer advanced features
- **Timeline**: All phases

---

## Success Metrics (MVP)

### Technical Metrics
- ✅ 95% uptime during beta
- ✅ < 2 second average AI latency
- ✅ 10,000+ training data entries collected
- ✅ All core features implemented

### Product Metrics
- ✅ 100 beta testers
- ✅ 50% complete at least 1 season
- ✅ Average session length > 15 minutes
- ✅ 70% 7-day retention

### Quality Metrics
- ✅ 80% AI responses score ≥ 0.7 authenticity
- ✅ < 5% inappropriate content flags
- ✅ 90% of training data exports usable

---

## Compliance Checklist

- [x] Uses canonical vocab & scales (Levels 0–5; Trust 0.0–1.0; Capacity 0.0-10.0)
- [x] Season = 12/24/36w (player choice at season start); 3 turns/day
- [x] Relationship Level 0 = "Not Met" (never displayed as "Level 0")
- [x] Level-up requires BOTH interaction count AND trust threshold
- [x] Currencies limited to Time/Energy/Money/Social Capital
- [x] Decisive decisions pause time; copy avoids FOMO framing
- [x] NPC Response Framework applied: OCEAN primary filter → Situational multiplier (1x-5x) → Relationship/capacity modifiers
- [x] Emotional capacity constraints respected (0-10 scale; support rule: capacity + 2)
- [x] This doc cites **Truths v1.2** at the top

---

**Document Version**: 1.0  
**Last Updated**: October 14, 2025  
**Status**: Approved for implementation  
**Target**: Playable MVP in 16 weeks, Beta-ready in 20 weeks

