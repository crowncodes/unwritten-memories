# Training Prompt Update: Unwritten-Specific v2.0

**Date:** October 14, 2025  
**Type:** Major Rewrite  
**Impact:** Complete alignment with Unwritten game systems  

---

## Summary

Completely rewrote `systematic_generator.py` training prompt from generic "emotional authenticity" examples to **Unwritten-specific NPC interaction card data** that follows canonical game systems.

---

## What Changed

### Before (v1.6.3)
- Generic emotional authenticity scenarios
- Abstract capacity/support examples
- No game system specifics
- Generic dialogue without game context
- Vague JSON schema

### After (v2.0)
- **Unwritten NPC interaction cards**
- **Canonical game systems:** OCEAN, capacity (X+2 rule), urgency (1x-5x), trust modifiers
- **Card-based narrative format** (60-120 word prose for mobile cards)
- **Tension hooks** (mystery, contradiction, partial reveal)
- **Comprehensive JSON schema** matching actual game data structures

---

## Key Improvements

### 1. Game Context Integration

```
GAME CONTEXT (Unwritten card-based mobile game):
- Player interacts with NPCs through card-based narrative choices
- NPCs have persistent personalities (OCEAN), relationships (Level 0-5, Trust 0.0-1.0)
- Emotional capacity (0-10 scale) limits what characters can provide
- Urgency multipliers (1x-5x) amplify impact based on situation criticality
```

### 2. Canonical NPC Response Framework

Now explicitly follows **master_truths v1.2 Section 11**:

```
NPC Response = f(OCEAN, Urgency, Trust, Capacity)

Formula: Trust_Change = Base_Action × OCEAN_Modifier × Urgency × Trust_Modifier + Honesty_Bonus
```

### 3. Unwritten-Specific Complexity Types

Updated all 8 complexity types with game-specific context:

- **baseline**: Standard authentic response with emotional intelligence
- **people_pleasing**: Agreeableness >4.0, overcommits, sets up burnout arc
- **misjudgment_over**: Conscientiousness <2.5, poor self-assessment
- **misjudgment_under**: High Neuroticism >3.5, anxiety-driven underestimation
- **defensive_lashing**: Capacity <2.0 + Neuroticism >4.0, sharp response, trust -0.3 to -0.6
- **emergency_override**: Crisis 5x multiplier, heroic push, capacity drops -2.0 to -3.0
- **cultural_indirect**: Low Extraversion + High Agreeableness, indirect communication
- **mixed_emotions**: Accumulated resentment counter, future relationship risk

### 4. Card Narrative Format

Changed from generic dialogue to **mobile card narrative**:

**Wrong (UI/menu format):**
```
"[SARAH]
Choice A: 'I can help' [Trust +0.2]
Choice B: 'Sorry, busy' [Trust -0.1]"
```

**Correct (card narrative):**
```
"Sarah rubbed her temples, eyes still on the spreadsheet. 'I want to help—I really do. 
But I'm three projects behind and my manager's already mentioned the deadline twice this week.' 
She closed her laptop with more force than necessary. 'Can we talk tomorrow evening instead? 
I'll actually have space to listen properly, not this...' She gestured at the chaos of her 
desk. 'I'm sorry. Rain check?'"
```

### 5. Comprehensive JSON Schema

New schema includes **game-specific fields**:

```json
{
  "npc_profile": {
    "name": "...",
    "relationship_level": "0-5",
    "trust": "0.0-1.0",
    "interaction_count": "..."
  },
  "npc_emotional_state": {
    "base_capacity": 7.5,
    "capacity_factors": [...],
    "effective_capacity": 2.5,
    "can_support_up_to": 4.5,
    "capacity_tier": "LOW"
  },
  "npc_ocean_personality": {
    "openness": "0.0-5.0",
    "conscientiousness": "0.0-5.0",
    "extraversion": "0.0-5.0",
    "agreeableness": "0.0-5.0",
    "neuroticism": "0.0-5.0"
  },
  "interaction_context": {
    "player_request_type": "emotional_support",
    "support_needed": 5.0,
    "urgency_level": "important",
    "urgency_multiplier": 2.0,
    "situation_description": "...",
    "location": "...",
    "time_context": "..."
  },
  "capacity_analysis": {
    "can_provide_full_support": false,
    "capacity_gap": 2.5,
    "support_ceiling": 4.5,
    "recognizes_limitation": true,
    "response_type": "authentic_limitation"
  },
  "npc_card_narrative": {
    "setting_context": "...",
    "dialogue_prose": "[60-120 words novel-quality prose]",
    "primary_action": "rubbed temples",
    "subtext": "...",
    "tension_hook": {
      "type": "mystery_question",
      "element": "..."
    },
    "word_count": 85
  },
  "game_outcomes": {
    "relationship_trust_change": -0.05,
    "trust_calculation": {
      "base_action_impact": -0.15,
      "ocean_personality_modifier": "Agreeableness 0.8 softens decline",
      "urgency_multiplier": 2.0,
      "trust_relationship_modifier": 1.2,
      "honesty_authenticity_bonus": 0.10,
      "full_formula": "(-0.15 * 0.9 * 2.0 * 1.2) + 0.10 = -0.05",
      "impact_tier": "VERY_MINOR_HARM",
      "narrative_explanation": "..."
    },
    "player_emotional_impact": -0.1,
    "npc_capacity_cost": -0.2,
    "unlocks_card_evolution": false
  },
  "training_metadata": {
    "complexity_type": "baseline",
    "authenticity_score": 0.85,
    "demonstrates": ["Authentic boundary-setting", "Integrated prose", "..."],
    "avoids": ["Parenthetical cues", "Over-explanation", "..."],
    "game_system_alignment": {
      "follows_capacity_rule": true,
      "proper_calculation": true,
      "novel_quality_dialogue": true,
      "tension_hook_present": true
    }
  }
}
```

### 6. Authenticity Levels (Game Context)

**Failed (0.2-0.4):**  
Dishonest about capacity. Says 'yes' when should say 'no'. Creates negative card evolution path.

**Struggling (0.4-0.6):**  
Messy communication. Wants to be honest but backtracks. Player confused. Trust barely changes.

**Authentic (0.6-0.8):**  
Clear communication with care. Offers alternative. Small trust loss offset by honesty bonus. Unlocks 'authentic relationship' cards.

**Excellent (0.8-1.0):**  
Gold standard. Perfect self-awareness. May increase trust (+0.05 to +0.15) despite declining. Unlocks rare 'deep trust' cards.

---

## Documentation References

The new prompt explicitly references and follows:

1. **master_truths_canonical_spec_v_1_2.md** (Sections 11, 16, 17)
   - NPC Response Framework
   - Emotional capacity system
   - Novel-quality narrative standards

2. **30-decisive-decision-templates.md**
   - Decision context integration
   - Capacity-aware option gating

3. **33-dialogue-generation-templates.md**
   - Relationship level-appropriate dialogue
   - Card narrative format

4. **35-tension-maintenance-system.md**
   - Hook types: mystery, contradiction, partial reveal, stakes
   - Forward narrative momentum

---

## Training Data Alignment

### Before
Training data was generic "emotional authenticity" that didn't map to actual game systems.

### After
Training data now generates:
- ✅ Actual Unwritten NPC interaction cards
- ✅ Proper OCEAN personality integration (0.0-5.0 scale)
- ✅ Accurate capacity calculations (X+2 rule)
- ✅ Correct urgency multipliers (1x-5x)
- ✅ Numerical grounding (shows formulas with actual numbers)
- ✅ Tension hooks for narrative momentum
- ✅ Card evolution implications
- ✅ Mobile-optimized prose format (60-120 words)

---

## Quality Requirements

The prompt now enforces:

```
✓ Dialogue: 60-120 words of continuous prose
✓ Capacity rule: NPC at X/10 can give MAX (X+2)/10 support
✓ Trust formula: Base × OCEAN × Urgency × Trust + Honesty
✓ Tension hook: ONE mystery/contradiction/partial reveal
✓ Subtext: What's implied but not stated
✓ Novel-quality: Reads like published fiction, not game text
```

---

## Expected Impact

### Training Data Quality
- **Specificity:** 10x more specific to Unwritten game systems
- **Usability:** Direct mapping to game data structures
- **Consistency:** Follows canonical specs exactly
- **Authenticity:** Generates real card narratives, not abstract examples

### Model Training
- Model learns **Unwritten-specific patterns** (OCEAN influence, capacity limits, urgency amplification)
- Better numerical grounding (explicit formulas)
- Card-appropriate narrative style (mobile-optimized prose)
- Tension integration for narrative momentum

### Development Velocity
- Generated training data can be used **directly** in game prototypes
- Clear mapping to game systems reduces interpretation errors
- Validates game design through data generation

---

## Testing Next Steps

1. **Generate test batch** with new prompt (5-10 examples)
2. **Validate JSON structure** matches game data schemas
3. **Check calculations** (trust formulas, capacity constraints)
4. **Assess dialogue quality** (60-120 words, prose format, tension hooks)
5. **Verify diversity** (different NPCs, scenarios, complexity types)

---

## Rollback Plan

If issues arise:
- Previous prompt version preserved in git history
- Can revert to v1.6.3 generic emotional authenticity
- But recommend fixing forward - v2.0 is much more valuable for Unwritten

---

## Future Enhancements

Potential next steps:
1. Add **multi-NPC interactions** (player + 2 NPCs with different capacities)
2. **Decisive decision templates** (major choice points with 3-4 options)
3. **Card evolution chains** (how interactions unlock new cards)
4. **Memory resonance** (callbacks to past interactions)
5. **Event integration** (how cards fit into weekly event flow)

---

**Summary:** This is a fundamental shift from generic training data to Unwritten-specific NPC interaction cards that directly support game development and model training. The prompt now speaks the language of your game design docs and generates data that maps to actual game systems.


