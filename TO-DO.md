# Unwritten - Master TODO List

**Last Updated**: October 15, 2025  
**Current Status**: Phase 1 Complete (14/17 AI Infrastructure) - Ready for Gameplay Systems  
**Next Up**: Fix Blocking Issues → Emotional Capacity → Scheduling System

---

## 🚨 **BLOCKING ISSUES** (Must Fix First)

### ❌ **Missing Entity Definitions** - CRITICAL
**Priority**: URGENT (Blocks Firebase AI from compiling)  
**Estimated Time**: 1-2 hours  
**Reference Docs**: 
- `@unwritten_data_contract_specification.json` (Complete schema definitions)
- `@master_truths_canonical_spec_v_1_2.md` (Section 11, 13 - OCEAN personality, Novel quality)
- `@1.concept/13-ai-personality-system.md` (OCEAN model, relationship dynamics)
- `@1.concept/16-archive-persistence.md` (Novel generation structures)
- `@3.ai/30-ai-architecture-overview.md` (NPC Response Framework)
- `@3.ai/32-prompt-engineering-principles.md` (Numerical grounding, context building)
- `@3.ai/33-prompt-templates-library.md` (Evolution templates)
- `@2.gameplay/21-card-evolution-mechanics.md` (Evolution triggers)

**Tasks**:
- [ ] Create `CardEvolutionResponse` model
  - Fields: `evolvedTitle`, `narrative`, `statsChanged`, `visualDescription`, `emotionalWeight`, `evolvedDescription`, `tensionType`, `tensionDescription`, `payoffTimeline`, `tensionScore`, `hookEffectiveness`, `essenceCost`
  - Location: `app/lib/features/ai/domain/entities/card_evolution_response.dart`

- [ ] Create `NovelResponse` model
  - Fields: `title`, `novel`, `wordCount`, `threeActBreakdown`, `qualityScores`, `content`, `overallQuality`, `essenceCost`
  - Location: `app/lib/features/ai/domain/entities/novel_response.dart`

- [ ] Create `AIContextPackage` (7-layer context model)
  - Layers: Character, Relationship, Interaction, Player, World, DramaticIrony, Meta
  - Method: `toPromptString()` for serialization
  - Location: `app/lib/features/ai/domain/entities/ai_context_package.dart`

- [ ] Create `AIResponse` model
  - Fields: `dialogue`, `emotion`, `behavioralCues`, `relationshipImpact`, `capacityAfter`, `qualityScore`, `tokenCount`, `generationTimeMs`
  - Location: `app/lib/features/ai/domain/entities/ai_response.dart`

- [ ] Create `SubscriptionTier` enum
  - Values: `free`, `plus`, `ultimate`
  - Location: `app/lib/features/monetization/data/models/subscription_tier.dart`

- [ ] Create `GenerationType` enum
  - Values: `npc_dialogue`, `card_evolution`, `season_novel`, `narrative_beat`
  - Location: `app/lib/features/ai/domain/entities/generation_type.dart`

- [ ] Fix `FirebaseAIService` missing methods
  - `_getModelForTier()` - Returns Gemini model based on subscription tier
  - `_logAIRequest()` - Logs to Firebase Analytics + training data
  - `generateText()` - Wrapper for firebase_ai text generation

---

## 📦 **BATCH 3: Emotional Capacity & Stressors System**

**Priority**: HIGH  
**Estimated Time**: 4-6 hours  
**Reference Docs**:
- `@unwritten_data_contract_specification.json` (EmotionalCapacity, Stressor definitions)
- `@master_truths_canonical_spec_v_1_2.md` (Section 2, 16 - Capacity constraints, support rule: capacity + 2)
- `@NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md` (Scale 2 - Capacity 0-10 with tier examples)
- `@1.concept/13-ai-personality-system.md` (Emotional intelligence, NPC capacity tracking)
- `@1.concept/19-emotional-state-system.md` (20 emotional states, state transitions)
- `@2.gameplay/13-meter-effects-tables.md` (What happens at each meter threshold)
- `@2.gameplay/14-emotional-state-mechanics.md` (State-driven filtering, evolution)
- `@3.ai/30-ai-architecture-overview.md` (NPC Response Framework: OCEAN → Urgency → Trust → Capacity)

### Models
- [ ] Fix `EmotionalCapacityModel` (already exists, needs validation)
  - Verify calculation: `(Physical + Mental + Social + Emotional) / 4 - stressorPenalties`
  - Implement capacity tiers: CRISIS (<2.0), VERY_LOW (2.0-4.0), LOW (4.0-6.0), MODERATE (6.0-8.0), HIGH (8.0-10.0)
  - Add "capacity + 2" rule for support availability
  - Location: `app/lib/features/ai/data/models/emotional_capacity.dart`

- [ ] Create `StressorModel`
  - 5 types: `workOverload`, `relationshipTension`, `financialPressure`, `healthConcerns`, `deadlinePressure`
  - Fields: `type`, `severity` (1-10), `penalty` (0.5-3.0), `duration` (weeks)
  - Location: `app/lib/features/game/data/models/stressor_model.dart`

- [ ] Integrate capacity into `GameStateModel`
  - Add `EmotionalCapacityModel emotionalCapacity` field
  - Auto-calculate from life meters on each turn
  - Store active stressors

### UI
- [ ] Create **Character State Cluster** (top-left of screen)
  - Capacity bar (0-10, color-coded by tier: red <2, orange 2-4, yellow 4-6, green 6-8, blue 8-10)
  - Stressor list (expandable, shows type + severity)
  - Burnout indicator (visual warning when capacity < 3.0)
  - Location: `app/lib/shared/widgets/character_state_cluster.dart`

---

## 🎨 **BATCH 4: Presentation Layer & Content Generation Framework** (RESTRUCTURED)

**Priority**: HIGH (Core scaffolding for AI content generation + polished UX)  
**Estimated Time**: 12-16 hours (broken into 3 parts)  

---

### **Part A: Visual Generation Scaffold** (4-6 hours)

**Reference Docs**:
- `@2.gameplay/61-visual-generation-specs.md` (665 lines - complete visual AI specs)
- `@2.gameplay/60-art-style-system.md` (10 art styles, emotional palettes)
- `@3.ai/37-model-deployment-optimization.md` (TFLite conversion, quantization)
- `@app/docs/packages/tflite_flutter.md` (On-device ML inference)
- `@1.concept/12-card-evolution.md` (Visual evolution system)
- `@5.architecture/55-flame-engine-fundamentals.md` (Asset loading, sprite sheets)

**Goal**: Set up infrastructure for AI image generation (cards, portraits, locations)

**Tasks**:
- [ ] Create `ImageGenerationService` scaffold
  - Placeholder for Firebase Imagen API integration
  - Stub methods: `generateCardArt()`, `generatePortrait()`, `generateLocation()`
  - Location: `app/lib/features/ai/domain/services/image_generation_service.dart`

- [ ] Create `ImageGenerationRequest` model
  - Fields: `prompt`, `style` (10 art packs), `emotionalPalette`, `size`, `seed`, `negativePrompt`
  - Validation: Ensure prompt follows visual specs (composition, lighting, mood)
  - Location: `app/lib/features/ai/data/models/image_generation_request.dart`

- [ ] Create `VisualStyleProfile` model
  - 10 art styles from specs: Ethereal, Impressionist, Neo-Deco, Cinematic, Watercolor, etc.
  - Emotional palettes: Joy (warm yellows/oranges), Melancholy (cool blues/grays), etc.
  - Technical parameters: Composition rules, lighting presets, color grading
  - Location: `app/lib/features/ai/data/models/visual_style_profile.dart`

- [ ] Create `ImageCache` with Hive integration
  - LRU cache (50 images in memory)
  - Persistent cache with `hive` (see `@app/docs/packages/hive.md`)
  - Auto-cleanup on low storage
  - Location: `app/lib/features/ai/data/services/image_cache_service.dart`

- [ ] Integrate with card system
  - Update `CardModel` to include `imageUrl` and `cacheKey`
  - Add placeholder images for each card type
  - Progressive loading: placeholder → low-res → full
  - Use Flame sprite loading (see `@5.architecture/55-flame-engine-fundamentals.md`)

---

### **Part B: UI/UX Cluster System** (6-8 hours)

**Reference Docs**:
- `@1.concept/25-app-book-design.md` (421 lines - complete UI/UX vision!)
- `@1.concept/26-unwritten-memories-ui-concept.tsx.md` (React component examples)
- `@app/docs/packages/flutter_animate.md` (Animation library)
- `@app/docs/packages/google_fonts.md` (Typography system)
- `@app/docs/packages/ui_packages.md` (UI best practices)
- `@5.architecture/56-card-physics-animations.md` (I/O FLIP physics)
- `@app/docs/CARD_INTERACTION_GUIDE.md` (Interaction states, gestures)
- `@app/docs/CARD_DRAG_INTERACTION_FEATURE.md` (Drag implementation details)

**Goal**: Implement polished, book-like UI clusters with smooth animations

**Tasks**:

#### **1. Create Unified Cluster System**
- [ ] Create `UICluster` base widget
  - Expandable/collapsible with `flutter_animate` (see `@app/docs/packages/flutter_animate.md`)
  - States: `collapsed`, `peek`, `expanded`
  - Smooth transitions with spring physics
  - Location: `app/lib/shared/widgets/ui_cluster.dart`

#### **2. Implement Stone/Amber/Parchment Theme**
- [ ] Create `UnwrittenTheme` class
  - Stone palette: `stone50` to `stone900`
  - Amber accents: `amber200`, `amber400`, `amber600`
  - Parchment textures: noise overlay, subtle grain
  - Typography: Use `google_fonts` (Poppins for headings, Merriweather for body - see `@app/docs/packages/google_fonts.md`)
  - Location: `app/lib/core/constants/unwritten_theme.dart`

- [ ] Update `main.dart` MaterialApp theme
  - Replace indigo → stone/amber
  - Add custom `TextTheme` with literary fonts
  - Set Material3 ColorScheme
  - Add parchment background texture to scaffold

#### **3. Polish Card Interactions** (using existing patterns)
- [ ] Apply stone/amber theme to `CardHandFanWidget`
  - Update shadow colors (stone-600 with low opacity)
  - Add parchment texture to card backgrounds
  - Enhance glow effects with amber accents
  - Reference: `@app/docs/CARD_INTERACTION_GUIDE.md` for interaction states

- [ ] Enhance animations with `flutter_animate`
  - Card draw: fade + slide with elastic curve
  - Card hover: subtle scale + lift
  - Card play: shimmer effect on success
  - Reference: `@app/docs/packages/flutter_animate.md` for animation patterns

#### **4. Create Book-Like Layout**
- [ ] Implement "page turn" transitions between screens
  - Use `flutter_animate` page flip effect
  - Parchment texture on page edges
  - Subtle crease shadow down the middle

- [ ] Add "bookmark" tab navigation
  - Vertical tabs on left edge (like book chapter markers)
  - Amber highlights on active bookmark
  - Smooth slide animations

#### **5. Responsive Cluster Layout**
- [ ] Implement smart cluster positioning
  - Desktop: clusters on edges (Character State top-left, Resources top-right, etc.)
  - Mobile: bottom sheet drawers (swipe up to expand)
  - Tablet: hybrid (side panels + bottom drawer)
  - Use Flutter's `MediaQuery` for breakpoints

---

### **Part C: Literary Styles Scaffold** (2-3 hours)

**Reference Docs**:
- `@1.concept/23-literary-styles.md` (Literary style system for novel generation)
- `@3.ai/33-prompt-templates-library.md` (Prompt engineering)
- `@3.ai/35-consistency-coherence.md` (Quality validation)
- `@unwritten_data_contract_specification.json` (Novel quality scoring)

**Goal**: Set up literary style profiles for novel generation (use in `FirebaseAIService.generateSeasonNovel()`)

**Tasks**:
- [ ] Create `LiteraryStyleProfile` model
  - Styles from doc: Lyrical, Minimalist, Gothic, Satirical, Stream of Consciousness, etc.
  - Fields: `styleName`, `narrativeVoice`, `sentenceStructure`, `vocabularyLevel`, `metaphorDensity`, `timeTreatment`
  - Location: `app/lib/features/ai/data/models/literary_style_profile.dart`

- [ ] Create `NovelStyleSelector` service
  - Match player's personality (OCEAN) → literary style
  - Openness 4+ → Experimental/Lyrical
  - Conscientiousness 4+ → Structured/Minimalist
  - Neuroticism 4+ → Gothic/Introspective
  - Location: `app/lib/features/ai/domain/services/novel_style_selector.dart`

- [ ] Integrate with `generateSeasonNovel()`
  - Add `literaryStyle` parameter to generation
  - Update prompt template to include style instructions
  - Validate output matches style profile
  - Location: Update `app/lib/features/ai/domain/services/firebase_ai_service.dart`

- [ ] Create style preview samples
  - Store 3-5 sample paragraphs per style
  - Show to player during character creation ("Choose your narrative voice")
  - Location: `app/assets/data/literary_style_samples.json`

---

### **Integration & Testing**
- [ ] Test image cache performance (see `@app/docs/packages/hive.md` for persistence)
- [ ] Verify cluster animations maintain 60 FPS (see `@5.architecture/55-flame-engine-fundamentals.md`)
- [ ] Test card interactions with new theme (see `@app/docs/CARD_INTERACTION_GUIDE.md`)
- [ ] Validate typography readability (see `@app/docs/packages/google_fonts.md`)
- [ ] Test responsive layout on 3 screen sizes

---

**Why This Matters**:
- **Part A** enables AI-generated visuals (critical for card art, portraits, locations)
- **Part B** creates the polished, book-like UX that makes Unwritten feel premium
- **Part C** ensures novels are literary-quality with personalized narrative voice

**Dependencies**:
- Requires `FirebaseAIService` (already implemented)
- Builds on existing card interaction system (see `@app/docs/CARD_DRAG_INTERACTION_FEATURE.md`)
- Uses Flame engine for rendering (see `@5.architecture/55-flame-engine-fundamentals.md`)

---

## 💰 **BATCH 5: Resources Cluster**

**Priority**: HIGH  
**Estimated Time**: 3-4 hours  
**Reference Docs**:
- `@unwritten_data_contract_specification.json` (PlayerResources definition)
- `@2.gameplay/10-resource-economy-spec.md` (6 resources, exact budgets, scarcity formulas)
- `@2.gameplay/11-turn-economy-implementation.md` (168h weekly model, 3 turns/day, energy mechanics)
- `@1.concept/21-turn-structure.md` (Multi-scale time architecture)
- `@app/docs/packages/utilities.md` (Intl for number formatting, Equatable for models)
- `@app/docs/packages/flutter_riverpod.md` (State management for resources)

### Models
- [ ] Fix `ResourcesModel` to match data contract
  - **CRITICAL**: `energy` is 0-3 (NOT 0-10!)
  - Fields: `money` (integer), `energy` (0-3), `timeThisWeek` (hours), `socialCapital` (0-15)
  - Energy regeneration: +8 hours per night (can overflow above 3 if player sleeps well)
  - Location: `app/lib/features/game/data/models/resources_model.dart` (already exists, needs fixing)

### UI
- [ ] Create **Resources Cluster** (top-right of screen)
  - Energy indicator (3 dots: filled/empty)
  - Money display with icon
  - Time remaining this week (hours)
  - Social capital meter (0-15)
  - Collapsed/expanded states
  - Location: `app/lib/shared/widgets/resources_cluster.dart`

---

## ⚡ **BATCH 6: Card Appeal System**

**Priority**: MEDIUM  
**Estimated Time**: 2-3 hours  
**Reference Docs**:
- `@master_truths_canonical_spec_v_1_2.md` (Section 10 - Card appeal mechanics)
- `@1.concept/11-card-system-basics.md` (All card types, anatomy, structure)
- `@1.concept/19-emotional-state-system.md` (State-driven card filtering)
- `@2.gameplay/01-emotional-authenticity.md` (System 2.10 - Card Appeal System integration)
- `@2.gameplay/14-emotional-state-mechanics.md` (Filtering rules, state evolution)

### Models
- [ ] Create `CardAppealCalculator` service
  - Base appeal from card data (0.0-1.0)
  - State-based modifiers:
    - High energy → +0.3 to active cards
    - Low capacity → -0.5 to demanding cards
    - High social meter → +0.4 to social cards
  - Final range: 0.0-3.0
  - Location: `app/lib/features/cards/domain/services/card_appeal_calculator.dart`

### UI
- [ ] Add appeal-based visual effects to cards
  - High appeal (>1.8): golden glow, sparkle particles
  - Medium appeal (1.0-1.8): subtle highlight
  - Low appeal (<0.5): slight desaturation
  - Location: Update `app/lib/features/game/presentation/components/card_hand_fan_widget.dart`

---

## 📅 **BATCH 7: Dynamic Scheduling System** (NEW)

**Priority**: HIGH  
**Estimated Time**: 6-8 hours  
**Reference Docs**:
- `@unwritten_data_contract_specification.json` (GameTime definition, turn enumeration)
- `@2.gameplay/11-turn-economy-implementation.md` (168h weekly model, 3 turns/day, batching rules)
- `@2.gameplay/71-daily-turn-flow-detailed.md` (Step-by-step turn implementation)
- `@2.gameplay/72-weekly-cycle-implementation.md` (Week structure, end-of-week processing)
- `@1.concept/21-turn-structure.md` (MICRO/MESO/MACRO time scales, day structure)
- `@1.concept/20-character-creation.md` (First week goal selection mechanics)
- `@5.architecture/56-card-physics-animations.md` (Drop zone detection, card snapping)
- `@5.architecture/55-flame-engine-fundamentals.md` (Component hierarchy for drop zones)
- `@app/docs/CARD_DRAG_INTERACTION_FEATURE.md` (Drag-to-commit implementation patterns)
- `@app/docs/packages/flutter_animate.md` (Zone highlight animations)
- `@app/docs/packages/utilities.md` (Intl for time formatting, UUID for card IDs)

### Design Specs
**System**: 3 drop zones per day (Morning/Day/Evening) with dynamic time tracking

**Features**:
1. **Start Time Selection**: Player sets wake-up time for first zone (6am-10am default 8am)
2. **Card Time Costs**: Each card has duration (0.5h-8h)
3. **Dynamic Zone Duration**: Zones expand based on cards dropped (no fixed 4-hour limit)
4. **Auto-calculation**: Show estimated completion time for each zone
5. **Zone Overflow**: If Morning ends at 2pm, that's when Day starts
6. **Obligation Cards**: Auto-placed (work, appointments) with suggested times
7. **Card Combinations**: Can chain cards (coffee + commute = combined time with bonus)

### Models
- [ ] Update `DayPhase` enum
  - Add `estimatedStartTime` (DateTime)
  - Add `estimatedEndTime` (DateTime)
  - Add `plannedCards` (List<String> cardIds)
  - Add `actualDuration` (double hours)

- [ ] Create `CardTimeCost` model
  - Fields: `baseTime` (hours), `minTime`, `maxTime`, `timeVariance`
  - Modifiers based on player state (tired = +20% time, energized = -10%)
  - Location: `app/lib/features/cards/data/models/card_time_cost.dart`

- [ ] Create `SchedulePlanner` service
  - `commitCardToZone(cardId, zoneIndex)` - Add card to morning/day/evening
  - `calculateZoneTiming(zoneIndex)` - Get estimated start/end for zone
  - `getObligationCards()` - Return auto-scheduled obligations
  - `canFitCard(cardId, zoneIndex)` - Check if card fits reasonably
  - Location: `app/lib/features/game/domain/services/schedule_planner.dart`

- [ ] Create `ObligationCard` model
  - Fields: `isObligation` (bool), `suggestedStartTime`, `isSkippable`, `skipConsequence`
  - Examples: Work (9am-5pm, 8h), Doctor (2pm, 1h, skippable with -trust)
  - Location: `app/lib/features/cards/data/models/obligation_card.dart`

### UI
- [ ] Create **Phase Drop Zones** (center-bottom of screen)
  - 3 zones side-by-side: Morning | Day | Evening
  - Each zone shows:
    - Estimated start time (e.g., "8:00 AM")
    - Estimated end time (e.g., "12:30 PM")
    - Total duration (e.g., "4.5 hours")
    - Cards committed (visual stack)
    - Drop target indicator
  - Location: `app/lib/shared/widgets/phase_drop_zones.dart`

- [ ] Update `CardHandFanWidget` for drag-to-commit
  - Draggable cards with time cost badge
  - Drop feedback (zone highlights, time preview)
  - Reorder cards within zone
  - Remove card from zone (drag back to hand)

- [ ] Create **Time Setter Widget** (morning zone only)
  - Time picker: 6am-10am slider
  - Shows "Wake up at: 8:00 AM"
  - Updates zone start times automatically

- [ ] Add **Obligation Indicators**
  - Visual badge on obligation cards (clock icon)
  - Suggested time shown ("Work: 9am-5pm")
  - Warning if zone conflicts with obligation

---

## 📊 **BATCH 8: Progress & Story Cluster**

**Priority**: MEDIUM  
**Estimated Time**: 3-4 hours  
**Reference Docs**:
- `@unwritten_data_contract_specification.json` (Aspiration, TensionHook definitions)
- `@master_truths_canonical_spec_v_1_2.md` (Section 2, 17 - Tension hooks, memory resonance)
- `@2.gameplay/31-narrative-arc-scaffolding.md` (3-act season structure implementation)
- `@2.gameplay/35-tension-maintenance-system.md` (Hook points, mystery threads, micro-cliffhangers)
- `@2.gameplay/36-stakes-escalation-mechanics.md` (Consequence chains, dramatic neglect)
- `@2.gameplay/40-season-structure-spec.md` (12/24/36 week options, pacing per length)
- `@1.concept/15-progression-phases.md` (Season-based structure, three-act narrative)

### Models
- [ ] Update `AspirationModel` (basic structure exists)
  - Add progress tracking (0-100%)
  - Add skill requirements
  - Add tension hooks
  - Location: Update existing aspiration model

- [ ] Create `TensionHookModel`
  - Fields: `hookId`, `seasonPlanted`, `hookType`, `status`, `tensionScore`, `payoffTimeline`
  - 4 types: `mysteryHook`, `partialReveal`, `contradiction`, `stakesEscalation`
  - Location: `app/lib/features/narrative/data/models/tension_hook_model.dart`

### UI
- [ ] Create **Progress & Story Cluster** (left side of screen)
  - Aspiration progress bar with milestone markers
  - Active tension hooks (expandable list)
  - Act structure timeline (Act 1/2/3 progress)
  - Current tension level indicator
  - Location: `app/lib/shared/widgets/progress_story_cluster.dart`

---

## 👥 **BATCH 9: Relationships Cluster**

**Priority**: MEDIUM  
**Estimated Time**: 2-3 hours  
**Reference Docs**:
- `@unwritten_data_contract_specification.json` (Relationship, NPCCapacity definitions)
- `@master_truths_canonical_spec_v_1_2.md` (Section 11 - OCEAN personality, relationship progression)
- `@2.gameplay/44-relationship-progression-spec.md` (Levels 0-5, trust thresholds, interaction counts)
- `@1.concept/13-ai-personality-system.md` (Relationship dynamics, trust 0.0-1.0, compatibility)

### Models (Already mostly complete from AI infrastructure)
- [ ] Verify `RelationshipModel` matches spec
  - Fields: `level` (1-5), `trust` (0.0-1.0), `interactionCount`, `relationshipAge`
  - Add `npcCapacity` tracking
  - Location: `app/lib/features/relationships/data/models/relationship_model.dart`

### UI
- [ ] Create **Relationships Cluster** (right side of screen)
  - NPC cards (mini portraits)
  - Trust dots (visual 0.0-1.0 indicator)
  - Relationship level badge (1-5: Stranger → Soulmate)
  - Last interaction time
  - Capacity indicator (NPC's current emotional bandwidth)
  - Location: `app/lib/shared/widgets/relationships_cluster.dart`

---

## 📆 **BATCH 10: Timeline Cluster**

**Priority**: LOW  
**Estimated Time**: 2-3 hours  
**Reference Docs**:
- `@unwritten_data_contract_specification.json` (GameTime definition)
- `@2.gameplay/72-weekly-cycle-implementation.md` (Week structure, end-of-week processing)
- `@2.gameplay/73-season-flow-implementation.md` (Act I → II → III mechanics, climax systems)
- `@1.concept/15-progression-phases.md` (Seasons & life arcs)
- `@1.concept/21-turn-structure.md` (MESO and MACRO time scales)

### UI
- [ ] Create **Timeline Cluster** (bottom-left of screen)
  - Week progress bar (e.g., "Week 5 of 12")
  - Day indicator (Mon-Sun)
  - Act structure (Act 1: Weeks 1-4, Act 2: Weeks 5-9, Act 3: Weeks 10-12)
  - Upcoming events preview
  - Location: `app/lib/shared/widgets/timeline_cluster.dart`

---

## 🎲 **BATCH 11: Turn Execution**

**Priority**: HIGH  
**Estimated Time**: 6-8 hours  
**Reference Docs**:
- `@2.gameplay/12-success-probability-formulas.md` (Exact math for success chances, 7 modifiers)
- `@2.gameplay/71-daily-turn-flow-detailed.md` (Moment-to-moment implementation)
- `@2.gameplay/13-meter-effects-tables.md` (What happens at each meter threshold)
- `@master_truths_canonical_spec_v_1_2.md` (Numerical grounding requirements)
- `@1.concept/21-turn-structure.md` (Individual turn structure 30sec-2min)
- `@5.architecture/61-riverpod-integration.md` (State management patterns)
- `@app/docs/packages/flutter_riverpod.md` (Riverpod 3.x usage)
- `@app/docs/packages/vibration.md` (Haptic feedback for turn events)

### Core Mechanics
- [ ] Create `SuccessCalculator` service
  - 7 modifiers: Base chance (40%) + Skill (0-40%) + Energy (0-10%) + Relationship (0-10%) + Momentum (±5%) + ComfortZone (±5%) + Randomness (±10%)
  - Output: Success score 0.0-1.0
  - Location: `app/lib/features/game/domain/services/success_calculator.dart`

- [ ] Create `TurnExecutor` service
  - `executeCard(cardId)` - Run full turn logic
    - Calculate success
    - Apply meter impacts
    - Deduct resources (energy, time, money)
    - Update relationships
    - Generate narrative
    - Trigger AI dialogue (if NPC card)
  - Location: `app/lib/features/game/domain/services/turn_executor.dart`

- [ ] Create `MeterImpactCalculator`
  - Calculate meter changes from card play
  - Apply decay rates (-0.5 to -1.0 per week)
  - Cap at 0-10 bounds
  - Location: `app/lib/features/game/domain/services/meter_impact_calculator.dart`

### Integration
- [ ] Connect to `GameStateNotifier`
  - Add `executePhase()` method (runs all committed cards in zone)
  - Update meters, resources, relationships
  - Generate narrative for phase
  - Advance to next phase

---

## 🎨 **BATCH 12: Polish & Animations**

**Priority**: LOW  
**Estimated Time**: 4-6 hours  
**Reference Docs**:
- `@5.architecture/56-card-physics-animations.md` (I/O FLIP drag physics, momentum, drop zones)
- `@5.architecture/59-performance-optimization-flame.md` (Sprite atlases, pooling, 60 FPS optimization)
- `@5.architecture/57-component-architecture.md` (Component hierarchy, lifecycle, communication)
- `@5.architecture/55-flame-engine-fundamentals.md` (Game loop, effects system, delta time)
- `@5.architecture/58-camera-viewport-systems.md` (Camera shake effects)
- `@2.gameplay/62-animation-specifications.md` (Holo cards, particle effects, loops)
- `@app/docs/packages/flutter_animate.md` (Animation library for UI)
- `@app/docs/packages/vibration.md` (Haptic patterns for polish)
- `@app/docs/CARD_INTERACTION_GUIDE.md` (Interaction states, timings)
- `@app/docs/CARD_DRAG_INTERACTION_FEATURE.md` (Drag implementation details)

### Animations
- [ ] Smooth cluster expand/collapse
  - Spring-based animations
  - Staggered reveals
  
- [ ] Card commitment animations
  - Slide into zone with bounce
  - Glow effect on drop
  - Card shuffle when reordering

- [ ] Phase transition effects
  - Screen wipe (morning → day → evening)
  - Time passage indicator
  - Subtle screen shake on turn end

- [ ] Card interaction polish
  - Hover peek (slight lift + scale)
  - Active card glow
  - Drag momentum physics
  - Snap-back spring

---

## 🤖 **AI SYSTEMS** (Parallel Track)

### **AI-1: Image Generation System**

**Priority**: MEDIUM  
**Estimated Time**: 4-6 hours  
**Reference Docs**:
- `@3.ai/30-ai-architecture-overview.md` (Hybrid cloud-local architecture, technology stack)
- `@3.ai/31-hybrid-cloud-local-system.md` (Smart routing algorithm, iOS/Android/Flutter code)
- `@3.ai/37-model-deployment-optimization.md` (PyTorch to LiteRT conversion, INT4 quantization)
- `@2.gameplay/60-card-art-specifications.md` (Art requirements per card type, resolutions)
- `@2.gameplay/61-visual-generation-specs.md` (Complete visual AI specs, 665 lines)
- `@2.gameplay/60-art-style-system.md` (10 art styles with emotional palettes)
- `@1.concept/12-card-evolution.md` (Visual evolution system, character level progression)
- `@app/docs/packages/tflite_flutter.md` (On-device ML inference, < 15ms target)
- `@app/docs/packages/hive.md` (Image caching with Hive)
- `@app/docs/packages/dio.md` (HTTP client for image downloads)
- `@5.architecture/55-flame-engine-fundamentals.md` (Asset loading, sprite sheets)

**Approach**: Firebase AI Logic (Imagen) for MVP → TFLite for production

**Tasks**:
- [ ] Implement `generateImage()` in `FirebaseAIService`
  - Character portraits (5 evolution levels: Stranger → Soulmate)
  - Card art generation from descriptions
  - Location backgrounds
  - Emotional state overlays

- [ ] Create `ImageGenerationRequest` model
  - Fields: `prompt`, `style`, `size`, `negativePrompt`
  - Presets for character/card/location

- [ ] Create `ImageCache` service
  - LRU cache (max 50 images in memory)
  - Persistent cache with Hive
  - Auto-download on card draw

- [ ] Integrate with card system
  - Generate portrait on character evolution
  - Cache card art
  - Progressive loading (placeholder → full image)

---

### **AI-2: Story Generation & Training Data** (CRITICAL)

**Priority**: HIGH  
**Estimated Time**: 8-10 hours  
**Reference Docs**:
- `@chapter_generation_packet (1).json` (THE GOLD STANDARD TEMPLATE! Complete chapter structure)
- `@master_story_context (1).json` (Master context tracking)
- `@master_truths_canonical_spec_v_1_2.md` (Section 13, 17 - Novel quality, tension hooks)
- `@1.concept/23-literary-styles.md` (Literary style system for narrative voice)
- `@2.gameplay/30-decisive-decision-templates.md` (Complete scaffolding with 20+ examples)
- `@2.gameplay/31-narrative-arc-scaffolding.md` (3-act season structure implementation)
- `@2.gameplay/34-novel-generation-pipeline.md` (Season → chapter conversion process)
- `@2.gameplay/35-tension-maintenance-system.md` (Hook points, mystery threads, micro-cliffhangers)
- `@2.gameplay/36-stakes-escalation-mechanics.md` (Consequence chains, dramatic neglect consequences)
- `@2.gameplay/37-dramatic-irony-system.md` (NPC perspectives, knowledge gaps, memory callbacks)
- `@2.gameplay/38-emotional-memory-tracking.md` (Emotional echoes, multi-season persistence)
- `@3.ai/32-prompt-engineering-principles.md` (Six principles, OCEAN → Response, numerical grounding)
- `@3.ai/33-prompt-templates-library.md` (Reusable templates, context injection, Marcus hospital example)
- `@3.ai/34-context-memory-systems.md` (Six-layer context, memory hierarchy, canonical facts)
- `@3.ai/35-consistency-coherence.md` (Eight-step validation, novel-quality checks, dialogue length)
- `@1.concept/16-archive-persistence.md` (Season-aware book generation, multi-volume compilation)
- `@1.concept/22-multi-lifetime-continuity.md` (Four-tier context, memory compression 50:1)
- `@app/docs/packages/hive.md` (Story data persistence)
- `@app/docs/packages/dio.md` (API calls to Firebase AI)
- `@app/docs/packages/utilities.md` (JSON serialization with Equatable, UUID for IDs)

**Goal**: Generate literary-quality chapters aligned to your proven structure

**Tasks**:

#### **Data Collection During Gameplay**
- [ ] Create `StoryContextBuilder` service
  - Captures gameplay as it happens
  - Builds `master_story_context.json` equivalent
  - Tracks:
    - Established facts (with week markers)
    - Character registry (voice profiles, behavioral tics)
    - Story arcs (status, last change week)
    - Previous chapters summary
  - Location: `app/lib/features/narrative/domain/services/story_context_builder.dart`

- [ ] Create `ChapterDataCollector` service
  - Captures per-chapter gameplay data
  - Builds `chapter_generation_packet.json` equivalent
  - Tracks:
    - **chapter_metadata**: Number, title, weeks covered, POV, act placement, emotional arc, word count, pacing
    - **chapter_narrative**: Scenes, decisive moments, emotional beats, key dialogues, tension arc
    - **pov_perspectives**: Character states, knowledge states, internal narratives, observations, voice profiles, memories, unspoken thoughts
    - **technique_guidance**: Scene techniques, dialogue guidance, emotional technique, chapter techniques
    - **continuity_anchors**: Recurring elements, must-honor facts, relationship continuity, world state, personality continuity, timeline markers
    - **foreshadowing**: Future events, planting methods, signals, payoffs
  - Location: `app/lib/features/narrative/domain/services/chapter_data_collector.dart`

- [ ] Create data models for story structure
  - `ChapterMetadata` model
  - `SceneData` model (with sensory_palette, narrative_beats, information_state, function, tension_level)
  - `DecisiveMoment` model (context_before with character states, the_choice, immediate_aftermath)
  - `EmotionalBeat` model (with build_up, physical_manifestation, behavioral_tells, show_dont_tell)
  - `KeyDialogue` model (exchanges with subtext, delivery, non-verbal, listener_reaction)
  - `POVPerspective` model (full character state, knowledge state, internal narrative, observations, voice profile, memories, unspoken)
  - `TechniqueGuidance` model
  - `ContinuityAnchors` model
  - `Foreshadowing` model
  - Location: `app/lib/features/narrative/data/models/`

#### **Chapter Generation**
- [ ] Create `ChapterGenerator` service
  - Uses `FirebaseAIService.generateSeasonNovel()` (already implemented!)
  - Input: `ChapterGenerationPacket` + `MasterStoryContext`
  - Output: 2,800-word literary chapter
  - Prompt template (use the exact prompt you provided above!)
  - Location: `app/lib/features/narrative/domain/services/chapter_generator.dart`

- [ ] Implement quality validation
  - Check POV consistency (second-person for player, third-person close for NPCs)
  - Verify knowledge boundaries respected
  - Validate emotional authenticity ≥0.70
  - Check sensory detail density
  - Verify show-don't-tell ratio

- [ ] Auto-save generated chapters
  - Save to `Unwrittenshelf` collection
  - Format as ePub/PDF for export
  - Track quality scores
  - Store for training data

#### **Training Data for Story Generation**
- [ ] Export chapter generation data
  - Pair: `ChapterGenerationPacket` (input) + Generated Chapter (output) + Quality Scores
  - Store in `training_data` collection (already implemented!)
  - Tag with `generation_type: 'chapter_generation'`

- [ ] Generate synthetic training samples
  - Use `TrainingDataGenerator.generateBatch()` (already implemented!)
  - Create varied scenarios (different personality combos, capacity levels, relationship stages)
  - Generate 1,000+ samples for fine-tuning

---

### **AI-3: Video Generation** (Phase 3 - Future)

**Priority**: LOW  
**Estimated Time**: TBD  
**Status**: Deferred until image generation is stable

---

## 🔧 **INFRASTRUCTURE & POLISH**

### **Testing**
- [ ] Fix broken unit tests
  - `card_model_test.dart` - Fix type cast errors
  - `game_state_model_test.dart` - Update for life meters
  - `card_widget_test.dart` - Fix ambiguous finder

- [ ] Add integration tests
  - Card play flow (draw → activate → play → outcome)
  - Phase execution (commit cards → execute → next phase)
  - AI generation (trigger → generate → validate)

### **Documentation**
- [ ] Polish missing public member docs (75+ warnings)
- [ ] Create architecture diagram
- [ ] Write player-facing tutorial

### **Production Auth** (Phase 3)
- [ ] Replace anonymous Firebase auth
- [ ] Implement email/password
- [ ] Add social logins (Google, Apple)
- [ ] Secure token management

---

## 📊 **PRIORITY MATRIX**

### **Sprint 1 (This Week):**
1. ✅ Fix blocking entity definitions (1-2h)
2. ✅ BATCH 3: Emotional Capacity (4-6h)
3. ✅ BATCH 5: Resources Cluster (fix energy 0-3) (2-3h)
4. ✅ BATCH 7: Scheduling System (6-8h)

**Total**: ~13-19 hours

### **Sprint 2 (Next Week):**
1. ✅ AI-2: Story Generation alignment (8-10h)
2. ✅ BATCH 11: Turn Execution (6-8h)
3. ✅ BATCH 6: Card Appeal (2-3h)

**Total**: ~16-21 hours

### **Sprint 3 (Week After):**
1. ✅ AI-1: Image Generation (4-6h)
2. ✅ BATCH 8: Progress & Story (3-4h)
3. ✅ BATCH 9: Relationships (2-3h)
4. ✅ BATCH 4: Theme Polish (3-4h)

**Total**: ~12-17 hours

### **Sprint 4 (Polish):**
1. ✅ BATCH 10: Timeline (2-3h)
2. ✅ BATCH 12: Animations (4-6h)
3. ✅ Testing & Bug Fixes (4-6h)

**Total**: ~10-15 hours

---

## 📝 **NOTES**

- **Story Generation is CRITICAL**: Your `chapter_generation_packet.json` structure is GOLD. We need to capture gameplay data in this exact format.
- **Scheduling System**: Your hybrid approach (3 drop zones with dynamic time) is perfect. Much better than fixed 4-hour phases.
- **Energy Fix**: Data contract says energy is 0-3, not 0-10. Need to fix `ResourcesModel` immediately.
- **Training Data**: We're already collecting AI generation data. Now we need to collect chapter/story data.

---

**Ready to start with blocking issues → emotional capacity → scheduling system?** 🚀

