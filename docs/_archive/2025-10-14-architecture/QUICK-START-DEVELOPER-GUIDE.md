# Quick Start Developer Guide

> **Canonical Reference**: Master Truths v1.2  
> **Purpose**: Fast onboarding for new developers joining Unwritten  
> **Last Updated**: October 14, 2025

---

## What is Unwritten?

Unwritten is a **narrative card game** that simulates life. Players:
- Build relationships with AI-powered NPCs
- Pursue aspirations through 12-36 week seasons
- Make meaningful decisions that affect their story
- Generate personalized novels from their gameplay

**Core Loop**: Play cards → Generate narrative → Build relationships → Evolve cards → Complete season → Generate novel

---

## Project Status: MVP Phase

**Current Focus**: Getting a playable game loop with cloud-based AI

**What's Working**: 
- ⏳ Phase 1 (Foundation) - In Progress
- ⏳ Card system design
- ⏳ Clean Architecture setup

**What's Next**:
- Phase 2: Core game loop (card playing, turn system)
- Phase 3: Cloud AI integration
- Phase 4: Season structure

**What's Deferred**:
- Local AI optimization
- Advanced graphics/animations
- Cloud save sync
- Novel generation

---

## 5-Minute Architecture Overview

### Tech Stack
- **Framework**: Flutter 3.x + Dart 3.x
- **State Management**: Riverpod (Provider pattern)
- **Storage**: Hive (local key-value storage)
- **AI**: Cloud API (OpenAI/Anthropic) - NOT local inference yet
- **Architecture**: Clean Architecture + MVVM

### Folder Structure
```
lib/
├── core/               # Constants, utils, errors
├── features/           # Feature modules (cards, game, relationships)
│   ├── cards/
│   │   ├── data/      # Models, repositories
│   │   ├── domain/    # Entities, use cases
│   │   └── presentation/ # UI, controllers
├── shared/            # Shared services, widgets
└── main.dart
```

### Key Concepts

**Cards**: Atomic units of content (activities, NPCs, places, etc.)  
**Turns**: 3 per day (Morning, Afternoon, Evening)  
**Seasons**: 12-36 week story arcs with aspirations  
**Relationships**: NPCs with levels (0-5) and trust (0.0-1.0)  
**Evolution**: Cards become personalized through use

---

## Getting Started in 10 Minutes

### Prerequisites
```bash
# Check Flutter installation
flutter doctor -v

# Should show:
# ✓ Flutter 3.24.0+
# ✓ Dart 3.5.0+
# ✓ Android toolchain (for Android)
# ✓ Xcode (for iOS, macOS only)
```

### Setup Project

```bash
# 1. Clone repository
git clone <repo_url>
cd unwritten/

# 2. Create Flutter project
flutter create --org com.unwritten unwritten_flutter
cd unwritten_flutter/

# 3. Copy project structure (see FLUTTER-PROJECT-SETUP.md)
# (Run the mkdir commands from setup guide)

# 4. Install dependencies
flutter pub get

# 5. Run app
flutter run
```

### First Contribution Path

**Option A: Implement a card type**
1. Read `docs/7.schema/base-card-schema-v1.md`
2. Implement `CardModel` in `lib/features/cards/data/models/card_model.dart`
3. Write unit tests
4. Submit PR

**Option B: Build a UI component**
1. Read Phase 1 deliverables in `IMPLEMENTATION-PLAN-MVP.md`
2. Implement `CardWidget` in `lib/features/cards/presentation/widgets/card_widget.dart`
3. Add to `PlaceholderScreen` for testing
4. Submit PR

**Option C: Set up game constants**
1. Implement `GameConstants` in `lib/core/constants/game_constants.dart`
2. Reference values from Master Truths v1.2
3. Write tests validating constants
4. Submit PR

---

## Essential Reading (Priority Order)

### Must Read First
1. **Master Truths v1.2** (`docs/master_truths_canonical_spec_v_1_2.md`)
   - Single source of truth for all systems
   - ~20 minute read
   - Reference constantly

2. **Implementation Plan** (`docs/5.architecture/IMPLEMENTATION-PLAN-MVP.md`)
   - Phase-by-phase roadmap
   - Current phase priorities
   - Success criteria

3. **Flutter Setup Guide** (`docs/5.architecture/FLUTTER-PROJECT-SETUP.md`)
   - Step-by-step project setup
   - Dependency configuration
   - Verification steps

### Read When Implementing

4. **Base Card Schema** (`docs/7.schema/base-card-schema-v1.md`)
   - Card JSON structure
   - All card types explained
   - Validation rules

5. **Concept Docs** (`docs/1.concept/`)
   - Game vision and systems
   - Read specific docs as needed for features

6. **Gameplay Docs** (`docs/2.gameplay/`)
   - Detailed mechanics
   - Reference when implementing specific systems

---

## Key Rules & Standards

### File Naming
```
✅ CORRECT:
  - card_model.dart
  - game_state_controller.dart
  - npc_response_request.dart

❌ WRONG:
  - CardModel.dart
  - gameStateController.dart
  - NPCResponseRequest.dart
```

### Documentation
```dart
✅ CORRECT:
/// Plays a card in the current game context.
/// 
/// Validates resource costs, applies effects to game state,
/// and returns updated state with narrative outcome.
/// 
/// Throws [InsufficientResourcesException] if costs cannot be paid.
Future<CardPlayResult> playCard(String cardId);

❌ WRONG:
// Plays card
Future<CardPlayResult> playCard(String cardId);
```

### Logging
```dart
✅ CORRECT:
AppLogger.info('Card played', data: {
  'card_id': cardId,
  'turn': currentTurn,
});

❌ WRONG:
print('Card played: $cardId');
```

### Constants
```dart
✅ CORRECT:
if (trust >= GameConstants.relationshipLevel3TrustMin) {
  // Level up to Friend
}

❌ WRONG:
if (trust >= 0.4) { // Magic number!
  // Level up to Friend
}
```

---

## Common Tasks

### Adding a New Card Type

1. **Define card in JSON** (`assets/data/base_cards.json`):
```json
{
  "id": "act_new_activity_001",
  "type": "activity",
  "title": "New Activity",
  "description": "Description here...",
  "costs": {"energy": 2.0},
  "effects": {"mood_impact": 0.3},
  "evolution_level": 0
}
```

2. **Test card loads**:
```dart
test('should load new card from JSON', () {
  final card = CardModel.fromJson(jsonData);
  expect(card.id, 'act_new_activity_001');
});
```

3. **Verify in UI**: Card appears in hand

### Implementing a Use Case

```dart
// 1. Define in domain layer
class PlayCardUsecase {
  Future<CardPlayResult> execute(String cardId, PlayContext context);
}

// 2. Implement in data layer
class PlayCardUsecaseImpl implements PlayCardUsecase {
  // Implementation with repository calls
}

// 3. Wire up with Riverpod
final playCardUsecaseProvider = Provider<PlayCardUsecase>((ref) {
  return PlayCardUsecaseImpl(ref.read(gameRepositoryProvider));
});

// 4. Use in controller
ref.read(playCardUsecaseProvider).execute(cardId, context);
```

### Adding a New Screen

```dart
// 1. Create screen widget
class NewScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Use ref.watch() for state
    final gameState = ref.watch(gameStateProvider);
    
    return Scaffold(
      appBar: AppBar(title: Text('New Screen')),
      body: // Your UI here
    );
  }
}

// 2. Add navigation
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => NewScreen()),
);
```

---

## Testing Strategy

### Unit Tests (Required)
```dart
// Test data models
test('CardModel should serialize to/from JSON', () {
  final card = CardModel(...);
  final json = card.toJson();
  final restored = CardModel.fromJson(json);
  expect(restored, equals(card));
});

// Test use cases
test('PlayCardUsecase should deduct costs', () async {
  final result = await usecase.execute('card_id', context);
  expect(result.updatedState.resources.energy, equals(8.0));
});
```

### Widget Tests (For UI Components)
```dart
testWidgets('CardWidget displays title and description', (tester) async {
  await tester.pumpWidget(CardWidget(card: testCard));
  
  expect(find.text('Card Title'), findsOneWidget);
  expect(find.text('Card description'), findsOneWidget);
});
```

### Integration Tests (For Flows)
```dart
testWidgets('Can play card and see narrative', (tester) async {
  await tester.pumpWidget(MyApp());
  
  await tester.tap(find.byType(CardWidget).first);
  await tester.pumpAndSettle();
  
  expect(find.byType(NarrativePanel), findsOneWidget);
});
```

---

## Code Review Checklist

Before submitting PR:
- [ ] Code follows snake_case naming
- [ ] Public APIs documented with `///` comments
- [ ] Uses `AppLogger` instead of `print()`
- [ ] References `GameConstants` instead of magic numbers
- [ ] Proper dispose() for controllers/streams
- [ ] Unit tests written and passing
- [ ] `flutter analyze` shows no errors
- [ ] `dart format .` applied
- [ ] Follows Clean Architecture layers (data/domain/presentation)

---

## Debugging Tips

### Common Issues

**"Card not found" errors**
- Check card JSON syntax
- Verify card ID matches exactly
- Ensure `assets/` in pubspec.yaml

**State not updating**
- Use `StateNotifier.state = newState` not `state.field = value`
- Verify provider is being watched with `ref.watch()`
- Check if state is immutable

**AI API errors**
- Verify API key in environment
- Check internet connection
- Look for rate limiting (429 errors)

### Useful Commands

```bash
# Hot reload
r (in Flutter console)

# Hot restart
R (in Flutter console)

# Clear build cache
flutter clean
flutter pub get

# Run tests
flutter test

# Profile performance
flutter run --profile

# Check for outdated packages
flutter pub outdated
```

---

## Communication & Support

### Asking Questions

**Good Question**:
> "I'm implementing the relationship level-up system. Master Truths v1.2 says level-up requires both interaction count AND trust threshold. Should I check both in `RelationshipLevelCalculator.canLevelUp()` or in the use case?"

**Better Question**:
> "Implementing relationship level-up (Phase 4). Question about where to validate requirements:
> 
> Context: Master Truths v1.2 Section 2 specifies both interaction count AND trust threshold required.
> 
> Option A: Validate in `RelationshipLevelCalculator` (domain service)  
> Option B: Validate in `LevelUpRelationshipUsecase` (use case)
> 
> I think Option A because it's business logic, but want to confirm architecture pattern."

### Resources

- **Master Truths**: `docs/master_truths_canonical_spec_v_1_2.md`
- **Implementation Plan**: `docs/5.architecture/IMPLEMENTATION-PLAN-MVP.md`
- **Discord**: [Join here] (if available)
- **GitHub Issues**: Tag with phase number (e.g., `[Phase 1]`)

---

## Success Milestones

### Week 1: Environment Setup
- ✅ Flutter installed and working
- ✅ Project compiles and runs
- ✅ Can navigate codebase
- ✅ First PR merged (even if small)

### Week 2: Feature Implementation
- ✅ Implemented a card type or UI component
- ✅ Written unit tests
- ✅ Familiar with state management pattern

### Week 3: Architecture Understanding
- ✅ Can explain Clean Architecture layers
- ✅ Understands game loop flow
- ✅ Can implement full feature (data → domain → presentation)

### Month 1: Core Contributor
- ✅ Contributed to multiple phases
- ✅ Comfortable with Master Truths v1.2
- ✅ Can review others' PRs
- ✅ Understands training data strategy

---

## Next Steps

1. **Read Master Truths v1.2** (30 minutes)
2. **Set up Flutter project** (20 minutes)
3. **Pick first task** from Phase 1 deliverables
4. **Implement & test** (1-2 hours)
5. **Submit PR** with clear description
6. **Iterate** based on feedback

**Welcome to Unwritten! Let's build something amazing.** 🎴✨

---

## Compliance Checklist

- [x] References Master Truths v1.2
- [x] Follows snake_case naming convention
- [x] Uses structured logging (AppLogger)
- [x] References GameConstants
- [x] This doc cites **Truths v1.2**

---

**Document Version**: 1.0  
**Last Updated**: October 14, 2025  
**Status**: Ready for use

