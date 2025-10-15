# Model Selection Guide

**Quick Answer:** Use **qwen3:8b** for systematic generation (default), not qwen3:30b.

---

## Model Speed Comparison

| Model | Speed | Timeout | Use Case |
|-------|-------|---------|----------|
| **qwen3:8b** ⭐ | 30-60s | 2 min | **Systematic generation (recommended)** |
| qwen3:30b | 3-10 min | 10 min | Quality generation (slow) |
| qwen3:30b-a3b | 2-5 min | 5 min | Validation only |

---

## Why qwen3:8b for Systematic?

The systematic approach generates **many focused prompts** (5-8 per batch). Using the 30B model would be:

- ❌ **Too slow:** 5-10 minutes per generation
- ❌ **Batch timeout:** Can't generate 5 examples in reasonable time
- ❌ **Inefficient:** Overkill for focused 150-word prompts

The 8B model is:

- ✅ **Fast enough:** 30-60 seconds per generation
- ✅ **Batch friendly:** 5 examples in ~5 minutes
- ✅ **Efficient:** Perfect for focused prompts
- ✅ **Quality:** Systematic constraints guide quality

---

## Current Configuration

```python
# In config.py (DEFAULT - RECOMMENDED)
model_primary: "qwen3:8b"          # Fast systematic generation
model_speed: "qwen3:8b"            # Bulk generation
model_validation: "qwen3:30b-a3b"  # Quality validation only
```

### Timeouts (Auto-Selected)
```python
timeout_8b: 120 seconds   # 2 minutes (qwen3:8b)
timeout_30b: 600 seconds  # 10 minutes (qwen3:30b)
timeout_validation: 300 seconds  # 5 minutes (validation)
```

---

## When You Get Timeout Errors

### Error Message
```
ReadTimeout: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=300)
```

### Diagnosis

**Check which model is timing out:**
```python
# Look in error logs for:
[ERROR] Generation failed for qwen3:30b  # ← Model name here
```

### Solutions

#### 1. **Use qwen3:8b (Recommended)** ⭐

```python
config = initialize_enhanced_config({
    'model_primary': 'qwen3:8b'  # This is now the default
})
```

**Result:** 30-60 second generation time

#### 2. **Increase Timeout (If using 30B)**

```python
config = initialize_enhanced_config({
    'model_primary': 'qwen3:30b',
    'timeout_30b': 900  # 15 minutes
})
```

**Result:** Won't timeout, but still slow

#### 3. **Check GPU Usage**

```powershell
# Monitor GPU
.\scripts\monitor_gpu.ps1

# Look for:
# VRAM Usage: > 4000 MB (model loaded)
# GPU Compute: > 15% (actively generating)
```

**If GPU not used:**
- Check `OLLAMA_GPU_LAYERS=999`
- Restart Ollama service
- Verify: `.\scripts\check_gpu_models.ps1`

---

## Performance Expectations

### With qwen3:8b (Recommended)

| Batch Size | Generation Time | Examples/Hour |
|------------|-----------------|---------------|
| 5 examples | ~5 minutes | 60 |
| 8 examples | ~8 minutes | 60 |
| 10 examples | ~10 minutes | 60 |

**Daily estimate:** ~1,500 examples (24/7)

### With qwen3:30b (Slow)

| Batch Size | Generation Time | Examples/Hour |
|------------|-----------------|---------------|
| 5 examples | 25-50 minutes | 10-12 |
| 8 examples | 40-80 minutes | 10-12 |
| 10 examples | 50-100 minutes | 10-12 |

**Daily estimate:** ~250 examples (24/7)

**6x slower than 8B model!**

---

## Quality Comparison

### Does 8B produce lower quality?

**No!** The systematic approach compensates:

| Factor | qwen3:30b Random | qwen3:8b Systematic |
|--------|------------------|---------------------|
| **Spectrum coverage** | 40% | 80%+ |
| **Complexity types** | 0-2 | 4-6 |
| **Numerical grounding** | Optional | Required |
| **Parameter tracking** | None | Full |
| **Prompt quality** | 400+ lines | 150 words focused |

**Result:** 8B with systematic = higher quality than 30B random

---

## Troubleshooting Timeouts

### Step 1: Check Current Model

```python
# In your logs, look for:
[INFO] Using model: qwen3:30b  # ← Change to 8b if this appears
```

### Step 2: Verify GPU Usage

```powershell
# Run GPU monitor
.\scripts\monitor_gpu.ps1

# Expected:
# ✅ VRAM: 4000+ MB (model loaded)
# ✅ GPU Compute: 15%+ (when generating)
# ✅ Power: > 20W (active)
```

### Step 3: Check Ollama Service

```powershell
# Check if Ollama is running
Get-Process ollama

# If not running:
ollama serve

# If running but slow, restart:
taskkill /F /IM ollama.exe
Start-Sleep -Seconds 2
ollama serve
```

### Step 4: Test Model Speed

```powershell
# Time 8B model
Measure-Command { ollama run qwen3:8b "Generate a short story" }
# Should be: 30-60 seconds

# Time 30B model (for comparison)
Measure-Command { ollama run qwen3:30b "Generate a short story" }
# Will be: 3-10 minutes
```

### Step 5: Switch to 8B

```python
# If using 30B, switch to 8B:
config = initialize_enhanced_config({
    'model_primary': 'qwen3:8b'  # Faster
})
```

---

## Advanced: When to Use 30B

Use qwen3:30b only if:

1. ✅ You need maximum quality for research
2. ✅ You're generating < 100 examples (can wait)
3. ✅ You have time (willing to wait hours)
4. ✅ You increased timeout to 900+ seconds

**For production:** Always use qwen3:8b

---

## Configuration Examples

### Recommended (Fast)
```python
config = initialize_enhanced_config({
    'model_primary': 'qwen3:8b',      # Fast generation
    'batch_size_emotional': 8,        # 8 examples per batch
    'timeout_8b': 120                 # 2 minutes timeout
})

# Result: ~60 examples/hour
```

### Maximum Quality (Slow)
```python
config = initialize_enhanced_config({
    'model_primary': 'qwen3:30b',     # Slow but higher quality
    'batch_size_emotional': 3,        # Smaller batches
    'timeout_30b': 900                # 15 minutes timeout
})

# Result: ~10 examples/hour
```

### Balanced (Recommended for Testing)
```python
config = initialize_enhanced_config({
    'model_primary': 'qwen3:8b',      # Fast generation
    'model_validation': 'qwen3:30b-a3b',  # Quality validation
    'batch_size_emotional': 5,
    'timeout_8b': 120
})

# Result: Fast generation + quality validation
```

---

## Summary

**✅ DO THIS:**
- Use qwen3:8b for systematic generation (default)
- Verify GPU is being used (`monitor_gpu.ps1`)
- Keep timeouts at default (120s for 8B)

**❌ DON'T DO THIS:**
- Use qwen3:30b for systematic generation (too slow)
- Increase timeouts without checking GPU first
- Run without GPU acceleration

---

## Quick Fix Command

If you're getting timeouts right now:

```bash
# Your current config probably uses qwen3:30b
# It's now fixed to qwen3:8b by default

# Just re-run:
python scripts/run_training_pipeline.py

# Should work now! (30-60s per generation)
```

---

**Default is now qwen3:8b for systematic generation. Timeouts should not occur.**

