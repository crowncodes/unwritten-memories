import 'package:flutter_test/flutter_test.dart';
import 'package:unwritten/core/constants/game_constants.dart';

void main() {
  group('GameConstants', () {
    test('time structure constants should be correct', () {
      expect(GameConstants.turnsPerDay, 3);
      expect(GameConstants.daysPerWeek, 7);
    });

    test('season length constants should be correct', () {
      expect(GameConstants.seasonLengthStandard, 12);
      expect(GameConstants.seasonLengthExtended, 24);
      expect(GameConstants.seasonLengthEpic, 36);
    });

    test('relationship level bounds should be correct', () {
      expect(GameConstants.relationshipLevelMin, 0);
      expect(GameConstants.relationshipLevelMax, 5);
      expect(GameConstants.trustMin, 0.0);
      expect(GameConstants.trustMax, 1.0);
    });

    test('relationship level thresholds should be in ascending order', () {
      expect(
        GameConstants.relationshipLevel1Threshold,
        lessThan(GameConstants.relationshipLevel2Threshold),
      );
      expect(
        GameConstants.relationshipLevel2Threshold,
        lessThan(GameConstants.relationshipLevel3Threshold),
      );
      expect(
        GameConstants.relationshipLevel3Threshold,
        lessThan(GameConstants.relationshipLevel4Threshold),
      );
      expect(
        GameConstants.relationshipLevel4Threshold,
        lessThan(GameConstants.relationshipLevel5Threshold),
      );
    });

    test('trust requirements should be in ascending order', () {
      expect(
        GameConstants.relationshipLevel1TrustMin,
        lessThan(GameConstants.relationshipLevel2TrustMin),
      );
      expect(
        GameConstants.relationshipLevel2TrustMin,
        lessThan(GameConstants.relationshipLevel3TrustMin),
      );
      expect(
        GameConstants.relationshipLevel3TrustMin,
        lessThan(GameConstants.relationshipLevel4TrustMin),
      );
      expect(
        GameConstants.relationshipLevel4TrustMin,
        lessThan(GameConstants.relationshipLevel5TrustMin),
      );
    });

    test('emotional capacity constants should be valid', () {
      expect(GameConstants.emotionalCapacityMin, 0.0);
      expect(GameConstants.emotionalCapacityMax, 10.0);
      expect(GameConstants.emotionalCapacityDefault, 5.0);
      expect(
        GameConstants.emotionalCapacityDefault,
        greaterThanOrEqualTo(GameConstants.emotionalCapacityMin),
      );
      expect(
        GameConstants.emotionalCapacityDefault,
        lessThanOrEqualTo(GameConstants.emotionalCapacityMax),
      );
    });

    test('urgency multipliers should be in ascending order', () {
      expect(
        GameConstants.urgencyMultiplierRoutine,
        lessThan(GameConstants.urgencyMultiplierImportant),
      );
      expect(
        GameConstants.urgencyMultiplierImportant,
        lessThan(GameConstants.urgencyMultiplierUrgent),
      );
      expect(
        GameConstants.urgencyMultiplierUrgent,
        lessThan(GameConstants.urgencyMultiplierCrisis),
      );
    });

    test('resource defaults should be positive', () {
      expect(GameConstants.energyDefault, greaterThan(0));
      expect(GameConstants.energyMax, greaterThanOrEqualTo(GameConstants.energyDefault));
      expect(GameConstants.moneyDefault, greaterThan(0));
      expect(GameConstants.timePerTurn, greaterThan(0));
    });

    test('quality thresholds should be valid percentages', () {
      final thresholds = [
        GameConstants.qualityThresholdEmotionalAuthenticity,
        GameConstants.qualityThresholdTensionBuilding,
        GameConstants.qualityThresholdDramaticIrony,
        GameConstants.qualityThresholdHookEffectiveness,
        GameConstants.qualityThresholdOverall,
      ];

      for (final threshold in thresholds) {
        expect(threshold, greaterThanOrEqualTo(0.0));
        expect(threshold, lessThanOrEqualTo(1.0));
      }
    });

    test('display strings should not be empty', () {
      expect(GameConstants.relationshipLevel0Display, isNotEmpty);
      expect(GameConstants.relationshipLevel1Display, isNotEmpty);
      expect(GameConstants.relationshipLevel2Display, isNotEmpty);
      expect(GameConstants.relationshipLevel3Display, isNotEmpty);
      expect(GameConstants.relationshipLevel4Display, isNotEmpty);
      expect(GameConstants.relationshipLevel5Display, isNotEmpty);
      expect(GameConstants.turnPhaseMorning, isNotEmpty);
      expect(GameConstants.turnPhaseAfternoon, isNotEmpty);
      expect(GameConstants.turnPhaseEvening, isNotEmpty);
    });
  });
}

