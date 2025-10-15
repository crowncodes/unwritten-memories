# Lyria Generation Scripts

Three scripts for generating music stems, from simplest to most complete.

---

## 📝 Scripts Overview

### 1. **simple_lyria_example.py** - START HERE
**Simplest possible example** - Just 60 lines of code

```bash
python simple_lyria_example.py
```

**What it does:**
- Generates a single pad stem for `calm_positive` cue
- Shows basic API call structure
- Perfect for understanding the basics

**Use when:**
- Learning how the API works
- Testing API connectivity
- Creating single stems manually

---

### 2. **generate_lyria_stems.py** - FULL FEATURED
**Production-ready script** - Complete workflow automation

```bash
# Generate one cue
python generate_lyria_stems.py --cue calm_positive

# Generate all cues
python generate_lyria_stems.py --cue all

# JSON only (no audio)
python generate_lyria_stems.py --cue all --json-only
```

**What it does:**
- Generates complete cues with all stems
- Creates proper directory structure
- Generates cue bank JSON entries
- Calculates loop points automatically
- Supports mock mode for testing

**Use when:**
- Generating production music assets
- Batch processing multiple cues
- Creating complete cue bank JSON

---

### 3. **LYRIA_GENERATION_GUIDE.md** - DOCUMENTATION
**Complete reference guide**

**What it covers:**
- Installation instructions
- All command-line options
- Available cues and their MSV parameters
- Troubleshooting common issues
- Post-generation workflow
- Manual generation alternatives

**Use when:**
- First-time setup
- Need detailed explanations
- Troubleshooting problems
- Understanding MSV parameters

---

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements_lyria.txt
```

### Step 2: Set API Key
```bash
# Windows PowerShell
$env:GOOGLE_API_KEY="your-key-here"

# Linux/Mac
export GOOGLE_API_KEY="your-key-here"
```

### Step 3: Test with Simple Example
```bash
python simple_lyria_example.py
```

### Step 4: Generate Production Assets
```bash
python generate_lyria_stems.py --cue all
```

---

## 📊 Feature Comparison

| Feature | simple_example | generate_stems | Guide |
|---------|---------------|----------------|-------|
| Lines of code | ~60 | ~400 | N/A |
| Single stem | ✅ | ✅ | 📖 |
| Multiple stems | ❌ | ✅ | 📖 |
| Multiple cues | ❌ | ✅ | 📖 |
| JSON generation | ❌ | ✅ | 📖 |
| Directory structure | ❌ | ✅ | 📖 |
| Loop calculation | ❌ | ✅ | 📖 |
| Mock mode | ✅ | ✅ | 📖 |
| Command-line args | ❌ | ✅ | 📖 |
| Error handling | Basic | Complete | 📖 |
| Documentation | Comments | Docstrings | Complete |

---

## 🎯 Recommended Workflow

### For Learning:
1. Read `LYRIA_GENERATION_GUIDE.md` (sections 1-3)
2. Run `simple_lyria_example.py`
3. Understand the output
4. Modify the prompt and re-run

### For Production:
1. Read `LYRIA_GENERATION_GUIDE.md` (full document)
2. Run `generate_lyria_stems.py --json-only` (test structure)
3. Review generated JSON
4. Run `generate_lyria_stems.py --cue calm_positive` (test single cue)
5. Verify audio quality
6. Run `generate_lyria_stems.py --cue all` (generate everything)

---

## 🔧 Customization

### Modify Simple Example
Edit `simple_lyria_example.py`:
```python
# Change the prompt
prompt = "YOUR CUSTOM MUSIC DESCRIPTION HERE"

# Change output location
output_file = "path/to/output.opus"
```

### Add New Cue to Full Script
Edit `CUE_DEFINITIONS` in `generate_lyria_stems.py`:
```python
"your_cue_name": {
    "tempo": 80,
    "key": "G",
    "mode": "Ionian",
    "bars": 8,
    "stems": ["pad", "piano"],
    "prompt": "Your detailed music description...",
    "msv": { ... }
}
```

---

## 🐛 Common Issues

### "google-generativeai not installed"
```bash
pip install google-generativeai
```

### "No API key found"
```bash
# Set environment variable
export GOOGLE_API_KEY="your-key-here"

# Or create .env file
echo "GOOGLE_API_KEY=your-key-here" > .env
```

### "Module not found"
```bash
# Install all requirements
pip install -r requirements_lyria.txt
```

---

## 📁 Files in This Directory

```
scripts/
├── simple_lyria_example.py        # ⭐ Simplest example (start here)
├── generate_lyria_stems.py        # 🚀 Full-featured generator
├── requirements_lyria.txt         # 📦 Python dependencies
├── LYRIA_GENERATION_GUIDE.md      # 📖 Complete documentation
└── README_SCRIPTS.md              # 📝 This file
```

---

## 💡 Tips

1. **Always test in mock mode first** - Verify structure before API calls
2. **Start with one cue** - Test the workflow with `calm_positive`
3. **Verify loop points** - Check audio seamlessly loops
4. **Read the guide** - `LYRIA_GENERATION_GUIDE.md` has detailed troubleshooting

---

## 🔗 Related Files

- **Implementation**: `../app/MUSIC_SYSTEM_IMPLEMENTATION.md`
- **Gem Prompt**: `../LYRIA_STEM_GENERATOR_GEM_PROMPT.md`
- **Music Engine**: `../app/lib/features/music/`
- **Cue Banks**: `../app/assets/music/cue_banks/`

---

## ❓ Which Script Should I Use?

**Use `simple_lyria_example.py` if:**
- You're new to the system
- Want to understand API structure
- Need to generate one stem
- Testing API connectivity

**Use `generate_lyria_stems.py` if:**
- Generating production assets
- Need complete cue bank JSON
- Want automated workflow
- Processing multiple cues

**Read `LYRIA_GENERATION_GUIDE.md` if:**
- First time setup
- Need detailed explanations
- Encountering errors
- Want to understand MSV system

---

**Happy generating! 🎵**

