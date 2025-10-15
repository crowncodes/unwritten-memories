# MSV Conversion Prompt for MIDI Generation Apps
## Bridging 6-Group Framework to Lifebond Music State Vector

> **Note**: This document is a reference for conversion formulas and mapping logic.
> For the complete music system architecture, see `00-MUSIC-SYSTEM-MASTER.md`

---

## Overview

This prompt enables you to convert inputs from MIDI/music generation apps using the **6-Group Contextual Framework** (Emotional, Temporal, Harmonic, Textural, Cultural, Functional) into the **Music State Vector (MSV)** parameters used by Lifebond's adaptive music system.

---

## Conversion Matrix

### INPUT: 6-Group Framework Parameters

#### Group 1: Emotional Arousal & Valence
- **Energy Level** (0-100)
- **Valence** (0-100)
- **Tension** (0-100)

#### Group 2: Temporal & Rhythmic Character
- **Tempo Intensity** (0-100)
- **Rhythmic Complexity** (0-100)
- **Metric Stability** (0-100)

#### Group 3: Harmonic & Tonal Architecture
- **Consonance Level** (0-100%)
- **Modal Character** (0-100%)
- **Harmonic Density** (0-100%)

#### Group 4: Textural Density & Space
- **Instrumental Density** (0-100)
- **Spatial Width** (0-100)
- **Dynamic Range** (0-100)

#### Group 5: Cultural & Stylistic Identity
- **Western Classical** (0-100%)
- **Popular/Contemporary** (0-100%)
- **World/Ethnic** (0-100%)

#### Group 6: Narrative & Contextual Function
- **Foreground Presence** (0-100)
- **Narrative Support** (0-100)
- **Emotional Directness** (0-100)

---

### OUTPUT: Lifebond MSV Parameters

#### Affect Parameters (0.0-1.0)
- **valence**: Positive vs negative emotional quality
- **arousal**: Low/calm vs high/energetic
- **tension**: Relaxed vs tense/anxious
- **agency**: Passive vs active/driven

#### Harmony Parameters (0.0-1.0)
- **brightness**: Dark/warm vs bright/clear
- **consonance**: Dissonant vs consonant
- **cadentialDrive**: Static vs strong progression

#### Temporal Parameters
- **tempo**: 0.0=58 BPM, 0.5=72 BPM, 1.0=100 BPM
- **regularity**: Rubato/free vs strict tempo (0.0-1.0)

#### Orchestration Parameters
- **sparsity**: 1 (dense, 4-6 stems) to 5 (minimal, 1 stem)
- **weights**: Map<String, double> - stem category weights

#### Texture Parameters (0.0-1.0)
- **intimacy**: Expansive vs close/personal
- **privacy**: Public vs private/internal

---

## Conversion Formulas

### 1. AFFECT PARAMETERS

#### Valence (Emotional Quality)
```
MSV.valence = (Group1.Valence / 100.0)

Adjustments:
- If Group3.ModalCharacter < 35: valence *= 0.7  (dark modes reduce valence)
- If Group3.ModalCharacter > 70: valence *= 1.15 (bright modes boost valence, cap at 1.0)
```

#### Arousal (Energy Level)
```
MSV.arousal = (Group1.Energy / 100.0)

Adjustments:
- If Group2.TempoIntensity > 75: arousal += 0.1 (fast tempo boosts arousal)
- If Group2.RhythmicComplexity > 70: arousal += 0.05 (complexity adds arousal)
- Cap final value at 1.0
```

#### Tension (Anxiety/Stress)
```
MSV.tension = (Group1.Tension / 100.0)

Adjustments:
- If Group3.Consonance < 35: tension += 0.15 (dissonance increases tension)
- If Group2.MetricStability < 40: tension += 0.1 (instability adds tension)
- Cap final value at 1.0
```

#### Agency (Active Control)
```
MSV.agency = ((Group1.Energy * 0.4) + (Group6.NarrativeSupport * 0.3) + (Group2.TempoIntensity * 0.3)) / 100.0

Rationale:
- High energy = active
- High narrative support = purposeful action
- Fast tempo = forward momentum
```

---

### 2. HARMONY PARAMETERS

#### Brightness (Timbral Color)
```
MSV.brightness = (Group3.ModalCharacter / 100.0)

Adjustments:
- If Group1.Valence > 70: brightness += 0.1 (positive emotion = brighter)
- If Group4.DynamicRange > 70: brightness += 0.05 (high dynamics = clarity)
- Cap final value at 1.0
```

#### Consonance (Harmonic Tension)
```
MSV.consonance = (Group3.Consonance / 100.0)

Adjustments:
- If Group1.Tension > 70: consonance *= 0.8 (tension reduces consonance)
- If Group5.WesternClassical > 60: consonance *= 1.1 (classical = more consonant, cap at 1.0)
```

#### Cadential Drive (Harmonic Momentum)
```
MSV.cadentialDrive = ((Group3.HarmonicDensity * 0.5) + (Group6.NarrativeSupport * 0.5)) / 100.0

Rationale:
- Complex harmony = more progression
- Narrative support = purposeful movement
```

---

### 3. TEMPORAL PARAMETERS

#### Tempo (BPM Mapping)
```
// Map Group2.TempoIntensity (0-100) to MSV.tempo (0.0-1.0)
// 0.0 = 58 BPM, 0.5 = 72 BPM, 1.0 = 100 BPM

TempoIntensity ranges:
- Low (0-33):     58-68 BPM  → MSV.tempo = 0.0 to 0.24
- Medium (34-66): 68-82 BPM  → MSV.tempo = 0.24 to 0.67
- High (67-100):  82-100 BPM → MSV.tempo = 0.67 to 1.0

Formula:
MSV.tempo = (Group2.TempoIntensity / 100.0)

Adjustments:
- If Group1.Energy < 30: tempo *= 0.85 (low energy = slower)
- If Group1.Arousal > 80: tempo *= 1.15 (high arousal = faster)
- Clamp to [0.0, 1.0]
```

#### Regularity (Metric Stability)
```
MSV.regularity = (Group2.MetricStability / 100.0)

Adjustments:
- If Group2.RhythmicComplexity > 75: regularity *= 0.85 (complexity reduces regularity)
- If Group1.Tension > 70: regularity *= 0.9 (tension reduces stability)
```

---

### 4. ORCHESTRATION PARAMETERS

#### Sparsity (Stem Count)
```
// Inverse relationship: High Instrumental Density → Low Sparsity
// Group4.InstrumentalDensity (0-100) → MSV.sparsity (5-1)

Density ranges:
- Low (0-33):    Sparse      → sparsity = 4-5 (1-2 stems)
- Medium (34-66): Moderate   → sparsity = 2-3 (2-3 stems)
- High (67-100):  Dense      → sparsity = 1-2 (4-6 stems)

Formula:
MSV.sparsity = 5 - (Group4.InstrumentalDensity / 25.0)
Round to nearest integer (1-5)

Adjustments:
- If Group4.SpatialWidth < 35: sparsity += 1 (narrow = more sparse, cap at 5)
- If intimacy > 0.7: sparsity = max(sparsity, 3) (intimate = at least moderate sparsity)
```

#### Weights (Stem Category Mapping)
```
// Map Cultural Identity (Group 5) to stem weights

weights = {
  "pad": 1.0,              // Always foundation
  "piano": 0.8,            // Nearly always present
  "rhythm": 0.0,           // Calculated below
  "melody": 0.0,           // Calculated below
  "bass": 0.0,             // Calculated below
  "texture": 0.0,          // Calculated below
  "orchestral": 0.0,       // Calculated below
  "electronic": 0.0        // Calculated below
}

// Rhythm weight (based on arousal + tempo)
weights["rhythm"] = (MSV.arousal + MSV.tempo) / 2.0
If sparsity >= 4: weights["rhythm"] *= 0.5  (sparse = less rhythm)

// Melody weight (based on agency + narrative)
weights["melody"] = (MSV.agency + (Group6.NarrativeSupport / 100.0)) / 2.0
If sparsity >= 4: weights["melody"] *= 0.6

// Bass weight (based on energy + density)
weights["bass"] = ((Group1.Energy / 100.0) + (1.0 - (Group4.InstrumentalDensity / 100.0))) / 2.0
If sparsity >= 4: weights["bass"] = 0.0  (no bass in sparse arrangements)

// Texture weight (based on intimacy + privacy)
weights["texture"] = (intimacy + privacy) / 2.0
Always present at some level for atmospheric depth

// Cultural weights
weights["orchestral"] = Group5.WesternClassical / 100.0
weights["electronic"] = Group5.PopularContemporary / 100.0
weights["world"] = Group5.WorldEthnic / 100.0

// Normalize weights to reasonable ranges (0.0-1.0)
```

---

### 5. TEXTURE PARAMETERS

#### Intimacy (Spatial Closeness)
```
// Inverse of Spatial Width and Density
MSV.intimacy = 1.0 - ((Group4.SpatialWidth * 0.6) + (Group4.InstrumentalDensity * 0.4)) / 100.0

Adjustments:
- If Group6.ForegroundPresence < 40: intimacy += 0.15 (background = intimate)
- If Group4.DynamicRange < 35: intimacy += 0.1 (compressed = close)
- Cap final value at 1.0
```

#### Privacy (Internal vs External)
```
MSV.privacy = 1.0 - ((Group6.ForegroundPresence * 0.5) + (Group4.SpatialWidth * 0.3) + (Group6.EmotionalDirectness * 0.2)) / 100.0

Rationale:
- Low presence = private/internal
- Narrow width = personal
- Subtle emotion = private reflection

Adjustments:
- If intimacy > 0.7: privacy = max(privacy, 0.6) (intimate implies at least moderate privacy)
```

---

## Stem Selection Guide

Based on converted MSV parameters, select appropriate stems:

### Foundation Stems (Always Required)

#### Pad Selection
```
If valence < 0.3: Use pad_dark, pad_drone_low, pad_synth_digital
If valence > 0.7: Use pad_warm, pad_ethereal, pad_strings
If 0.3 <= valence <= 0.7: Use pad_tape_saturation, pad_analog, pad_granular

Cultural modifiers:
- If weights["orchestral"] > 0.6: Prefer pad_strings, pad_choir
- If weights["electronic"] > 0.6: Prefer pad_synth_analog, pad_synth_digital
- If weights["world"] > 0.6: Prefer pad_field_recording, pad_drone
```

#### Piano/Harmonic Selection
```
If intimacy > 0.7: Use piano_felt, piano_prepared, music_box
If brightness > 0.7: Use piano_bright, celeste, harp
If consonance < 0.4: Use piano_detuned, prepared_piano
If agency > 0.7: Use piano_bright, rhodes (with arpeggios)

Cultural modifiers:
- If weights["orchestral"] > 0.6: Prefer concert piano, harp, celeste
- If weights["electronic"] > 0.6: Prefer rhodes, wurlitzer, synth leads
- If weights["world"] > 0.6: Prefer kalimba, dulcimer, ethnic instruments
```

---

### Rhythm Stems (Conditional)

```
If weights["rhythm"] < 0.3: Skip rhythm entirely (or use minimal)
If 0.3 <= weights["rhythm"] < 0.6: Use minimal rhythm
If 0.6 <= weights["rhythm"] < 0.8: Use light rhythm
If weights["rhythm"] >= 0.8: Use full rhythm

Minimal rhythm (low arousal):
- brush_whisper, shaker_soft, finger_snaps, stick_clicks

Light rhythm (medium arousal):
- brush_swing, kick_soft, hihat_closed, cajon, tabla

Full rhythm (high arousal):
- kick_punch, snare_crisp, hihat_open, cymbals_crash, toms_full

Irregular rhythm (high tension, low regularity):
- stutter_glitch, polyrhythm_odd, rubato_drums, industrial_hits
```

---

### Melodic Stems (Conditional)

```
If weights["melody"] < 0.4: Skip melody
If agency < 0.3: Use counter melody or ambient melody
If agency > 0.7: Use lead melody

High agency (active):
- violin_solo, flute, synth_lead_bright, trumpet_muted

Medium agency (contemplative):
- cello_melody, clarinet, sax_tenor, vibraphone

Low agency (passive):
- strings_pizzicato, kalimba, music_box, pan_flute

Cultural modifiers:
- Orchestral: violin_solo, cello, flute, oboe
- Electronic: synth_lead_warm, synth_lead_bright
- World: shakuhachi, erhu, duduk, ney
```

---

### Texture Stems (Conditional)

```
Always include at least one texture stem for depth.

If intimacy > 0.7 AND privacy > 0.6:
- vinyl_crackle, tape_hiss, room_tone_small, breath
- paper_rustle, pen_writing, typewriter, fireplace_crackle

If intimacy < 0.4 AND privacy < 0.4:
- reverb_tail_long, crowd_murmur, city_ambience, wind_open
- ocean_distant, birds_forest, thunder_distant

If tension > 0.7:
- granular_dark, bit_crush, sample_stutter, time_stretch
- industrial ambience, distorted textures

If valence > 0.7:
- granular_shimmer, reverse_cymbal, chimes, bells
- natural ambiences (birds, water)
```

---

### Bass Stems (Conditional)

```
If weights["bass"] < 0.3: Skip bass
If sparsity >= 4: Skip bass (too dense for sparse arrangements)

If arousal > 0.7:
- bass_electric_pick, bass_synth_fm, sub_bass_synth

If arousal < 0.4:
- bass_upright, bass_fretless, cello_bass_notes

If tension > 0.6:
- bass_chromatic, sub_bass_sine (physical weight)

Cultural modifiers:
- Classical: bass_upright, cello_bass_notes, double_bass
- Electronic: sub_bass_synth, bass_synth_analog, bass_drum_sub
- World: various ethnic bass instruments
```

---

## Example Conversions

### Example 1: Tense Boss Battle

**INPUT (6-Group Framework):**
```
Group 1 (Emotional):
- Energy: 95
- Valence: 20
- Tension: 95

Group 2 (Temporal):
- Tempo Intensity: 85
- Rhythmic Complexity: 75
- Metric Stability: 90

Group 3 (Harmonic):
- Consonance: 30%
- Modal Character: 20% (dark)
- Harmonic Density: 50%

Group 4 (Textural):
- Instrumental Density: 85
- Spatial Width: 90
- Dynamic Range: 95

Group 5 (Cultural):
- Western Classical: 40%
- Popular/Contemporary: 60%
- World/Ethnic: 0%

Group 6 (Functional):
- Foreground Presence: 95
- Narrative Support: 85
- Emotional Directness: 90
```

**OUTPUT (MSV Parameters):**
```dart
final msv = MusicStateVector(
  // Affect
  valence: 0.14,        // 20/100 * 0.7 (dark modal reduction)
  arousal: 0.95,        // 95/100
  tension: 0.95,        // 95/100
  agency: 0.84,         // (95*0.4 + 85*0.3 + 85*0.3) / 100

  // Harmony
  brightness: 0.20,     // Dark modes
  consonance: 0.24,     // 30/100 * 0.8 (high tension reduction)
  cadentialDrive: 0.68, // (50*0.5 + 85*0.5) / 100

  // Temporal
  tempo: 0.85,          // 85/100
  regularity: 0.81,     // 90/100 * 0.9 (complexity reduction)

  // Orchestration
  sparsity: 1,          // 5 - (85/25) = 1.6 → round to 2, but high density = 1
  weights: {
    'pad': 1.0,
    'piano': 0.8,
    'rhythm': 0.9,      // High arousal + tempo
    'melody': 0.85,     // High agency + narrative
    'bass': 0.8,        // High energy
    'texture': 0.1,     // Low intimacy/privacy (public/exposed)
    'orchestral': 0.4,
    'electronic': 0.6,
  },

  // Texture
  intimacy: 0.10,       // 1.0 - (90*0.6 + 85*0.4) / 100 = 0.11
  privacy: 0.13,        // 1.0 - (95*0.5 + 90*0.3 + 90*0.2) / 100
);
```

**SELECTED STEMS:**
```
Foundation:
- pad_synth_digital (dark, tense, electronic)
- bass_synth_fm (bright, aggressive electronic bass)

Rhythm:
- kick_punch
- snare_crisp
- hihat_open
- cymbals_crash

Melody:
- synth_lead_bright (high agency, electronic)
- strings_tremolo (tension, orchestral)

Orchestral Support:
- brass_stabs (punctuation)
- strings_dissonant (tension)

Total: 9 stems (sparsity=1 allows 4-6, but high density justifies more)
```

---

### Example 2: Peaceful Village

**INPUT (6-Group Framework):**
```
Group 1 (Emotional):
- Energy: 25
- Valence: 80
- Tension: 15

Group 2 (Temporal):
- Tempo Intensity: 30
- Rhythmic Complexity: 35
- Metric Stability: 50

Group 3 (Harmonic):
- Consonance: 70%
- Modal Character: 75% (bright)
- Harmonic Density: -45% (simple, sparse)

Group 4 (Textural):
- Instrumental Density: 35
- Spatial Width: 60
- Dynamic Range: 40

Group 5 (Cultural):
- Western Classical: 20%
- Popular/Contemporary: 0%
- World/Ethnic: 80%

Group 6 (Functional):
- Foreground Presence: 30
- Narrative Support: 40
- Emotional Directness: 45
```

**OUTPUT (MSV Parameters):**
```dart
final msv = MusicStateVector(
  // Affect
  valence: 0.92,        // 80/100 * 1.15 (bright modal boost, cap at 1.0) → 0.92
  arousal: 0.25,        // 25/100
  tension: 0.15,        // 15/100

  agency: 0.29,         // (25*0.4 + 40*0.3 + 30*0.3) / 100

  // Harmony
  brightness: 0.85,     // 75/100 + 0.1 (high valence)
  consonance: 0.70,     // 70/100
  cadentialDrive: 0.20, // Low density + low narrative

  // Temporal
  tempo: 0.26,          // 30/100 * 0.85 (low energy adjustment)
  regularity: 0.50,     // 50/100

  // Orchestration
  sparsity: 4,          // 5 - (35/25) = 3.6 → round to 4
  weights: {
    'pad': 1.0,
    'piano': 0.8,
    'rhythm': 0.13,     // Very low (arousal 0.25 + tempo 0.26) / 2 * 0.5 (sparse)
    'melody': 0.23,     // Low agency
    'bass': 0.0,        // Sparsity 4 = no bass
    'texture': 0.65,    // Moderate intimacy/privacy
    'orchestral': 0.2,
    'electronic': 0.0,
    'world': 0.8,
  },

  // Texture
  intimacy: 0.49,       // 1.0 - (60*0.6 + 35*0.4) / 100 = 0.50
  privacy: 0.58,        // 1.0 - (30*0.5 + 60*0.3 + 45*0.2) / 100
);
```

**SELECTED STEMS:**
```
Foundation:
- pad_ethereal (bright, open, peaceful)
- kalimba (world, melodic, simple)

Rhythm (minimal):
- shaker_soft (gentle pulse)

Texture:
- birds_forest (natural, peaceful ambience)
- wind_chimes_close (delicate, world aesthetic)

Total: 5 stems (sparsity=4 allows 1-2 core + textures)
```

---

### Example 3: Melancholic Private Moment

**INPUT (6-Group Framework):**
```
Group 1 (Emotional):
- Energy: 30
- Valence: 35
- Tension: 55

Group 2 (Temporal):
- Tempo Intensity: 25
- Rhythmic Complexity: 20
- Metric Stability: 65

Group 3 (Harmonic):
- Consonance: 60%
- Modal Character: 35% (Dorian - neutral/bittersweet)
- Harmonic Density: 5%

Group 4 (Textural):
- Instrumental Density: 25
- Spatial Width: 35
- Dynamic Range: 60

Group 5 (Cultural):
- Western Classical: 85%
- Popular/Contemporary: 15%
- World/Ethnic: 0%

Group 6 (Functional):
- Foreground Presence: 35
- Narrative Support: 80
- Emotional Directness: 50
```

**OUTPUT (MSV Parameters):**
```dart
final msv = MusicStateVector(
  // Affect
  valence: 0.35,        // 35/100
  arousal: 0.30,        // 30/100
  tension: 0.55,        // 55/100
  agency: 0.36,         // (30*0.4 + 80*0.3 + 25*0.3) / 100

  // Harmony
  brightness: 0.40,     // 35/100 + 0.05 (moderate dynamics)
  consonance: 0.66,     // 60/100 * 1.1 (classical boost, cap at 1.0) → 0.66
  cadentialDrive: 0.43, // (5*0.5 + 80*0.5) / 100

  // Temporal
  tempo: 0.21,          // 25/100 * 0.85 (low energy)
  regularity: 0.65,     // 65/100

  // Orchestration
  sparsity: 4,          // 5 - (25/25) = 4
  weights: {
    'pad': 1.0,
    'piano': 0.8,
    'rhythm': 0.0,      // Very sparse
    'melody': 0.58,     // Cello melody for emotional depth
    'bass': 0.0,        // Sparsity 4
    'texture': 0.85,    // High intimacy + privacy
    'orchestral': 0.85,
    'electronic': 0.15,
  },

  // Texture
  intimacy: 0.75,       // 1.0 - (35*0.6 + 25*0.4) / 100 + 0.15 (low presence)
  privacy: 0.73,        // 1.0 - (35*0.5 + 35*0.3 + 50*0.2) / 100
);
```

**SELECTED STEMS:**
```
Foundation:
- pad_dark (melancholic, low valence)
- piano_detuned (nostalgic, bittersweet Dorian)

Melody:
- cello_melody (emotional depth, orchestral, narrative support)

Texture:
- room_tone_small (intimate, private)
- vinyl_crackle (nostalgic, intimate)
- rain_window (melancholic atmosphere)

Total: 6 stems (sparsity=4 allows 1-2 core + textures for emotional richness)
```

---

## Implementation Checklist

When converting 6-group parameters to MSV:

### Pre-Conversion
- [ ] Validate all input parameters are in correct ranges (0-100 or 0-100%)
- [ ] Ensure Group 3 (Harmonic) sums to ~100% (±10% tolerance)
- [ ] Ensure Group 5 (Cultural) sums to ~100% (±10% tolerance)

### Conversion Process
- [ ] Calculate affect parameters (valence, arousal, tension, agency)
- [ ] Calculate harmony parameters (brightness, consonance, cadentialDrive)
- [ ] Calculate temporal parameters (tempo, regularity)
- [ ] Calculate sparsity from instrumental density
- [ ] Calculate stem weights based on all groups
- [ ] Calculate texture parameters (intimacy, privacy)
- [ ] Apply all adjustments and modifiers
- [ ] Clamp all values to valid ranges (0.0-1.0 or 1-5)

### Post-Conversion
- [ ] Verify MSV parameters are coherent (e.g., high intimacy should correlate with higher privacy)
- [ ] Select appropriate stems based on weights and sparsity
- [ ] Ensure stem count matches sparsity level
- [ ] Validate stem compatibility (same tempo/key per cue)
- [ ] Generate Lyria prompts for selected stems
- [ ] Calculate loop points (8 bars, bar-aligned)

---

## Usage Example

```python
# Pseudo-code for conversion tool

def convert_to_msv(six_group_params):
    """
    Convert 6-group framework parameters to MSV.
    
    Args:
        six_group_params: Dictionary with keys:
            - emotional: {energy, valence, tension}
            - temporal: {tempo_intensity, rhythmic_complexity, metric_stability}
            - harmonic: {consonance, modal_character, harmonic_density}
            - textural: {instrumental_density, spatial_width, dynamic_range}
            - cultural: {western_classical, popular, world_ethnic}
            - functional: {foreground_presence, narrative_support, emotional_directness}
    
    Returns:
        msv: MusicStateVector object
    """
    
    # Extract parameters
    e = six_group_params['emotional']
    t = six_group_params['temporal']
    h = six_group_params['harmonic']
    tex = six_group_params['textural']
    c = six_group_params['cultural']
    f = six_group_params['functional']
    
    # Calculate affect
    valence = (e['valence'] / 100.0)
    if h['modal_character'] < 35:
        valence *= 0.7
    elif h['modal_character'] > 70:
        valence = min(valence * 1.15, 1.0)
    
    arousal = (e['energy'] / 100.0)
    if t['tempo_intensity'] > 75:
        arousal = min(arousal + 0.1, 1.0)
    if t['rhythmic_complexity'] > 70:
        arousal = min(arousal + 0.05, 1.0)
    
    tension = (e['tension'] / 100.0)
    if h['consonance'] < 35:
        tension = min(tension + 0.15, 1.0)
    if t['metric_stability'] < 40:
        tension = min(tension + 0.1, 1.0)
    
    agency = ((e['energy'] * 0.4) + (f['narrative_support'] * 0.3) + (t['tempo_intensity'] * 0.3)) / 100.0
    
    # Calculate harmony
    brightness = (h['modal_character'] / 100.0)
    if e['valence'] > 70:
        brightness = min(brightness + 0.1, 1.0)
    if tex['dynamic_range'] > 70:
        brightness = min(brightness + 0.05, 1.0)
    
    consonance = (h['consonance'] / 100.0)
    if e['tension'] > 70:
        consonance *= 0.8
    if c['western_classical'] > 60:
        consonance = min(consonance * 1.1, 1.0)
    
    cadential_drive = ((h['harmonic_density'] * 0.5) + (f['narrative_support'] * 0.5)) / 100.0
    
    # Calculate temporal
    tempo = (t['tempo_intensity'] / 100.0)
    if e['energy'] < 30:
        tempo *= 0.85
    if arousal > 0.8:
        tempo *= 1.15
    tempo = max(0.0, min(tempo, 1.0))
    
    regularity = (t['metric_stability'] / 100.0)
    if t['rhythmic_complexity'] > 75:
        regularity *= 0.85
    if e['tension'] > 70:
        regularity *= 0.9
    
    # Calculate orchestration
    sparsity = round(5 - (tex['instrumental_density'] / 25.0))
    sparsity = max(1, min(sparsity, 5))
    
    intimacy = 1.0 - ((tex['spatial_width'] * 0.6) + (tex['instrumental_density'] * 0.4)) / 100.0
    if f['foreground_presence'] < 40:
        intimacy = min(intimacy + 0.15, 1.0)
    if tex['dynamic_range'] < 35:
        intimacy = min(intimacy + 0.1, 1.0)
    
    if tex['spatial_width'] < 35:
        sparsity = min(sparsity + 1, 5)
    if intimacy > 0.7:
        sparsity = max(sparsity, 3)
    
    # Calculate weights
    weights = calculate_weights(
        arousal, tempo, agency, f['narrative_support'],
        e['energy'], tex['instrumental_density'],
        intimacy, privacy, sparsity,
        c['western_classical'], c['popular'], c['world_ethnic']
    )
    
    # Calculate texture
    privacy = 1.0 - ((f['foreground_presence'] * 0.5) + (tex['spatial_width'] * 0.3) + (f['emotional_directness'] * 0.2)) / 100.0
    if intimacy > 0.7:
        privacy = max(privacy, 0.6)
    
    # Build MSV object
    msv = MusicStateVector(
        valence=valence,
        arousal=arousal,
        tension=tension,
        agency=agency,
        brightness=brightness,
        consonance=consonance,
        cadentialDrive=cadential_drive,
        tempo=tempo,
        regularity=regularity,
        sparsity=sparsity,
        weights=weights,
        intimacy=intimacy,
        privacy=privacy,
    )
    
    return msv
```

---

## Quality Assurance

### Validation Rules

After conversion, verify:

1. **Coherence checks:**
   - High intimacy (>0.7) should have privacy >0.5
   - High tension (>0.7) should have consonance <0.6
   - High arousal (>0.7) should have tempo >0.5
   - Low valence (<0.3) should have brightness <0.5

2. **Sparsity vs. weights:**
   - Sparsity 5: Only pad + piano (maybe texture)
   - Sparsity 4: Pad + piano + 1-2 textures
   - Sparsity 3: Pad + piano + optional rhythm/melody
   - Sparsity 2: Pad + piano + rhythm + texture
   - Sparsity 1: All categories active (4-6 stems)

3. **Cultural consistency:**
   - If weights["orchestral"] > 0.7: Use classical instruments
   - If weights["electronic"] > 0.7: Use synths/electronic
   - If weights["world"] > 0.7: Use ethnic instruments

4. **Emotional alignment:**
   - Calm (arousal <0.3): Minimal rhythm, simple harmony
   - Tense (tension >0.7): Dissonance, irregular rhythm
   - Positive (valence >0.7): Bright modes, consonant harmony
   - Active (agency >0.7): Strong melodies, clear rhythms

---

## Notes for Developers

### When to Use This Conversion

✅ **Use when:**
- Importing presets from other music generation tools
- Converting existing music parameters to MSV format
- Bridging between different adaptive music systems
- Batch-converting large parameter sets

❌ **Don't use when:**
- Working directly in MSV (no conversion needed)
- Parameters already match Lifebond's native format
- Real-time game state already generates MSV directly

### Performance Considerations

- Conversion is **one-time** per cue/preset
- Pre-convert and cache results for frequently used states
- Conversion takes <1ms on modern hardware
- No runtime overhead after conversion

### Customization

Feel free to adjust:
- Adjustment weights (e.g., 0.7 dark modal reduction)
- Threshold values (e.g., >75 for tempo boost)
- Stem selection priorities based on your asset library
- Cultural weight mapping for your specific instruments

---

## Appendix: Quick Reference

### MSV Value Ranges

| Parameter | Min | Max | Typical |
|-----------|-----|-----|---------|
| valence | 0.0 | 1.0 | 0.3-0.8 |
| arousal | 0.0 | 1.0 | 0.2-0.8 |
| tension | 0.0 | 1.0 | 0.1-0.9 |
| agency | 0.0 | 1.0 | 0.2-0.8 |
| brightness | 0.0 | 1.0 | 0.3-0.8 |
| consonance | 0.0 | 1.0 | 0.4-0.9 |
| cadentialDrive | 0.0 | 1.0 | 0.2-0.7 |
| tempo | 0.0 | 1.0 | 0.3-0.7 (60-80 BPM) |
| regularity | 0.0 | 1.0 | 0.5-0.9 |
| sparsity | 1 | 5 | 2-4 |
| intimacy | 0.0 | 1.0 | 0.3-0.8 |
| privacy | 0.0 | 1.0 | 0.3-0.8 |

### Stem Count by Sparsity

| Sparsity | Stem Count | Typical Categories |
|----------|------------|-------------------|
| 1 | 4-6 | All categories active |
| 2 | 3-4 | Foundation + rhythm + texture |
| 3 | 2-3 | Foundation + optional |
| 4 | 1-2 | Foundation + texture |
| 5 | 1 | Foundation only |

---

**Document Version:** 1.0  
**Last Updated:** October 15, 2025  
**Compatible with:** Lifebond MSV System v1.0, 6-Group Framework v2.0

