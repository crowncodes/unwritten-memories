# Flutter App Comprehensive Audit & Restructuring Plan
**Date:** October 16, 2025  
**Purpose:** Full audit of current state + complete implementation roadmap  
**Goal:** Production-ready gameplay with proper auth, state, and content management

---

## Executive Summary

### Current State: Foundation Phase ✅
**What Works:**
- Clean Architecture foundation (core, features, shared)
- Firebase infrastructure (Firestore, Auth, Storage, Analytics, Functions)
- Basic Riverpod state management (GameStateNotifier)
- Flame game engine integration for card rendering
- UI cluster system with expandable sections
- Music system with MSV-based stem matching
- TensorFlow Lite scaffolding for AI
- Story generation flows in Cloud Functions

### Critical Gaps: 🚨
1. **NO PROPER AUTHENTICATION** - Anonymous only, no user accounts
2. **NO CONTENT MANAGEMENT** - Cards hardcoded, no dynamic loading
3. **NO GAME FLOW** - Missing season start, aspiration selection, progression
4. **INCOMPLETE STATE MANAGEMENT** - No persistence, no sync with Firestore
5. **NO CARD EVOLUTION** - Base cards exist but no evolution system
6. **NO NPC SYSTEM** - Relationships tracked but no NPC entities
7. **NO NARRATIVE ENGINE** - Dialogue generation exists but not integrated
8. **NO SAVE/LOAD** - Game state lives in memory only

---

## Part 1: Current Architecture Audit

### 1.1 Authentication & User Management

**Current:**
```dart
// main.dart:27-28
await FirebaseService.signInAnonymously(); // ❌ TEMPORARY
```

**Problems:**
- Anonymous auth only
- No user profiles
- No data ownership
- No monetization path
- No multi-device sync

**Required:**
- Email/password authentication
- Social auth (Google, Apple)
- User profile creation
- Onboarding flow
- Account recovery
- Data migration from anonymous → authenticated

### 1.2 State Management Assessment

**Current State Architecture:**
```
GameStateModel (data/models/game_state_model.dart)
├── playerId: String
├── currentWeek/Day/Phase: temporal tracking
├── resources: ResourcesModel (energy, money, time)
├── lifeMeters: LifeMetersModel (physical, mental, social, emotional)
├── emotionalCapacity: EmotionalCapacity
├── relationships: Map<String, RelationshipModel>
├── deckCardIds/handCardIds: List<String>
├── lastNarrative: String?
├── currentLocation: String
└── completedEventIds: List<String>

GameStateNotifier (presentation/providers/game_state_providers.dart)
├── advancePhase() - time progression
├── consumeTime() - phase time management
├── drawCard() - deck → hand
├── canPlayCard() - resource validation
└── deductCosts() - resource consumption
```

**What's Missing:**
- ❌ No Firestore persistence
- ❌ No save/load system
- ❌ No cloud backup
- ❌ No autosave
- ❌ No state versioning
- ❌ No migration strategy
- ❌ No undo/redo
- ❌ No conflict resolution
- ❌ No offline support

### 1.3 Content Management

**Current:**
```dart
// CardRepositoryImpl loads from static JSON
static const String _cardsAssetPath = 'assets/data/base_cards.json';
```

**Problems:**
- ❌ Cards are static assets (cannot update without app release)
- ❌ No dynamic card generation
- ❌ No card evolution tracking per user
- ❌ No personalized card variants
- ❌ No A/B testing capability
- ❌ No content versioning
- ❌ No hot-reload for balance changes

**Required Architecture:**
```
Content Management Layer
├── Static Base Cards (Firestore collection: base_cards)
├── User-Evolved Cards (Firestore: users/{uid}/evolved_cards)
├── NPC Definitions (Firestore: base_npcs)
├── User NPCs (Firestore: users/{uid}/npcs)
├── Event Templates (Firestore: event_templates)
├── Location Data (Firestore: locations)
└── Aspiration Cards (Firestore: aspiration_catalog)
```

### 1.4 Game Flow & Progression

**Currently Missing:**
1. New game setup flow
2. Aspiration selection screen
3. Initial story generation (buildSeasonStory flow exists but not called)
4. Week/day progression system
5. Event scheduling and triggering
6. Decisive decision windows
7. Season conclusion
8. Season-to-season transitions
9. Character retirement
10. Life bookshelf

**Core Loop Not Implemented:**
```
❌ Choose Aspiration
❌ Generate Starting World (Story Flow)
❌ Build Initial Deck
❌ Tutorial / First Week
❌ Daily Loop (draw cards, play cards, advance time)
❌ Event System (tension hooks, mysteries, stakes)
❌ Decisive Decisions (3-act structure)
❌ Week Transitions
❌ Season Climax & Resolution
❌ Next Season Setup / Character Retirement
```

### 1.5 Card System Analysis

**Current:**
```dart
class CardModel extends Equatable {
  final String id;
  final String name;
  final String description;
  final CardType type;
  final Map<String, double> costs;
  final Map<String, double> effects;
  final int evolutionLevel; // ✅ Exists
  final int playCount; // ✅ Tracked
  final DateTime? lastPlayed;
  final List<String> tags;
  final Map<String, dynamic>? metadata;
}
```

**What Works:**
- ✅ Base card data structure
- ✅ Evolution level tracking
- ✅ Play count tracking
- ✅ Cost/effect system
- ✅ Card type enum

**What's Missing:**
- ❌ Evolution trigger system
- ❌ Memory attachment (cards ← memories)
- ❌ Fusion system implementation
- ❌ Personalized flavor text
- ❌ Emotional capacity requirements (Master Truths v1.2)
- ❌ Memory resonance tracking
- ❌ Tension injection metadata
- ❌ Success chance calculation

### 1.6 NPC & Relationship System

**Current:**
```dart
class RelationshipModel extends Equatable {
  final String npcId;
  final int level; // 1-5
  final double trust; // 0-100
  final List<String> sharedMemories;
  final Map<String, double> emotionalBonds;
}
```

**What Works:**
- ✅ Basic relationship tracking
- ✅ Trust/level system
- ✅ Shared memories list

**Critical Missing:**
- ❌ No NPC entity model
- ❌ No NPC OCEAN personality
- ❌ No NPC backstory
- ❌ No NPC goals/motivations
- ❌ No dynamic dialogue generation integration
- ❌ No relationship evolution triggers
- ❌ No NPC-driven events
- ❌ No support/conflict mechanics

### 1.7 AI Integration Status

**What Exists:**
- ✅ Cloud Functions for dialogue generation (generateDialogue)
- ✅ Cloud Functions for location image (generateLocationImageWithImagen)
- ✅ Cloud Functions for music (generateMusicStems, generateMusicWithLyria)
- ✅ Cloud Functions for story crafting (buildSeasonStory)
- ✅ StoryRepository in Flutter (created today)
- ✅ FirebaseImageGenerationService (rerouted to cloud function)

**What's Not Integrated:**
- ❌ Dialogue generation not called during gameplay
- ❌ Story crafting not triggered on new game
- ❌ Music generation not triggered by emotional context
- ❌ Image generation called manually, not automated
- ❌ No AI request queue for concurrency management
- ❌ No caching layer for AI responses
- ❌ No fallback for AI failures
- ❌ No premium tier gating (thinking mode)

### 1.8 Data Persistence Strategy

**Current Reality:**
```dart
// GameStateModel has toJson/fromJson ✅
// But NEVER saved to Firestore ❌
// Lives only in memory ❌
```

**Required Firestore Structure:**
```
users/
  {uid}/
    profile/
      - display_name
      - created_at
      - premium_tier
    
    characters/
      {character_id}/
        - name
        - created_at
        - current_season
        - seasons_completed
        
        seasons/
          {season_id}/
            - aspiration_id
            - start_date
            - end_date
            - story_plan (StoryOutput)
            - game_state (GameStateModel snapshots)
            
            evolved_cards/
              {card_id}/
                - base_card_id
                - evolution_level
                - custom_description
                - memories[]
                - play_count
            
            npcs/
              {npc_id}/
                - base_npc_id
                - relationship_level
                - trust
                - personality (OCEAN)
                - shared_memories[]
            
            events/
              {event_id}/
                - type
                - week
                - resolved
            
            memories/
              {memory_id}/
                - week
                - cards_involved
                - emotional_weight
                - text
```

---

## Part 2: Implementation Roadmap

### Phase 1: Authentication & User Foundation (Week 1-2)

**Priority: CRITICAL** 🚨

#### 1.1 Remove Anonymous Auth
- [ ] Create auth onboarding screens
  - [ ] Welcome/splash screen
  - [ ] Sign in screen (email/password)
  - [ ] Sign up screen with validation
  - [ ] Password reset flow
  - [ ] Social auth buttons (Google, Apple - optional for later)

#### 1.2 User Profile System
- [ ] Create UserProfile model
  ```dart
  class UserProfile {
    final String uid;
    final String displayName;
    final String? email;
    final DateTime createdAt;
    final PremiumTier tier;
    final Map<String, dynamic> preferences;
  }
  ```
- [ ] Create UserProfileRepository
- [ ] Implement profile CRUD operations
- [ ] Add Riverpod provider for current user

#### 1.3 Auth State Management
- [ ] Create AuthNotifier (Riverpod)
- [ ] Listen to auth state changes
- [ ] Implement sign in/out flows
- [ ] Add loading states
- [ ] Handle auth errors gracefully

#### 1.4 Routing & Guards
- [ ] Implement auth guards for protected routes
- [ ] Redirect unauthenticated users to sign in
- [ ] Add "Continue as Guest" for later (anonymous → real account migration)

**Deliverable:** Proper authentication with real user accounts

---

### Phase 2: State Persistence & Save System (Week 2-3)

**Priority: CRITICAL** 🚨

#### 2.1 Firestore Schema Implementation
- [ ] Create Firestore security rules
  ```
  match /users/{userId} {
    allow read, write: if request.auth.uid == userId;
    
    match /characters/{characterId} {
      allow read, write: if request.auth.uid == userId;
    }
  }
  ```
- [ ] Create compound indexes for queries
- [ ] Document schema in code comments

#### 2.2 Character System
- [ ] Create Character model
  ```dart
  class Character {
    final String id;
    final String userId;
    final String name;
    final int currentSeason;
    final List<String> completedSeasonIds;
    final DateTime createdAt;
    final DateTime lastPlayedAt;
  }
  ```
- [ ] Create CharacterRepository
- [ ] Implement CRUD operations
- [ ] Add character selection screen
- [ ] Support multiple characters per user

#### 2.3 Season Management
- [ ] Create Season model
  ```dart
  class Season {
    final String id;
    final String characterId;
    final int seasonNumber;
    final String aspirationId;
    final StoryOutput storyPlan;
    final GameStateModel currentState;
    final DateTime startedAt;
    final DateTime? completedAt;
  }
  ```
- [ ] Create SeasonRepository
- [ ] Implement season lifecycle methods
- [ ] Add autosave (every 30s + on major actions)
- [ ] Add manual save button
- [ ] Implement cloud sync indicator

#### 2.4 Game State Persistence
- [ ] Extend GameStateNotifier with save/load
  ```dart
  class GameStateNotifier extends Notifier<GameStateModel> {
    Future<void> saveToFirestore() async { }
    Future<void> loadFromFirestore(String seasonId) async { }
    Future<void> autoSave() async { }
  }
  ```
- [ ] Implement periodic autosave timer
- [ ] Add save indicators in UI
- [ ] Handle offline mode (queue writes)
- [ ] Implement conflict resolution

**Deliverable:** Complete save/load system with Firestore backend

---

### Phase 3: Content Management System (Week 3-4)

**Priority: HIGH** 🔥

#### 3.1 Firestore Content Collections
- [ ] Migrate base_cards.json → Firestore `base_cards` collection
- [ ] Create base_npcs collection
- [ ] Create event_templates collection
- [ ] Create locations collection
- [ ] Create aspiration_catalog collection
- [ ] Create admin scripts for content upload

#### 3.2 Dynamic Card Repository
- [ ] Rewrite CardRepository to fetch from Firestore
  ```dart
  class FirestoreCardRepository implements CardRepository {
    // Cascade: Memory cache → Hive → Firestore
    Future<List<CardModel>> loadBaseCards() async { }
    Future<List<CardModel>> loadUserEvolvedCards(String uid) async { }
    Future<void> saveEvolvedCard(String uid, CardModel card) async { }
  }
  ```
- [ ] Implement LRU cache for base cards
- [ ] Use Hive for offline access
- [ ] Add card versioning (schemaVersion)

#### 3.3 NPC Content System
- [ ] Create NPC model
  ```dart
  class NPC {
    final String id;
    final String name;
    final String backstory;
    final OCEANPersonality personality;
    final Map<String, dynamic> metadata;
  }
  ```
- [ ] Create NPCRepository (Firestore + cache)
- [ ] Load base NPCs from Firestore
- [ ] Track user-specific NPC state separately

#### 3.4 Content Update System
- [ ] Implement remote config for feature flags
- [ ] Add content version checking
- [ ] Show "New content available" notifications
- [ ] Implement background sync

**Deliverable:** Dynamic content system with Firestore backend

---

### Phase 4: Game Flow & Core Loop (Week 4-6)

**Priority: CRITICAL** 🚨

#### 4.1 New Game Setup
- [ ] Create new game flow screens
  1. [ ] Character creation (name input)
  2. [ ] Aspiration selection screen (display ~20 aspiration cards)
  3. [ ] Season length selection (12/24/36 weeks)
  4. [ ] Starting location selection
  5. [ ] Starting career selection
  6. [ ] Optional backstory hint input

#### 4.2 Story Generation Integration
- [ ] Call `buildSeasonStory` on new game creation
  ```dart
  Future<void> startNewSeason({
    required String characterId,
    required String aspirationId,
    required int seasonLength,
  }) async {
    // 1. Build StoryInput from user choices
    // 2. Call StoryRepository.buildSeasonStory()
    // 3. Save StoryOutput to Firestore
    // 4. Initialize GameState
    // 5. Generate initial deck
    // 6. Navigate to game board
  }
  ```
- [ ] Show loading screen during generation
- [ ] Handle generation failures gracefully
- [ ] Add retry mechanism

#### 4.3 Deck Initialization
- [ ] Implement deck builder
  ```dart
  class DeckBuilder {
    List<String> buildInitialDeck({
      required StoryOutput story,
      required String aspirationId,
    }) {
      // Return ~40 base card IDs based on:
      // - Aspiration (10 cards)
      // - Starting location (5 cards)
      // - Starting career (5 cards)
      // - Life situation (5 cards)
      // - Generic activities (15 cards)
    }
  }
  ```
- [ ] Draw initial hand (5-7 cards)
- [ ] Implement deck shuffling

#### 4.4 Card Playing System
- [ ] Implement playCard() in GameStateNotifier
  ```dart
  Future<CardPlayResult> playCard(CardModel card) async {
    // 1. Validate resources
    // 2. Deduct costs
    // 3. Apply effects
    // 4. Update meters
    // 5. Track memory
    // 6. Generate narrative (AI)
    // 7. Trigger card evolution check
    // 8. Update relationship if NPC involved
    // 9. Autosave
    // 10. Return result
  }
  ```
- [ ] Add card play animation
- [ ] Show narrative result
- [ ] Update UI reactively

#### 4.5 Time Progression
- [ ] Implement end-of-phase logic
  ```dart
  void endPhase() {
    // 1. Advance currentPhase
    // 2. Reset phaseTimeRemaining
    // 3. If end of day: regenerate energy
    // 4. If end of week: trigger weekly events
    // 5. Check for scheduled events
    // 6. Update UI
    // 7. Autosave
  }
  ```
- [ ] Add "End Phase" button
- [ ] Show phase transition animation
- [ ] Display week summary on week end

#### 4.6 Event System
- [ ] Create Event model
  ```dart
  class GameEvent {
    final String id;
    final String type; // tension_hook, mystery, decisive_decision
    final int weekNumber;
    final bool resolved;
    final String description;
    final List<String> choices;
  }
  ```
- [ ] Create EventManager
- [ ] Schedule events based on StoryOutput.events_plan
- [ ] Trigger events at appropriate times
- [ ] Show event popup UI
- [ ] Track event resolution

#### 4.7 Decisive Decision System
- [ ] Implement decisive decision windows
- [ ] Show special UI for decisive moments
- [ ] Track decision outcomes
- [ ] Apply long-term consequences

**Deliverable:** Complete core gameplay loop from new game → playing cards → progression

---

### Phase 5: Card Evolution System (Week 6-7)

**Priority: HIGH** 🔥

#### 5.1 Evolution Trigger System
- [ ] Implement evolution checker
  ```dart
  class CardEvolutionManager {
    bool shouldEvolve(CardModel card, GameContext context) {
      // Check:
      // - Play count threshold
      // - Relationship level (if NPC card)
      // - Specific event triggers
      // - Story arc progress
    }
    
    Future<CardModel> evolveCard(CardModel card, GameContext context) async {
      // 1. Generate personalized description (AI)
      // 2. Update evolution level
      // 3. Attach relevant memories
      // 4. Update costs/effects
      // 5. Save to Firestore
    }
  }
  ```
- [ ] Trigger evolution checks after card play
- [ ] Show evolution animation
- [ ] Display "before/after" comparison

#### 5.2 Memory Attachment
- [ ] Create Memory model
  ```dart
  class Memory {
    final String id;
    final int week;
    final String description;
    final List<String> cardIds;
    final double emotionalWeight;
    final String? imageUrl;
  }
  ```
- [ ] Create MemoryRepository
- [ ] Attach memories to evolved cards
- [ ] Show memories in card details

#### 5.3 Custom Descriptions
- [ ] Generate personalized card text using AI
- [ ] Reference specific past events
- [ ] Include relationship context
- [ ] Maintain tone consistency

**Deliverable:** Cards evolve based on player actions with personalized narratives

---

### Phase 6: NPC System Integration (Week 7-8)

**Priority: MEDIUM** 📊

#### 6.1 NPC Loading
- [ ] Load base NPCs from Firestore on season start
- [ ] Spawn ~5-10 NPCs based on story plan
- [ ] Initialize relationship tracking

#### 6.2 NPC Interaction
- [ ] Implement NPC card play logic
  ```dart
  Future<void> playNPCCard(CardModel npcCard) async {
    // 1. Call generateDialogue (Cloud Function)
    // 2. Show dialogue UI
    // 3. Update relationship based on choice
    // 4. Track shared memory
    // 5. Check for relationship level-up
  }
  ```
- [ ] Show dialogue choices
- [ ] Apply relationship changes
- [ ] Update trust/level meters

#### 6.3 Relationship Evolution
- [ ] Implement relationship level-up logic
- [ ] Trigger special events at milestones
- [ ] Generate personalized relationship narratives
- [ ] Update NPC card evolution

**Deliverable:** Dynamic NPCs with evolving relationships

---

### Phase 7: UI/UX Polish (Week 8-9)

**Priority: MEDIUM** 📊

#### 7.1 Onboarding Tutorial
- [ ] Create first-time user experience
- [ ] Teach card playing
- [ ] Explain meters
- [ ] Introduce aspirations
- [ ] Show evolution mechanic

#### 7.2 Improved UI Elements
- [ ] Loading states for all async operations
- [ ] Error messages with retry options
- [ ] Success/failure feedback
- [ ] Smooth animations
- [ ] Haptic feedback

#### 7.3 Settings & Preferences
- [ ] Sound/music volume
- [ ] Notifications preferences
- [ ] Data usage settings (AI image generation)
- [ ] Accessibility options

#### 7.4 Life Bookshelf
- [ ] Character/season history view
- [ ] Completed season summaries
- [ ] Memory gallery
- [ ] Export story as text

**Deliverable:** Polished, user-friendly experience

---

### Phase 8: Premium Features & Monetization (Week 9-10)

**Priority: LOW** 💰

#### 8.1 Subscription System
- [ ] Integrate RevenueCat or similar
- [ ] Create subscription tiers
  - Free: 1 character, basic AI
  - Premium: 3 characters, thinking mode, faster generation

#### 8.2 Premium Feature Gating
- [ ] Enable thinking mode for premium users
  ```dart
  if (userProfile.tier == PremiumTier.premium) {
    context.routing.thinkingEnabled = true;
  }
  ```
- [ ] Add many-shot in-context learning for premium
- [ ] Faster image generation
- [ ] Higher quality music stems

#### 8.3 In-App Purchases
- [ ] Extra character slots
- [ ] Story export (PDF)
- [ ] Custom card art

**Deliverable:** Revenue-generating premium features

---

## Part 3: Technical Debt & Architecture Improvements

### 3.1 Missing Infrastructure

#### Observability
- [ ] Add Firebase Crashlytics
- [ ] Implement proper error boundaries
- [ ] Create analytics event tracking
  ```dart
  FirebaseService.logEvent('card_played', parameters: {
    'card_id': card.id,
    'card_type': card.type.name,
    'evolution_level': card.evolutionLevel,
  });
  ```
- [ ] Add performance monitoring

#### Testing
- [ ] Unit tests for repositories
- [ ] Widget tests for key screens
- [ ] Integration tests for core flows
- [ ] E2E tests for critical paths

#### CI/CD
- [ ] GitHub Actions for:
  - [ ] Lint checks
  - [ ] Unit tests
  - [ ] Build validation
  - [ ] Automated deployment (beta tracks)

### 3.2 Performance Optimization

#### Memory Management
- [ ] Implement proper image caching (LRU)
- [ ] Dispose controllers in widgets
- [ ] Monitor memory usage
- [ ] Profile with DevTools

#### AI Request Optimization
- [ ] Implement AIRequestQueue
  ```dart
  class AIRequestQueue {
    Future<T> enqueue<T>(Future<T> Function() request) async {
      // Limit concurrent requests
      // Add timeout handling
      // Implement retry logic
      // Cache responses
    }
  }
  ```
- [ ] Add request deduplication
- [ ] Implement response caching with TTL
- [ ] Add fallback for failures

### 3.3 Code Quality

#### Documentation
- [ ] Add comprehensive docstrings (missing from models)
- [ ] Document architecture decisions
- [ ] Create developer guides
- [ ] Update README

#### Refactoring
- [ ] Extract magic numbers to constants
- [ ] Split large widgets into smaller components
- [ ] Consolidate duplicate code
- [ ] Improve error messages

---

## Part 4: Priority Matrix

### Must Have Before Beta Launch 🚨
1. ✅ Proper authentication (no anonymous)
2. ✅ Save/load system (Firestore)
3. ✅ New game flow (aspiration → story generation → deck)
4. ✅ Core gameplay loop (play cards, advance time)
5. ✅ Card evolution system
6. ✅ Basic NPC interactions
7. ✅ Event system
8. ✅ Autosave

### Should Have for Quality Experience 🔥
1. Smooth animations & feedback
2. Loading states
3. Error handling
4. Tutorial/onboarding
5. Settings screen
6. Multiple characters
7. Season transitions
8. Memory system

### Nice to Have for Launch 📊
1. Premium features
2. Music generation integration
3. Life bookshelf
4. Social features
5. Advanced analytics
6. A/B testing

---

## Part 5: Estimated Timeline

**Total Time:** 10-12 weeks for MVP

- **Weeks 1-2:** Authentication & user system (CRITICAL)
- **Weeks 2-3:** State persistence (CRITICAL)
- **Weeks 3-4:** Content management (HIGH)
- **Weeks 4-6:** Core gameplay loop (CRITICAL)
- **Weeks 6-7:** Card evolution (HIGH)
- **Weeks 7-8:** NPC system (MEDIUM)
- **Weeks 8-9:** UI/UX polish (MEDIUM)
- **Weeks 9-10:** Premium features (LOW)
- **Weeks 10-12:** Testing & bug fixes (CRITICAL)

---

## Part 6: Risk Assessment

### High Risk Areas 🚨
1. **AI Generation Latency** - 10-30s story generation
   - **Mitigation:** Show engaging loading screens, allow background generation
2. **Firestore Costs** - High read/write volume
   - **Mitigation:** Aggressive caching, batch writes, optimize queries
3. **Complexity Creep** - Game is inherently complex
   - **Mitigation:** Strict MVP scope, defer non-critical features
4. **Content Quality** - AI-generated content may be inconsistent
   - **Mitigation:** Extensive prompt engineering, fallbacks, quality gates

### Medium Risk Areas 🔥
1. Performance on low-end devices
2. Offline mode reliability
3. State conflict resolution
4. Card evolution balance

---

## Part 7: Success Metrics

### Technical KPIs
- **Crash-free rate:** > 99%
- **FPS:** Stable 60 FPS
- **Load times:** < 3s cold start
- **AI response time:** < 30s for story generation

### User Experience KPIs
- **Onboarding completion:** > 70%
- **D1 retention:** > 40%
- **D7 retention:** > 20%
- **Session length:** 15-30 minutes
- **Cards played per session:** 10-20

---

## Conclusion

The Flutter app has a **solid foundation** but is currently in a **prototype state**. To reach production:

1. **Remove anonymous auth** → proper user accounts
2. **Implement save system** → Firestore persistence
3. **Build content management** → dynamic loading
4. **Create game flow** → new game → core loop
5. **Add card evolution** → personalized narratives
6. **Integrate NPC system** → dynamic relationships

**Estimated effort:** 10-12 weeks with 1-2 developers working full-time.

**Next immediate action:** Start with authentication (Phase 1), as everything else depends on having real users.


