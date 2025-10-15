# Music Generation Pipeline Scripts

**Layer 2 Tools**: Generation Pipeline automation scripts

These scripts implement the Generation Pipeline (Layer 2) from `00-MUSIC-SYSTEM-MASTER.md`. They process stems between the Design Tool (Layer 1) and Runtime System (Layer 3).

---

## Scripts Overview

| Script | Purpose | Status | Usage |
|--------|---------|--------|-------|
| `convert_to_opus.ps1` | Convert WAV stems to Opus @ 48kHz | ✅ Active | Production |
| `validate_stems.ps1` | Validate stem duration, format, loop points | ✅ Active | QA |
| `generate_silence_stems.ps1` | Generate silent test stems for architecture validation | ✅ Active | Testing |
| `generate_lyria_stems.py` | Lyria API integration template | ⚠️ Template | Example |

---

## 1. convert_to_opus.ps1

**Purpose**: Convert raw music stems (WAV) to Opus format @ 48kHz for optimal Flutter performance.

### Requirements
- FFmpeg installed (`choco install ffmpeg` or [ffmpeg.org](https://ffmpeg.org))
- Raw WAV stems from Lyria or DAW

### Usage
```powershell
cd docs\9.music\scripts

# Convert all stems in directory
.\convert_to_opus.ps1 -InputDir "./raw_stems" -OutputDir "../../../app/assets/music/stems"

# Default paths (current directory → app assets)
.\convert_to_opus.ps1
```

### Parameters
- `-InputDir`: Source directory with WAV files (default: current directory)
- `-OutputDir`: Destination for Opus files (default: `../../../app/assets/music/stems`)

### Output Format
- **Codec**: Opus
- **Sample Rate**: 48kHz
- **Bitrate**: 96kbps
- **Channels**: Stereo
- **Target Size**: ~2MB per stem for 8-bar loop

### What It Does
1. Checks for FFmpeg installation
2. Converts specified stem types (pad, piano, rhythm, etc.)
3. Creates directory structure automatically
4. Validates conversion success
5. Reports file sizes and success/failure

### Expected Stem Types
Based on Priority Tier 1 emotional states:
- `pad.opus` - Foundation ambient layer
- `piano.opus` - Harmonic/melodic core
- `light_rhythm.opus` - Subtle percussion (brush, shaker)
- `melody.opus` - Lead instrument (optional)
- `texture.opus` - Atmospheric layer (optional)

---

## 2. validate_stems.ps1

**Purpose**: Quality assurance - validates that stems meet technical requirements for looping and playback.

### Requirements
- FFmpeg/FFprobe installed
- Generated stem files in `app/assets/music/stems/`

### Usage
```powershell
cd docs\9.music\scripts

# Validate all stems
.\validate_stems.ps1

# Specify custom directory
.\validate_stems.ps1 -CuesDir "../../../app/assets/music/stems"
```

### Validation Checks

| Check | Requirement | Tolerance |
|-------|-------------|-----------|
| **Duration** | Matches expected bar length | ±0.1s |
| **Codec** | Opus | Exact |
| **Sample Rate** | 48000 Hz | Exact |
| **File Size** | Reasonable for duration/bitrate | ±50% |
| **Loop Points** | Bar-aligned (calculated from BPM) | Perfect |

### Expected Durations
- `calm_positive` (72 BPM, 8 bars): 26.667s
- `melancholic_private` (60 BPM, 8 bars): 32.000s
- `motivated` (80 BPM, 8 bars): 24.000s

### Output
- ✅ Green check: Stem passes all validation
- ❌ Red X: Issues found (duration mismatch, wrong format, etc.)
- Summary report with total issues count

### When to Run
- After stem generation
- Before committing stems to repository
- After converting from another format
- As part of CI/CD pipeline

---

## 3. generate_silence_stems.ps1

**Purpose**: Generate silent placeholder stems for testing the music system architecture without real audio.

### Requirements
- FFmpeg installed

### Usage
```powershell
cd docs\9.music\scripts

# Generate silent test stems
.\generate_silence_stems.ps1

# Custom output directory
.\generate_silence_stems.ps1 -OutputDir "../../../app/assets/music/stems"
```

### What It Generates
- **calm_positive**: 3 silent stems at 26.667s (72 BPM, 8 bars)
- **melancholic_private**: 3 silent stems at 32.000s (60 BPM, 8 bars)
- All in Opus format @ 48kHz, 96kbps

### Use Cases
1. **Architecture Testing**: Validate music engine without real music
2. **Cue Loading**: Test library loading and JSON parsing
3. **Transitions**: Verify bar-quantized crossfading works
4. **Integration**: Test game state → MSV → stem selection
5. **Performance**: Measure system overhead without audio processing

### What You Can Test
- ✅ Cue loading and selection
- ✅ Bar-quantized transitions
- ✅ Stem mixing and crossfades
- ✅ Game state integration
- ❌ Actual music quality (use real stems for this)

---

## 4. generate_lyria_stems.py

**Purpose**: Template/example for integrating with Google's Lyria API for music generation.

⚠️ **Status**: Template only - No public Lyria API currently available

### Requirements
```bash
pip install google-generativeai requests python-dotenv
```

### Environment Setup
```bash
# Set API key
export GOOGLE_API_KEY="your-key-here"

# Or use .env file
echo "GOOGLE_API_KEY=your-key" > .env
```

### Usage
```bash
cd docs/9.music/scripts

# Generate a specific cue
python generate_lyria_stems.py --cue calm_positive --output ../../../app/assets/music/stems

# Generate all cues
python generate_lyria_stems.py --cue all

# JSON-only mode (no stem generation)
python generate_lyria_stems.py --cue calm_positive --json-only
```

### What It Does (When Lyria API Exists)
1. Loads cue definitions (MSV parameters, tempo, key, mode)
2. Generates Lyria-compatible prompts
3. Calls Lyria API to generate individual stems
4. Downloads generated audio files
5. Creates cue bank JSON entries
6. Organizes stems in proper directory structure

### Current Behavior
- **MOCK MODE**: Generates specifications without real audio
- Uses Gemini to create detailed technical specifications
- Outputs JSON structure for cue bank
- Placeholder files created for testing

### Cue Definitions
Pre-configured in script:
- `calm_positive` (72 BPM, C Ionian)
- `melancholic_private` (60 BPM, C Dorian)
- `motivated` (80 BPM, G Mixolydian)

### Future Use
When Lyria API becomes publicly available:
1. Update API endpoint in `_real_generate()` method
2. Configure authentication
3. Test with one cue first
4. Batch generate all Priority Tier 1 cues (30 packages)

---

## Workflow: Complete Generation Pipeline

### Step 1: Design (Cloud Run App - Layer 1)
```
1. Open: https://adaptive-music-concept-generator-649888100218.us-west1.run.app
2. Adjust 6-Group Framework sliders
3. Click "Generate Stem Package"
4. Download: msv.json, lyria_prompt.txt, stem_profile.json
```

### Step 2: Generate (Lyria API)
```
5. Use lyria_prompt.txt with Lyria API
6. Generate each stem individually (pad, piano, rhythm, etc.)
7. Download raw WAV files
```

### Step 3: Process (These Scripts - Layer 2)
```
8. Run: convert_to_opus.ps1
   - Converts WAV → Opus @ 48kHz
9. Run: validate_stems.ps1
   - Checks duration, format, loop points
10. Fix any issues and re-validate
```

### Step 4: Integrate (Flutter App - Layer 3)
```
11. Update: app/assets/music/stems/library.json
    - Add stem_profile.json contents
12. Copy stems to: app/assets/music/stems/{stem_id}/
13. Test: flutter run
    - Verify music loads and plays
    - Check crossfading works
    - Validate game state integration
```

---

## Performance Targets

| Metric | Target | Script Verification |
|--------|--------|---------------------|
| **Stem Size** | <2MB per stem | validate_stems.ps1 |
| **Duration Accuracy** | ±0.1s | validate_stems.ps1 |
| **Format** | Opus @ 48kHz | validate_stems.ps1 |
| **Loop Safety** | Bar-aligned | validate_stems.ps1 |
| **Conversion Speed** | <10s per stem | convert_to_opus.ps1 |

---

## Troubleshooting

### FFmpeg Not Found
```powershell
# Install on Windows
choco install ffmpeg

# Or download from
# https://ffmpeg.org/download.html
```

### Stems Wrong Duration
```
1. Check source file duration in DAW
2. Re-export with exact bar length
3. Use Audacity to trim/pad if needed
4. Re-run convert_to_opus.ps1
```

### Validation Failures
```
- Duration mismatch: Re-generate with correct tempo/bars
- Wrong codec: Ensure convert_to_opus.ps1 ran successfully
- Wrong sample rate: Check FFmpeg output, may need to specify -ar 48000
- File size issues: Check source quality, may have silence or excessive reverb
```

---

## Next Steps

1. **Generate Priority Tier 1 stems** (30 packages)
   - Use Cloud Run app for MSV + Lyria prompts
   - Generate with Lyria (when available) or DAW
   - Process with these scripts

2. **Automate pipeline**
   - Create batch script to process multiple cues
   - Add CI/CD integration for validation
   - Automate library.json updates

3. **Expand library**
   - Tier 2: Additional emotional states
   - Tier 3: Seasonal variations
   - Tier 4: Special moments/transitions

---

## References

- **Master Documentation**: `../00-MUSIC-SYSTEM-MASTER.md`
- **Generation Workflow**: `../05-generation-workflow.md`
- **Lyria Guide**: `../03-lyria-generation-guide.md`
- **Flutter Implementation**: `../04-flutter-implementation.md`

---

*Layer 2 Generation Pipeline Tools - Version 1.0*


