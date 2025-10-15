# Unwritten Flutter App

> **Phase**: 1 (Foundation)  
> **Status**: In Development  
> **Last Updated**: October 14, 2025

---

## Overview

Unwritten is an AI-powered narrative card game built with Flutter. This is the mobile app implementation following Clean Architecture principles with cloud-first AI integration.

**Core Concept**: Players build relationships with AI-powered NPCs, pursue aspirations through seasonal story arcs, and generate personalized novels from their gameplay.

---

## Quick Start

### Prerequisites

- **Flutter SDK**: 3.24.0+
- **Dart SDK**: 3.5.0+ (bundled with Flutter)
- **Android Studio** or **Xcode** (for device builds)
- **VS Code** (recommended) with Flutter/Dart extensions

### Setup

```bash
# 1. Install dependencies
flutter pub get

# 2. Verify setup
flutter doctor -v

# 3. Run code generation (when needed)
flutter pub run build_runner build --delete-conflicting-outputs

# 4. Run app
flutter run
```

### First Time Setup

If this is your first time running Flutter:

```bash
# Check Flutter installation
flutter doctor

# Fix any issues shown (Android licenses, etc.)
flutter doctor --android-licenses

# Run on available device
flutter devices
flutter run -d <device_id>
```

### Firebase Setup

Unwritten uses Firebase for authentication, data storage, and security. Follow these guides to set up Firebase:

#### 📚 Firebase Documentation

| Guide | Purpose |
|-------|---------|
| [Firebase Authentication Setup](docs/FIREBASE_AUTH_SETUP.md) | Configure auth methods, emulators, and testing |
| [Firebase App Check Setup](docs/FIREBASE_APP_CHECK_SETUP.md) | Configure security and abuse prevention |
| [Firebase Integration Summary](docs/FIREBASE_INTEGRATION_COMPLETE.md) | Overview of all Firebase features |

#### Quick Firebase Setup

1. **Create Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project or select existing one
   - Follow the setup wizard

2. **Configure FlutterFire**
   ```bash
   # Install FlutterFire CLI
   dart pub global activate flutterfire_cli
   
   # Configure Firebase for your Flutter app
   flutterfire configure
   ```

3. **Enable Services**
   - **Authentication**: Enable Email/Password and Anonymous
   - **Firestore**: Create database in your region
   - **Storage**: Create default bucket
   - **App Check**: Register your app and get debug tokens

4. **For Local Development**
   - Install Firebase Emulator Suite
   - See [Firebase Auth Setup Guide](docs/FIREBASE_AUTH_SETUP.md) for details

**Note**: The app will run without Firebase, but authentication and cloud features won't work. See the guides above for complete setup instructions.

---

## Project Structure

```
lib/
├── core/                          # Core utilities and constants
│   ├── constants/
│   │   └── game_constants.dart   # Canonical game constants
│   ├── config/
│   │   └── environment.dart      # Environment configuration
│   ├── errors/
│   │   └── exceptions.dart       # Custom exceptions
│   └── utils/
│       └── app_logger.dart       # Structured logging
│
├── features/                      # Feature modules
│   ├── cards/
│   │   ├── data/                 # Data layer (models, repositories)
│   │   ├── domain/               # Business logic (entities, use cases)
│   │   └── presentation/         # UI (screens, widgets, controllers)
│   │
│   ├── game/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   │
│   └── relationships/
│       ├── data/
│       ├── domain/
│       └── presentation/
│
├── shared/                        # Shared across features
│   ├── services/                 # Shared services
│   └── widgets/                  # Reusable widgets
│
└── main.dart                      # App entry point

assets/
├── data/
│   └── base_cards.json           # Card database
└── images/
    ├── cards/                    # Card artwork (future)
    └── ui/                       # UI assets (future)

test/                             # Unit & widget tests
```

---

## Architecture

### Clean Architecture Layers

1. **Data Layer** (`data/`)
   - Models (JSON serialization)
   - Repositories (data access)
   - Data sources (local/remote)

2. **Domain Layer** (`domain/`)
   - Entities (business objects)
   - Use Cases (business logic)
   - Repository interfaces

3. **Presentation Layer** (`presentation/`)
   - Screens (full pages)
   - Widgets (UI components)
   - Controllers (Riverpod state management)

### State Management

Using **Riverpod** for dependency injection and state management:

```dart
// Define provider
final gameStateProvider = StateNotifierProvider<GameStateController, GameStateModel>((ref) {
  return GameStateController(ref.read(gameRepositoryProvider));
});

// Use in widget
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final gameState = ref.watch(gameStateProvider);
    // Use gameState...
  }
}
```

---

## Key Concepts

### Game Constants

All numerical values are defined in `game_constants.dart`:

```dart
// ✅ CORRECT
if (trust >= GameConstants.relationshipLevel3TrustMin) {
  // Level up to Friend
}

// ❌ WRONG - Don't hardcode!
if (trust >= 0.4) {
  // Magic number!
}
```

### Logging

Use `AppLogger` for structured logging:

```dart
import 'package:unwritten/core/utils/app_logger.dart';

// Info logging
AppLogger.info('Card played', data: {
  'card_id': cardId,
  'turn': currentTurn,
});

// Performance logging (only logs if > 16ms)
AppLogger.performance('AI inference', duration);

// Error logging
AppLogger.error('Failed to load card', error, stackTrace);
```

### Card System

Cards are loaded from `assets/data/base_cards.json`:

```dart
final card = CardModel(
  id: 'act_coffee_chat_001',
  type: CardType.activity,
  title: 'Coffee Chat',
  costs: {'energy': 1.0, 'time': 1.0, 'money': 5.0},
  effects: {'relationship_gain': 0.1},
);
```

---

## Development Workflow

### Running the App

```bash
# Development mode (debug)
flutter run

# Profile mode (performance testing)
flutter run --profile

# Release mode (production build)
flutter run --release
```

### Hot Reload & Restart

- **Hot Reload**: Press `r` in terminal (preserves state)
- **Hot Restart**: Press `R` in terminal (resets state)
- **Quit**: Press `q` in terminal

### Code Generation

When adding/modifying models with annotations:

```bash
# One-time build
flutter pub run build_runner build --delete-conflicting-outputs

# Watch mode (rebuilds on file change)
flutter pub run build_runner watch --delete-conflicting-outputs
```

### Code Quality

```bash
# Format code
dart format .

# Analyze code
flutter analyze

# Run tests
flutter test

# Run specific test
flutter test test/features/cards/card_model_test.dart
```

---

## Testing

### Unit Tests

Test data models, use cases, and business logic:

```dart
// test/features/cards/data/models/card_model_test.dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('CardModel', () {
    test('should serialize to/from JSON', () {
      final card = CardModel(/* ... */);
      final json = card.toJson();
      final restored = CardModel.fromJson(json);
      
      expect(restored, equals(card));
    });
  });
}
```

### Widget Tests

Test UI components:

```dart
// test/features/cards/presentation/widgets/card_widget_test.dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('CardWidget displays title', (tester) async {
    await tester.pumpWidget(CardWidget(card: testCard));
    
    expect(find.text('Coffee Chat'), findsOneWidget);
  });
}
```

---

## Common Tasks

### Adding a New Card

1. Edit `assets/data/base_cards.json`
2. Add card JSON object
3. Run app - card automatically loads

### Creating a New Screen

1. Create file: `lib/features/[feature]/presentation/screens/my_screen.dart`
2. Extend `ConsumerWidget` for state access
3. Add navigation from existing screen

### Implementing a Use Case

1. Define interface: `lib/features/[feature]/domain/usecases/my_usecase.dart`
2. Implement: Use repositories from data layer
3. Provide via Riverpod: Create provider
4. Use in controller: `ref.read(myUsecaseProvider).execute()`

---

## Phase 1 Checklist

Current phase deliverables:

- [x] Project structure (Clean Architecture)
- [x] Core utilities (AppLogger, GameConstants)
- [x] Data models (CardModel, GameStateModel, RelationshipModel)
- [x] Base cards JSON (10 starter cards)
- [x] Main app setup with placeholder UI
- [ ] Card loading system
- [ ] Basic UI components (CardWidget, ResourcesBar)
- [ ] Navigation between screens
- [ ] Unit tests for data models

---

## Troubleshooting

### "Package not found" errors

```bash
flutter clean
flutter pub get
```

### Code generation issues

```bash
flutter pub run build_runner clean
flutter pub run build_runner build --delete-conflicting-outputs
```

### Device not detected

```bash
# List available devices
flutter devices

# Start Android emulator
flutter emulators --launch <emulator_id>

# Run on specific device
flutter run -d <device_id>
```

### Hot reload not working

- Try hot restart (`R` key)
- If still broken, stop and `flutter run` again
- Check for compilation errors in terminal

---

## Code Standards

### File Naming

- **snake_case**: `card_model.dart`, `game_state_controller.dart`
- **NOT PascalCase**: ~~`CardModel.dart`~~
- **NOT camelCase**: ~~`cardModel.dart`~~

### Documentation

All public APIs must have doc comments:

```dart
/// Plays a card in the current game context.
/// 
/// Validates resource costs, applies effects to game state,
/// and returns updated state with narrative outcome.
/// 
/// Throws [InsufficientResourcesException] if costs cannot be paid.
Future<CardPlayResult> playCard(String cardId);
```

### Constants

- Define in `game_constants.dart`
- Reference, don't duplicate
- No magic numbers in code

---

## Resources

### Documentation

- **Master Truths v1.2**: `../docs/master_truths_canonical_spec_v_1_2.md`
- **Implementation Plan**: `../docs/5.architecture/IMPLEMENTATION-PLAN-MVP.md`
- **Flutter Setup Guide**: `../docs/5.architecture/FLUTTER-PROJECT-SETUP.md`
- **Quick Start Guide**: `../docs/5.architecture/QUICK-START-DEVELOPER-GUIDE.md`

### Flutter Resources

- [Flutter Documentation](https://docs.flutter.dev/)
- [Riverpod Documentation](https://riverpod.dev/)
- [Dart Language Tour](https://dart.dev/guides/language/language-tour)

---

## Contributing

1. Create feature branch: `git checkout -b feature/my-feature`
2. Follow code standards
3. Write tests
4. Run `flutter analyze` and `dart format .`
5. Submit PR with clear description

---

## License

See LICENSE file in repository root.

---

**Status**: Phase 1 Foundation ✅  
**Next**: Phase 2 Core Game Loop  
**Contact**: [Project maintainer contact]

