# Flutter Project Setup Guide

> **Canonical Reference**: Master Truths v1.2  
> **Purpose**: Step-by-step setup instructions for Unwritten Flutter project  
> **Last Updated**: October 14, 2025

---

## Prerequisites

### Required Software
- **Flutter SDK**: 3.24.0 or higher
- **Dart SDK**: 3.5.0 or higher (bundled with Flutter)
- **Android Studio**: Latest stable (for Android development)
- **Xcode**: 15.0+ (for iOS development, macOS only)
- **VS Code** or **Android Studio** with Flutter/Dart plugins

### Environment Setup

```bash
# Verify Flutter installation
flutter doctor -v

# Expected output should show:
# ✓ Flutter (Channel stable, 3.24.0+)
# ✓ Dart (3.5.0+)
# ✓ Android toolchain
# ✓ iOS toolchain (macOS only)
```

---

## Project Initialization

### 1. Create Flutter Project

```bash
# Navigate to workspace directory
cd unwritten/

# Create Flutter project
flutter create --org com.unwritten --project-name unwritten unwritten_flutter

# Move into project directory
cd unwritten_flutter/
```

### 2. Configure Project Structure

Create Clean Architecture folder structure:

```bash
# Create core directories
mkdir -p lib/core/constants
mkdir -p lib/core/errors
mkdir -p lib/core/utils
mkdir -p lib/core/performance

# Create feature directories
mkdir -p lib/features/cards/data/models
mkdir -p lib/features/cards/data/repositories
mkdir -p lib/features/cards/domain/entities
mkdir -p lib/features/cards/domain/usecases
mkdir -p lib/features/cards/presentation/widgets
mkdir -p lib/features/cards/presentation/screens
mkdir -p lib/features/cards/presentation/controllers

mkdir -p lib/features/game/data/models
mkdir -p lib/features/game/data/repositories
mkdir -p lib/features/game/domain/entities
mkdir -p lib/features/game/domain/usecases
mkdir -p lib/features/game/domain/services
mkdir -p lib/features/game/presentation/screens
mkdir -p lib/features/game/presentation/controllers
mkdir -p lib/features/game/presentation/widgets

mkdir -p lib/features/relationships/data/models
mkdir -p lib/features/relationships/data/repositories
mkdir -p lib/features/relationships/domain/entities
mkdir -p lib/features/relationships/domain/usecases
mkdir -p lib/features/relationships/domain/services
mkdir -p lib/features/relationships/presentation/widgets

# Create shared directories
mkdir -p lib/shared/widgets
mkdir -p lib/shared/services

# Create assets directories
mkdir -p assets/data
mkdir -p assets/images/cards
mkdir -p assets/images/ui
```

### 3. Update pubspec.yaml

Replace `pubspec.yaml` content with:

```yaml
name: unwritten
description: AI-powered narrative card game
publish_to: 'none'
version: 0.1.0+1

environment:
  sdk: '>=3.5.0 <4.0.0'
  flutter: '>=3.24.0'

dependencies:
  flutter:
    sdk: flutter

  # State Management
  flutter_riverpod: ^2.5.1
  riverpod_annotation: ^2.3.5

  # Local Storage
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  path_provider: ^2.1.3

  # HTTP & API
  http: ^1.2.1
  dio: ^5.4.3+1

  # Utilities
  uuid: ^4.4.0
  intl: ^0.19.0
  equatable: ^2.0.5
  freezed_annotation: ^2.4.1
  json_annotation: ^4.9.0

  # UI
  flutter_animate: ^4.5.0
  google_fonts: ^6.2.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^4.0.0
  
  # Code Generation
  build_runner: ^2.4.9
  riverpod_generator: ^2.4.0
  freezed: ^2.5.2
  json_serializable: ^6.8.0
  hive_generator: ^2.0.1

flutter:
  uses-material-design: true

  assets:
    - assets/data/
    - assets/images/cards/
    - assets/images/ui/
```

### 4. Install Dependencies

```bash
flutter pub get
```

---

## Code Generation Setup

### 1. Create analysis_options.yaml

```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    # Style Rules
    - prefer_const_constructors
    - prefer_const_literals_to_create_immutables
    - prefer_final_fields
    - prefer_final_locals
    - prefer_single_quotes
    - sort_constructors_first
    - sort_unnamed_constructors_first
    - use_key_in_widget_constructors
    
    # Performance
    - avoid_function_literals_in_foreach_calls
    - avoid_unnecessary_containers
    - sized_box_for_whitespace
    
    # Safety
    - avoid_print
    - avoid_returning_null_for_void
    - cancel_subscriptions
    - close_sinks
    - only_throw_errors
    - prefer_void_to_null
    
    # Documentation
    - public_member_api_docs

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
  errors:
    invalid_annotation_target: ignore
```

### 2. Run Code Generation

```bash
# Generate code for first time
flutter pub run build_runner build --delete-conflicting-outputs

# Watch for changes (during development)
flutter pub run build_runner watch --delete-conflicting-outputs
```

---

## Environment Configuration

### 1. Create .env File

Create `.env` in project root:

```env
# AI Service Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Environment
ENVIRONMENT=development

# API Endpoints (for future cloud services)
API_BASE_URL=https://api.unwritten.com
```

### 2. Add .env to .gitignore

```bash
echo ".env" >> .gitignore
```

### 3. Create Environment Config

Create `lib/core/config/environment.dart`:

```dart
/// Environment configuration loaded from .env file.
/// 
/// Contains API keys, endpoints, and environment-specific settings.
class Environment {
  static const String openAIApiKey = String.fromEnvironment(
    'OPENAI_API_KEY',
    defaultValue: '',
  );

  static const String openAIModel = String.fromEnvironment(
    'OPENAI_MODEL',
    defaultValue: 'gpt-4o-mini',
  );

  static const String environment = String.fromEnvironment(
    'ENVIRONMENT',
    defaultValue: 'development',
  );

  static bool get isDevelopment => environment == 'development';
  static bool get isProduction => environment == 'production';
}
```

---

## Run Configuration

### Development Run

```bash
# Run with environment variables
flutter run --dart-define=OPENAI_API_KEY=your_key \
            --dart-define=ENVIRONMENT=development
```

### VS Code Launch Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Unwritten (Development)",
      "request": "launch",
      "type": "dart",
      "program": "lib/main.dart",
      "args": [
        "--dart-define=OPENAI_API_KEY=${env:OPENAI_API_KEY}",
        "--dart-define=ENVIRONMENT=development"
      ]
    },
    {
      "name": "Unwritten (Profile)",
      "request": "launch",
      "type": "dart",
      "program": "lib/main.dart",
      "flutterMode": "profile",
      "args": [
        "--dart-define=OPENAI_API_KEY=${env:OPENAI_API_KEY}",
        "--dart-define=ENVIRONMENT=development"
      ]
    }
  ]
}
```

---

## Initial Project Files

### 1. App Logger

Create `lib/core/utils/app_logger.dart`:

```dart
import 'package:flutter/foundation.dart';

/// Structured logging utility for Unwritten.
/// 
/// Provides categorized logging with automatic debug-mode gating.
/// All logs are no-ops in release builds.
class AppLogger {
  static const _debugMode = kDebugMode;

  /// General information logging.
  static void info(String message, {Map<String, dynamic>? data}) {
    if (_debugMode) {
      print('ℹ️ INFO: $message ${data != null ? '- $data' : ''}');
    }
  }

  /// Performance metric logging.
  /// 
  /// Only logs if operation took > 16ms (one frame at 60fps).
  static void performance(String operation, Duration duration) {
    if (_debugMode && duration.inMilliseconds > 16) {
      print('⚠️ PERF: $operation took ${duration.inMilliseconds}ms');
    }
  }

  /// AI/ML specific event logging.
  static void ai(String event, {Map<String, dynamic>? metrics}) {
    if (_debugMode) {
      print('🤖 AI: $event ${metrics != null ? '- $metrics' : ''}');
    }
  }

  /// Error logging with optional stack trace.
  static void error(String message, Object error, [StackTrace? stack]) {
    print('❌ ERROR: $message - $error');
    if (stack != null && _debugMode) {
      print(stack);
    }
  }

  /// Warning logging.
  static void warning(String message, {Map<String, dynamic>? data}) {
    if (_debugMode) {
      print('⚠️ WARNING: $message ${data != null ? '- $data' : ''}');
    }
  }
}
```

### 2. Game Constants

Create `lib/core/constants/game_constants.dart`:

```dart
/// Canonical game constants from Master Truths v1.2.
/// 
/// All numerical values and scales defined here.
/// DO NOT hardcode these values elsewhere - reference this file.
class GameConstants {
  // Time Structure
  static const int turnsPerDay = 3;
  static const int daysPerWeek = 7;
  
  // Season Lengths
  static const int seasonLengthStandard = 12; // weeks
  static const int seasonLengthExtended = 24; // weeks
  static const int seasonLengthEpic = 36; // weeks
  
  // Relationship Scale
  static const int relationshipLevelMin = 0; // Not Met (internal only)
  static const int relationshipLevelMax = 5; // Soulmate/Best Friend
  static const double trustMin = 0.0;
  static const double trustMax = 1.0;
  
  // Relationship Level Thresholds (interaction counts)
  static const int relationshipLevel1Threshold = 1; // Stranger
  static const int relationshipLevel2Threshold = 6; // Acquaintance
  static const int relationshipLevel3Threshold = 16; // Friend
  static const int relationshipLevel4Threshold = 31; // Close Friend
  static const int relationshipLevel5Threshold = 76; // Soulmate
  
  // Relationship Level Trust Requirements
  static const double relationshipLevel1TrustMin = 0.0;
  static const double relationshipLevel2TrustMin = 0.2;
  static const double relationshipLevel3TrustMin = 0.4;
  static const double relationshipLevel4TrustMin = 0.6;
  static const double relationshipLevel5TrustMin = 0.8;
  
  // Emotional Capacity
  static const double emotionalCapacityMin = 0.0;
  static const double emotionalCapacityMax = 10.0;
  static const double emotionalCapacityDefault = 5.0;
  static const double emotionalCapacityCrisis = 1.0;
  static const double emotionalCapacityLow = 5.0;
  static const double emotionalCapacityHigh = 8.0;
  
  // NPC Response Framework - Urgency Multipliers
  static const double urgencyMultiplierRoutine = 1.0;
  static const double urgencyMultiplierImportant = 2.0;
  static const double urgencyMultiplierUrgent = 3.0;
  static const double urgencyMultiplierCrisis = 5.0;
  
  // NPC Response Framework - Trust Modifiers
  static const double trustModifierLow = 0.5;
  static const double trustModifierNeutral = 1.0;
  static const double trustModifierHigh = 2.0;
  
  // Resources
  static const double energyDefault = 10.0;
  static const double energyMax = 10.0;
  static const double moneyDefault = 100.0;
  static const double timePerTurn = 1.0;
  static const double socialCapitalDefault = 0.0;
  
  // Novel-Quality Thresholds
  static const double qualityThresholdEmotionalAuthenticity = 0.7;
  static const double qualityThresholdTensionBuilding = 0.6;
  static const double qualityThresholdDramaticIrony = 0.5;
  static const double qualityThresholdHookEffectiveness = 0.6;
  static const double qualityThresholdOverall = 0.7;
  
  // Essence Tokens (Monetization)
  static const int essenceTokensDailyFree = 25;
  
  // Pack Sizes
  static const int packSizeStandardMin = 20;
  static const int packSizeStandardMax = 30;
  static const int packSizeDeluxeMin = 35;
  static const int packSizeDeluxeMax = 50;
  static const int packSizeMegaMin = 60;
  static const int packSizeMegaMax = 80;
  
  // Display Strings
  static const String relationshipLevel0Display = 'Not Met';
  static const String relationshipLevel1Display = 'Stranger';
  static const String relationshipLevel2Display = 'Acquaintance';
  static const String relationshipLevel3Display = 'Friend';
  static const String relationshipLevel4Display = 'Close Friend';
  static const String relationshipLevel5Display = 'Soulmate';
  
  // Turn Phases
  static const String turnPhaseMorning = 'Morning';
  static const String turnPhaseAfternoon = 'Afternoon';
  static const String turnPhaseEvening = 'Evening';
}
```

### 3. Main Entry Point

Update `lib/main.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'core/utils/app_logger.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  AppLogger.info('Unwritten starting...');

  runApp(
    const ProviderScope(
      child: UnwrittenApp(),
    ),
  );
}

/// Root application widget.
/// 
/// Sets up theme, routing, and provider scope.
class UnwrittenApp extends StatelessWidget {
  const UnwrittenApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Unwritten',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF6366F1), // Indigo
          brightness: Brightness.light,
        ),
        textTheme: GoogleFonts.interTextTheme(),
        useMaterial3: true,
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF6366F1),
          brightness: Brightness.dark,
        ),
        textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme),
        useMaterial3: true,
      ),
      home: const PlaceholderScreen(),
    );
  }
}

/// Placeholder screen for Phase 1 development.
class PlaceholderScreen extends StatelessWidget {
  const PlaceholderScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Unwritten - Development'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.favorite,
              size: 100,
              color: Theme.of(context).colorScheme.primary,
            ),
            const SizedBox(height: 24),
            Text(
              'Unwritten',
              style: Theme.of(context).textTheme.headlineLarge,
            ),
            const SizedBox(height: 8),
            Text(
              'Phase 1: Foundation Setup',
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## Verification

### Run Checks

```bash
# 1. Analyze code
flutter analyze

# Expected: No issues found!

# 2. Format code
dart format .

# Expected: All files formatted

# 3. Run app
flutter run

# Expected: App launches with "Unwritten - Development" screen
```

### Verify Structure

```bash
# Check folder structure
tree lib/ -L 3

# Expected output:
# lib/
# ├── core/
# │   ├── constants/
# │   │   └── game_constants.dart
# │   └── utils/
# │       └── app_logger.dart
# ├── features/
# │   ├── cards/
# │   ├── game/
# │   └── relationships/
# ├── shared/
# └── main.dart
```

---

## Next Steps

1. ✅ **Project compiles and runs** → Proceed to Phase 1 data models
2. ✅ **All dependencies installed** → Begin implementing card system
3. ✅ **Clean Architecture validated** → Start writing domain entities

See `IMPLEMENTATION-PLAN-MVP.md` for detailed phase roadmap.

---

## Troubleshooting

### Flutter Doctor Issues

```bash
# Android license issues
flutter doctor --android-licenses

# iOS CocoaPods issues
cd ios/
pod install
cd ..
```

### Build Runner Issues

```bash
# Clear build cache
flutter clean
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

### Dependency Conflicts

```bash
# Update dependencies
flutter pub upgrade

# Check for outdated packages
flutter pub outdated
```

---

## Compliance Checklist

- [x] Snake_case file naming convention
- [x] Clean Architecture structure
- [x] Maximum 300 lines per file (enforced via linter)
- [x] Canonical constants referenced (game_constants.dart)
- [x] Structured logging (app_logger.dart)
- [x] This doc cites **Truths v1.2**

---

**Document Version**: 1.0  
**Last Updated**: October 14, 2025  
**Status**: Ready for use

