# Music Stem Generation Guide

Complete workflow for generating loop-safe music stems for Unwritten using Lyria.

## Option 1: Using music.V2 (Recommended)

### Setup

```bash
cd music.V2
npm install
npm run dev
# Opens http://localhost:5173
```

### Generation Workflow

#### 1. Calm Positive (Priority 1)

**Target Specs:**
- **Tempo:** 72 BPM
- **Meter:** 4/4
- **Bars:** 8
- **Key:** C Major (Ionian)
- **Duration:** 26.667 seconds (26667ms)

**MSV Settings in UI:**
```json
{
  "affect": {
    "valence": 0.75,
    "arousal": 0.30,
    "tension": 0.20,
    "agency": 0.60
  },
  "harmony": {
    "brightness": 0.70,
    "consonance": 0.85,
    "cadentialDrive": 0.65
  },
  "temporal": {
    "tempo": 0.40,
    "regularity": 0.80
  },
  "orchestration": {
    "sparsity": 3,
    "weights": {
      "pad": 0.60,
      "piano": 0.70,
      "light_rhythm": 0.25
    }
  },
  "texture": {
    "intimacy": 0.60,
    "bloom": 0.45
  },
  "style": {
    "journal": 0.60,
    "lofi_jazz": 0.30
  }
}
```

**Lyria Prompt:**
```
Create a calm, peaceful composition at 72 BPM in C Major. 8 bars, 4/4 time.

Style: Intimate journal music, lo-fi jazz influence. Warm and hopeful.

Stems needed (separate files):
1. Ambient pad - warm, sustained, gentle
2. Felt piano - simple melody, consonant chords, add9 voicings
3. Light brush percussion - subtle, jazzy, very soft

Requirements:
- Loop-safe: smooth fade in/out at bar boundaries
- Bar-aligned: exactly 26.667 seconds
- Clean separation between stems
- Same tempo/key across all stems
```

**Download:**
1. Export each stem separately
2. Save as: `calm_positive_pad_raw.wav`, `calm_positive_piano_raw.wav`, `calm_positive_brush_raw.wav`

---

#### 2. Melancholic Private (Priority 2)

**Target Specs:**
- **Tempo:** 60 BPM
- **Meter:** 4/4
- **Bars:** 8
- **Key:** C Dorian
- **Duration:** 32.000 seconds (32000ms)

**MSV Settings:**
```json
{
  "affect": {
    "valence": 0.30,
    "arousal": 0.25,
    "tension": 0.40,
    "agency": 0.40
  },
  "harmony": {
    "brightness": 0.35,
    "consonance": 0.70,
    "cadentialDrive": 0.40
  },
  "temporal": {
    "tempo": 0.25,
    "regularity": 0.60
  },
  "orchestration": {
    "sparsity": 2,
    "weights": {
      "pad": 0.70,
      "piano": 0.65,
      "texture": 0.30
    }
  },
  "texture": {
    "intimacy": 0.80,
    "bloom": 0.50
  },
  "style": {
    "journal": 0.70,
    "ambient_tape": 0.40
  }
}
```

**Lyria Prompt:**
```
Create a melancholic, intimate composition at 60 BPM in C Dorian. 8 bars, 4/4 time.

Style: Very close, private journal music. Sad but not depressing. Tape-like quality.

Stems needed (separate files):
1. Dark ambient pad - rich, warm, sustained low frequencies
2. Intimate piano - sparse, reflective, simple add9 chords, rubato feel
3. Subtle texture - tape grain, vinyl crackle, or gentle shaker

Requirements:
- Loop-safe: smooth fade in/out at bar boundaries
- Bar-aligned: exactly 32.000 seconds
- Clean separation between stems
- Same tempo/key across all stems
```

---

#### 3. Motivated (Priority 3, Optional)

**Target Specs:**
- **Tempo:** 80 BPM
- **Meter:** 4/4
- **Bars:** 8
- **Key:** C Mixolydian
- **Duration:** 24.000 seconds (24000ms)

**Lyria Prompt:**
```
Create an energetic, motivated composition at 80 BPM in C Mixolydian. 8 bars, 4/4 time.

Style: Productive work music. Steady pulse, uplifting but grounded.

Stems needed (separate files):
1. Bright pad - open, supportive, steady
2. Piano - rhythmic chords, driving but not aggressive
3. Light percussion - steady brushes, snaps, light kick pattern
4. Optional strings - warm, supportive harmony

Requirements:
- Loop-safe: smooth fade in/out at bar boundaries
- Bar-aligned: exactly 24.000 seconds
- Clean separation between stems
- Same tempo/key across all stems
```

---

## Option 2: Direct Lyria API (Advanced)

### Setup

```bash
# Set API key
export GEMINI_API_KEY="your-key-here"

# Or use .env file
echo "GEMINI_API_KEY=your-key" > .env
```

### Python Script (requires google-generativeai)

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Note: Lyria API details may vary
# This is a conceptual example
model = genai.GenerativeModel('lyria-music')

response = model.generate_content(
    "Create calm peaceful music at 72 BPM...",
    generation_config={
        "tempo": 72,
        "duration": 27,
        "stems": ["pad", "piano", "percussion"]
    }
)

# Download stems
for stem in response.stems:
    stem.save(f"calm_positive_{stem.name}.wav")
```

---

## Step 2: Convert to Opus

### Install FFmpeg (if needed)

**Windows:**
```powershell
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### Conversion Script

Create `scripts/convert_to_opus.ps1`:

```powershell
param(
    [string]$InputDir = ".",
    [string]$OutputDir = "../app/assets/music/cues"
)

# Calm Positive
Write-Host "Converting calm_positive stems..."
New-Item -ItemType Directory -Force -Path "$OutputDir/calm_positive"

ffmpeg -i "$InputDir/calm_positive_pad_raw.wav" `
    -c:a libopus -b:a 96k `
    -vn -y `
    "$OutputDir/calm_positive/pad.opus"

ffmpeg -i "$InputDir/calm_positive_piano_raw.wav" `
    -c:a libopus -b:a 96k `
    -vn -y `
    "$OutputDir/calm_positive/piano.opus"

ffmpeg -i "$InputDir/calm_positive_brush_raw.wav" `
    -c:a libopus -b:a 96k `
    -vn -y `
    "$OutputDir/calm_positive/brush.opus"

# Melancholic Private
Write-Host "Converting melancholic_private stems..."
New-Item -ItemType Directory -Force -Path "$OutputDir/melancholic_private"

ffmpeg -i "$InputDir/melancholic_pad_raw.wav" `
    -c:a libopus -b:a 96k `
    -vn -y `
    "$OutputDir/melancholic_private/pad.opus"

ffmpeg -i "$InputDir/melancholic_piano_raw.wav" `
    -c:a libopus -b:a 96k `
    -vn -y `
    "$OutputDir/melancholic_private/piano.opus"

ffmpeg -i "$InputDir/melancholic_shaker_raw.wav" `
    -c:a libopus -b:a 96k `
    -vn -y `
    "$OutputDir/melancholic_private/shaker.opus"

Write-Host "Conversion complete!"
Write-Host "Files saved to: $OutputDir"
```

**Usage:**
```powershell
cd scripts
./convert_to_opus.ps1 -InputDir "./raw_stems" -OutputDir "../app/assets/music/cues"
```

---

## Step 3: Validate Loop Points

### Check Duration

```bash
# Check if files are correct length
ffprobe -i calm_positive/pad.opus -show_entries format=duration -v quiet -of csv="p=0"
# Should output: 26.667000

ffprobe -i melancholic_private/pad.opus -show_entries format=duration -v quiet -of csv="p=0"
# Should output: 32.000000
```

### Calculate Loop End Times

```dart
// Formula for loopEndMs
final bpm = 72;
final bars = 8;
final meterBeats = 4;

final secondsPerBar = (60.0 / bpm) * meterBeats; // 3.333...
final loopDurationSeconds = secondsPerBar * bars; // 26.667
final loopEndMs = (loopDurationSeconds * 1000).round(); // 26667
```

**Quick reference:**
- 72 BPM × 8 bars × 4/4 = 26667ms
- 60 BPM × 8 bars × 4/4 = 32000ms
- 80 BPM × 8 bars × 4/4 = 24000ms

---

## Step 4: Update Cue Bank JSON

Already done in: `app/assets/music/cue_banks/core_season_a.json`

Verify paths match:
```json
{
  "cues": [
    {
      "id": "calm_positive_c72",
      "tempo": 72,
      "stems": {
        "pad": "assets/music/cues/calm_positive/pad.opus",
        "piano": "assets/music/cues/calm_positive/piano.opus",
        "light_rhythm": "assets/music/cues/calm_positive/brush.opus"
      }
    }
  ]
}
```

---

## Step 5: Test

```bash
cd app
flutter run
```

**Check logs for:**
- "Cue bank loaded" (count > 0)
- "Selected cue: calm_positive_c72"
- "Music playback started"
- "Mix applied" with active stems

---

## Option 3: Test with Silence (Quick Validation)

If you want to test the architecture without real music:

```bash
# Generate 8 bars of silence at correct length
ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo -t 26.667 -c:a libopus -b:a 96k app/assets/music/cues/calm_positive/pad.opus
ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo -t 26.667 -c:a libopus -b:a 96k app/assets/music/cues/calm_positive/piano.opus
ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo -t 26.667 -c:a libopus -b:a 96k app/assets/music/cues/calm_positive/brush.opus

ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo -t 32.000 -c:a libopus -b:a 96k app/assets/music/cues/melancholic_private/pad.opus
ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo -t 32.000 -c:a libopus -b:a 96k app/assets/music/cues/melancholic_private/piano.opus
ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo -t 32.000 -c:a libopus -b:a 96k app/assets/music/cues/melancholic_private/shaker.opus
```

This validates:
- ✅ File loading works
- ✅ Bar quantization works
- ✅ Crossfades work
- ✅ Cue selection works
- ❌ No actual music (add later)

---

## Troubleshooting

### Issue: Stems not exactly the same length
**Solution:** Trim/extend in Audacity before converting:
```
1. Open in Audacity
2. Generate > Silence... (if too short)
3. Effect > Truncate Silence... (if too long)
4. Ensure exact duration matches
```

### Issue: Pops/clicks at loop points
**Solution:** Add crossfade at loop boundaries:
```
1. Select last 100ms
2. Effect > Fade Out
3. Select first 100ms  
4. Effect > Fade In
```

### Issue: Stems don't mix well
**Solution:** Check levels:
```bash
# Normalize to -3dB headroom
ffmpeg -i input.wav -af "loudnorm=I=-16:LRA=11:TP=-1.5" output.wav
```

---

## Expected File Sizes

Per stem (8 bars, Opus @ 96kbps):
- **calm_positive** (~27s): ~320KB per stem, ~960KB total
- **melancholic_private** (~32s): ~384KB per stem, ~1.1MB total
- **motivated** (~24s): ~288KB per stem, ~1.1MB total (4 stems)

**Total for all 3 cues:** ~3-4MB

---

## Next Steps

1. Generate stems using music.V2 or Lyria API
2. Convert to Opus using provided script
3. Validate loop points and duration
4. Test in app
5. Iterate on mix balance if needed
6. Generate remaining 7 priority cues

