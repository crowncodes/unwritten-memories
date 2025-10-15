# Stem Library Schema

**Version**: 1.0  
**Last Updated**: October 15, 2025

This document defines the JSON schema for the music stem library used by the Lifebond game's adaptive music system.

## Overview

The stem library (`library.json`) contains metadata for all pre-generated music stem packages. Each stem package represents a distinct emotional/musical state and includes:

- **MSV parameters** - Musical characteristics (affect, harmony, temporal, orchestration, texture)
- **Game state matching criteria** - Capacity ranges, valence/arousal ranges, day phases
- **Technical details** - Tempo, key, mode, duration, loop points
- **File paths** - Locations of individual stem audio files (Opus @ 48kHz)
- **Generation provenance** - Original 6-Group parameters and Lyria prompt used

## JSON Schema

```typescript
interface StemLibrary {
  version: string;           // Library version (semantic versioning)
  lastUpdated: string;       // ISO 8601 timestamp
  totalStems: number;        // Total number of stem packages
  stems: StemPackage[];      // Array of stem packages
}

interface StemPackage {
  id: string;                // Unique identifier (e.g., "calm_positive_intimate_c72")
  tags: string[];            // Searchable tags (e.g., ["calm", "positive", "intimate"])
  msv: MSVOutput;            // Music State Vector parameters
  gameStateMatch: GameStateMatch;  // Matching criteria for game state
  technical: TechnicalSpec;  // Audio technical details
  files: FilePaths;          // Paths to stem audio files
  generatedFrom: Provenance; // Generation metadata
}

interface MSVOutput {
  affect: {
    valence: number;         // 0.0-1.0 (negative to positive)
    arousal: number;         // 0.0-1.0 (calm to energetic)
    tension: number;         // 0.0-1.0 (relaxed to tense)
    agency: number;          // 0.0-1.0 (passive to active)
  };
  harmony: {
    brightness: number;      // 0.0-1.0 (dark to bright)
    consonance: number;      // 0.0-1.0 (dissonant to consonant)
    cadentialDrive: number;  // 0.0-1.0 (static to resolving)
  };
  temporal: {
    tempo: number;           // 0.0-1.0 (slow to fast, maps to 58-100 BPM)
    regularity: number;      // 0.0-1.0 (irregular to regular)
  };
  orchestration: {
    sparsity: number;        // 1-5 (dense to sparse, number of stems)
    weights: {               // Relative weights for each stem type
      [stemType: string]: number;  // 0.0-1.0
    };
  };
  texture: {
    intimacy: number;        // 0.0-1.0 (expansive to intimate)
    privacy: number;         // 0.0-1.0 (public to private)
  };
}

interface GameStateMatch {
  capacityRange: [number, number];   // [min, max] emotional capacity (0-10 scale)
  valenceRange: [number, number];    // [min, max] valence match range
  arousalRange: [number, number];    // [min, max] arousal match range
  dayPhases?: string[];              // Optional: ["morning", "afternoon", "evening"]
}

interface TechnicalSpec {
  tempo: number;             // BPM (58-100)
  key: string;               // Musical key (e.g., "C", "D")
  mode: string;              // Musical mode (e.g., "Ionian", "Dorian", "Aeolian")
  bars: number;              // Number of bars (typically 8)
  durationMs: number;        // Total duration in milliseconds
  loopPoints: [number, number];  // [start, end] in milliseconds
}

interface FilePaths {
  [stemType: string]: string;  // Relative paths from app root (e.g., "assets/music/stems/...")
}

interface Provenance {
  sixGroupParams: {
    emotional: [number, number, number];
    temporal: [number, number, number];
    harmonic: [number, number, number];
    textural: [number, number, number];
    cultural: [number, number, number];
    functional: [number, number, number];
  };
  lyriaPrompt: string;       // Full Lyria generation prompt
}
```

## Example Entry

```json
{
  "id": "calm_positive_intimate_c72",
  "tags": ["calm", "positive", "intimate", "journal", "baseline", "consonant", "slow"],
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
    "lyriaPrompt": "Warm analog synthesizer pad with gentle movement. Intimate felt piano, soft hammers, close-miked..."
  }
}
```

## File Naming Conventions

### Stem Package IDs

Format: `{emotionalState}_{intimacyLevel}_{key}{tempo}`

**Emotional States** (Priority Tier 1):
- `calm_positive`
- `melancholic`
- `motivated`
- `exhausted`
- `anxious`
- `content`
- `excited`
- `worried`
- `sad`
- `reflective`

**Intimacy Levels**:
- `intimate` (intimacy > 0.7)
- `moderate` (0.4 ≤ intimacy ≤ 0.7)
- `expansive` (intimacy < 0.4)

**Key**: Musical key in lowercase (e.g., `c`, `d`, `g`)

**Tempo**: BPM value (e.g., `72`, `84`, `96`)

### Stem File Names

Format: `{stemType}.opus`

**Common Stem Types**:
- `pad` - Foundational pad/drone
- `piano` - Piano layer
- `light_rhythm` - Subtle percussion
- `melody` - Melodic line
- `texture` - Textural layer
- `bass` - Bass layer (only when sparsity < 4)

## Directory Structure

```
app/assets/music/stems/
├── library.json
├── calm_positive_intimate_c72/
│   ├── pad.opus
│   ├── piano.opus
│   └── brush.opus
├── melancholic_intimate_c60/
│   ├── pad.opus
│   └── piano.opus
├── motivated_moderate_g84/
│   ├── pad.opus
│   ├── piano.opus
│   ├── light_rhythm.opus
│   └── melody.opus
└── ...
```

## Usage

### Loading the Library

```dart
// app/lib/features/music/data/models/stem_library.dart
final library = await StemLibrary.loadFromAssets();
```

### Querying Stems

```dart
// Find best match for current game state
final currentMSV = MusicStateVector.fromGameState(gameState, meters);
final match = library.findBestMatch(currentMSV);
```

### Playing Stems

```dart
// app/lib/features/music/presentation/components/flame_stem_mixer.dart
await stemMixer.transitionToStem(match.profile);
```

## Validation Rules

1. **MSV values**: All must be in range [0.0, 1.0]
2. **Capacity range**: Must be in [0.0, 10.0]
3. **Sparsity**: Must be integer 1-5
4. **Tempo**: Must be in range [58, 100] BPM
5. **Loop points**: `[0, durationMs]`
6. **File paths**: Must exist in assets
7. **Tags**: Must include at least emotional state
8. **ID**: Must be unique across library

## Performance Considerations

- **Total library size**: Target <100MB for Tier 1 (30 packages)
- **Individual stem size**: Target <2MB per stem (Opus compression)
- **Load time**: Library JSON should load in <50ms
- **Query time**: Best match search should complete in <5ms
- **Memory footprint**: Keep active stems in memory, lazy-load others

## Version History

**v1.0** (2025-10-15): Initial schema definition


