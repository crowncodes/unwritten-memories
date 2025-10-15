# I/O FLIP Architecture Analysis & Unwritten Application

> **Source**: Google I/O 2023 FLIP game by Flutter team & Very Good Ventures  
> **Purpose**: Comprehensive analysis of I/O FLIP architecture patterns for Unwritten implementation  
> **Canonical Reference**: Master Truths v1.2  
> **Last Updated**: October 14, 2025

---

## Executive Summary

I/O FLIP demonstrates production-ready patterns for Flutter game development with:
- **Full-stack Dart** (Flutter + Dart Frog backend)
- **Firebase ecosystem** (Firestore, Auth, Storage, Hosting)
- **Server-authoritative model** (prevents cheating)
- **Shared logic packages** (code reuse between client/server)
- **Real-time multiplayer** (WebSocket connections)
- **Cloud-native scaling** (Google Cloud Run)

**Key Insight for Unwritten**: We can adopt I/O FLIP's architecture while adapting it for single-player narrative gameplay with AI generation instead of multiplayer card battles.

---

## Table of Contents

1. [I/O FLIP Architecture Overview](#io-flip-architecture-overview)
2. [Frontend Layer (Flutter + Flame)](#frontend-layer)
3. [Backend Layer (Dart Frog)](#backend-layer)
4. [Data Layer (Firebase)](#data-layer)
5. [Shared Packages Architecture](#shared-packages)
6. [State Management (BLoC Pattern)](#state-management)
7. [Real-Time Communication](#real-time-communication)
8. [Deployment & Infrastructure](#deployment-infrastructure)
9. [Adapting I/O FLIP for Unwritten](#adapting-for-unwritten)
10. [Implementation Roadmap](#implementation-roadmap)

---

## I/O FLIP Architecture Overview

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     FLUTTER WEB CLIENT                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │  Flame Game  │  │   BLoC       │  │  Custom Shaders    │    │
│  │   Engine     │  │   State      │  │  (GLSL for cards)  │    │
│  └──────┬───────┘  └──────┬───────┘  └─────────┬──────────┘    │
│         │                  │                     │               │
│         └──────────────────┴─────────────────────┘               │
│                            │                                     │
│  ┌─────────────────────────▼──────────────────────────────┐    │
│  │         go_router Navigation & Routing                  │    │
│  └─────────────────────────┬──────────────────────────────┘    │
│                            │                                     │
│  ┌─────────────────────────▼──────────────────────────────┐    │
│  │         Firebase SDK (Auth, Firestore, Storage)         │    │
│  └─────────────────────────┬──────────────────────────────┘    │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                             │ HTTP/REST + WebSocket
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                    DART FROG BACKEND                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │    Routes    │  │  Middleware  │  │  WebSocket Handler   │  │
│  │  (HTTP API)  │  │  (Auth, Log) │  │  (Real-time match)   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                  │                      │               │
│         └──────────────────┴──────────────────────┘               │
│                            │                                      │
│  ┌─────────────────────────▼──────────────────────────────────┐ │
│  │         Shared Game Logic Package                           │ │
│  │  ┌───────────────┐  ┌───────────────┐  ┌────────────────┐ │ │
│  │  │ Match Solver  │  │ Card Models   │  │  Game Rules    │ │ │
│  │  └───────────────┘  └───────────────┘  └────────────────┘ │ │
│  └─────────────────────────┬──────────────────────────────────┘ │
│                            │                                      │
│  ┌─────────────────────────▼──────────────────────────────────┐ │
│  │         Firebase Admin SDK                                   │ │
│  └─────────────────────────┬──────────────────────────────────┘ │
│                            │                                      │
└────────────────────────────┼──────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                    FIREBASE SERVICES                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Firestore   │  │  Firebase    │  │  Cloud Storage       │  │
│  │  (Database)  │  │  Auth        │  │  (Assets/Images)     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Firebase    │  │  App Check   │  │  Firebase Hosting    │  │
│  │  Security    │  │  (Anti-bot)  │  │  (Static assets)     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                   │
└────────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                    INFRASTRUCTURE                                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Cloud Run   │  │  Load        │  │  Cloud CDN           │  │
│  │  (Backend)   │  │  Balancing   │  │  (Global delivery)   │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                   │
└────────────────────────────────────────────────────────────────────┘
```

### Technology Stack Breakdown

```dart
const IO_FLIP_TECH_STACK = {
  // Frontend
  frontend: {
    framework: 'Flutter 3.x (Web-first, responsive)',
    gameEngine: 'Flame 1.x (for game loop, sprites, animations)',
    stateManagement: 'BLoC pattern (flutter_bloc)',
    navigation: 'go_router (declarative routing)',
    rendering: {
      ui: 'Flutter Material Design 3',
      gameGraphics: 'Flame components',
      specialEffects: 'Custom GLSL shaders (foil cards)'
    },
    audio: 'Flame audio system'
  },
  
  // Backend
  backend: {
    framework: 'Dart Frog (lightweight Dart server)',
    routing: 'File-based routes (/routes directory)',
    middleware: 'Custom middleware chain',
    realTime: 'WebSocket support (built-in)',
    deployment: 'Google Cloud Run (containerized)'
  },
  
  // Shared Code
  sharedPackages: {
    matchSolver: 'Game logic (card battles)',
    gameModels: 'Data models (cards, players, matches)',
    gameConfig: 'Constants and configuration'
  },
  
  // Data Layer
  dataLayer: {
    database: 'Cloud Firestore (NoSQL, real-time)',
    auth: 'Firebase Authentication (anonymous + email)',
    storage: 'Cloud Storage (card images)',
    security: 'Firestore Security Rules + App Check'
  },
  
  // Infrastructure
  infrastructure: {
    hosting: 'Firebase Hosting (static Flutter web)',
    backend: 'Google Cloud Run (auto-scaling Dart Frog)',
    cdn: 'Firebase CDN (global asset delivery)',
    monitoring: 'Firebase Analytics + Performance Monitoring'
  }
};
```

---

## Frontend Layer

### Flutter + Flame Architecture

```
lib/
├── main_development.dart       # Dev entry point
├── main_staging.dart           # Staging entry point
├── main_production.dart        # Production entry point
│
├── app/                        # Root app setup
│   ├── app.dart               # MaterialApp configuration
│   └── view/
│       └── app.dart           # Root widget
│
├── game/                       # Flame game implementation
│   ├── game.dart              # Main game class
│   ├── components/            # Flame game components
│   │   ├── card_component.dart
│   │   ├── player_component.dart
│   │   └── match_area_component.dart
│   └── views/
│       └── game_view.dart     # Flutter wrapper for Flame
│
├── match/                      # Match/gameplay feature
│   ├── match.dart             # Feature barrel export
│   ├── bloc/                  # BLoC state management
│   │   ├── match_bloc.dart
│   │   ├── match_event.dart
│   │   └── match_state.dart
│   ├── models/                # Data models
│   │   └── match_model.dart
│   ├── widgets/               # Reusable widgets
│   │   ├── card_widget.dart
│   │   └── player_hand_widget.dart
│   └── view/                  # Screens
│       └── match_screen.dart
│
├── leaderboard/               # Leaderboard feature
│   ├── leaderboard.dart
│   ├── bloc/
│   ├── models/
│   └── view/
│
├── audio/                     # Audio system
│   ├── audio_controller.dart
│   └── sounds.dart
│
├── l10n/                      # Internationalization
│   ├── arb/
│   │   ├── app_en.arb
│   │   └── app_es.arb
│   └── l10n.dart
│
├── gen/                       # Generated assets
│   └── assets.gen.dart
│
└── share/                     # Shared utilities
    ├── extensions/
    ├── theme/
    └── widgets/
```

### Flame Game Integration

> **📖 Detailed Guide**: See `CARD-DRAG-PHYSICS-GUIDE.md` for comprehensive documentation of card drag animations, momentum physics, and implementation options.

```dart
/// Main game class using Flame engine.
/// 
/// Integrates with Flutter via GameWidget wrapper.
/// Handles game loop, rendering, and component management.
class IoFlipGame extends FlameGame {
  IoFlipGame({
    required this.matchBloc,
    required this.audioController,
  });

  final MatchBloc matchBloc;
  final AudioController audioController;

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    
    // Initialize game components
    await _loadAssets();
    await _setupComponents();
    await _setupListeners();
  }

  Future<void> _loadAssets() async {
    // Load sprites, images, audio
    await images.loadAll([
      'card_back.png',
      'card_frame.png',
      'player_avatar.png',
    ]);
  }

  Future<void> _setupComponents() async {
    // Add game components to world
    await add(MatchAreaComponent());
    await add(PlayerHandComponent(position: Vector2(100, 500)));
    await add(OpponentHandComponent(position: Vector2(100, 50)));
  }

  void _setupListeners() {
    // Listen to BLoC state changes
    matchBloc.stream.listen((state) {
      if (state is MatchInProgress) {
        _updateGameState(state);
      } else if (state is MatchComplete) {
        _showMatchResult(state);
      }
    });
  }

  void _updateGameState(MatchInProgress state) {
    // Update game components based on state
    final matchArea = children.query<MatchAreaComponent>().first;
    matchArea.updateCards(state.playedCards);
  }
}
```

### Flutter Wrapper for Flame Game

```dart
/// Game screen that wraps Flame game in Flutter widget tree.
/// 
/// Provides BLoC integration and lifecycle management.
class GameScreen extends StatelessWidget {
  const GameScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => MatchBloc(
        matchRepository: context.read<MatchRepository>(),
        audioController: context.read<AudioController>(),
      )..add(const MatchStarted()),
      child: const GameView(),
    );
  }
}

class GameView extends StatelessWidget {
  const GameView({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<MatchBloc, MatchState>(
      listener: (context, state) {
        if (state is MatchError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message)),
          );
        }
      },
      builder: (context, state) {
        return Scaffold(
          body: Stack(
            children: [
              // Flame game widget
              GameWidget<IoFlipGame>(
                game: IoFlipGame(
                  matchBloc: context.read<MatchBloc>(),
                  audioController: context.read<AudioController>(),
                ),
              ),
              
              // Flutter UI overlays
              Positioned(
                top: 16,
                left: 16,
                right: 16,
                child: MatchStatusBar(state: state),
              ),
              
              if (state is MatchComplete)
                Positioned.fill(
                  child: MatchResultOverlay(result: state.result),
                ),
            ],
          ),
        );
      },
    );
  }
}
```

### Custom GLSL Shaders for Card Effects

```dart
/// Card component with holographic foil shader effect.
/// 
/// Uses Fragment shaders for GPU-accelerated visual effects.
class CardComponent extends PositionComponent with TapCallbacks {
  CardComponent({
    required this.card,
    required this.isHolographic,
  });

  final CardModel card;
  final bool isHolographic;
  
  late final FragmentProgram _foilShader;
  late final FragmentShader _shader;

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    
    if (isHolographic) {
      // Load custom GLSL shader
      _foilShader = await FragmentProgram.fromAsset(
        'shaders/holographic_foil.frag',
      );
      _shader = _foilShader.fragmentShader();
    }
    
    // Set component size
    size = Vector2(120, 180);
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    
    if (isHolographic) {
      // Apply shader effect
      _shader.setFloat(0, size.x); // width
      _shader.setFloat(1, size.y); // height
      _shader.setFloat(2, gameRef.currentTime()); // animation time
      _shader.setFloat(3, 0.8); // foil strength
      _shader.setFloat(4, 1.2); // saturation
      _shader.setFloat(5, 1.0); // lightness
      
      final paint = Paint()..shader = _shader;
      canvas.drawRect(size.toRect(), paint);
    }
    
    // Render card image and text
    _renderCardContent(canvas);
  }
}
```

**GLSL Shader** (`shaders/holographic_foil.frag`):
```glsl
#version 460 core

precision mediump float;

#include <flutter/runtime_effect.glsl>

uniform vec2 uSize;
uniform float uTime;
uniform float uStrength;
uniform float uSaturation;
uniform float uLightness;

out vec4 fragColor;

void main() {
  vec2 uv = FlutterFragCoord().xy / uSize;
  
  // Create rainbow gradient that shifts over time
  float angle = atan(uv.y - 0.5, uv.x - 0.5) + uTime;
  float radius = length(uv - vec2(0.5, 0.5));
  
  // Rainbow hue calculation
  float hue = fract(angle / (2.0 * 3.14159) + radius * 2.0);
  
  // Convert HSL to RGB
  vec3 rgb = vec3(
    abs(hue * 6.0 - 3.0) - 1.0,
    2.0 - abs(hue * 6.0 - 2.0),
    2.0 - abs(hue * 6.0 - 4.0)
  );
  rgb = clamp(rgb, 0.0, 1.0);
  
  // Apply saturation and lightness
  rgb = mix(vec3(0.5), rgb, uSaturation);
  rgb = mix(vec3(0.0), rgb, uLightness);
  
  // Mix with original pixel color
  vec4 texColor = texture(uTexture, uv);
  fragColor = mix(texColor, vec4(rgb, 1.0), uStrength);
}
```

---

## Backend Layer (Dart Frog)

### Dart Frog Project Structure

```
backend/
├── routes/                    # File-based routing
│   ├── index.dart            # GET /
│   ├── match/
│   │   ├── [id].dart        # GET/DELETE /match/:id
│   │   ├── create.dart      # POST /match/create
│   │   └── join.dart        # POST /match/join
│   ├── leaderboard/
│   │   └── index.dart       # GET /leaderboard
│   └── ws.dart              # WebSocket /ws
│
├── middleware/               # Middleware chain
│   ├── auth_middleware.dart
│   ├── logging_middleware.dart
│   └── cors_middleware.dart
│
├── services/                # Business logic
│   ├── match_service.dart
│   ├── leaderboard_service.dart
│   └── ai_service.dart
│
├── main.dart                # Server entry point
├── pubspec.yaml            # Dependencies
└── Dockerfile              # Container definition
```

### Example Route: Match Creation

```dart
/// POST /match/create
/// 
/// Creates a new match and returns match ID.
/// Server-authoritative: validates all inputs.
Future<Response> onRequest(RequestContext context) async {
  try {
    // Parse request body
    final json = await context.request.json() as Map<String, dynamic>;
    final userId = json['user_id'] as String;
    final deck = (json['deck'] as List).cast<String>();
    
    // Validate deck
    if (deck.length != 3) {
      return Response.json(
        statusCode: HttpStatus.badRequest,
        body: {'error': 'Deck must contain exactly 3 cards'},
      );
    }
    
    // Validate user authentication
    final user = await context.read<AuthService>().verifyUser(userId);
    if (user == null) {
      return Response.json(
        statusCode: HttpStatus.unauthorized,
        body: {'error': 'Invalid user'},
      );
    }
    
    // Create match using shared logic
    final matchService = context.read<MatchService>();
    final match = await matchService.createMatch(
      userId: userId,
      deck: deck,
    );
    
    // Save to Firestore
    await context.read<FirestoreService>().saveMatch(match);
    
    // Return match data
    return Response.json(
      body: {
        'match_id': match.id,
        'status': match.status,
        'created_at': match.createdAt.toIso8601String(),
      },
    );
  } catch (e, stack) {
    context.read<Logger>().severe('Match creation failed', e, stack);
    
    return Response.json(
      statusCode: HttpStatus.internalServerError,
      body: {'error': 'Failed to create match'},
    );
  }
}
```

### WebSocket Handler for Real-Time Gameplay

```dart
/// WebSocket route: /ws
/// 
/// Handles real-time match communication.
/// Maintains persistent connection during match.
Future<Response> onRequest(RequestContext context) async {
  final handler = webSocketHandler((channel, protocol) {
    final matchConnection = MatchConnection(
      channel: channel,
      matchService: context.read<MatchService>(),
      firestore: context.read<FirestoreService>(),
    );
    
    matchConnection.listen();
  });
  
  return handler(context.request);
}

class MatchConnection {
  MatchConnection({
    required this.channel,
    required this.matchService,
    required this.firestore,
  });

  final WebSocketChannel channel;
  final MatchService matchService;
  final FirestoreService firestore;
  
  String? matchId;
  String? userId;

  void listen() {
    channel.stream.listen(
      (message) async {
        try {
          final data = jsonDecode(message as String) as Map<String, dynamic>;
          await _handleMessage(data);
        } catch (e) {
          _sendError('Invalid message format');
        }
      },
      onDone: () => _handleDisconnect(),
      onError: (error) => _handleError(error),
    );
  }

  Future<void> _handleMessage(Map<String, dynamic> data) async {
    final type = data['type'] as String;
    
    switch (type) {
      case 'join_match':
        await _handleJoinMatch(data);
        break;
      case 'play_card':
        await _handlePlayCard(data);
        break;
      case 'end_turn':
        await _handleEndTurn(data);
        break;
      default:
        _sendError('Unknown message type: $type');
    }
  }

  Future<void> _handlePlayCard(Map<String, dynamic> data) async {
    final cardId = data['card_id'] as String;
    
    // Server-side validation using shared logic
    final result = await matchService.playCard(
      matchId: matchId!,
      userId: userId!,
      cardId: cardId,
    );
    
    if (result.isValid) {
      // Update Firestore
      await firestore.updateMatch(matchId!, result.matchState);
      
      // Broadcast to both players
      _broadcast({
        'type': 'card_played',
        'player_id': userId,
        'card_id': cardId,
        'match_state': result.matchState.toJson(),
      });
    } else {
      _sendError(result.error);
    }
  }

  void _broadcast(Map<String, dynamic> message) {
    channel.sink.add(jsonEncode(message));
  }

  void _sendError(String error) {
    channel.sink.add(jsonEncode({'type': 'error', 'message': error}));
  }

  void _handleDisconnect() {
    // Player disconnected, handle gracefully
    if (matchId != null) {
      matchService.handlePlayerDisconnect(matchId!, userId!);
    }
  }
}
```

### Middleware Stack

```dart
/// Auth middleware: Validates Firebase tokens.
Handler authMiddleware(Handler handler) {
  return (context) async {
    final authHeader = context.request.headers['authorization'];
    
    if (authHeader == null) {
      return Response.json(
        statusCode: HttpStatus.unauthorized,
        body: {'error': 'Missing authorization header'},
      );
    }
    
    try {
      // Verify Firebase token
      final token = authHeader.replaceFirst('Bearer ', '');
      final decodedToken = await FirebaseAuth.instance.verifyIdToken(token);
      
      // Add user to context
      return handler(
        context.provide<AuthenticatedUser>(
          () => AuthenticatedUser(
            uid: decodedToken.uid,
            email: decodedToken.email,
          ),
        ),
      );
    } catch (e) {
      return Response.json(
        statusCode: HttpStatus.unauthorized,
        body: {'error': 'Invalid token'},
      );
    }
  };
}

/// Logging middleware: Logs all requests.
Handler loggingMiddleware(Handler handler) {
  return (context) async {
    final stopwatch = Stopwatch()..start();
    
    final response = await handler(context);
    
    stopwatch.stop();
    
    context.read<Logger>().info(
      '${context.request.method} ${context.request.uri.path} '
      '- ${response.statusCode} (${stopwatch.elapsedMilliseconds}ms)',
    );
    
    return response;
  };
}
```

---

## Shared Packages Architecture

### Match Solver Package

**Purpose**: Share game logic between Flutter client and Dart Frog backend.

```
packages/match_solver/
├── lib/
│   ├── match_solver.dart        # Barrel export
│   ├── src/
│   │   ├── models/
│   │   │   ├── card.dart
│   │   │   ├── match_state.dart
│   │   │   └── player.dart
│   │   ├── solver/
│   │   │   ├── match_solver.dart
│   │   │   ├── damage_calculator.dart
│   │   │   └── win_conditions.dart
│   │   └── validators/
│   │       ├── deck_validator.dart
│   │       └── move_validator.dart
│   └── match_solver.dart
├── test/
│   └── match_solver_test.dart
└── pubspec.yaml
```

### Shared Game Logic

```dart
/// Match solver calculates game outcomes deterministically.
/// 
/// Used by both client (optimistic UI) and server (authority).
class MatchSolver {
  const MatchSolver();

  /// Calculates damage based on card elements.
  /// 
  /// Water beats Fire (+2 damage)
  /// Earth beats Water (+2 damage)
  /// Fire beats Earth (+2 damage)
  int calculateDamage(Card attackCard, Card defendCard) {
    var damage = attackCard.power;
    
    // Apply elemental bonuses
    if (_hasElementalAdvantage(attackCard.element, defendCard.element)) {
      damage += 2;
    }
    
    return damage;
  }

  bool _hasElementalAdvantage(Element attacker, Element defender) {
    return (attacker == Element.water && defender == Element.fire) ||
           (attacker == Element.earth && defender == Element.water) ||
           (attacker == Element.fire && defender == Element.earth);
  }

  /// Resolves a round and returns updated match state.
  MatchState resolveRound(
    MatchState currentState,
    Card player1Card,
    Card player2Card,
  ) {
    final p1Damage = calculateDamage(player1Card, player2Card);
    final p2Damage = calculateDamage(player2Card, player1Card);
    
    // Determine round winner
    RoundWinner winner;
    if (p1Damage > p2Damage) {
      winner = RoundWinner.player1;
    } else if (p2Damage > p1Damage) {
      winner = RoundWinner.player2;
    } else {
      winner = RoundWinner.tie;
    }
    
    // Update match state
    return currentState.copyWith(
      round: currentState.round + 1,
      player1Score: currentState.player1Score + (winner == RoundWinner.player1 ? 1 : 0),
      player2Score: currentState.player2Score + (winner == RoundWinner.player2 ? 1 : 0),
      lastRoundWinner: winner,
      playedCards: [
        ...currentState.playedCards,
        RoundResult(
          player1Card: player1Card,
          player2Card: player2Card,
          winner: winner,
        ),
      ],
    );
  }

  /// Checks if match is complete and returns winner.
  MatchResult? checkMatchComplete(MatchState state) {
    if (state.player1Score >= 2) {
      return MatchResult(winner: Player.player1, rounds: state.round);
    } else if (state.player2Score >= 2) {
      return MatchResult(winner: Player.player2, rounds: state.round);
    }
    return null;
  }
}
```

### Benefits of Shared Package

1. **Single Source of Truth**: Game rules defined once
2. **Optimistic UI**: Client can predict outcomes instantly
3. **Server Authority**: Server validates using same logic
4. **Type Safety**: Dart's type system ensures consistency
5. **Testability**: Logic tested independently

---

## State Management (BLoC Pattern)

### BLoC Architecture

```dart
/// Match BLoC manages match gameplay state.
/// 
/// Separates business logic from UI.
class MatchBloc extends Bloc<MatchEvent, MatchState> {
  MatchBloc({
    required MatchRepository matchRepository,
    required AudioController audioController,
  })  : _matchRepository = matchRepository,
        _audioController = audioController,
        super(const MatchState.initial()) {
    on<MatchStarted>(_onMatchStarted);
    on<CardPlayed>(_onCardPlayed);
    on<RoundCompleted>(_onRoundCompleted);
    on<MatchUpdated>(_onMatchUpdated);
  }

  final MatchRepository _matchRepository;
  final AudioController _audioController;
  
  StreamSubscription<MatchState>? _matchSubscription;

  Future<void> _onMatchStarted(
    MatchStarted event,
    Emitter<MatchState> emit,
  ) async {
    emit(const MatchState.loading());
    
    try {
      // Create or join match
      final match = await _matchRepository.createMatch(
        userId: event.userId,
        deck: event.deck,
      );
      
      // Subscribe to real-time updates
      _matchSubscription = _matchRepository
          .watchMatch(match.id)
          .listen((matchState) {
        add(MatchUpdated(matchState));
      });
      
      emit(MatchState.inProgress(match));
      
      // Play start sound
      _audioController.playSfx(Sfx.matchStart);
    } catch (e) {
      emit(MatchState.error(e.toString()));
    }
  }

  Future<void> _onCardPlayed(
    CardPlayed event,
    Emitter<MatchState> emit,
  ) async {
    final currentState = state;
    if (currentState is! MatchInProgress) return;
    
    // Optimistic update (local prediction)
    final optimisticState = _applyCardPlayLocally(
      currentState,
      event.card,
    );
    emit(optimisticState);
    
    // Play card sound
    _audioController.playSfx(Sfx.cardPlayed);
    
    try {
      // Send to server for validation
      await _matchRepository.playCard(
        matchId: currentState.match.id,
        cardId: event.card.id,
      );
      
      // Server will send back validated state via WebSocket
      // which triggers MatchUpdated event
    } catch (e) {
      // Rollback optimistic update
      emit(currentState);
      emit(MatchState.error('Failed to play card: $e'));
    }
  }

  Future<void> _onMatchUpdated(
    MatchUpdated event,
    Emitter<MatchState> emit,
  ) async {
    final matchState = event.matchState;
    
    // Check if match is complete
    if (matchState.isComplete) {
      emit(MatchState.complete(matchState));
      
      // Play end sound
      _audioController.playSfx(
        matchState.didPlayerWin ? Sfx.victory : Sfx.defeat,
      );
    } else {
      emit(MatchState.inProgress(matchState));
    }
  }

  MatchState _applyCardPlayLocally(
    MatchInProgress currentState,
    Card card,
  ) {
    // Use shared match solver for local prediction
    final solver = const MatchSolver();
    
    // Calculate expected outcome
    final updatedMatch = solver.resolveRound(
      currentState.match,
      card,
      currentState.opponentCard, // May not know yet
    );
    
    return MatchState.inProgress(updatedMatch);
  }

  @override
  Future<void> close() {
    _matchSubscription?.cancel();
    return super.close();
  }
}
```

### Match State Definition

```dart
/// Match state using freezed for immutability.
@freezed
class MatchState with _$MatchState {
  const factory MatchState.initial() = MatchInitial;
  
  const factory MatchState.loading() = MatchLoading;
  
  const factory MatchState.inProgress(Match match) = MatchInProgress;
  
  const factory MatchState.complete(Match match) = MatchComplete;
  
  const factory MatchState.error(String message) = MatchError;
}
```

---

## Data Layer (Firebase)

### Firestore Data Model

```dart
/// Firestore collections structure.
const FIRESTORE_SCHEMA = {
  // Users collection
  'users': {
    '[userId]': {
      'displayName': 'string',
      'wins': 'number',
      'losses': 'number',
      'currentStreak': 'number',
      'createdAt': 'timestamp',
    }
  },
  
  // Matches collection
  'matches': {
    '[matchId]': {
      'player1Id': 'string',
      'player2Id': 'string',
      'player1Deck': ['cardId1', 'cardId2', 'cardId3'],
      'player2Deck': ['cardId1', 'cardId2', 'cardId3'],
      'player1Score': 'number',
      'player2Score': 'number',
      'currentRound': 'number',
      'status': 'string', // 'waiting', 'in_progress', 'complete'
      'winnerId': 'string?',
      'playedCards': [{
        'round': 'number',
        'player1CardId': 'string',
        'player2CardId': 'string',
        'winner': 'string',
      }],
      'createdAt': 'timestamp',
      'updatedAt': 'timestamp',
    }
  },
  
  // Cards collection (AI-generated)
  'cards': {
    '[cardId]': {
      'name': 'string',
      'description': 'string',
      'element': 'string', // 'water', 'fire', 'earth'
      'power': 'number',
      'suit': 'string',
      'rarity': 'string',
      'imageUrl': 'string',
      'generatedBy': 'string', // 'Muse', 'PaLM', etc.
      'createdAt': 'timestamp',
    }
  },
  
  // Leaderboard collection
  'leaderboard': {
    '[entryId]': {
      'userId': 'string',
      'displayName': 'string',
      'wins': 'number',
      'currentStreak': 'number',
      'rank': 'number',
      'updatedAt': 'timestamp',
    }
  },
};
```

### Firestore Security Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Users can read any user profile
    // Users can only update their own profile
    match /users/{userId} {
      allow read: if true;
      allow write: if request.auth.uid == userId;
    }
    
    // Matches can be read by participants
    // Matches can only be created/updated by backend
    match /matches/{matchId} {
      allow read: if request.auth.uid in resource.data.playerIds;
      allow create: if false; // Only backend can create
      allow update: if false; // Only backend can update
    }
    
    // Cards can be read by anyone
    // Cards can only be created by backend
    match /cards/{cardId} {
      allow read: if true;
      allow write: if false; // Only backend
    }
    
    // Leaderboard is read-only for clients
    match /leaderboard/{entryId} {
      allow read: if true;
      allow write: if false; // Only backend
    }
  }
}
```

### Firebase Repository Implementation

```dart
/// Repository pattern for Firestore access.
/// 
/// Abstracts Firebase SDK from business logic.
class MatchRepository {
  MatchRepository({
    required FirebaseFirestore firestore,
    required FirebaseAuth auth,
  })  : _firestore = firestore,
        _auth = auth;

  final FirebaseFirestore _firestore;
  final FirebaseAuth _auth;

  /// Creates a new match.
  Future<Match> createMatch({
    required String userId,
    required List<String> deck,
  }) async {
    final matchRef = _firestore.collection('matches').doc();
    
    final match = Match(
      id: matchRef.id,
      player1Id: userId,
      player1Deck: deck,
      status: MatchStatus.waiting,
      createdAt: DateTime.now(),
    );
    
    await matchRef.set(match.toFirestore());
    
    return match;
  }

  /// Watches match for real-time updates.
  Stream<Match> watchMatch(String matchId) {
    return _firestore
        .collection('matches')
        .doc(matchId)
        .snapshots()
        .map((snapshot) {
      if (!snapshot.exists) {
        throw MatchNotFoundException(matchId);
      }
      return Match.fromFirestore(snapshot);
    });
  }

  /// Gets leaderboard with pagination.
  Future<List<LeaderboardEntry>> getLeaderboard({
    int limit = 50,
  }) async {
    final snapshot = await _firestore
        .collection('leaderboard')
        .orderBy('wins', descending: true)
        .limit(limit)
        .get();
    
    return snapshot.docs
        .map((doc) => LeaderboardEntry.fromFirestore(doc))
        .toList();
  }

  /// Gets card by ID from cache or Firestore.
  Future<Card> getCard(String cardId) async {
    final doc = await _firestore
        .collection('cards')
        .doc(cardId)
        .get();
    
    if (!doc.exists) {
      throw CardNotFoundException(cardId);
    }
    
    return Card.fromFirestore(doc);
  }
}
```

---

## Deployment & Infrastructure

### Cloud Run Deployment

```dockerfile
# Dockerfile for Dart Frog backend
FROM dart:stable AS build

WORKDIR /app

# Copy pubspec files
COPY pubspec.* ./

# Get dependencies
RUN dart pub get

# Copy source code
COPY . .

# Build production bundle
RUN dart pub global activate dart_frog_cli
RUN dart_frog build

# Runtime stage
FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /app/build /app

WORKDIR /app

EXPOSE 8080

CMD ["/app/bin/server"]
```

### Cloud Run Configuration

```yaml
# cloud-run.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: io-flip-backend
spec:
  template:
    metadata:
      annotations:
        # Auto-scaling configuration
        autoscaling.knative.dev/minScale: "0"  # Scale to zero when idle
        autoscaling.knative.dev/maxScale: "100"
        
        # Resource limits
        run.googleapis.com/cpu-throttling: "true"
        run.googleapis.com/startup-cpu-boost: "true"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      serviceAccountName: io-flip-backend@PROJECT.iam.gserviceaccount.com
      
      containers:
      - image: gcr.io/PROJECT/io-flip-backend:latest
        ports:
        - name: http1
          containerPort: 8080
        
        env:
        - name: FIREBASE_PROJECT_ID
          value: "io-flip-prod"
        - name: ENVIRONMENT
          value: "production"
        
        resources:
          limits:
            cpu: "2"
            memory: "512Mi"
          requests:
            cpu: "1"
            memory: "256Mi"
```

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud Run

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.24.0'
    
    # Build Frontend
    - name: Build Flutter Web
      run: |
        cd frontend
        flutter pub get
        flutter build web --release
    
    # Deploy Frontend to Firebase Hosting
    - name: Deploy to Firebase Hosting
      uses: FirebaseExtended/action-hosting-deploy@v0
      with:
        repoToken: '${{ secrets.GITHUB_TOKEN }}'
        firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
        projectId: io-flip-prod
    
    # Build Backend
    - name: Setup Dart
      uses: dart-lang/setup-dart@v1
    
    - name: Build Dart Frog Backend
      run: |
        cd backend
        dart pub global activate dart_frog_cli
        dart_frog build
    
    # Deploy Backend to Cloud Run
    - name: Authenticate to Google Cloud
      uses: google-github-actions/auth@v1
      with:
        credentials_json: '${{ secrets.GCP_SA_KEY }}'
    
    - name: Build and Push Docker Image
      run: |
        cd backend
        gcloud builds submit --tag gcr.io/io-flip-prod/backend
    
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy io-flip-backend \
          --image gcr.io/io-flip-prod/backend \
          --platform managed \
          --region us-central1 \
          --allow-unauthenticated
```

---

## Adapting I/O FLIP for Unwritten

### Key Differences

| Aspect | I/O FLIP | Unwritten |
|--------|----------|----------|
| **Genre** | Multiplayer card battle | Single-player narrative |
| **Backend Purpose** | Match validation, matchmaking | AI generation, progression tracking |
| **Real-Time** | WebSocket (PvP sync) | Optional (cloud saves) |
| **AI Usage** | Card generation (pre-game) | Live narrative generation (in-game) |
| **State Management** | Server-authoritative (anti-cheat) | Client-first with cloud sync |
| **Game Loop** | Turn-based battles | Turn-based life simulation |

### Architecture Adaptations

#### 1. Replace Multiplayer with AI Backend

**I/O FLIP Pattern**:
```dart
// Client sends move to server
await matchRepository.playCard(cardId);

// Server validates and broadcasts to both players via WebSocket
```

**Unwritten Adaptation**:
```dart
// Client sends card play with context
final result = await gameRepository.playCard(
  cardId: cardId,
  context: InteractionContext(
    npcId: selectedNpc.id,
    location: currentLocation,
    emotionalState: playerState.emotion,
  ),
);

// Backend generates AI narrative response
final narrative = await aiService.generateResponse(result);

// Client updates state with narrative
gameBloc.add(NarrativeGenerated(narrative));
```

#### 2. Adapt Shared Package for Single-Player Logic

**I/O FLIP** (`match_solver`):
```dart
// Calculates who wins the round
final result = matchSolver.resolveRound(card1, card2);
```

**Unwritten** (`game_logic`):
```dart
// Calculates relationship impact
final impact = relationshipCalculator.calculateImpact(
  card: card,
  npc: npc,
  context: context,
);

// Determines progression
final progress = progressionCalculator.calculateProgress(
  aspiration: currentAspiration,
  completedMilestones: milestones,
);
```

#### 3. Firestore Schema for Narrative Game

```dart
const UNWRITTEN_FIRESTORE_SCHEMA = {
  'users': {
    '[userId]': {
      'displayName': 'string',
      'tier': 'string', // 'free', 'premium'
      'currentSeasonId': 'string?',
      'stats': {
        'seasonsCompleted': 'number',
        'totalPlaytime': 'number',
      },
    }
  },
  
  'seasons': {
    '[seasonId]': {
      'userId': 'string',
      'aspirationId': 'string',
      'length': 'number', // 12, 24, or 36 weeks
      'currentWeek': 'number',
      'currentDay': 'number',
      'status': 'string', // 'active', 'complete'
      'startedAt': 'timestamp',
      'lastPlayedAt': 'timestamp',
    }
  },
  
  'cards': {
    '[cardId]': {
      'userId': 'string',
      'type': 'string',
      'title': 'string',
      'description': 'string',
      'level': 'number',
      'evolutionHistory': [{
        'date': 'timestamp',
        'changes': 'string',
      }],
    }
  },
  
  'relationships': {
    '[relationshipId]': {
      'userId': 'string',
      'seasonId': 'string',
      'npcId': 'string',
      'level': 'number',
      'trust': 'number',
      'interactionCount': 'number',
      'memories': [{
        'description': 'string',
        'significance': 'number',
        'week': 'number',
      }],
    }
  },
  
  'ai_queue': {
    '[jobId]': {
      'userId': 'string',
      'type': 'string', // 'evolution', 'dialogue', 'narrative'
      'status': 'string', // 'pending', 'processing', 'complete'
      'input': 'map',
      'output': 'map?',
      'createdAt': 'timestamp',
      'completedAt': 'timestamp?',
    }
  },
};
```

#### 4. Backend Routes for Unwritten

```
backend/
├── routes/
│   ├── ai/
│   │   ├── generate_dialogue.dart      # POST /ai/generate-dialogue
│   │   ├── evolve_card.dart           # POST /ai/evolve-card
│   │   └── generate_narrative.dart    # POST /ai/generate-narrative
│   ├── game/
│   │   ├── play_card.dart             # POST /game/play-card
│   │   ├── advance_turn.dart          # POST /game/advance-turn
│   │   └── complete_season.dart       # POST /game/complete-season
│   ├── sync/
│   │   ├── upload.dart                # POST /sync/upload
│   │   └── download.dart              # GET /sync/download
│   └── training/
│       └── log_interaction.dart       # POST /training/log
```

#### 5. Dart Frog AI Integration

```dart
/// POST /ai/generate-dialogue
/// 
/// Generates NPC dialogue using cloud AI.
Future<Response> onRequest(RequestContext context) async {
  final json = await context.request.json() as Map<String, dynamic>;
  
  final request = DialogueRequest.fromJson(json);
  
  // Validate request
  final user = await context.read<AuthService>().verifyUser(request.userId);
  if (user == null) {
    return Response.json(
      statusCode: HttpStatus.unauthorized,
      body: {'error': 'Invalid user'},
    );
  }
  
  // Check AI quota
  final quotaService = context.read<QuotaService>();
  if (!await quotaService.hasQuota(user.id, user.tier)) {
    return Response.json(
      statusCode: HttpStatus.tooManyRequests,
      body: {'error': 'AI quota exceeded'},
    );
  }
  
  // Generate dialogue using OpenAI/Anthropic
  final aiService = context.read<AIService>();
  final dialogue = await aiService.generateNPCDialogue(
    npcId: request.npcId,
    personality: request.personality,
    context: request.context,
    relationshipLevel: request.relationshipLevel,
    emotionalCapacity: request.emotionalCapacity,
  );
  
  // Log for training data
  await context.read<TrainingDataService>().logInteraction(
    userId: user.id,
    type: 'dialogue_generation',
    input: request.toJson(),
    output: dialogue.toJson(),
  );
  
  // Deduct quota
  await quotaService.deductQuota(user.id);
  
  return Response.json(body: dialogue.toJson());
}
```

---

## Implementation Roadmap

### Phase 1: Foundation with I/O FLIP Patterns (Weeks 1-4)

**Goal**: Set up Flutter + Dart Frog architecture

**Tasks**:
1. **Flutter Project Setup**
   - Use I/O FLIP's feature-first structure
   - Implement BLoC pattern for state management
   - Set up go_router for navigation
   - Configure Firebase (Firestore, Auth, Storage)

2. **Dart Frog Backend Setup**
   - Initialize Dart Frog project
   - Set up file-based routes
   - Configure middleware (auth, logging, CORS)
   - Deploy to Cloud Run

3. **Shared Package**
   - Create `game_logic` package
   - Define data models (Card, GameState, Relationship)
   - Implement relationship calculator
   - Share between frontend and backend

4. **Basic UI with Flame** (Optional)
   - Set up Flame game engine
   - Create basic card components
   - Implement card animations

**Deliverables**:
- ✅ Flutter app compiles and runs
- ✅ Dart Frog backend deployed to Cloud Run
- ✅ Firebase connected and working
- ✅ Shared package used by both frontend/backend

### Phase 2: Game Loop + Backend Integration (Weeks 5-8)

**Goal**: Implement playable turn-based loop with backend

**Tasks**:
1. **Card System**
   - Card display with Flutter widgets
   - Card playing mechanics
   - Hand management

2. **Backend Routes**
   - POST /game/play-card
   - POST /game/advance-turn
   - GET /game/state

3. **State Sync**
   - Optimistic UI updates
   - Server validation
   - State synchronization

4. **Persistence**
   - Save game state to Firestore
   - Load game on app start
   - Auto-save every turn

**Deliverables**:
- ✅ Can play cards from hand
- ✅ Backend validates moves
- ✅ State persists to Firestore
- ✅ Optimistic UI feels responsive

### Phase 3: AI Integration (Weeks 9-12)

**Goal**: Add cloud AI for narrative generation

**Tasks**:
1. **AI Service (Backend)**
   - OpenAI/Anthropic integration
   - Prompt engineering for dialogue
   - Response parsing and validation

2. **AI Routes**
   - POST /ai/generate-dialogue
   - POST /ai/evolve-card
   - POST /ai/generate-narrative

3. **Training Data Logging**
   - Log all AI interactions
   - Store in Firestore or BigQuery
   - Export as JSONL for fine-tuning

4. **Quota Management**
   - Track AI usage per user
   - Implement daily limits
   - Premium tier unlimited

**Deliverables**:
- ✅ NPCs respond with AI-generated dialogue
- ✅ Cards evolve with AI descriptions
- ✅ All interactions logged for training
- ✅ Quota system working

### Phase 4: Season System (Weeks 13-16)

**Goal**: Full season structure with progression

**Tasks**:
1. **Season Management**
   - Start/end season flows
   - Week/day progression
   - Aspiration tracking

2. **Relationship System**
   - Level progression
   - Trust calculation
   - Memory storage

3. **Archives**
   - Season completion
   - Save to archive
   - View past seasons

**Deliverables**:
- ✅ Complete 12-week season
- ✅ Relationships progress correctly
- ✅ Season archived on completion

### Phase 5: Polish & Beta (Weeks 17-20)

**Goal**: Production-ready with monitoring

**Tasks**:
1. **Performance Optimization**
   - Caching strategies
   - Asset optimization
   - Backend scaling validation

2. **Monitoring**
   - Firebase Analytics
   - Error tracking (Sentry)
   - Performance monitoring

3. **Testing**
   - Integration tests
   - Load testing backend
   - User acceptance testing

**Deliverables**:
- ✅ Beta ready
- ✅ Monitoring in place
- ✅ Performance validated

---

## Key Takeaways

### What We Adopt from I/O FLIP

1. **✅ Full-Stack Dart Architecture**
   - Flutter frontend + Dart Frog backend
   - Shared packages for code reuse
   - Type-safe end-to-end

2. **✅ Firebase Ecosystem**
   - Firestore for database
   - Firebase Auth for users
   - Cloud Storage for assets
   - Firebase Hosting for static files

3. **✅ BLoC State Management**
   - Separates UI from business logic
   - Testable and maintainable
   - Reactive state updates

4. **✅ Server-Side Logic**
   - Backend validates critical operations
   - Prevents cheating/tampering
   - Authoritative source of truth

5. **✅ Cloud-Native Deployment**
   - Cloud Run auto-scaling
   - Firebase CDN
   - Global availability

### What We Adapt for Unwritten

1. **🔄 WebSocket → Polling/Cloud Sync**
   - No real-time multiplayer needed
   - Periodic sync for cloud saves
   - Background AI generation

2. **🔄 Match Validation → AI Generation**
   - Backend generates content, not validates matches
   - AI routes instead of match routes
   - Training data collection

3. **🔄 Shared Battle Logic → Shared Game Logic**
   - Relationship calculations
   - Progression formulas
   - Resource management

4. **🔄 Leaderboards → Season Archives**
   - Personal progression tracking
   - No competitive elements
   - Novel generation from archives

---

## Compliance Checklist

- [x] Uses I/O FLIP's proven architecture patterns
- [x] Adapts for single-player narrative gameplay
- [x] Full-stack Dart (Flutter + Dart Frog)
- [x] Firebase ecosystem integration
- [x] BLoC state management pattern
- [x] Shared package architecture
- [x] Cloud-native deployment (Cloud Run)
- [x] Follows Master Truths v1.2 specifications
- [x] Training data collection strategy
- [x] Scalable and production-ready

---

**Document Version**: 1.0  
**Last Updated**: October 14, 2025  
**Status**: Ready for implementation  
**Next**: Begin Phase 1 with Flutter + Dart Frog setup


