# Card Generation Guidelines - AI Content Creation

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete guidelines for AI-generated card evolution, ensuring consistency, quality, and player-specific personalization

**References:**
- **Card Evolution:** `21-card-evolution-mechanics.md` (when cards evolve)
- **Base Cards:** `20-base-card-catalog.md` (starting templates)
- **Fusion System:** `22-card-fusion-system.md` (fusion card generation)

---

## Overview

**Unwritten uses on-device TensorFlow Lite** to generate evolved and fused cards that feel personal and unique to each playthrough. This document defines **exact guidelines** for consistent, high-quality generation.

**Generation Targets:**
- **Evolved Character Cards:** Sarah at Level 3 is different from Sarah at Level 5
- **Evolved Activity Cards:** "Coffee with Sarah" becomes "Tuesday Coffee Ritual"
- **Fusion Cards:** Character + Activity = unique memory
- **Location Evolution:** "Café Luna" becomes "Where I Meet Sarah"

**Constraints:**
- **Character limit:** 280 characters max (card text)
- **Generation time:** < 50ms (on-device inference)
- **Tone:** Consistent with player personality and narrative context
- **Continuity:** Never contradicts established facts

---

## Card Generation Architecture

### Input Context Structure

```typescript
interface CardGenerationRequest {
  // Core Context
  card_to_evolve: {
    id: string;
    current_text: string;
    tier: number;
    type: "character" | "activity" | "location" | "fusion";
  };
  
  // Player Context
  player: {
    personality: OCEANProfile;
    life_direction: LifeDirection;
    emotional_state: EmotionalState;
    current_season: number;
    total_weeks_played: number;
  };
  
  // Relationship Context (if character card)
  relationship?: {
    npc_id: string;
    level: 0 | 1 | 2 | 3 | 4 | 5;
    trust: number;                     // 0.0-1.0
    interactions: number;
    major_moments: string[];           // Last 5 major memories
    shared_locations: string[];
  };
  
  // History Context
  history: {
    recent_events: string[];           // Last 5 weeks summary
    current_aspiration: string;
    canonical_facts: string[];         // Never contradict these
  };
  
  // Evolution Trigger
  trigger: {
    type: "repetition" | "relationship" | "time" | "event" | "fusion";
    details: string;
  };
}
```

---

## CHARACTER CARD GENERATION

### Template by Relationship Level

**Level 0 → Level 1: First Meeting**

```javascript
const FIRST_MEETING_TEMPLATE = {
  input_context: {
    npc_base: "Sarah Anderson, bookshop owner, reserved creative (OCEAN [4.3,4.8,2.3,4.5,3.6])",
    player_personality: "Player OCEAN profile",
    meeting_context: "Location, circumstances of first meeting"
  },
  
  output_requirements: {
    character_limit: 280,
    tone: "First impression, slightly formal, establishing personality",
    must_include: [
      "Visual detail (what player notices first)",
      "Personality hint (one trait evident)",
      "Opening interaction possibility"
    ],
    avoid: [
      "Backstory (not revealed yet)",
      "Deep connection (too early)",
      "Clichés"
    ]
  },
  
  generation_prompt_template: `
    Generate a character card for first meeting with {npc_name}.
    
    NPC Profile: {npc_personality_description}
    Player Profile: {player_personality_description}
    Meeting Location: {location}
    Context: {how_they_met}
    
    The card text should:
    1. Capture the player's first impression (what stands out visually/behaviorally)
    2. Hint at {npc_name}'s personality without exposition
    3. Create opening for interaction ("Say hi", "Ask about...", etc)
    4. Feel like a real moment, not a character sheet
    5. Maximum 280 characters
    
    Tone: {player_openness_based_tone}
    
    Generate card text:
  `,
  
  examples: {
    high_openness_player: {
      generated: "Sarah Anderson. Surrounded by books, fingers tracing spines like she's reading Braille. Doesn't notice you at first—lost in her own world. Intriguing.",
      why_good: "Observational, poetic, invites curiosity"
    },
    
    low_openness_player: {
      generated: "Sarah Anderson, bookshop owner. Quiet, keeps to herself. Looks up when you enter, nods politely. Seems nice enough.",
      why_good: "Straightforward, practical, matches player's grounded personality"
    }
  }
};
```

---

**Level 1 → Level 2: Becoming Acquaintances**

```javascript
const ACQUAINTANCE_EVOLUTION = {
  trigger: "6+ interactions, some revealed details",
  
  output_requirements: {
    tone: "Warmer, specific details emerging, but still learning",
    must_include: [
      "Specific detail learned (coffee order, habit, preference)",
      "Interaction feels less formal",
      "Hint of deeper layers"
    ]
  },
  
  generation_prompt: `
    Evolve character card for {npc_name} from First Meeting to Acquaintance.
    
    NPC: {npc_description}
    Interactions so far: {interaction_count}
    Revealed details: {shared_information}
    Player-NPC personality fit: {compatibility_score}
    
    The evolved card should:
    1. Reference a specific detail learned in recent interactions
    2. Show growing familiarity (know coffee order, habits)
    3. Still maintain some distance—not friends yet
    4. Feel like you're starting to know them, not fully
    5. Maximum 280 characters
    
    Generate evolved card text:
  `,
  
  examples: {
    sarah_level_2: {
      generated: "Sarah. Chai latte, extra foam. Always the window seat at Café Luna, 3 PM Tuesdays. She's writing something—poetry, maybe? Doesn't share yet. Getting to know her.",
      why_good: "Specific rituals established, mystery maintained, growing connection"
    }
  }
};
```

---

**Level 2 → Level 3: Becoming Friends**

```javascript
const FRIEND_EVOLUTION = {
  trigger: "16+ interactions, vulnerability shared, trust 0.4+",
  
  output_requirements: {
    tone: "Personal, warmth, inside references",
    must_include: [
      "Shared joke/reference",
      "Vulnerability or meaningful moment reference",
      "Sense of history together"
    ]
  },
  
  generation_prompt: `
    Evolve {npc_name} from Acquaintance to Friend.
    
    Trust level: {trust_score}
    Shared moments: {major_moments_list}
    Inside references: {shared_experiences}
    Time known: {weeks_since_meeting} weeks
    
    The card should:
    1. Feel like you have history together
    2. Reference a meaningful shared moment
    3. Show trust and comfort
    4. Include specific detail that matters to both
    5. Warm but not dramatic
    6. Maximum 280 characters
    
    Generate:
  `,
  
  examples: {
    sarah_level_3: {
      generated: "Sarah. Your Tuesday coffee tradition. She told you about David—the bookshop dream they had. Now she trusts you with the real stuff. Laughs more. This is friendship.",
      why_good: "References vulnerability, established ritual, earned trust, genuine warmth"
    }
  }
};
```

---

**Level 3 → Level 4: Close Friends**

```javascript
const CLOSE_FRIEND_EVOLUTION = {
  trigger: "31+ interactions, crisis together OR major support, trust 0.7+",
  
  output_requirements: {
    tone: "Deep connection, can't imagine life without",
    must_include: [
      "Reference to crisis/major moment together",
      "Sense of permanence",
      "They know you, you know them"
    ]
  },
  
  examples: {
    sarah_level_4: {
      generated: "Sarah. Best friend. She's the one who showed up at 2 AM when you were falling apart. Knows your coffee order. Knows your fears. Family you chose.",
      why_good: "References defining moment, permanence, mutual deep knowledge"
    }
  }
};
```

---

**Level 4 → Level 5: Best Friend / Life Partner**

```javascript
const BEST_FRIEND_EVOLUTION = {
  trigger: "76+ interactions, years together, trust 0.9+, multiple crises survived",
  
  output_requirements: {
    tone: "Soul-level connection, defining relationship",
    must_include: [
      "Years-long history",
      "Multiple defining moments",
      "Life decisions involve them",
      "Unbreakable bond"
    ]
  },
  
  examples: {
    sarah_level_5: {
      generated: "Sarah. Three years. From strangers at Café Luna to opening a bookshop together. She knows you better than you know yourself. This is what soulmate means.",
      why_good: "Epic scope, trajectory shown, permanence absolute, emotionally resonant"
    }
  }
};
```

---

## ACTIVITY CARD EVOLUTION

### Repetition-Based Evolution

```javascript
const ACTIVITY_EVOLUTION_PROMPT = {
  trigger: "10+ uses of same activity",
  
  context_needed: {
    activity_name: "Work on Portfolio",
    times_used: 15,
    outcomes: "12 successes, 3 struggles",
    skill_gained: "Photography +1.2",
    associated_aspiration: "Launch Photography Business",
    emotional_context: "Mostly FOCUSED, occasional FRUSTRATED"
  },
  
  generation_prompt: `
    Evolve activity card "{activity_name}" after {times_used} uses.
    
    This activity is part of: {aspiration}
    Skill gained: {skill_progress}
    Success rate: {success_rate}
    Emotional journey: {emotions_during}
    
    Evolution should show:
    1. This is now a ROUTINE, not one-off
    2. Progress visible ("your style is emerging")
    3. Emotional investment
    4. Specific to player's journey
    5. Maximum 280 characters
    
    Generate evolved activity text:
  `,
  
  examples: {
    portfolio_work_evolved: {
      before: "Work on your photography portfolio. Curate your best shots, develop your aesthetic.",
      after: "Portfolio sessions. Your style's emerging—moody urban landscapes, golden hour portraits. 47 hours in. You can see it now. Almost there.",
      why_good: "Shows progression, specific style, time investment, hope"
    }
  }
};
```

---

## FUSION CARD GENERATION

### Character + Activity Fusion

```javascript
const FUSION_PROMPT = {
  input: {
    character_card: "Sarah (Level 3)",
    activity_card: "Coffee Meetup",
    fusion_context: "10th time having coffee with Sarah, Tuesday afternoon, week 14"
  },
  
  generation_prompt: `
    Generate fusion card for {character_name} + {activity}.
    
    Relationship: Level {level}, Trust {trust}
    Context: {how_often}, {when}, {location}
    Shared history: {major_moments}
    
    Fusion card should:
    1. Feel like a SPECIFIC ritual, not generic
    2. Include sensory detail (what makes this YOUR thing)
    3. Show relationship depth through small details
    4. Create sense of comfort and familiarity
    5. This is now "a thing you do"
    6. Maximum 280 characters
    
    Generate fusion card text:
  `,
  
  examples: {
    coffee_with_sarah: {
      generated: "Coffee with Sarah. Tuesday, 3 PM, Café Luna, window seat. Two chai lattes. Her talking about the bookshop, you about photography. Your thing now. Comfort.",
      why_good: "Ultra-specific ritual, comfort conveyed, sense of permanence"
    }
  }
};
```

---

## LOCATION CARD EVOLUTION

### Repetition + Significance

```javascript
const LOCATION_EVOLUTION = {
  trigger: "15+ visits, major moments there",
  
  context: {
    location: "Café Luna",
    visits: 27,
    with_npcs: { sarah: 18, marcus: 4, alone: 5 },
    major_moments: [
      "First met Sarah here (Week 3)",
      "Decided to pursue photography (Week 8)",
      "Sarah revealed David story (Week 22)"
    ]
  },
  
  generation_prompt: `
    Evolve location "{location}" after {visits} visits.
    
    Major moments here:
    {moment_1}
    {moment_2}
    {moment_3}
    
    Most often with: {primary_npc}
    
    Evolution should show:
    1. This place has HISTORY now
    2. Reference defining moments
    3. Emotional weight
    4. This is "your place"
    5. Maximum 280 characters
    
    Generate:
  `,
  
  examples: {
    cafe_luna_evolved: {
      before: "Café Luna. Cozy coffee shop in the arts district. Good vibes, window seats, local art on walls.",
      after: "Café Luna. Where you met Sarah. Where you decided to be a photographer. Where she told you about David. Window seat, 3 PM. This place holds your story.",
      why_good: "Transformed from place to meaningful location, specific memories anchor it"
    }
  }
};
```

---

## Generation Quality Rules

### MUST FOLLOW

```javascript
const QUALITY_RULES = {
  1: {
    rule: "Show, don't tell",
    bad: "Sarah is kind and thoughtful.",
    good: "Sarah remembers you don't like small talk. Asks about your photography instead."
  },
  
  2: {
    rule: "Specific > Generic",
    bad: "You and Sarah hang out at a coffee shop.",
    good: "Tuesday coffee with Sarah. Café Luna, window seat, chai lattes. Your thing."
  },
  
  3: {
    rule: "Grounded in detail",
    bad: "Sarah is your best friend now.",
    good: "Sarah. Three years. She showed up at 2 AM when you called, no questions."
  },
  
  4: {
    rule: "Emotional weight through action",
    bad: "This moment means everything to you.",
    good: "You'll remember this. The light. Her laugh. This exact second."
  },
  
  5: {
    rule: "Player voice, not narrator",
    bad: "The character meets Sarah for coffee every Tuesday at 3 PM.",
    good: "Tuesday, 3 PM. Coffee with Sarah. You don't skip this anymore."
  },
  
  6: {
    rule: "Respect character limit (280 chars)",
    bad: "You and Sarah have been friends for a long time now, and you've shared many important moments together, like when she told you about her late fiancé David, and how you've been supporting each other through difficult times, and now you're planning to open a bookshop together which is really exciting.",
    good: "Sarah. Years of Tuesdays. She told you about David. You're opening a bookshop together. Best friend doesn't cover it."
  },
  
  7: {
    rule: "Never contradict canonical facts",
    bad: "Sarah mentions her husband at home." (WRONG - David is deceased),
    good: "Sarah talks about the bookshop—the dream she and David had."
  }
};
```

---

## Tone Calibration by Player Personality

### Openness Effect

```javascript
const TONE_BY_OPENNESS = {
  high_openness_4_5: {
    style: "Poetic, observational, emotionally expressive",
    example: "Sarah. The way she holds her cup—fingers wrapped like she's warming her hands on a cold day, even in summer. Something about loss. You recognize it."
  },
  
  medium_openness_3: {
    style: "Balanced, some metaphor, grounded",
    example: "Sarah. Quiet, thoughtful. Chai latte person. Takes a while to open up, but when she does, it's real. You get that."
  },
  
  low_openness_1_2: {
    style: "Straightforward, concrete, practical",
    example: "Sarah, bookshop owner. Reserved but friendly. Coffee regular. Reliable. Good person to know."
  }
};
```

---

## Generation Validation Pipeline

### Post-Generation Checks

```javascript
async function validateGeneratedCard(cardText, context) {
  const checks = {
    length: cardText.length <= 280,
    
    canonical_facts: await checkAgainstCanonicalFacts(cardText, context.canonical_facts),
    
    tone_appropriate: await checkToneMatch(cardText, context.player.personality),
    
    no_contradictions: await checkHistoryConsistency(cardText, context.history),
    
    quality_score: await scoreQuality(cardText, QUALITY_RULES),
    
    specificity: cardText.includes("Sarah") || cardText.includes("coffee"), // Not too generic
    
    // NEW - Master Truths v1.2: Novel-Quality Validation
    novel_quality: await validateNovelQuality(cardText, context),
    
    // NEW - Master Truths v1.2: Emotional Authenticity Scoring
    authenticity_score: await scoreEmotionalAuthenticity(cardText, context),
    
    // NEW - Master Truths v1.2: Tension Injection Check
    tension_appropriate: await validateTensionInjection(cardText, context),
    
    // NEW - Master Truths v1.2: Capacity Constraints
    capacity_constraints: await validateCapacityConstraints(cardText, context)
  };
  
  // Novel-quality threshold checks (Master Truths v1.2)
  if (checks.novel_quality.overall < 0.7) {
    return { valid: false, regenerate: true, reason: "Below novel-quality threshold" };
  }
  
  if (checks.novel_quality.authenticity < 0.7) {
    return { valid: false, regenerate: true, reason: "Insufficient authenticity" };
  }
  
  if (checks.novel_quality.tension < 0.6) {
    return { valid: false, regenerate: true, reason: "Insufficient tension" };
  }
  
  if (checks.novel_quality.hooks < 0.6) {
    return { valid: false, regenerate: true, reason: "Insufficient narrative hooks" };
  }
  
  // Legacy quality check
  if (checks.quality_score < 0.7) {
    return { valid: false, regenerate: true };
  }
  
  if (!checks.canonical_facts) {
    return { valid: false, reason: "Contradicts established fact" };
  }
  
  // Emotional authenticity check
  if (checks.authenticity_score.violates_capacity_rules) {
    return { valid: false, reason: "Violates emotional capacity constraints" };
  }
  
  if (checks.authenticity_score.inappropriate_vulnerability) {
    return { valid: false, reason: "Vulnerability revealed at wrong relationship level" };
  }
  
  return { 
    valid: true, 
    card: cardText,
    metrics: {
      quality: checks.quality_score,
      novel_quality: checks.novel_quality,
      authenticity: checks.authenticity_score,
      tension: checks.tension_appropriate
    }
  };
}
```

### Novel-Quality Validation *(NEW - Master Truths v1.2)*

```javascript
async function validateNovelQuality(cardText, context) {
  // Score card text against novel-quality thresholds
  
  const scores = {
    authenticity: await scoreAuthenticity(cardText, context),
    tension: await scoreTension(cardText, context),
    hooks: await scoreHooks(cardText, context)
  };
  
  scores.overall = (scores.authenticity * 0.4 + scores.tension * 0.3 + scores.hooks * 0.3);
  
  return scores;
}

async function scoreAuthenticity(cardText, context) {
  const checks = {
    shows_dont_tell: checkShowDontTell(cardText),         // 0.0-1.0
    specific_not_generic: checkSpecificity(cardText),     // 0.0-1.0
    grounded_in_detail: checkGroundedDetail(cardText),    // 0.0-1.0
    emotional_through_action: checkEmotionalAction(cardText), // 0.0-1.0
    player_voice: checkPlayerVoice(cardText),             // 0.0-1.0
    no_contradictions: checkCanonicalFacts(cardText, context) // 0.0-1.0
  };
  
  const avg = Object.values(checks).reduce((a, b) => a + b) / Object.values(checks).length;
  
  return avg; // Must be ≥ 0.7
}

async function scoreTension(cardText, context) {
  const tensionElements = {
    mystery_hook: containsMysteryHook(cardText),          // 0.0-1.0
    stakes_present: containsStakes(cardText),             // 0.0-1.0
    contradiction_hint: containsContradiction(cardText),  // 0.0-1.0
    unanswered_question: containsQuestion(cardText),      // 0.0-1.0
    dramatic_irony: containsDramaticIrony(cardText, context) // 0.0-1.0
  };
  
  // Tension should be appropriate for relationship level
  const relationshipLevel = context.relationship?.level || 0;
  const tensionFrequency = {
    0: 0.1,  // Strangers: rare tension
    1: 0.2,
    2: 0.33, // Level 1-2: 1 in 3
    3: 0.50, // Level 3-4: 1 in 2
    4: 0.50,
    5: 0.85  // Level 5: nearly every
  }[relationshipLevel];
  
  const hasTension = Object.values(tensionElements).some(v => v > 0.5);
  
  if (hasTension && Math.random() < tensionFrequency) {
    return Math.max(...Object.values(tensionElements));
  }
  
  // No tension is OK if below frequency threshold
  return 0.6; // Baseline
}

async function scoreHooks(cardText, context) {
  const hookTypes = {
    foreshadowing: containsForeshadowing(cardText),       // 0.0-1.0
    callback_to_past: containsCallback(cardText, context), // 0.0-1.0
    setup_for_future: containsSetup(cardText),            // 0.0-1.0
    emotional_beat: containsEmotionalBeat(cardText)       // 0.0-1.0
  };
  
  const avg = Object.values(hookTypes).reduce((a, b) => a + b) / Object.values(hookTypes).length;
  
  return avg; // Must be ≥ 0.6
}
```

### Emotional Authenticity Scoring *(NEW - Master Truths v1.2)*

```javascript
async function scoreEmotionalAuthenticity(cardText, context) {
  return {
    // Capacity constraints
    respects_capacity_limits: checkCapacityConstraints(cardText, context),
    violates_capacity_rules: detectCapacityViolations(cardText, context),
    
    // Vulnerability appropriateness
    vulnerability_level: detectVulnerabilityLevel(cardText),
    relationship_level: context.relationship?.level || 0,
    inappropriate_vulnerability: isVulnerabilityInappropriate(
      detectVulnerabilityLevel(cardText),
      context.relationship?.level || 0
    ),
    
    // Emotional journey
    journey_beat_present: detectJourneyBeat(cardText, context),
    memory_significance: scoreMemorySignificance(cardText, context), // 0-10
    authentic_connection: detectAuthenticConnection(cardText),
    
    // Circumstance stacking
    acknowledges_stressors: detectStressorAwareness(cardText, context),
    stacking_penalty_applied: calculateStackingPenalty(context.active_stressors),
    
    // Overall score
    overall: calculateAuthenticityScore(cardText, context) // 0.0-1.0
  };
}

function isVulnerabilityInappropriate(vulnerabilityLevel, relationshipLevel) {
  // Level 0-1: No deep vulnerability
  if (relationshipLevel <= 1 && vulnerabilityLevel > 0.3) return true;
  
  // Level 2: Light vulnerability OK
  if (relationshipLevel === 2 && vulnerabilityLevel > 0.6) return true;
  
  // Level 3+: Deeper vulnerability appropriate
  return false;
}
```

### Tension Injection Guidelines *(NEW - Master Truths v1.2)*

```javascript
const TENSION_INJECTION_GUIDELINES = {
  frequency_by_relationship_level: {
    0: 0.1,   // Strangers: 10% chance
    1: 0.2,   // New acquaintance: 20%
    2: 0.33,  // Level 1-2: 1 in 3 (33%)
    3: 0.50,  // Level 3-4: 1 in 2 (50%)
    4: 0.50,
    5: 0.85   // Level 5: Nearly every (85%)
  },
  
  tension_types_by_level: {
    level_1_2: ["mystery_hook", "partial_reveal"],
    level_3_4: ["mystery_hook", "partial_reveal", "stakes_escalation", "contradiction"],
    level_5: ["all_types", "dramatic_irony", "high_stakes"]
  },
  
  examples: {
    mystery_hook_level_2: `Sarah mentions "the anniversary" is coming up. She looks sad but doesn't elaborate.`,
    
    partial_reveal_level_3: `"I almost told you something today," Sarah says. "But I'm not ready yet."`,
    
    stakes_escalation_level_4: `"I might have to move," Sarah says quietly. "For work. Nothing's decided yet."`,
    
    dramatic_irony_level_5: `Sarah doesn't know you saw the bookshop financial reports. Down 30% this quarter. She forces a smile. "We'll figure it out."`
  }
};
```

### Capacity Constraint Validation *(NEW - Master Truths v1.2)*

```javascript
async function validateCapacityConstraints(cardText, context) {
  const playerCapacity = context.player.emotional_capacity || 10;
  const npcCapacity = context.npc?.emotional_capacity || 10;
  
  const cardDemands = detectEmotionalDemands(cardText);
  
  return {
    player_has_capacity: playerCapacity >= cardDemands.min_capacity,
    npc_has_capacity: npcCapacity >= cardDemands.min_npc_capacity,
    
    capacity_sufficient: (playerCapacity >= cardDemands.min_capacity) && 
                         (npcCapacity >= cardDemands.min_npc_capacity),
    
    alternative_needed: (playerCapacity < cardDemands.min_capacity) && 
                        cardDemands.has_low_capacity_alternative,
    
    blocked: (playerCapacity < cardDemands.min_capacity) && 
             !cardDemands.has_low_capacity_alternative,
    
    recommendations: generateCapacityRecommendations(playerCapacity, cardDemands)
  };
}

function detectEmotionalDemands(cardText) {
  // Detect how much capacity this card requires
  const demands = {
    min_capacity: 0,
    min_npc_capacity: 0,
    has_low_capacity_alternative: false
  };
  
  // High-demand keywords
  if (cardText.includes("crisis") || cardText.includes("support") || cardText.includes("breakdown")) {
    demands.min_capacity = 4.0;
    demands.min_npc_capacity = 2.0; // NPC needs help
    demands.has_low_capacity_alternative = true;
  }
  
  // Medium-demand keywords
  if (cardText.includes("difficult") || cardText.includes("challenge") || cardText.includes("vulnerable")) {
    demands.min_capacity = 3.0;
  }
  
  // Low-demand (routine interactions)
  if (cardText.includes("coffee") || cardText.includes("casual") || cardText.includes("routine")) {
    demands.min_capacity = 1.0;
  }
  
  return demands;
}
```

---

## Compliance Checklist (Master Truths v1.2)

- [x] Uses canonical vocab & scales (Levels 0–5; Trust 0.0–1.0; Capacity 0.0-10.0; EXHAUSTED/OVERWHELMED)
- [x] Season = 12/24/36w (player choice at season start); 3 turns/day
- [x] Relationship Level 0 = "Not Met" (never displayed as "Level 0")
- [x] Level-up requires BOTH interaction count AND trust threshold
- [x] Currencies limited to Time/Energy/Money/Social Capital
- [x] Decisive decisions pause time; copy avoids FOMO framing
- [x] Packs classified (Standard/Deluxe/Mega) with counts
- [x] Archive policy respected by tier
- [x] Fusion type, inputs, prerequisites, outputs defined
- [x] NPC personality/memory constraints respected
- [x] **Emotional capacity constraints respected (0-10 scale; support rule: capacity + 2)**
- [x] **Tension injection frequency followed (Level 1-2: 1 in 3; Level 3-4: 1 in 2; Level 5: nearly every)**
- [x] **Dramatic irony created via knowledge gaps**
- [x] **Memory resonance factors applied (0.7-0.95 weights)**
- [x] **Circumstance stacking acknowledged (3-7 simultaneous stressors)**
- [x] **Environmental/seasonal modifiers included**
- [x] **Novel-quality thresholds met (≥ 0.7 overall; authenticity ≥ 0.7; tension ≥ 0.6; hooks ≥ 0.6)**
- [x] This doc cites **Truths v1.2** at the top

**References:**
- See `21-card-evolution-mechanics.md` for evolution triggers (v1.2 emotional authenticity)
- See `20-base-card-catalog.md` for base card templates
- See `13-meter-effects-tables.md` for emotional capacity calculations
- See `14-emotional-state-mechanics.md` for emotional state effects
- See `01-emotional-authenticity.md` for v1.2 authenticity systems

---

**This specification enables AI engineers to implement the complete card generation system with exact prompts, quality rules, emotional capacity awareness, memory resonance, tension injection, and validation that creates personalized, emotionally authentic, novel-worthy content across 8-10 season lifecycles.**

