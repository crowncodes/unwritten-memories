# Training Data Quality Standards

**Purpose:** Define quality requirements for AI training data generation  
**Audience:** AI engineers, data scientists, content generators  
**Status:** ✅ Master Truths v1.2 Compliant  
**Related:** ← 32-prompt-engineering-principles.md | → 36-local-model-training.md

---

## The Quality Problem

**Issue Identified (2025-10-14):**

Initial training data generation was too clean, formulaic, and lacked realistic complexity. This document establishes standards to ensure training data captures authentic human behavior, including failures and messiness.

### What Was Wrong

```markdown
❌ TOO FORMULAIC:
- Repetitive response patterns ("I can't right now...")
- Rigid capacity + 2 rule applied mechanically
- No variation in communication styles

❌ MISSING COMPLEXITY:
- No examples of misjudgment (over/underestimating capacity)
- No poorly handled boundaries
- No emergency overrides
- No cultural variation

❌ AUTHENTICITY SCORE INFLATION:
- All examples scored 0.82-0.95
- No low authenticity examples (0.2-0.5)
- Real humans fail more often than this dataset showed

❌ OVERSIMPLIFIED IMPACTS:
- Relationship impacts reduced to single numbers
- Context-free scoring (same action, same score)
- Ignored NPC's OCEAN personality in evaluation
```

---

## ⚠️ CRITICAL: Numerical Grounding Requirement *(NEW)*

> **See `NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md` for complete system**

**Problem:** Numbers without qualitative meaning are arbitrary and unlearnable.

**Solution:** Every numerical assignment MUST include:

### The Three-Step Grounding Process

```
1. ANCHOR: Identify qualitative tier
   "This is major harm" → -1.5 to -2.0 range

2. CALCULATE: Apply formula with explicit factors
   base × personality × urgency × trust × capacity

3. VALIDATE: Confirm narrative matches number
   Does dialogue match the tier? Does it feel right?
```

### Mandatory Fields for All Numerical Assignments

```json
{
  "value": -1.9,
  
  "calculation": {
    "base": -0.5,
    "factors": {
      "personality_modifier": 0.7,
      "urgency_multiplier": 5.0,
      "trust_modifier": 1.2,
      "capacity_factor": 0.9
    },
    "formula": "(-0.5 × 0.7 × 5.0 × 1.2 × 0.9) = -1.89 → -1.9"
  },
  
  "qualitative_anchor": {
    "tier": "MAJOR HARM (-1.5 to -2.0)",
    "narrative_markers": ["This really hurt", "I feel let down", "Weeks to recover"],
    "recovery_time": "2-3 weeks"
  },
  
  "validation": {
    "does_dialogue_match_tier": true,
    "reasoning": "Response shows hurt without melodrama, matches -1.9 tier"
  }
}
```

### Common Errors to Avoid

**❌ Error 1: No justification**
```json
{ "relationship_impact": -1.3 }
```

**❌ Error 2: Dialogue/score mismatch**
```json
{ 
  "impact": -2.5,
  "dialogue": "No worries! All good!" 
}
```

**❌ Error 3: Ignoring capacity constraints**
```json
{
  "capacity": 2.5,
  "provides_support_level": 7.0  // Violates capacity + 2 rule
}
```

**❌ Error 4: Inconsistent tier mapping**
```json
{
  "impact": -0.3,  // Minor harm tier
  "narrative": "You shattered my trust"  // Relationship shattering tier
}
```

### Quality Gates

All training data MUST pass:
- [ ] Every numerical value has explicit formula
- [ ] Every value mapped to qualitative tier
- [ ] Dialogue/narrative matches tier
- [ ] Capacity constraints respected
- [ ] Validation check included

**Reject any data that assigns numbers without grounding.**

---

## Core Quality Standards

### Standard 1: Full Authenticity Spectrum

**Requirement:** Every batch must include examples across the full authenticity range.

**Distribution Requirements:**

```markdown
0.2-0.4 (Very Inauthentic): 10-15% of batch
├─ Lies about availability
├─ People-pleasing despite exhaustion
├─ Defensive lashing out
└─ Complete avoidance

0.4-0.6 (Struggling/Mixed): 20-25% of batch
├─ Wants to be honest but can't
├─ Overcommits with awareness
├─ Apologizes excessively
└─ Half-truths and hedging

0.6-0.8 (Authentic but Imperfect): 30-35% of batch
├─ Honest but stumbling
├─ Sets boundary with guilt
├─ Offers alternatives
└─ Could be clearer

0.8-1.0 (Highly Authentic): 30-35% of batch
├─ Clear, kind boundary-setting
├─ Honest acknowledgment
├─ No excessive guilt
└─ Offers what they CAN provide
```

**Validation:**

```python
def validate_authenticity_distribution(batch: List[Dict]) -> bool:
    """Ensure batch covers full authenticity spectrum."""
    scores = [item['authenticity_score'] for item in batch]
    
    low = sum(1 for s in scores if 0.2 <= s < 0.5)
    medium = sum(1 for s in scores if 0.5 <= s < 0.7)
    high = sum(1 for s in scores if 0.7 <= s < 0.9)
    excellent = sum(1 for s in scores if 0.9 <= s <= 1.0)
    
    total = len(scores)
    return (
        low >= total * 0.10 and      # At least 10% low
        medium >= total * 0.20 and   # At least 20% medium
        high >= total * 0.30         # At least 30% high
    )
```

---

### Standard 2: Complexity Requirements

**Requirement:** Every batch must include realistic complexity factors.

**Required Complexity Types:**

**1. Misjudgment (20% of batch)**

```markdown
CAPACITY OVERESTIMATE:
Character: Capacity 3.5/10, Support needed: 7.0/10
Response: "Yeah, I can totally help!" (thinks they can, but can't)
Consequence: Overcommits → burns out → has to cancel → damages relationship

CAPACITY UNDERESTIMATE:
Character: Capacity 7.5/10, Support needed: 6.0/10
Response: "I don't think I can handle that..." (could have, but didn't)
Consequence: Missed opportunity → friend goes elsewhere → growth moment lost

Why needed:
- Real people constantly misjudge their capacity
- Shows consequences of poor self-assessment
- Creates authentic regret/relief patterns
- Demonstrates learning opportunities
```

**2. Failed Boundary-Setting (15% of batch)**

```markdown
PEOPLE-PLEASING FAILURE:
"I... I guess I can help. [internal thought: Why can't I say no? I'm exhausted but I can't disappoint them.]"
Authenticity: 0.35 (knows it's wrong, does it anyway)

DEFENSIVE/AGGRESSIVE FAILURE:
"Why do you always ask me when I'm busy? Figure it out yourself!"
Authenticity: 0.25 (lashes out, damages relationship unnecessarily)

AVOIDANT FAILURE:
[Reads message, anxious spike, closes phone, avoids for 3 days]
Authenticity: 0.20 (completely avoids instead of honest conversation)

Why needed:
- Many people handle boundaries poorly
- Cultural/personality factors affect ability
- Anxiety/guilt prevent honest communication
- Shows cost of poor boundary-setting
```

**3. Emergency Override (10% of batch)**

```markdown
PARENT/CHILD SCENARIO:
Capacity: 1.5/10 (crisis mode)
Situation: Child calls from school, panic attack
Response: "I'm coming. Right now. I'll be there in 10 minutes."
[Pushes through exhaustion because child > capacity limit]

LIFE-THREATENING EMERGENCY:
Capacity: 2.0/10 (barely functioning)
Situation: Friend suicide risk, needs immediate intervention
Response: "I'm not okay but neither are you. Stay on the phone. I'm here."
[Capacity doesn't matter when life is at stake]

Why needed:
- Sometimes limits ARE overridden
- Shows what people prioritize (hierarchy of needs)
- Demonstrates cost of pushing beyond limits
- Realistic sacrifice moments
```

**4. Cultural/Communication Variation (20% of batch)**

```markdown
INDIRECT COMMUNICATION:
Capacity: 3.5/10
Request: "Can you help me move this weekend?"
Response: "Oh, I'm a little busy, but... I mean, if you really need... I can try?"
[Says yes when should say no; cultural norm prevents directness]

EXCESSIVE APOLOGIZING:
Capacity: 4.0/10
Response: "I'm so so sorry, I know I'm the worst friend, I just—I'm sorry—I really can't—I feel terrible—sorry..."
[Can't set boundary without self-flagellation; low self-worth]

AGGRESSIVE/BLUNT:
Capacity: 2.5/10 + Low Agreeableness
Response: "No. Figure it out yourself. I'm not your therapist."
[Effective boundary but damages relationship; personality-driven style]

Why needed:
- Not everyone communicates like therapy-speak
- Personality (OCEAN) shapes boundary-setting style
- Cultural norms affect directness
- Some responses are effective but relationally costly
```

**5. Mixed Emotions (15% of batch)**

```markdown
WANTS TO HELP + RESENTFUL:
"Of course I'll help. [internal: Why is it always me? I'm exhausted and they never ask anyone else.]"
Authenticity: 0.45 (says yes, but resentment will poison interaction)

GUILTY + RELIEVED:
"I can't, I'm sorry. [internal: I feel terrible... but also relieved. I need this break.]"
Authenticity: 0.75 (honest no, but complex emotions about it)

ANGRY + UNDERSTANDING:
"I'm frustrated you asked when I'm clearly struggling. But I get it—you're desperate. I still can't help."
Authenticity: 0.80 (processes both emotions, sets boundary anyway)

Why needed:
- Real emotions aren't clean/simple
- Cognitive dissonance is normal
- Complex feelings don't negate authenticity
- Shows emotional maturity in handling ambiguity
```

**Validation:**

```python
def validate_complexity_requirements(batch: List[Dict]) -> Dict:
    """Check if batch includes required complexity types."""
    has_misjudgment = any('misjudg' in str(item.get('tags', [])) for item in batch)
    has_failed_boundaries = any('boundary_failure' in str(item.get('tags', [])) for item in batch)
    has_emergency = any('emergency' in str(item.get('tags', [])) for item in batch)
    has_cultural = any('cultural' in str(item.get('tags', [])) for item in batch)
    has_mixed_emotions = any('mixed_emotion' in str(item.get('tags', [])) for item in batch)
    
    return {
        'misjudgment': has_misjudgment,
        'failed_boundaries': has_failed_boundaries,
        'emergency_override': has_emergency,
        'cultural_variation': has_cultural,
        'mixed_emotions': has_mixed_emotions,
        'meets_standard': all([has_misjudgment, has_failed_boundaries, has_emergency, has_cultural])
    }
```

---

### Standard 3: Capacity Buffer Explanation

**The "+2 Buffer" - What It Actually Means:**

```markdown
ORIGINAL RULE (too rigid):
"Character at X/10 capacity can provide UP TO (X + 2)/10 level of emotional support"

PROBLEMS:
- Why exactly 2? Seems arbitrary
- Doesn't account for personality
- Doesn't account for relationship
- Doesn't account for desperation
- Applied mechanically without reasoning

IMPROVED RULE (context-dependent):
"Character's maximum supportable level depends on capacity + variable buffer (1-3)"

BUFFER DETERMINANTS:

Buffer = 1 (minimal):
- Low agreeableness (less motivated to stretch)
- Low relationship trust (won't overextend)
- Recent pattern of overextension (learned not to)

Buffer = 2 (standard):
- Medium agreeableness
- Medium trust
- Normal relationship dynamics
- No special circumstances

Buffer = 3 (maximum):
- High agreeableness (wants to help desperately)
- High trust/love (will push for this person)
- Emergency context (life/death override)
- Parent/child or life partner relationship

EXAMPLES:

Low Agreeableness NPC:
Capacity 4.0/10 + Buffer 1 = Max 5.0/10 support
"I can help a little, but don't expect too much."

Medium Agreeableness NPC:
Capacity 4.0/10 + Buffer 2 = Max 6.0/10 support
"I'll do what I can. Let me see how I'm feeling."

High Agreeableness NPC + Best Friend + Emergency:
Capacity 4.0/10 + Buffer 3 = Max 7.0/10 support
"I'm exhausted but you're my best friend and this is an emergency. I'll find the energy."
```

**Implementation:**

```python
def calculate_support_buffer(npc_state: Dict, context: Dict) -> float:
    """Calculate variable buffer based on personality, relationship, and context."""
    base_buffer = 2.0
    
    # Personality adjustment
    if npc_state['ocean']['agreeableness'] >= 0.7:
        base_buffer += 0.5  # High agreeableness pushes harder
    elif npc_state['ocean']['agreeableness'] <= 0.3:
        base_buffer -= 0.5  # Low agreeableness less motivated
    
    # Relationship adjustment
    if context['relationship']['trust'] >= 0.8:
        base_buffer += 0.3  # High trust = willing to stretch
    elif context['relationship']['trust'] <= 0.4:
        base_buffer -= 0.3  # Low trust = won't overextend
    
    # Context adjustment
    if context['urgency'] >= 4:  # Emergency
        base_buffer += 0.5
    
    if context['relationship']['type'] in ['parent_child', 'life_partner']:
        base_buffer += 0.3
    
    # Clamp to 1-3 range
    return max(1.0, min(3.0, base_buffer))
```

---

### Standard 4: Context-Dependent Scoring

**Requirement:** Relationship impact scoring must account for NPC frame of reference.

**Scoring Formula (Master Truths v1.2):**

```
Player_Action_Impact = NPC_Personality_Filter 
                      × NPC_Current_Urgency (1x-5x)
                      × Relationship_History (0.5x-2x)
                      × NPC_Capacity_Constraint
```

**NO Fixed Scoring Tables:**

```markdown
❌ WRONG (fixed scoring):
"Player declines help = -0.5 trust (always)"

✅ CORRECT (context-dependent):
"Player declines help = calculate based on NPC state"

SAME ACTION, DIFFERENT IMPACTS:

Scenario A: High-agreeableness NPC, routine favor, high trust, high capacity
Impact: -0.1 to -0.2 trust
Response: "No worries! I totally understand. Let me know if you change your mind."

Scenario B: High-agreeableness NPC, crisis need (5x), medium trust, low capacity
Impact: -2.5 to -3.0 trust
Response: "I... I really needed you. I don't know who else to ask. This really hurts."

Scenario C: Low-agreeableness NPC, routine favor, medium trust, high capacity
Impact: -0.3 to -0.5 trust
Response: "Whatever. I'll figure it out myself. Not surprised."

Scenario D: Low-agreeableness NPC, crisis need (5x), low trust, high capacity
Impact: -1.0 to -1.5 trust
Response: "Typical. I knew I couldn't count on you. We're done."
```

**Implementation:**

```python
def calculate_relationship_impact(
    player_action: Dict,
    npc_state: Dict,
    context: Dict
) -> float:
    """Calculate relationship impact based on NPC frame of reference."""
    
    # Base response from personality
    base_impact = calculate_personality_response(
        action=player_action,
        ocean=npc_state['ocean']
    )
    
    # Apply urgency multiplier
    urgency_mult = context['urgency']  # 1-5
    
    # Apply trust modifier
    trust_mod = calculate_trust_modifier(context['relationship']['trust'])
    
    # Apply capacity constraint (affects judgment quality)
    capacity_factor = calculate_capacity_judgment(npc_state['capacity'])
    
    # Calculate final impact
    impact = base_impact * urgency_mult * trust_mod * capacity_factor
    
    # Add memory resonance if applicable
    if context.get('resonates_with_past_betrayal'):
        impact *= 1.5  # Past trauma amplifies
    
    return clamp(impact, -3.0, +1.0)
```

---

## Multi-Step Generation Process

### The Problem with Single-Step Generation

```markdown
SINGLE-STEP (what we were doing):
Prompt → "Generate complete emotional authenticity example" → Done

PROBLEMS:
- Formulaic output (model defaults to safe patterns)
- Missing complexity (model avoids messiness)
- High authenticity bias (model prefers "good" examples)
- No reasoning chain (can't see thinking process)
```

### Multi-Step Compositional Approach

```markdown
PHASE 1: Generate Primitives (small focused chunks)
├─ Character state primitive (capacity calculation only)
├─ Interaction primitive (situation context only)
└─ OCEAN personality primitive (trait implications only)

PHASE 2: Combine with Chain-of-Thought Reasoning
├─ "Given this capacity, can they provide support?"
├─ "How would personality affect response style?"
├─ "What's the buffer in this context?"
└─ Generate 3 responses: high/medium/low authenticity

PHASE 3: Add Complexity Layer
├─ Add misjudgment factor
├─ Add cultural communication style
├─ Add emergency override scenario
└─ Add mixed emotions

PHASE 4: Validate Quality Spectrum
├─ Check authenticity distribution
├─ Check complexity requirements met
├─ Flag if too clean/formulaic
└─ Regenerate low-quality samples
```

**Benefits:**

```markdown
✓ More varied output (primitives prevent formula lock-in)
✓ Reasoning visible (can audit thinking process)
✓ Complexity forced (Phase 3 requirement)
✓ Quality assured (Phase 4 validation)
✓ Faster iteration (regenerate only failed phases)
```

**Current Implementation:** 
- `src/unwritten/training/multi_step_systematic.py` - Multi-step compositional generation with systematic parameter coverage
- `src/unwritten/training/systematic_generator.py` - Systematic parameter coverage with batch processing
- `src/unwritten/training/validation.py` - Comprehensive validation pipeline

**Systematic Coverage Architecture:**

Instead of random generation, the pipeline ensures comprehensive coverage of the parameter space:

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
    "baseline", "misjudgment_over", "misjudgment_under",
    "people_pleasing", "defensive_lashing", "emergency_override",
    "cultural_indirect", "mixed_emotions"
]
```

**Coverage Tracking:** SQLite database (`coverage_tracking.db`) tracks which parameter combinations have been generated, automatically filling gaps to ensure complete coverage across all dimensions.

**Benefits:**
- ✅ Guaranteed full authenticity spectrum (no high-score bias)
- ✅ All complexity types represented
- ✅ No parameter combinations skipped
- ✅ Systematic quality instead of random luck

---

## Novel-Quality Dialogue Requirements *(NEW - 2025-10-14)*

### The Problem: Flat Game Dialogue

**Issue Identified:** Initial training data had flat, functional dialogue more suited to mobile games than immersive narrative experiences.

**Comparison:**

```markdown
❌ FLAT (Game Dialogue):
{
  "character_response": "I can't help right now. I'm overwhelmed."
}

✅ NOVEL-QUALITY (Literary Narrative):
{
  "character_response": "She reaches across the table, takes your hand. 
  'I can see you're really hurting,' she says softly. 'But I need to be 
  honest—I'm not in a good place myself right now. Work is crushing me, 
  I haven't slept in two days.' She pauses, looking down at her coffee. 
  Her hands are shaking slightly. 'I've got maybe an hour. I can listen. 
  But I can't give you the full emotional support you need right now. 
  I wish I could. I really do.'"
}
```

### The Three Pillars of Novel-Quality Content

**1. Length & Depth (150-200 words minimum)**
```markdown
❌ One-liner: "I can't, sorry." (3 words)
✅ Rich narrative: 150-200 word response with context, behavior, emotion
```

**2. Show, Don't Tell (Behavioral Grounding)**
```markdown
❌ "She was nervous"
✅ "She fidgeted with her napkin, folding and refolding the corner. 
    Her voice came out quieter than usual."
```

**3. OCEAN Personality Influence**
```markdown
Every character response must reflect their personality scores:

High Agreeableness (4.5):
"She immediately reaches out. 'Of course I'll help. What do you need?'"

Low Agreeableness (2.0):
"She leans back, arms crossed. 'Look, I'm dealing with my own stuff right now.'"

High Neuroticism (4.2):
"Her eyes widen. 'Oh god, is it serious? Should I be worried? I mean—
sorry—what happened?'"

Low Neuroticism (1.8):
"She nods calmly. 'Okay. Let's break this down step by step.'"
```

### Implementation Requirements

**All training examples MUST include:**

```json
{
  "character_response": "150-200 word narrative with behavioral depth",
  "behavioral_cues": [
    "Physical actions (fidgeting, eye contact, posture)",
    "Vocal qualities (tone, volume, pauses)",
    "Micro-expressions (fleeting emotions)"
  ],
  "ocean_influence": {
    "agreeableness": "How this trait shaped the response style",
    "neuroticism": "How emotional stability affected reaction",
    "extraversion": "How social energy influenced engagement"
  },
  "sensory_details": [
    "Environmental details (coffee shop ambiance)",
    "Specific objects (chipped mug, torn book)",
    "Physical sensations (cold hands, racing heart)"
  ],
  "dialogue_quality_metrics": {
    "word_count": 175,
    "shows_vs_tells_ratio": 0.85,
    "specificity_score": 0.90,
    "cliche_count": 0
  }
}
```

### Quality Gates

Before accepting any training example:

- [ ] **Length**: 150-200 words for primary response
- [ ] **Behavioral Grounding**: At least 3 physical/behavioral cues
- [ ] **OCEAN Visibility**: Personality clearly influences communication style
- [ ] **Specificity**: Includes specific objects, places, or sensory details
- [ ] **No Clichés**: Zero generic phrases ("mysterious past", "hidden depths")
- [ ] **Emotional Authenticity**: Response constrained by emotional capacity
- [ ] **Show vs Tell**: 80%+ showing emotion through action, not stating it

**Validation Script:** `src/unwritten/training/validation.py` enforces these requirements automatically.

---

## Quality Validation Checklist

### Before Accepting Batch

```markdown
✅ Authenticity Distribution
- [ ] 10-15% score 0.2-0.4 (very inauthentic)
- [ ] 20-25% score 0.4-0.6 (struggling)
- [ ] 30-35% score 0.6-0.8 (authentic but imperfect)
- [ ] 30-35% score 0.8-1.0 (highly authentic)

✅ Complexity Requirements
- [ ] At least 20% include misjudgment
- [ ] At least 15% include failed boundaries
- [ ] At least 10% include emergency override
- [ ] At least 20% include cultural variation
- [ ] At least 15% include mixed emotions

✅ Variation Requirements
- [ ] No more than 3 examples use same dialogue pattern
- [ ] At least 5 different communication styles represented
- [ ] Buffer reasoning varies (not always +2)
- [ ] Relationship impacts context-dependent (not fixed)

✅ Realism Requirements
- [ ] Examples feel "messy" and human
- [ ] Failures and successes both represented
- [ ] Capacity buffer explained, not just applied
- [ ] OCEAN personality visible in communication style
- [ ] Context affects scoring (no fixed tables)
```

---

## Summary

**Key Changes from Initial Approach:**

```markdown
BEFORE (too clean):
- Single-step generation
- Formulaic patterns
- All high authenticity scores
- Fixed "+2 buffer"
- Context-free scoring

AFTER (realistic):
- Multi-step compositional generation
- Required complexity factors
- Full authenticity spectrum (0.2-1.0)
- Variable buffer (1-3) with reasoning
- Context-dependent scoring (NPC frame of reference)
```

**Result:** Training data that teaches model to generate authentic, messy, realistic human emotional behavior instead of clean "therapy-speak" NPCs.

---

**Related Documents:**
- → 32-prompt-engineering-principles.md (complexity requirements)
- → 36-local-model-training.md (model training process)
- → Master Truths v1.2 Section 11 (bidirectional scoring framework)

