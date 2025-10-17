# Ollama max_tokens Bug & Workaround

**Date:** October 14, 2025  
**Severity:** HIGH - Causes empty responses  
**Status:** WORKAROUND FOUND  

---

## Bug Description

When Ollama hits the `max_tokens` limit during generation, it returns an **empty `response` field** instead of the partial output or an error.

### Symptoms

```json
{
  "model": "qwen3:8b",
  "created_at": "2025-10-14T...",
  "response": "",  // ← EMPTY despite generating tokens
  "done": true,
  "done_reason": "length",  // ← Hit token limit
  "eval_count": 500,  // ← Generated 500 tokens
  "context": [...]  // ← Context shows tokens were generated
}
```

**What happens:**
1. Model generates tokens up to `max_tokens` limit
2. Generation stops at limit (`done_reason: "length"`)
3. **Ollama discards all generated tokens**
4. Returns empty string instead of partial output

### Impact

- **Empty responses** despite successful generation
- **Wasted computation** (tokens generated but discarded)
- **Pipeline failures** (can't parse empty responses)
- **Debugging confusion** (no error message, just empty)

---

## Root Cause Analysis

### Timeline

1. **Initial Issue:** Step 1 worked, Step 2 returned empty
2. **Hypothesis:** Context accumulation, prompt format, model limitations
3. **Investigation:** Added debug logging to see Ollama responses
4. **Discovery:** `'done_reason': 'length', 'eval_count': 500, 'response_length': 0`
5. **Conclusion:** Ollama bug when hitting `max_tokens` limit

### Evidence

```
[INFO] Sending to qwen3:8b - {'max_tokens': 500}
[WARNING] Empty response - {'done': True, 'done_reason': 'length', 'eval_count': 500}
[PERF] Qwen3 generation - {'response_length': 0}

→ Generated 500 tokens, hit limit, returned EMPTY
```

When `max_tokens` increased to 4000:
```
[INFO] Sending to qwen3:8b - {'max_tokens': 4000}
[PERF] Qwen3 generation - {'response_length': 332}
[INFO] Successfully parsed

→ Generated 332 tokens, completed naturally, returned OUTPUT
```

---

## Workaround

### Solution: High max_tokens

**Always set `max_tokens` much higher than expected output.**

```python
# ❌ BAD - Likely to hit limit
response = generate_with_qwen3(
    prompt=prompt,
    max_tokens=500  # Risky - may trigger bug
)

# ✅ GOOD - Safe buffer
response = generate_with_qwen3(
    prompt=prompt,
    max_tokens=3000  # High enough to complete naturally
)
```

### Rationale

1. **Only charged for actual tokens generated** - no cost penalty for high limit
2. **Model completes naturally** - stops when done, not at arbitrary limit
3. **Avoids Ollama bug** - never hits limit, never returns empty
4. **Better output quality** - model can complete thoughts fully

### Recommended Values

| Use Case | max_tokens | Rationale |
|----------|------------|-----------|
| **Short JSON** (< 100 tokens) | 1000-2000 | 10-20x buffer |
| **Medium JSON** (100-300 tokens) | 3000-4000 | 10-15x buffer |
| **Long dialogue** (500-1000 tokens) | 4000-8000 | 4-8x buffer |
| **Complex generation** | 8000-16000 | Large buffer for creativity |

### Implementation

```python
# Multi-step pipeline
STEP_1_MAX_TOKENS = 3000  # NPC primitives (~250 tokens)
STEP_2_MAX_TOKENS = 4000  # Situational context (~350 tokens)
STEP_3_MAX_TOKENS = 3000  # Tension/subtext (~250 tokens)
STEP_4_MAX_TOKENS = 4000  # Dialogue (~700 tokens)

# Rule of thumb: 10x expected output
expected_tokens = estimate_output_length(prompt)
max_tokens = expected_tokens * 10
```

---

## Testing

### Verify Workaround

```python
# Test with various max_tokens values
for max_t in [500, 1000, 2000, 4000]:
    response = generate_with_qwen3(
        prompt="Generate JSON with 5 fields",
        max_tokens=max_t
    )
    
    if not response:
        print(f"❌ Empty at max_tokens={max_t}")
    else:
        print(f"✅ Success at max_tokens={max_t}, length={len(response)}")
```

**Expected Results:**
- `max_tokens=500`: May return empty (bug triggered)
- `max_tokens=4000`: Always returns output (bug avoided)

### Monitor in Production

```python
# Log done_reason to detect bug
if response_data.get("done_reason") == "length":
    AppLogger.warning(
        "Hit max_tokens limit - increase to avoid Ollama bug",
        data={
            "eval_count": response_data.get("eval_count"),
            "max_tokens": max_tokens,
        }
    )
```

---

## Alternative Solutions (Future)

### 1. Ollama Fix

Report to Ollama maintainers:
- Bug: Empty response when `done_reason == "length"`
- Expected: Return partial output or clear error
- Impact: Breaks generation pipelines

### 2. Streaming Mode

```python
# Use streaming to get partial output
response = requests.post(
    ollama_url,
    json={
        "model": model,
        "prompt": prompt,
        "stream": True  # Get tokens as they're generated
    },
    stream=True
)

# Collect tokens until done
tokens = []
for line in response.iter_lines():
    chunk = json.loads(line)
    tokens.append(chunk.get("response", ""))
    if chunk.get("done"):
        break

result = "".join(tokens)
```

**Pro:** Always get partial output  
**Con:** More complex, slower

### 3. Fallback Logic

```python
# Detect empty response and retry with higher max_tokens
response = generate_with_qwen3(prompt, max_tokens=1000)

if not response:
    AppLogger.warning("Empty response, retrying with higher max_tokens")
    response = generate_with_qwen3(prompt, max_tokens=4000)
```

**Pro:** Automatic recovery  
**Con:** Wasted retry time

---

## Best Practices

### DO ✅

1. **Set max_tokens 10x expected output**
2. **Monitor `done_reason` in logs**
3. **Use high values for complex generation** (8000-16000)
4. **Test with various prompt lengths**
5. **Document max_tokens choices**

### DON'T ❌

1. **Don't use low max_tokens** (<1000) unless certain of output length
2. **Don't assume empty = model failure** - may be Ollama bug
3. **Don't retry without increasing max_tokens**
4. **Don't optimize max_tokens prematurely** - only charged for actual use

---

## Impact on Unwritten Pipeline

### Before Workaround
- ❌ Steps 2-5 consistently returned empty
- ❌ 0% success rate for multi-step pipeline
- ❌ Debugging took 2+ hours

### After Workaround
- ✅ All steps working reliably
- ✅ 100% success rate
- ✅ 1.5-2 min per complete interaction

### Changes Made

```python
# config.py
max_tokens: int = 4000  # Increased from 1000

# multi_step_pipeline.py
Step 1: max_tokens=3000  # Was 1000
Step 2: max_tokens=4000  # Was 800
Step 3: max_tokens=3000  # Was 1000
Step 4: max_tokens=4000  # Was 1500
```

---

## References

- **Issue:** Ollama returns empty response when hitting max_tokens limit
- **Workaround:** Set max_tokens 10x expected output
- **Status:** Working reliably with high max_tokens
- **Version:** Ollama (unknown), Model: qwen3:8b

---

**Created:** October 14, 2025  
**Author:** Unwritten Training Pipeline Team  
**Status:** RESOLVED (workaround implemented)

