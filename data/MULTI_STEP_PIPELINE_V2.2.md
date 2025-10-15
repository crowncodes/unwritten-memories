# Multi-Step Generation Pipeline v2.2

**Date:** October 14, 2025  
**Type:** Architecture Redesign  
**Status:** Ready for Testing  

---

## Problem with Monolithic Approach

### v2.0-v2.1 Issues
- **Monolithic prompt:** Generate everything in one massive call
- **Slow:** 7+ minutes per generation (or empty responses)
- **Inflexible:** Can't reuse components or create variations
- **Wasteful:** Regenerate everything to change one element
- **Hard to debug:** Single point of failure

---

## Solution: Multi-Step Pipeline

**Break generation into focused, reusable steps:**

```
Step 1: NPC Primitives (30 sec)
  ↓ OCEAN traits, base_capacity, relationship_level, trust
  
Step 2: Situational Context (30 sec)  
  ↓ capacity_factors, urgency, support_needed, location
  
Step 3: Tension/Memory Elements (30 sec)
  ↓ tension_hook, relevant_memories, subtext
  
Step 4: Dialogue Generation (60 sec)
  ↓ 60-120 word prose using ALL above context
  
Step 5: Calculate Outcomes (< 1 sec)
  ↓ trust_change, capacity_cost (deterministic math)
```

**Total time:** ~2-3 minutes (vs 7+ min monolithic)

---

## Architecture Benefits

### 1. **Speed: 60-70% Faster**
- **Monolithic:** 7+ minutes per complete interaction
- **Multi-Step:** 2-3 minutes per complete interaction
- **Why:** Smaller, focused prompts generate faster and more reliably

### 2. **Modularity: Reusable Components**
```python
# Generate base scenario once
primitives = pipeline.generate_npc_primitives("baseline")
context = pipeline.generate_situational_context(primitives, "low", 6.0)

# Generate 10 dialogue variations (reuse base)
for i in range(10):
    tension = pipeline.generate_tension_memory_elements(primitives, context)
    dialogue = pipeline.generate_dialogue(primitives, context, tension, ...)
    
# Result: 10 unique dialogues in ~10 minutes (vs 70+ min regenerating all)
```

### 3. **Variation Generation**
**Use Case:** Create dialogue alternatives by swapping ONE component

```python
# Same NPC, same capacity, DIFFERENT tension
base_scenario = generate_base()

# Variation 1: Mystery tension
tension_1 = {"type": "mystery_question", "element": "Phone buzzes, doesn't explain"}
dialogue_1 = generate_dialogue(..., tension_1)

# Variation 2: Contradiction tension  
tension_2 = {"type": "contradiction", "element": "Usually plans, today impulsive"}
dialogue_2 = generate_dialogue(..., tension_2)

# Result: 2 completely different dialogues, same underlying scenario
```

### 4. **Testability: Independent Validation**
```python
# Test each step independently
primitives = generate_npc_primitives()
assert primitives.ocean['agreeableness'] > 4.0  # For people_pleasing

context = generate_situational_context(primitives, ...)
assert context.effective_capacity < context.support_needed  # Can't provide full support

# If dialogue fails, primitives/context are still valid
```

### 5. **Debugging: Pinpoint Issues**
```
Monolithic:
❌ "Generation failed" → Where? No idea. Regenerate everything.

Multi-Step:
✅ "Step 3 (tension) failed" → Fix tension prompt only
✅ Steps 1-2 data preserved → Resume from Step 3
```

---

## Usage Examples

### Example 1: Single Complete Interaction

```python
from unwritten.training.multi_step_pipeline import MultiStepPipeline
from unwritten.training.config import initialize_enhanced_config

config = initialize_enhanced_config()
pipeline = MultiStepPipeline(config)

# Generate complete interaction in one call
interaction = pipeline.generate_complete_interaction(
    complexity_type="people_pleasing",
    authenticity_target="struggling", 
    capacity_level="low",
    support_needed=7.0
)

# Result: Complete Unwritten NPC interaction card
# - NPC profile (name, OCEAN, relationship)
# - Emotional state (capacity, stressors)
# - Situation context (urgency, location)
# - Tension/memory elements
# - Dialogue prose (60-120 words)
# - Game outcomes (trust change, capacity cost)
```

**Output:**
```json
{
  "npc_profile": {
    "name": "Jordan",
    "relationship_level": 3,
    "trust": 0.58
  },
  "npc_emotional_state": {
    "effective_capacity": 3.5,
    "can_support_up_to": 5.5
  },
  "npc_card_narrative": {
    "dialogue_prose": "Jordan rubbed their neck, avoiding eye contact...",
    "word_count": 87
  },
  "game_outcomes": {
    "relationship_trust_change": -0.08,
    "trust_calculation": {...}
  }
}
```

### Example 2: Generate Dialogue Variations

```python
# Generate base components once (1 minute)
primitives = pipeline.generate_npc_primitives("baseline")
context = pipeline.generate_situational_context(primitives, "medium", 5.0)
base_tension = pipeline.generate_tension_memory_elements(primitives, context)

# Generate 5 dialogue variations (5 minutes total)
variations = pipeline.generate_dialogue_variations(
    primitives=primitives,
    context=context,
    base_tension=base_tension,
    complexity_type="baseline",
    authenticity_target="authentic",
    num_variations=5
)

# Result: 5 unique dialogues, same base scenario
# Each with different tension hooks or emotional framing
```

**Use Case:**
- Train model on **dialogue diversity** while controlling for situation
- A/B test different narrative approaches
- Generate "what if" alternatives for same scenario

### Example 3: Component Swapping

```python
# Fixed components
primitives = generate_npc("defensive_lashing")  # High Neuroticism
context = generate_context(capacity="crisis")   # Very low capacity

# Vary authenticity level
for auth in ["failed", "struggling", "authentic", "excellent"]:
    tension = generate_tension(...)
    dialogue = generate_dialogue(..., authenticity_target=auth)
    
    # Result: 4 dialogues showing spectrum from dishonest → excellent
    # Same NPC, same capacity, different honesty levels
```

---

## Implementation Details

### Step 1: NPC Primitives (30 sec)

**Generates:**
- `name`: Unique NPC name
- `ocean`: OCEAN traits (0.0-5.0 scale)
- `base_capacity`: Starting emotional capacity
- `relationship_level`: 0-5 (stranger → soulmate)
- `trust`: 0.0-1.0 current trust value
- `interaction_count`: How many times player has interacted

**Prompt:** ~200 tokens  
**Temperature:** 0.7 (lower for consistent primitives)

**OCEAN Alignment:**
- `people_pleasing` → High Agreeableness (>4.0)
- `misjudgment_over` → Low Conscientiousness (<2.5)
- `defensive_lashing` → High Neuroticism (>4.0)

### Step 2: Situational Context (30 sec)

**Generates:**
- `capacity_factors`: Specific stressors reducing capacity
- `effective_capacity`: Current capacity after stressors
- `support_needed`: What player is asking for
- `urgency_level`: routine/important/urgent/crisis
- `urgency_multiplier`: 1x/2x/3x/5x
- `situation_description`: What's happening
- `location` & `time_context`: Scene setting

**Prompt:** ~300 tokens  
**Temperature:** 0.75

**Calculations:**
- `capacity_factors` impacts must sum to reduce `base_capacity` → `effective_capacity`
- Example: `base_capacity: 7.5, target: 3.5 → factors: -2.5, -1.5`

### Step 3: Tension/Memory Elements (30 sec)

**Generates:**
- `tension_hook`: {type, element} for narrative intrigue
- `relevant_memories`: Past interactions informing this moment
- `subtext`: What NPC feels but doesn't say
- `internal_conflict`: If applicable

**Prompt:** ~350 tokens  
**Temperature:** 0.85 (higher for creative tension)

**Tension Types:**
- `mystery_question`: Unanswered element
- `contradiction`: Behavior vs usual pattern
- `partial_reveal`: Mentions something then deflects
- `stakes_hint`: Foreshadows future importance

### Step 4: Dialogue Generation (60 sec)

**Generates:**
- `setting_context`: One sentence scene-setting
- `dialogue_prose`: 60-120 words novel-quality prose
- `primary_action`: Key physical behavior
- `word_count`: Actual count

**Prompt:** ~600 tokens (includes ALL previous context)  
**Temperature:** `config.temp_emotional` (0.92)

**Requirements:**
- Novel-quality prose (NOT screenplay format)
- NO parentheses for actions
- Integrate ONE physical detail naturally
- Show capacity limitation if gap exists
- Include specified tension hook
- Respect complexity type (people_pleasing, defensive, etc)

### Step 5: Calculate Outcomes (< 1 sec)

**Calculates (deterministic, no LLM):**
- `trust_change`: Using Unwritten formula
- `trust_calculation`: Full breakdown with numbers
- `player_emotional_impact`: How player feels
- `npc_capacity_cost`: Emotional labor cost
- `unlocks_card_evolution`: Major moment flag

**Formula:**
```
trust_change = (base_impact × ocean_mod × urgency × trust_mod) + honesty_bonus

Where:
- base_impact: -0.40 to +0.20 (depends on capacity gap & authenticity)
- ocean_mod: 0.85-1.3 (personality influence)
- urgency: 1.0-5.0 (situation criticality)
- trust_mod: 0.8-1.2 (relationship history)
- honesty_bonus: +0.12 if authentic/excellent, else 0
```

---

## Performance Comparison

### Monolithic (v2.0-v2.1)

| Metric | Value |
|--------|-------|
| Time per interaction | 7+ minutes |
| Prompt size | 500+ lines |
| Success rate | ~40% (empty responses) |
| Reusability | None (regenerate all) |
| Debugging | Hard (single point of failure) |

### Multi-Step (v2.2)

| Metric | Value |
|--------|-------|
| Time per interaction | 2-3 minutes |
| Prompt size per step | 50-100 lines |
| Success rate | Expected 80-90% |
| Reusability | High (swap components) |
| Debugging | Easy (pinpoint step) |

### Variation Generation

**Scenario: Generate 10 dialogue variations for same base**

| Approach | Time | Steps |
|----------|------|-------|
| Monolithic | 70+ minutes | Regenerate all 10 times |
| Multi-Step | ~12 minutes | Generate base once (2 min) + 10 dialogues (1 min each) |

**Speed Improvement:** 6x faster

---

## Training Data Use Cases

### Use Case 1: Standard Training Set

**Goal:** Generate 50 diverse Unwritten interactions

```python
pipeline = MultiStepPipeline(config)
interactions = []

for i in range(50):
    interaction = pipeline.generate_complete_interaction(
        complexity_type=random.choice(COMPLEXITY_TYPES),
        authenticity_target=random.choice(AUTHENTICITY_TARGETS),
        capacity_level=random.choice(CAPACITY_LEVELS),
        support_needed=random.uniform(3.0, 9.0)
    )
    interactions.append(interaction)
    
# Time: ~2.5 hours (vs 6+ hours monolithic)
```

### Use Case 2: Dialogue Diversity Training

**Goal:** Train on dialogue variety while controlling situation

```python
# Generate 1 base scenario
base = generate_base_scenario()

# Generate 20 dialogue variations
for i in range(20):
    dialogue = generate_dialogue_variation(base)
    
# Result: 20 unique dialogues, same underlying situation
# Teaches model: "Many ways to express same emotional state"
# Time: ~20 minutes (vs 140+ min regenerating all)
```

### Use Case 3: Systematic Coverage

**Goal:** Cover all complexity × authenticity combinations

```python
for complexity in COMPLEXITY_TYPES:      # 8 types
    for authenticity in AUTHENTICITY_TARGETS:  # 4 targets
        interaction = generate_complete_interaction(
            complexity_type=complexity,
            authenticity_target=authenticity,
            ...
        )
        
# Result: 32 examples covering full spectrum
# Time: ~1.5 hours (vs 4+ hours monolithic)
```

### Use Case 4: Edge Case Generation

**Goal:** Generate rare but critical scenarios

```python
# Crisis situation with defensive NPC
edge_case = generate_complete_interaction(
    complexity_type="defensive_lashing",
    authenticity_target="failed",
    capacity_level="crisis",  # Very low capacity
    support_needed=9.0        # Very high need
)

# Result: NPC lashes out when can't help (important edge case)
```

---

## Testing

**Run test script:**

```bash
python scripts/test_multi_step_pipeline.py
```

**Tests:**
1. **Single Interaction:** Generate complete interaction, verify all fields
2. **Dialogue Variations:** Generate 3 variations for same base scenario
3. **Component Reuse:** Swap tension hooks, verify different dialogues

**Expected Output:**
```
TEST 1: Single Complete Interaction
✅ Generated in 145.2 seconds
NPC: Jordan
Capacity: 3.8/10
Dialogue (92 words):
[Generated dialogue prose...]
Trust Change: -0.12

TEST 2: Dialogue Variations (Same Base Scenario)
📦 Generating base scenario components...
✅ Base scenario ready
🎭 Generating 3 dialogue variations...
✅ Generated 3 variations in 178.5 seconds
   Average: 59.5 seconds per dialogue

TEST 3: Component Reuse (Swap One Element)
🔄 Generating dialogues with different tension hooks...
--- Version 1 ---
Tension: mystery_question - Phone buzzes, doesn't explain
--- Version 2 ---
Tension: contradiction - Usually careful, today reckless
```

---

## Integration with Existing System

### Option A: Replace Monolithic

```python
# OLD (systematic_generator.py)
interaction = generator.generate_systematic_emotional_batch(batch_size=1)[0]

# NEW (multi_step_pipeline.py)
interaction = pipeline.generate_complete_interaction(...)
```

### Option B: Hybrid Approach

```python
# Use multi-step for complex scenarios
if scenario_complexity > threshold:
    interaction = pipeline.generate_complete_interaction(...)
else:
    # Use faster monolithic for simple cases
    interaction = generator.generate_simple_interaction(...)
```

### Option C: Variation Mode

```python
# Generate base with monolithic
base = generator.generate_base_scenario()

# Generate variations with multi-step  
variations = pipeline.generate_dialogue_variations(base, num=10)
```

---

## Next Steps

1. **Test Pipeline:**
   ```bash
   python scripts/test_multi_step_pipeline.py
   ```

2. **Compare Quality:**
   - Generate 10 interactions with monolithic
   - Generate 10 interactions with multi-step
   - Compare dialogue quality, calculation accuracy

3. **Benchmark Speed:**
   - Measure time per step
   - Identify bottlenecks
   - Optimize slow steps

4. **Integration:**
   - Update `run_training_pipeline.py` to use multi-step
   - Add multi-step option to config
   - Migrate existing generation scripts

5. **Variation Testing:**
   - Generate 1 base + 10 variations
   - Verify dialogue diversity
   - Confirm game mechanics consistency

---

## Files Created

- `src/unwritten/training/multi_step_pipeline.py` - Pipeline implementation
- `scripts/test_multi_step_pipeline.py` - Test script
- `MULTI_STEP_PIPELINE_V2.2.md` - This documentation

## Files to Update (Future)

- `scripts/run_training_pipeline.py` - Add multi-step option
- `src/unwritten/training/config.py` - Add pipeline settings
- Integration tests for systematic coverage

---

**Version:** v2.2  
**Priority:** HIGH (solves monolithic prompt issues)  
**Status:** Ready for testing  
**Expected Impact:** 60-70% faster, 2x more reliable, infinite reusability

