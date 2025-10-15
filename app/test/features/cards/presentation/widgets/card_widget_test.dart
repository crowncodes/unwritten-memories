import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:unwritten/features/cards/data/models/card_model.dart';
import 'package:unwritten/features/cards/data/models/card_type.dart';
import 'package:unwritten/features/cards/presentation/widgets/card_widget.dart';

void main() {
  group('CardWidget', () {
    late CardModel testCard;

    setUp(() {
      testCard = const CardModel(
        id: 'test_card_001',
        type: CardType.activity,
        title: 'Test Activity',
        description: 'A test activity for widget testing',
        costs: {'energy': 2.0, 'time': 1.0},
        effects: {'mood_boost': 0.5},
      );
    });

    testWidgets('should display card title', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CardWidget(card: testCard),
          ),
        ),
      );

      expect(find.text('Test Activity'), findsOneWidget);
    });

    testWidgets('should display card description', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CardWidget(card: testCard),
          ),
        ),
      );

      expect(find.text('A test activity for widget testing'), findsOneWidget);
    });

    testWidgets('should display costs', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CardWidget(card: testCard),
          ),
        ),
      );

      expect(find.textContaining('Energy'), findsOneWidget);
      expect(find.textContaining('Time'), findsOneWidget);
    });

    testWidgets('should display effects', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CardWidget(card: testCard),
          ),
        ),
      );

      expect(find.textContaining('Mood Boost'), findsOneWidget);
    });

    testWidgets('should call onTap when tapped and playable', (tester) async {
      var tapped = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CardWidget(
              card: testCard,
              onTap: () => tapped = true,
              isPlayable: true,
            ),
          ),
        ),
      );

      await tester.tap(find.byType(InkWell));
      await tester.pump();

      expect(tapped, isTrue);
    });

    testWidgets('should not call onTap when not playable', (tester) async {
      var tapped = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CardWidget(
              card: testCard,
              onTap: () => tapped = true,
              isPlayable: false,
            ),
          ),
        ),
      );

      await tester.tap(find.byType(InkWell));
      await tester.pump();

      expect(tapped, isFalse);
    });

    testWidgets('should show evolution badge when evolved', (tester) async {
      final evolvedCard = testCard.copyWith(evolutionLevel: 2);

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CardWidget(card: evolvedCard),
          ),
        ),
      );

      expect(find.text('Lvl 2'), findsOneWidget);
      expect(find.byIcon(Icons.auto_awesome), findsOneWidget);
    });

    testWidgets('should not show evolution badge at level 0', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CardWidget(card: testCard),
          ),
        ),
      );

      expect(find.text('Lvl 0'), findsNothing);
    });
  });
}

