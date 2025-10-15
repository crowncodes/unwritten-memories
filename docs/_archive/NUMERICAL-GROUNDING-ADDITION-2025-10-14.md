# Numerical Grounding System Added - October 14, 2025

**Change Type:** Documentation Enhancement  
**Status:** ✅ Complete  
**Files Added:** `NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md`  
**Files Updated:** `master_truths_canonical_spec_v_1_2.md`, `3.ai/37-training-data-quality-standards.md`

---

## The Problem Identified

User observation:
> "Docs have number assignments everywhere (capacity 2.5/10, trust -1.8, meter +3)... but isn't it hard for an LLM to gauge what that actually means? How does the LLM determine during training that something is a +3 or a +1 to relationship? I fear they don't really mean anything and are thus arbitrarily applied."

**This was absolutely correct.** The documentation defined:
- Scales (0-10, 0.0-1.0)
- Formulas (`base × urgency × trust`)
- Constants (5x multiplier, capacity + 2 rule)

But did NOT define:
- What does `-0.2 trust` vs `-1.8 trust` actually **mean** experientially?
- How do you **determine** when to use which number?
- What are the **qualitative anchors** for quantitative values?

Without grounding, numbers become arbitrary - both for humans writing specs and LLMs generating training data.

---

## The Solution: Numerical Grounding & Calibration Guide

Created comprehensive calibration guide establishing qualitative anchors for ALL numerical scales:

### 1. Trust Impact Scale (-3.0 to +1.0)

**Five Qualitative Tiers with Narrative Markers:**

```
-3.0: RELATIONSHIP SHATTERING
- "I don't know if I can trust you anymore"
- May never fully recover
- Examples: Betrayal of deep secret, abandonment in crisis

-1.5 to -2.0: MAJOR HARM
- "You really hurt me"
- Weeks to recover
- Examples: Missing important event, harsh criticism during vulnerability

-0.8 to -1.2: MODERATE HARM
- "That stung" / "I'm disappointed"
- Days to recover
- Examples: Forgetting birthday, declining help when hoped you'd say yes

-0.3 to -0.5: MINOR HARM
- "A little disappointed, but I get it"
- Hours to recover
- Examples: Declining routine favor, being slightly late

-0.1 to -0.2: NEGLIGIBLE
- "All good!" / "Don't even think about it"
- Immediate recovery
- Examples: Trivial conflicts, minor scheduling issues
```

### 2. Emotional Capacity Scale (0-10)

**Four Qualitative Tiers with Behavioral Descriptions:**

```
0-1: DEPLETED
- "I can't do this" / Complete withdrawal
- Cannot provide ANY support
- Narrative: "She stares at her phone. Can't respond. Not today."

2-4: LOW (Struggling)
- "I'm barely holding it together"
- Can support needs ≤ 0-2 only
- Narrative: "She's there, but you can see the exhaustion. 'I can't help the way you need.'"

5-7: MODERATE (Stable)
- "I'm doing okay" / "I've got some bandwidth"
- Can support needs ≤ 3-5
- Narrative: "Present and engaged. Listens for an hour. Suggests continuing this weekend."

8-10: HIGH (Thriving)
- "I'm here for you" / "Tell me everything"
- Can support needs ≤ 6-8
- Narrative: "She picks up on the second ring. 'Come over. I've got all night.'"
```

### 3. Meter Values (0-10) for All Four Meters

Established narrative anchors for each level:
- **Crisis (0-1)**: "Body broken" / "Burnout" / "Completely isolated" / "Despair"
- **Low (2-3)**: "Exhausted" / "Foggy" / "Lonely" / "Struggling"
- **Normal (4-6)**: "Functioning" / "Stable" / "Connected" / "Okay"
- **High (7-8)**: "Energized" / "Sharp" / "Thriving" / "Fulfilled"
- **Peak (9-10)**: "Optimal" / "Flow state" / "Social catalyst" / "Joyful"

### 4. Quality Scores (0.0-1.0)

```
0.0-0.3: INAUTHENTIC
- Lies, defensive, avoids truth
- Example: "I'm fine!" (when clearly not)

0.4-0.6: STRUGGLING/MIXED
- Wants to be honest but can't quite
- Example: "I can try... I'm just... I'm sorry"

0.7-0.8: AUTHENTIC (Target minimum)
- Honest about limitations, clear boundaries
- Example: "I want to help, but I'm barely keeping it together myself"

0.9-1.0: HIGHLY AUTHENTIC
- Crystal clear, kind but firm, no guilt
- Example: "I'm at capacity. I can't take this on. But I care."
```

---

## The Three-Step Calibration Process

### Every Numerical Assignment Must Follow:

```
1. ANCHOR: Identify qualitative tier
   "This feels like major harm" → -1.5 to -2.0 range

2. CALCULATE: Apply formulas with explicit factors
   base -0.6 × personality 0.8 × urgency 3x × trust 1.2 = -1.73

3. VALIDATE: Confirm narrative matches number
   Does dialogue show "weeks to recover" level harm? YES ✓
```

### Worked Example Included

Full calculation with narrative for:
- Player declines to help Sarah move (crisis context)
- Shows meter → capacity → personality → urgency → trust → final impact
- Every step explained with "what this means narratively"
- Formula: `(-0.5 × 0.7 × 5.0 × 1.2 × 0.9) = -1.89 → -1.9`
- Validation: "Does -1.9 feel like 'major harm'? YES"

---

## Training Data Requirements Updated

### Every Training Sample Must Now Include:

```json
{
  "relationship_impact": -1.9,
  
  "impact_calculation": {
    "base": -0.5,
    "personality_modifier": 0.7,
    "urgency_multiplier": 5.0,
    "trust_modifier": 1.2,
    "capacity_factor": 0.9,
    "result": -1.89,
    "rounded": -1.9
  },
  
  "qualitative_anchor": {
    "tier": "MAJOR HARM (-1.5 to -2.0)",
    "narrative_markers": ["This really hurt", "I feel let down", "Weeks to recover"],
    "recovery_time": "2-3 weeks"
  },
  
  "validation": {
    "does_dialogue_match_score": true,
    "reasoning": "Response shows hurt without melodrama, matches -1.9 tier"
  }
}
```

**NO MORE:** "relationship_impact": -1.3 (with no justification)

**ALWAYS:** Number + Formula + Anchor + Validation

---

## Common Calibration Errors Documented

### Error 1: Arbitrary Numbers
```
❌ "relationship_impact": -1.3
✅ -1.3 with calculation, tier, validation
```

### Error 2: Dialogue/Score Mismatch
```
❌ Impact: -2.5, Dialogue: "No worries! All good!"
✅ Impact: -2.5, Dialogue: "I don't know what to say. I need space."
```

### Error 3: Ignoring Capacity Constraints
```
❌ Capacity 2.5, provides 7.0 support level
✅ Capacity 2.5, cannot support needs > 0.5, dialogue reflects limitation
```

### Error 4: Inconsistent Tier Mapping
```
❌ Impact -0.3 with "shattered trust" narrative
✅ Impact -0.3 with "minor disappointment" narrative
```

---

## Integration Points

### Master Truths v1.2 Updated

Added to Section 13 (Authoring Rules):

```markdown
13. **Numerical Grounding** *(NEW v1.2)*: Use qualitative anchors from 
    `NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md` - every number must have 
    derivation, anchor, and validation.
```

### Training Data Standards Updated

`3.ai/37-training-data-quality-standards.md` now requires:
- Qualitative anchors for all numerical assignments
- Formula breakdown with explicit factors
- Validation checks (does narrative match tier?)
- Reference to calibration guide

### Compliance Checklist Extended

New checklist item for all documentation:
- [ ] **Numerical assignments grounded**: Every number has derivation, qualitative anchor, and validation check

---

## Impact

### For Humans Writing Specs
- Clear guidance on when to use which number
- Consistency across documentation
- Validation framework (does this feel right?)

### For LLMs Generating Training Data
- Concrete examples of what numbers mean
- Formula + narrative pairing
- Quality validation built in
- No more arbitrary number assignments

### For Game Implementation
- Numbers now have experiential meaning
- Can explain to players what changes mean
- Easier to debug ("does this feel like -1.8 trust loss?")

---

## Example: Before vs After

### BEFORE (Arbitrary)
```json
{
  "player_action": "Declines help",
  "relationship_impact": -1.3,
  "dialogue": "Whatever."
}
```

**Problems:**
- Why -1.3?
- Dialogue doesn't match magnitude
- No validation

### AFTER (Grounded)
```json
{
  "player_action": "Declines to help Sarah move (crisis context)",
  
  "context": {
    "npc_capacity": 3.85,
    "capacity_tier": "LOW - struggling",
    "urgency": "crisis",
    "urgency_multiplier": 5.0,
    "relationship_trust": 0.65
  },
  
  "calculation": {
    "base": -0.5,
    "personality_adjusted": -0.35,
    "after_urgency": -1.75,
    "after_trust": -2.1,
    "after_capacity": -1.89,
    "final": -1.9,
    "formula": "(-0.5 × 0.7 × 5.0 × 1.2 × 0.9) = -1.89 → -1.9"
  },
  
  "qualitative_anchor": {
    "tier": "MAJOR HARM (-1.5 to -2.0)",
    "expected_narrative": "This really hurt / I feel let down / Weeks to recover",
    "recovery_time": "2-3 weeks"
  },
  
  "dialogue": "Oh. Okay. I... I understand. I'll figure something out. 
  [pause] I really needed your help with this, you know? It's... it's fine. 
  I'll manage.",
  
  "validation": {
    "does_impact_match_narrative": true,
    "does_dialogue_match_capacity": true,
    "does_score_match_tier": true,
    "reasoning": "Low capacity (3.85) prevents generous interpretation. Crisis 
    urgency (5x) amplifies routine rejection to major harm. Dialogue shows 
    hurt without melodrama. Matches -1.9 tier perfectly."
  }
}
```

---

## Next Steps

1. ✅ Calibration guide created
2. ✅ Master Truths updated
3. ⏳ Review existing training data samples against new standards
4. ⏳ Update `qwen3_generator.py` to enforce grounding requirements
5. ⏳ Regenerate low-quality training samples with proper calibration

---

## Key Insight

> **Numbers without meaning are arbitrary. Meaning without numbers is vague. Numbers WITH qualitative anchors are usable.**

The calibration guide bridges the gap between abstract scales and concrete narrative, enabling both humans and LLMs to:
1. Determine appropriate numerical values
2. Validate consistency
3. Generate authentic, grounded content

---

## Files Changed

### Created
- `docs/NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md` (~1000 lines, comprehensive)

### Modified
- `docs/master_truths_canonical_spec_v_1_2.md` (Section 13 updated, calibration reference added)
- `docs/3.ai/37-training-data-quality-standards.md` (Requirements updated, references calibration guide)

### Next Updates Needed
- `docs/3.ai/32-prompt-engineering-principles.md` (Add calibration principle)
- `src/unwritten/training/qwen3_generator.py` (Enforce grounding in generation)
- Training data regeneration with proper calibration

---

**The documentation now has a complete grounding system. Every number means something specific, derived from formulas, validated against narrative, and consistent across all systems.**

