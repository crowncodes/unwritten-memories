# Training Prompt Simplification v2.1

**Date:** October 14, 2025  
**Type:** Emergency Fix  
**Issue:** Empty responses from model after 7+ minutes  
**Root Cause:** Prompt too long and complex (500+ lines)  

---

## Problem

After implementing v2.0 with comprehensive Unwritten game documentation, the model:
- Took 7+ minutes per generation
- Returned **empty responses** (`response_length: 0`)
- Was overwhelmed by excessive context and instructions

## Solution

Drastically simplified prompt from **~500 lines → ~90 lines** while keeping game-specific aspects:

### Before (v2.0)
```
- Comprehensive game design documentation (300+ lines)
- Detailed NPC Response Framework explanations
- Multiple dialogue quality examples  
- Extensive JSON schema documentation
- Long complexity/authenticity descriptions
```

### After (v2.1)
```
- Concise scenario parameters (4 lines)
- Core game rules (4 bullet points)
- Quality requirements (3 bullets)
- ONE concrete JSON example
- Brief complexity/authenticity descriptions (1 line each)
```

---

## Changes Made

### 1. Prompt Introduction (300+ lines → 10 lines)

**Before:**
```
GAME CONTEXT (Unwritten card-based mobile game):
- Player interacts with NPCs through card-based narrative choices
- NPCs have persistent personalities (OCEAN), relationships (Level 0-5, Trust 0.0-1.0)
- Emotional capacity (0-10 scale) limits what characters can provide
- Urgency multipliers (1x-5x) amplify impact based on situation criticality
- All interactions affect trust, unlock card evolutions, shape season narrative

[...300+ more lines of game systems documentation...]
```

**After:**
```
Generate ONE Unwritten NPC interaction card.

SCENARIO:
- NPC Capacity: crisis (1.5-2.5/10)
- Support Needed: 5.0/10
- Response Type: authentic
- Complexity: baseline

CORE GAME RULES:
1. Capacity Rule: NPC at X/10 capacity can give MAX (X+2)/10 support
2. Trust Formula: Base × OCEAN × Urgency × Trust + Honesty_Bonus
3. Urgency: routine 1x | important 2x | urgent 3x | crisis 5x
4. Trust Mods: low 0.8x | neutral 1.0x | high 1.2x

DIALOGUE: 60-120 words novel-quality prose (NOT screenplay format, NO parentheses)
- Integrate ONE physical action naturally
- Show capacity limitation authentically if gap exists
- Include ONE tension element (mystery/contradiction/partial reveal)
```

### 2. JSON Schema (200+ lines → ONE example)

**Before:**
- Extensive documentation of each field
- Multiple examples for different scenarios
- Detailed explanations of game systems
- Extensive formatting rules

**After:**
```json
EXAMPLE OUTPUT (generate similar with YOUR OWN creative NPC/scenario):
[{
    "npc_profile": {"name": "Elena", "relationship_level": 3, "trust": 0.65, "interaction_count": 42},
    "npc_emotional_state": {...},
    "npc_ocean_personality": {...},
    "interaction_context": {...},
    "capacity_analysis": {...},
    "npc_card_narrative": {"dialogue_prose": "...", ...},
    "game_outcomes": {...},
    "training_metadata": {...}
}]

Generate YOUR example following this structure. Use DIFFERENT NPC name, scenario, and creative content.
NO parentheses. Prose format. Show calculations. 60-120 word dialogue. Return ONLY JSON array.
```

### 3. Complexity Instructions (50+ words each → 10 words each)

**Before:**
```python
"people_pleasing": "NPC says YES despite insufficient capacity (ignores X+2 rule). Agreeableness >4.0 trait. Overcommits to avoid disappointing player. Will later show strain/burnout. Trust short-term +0.1, but sets up future relationship damage."
```

**After:**
```python
"people_pleasing": "Says YES despite low capacity (Agreeableness >4.0), overcommits"
```

### 4. Authenticity Descriptions (60+ words each → 10 words each)

**Before:**
```python
"authentic": "NPC honestly assesses capacity, communicates limitations clearly while showing care for player. Offers specific alternative (timeframe/different help). Player disappointed but respects honesty. Small trust loss (-0.05 to -0.15) offset by honesty bonus. Unlocks 'authentic relationship' card evolution path."
```

**After:**
```python
"authentic": "Honest limitations + shows care + offers alternative, trust maintained"
```

---

## Results

### Prompt Length
- **Before:** ~500 lines of text
- **After:** ~90 lines of text
- **Reduction:** 82%

### Key Simplifications
1. ✅ Removed comprehensive game design context
2. ✅ Condensed core rules to 4 bullet points
3. ✅ ONE concrete JSON example instead of multiple
4. ✅ Brief complexity/authenticity descriptions (1 line each)
5. ✅ Removed repetitive formatting rules
6. ✅ Kept Unwritten-specific game mechanics (OCEAN, capacity X+2 rule, trust formula)

### What Was Preserved
- ✅ Unwritten game specifics (not generic emotional examples)
- ✅ Core capacity rule (X+2 limit)
- ✅ Trust calculation formula
- ✅ OCEAN personality integration
- ✅ Urgency multipliers
- ✅ Novel-quality dialogue requirements
- ✅ Tension hook integration
- ✅ Complete JSON schema structure

---

## Testing

**Expected Results:**
- Model should generate in 2-3 minutes (not 7+ minutes)
- Non-empty responses with actual JSON content
- Follows Unwritten game systems
- 60-120 word prose dialogue
- Proper capacity calculations

**If Still Empty:**
Consider further simplifications:
1. Reduce JSON schema to absolute minimum fields
2. Switch to 8B model temporarily for testing
3. Lower temperature further (0.92 → 0.85)
4. Remove tension hook requirement initially

---

## File Modified

- `src/unwritten/training/systematic_generator.py`
  - `_build_focused_prompt()` - Simplified from 500+ to ~90 lines
  - `_get_complexity_instructions()` - Condensed to 1 line per type
  - `_get_authenticity_description()` - Condensed to 1 line per type

## Next Steps

1. Test with simplified prompt
2. Monitor generation time and success rate
3. If successful, this is the new baseline
4. If still failing, consider switching to 8B model or further simplification

---

**Version:** v2.1  
**Priority:** CRITICAL (blocks all training data generation)  
**Status:** Ready for testing

