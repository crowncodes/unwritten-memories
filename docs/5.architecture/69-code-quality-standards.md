# Code Quality Standards

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete

---

## Linter Configuration

### analysis_options.yaml

```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    - always_declare_return_types
    - always_use_package_imports
    - avoid_print
    - prefer_const_constructors
    - prefer_const_literals_to_create_immutables
    - prefer_final_fields
    - require_trailing_commas
    - sort_constructors_first
    - sort_pub_dependencies
    - unawaited_futures

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
  errors:
    invalid_annotation_target: ignore
```

---

## Code Formatting

```bash
# Format all files
dart format .

# Check without modifying
dart format --output=none --set-exit-if-changed .
```

---

## Documentation Standards

### Public API Documentation

```dart
/// Manages AI inference for card interactions.
/// 
/// This service handles:
/// - Personality trait prediction (0.0-1.0 for Big 5)
/// - Sentiment analysis (positive/neutral/negative)
/// 
/// Example:
/// ```dart
/// final service = AIService();
/// await service.initialize();
/// final response = await service.predict(request);
/// ```
class AIService {
  /// Initializes the TensorFlow Lite model.
  /// 
  /// Throws [ModelLoadException] if model file not found.
  Future<void> initialize() async {
    // Implementation
  }
}
```

---

## Pre-Commit Checklist

- [ ] Code formatted (`dart format .`)
- [ ] No linter errors (`flutter analyze`)
- [ ] Tests pass (`flutter test`)
- [ ] Documentation updated
- [ ] No hardcoded values
- [ ] Proper dispose() implementations

---

## Git Commit Standards

```
feat(cards): add drag physics
fix(ai): prevent memory leak in model disposal
perf(game): optimize card rendering with sprite batching
```

**See:** Git commit standards in project rules

---

**Status:** ✅ Code Quality Standards Complete  
**Enforcement:** CI/CD pipeline

