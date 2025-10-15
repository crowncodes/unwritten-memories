# Lyria Stem Generation Guide

Complete guide for generating adaptive music stems for the Lifebond game.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd scripts
pip install -r requirements_lyria.txt
```

### 2. Set Up API Key

Get your Google AI API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

```bash
# Option A: Environment variable
export GOOGLE_API_KEY="your-api-key-here"

# Option B: .env file in project root
echo "GOOGLE_API_KEY=your-api-key-here" > .env
```

### 3. Generate Your First Cue

```bash
# Mock mode (for testing structure)
python generate_lyria_stems.py --cue calm_positive

# With real API key
python generate_lyria_stems.py --cue calm_positive --api-key YOUR_KEY
```

---

## 📖 Usage Examples

### Generate Single Cue

```bash
python generate_lyria_stems.py --cue calm_positive --output ../app/assets/music/cues
```

### Generate All Cues

```bash
python generate_lyria_stems.py --cue all --output ../app/assets/music/cues
```

### Generate JSON Only (No Audio)

```bash
python generate_lyria_stems.py --cue calm_positive --json-only
```

This creates cue bank JSON entries without attempting to generate audio files.

---

## 🎵 Available Cues

### 1. **calm_positive**
- **Tempo**: 72 BPM
- **Key**: C Ionian (major)
- **Stems**: pad, piano, light_rhythm
- **MSV**: High valence (0.7), Low arousal (0.3), High intimacy (0.7)
- **Use**: Default baseline, journal writing, peaceful moments

### 2. **melancholic_private**
- **Tempo**: 60 BPM
- **Key**: C Dorian
- **Stems**: pad, piano, cello
- **MSV**: Low valence (0.3), Low arousal (0.2), High intimacy (0.8)
- **Use**: Sad moments, low capacity, introspection

### 3. **motivated**
- **Tempo**: 80 BPM
- **Key**: G Mixolydian
- **Stems**: pad, piano, kick, hihat
- **MSV**: Moderate valence (0.6), High arousal (0.6), Moderate intimacy (0.5)
- **Use**: Work scenes, aspiration, goal-setting

---

## 📂 Output Structure

```
app/assets/music/cues/
├── calm_positive/
│   ├── pad.opus
│   ├── piano.opus
│   └── light_rhythm.opus
├── melancholic_private/
│   ├── pad.opus
│   ├── piano.opus
│   └── cello.opus
├── motivated/
│   ├── pad.opus
│   ├── piano.opus
│   ├── kick.opus
│   └── hihat.opus
└── cue_bank_generated.json
```

---

## 🔧 Current Limitations

### ⚠️ Lyria API Access

**Important**: As of late 2024, Lyria/MusicLM may not have direct public API access.

The script provides **two modes**:

### 1. **Mock Mode** (Default)
- Creates directory structure
- Generates placeholder files
- Produces valid JSON cue bank entries
- Perfect for testing integration

### 2. **Specification Mode** (With API Key)
- Uses Gemini to generate detailed music specifications
- Provides MIDI note ranges, velocity curves, effects chains
- Output can be used with:
  - Google AI Studio (manual generation)
  - DAW (Digital Audio Workstation) for manual creation
  - Future Lyria API when available

---

## 🎼 Alternative Generation Methods

If direct API access isn't available, use these workflows:

### Option 1: Google AI Studio (Web UI)

1. Go to [Google AI Studio](https://makersuite.google.com/)
2. Select "Music Generation" (if available)
3. Use the prompts from `CUE_DEFINITIONS` in the script
4. Download generated stems
5. Convert to Opus:

```bash
ffmpeg -i pad.wav -c:a libopus -b:a 96k -ar 48000 pad.opus
```

### Option 2: Use Music.V2 Tool

The project includes a web-based music generator in `music.V2/`:

```bash
cd music.V2
npm install
npm run dev
```

Then use the UI to adjust MSV parameters and generate stems.

### Option 3: Manual DAW Creation

Use the generated specifications with your DAW (Ableton, Logic, etc.):

1. Run script in specification mode
2. Follow the detailed instrument/effect specifications
3. Export each stem as 48kHz audio
4. Convert to Opus format
5. Place in appropriate directory

---

## 🔍 Understanding the Output

### Generated Cue Bank JSON

```json
{
  "cues": [
    {
      "id": "calm_positive_c72",
      "tempo": 72,
      "meterBeats": 4,
      "bars": 8,
      "loopStartMs": 0,
      "loopEndMs": 26667,
      "key": "C",
      "mode": "Ionian",
      "tags": ["calm_positive", "adaptive", "game"],
      "stems": {
        "pad": "assets/music/cues/calm_positive/pad.opus",
        "piano": "assets/music/cues/calm_positive/piano.opus",
        "light_rhythm": "assets/music/cues/calm_positive/light_rhythm.opus"
      }
    }
  ]
}
```

### Key Fields Explained

- **id**: Unique identifier (cue_name + key + tempo)
- **loopEndMs**: Calculated from tempo and bars for perfect loops
- **stems**: Paths relative to `app/assets/` directory
- **tags**: Used for MSV matching in the game engine

---

## 🛠️ Customizing Cues

### Add New Cue Definition

Edit `CUE_DEFINITIONS` in `generate_lyria_stems.py`:

```python
CUE_DEFINITIONS = {
    # ... existing cues ...
    
    "excited": {
        "tempo": 92,
        "key": "D",
        "mode": "Ionian",
        "bars": 8,
        "stems": ["bass", "kick", "snare", "brass"],
        "prompt": "Energetic bass with punchy drums and bright brass fanfare. 92 BPM, 8 bars, D major. Exciting, celebratory, social. High energy and forward momentum.",
        "msv": {
            "valence": 0.8,
            "arousal": 0.8,
            "tension": 0.2,
            "intimacy": 0.3,
            "sparsity": 2
        }
    }
}
```

### Modify Existing Prompts

Change the `prompt` field to adjust musical characteristics:

```python
"calm_positive": {
    # ... other fields ...
    "prompt": "YOUR CUSTOM PROMPT HERE. Be specific about instruments, tempo, mood, and loop requirements."
}
```

---

## 📋 Post-Generation Checklist

After generating stems:

### 1. ✅ Verify File Structure
```bash
tree app/assets/music/cues
```

### 2. ✅ Check Audio Format
```bash
# Should be Opus, 48kHz
ffprobe pad.opus
```

### 3. ✅ Test Loop Points
- Import into audio editor
- Verify seamless loop at calculated loopEndMs
- No clicks or pops at loop boundary

### 4. ✅ Update Cue Bank
```bash
# Copy entries from cue_bank_generated.json to:
app/assets/music/cue_banks/core_season_a.json
```

### 5. ✅ Update pubspec.yaml
```yaml
flutter:
  assets:
    - assets/music/cues/calm_positive/
    - assets/music/cues/melancholic_private/
    - assets/music/cues/motivated/
```

### 6. ✅ Test in Game
```bash
cd app
flutter run
# Check logs for "Music playback started"
```

---

## 🐛 Troubleshooting

### "No API key found" Warning

**Solution**: Set `GOOGLE_API_KEY` environment variable or create `.env` file.

```bash
export GOOGLE_API_KEY="your-key-here"
```

### "google-generativeai not installed"

**Solution**: Install dependencies.

```bash
pip install -r requirements_lyria.txt
```

### Generated Files Not Playing

**Solution**: Ensure correct Opus format.

```bash
# Convert to proper format
ffmpeg -i input.wav -c:a libopus -b:a 96k -ar 48000 output.opus
```

### Loop Not Seamless

**Solution**: 
1. Check audio tail doesn't cut off abruptly
2. Verify loopEndMs matches actual audio duration
3. Ensure bar-aligned (no tempo drift)
4. Add small crossfade in generation prompt

### Wrong loopEndMs Calculation

**Solution**: Verify tempo and time signature.

```python
# Formula for 4/4 time:
seconds_per_bar = (60.0 / tempo) * 4
total_duration = seconds_per_bar * bars
loop_end_ms = int(total_duration * 1000)

# Example: 72 BPM, 8 bars
# = (60/72) * 4 * 8 = 26.67 seconds = 26667ms
```

---

## 🎯 Workflow: Mock to Real

### Phase 1: Mock Generation (Testing)

```bash
# Generate structure without API
python generate_lyria_stems.py --cue all --json-only
```

**Output**: 
- Directory structure created
- JSON entries ready
- Integration testable

### Phase 2: Specification Generation (With API)

```bash
# Generate detailed specs with Gemini
python generate_lyria_stems.py --cue calm_positive --api-key YOUR_KEY
```

**Output**:
- Detailed instrument specifications
- MIDI note ranges
- Effects chain recommendations
- Use with AI Studio or DAW

### Phase 3: Real Audio (When Available)

```bash
# Direct generation (future)
python generate_lyria_stems.py --cue all --api-key YOUR_KEY
```

**Output**:
- Actual Opus files downloaded
- Ready to use in game

---

## 📊 Expected Performance

### Per Cue:
- **Generation time**: 1-5 minutes (depends on API)
- **File size**: ~1.5-3 MB (3 stems @ 500KB-1MB each)
- **Audio duration**: 19-32 seconds (depends on tempo)

### All Cues:
- **Total size**: ~5-10 MB (3 cues × 3 stems average)
- **Generation time**: 5-15 minutes
- **Result**: Playable adaptive music system

---

## 🔗 Related Files

- **Music Engine**: `app/lib/features/music/presentation/services/music_engine_service.dart`
- **MSV Model**: `app/lib/features/music/data/models/music_state_vector.dart`
- **Cue Bank**: `app/assets/music/cue_banks/core_season_a.json`
- **Implementation Doc**: `app/MUSIC_SYSTEM_IMPLEMENTATION.md`
- **Gem Prompt**: `LYRIA_STEM_GENERATOR_GEM_PROMPT.md`

---

## 💡 Tips

1. **Start small**: Generate `calm_positive` first, test full workflow
2. **Verify loops**: Always test seamless looping before batch generation
3. **Match keys**: Keep stems in same cue at same key/tempo
4. **Use specifications**: Even in mock mode, the specs are valuable for manual creation
5. **Document changes**: If you modify prompts, note what worked well

---

## 🆘 Need Help?

1. Check `app/MUSIC_SYSTEM_IMPLEMENTATION.md` for comprehensive documentation
2. Review `LYRIA_STEM_GENERATOR_GEM_PROMPT.md` for detailed MSV explanations
3. Test with mock mode first to verify integration
4. Use `app/lib/features/music/README.md` for engine details

---

**Happy generating! 🎵✨**

