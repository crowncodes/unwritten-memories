# Project Structure

## Complete Directory Layout

```
app/
├── lib/
│   ├── core/
│   │   ├── constants/
│   │   │   ├── app_constants.dart
│   │   │   ├── game_constants.dart
│   │   │   └── responsive_breakpoints.dart
│   │   ├── errors/
│   │   │   ├── exceptions.dart
│   │   │   └── failures.dart
│   │   ├── utils/
│   │   │   ├── logger.dart
│   │   │   └── extensions.dart
│   │   └── performance/
│   │       ├── performance_monitor.dart
│   │       └── memory_tracker.dart
│   ├── features/
│   │   ├── cards/
│   │   │   ├── data/
│   │   │   │   ├── models/
│   │   │   │   ├── repositories/
│   │   │   │   └── datasources/
│   │   │   ├── domain/
│   │   │   │   ├── entities/
│   │   │   │   ├── usecases/
│   │   │   │   └── repositories/
│   │   │   └── presentation/
│   │   │       ├── screens/
│   │   │       ├── widgets/
│   │   │       ├── components/    # Flame components
│   │   │       └── providers/
│   │   ├── game/
│   │   └── ai/
│   ├── shared/
│   │   ├── widgets/
│   │   │   ├── loading_indicator.dart
│   │   │   └── error_display.dart
│   │   └── services/
│   │       ├── audio_manager.dart
│   │       ├── haptic_feedback.dart
│   │       └── firebase_service.dart
│   ├── firebase_options.dart
│   └── main.dart
├── assets/
│   ├── images/
│   ├── audio/
│   ├── music/
│   └── data/
├── test/
├── docs/
└── pubspec.yaml
```

## Layer Responsibilities

### Core (`lib/core/`)

Cross-cutting concerns used by all features:
- **constants/** - App-wide constants, breakpoints
- **errors/** - Custom exceptions and failures
- **utils/** - Logging, extensions, helpers
- **performance/** - Performance monitoring utilities

### Features (`lib/features/`)

Self-contained feature modules:
- Each feature has data/domain/presentation
- Minimal cross-feature dependencies
- Use dependency injection for shared services

### Shared (`lib/shared/`)

Reusable across features:
- **widgets/** - Generic UI components
- **services/** - Global services (audio, haptics, Firebase)

## File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Widgets | `*_widget.dart` | `card_widget.dart` |
| Screens | `*_screen.dart` | `game_board_screen.dart` |
| Models | `*_model.dart` | `card_model.dart` |
| Entities | `*.dart` | `card.dart` |
| Services | `*_service.dart` | `audio_service.dart` |
| Providers | `*_provider.dart` | `game_state_provider.dart` |
| Components | `*_component.dart` | `card_component.dart` |

---

**Next:** [Clean Architecture Layers](./02-clean-architecture-layers.md)  
**Index:** [Architecture Index](./00-INDEX.md)


