# Unwritten Architecture Overview

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete

---

## Overview

Unwritten adopts a production-proven architecture based on [Google's I/O FLIP](https://github.com/flutter/io_flip), combining Flutter for cross-platform UI, Flame for 60 FPS game mechanics, Dart Frog for backend services, and Firebase for cloud infrastructure.

**Core Principle:** Build with proven patterns from day one, not "simple now, refactor later."

---

## Why I/O FLIP Patterns?

### Proven at Scale

**I/O FLIP** (Google I/O 2023):
- Built by Very Good Ventures for Google
- Handled **thousands of concurrent players**
- Real-time multiplayer card game
- Production-tested architecture
- Open source reference implementation

**What We Adopt:**
- Flutter + Flame game engine
- Dart Frog backend (full-stack Dart)
- Firebase ecosystem (Firestore, Auth, Storage)
- Shared packages (game logic used by client + server)
- Backend-authoritative model
- BLoC/Riverpod state management patterns

**What We Adapt:**
- Single-player focus (vs multiplayer)
- On-device AI (vs cloud-only)
- Narrative-driven (vs competitive)
- Riverpod 3.x (vs Riverpod 2.x)

---

## Technology Stack

### Frontend (Flutter + Flame)

| Technology | Version | Purpose |
|------------|---------|---------|
| **Flutter** | 3.27+ | Cross-platform UI framework |
| **Dart** | 3.5+ | Programming language |
| **Flame** | 1.20+ | Game engine (REQUIRED from day 1) |
| **Riverpod** | 3.0+ | State management |
| **Hive** | 2.2+ | Local storage |
| **audioplayers** | 6.1+ | Audio playback |
| **vibration** | 2.0+ | Haptic feedback |

### Backend (Dart Frog + Firebase)

| Technology | Version | Purpose |
|------------|---------|---------|
| **Dart Frog** | Latest | Backend framework |
| **Firebase Firestore** | Latest | Database (NoSQL) |
| **Firebase Auth** | Latest | Authentication |
| **Firebase Storage** | Latest | Asset storage |
| **Cloud Run** | Latest | Auto-scaling hosting |
| **OpenAI/Anthropic** | Latest | Cloud AI (Phase 1-4) |

### Shared Packages

| Package | Purpose | Used By |
|---------|---------|---------|
| **game_logic** | Core game mechanics | Client + Server |
| **data_models** | Card, GameState, Relationship | Client + Server |
| **calculators** | Relationship, success formulas | Client + Server |

### Future (Phase 5+)

| Technology | Version | Purpose |
|------------|---------|---------|
| **TensorFlow Lite** | 2.x | On-device AI |
| **Custom Shaders** | GLSL | Advanced visual effects |
| **Forge2D** | Latest | Advanced physics (optional) |

---

## Architecture Principles

### 1. Flame from Day 1 (Non-Negotiable)

**Decision:** Use Flame game engine from the start, not "Flutter first, Flame later."

**Rationale:**
- **Code structure fundamentally different**: Widget tree vs Component tree
- **Migration cost prohibitive**: 2-3 weeks to rewrite everything
- **Different paradigms**: `build()` vs `update(dt)` + `render()`
- **I/O FLIP validation**: Proven at scale with Flame from start
- **Performance guaranteed**: 60 FPS stable, not "hope for best"

**What Would Need Rewriting:**
- ❌ All rendering (Widget → Component)
- ❌ All input handling (GestureDetector → DragCallbacks)
- ❌ All animations (AnimationController → EffectController)
- ❌ All physics (manual → Flame physics)
- ❌ Game loop structure (setState → update/render)

**Conclusion:** Starting with Flame saves 2-3 weeks and avoids technical debt.

**See:** `56-card-physics-animations.md` for detailed physics implementation

### 2. Clean Architecture (Mandatory)

```
lib/
├── core/              # Shared utilities, constants, config
├── features/          # Feature modules (cards, game, ai)
│   └── [feature]/
│       ├── data/      # Models, repositories
│       ├── domain/    # Business logic, use cases
│       └── presentation/
│           ├── components/  # Flame components
│           ├── widgets/     # Flutter widgets
│           └── providers/   # Riverpod state
└── shared/            # Shared services, widgets
```

**Benefits:**
- Clear separation of concerns
- Testable business logic
- Independent layers
- Scalable to large teams

**See:** `51-project-structure-guide.md` for complete structure

### 3. Backend-Authoritative Model

**Decision:** Server validates all critical operations.

**Client Responsibilities:**
- Optimistic UI updates (instant feedback)
- Local game state management
- Rendering and input handling

**Server Responsibilities:**
- Validate card plays (prevent cheating)
- Generate AI content (narrative, dialogue)
- Store training data (for future local models)
- Manage relationships and progression

**Benefits:**
- Prevent cheating
- Centralized training data collection
- Server-side AI generation
- Consistent game state

**Flow:**
```
User plays card → Client updates optimistically → Server validates → 
Server applies effects → Server returns authoritative state → 
Client reconciles (or rolls back)
```

### 4. Shared Game Logic

**Decision:** Core game logic shared between client and server.

**Implementation:**
```dart
// packages/game_logic/lib/src/calculators/relationship_calculator.dart
class RelationshipCalculator {
  RelationshipImpact calculate({
    required PersonalityProfile personality,
    required double emotionalCapacity,
    required double currentTrust,
    required UrgencyLevel urgency,
    required String playerAction,
  }) {
    // Formula from Master Truths v1.2
    final baseImpact = _calculateBase(personality, playerAction);
    final urgencyMultiplier = _getUrgencyMultiplier(urgency); // 1x-5x
    final trustModifier = _getTrustModifier(currentTrust); // 0.5x-2x
    final capacityConstraint = emotionalCapacity; // 0-10
    
    return RelationshipImpact(
      trustDelta: (baseImpact * urgencyMultiplier * trustModifier)
          .clamp(0, capacityConstraint),
    );
  }
}
```

**Benefits:**
- Single source of truth
- Client can predict outcome (optimistic UI)
- Server uses same logic (authoritative)
- Guaranteed consistency

### 5. Hybrid UI Architecture

**Decision:** Flame for game world, Flutter for UI overlays.

**Implementation:**
```dart
Scaffold(
  body: Stack(
    children: [
      // Flame game world (cards, animations, physics)
      GameWidget<UnwrittenGame>(
        game: UnwrittenGame(),
      ),
      
      // Flutter UI overlays (dialogs, HUD, menus)
      Positioned(
        top: 16,
        child: ResourcesBar(), // Flutter widget
      ),
      
      Positioned(
        bottom: 0,
        child: NarrativePanel(), // Flutter widget
      ),
    ],
  ),
)
```

**Benefits:**
- Flame handles game mechanics (60 FPS)
- Flutter handles UI (Material Design)
- Best of both worlds
- Easier development

---

## Performance Targets

### Primary Metrics (Must Achieve)

| Metric | Target | Why |
|--------|--------|-----|
| **Frame Rate** | 60 FPS stable | Smooth gameplay feel |
| **Frame Time** | < 16ms | 60 FPS = 16.67ms budget |
| **Memory Usage** | < 200MB | Mobile device constraints |
| **App Size** | < 50MB | Download/storage limits |
| **Battery Drain** | < 10% per 30min | User retention |

### Secondary Metrics (Nice to Have)

| Metric | Target | Why |
|--------|--------|-----|
| **Cold Start** | < 3s | First impression |
| **Hot Reload** | < 1s | Developer experience |
| **AI Inference** | < 15ms | Future on-device AI |
| **Network Latency** | < 100ms | Cloud AI feels instant |

### How We Achieve These

**60 FPS:**
- Flame game engine (optimized game loop)
- Sprite atlases (reduce draw calls)
- Component pooling (reduce allocations)
- Fixed timestep physics

**< 16ms Frame Time:**
- Efficient rendering (batching)
- Minimal rebuilds (const constructors)
- Optimistic UI (don't wait for server)

**< 200MB Memory:**
- Asset streaming (not all in memory)
- Card caching (LRU)
- Proper disposal (no leaks)

**< 50MB App Size:**
- Tree shaking (remove unused code)
- Asset compression (smaller images)
- Code minification

**< 10% Battery:**
- Reduce AI frequency (when on battery)
- Cache AI responses
- Efficient rendering
- Sleep inactive components

**See:** `59-performance-optimization-flame.md` for optimization techniques

---

## I/O FLIP vs Unwritten Comparison

### Similarities (What We Keep)

| Feature | I/O FLIP | Unwritten | Notes |
|---------|----------|----------|-------|
| **Frontend** | Flutter + Flame | Flutter + Flame | ✅ Same |
| **Backend** | Dart Frog | Dart Frog | ✅ Same |
| **Database** | Firestore | Firestore | ✅ Same |
| **Auth** | Firebase Auth | Firebase Auth | ✅ Same |
| **Hosting** | Cloud Run | Cloud Run | ✅ Same |
| **Shared Logic** | Match Solver package | Game Logic package | ✅ Same pattern |
| **Architecture** | Feature-first | Feature-first | ✅ Same |

### Differences (What We Adapt)

| Feature | I/O FLIP | Unwritten | Reason |
|---------|----------|----------|--------|
| **Game Type** | Multiplayer PvP | Single-player narrative | Different genre |
| **AI** | Vertex AI (cloud) | OpenAI → TensorFlow Lite | Cost + privacy |
| **State** | Riverpod 2.x | Riverpod 3.x | Latest version |
| **Complexity** | Match logic | Full life simulation | More complex |
| **Focus** | Quick matches | Long sessions (seasons) | Different pacing |
| **WebSocket** | Real-time battles | Not needed (single-player) | Simpler |

### Key Takeaway

**Keep the architecture, adapt the content.**

We use I/O FLIP's proven patterns but apply them to our narrative card game instead of competitive battles.

---

## Architecture Decision Record

### ADR-001: Why Flame from Day 1?

**Decision:** Use Flame game engine from project start.

**Status:** ✅ Approved

**Context:**
- Need 60 FPS smooth animations
- Want "Unity-like game feel" (per spec)
- I/O FLIP uses Flame successfully

**Options Considered:**
1. **Pure Flutter widgets** → Migrate to Flame later
2. **Flame from start** → Never need migration
3. **Custom game engine** → Too much work

**Decision:** Option 2 (Flame from start)

**Consequences:**
- ✅ PRO: No migration needed (saves 2-3 weeks)
- ✅ PRO: 60 FPS guaranteed
- ✅ PRO: Proven at scale (I/O FLIP)
- ⚠️ CON: Steeper learning curve initially
- ⚠️ CON: More complex setup

**Mitigation:**
- Use I/O FLIP as reference implementation
- Document patterns clearly
- Provide examples

**See:** Discussion in `CARD-DRAG-PHYSICS-GUIDE.md` (archived)

### ADR-002: Why Riverpod 3.x Over Riverpod 2.x?

**Decision:** Use Riverpod 3.x (latest) instead of 2.x like I/O FLIP.

**Status:** ✅ Approved

**Context:**
- I/O FLIP uses Riverpod 2.x
- Riverpod 3.x released with improvements
- flame_riverpod requires 2.x (incompatible)

**Decision:** Use Riverpod 3.x, integrate Flame manually

**Consequences:**
- ✅ PRO: Latest features and improvements
- ✅ PRO: Future-proof
- ⚠️ CON: Can't use flame_riverpod package
- ⚠️ CON: Manual integration needed

**Implementation:**
```dart
// Manual integration (simple)
class GameView extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(gameStateProvider);
    return GameWidget(game: UnwrittenGame(state: state));
  }
}
```

**See:** `53-state-management-architecture.md` for patterns

### ADR-003: Why Backend-Authoritative?

**Decision:** Server validates all card plays and generates AI.

**Status:** ✅ Approved

**Context:**
- Single-player game (could be client-only)
- Need training data collection
- Want to prevent cheating

**Decision:** Backend-authoritative with optimistic UI

**Consequences:**
- ✅ PRO: Collect training data (for future local AI)
- ✅ PRO: Prevent cheating/tampering
- ✅ PRO: Centralized AI generation
- ⚠️ CON: Requires internet connection
- ⚠️ CON: More complex architecture

**Mitigation:**
- Optimistic UI (feels instant)
- Graceful offline mode (cached content)
- Local fallback for basic mechanics

**See:** `54-build-configuration-deployment.md` for deployment

### ADR-004: Why Dart Frog Over Express/Nest?

**Decision:** Use Dart Frog for backend instead of Node.js frameworks.

**Status:** ✅ Approved

**Context:**
- I/O FLIP uses Dart Frog successfully
- Could use Express.js, NestJS, etc.
- Team knows Dart from Flutter

**Decision:** Dart Frog (full-stack Dart)

**Consequences:**
- ✅ PRO: Same language as frontend (Dart)
- ✅ PRO: Share code (game logic package)
- ✅ PRO: Type safety across stack
- ✅ PRO: Proven at scale (I/O FLIP)
- ⚠️ CON: Smaller ecosystem than Node.js
- ⚠️ CON: Fewer developers know Dart

**Mitigation:**
- Dart easy to learn for TypeScript devs
- I/O FLIP provides examples
- Growing ecosystem

---

## Related Documentation

### Within This Folder (5.architecture/)
- **51-project-structure-guide.md** - Complete folder structure
- **52-development-environment-setup.md** - Setup instructions
- **53-state-management-architecture.md** - Riverpod patterns
- **54-build-configuration-deployment.md** - Build and deploy
- **55-flame-engine-fundamentals.md** - Flame basics
- **56-card-physics-animations.md** - I/O FLIP physics
- **60-package-integration-overview.md** - All packages

### Other Folders
- **docs/master_truths_canonical_spec_v_1_2.md** - Canonical rules
- **docs/1.concept/** - Design philosophy
- **docs/2.gameplay/** - Implementation specs
- **docs/3.ai/** - AI architecture
- **docs/CANONICAL-DECISIONS-LOG.md** - All decisions

### External References
- **I/O FLIP GitHub:** https://github.com/flutter/io_flip
- **I/O FLIP Blog:** https://flutter.dev/flip
- **Flame Docs:** https://docs.flame-engine.org/
- **Riverpod Docs:** https://riverpod.dev/

---

## Next Steps

### For New Developers
1. Read this document (you're here!)
2. Read `51-project-structure-guide.md`
3. Follow `52-development-environment-setup.md`
4. Study `55-flame-engine-fundamentals.md`
5. Review `56-card-physics-animations.md`

### For Integration Work
1. Read `60-package-integration-overview.md`
2. Pick specific integration guide (61-66)
3. Follow implementation examples
4. Test thoroughly

### For Testing
1. Read `67-testing-strategy.md`
2. Set up test environment
3. Write tests following patterns
4. Monitor with `68-performance-monitoring.md`

---

## Success Criteria

This architecture is successful when:

- ✅ Maintains 60 FPS during gameplay
- ✅ Feels like "Unity game" per spec
- ✅ Scales to thousands of users
- ✅ New developers onboard quickly
- ✅ Easy to add features
- ✅ Training data collected automatically
- ✅ Works offline (gracefully)
- ✅ Runs on mid-range devices

---

**Status:** ✅ Architecture Complete  
**Next:** Implement following this plan  
**Reference:** I/O FLIP for proven patterns

