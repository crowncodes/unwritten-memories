# Unwritten Training Data Generation Setup

## Overview

This guide will help you set up the Qwen3-based training data generation pipeline for Unwritten. The pipeline generates 40,000+ high-quality character interaction samples optimized for your RTX 4070 SUPER.

## System Requirements

### Hardware (Your Setup)
- ✅ **GPU:** RTX 4070 SUPER (12GB VRAM)
- ✅ **RAM:** 128GB
- ✅ **Storage:** ~60GB for models + space for generated data
- ✅ **OS:** Windows 10/11

### Software Requirements
- Python 3.9+ (already installed)
- Ollama (local LLM runtime)
- Required Python packages (see requirements.txt)

## Quick Start (15-20 minutes)

### Step 1: Install Ollama (5 minutes)

1. **Download Ollama for Windows:**
   - Visit: https://ollama.ai/download
   - Download the Windows installer
   - Run the installer
   - Restart PowerShell/Terminal

2. **Verify installation:**
   ```powershell
   ollama --version
   ```

### Step 2: Run Setup Script (10-15 minutes)

Open PowerShell in your project directory and run:

```powershell
# Run the automated setup
.\scripts\setup_ollama.ps1
```

This script will:
- ✅ Verify Ollama installation
- ✅ Start Ollama service
- ✅ Configure environment variables
- ✅ Download required models (~60GB total)
- ✅ Test model generation
- ✅ Create output directories

**Note:** Model downloads may take 30-60 minutes depending on your internet speed.

### Step 3: Install Python Dependencies

```powershell
# Activate your Python environment
.\unwritten-env\Scripts\Activate.ps1

# Install project in development mode
pip install -e .
```

### Step 4: Start Training Data Generation

```powershell
# Run the training pipeline
python scripts\run_training_pipeline.py
```

Choose your run duration:
- **Test run (1 hour):** ~270 samples - verify everything works
- **Half day (12 hours):** ~3,250 samples - good first run
- **Full day (24 hours):** ~6,500 samples - production rate
- **Multi-day:** Run for 7 days to generate 45,000+ samples

## What Gets Generated

### Training Data Types

The pipeline generates 5 types of high-quality training data:

1. **Emotional Authenticity (1,500/day)**
   - Characters constrained by emotional capacity (1-10 scale)
   - Realistic human limitations
   - Core system data

2. **Dramatic Irony (1,200/day)**
   - Knowledge gap scenarios
   - "Yelling at screen" tension moments
   - 3 dialogue options per scenario

3. **Personality Traits (2,000/day)**
   - OCEAN trait predictions
   - Diverse character interactions
   - Foundation data

4. **Tension Building (800/day)**
   - Incomplete revelations
   - Contradictory behavior
   - Narrative mystery

5. **Relationship Scoring (1,000/day)**
   - Interaction quality scores
   - Relationship impact analysis

### Output Format

Generated files are saved to `training_output/`:

```
training_output/
├── emotional_authenticity_batch0001_20251014_143022.json
├── dramatic_irony_batch0001_20251014_143045.json
├── personality_traits_batch0001_20251014_143108.json
├── tension_building_batch0001_20251014_143131.json
└── relationship_scoring_batch0001_20251014_143154.json
```

Each file contains JSON arrays of training examples with complete metadata.

## Model Configuration

### Three-Model Strategy

| Model | Size | Speed | Use Case |
|-------|------|-------|----------|
| **Qwen3-30B-A3B** | ~18GB | 25-40 tok/s | Emotional authenticity, dramatic irony |
| **Qwen3-8B** | ~5GB | 35-50 tok/s | Personality traits, relationship scoring |
| **Qwen3-32B** | ~20GB | 12-20 tok/s | Quality validation (10% sample) |

All three models run simultaneously using your 128GB RAM for maximum throughput.

## Performance Expectations

### Daily Output (24/7 Operation)

- **Emotional Authenticity:** 1,500 samples
- **Dramatic Irony:** 1,200 scenarios (×3 options = 3,600 examples)
- **Personality Traits:** 2,000 samples
- **Tension Building:** 800 samples
- **Relationship Scoring:** 1,000 samples
- **TOTAL:** ~6,500 training examples/day

### Quality Targets

- Overall quality score: >0.85
- Authenticity: >0.90
- Consistency: >0.92
- Novel-quality writing
- Nuanced psychology

### Cost Analysis

**Local Generation (Qwen3):**
- Electricity: ~$3-5/day
- 7-day cost: **~$25-35**
- Output: 45,000+ samples

**Cloud Alternative (Claude 3.5 Sonnet):**
- API costs: **~$180**
- Same output

**Savings: $145-155 (5-7x cheaper)**

## Monitoring Progress

### View Logs

```powershell
# Real-time log viewing
Get-Content training_generation.log -Wait

# Or on Unix-like systems:
tail -f training_generation.log
```

### Log Output

```
ℹ️  [2025-10-14 14:30:22] INFO: Qwen3DataGenerator initialized - {'output_dir': 'C:\\Users\\TCROW\\Documents\\GitHub\\unwritten\\training_output', 'daily_target': 6500}
🤖 [2025-10-14 14:30:45] AI: Inference completed - {'duration_ms': 2847, 'samples': 15}
✅ [2025-10-14 14:30:45] SUCCESS: Saved emotional_authenticity batch - {'file': 'emotional_authenticity_batch0001_20251014_143045.json', 'samples': 15}
```

### Check Output Directory

```powershell
# List generated files
Get-ChildItem .\training_output\ | Format-Table Name, Length, LastWriteTime

# Count total samples
$files = Get-ChildItem .\training_output\*.json
$total = 0
foreach ($file in $files) {
    $data = Get-Content $file | ConvertFrom-Json
    $total += $data.Count
}
Write-Host "Total samples generated: $total"
```

## Troubleshooting

### Ollama Not Found

```
❌ Ollama not found
```

**Solution:**
1. Install from https://ollama.ai/download
2. Restart PowerShell
3. Verify with `ollama --version`

### Service Not Running

```
❌ Cannot connect to Ollama service
```

**Solution:**
```powershell
# Start Ollama service
ollama serve
```

Or ensure it's running as a background service.

### Model Download Failed

```
❌ Failed to download qwen3:30b-a3b
```

**Solution:**
1. Check internet connection
2. Ensure sufficient disk space (~60GB needed)
3. Retry download:
   ```powershell
   ollama pull qwen3:30b-a3b
   ```

### Generation Slow

```
⚠️  PERF: Qwen3 generation - {'duration_ms': 15000}
```

**Solution:**
1. Check GPU utilization: `nvidia-smi`
2. Ensure GPU layers enabled:
   ```powershell
   $env:OLLAMA_GPU_LAYERS = "999"
   ```
3. Reduce loaded models to 2 instead of 3
4. Close other GPU-intensive applications

### Low Quality Scores

```
⚠️  Quality score: 0.62 (below target 0.85)
```

**Solution:**
1. Review generated samples in output files
2. Adjust temperature settings in `src/unwritten/training/config.py`
3. Modify prompts in `qwen3_generator.py`
4. Increase batch validation rate

## Advanced Configuration

### Custom Output Directory

```powershell
# Set custom output directory
$env:TRAINING_OUTPUT_DIR = "D:\unwritten_training"
python scripts\run_training_pipeline.py
```

### Modify Generation Parameters

Edit `src/unwritten/training/config.py`:

```python
@dataclass
class TrainingConfig:
    # Adjust batch sizes
    batch_size_emotional: int = 15  # Default
    
    # Adjust temperatures for more/less variety
    temp_emotional: float = 0.88    # Default
    
    # Adjust daily targets
    target_emotional_authenticity: int = 1500  # Default
```

### Enable Debug Logging

```powershell
# Enable verbose logging
$env:UNWRITTEN_DEBUG = "true"
python scripts\run_training_pipeline.py
```

## Next Steps After Generation

### 1. Data Review (1-2 hours)

Review a sample of generated data:

```powershell
# Open a sample file
code .\training_output\emotional_authenticity_batch0001_*.json
```

Check for:
- ✅ Realistic character behavior
- ✅ Clear capacity constraints
- ✅ High authenticity scores (>0.85)
- ✅ Diverse scenarios

### 2. Combine Multi-Day Runs

After running for multiple days, combine datasets:

```python
# Example combining script
import json
from pathlib import Path

output_dir = Path("training_output")
combined = {
    'emotional_authenticity': [],
    'dramatic_irony': [],
    # ... etc
}

for file in output_dir.glob("*.json"):
    data_type = file.stem.split('_batch')[0]
    with open(file) as f:
        data = json.load(f)
        combined[data_type].extend(data)

# Save combined datasets
for data_type, samples in combined.items():
    with open(f"final_{data_type}_dataset.json", 'w') as f:
        json.dump(samples, f, indent=2)
    print(f"✅ {data_type}: {len(samples):,} samples")
```

### 3. Prepare for Model Training

1. **Split train/validation/test sets (80/10/10)**
2. **Remove duplicates** (similarity threshold 0.85)
3. **Balance dataset** proportions
4. **Format for your training framework** (PyTorch, TensorFlow, etc.)

### 4. Fine-tune Your Model

Use the generated data to fine-tune your chosen base model (e.g., Llama, Qwen, Mistral).

Recommended approach:
- **Method:** LoRA fine-tuning
- **Epochs:** 3-5
- **Learning rate:** 2e-4
- **Batch size:** 8
- **Evaluation:** Human review + automated metrics

## Support & Resources

### Documentation

- **Strategy Document:** `data/qwen3_strategy_doc.md`
- **Original Pipeline:** `data/qwen3_training_pipeline.py`
- **Project README:** `README.md`

### Estimated Timeline

- **Days 1-2:** Setup and testing (this guide)
- **Days 3-7:** First production run (30,000+ samples)
- **Days 8-10:** Targeted generation (10,000-15,000 more)
- **Days 11-12:** Quality review and deduplication
- **Days 13-14:** Dataset preparation and split

**Total: 2 weeks from setup to training-ready dataset**

---

## Ready to Start?

```powershell
# 1. Run setup (if not done already)
.\scripts\setup_ollama.ps1

# 2. Activate environment
.\unwritten-env\Scripts\Activate.ps1

# 3. Start generating!
python scripts\run_training_pipeline.py
```

🚀 **Let's generate some novel-quality training data!**

