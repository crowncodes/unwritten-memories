# Language-Agnostic Prompt Improvements v1.6.3

**Date:** 2025-10-14  
**Status:** ✅ Implemented  
**Version:** v1.6.3

## Problem Identified

The training prompt was **heavily biased** toward English/Western conventions:

### 🔴 Bias Sources Found

1. **English-specific examples**
   - "Coffee shop, late afternoon"
   - "Can we do lunch tomorrow?"
   - "Call Maya" (Western name)

2. **English idioms**
   - "running on fumes"
   - "head above water"
   - "half a tank left"

3. **Western cultural assumptions**
   - Direct communication style
   - Coffee culture
   - Specific meal timing patterns

4. **Gendered language**
   - "She stared at her phone..."
   - Fixed gender pronouns in examples

5. **Western interaction patterns**
   - Direct refusals
   - Explicit boundary-setting
   - Western social norms assumed universal

## Changes Implemented

### ✅ Removed All Cultural Markers

#### Before (Biased):
```
"She stared at her phone for a long moment before responding. 
'I care about you. You know I do. But I'm barely keeping my 
own head above water right now.' Her coffee sat untouched, 
going cold. 'Can we do lunch tomorrow? I'll actually be able 
to listen then, not just... exist in the same room.'"
```

#### After (Language-Agnostic):
```
[Character takes a moment to consider before responding. 
Expresses care while being honest about current limitations. 
One or two physical details integrated naturally. Shows 
internal conflict through word choice and pacing. Offers 
specific alternative or timeframe. Genuine emotion without 
exaggeration.]
```

### ✅ Made Examples Abstract

#### Before:
```
Example - Player declines to help:
• Routine context (1x): "No worries! Maybe next time."
• CRISIS context (5x): "Oh. I... I really needed you."
```

#### After:
```
Example - Player declines to help:
• Routine context (1x): [Casual response, minimal emotional weight]
• CRISIS context (5x): [Betrayed, hurt, strained response despite trying to hide it]
```

### ✅ Removed English Idioms

All English-specific phrases removed from examples:
- ❌ "running on fumes"
- ❌ "head above water"
- ❌ "half a tank left"
- ❌ "keeping my own head above water"

### ✅ Made Cultural References Generic

#### Tension Hooks - Before:
```
- Mystery hook: Mention something, don't explain ("David called again...")
- Partial reveal: Show effect without cause (phone rings, they go pale)
```

#### Tension Hooks - After:
```
- Mystery hook: Mention something, don't explain it yet
- Partial reveal: Show effect without explaining the cause
```

### ✅ Removed Gender Bias

#### Before:
```json
"dialogue": "She stared at her phone..."
```

#### After:
```json
"dialogue": "[60-120 words of natural prose dialogue...]"
```

### ✅ Removed Western-Specific Settings

#### Before:
```json
"setting": "Coffee shop, late afternoon",
"situation": "Friend dealing with breakup, needs to talk through feelings"
```

#### After:
```json
"setting": "[Contextually appropriate setting]",
"situation": "[Specific situation requiring support]"
```

### ✅ Made Complexity Instructions Universal

#### Before:
```
"defensive_lashing": "'Why is this MY problem?'"
"cultural_indirect": "'Maybe... we'll see... I'll try...'"
```

#### After:
```
"defensive_lashing": "Hostile or sharp response."
"cultural_indirect": "Uses indirect communication patterns to decline."
```

## Impact

### Expected Improvements

1. **Linguistic Diversity**
   - Model can generate dialogue in any communication style
   - Not biased toward Western direct communication
   - Supports indirect, contextual, and culturally-varied patterns

2. **Cultural Neutrality**
   - No assumptions about social norms
   - No English-specific metaphors or idioms
   - Universal emotional patterns, not culturally-specific expressions

3. **Gender Neutrality**
   - No gendered pronouns in examples
   - Model free to choose appropriate representation
   - No bias toward any gender presentation

4. **Setting Flexibility**
   - Can generate appropriate contexts for any culture
   - No Western locations or social patterns assumed
   - Universal emotional situations, not culture-specific

## Technical Changes

### Files Modified
- `src/unwritten/training/systematic_generator.py`
  - Line 318-325: Removed English dialogue examples
  - Line 349-364: Made quality spectrum abstract
  - Line 366-370: Removed Western names/scenarios from tension hooks
  - Line 373-443: Converted JSON example to template format
  - Line 451-463: Removed English phrases from complexity instructions

### Backward Compatibility
✅ Fully compatible - only changes prompt guidance, not data structure

## Testing Recommendations

Test that generated dialogue:
1. ✅ Uses diverse communication patterns (not just Western direct style)
2. ✅ Avoids English-specific idioms
3. ✅ Creates culturally-appropriate settings
4. ✅ Shows emotional authenticity without cultural assumptions
5. ✅ Maintains emotional weight across different communication styles

## Next Steps

1. **Generate new batch** with language-agnostic prompt
2. **Verify diversity** in:
   - Communication styles (direct vs indirect)
   - Emotional expression patterns
   - Setting variety
   - Absence of English idioms
3. **Compare quality** against previous batches

## Version History

- **v1.6.3**: Language-agnostic prompt (current)
- **v1.6.2**: Diversity tuning (temperature, tokens, sampling)
- **v1.6.1**: Timeout increases (4x)
- **v1.6**: Coverage fixes (authenticity, complexity)
- **v1.5**: NPC Response Framework integration
- **v1.4**: Sweet spot dialogue quality
- **v1.3**: Anti-melodrama rules

---

**Result:** Prompt is now **culturally neutral** and **linguistically agnostic**, allowing the model to generate authentic emotional dialogue without Western/English bias.


