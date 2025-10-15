# Qwen3 Training Data Generation Strategy
## Novel-Quality Character Interactions for Dramatic Irony System

---

## Executive Summary

This strategy leverages **Qwen3 models via Ollama** to generate 40,000+ high-quality training samples over 7-10 days for your narrative game system. By using a multi-model approach optimized for your RTX 4070 SUPER, you'll generate authentic character psychology, dramatic irony scenarios, and emotional capacity constraints at scale.

**Key Innovation:** Local 24/7 generation with Qwen3's MoE architecture gives you Claude Sonnet-level quality at ~10x lower cost and 3-4x faster speeds.

---

## Hardware Configuration

### Your Setup
- **GPU:** RTX 4070 SUPER (12GB VRAM)
- **RAM:** 128GB
- **Storage:** Sufficient for models (~60GB needed)

### Model Assignment Strategy

| Model | Size | Use Case | Performance | When to Use |
|-------|------|----------|-------------|-------------|
| **Qwen3-30B-A3B** | ~18GB | Primary quality generation | 25-40 tok/s | Emotional authenticity, dramatic irony |
| **Qwen3-8B** | ~5GB | Volume generation | 35-50 tok/s | Personality traits, relationship scoring |
| **Qwen3-32B** | ~20GB | Validation | 12-20 tok/s | Quality checking (10% sample) |

**Why this works:**
- **30B-A3B** fits in VRAM with 3B active parameters (MoE efficiency)
- **8B** runs entirely on GPU for maximum speed
- **32B** uses CPU+GPU hybrid for thorough validation
- All three can be loaded simultaneously with your 128GB RAM

---

## Training Data Types & Priorities

### 1. Emotional Authenticity Data (HIGHEST PRIORITY)
**Target:** 1,500 samples/day | 12,000 total

**Why Critical:**
- Core of your system's realism
- Characters must behave according to emotional capacity (1-10 scale)
- Low capacity = cannot provide emotional support, regardless of caring
- This is what makes characters feel real vs. robotic

**Generation Parameters:**
- Model: Qwen3-30B-A3B (needs sophisticated psychology understanding)
- Batch size: 15 examples
- Temperature: 0.88 (high variety while maintaining coherence)
- Focus: Realistic human limitations, authentic failure modes

**Quality Metrics:**
- Authenticity score >0.85
- Clear capacity constraint demonstration
- Realistic internal thoughts
- OCEAN trait integration

### 2. Dramatic Irony Scenarios (HIGH COMPLEXITY)
**Target:** 1,200 samples/day | 9,600 total

**Purpose:**
- Create "yelling at screen" tension moments
- Player knows something character doesn't
- Three dialogue options per scenario (tone-deaf, misguided, growth)

**Generation Parameters:**
- Model: Qwen3-30B-A3B (complex reasoning about knowledge gaps)
- Batch size: 10 scenarios (3 options each = 30 total examples)
- Temperature: 0.82 (controlled creativity)
- Focus: Knowledge gap clarity, tension building, realistic consequences

**Structure:**
```
Player Knows → Character Doesn't Know → Knowledge Gap → Tension
```

### 3. Personality Trait Data (FOUNDATION)
**Target:** 2,000 samples/day | 16,000 total

**Purpose:**
- OCEAN trait prediction from dialogue
- Foundation for personality-driven behavior
- Largest volume dataset

**Generation Parameters:**
- Model: Qwen3-8B (fast generation for volume)
- Batch size: 25 examples
- Temperature: 0.9 (maximum diversity)
- Focus: Diverse scenarios, clear trait expression

### 4. Tension Building Data (NARRATIVE QUALITY)
**Target:** 800 samples/day | 6,400 total

**Purpose:**
- Incomplete revelations
- Contradictory behavior
- Information debt
- Foreshadowing

**Generation Parameters:**
- Model: Qwen3-30B-A3B (sophisticated narrative understanding)
- Batch size: 12 examples
- Temperature: 0.85
- Focus: Mystery creation, payoff timing

### 5. Relationship Scoring Data (INTERACTION QUALITY)
**Target:** 1,000 samples/day | 8,000 total

**Purpose:**
- Score player-character interactions (0-1 scale)
- Teach model what strengthens/damages relationships

**Generation Parameters:**
- Model: Qwen3-8B (fast generation)
- Batch size: 20 examples
- Temperature: 0.88
- Focus: Clear scoring rationale, diverse interaction types

---

## Daily Production Schedule (24/7 Operation)

### Optimal Batch Timing

**Phase 1: High-Quality Generation (Hours 0-16)**
```
00:00-04:00  Emotional Authenticity (100 batches × 15 = 1,500 samples)
04:00-08:00  Dramatic Irony (120 batches × 10 = 1,200 scenarios)
08:00-12:00  Personality Traits (80 batches × 25 = 2,000 samples)
12:00-14:00  Tension Building (67 batches × 12 = 800 samples)
14:00-16:00  Relationship Scoring (50 batches × 20 = 1,000 samples)
```

**Phase 2: Validation (Hours 16-20)**
```
16:00-20:00  Quality validation with Qwen3-32B (10% sample)
             - Check authenticity scores
             - Verify logical consistency
             - Flag problematic examples
```

**Phase 3: Data Processing (Hours 20-24)**
```
20:00-24:00  Compile results, save files, prepare next cycle
             - Merge JSON outputs
             - Run deduplication
             - Generate quality reports
```

### Expected Output

**Per Day:**
- Emotional Authenticity: ~1,500 samples
- Dramatic Irony: ~1,200 scenarios (×3 options = 3,600 examples)
- Personality Traits: ~2,000 samples
- Tension Building: ~800 samples
- Relationship Scoring: ~1,000 samples

**Total Daily:** ~6,500 training examples

**7-Day Production:** ~45,000 samples (exceeds 40k target with buffer)

---

## Quality Assurance Strategy

### Multi-Stage Validation

**Stage 1: Generation-Time Checks**
- JSON parsing validation
- Required field verification
- Score range validation (0-1 bounds)
- Basic consistency checks

**Stage 2: Batch Validation (Qwen3-32B)**
- Sample 10% of each data type
- Evaluate on 4 dimensions:
  - Authenticity (0-1)
  - Consistency (0-1)
  - Complexity (0-1)
  - Usability (0-1)
- Flag batches <0.7 overall quality

**Stage 3: Human Review**
- Review flagged batches
- Check edge cases
- Verify dramatic irony tension
- Validate emotional capacity constraints

### Quality Metrics

**Minimum Acceptable:**
- Overall quality score: >0.75
- Authenticity: >0.80
- Consistency: >0.85
- No logical contradictions
- Clear training signal

**Target Quality:**
- Overall quality score: >0.85
- Authenticity: >0.90
- Consistency: >0.92
- Novel-quality writing
- Nuanced psychology

---

## Prompt Engineering Best Practices

### Key Principles for Qwen3

1. **Be Explicit About Constraints**
   - State capacity limitations clearly
   - Define OCEAN trait ranges
   - Specify score bounds (0-1, 1-10, etc.)

2. **Provide High-Quality Examples**
   - Include 2-3 examples per prompt
   - Show edge cases (capacity 2/10 vs 8/10)
   - Demonstrate good vs bad quality

3. **Use Structured Output Formats**
   - Always request JSON
   - Define schema clearly
   - Include all required fields

4. **Leverage Qwen3's Reasoning Mode**
   - For dramatic irony: "Think through the knowledge gap..."
   - For authenticity: "Consider realistic human limitations..."
   - For tension: "Analyze what makes this create suspense..."

5. **Temperature Settings**
   - Creative generation: 0.85-0.9
   - Consistent quality: 0.75-0.82
   - Validation: 0.3-0.5 (lower for consistency)

### Common Pitfalls to Avoid

❌ **Don't:**
- Request too many examples per batch (causes quality degradation)
- Use vague emotional descriptors
- Mix multiple objectives in one prompt
- Forget to clean JSON responses (remove markdown)

✅ **Do:**
- Keep batches focused (10-25 examples max)
- Provide specific emotional capacity values
- One prompt = one clear objective
- Always strip ```json markdown blocks

---

## Cost & Efficiency Analysis

### Local vs Cloud Comparison

**Local (Qwen3 via Ollama):**
- Hardware: Already owned (RTX 4070 SUPER)
- Electricity: ~$3-5/day (24/7 operation)
- Total 7-day cost: **~$25-35**
- Output: 45,000+ samples

**Cloud (Claude 3.5 Sonnet API):**
- API costs: ~$15 per 1M tokens
- 40k samples × ~500 tokens avg = 20M tokens
- Input: ~10M tokens × $3 = $30
- Output: ~10M tokens × $15 = $150
- Total: **~$180**

**Savings: ~$145-155** (5-7x cheaper)

**Additional Benefits:**
- No API rate limits
- No network latency
- Full data privacy
- Unlimited iterations

### Performance Expectations

**Generation Speed:**
| Model | Tokens/Second | Samples/Hour | Daily Output |
|-------|---------------|--------------|--------------|
| 30B-A3B | 25-40 | 150-240 | 3,600-5,760 |
| 8B | 35-50 | 400-600 | 9,600-14,400 |
| 32B (validation) | 12-20 | 90-150 | 2,160-3,600 |

**Realistic Mixed Workload:**
- High-quality (30B-A3B): ~4,500 samples/day
- Volume (8B): ~3,000 samples/day
- **Total: ~6,500-7,500 samples/day**

---

## Implementation Roadmap

### Week 1: Setup & Initial Generation

**Days 1-2: Environment Setup**
- [ ] Install Ollama
- [ ] Pull Qwen3 models (30b-a3b, 8b, 32b)
- [ ] Configure OLLAMA_KEEP_ALIVE=24h
- [ ] Test generation pipeline
- [ ] Verify GPU/CPU utilization

**Days 3-7: Full Production**
- [ ] Run 24/7 generation pipeline
- [ ] Monitor quality scores
- [ ] Adjust prompts based on validation
- [ ] Collect ~30,000+ samples

### Week 2: Optimization & Completion

**Days 8-10: Targeted Generation**
- [ ] Focus on low-sample areas
- [ ] Generate edge cases
- [ ] Increase dramatic irony complexity
- [ ] Collect final 10,000-15,000 samples

**Days 11-12: Quality Review**
- [ ] Human review of sample batches
- [ ] Remove duplicates/low-quality
- [ ] Balance dataset proportions
- [ ] Create final training dataset

**Days 13-14: Preparation for Training**
- [ ] Split train/validation/test sets
- [ ] Format for your training pipeline
- [ ] Document dataset statistics
- [ ] Archive raw generation logs

---

## Advanced Techniques

### 1. Iterative Refinement
```python
# Generate initial batch
batch_1 = generator.generate_emotional_authenticity_batch()

# Validate and identify issues
validation = generator.validate_with_qwen3_32b(batch_1, 'emotional_authenticity')

# Regenerate low-quality examples with refined prompt
if validation['overall_quality'] < 0.8:
    # Add specific guidance based on validation feedback
    batch_2 = generator.generate_with_refined_prompt(validation['recommendations'])
```

### 2. Chain-of-Thought for Complex Scenarios
For dramatic irony, use reasoning prompts:
```
"Before generating the scenario, think through:
1. What secret information exists?
2. Why doesn't the character know?
3. What would create maximum tension?
4. How would different personality types respond?

Then generate the complete scenario."
```

### 3. Few-Shot Learning with Quality Examples
Always include 2-3 high-quality examples in prompts to anchor output quality.

### 4. Temperature Ramping
- Start with lower temp (0.7-0.75) for consistent baseline
- Gradually increase (0.85-0.9) for diversity
- Blend both approaches in final dataset

### 5. Cross-Model Validation
- Generate with 30B-A3B
- Validate with 32B (different model reduces bias)
- Regenerate flagged examples with 30B-A3B

---

## Monitoring & Metrics

### Real-Time Monitoring

**Dashboard Metrics:**
```python
{
  "samples_generated": 0,
  "samples_per_hour": 0,
  "current_model": "qwen3:30b-a3b",
  "gpu_utilization": "95%",
  "vram_usage": "11.2 / 12 GB",
  "estimated_completion": "14:30:00",
  "quality_score_avg": 0.87,
  "batches_failed": 0
}
```

### Daily Quality Reports

**Generate Summary:**
```
📊 Day 3 Production Report
==========================
Emotional Authenticity: 1,487 samples (99% of target)
  - Avg quality: 0.89
  - Authenticity: 0.92
  - Consistency: 0.88

Dramatic Irony: 1,203 scenarios (100% of target)
  - Avg quality: 0.86
  - Tension scores: 0.75-0.95
  - Knowledge gaps: Clear

Personality Traits: 2,041 samples (102% of target)
  - Avg quality: 0.84
  - Trait diversity: High
  - Scenario variety: Excellent

⚠️ Issues:
- 3 batches failed JSON parsing
- 2 batches < 0.7 quality (regenerated)

✅ Status: On track for 45k samples by Day 7
```

---

## Troubleshooting Common Issues

### Issue: JSON Parsing Failures

**Symptoms:** `json.JSONDecodeError` when parsing responses

**Solutions:**
1. Strip markdown blocks: ` ```json\n...\n``` `
2. Increase temperature slightly (0.82 → 0.85)
3. Add explicit "Return ONLY valid JSON array" instruction
4. Implement retry logic (max 3 attempts)

### Issue: Low Quality Scores

**Symptoms:** Validation <0.7, generic responses

**Solutions:**
1. Reduce batch size (25 → 15)
2. Add more specific examples
3. Increase prompt detail (constraints, edge cases)
4. Use Qwen3-30B-A3B instead of 8B for complex tasks

### Issue: Model Running Slow

**Symptoms:** <15 tokens/sec for 30B-A3B

**Solutions:**
1. Check GPU layers: `export OLLAMA_GPU_LAYERS=999`
2. Reduce loaded models (keep only 1-2 in memory)
3. Restart Ollama daemon
4. Verify VRAM not saturated (use `nvidia-smi`)

### Issue: Repetitive Outputs

**Symptoms:** Similar examples, low diversity

**Solutions:**
1. Increase temperature (0.85 → 0.92)
2. Add "Generate DIVERSE examples" instruction
3. Use different seed examples
4. Vary prompt phrasing between batches

### Issue: Dramatic Irony Scenarios Too Simple

**Symptoms:** Obvious knowledge gaps, low tension

**Solutions:**
1. Request "subtle" irony in prompt
2. Add examples of complex scenarios
3. Use chain-of-thought reasoning
4. Specify minimum tension score (>0.75)

---

## Success Metrics

### Quantitative Targets

**Volume:**
- [ ] ≥40,000 total samples
- [ ] ≥10,000 emotional authenticity
- [ ] ≥8,000 dramatic irony scenarios
- [ ] ≥12,000 personality traits
- [ ] ≥5,000 tension building
- [ ] ≥6,000 relationship scoring

**Quality:**
- [ ] Overall quality >0.85
- [ ] Authenticity >0.88
- [ ] Consistency >0.90
- [ ] <5% failed batches
- [ ] <2% duplicate samples

**Efficiency:**
- [ ] ≥6,000 samples/day average
- [ ] <$50 total cost (electricity)
- [ ] <3 hours manual review/day
- [ ] 90%+ automated generation

### Qualitative Targets

**Emotional Authenticity:**
- [ ] Characters clearly constrained by capacity
- [ ] Realistic failure modes shown
- [ ] Internal thoughts feel authentic
- [ ] OCEAN traits integrated naturally

**Dramatic Irony:**
- [ ] Clear knowledge gaps
- [ ] "Yelling at screen" tension evident
- [ ] Three distinct option types
- [ ] Realistic consequences

**Overall:**
- [ ] Novel-quality writing
- [ ] Nuanced psychology
- [ ] Varied scenarios
- [ ] Trainable signal for model

---

## Next Steps After Generation

### 1. Dataset Preparation
```python
# Combine all JSON files
combined_data = merge_all_training_files()

# Remove duplicates
deduplicated = remove_near_duplicates(combined_data, threshold=0.85)

# Balance dataset
balanced = balance_data_types(deduplicated)

# Split train/val/test
train, val, test = split_dataset(balanced, ratios=[0.8, 0.1, 0.1])
```

### 2. Training Configuration
```python
training_config = {
  "base_model": "your-chosen-model",
  "lora_rank": 16,
  "lora_alpha": 32,
  "learning_rate": 2e-4,
  "batch_size": 8,
  "epochs": 3,
  "warmup_steps": 100,
  "gradient_accumulation": 4
}
```

### 3. Evaluation Metrics
- Emotional authenticity accuracy
- Dramatic irony tension scores
- OCEAN trait prediction MAE
- Relationship scoring accuracy
- Narrative quality (human eval)

### 4. Iteration
- Identify weak areas
- Generate targeted supplemental data
- Retrain with enhanced dataset
- A/B test in actual game scenarios

---

## Conclusion

This strategy leverages Qwen3's advanced capabilities to generate 40,000+ high-quality training samples in 7-10 days at <$50 cost. By using a multi-model approach optimized for your hardware:

**✅ Quality:** Qwen3-30B-A3B provides Claude Sonnet-level psychological understanding  
**✅ Speed:** MoE architecture delivers 3-4x faster generation  
**✅ Cost:** Local generation is 5-7x cheaper than cloud APIs  
**✅ Scale:** 24/7 operation produces 6,500+ samples daily  

Your dramatic irony system's core innovations—emotional capacity constraints, knowledge gap tension, and personality-driven behavior—require sophisticated training data. Qwen3's 36 trillion token training, 128K context window, and enhanced reasoning modes make it ideal for this use case.

**Start with the provided Python pipeline, run your first 24-hour cycle, and iterate based on validation results. Within 2 weeks, you'll have a complete, high-quality dataset ready for fine-tuning.**

---

## Quick Start Commands

```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Pull models
ollama pull qwen3:30b-a3b
ollama pull qwen3:8b
ollama pull qwen3:32b

# 3. Configure for 24/7
export OLLAMA_KEEP_ALIVE=24h
export OLLAMA_MAX_LOADED_MODELS=3
export OLLAMA_GPU_LAYERS=999

# 4. Start generation
python qwen3_training_pipeline.py

# 5. Monitor progress
tail -f generation.log
```

**You're ready to generate novel-quality training data at scale! 🚀**
