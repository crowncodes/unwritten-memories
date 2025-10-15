/// Basic smoke test for Unwritten app initialization.
/// 
/// Verifies that the app starts correctly and displays the game screen.

import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:unwritten/main.dart';
import 'package:unwritten/features/game/presentation/screens/game_screen_flame.dart';

void main() {
  testWidgets('App smoke test - loads game screen', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(
      const ProviderScope(
        child: UnwrittenApp(),
      ),
    );

    // Let the app initialize
    await tester.pump();

    // Verify that the game screen is displayed
    expect(find.byType(GameScreenFlame), findsOneWidget);
    
    // Verify app title in AppBar
    expect(find.text('Unwritten'), findsOneWidget);
  });
}
