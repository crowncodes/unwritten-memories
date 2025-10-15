# Music System - Index

**Version**: 1.0  
**Last Updated**: October 15, 2025  
**Status**: Active

---

## 🎯 Start Here

**New to the music system?** Begin with the master documentation:

📖 **[00-MUSIC-SYSTEM-MASTER.md](./00-MUSIC-SYSTEM-MASTER.md)** - Complete system architecture, MSV conversion formulas, stem library schema, and workflow documentation.

---

## 📁 Directory Structure

```
docs/9.music/
├── 00-INDEX.md (this file)
├── 00-MUSIC-SYSTEM-MASTER.md          ⭐ START HERE
├── MSV_CONVERSION_PROMPT.md            (Reference: conversion formulas)
├── MUSIC_SYSTEM_IMPLEMENTATION.md      (Reference: Flutter implementation)
├── LYRIA_STEM_GENERATOR_GEM_PROMPT.md (Reference: Lyria generation)
├── adaptive-music-concept-generator/   (Cloud Run app source)
│   ├── services/
│   │   ├── msvConverter.ts
│   │   ├── lyriaPromptGenerator.ts
│   │   └── stemProfileGenerator.ts
│   └── ...
└── _archive/                           (Old documentation)
```

---

## 🏗️ System Architecture Overview

The music system uses a **3-layer architecture**:

### Layer 1: Design Tool (Cloud Run)
- **Location**: `adaptive-music-concept-generator/`
- **URL**: https://adaptive-music-concept-generator-649888100218.us-west1.run.app
- **Purpose**: Offline stem design and parameter exploration
- **Output**: MSV JSON + Lyria prompts + stem metadata

### Layer 2: Generation Pipeline (Lyria)
- **Purpose**: Batch generation of high-quality music stems
- **Process**: Design tool → Lyria API → Convert to Opus → Add to library
- **Output**: `app/assets/music/stems/library.json`

### Layer 3: Runtime System (Flutter + Flame)
- **Location**: `app/lib/features/music/`
- **Purpose**: Real-time stem selection and mixing
- **Process**: Game state → MSV → Library query → Flame mixer

---

## 📚 Documentation Map

| Document | Purpose | Audience |
|----------|---------|----------|
| **00-MUSIC-SYSTEM-MASTER.md** | Complete system architecture | Everyone |
| **01-QUICK-REFERENCE.md** | Cheat sheet and common workflows | Everyone |
| **02-msv-conversion-formulas.md** | 6-Group → MSV conversion formulas | Engineers |
| **03-lyria-generation-guide.md** | Lyria prompt creation and Gemini Gem setup | Audio designers |
| **04-flutter-implementation.md** | Flutter/Dart implementation details | Flutter devs |
| **05-generation-workflow.md** | End-to-end stem generation workflow | Audio designers |
| library-schema.md | Stem library JSON schema | Backend devs |

## 🛠️ Scripts & Tools (Layer 2: Generation Pipeline)

| Script | Purpose | Layer | Status |
|--------|---------|-------|--------|
| `scripts/convert_to_opus.ps1` | Convert WAV stems to Opus @ 48kHz | Layer 2 | ✅ Active |
| `scripts/validate_stems.ps1` | Validate stem duration, format, loop points | Layer 2 | ✅ Active |
| `scripts/generate_silence_stems.ps1` | Generate silent test stems for architecture validation | Layer 2 | ✅ Active |
| `scripts/generate_lyria_stems.py` | Lyria API integration template (no public API yet) | Layer 2 | ⚠️ Template |

📖 **See**: `scripts/README.md` for detailed usage instructions

---

## 🚀 Quick Start Workflows

### For Game Developers

**Goal**: Understand how music adapts to gameplay

1. Read: `00-MUSIC-SYSTEM-MASTER.md` → "Game State Integration" section
2. Review: `app/lib/features/music/data/models/music_state_vector.dart`
3. Test: Run game and observe music changes with life meter adjustments

### For Audio Designers

**Goal**: Create new stem packages

1. Open: https://adaptive-music-concept-generator-649888100218.us-west1.run.app
2. Adjust: 6-Group Framework sliders to desired musical character
3. Generate: Click "Generate Stem Package" → Download MSV + Lyria prompt
4. Generate stems: Use Lyria API with generated prompt
5. Package: Convert to Opus @ 48kHz, add to library

### For Flutter Engineers

**Goal**: Implement music system integration

1. Read: `00-MUSIC-SYSTEM-MASTER.md` → "Runtime System" section
2. Review: `app/lib/features/music/domain/usecases/match_stem_to_msv.dart`
3. Implement: Flame audio mixer based on FlameAudio or SoLoud examples
4. Test: Load library, match stems, verify crossfades

### For System Architects

**Goal**: Understand complete data flow

1. Read: `00-MUSIC-SYSTEM-MASTER.md` → "Architecture Overview"
2. Review: `adaptive-music-concept-generator/services/` TypeScript services
3. Review: `app/lib/features/music/data/models/stem_library.dart`
4. Document: Any new components or integration points

---

## 🔗 Key Files by Layer

### Layer 1: Design Tool (TypeScript)

```
adaptive-music-concept-generator/
├── App.tsx                                (Main UI component)
├── types.ts                               (TypeScript interfaces)
├── constants.ts                           (6-Group definitions)
└── services/
    ├── msvConverter.ts                    (6-Group → MSV conversion)
    ├── lyriaPromptGenerator.ts            (MSV → Lyria prompt)
    └── stemProfileGenerator.ts            (Generate metadata)
```

### Layer 2: Generation Pipeline (Scripts)

- Lyria API integration (to be documented)
- Opus conversion scripts (to be created)
- Library management scripts (to be created)

### Layer 3: Runtime System (Dart/Flutter)

```
app/lib/features/music/
├── data/models/
│   ├── music_state_vector.dart           (MSV calculation from game state)
│   └── stem_library.dart                 (Library loader & parser)
├── domain/usecases/
│   └── match_stem_to_msv.dart            (Stem matching algorithm)
└── presentation/components/
    └── flame_stem_mixer.dart             (Flame audio mixer - to be created)
```

---

## 📊 Priority Tier 1 Stems

**Target**: 30 stem packages (10 emotional states × 3 variants)

| # | State | Capacity | Valence | Arousal | Variants |
|---|-------|----------|---------|---------|----------|
| 1 | calm_positive | 5-7 | 0.6-0.8 | 0.2-0.4 | Morning/Evening/Crisis |
| 2 | melancholic | 2-4 | 0.2-0.4 | 0.2-0.4 | Morning/Evening/Crisis |
| 3 | motivated | 6-8 | 0.5-0.7 | 0.6-0.8 | Morning/Evening/Crisis |
| 4 | exhausted | 1-3 | 0.3-0.5 | 0.1-0.3 | Morning/Evening/Crisis |
| 5 | anxious | 3-5 | 0.4-0.6 | 0.4-0.6 | Morning/Evening/Crisis |
| 6 | content | 7-9 | 0.7-0.9 | 0.2-0.4 | Morning/Evening/Crisis |
| 7 | excited | 6-8 | 0.7-0.9 | 0.7-0.9 | Morning/Evening/Crisis |
| 8 | worried | 4-6 | 0.4-0.6 | 0.5-0.7 | Morning/Evening/Crisis |
| 9 | sad | 2-4 | 0.1-0.3 | 0.2-0.4 | Morning/Evening/Crisis |
| 10 | reflective | 5-7 | 0.4-0.6 | 0.3-0.5 | Morning/Evening/Crisis |

See `00-MUSIC-SYSTEM-MASTER.md` for complete specifications.

---

## 🎵 Music State Vector (MSV) Parameters

The MSV consists of 13 parameters organized into 5 groups:

### Affect (Emotional State)
- `valence` (0.0-1.0): Negative to positive
- `arousal` (0.0-1.0): Calm to energetic
- `tension` (0.0-1.0): Relaxed to tense
- `agency` (0.0-1.0): Passive to active

### Harmony (Tonal Character)
- `brightness` (0.0-1.0): Dark to bright
- `consonance` (0.0-1.0): Dissonant to consonant
- `cadentialDrive` (0.0-1.0): Static to resolving

### Temporal (Rhythmic Feel)
- `tempo` (0.0-1.0): Slow to fast (58-100 BPM)
- `regularity` (0.0-1.0): Irregular to regular

### Orchestration (Instrumentation)
- `sparsity` (1-5): Dense to sparse (number of stems)
- `weights`: Relative weights for each stem type

### Texture (Spatial & Intimacy)
- `intimacy` (0.0-1.0): Expansive to intimate
- `privacy` (0.0-1.0): Public to private

---

## 🔄 Typical Workflow

### End-to-End: Creating a New Stem Package

1. **Design** (Cloud Run app)
   - Adjust 6-Group Framework sliders
   - Preview emotional character
   - Generate MSV + Lyria prompt + metadata

2. **Generate** (Lyria API)
   - Use generated prompt
   - Generate individual stems (pad, piano, rhythm, etc.)
   - Download audio files

3. **Process** (Command line)
   - Convert stems to Opus @ 48kHz
   - Validate loop points
   - Create directory structure

4. **Integrate** (Flutter app)
   - Add stem entry to `library.json`
   - Copy stem files to `assets/music/stems/`
   - Test in game

5. **Verify** (Runtime)
   - Check stem matching algorithm
   - Verify crossfading works
   - Confirm emotional capacity reflection

---

## 📦 Assets Structure

```
app/assets/music/stems/
├── library.json                          (Master index)
├── library-schema.md                     (Schema documentation)
└── [stem_package_id]/
    ├── pad.opus
    ├── piano.opus
    ├── light_rhythm.opus (optional)
    ├── melody.opus (optional)
    └── texture.opus (optional)
```

---

## 🛠️ Development Status

### ✅ Completed
- [x] Master documentation created
- [x] TypeScript services implemented (MSV converter, Lyria prompt generator, stem profile generator)
- [x] Dart library loader implemented
- [x] Stem matching algorithm implemented
- [x] Library schema documented
- [x] Old docs archived

### 🚧 In Progress
- [ ] Flame audio mixer component
- [ ] UI integration for "Generate Stem Package" button in Cloud Run app
- [ ] Generation pipeline scripts
- [ ] Priority Tier 1 stem generation (30 packages)

### 📋 Planned
- [ ] Lyria API integration documentation
- [ ] Batch processing scripts for stem generation
- [ ] Quality validation tools
- [ ] Training data collection system

---

## 📚 Related Documentation

- **Game Design**: `docs/master_truths_canonical_spec_v_1_2.md` (Section 16: Emotional Authenticity, Section 17: Tension Injection)
- **Flame Engine**: `docs/master_flutter_flame_spec_v_1_0.md` (Section III: Audio System)
- **Flutter MSV**: `app/lib/features/music/data/models/music_state_vector.dart`
- **Cloud Run Repo**: https://github.com/crowncodes/unwritten-adaptive-music

---

## 🔐 Archived Documentation

Old conflicting documentation has been moved to `_archive/`:
- Python framework definition scripts
- Old scenario generation
- Technical implementation specs
- Various conversion prompts
- Old visualization files

**Note**: Archived files are kept for historical reference but should not be used for new development. Always refer to `00-MUSIC-SYSTEM-MASTER.md` for current system architecture.

---

## 💡 Tips & Best Practices

### For Audio Design
- Start with existing emotional states, create variants
- Use morning/evening/crisis variants for day phase differentiation
- Keep intimacy high (>0.7) for low capacity states (≤4)
- Test stems at different volume combinations

### For Implementation
- Always use `StemLibrary.findBestMatch()` for stem selection
- Implement crossfading over 2 seconds minimum
- Use Flame's built-in audio system (FlameAudio or SoLoud)
- Cache loaded stems to reduce file I/O

### For Performance
- Pre-load library.json at app startup
- Lazy-load individual stem files
- Keep active stems in memory, unload unused ones
- Target <16ms frame time for 60 FPS

---

## 📧 Support

- **System architecture questions**: See `00-MUSIC-SYSTEM-MASTER.md`
- **Conversion formulas**: See `MSV_CONVERSION_PROMPT.md`
- **Flutter implementation**: See `MUSIC_SYSTEM_IMPLEMENTATION.md`
- **Cloud Run app**: https://github.com/crowncodes/unwritten-adaptive-music

---

*This index is part of the Lifebond adaptive music system.*  
*Version 1.0 - October 2025*
