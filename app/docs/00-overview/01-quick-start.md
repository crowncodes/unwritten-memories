# Quick Start Guide

## Prerequisites

- **Flutter SDK:** 3.24.0 or higher
- **Dart SDK:** 3.0 or higher
- **IDE:** VS Code or Android Studio with Flutter extensions
- **Devices:** iOS Simulator, Android Emulator, or Chrome (web)

## Setup

### 1. Clone and Install

```bash
cd app
flutter pub get
```

### 2. Run the App

```bash
# Web (fastest for development)
flutter run -d chrome --hot

# iOS Simulator
flutter run -d ios

# Android Emulator
flutter run -d android
```

### 3. Verify Installation

Check for errors:

```bash
flutter analyze
flutter test
```

## Project Structure

```
app/lib/
├── core/              # Constants, errors, utilities
├── features/          # Feature modules (cards, game, ai)
│   ├── cards/
│   ├── game/
│   └── ai/
├── shared/            # Shared widgets and services
└── main.dart          # App entry point
```

## Environment Variables

### Gemini API Key (for image generation)

```bash
flutter run --dart-define=GEMINI_API_KEY=your_key_here
```

### Firebase reCAPTCHA Site Key (web only)

```bash
flutter run -d chrome --dart-define=RECAPTCHA_SITE_KEY=your_site_key
```

## First Feature: Create a Card Component

```dart
// lib/features/cards/presentation/components/my_card.dart
import 'package:flame/components.dart';

class MyCard extends SpriteComponent with TapCallbacks {
  @override
  Future<void> onLoad() async {
    sprite = await Sprite.load('cards/example.png');
    size = Vector2(120, 168);
    anchor = Anchor.center;
  }
  
  @override
  void onTapDown(TapDownEvent event) {
    print('Card tapped!');
  }
}
```

## Development Workflow

1. **Make changes** to code
2. **Hot reload:** Press `r` in terminal or IDE
3. **Hot restart:** Press `R` for full restart
4. **Check linter:** `flutter analyze`
5. **Run tests:** `flutter test`

## Performance Monitoring

Enable performance overlay:

```dart
MaterialApp(
  showPerformanceOverlay: true,  // Shows FPS
)
```

Use DevTools:

```bash
flutter pub global activate devtools
flutter pub global run devtools
```

## Common Issues

### Build Errors

```bash
flutter clean
flutter pub get
flutter run
```

### Web CORS Issues

Use Chrome with disabled security (dev only):

```bash
flutter run -d chrome --web-browser-flag "--disable-web-security"
```

---

**Next:** [Performance Targets](./02-performance-targets.md)  
**Related:** [Setup Guide](../SETUP.md), [Architecture](../01-architecture/01-project-structure.md)


