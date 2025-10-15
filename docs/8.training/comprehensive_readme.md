# Unwritten Training Data Generation Pipeline
## Master Truths Canonical Spec v1.2 Compliant

> **Novel-quality character interactions with emotional authenticity, dramatic irony, and sophisticated narrative tension**

---

## 🎯 What This Does

Generates high-quality training data for AI character interactions that feel like **literary fiction**, not generic game dialogue. The system creates:

1. **Emotional Authenticity** (CORE): Characters constrained by realistic emotional capacity (X+2 rule)
2. **Dramatic Irony**: "Yelling at screen" tension through knowledge gaps
3. **Tension Building**: Four types of narrative hooks (mystery, reveal, contradiction, stakes)
4. **Memory Resonance**: Emotionally-weighted memory recall (5 resonance types)
5. **OCEAN Personality**: Foundation personality trait data
6. **Relationship Scoring**: Interaction quality tracking

### Why This Matters

**Before**: "I'll help you with anything!" (unrealistic, always-available NPCs)

**After**: "I want to help, but I'm completely wiped right now. Can we talk tomorrow when I'm more present? I care about you, I'm just running on empty." (authentic human limitation)

---

## 🚀 Quick Start

### Prerequisites

- **GPU**: NVIDIA RTX 4070 SUPER (12GB VRAM) or equivalent
- **RAM**: 32GB minimum (64GB+ recommended)
- **Disk**: 100GB+ free space
- **OS**: Linux, macOS, or Windows with WSL2
- **Python**: 3.8+
- **Ollama**: Latest version

### Installation

```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Download models (~40GB total)
ollama pull qwen3:30b-a3b  # Primary - emotional depth (~17GB)
ollama pull qwen3:8b        # Speed - high volume (~4.7GB)
ollama pull qwen3:32b       # Validation - quality (~18GB)

# 3. Start Ollama service
ollama serve

# 4. Install Python dependencies
pip install requests tqdm

# 5. Verify setup
python scripts/run_training_pipeline.py --check-only
```

### Generate Your First Batch

```bash
# Test run (1 hour, ~380 samples)
python scripts/run_training_pipeline.py

# Select option 1 when prompted
```

---

## 📊 What Gets Generated

### Daily Production Target: ~9,200 Samples

| Data Type | Samples/Day | Priority | Model | Quality Threshold |
|-----------|-------------|----------|-------|-------------------|
| **Emotional Authenticity** | 2,000 | 🎭 CORE | Qwen3-30B-A3B | ≥ 0.7 |
| **Dramatic Irony** | 1,500 | ⚡ HIGH | Qwen3-30B-A3B | ≥ 0.5 |
| **Tension Building** | 1,200 | ⚡ HIGH | Qwen3-30B-A3B | ≥ 0.6 |
| **Memory Resonance** | 1,000 | 🆕 NEW v1.2 | Qwen3-30B-A3B | ≥ 0.7 |
| **Personality Traits** | 2,500 | 📚 FOUNDATION | Qwen3-8B | ≥ 0.6 |
| **Relationship Scoring** | 1,000 | 📚 FOUNDATION | Qwen3-8B | ≥ 0.6 |

### Sample Output Structure

```json
{
  "master_truths_version": "v1.2",
  "data_type": "emotional_authenticity",
  "batch_number": 1,
  "timestamp": "20251014_143022",
  "sample_count": 12,
  "samples": [
    {
      "context": "Emergency at work, family crisis, no sleep",
      "base_capacity": 8.0,
      "capacity_factors": [
        {"factor": "work_crisis", "impact": -3.0},
        {"factor": "family_emergency", "impact": -3.0},
        {"factor": "sleep_deprivation", "impact": -2.0}
      ],
      "effective_capacity": 0.0,
      "situation": "Friend needs emotional support",
      "support_level_needed": 9.5,
      "character_response": "I—[voice breaks] I'm so sorry...",
      "authenticity_score": 0.95,
      "demonstrates_constraint": "Capacity 0.0 + 2 = 2.0 max..."
    }
  ]
}
```

---

## 🎮 Usage

### Option 1: Interactive Mode

```bash
python scripts/run_training_pipeline.py
```

Choose from:
- **Test Run** (1 hour): ~380 samples
- **Half Day** (12 hours): ~4,600 samples  
- **Full Day** (24 hours): ~9,200 samples
- **Custom**: Specify hours

### Option 2: Programmatic

```python
from unwritten.training.config import TrainingConfig
from unwritten.training.qwen3_generator import Qwen3DataGenerator

# Initialize
config = TrainingConfig()
config.target_emotional_authenticity = 2000
config.min_emotional_authenticity = 0.7

generator = Qwen3DataGenerator(config)

# Generate specific data type
batch = generator.generate_emotional_authenticity_batch(batch_size=10)

# Run full production
results = generator.run_production_cycle(duration_hours=24)
```

### Option 3: Continuous Production

```bash
# Run indefinitely (stop with Ctrl+C)
while true; do
  python scripts/run_training_pipeline.py --duration 24
  sleep 60
done
```

---

## 📈 Monitoring & Analysis

### Real-Time Monitoring

```bash
# In separate terminal while generation runs
python scripts/monitor_generation.py training_output_v1.2
```

Shows:
- ⏱️  Elapsed time
- 📝 Total samples generated
- ⚡ Samples per hour
- 🆕 New samples since last check
- 💻 CPU usage
- 🧠 RAM usage

### Post-Generation Analysis

```bash
# Analyze quality metrics
python scripts/analyze_training_data.py training_output_v1.2 --analyze

# Validate capacity constraints
python scripts/analyze_training_data.py training_output_v1.2 --validate-capacity

# Combine all batches
python scripts/analyze_training_data.py training_output_v1.2 --combine --min-quality 0.7

# Export by type
python scripts/analyze_training_data.py training_output_v1.2 --export-by-type --min-quality 0.7

# Generate train/val/test splits
python scripts/analyze_training_data.py training_output_v1.2 --generate-splits

# Do everything
python scripts/analyze_training_data.py training_output_v1.2 --all --min-quality 0.7
```

---

## ✅ Quality Assurance

### Automated Validation

Every sample is validated against **Master Truths v1.2** requirements:

| Check | Threshold | Purpose |
|-------|-----------|---------|
| Emotional Authenticity | ≥ 0.7 | Capacity constraints followed |
| Tension Building | ≥ 0.6 | Creates "one more week" desire |
| Dramatic Irony | ≥ 0.5 | Knowledge gaps effective |
| Hook Effectiveness | ≥ 0.6 | Player curiosity generated |
| Overall Novel-Quality | ≥ 0.7 | Literary fiction standard |

### Manual Review Checkpoints

**After First Batch** (5 samples):
```bash
# Generate test batch
python scripts/run_training_pipeline.py --test

# Manually review
cat training_output_v1.2/emotional_authenticity_batch0001_*.json | head -50
```

Check for:
- ✅ Capacity calculation shown (base → factors → effective)
- ✅ X+2 rule explained in demonstrates_constraint
- ✅ Authentic limitation in character_response
- ✅ Quality score ≥ 0.7

**After 1000 Samples**:
```bash
# Run full analysis
python scripts/analyze_training_data.py training_output_v1.2 --analyze --validate-capacity
```

Check for:
- ✅ Pass rate ≥ 80% for each data type
- ✅ Capacity violations < 5%
- ✅ Average quality scores meet thresholds

---

## 🔧 Configuration

### Adjusting Daily Targets

```python
# config.py
target_emotional_authenticity: int = 3000  # Increase from 2000
target_dramatic_irony: int = 2000          # Increase from 1500
```

### Tuning Quality Thresholds

```python
# config.py
min_emotional_authenticity: float = 0.8    # Stricter (from 0.7)
min_tension_building: float = 0.7          # Stricter (from 0.6)
```

### Optimizing Batch Sizes

**For your hardware** (RTX 4070 SUPER 12GB):
```python
# config.py
batch_size_emotional: int = 10    # Sweet spot for quality
batch_size_dramatic: int = 8      # Complex reasoning
batch_size_tension: int = 10      # Balanced
```

**If running out of VRAM**:
```python
batch_size_emotional: int = 6     # Reduce
batch_size_dramatic: int = 4      # Reduce
```

**If too slow**:
```python
model_primary: str = "qwen3:8b"   # Use faster model (lower quality)
```

### Temperature Tuning

**For more consistency**:
```python
temp_emotional: float = 0.75      # Reduce from 0.82
temp_dramatic: float = 0.78       # Reduce from 0.85
```

**For more variety**:
```python
temp_emotional: float = 0.88      # Increase from 0.82
temp_tension: float = 0.92        # Increase from 0.88
```

---

## 📚 Master Truths v1.2 Compliance

### Core Systems Implemented

#### 1. Emotional Capacity (Section 16)

**Scale**: 0.0-10.0
- Default: 5.0 (baseline human)
- Low: < 5.0 (shows limitations)
- High: ≥ 8.0 (full support)
- Crisis: ≤ 1.0 (cannot support)

**X+2 Support Rule**:
> Character at X/10 capacity can provide UP TO (X + 2)/10 level of emotional support

**Example**:
- Capacity 2.5/10 → Max support 4.5/10
- Needs 7.5/10 support → Shows authentic limitation

#### 2. Dramatic Irony (Section 17)

**Knowledge Gap Score**: ≥ 0.6 triggers irony

**Three Response Types**:
1. **Tone-Deaf** (capacity < 4): High tension (-0.5 to -1.5 relationship)
2. **Misguided** (capacity 4-6): Medium tension (-0.2 to -0.5)
3. **Growth** (capacity ≥ 7): Positive resolution (+0.3 to +0.8)

#### 3. Tension Building (Section 17)

**Four Types**:
1. **Mystery Hook**: Unexplained references (payoff: 2-4 weeks)
2. **Partial Reveal**: Show effect without cause (payoff: 2-4 weeks)
3. **Contradiction**: Against established pattern (payoff: 5-8 weeks)
4. **Stakes Escalation**: Time pressure (payoff: immediate-2 weeks)

**Frequencies**:
- Level 1-2: 33% (1 in 3)
- Level 3-4: 50% (1 in 2)
- Level 5: 90% (nearly every)

#### 4. Memory Resonance (Section 17)

**Five Types**:
1. **Same Emotion, Different Context** (0.8 weight)
2. **Opposite Emotion, Growth** (0.9 weight)
3. **Past Trauma Trigger** (0.95 weight - highest)
4. **Joy/Sadness Contrast** (0.85 weight)
5. **Emotional Growth Callback** (0.7 weight)

---

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **"Cannot connect to Ollama"** | Run `ollama serve` in separate terminal |
| **"Model not found"** | Run `ollama pull qwen3:30b-a3b` |
| **"Out of memory"** | Reduce batch sizes or use qwen3:8b |
| **"JSON parse error"** | Check logs, reduce temperature, increase max_tokens |
| **"Quality scores too low"** | Reduce temperature, smaller batch sizes, add examples |
| **"Generation too slow"** | Use qwen3:8b for speed, check GPU utilization |

### Debug Mode

```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG
python scripts/run_training_pipeline.py
```

### Get Help

```bash
# Collect system information
python scripts/system_check.sh

# View recent logs
tail -n 100 training_generation_v1.2.log

# Test single generation
python -c "
from unwritten.training.qwen3_generator import Qwen3DataGenerator
gen = Qwen3DataGenerator()
batch = gen.generate_emotional_authenticity_batch(batch_size=1)
print(batch)
"
```

---

## 📁 File Structure

```
training_output_v1.2/
├── emotional_authenticity_batch0001_20251014_143022.json
├── emotional_authenticity_batch0002_20251014_145031.json
├── dramatic_irony_batch0001_20251014_143524.json
├── tension_building_batch0001_20251014_144112.json
├── memory_resonance_batch0001_20251014_144558.json
├── personality_traits_batch0001_20251014_142033.json
├── relationship_scoring_batch0001_20251014_142544.json
├── combined_training_data.json (after running --combine)
├── emotional_authenticity_combined_v1.2.json (after --export-by-type)
├── train_set_v1.2.json (after --generate-splits)
├── validation_set_v1.2.json
└── test_set_v1.2.json
```

---

## 🎓 Best Practices

### DO:
✅ Start with test run (1 hour) to verify quality  
✅ Monitor GPU/RAM during generation  
✅ Validate first 100 samples manually  
✅ Use qwen3-30b-a3b for emotional/dramatic/tension/memory  
✅ Use qwen3-8b for personality/relationship (volume)  
✅ Run validation after every 1000 samples  
✅ Filter by quality (≥ 0.7) before training  
✅ Generate train/val/test splits  

### DON'T:
❌ Run on CPU (100x slower)  
❌ Set batch sizes too large (quality degrades)  
❌ Skip quality validation  
❌ Mix v1.1 and v1.2 data  
❌ Delete partial batches (they're valuable)  
❌ Run multiple generators simultaneously  
❌ Ignore capacity constraint violations  

---

## 📊 Expected Performance

### Hardware: RTX 4070 SUPER (12GB VRAM)

**Generation Speed**:
- Emotional Authenticity: 4-6 samples/min (Qwen3-30B)
- Dramatic Irony: 3-5 samples/min (Qwen3-30B)
- Tension Building: 4-6 samples/min (Qwen3-30B)
- Memory Resonance: 5-7 samples/min (Qwen3-30B)
- Personality Traits: 15-20 samples/min (Qwen3-8B)
- Relationship Scoring: 12-15 samples/min (Qwen3-8B)

**Daily Output**: ~9,200 samples (24h continuous)

**Quality Distribution** (expected):
- Excellent (≥ 0.9): 25-35%
- Good (0.7-0.89): 45-55%
- Acceptable (0.5-0.69): 10-15%
- Poor (< 0.5): < 5%

---

## 🔗 Resources

- **Master Truths Spec**: `master_truths_canonical_spec_v_1_2.md`
- **Config Reference**: `config.py`
- **Generator Code**: `qwen3_generator.py`
- **Quality Testing**: `Quality Testing & Validation Guide`
- **Troubleshooting**: `Troubleshooting & Optimization Guide`
- **Analysis Tools**: `analyze_training_data.py`

---

## 📝 Version History

### v1.2 (October 14, 2025)
- ✅ Added Emotional Capacity System (Section 16)
- ✅ Added Dramatic Irony Mechanics (Section 17)
- ✅ Added Tension Building Framework (Section 17)
- ✅ Added Memory Resonance System (Section 17)
- ✅ Enhanced quality validation (5 metrics)
- ✅ Improved prompts (3x longer, 10x more specific)
- ✅ Added capacity constraint validation
- ✅ Increased daily target (6,500 → 9,200 samples)

### v1.1 (October 13, 2025)
- Basic training data generation
- Emotional authenticity (limited)
- OCEAN personality traits
- Relationship scoring

---

## 🎯 Next Steps

1. **Generate Test Batch**: Verify quality with 1-hour run
2. **Manual Review**: Check first 10-20 samples
3. **Full Production**: Run 24-hour cycle
4. **Quality Analysis**: Validate all samples
5. **Export & Split**: Prepare for model training

---

## 📞 Support

**Documentation**:
- Master Truths Spec v1.2
- Quality Testing Guide
- Troubleshooting Guide

**Common Questions**:
- "How do I increase quality?" → Reduce temperature, smaller batches
- "How do I speed up?" → Use qwen3:8b, increase batch size
- "Low pass rate?" → Review prompt examples, adjust thresholds
- "VRAM errors?" → Reduce batch sizes, close other apps

---

**Version**: Master Truths v1.2 Compliant  
**Hardware**: Optimized for RTX 4070 SUPER (12GB VRAM)  
**Model**: Qwen3-30B-A3B (primary)  
**Updated**: October 14, 2025

**Status**: ✅ Production Ready
