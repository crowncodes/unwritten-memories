# Music System - Quick Reference

**Version**: 1.0  
**Last Updated**: October 15, 2025

> **Cheat sheet for the Lifebond adaptive music system**

---

## 📐 Architecture at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│                    3-LAYER ARCHITECTURE                      │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  LAYER 1: DESIGN │      │ LAYER 2: GENERATE│      │ LAYER 3: RUNTIME │
│                  │      │                  │      │                  │
│  Cloud Run App   │──────│  Lyria API       │──────│  Flutter + Flame │
│  (TypeScript)    │      │  (Batch)         │      │  (Dart)          │
│                  │      │                  │      │                  │
│  6-Group Sliders │      │  Audio Stems     │      │  Game State →    │
│       ↓          │      │       ↓          │      │  MSV Calculation │
│  MSV JSON        │      │  Opus @ 48kHz    │      │       ↓          │
│  Lyria Prompt    │      │       ↓          │      │  Library Query   │
│  Stem Profile    │      │  library.json    │      │       ↓          │
│                  │      │                  │      │  Crossfade Stems │
└──────────────────┘      └──────────────────┘      └──────────────────┘
```

---

## 🎯 Core Concepts

### Music State Vector (MSV)

13 parameters describing musical character:

| Group | Parameters | Range | Description |
|-------|-----------|-------|-------------|
| **Affect** | valence, arousal, tension, agency | 0.0-1.0 | Emotional state |
| **Harmony** | brightness, consonance, cadentialDrive | 0.0-1.0 | Tonal character |
| **Temporal** | tempo, regularity | 0.0-1.0 | Rhythmic feel |
| **Orchestration** | sparsity, weights | 1-5, {...} | Instrumentation |
| **Texture** | intimacy, privacy | 0.0-1.0 | Spatial feel |

### Game State → MSV Mapping

```dart
// From life meters (0-10 scale each)
valence = (emotional + social) / 20.0 + 0.3
arousal = (physical + mental) / 20.0 + 0.2
tension = 1.0 - (capacity / 10.0)
agency = (mental + emotional) / 20.0 + 0.3

// Capacity affects orchestration
capacity ≤ 4 → high intimacy (0.7+), low sparsity (2-3 stems)
capacity ≥ 8 → lower intimacy (0.3-0.4), high sparsity (4-5 stems)
```

---

## 🔄 Common Workflows

### 1. Create New Stem Package

```
1. Open Cloud Run app
   https://adaptive-music-concept-generator-649888100218.us-west1.run.app

2. Adjust 6-Group Framework sliders
   - Emotional: Energy, Valence, Tension
   - Temporal: Tempo, Complexity, Stability
   - Harmonic: Consonance, Modal Character, Density
   - Textural: Density, Spatial Width, Dynamic Range
   - Cultural: Classical, Contemporary, World
   - Functional: Presence, Narrative, Directness

3. Click "Generate Stem Package"

4. Download:
   - msv.json (MSV parameters)
   - lyria_prompt.txt (Lyria generation prompt)
   - stem_profile.json (Library metadata)

5. Generate with Lyria:
   - Use lyria_prompt.txt
   - Generate each stem individually (pad, piano, etc.)
   - Download audio files

6. Process:
   - Convert to Opus @ 48kHz
   - Validate loop points (8 bars, seamless)
   - Create directory: assets/music/stems/{stem_id}/

7. Add to library:
   - Update library.json with stem_profile.json contents
   - Copy stem files to directory
   - Test in game
```

### 2. Query Stems at Runtime

```dart
// Load library
final library = await StemLibrary.loadFromAssets();

// Calculate current MSV
final msv = MusicStateVector.fromGameState(gameState, meters);

// Find best match
final stemPackage = library.findBestMatch(msv);

// Play stems
await stemMixer.transitionToStem(stemPackage);
```

### 3. Implement Flame Mixer

```dart
class FlameStemMixer extends Component with HasGameReference {
  final AudioCache _audioCache = FlameAudio.audioCache;
  final Map<String, AudioPlayer> _activePlayers = {};
  
  Future<void> transitionToStem(StemPackage package) async {
    // Load new stems
    final newPlayers = await _loadStems(package);
    
    // Crossfade (2 seconds)
    await _crossfade(_activePlayers, newPlayers);
    
    // Update active
    _activePlayers = newPlayers;
  }
  
  Future<void> _crossfade(old, new) async {
    // Start new at volume 0
    // Fade out old over 2s
    // Fade in new over 2s
    // Stop old
  }
}
```

---

## 📊 Priority Tier 1: 10 Emotional States

| ID | Capacity | Valence | Arousal | Use Case |
|----|----------|---------|---------|----------|
| **calm_positive** | 5-7 | 0.6-0.8 | 0.2-0.4 | Baseline gameplay |
| **melancholic** | 2-4 | 0.2-0.4 | 0.2-0.4 | Sad/withdrawn |
| **motivated** | 6-8 | 0.5-0.7 | 0.6-0.8 | Working on goals |
| **exhausted** | 1-3 | 0.3-0.5 | 0.1-0.3 | Overwhelmed |
| **anxious** | 3-5 | 0.4-0.6 | 0.4-0.6 | Tense/worried |
| **content** | 7-9 | 0.7-0.9 | 0.2-0.4 | Peaceful |
| **excited** | 6-8 | 0.7-0.9 | 0.7-0.9 | Celebration |
| **worried** | 4-6 | 0.4-0.6 | 0.5-0.7 | Uncertain |
| **sad** | 2-4 | 0.1-0.3 | 0.2-0.4 | Grief/loss |
| **reflective** | 5-7 | 0.4-0.6 | 0.3-0.5 | Introspective |

**Each → 3 variants**: Morning, Evening, Crisis = **30 total packages**

---

## 🎹 6-Group Framework → MSV Conversion

### Quick Formulas

```typescript
// Affect
valence = (emotional.valence / 100) * modalModifier
arousal = (emotional.energy / 100) + tempoBoost
tension = (emotional.tension / 100) + dissonanceBoost
agency = (emotional.energy*0.4 + functional.narrative*0.3 + temporal.tempo*0.3) / 100

// Harmony
brightness = (harmonic.modalCharacter / 100) + valenceBoost
consonance = (harmonic.consonance / 100) * tensionModifier
cadentialDrive = (harmonic.density*0.5 + functional.narrative*0.5) / 100

// Temporal
tempo = (temporal.intensity / 100) * energyModifier
regularity = (temporal.stability / 100) * complexityModifier

// Orchestration
sparsity = 5 - (textural.density / 25)  // 1-5
weights = calculateWeights(...)  // Based on arousal, agency, cultural

// Texture
intimacy = 1.0 - ((textural.width*0.6 + textural.density*0.4) / 100)
privacy = 1.0 - ((functional.presence*0.5 + textural.width*0.3 + functional.directness*0.2) / 100)
```

---

## 🎵 Stem Types & Roles

| Stem Type | Always Present? | Weight Calculation | Use When |
|-----------|----------------|-------------------|----------|
| **pad** | ✅ Yes | 1.0 | Foundation drone |
| **piano** | ✅ Yes | 0.8 | Melodic foundation |
| **light_rhythm** | No | (arousal + tempo) / 2 | Sparsity < 4 |
| **melody** | No | (agency + narrative) / 2 | Sparsity < 4 |
| **texture** | No | (intimacy + (1 - density)) / 2 | Sparsity < 4 |
| **bass** | No | (energy + (1 - density)) / 2 | Sparsity < 4 |

**Sparsity determines max stems**:
- Sparsity 1 = Dense (5 stems)
- Sparsity 3 = Moderate (3 stems)
- Sparsity 5 = Sparse (1-2 stems)

---

## 📁 File Locations Cheat Sheet

### Documentation
```
docs/9.music/
├── 00-MUSIC-SYSTEM-MASTER.md           ⭐ Complete guide
├── 00-INDEX.md                         📑 Navigation
├── 01-QUICK-REFERENCE.md               🚀 This file
├── 02-msv-conversion-formulas.md       🧮 Formulas
├── 03-lyria-generation-guide.md        🎵 Lyria prompts
├── 04-flutter-implementation.md        📱 Flutter code
├── 05-generation-workflow.md           ⚙️ Workflow
├── adaptive-music-concept-generator/   💻 Cloud Run app
│   └── services/                       📦 TypeScript services
└── scripts/                            🛠️ Generation Pipeline tools
    ├── convert_to_opus.ps1             (WAV → Opus conversion)
    ├── validate_stems.ps1              (Quality validation)
    ├── generate_silence_stems.ps1      (Test stems)
    └── generate_lyria_stems.py         (Lyria API template)
```

### Flutter Code
```
app/lib/features/music/
├── data/models/
│   ├── music_state_vector.dart      (MSV calculation)
│   └── stem_library.dart            (Library loader)
└── domain/usecases/
    └── match_stem_to_msv.dart       (Matching algorithm)
```

### Assets
```
app/assets/music/stems/
├── library.json                     (Master index)
└── {stem_id}/
    ├── pad.opus
    ├── piano.opus
    └── ...
```

---

## 🔧 Common Code Snippets

### Load Library
```dart
final library = await StemLibrary.loadFromAssets();
```

### Calculate MSV
```dart
final msv = MusicStateVector.fromGameState(
  gameState,
  lifeMeters,
);
```

### Find Best Match
```dart
final match = library.findBestMatch(msv);
```

### Get Top 3 Matches
```dart
final matcher = MatchStemToMSV(library);
final topMatches = matcher.getTopMatches(msv, count: 3);
```

### Filter by Tags
```dart
final calmStems = library.findByTags(['calm', 'positive']);
```

### Filter by Capacity
```dart
final lowCapacityStems = library.findByCapacity(3.5);
```

---

## 🎚️ Volume Calculation

```dart
double calculateStemVolume(String stemType, MSVOutput msv) {
  // Get weight from MSV
  final weight = msv.orchestration.weights[stemType] ?? 0.5;
  
  // Apply capacity factor
  final capacity = game.lifeMeters.average;
  final capacityFactor = capacity <= 4.0 ? 0.6 :
                         capacity >= 8.0 ? 1.0 :
                         0.6 + ((capacity - 4.0) / 4.0) * 0.4;
  
  return (weight * capacityFactor).clamp(0.0, 1.0);
}
```

---

## 🐛 Troubleshooting

### Stem Not Found
```
Error: "Cannot find stem assets/music/stems/..."
Solution: Check library.json paths match actual file structure
```

### Crossfade Glitches
```
Problem: Audible pops during transition
Solution: Ensure loop points are exact (bar-aligned)
         Use longer crossfade duration (3-4 seconds)
```

### Performance Issues
```
Problem: Frame drops during stem transitions
Solution: Pre-load stems in background
         Use object pooling for AudioPlayers
         Limit concurrent stem loads
```

### Wrong Stem Selected
```
Problem: Music doesn't match emotional state
Solution: Check MSV calculation (log values)
         Verify library has appropriate stems for state
         Adjust distance weights in matching algorithm
```

---

## 📊 Performance Targets

| Metric | Target | Critical |
|--------|--------|----------|
| **Frame time** | <16ms | <33ms |
| **Library load** | <50ms | <100ms |
| **Stem query** | <5ms | <10ms |
| **Crossfade latency** | <100ms | <200ms |
| **Memory (music)** | <50MB | <100MB |
| **Battery (30min)** | <10% | <15% |

---

## 🔗 Quick Links

- **Master Docs**: [00-MUSIC-SYSTEM-MASTER.md](./00-MUSIC-SYSTEM-MASTER.md)
- **Cloud Run App**: https://adaptive-music-concept-generator-649888100218.us-west1.run.app
- **GitHub Repo**: https://github.com/crowncodes/unwritten-adaptive-music
- **Game Design**: `docs/master_truths_canonical_spec_v_1_2.md`
- **Flame Docs**: `docs/master_flutter_flame_spec_v_1_0.md` (Section III)

---

## 💡 Pro Tips

1. **Start simple**: Generate calm_positive stem first, test everything works
2. **Use presets**: Cloud Run app includes preset scenarios
3. **Test capacity range**: Manually adjust capacity slider to verify music changes
4. **Log MSV values**: Add debug logging to understand parameter ranges
5. **Cache library**: Load once at startup, keep in memory
6. **Batch generate**: Use Lyria API for multiple stems at once
7. **Version control stems**: Keep generation metadata with audio files

---

*Quick reference for Lifebond adaptive music system v1.0*

