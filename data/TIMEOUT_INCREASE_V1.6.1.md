# Timeout Increase v1.6.1 - 4x Stability Enhancement

## Summary

**Increased all timeout values by 4x** to provide more stability for complex training data generation, especially with larger batch sizes (8 examples per batch vs 2).

## Changes Made

### Configuration Timeouts (`src/unwritten/training/config.py`)

#### Request Timeout (General)
```python
# Before (v1.6)
request_timeout: int = 600  # 10 minutes

# After (v1.6.1)
request_timeout: int = 2400  # 40 minutes (4x increase)
```

#### Model-Specific Timeouts

**qwen3:8b (Fast Model)**
```python
# Before (v1.6)
timeout_8b: int = 120  # 2 minutes

# After (v1.6.1)
timeout_8b: int = 480  # 8 minutes (4x increase)
```

**qwen3:30b (Validation Model)**
```python
# Before (v1.6)
timeout_30b: int = 600  # 10 minutes

# After (v1.6.1)
timeout_30b: int = 2400  # 40 minutes (4x increase)
```

**Validation**
```python
# Before (v1.6)
timeout_validation: int = 300  # 5 minutes

# After (v1.6.1)
timeout_validation: int = 1200  # 20 minutes (4x increase)
```

#### Batch Processing Timeout

```python
# Before (v1.6)
batch_processing: Dict = {
    "batch_timeout_seconds": 120,  # 2 minutes
    ...
}

# After (v1.6.1)
batch_processing: Dict = {
    "batch_timeout_seconds": 480,  # 8 minutes (4x increase)
    ...
}
```

## Rationale

### Why 4x Increase?

1. **Larger Batch Sizes (v1.6)**
   - Increased from `batch_size = 2` to `batch_size = 8`
   - 4x more examples per batch = 4x more generation time
   - Linear scaling: 2 min × 4 = 8 min

2. **Complex Generation Requirements**
   - Novel-quality dialogue (60-120 words)
   - Integrated behavioral details
   - NPC Response Framework calculations
   - Urgency × Trust × Capacity multipliers
   - Subtext and tension hooks

3. **Systematic Coverage**
   - 8 complexity types requiring different processing
   - Shuffled complexity ensures variety (more branching)
   - Urgency levels (routine → crisis) add context depth
   - Trust calculations require formula validation

4. **Safety Margin**
   - Prevents timeout errors during peak load
   - Accommodates variation in generation complexity
   - Allows for model "thinking time" on difficult examples

## Timeout Mapping by Operation

| Operation | Old Timeout | New Timeout | Use Case |
|-----------|-------------|-------------|----------|
| **General Request** | 10 min | 40 min | Fallback for unspecified operations |
| **8B Model (Fast)** | 2 min | 8 min | Batch generation (8 examples) |
| **30B Model (Validation)** | 10 min | 40 min | Quality validation (5 examples) |
| **Validation Pass** | 5 min | 20 min | Comprehensive quality checks |
| **Batch API Call** | 2 min | 8 min | Batch processing operations |

## Expected Impact

### Positive Effects ✅
- **Fewer Timeout Errors:** Batch generation won't fail prematurely
- **Better Quality:** Model has time to generate thoughtful responses
- **Higher Success Rate:** Complex scenarios (crisis, mixed_emotions) complete
- **Stability:** Handles variation in generation complexity

### Considerations ⚠️
- **Longer Wait Times:** User must wait up to 8 min per batch (vs 2 min)
- **Delayed Feedback:** Errors discovered later in process
- **Resource Hold:** Model occupied longer per request

### Mitigation Strategies
1. **Progress Logging:** Clear feedback on generation status
2. **Batch Tracking:** Show "Batch X/Y" progress
3. **Early Validation:** Catch issues in parameters before generation
4. **Fallback Behavior:** Auto-retry with individual generation if batch times out

## Testing Recommendations

### Before Full Production Run

1. **Test Single Batch (8 examples)**
   ```bash
   python scripts/run_training_pipeline.py
   # Select option: 8 samples
   ```
   - Verify completion within 8 minutes
   - Check all 8 examples generated
   - Confirm timeout didn't trigger

2. **Test Medium Batch (50 examples)**
   ```bash
   python scripts/run_training_pipeline.py
   # Select option: 50 samples
   ```
   - Verify ~7 batches complete (50 / 8 ≈ 6.25 → 7 batches)
   - Total time: ~56 minutes (7 batches × 8 min)
   - Check coverage report for all 8 complexity types

3. **Monitor Actual Generation Times**
   ```python
   # Check logs for actual durations
   grep "Qwen3 generation" training_generation_systematic.log
   ```
   - If consistently under 2 minutes → timeouts too generous
   - If approaching 8 minutes → timeouts appropriate
   - If timing out → need further increase

### Success Criteria

- ✅ All batches complete without timeout errors
- ✅ Coverage report shows 8/8 complexity types
- ✅ Authenticity distribution balanced (not 64% excellent)
- ✅ Quality assessment: "complete" and "good"

## Rollback Plan

If 4x increase causes issues:

### Scenario 1: Timeouts Still Too Short
```python
# Increase to 6x or 8x
timeout_8b: int = 720  # 12 minutes (6x)
# OR
timeout_8b: int = 960  # 16 minutes (8x)
```

### Scenario 2: Timeouts Too Long (Unnecessary)
```python
# Reduce to 3x or 2x
timeout_8b: int = 360  # 6 minutes (3x)
# OR
timeout_8b: int = 240  # 4 minutes (2x)
```

### Scenario 3: Batch Size Too Large
```python
# Reduce batch_size back to 4 (v1.6 fix)
batch_size = 4  # Instead of 8
timeout_8b: int = 240  # 4 minutes (2x)
```

## Files Modified

### Core Configuration
- **src/unwritten/training/config.py**
  - `request_timeout`: 600 → 2400 (+1800 seconds)
  - `timeout_8b`: 120 → 480 (+360 seconds)
  - `timeout_30b`: 600 → 2400 (+1800 seconds)
  - `timeout_validation`: 300 → 1200 (+900 seconds)
  - `batch_timeout_seconds`: 120 → 480 (+360 seconds)

### Documentation
- **TIMEOUT_INCREASE_V1.6.1.md** (this file)

## Version History

- **v1.6:** Fixed complexity coverage (batch_size 2 → 8, shuffling)
- **v1.6.1:** Increased timeouts 4x to match batch_size increase ← **CURRENT**

## Next Steps

1. ✅ Test with 8-example batch (single batch test)
2. ⏳ Test with 50-example generation (coverage test)
3. ⏳ Analyze actual generation times vs timeouts
4. ⏳ Adjust if needed based on real-world performance
5. ⏳ Run full 2000-example production if tests pass

## Credits

**v1.6.1 timeout adjustment:**
- Matched timeout increase to batch_size increase (2 → 8)
- Linear scaling principle: 4x examples = 4x time
- Safety margin for complex generation scenarios

Version: 1.6.1  
Date: 2025-10-14  
Status: Ready for Testing  
Impact: Stability Enhancement  
Maintainer: Unwritten Training Pipeline


