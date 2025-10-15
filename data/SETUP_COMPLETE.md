# ✅ Unwritten Training Pipeline - Setup Complete

## What Was Created

Your Qwen3 training data generation pipeline is now fully configured and ready to run!

### 📁 Project Structure

```
unwritten/
├── src/unwritten/training/
│   ├── __init__.py                    # Training module exports
│   ├── config.py                      # Configuration settings
│   └── qwen3_generator.py             # Main generation pipeline
│
├── src/unwritten/utils/
│   └── logger.py                      # Structured logging utility
│
├── scripts/
│   ├── setup_ollama.ps1               # Ollama setup script (Windows)
│   ├── run_training_pipeline.py       # Main runner script
│   ├── quick_test.py                  # Quick verification test
│   └── README.md                      # Scripts documentation
│
├── TRAINING_SETUP.md                  # Comprehensive setup guide
├── SETUP_COMPLETE.md                  # This file
├── .gitignore                         # Excludes training_output/
│
└── training_output/                   # Generated data (created on first run)
    └── [batch files will appear here]
```

### 🎯 What Each Component Does

#### Core Training Module (`src/unwritten/training/`)

**`qwen3_generator.py`** - Main generation pipeline with 5 data type generators:
- ✅ `generate_emotional_authenticity_batch()` - Core character behavior (1,500/day)
- ✅ `generate_dramatic_irony_batch()` - Knowledge gap scenarios (1,200/day)
- ✅ `generate_personality_trait_batch()` - OCEAN trait data (2,000/day)
- ✅ `generate_tension_building_batch()` - Narrative tension (800/day)
- ✅ `generate_relationship_scoring_batch()` - Interaction quality (1,000/day)
- ✅ `validate_with_qwen3_32b()` - Quality validation
- ✅ `run_production_cycle()` - 24/7 production runner

**`config.py`** - Configuration management:
- Model selection (30b-a3b, 8b, 32b)
- Batch sizes optimized for RTX 4070 SUPER
- Temperature settings per data type
- Daily production targets
- Quality thresholds

#### Utilities (`src/unwritten/utils/`)

**`logger.py`** - Structured logging:
- `AppLogger.info()` - General information
- `AppLogger.performance()` - Performance metrics
- `AppLogger.ai()` - AI/ML specific events
- `AppLogger.error()` - Error tracking
- `AppLogger.success()` - Success messages

#### Scripts (`scripts/`)

**`setup_ollama.ps1`** - One-time setup:
- Verifies Ollama installation
- Downloads required models (~60GB)
- Configures environment variables
- Tests generation

**`run_training_pipeline.py`** - Main runner:
- Verifies system readiness
- Runs production cycles
- Saves data incrementally
- Validates quality

**`quick_test.py`** - Quick verification:
- Tests Ollama connection
- Checks model availability
- Runs sample generation

### 📊 Expected Performance

#### Your Hardware Capabilities

| Component | Spec | Optimized For |
|-----------|------|---------------|
| GPU | RTX 4070 SUPER (12GB) | Runs Qwen3-30B-A3B + 8B |
| RAM | 128GB | Keeps all 3 models loaded |
| Storage | ~60GB for models | Plus growing training data |

#### Daily Output (24/7 Operation)

| Data Type | Daily Target | Model Used | Purpose |
|-----------|--------------|------------|---------|
| Emotional Authenticity | 1,500 samples | Qwen3-30B-A3B | Core realism |
| Dramatic Irony | 1,200 scenarios | Qwen3-30B-A3B | Tension moments |
| Personality Traits | 2,000 samples | Qwen3-8B | Foundation |
| Tension Building | 800 samples | Qwen3-30B-A3B | Narrative quality |
| Relationship Scoring | 1,000 samples | Qwen3-8B | Interactions |
| **TOTAL** | **~6,500 samples/day** | | |

#### 7-Day Campaign Output

- **Total samples:** ~45,000
- **Cost:** ~$25-35 (electricity only)
- **vs Cloud API:** $180 (5-7x savings)
- **Quality:** Claude Sonnet-level

---

## 🚀 Next Steps - Getting Started

### Step 1: Install Ollama (if not done yet)

```powershell
# Download from https://ollama.ai/download
# Run installer
# Restart PowerShell
```

Verify installation:
```powershell
ollama --version
```

### Step 2: Run Setup Script

```powershell
# From project root
.\scripts\setup_ollama.ps1
```

This will:
- ✅ Start Ollama service
- ✅ Download models (~60GB, 30-60 minutes)
- ✅ Configure environment
- ✅ Test generation

### Step 3: Activate Python Environment

```powershell
# Activate your virtual environment
.\unwritten-env\Scripts\Activate.ps1

# Install project (if not done)
pip install -e .
```

### Step 4: Run Quick Test

```powershell
# Verify everything works
python scripts\quick_test.py
```

Expected output:
```
✅ PASS - Ollama Connection
✅ PASS - Model Availability
✅ PASS - Data Generation
```

### Step 5: Start Training Data Generation

```powershell
# Run the pipeline
python scripts\run_training_pipeline.py
```

Choose your duration:
- **Option 1:** Test run (1 hour) - ~270 samples
- **Option 2:** Half day (12 hours) - ~3,250 samples
- **Option 3:** Full day (24 hours) - ~6,500 samples
- **Option 4:** Custom duration

### Step 6: Monitor Progress

In another PowerShell window:

```powershell
# Watch logs in real-time
Get-Content training_generation.log -Wait
```

Or check output directory:
```powershell
# See generated files
Get-ChildItem training_output\
```

---

## 📈 Usage Patterns

### Daily Production Run

```powershell
# Morning: Start 24-hour run
.\unwritten-env\Scripts\Activate.ps1
python scripts\run_training_pipeline.py
# Select option 3 (Full day)

# Next morning: Check results
Get-ChildItem training_output\ | Measure-Object
```

### Week-Long Campaign (45k samples)

```powershell
# Run for 7 consecutive days
# Each morning, start a new 24-hour cycle
# After 7 days: ~45,000 samples generated
```

### Test & Iterate

```powershell
# Quick test run
python scripts\run_training_pipeline.py
# Select option 1 (1 hour, ~270 samples)

# Review output
code training_output\emotional_authenticity_batch0001_*.json

# Adjust config if needed
code src\unwritten\training\config.py

# Run again with refined settings
```

---

## 🔧 Configuration Options

### Environment Variables

Set for optimal performance:

```powershell
# Keep models loaded for 24 hours
$env:OLLAMA_KEEP_ALIVE = "24h"

# Load all 3 models simultaneously
$env:OLLAMA_MAX_LOADED_MODELS = "3"

# Use all GPU layers
$env:OLLAMA_GPU_LAYERS = "999"

# Enable debug logging (optional)
$env:UNWRITTEN_DEBUG = "true"
```

### Custom Output Directory

```powershell
# Use a different output location
$env:TRAINING_OUTPUT_DIR = "D:\unwritten_training"
python scripts\run_training_pipeline.py
```

### Adjust Batch Sizes

Edit `src/unwritten/training/config.py`:

```python
@dataclass
class TrainingConfig:
    # Increase for faster generation (if GPU allows)
    batch_size_emotional: int = 20  # Default: 15
    
    # Decrease if running out of memory
    batch_size_personality: int = 15  # Default: 25
```

### Modify Temperature Settings

Edit `src/unwritten/training/config.py`:

```python
@dataclass
class TrainingConfig:
    # Higher temp = more variety
    temp_emotional: float = 0.92  # Default: 0.88
    
    # Lower temp = more consistency
    temp_dramatic: float = 0.75  # Default: 0.82
```

---

## 📚 Documentation

### Comprehensive Guides

- **`TRAINING_SETUP.md`** - Complete setup guide with troubleshooting
- **`scripts/README.md`** - Script documentation and workflows
- **`data/qwen3_strategy_doc.md`** - Strategy and methodology

### Quick Reference

**View configuration:**
```powershell
code src\unwritten\training\config.py
```

**Check logs:**
```powershell
Get-Content training_generation.log -Tail 50
```

**Count generated samples:**
```powershell
$files = Get-ChildItem training_output\*.json
$total = 0
foreach ($file in $files) {
    $data = Get-Content $file | ConvertFrom-Json
    $total += $data.Count
}
Write-Host "Total samples: $total"
```

---

## 🎯 Quality Targets

### Automated Validation

The pipeline automatically validates 10% of samples with Qwen3-32B:

```
Minimum Acceptable:
- Overall quality: >0.75
- Authenticity: >0.80
- Consistency: >0.85

Target Quality:
- Overall quality: >0.85
- Authenticity: >0.90
- Consistency: >0.92
```

### Manual Review

After generation, review samples:

```powershell
# Open a sample file
code training_output\emotional_authenticity_batch0001_20251014_143022.json
```

Check for:
- ✅ Realistic character behavior
- ✅ Clear capacity constraints
- ✅ Authentic internal thoughts
- ✅ Diverse scenarios

---

## 🔍 Monitoring & Debugging

### Real-Time Monitoring

```powershell
# Terminal 1: Run pipeline
python scripts\run_training_pipeline.py

# Terminal 2: Watch logs
Get-Content training_generation.log -Wait

# Terminal 3: Monitor GPU
nvidia-smi -l 1
```

### Check System Resources

```powershell
# GPU utilization
nvidia-smi

# Memory usage
Get-Process python | Format-Table ProcessName, @{L='Memory(MB)'; E={($_.WS / 1MB)}}

# Disk space
Get-PSDrive C
```

### Troubleshooting

**Issue: Generation slow**
```powershell
# Check if GPU is being used
nvidia-smi

# Ensure GPU layers enabled
$env:OLLAMA_GPU_LAYERS = "999"
```

**Issue: Out of memory**
```powershell
# Reduce batch sizes in config.py
# Or run fewer models simultaneously
```

**Issue: Low quality scores**
```powershell
# Review generated samples
code training_output\emotional_authenticity_batch0001_*.json

# Adjust temperature or prompts
code src\unwritten\training\qwen3_generator.py
```

---

## 📦 Data Output Format

### File Structure

```
training_output/
├── emotional_authenticity_batch0001_20251014_143022.json
├── emotional_authenticity_batch0002_20251014_143145.json
├── dramatic_irony_batch0001_20251014_143308.json
├── personality_traits_batch0001_20251014_143431.json
├── tension_building_batch0001_20251014_143554.json
└── relationship_scoring_batch0001_20251014_143717.json
```

### Sample Output

**Emotional Authenticity:**
```json
[
  {
    "context": "exhausted from work crisis, emotional capacity 2.5/10",
    "situation": "friend needs to process breakup",
    "character_response": "I hear you, and I want to help...",
    "internal_thought": "I feel terrible. They need me...",
    "authenticity_score": 0.92,
    "capacity_demonstration": "Character recognizes limitation...",
    "ocean_context": {
      "conscientiousness": 0.7,
      "agreeableness": 0.8,
      "neuroticism": 0.4
    }
  }
]
```

---

## 🎉 You're All Set!

### Your training pipeline is ready to:

✅ Generate 6,500+ samples daily  
✅ Run 24/7 with automatic quality validation  
✅ Save data incrementally (no data loss)  
✅ Use Claude Sonnet-level quality at 5-7x lower cost  
✅ Produce 45,000+ samples in 7 days  

### Start generating with:

```powershell
python scripts\run_training_pipeline.py
```

### Questions or issues?

Check `TRAINING_SETUP.md` for comprehensive troubleshooting and FAQs.

**Happy training! 🚀**

