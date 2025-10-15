# Multi-Step Pipeline Issues

**Date:** October 14, 2025  
**Status:** ⚠️ BLOCKED - Systematic empty response issue  

---

## Problem Summary

The multi-step pipeline consistently fails at **Step 2** with empty responses from both `qwen3:8b` and `qwen3:30b` models.

### Observed Pattern

```
✅ Step 1 (NPC Primitives): ALWAYS works
   - Generates name (e.g., "Elena", "Aelara Tidecall")  
   - Returns valid JSON
   - Takes ~10-15 seconds

❌ Step 2 (Situational Context): ALWAYS fails
   - Empty response from model
   - Takes ~14-19 seconds (longer than step 1)
   - response_length: 0
   - No error from Ollama, just empty `"response": ""`
```

### Test Runs

**Run 1:** `qwen3:30b-a3b`
- Step 1: ✅ (40 sec, 0 length - empty)
- Result: FAILED

**Run 2:** `qwen3:8b`  
- Step 1: ✅ Generated "Aelara Tidecall" (24 sec)
- Step 2: ❌ Empty response (14 sec)
- Result: FAILED

**Run 3:** `qwen3:30b` (standard)
- Step 1: ❌ Empty response (40 sec)
- Result: FAILED

**Run 4-6:** `qwen3:8b` (simplified prompts)
- Step 1: ✅ Generated "Elena" (~10-15 sec)
- Step 2: ❌ Empty response (~14-19 sec)
- Result: FAILED (consistent pattern)

---

## Possible Causes

### 1. **Context Accumulation** (Most Likely)
- Ollama may be maintaining context from Step 1
- Accumulated context + Step 2 prompt exceeds some limit
- Model returns empty rather than error

**Test:** Clear Ollama context between steps or use separate sessions

### 2. **Prompt Format Issues**
- Step 2 prompt format confuses model
- JSON template with multiple numeric values problematic
- Model can't decide what to generate

**Test:** Further simplify Step 2 prompt, remove all f-string interpolation

### 3. **Model Limitations**
- Model can't handle multi-step generation reliably
- Works once, fails on subsequent calls in same session

**Test:** Restart Ollama between steps

### 4. **Temperature/Sampling Issues**
- temp 0.7-0.75 may be causing issues
- Model getting "stuck" in sampling

**Test:** Lower temperature to 0.5 or increase to 0.9

---

## Attempted Fixes

### ❌ Fix 1: Switch from 30B to 8B
- Result: Step 1 worked, Step 2 still empty

### ❌ Fix 2: Switch from a3b to standard 30B
- Result: Both steps failed (empty)

### ❌ Fix 3: Simplify prompts (remove bracket placeholders)
- Removed `[1.0/2.0/3.0/5.0]` notation
- Used concrete examples instead
- Result: Step 1 worked, Step 2 still empty

### ❌ Fix 4: Lower temperature, increase max_tokens
- temp: 0.75 → 0.7
- max_tokens: 600 → 800
- Result: Step 1 worked, Step 2 still empty

### ❌ Fix 5: Condense NPC traits in prompt
- Used `O=3.2 C=4.1` format instead of full dict
- Result: Step 1 worked, Step 2 still empty

---

## Comparison: Monolithic vs Multi-Step

### Monolithic Prompt (v2.0-v2.1)
- **Issue:** Too long, model returns empty or takes 7+ minutes
- **Success Rate:** ~40%
- **When it works:** Generates complete interaction in one call

### Multi-Step Prompt (v2.2)
- **Issue:** Step 2 consistently returns empty
- **Success Rate:** 0% (can't complete pipeline)
- **When it works:** Step 1 always works, but pipeline blocked at Step 2

---

## Recommendation

**The multi-step architecture is sound, but blocked by Ollama/model behavior.**

### Option A: Debug Ollama Context (RECOMMENDED)
1. Add explicit context clearing between steps
2. Test if Ollama has context parameter to reset
3. Or use separate Ollama sessions per step

### Option B: Revert to Monolithic with Fixes
1. Use the simplified prompt style from multi-step
2. Keep temperature at 0.7
3. Reduce overall prompt length to ~200 lines
4. Test if monolithic works better with these optimizations

### Option C: Hybrid Approach
1. Use multi-step for base scenario generation (when it works)
2. Fall back to monolithic if any step fails
3. Cache successful step outputs for reuse

### Option D: Investigate Ollama
1. Check Ollama logs for errors
2. Test if other models (llama3, mistral) have same issue
3. File Ollama bug report if systematic

---

## Next Steps

1. **PRIORITY:** Investigate why Step 2 returns empty
   - Check Ollama documentation for context handling
   - Test with minimal Step 2 prompt (just "Generate {}")
   - Monitor Ollama process memory/CPU during generation

2. **FALLBACK:** Return to monolithic with lessons learned
   - Use simpler prompt format from multi-step
   - Concrete examples, not bracket placeholders
   - Lower temperature (0.7)
   - Test reliability

3. **LONG-TERM:** Once Step 2 issue fixed
   - Complete multi-step pipeline testing
   - Benchmark speed vs monolithic
   - Implement variation generation

---

## Code Status

### Files Created
- ✅ `src/unwritten/training/multi_step_pipeline.py` (complete implementation)
- ✅ `scripts/test_multi_step_pipeline.py` (test suite)
- ✅ `MULTI_STEP_PIPELINE_V2.2.md` (documentation)

### Current State
- Pipeline architecture: ✅ Complete
- Step 1 (Primitives): ✅ Works reliably
- Step 2 (Context): ❌ BLOCKED (empty responses)
- Steps 3-5: ⏸️ Untested (blocked by Step 2)

### Can Be Used For
- ❌ Complete interaction generation (blocked)
- ✅ NPC primitive generation only (Step 1 works)
- ❌ Dialogue variations (requires Steps 1-4)

---

**Version:** v2.2  
**Status:** BLOCKED  
**Blocker:** Systematic empty responses at Step 2  
**Investigation Required:** YES

