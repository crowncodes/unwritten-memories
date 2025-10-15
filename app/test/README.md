# Unwritten Testing Guide

## Test Structure

```
test/
├── helpers/
│   └── test_helpers.dart           # Common test utilities
├── core/
│   └── [mirrors lib/core]          # Core functionality tests
├── features/
│   └── [mirrors lib/features]      # Feature tests
├── shared/
│   └── [mirrors lib/shared]        # Shared component tests
└── integration/
    └── game_flow_test.dart         # End-to-end tests
```

## Testing Strategy

### Unit Tests (TDD Preferred)
- Test individual classes and functions
- Fast, isolated, no dependencies
- Target: >80% code coverage
- Location: Mirror `lib/` structure

### Widget Tests
- Test individual widgets and their interactions
- Use `test_helpers.dart` utilities
- Test both UI and behavior

### Integration Tests
- Test complete user flows
- Test system interactions
- Test performance and memory

## Running Tests

```bash
# All tests
flutter test

# Specific test file
flutter test test/features/cards/data/models/card_model_test.dart

# With coverage
flutter test --coverage

# Integration tests only
flutter test test/integration/

# Watch mode (re-run on changes)
flutter test --watch
```

## Test Helpers

### WidgetTesterExtensions
```dart
// Pump widget with Riverpod
await tester.pumpProviderWidget(
  const MyWidget(),
  overrides: [myProvider.overrideWithValue(mockValue)],
);
```

### TestDataBuilders
```dart
// Create test data easily
final card = TestDataBuilders.card(
  title: 'Test Card',
  energyCost: 2,
);

final gameState = TestDataBuilders.gameState(energy: 3);
```

### CustomMatchers
```dart
// Use domain-specific matchers
expect(trust, isValidTrustValue());  // 0.0-1.0
expect(capacity, isValidCapacityValue());  // 0.0-10.0
expect(ocean, isValidOceanValue());  // 1.0-5.0
```

### PerformanceTestUtils
```dart
// Test performance budgets
await PerformanceTestUtils.assertPerformance(
  () async => await expensiveOperation(),
  target: const Duration(milliseconds: 100),
);

// Benchmark operations
final avgDuration = await PerformanceTestUtils.benchmark(
  () async => await operation(),
  iterations: 100,
);
```

## Writing Good Tests

### ✅ DO
- Write tests before implementation (TDD)
- Test behavior, not implementation
- Use descriptive test names
- Use test helpers for common setups
- Test edge cases and error conditions
- Keep tests fast and isolated
- Use const constructors where possible

### ❌ DON'T
- Test private methods (test through public API)
- Make tests dependent on each other
- Use real network calls (mock them)
- Skip error case testing
- Ignore flaky tests (fix them)

## Example Test Structure

```dart
import 'package:flutter_test/flutter_test.dart';
import '../../../helpers/test_helpers.dart';

void main() {
  group('CardModel', () {
    test('creates valid card from JSON', () {
      // Arrange
      final json = TestDataBuilders.card(title: 'Test');
      
      // Act
      final card = CardModel.fromJson(json);
      
      // Assert
      expect(card.title, equals('Test'));
      expect(card.energyCost, isPositive);
    });
    
    test('throws when required field missing', () {
      // Arrange
      final json = <String, dynamic>{'title': 'Test'};
      
      // Act & Assert
      expect(
        () => CardModel.fromJson(json),
        throwsA(isA<FormatException>()),
      );
    });
  });
}
```

## Performance Targets

Tests should verify these targets:
- **60 FPS** gameplay (16.67ms frame budget)
- **<200MB** memory usage
- **<3s** cold start time
- **<100ms** UI response time
- **<15ms** AI inference (local)

## Test Coverage Goals

- **Core logic:** 90%+ coverage
- **Features:** 80%+ coverage
- **Widgets:** 70%+ coverage
- **Integration:** Critical paths covered

## Continuous Integration

Tests run automatically on:
- Every commit (unit + widget tests)
- Pull requests (full test suite)
- Pre-deployment (integration tests)

## Common Issues & Solutions

### Issue: Widget test times out
```dart
// Solution: Increase timeout
await tester.pumpAndSettle(const Duration(seconds: 10));
```

### Issue: Async operation not completing
```dart
// Solution: Ensure proper awaiting
await tester.runAsync(() async {
  await Future.delayed(const Duration(seconds: 1));
});
```

### Issue: Provider not found
```dart
// Solution: Wrap in ProviderScope
await tester.pumpProviderWidget(widget);
```

### Issue: Flaky test
```dart
// Solution: Use pump() with fixed duration instead of pumpAndSettle()
await tester.pump(const Duration(milliseconds: 100));
```

## Resources

- [Flutter Testing Guide](https://docs.flutter.dev/testing)
- [Riverpod Testing](https://riverpod.dev/docs/essentials/testing)
- [Flame Testing](https://docs.flame-engine.org/latest/testing.html)
- [Integration Testing](https://docs.flutter.dev/testing/integration-tests)

