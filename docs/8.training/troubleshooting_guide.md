# Troubleshooting & Optimization Guide
## For Qwen3 Training Data Generation

---

## 🔧 Common Issues & Solutions

### Issue 1: "Cannot connect to Ollama service"

**Symptoms**:
```
❌ Cannot connect to Ollama service
Failed to connect: Connection refused
```

**Causes**:
1. Ollama service not running
2. Wrong port (default is 11434)
3. Firewall blocking connection

**Solutions**:

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve

# Or on Windows PowerShell
Start-Process ollama -ArgumentList "serve"

# Verify models are installed
ollama list

# Should see:
# qwen3:30b-a3b
# qwen3:8b
# qwen3:32b
```

**If models missing**:
```bash
# Download models (this will take time)
ollama pull qwen3:30b-a3b  # ~17GB, primary model
ollama pull qwen3:8b        # ~4.7GB, speed model
ollama pull qwen3:32b       # ~18GB, validation model
```

---

### Issue 2: "Empty response from model"

**Symptoms**:
```python
AppLogger.warning("Empty response from qwen3:30b-a3b")
# Response has 0 length
```

**Causes**:
1. Model not fully loaded
2. Prompt too long for context window
3. Timeout too short
4. Model crashed/restarted

**Solutions**:

**Check 1 - Model Loading**:
```bash
# Manually load model to check for errors
ollama run qwen3:30b-a3b "test"

# Should respond with something
# If it hangs or errors, model file may be corrupted
```

**Check 2 - Context Window**:
```python
# In config.py, reduce max_tokens if hitting limits
max_tokens: int = 4000  # Reduce from 6000
```

**Check 3 - Timeout**:
```python
# In config.py, increase timeout for slow generations
request_timeout: int = 240  # Increase from 180
```

**Check 4 - Model Reload**:
```bash
# Stop Ollama
pkill ollama  # or Ctrl+C if running in terminal

# Clear model cache
rm -rf ~/.ollama/models/manifests/

# Restart and re-pull
ollama serve
ollama pull qwen3:30b-a3b
```

---

### Issue 3: "JSON parsing failed"

**Symptoms**:
```python
JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Causes**:
1. Model outputting text before/after JSON
2. Markdown code blocks (`\`\`\`json`)
3. Truncated response
4. Invalid JSON syntax

**Solutions**:

**Already Handled** in `_parse_json_response()`:
```python
# Strips markdown automatically
if cleaned.startswith('```'):
    lines = cleaned.split('\n')
    cleaned = '\n'.join(lines[1:])
    if cleaned.rstrip().endswith('```'):
        cleaned = cleaned.rstrip()[:-3]
```

**If still failing**:
1. Check response preview in logs
2. Reduce temperature (less creative = more valid JSON)
3. Add more "ONLY JSON" emphasis to prompt
4. Increase max_tokens (response may be truncated)

**Debug Script**:
```python
# Save raw responses to see what's failing
def debug_json_parsing(response_text, data_type):
    print(f"\n=== RAW RESPONSE ({data_type}) ===")
    print(response_text[:500])
    print("=== END RAW ===\n")
    
    try:
        # Try parsing
        data = json.loads(response_text)
        print(f"✅ Valid JSON: {len(data)} items")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        # Show problematic area
        start = max(0, e.pos - 50)
        end = min(len(response_text), e.pos + 50)
        print(f"Near error: {response_text[start:end]}")
```

---

### Issue 4: "Generation too slow"

**Symptoms**:
- Taking 60+ seconds per batch
- System feels laggy
- GPU utilization low

**Causes**:
1. Not using GPU (CPU mode)
2. Other processes using VRAM
3. Batch size too large
4. Model not optimized

**Check GPU Usage**:
```bash
# NVIDIA GPU
nvidia-smi

# Should show ollama process using ~10GB VRAM
# If not, Ollama may be in CPU mode
```

**Optimize Performance**:

**1. Verify GPU Mode**:
```bash
# Check Ollama GPU support
ollama run qwen3:30b-a3b "test" --verbose

# Should show GPU layers loaded
# If not, reinstall Ollama with CUDA support
```

**2. Reduce Batch Sizes**:
```python
# In config.py
batch_size_emotional: int = 8   # Reduce from 12
batch_size_dramatic: int = 6    # Reduce from 8
```

**3. Use Speed Model**:
```python
# For testing, use faster model
model_primary: str = "qwen3:8b"  # Instead of 30b-a3b
```

**4. Adjust Concurrent Requests**:
```python
# In generator, add delay between requests
time.sleep(2)  # Increase from 1 second
```

---

### Issue 5: "Quality scores too low"

**Symptoms**:
- authenticity_score < 0.7
- tension_score < 0.6
- Most samples failing validation

**Causes**:
1. Prompts not specific enough
2. Temperature too high/low
3. Model not understanding requirements
4. Batch size causing quality degradation

**Solutions**:

**1. Adjust Temperature**:
```python
# For better quality (less random)
temp_emotional: float = 0.75   # Reduce from 0.82
temp_dramatic: float = 0.78    # Reduce from 0.85

# For more variety (if too repetitive)
temp_emotional: float = 0.88   # Increase from 0.82
```

**2. Reduce Batch Size**:
```python
# Smaller batches = better quality per sample
batch_size_emotional: int = 6   # Reduce from 12
batch_size_dramatic: int = 4    # Reduce from 8
```

**3. Add More Examples**:
- Increase high-quality examples in prompts from 4 to 6-8
- Make examples more detailed
- Show exact calculation of scores

**4. Retry Failed Batches**:
```python
def generate_with_quality_filter(generator, batch_func, min_score=0.7):
    """Only keep samples meeting quality threshold"""
    attempts = 0
    good_samples = []
    
    while len(good_samples) < 12 and attempts < 5:
        batch = batch_func()
        for sample in batch:
            score = sample.get('authenticity_score', 0)
            if score >= min_score:
                good_samples.append(sample)
        attempts += 1
    
    return good_samples[:12]
```

---

### Issue 6: "Out of memory" / VRAM errors

**Symptoms**:
```
CUDA out of memory
RuntimeError: CUDA error
```

**Causes**:
1. Model too large for GPU (30B needs ~12GB)
2. Multiple models loaded simultaneously
3. Other applications using VRAM

**Solutions**:

**1. Check VRAM**:
```bash
nvidia-smi

# If VRAM full, close other applications:
# - Games
# - Chrome/browsers (can use 2-4GB)
# - Other AI tools
# - Video rendering software
```

**2. Use Smaller Model**:
```python
# For RTX 4070 SUPER (12GB), 30B is at limit
# If OOM, use 8B model instead
model_primary: str = "qwen3:8b"  # ~4.7GB vs ~17GB
```

**3. Reduce Context**:
```python
# Reduce max_tokens to use less memory
max_tokens: int = 3000  # Reduce from 6000
```

**4. Sequential Loading**:
```python
# Don't load multiple models at once
# Process one data type fully before starting next
```

---

## 🚀 Performance Optimization

### Hardware: RTX 4070 SUPER (12GB VRAM)

**Optimal Settings**:
```python
# config.py optimizations
class TrainingConfig:
    # Model selection
    model_primary: str = "qwen3:30b-a3b"     # Fits in 12GB
    model_speed: str = "qwen3:8b"            # For high volume
    model_validation: str = "qwen3:32b"      # Might need to run separately
    
    # Batch sizes (tuned for 12GB)
    batch_size_emotional: int = 10           # Sweet spot
    batch_size_dramatic: int = 8             # Complex reasoning
    batch_size_tension: int = 10             # Balanced
    batch_size_memory: int = 12              # Can be larger
    batch_size_personality: int = 25         # High volume with 8B
    batch_size_relationship: int = 20        # Moderate
    
    # Temperatures (quality focus)
    temp_emotional: float = 0.80             # Controlled creativity
    temp_dramatic: float = 0.82              # Slight variety
    temp_tension: float = 0.85               # More creative
    temp_memory: float = 0.78                # Emotional coherence
    temp_personality: float = 0.92           # Maximum diversity
    temp_relationship: float = 0.83          # Varied
    temp_validation: float = 0.25            # Strict
    
    # Timing
    request_timeout: int = 150               # Not too long
```

**Expected Performance**:
- Emotional Authenticity: ~4-6 samples/min (Qwen3-30B)
- Dramatic Irony: ~3-5 samples/min (Qwen3-30B)
- Tension Building: ~4-6 samples/min (Qwen3-30B)
- Memory Resonance: ~5-7 samples/min (Qwen3-30B)
- Personality Traits: ~15-20 samples/min (Qwen3-8B)
- Relationship Scoring: ~12-15 samples/min (Qwen3-8B)

**Daily Output** (24h continuous):
- ~9,200 samples total
- Mix of high-quality (30B) and high-volume (8B)

---

### System Requirements Check

```bash
#!/bin/bash
# system_check.sh

echo "=== System Requirements Check ==="

# GPU
echo "GPU:"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
# Need: 12GB+ VRAM

# RAM
echo "RAM:"
free -h | grep "Mem:"
# Need: 32GB+ total (64GB+ recommended)

# Disk Space
echo "Disk Space:"
df -h | grep -E '/$|/home'
# Need: 100GB+ free for models and output

# Ollama
echo "Ollama:"
which ollama
ollama --version
# Need: v0.1.0+

# Python
echo "Python:"
python3 --version
# Need: 3.8+

echo "=== Check Complete ==="
```

---

## 📊 Monitoring & Metrics

### Real-Time Monitoring Script

```python
import time
import psutil
import json
from pathlib import Path

def monitor_generation(output_dir, interval=60):
    """Monitor generation progress in real-time"""
    
    output_path = Path(output_dir)
    start_time = time.time()
    last_count = 0
    
    print("📊 Monitoring generation...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Count files
            files = list(output_path.glob("*.json"))
            total_samples = 0
            
            for file in files:
                try:
                    with open(file) as f:
                        data = json.load(f)
                        if 'samples' in data:
                            total_samples += len(data['samples'])
                        elif isinstance(data, list):
                            total_samples += len(data)
                except:
                    pass
            
            # Calculate rates
            elapsed = time.time() - start_time
            elapsed_hours = elapsed / 3600
            samples_per_hour = total_samples / elapsed_hours if elapsed_hours > 0 else 0
            
            new_samples = total_samples - last_count
            last_count = total_samples
            
            # System stats
            cpu_percent = psutil.cpu_percent()
            ram_percent = psutil.virtual_memory().percent
            
            # Display
            print(f"\r⏱️  {elapsed/60:.1f}m | "
                  f"📝 {total_samples:,} samples | "
                  f"⚡ {samples_per_hour:.0f}/hr | "
                  f"🆕 +{new_samples} | "
                  f"💻 CPU {cpu_percent:.0f}% | "
                  f"🧠 RAM {ram_percent:.0f}%", 
                  end='', flush=True)
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped")
        print(f"Final: {total_samples:,} samples in {elapsed/3600:.1f} hours")

# Usage
monitor_generation("training_output_v1.2", interval=30)
```

---

## 🔍 Quality Assurance Workflow

### 1. Pre-Generation Check
```bash
# Verify everything is ready
python scripts/run_training_pipeline.py --check-only

# Should verify:
# ✅ Ollama running
# ✅ Models downloaded
# ✅ GPU detected
# ✅ Disk space available
# ✅ Config validated
```

### 2. Test Batch
```bash
# Generate small test batch first
python scripts/run_training_pipeline.py --test

# Generates 1 batch of each type
# Manual review before full run
```

### 3. Full Production
```bash
# Start full generation
python scripts/run_training_pipeline.py

# Monitor in separate terminal
python scripts/monitor_generation.py
```

### 4. Post-Generation Validation
```python
# validate_output.py
from pathlib import Path
import json

def validate_output_directory(output_dir):
    """Validate all generated files"""
    
    output_path = Path(output_dir)
    files = list(output_path.glob("*.json"))
    
    stats = {
        'total_files': len(files),
        'total_samples': 0,
        'by_type': {},
        'quality_summary': {
            'excellent': 0,
            'good': 0,
            'poor': 0
        }
    }
    
    for file in files:
        with open(file) as f:
            data = json.load(f)
            
        data_type = data.get('data_type', 'unknown')
        samples = data.get('samples', [])
        
        if data_type not in stats['by_type']:
            stats['by_type'][data_type] = 0
        
        stats['by_type'][data_type] += len(samples)
        stats['total_samples'] += len(samples)
        
        # Check quality
        for sample in samples:
            score = sample.get('authenticity_score', 
                             sample.get('tension_score',
                             sample.get('dramatic_irony_score', 0.5)))
            
            if score >= 0.9:
                stats['quality_summary']['excellent'] += 1
            elif score >= 0.7:
                stats['quality_summary']['good'] += 1
            else:
                stats['quality_summary']['poor'] += 1
    
    # Print report
    print("\n" + "="*60)
    print("OUTPUT VALIDATION REPORT")
    print("="*60)
    print(f"\n📁 Files: {stats['total_files']}")
    print(f"📝 Total Samples: {stats['total_samples']:,}")
    
    print("\n📊 By Type:")
    for dtype, count in stats['by_type'].items():
        print(f"  {dtype}: {count:,}")
    
    print("\n⭐ Quality:")
    total = sum(stats['quality_summary'].values())
    for level, count in stats['quality_summary'].items():
        pct = (count/total*100) if total > 0 else 0
        print(f"  {level}: {count:,} ({pct:.1f}%)")
    
    # Pass/fail
    poor_pct = (stats['quality_summary']['poor']/total*100) if total > 0 else 0
    if poor_pct < 20:
        print("\n✅ PASS: Quality threshold met (< 20% poor)")
    else:
        print(f"\n❌ FAIL: Too many poor samples ({poor_pct:.1f}%)")
    
    return stats

# Usage
validate_output_directory("training_output_v1.2")
```

---

## 🎯 Best Practices

### DO:
✅ Test with small batches first  
✅ Monitor GPU/RAM usage  
✅ Validate samples manually (first few batches)  
✅ Use appropriate model for task (30B for quality, 8B for volume)  
✅ Set realistic daily targets based on hardware  
✅ Save incremental batches (don't lose work if interrupted)  
✅ Keep Ollama service running continuously  
✅ Check quality scores regularly  

### DON'T:
❌ Run on CPU (too slow)  
❌ Set batch sizes too large (degrades quality)  
❌ Ignore quality warnings  
❌ Mix data from different Master Truths versions  
❌ Delete partial batches (they have value)  
❌ Run multiple generation scripts simultaneously  
❌ Ignore memory warnings  
❌ Skip validation step  

---

## 📞 Getting Help

### Debug Information to Collect

When reporting issues:

```bash
# System info
uname -a
nvidia-smi
free -h
df -h

# Ollama info
ollama --version
ollama list
curl http://localhost:11434/api/tags

# Python info
python3 --version
pip list | grep -E 'requests|tqdm'

# Recent logs
tail -n 50 training_generation_v1.2.log

# Sample error
# Copy full error message including stack trace
```

### Common Error Messages

**"Connection refused"** → Ollama not running  
**"Model not found"** → Model not downloaded  
**"Out of memory"** → GPU VRAM full  
**"JSON decode error"** → Model output invalid  
**"Timeout"** → Generation too slow, increase timeout  
**"Empty response"** → Model crashed or prompt too long  

---

**Version**: Master Truths v1.2  
**Hardware**: Optimized for RTX 4070 SUPER (12GB)  
**Updated**: October 14, 2025
