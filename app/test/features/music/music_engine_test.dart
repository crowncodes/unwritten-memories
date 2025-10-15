import 'package:flutter_test/flutter_test.dart';
import 'package:unwritten/features/music/data/models/music_state_vector.dart';
import 'package:unwritten/features/music/data/models/cue_model.dart';
import 'package:unwritten/features/music/data/models/cue_bank_model.dart';
import 'package:unwritten/features/game/data/models/game_state_model.dart';
import 'package:unwritten/features/game/data/models/life_meters.dart';
import 'package:unwritten/features/game/data/models/day_phase.dart';
import 'package:unwritten/features/game/data/models/resources_model.dart';

void main() {
  group('MusicStateVector', () {
    test('fromGameState maps low capacity to high intimacy', () {
      // Arrange: Low capacity meters
      final meters = const LifeMetersModel(
        physical: 2.0,
        mental: 2.0,
        social: 2.0,
        emotional: 2.0,
      );
      
      final gameState = GameStateModel.initial('test_player').copyWith(
        lifeMeters: meters,
      );

      // Act
      final msv = MusicStateVector.fromGameState(gameState, meters);

      // Assert: Low capacity should increase intimacy and privacy
      expect(msv.textureIntimacy, greaterThanOrEqualTo(0.7));
      expect(msv.contextPrivacy, greaterThanOrEqualTo(0.6));
      expect(msv.orchestrationSparsity, equals(2)); // Fewer stems
    });

    test('fromGameState maps evening phase to higher privacy', () {
      // Arrange: Evening phase
      final meters = LifeMetersModel.initial();
      final gameState = GameStateModel.initial('test_player').copyWith(
        currentPhase: DayPhase.evening,
        lifeMeters: meters,
      );

      // Act
      final msv = MusicStateVector.fromGameState(gameState, meters);

      // Assert: Evening should increase privacy/intimacy
      expect(msv.contextPrivacy, greaterThanOrEqualTo(0.5));
      expect(msv.textureIntimacy, greaterThan(0.5));
    });

    test('fromGameState maps high arousal to higher tempo', () {
      // Arrange: High physical/mental meters (arousal)
      final meters = const LifeMetersModel(
        physical: 9.0,
        mental: 9.0,
        social: 7.0,
        emotional: 7.0,
      );
      
      final gameState = GameStateModel.initial('test_player').copyWith(
        currentPhase: DayPhase.morning,
        lifeMeters: meters,
      );

      // Act
      final msv = MusicStateVector.fromGameState(gameState, meters);

      // Assert: High arousal should increase tempo
      expect(msv.affectArousal, greaterThanOrEqualTo(0.6));
      expect(msv.temporalTempo, greaterThan(0.5));
      expect(msv.orchestrationSparsity, greaterThanOrEqualTo(3));
    });

    test('initial creates sensible defaults', () {
      // Act
      final msv = MusicStateVector.initial();

      // Assert: Should have balanced, calm defaults
      expect(msv.affectValence, closeTo(0.55, 0.1));
      expect(msv.affectArousal, closeTo(0.35, 0.1));
      expect(msv.orchestrationSparsity, equals(3));
      expect(msv.orchestrationWeights, isNotEmpty);
    });

    test('copyWith updates specific fields', () {
      // Arrange
      final original = MusicStateVector.initial();

      // Act
      final updated = original.copyWith(
        affectValence: 0.8,
        orchestrationSparsity: 5,
      );

      // Assert
      expect(updated.affectValence, equals(0.8));
      expect(updated.orchestrationSparsity, equals(5));
      // Other fields unchanged
      expect(updated.affectArousal, equals(original.affectArousal));
      expect(updated.temporalTempo, equals(original.temporalTempo));
    });
  });

  group('CueModel', () {
    test('barDuration calculates correctly for 4/4 at 72 BPM', () {
      // Arrange
      final cue = const CueModel(
        id: 'test_cue',
        tempoBpm: 72,
        meterBeats: 4,
        bars: 8,
        loopStartMs: 0,
        loopEndMs: 26667,
        stems: {},
        tags: [],
        key: 'C',
        mode: 'Ionian',
      );

      // Act
      final barDuration = cue.barDuration;

      // Assert: (60 / 72 BPM) * 4 beats = 3.333 seconds
      expect(barDuration.inMilliseconds, closeTo(3333, 10));
    });

    test('matchScore prefers exact meter match', () {
      // Arrange
      final cue = const CueModel(
        id: 'test_cue',
        tempoBpm: 72,
        meterBeats: 4,
        bars: 8,
        loopStartMs: 0,
        loopEndMs: 26667,
        stems: {},
        tags: ['calm'],
        key: 'C',
        mode: 'Ionian',
      );

      // Act
      final scoreWithMeter = cue.matchScore(
        targetBpm: 75,
        targetMeterBeats: 4,
      );
      final scoreWithoutMeter = cue.matchScore(
        targetBpm: 75,
        targetMeterBeats: 6,
      );

      // Assert: Exact meter match should score higher
      expect(scoreWithMeter, greaterThan(scoreWithoutMeter));
    });

    test('matchScore rewards BPM proximity', () {
      // Arrange
      final cue = const CueModel(
        id: 'test_cue',
        tempoBpm: 72,
        meterBeats: 4,
        bars: 8,
        loopStartMs: 0,
        loopEndMs: 26667,
        stems: {},
        tags: [],
        key: 'C',
        mode: 'Ionian',
      );

      // Act
      final closeScore = cue.matchScore(targetBpm: 73, targetMeterBeats: 4);
      final farScore = cue.matchScore(targetBpm: 100, targetMeterBeats: 4);

      // Assert: Closer BPM should score higher
      expect(closeScore, greaterThan(farScore));
    });

    test('matchScore rewards tag match', () {
      // Arrange
      final cue = const CueModel(
        id: 'test_cue',
        tempoBpm: 72,
        meterBeats: 4,
        bars: 8,
        loopStartMs: 0,
        loopEndMs: 26667,
        stems: {},
        tags: ['calm_positive', 'journal'],
        key: 'C',
        mode: 'Ionian',
      );

      // Act
      final scoreWithTag = cue.matchScore(
        targetBpm: 72,
        targetMeterBeats: 4,
        tag: 'calm_positive',
      );
      final scoreWithoutTag = cue.matchScore(
        targetBpm: 72,
        targetMeterBeats: 4,
        tag: 'anxious',
      );

      // Assert: Tag match should score higher
      expect(scoreWithTag, greaterThan(scoreWithoutTag));
    });
  });

  group('CueBankModel', () {
    test('bestMatch selects highest scoring cue', () {
      // Arrange
      final calmCue = const CueModel(
        id: 'calm_c72',
        tempoBpm: 72,
        meterBeats: 4,
        bars: 8,
        loopStartMs: 0,
        loopEndMs: 26667,
        stems: {},
        tags: ['calm_positive'],
        key: 'C',
        mode: 'Ionian',
      );
      
      final anxiousCue = const CueModel(
        id: 'anxious_c90',
        tempoBpm: 90,
        meterBeats: 4,
        bars: 8,
        loopStartMs: 0,
        loopEndMs: 21333,
        stems: {},
        tags: ['anxious'],
        key: 'C',
        mode: 'Phrygian',
      );

      final bank = CueBankModel(cues: [calmCue, anxiousCue]);

      // Act: Request calm, slow music
      final match = bank.bestMatch(
        bpm: 70,
        meterBeats: 4,
        tag: 'calm_positive',
      );

      // Assert: Should select calm cue
      expect(match?.id, equals('calm_c72'));
    });

    test('bestMatch returns null for empty bank', () {
      // Arrange
      final bank = const CueBankModel(cues: []);

      // Act
      final match = bank.bestMatch(bpm: 72, meterBeats: 4);

      // Assert
      expect(match, isNull);
    });

    test('fromJson parses cue bank correctly', () {
      // Note: This would need actual JSON loading in integration test
      // Just verifying model structure here
      final cue = CueModel.fromJson({
        'id': 'test',
        'tempo': 72,
        'meterBeats': 4,
        'bars': 8,
        'loopStartMs': 0,
        'loopEndMs': 26667,
        'key': 'C',
        'mode': 'Ionian',
        'tags': ['calm'],
        'stems': {'pad': 'assets/pad.opus'},
      });

      expect(cue.id, equals('test'));
      expect(cue.tempoBpm, equals(72));
      expect(cue.stems['pad'], equals('assets/pad.opus'));
    });
  });
}

