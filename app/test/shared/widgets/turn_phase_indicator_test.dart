import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:unwritten/features/game/data/models/turn_phase.dart';
import 'package:unwritten/shared/widgets/turn_phase_indicator.dart';

void main() {
  group('TurnPhaseIndicator', () {
    testWidgets('should display week and day number', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: TurnPhaseIndicator(
              currentWeek: 3,
              currentDay: 5,
              currentTurn: TurnPhase.afternoon,
            ),
          ),
        ),
      );

      expect(find.text('Week 3, Day 5'), findsOneWidget);
    });

    testWidgets('should display day name', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: TurnPhaseIndicator(
              currentWeek: 1,
              currentDay: 1,
              currentTurn: TurnPhase.morning,
            ),
          ),
        ),
      );

      expect(find.text('Monday'), findsOneWidget);
    });

    testWidgets('should display turn phase name', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: TurnPhaseIndicator(
              currentWeek: 1,
              currentDay: 1,
              currentTurn: TurnPhase.morning,
            ),
          ),
        ),
      );

      expect(find.text('Morning'), findsOneWidget);
    });

    testWidgets('should display morning icon', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: TurnPhaseIndicator(
              currentWeek: 1,
              currentDay: 1,
              currentTurn: TurnPhase.morning,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.wb_sunny), findsOneWidget);
    });

    testWidgets('should display afternoon icon', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: TurnPhaseIndicator(
              currentWeek: 1,
              currentDay: 1,
              currentTurn: TurnPhase.afternoon,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.wb_twilight), findsOneWidget);
    });

    testWidgets('should display evening icon', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: TurnPhaseIndicator(
              currentWeek: 1,
              currentDay: 1,
              currentTurn: TurnPhase.evening,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.nightlight), findsOneWidget);
    });

    testWidgets('should display calendar icon', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: TurnPhaseIndicator(
              currentWeek: 1,
              currentDay: 1,
              currentTurn: TurnPhase.morning,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.calendar_today), findsOneWidget);
    });
  });
}

