# Music System - Master Documentation

**Version**: 1.0  
**Last Updated**: October 15, 2025  
**Status**: Active

> **Purpose**: Single source of truth for the Lifebond music system. All three layers (Design Tool, Generation Pipeline, Runtime System) are documented here.

---

## Architecture Overview

The music system uses a **3-layer architecture** to enable adaptive, emotionally authentic music that responds to gameplay state:

### Layer 1: Design Tool (Cloud Run)

- **Location**: `docs/9.music/adaptive-music-concept-generator/`
- **Purpose**: Offline stem design and parameter exploration
- **URL**: https://adaptive-music-concept-generator-649888100218.us-west1.run.app
- **Repository**: https://github.com/crowncodes/unwritten-adaptive-music

**Inputs**: 6-Group Framework sliders (18 parameters, 0-100 scale)
- Group 1: Emotional Arousal & Valence (Energy, Valence, Tension)
- Group 2: Temporal & Rhythmic Character (Tempo Intensity, Rhythmic Complexity, Metric Stability)
- Group 3: Harmonic & Tonal Architecture (Consonance/Dissonance, Modal Character, Harmonic Density)
- Group 4: Textural Density & Space (Instrumental Density, Spatial Width, Dynamic Range)
- Group 5: Cultural & Stylistic Identity (Classical, Contemporary, World)
- Group 6: Narrative & Contextual Function (Presence/Absence, Narrative Drive, Directness)

**Outputs**: 
- MSV JSON (13 parameters, 0.0-1.0 scale)
- Lyria prompt (detailed, technical, loop-safe)
- Stem metadata profile (game state matching criteria)

### Layer 2: Generation Pipeline (Lyria)

- **Purpose**: Batch generation of high-quality stems
- **Process**: Design tool output → Lyria API → Download → Convert to Opus @ 48kHz → Validate → Add to library
- **Storage**: `app/assets/music/stems/library.json` + individual stem folders
- **Quality**: 8-bar loops, Opus @ 48kHz, seamless crossfades, <10MB per stem package

### Layer 3: Runtime System (Flutter + Flame)

- **Location**: `app/lib/features/music/`
- **Purpose**: Real-time stem selection and mixing based on game state
- **Process**: Life meters → MSV calculation → Library query → Flame audio mixer → Crossfade stems
- **Performance**: <16ms frame time, battery-friendly (<10% drain per 30min), privacy-first (on-device)
- **Audio Engine**: FlameAudio or SoLoud for professional crossfading and dynamic mixing

---

## Game State Integration

Based on `master_truths_canonical_spec_v_1_2.md`:

### Emotional Capacity (0-10 scale)

Music directly reflects emotional capacity limitations:

- **Capacity ≤ 4**: High intimacy (0.7+), low sparsity (2-3 stems), high privacy (0.6+)
  - Music becomes minimal, close-mic'd, sparse
  - Example: Capacity 2.5 → pad + soft piano only, very intimate
- **Capacity 4-7**: Medium intimacy (0.4-0.7), moderate sparsity (3-4 stems)
  - Baseline gameplay music
- **Capacity ≥ 8**: Full orchestration available, lower intimacy (0.3-0.4), high sparsity (4-5 stems)
  - Richer, more complex arrangements

### Life Meters → MSV Mapping

```dart
// From app/lib/features/music/data/models/music_state_vector.dart
valence = (meters.emotional + meters.social) / 20.0 + 0.3
arousal = (meters.physical + meters.mental) / 20.0 + 0.2
tension = 1.0 - (capacity / 10.0)
agency = (meters.mental + meters.emotional) / 20.0 + 0.3
```

### Day Phase Effects

- **Morning**: Tempo boost (+0.5), brighter harmony, lower privacy
- **Afternoon**: Moderate tempo (+0.45), balanced
- **Evening**: Lower tempo (+0.3), higher intimacy, higher privacy

### Tension Injection (Section 17)

Music subtly builds narrative tension:
- Instruments fading in/out mysteriously
- Mystery hooks in soundscape (unexplained sounds)
- Stakes escalation via tempo/intensity increases
- Frequency: 1 in 3 (Level 1-2), 1 in 2 (Level 3-4), nearly every (Level 5)

---

## MSV Conversion Formulas

From 6-Group Framework to Music State Vector (MSV):

### Affect (Emotional State)

```typescript
valence = (Group1.Valence / 100) * modalCharacterModifier
  where modalCharacterModifier = {
    0.7 if Group3.ModalCharacter < 35 (dark minor),
    1.15 if Group3.ModalCharacter > 70 (bright major),
    1.0 otherwise
  }

arousal = (Group1.Energy / 100) + tempoBoost + rhythmicBoost
  where tempoBoost = 0.1 if Group2.TempoIntensity > 75,
        rhythmicBoost = 0.05 if Group2.RhythmicComplexity > 70

tension = (Group1.Tension / 100) + dissonanceBoost + metricsBoost
  where dissonanceBoost = 0.15 if Group3.Consonance < 35,
        metricsBoost = 0.1 if Group2.MetricStability < 40

agency = (Group1.Energy * 0.4 + Group6.NarrativeDrive * 0.3 + Group2.TempoIntensity * 0.3) / 100
```

### Harmony (Tonal Character)

```typescript
brightness = (Group3.ModalCharacter / 100) + valenceBoost + rangeBoost
  where valenceBoost = 0.1 if Group1.Valence > 70,
        rangeBoost = 0.05 if Group4.DynamicRange > 70

consonance = (Group3.Consonance / 100) * tensionModifier * culturalModifier
  where tensionModifier = 0.8 if Group1.Tension > 70,
        culturalModifier = 1.1 if Group5.Classical > 60

cadentialDrive = (Group3.HarmonicDensity * 0.5 + Group6.NarrativeDrive * 0.5) / 100
```

### Temporal (Rhythmic Feel)

```typescript
tempo = (Group2.TempoIntensity / 100) * energyModifier * arousalModifier
  where energyModifier = 0.85 if Group1.Energy < 30,
        arousalModifier = 1.15 if arousal > 0.8

regularity = (Group2.MetricStability / 100) * complexityModifier * tensionModifier
  where complexityModifier = 0.85 if Group2.RhythmicComplexity > 75,
        tensionModifier = 0.9 if Group1.Tension > 70
```

### Orchestration (Instrumentation)

```typescript
sparsity = clamp(round(5 - (Group4.InstrumentalDensity / 25) + spatialBonus), 1, 5)
  where spatialBonus = 1 if Group4.SpatialWidth < 35

weights = {
  pad: 1.0 (always present),
  piano: 0.8 (always present),
  rhythm: (arousal + tempo) / 2 * (sparsity >= 4 ? 0.5 : 1.0),
  melody: (agency + Group6.NarrativeDrive / 100) / 2 * (sparsity >= 4 ? 0.6 : 1.0),
  bass: sparsity >= 4 ? 0 : (Group1.Energy / 100 + (1 - Group4.InstrumentalDensity / 100)) / 2,
  texture: (intimacy + clamp(1.0 - Group4.InstrumentalDensity / 100)) / 2,
  orchestral: Group5.Classical / 100,
  electronic: Group5.Contemporary / 100,
  world: Group5.World / 100
}
```

### Texture (Spatial & Intimacy)

```typescript
intimacy = clamp(1.0 - ((Group4.SpatialWidth * 0.6 + Group4.InstrumentalDensity * 0.4) / 100) 
                  + presenceBonus + dynamicBonus)
  where presenceBonus = 0.15 if Group6.Presence < 40,
        dynamicBonus = 0.1 if Group4.DynamicRange < 35

privacy = clamp(1.0 - ((Group6.Presence * 0.5 + Group4.SpatialWidth * 0.3 + Group6.Directness * 0.2) / 100),
                minPrivacy)
  where minPrivacy = 0.6 if intimacy > 0.7, else 0.0
```

---

## Stem Library Schema

**Location**: `app/assets/music/stems/library.json`

```json
{
  "version": "1.0",
  "lastUpdated": "2025-10-15",
  "totalStems": 30,
  "stems": [
    {
      "id": "calm_positive_intimate_c72",
      "tags": ["calm", "positive", "intimate", "journal", "baseline"],
      "msv": {
        "affect": {
          "valence": 0.7,
          "arousal": 0.3,
          "tension": 0.2,
          "agency": 0.6
        },
        "harmony": {
          "brightness": 0.65,
          "consonance": 0.85,
          "cadentialDrive": 0.6
        },
        "temporal": {
          "tempo": 0.4,
          "regularity": 0.7
        },
        "orchestration": {
          "sparsity": 3,
          "weights": {
            "pad": 0.6,
            "piano": 0.7,
            "light_rhythm": 0.25
          }
        },
        "texture": {
          "intimacy": 0.7,
          "privacy": 0.6
        }
      },
      "gameStateMatch": {
        "capacityRange": [4.0, 7.0],
        "valenceRange": [0.6, 0.8],
        "arousalRange": [0.2, 0.4],
        "dayPhases": ["morning", "afternoon"]
      },
      "technical": {
        "tempo": 72,
        "key": "C",
        "mode": "Ionian",
        "bars": 8,
        "durationMs": 26667,
        "loopPoints": [0, 26667]
      },
      "files": {
        "pad": "assets/music/stems/calm_positive_intimate_c72/pad.opus",
        "piano": "assets/music/stems/calm_positive_intimate_c72/piano.opus",
        "brush": "assets/music/stems/calm_positive_intimate_c72/brush.opus"
      },
      "generatedFrom": {
        "sixGroupParams": {
          "emotional": [30, 75, 20],
          "temporal": [40, 50, 70],
          "harmonic": [85, 70, 60],
          "textural": [35, 20, 50],
          "cultural": [60, 30, 10],
          "functional": [40, 65, 45]
        },
        "lyriaPrompt": "Warm analog synthesizer pad with gentle movement. Intimate felt piano, soft hammers, close-miked. Tempo: 72 BPM, Time Signature: 4/4, Duration: 8 bars (26.67s). Key: C Ionian. Emotional Character: warm, hopeful, positive, calm, serene, peaceful, relaxed, comfortable, intimate, close, personal. Technical Requirements: Loop-safe audio with seamless crossfade at bar boundaries, Bar-aligned with natural fade tail at loop point, Opus format @ 48kHz sample rate, Clean separation between stems, Intimate journal music aesthetic, battery-friendly. Style References: Nils Frahm, Ólafur Arnalds, Erik Satie - intimate journal music."
      }
    }
  ]
}
```

---

## Priority Tier 1: Core Emotional States

Generate these 10 states first (3 variants each = **30 stem packages total**):

| # | State | Capacity Range | Valence | Arousal | Use Case |
|---|-------|---------------|---------|---------|----------|
| 1 | **calm_positive** | 5-7 | 0.6-0.8 | 0.2-0.4 | Baseline gameplay, journaling, routine |
| 2 | **melancholic_private** | 2-4 | 0.2-0.4 | 0.2-0.4 | Sad/withdrawn, low capacity |
| 3 | **motivated** | 6-8 | 0.5-0.7 | 0.6-0.8 | Working on goals, aspiration progress |
| 4 | **exhausted** | 1-3 | 0.3-0.5 | 0.1-0.3 | Overwhelmed, crisis, cannot cope |
| 5 | **anxious** | 3-5 | 0.4-0.6 | 0.4-0.6 | Tense/worried, uncertain future |
| 6 | **content** | 7-9 | 0.7-0.9 | 0.2-0.4 | Peaceful satisfaction, goals met |
| 7 | **excited** | 6-8 | 0.7-0.9 | 0.7-0.9 | High arousal/positive, celebration |
| 8 | **worried** | 4-6 | 0.4-0.6 | 0.5-0.7 | Uncertain, decision stress |
| 9 | **sad** | 2-4 | 0.1-0.3 | 0.2-0.4 | Low valence, grief, loss |
| 10 | **reflective** | 5-7 | 0.4-0.6 | 0.3-0.5 | Introspective, contemplative |

**Each state → 3 variants**:
- **Morning** (brighter, higher tempo, +0.5 tempo, -0.1 intimacy)
- **Evening** (intimate, lower tempo, +0.3 tempo, +0.2 intimacy, +0.2 privacy)
- **Crisis** (tension +0.3, irregular rhythm, -0.2 regularity, stakes escalation)

---

## Flame Audio Integration

### Runtime Mixer Architecture

**FlameAudio Approach** (Standard):
```dart
class FlameStemMixer extends Component with HasGameReference {
  final AudioCache _audioCache = FlameAudio.audioCache;
  final Map<String, AudioPlayer> _activePlayers = {};
  final Map<String, double> _targetVolumes = {};
  
  Future<void> transitionToStem(StemProfile profile, {Duration duration = const Duration(seconds: 2)}) async {
    // Load new stems, crossfade from old to new
    // Respect MSV-based volume weights
  }
  
  void update(double dt) {
    // Real-time volume adjustment based on game state changes
    // Smooth interpolation between target and current volumes
  }
}
```

**SoLoud Approach** (Advanced):
```dart
class SoLoudStemMixer extends Component with HasGameReference {
  late SoLoud _soloud;
  final Map<String, SoundHandle> _activeHandles = {};
  
  // Built-in crossfading, 3D spatial audio (optional), real-time effects
}
```

### Stem Matching Algorithm

**Location**: `app/lib/features/music/domain/usecases/match_stem_to_msv.dart`

```dart
StemProfile findBestMatch(MusicStateVector currentMSV) {
  double bestDistance = double.infinity;
  StemProfile? bestMatch;
  
  for (final profile in stemLibrary.stems) {
    final distance = _calculateDistance(currentMSV, profile.msv);
    if (distance < bestDistance) {
      bestDistance = distance;
      bestMatch = profile;
    }
  }
  
  return bestMatch!;
}

double _calculateDistance(MusicStateVector a, MSVOutput b) {
  return (
    abs(a.affectValence - b.affect.valence) * 2.0 +  // Valence most important
    abs(a.affectArousal - b.affect.arousal) * 1.5 +
    abs(a.affectTension - b.affect.tension) * 1.2 +
    abs(a.textureIntimacy - b.texture.intimacy) * 1.8 +  // Intimacy critical for capacity
    abs(a.temporalTempo - b.temporal.tempo) * 1.0 +
    abs(a.contextPrivacy - b.texture.privacy) * 1.3
  );
}
```

---

## Workflow: From Design to Runtime

### 1. Design Tool Workflow (Cloud Run App)

1. Adjust 6-Group Framework sliders to desired musical character
2. Click **"Generate Stem Package"**
3. Download outputs:
   - `msv.json` - Music State Vector parameters
   - `lyria_prompt.txt` - Detailed generation prompt for Lyria
   - `stem_profile.json` - Metadata for library

### 2. Generation Pipeline Workflow

1. **Input**: Lyria prompt from design tool
2. **Generate**: Use Lyria API to create individual stems (pad, piano, rhythm, etc.)
3. **Convert**: Convert to Opus @ 48kHz using `ffmpeg`
4. **Validate**: Check loop points, duration, silence detection
5. **Package**: Create folder structure with metadata
6. **Add to Library**: Update `library.json` with new stem profile

### 3. Runtime System Workflow

1. **Game state changes** (capacity drops to 3.5, valence 0.4, arousal 0.3)
2. **MSV calculated** → High intimacy (0.8), low arousal, high privacy
3. **Library query** → Find best matching stem profile
4. **Crossfade** → Flame mixer transitions from current stems to new stems over 2 seconds
5. **Dynamic mixing** → Individual stem volumes adjust in real-time based on ongoing game state changes

---

## Performance Targets

- **Frame time**: <16ms (60 FPS maintained)
- **Audio latency**: <100ms for stem transitions
- **Battery drain**: <10% per 30-minute session
- **Memory footprint**: <50MB for music system (excluding assets)
- **Stem file size**: <2MB per individual stem (Opus compression)
- **Library size**: ~60MB for 30 stem packages (Tier 1)

---

## Training Data Collection

### Future ML Model Training

Every stem usage is logged for future local TFLite model training:

```json
{
  "timestamp": "2025-10-15T14:30:00Z",
  "stemId": "calm_positive_intimate_c72",
  "gameState": {
    "capacity": 5.5,
    "valence": 0.7,
    "arousal": 0.3,
    "dayPhase": "afternoon"
  },
  "playerFeedback": {
    "manualSkip": false,
    "durationPlayed": 180
  }
}
```

**Goal**: Train local model to generate stems on-device, eliminating need for pre-generated library.

---

## References

- **Master game design**: `docs/master_truths_canonical_spec_v_1_2.md`
- **Conversion formulas**: `docs/9.music/02-msv-conversion-formulas.md`
- **Flutter MSV implementation**: `app/lib/features/music/data/models/music_state_vector.dart`
- **Flame audio documentation**: See `docs/master_flutter_flame_spec_v_1_0.md` Section III
- **Generation workflow**: `docs/9.music/05-generation-workflow.md`
- **Generation scripts**: `docs/9.music/scripts/README.md`
- **Cloud Run repository**: https://github.com/crowncodes/unwritten-adaptive-music
- **Cloud Run URL**: https://adaptive-music-concept-generator-649888100218.us-west1.run.app

---

## Version History

**v1.0** (2025-10-15): Initial master documentation
- Consolidated 15+ conflicting documents
- Established 3-layer architecture
- Defined Priority Tier 1 stem requirements
- Integrated Flame audio system

