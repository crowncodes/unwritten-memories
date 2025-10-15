import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:unwritten/features/game/data/models/resources_model.dart';
import 'package:unwritten/shared/widgets/resources_bar.dart';

void main() {
  group('ResourcesBar', () {
    testWidgets('should display all resource values', (tester) async {
      const resources = ResourcesModel(
        energy: 7.5,
        money: 85.0,
        timeRemaining: 2.0,
        socialCapital: 10.0,
      );

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: ResourcesBar(resources: resources),
          ),
        ),
      );

      expect(find.text('7.5/10.0'), findsOneWidget);
      expect(find.text('\$85'), findsOneWidget);
      expect(find.text('2.0'), findsOneWidget);
      expect(find.text('10'), findsOneWidget);
    });

    testWidgets('should display resource labels', (tester) async {
      const resources = ResourcesModel(
        energy: 10.0,
        money: 100.0,
        timeRemaining: 3.0,
        socialCapital: 0.0,
      );

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: ResourcesBar(resources: resources),
          ),
        ),
      );

      expect(find.text('Energy'), findsOneWidget);
      expect(find.text('Money'), findsOneWidget);
      expect(find.text('Time'), findsOneWidget);
      expect(find.text('Social'), findsOneWidget);
    });

    testWidgets('should display resource icons', (tester) async {
      const resources = ResourcesModel(
        energy: 5.0,
        money: 50.0,
        timeRemaining: 1.5,
        socialCapital: 5.0,
      );

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: ResourcesBar(resources: resources),
          ),
        ),
      );

      expect(find.byIcon(Icons.bolt), findsOneWidget);
      expect(find.byIcon(Icons.attach_money), findsOneWidget);
      expect(find.byIcon(Icons.access_time), findsOneWidget);
      expect(find.byIcon(Icons.people), findsOneWidget);
    });
  });
}

