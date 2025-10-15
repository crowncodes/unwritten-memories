# Testing Strategy

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete

---

## Testing Pyramid

```
      /\
     /  \  Integration (10%)
    /____\
   /      \
  / Widget \ (30%)
 /__________\
/    Unit    \ (60%)
/______________\
```

---

## Unit Tests

### Provider Tests

```dart
void main() {
  group('CardNotifier', () {
    late ProviderContainer container;
    
    setUp(() {
      container = ProviderContainer();
    });
    
    tearDown(() {
      container.dispose();
    });
    
    test('loads cards on init', () async {
      final cards = await container.read(cardNotifierProvider.future);
      expect(cards, isNotEmpty);
    });
    
    test('playCard removes card', () async {
      final notifier = container.read(cardNotifierProvider.notifier);
      await container.read(cardNotifierProvider.future);
      
      await notifier.playCard('card-1');
      
      final state = container.read(cardNotifierProvider).value!;
      expect(state.any((c) => c.id == 'card-1'), false);
    });
  });
}
```

---

## Widget Tests

```dart
testWidgets('CardWidget displays card data', (tester) async {
  await tester.pumpWidget(
    ProviderScope(
      child: MaterialApp(
        home: CardWidget(card: testCard),
      ),
    ),
  );
  
  expect(find.text('Test Card'), findsOneWidget);
});
```

---

## Integration Tests

```dart
void main() {
  testWidgets('Complete game flow', (tester) async {
    app.main();
    await tester.pumpAndSettle();
    
    // Draw card
    await tester.tap(find.text('Draw'));
    await tester.pumpAndSettle();
    
    // Play card
    await tester.drag(find.byType(CardWidget), Offset(200, 0));
    await tester.pumpAndSettle();
    
    // Verify state
    expect(find.text('Resources: 2'), findsOneWidget);
  });
}
```

---

## Test Coverage

```bash
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

---

**Status:** ✅ Testing Strategy Complete  
**Target:** 80%+ code coverage

