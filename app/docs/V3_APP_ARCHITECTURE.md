# V3 App Architecture — Complete Restructure

> **Purpose**: Clean-slate architecture aligned with V3 Master Truths. This document defines the complete `lib/` structure and justifies each component.

**Context**: The existing `lib/features/` codebase is fundamentally misaligned with V3. Rather than incremental patches, this proposes a full restructure that will be faster and produce better results.

---

## 1. Top-Level Structure

```
lib/
├── core/                     # Framework-level shared code
│   ├── constants/
│   ├── errors/
│   ├── utils/
│   └── engine/              # Core Simulation Engines (NEW)
│
├── data/                     # Data layer (Clean Architecture)
│   ├── models/              # L2 Templates, L3 Instances, GameContext
│   ├── repositories/        # Data access abstractions
│   └── sources/             # Remote (Firebase/Supabase) & Local (Hive/SQLite)
│
├── domain/                   # Business logic layer
│   ├── entities/            # Pure domain models
│   ├── repositories/        # Repository interfaces
│   └── usecases/            # Business logic use cases
│
├── services/                 # Cross-cutting services (V3-aligned)
│   ├── ewr/                 # ENGINE_WRITERS_ROOM (unified AI)
│   ├── cfp/                 # Contextually Filtered Pool
│   ├── memory/              # Archive, Vector DB, Graph DB
│   ├── prefetch/            # Predictive pre-fetching
│   └── state/               # Riverpod state management
│
├── game/                     # Flame rendering layer (NEW)
│   ├── unwritten_game.dart
│   ├── components/
│   ├── systems/
│   └── assets/
│
├── presentation/             # Flutter overlays only (REVISED)
│   ├── overlays/            # UI clusters, HUD
│   ├── screens/             # Menu screens only
│   └── theme/               # Design system
│
├── game_loop/                # Core gameplay loop (V3 Turn Structure)
│   ├── turn_controller.dart
│   ├── hand_manager.dart
│   ├── time_progression.dart
│   └── state_card_manager.dart
│
└── main.dart
```

---

## 2. Core Simulation Engines (`lib/core/engine/`)

**Purpose**: Implement the four foundational engines that power all simulation logic.

```
lib/core/engine/
├── engine_personality.dart   # OCEAN perceptual filtering
├── engine_capacity.dart       # Emotional bandwidth and support limits
├── engine_memory.dart         # Archive, Vector DB, Graph DB
├── engine_writers_room.dart   # AI orchestrator (qualitative assessment)
└── engine_interface.dart      # Base interfaces for all engines
```

### `engine_personality.dart`

```dart
/// ENGINE_PERSONALITY: OCEAN-based perceptual filtering system
class EnginePersonality {
  /// OCEAN traits: 0.0-1.0 each
  final double openness;
  final double conscientiousness;
  final double extraversion;
  final double agreeableness;
  final double neuroticism;
  
  /// Calculate personality compatibility between two characters
  double calculateCompatibility(EnginePersonality other);
  
  /// Apply perceptual filter to objective tension level
  /// High Neuroticism amplifies tension, Low Neuroticism dampens
  double applyTensionFilter(double objectiveTension);
  
  /// Modify costs based on personality
  InstanceCosts modifyCosts(BaseCosts base, String activityType);
  
  /// Determine available options based on personality
  List<String> filterAvailableOptions(
    List<String> allOptions,
    GameContext context,
  );
}
```

### `engine_capacity.dart`

```dart
/// ENGINE_CAPACITY: Emotional bandwidth and support system
class EngineCapacity {
  /// Current capacity: 0.0-10.0
  double current;
  
  /// Default baseline: 5.0 (healthy human)
  static const double baseline = 5.0;
  
  /// Capacity zones
  bool get isThriving => current >= 8.0;
  bool get isStable => current >= 5.0 && current < 8.0;
  bool get isVulnerable => current >= 3.0 && current < 5.0;
  bool get isFragile => current >= 1.0 && current < 3.0;
  bool get isBreakdown => current < 1.0;
  
  /// Support rule: Can provide up to (capacity + 2) level support
  double get maxSupportLevel => current + 2.0;
  
  /// Check if can effectively support a crisis
  bool canSupportCrisis(double crisisLevel) =>
      maxSupportLevel > crisisLevel;
  
  /// Apply perception gate (can't see what you're too overwhelmed to notice)
  bool canPerceiveOption(String optionId, double requiredCapacity) =>
      current >= requiredCapacity;
  
  /// Modify XP gain based on capacity (learning bandwidth)
  double modifyXP(double baseXP) {
    if (current >= 7.0) return baseXP * 1.2;
    if (current <= 3.0) return baseXP * 0.5;
    return baseXP;
  }
}
```

### `engine_memory.dart`

```dart
/// ENGINE_MEMORY: Archive, Vector DB, Graph DB integration
class EngineMemory {
  /// Store interaction in Archive with full metadata
  Future<void> storeInteraction(L3_ContextualInstance instance, {
    required Map<String, dynamic> metadata,
    required List<String> thematicTags,
    required List<String> emotionalTones,
  });
  
  /// Query Vector DB for semantic patterns
  Future<List<MemoryMatch>> queryPatterns({
    required String query,
    required int topK,
    double? minSimilarity,
  });
  
  /// Calculate Memory Resonance for current moment
  Future<MemoryResonance> calculateResonance({
    required String currentContext,
    required List<String> thematicTags,
  });
  
  /// Graph DB: Get relationship network
  Future<RelationshipGraph> getRelationshipGraph(String npcId);
  
  /// Graph DB: Get location associations
  Future<LocationGraph> getLocationGraph(String locationId);
}
```

### `engine_writers_room.dart`

```dart
/// ENGINE_WRITERS_ROOM: AI orchestrator for qualitative assessment
class EngineWritersRoom {
  /// Assess evolution readiness (qualitative, NOT numerical)
  Future<EvolutionAssessment> assessEvolution({
    required List<Memory> interactionHistory,
    required List<String> qualityIndicators,
    required double personalityCompatibility,
    required List<double> currentReceptivity,
  });
  
  /// Instantiate L3 Instance from L2 Template
  Future<L3_ContextualInstance> instantiateTemplate({
    required L2_MasterTemplate template,
    required GameContext context,
  });
  
  /// Determine outcome tier from outcome spectrum
  Future<OutcomeResult> determineOutcome({
    required L2_MasterTemplate template,
    required GameContext context,
  });
  
  /// Detect Journey Beat occurrence
  Future<JourneyBeat?> detectJourneyBeat({
    required L3_ContextualInstance instance,
    required String npcId,
    required GameContext context,
  });
  
  /// Generate Season Novel
  Future<String> generateSeasonNovel({
    required List<Memory> seasonArchive,
    required List<String> thematicArcs,
    required int targetWordCount,
  });
}
```

---

## 3. Data Layer (`lib/data/`)

**Purpose**: Clean Architecture separation - data access logic isolated from business logic.

```
lib/data/
├── models/
│   ├── l2_master_template.dart        # Master Template JSON → Dart
│   ├── l3_contextual_instance.dart    # Generated card instances
│   ├── game_context.dart              # Complete game state snapshot
│   ├── cfp_state.dart                 # CFP probability distribution
│   ├── journey_beat.dart              # Relationship progression beats
│   └── state_card.dart                # Passive modifiers
│
├── repositories/
│   ├── template_repository.dart       # Load/cache L2 Templates
│   ├── instance_repository.dart       # Store/retrieve L3 Instances
│   ├── game_state_repository.dart     # Save/load game state
│   └── archive_repository.dart        # Archive queries
│
└── sources/
    ├── remote/
    │   ├── firebase_ewr_api.dart      # EWR API client
    │   ├── supabase_storage_api.dart  # Archive/Graph DB
    │   └── vector_db_api.dart         # Semantic search
    │
    └── local/
        ├── hive_cache.dart            # Local template cache
        ├── sqlite_archive.dart        # Local archive mirror
        └── preferences.dart           # Settings
```

### Key Models

**`l2_master_template.dart`:**
```dart
/// Master Template (L2) - Design artifact defining generation rules
@freezed
class L2_MasterTemplate with _$L2_MasterTemplate {
  const factory L2_MasterTemplate({
    required String id,
    required DNAStrand dnaStrand,
    required TemplateMeta meta,
    required CFPRules cfpRules,
    required InstantiationRules instantiation,
    required CostStructure costs,
    required OutcomeSpectrums outcomes,
    required EvolutionRules evolution,
    required FusionRules fusion,
  }) = _L2_MasterTemplate;
  
  factory L2_MasterTemplate.fromJson(Map<String, dynamic> json) =>
      _$L2_MasterTemplateFromJson(json);
}
```

**`l3_contextual_instance.dart`:**
```dart
/// Contextual Instance (L3) - Unique generated card
@freezed
class L3_ContextualInstance with _$L3_ContextualInstance {
  const factory L3_ContextualInstance({
    required String instanceId,
    required String templateId,
    required String title,
    required String description,
    required InstanceCosts costs,
    required EvolutionStage evolutionStage,
    String? artUrl,
    required GenerationMetadata metadata,
  }) = _L3_ContextualInstance;
  
  factory L3_ContextualInstance.fromJson(Map<String, dynamic> json) =>
      _$L3_ContextualInstanceFromJson(json);
}

enum EvolutionStage { generic, personalized, cherished }
```

**`game_context.dart`:**
```dart
/// Complete snapshot of game state for EWR context
@freezed
class GameContext with _$GameContext {
  const factory GameContext({
    required CharacterState character,
    required Map<String, NPCState> npcs,
    required List<StateCard> activeStates,
    required DateTime currentTime,
    required List<Aspiration> activeAspirations,
    required List<L3_ContextualInstance> recentInteractions,
    required Map<String, double> resourceLevels,
  }) = _GameContext;
}
```

---

## 4. Services Layer (`lib/services/`)

**Purpose**: V3-aligned services that orchestrate the simulation.

```
lib/services/
├── ewr/
│   ├── ewr_service.dart               # Main EWR orchestrator
│   ├── tier_router.dart               # T1/T2/T3 routing logic
│   ├── batch_generator.dart           # Batch generation optimization
│   └── quality_validator.dart         # Narrative quality validation
│
├── cfp/
│   ├── cfp_service.dart               # CFP probability management
│   ├── incremental_updater.dart       # Efficient CFP updates
│   ├── hand_generator.dart            # 7-card hand composition
│   └── diversity_enforcer.dart        # Prevent stale hands
│
├── memory/
│   ├── archive_service.dart           # Archive storage/retrieval
│   ├── vector_service.dart            # Semantic pattern detection
│   ├── graph_service.dart             # Relationship/location networks
│   └── resonance_calculator.dart      # Memory Resonance
│
├── prefetch/
│   ├── prefetch_service.dart          # Predictive pre-fetching
│   ├── buffer_manager.dart            # Instance buffer (3-4 cards)
│   └── hit_rate_monitor.dart          # Track buffer efficiency
│
└── state/
    ├── game_state_provider.dart       # Riverpod global state
    ├── turn_state_provider.dart       # Current turn state
    └── ui_state_provider.dart         # UI-specific state
```

### Key Services

**`ewr_service.dart`:**
```dart
/// ENGINE_WRITERS_ROOM Service - Unified AI orchestrator
class EWRService {
  final FirebaseEWRApi _api;
  final TierRouter _tierRouter;
  final QualityValidator _validator;
  
  /// Main instantiation method (replaces all V1.2 specialized methods)
  Future<L3_ContextualInstance> instantiateTemplate({
    required L2_MasterTemplate template,
    required GameContext context,
  }) async {
    // Determine tier
    final tier = _tierRouter.selectTier(template, context);
    
    // Route to appropriate generation
    final instance = switch (tier) {
      GenerationTier.t1_local => _generateTier1Local(template, context),
      GenerationTier.t2_ewr_light => await _generateTier2Light(template, context),
      GenerationTier.t3_ewr_heavy => await _generateTier3Heavy(template, context),
    };
    
    // Validate quality (T2/T3 only)
    if (tier != GenerationTier.t1_local) {
      await _validator.validate(instance);
    }
    
    return instance;
  }
  
  /// Assess evolution readiness (qualitative)
  Future<EvolutionAssessment> assessEvolution({
    required String templateId,
    required String npcId,
    required GameContext context,
  }) async {
    final history = await _memoryService.queryPatterns(
      query: "interactions_with_$npcId",
      topK: 50,
    );
    
    final assessment = await _api.assessEvolution(
      interactionHistory: history,
      qualityIndicators: ["emotional_depth", "reciprocity", "consistency"],
      personalityCompatibility: _calculateCompatibility(context, npcId),
      currentReceptivity: [context.character.capacity, context.npcs[npcId]!.capacity],
    );
    
    return assessment;
  }
  
  /// Determine outcome from spectrum (replaces deterministic formula)
  Future<OutcomeResult> determineOutcome({
    required L3_ContextualInstance instance,
    required GameContext context,
  }) async {
    final template = await _templateRepo.getTemplate(instance.templateId);
    
    final outcome = await _api.determineOutcome(
      template: template,
      context: context,
    );
    
    return outcome;
  }
}
```

**`cfp_service.dart`:**
```dart
/// Contextually Filtered Pool service
class CFPService {
  /// Update CFP incrementally (NOT full recalculation)
  Future<void> updateCFP({
    required CFPChangeType changeType,
    required Map<String, dynamic> changeData,
  }) async {
    // Identify affected templates only
    final affected = _identifyAffectedTemplates(changeType, changeData);
    
    // Recalculate only affected weights (10-60 templates, < 10ms)
    for (final templateId in affected) {
      final template = await _templateRepo.getTemplate(templateId);
      final newWeight = _calculateWeight(template, _currentContext);
      _cfpState[templateId] = newWeight;
    }
    
    // Normalize total probability mass to 1.0
    _normalizeProbabilities();
    
    // Emit updated CFP
    _cfpController.add(_cfpState);
  }
  
  /// Draw 7-card hand from CFP
  Future<List<L3_ContextualInstance>> drawHand() async {
    // Weighted draw ensuring diversity
    final selectedTemplates = _diversityEnforcer.weightedDraw(
      cfp: _cfpState,
      count: 7,
    );
    
    // Instantiate via EWR (respects tiers)
    final instances = await Future.wait(
      selectedTemplates.map((template) => 
        _ewrService.instantiateTemplate(
          template: template,
          context: _currentContext,
        ),
      ),
    );
    
    return instances;
  }
}
```

**`prefetch_service.dart`:**
```dart
/// Predictive pre-fetching to mask T2 latency
class PrefetchService {
  final BufferManager _buffer;
  final CFPService _cfpService;
  final EWRService _ewrService;
  
  /// Trigger pre-fetch when hand size drops to 4
  Future<void> triggerPreFetch() async {
    if (_buffer.size >= 3) return; // Buffer already full
    
    // Update CFP
    await _cfpService.updateCFP(
      changeType: CFPChangeType.prefetch,
      changeData: {},
    );
    
    // Draw 3-4 templates
    final templates = _cfpService.selectForPrefetch(count: 4);
    
    // Batch generate (T1/T2 only, NOT T3)
    final instances = await _ewrService.batchGenerate(
      templates: templates,
      context: _getCurrentContext(),
    );
    
    // Add to buffer
    _buffer.addAll(instances);
  }
  
  /// Get next instance (from buffer if available, else generate)
  Future<L3_ContextualInstance> getNext(String templateId) async {
    // Try buffer first (> 95% hit rate target)
    final buffered = _buffer.pop(templateId);
    if (buffered != null) {
      _hitRateMonitor.recordHit();
      return buffered;
    }
    
    // Buffer miss - generate immediately (fallback to T1 if needed)
    _hitRateMonitor.recordMiss();
    final template = await _templateRepo.getTemplate(templateId);
    return _ewrService.instantiateTemplate(
      template: template,
      context: _getCurrentContext(),
    );
  }
}
```

---

## 5. Game Loop (`lib/game_loop/`)

**Purpose**: Core gameplay mechanics aligned with V3 Turn Structure.

```
lib/game_loop/
├── turn_controller.dart       # Main turn orchestration
├── hand_manager.dart           # 7-card hand management
├── time_progression.dart       # Fluid time advancement
├── state_card_manager.dart     # Passive modifier system
└── narrative_interlude.dart    # T3 latency experience
```

**`turn_controller.dart`:**
```dart
/// Main turn orchestration (V3 fluid time structure)
class TurnController {
  /// Play a card from hand
  Future<TurnResult> playCard(L3_ContextualInstance instance) async {
    // 1. Determine outcome via EWR (emergent, not formula)
    final outcome = await _ewrService.determineOutcome(
      instance: instance,
      context: _gameContext,
    );
    
    // 2. Apply effects
    await _applyEffects(outcome);
    
    // 3. Advance time based on instance duration
    _timeProgression.advance(instance.costs.time);
    
    // 4. Store in Archive
    await _archiveService.store(instance, outcome);
    
    // 5. Check for Journey Beat
    final beat = await _ewrService.detectJourneyBeat(
      instance: instance,
      npcId: outcome.npcInvolved,
      context: _gameContext,
    );
    if (beat != null) {
      await _processJourneyBeat(beat);
    }
    
    // 6. Check for evolution opportunity
    if (await _shouldCheckEvolution(instance)) {
      final assessment = await _ewrService.assessEvolution(
        templateId: instance.templateId,
        npcId: outcome.npcInvolved,
        context: _gameContext,
      );
      
      if (assessment.qualifiesForEvolution) {
        await _evolveInstance(instance, assessment);
      }
    }
    
    // 7. Trigger CFP update (incremental)
    await _cfpService.updateCFP(
      changeType: CFPChangeType.cardPlayed,
      changeData: {
        'templateId': instance.templateId,
        'outcome': outcome,
      },
    );
    
    // 8. Trigger pre-fetch if hand size <= 4
    if (_handManager.size <= 4) {
      _prefetchService.triggerPreFetch();
    }
    
    return TurnResult(outcome: outcome, beat: beat);
  }
}
```

---

## 6. Flame Game Layer (`lib/game/`)

**Purpose**: High-performance rendering, animation, and input detection for game elements (cards, effects, animations).

### Architecture Overview

```
lib/game/
├── unwritten_game.dart           # FlameGame class
├── components/
│   ├── cards/
│   │   ├── card_component.dart              # SpriteAnimationGroupComponent for cards
│   │   ├── card_hand_component.dart         # Manages 7-card fan layout
│   │   ├── draggable_card_mixin.dart        # Drag interaction behavior
│   │   └── card_animation_states.dart       # Card state enum and configs
│   ├── world/
│   │   ├── game_world.dart                  # World component
│   │   ├── background_layer.dart            # Background visuals
│   │   ├── game_board_layer.dart            # Card play zones
│   │   └── drop_zone_component.dart         # Card drop detection
│   ├── effects/
│   │   ├── card_play_effect.dart            # Particle effects for card play
│   │   ├── journey_beat_effect.dart         # Beat celebration effects
│   │   ├── particle_recipes.dart            # Reusable particle definitions
│   │   └── camera_effects.dart              # Camera shake, zoom, etc.
│   └── ui/
│       ├── debug_overlay.dart               # FPS/performance HUD
│       └── fps_counter.dart                 # Real-time FPS display
├── systems/
│   ├── input_coordinator.dart               # Coordinate input with business logic
│   ├── camera_controller.dart               # Camera management
│   ├── performance_monitor.dart             # 60 FPS tracking
│   └── asset_manager.dart                   # Sprite/animation loading
└── assets/
    ├── sprite_loader.dart                   # Load sprite sheets
    ├── animation_loader.dart                # Load animations
    └── texture_atlas_config.dart            # Texture atlas definitions
```

### UnwrittenGame Class

**`unwritten_game.dart`:**
```dart
/// Main Flame game class for Unwritten
class UnwrittenGame extends FlameGame with HasCollisionDetection {
  final WidgetRef ref;
  
  // Services injected from V3
  late final TurnController turnController;
  late final CFPService cfpService;
  late final PrefetchService prefetchService;
  
  // Flame components
  late final GameWorld world;
  late final CardHandComponent cardHand;
  
  UnwrittenGame(this.ref);
  
  @override
  Color backgroundColor() => const Color(0xFF1A1A1A);
  
  @override
  Future<void> onLoad() async {
    // Initialize services from V3 providers
    turnController = ref.read(turnControllerProvider);
    cfpService = ref.read(cfpServiceProvider);
    prefetchService = ref.read(prefetchServiceProvider);
    
    // Setup camera with fixed resolution (1920×1080 logical space)
    camera = CameraComponent.withFixedResolution(
      world: world,
      width: 1920,
      height: 1080,
    );
    
    camera.viewport = FixedResolutionViewport(
      resolution: Vector2(1920, 1080),
    );
    camera.viewfinder.anchor = Anchor.center;
    
    // Build world hierarchy
    world = GameWorld();
    await add(world);
    
    // Add component layers (priority-based z-index)
    await world.addAll([
      BackgroundLayer()..priority = -100,
      GameBoardLayer()..priority = 0,
      cardHand = CardHandComponent()..priority = 50,
    ]);
    
    AppLogger.info('UnwrittenGame initialized');
  }
  
  /// Called from Flame components when user plays a card
  Future<void> playCard(L3_ContextualInstance instance) async {
    // Trigger V3 business logic
    final result = await turnController.playCard(instance);
    
    // Trigger Flame visual effects
    _showOutcomeEffect(result);
    
    // Update Riverpod state (triggers Flutter overlay updates)
    ref.read(gameStateProvider.notifier).updateFromResult(result);
  }
  
  void _showOutcomeEffect(TurnResult result) {
    // Add particle effect to world
    world.add(
      CardPlayEffect(
        position: cardHand.position,
        outcome: result.outcome,
      ),
    );
    
    // Camera shake if dramatic
    if (result.outcome.tension > 0.7) {
      camera.viewfinder.add(
        MoveEffect.by(
          Vector2.random() * 10,
          EffectController(duration: 0.05),
        ),
      );
    }
  }
  
  @override
  void update(double dt) {
    super.update(dt);
    
    // Performance monitoring
    if (_performanceMonitor.currentFPS < 55) {
      AppLogger.performance('Low FPS', {
        'fps': _performanceMonitor.currentFPS,
        'components': world.children.length,
      });
    }
  }
}
```

### CardComponent Implementation

**`card_component.dart`:**
```dart
/// Flame component for rendering a single card
class CardComponent extends SpriteAnimationGroupComponent<CardState>
    with HasGameReference<UnwrittenGame>, TapCallbacks, DragCallbacks {
  
  final L3_ContextualInstance instance;
  Vector2? _dragStartPosition;
  int _originalPriority = 0;
  
  CardComponent({required this.instance});
  
  @override
  Future<void> onLoad() async {
    // Load sprite animations from texture atlas
    final spriteSheet = await game.images.load('cards/card_atlas.png');
    
    animations = {
      CardState.idle: await _createIdleAnimation(spriteSheet),
      CardState.hover: await _createHoverAnimation(spriteSheet),
      CardState.dragging: await _createDraggingAnimation(spriteSheet),
      CardState.playing: await _createPlayingAnimation(spriteSheet),
    };
    
    current = CardState.idle;
    
    size = Vector2(120, 168);
    anchor = Anchor.center;
    
    // Setup animation callbacks
    animationTickers?[CardState.playing]?.onComplete = _onPlayAnimationComplete;
  }
  
  // Tap handling
  @override
  void onTapDown(TapDownEvent event) {
    if (current == CardState.idle) {
      current = CardState.hover;
      add(ScaleEffect.to(
        Vector2.all(2.5),
        EffectController(duration: 0.3, curve: Curves.easeOutBack),
      ));
      priority = 100;
      
      game.audioManager.playSfx('card_hover');
      game.hapticFeedback.light();
    }
  }
  
  @override
  void onTapUp(TapUpEvent event) {
    if (current == CardState.hover) {
      // Quick tap plays card
      _playCard();
    }
  }
  
  // Drag handling
  @override
  void onDragStart(DragStartEvent event) {
    _dragStartPosition = position.clone();
    _originalPriority = priority;
    priority = 1000;
    
    current = CardState.dragging;
    
    add(ScaleEffect.to(
      Vector2.all(2.5),
      EffectController(duration: 0.2),
    ));
    
    game.audioManager.playSfx('card_pickup');
    game.hapticFeedback.medium();
  }
  
  @override
  void onDragUpdate(DragUpdateEvent event) {
    position += event.delta;
  }
  
  @override
  void onDragEnd(DragEndEvent event) {
    if (_isInValidDropZone()) {
      _playCard();
    } else {
      _returnToHand();
    }
  }
  
  void _playCard() {
    current = CardState.playing;
    
    // Trigger V3 business logic via game reference
    game.playCard(instance);
  }
  
  void _returnToHand() {
    current = CardState.idle;
    
    add(CombinedEffect([
      MoveEffect.to(
        _dragStartPosition!,
        EffectController(duration: 0.3, curve: Curves.easeOut),
      ),
      ScaleEffect.to(
        Vector2.all(1.0),
        EffectController(duration: 0.2),
      ),
    ], onComplete: () {
      priority = _originalPriority;
    }));
  }
  
  void _onPlayAnimationComplete() {
    removeFromParent();
  }
  
  bool _isInValidDropZone() {
    final dropZone = game.world.findByKey(ComponentKey.named('drop_zone'));
    return dropZone?.containsPoint(position) ?? false;
  }
}

enum CardState { idle, hover, dragging, playing }
```

### Integration with V3 Services

**Access patterns:**
```dart
// Flame component accesses V3 services via game reference
class CardComponent extends PositionComponent 
    with HasGameReference<UnwrittenGame> {
  
  void someMethod() {
    // Access injected services
    final turnController = game.turnController;
    final cfpService = game.cfpService;
    
    // Access Riverpod providers
    final gameState = game.ref.read(gameStateProvider);
  }
}
```

**State synchronization:**
```dart
// V3 state changes trigger Flame updates
class UnwrittenGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    // Listen to Riverpod state changes
    ref.listen<List<L3_ContextualInstance>>(
      handProvider,
      (previous, next) {
        _updateCardHand(next);
      },
    );
  }
  
  void _updateCardHand(List<L3_ContextualInstance> newHand) {
    // Update Flame components based on V3 state
    cardHand.updateCards(newHand);
  }
}
```

### Performance Monitoring

**`performance_monitor.dart`:**
```dart
/// Tracks FPS and frame times
class PerformanceMonitor {
  final List<double> _frameTimes = [];
  final int _maxSamples = 60;
  
  Stopwatch? _frameStopwatch;
  
  void startFrame() {
    _frameStopwatch = Stopwatch()..start();
  }
  
  void endFrame() {
    _frameStopwatch?.stop();
    final frameTime = _frameStopwatch!.elapsedMilliseconds.toDouble();
    
    _frameTimes.add(frameTime);
    if (_frameTimes.length > _maxSamples) {
      _frameTimes.removeAt(0);
    }
    
    // Log slow frames
    if (frameTime > 16.67) {
      AppLogger.performance('Slow frame', {
        'time_ms': frameTime,
        'target_ms': 16.67,
      });
    }
  }
  
  double get currentFPS => 1000 / (_frameTimes.last);
  double get averageFPS => 1000 / (_frameTimes.reduce((a, b) => a + b) / _frameTimes.length);
}
```

---

## 7. Flame-Business Logic Integration

**Purpose**: Define how Flame rendering layer communicates with V3 business logic layer.

### Integration Points

#### 1. Game Initialization

```dart
// main.dart
void main() {
  runApp(
    ProviderScope(
      child: MaterialApp(
        home: GameScreen(),
      ),
    ),
  );
}

// GameScreen
class GameScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return GameWidget<UnwrittenGame>(
      game: UnwrittenGame(ref),  // Pass WidgetRef to Flame
      overlayBuilderMap: {
        'character_state': (context, game) => CharacterStateCluster(),
        'resources': (context, game) => ResourcesCluster(),
        'relationships': (context, game) => RelationshipsCluster(),
        'timeline': (context, game) => TimelineCluster(),
      },
      initialActiveOverlays: const [
        'character_state',
        'resources',
        'relationships',
        'timeline',
      ],
    );
  }
}
```

#### 2. Card Play Flow (Flame → V3 → Flame)

```
User taps card in Flame
    ↓
CardComponent.onTapUp()
    ↓
game.playCard(instance)
    ↓
UnwrittenGame.playCard()
    ↓
turnController.playCard() [V3 BUSINESS LOGIC]
    ├─ EWR determines outcome
    ├─ Apply effects
    ├─ Update CFP
    └─ Store in archive
    ↓
Returns TurnResult
    ↓
UnwrittenGame._showOutcomeEffect() [FLAME VISUAL EFFECTS]
    ├─ Particle effects
    ├─ Camera shake
    └─ Card animation
    ↓
Update Riverpod state
    ↓
Flutter overlays rebuild automatically
```

#### 3. State Synchronization (V3 → Flame)

```dart
// UnwrittenGame listens to V3 state changes
class UnwrittenGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    // Hand updates
    ref.listen<List<L3_ContextualInstance>>(
      handProvider,
      (previous, next) => cardHand.updateCards(next),
    );
    
    // Resource changes (for visual feedback)
    ref.listen<Map<String, double>>(
      resourcesProvider,
      (previous, next) => _updateResourceVisuals(next),
    );
    
    // State cards (passive modifiers)
    ref.listen<List<StateCard>>(
      stateCardsProvider,
      (previous, next) => _updateStateCardEffects(next),
    );
  }
}
```

#### 4. Effect Triggers (V3 → Flame)

```dart
// V3 triggers Flame effects via method calls
class UnwrittenGame extends FlameGame {
  void triggerJourneyBeat(JourneyBeat beat) {
    world.add(JourneyBeatEffect(beat: beat));
    camera.viewfinder.add(
      SequenceEffect([
        ScaleEffect.to(Vector2.all(1.1), EffectController(duration: 0.2)),
        ScaleEffect.to(Vector2.all(1.0), EffectController(duration: 0.3)),
      ]),
    );
  }
  
  void triggerEvolution(L3_ContextualInstance oldCard, L3_ContextualInstance newCard) {
    world.add(CardEvolutionEffect(
      oldCard: oldCard,
      newCard: newCard,
    ));
  }
}
```

### Complete Example: Playing a Card

**1. User interaction (Flame):**
```dart
// card_component.dart
@override
void onTapUp(TapUpEvent event) {
  game.playCard(instance);  // Triggers business logic
}
```

**2. Game orchestration (Flame + V3 bridge):**
```dart
// unwritten_game.dart
Future<void> playCard(L3_ContextualInstance instance) async {
  // Call V3 business logic
  final result = await turnController.playCard(instance);
  
  // Trigger Flame effects
  _showOutcomeEffect(result);
  
  // Update Riverpod state (triggers Flutter overlay updates)
  ref.read(gameStateProvider.notifier).updateFromResult(result);
}
```

**3. Business logic (V3):**
```dart
// turn_controller.dart (from Section 5)
Future<TurnResult> playCard(L3_ContextualInstance instance) async {
  final outcome = await _ewrService.determineOutcome(instance, context);
  await _applyEffects(outcome);
  // ... (all V3 logic)
  return TurnResult(outcome: outcome);
}
```

**4. Visual effects (Flame):**
```dart
// unwritten_game.dart
void _showOutcomeEffect(TurnResult result) {
  world.add(CardPlayEffect(outcome: result.outcome));
  if (result.beat != null) {
    triggerJourneyBeat(result.beat!);
  }
}
```

**5. UI updates (Flutter overlays):**
```dart
// character_state_cluster.dart (Flutter widget)
class CharacterStateCluster extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final capacity = ref.watch(capacityProvider);
    // Rebuilds automatically when capacity changes
    return CapacityMeter(capacity: capacity);
  }
}
```

---

## 8. Presentation Layer (`lib/presentation/`)

**Purpose**: Flutter overlays and non-game screens only. Game elements (cards, animations) are rendered by Flame (Section 6).

**Key distinction:**
- **Flame (`lib/game/`)**: Cards, drag interactions, particle effects, 60 FPS animations
- **Flutter (`lib/presentation/`)**: UI clusters, menus, dialogs, low-frequency updates

```
lib/presentation/
├── overlays/                     # Flutter overlays on Flame canvas
│   ├── clusters/
│   │   ├── character_state_cluster.dart
│   │   ├── resources_cluster.dart
│   │   ├── relationships_cluster.dart
│   │   ├── timeline_cluster.dart
│   │   ├── life_meters_cluster.dart
│   │   └── progress_story_cluster.dart
│   ├── hud/
│   │   ├── phase_selector.dart
│   │   └── turn_indicator.dart
│   ├── modals/
│   │   ├── outcome_overlay.dart            # Post-action outcome
│   │   ├── journey_beat_overlay.dart       # Beat celebration
│   │   └── evolution_overlay.dart          # Card evolution notification
│   └── base_cluster_widget.dart            # Shared cluster UI
│
├── screens/                      # Non-game screens
│   ├── main_menu_screen.dart
│   ├── settings_screen.dart
│   ├── narrative_interlude_screen.dart     # T3 latency experience
│   └── season_summary_screen.dart          # Season retrospective
│
└── theme/
    ├── app_theme.dart
    ├── cluster_styles.dart
    └── narrative_typography.dart           # Literary aesthetic
```

**Important:** Flutter overlays sit on top of Flame canvas. They handle low-frequency UI updates (clusters update 1-2 times per minute) while Flame handles high-frequency game rendering (60 FPS for cards and animations).

### Key UI Components

**`character_state_cluster.dart`:**
```dart
/// Flutter overlay for character state display
class CharacterStateCluster extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final capacity = ref.watch(capacityProvider);
    final personality = ref.watch(personalityProvider);
    final stateCards = ref.watch(stateCardsProvider);
    
    return BaseClusterWidget(
      title: 'Character',
      peekFromLeft: true,
      child: Column(
        children: [
          // ENGINE_CAPACITY display
          CapacityMeter(capacity: capacity),
          
          SizedBox(height: 8),
          
          // ENGINE_PERSONALITY display
          PersonalityIndicator(personality: personality),
          
          SizedBox(height: 12),
          
          // Active state cards
          ...stateCards.map((card) => StateCardWidget(card: card)),
        ],
      ),
    );
  }
}
```

**`resources_cluster.dart`:**
```dart
/// Flutter overlay for resource tracking
class ResourcesCluster extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final resources = ref.watch(resourcesProvider);
    
    return BaseClusterWidget(
      title: 'Resources',
      peekFromLeft: false,
      child: Column(
        children: resources.entries.map((entry) {
          return ResourceDisplay(
            name: entry.key,
            value: entry.value,
          );
        }).toList(),
      ),
    );
  }
}
```

**`narrative_interlude_screen.dart`:**
```dart
/// T3 latency transformed into thematic pause
class NarrativeInterludeScreen extends StatelessWidget {
  final String reflectiveText;
  final Stream<double> progressStream;
  
  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.black.withOpacity(0.9),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // Memory web animation
          MemoryWebAnimation(progress: progressStream),
          
          SizedBox(height: 48),
          
          // Reflective text
          Text(
            reflectiveText,
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
              fontFamily: 'Lora', // Serif for literary feel
              color: Colors.white70,
            ),
            textAlign: TextAlign.center,
          ),
          
          SizedBox(height: 32),
          
          // Subtle progress indicator (NOT a loading bar)
          StreamBuilder<double>(
            stream: progressStream,
            builder: (context, snapshot) {
              return Opacity(
                opacity: 0.3,
                child: LinearProgressIndicator(
                  value: snapshot.data ?? 0.0,
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}
```

---

## 9. Migration Plan

### Step 1: Backup & Branch
```bash
git checkout -b v3-restructure
# Keep lib/features/ as reference, don't delete yet
```

### Step 2: Build Core Engines (Foundation)
1. Implement `lib/core/engine/` (4 engines)
2. Write tests for each engine
3. Ensure ENGINE_WRITERS_ROOM stub works before full EWR API

### Step 3: Build Data Layer
1. Define models (`l2_master_template`, `l3_contextual_instance`, `game_context`)
2. Implement repositories (interfaces + implementations)
3. Set up Firebase/Supabase connections

### Step 4: Build Services
1. Implement `ewr_service.dart` (start with T1 only, T2/T3 stubs)
2. Implement `cfp_service.dart`
3. Implement `memory_service.dart`
4. Implement `prefetch_service.dart`

### Step 5: Build Flame Game Layer
1. Implement `unwritten_game.dart` (FlameGame class with WidgetRef injection)
2. Implement `card_component.dart` (SpriteAnimationGroupComponent)
3. Implement `card_hand_component.dart` (7-card fan layout)
4. Build world structure (BackgroundLayer, GameBoardLayer, CardHandLayer)
5. Wire up input handling (TapCallbacks, DragCallbacks)
6. Test 60 FPS performance with performance monitor

### Step 6: Build Game Loop & Integration
1. Implement `turn_controller.dart`
2. Implement `hand_manager.dart`
3. Wire up services
4. Integrate Flame components with V3 business logic
5. Test card play flow (Flame → V3 → Flame)

### Step 7: Build Flutter Overlays
1. Implement cluster widgets (character state, resources, relationships, timeline)
2. Implement `base_cluster_widget.dart` (peek-from-edges pattern)
3. Build GameWidget with overlay system
4. Wire up Riverpod state to overlays
5. Test responsive design (mobile peek, tablet/desktop full layout)

### Step 8: Enable T2/T3 EWR
1. Implement actual EWR API calls
2. Add quality validation
3. Tune pre-fetch strategy
4. Implement narrative interlude screen (T3 latency masking)

### Step 9: Polish & Optimize
1. Component pooling for cards
2. Sprite batching optimization
3. Performance profiling (target 60 FPS)
4. Battery usage testing

### Step 10: Delete Old Code
Once V3 + Flame is working:
```bash
# Delete entire V1.2 codebase
rm -rf lib/features/
```

---

## 10. Performance Targets

### Flame Layer (Critical)
- **60 FPS** stable during all animations and interactions
- **< 16ms** frame time (16.67ms = 60 FPS budget)
- **< 200MB** memory usage during gameplay
- **Component pooling** for frequently created/destroyed cards
- **Sprite batching** for efficient rendering (single texture atlas)
- **Off-screen culling** to skip rendering invisible components
- **No frame drops** during card drag interactions

### V3 Services (Business Logic)
- **< 10ms** CFP incremental updates (10-60 templates affected)
- **> 95%** prefetch buffer hit rate (minimize waiting)
- **< 100ms** T1 local generation (template fill)
- **< 2s** T2 EWR light generation
- **< 10s** T3 EWR heavy generation (masked by narrative interlude)

### Overall System
- **< 10%** battery drain per 30min gameplay session
- **< 50MB** app size (excluding assets)
- **Smooth state transitions** between game phases
- **No memory leaks** (proper component disposal)
- **Responsive UI** (Flutter overlays rebuild < 5ms)

### Monitoring & Validation
- **PerformanceMonitor** tracks FPS in real-time
- **Log slow frames** (> 16.67ms) with component count
- **Prefetch hit rate** logged per buffer refill
- **CFP update time** logged per incremental update
- **Memory warnings** trigger optimization (reduce particles, cull off-screen)

---

## 11. Key Differences from V1.2

### V1.2 (Deprecated)
```
lib/features/
├── ai/                            # Task-specific AI
│   ├── npc_response_calculator.dart  ❌ Deterministic formula
│   └── firebase_ai_service.dart      ❌ Specialized methods
├── cards/                         # Static cards
│   └── card_widget.dart           ❌ Flutter widgets for cards
├── game_state/                    # Mixed concerns
└── ...
```

**V1.2 Issues:**
- ❌ No game engine (just Flutter widgets)
- ❌ Can't achieve 60 FPS for card animations
- ❌ Deterministic AI formulas
- ❌ Static card deck
- ❌ Mixed concerns (UI + business logic)

### V3 (New)
```
lib/
├── core/engine/                   # Core Simulation Engines
│   ├── engine_personality.dart    ✅ OCEAN perceptual filtering
│   ├── engine_capacity.dart       ✅ Emotional bandwidth
│   ├── engine_memory.dart         ✅ Archive/Vector/Graph DB
│   └── engine_writers_room.dart   ✅ AI orchestrator
│
├── game/                          # Flame rendering layer
│   ├── unwritten_game.dart        ✅ FlameGame with 60 FPS
│   ├── components/cards/          ✅ SpriteAnimationGroupComponent
│   ├── components/effects/        ✅ Particle effects
│   └── systems/                   ✅ Performance monitoring
│
├── services/
│   ├── ewr/ewr_service.dart       ✅ Unified instantiation
│   ├── cfp/cfp_service.dart       ✅ Probability management
│   └── memory/archive_service.dart ✅ Semantic search
│
├── presentation/                  # Flutter overlays only
│   ├── overlays/clusters/         ✅ UI clusters
│   └── screens/                   ✅ Menu screens
│
└── data/models/
    ├── l2_master_template.dart    ✅ Template JSON → Dart
    └── l3_contextual_instance.dart ✅ Generated cards
```

**V3 Improvements:**
- ✅ Flame engine for game rendering (60 FPS)
- ✅ Flutter overlays for UI (hybrid approach)
- ✅ Clean architecture (separation of concerns)
- ✅ Emergent AI via ENGINE_WRITERS_ROOM
- ✅ Dynamic card generation from CFP
- ✅ Performance targets enforced

---

## 12. Critical Success Factors

**1. Core Engines First**
- Cannot build anything without ENGINE_PERSONALITY, ENGINE_CAPACITY, ENGINE_MEMORY, ENGINE_WRITERS_ROOM
- These are the foundation

**2. Flame Layer Integration**
- Must achieve 60 FPS with performance monitoring
- Component pooling and sprite batching required
- Test on real devices early

**3. Stub EWR Early**
- Start with simple T1 (local template fill)
- Proves architecture works before complex AI

**4. CFP Incremental Updates**
- Performance critical path
- Test with 300 templates to ensure < 10ms updates

**5. Pre-Fetch Strategy**
- Target > 95% buffer hit rate
- Monitor and tune based on real usage

**6. Quality Gates**
- All T2/T3 generations must pass quality validation
- Narrative Quality Score ≥ 0.7
- Fallback to T1 if repeated failures

**7. Hybrid UI Approach**
- Flame for cards (60 FPS)
- Flutter overlays for clusters (low-frequency updates)
- Clear separation of concerns

---

## 13. Estimated Timeline

**Week 1-2:** Core Engines + Data Models  
**Week 3-4:** Services Layer (EWR stub, CFP, Memory)  
**Week 5:** Flame Game Layer (UnwrittenGame, CardComponent, performance monitoring)  
**Week 6:** Game Loop + Flame Integration (TurnController, Flame ↔ V3 bridge)  
**Week 7:** Flutter Overlays (clusters, responsive design, GameWidget setup)  
**Week 8:** Full EWR Integration (T2/T3)  
**Week 9-10:** Polish + Migration (optimization, testing, cleanup)

**Total:** ~10 weeks for complete V3 + Flame restructure

**Alternative (incremental patching):** 6+ months of painful patching

---

## 14. Why Flame + Flutter Hybrid?

### Flame for Game Elements

**Why use Flame for cards:**
- ✅ **60 FPS animations** - SpriteAnimationGroupComponent with GPU acceleration
- ✅ **Smooth drag interactions** - Direct position manipulation every frame
- ✅ **Particle effects** - GPU-accelerated visual feedback
- ✅ **Component lifecycle** - onLoad, onMount, onRemove for resource management
- ✅ **Performance optimizations** - Component pooling, sprite batching, culling

**Card requirements demand Flame:**
- Idle animations (8 frames looping)
- Hover scale effects (< 200ms transitions)
- Drag tracking (60 times per second)
- Play animations with particle effects
- Camera shake on dramatic moments

### Flutter for UI Clusters

**Why use Flutter for clusters:**
- ✅ **Complex layouts** - ListView, Column, Row, Stack built-in
- ✅ **Low update frequency** - Clusters update 1-2 times per minute, not 60 times per second
- ✅ **Accessibility** - Screen reader support, text scaling, high contrast
- ✅ **Rich text** - Multi-style text, wrapping, alignment
- ✅ **Rapid development** - Material widgets, hot reload, DevTools

**Cluster requirements suit Flutter:**
- Scrollable lists (relationships, timeline)
- Progress bars (capacity, resources)
- Text-heavy content (event descriptions)
- Forms and inputs (rare, but needed for settings)

### Standard Pattern

**GameWidget overlay system exists for this:**
```dart
GameWidget<UnwrittenGame>(
  game: game,
  overlayBuilderMap: {
    'character_state': (context, game) => CharacterStateCluster(),
    'resources': (context, game) => ResourcesCluster(),
  },
)
```

**Production Flame games use this:**
- **Bonfire**: Flame canvas + Flutter HUD
- **Flame examples**: Hybrid approach throughout
- **Casual games**: Standard industry pattern

**Best tool for each job:**
- Flame excels at game rendering
- Flutter excels at UI layouts
- Use both, integrated via Riverpod

---

## Conclusion

This V3 + Flame architecture is:
- ✅ Aligned with Master Truths v3.0
- ✅ Clean separation of concerns (Flame for game, Flutter for UI, V3 for logic)
- ✅ Testable (engines isolated, services injectable)
- ✅ Performant (60 FPS game, < 10ms CFP updates, pre-fetch optimization)
- ✅ Maintainable (clear structure, single responsibility)
- ✅ Scalable (300+ templates, infinite instances)
- ✅ Hybrid approach (Flame + Flutter = best of both worlds)

**The old codebase cannot be saved. Clean slate is the only efficient path forward.**

**Recommend:** Approve architecture, start Week 1 (Core Engines), implement Flame layer Week 5, delete `lib/features/` when V3 + Flame working.

