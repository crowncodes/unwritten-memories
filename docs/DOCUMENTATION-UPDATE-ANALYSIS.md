# Documentation Update Analysis

**Date**: October 14, 2025  
**Purpose**: Identify documentation updates needed to align with recent training pipeline changes  
**Context**: Systematic generation, novel-quality dialogue, enhanced schema implementation

---

## Executive Summary

After implementing systematic training data generation with novel-quality dialogue requirements, several documentation files need updates to:
1. **Reflect actual implementation** (Python, not JavaScript examples)
2. **Reference correct file names** (systematic_generator.py, not deleted files)
3. **Include new schema fields** (enhanced v1.2 schema with novel-quality requirements)
4. **Align with numerical grounding** (explicit calculations, qualitative anchors)
5. **Document the systematic approach** (parameter coverage, authenticity spectrum)

---

## Files Requiring Updates

### 1. `docs/3.ai/37-training-data-quality-standards.md`

**Status**: ⚠️ **NEEDS UPDATES**

**Issues Identified**:

1. **Incorrect File References** (Line 549)
   ```markdown
   Current: "Implementation:** See `src/unwritten/training/multi_step_generator.py`"
   Problem: multi_step_generator.py was deleted
   Fix: Update to "src/unwritten/training/multi_step_systematic.py"
   ```

2. **Missing Novel-Quality Dialogue Requirements**
   - Document doesn't mention 150-200 word dialogue requirement
   - No reference to behavioral cues ("Show don't tell")
   - Missing OCEAN personality influence on communication style
   - No mention of "novel-quality" vs "flat game dialogue" distinction

3. **Missing Systematic Coverage Approach**
   - Doesn't explain the systematic parameter buckets
   - No mention of coverage tracking database
   - Missing batch processing optimization details

4. **Schema Mismatch**
   - Examples show older schema without new fields:
     - `ocean_influence` (how personality shapes response)
     - `behavioral_cues` (physical actions, not told emotions)
     - `trust_calculation` (explicit formula + validation)
     - `dialogue_richness` (word count, sensory details, specificity)

**Recommended Changes**:

```markdown
## Add New Section (After Line 95):

### Quality Gate 5: Novel-Quality Dialogue Requirements

**Problem Identified (2025-10-14):**
Initial training data had flat, game-like dialogue ("I can't help right now.") 
instead of rich, novel-quality narrative.

**Solution:** Enforce 150-200 word responses with behavioral depth.

**Requirements:**
- [ ] Dialogue is 150-200 words (not one-liners)
- [ ] Includes physical behavioral cues (fidgeting, eye contact, voice tone)
- [ ] Shows OCEAN personality influence on communication style
- [ ] Uses sensory details and specific objects/places
- [ ] "Shows" emotion through action, doesn't "tell"

**Example Comparison:**

❌ FLAT (Old approach):
"I can't help right now. I'm overwhelmed."

✅ NOVEL-QUALITY (New approach):
"She reaches across the table, takes your hand. 'I can see you're really 
hurting,' she says softly. 'But I need to be honest—I'm not in a good place 
myself right now. Work is crushing me, I haven't slept in two days.' She 
pauses, looking down at her coffee. Her hands are shaking slightly. 'I've 
got maybe an hour. I can listen. But I can't give you the full emotional 
support you need right now. I wish I could. I really do.'"

**Why This Matters:**
- Creates page-turner experience (not just game mechanics)
- Makes characters feel real and memorable
- Teaches model authentic human limitation patterns
- Elevates quality from "game dialogue" to "literary fiction"
```

```markdown
## Update Section 496-551 (Multi-Step Generation):

Replace references to `multi_step_generator.py` with:

**Current Implementation:** `src/unwritten/training/multi_step_systematic.py`

This combines multi-step compositional generation with systematic parameter 
coverage, ensuring both quality (through multi-turn refinement) and 
completeness (through coverage tracking).

**Systematic Coverage Architecture:**

Instead of random generation, the pipeline ensures comprehensive coverage:

```python
# Capacity buckets (not random)
capacity_levels = [
    {"name": "crisis", "range": (0.5, 1.5), "frequency": 0.15},
    {"name": "low", "range": (2.0, 4.0), "frequency": 0.25},
    {"name": "medium", "range": (4.5, 6.5), "frequency": 0.35},
    {"name": "high", "range": (7.0, 9.5), "frequency": 0.25}
]

# Authenticity targets (ensures full spectrum)
authenticity_targets = [
    {"name": "failed", "range": (0.2, 0.4), "frequency": 0.15},
    {"name": "struggling", "range": (0.4, 0.6), "frequency": 0.20},
    {"name": "authentic", "range": (0.6, 0.8), "frequency": 0.35},
    {"name": "excellent", "range": (0.8, 1.0), "frequency": 0.30}
]

# Complexity types (ensures messy human realism)
complexity_types = [
    "baseline",
    "misjudgment_over",
    "misjudgment_under",
    "people_pleasing",
    "defensive_lashing",
    "emergency_override",
    "cultural_indirect",
    "mixed_emotions"
]
```

**Coverage Tracking:** SQLite database tracks which parameter combinations 
have been generated, automatically filling gaps to ensure complete coverage.
```

---

### 2. `docs/3.ai/36-local-model-training.md`

**Status**: ⚠️ **NEEDS CLARIFICATION**

**Issues Identified**:

1. **Scope Confusion**
   - This doc is about training the on-device TensorFlow Lite model (2-3MB)
   - Our current work is about generating training data using Qwen3
   - These are TWO DIFFERENT PROCESSES

2. **Misleading Examples**
   - Shows Claude 3.5 Sonnet for synthetic data generation
   - But we're actually using local Qwen3 via Ollama
   - Could confuse readers about the pipeline

**Recommended Changes**:

```markdown
## Add Clarification Section (After Line 162):

### ⚠️ Important Distinction: Two Training Processes

This document describes **Training Process #1**: Training the on-device 
TensorFlow Lite model that runs in the Flutter app (personality analysis, 
sentiment classification, etc.).

**Training Process #2** (Generating Training Data) is documented separately:
- See: `docs/TRAINING-DATA-SCHEMA-V1.2.md` for schema
- See: `docs/TRAINING-DATA-QUALITY-UPGRADE.md` for quality standards
- See: `src/unwritten/training/` for data generation pipeline

**The Flow:**
1. Generate training data using Qwen3 → (You are here in this pipeline)
2. Use generated data to train on-device model → (This document)
3. Deploy on-device model to Flutter app → (37-model-deployment-optimization.md)
```

```markdown
## Update Lines 330-388 (Emotional Authenticity Section):

Current implementation uses **Qwen3 (local) via Ollama**, not Claude 3.5 Sonnet.

See actual implementation:
- `src/unwritten/training/qwen3_generator.py` (base generator)
- `src/unwritten/training/systematic_generator.py` (systematic coverage)
- `src/unwritten/training/multi_step_systematic.py` (multi-step + systematic)

**Why Qwen3 instead of Claude:**
- Free (no API costs for 10K+ examples)
- Local (no data privacy concerns)
- Fast enough with systematic batching (2 examples per API call)
- 8B model handles focused prompts well
- 30B model available for validation when needed

**See:** `data/QUICKSTART_WINDOWS.md` for Ollama + Qwen3 setup
```

---

### 3. `docs/3.ai/35-consistency-coherence.md`

**Status**: ⚠️ **NEEDS ALIGNMENT**

**Issues Identified**:

1. **Language Mismatch**
   - All validation code examples are JavaScript
   - Our actual implementation is Python (`src/unwritten/training/validation.py`)
   - Could confuse developers

2. **Novel-Quality Validator Exists But Different**
   - Doc has `NovelQualityValidator` (lines 718-1146)
   - But our Python implementation may differ
   - Need to align

3. **Emotional Capacity Logic**
   - JavaScript version checks capacity constraints
   - Should align with systematic_generator.py capacity logic
   - Formula: "Character at X/10 capacity can provide UP TO (X+2)/10 support"

**Recommended Changes**:

```markdown
## Add Note at Top of Document (After Line 20):

### 📝 Implementation Note

**Code examples in this document use JavaScript for readability.**

For actual Python implementation, see:
- `src/unwritten/training/validation.py` (validation pipeline)
- `src/unwritten/training/systematic_generator.py` (capacity constraints)
- `src/unwritten/training/multi_step_systematic.py` (multi-turn refinement)

**The concepts and logic are identical**, only the language differs.
```

```markdown
## Update Lines 756-811 (Emotional Authenticity Check):

Align with actual capacity formula from systematic_generator.py:

```python
def check_emotional_authenticity(generated, context):
    """
    CRITICAL RULE: Character at X/10 capacity can provide UP TO (X+2)/10 
    level of emotional support.
    
    Examples:
    - Capacity 2.0/10 → Max support: 4.0/10 (buffer of +2)
    - Capacity 5.0/10 → Max support: 7.0/10 (buffer of +2)
    - Capacity 8.0/10 → Max support: 10.0/10 (capped at max)
    
    Buffer can vary (1-3) based on:
    - Personality (high agreeableness = larger buffer)
    - Relationship trust (high trust = willing to stretch)
    - Emergency context (life/death = override capacity)
    """
    capacity = context['character']['effective_capacity']
    support_needed = context['support_level_needed']
    
    # Calculate maximum supportable level
    buffer = calculate_buffer(context)  # 1-3 based on personality, trust, emergency
    max_support = min(10.0, capacity + buffer)
    
    if support_needed > max_support:
        return {
            'authentic': False,
            'issue': 'Character cannot provide this level of support',
            'capacity': capacity,
            'needed': support_needed,
            'max_possible': max_support,
            'suggestion': 'Show character trying but failing, or acknowledging limitations'
        }
```

**This aligns with:** `src/unwritten/training/systematic_generator.py` lines 263-310
```

---

### 4. `docs/3.ai/34-context-memory-systems.md`

**Status**: ✅ **MOSTLY GOOD** (Minor updates)

**Issues Identified**:

1. **New Field Added** (Line 61)
   - Document already includes `emotionalCapacity: 0-10 scale` ✅
   - This is correct and aligned

2. **Could Add Reference to Training Data Context**
   - Currently focused on game runtime context
   - Could clarify how context differs for training data generation

**Recommended Changes**:

```markdown
## Add Subsection (After Line 140):

### Context for Training Data Generation

**Different from Runtime Context:**

When generating training data (not game runtime), context focuses on:

```python
{
  "character_state": {
    "base_capacity": 6.0,  # Before stress factors
    "capacity_factors": [
      {"factor": "work_stress", "impact": -2.0},
      {"factor": "sleep_deprivation", "impact": -1.5}
    ],
    "effective_capacity": 2.5,  # After factors applied
    "can_support_up_to": 4.5  # effective_capacity + buffer
  },
  "situation": {
    "support_level_needed": 7.0,  # What the situation requires
    "urgency": 4.0,  # 1-5 scale (5 = life/death)
    "relationship_type": "close_friend"
  },
  "target_authenticity": {
    "range": (0.4, 0.6),  # Struggling response
    "demonstrates": "Character wants to help but capacity insufficient"
  }
}
```

**See:** `src/unwritten/training/systematic_generator.py` for complete context structure
```

---

### 5. `docs/3.ai/32-prompt-engineering-principles.md`

**Status**: ✅ **MOSTLY GOOD** (Minor enhancement)

**Issues Identified**:

1. **Novel-Quality Principle Not Explicit**
   - Covers specificity, constraints, OCEAN
   - But doesn't explicitly state "novel-quality vs game dialogue" distinction
   - Could add this as enhancement

**Recommended Changes**:

```markdown
## Add New Principle (After Principle 5):

### Principle 6: Novel-Quality Narrative (NEW - 2025-10-14)

**The Problem:**
Game dialogue is often flat and functional ("I can't help.") rather than 
immersive and emotionally engaging.

**The Solution:**
Write as if creating a literary fiction novel, not a video game script.

**Key Differences:**

| Game Dialogue | Novel-Quality Narrative |
|---------------|------------------------|
| "I'm stressed." | "Her hands won't stop shaking. She's gripping the coffee cup so hard her knuckles are white." |
| "I want to help but I can't." | "She reaches for your hand, then pulls back. 'God, I wish I could give you what you need right now. But I'm running on empty myself.'" |
| Functional, tells state | Immersive, shows state through behavior |
| 10-20 words | 150-200 words |
| One emotional note | Layered, complex emotions |

**The Three Novel-Quality Requirements:**

1. **Show, Don't Tell**
   ```markdown
   ❌ "She was nervous"
   ✅ "She fidgeted with her napkin, folding and refolding the corner"
   ```

2. **Behavioral Grounding**
   ```markdown
   ❌ "He felt overwhelmed"
   ✅ "He rubbed his temples, closed his eyes for a moment too long"
   ```

3. **Sensory & Specific Details**
   ```markdown
   ❌ "They met at a coffee shop"
   ✅ "The espresso machine hissed. She ordered her usual—americano, no 
        room for cream. You noticed her hands were stained with charcoal 
        from her morning drawing session."
   ```

**Why This Matters:**
- Creates "one more week" engagement (page-turner effect)
- Makes characters feel real, not like NPCs
- Elevates game from "mobile time-killer" to "emotional experience"
- Training data quality directly impacts model output quality

**Implementation:**
See `docs/TRAINING-DATA-SCHEMA-V1.2.md` for complete schema requirements
```

---

## Summary of Changes Needed

### High Priority (Implementation-Critical)

1. **37-training-data-quality-standards.md**
   - ✅ Fix deleted file references
   - ✅ Add novel-quality dialogue section
   - ✅ Add systematic coverage explanation
   - ✅ Update schema examples

2. **36-local-model-training.md**
   - ✅ Add scope clarification (two different training processes)
   - ✅ Update Claude → Qwen3 references

### Medium Priority (Developer Clarity)

3. **35-consistency-coherence.md**
   - ✅ Add JavaScript/Python note
   - ✅ Align capacity formula with Python implementation

4. **34-context-memory-systems.md**
   - ⚠️ Add training data context section

### Low Priority (Enhancement)

5. **32-prompt-engineering-principles.md**
   - ⚠️ Add Principle 6 (novel-quality narrative)

---

## Validation Checklist

After updates, verify:
- [ ] All file paths reference existing files
- [ ] Schema examples match `TRAINING-DATA-SCHEMA-V1.2.md`
- [ ] Capacity formulas consistent across all docs
- [ ] Python/JavaScript distinction clear
- [ ] Numerical grounding approach documented
- [ ] Systematic coverage approach explained
- [ ] Novel-quality requirements defined

---

## Next Steps

1. **Review this analysis** with team
2. **Prioritize changes** (high → medium → low)
3. **Update documents** systematically
4. **Cross-reference** to ensure consistency
5. **Update CHANGELOG** with documentation improvements

---

**Related Documents:**
- `docs/TRAINING-DATA-SCHEMA-V1.2.md` (new schema)
- `docs/TRAINING-DATA-QUALITY-UPGRADE.md` (quality improvements)
- `docs/master_truths_canonical_spec_v_1_2.md` (ground truth)
- `docs/NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md` (numerical standards)

