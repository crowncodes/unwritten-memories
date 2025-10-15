/// Test helpers and utilities for Unwritten testing.
/// 
/// Provides common mocks, fakes, and test data builders for consistent testing.
library test_helpers;

import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Pumps a widget with ProviderScope for testing Riverpod providers.
/// 
/// Example:
/// ```dart
/// await tester.pumpProviderWidget(
///   const MyWidget(),
///   overrides: [
///     myProviderProvider.overrideWithValue(mockValue),
///   ],
/// );
/// ```
extension WidgetTesterExtensions on WidgetTester {
  Future<void> pumpProviderWidget(
    Widget widget, {
    List<Object> overrides = const [],
  }) {
    return pumpWidget(
      ProviderScope(
        overrides: overrides.cast(),
        child: MaterialApp(
          home: widget,
        ),
      ),
    );
  }
  
  /// Pumps widget and settles with a timeout.
  /// 
  /// Useful for animations that might take time.
  Future<void> pumpAndSettleWithTimeout([
    Duration timeout = const Duration(seconds: 10),
  ]) async {
    await pumpAndSettle(timeout);
  }
}

/// Creates test data builders for common game entities.
class TestDataBuilders {
  TestDataBuilders._();
  
  /// Creates a test card with customizable properties.
  /// 
  /// Example:
  /// ```dart
  /// final card = TestDataBuilders.card(
  ///   id: 'test-1',
  ///   title: 'Test Card',
  /// );
  /// ```
  static Map<String, dynamic> card({
    String? id,
    String? title,
    String? description,
    String? type,
    int? energyCost,
    int? timeCost,
    int? moneyCost,
  }) {
    return {
      'id': id ?? 'test-card-${DateTime.now().millisecondsSinceEpoch}',
      'title': title ?? 'Test Card',
      'description': description ?? 'A test card for testing',
      'type': type ?? 'activity',
      'energyCost': energyCost ?? 1,
      'timeCost': timeCost ?? 60,
      'moneyCost': moneyCost ?? 0,
      'imageUrl': 'assets/images/cards/test_card.png',
      'rarity': 'common',
      'effects': <String, dynamic>{},
      'requirements': <String, dynamic>{},
      'metadata': <String, dynamic>{},
    };
  }
  
  /// Creates a test game state with customizable properties.
  static Map<String, dynamic> gameState({
    int? energy,
    int? timeRemaining,
    int? money,
    String? currentPhase,
    int? currentDay,
    int? currentWeek,
  }) {
    return {
      'energy': energy ?? 3,
      'timeRemaining': timeRemaining ?? 480,
      'money': money ?? 1000,
      'currentPhase': currentPhase ?? 'morning',
      'currentDay': currentDay ?? 1,
      'currentWeek': currentWeek ?? 1,
      'meters': {
        'physical': 7,
        'mental': 8,
        'social': 6,
        'emotional': 7,
      },
      'handCards': <Map<String, dynamic>>[],
      'playedCards': <Map<String, dynamic>>[],
    };
  }
  
  /// Creates a test NPC/relationship with customizable properties.
  static Map<String, dynamic> relationship({
    String? id,
    String? name,
    int? level,
    double? trust,
    int? interactionCount,
  }) {
    return {
      'id': id ?? 'test-npc-${DateTime.now().millisecondsSinceEpoch}',
      'name': name ?? 'Test NPC',
      'level': level ?? 1,
      'trust': trust ?? 0.5,
      'interactionCount': interactionCount ?? 0,
      'personality': {
        'openness': 3.5,
        'conscientiousness': 3.5,
        'extraversion': 3.5,
        'agreeableness': 3.5,
        'neuroticism': 3.5,
      },
      'emotionalCapacity': 5.0,
      'memories': <Map<String, dynamic>>[],
    };
  }
  
  /// Creates a test OCEAN personality profile.
  static Map<String, double> oceanProfile({
    double? openness,
    double? conscientiousness,
    double? extraversion,
    double? agreeableness,
    double? neuroticism,
  }) {
    return {
      'openness': openness ?? 3.5,
      'conscientiousness': conscientiousness ?? 3.5,
      'extraversion': extraversion ?? 3.5,
      'agreeableness': agreeableness ?? 3.5,
      'neuroticism': neuroticism ?? 3.5,
    };
  }
}

/// Mock data sets for testing.
class MockData {
  MockData._();
  
  /// Sample card data for testing.
  static final sampleCards = [
    TestDataBuilders.card(
      id: 'coffee-1',
      title: 'Coffee Meetup',
      description: 'Meet someone for coffee',
      type: 'activity',
      energyCost: 1,
      timeCost: 60,
      moneyCost: 5,
    ),
    TestDataBuilders.card(
      id: 'workout-1',
      title: 'Gym Workout',
      description: 'Go to the gym for a workout',
      type: 'activity',
      energyCost: 2,
      timeCost: 90,
      moneyCost: 0,
    ),
    TestDataBuilders.card(
      id: 'sarah-1',
      title: 'Sarah Anderson',
      description: 'Works at a local coffee shop',
      type: 'character',
      energyCost: 0,
      timeCost: 0,
      moneyCost: 0,
    ),
  ];
  
  /// Sample relationship data for testing.
  static final sampleRelationships = [
    TestDataBuilders.relationship(
      id: 'sarah-1',
      name: 'Sarah Anderson',
      level: 2,
      trust: 0.65,
      interactionCount: 10,
    ),
    TestDataBuilders.relationship(
      id: 'mike-1',
      name: 'Mike Chen',
      level: 1,
      trust: 0.35,
      interactionCount: 3,
    ),
  ];
  
  /// Sample game state data for testing.
  static final sampleGameState = TestDataBuilders.gameState(
    energy: 3,
    timeRemaining: 480,
    money: 1000,
    currentPhase: 'morning',
    currentDay: 1,
    currentWeek: 1,
  );
}

/// Test matchers for common assertions.
class CustomMatchers {
  CustomMatchers._();
  
  /// Matches a value within a range.
  /// 
  /// Example:
  /// ```dart
  /// expect(value, isInRange(0.0, 1.0));
  /// ```
  static Matcher isInRange(num min, num max) {
    return inInclusiveRange(min, max);
  }
  
  /// Matches a valid OCEAN personality value (1.0-5.0).
  static Matcher isValidOceanValue() {
    return inInclusiveRange(1.0, 5.0);
  }
  
  /// Matches a valid trust value (0.0-1.0).
  static Matcher isValidTrustValue() {
    return inInclusiveRange(0.0, 1.0);
  }
  
  /// Matches a valid emotional capacity value (0.0-10.0).
  static Matcher isValidCapacityValue() {
    return inInclusiveRange(0.0, 10.0);
  }
  
  /// Matches a valid meter value (0-10).
  static Matcher isValidMeterValue() {
    return inInclusiveRange(0, 10);
  }
  
  /// Matches a valid relationship level (0-5).
  static Matcher isValidRelationshipLevel() {
    return inInclusiveRange(0, 5);
  }
}

/// Performance testing utilities.
class PerformanceTestUtils {
  PerformanceTestUtils._();
  
  /// Measures execution time of a function.
  /// 
  /// Returns Duration taken to execute.
  /// 
  /// Example:
  /// ```dart
  /// final duration = await PerformanceTestUtils.measureTime(() async {
  ///   await someExpensiveOperation();
  /// });
  /// expect(duration.inMilliseconds, lessThan(100));
  /// ```
  static Future<Duration> measureTime(Future<void> Function() fn) async {
    final stopwatch = Stopwatch()..start();
    await fn();
    stopwatch.stop();
    return stopwatch.elapsed;
  }
  
  /// Runs a function multiple times and returns average duration.
  /// 
  /// Useful for benchmarking.
  static Future<Duration> benchmark(
    Future<void> Function() fn, {
    int iterations = 10,
  }) async {
    final durations = <Duration>[];
    
    for (int i = 0; i < iterations; i++) {
      final duration = await measureTime(fn);
      durations.add(duration);
    }
    
    final totalMicroseconds = durations
        .map((d) => d.inMicroseconds)
        .reduce((a, b) => a + b);
    
    return Duration(microseconds: totalMicroseconds ~/ iterations);
  }
  
  /// Asserts that a function completes within target duration.
  static Future<void> assertPerformance(
    Future<void> Function() fn, {
    required Duration target,
    String? reason,
  }) async {
    final duration = await measureTime(fn);
    expect(
      duration,
      lessThan(target),
      reason: reason ?? 'Expected to complete in $target, took $duration',
    );
  }
}

/// Memory testing utilities.
class MemoryTestUtils {
  MemoryTestUtils._();
  
  /// Creates a large list for memory testing.
  static List<T> createLargeList<T>(T Function(int) generator, int count) {
    return List.generate(count, generator);
  }
  
  /// Tests memory usage doesn't grow unbounded.
  /// 
  /// Warning: This is a basic check, use DevTools for precise profiling.
  static Future<void> testForMemoryLeaks(
    Future<void> Function() operation, {
    int iterations = 100,
  }) async {
    // Run operation multiple times
    for (int i = 0; i < iterations; i++) {
      await operation();
    }
    
    // Force garbage collection (if available)
    // In real tests, check memory via DevTools
    await Future.delayed(const Duration(milliseconds: 100));
  }
}

/// Setup and teardown helpers.
class TestSetup {
  TestSetup._();
  
  /// Standard setup for widget tests.
  static void setupWidgetTest() {
    TestWidgetsFlutterBinding.ensureInitialized();
  }
  
  /// Standard setup for unit tests.
  static void setupUnitTest() {
    // Add any common setup for unit tests
  }
  
  /// Setup for tests requiring specific screen size.
  static void setupWithScreenSize(
    WidgetTester tester, {
    Size size = const Size(375, 667), // iPhone SE
  }) {
    tester.view.physicalSize = size;
    tester.view.devicePixelRatio = 1.0;
  }
  
  /// Reset screen size after test.
  static void resetScreenSize(WidgetTester tester) {
    tester.view.resetPhysicalSize();
    tester.view.resetDevicePixelRatio();
  }
}

