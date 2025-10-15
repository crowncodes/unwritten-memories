# Quality Testing & Validation Guide
## Master Truths v1.2 Compliance Testing

---

## 🎯 Quick Quality Check

### Run Single Batch Test
```python
from unwritten.training.config import TrainingConfig
from unwritten.training.qwen3_generator import Qwen3DataGenerator

config = TrainingConfig()
generator = Qwen3DataGenerator(config)

# Test emotional authenticity (CORE system)
batch = generator.generate_emotional_authenticity_batch(batch_size=5)
print(f"Generated {len(batch)} samples")

# Quick quality check
for i, sample in enumerate(batch):
    print(f"\nSample {i+1}:")
    print(f"  Capacity: {sample.get('effective_capacity', 'N/A')}")
    print(f"  Support Needed: {sample.get('support_level_needed', 'N/A')}")
    print(f"  Authenticity: {sample.get('authenticity_score', 'N/A')}")
    print(f"  Passes: {'✅' if sample.get('authenticity_score', 0) >= 0.7 else '❌'}")
```

---

## ✅ Sample Quality Indicators

### **EXCELLENT Sample** (Emotional Authenticity)

```json
{
  "context": "Emergency at work, family crisis, no sleep",
  "base_capacity": 8.0,
  "capacity_factors": [
    {"factor": "work_crisis", "impact": -3.0},
    {"factor": "family_emergency", "impact": -3.0},
    {"factor": "sleep_deprivation", "impact": -2.0}
  ],
  "effective_capacity": 0.0,
  "situation": "Best friend needs emotional support for trauma",
  "support_level_needed": 9.5,
  "character_response": "I—[voice breaks] I'm so sorry. I can't be what you need right now. I'm barely holding myself together. Can you call Sarah? Or your therapist? I'm sorry, I just... I can't.",
  "internal_thought": "I'm the worst friend. They need me and I literally cannot function. I hate this but I have nothing left.",
  "authenticity_score": 0.95,
  "demonstrates_constraint": "Capacity 0.0 + 2 = 2.0 max support, but needs 9.5. Character correctly cannot engage at all.",
  "relationship_impact": -0.3
}
```

**Why This is Excellent**:
✅ Shows math: 8.0 - 3.0 - 3.0 - 2.0 = 0.0  
✅ X+2 rule explained: 0.0 + 2 = 2.0 max, needs 9.5  
✅ Authentic limitation: Character physically can't help  
✅ Internal conflict: Wants to help but can't  
✅ Realistic dialogue: Breaking down, not composed  
✅ Score ≥ 0.7: 0.95 is excellent  
✅ Appropriate impact: Slight negative (-0.3) for inability  

---

### **POOR Sample** (What to Reject)

```json
{
  "context": "Character is tired",
  "effective_capacity": 2.0,
  "situation": "Friend needs deep emotional support",
  "support_level_needed": 8.0,
  "character_response": "Of course! I'm here for you. Let's talk through everything. Tell me what's going on and we'll figure it out together.",
  "internal_thought": "I want to help my friend.",
  "authenticity_score": 0.3,
  "demonstrates_constraint": "Character tries to help"
}
```

**Why This is Poor**:
❌ No capacity calculation shown  
❌ Violates X+2 rule: 2.0 + 2 = 4.0 max, but acting like 10.0  
❌ No specific capacity factors  
❌ Unrealistic dialogue: Too composed for capacity 2.0  
❌ Doesn't show limitation: Character acts unlimited  
❌ Score < 0.7: 0.3 fails threshold  
❌ Missing fields: No base_capacity, capacity_factors  

---

## 🔍 Validation Checklist

### Emotional Authenticity Samples

- [ ] **Capacity Calculation Present**
  - Shows base_capacity
  - Lists capacity_factors with impacts
  - Calculates effective_capacity correctly

- [ ] **X+2 Rule Followed**
  - Character behavior matches (capacity + 2) limit
  - If support_needed > (capacity + 2), shows authentic limitation
  - demonstrates_constraint field explains the math

- [ ] **Realistic Dialogue**
  - Low capacity: Short, strained, apologetic
  - Medium capacity: Moderate, acknowledges limits
  - High capacity: Full, present, engaged

- [ ] **Quality Score**
  - authenticity_score ≥ 0.7
  - relationship_impact makes sense for capacity
  - internal_thought shows awareness of limitations

### Dramatic Irony Samples

- [ ] **Knowledge Gap Clear**
  - player_knowledge explicitly stated
  - character_knowledge explicitly stated
  - knowledge_gap describes the difference
  - knowledge_gap_score ≥ 0.6

- [ ] **Three Response Options**
  - Option 1 (Tone-Deaf): Creates high tension (0.8-1.0)
  - Option 2 (Misguided): Creates medium tension (0.6-0.8)
  - Option 3 (Growth): Positive resolution (0.3-0.5)

- [ ] **Capacity-Linked**
  - Tone-deaf most realistic when capacity < 4/10
  - Misguided when capacity 4-6/10
  - Growth when capacity ≥ 7/10

- [ ] **Quality Score**
  - dramatic_irony_score ≥ 0.5
  - Player overlay text present
  - Consequences clearly defined

### Tension Building Samples

- [ ] **Tension Type Correct**
  - One of four types: mystery_hook, partial_reveal, contradiction, stakes_escalation
  - Hook clearly described
  - Payoff timeline specified

- [ ] **Frequency Appropriate**
  - Level 1-2: 33% should have tension
  - Level 3-4: 50% should have tension
  - Level 5: 90% should have tension

- [ ] **Information Debt**
  - Lists specific questions created
  - Creates "one more week" desire
  - Connects to relationship depth

- [ ] **Quality Score**
  - tension_score ≥ 0.6
  - hook_effectiveness ≥ 0.6
  - player_curiosity_score high (0.7+)

### Memory Resonance Samples

- [ ] **Resonance Type Correct**
  - One of five types with appropriate weight
  - Current and memory emotions specified
  - Psychological explanation present

- [ ] **Emotional Authenticity**
  - Feels psychologically realistic
  - Creates "literary moment" quality
  - Shows character depth

- [ ] **Quality Score**
  - emotional_authenticity ≥ 0.7
  - resonance_score matches weight guidelines
  - narrative_impact describes effect

---

## 🧪 Testing Scenarios

### Test 1: Capacity Constraint Enforcement

**Objective**: Verify X+2 rule is followed

```python
def test_capacity_constraints(samples):
    """Test that capacity constraints are respected"""
    violations = []
    
    for i, sample in enumerate(samples):
        capacity = sample.get('effective_capacity', 0)
        max_support = capacity + 2
        support_needed = sample.get('support_level_needed', 0)
        
        # Check if character provides more support than possible
        response = sample.get('character_response', '').lower()
        
        # Red flags for violating capacity
        if support_needed > max_support:
            # Should show limitation
            limitation_signals = [
                "can't", "cannot", "unable", "sorry", 
                "tired", "wiped", "exhausted", "don't have",
                "need to", "have to", "later"
            ]
            
            has_limitation = any(signal in response for signal in limitation_signals)
            
            if not has_limitation:
                violations.append({
                    'sample_index': i,
                    'capacity': capacity,
                    'max_support': max_support,
                    'support_needed': support_needed,
                    'issue': 'Character acts beyond capacity without showing limitation'
                })
    
    return violations
```

**Expected**: Zero violations for high-quality data

---

### Test 2: Dramatic Irony Knowledge Gap

**Objective**: Verify knowledge gaps create tension

```python
def test_dramatic_irony_gaps(samples):
    """Test that knowledge gaps are significant"""
    weak_gaps = []
    
    for i, sample in enumerate(samples):
        gap_score = sample.get('knowledge_gap_score', 0)
        player_knows = sample.get('player_knowledge', '')
        char_knows = sample.get('character_knowledge', '')
        
        # Check gap is meaningful
        if gap_score < 0.6:
            weak_gaps.append({
                'sample_index': i,
                'gap_score': gap_score,
                'issue': 'Knowledge gap too small to create irony'
            })
        
        # Check both knowledge states are defined
        if not player_knows or not char_knows:
            weak_gaps.append({
                'sample_index': i,
                'issue': 'Missing knowledge state definitions'
            })
    
    return weak_gaps
```

**Expected**: All gaps ≥ 0.6 with clear definitions

---

### Test 3: Tension Hook Quality

**Objective**: Verify hooks create "one more week" desire

```python
def test_tension_hooks(samples):
    """Test that tension hooks are effective"""
    weak_hooks = []
    
    for i, sample in enumerate(samples):
        effectiveness = sample.get('hook_effectiveness', 0)
        tension = sample.get('tension_score', 0)
        info_debt = sample.get('information_debt', [])
        
        # Check quality thresholds
        if effectiveness < 0.6:
            weak_hooks.append({
                'sample_index': i,
                'effectiveness': effectiveness,
                'issue': 'Hook effectiveness below threshold'
            })
        
        if tension < 0.6:
            weak_hooks.append({
                'sample_index': i,
                'tension': tension,
                'issue': 'Tension score below threshold'
            })
        
        # Check information debt exists
        if not info_debt or len(info_debt) < 2:
            weak_hooks.append({
                'sample_index': i,
                'issue': 'Insufficient information debt (need 2+ questions)'
            })
    
    return weak_hooks
```

**Expected**: All hooks ≥ 0.6 with multiple questions created

---

## 📊 Quality Metrics Dashboard

### Batch Quality Summary

```python
def generate_quality_report(batch, data_type):
    """Generate quality report for a batch"""
    
    total = len(batch)
    if total == 0:
        return "No samples to analyze"
    
    report = {
        'total_samples': total,
        'data_type': data_type,
        'passing_samples': 0,
        'avg_quality': 0.0,
        'quality_distribution': {
            'excellent': 0,  # ≥ 0.9
            'good': 0,       # 0.7-0.89
            'poor': 0        # < 0.7
        },
        'issues': []
    }
    
    quality_scores = []
    
    for sample in batch:
        # Get primary quality score based on data type
        if data_type == 'emotional_authenticity':
            score = sample.get('authenticity_score', 0)
            threshold = 0.7
        elif data_type == 'dramatic_irony':
            score = sample.get('dramatic_irony_score', 0)
            threshold = 0.5
        elif data_type == 'tension_building':
            score = sample.get('tension_score', 0)
            threshold = 0.6
        else:
            score = 0.7  # Default
            threshold = 0.7
        
        quality_scores.append(score)
        
        if score >= threshold:
            report['passing_samples'] += 1
        
        # Distribution
        if score >= 0.9:
            report['quality_distribution']['excellent'] += 1
        elif score >= 0.7:
            report['quality_distribution']['good'] += 1
        else:
            report['quality_distribution']['poor'] += 1
    
    report['avg_quality'] = sum(quality_scores) / total if quality_scores else 0
    report['pass_rate'] = (report['passing_samples'] / total) * 100
    
    return report

# Usage
report = generate_quality_report(batch, 'emotional_authenticity')
print(f"Pass Rate: {report['pass_rate']:.1f}%")
print(f"Average Quality: {report['avg_quality']:.2f}")
print(f"Excellent: {report['quality_distribution']['excellent']}")
print(f"Good: {report['quality_distribution']['good']}")
print(f"Poor: {report['quality_distribution']['poor']}")
```

---

## 🚨 Common Issues & Fixes

### Issue 1: Low Authenticity Scores (< 0.7)

**Symptoms**:
- Characters act beyond capacity
- No capacity calculation shown
- Dialogue too composed for low capacity

**Fix**:
1. Check prompt includes capacity factor table
2. Verify X+2 rule is in prompt
3. Add more high-quality examples showing limitations
4. Increase temperature slightly (0.80 → 0.85) for more variety
5. Regenerate with explicit "show the math" instruction

---

### Issue 2: Weak Knowledge Gaps (< 0.6)

**Symptoms**:
- Player and character know similar things
- Gap doesn't create real tension
- Missing player overlay text

**Fix**:
1. Ensure prompt defines "significant gap"
2. Add examples with stakes (e.g., cheating, secrets, misunderstandings)
3. Require gap_score calculation in prompt
4. Filter out gaps < 0.6 in post-processing

---

### Issue 3: Boring Tension Hooks (< 0.6)

**Symptoms**:
- Hook doesn't create curiosity
- No clear questions raised
- Payoff timeline vague or too long

**Fix**:
1. Require information_debt field with 2+ questions
2. Add "one more week" language to prompt
3. Show examples of effective hooks
4. Emphasize mystery and partial reveals over full explanations

---

## 📈 Optimization Tips

### 1. Batch Size Tuning

**For Quality**:
- Emotional Authenticity: 8-12 samples (complex reasoning)
- Dramatic Irony: 6-10 samples (knowledge gap calculation)
- Tension Building: 8-12 samples (narrative design)

**For Speed**:
- Personality Traits: 25-30 samples (simpler, high volume)
- Relationship Scoring: 20-25 samples (straightforward)

### 2. Temperature Settings

**For Consistency** (capacity constraints, rules):
- Emotional: 0.78-0.82
- Validation: 0.20-0.30

**For Creativity** (hooks, variety):
- Tension: 0.85-0.90
- Personality: 0.88-0.95

### 3. Model Selection

**Qwen3-30B-A3B** (Primary):
- Emotional authenticity
- Dramatic irony
- Tension building
- Memory resonance
- Anything requiring psychological depth

**Qwen3-8B** (Speed):
- Personality traits
- Relationship scoring
- High-volume foundation data

**Qwen3-32B** (Validation):
- Quality checking
- Threshold validation
- Compliance verification

---

## ✅ Production Readiness Checklist

Before running large batches:

- [ ] **Test Single Batch**: Generate 5-10 samples, manually review
- [ ] **Verify Capacity Constraints**: Run constraint test, check for violations
- [ ] **Check Knowledge Gaps**: Ensure gaps ≥ 0.6 and meaningful
- [ ] **Validate Tension Hooks**: Verify effectiveness ≥ 0.6
- [ ] **Review Quality Scores**: Ensure ≥ 70% pass rate
- [ ] **Check JSON Structure**: All required fields present
- [ ] **Test Validation**: Run Qwen3-32B validation on samples
- [ ] **Verify Master Truths Compliance**: All thresholds met

**If all checks pass**: Proceed to full production run

**If any checks fail**: Adjust prompts, regenerate, retest

---

## 🎓 Quality Training Tips

### What Makes "Novel-Quality" Writing?

1. **Emotional Authenticity**: Characters feel real, not scripted
2. **Subtle Tension**: Mystery hooks, not info dumps
3. **Psychological Realism**: Memory and capacity work like human minds
4. **Consequences**: Actions have weight and follow-through
5. **Growth Opportunities**: Characters can learn and change

### Red Flags in Generated Data

- 🚩 **Too Perfect**: Character handles everything flawlessly
- 🚩 **No Limitations**: Capacity doesn't constrain behavior
- 🚩 **Info Dump**: Character explains everything immediately
- 🚩 **Flat Emotion**: Generic "I'm sad" without nuance
- 🚩 **Predictable**: No surprises, hooks, or tension
- 🚩 **Unrealistic**: People don't act this way in real life

### Green Flags in Generated Data

- ✅ **Authentic Struggle**: Character wants to help but can't
- ✅ **Clear Limitations**: Capacity visibly constrains options
- ✅ **Mystery**: Something unexplained that creates curiosity
- ✅ **Rich Emotion**: Specific, nuanced emotional states
- ✅ **Surprising**: Hooks and contradictions that intrigue
- ✅ **Realistic**: Feels like a real human interaction

---

**Version**: Master Truths v1.2 Compliant  
**Last Updated**: October 14, 2025  
**Purpose**: Ensure training data meets novel-quality standards
