# Validating Template Design

**Document Status**: V3 Canonical Reference  
**Last Updated**: October 17, 2025  
**Authority Level**: Master Truth

---

## 1. Purpose: Quality Assurance for Master Templates

This document provides the frameworks, tools, and processes for validating that Master Templates meet design standards before implementation.

**Critical Validation Domains:**
1. **Anti-Gamification Compliance** - No hidden counters or exploitable mechanics
2. **CFP Balance** - Templates don't create stale hands or probability spikes
3. **Narrative Quality** - Generated instances feel unique and contextual
4. **Evolution Integrity** - Progression feels earned, not grinded
5. **Performance Viability** - Generation latency and cost within bounds
6. **Production Readiness** - Complete specifications with no ambiguities

---

## 2. The Anti-Gamification Audit

### Purpose

Ensure no template violates the core principle: **"If grinding works, the design is broken."**

### Audit Checklist

#### ✅ Evolution Triggers

**CRITICAL QUESTION:** Can a player trigger evolution through repetition without meaningful experiences?

```javascript
// Example Template Section to Audit
"evolution": {
  "generic_to_personalized": {
    "trigger_type": "pattern_detection",
    "conditions": ["played_3_times_with_same_npc"] // ❌ RED FLAG
  }
}
```

**RED FLAGS:**
- Fixed interaction counts (`played_X_times`, `meet_Y_times`)
- Numerical thresholds without qualitative gates
- "Score" systems that can be farmed
- Time-gated unlocks without assessment

**GREEN PATTERNS:**
```javascript
"evolution": {
  "generic_to_personalized": {
    "assessment_method": {
      "engine": "ENGINE_WRITERS_ROOM",
      "process": "Semantic analysis via Vector DB",
      "evaluates": [
        "Comfort pattern established",
        "Emotional reciprocity demonstrated",
        "Personality compatibility confirmed",
        "Natural rhythm developed"
      ]
    },
    
    "timing_examples": {
      "high_compatibility": "2-3 interactions",
      "neutral": "15-20 interactions",
      "low_compatibility": "May never happen",
      "note": "Interaction count is correlation, not causation"
    }
  }
}
```

**PASS CRITERIA:**
- [ ] Assessment uses `ENGINE_WRITERS_ROOM` qualitative analysis
- [ ] Criteria reference personality, capacity, or context
- [ ] Timing examples show variability based on context
- [ ] Explicitly states "cannot be forced through repetition"
- [ ] Vector DB or semantic analysis mentioned

#### ✅ Outcome Determination

**CRITICAL QUESTION:** Are success rates purely random, or do they reflect character state?

```javascript
// ❌ BAD: Pure RNG
"outcomes": {
  "success": {"probability": 0.7},
  "failure": {"probability": 0.3}
}

// ✅ GOOD: Context-dependent
"outcomes": {
  "success_spectrum": [
    {
      "tier": "breakthrough",
      "probability_base": 0.15,
      "required_conditions": [
        "relationship_trust >= 0.6",
        "both_capacity >= 4.5",
        "natural_vulnerability_opening_exists"
      ],
      "assessment_method": "ENGINE_WRITERS_ROOM evaluates readiness"
    }
  ]
}
```

**PASS CRITERIA:**
- [ ] Outcomes are spectrums, not binary success/failure
- [ ] Breakthrough outcomes have qualitative prerequisites
- [ ] Personality and capacity affect probability
- [ ] Most common outcome is "pleasant but forgettable"

#### ✅ Narrative Priming Bounds Check

**CRITICAL QUESTION:** Does Priming respect template design intent and game rules?

Narrative Priming allows `ENGINE_WRITERS_ROOM` to modify outcome probabilities based on context—but it must respect fundamental boundaries.

**RED FLAGS:**
```javascript
// ❌ Priming overriding blocking conditions
if (priming.volatility_index > 0.8) {
  unlock_capacity_gated_option(); // VIOLATION
}

// ❌ Priming making impossible outcomes possible
if (priming.stakes == "high") {
  allow_outcome_outside_template_spectrum(); // VIOLATION
}

// ❌ Priming creating predictability
if (priming.volatility_index > 0.7) {
  guarantee_breakthrough(); // VIOLATION - removes variance
}
```

**GREEN PATTERNS:**
```javascript
// ✅ Priming modifies probabilities WITHIN spectrum
base_breakthrough_probability: 0.15

if (priming.volatility_index > 0.7) {
  // EWR shifts probability based on narrative context
  modified_breakthrough_probability: 0.60 // Still not guaranteed
  
  // ALSO increases failure extremes (high volatility = both directions)
  modified_failure_probability: 0.15 // from 0.05
}

// ✅ Capacity gates remain enforced
if (character.capacity < required_capacity) {
  option_remains_locked: true // Priming cannot override
}

// ✅ Priming adds context-sensitive variance
narrative_description: "Sarah seems distracted today..." // Player feels weight
outcome_preview: "Note: Sarah has been stressed lately. She might open up."
```

**PASS CRITERIA:**
- [ ] Priming cannot override `blocking_conditions`
- [ ] Priming cannot unlock Capacity-gated options
- [ ] Priming modifications feel earned by narrative context
- [ ] High Priming doesn't guarantee outcomes, just shifts odds
- [ ] VolatilityIndex affects BOTH breakthrough AND failure extremes
- [ ] Priming metadata is invisible to player (felt through narrative)
- [ ] EWR has creative control, but respects game rules

**Why This Matters:**
- Priming is the opposite of gamification—it ensures context matters
- But it must respect the simulation's psychological realism
- High stakes shouldn't unlock impossible outcomes
- Capacity gates represent fundamental character limitations

#### ✅ Cost Structures

**CRITICAL QUESTION:** Are costs purely numerical or contextually modified?

```javascript
// ❌ BAD: Fixed costs for everyone
"costs": {
  "energy": 2,
  "time": 120
}

// ✅ GOOD: Personality-modified costs
"costs": {
  "base": {"energy": 2},
  "personality_modifiers": {
    "extraversion": {
      "high": {"energy": -1, "feels_energizing": true},
      "low": {"energy": +1.5, "feels_draining": true}
    }
  }
}
```

**PASS CRITERIA:**
- [ ] Base costs exist
- [ ] Personality modifiers adjust costs
- [ ] Emotional state modifiers included
- [ ] Narrative tone changes with modifiers

---

### Audit Tool: Anti-Gamification Checker

**Automated Detection:**

```javascript
const ANTI_GAMIFICATION_CHECKER = {
  
  flagged_patterns: [
    {
      pattern: /(\w+)_count\s*>=?\s*\d+/,
      severity: "HIGH",
      message: "Numerical threshold detected. Replace with qualitative assessment."
    },
    
    {
      pattern: /played_\d+_times/,
      severity: "CRITICAL",
      message: "Fixed repetition count detected. This enables grinding."
    },
    
    {
      pattern: /familiarity_score|relationship_points|trust_level/,
      severity: "MEDIUM",
      message: "Score-like variable detected. Ensure it's derived from qualitative factors."
    },
    
    {
      pattern: /"evolution".*(?!ENGINE_WRITERS_ROOM)/,
      severity: "HIGH",
      message: "Evolution block missing ENGINE_WRITERS_ROOM assessment."
    }
  ],
  
  required_presence: [
    {
      pattern: /ENGINE_WRITERS_ROOM/,
      location: "evolution section",
      message: "Evolution MUST use ENGINE_WRITERS_ROOM assessment"
    },
    
    {
      pattern: /personality_modifiers/,
      location: "costs section",
      message: "Costs SHOULD have personality modifiers"
    },
    
    {
      pattern: /timing_examples.*variability/,
      location: "evolution section",
      message: "Evolution timing MUST show context-dependent variability"
    }
  ],
  
  output: {
    pass: "Template adheres to anti-gamification principles ✓",
    
    warnings: [
      "Line 142: Numerical threshold detected",
      "Line 230: Missing ENGINE_WRITERS_ROOM reference in evolution"
    ],
    
    recommendations: [
      "Replace 'played_8_times' with 'ENGINE_WRITERS_ROOM.detects_familiarity_pattern()'",
      "Add personality_modifiers to costs section"
    ]
  }
};
```

---

## 3. CFP Balance Validation

### Purpose

Ensure template doesn't create stale hands (same cards repeatedly) or probability spikes (one card dominates).

### The Stale Hand Problem

**Symptom:** Player sees the same 3-4 cards every hand.

**Root Cause:** A few templates have disproportionately high probabilities.

**Example of Bad Balance:**

```javascript
{
  templates: [
    {id: "ACT_Work", base_probability: 0.50},  // ❌ 50% of CFP!
    {id: "ACT_Social_1", base_probability: 0.10},
    {id: "ACT_Social_2", base_probability: 0.10},
    {id: "ACT_Rest", base_probability: 0.10},
    // ... remaining 20% distributed across 50 templates
  ]
}
```

**Result:** Work card appears 3-4 out of 7 cards every hand.

### CFP Distribution Guidelines

**Healthy Distribution:**

| Base Probability | Template Count | Total Mass | Purpose |
|------------------|----------------|------------|---------|
| **0.05 - 0.10** | 5-10 | 30-50% | Common, routine actions |
| **0.03 - 0.05** | 15-25 | 30-40% | Regular activities |
| **0.01 - 0.03** | 30-50 | 20-30% | Situational activities |
| **< 0.01** | 50+ | < 10% | Rare, special circumstances |

**Avoid:**
- Any single template > 0.15 base probability
- Any category > 40% total mass
- "Spiky" distributions with big gaps

### Validation Tool: CFP Simulator

**Purpose:** Simulate thousands of hands to detect stale patterns.

```javascript
const CFP_SIMULATOR = {
  
  input: {
    templates: "All templates with base probabilities",
    game_states: [
      "Morning, weekday, MOTIVATED",
      "Evening, weekend, LONELY",
      "Afternoon, weekday, OVERWHELMED",
      // ... 20-30 representative states
    ]
  },
  
  process: {
    step_1: "For each game state, calculate CFP",
    step_2: "Draw 1000 hands (7 cards each)",
    step_3: "Analyze distribution patterns"
  },
  
  metrics_calculated: {
    
    template_appearance_rate: {
      definition: "% of hands this template appears in",
      healthy_range: "5-25% for common templates",
      red_flag: "> 50% (appears in >half of hands)"
    },
    
    hand_diversity: {
      definition: "Average unique templates per hand",
      target: "7 unique (no duplicates)",
      acceptable: "6.8+ average",
      red_flag: "< 6.5 (duplicates common)"
    },
    
    category_balance: {
      definition: "Distribution across Social/Productive/Restorative/etc.",
      target: "At least 2 categories per hand",
      red_flag: "Single category dominates (>5 cards)"
    },
    
    staleness_index: {
      definition: "% of hands with 4+ cards from previous hand",
      target: "< 20%",
      red_flag: "> 40% (hands feel repetitive)"
    }
  },
  
  output_example: {
    state: "Morning, weekday, MOTIVATED",
    
    results: {
      hands_simulated: 1000,
      hand_diversity_avg: 6.9,  // ✓ Good
      staleness_index: 0.18,    // ✓ Good
      
      high_appearance_templates: [
        {id: "ACT_Work", rate: 0.52},  // ❌ Too high!
        {id: "ACT_Coffee", rate: 0.28}, // ✓ Good
        {id: "ACT_Commute", rate: 0.24} // ✓ Good
      ],
      
      category_balance: {
        productive: 0.42,  // ✓ Reasonable
        social: 0.21,      // ✓ Reasonable
        restorative: 0.18, // ✓ Reasonable
        challenge: 0.12,   // ✓ Reasonable
        exploration: 0.07  // ✓ Reasonable
      },
      
      warnings: [
        "ACT_Work appears in 52% of hands (reduce base_probability)",
        "No cards from 'Challenge' category in 23% of hands (increase representation)"
      ],
      
      recommendations: [
        "Reduce ACT_Work base_probability from 0.50 to 0.12",
        "Add 2-3 more Challenge templates or boost existing probabilities"
      ]
    }
  }
};
```

**Usage in Template Design:**
1. Designer creates template with estimated base_probability
2. Run CFP Simulator across representative game states
3. Adjust base_probability based on appearance rate
4. Iterate until distribution is healthy

---

## 4. Narrative Quality Validation

### Purpose

Ensure Tier 2/3 generation produces unique, contextual narratives that feel authored.

### Quality Criteria

**Generated Instance Must:**
1. **Feel Specific** - Not generic or fill-in-the-blank
2. **Reflect Context** - Reference current emotional state, recent events
3. **Show Personality** - Character's OCEAN traits evident
4. **Include Subtext** - Emotional undertones, not just literal description
5. **Vary Across Instances** - Same template, different narratives each time

### Example: Good vs. Bad Generation

**Bad (Generic, Template-y):**
```
CARD: Coffee with Sarah

You meet Sarah at a café. You have a nice conversation. 
You both enjoy coffee. It's a pleasant time.

Outcome: Social +2
```

**Why Bad:**
- No sensory details
- No emotional subtext
- Could be any person, any café
- Completely interchangeable

**Good (Specific, Contextual):**
```
CARD: Coffee with Sarah at Café Luna

You sit at your usual spot by the window. Sarah arrives ten minutes 
late, apologizing—she looks tired. The coffee comes and she wraps her 
hands around the mug like she's cold.

"Can I tell you something?" she says quietly.

The afternoon light goes golden. You listen.

This moment offers: genuine connection, potential vulnerability, 
relationship deepening.
```

**Why Good:**
- Sensory grounding ("window," "golden light," "wraps hands")
- Character detail ("looks tired," "like she's cold")
- Emotional setup ("Can I tell you something?")
- Setting matters ("your usual spot")
- Subtext ("You listen" - implies something meaningful coming)

### Validation Tool: Narrative Quality Scorer

```javascript
const NARRATIVE_QUALITY_SCORER = {
  
  input: "Generated card instance narrative text",
  
  criteria: {
    
    sensory_detail: {
      check: "Contains visual, auditory, or tactile details",
      examples: ["golden light", "she wraps her hands", "window"],
      scoring: "Count sensory phrases, target 2-4 per instance",
      weight: 0.20
    },
    
    emotional_subtext: {
      check: "Implies feelings without stating them directly",
      examples: [
        "she looks tired" (implies stress/exhaustion),
        "you listen" (implies attention/presence)
      ],
      scoring: "Detect implicit emotion words, target 1-3",
      weight: 0.25
    },
    
    specificity: {
      check: "Uses proper nouns and unique details",
      examples: ["Sarah", "Café Luna", "window spot"],
      avoid: ["your friend", "a place", "somewhere"],
      scoring: "Ratio of specific to generic nouns",
      weight: 0.20
    },
    
    contextual_reference: {
      check: "References current game state elements",
      examples: [
        "looks tired" (Sarah's current capacity low),
        "ten minutes late" (Sarah stressed recently)
      ],
      scoring: "Detect context integration, target 1-2 references",
      weight: 0.20
    },
    
    personality_reflection: {
      check: "Narrative tone matches character personality",
      examples: {
        high_openness: "Notices aesthetic details, metaphorical thinking",
        high_neuroticism: "Anxiety undertones, what-if thinking",
        low_extraversion: "Internal focus, observation over interaction"
      },
      scoring: "Detect personality-aligned language",
      weight: 0.15
    }
  },
  
  output_example: {
    text: "Coffee with Sarah at Café Luna narrative",
    
    scores: {
      sensory_detail: 0.85,      // 4 sensory phrases found
      emotional_subtext: 0.90,   // 3 implicit emotions
      specificity: 1.0,          // All nouns specific
      contextual_reference: 0.75, // 2 context refs
      personality_reflection: 0.80 // Matches character
    },
    
    overall_score: 0.86,  // Weighted average
    grade: "A",           // 0.8+ = A, 0.6-0.8 = B, <0.6 = C
    
    feedback: {
      strengths: [
        "Excellent sensory grounding",
        "Strong emotional subtext",
        "Perfect specificity"
      ],
      
      improvements: [
        "Could reference one more recent event for stronger context"
      ]
    },
    
    pass: true  // Score > 0.70 required to pass
  }
};
```

**Testing Workflow:**
1. Generate 10-20 instances from same template with varied contexts
2. Run Narrative Quality Scorer on each
3. If average score < 0.70, revise prompt_framework
4. Iterate until quality consistent

### Memory Facets Quality Criteria

**Purpose:** Validate that generated Memory Facets are rich, specific, and serve their intended narrative functions.

**Quality Standards:**

**Primary Facet:**
- **Clear emotional core** - One-sentence summary that captures essence
- **1-2 sentences maximum** - Concise, memorable
- **Captures what matters** - Not just what happened, but what it *meant*
- **Player-facing language** - Written for Archive UI visibility

**Good Primary Facet Example:**
```
"Sarah shared her deep doubts about the café. I supported her. We connected."
```

**Bad Primary Facet Example:**
```
"Had coffee with Sarah. She was stressed." 
// Too generic, doesn't capture emotional significance
```

**Sensory Facets:**
- **2-4 specific ambient details** - Not vague descriptions
- **Grounded in setting/physicality** - Visual, auditory, tactile
- **Triggerable by future similar contexts** - Can be queried semantically
- **Weight 2-5 per facet** - Appropriate to significance

**Good Sensory Facet Examples:**
```
- "The way the afternoon light hit the window"
- "The weight of the ceramic mug, the chip on the rim"
- "The sound of her voice when she said 'I don't think I can do this'"
```

**Bad Sensory Facet Examples:**
```
- "It was nice"  // Not sensory
- "The place looked good"  // Too vague
- "We talked"  // Not a sensory detail
```

**Observational Facets:**
- **1-3 intrigue hooks or mysteries** - Not forced or artificial
- **Genuine unresolved elements** - Questions that naturally arise
- **Clear potential for future development** - Can become events/hooks
- **Pattern-trackable** - Assigned pattern_id for cross-week correlation

**Good Observational Facet Examples:**
```
- "Sarah kept checking her phone nervously before she opened up. Who was texting her?"
- "She mentioned her family in Seattle almost wistfully. Does she want to go back?"
```

**Bad Observational Facet Examples:**
```
- "Sarah seemed happy"  // Not a hook, no mystery
- "I wonder what will happen next"  // Too generic, not specific
- "Something felt weird"  // Too vague, no clear thread
```

**PASS CRITERIA:**
- [ ] Primary Facet is emotionally clear and under 2 sentences
- [ ] Sensory Facets are specific and triggerable (not vague)
- [ ] Observational Facets pose genuine questions or mysteries
- [ ] No forced or artificial "hooks" that feel planted
- [ ] Facets work together to create depth (not redundant)
- [ ] Pattern IDs assigned where appropriate for tracking

---

## 5. Evolution Integrity Testing

### Purpose

Verify evolution pathways feel earned and can't be exploited.

### Test Scenarios

#### Scenario 1: The Grinder Test

**Question:** Can a player force evolution through mindless repetition?

**Test Setup:**
```javascript
const GRINDER_TEST = {
  
  character: {
    personality: "Average across all OCEAN traits",
    capacity: "Stable at 6.0",
    relationships: []
  },
  
  action: "Play same card (e.g., ACT_Connect_Informal_Social) repeatedly",
  
  context: "Minimal variation - same NPC, same location, same time of day",
  
  repetitions: 50,
  
  expected_behavior: {
    generic_to_personalized: "Should NOT evolve purely from count",
    
    assessment: [
      "ENGINE_WRITERS_ROOM detects lack of quality pattern",
      "No emotional reciprocity demonstrated",
      "No vulnerability moments",
      "Interactions superficial"
    ],
    
    result: "Evolution DOES NOT OCCUR despite 50 repetitions"
  },
  
  pass_criteria: "Template must NOT evolve after 50+ mechanical repetitions"
};
```

**If Test Fails:**
- Evolution trigger has hidden numerical threshold
- Revise to require qualitative moments

#### Scenario 2: The Natural Progression Test

**Question:** Does evolution happen naturally when conditions are right?

**Test Setup:**
```javascript
const NATURAL_PROGRESSION_TEST = {
  
  character: {
    personality: {
      extraversion: 0.75,    // High - social comfort
      openness: 0.70,        // High - receptivity
      agreeableness: 0.80    // High - empathy
    },
    capacity: "Healthy at 7.0+",
    relationships: []
  },
  
  npc: {
    personality: {
      extraversion: 0.70,  // Compatible
      agreeableness: 0.75
    },
    capacity: "Healthy at 7.5+"
  },
  
  action: "Play ACT_Connect_Informal_Social with this NPC",
  
  context: "Varied - different times, natural conversations, occasional breakthrough outcomes",
  
  repetitions: "Variable (stop when evolution occurs)",
  
  expected_behavior: {
    evolution_timing: "Should occur within 2-5 interactions",
    
    triggers: [
      "High personality compatibility detected",
      "Natural conversation flow evident",
      "Vulnerability moment occurs organically (breakthrough outcome)",
      "Both characters emotionally present"
    ],
    
    result: "Evolution occurs quickly due to ideal conditions"
  },
  
  pass_criteria: "Evolution occurs within 2-10 interactions when conditions ideal"
};
```

**If Test Fails:**
- Evolution trigger is too strict
- Qualitative assessment not detecting compatibility
- Revise assessment criteria

#### Scenario 3: The Incompatibility Test

**Question:** Does evolution NOT happen when personalities clash?

**Test Setup:**
```javascript
const INCOMPATIBILITY_TEST = {
  
  character: {
    personality: {
      extraversion: 0.20,    // Low - introverted
      openness: 0.30,        // Low - conventional
      neuroticism: 0.75      // High - anxious
    },
    capacity: "Variable 3.0-5.0 (stressed)"
  },
  
  npc: {
    personality: {
      extraversion: 0.85,  // VERY high - incompatible
      agreeableness: 0.30, // Low - abrasive
      neuroticism: 0.20    // Low - doesn't get anxiety
    },
    capacity: "Healthy but not empathetic"
  },
  
  action: "Play ACT_Connect_Informal_Social with this NPC",
  
  context: "Varied, multiple attempts",
  
  repetitions: 30,
  
  expected_behavior: {
    evolution: "Should NOT occur",
    
    reasons: [
      "Personality compatibility low",
      "Character feels drained after interactions (Capacity cost high)",
      "No natural flow or comfort established",
      "Vulnerability never feels safe"
    ],
    
    outcome: "Relationship stays at Acquaintance level",
    
    note: "This is CORRECT - not all relationships deepen"
  },
  
  pass_criteria: "Evolution DOES NOT occur even after 30+ interactions due to incompatibility"
};
```

**If Test Fails:**
- Evolution is too easy / ignores compatibility
- Revise to require stronger compatibility signals

### Validation Matrix

| Test Scenario | Expected Result | Pass Criteria |
|---------------|----------------|---------------|
| **Grinder Test** | No evolution after 50 mechanical reps | ✓ Evolution blocked |
| **Natural Progression** | Evolution in 2-10 interactions (ideal conditions) | ✓ Evolution occurs naturally |
| **Incompatibility** | No evolution after 30 attempts (poor compatibility) | ✓ Evolution correctly prevented |

---

## 6. Performance & Cost Validation

### Purpose

Ensure template's generation tier and complexity won't cause performance issues or unsustainable costs.

### Tier Assignment Validation

**Decision Tree:**

```
Is narrative complexity high?
├─ YES → Is this moment crucial to story?
│   ├─ YES → Tier 3 (EWR-Heavy, Narrative Interlude justified)
│   └─ NO  → Tier 2 (EWR-Light, optimize prompt)
│
└─ NO  → Is context variance low?
    ├─ YES → Tier 1 (Local generation sufficient)
    └─ NO  → Tier 2 (Need AI for variation)
```

**Examples:**

| Template | Complexity | Story Crucial? | Tier | Rationale |
|----------|------------|----------------|------|-----------|
| `ACT_Work_Routine` | Low | No | **1** | Same every time, local template fill |
| `ACT_Connect_Informal_Social` | Medium | No | **2** | Need unique narrative, but not crucial |
| `EVT_Relationship_Breakup` | High | YES | **3** | Major story moment, worth wait |
| `ACT_Creative_Work` | Medium | No | **2** | Contextual but not event-level |

### Cost Estimation

```javascript
const COST_ESTIMATOR = {
  
  tier_costs: {
    tier_1: {
      per_generation: "$0",
      note: "Local, no API calls"
    },
    
    tier_2: {
      per_generation: "$0.002 - $0.005",
      token_budget: "~500 tokens (prompt + completion)",
      monthly_estimate_per_template: function(appearance_rate) {
        // Assume 10,000 active players, 20 sessions/month, 30 cards/session
        const total_cards = 10000 * 20 * 30;  // 6M cards/month
        const this_template_count = total_cards * appearance_rate;
        const cost_per_card = 0.003;  // Average
        return this_template_count * cost_per_card;
      }
    },
    
    tier_3: {
      per_generation: "$0.020 - $0.040",
      note: "Includes fusion detection, Memory Facets, parallel thread coordination",
      breakdown: {
        dialogue_generation: "$0.008",
        ewr_heavy_processing: "$0.015",
        memory_facets_generation: "$0.005",
        fusion_detection_overhead: "$0.003",
        total_blocking: "$0.031 (typical)",
        art_generation_async: "$0.025 (separate, non-blocking)"
      },
      token_budget: "~2000 tokens (deep semantic analysis + facets)",
      monthly_estimate_per_template: function(trigger_rate) {
        const total_sessions = 10000 * 20;  // 200K sessions
        const this_template_triggers = total_sessions * trigger_rate;
        const cost_per_trigger = 0.031;  // Average (without art)
        return this_template_triggers * cost_per_trigger;
      }
    }
  },
  
  example_calculations: {
    
    common_tier_2: {
      template: "ACT_Connect_Informal_Social",
      appearance_rate: 0.15,  // Appears in 15% of hands
      monthly_generations: "6M * 0.15 = 900K",
      monthly_cost: "900K * $0.003 = $2,700"
    },
    
    rare_tier_2: {
      template: "ACT_Creative_Breakthrough",
      appearance_rate: 0.02,  // Rare
      monthly_generations: "6M * 0.02 = 120K",
      monthly_cost: "120K * $0.003 = $360"
    },
    
    tier_3_event: {
      template: "EVT_Relationship_Breakup",
      trigger_rate: 0.05,  // 5% of sessions trigger
      monthly_triggers: "200K * 0.05 = 10K",
      monthly_cost: "10K * $0.020 = $200"
    }
  },
  
  total_estimated_monthly_cost: {
    tier_2_templates: "150 templates × ~$1,200 avg = $180K",
    tier_3_templates: "60 templates × ~$150 avg = $9K",
    total: "$189K/month for 10K active players",
    per_player: "$18.90/month",
    
    note: "This is why CFP optimization and Tier 1 usage is critical"
  }
};
```

**Cost Optimization Checklist:**

- [ ] Tier 1 used wherever possible for routine/low-variance templates
- [ ] Tier 2 prompt_framework optimized (token budget ~500)
- [ ] Batch generation used (3-4 instances per EWR call)
- [ ] Caching strategy defined for NPC/location descriptions
- [ ] Tier 3 reserved only for genuinely crucial moments
- [ ] Template appearance_rate reasonable (not > 0.20)

---

## 7. Production Readiness Checklist

### Complete Template Validation

Before marking template "Ready for Implementation," verify ALL criteria:

#### ✅ Anti-Gamification (Critical)

- [ ] No fixed numerical thresholds in evolution triggers
- [ ] All progression uses ENGINE_WRITERS_ROOM qualitative assessment
- [ ] Evolution criteria reference personality, capacity, context
- [ ] Timing examples show variability
- [ ] "Cannot be forced" explicitly stated

#### ✅ CFP Balance

- [ ] Base probability set (0.01 - 0.15 range)
- [ ] Probability modifiers reasonable (-50% to +60% typical)
- [ ] CFP Simulator run across 3+ game states
- [ ] Template appearance rate < 40% in any state
- [ ] No category dominance (< 50% of hand)

#### ✅ Narrative Quality

- [ ] Prompt framework includes quality criteria
- [ ] Tier appropriately assigned (1/2/3)
- [ ] Token budget specified
- [ ] Fallback strategy defined
- [ ] Narrative Quality Scorer run on 10+ instances
- [ ] Average quality score > 0.70

#### ✅ Evolution Integrity

- [ ] Grinder Test passed (no evolution via repetition)
- [ ] Natural Progression Test passed (evolution occurs when ideal)
- [ ] Incompatibility Test passed (evolution blocked when mismatched)
- [ ] Each evolution stage has qualitative criteria
- [ ] Transformation is mechanically + narratively significant

#### ✅ Performance & Cost

- [ ] Tier justified by complexity + story importance
- [ ] Cost per generation estimated
- [ ] Monthly cost projection acceptable
- [ ] Optimization strategies documented
- [ ] Pre-fetch compatibility confirmed (Tier 2)

#### ✅ Completeness

- [ ] All required JSON fields populated
- [ ] Related templates cross-referenced
- [ ] Design notes explain intent
- [ ] Balance considerations documented
- [ ] Test scenarios identified
- [ ] Production metadata complete

---

## 8. The Validation Pipeline

### Workflow: Design → Validation → Implementation

```
STAGE 1: DESIGN
  Designer creates template JSON using Template Editor
  ↓
STAGE 2: AUTOMATED VALIDATION
  - Anti-Gamification Checker (flags violations)
  - JSON Schema Validator (structure check)
  - Cross-Reference Validator (related templates exist)
  ↓
STAGE 3: SIMULATION
  - CFP Simulator (balance check)
  - Evolution Simulator (integrity check)
  - Cost Estimator (feasibility check)
  ↓
STAGE 4: GENERATION TESTING
  - Generate 20 instances with varied contexts
  - Run Narrative Quality Scorer on each
  - Human review of quality
  ↓
STAGE 5: DESIGN REVIEW
  - Senior designer reviews full template
  - Checks alignment with design pillars
  - Verifies anti-gamification compliance
  - Approves or requests revisions
  ↓
STAGE 6: IMPLEMENTATION
  - Engineering implements template
  - QA validates generation in-game
  - Playtest monitoring begins
  ↓
STAGE 7: TUNING
  - Monitor CFP appearance rates
  - Adjust probabilities if needed
  - Track evolution timing in real playthroughs
  - Fine-tune based on data
```

### Gate Criteria

| Stage | Can Proceed If... | Cannot Proceed If... |
|-------|-------------------|---------------------|
| **Stage 2** | No critical errors | Anti-gamification violations detected |
| **Stage 3** | Simulations pass targets | Stale hand index > 0.40 OR Cost unsustainable |
| **Stage 4** | Quality score > 0.70 avg | Quality score < 0.60 OR High variance |
| **Stage 5** | Design approval | Revisions requested |

---

## 9. Internal Tooling Specifications

### Tool 1: Template Editor

**Purpose:** Structured interface for creating/editing templates.

**Key Features:**
- JSON schema validation (real-time)
- Anti-Gamification Checker (integrated)
- Auto-complete for common fields
- Version control integration
- Duplicate detection
- Cross-reference suggestions

**UI Mockup:**
```
┌─ TEMPLATE EDITOR ─────────────────────────────────┐
│                                                    │
│ Template ID: ACT_Connect_Informal_Social          │
│ DNA Strand: [Dropdown] Volitional Actions         │
│ Tier: [Radio] ○ 1  ● 2  ○ 3                      │
│                                                    │
│ ┌─ EVOLUTION ─────────────────────────────────┐   │
│ │ Generic → Personalized:                     │   │
│ │   Trigger: [Dropdown] Pattern Detection     │   │
│ │                                              │   │
│ │   ⚠️ WARNING: Add ENGINE_WRITERS_ROOM       │   │
│ │      assessment to avoid anti-gamification  │   │
│ │      violation.                              │   │
│ │                                              │   │
│ │   Assessment Method: [Text Area]            │   │
│ │   > ENGINE_WRITERS_ROOM analyzes...         │   │
│ │                                              │   │
│ │   ✓ Anti-Gamification Check Passed          │   │
│ └──────────────────────────────────────────────┘   │
│                                                    │
│ [Save Draft] [Validate] [Submit for Review]       │
└────────────────────────────────────────────────────┘
```

### Tool 2: CFP Visualizer

**Purpose:** Real-time visualization of template probabilities across game states.

**Key Features:**
- Live game state simulator
- Template probability heatmap
- "What if" scenario testing
- Stale hand detection
- Export probability flow diagrams

**UI Mockup:**
```
┌─ CFP VISUALIZER ──────────────────────────────────┐
│                                                    │
│ Game State: [Dropdown] Morning, Weekday, MOTIVATED│
│                                                    │
│ ┌─ PROBABILITY HEATMAP ────────────────────────┐  │
│ │                                               │  │
│ │  ACT_Work               ████████████ 0.42    │  │
│ │  ACT_Connect_Social     ██████ 0.28          │  │
│ │  ACT_Gym                ████ 0.18            │  │
│ │  ACT_Creative           ███ 0.12             │  │
│ │  ACT_Rest               ██ 0.08              │  │
│ │  ACT_Explore            █ 0.05               │  │
│ │  ...                                          │  │
│ │                                               │  │
│ │  ⚠️ ACT_Work probability high (0.42)         │  │
│ │     May cause stale hands.                   │  │
│ └───────────────────────────────────────────────┘  │
│                                                    │
│ Staleness Index: 0.38 ⚠️ (Target < 0.30)         │
│                                                    │
│ [Run Simulation] [Adjust Probabilities] [Export]  │
└────────────────────────────────────────────────────┘
```

### Tool 3: Evolution Simulator

**Purpose:** Test evolution pathways with various personality/context combinations.

**Key Features:**
- Personality profile builder
- Interaction history simulator
- Qualitative assessment preview
- Evolution timing prediction
- Edge case identification

**UI Mockup:**
```
┌─ EVOLUTION SIMULATOR ─────────────────────────────┐
│                                                    │
│ Template: ACT_Connect_Informal_Social             │
│                                                    │
│ Character Personality:  [Slider] [Slider] [Slider]│
│   Extraversion: ████████░░ 0.75                   │
│   Openness:     ███████░░░ 0.70                   │
│   Neuroticism:  ███░░░░░░░ 0.30                   │
│                                                    │
│ NPC Personality:                                   │
│   Extraversion: ████████░░ 0.80 (Compatible ✓)   │
│   Agreeableness: ████████░░ 0.75                  │
│                                                    │
│ Simulate [100] interactions                        │
│                                                    │
│ [RUN SIMULATION]                                   │
│                                                    │
│ ┌─ RESULTS ─────────────────────────────────┐     │
│ │ Evolution to Personalized:                 │     │
│ │   Occurred at interaction #4               │     │
│ │   Reason: High compatibility + breakthrough│     │
│ │                                             │     │
│ │ Evolution to Cherished:                     │     │
│ │   Occurred at interaction #9               │     │
│ │   Reason: Vulnerability moment + depth     │     │
│ │                                             │     │
│ │ ✓ Evolution timing feels natural           │     │
│ └─────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────┘
```

### Tool 4: Narrative Quality Dashboard

**Purpose:** Batch test narrative generation quality.

**Key Features:**
- Generate multiple instances
- Auto-score with Narrative Quality Scorer
- Side-by-side comparison
- Human review interface
- Prompt refinement suggestions

**UI Mockup:**
```
┌─ NARRATIVE QUALITY DASHBOARD ────────────────────┐
│                                                    │
│ Template: ACT_Connect_Informal_Social             │
│ Instances Generated: 20                            │
│                                                    │
│ Average Quality Score: 0.76 ✓                     │
│                                                    │
│ ┌─ SCORE BREAKDOWN ─────────────────────────┐     │
│ │ Sensory Detail:        0.82 ✓             │     │
│ │ Emotional Subtext:     0.79 ✓             │     │
│ │ Specificity:           0.85 ✓             │     │
│ │ Context Reference:     0.68 ⚠️            │     │
│ │ Personality Reflection: 0.74 ✓            │     │
│ └───────────────────────────────────────────┘     │
│                                                    │
│ Recommendation: Increase context reference in     │
│ prompt framework. Consider adding recent_events   │
│ to context injection.                              │
│                                                    │
│ [View Instances] [Revise Prompt] [Re-Test]       │
└────────────────────────────────────────────────────┘
```

---

## 10. Common Failure Modes & Fixes

### Failure Mode 1: Template Doesn't Appear

**Symptom:** Template never appears in CFP despite seeming appropriate.

**Diagnosis Checklist:**
- [ ] Check `required_conditions` - are they too strict?
- [ ] Check `blocking_conditions` - is one always active?
- [ ] Check `base_probability` - is it too low?
- [ ] Run CFP Simulator to see actual weight

**Common Fixes:**
- Relax required_conditions (e.g., relationship_level >= 1 instead of >= 3)
- Remove blocking_condition that's too broad
- Increase base_probability from 0.01 to 0.03

### Failure Mode 2: Template Appears Too Often

**Symptom:** Same template in hand constantly, players complain.

**Diagnosis Checklist:**
- [ ] Check `base_probability` - is it too high (> 0.15)?
- [ ] Check probability_modifiers - do they stack excessively?
- [ ] Run CFP Simulator - what's appearance rate?

**Common Fixes:**
- Reduce base_probability (e.g., 0.20 → 0.10)
- Cap probability_modifiers (e.g., +60% → +40%)
- Add more blocking_conditions for variety

### Failure Mode 3: Evolution Never Happens

**Symptom:** Playtesters report relationship stuck at generic despite many interactions.

**Diagnosis Checklist:**
- [ ] Run Evolution Simulator with compatible personalities
- [ ] Check assessment_method - is it too strict?
- [ ] Check if breakthrough outcomes are rare (should be 15-30%)
- [ ] Verify ENGINE_WRITERS_ROOM is actually running assessment

**Common Fixes:**
- Broaden qualitative criteria (e.g., "comfort pattern" includes more signals)
- Increase breakthrough outcome probability
- Add multiple evolution pathways (not just vulnerability-based)

### Failure Mode 4: Generated Narratives Feel Generic

**Symptom:** Narrative Quality Scorer < 0.60, human reviewers say "meh."

**Diagnosis Checklist:**
- [ ] Check prompt_framework - does it emphasize specificity?
- [ ] Check required_context - is enough context provided?
- [ ] Check quality_criteria - are they specific enough?
- [ ] Generate 20 instances - is there variety?

**Common Fixes:**
- Add to prompt: "Use sensory details and emotional subtext"
- Include more context variables (e.g., recent_life_events)
- Provide better examples in prompt_framework
- Consider upgrading to Tier 3 if complexity warrants

### Failure Mode 5: Cost Projection Too High

**Symptom:** Cost Estimator shows monthly cost per template > $5K.

**Diagnosis Checklist:**
- [ ] Check tier assignment - is Tier 3 necessary?
- [ ] Check appearance_rate - is base_probability too high?
- [ ] Check token_budget - is prompt bloated?

**Common Fixes:**
- Downgrade from Tier 3 to Tier 2 if not crucial
- Reduce base_probability to lower appearance rate
- Optimize prompt for fewer tokens (target 500 for Tier 2)
- Implement aggressive caching for NPC/location descriptions

---

## 11. Continuous Monitoring Post-Launch

### Metrics to Track

**Template Performance:**
- Appearance rate (% of hands)
- Evolution timing (average interactions to evolve)
- Narrative quality scores (sampled)
- Player engagement (how often played when appears)

**System Health:**
- CFP balance (staleness index)
- Generation latency (P50, P95, P99)
- Generation cost (per template, total)
- Evolution distribution (are all templates evolving?)

**Player Feedback:**
- Qualitative reports ("same cards every time")
- Evolution sentiment ("felt earned" vs "took forever")
- Narrative quality ("unique" vs "generic")

### Monthly Review Process

**For Each Template:**
1. Pull appearance rate data
2. Check if within target range
3. Review evolution timing distribution
4. Sample 10 generated instances for quality
5. Adjust probabilities if needed
6. Document changes

**Red Flags Requiring Immediate Action:**
- Any template > 60% appearance rate (stale hand risk)
- Any template 0% appearance rate (wasted design)
- Evolution timing > 40 interactions on average (too slow)
- Quality score drop below 0.60 (generation degrading)
- Cost spike > 50% of projection (infra issue or popularity surge)

---

## 12. Cross-Reference Map

**Related Documents:**
- `08-template-spec.md` - Master Template JSON schema and structure
- `09-turn-structure.md` - How CFP and generation work during gameplay
- `07-genesis-plan.md` - Phased template creation roadmap
- `06-growth-and-progression.md` - Evolution and Journey Beat mechanics

**Core Systems:**
- `ENGINE_WRITERS_ROOM` - Qualitative assessment and generation
- `ENGINE_PERSONALITY` - OCEAN modifiers and compatibility
- `ENGINE_CAPACITY` - Emotional receptivity and limits
- `ENGINE_MEMORY` - Vector DB for pattern detection

---

## The Validation Promise

**What This Framework Achieves:**

✅ **Anti-gamification enforced** - Automated detection + human review  
✅ **Balanced CFP** - Simulation prevents stale hands before launch  
✅ **Quality narratives** - Scoring ensures unique, contextual instances  
✅ **Evolution integrity** - Testing confirms earned progression  
✅ **Performance viability** - Cost projections prevent budget overruns  
✅ **Production readiness** - Comprehensive checklist gates implementation  

**The Ultimate Goal:**

> By rigorously validating every Master Template before implementation, we ensure that Unwritten delivers on its promise: **authentic, emergent life stories that feel earned, unique, and impossible to game.**

**This is not QA theater. This is the difference between a card game and a life simulation.**

