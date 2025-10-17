# Single-Example Mode for Stability v1.6.3

**Date:** 2025-10-14  
**Status:** ✅ Implemented  
**Version:** v1.6.3  
**Reason:** Prevent crashes from 30B model memory usage

## Problem

Computer crashed during batch generation with 30B model due to **memory pressure**.

### Memory Issues
- **30B model**: ~18-20GB VRAM when active
- **Batch of 8**: Trying to keep context for all 8 examples in memory
- **16K max_tokens**: Huge output buffer allocated
- **Result**: System crash from memory exhaustion

## Solution: Single-Example Mode

Generate **ONE example at a time** instead of batches.

## Changes Made

### 1. Batch Sizes → 1
```python
# Before
batch_size_emotional: int = 8  # Crashes on 30B model

# After
batch_size_emotional: int = 1  # ONE at a time
batch_size_dramatic: int = 1
batch_size_tension: int = 1
batch_size_memory: int = 1
batch_size_personality: int = 1
batch_size_relationship: int = 1
```

### 2. Disable Batch API Calls
```python
# Before
"enable_batch_api_calls": True,  # Multiple examples per call
"batch_api_max_examples": 5,

# After
"enable_batch_api_calls": False,  # v1.6.3: DISABLED
"batch_api_max_examples": 1,     # Only 1 per call
```

### 3. Reduce max_tokens for Stability
```python
# Before
max_tokens: int = 16000  # Too memory-intensive

# After
max_tokens: int = 4000  # Still allows 60-120 word dialogue + full JSON
```

### 4. Updated systematic_generator.py
```python
# Now uses config value instead of hardcoded
max_tokens=self.config.max_tokens  # v1.6.3: Use config for stability
```

## Expected Behavior

### Generation Process (Single-Example Mode)
```
1. Generate parameter combination
2. Build prompt
3. Call Ollama with ONE example
4. Parse JSON response
5. Save to file
6. Update coverage database
7. [REPEAT for next example]
```

### Memory Profile
- **Before**: 18-20GB VRAM (batch of 8)
- **After**: 12-15GB VRAM (single example)
- **Stability**: Much lower peak memory, no crashes

### Performance
- **Before**: 8 examples in 8-12 minutes (when it doesn't crash)
- **After**: 1 example in 1-2 minutes, 50 examples = ~50-100 minutes
- **Trade-off**: Slower but **STABLE**

## If Still Crashing

Switch to **8B model** for even lower memory usage:

```python
# In config.py line 51
model_primary: str = "qwen3:8b"  # Instead of "qwen3:30b-a3b"
```

### 8B Model Profile
- **VRAM**: 6-8GB (much lighter)
- **Speed**: 30-45 seconds per example
- **Trade-off**: More likely to use clichés, but won't crash

## Recommendations

### For Your RTX 4070 SUPER (12GB VRAM)

**Option 1: Try 30B single-example first**
- Should work now with batch_size=1
- Best quality, language-agnostic
- ~1-2 min per example

**Option 2: If 30B still crashes → switch to 8B**
- Guaranteed stable
- Faster generation
- Acceptable quality with language-agnostic prompt

**Option 3: Hybrid approach**
- Use 8B for bulk generation (500+ examples)
- Use 30B for final polish/quality checks

## Testing

Run a small test first:
```bash
python scripts/run_training_pipeline.py
# When prompted, enter target: 5
# Should generate 5 examples without crashing
```

Watch Task Manager:
- GPU memory should stay under 15GB
- If approaching 12GB, kill and switch to 8B

## Files Modified

- `src/unwritten/training/config.py`
  - Line 51: Added note about switching to 8B if needed
  - Line 63-68: All batch sizes set to 1
  - Line 101: max_tokens reduced to 4000
  - Line 179: Batch API disabled

- `src/unwritten/training/systematic_generator.py`
  - Line 507: Use config.max_tokens
  - Line 664: Use config.max_tokens

## Backward Compatibility

✅ Fully compatible - just changes batch size, no data structure changes

## Version History

- **v1.6.3**: Single-example mode for stability (current)
- **v1.6.2**: Diversity tuning (caused crashes with batches)
- **v1.6.1**: Timeout increases
- **v1.6**: Coverage fixes

---

**Status:** Ready to test! Should be stable now with ONE example at a time. 🎯

