# ⚡ Quick Start Guide - Windows

Get your training pipeline running in **15-20 minutes** (plus model download time).

## Prerequisites

- ✅ Windows 10/11
- ✅ RTX 4070 SUPER (12GB VRAM) or better
- ✅ 32GB+ RAM (128GB recommended)
- ✅ Python 3.9+
- ✅ ~60GB free disk space

---

## Step-by-Step Setup

### 1. Install Ollama (5 minutes)

**Download and install:**
1. Visit: https://ollama.ai/download
2. Click "Download for Windows"
3. Run `OllamaSetup.exe`
4. Follow installer prompts
5. **Restart PowerShell** after installation

**Verify installation:**
```powershell
ollama --version
```

Expected output: `ollama version 0.x.x`

---

### 2. Clone Repository (1 minute)

```powershell
# Navigate to your projects directory
cd Documents\GitHub

# Clone repository
git clone https://github.com/yourusername/unwritten.git
cd unwritten
```

---

### 3. Setup Python Environment (2 minutes)

```powershell
# Create virtual environment
python -m venv unwritten-env

# Activate it
.\unwritten-env\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -e .
```

---

### 4. Run Automated Setup (30-60 minutes)

This downloads the required models (~60GB). Get some coffee! ☕

```powershell
.\scripts\setup_ollama.ps1
```

**What it does:**
- ✅ Verifies Ollama is running
- ✅ Configures environment variables
- ✅ Downloads qwen3:30b-a3b (~18GB)
- ✅ Downloads qwen3:8b (~5GB)
- ✅ Downloads qwen3:32b (~20GB)
- ✅ Tests generation
- ✅ Creates output directories

**Optional:** When prompted, choose `y` to set environment variables permanently.

---

### 5. Quick Test (2 minutes)

Verify everything works:

```powershell
python scripts\quick_test.py
```

**Expected output:**
```
🚀 Unwritten Training Setup - Quick Test
============================================================
🔍 Testing Ollama connection...
✅ Ollama is running
   Available models: 3

📦 Checking required models...
   ✅ qwen3:30b-a3b
   ✅ qwen3:8b
   ✅ qwen3:32b

🧪 Testing data generation...
   Generating 2 emotional authenticity examples...
   ✅ Generated 2 samples

============================================================
📊 Test Summary
============================================================
   ✅ PASS - Ollama Connection
   ✅ PASS - Model Availability
   ✅ PASS - Data Generation
============================================================

🎉 All tests passed! Ready to generate training data.
```

---

### 6. Start Training Data Generation

```powershell
python scripts\run_training_pipeline.py
```

**Choose your duration:**

```
⏱️  Run duration options:
  1. Test run (1 hour) - ~270 samples
  2. Half day (12 hours) - ~3,250 samples
  3. Full day (24 hours) - ~6,500 samples
  4. Multi-day (specify hours)

Select option (1-4):
```

**For first time:** Choose option 1 (test run) to verify everything works.

---

## Monitoring Your Run

### Terminal 1: Generation Progress

```powershell
# Already running the pipeline
python scripts\run_training_pipeline.py
```

You'll see progress bars and real-time updates:
```
🎯 Starting data generation...

Generating batches: 45%|████████████░░░░░░| 23/51 [02:15<02:45, 5.9s/it]
```

### Terminal 2: Watch Logs

Open a new PowerShell window:

```powershell
cd Documents\GitHub\unwritten
Get-Content training_generation.log -Wait
```

### Terminal 3: Monitor GPU

```powershell
# Watch GPU utilization
nvidia-smi -l 1
```

---

## What Happens During Generation

### Files Created

Generated files appear in `training_output/`:

```
training_output/
├── emotional_authenticity_batch0001_20251014_143022.json
├── emotional_authenticity_batch0002_20251014_143145.json
├── dramatic_irony_batch0001_20251014_143308.json
├── personality_traits_batch0001_20251014_143431.json
├── tension_building_batch0001_20251014_143554.json
└── relationship_scoring_batch0001_20251014_143717.json
```

### Performance Indicators

**Good Performance (RTX 4070 SUPER):**
- Generation speed: 25-40 tokens/sec
- Batch time: 2-5 seconds
- GPU utilization: 85-95%
- Expected samples/hour: ~270

**If Slower:**
- Check GPU utilization: `nvidia-smi`
- Ensure OLLAMA_GPU_LAYERS=999
- Close other GPU applications

---

## After Generation Completes

### 1. Review Generated Data

```powershell
# Open a sample file
code training_output\emotional_authenticity_batch0001_*.json
```

**Check for:**
- ✅ Realistic character responses
- ✅ Clear capacity constraints
- ✅ Authentic internal thoughts
- ✅ Diverse scenarios

### 2. Count Total Samples

```powershell
$files = Get-ChildItem training_output\*.json
$total = 0
foreach ($file in $files) {
    $data = Get-Content $file | ConvertFrom-Json
    $total += $data.Count
}
Write-Host "Total samples generated: $total"
```

### 3. Start Longer Run

If test run succeeded:

```powershell
python scripts\run_training_pipeline.py
# Choose option 3 (24 hours)
```

---

## Troubleshooting

### ❌ "Ollama not found"

**Solution:**
1. Install from https://ollama.ai/download
2. Restart PowerShell
3. Verify: `ollama --version`

---

### ❌ "Cannot load scripts"

```
cannot be loaded because running scripts is disabled
```

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### ❌ "Cannot connect to Ollama service"

**Solution:**
```powershell
# Start Ollama service
ollama serve

# In another terminal, test:
ollama run qwen3:8b "Hello"
```

---

### ❌ "Model not found: qwen3:30b-a3b"

**Solution:**
```powershell
# Download missing model
ollama pull qwen3:30b-a3b
ollama pull qwen3:8b
ollama pull qwen3:32b
```

---

### ❌ Generation Very Slow

**Symptoms:** <15 tokens/sec, long batch times

**Solution:**
```powershell
# 1. Check GPU is being used
nvidia-smi

# 2. Set GPU layers
$env:OLLAMA_GPU_LAYERS = "999"

# 3. Restart Ollama
# Close Ollama window
ollama serve

# 4. Close other GPU apps (browsers, games, etc.)

# 5. Reduce batch sizes if needed
code src\unwritten\training\config.py
```

---

### ❌ Low Quality Scores

**Symptoms:** Validation reports quality <0.75

**Solution:**
1. Review generated samples
2. Adjust temperature in `config.py`
3. Modify prompts in `qwen3_generator.py`
4. Re-run with refined settings

---

## Next Steps

### ✅ After Test Run Success

1. **Run full 24-hour cycle:**
   ```powershell
   python scripts\run_training_pipeline.py
   # Choose option 3
   ```

2. **Monitor overnight**
3. **Check results in morning**
4. **Repeat for 7 days** to reach 45,000+ samples

### ✅ Using Generated Data

1. Review and validate samples
2. Combine datasets from multiple days
3. Remove duplicates
4. Split train/validation/test sets (80/10/10)
5. Use for model fine-tuning

---

## Performance Benchmarks

### Expected Speeds (RTX 4070 SUPER)

| Model | Tokens/Sec | Batch Time | Samples/Hour |
|-------|------------|------------|--------------|
| Qwen3-30B-A3B | 25-40 | 3-5s | 180-240 |
| Qwen3-8B | 35-50 | 2-3s | 400-600 |
| Mixed (actual) | 30-45 | 2-5s | ~270 |

### Daily Output

- **Test run (1h):** ~270 samples
- **Half day (12h):** ~3,250 samples
- **Full day (24h):** ~6,500 samples
- **Week (7 days):** ~45,000 samples

---

## Cost & Efficiency

### Your Setup (Local)

- **Hardware:** Already owned
- **Electricity:** ~$3-5/day (24/7 operation)
- **7 days:** ~$25-35 total
- **Output:** 45,000+ samples

### Alternative (Cloud API)

- **Service:** Claude 3.5 Sonnet
- **Cost:** ~$180 for 45,000 samples
- **Savings:** **5-7x cheaper locally**

---

## Tips for Success

### 🔥 Keep GPU Cool

- Ensure good case airflow
- Monitor temps: `nvidia-smi`
- Target: <80°C under load

### ⚡ Optimize for Speed

- Keep all 3 models loaded
- Set OLLAMA_KEEP_ALIVE=24h
- Don't interrupt during batches

### 📊 Quality Over Quantity

- Review samples regularly
- Adjust prompts as needed
- Maintain >0.85 quality scores

### 💾 Data Management

- Save generated files regularly
- Back up to external storage
- Track daily production metrics

---

## Workflow Example

### Morning Routine

```powershell
# 1. Activate environment
.\unwritten-env\Scripts\Activate.ps1

# 2. Check yesterday's results
Get-ChildItem training_output\ | Measure-Object

# 3. Start today's run
python scripts\run_training_pipeline.py
# Choose option 3 (24 hours)

# 4. Monitor for first few minutes
Get-Content training_generation.log -Wait

# 5. Let it run all day
```

### Evening Check

```powershell
# Review progress
Get-Content training_generation.log -Tail 50

# Check GPU
nvidia-smi

# View samples
code training_output\emotional_authenticity_batch0010_*.json
```

---

## Getting Help

### 📚 Documentation

- **Detailed setup:** `TRAINING_SETUP.md`
- **Full reference:** `SETUP_COMPLETE.md`
- **Scripts guide:** `scripts/README.md`

### 🔧 Common Issues

All covered in `TRAINING_SETUP.md` troubleshooting section.

### 💬 Support

Review logs in `training_generation.log` for error details.

---

## ✅ Quick Start Checklist

- [ ] Ollama installed and verified
- [ ] Repository cloned
- [ ] Python environment created and activated
- [ ] Dependencies installed (`pip install -e .`)
- [ ] Setup script run (`.\scripts\setup_ollama.ps1`)
- [ ] Models downloaded (qwen3:30b-a3b, 8b, 32b)
- [ ] Quick test passed (`python scripts\quick_test.py`)
- [ ] Test run successful (1 hour)
- [ ] Ready for production runs

---

**🚀 You're ready to generate 45,000+ training samples!**

**Start with:** `python scripts\run_training_pipeline.py`

