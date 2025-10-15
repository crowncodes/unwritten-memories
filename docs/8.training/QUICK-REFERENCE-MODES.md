# Quick Reference: Generation Modes

Choose the right mode for your needs:

---

## 🎯 Balanced Mode (Default) ⭐ RECOMMENDED

```python
generation_mode = "balanced"
```

### Use When
- Generating production training data
- Need both coverage AND authenticity
- Want natural variation with systematic guarantees

### Results
- ✅ **80% spectrum coverage** (vs 40% random, 100% strict)
- ✅ **4-6 complexity types** per batch (natural emergence)
- ✅ **High authenticity** (feels real, not calculated)
- ✅ **±20% score flexibility** (not hitting exact targets)
- ✅ **30% distribution tolerance** (allows natural clustering)

### Trade-offs
- Slightly less coverage than strict mode
- More monitoring needed than strict mode
- Best balance of all approaches

---

## 🔬 Strict Mode

```python
generation_mode = "strict"
```

### Use When
- Testing coverage algorithms
- Research purposes
- Need guaranteed 100% parameter coverage
- Willing to sacrifice some naturalness

### Results
- ✅ **100% spectrum coverage** (every category represented)
- ✅ **All 8 complexity types** (forced in every batch)
- ✅ **Systematic guarantees** (no gaps)
- ⚠️ **May feel mechanical** (optimized for coverage)
- ⚠️ **±10% score flexibility** (tight targeting)

### Trade-offs
- Risk of artificial variation
- May feel "written to spec"
- Good for algorithms, not production

---

## 🌿 Organic Mode

```python
generation_mode = "organic"
```

### Use When
- Maximum authenticity needed
- Creative/novel scenarios
- Don't need comprehensive coverage
- Want human-like natural variation

### Results
- ✅ **Very high authenticity** (most natural feeling)
- ✅ **3-4 complexity types** (organic emergence only)
- ✅ **±40% score flexibility** (wide natural variation)
- ✅ **No tracking overhead** (fast generation)
- ⚠️ **60% spectrum coverage** (lower than systematic)

### Trade-offs
- Less systematic coverage
- May miss important edge cases
- More like improved random generation

---

## Quick Comparison

| Feature | Organic | **Balanced** ⭐ | Strict |
|---------|---------|----------------|--------|
| **Spectrum Coverage** | 60% | **80%** | 100% |
| **Complexity Types** | 3-4 | **4-6** | 8 |
| **Authenticity Feel** | Very High | **High** | Medium |
| **Score Flexibility** | ±40% | **±20%** | ±10% |
| **Natural Variation** | Maximum | **Good** | Limited |
| **Over-engineering Risk** | Low | **Low** | High |
| **Production Ready** | Yes | **✅ YES** | Research |

---

## How to Set Mode

### In Script
```python
from unwritten.training.config import initialize_enhanced_config

# Balanced (default)
config = initialize_enhanced_config({
    'generation_mode': 'balanced'
})

# Strict
config = initialize_enhanced_config({
    'generation_mode': 'strict'
})

# Organic
config = initialize_enhanced_config({
    'generation_mode': 'organic'
})
```

### Mode Effects

Each mode automatically adjusts:
- Complexity type requirements
- Spectrum tolerances
- Score targeting flexibility
- Coverage tracking behavior
- Validation strictness
- Prompt constraint style

See `config.get_mode_adjustments()` in `config.py`

---

## Recommendation by Use Case

| Use Case | Mode | Rationale |
|----------|------|-----------|
| **Production training** | **Balanced** ⭐ | Best quality-coverage balance |
| **Novel generation** | Organic | Maximum authenticity |
| **Edge case testing** | Strict | Comprehensive coverage |
| **Research** | Strict | Algorithmic validation |
| **Creative scenarios** | Organic | Natural variation |
| **Default choice** | **Balanced** ⭐ | Safe for most uses |

---

## Key Differences Explained

### Complexity Types

- **Organic:** Natural emergence only (3-4 types)
- **Balanced:** Suggested + natural (4-6 types)  
- **Strict:** All mandated (8 types)

### Score Targeting

- **Organic:** Describe behavior, let score emerge naturally
- **Balanced:** Suggest score bands (e.g., "low authenticity 0.2-0.4")
- **Strict:** Target exact scores (e.g., "score = 0.35")

### Validation

- **Organic:** Minimal validation, trust generation
- **Balanced:** 25% AI + 100% rule-based
- **Strict:** Comprehensive AI + strict rule-based

### Prompts

- **Organic:** "Generate character struggling with boundaries"
- **Balanced:** "Generate low authenticity example (0.2-0.4 range)"
- **Strict:** "Generate authenticity score 0.35 with people-pleasing"

---

## Monitoring Your Choice

### Signs Mode Is Right

**Balanced:**
- ✅ Examples feel natural
- ✅ Good variety without repetition
- ✅ 70-90% spectrum coverage achieved
- ✅ No obvious patterns or formulas

**Organic:**
- ✅ Very authentic feeling
- ✅ Creative unexpected scenarios
- ✅ No mechanical patterns
- ⚠️ Some coverage gaps OK

**Strict:**
- ✅ Complete parameter coverage
- ✅ All requirements met
- ⚠️ May feel systematic
- ⚠️ Some examples formulaic

### Signs to Switch Modes

**Switch to Organic if:**
- Data feels too mechanical
- Patterns are obvious
- Responses feel calculated
- Need more authenticity

**Switch to Strict if:**
- Coverage gaps are problem
- Need all edge cases
- Research requires completeness
- Testing algorithms

**Switch to Balanced if:**
- Need better coverage than organic
- Need more authenticity than strict
- Want safe default
- Production use

---

## Default Recommendation

```python
# Just use this for production:
config = initialize_enhanced_config()
# Defaults to balanced mode
```

**Balanced mode** addresses over-engineering concerns while maintaining systematic benefits. It's the sweet spot for production training data.

---

See `docs/ADDRESSING-OVER-ENGINEERING-CONCERNS.md` for detailed rationale and mitigation strategies.

