# Training Data Quality Upgrade - Novel-Quality Dialogue

**Date**: October 14, 2025  
**Purpose**: Upgrade training data from flat/bland responses to novel-quality, emotionally authentic dialogue matching gameplay spec standards  
**Compliance**: master_truths_canonical_spec_v_1_2.md Sections 16 & 17

---

## Problem Identified

### Current State (FLAT/BLAND ❌)
```json
{
  "character_response": "I can't help right now, I'm overwhelmed.",
  "internal_thought": "Character feels bad",
  "authenticity_score": 0.85
}
```

**Issues:**
- ❌ One-line dialogue with no depth
- ❌ No behavioral cues or physical details
- ❌ Missing OCEAN personality influence
- ❌ No numerical grounding (trust calculation)
- ❌ Doesn't match rich examples in `71-daily-turn-flow-detailed.md`

### Target State (NOVEL-QUALITY ✅)

From `71-daily-turn-flow-detailed.md`:
```
Sarah reaches across the table, takes your hand. Her grip is warm 
but her smile is tired.

"I can see you're really hurting," she says softly. "And I want to 
be here for you. I really do."

She pauses, looking down at her coffee. "But I need to be honest 
with you. I'm... I'm not in a good place myself right now. Work is 
crushing me, I haven't slept in two days, and I'm barely keeping 
my own head above water."

"I've got an hour before I need to get back," she continues, 
meeting your eyes again. "I can listen. I can be here. But I 
can't... I can't give you the hours of processing you need right 
now. I'm sorry. I wish I could."

She squeezes your hand. "You deserve someone who can show up 
fully. That's just not me today. Is that okay?"
```

**Features:**
- ✅ Multi-paragraph rich dialogue (185 words)
- ✅ Behavioral cues (reaches, warm grip, tired smile, looking down, squeezes hand)
- ✅ Physical details and setting
- ✅ Emotional subtext (guilt, exhaustion, care)
- ✅ Realistic pauses and hesitations
- ✅ Authentic vulnerability

---

## Changes Made

### 1. New Schema Definition

**File**: `docs/TRAINING-DATA-SCHEMA-V1.2.md`

**New Required Fields:**
```json
{
  "character_state": {
    "base_capacity": 8.0,
    "capacity_factors": [{"factor": "work_stress", "impact": -2.0}],
    "effective_capacity": 4.5,
    "capacity_tier": "LOW",
    "can_support_up_to": 6.5
  },
  "ocean_personality": {
    "openness": 0.75,
    "agreeableness": 0.80,
    "neuroticism": 0.45
  },
  "capacity_analysis": {
    "can_character_support": false,
    "capacity_gap": 0.5,
    "reasoning": "Capacity 4.5 + 2 = 6.5 max. Needs 7.0. GAP.",
    "recognizes_limitation": true
  },
  "response_classification": {
    "response_type": "authentic_limitation",
    "personality_driver": "High agreeableness + openness = wants to help but recognizes can't"
  },
  "character_response": {
    "setting": "Coffee shop, afternoon. Hands shake slightly.",
    "dialogue_parts": [
      "Opening: 'Sarah reaches across table, takes hand'",
      "Acknowledgment: 'I can see you're hurting'",
      "Limitation: 'But I'm not in a good place myself'",
      "Offering: 'I've got an hour. I can listen.'",
      "Validation: 'You deserve someone who can show up fully'"
    ],
    "behavioral_cues": ["reaches across", "tired smile", "looks down"],
    "internal_monologue": "Guilt + exhaustion + care conflict",
    "word_count": 185
  },
  "outcomes": {
    "relationship_trust_change": -0.05,
    "trust_calculation": {
      "formula": "base -0.15 + openness +0.08 + honesty +0.02 = -0.05",
      "tier": "VERY MINOR HARM (-0.1 to 0.0)",
      "narrative": "Disappointed but understands",
      "validation": "Number matches tone"
    }
  },
  "quality_metrics": {
    "emotional_authenticity": 0.85,
    "dialogue_quality": 0.80,
    "behavioral_cues": 0.90,
    "overall_quality": 0.82
  }
}
```

### 2. Enhanced Prompts

**File**: `src/unwritten/training/systematic_generator.py`

**Changes:**
- ✅ Increased `max_tokens` from 1500 → 3500 (individual) and 800 → 2000 per example (batch)
- ✅ Added novel-quality requirements to prompts
- ✅ Emphasized "SHOW don't tell" (behavioral cues, not flat statements)
- ✅ Required 150-200 word rich dialogue
- ✅ Added example of BAD vs GOOD dialogue in prompt
- ✅ Required complete capacity analysis and numerical grounding
- ✅ Requested OCEAN personality influence explanation

**Prompt Improvements:**
```
NOVEL-QUALITY REQUIREMENTS:
✓ Multi-paragraph dialogue with behavioral cues
✓ Physical details (body language, setting, actions)
✓ Emotional subtext (what's not being said)
✓ Realistic pauses and hesitations
✓ Vulnerability and authenticity

BAD (flat): "I can't help right now."
GOOD (rich): "She reaches for your hand. 'I want to help,' she says, 
and you can tell she means it. 'But I'm barely keeping it together 
myself.' Her voice cracks slightly."
```

### 3. Batch Processing Adjustments

**Changes:**
- Reduced batch size from 5 → 2 examples per API call (8B model stability)
- Updated batch prompt to request rich dialogue
- Increased max_tokens per batch
- Added note: May need to disable batch processing if JSON parsing issues persist

---

## Expected Output Quality

### Before ❌
```json
{
  "character_response": "I can't help right now.",
  "authenticity_score": 0.85
}
```

**Problems:**
- Flat, one-line response
- No behavioral cues
- No context or setting
- Missing capacity analysis
- No trust calculation

### After ✅
```json
{
  "character_state": {
    "base_capacity": 8.0,
    "capacity_factors": [
      {"factor": "work_stress", "impact": -2.0, "description": "Major project deadline tomorrow"},
      {"factor": "sleep_deprivation", "impact": -1.5, "description": "Only 4h sleep"}
    ],
    "effective_capacity": 4.5,
    "capacity_tier": "LOW"
  },
  "ocean_personality": {"openness": 0.75, "agreeableness": 0.80},
  "capacity_analysis": {
    "can_character_support": false,
    "capacity_gap": 0.5,
    "reasoning": "Capacity 4.5 + 2 = 6.5 max support. Friend needs 7.0."
  },
  "response_type": "authentic_limitation",
  "character_response": {
    "setting": "Coffee shop, afternoon. Character's hands shake slightly.",
    "dialogue": "Sarah reaches across the table, takes your hand. 'I can see you're really hurting,' she says softly. 'But I need to be honest—I'm not in a good place myself. Work is crushing me, I haven't slept in two days.' She pauses, looking down. 'I've got an hour. I can listen. But I can't give you the hours you need right now. I'm sorry.' She squeezes your hand. 'You deserve someone who can show up fully. That's just not me today.'",
    "behavioral_cues": ["reaches across table", "speaks softly", "tired smile", "looks down", "squeezes hand"],
    "internal_monologue": "Sarah feels guilty wanting to help but knowing she can't. Chest tightens. But pushing past limits helps no one.",
    "word_count": 118
  },
  "outcomes": {
    "relationship_trust_change": -0.05,
    "trust_calculation": {
      "formula": "-0.15 (need unmet) + 0.08 (openness appreciates honesty) + 0.02 (authentic boundary) = -0.05",
      "tier": "VERY MINOR HARM",
      "narrative": "Disappointed but understands honesty",
      "validation": "Number matches tone - minor disappointment, respects boundary"
    }
  },
  "quality_metrics": {
    "emotional_authenticity": 0.85,
    "dialogue_quality": 0.80,
    "behavioral_cues": 0.90,
    "overall_quality": 0.82
  },
  "demonstrates": [
    "Capacity + 2 rule enforced",
    "Behavioral cues show exhaustion",
    "OCEAN personality drives response type",
    "Rich multi-paragraph dialogue",
    "Numerical grounding with validation"
  ]
}
```

---

## Testing & Validation

### Run Generation
```bash
python scripts/run_training_pipeline.py
```

### Check Output Quality

**File Location**: `training_output_v1.2_systematic/emotional_authenticity_systematic_batch####_*.json`

**Quality Checklist:**
- [ ] Dialogue is 150-200+ words (not one-liners)
- [ ] Includes behavioral cues (physical actions, body language)
- [ ] Setting/context provided
- [ ] OCEAN personality influences response
- [ ] Capacity analysis with formula
- [ ] Trust calculation with formula + qualitative anchor
- [ ] Response type classified (authentic_limitation, overextension_burnout, etc.)
- [ ] Overall quality score ≥ 0.7

### If Output Still Flat

**Troubleshooting Options:**

1. **Switch to qwen3:30b** (slower but higher quality)
   - Edit `src/unwritten/training/config.py`
   - Change `model_primary: "qwen3:8b"` → `"qwen3:30b-a3b"`
   - Increase timeout if needed

2. **Disable Batch Processing** (individual generation more reliable)
   - Edit `scripts/run_training_pipeline.py`
   - Change `use_batch_processing=True` → `False`

3. **Add Few-Shot Examples** to prompts
   - Include 1-2 complete rich examples in prompt as reference

4. **Temperature Adjustment**
   - Try `temperature=0.9` for more creative responses

---

## Compliance Verification

### Master Truths v1.2 Section 16 (Emotional Authenticity)
- [x] Capacity constraints (0-10 scale)
- [x] Capacity + 2 rule enforced
- [x] Factors affecting capacity tracked
- [x] Response types classified (8 types)
- [x] Authentic limitation responses

### Master Truths v1.2 Section 17 (Novel-Quality Narratives)
- [x] Rich dialogue (150-200+ words)
- [x] Behavioral cues (shows, not tells)
- [x] OCEAN personality influences
- [x] Numerical grounding (formula + anchor + validation)
- [x] Quality metrics (≥ 0.7 threshold)

### Schema Completeness (`TRAINING-DATA-SCHEMA-V1.2.md`)
- [x] character_state with capacity analysis
- [x] ocean_personality (5 traits)
- [x] situation with urgency
- [x] capacity_analysis with gap calculation
- [x] response_classification with personality driver
- [x] character_response with rich dialogue array
- [x] outcomes with trust calculation
- [x] quality_metrics with validation

---

## Next Steps

1. **Run Generation**: `python scripts/run_training_pipeline.py`
2. **Inspect Output**: Check first few examples in `training_output_v1.2_systematic/`
3. **Verify Quality**:
   - Dialogue is multi-paragraph and rich
   - Behavioral cues present
   - Trust calculations include formulas
   - Overall quality ≥ 0.7
4. **Adjust if Needed**:
   - Switch to 30B model if output still flat
   - Disable batching if JSON parsing fails
   - Add few-shot examples if quality insufficient

---

## Success Criteria

✅ **Training data matches `71-daily-turn-flow-detailed.md` quality**  
✅ **Rich, multi-paragraph dialogue with vulnerability**  
✅ **Behavioral cues show exhaustion (not just tell)**  
✅ **OCEAN personality drives response types**  
✅ **Numerical grounding with formulas and validation**  
✅ **Overall quality score ≥ 0.7 consistently**

---

**Document Version**: 1.0  
**Last Updated**: October 14, 2025  
**Cross-References**:
- `docs/TRAINING-DATA-SCHEMA-V1.2.md` - Complete schema definition
- `docs/71-daily-turn-flow-detailed.md` - Target dialogue quality examples
- `docs/master_truths_canonical_spec_v_1_2.md` - Sections 16 & 17
- `src/unwritten/training/systematic_generator.py` - Updated prompts

