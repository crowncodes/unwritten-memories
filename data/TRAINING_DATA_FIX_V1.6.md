# Training Data Generation Fix v1.6 - Coverage Issues Resolved

## Summary

**v1.6 fixes critical coverage issues** discovered in the coverage report showing only 2/8 complexity types covered and 64% clustering in "excellent" authenticity.

## Problems Identified from Coverage Report

### 1. ❌ Complexity Coverage - CRITICAL FAILURE
**Observed:**
- Only **2 out of 8** complexity types generated:
  - `people_pleasing`: 32 samples (64%)
  - `baseline`: 18 samples (36%)
  
**Missing 6 complexity types:**
- `misjudgment_over` ❌
- `emergency_override` ❌
- `mixed_emotions` ❌
- `misjudgment_under` ❌
- `defensive_lashing` ❌
- `cultural_indirect` ❌

**Root Cause:**
- `batch_size = 2` meant only 2 complexity types per batch
- Cycling through 8 types with `i % 8` always selected types 0 and 1
- Model may have been defaulting to "easy" types (baseline, people_pleasing)

### 2. ❌ Authenticity Distribution - SEVERE IMBALANCE
**Observed:**
```
excellent (0.8-1.0):  32 samples (64%) ← WAY TOO HIGH!
authentic (0.6-0.8):   8 samples (16%)
struggling (0.4-0.6):  6 samples (12%)
failed (0.2-0.4):      4 samples (8%)
```

**Target (from config):**
```
excellent: 25-30% (config: 0.30)
authentic: 30-35% (config: 0.35)
struggling: 20-25% (config: 0.20)
failed: 15-20% (config: 0.15)
```

**Root Cause:**
- Model was generating higher quality than requested
- Frequency weights not strong enough to overcome model bias

### 3. ❌ Quality Assessment
```json
"quality_assessment": {
    "meets_spectrum_requirements": false,
    "authenticity_balance": "needs_improvement",
    "complexity_coverage": "incomplete"
}
```

## Fixes Implemented

### Fix 1: ✅ Shuffle Complexity Types

**Before (v1.5):**
```python
complexity = complexity_types[i % len(complexity_types)]
# With batch_size=2, always selected [0, 1] (baseline, people_pleasing)
```

**After (v1.6):**
```python
# Shuffle complexity types each batch to ensure variety
shuffled_complexity = complexity_types.copy()
random.shuffle(shuffled_complexity)

# Use shuffled list
complexity = shuffled_complexity[i % len(shuffled_complexity)]
```

**Impact:**
- Each batch now gets random selection of complexity types
- No more clustering on first 2 types
- Better coverage across all 8 types

### Fix 2: ✅ Increase Batch Size

**Before (v1.5):**
```python
batch_size = 2  # Only 2 complexity types per batch
```

**After (v1.6):**
```python
if use_batch_processing:
    batch_size = 4  # Doubled to cover more types
else:
    batch_size = 8  # Individual mode covers all types
```

**Impact:**
- Batch processing now generates 4 examples per call (instead of 2)
- 4 different complexity types per batch minimum
- Faster coverage of all 8 types
- Balance of coverage vs API stability

### Fix 3: ✅ Rebalanced Authenticity Frequencies

**Before (v1.5):**
```python
authenticity_targets = [
    {"name": "failed", "range": (0.2, 0.4), "frequency": 0.15},
    {"name": "struggling", "range": (0.4, 0.6), "frequency": 0.20},
    {"name": "authentic", "range": (0.6, 0.8), "frequency": 0.35},
    {"name": "excellent", "range": (0.8, 1.0), "frequency": 0.30},
]
# Result: 64% excellent (model bias toward high quality)
```

**After (v1.6):**
```python
authenticity_targets = [
    {"name": "failed", "range": (0.2, 0.4), "frequency": 0.20},  # +5%
    {"name": "struggling", "range": (0.4, 0.6), "frequency": 0.25},  # +5%
    {"name": "authentic", "range": (0.6, 0.8), "frequency": 0.30},  # -5%
    {"name": "excellent", "range": (0.8, 1.0), "frequency": 0.25},  # -5%
]
# Target: More balanced distribution
```

**Impact:**
- Increased weight for lower-quality examples
- Reduced excellent clustering
- Better spectrum coverage

### Fix 4: ✅ Stronger Prompt Enforcement

**Added to prompt:**
```
⚠️ REQUIRED COMPLEXITY TYPE: {scenario['complexity_type']}
You MUST implement this specific complexity type. Do NOT default to baseline or people_pleasing.
COMPLEXITY: {instructions}
```

**Impact:**
- Explicit warning against defaulting to easy types
- Model reminded to follow specified complexity
- Reduces model bias toward simple examples

## Expected Results (Next Generation)

### Complexity Coverage Target
```
baseline:            12-15% (6-8 samples per 50)
people_pleasing:     12-15% (6-8 samples per 50)
misjudgment_over:    12-15% (6-8 samples per 50)
misjudgment_under:   10-12% (5-6 samples per 50)
defensive_lashing:   10-12% (5-6 samples per 50)
emergency_override:  12-15% (6-8 samples per 50)
cultural_indirect:   10-12% (5-6 samples per 50)
mixed_emotions:      12-15% (6-8 samples per 50)
```
**All 8 types covered, roughly balanced**

### Authenticity Distribution Target
```
excellent (0.8-1.0):  25-30% (12-15 samples per 50)
authentic (0.6-0.8):  30-35% (15-18 samples per 50)
struggling (0.4-0.6): 20-25% (10-12 samples per 50)
failed (0.2-0.4):     15-20% (8-10 samples per 50)
```
**Balanced across full spectrum**

### Quality Assessment Target
```json
"quality_assessment": {
    "meets_spectrum_requirements": true,
    "authenticity_balance": "good",
    "complexity_coverage": "complete"
}
```

## Validation Checklist

After next generation, verify:

### Complexity Coverage
- [ ] All 8 complexity types present
- [ ] No type exceeds 20% of total
- [ ] No type below 8% of total
- [ ] `gaps_to_fill` array is empty

### Authenticity Distribution
- [ ] Excellent: 20-35% (not 64%!)
- [ ] Authentic: 25-40%
- [ ] Struggling: 15-30%
- [ ] Failed: 10-25%
- [ ] `meets_spectrum_requirements: true`

### Quality Metrics
- [ ] `authenticity_balance: "good"` or better
- [ ] `complexity_coverage: "complete"`
- [ ] No clustering warnings

## Testing Instructions

### 1. Generate New Batch
```powershell
python scripts/run_training_pipeline.py
```
Select option 1 (50 samples) for quick test.

### 2. Check Coverage Report
```powershell
# Find latest coverage report
ls training_output_v1.2_systematic/coverage_report_*.json | sort -Descending | select -First 1

# View coverage
cat training_output_v1.2_systematic/coverage_report_[timestamp].json
```

### 3. Validate Results
```python
import json
from pathlib import Path

# Load latest coverage report
reports = sorted(Path("training_output_v1.2_systematic").glob("coverage_report_*.json"))
with open(reports[-1]) as f:
    report = json.load(f)

# Check complexity coverage
complexity = report['current_batch_coverage']['complexity_coverage']
print(f"Complexity types covered: {len(complexity)}/8")
print("Distribution:")
for ctype, count in sorted(complexity.items()):
    pct = count / 50 * 100
    print(f"  {ctype}: {count} ({pct:.1f}%)")

# Check authenticity distribution
auth = report['current_batch_coverage']['authenticity_distribution']
print("\nAuthenticity distribution:")
for tier, count in sorted(auth.items()):
    pct = count / 50 * 100
    print(f"  {tier}: {count} ({pct:.1f}%)")

# Check quality
quality = report['quality_assessment']
print(f"\nQuality Assessment:")
print(f"  Spectrum requirements: {quality['meets_spectrum_requirements']}")
print(f"  Authenticity balance: {quality['authenticity_balance']}")
print(f"  Complexity coverage: {quality['complexity_coverage']}")
```

## If Issues Persist

### Issue: Still seeing only 2-3 complexity types

**Additional Fix:**
```python
# In systematic_generator.py, increase batch_size further
batch_size = 8  # Ensure all 8 types per batch
```

### Issue: Still clustering in "excellent"

**Additional Fix:**
```python
# Further reduce excellent frequency
{"name": "excellent", "range": (0.8, 1.0), "frequency": 0.20},  # Down to 20%
```

### Issue: Model ignoring complexity instructions

**Additional Fix:**
Add validation that rejects examples that don't match requested complexity:

```python
def validate_complexity_match(sample, requested_complexity):
    """Validate sample matches requested complexity type"""
    response = sample['character_response']['dialogue'].lower()
    
    # Check for complexity indicators
    indicators = {
        'people_pleasing': ['yes', 'sure', 'can do', 'no problem'],
        'defensive_lashing': ['why is this my problem', 'not my fault'],
        'misjudgment_over': ['I thought I could', 'I can handle'],
        # ... etc
    }
    
    if requested_complexity in indicators:
        has_indicator = any(ind in response for ind in indicators[requested_complexity])
        if not has_indicator:
            return False, f"Missing {requested_complexity} indicators"
    
    return True, "Valid"
```

## Files Modified

### Core Changes
- **src/unwritten/training/systematic_generator.py**
  - `_generate_systematic_parameters()`: Added complexity shuffling
  - Rebalanced authenticity frequencies
  - Increased batch_size from 2 to 4
  - Added stronger prompt enforcement

### Documentation
- **TRAINING_DATA_FIX_V1.6.md** (this file)

## Version History

- **v1.2:** Original (melodramatic)
- **v1.3:** Reduced dialogue (too sparse)
- **v1.4:** Sweet spot dialogue (60-120 words)
- **v1.5:** Added NPC Response Framework
- **v1.6:** Fixed complexity coverage & authenticity clustering ← **CURRENT**

## Impact Summary

### Before v1.6 (Coverage Report Issues)
- ❌ Complexity: 2/8 types (25% coverage)
- ❌ Authenticity: 64% excellent (severe clustering)
- ❌ Quality: "needs_improvement", "incomplete"

### After v1.6 (Expected)
- ✅ Complexity: 8/8 types (100% coverage)
- ✅ Authenticity: 25% excellent (balanced)
- ✅ Quality: "good", "complete"

### Generation Efficiency
- Before: 25 batches × 2 examples = 50 samples (only 2 types per batch)
- After: 13 batches × 4 examples = 52 samples (4+ types per batch)
- **Improvement:** 2x faster coverage of all complexity types

## Next Steps

1. ✅ Generate test batch (50 samples)
2. ⏳ Verify complexity coverage (all 8 types)
3. ⏳ Verify authenticity distribution (no clustering)
4. ⏳ Check quality assessment (meets requirements)
5. ⏳ If good, scale to full production (2000 samples)
6. ⏳ Document final quality metrics

## Credits

**v1.6 fixes based on coverage report analysis:**
- Identified complexity coverage failure (2/8 types)
- Identified authenticity clustering (64% excellent)
- Implemented shuffling + rebalancing + batch size increase
- Added stronger prompt enforcement

Version: 1.6  
Date: 2025-10-14  
Status: Ready for Testing  
Maintainer: Unwritten Training Pipeline



