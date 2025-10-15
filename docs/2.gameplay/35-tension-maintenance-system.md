# Tension Maintenance & Hook Point System - Implementation

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete system for maintaining narrative tension with personality-based perception and dynamic adjustment

**References:**
- **Arc Structure:** `31-narrative-arc-scaffolding.md` (3-act beats)
- **Decision Templates:** `30-decisive-decision-templates.md` (high-tension moments)
- **Event Generation:** `32-event-generation-rules.md` (tension-appropriate events)

---

## Overview

**Tension** is the player's emotional investment in "what happens next." The system maintains appropriate tension through hook points (unanswered questions), mysteries (long-term intrigue), and dynamic tension curves that match narrative structure.

**Core Principle:** Players should always have 2-3 unresolved hooks creating forward momentum, with tension rising and falling in rhythm with the 3-act structure.

**Compliance:** master_truths v1.1 requires "no FOMO, no anxiety mechanics" - tension should create intrigue, not stress.

---

## Hook Point System

### What is a Hook Point?

**Definition:** An unresolved narrative thread that creates anticipation for resolution.

```typescript
interface HookPoint {
  id: string;
  title: string;
  type: "question" | "promise" | "threat" | "opportunity" | "mystery";
  
  introduced_week: number;
  target_resolution_week: number;
  
  tension_level: number;              // 0.0-1.0
  player_knowledge: "full" | "partial" | "oblivious";
  
  resolution_path: "decisive_decision" | "complication" | "arc_climax" | "slow_burn";
  
  tags: string[];
  affects_arcs: string[];
}
```

---

### Hook Types

```javascript
const HOOK_TYPES = {
  question: {
    description: "An unanswered question creating curiosity",
    examples: [
      "Why has Sarah been so distant lately?",
      "What did the boss mean by 'changes coming'?",
      "Will the client approve the portfolio?"
    ],
    tension_pattern: "rises until answered",
    typical_duration: "2-8 weeks"
  },
  
  promise: {
    description: "Something anticipated that hasn't happened yet",
    examples: [
      "Marcus promised to introduce you to his gallery contact 'soon'",
      "The big presentation is in 3 weeks",
      "Your first paid photography gig is scheduled for Saturday"
    ],
    tension_pattern: "rises as date approaches",
    typical_duration: "1-4 weeks"
  },
  
  threat: {
    description: "Potential negative consequence looming",
    examples: [
      "Rent is due and you're $200 short",
      "Boss mentioned 'performance review' next month",
      "Client seems unhappy with drafts"
    ],
    tension_pattern: "high and sustained until resolved",
    typical_duration: "1-6 weeks"
  },
  
  opportunity: {
    description: "Potential positive outcome requiring action",
    examples: [
      "Gallery owner mentioned 'we might have a slot opening up'",
      "Friend offered to connect you with someone important",
      "Job posting for dream position just appeared"
    ],
    tension_pattern: "moderate, spikes if deadline approaches",
    typical_duration: "2-8 weeks"
  },
  
  mystery: {
    description: "Long-term intrigue with slow reveals",
    examples: [
      "Who is David that Sarah mentions sometimes?",
      "Why did Marcus really leave his last job?",
      "What happened to make your mentor so cynical?"
    ],
    tension_pattern: "low background tension, spikes on reveals",
    typical_duration: "12-36+ weeks (can span seasons)"
  }
};
```

---

## Hook Point Management

### Active Hook Rules

```javascript
const HOOK_MANAGEMENT_RULES = {
  optimal_active_hooks: {
    minimum: 2,                        // Always at least 2 active
    maximum: 5,                        // Never more than 5 simultaneously
    sweet_spot: 3,                     // 3 is ideal
    
    rationale: "2 = forward momentum, 3 = rich story, 5+ = overwhelming"
  },
  
  hook_distribution: {
    short_term: 1-2,                   // Resolve within 1-4 weeks
    medium_term: 1-2,                  // Resolve within 4-12 weeks  
    long_term: 0-1,                    // Mysteries spanning 12+ weeks
    
    example: {
      short: "Will client approve portfolio? (2 weeks)",
      medium: "Why is Sarah distant? (8 weeks)",
      long: "Who is David? (season-long mystery)"
    }
  },
  
  tension_balance: {
    high_tension_hooks: 1,             // One threat/deadline
    moderate_hooks: 1-2,               // Questions/opportunities
    low_tension_hooks: 1,              // Slow-burn mysteries
    
    example: {
      high: "Rent due, $200 short (threat)",
      moderate: "Marcus's gallery contact intro (promise)",
      low: "David mystery (long-term intrigue)"
    }
  }
};
```

---

### Hook Lifecycle

```javascript
function manageHookLifecycle(currentWeek, activeHooks, seasonPlan) {
  // PHASE 1: Introduction
  function introduceHook(hook) {
    return {
      week: hook.introduced_week,
      card: generateHookIntroCard(hook),
      narrative_beat: hook.title,
      tension_level: calculateInitialTension(hook.type),
      
      example: {
        type: "question",
        card: "Sarah cancels coffee plans. Again. She says she's busy, but her voice sounds... off.",
        creates_question: "Why is Sarah avoiding you?"
      }
    };
  }
  
  // PHASE 2: Development (keep tension alive)
  function developHook(hook, weeksSinceIntro) {
    const developmentCards = [];
    
    // Reminder every 2-4 weeks
    if (weeksSinceIntro % 3 === 0) {
      developmentCards.push({
        type: "reminder",
        card: generateReminderCard(hook),
        tension_adjustment: +0.1,
        
        example: "You see Sarah's car parked at the coffee shop. She said she was too busy to meet..."
      });
    }
    
    // Escalation if approaching deadline
    if (hook.target_resolution_week - currentWeek <= 2) {
      developmentCards.push({
        type: "escalation",
        card: generateEscalationCard(hook),
        tension_adjustment: +0.3,
        
        example: "Two weeks until rent is due. Still $200 short. Time is running out."
      });
    }
    
    return developmentCards;
  }
  
  // PHASE 3: Resolution
  function resolveHook(hook, resolutionType) {
    return {
      week: hook.target_resolution_week,
      resolution_card: generateResolutionCard(hook, resolutionType),
      tension_release: 0.8,
      creates_new_hooks: generateFollowUpHooks(hook, resolutionType),
      
      example: {
        resolution: "Sarah finally opens up: 'Today is David's birthday. He was my fiancé. He died 2 years ago.'",
        mystery_solved: "David identity revealed",
        creates_new: "How do you support Sarah through grief?"
      }
    };
  }
  
  return {
    introduce: introduceHook,
    develop: developHook,
    resolve: resolveHook
  };
}
```

---

## Mystery System

### Long-Term Mysteries

```javascript
const MYSTERY_STRUCTURE = {
  definition: "Season-spanning (or multi-season) narrative thread with slow reveals",
  
  characteristics: {
    duration: "12-36+ weeks",
    tension_type: "Low background intrigue with periodic spikes",
    resolution: "Major reveal or gradual understanding",
    purpose: "Create long-term engagement and character depth"
  },
  
  mystery_template: {
    id: "sarah_david_mystery",
    title: "Who is David?",
    category: "npc_backstory",
    
    // CLUE TRAIL
    clues: [
      {
        week: 4,
        reveal_type: "mention",
        content: "Sarah: 'David would have loved this place.' (wistful)",
        player_learns: "David is someone from Sarah's past",
        tension: 0.2
      },
      {
        week: 9,
        reveal_type: "photograph",
        content: "You notice a photo in Sarah's apartment. Young man, arm around Sarah. Both smiling. Photo is face-down when you visit next time.",
        player_learns: "David was significant, Sarah still emotional about him",
        tension: 0.4
      },
      {
        week: 14,
        reveal_type: "behavioral_clue",
        content: "Sarah seems sad every August 14th. Won't explain why. Marcus knows but won't say - 'It's Sarah's story to tell.'",
        player_learns: "August 14 is significant, Marcus knows the story",
        tension: 0.5
      },
      {
        week: 18,
        reveal_type: "partial_reveal",
        content: "Sarah, after a few drinks: 'I was engaged once. It... didn't work out.' She won't elaborate.",
        player_learns: "David was Sarah's fiancé, relationship ended badly",
        tension: 0.6
      },
      {
        week: 24,
        reveal_type: "full_reveal",
        content: "Today is August 14. Sarah finally tells you: David was killed in a car accident 2 years ago. They were planning the wedding. She's been afraid to get close to anyone since.",
        player_learns: "Complete story, recontextualizes all of Sarah's behavior",
        tension: 1.0 → 0.0 (release),
        emotional_weight: 9,
        affects_relationship: "Trust +0.4, new understanding, deeper bond"
      }
    ],
    
    pacing: "Clue every 4-6 weeks, full reveal at Act III",
    player_agency: "Can ask Sarah directly (she deflects until ready) OR wait for reveal",
    carries_across_seasons: true,
    affects_future: "Sarah's fear of commitment becomes understandable context"
  }
};
```

---

## Tension Curve System

### Act-Based Tension Patterns

```javascript
const TENSION_CURVES = {
  standard_12_week: {
    act_1_setup: {
      weeks: [1, 3],
      tension_pattern: "0.3 → 0.5",
      description: "Gentle rise, establishing intrigue",
      
      target_curve: [
        { week: 1, tension: 0.3, reason: "New season, fresh start, gentle hooks" },
        { week: 2, tension: 0.4, reason: "First complications hinted" },
        { week: 3, tension: 0.5, reason: "Act I climax, stakes established" }
      ]
    },
    
    act_2_complications: {
      weeks: [4, 9],
      tension_pattern: "0.5 → 0.8 (peaks and valleys)",
      description: "Rising action with breathing room",
      
      target_curve: [
        { week: 4, tension: 0.5, reason: "Post-Act I reset" },
        { week: 5, tension: 0.6, reason: "Complication #1 develops" },
        { week: 6, tension: 0.8, reason: "Decisive Decision #1 (midpoint)" },
        { week: 7, tension: 0.5, reason: "Breathing room post-decision" },
        { week: 8, tension: 0.7, reason: "Complication #2 + consequences" },
        { week: 9, tension: 0.8, reason: "Pre-climax crisis" }
      ]
    },
    
    act_3_resolution: {
      weeks: [10, 12],
      tension_pattern: "0.8 → 1.0 → 0.2",
      description: "Climax spike then release",
      
      target_curve: [
        { week: 10, tension: 0.9, reason: "Final push begins" },
        { week: 11, tension: 1.0, reason: "CLIMAX - decisive decision" },
        { week: 12, tension: 0.2, reason: "Resolution, reflection, closure" }
      ]
    }
  },
  
  // Similar patterns for 24w and 36w seasons (scaled)
};
```

---

## Dynamic Tension Adjustment

### Real-Time Tension Management

```javascript
function calculateCurrentTension(gameState, activeHooks, recentEvents) {
  let baseTension = 0.5; // Neutral
  
  // Factor 1: Active hook contributions
  const hookTension = activeHooks.reduce((sum, hook) => {
    const weeksActive = gameState.currentWeek - hook.introduced_week;
    const weeksUntilDeadline = hook.target_resolution_week - gameState.currentWeek;
    
    let hookContribution = hook.tension_level * 0.2; // Base contribution
    
    // Increase if approaching deadline
    if (weeksUntilDeadline <= 2 && weeksUntilDeadline > 0) {
      hookContribution *= 1.5;
    }
    
    // Increase if unresolved for too long (frustration)
    if (weeksActive > 8) {
      hookContribution *= 1.2;
    }
    
    return sum + hookContribution;
  }, 0);
  
  // Factor 2: Meter states (low meters = stress = tension)
  const meterTension = calculateMeterTension(gameState.meters);
  
  // Factor 3: Recent decisive decisions (post-decision = lower tension)
  const recentDecisionWeeks = getWeeksSinceLastDecision(recentEvents);
  const decisionTension = recentDecisionWeeks < 2 ? -0.2 : 0;
  
  // Factor 4: Act position (Act II should be higher than Act I)
  const actPositionTension = calculateActPositionTension(gameState.currentWeek, gameState.seasonLength);
  
  const totalTension = Math.max(0, Math.min(1.0, 
    baseTension + hookTension + meterTension + decisionTension + actPositionTension
  ));
  
  return {
    current: totalTension,
    target: getTargetTension(gameState.currentWeek, gameState.seasonLength),
    adjustment_needed: totalTension < getTargetTension() - 0.2 ? "increase" : totalTension > getTargetTension() + 0.2 ? "decrease" : "maintain"
  };
}

function adjustTensionIfNeeded(currentTension, targetTension, activeHooks) {
  if (currentTension < targetTension - 0.2) {
    // TENSION TOO LOW - inject hook
    return {
      action: "introduce_hook",
      hook_type: selectAppropriateHookType(currentTension, targetTension),
      urgency: "within_2_weeks",
      
      examples: [
        "Introduce threat (rent due, money short)",
        "Introduce question (NPC acting strange)",
        "Introduce promise (opportunity mentioned)"
      ]
    };
  }
  
  if (currentTension > targetTension + 0.2) {
    // TENSION TOO HIGH - provide relief
    return {
      action: "resolve_minor_hook",
      target: activeHooks.find(h => h.tension_level < 0.6),
      provide_breathing_room: true,
      
      examples: [
        "Resolve one small question",
        "Provide partial progress on goal",
        "Positive social moment (friend support)"
      ]
    };
  }
  
  return {
    action: "maintain",
    status: "Tension within target range"
  };
}
```

---

## Master Truths v1.2: Personality-Based Tension Perception *(NEW - Gap 5.1)*

### Objective vs Subjective Tension

**Purpose:** Same situation creates different tension for different personalities - high neuroticism amplifies, low neuroticism reduces.

```javascript
const PERSONALIZED_TENSION_SYSTEM = {
  core_principle: "Objective reality vs subjective experience",
  
  tension_types: {
    objective: {
      definition: "What's actually happening (situation severity)",
      scale: "0.0-1.0 universal",
      example: "Job performance review in 2 weeks = objective 6.0"
    },
    
    subjective: {
      definition: "What player experiences (personality-filtered)",
      scale: "0.0-1.0 personalized",
      modifiers: ["neuroticism", "conscientiousness", "past_experiences"]
    },
    
    differential: {
      definition: "perceived - objective",
      interpretation: {
        positive: "Player feels more tension than situation warrants (anxiety amplification)",
        near_zero: "Player's perception matches reality",
        negative: "Player underestimates tension (may be unaware of risks)"
      }
    }
  }
};
```

---

### Neuroticism-Based Tension Amplification

**High Neuroticism:** Amplifies tension, anticipatory anxiety, stress spillover.

```javascript
const HIGH_NEUROTICISM_TENSION = {
  amplification_factor: function(neuroticism_score) {
    // Neuroticism 0.0-5.0 scale
    // High = 3.5+, Very High = 4.5+
    
    if (neuroticism_score >= 4.5) return 1.8;  // 80% amplification
    if (neuroticism_score >= 4.0) return 1.6;  // 60% amplification
    if (neuroticism_score >= 3.5) return 1.4;  // 40% amplification
    return 1.0;  // No amplification below 3.5
  },
  
  example_scenario: {
    situation: "Job performance review in 2 weeks",
    objective_tension: 6.0,
    
    high_neuroticism_player: {
      neuroticism_score: 4.3,
      amplification_factor: 1.5,
      perceived_tension: 9.0,  // 6.0 * 1.5 = 9.0
      
      internal_experience: `
        Two weeks. The review is in two weeks.
        
        You can't stop thinking about it.
        Every small mistake at work feels like evidence.
        Your anxiety amplifies everything.
        
        To you, this feels like 9/10. To someone else? Maybe 6/10.
        But you've never been someone else.
      `,
      
      behavioral_effects: {
        sleep_affected: true,
        intrusive_thoughts: true,
        stress_spillover: "affects other life areas",
        rumination_cards: [
          "You lie awake replaying work mistakes",
          "During coffee with Sarah, you can't focus",
          "Your physical meter drops from stress"
        ]
      }
    },
    
    narrative_reflects_perception: true,
    meter_effects: {
      mental: -2,  // Anxiety drains mental meter
      physical: -1  // Stress affects sleep/health
    }
  }
};
```

**Low Neuroticism:** Reduces tension, stays calm, proportional responses.

```javascript
const LOW_NEUROTICISM_TENSION = {
  reduction_factor: function(neuroticism_score) {
    // Neuroticism 0.0-5.0 scale
    // Low = 0.0-2.0, Very Low = 0.0-1.5
    
    if (neuroticism_score <= 1.5) return 0.65;  // 35% reduction
    if (neuroticism_score <= 2.0) return 0.75;  // 25% reduction
    if (neuroticism_score <= 2.5) return 0.85;  // 15% reduction
    return 1.0;  // No reduction above 2.5
  },
  
  example_scenario: {
    situation: "Job performance review in 2 weeks",
    objective_tension: 6.0,
    
    low_neuroticism_player: {
      neuroticism_score: 1.8,
      reduction_factor: 0.75,
      perceived_tension: 4.5,  // 6.0 * 0.75 = 4.5
      
      internal_experience: `
        Performance review in two weeks. Okay.
        
        You're not worried. Maybe you should be?
        But you've never been good at anxiety.
        You'll prepare, do your best, and see what happens.
        
        To you, this feels manageable. Maybe 4/10.
        You know people who'd be panicking right now.
        You're just... not.
      `,
      
      behavioral_effects: {
        sleep_unaffected: true,
        calm_approach: true,
        proportional_response: "Prepares without spiraling"
      }
    },
    
    narrative_reflects_perception: true,
    meter_effects: {
      mental: 0,  // Calm = no mental drain
      physical: 0  // No stress symptoms
    }
  }
};
```

---

### Threshold Variance by Personality

**Breaking Point Differs by Personality Composition**

```javascript
const BREAKING_POINT_THRESHOLDS = {
  high_resilience_profile: {
    traits: {
      neuroticism: "<= 2.5",
      conscientiousness: ">= 3.5",
      agreeableness: ">= 3.0"
    },
    
    tension_threshold: 8.5,  // Can handle high tension
    
    narrative: "You can handle a lot. Always have. It takes a lot to break you.",
    
    example_player: {
      OCEAN: { O: 3.2, C: 4.2, E: 3.5, A: 4.0, N: 2.0 },
      breaking_point: 8.5,
      
      at_tension_7: "Stressed, but functioning. You've been here before.",
      at_tension_8: "This is hard. But you keep going.",
      at_tension_8_5: "You're at your limit. Can't take much more.",
      at_tension_9: "Breaking. This is too much. Even for you."
    }
  },
  
  moderate_resilience_profile: {
    traits: {
      neuroticism: "2.5-3.5",
      conscientiousness: "2.5-3.5",
      varies: "Mixed other traits"
    },
    
    tension_threshold: 7.0,  // Average breaking point
    
    narrative: "You can handle a normal amount of stress. Most people's limit is yours too.",
    
    example_player: {
      OCEAN: { O: 3.0, C: 3.0, E: 3.0, A: 3.0, N: 3.0 },
      breaking_point: 7.0,
      
      at_tension_6: "Getting difficult. You're feeling the strain.",
      at_tension_7: "At capacity. Can't take on anything else.",
      at_tension_7_5: "Overwhelmed. Breaking point passed.",
      at_tension_8: "Way past limit. Everything's crumbling."
    }
  },
  
  low_resilience_profile: {
    traits: {
      neuroticism: ">= 3.5",
      conscientiousness: "<= 2.5",
      emotional_meter: "often low"
    },
    
    tension_threshold: 5.5,  // Lower breaking point
    
    narrative: "You hit your limit faster than most. Not weakness. Just how you're wired.",
    
    example_player: {
      OCEAN: { O: 2.5, C: 2.0, E: 2.5, A: 3.5, N: 4.2 },
      breaking_point: 5.5,
      
      at_tension_5: "This is a lot. You're struggling.",
      at_tension_5_5: "Too much. You're at your breaking point.",
      at_tension_6: "Overwhelmed. Can't function. Need help.",
      at_tension_7: "Complete breakdown. Everything's impossible."
    }
  },
  
  calculation: function(player_personality, player_meters) {
    let base_threshold = 7.0;
    
    // Neuroticism effects (strongest factor)
    if (player_personality.neuroticism >= 4.0) base_threshold -= 2.0;
    else if (player_personality.neuroticism >= 3.5) base_threshold -= 1.0;
    else if (player_personality.neuroticism <= 2.0) base_threshold += 1.5;
    else if (player_personality.neuroticism <= 2.5) base_threshold += 0.5;
    
    // Conscientiousness effects
    if (player_personality.conscientiousness >= 4.0) base_threshold += 0.5;
    else if (player_personality.conscientiousness <= 2.0) base_threshold -= 0.5;
    
    // Agreeableness effects (support-seeking)
    if (player_personality.agreeableness >= 4.0) base_threshold += 0.5;
    
    // Current emotional meter (situational modifier)
    if (player_meters.emotional <= 3) base_threshold -= 1.0;
    else if (player_meters.emotional >= 7) base_threshold += 0.5;
    
    return Math.max(4.0, Math.min(9.0, base_threshold));
  }
};
```

---

### Tension Tracking Differential

**Track both objective and perceived tension, show differential to understand player experience.**

```javascript
const TENSION_DIFFERENTIAL_TRACKING = {
  data_structure: {
    week: number,
    objective_tension: number,       // 0.0-1.0 (what's actually happening)
    perceived_tension: number,       // 0.0-1.0 (what player feels)
    differential: number,            // perceived - objective
    personality_modifier: number,    // multiplier applied
    active_stressors: string[],
    player_narrative: string
  },
  
  example_tracking_high_neuroticism: {
    week: 8,
    objective_tension: 0.6,
    personality_modifier: 1.5,
    perceived_tension: 0.9,
    differential: +0.3,
    
    interpretation: "Anxiety amplifies situation by 50%",
    
    narrative_reflects_perception: `
      [Narrative shows perceived 0.9, not objective 0.6]
      
      Everything feels like too much right now.
      Work. Money. Sarah's distance. The review coming up.
      
      Objectively? Maybe you're handling it fine.
      But it doesn't feel that way.
      To you, this is 9/10. Overwhelming.
    `,
    
    active_stressors: [
      "Performance review (2 weeks)",
      "Rent due ($200 short)",
      "Sarah acting distant",
      "Client feedback delayed"
    ]
  },
  
  example_tracking_low_neuroticism: {
    week: 8,
    objective_tension: 0.6,
    personality_modifier: 0.75,
    perceived_tension: 0.45,
    differential: -0.15,
    
    interpretation: "Calm personality reduces tension by 25%",
    
    narrative_reflects_perception: `
      [Narrative shows perceived 0.45, not objective 0.6]
      
      A lot going on. Review soon, rent's tight, Sarah's off.
      
      You take it in stride.
      One thing at a time. You'll handle it.
      
      To you, this is 4/10. Manageable.
    `,
    
    active_stressors: [
      "Performance review (2 weeks)",
      "Rent due ($200 short)",
      "Sarah acting distant",
      "Client feedback delayed"
    ]
  },
  
  narrative_implementation: {
    principle: "Narrative voice matches perceived tension, not objective",
    
    high_differential_positive: {
      narrative_style: "Anxious, catastrophizing, stress evident",
      internal_monologue: "What if this goes wrong? Everything feels fragile.",
      physical_descriptions: "Heart racing, can't sleep, stomach churning"
    },
    
    low_differential_near_zero: {
      narrative_style: "Realistic, proportional, balanced",
      internal_monologue: "This is hard. But I can handle it.",
      physical_descriptions: "Tired but coping, some stress visible"
    },
    
    high_differential_negative: {
      narrative_style: "Calm, maybe too calm, potential obliviousness",
      internal_monologue: "Not sure why everyone else is stressed about this.",
      physical_descriptions: "Relaxed, unfazed, maybe missing warning signs",
      risk: "Player may underestimate danger"
    }
  },
  
  npc_reactions_to_differential: {
    high_positive_differential: {
      observant_npcs: "Level 3+ NPCs may notice player is more anxious than situation warrants",
      dialogue: `
        [Sarah, gently]
        "Hey. I think you're spiraling a bit. It's not as bad as it feels right now."
        [Offers perspective]
      `
    },
    
    high_negative_differential: {
      observant_npcs: "Level 3+ NPCs may notice player is too calm, warn them",
      dialogue: `
        [Marcus, concerned]
        "You seem really chill about this. But... it's kind of serious. Are you okay?"
        [Checks if player is in denial]
      `
    }
  }
};
```

---

### Integrated Example: Same Situation, Different Personalities

```javascript
const INTEGRATED_TENSION_EXAMPLE = {
  situation: "Performance review in 2 weeks + rent due ($200 short) + relationship tension",
  objective_tension: 7.0,
  objective_stressors: 3,
  
  player_a_high_neuroticism: {
    personality: { O: 3.5, C: 3.0, E: 3.0, A: 3.5, N: 4.5 },
    amplification_factor: 1.6,
    perceived_tension: 11.2,  // Capped at 10.0
    breaking_point: 5.5,
    
    status: "BEYOND BREAKING POINT",
    
    narrative: `
      Week 8. Everything's falling apart.
      
      The review is in 2 weeks. You're going to fail.
      Rent is due and you're $200 short. Eviction?
      Sarah won't talk to you. What did you do?
      
      You can't sleep. Can't eat. Can't focus.
      At work, you're making mistakes. Which makes the review worse.
      Which makes you more anxious. Which makes more mistakes.
      
      You're spiraling.
      
      For you, this is 10/10. Maximum capacity exceeded.
      You need help. But you're too ashamed to ask.
    `,
    
    gameplay_state: {
      emotional_capacity: 2.0,
      options_locked: "High-demand choices unavailable",
      npcs_noticing: "Level 2+ can see you're struggling",
      intervention_available: "Marcus offers help if you accept"
    }
  },
  
  player_b_moderate_neuroticism: {
    personality: { O: 3.0, C: 3.5, E: 3.0, A: 3.0, N: 3.0 },
    amplification_factor: 1.0,
    perceived_tension: 7.0,
    breaking_point: 7.0,
    
    status: "AT BREAKING POINT",
    
    narrative: `
      Week 8. It's a lot.
      
      Review in 2 weeks. Rent's short. Sarah's distant.
      Three major things at once.
      
      You're at capacity. Can't take on anything else.
      Sleep's suffering. You're snappier than usual.
      
      This is your limit. 7/10.
      One more thing and you'll break.
    `,
    
    gameplay_state: {
      emotional_capacity: 4.0,
      options_locked: "Some high-demand choices unavailable",
      npcs_noticing: "Level 3+ concerned",
      manageable_if: "One stressor resolves soon"
    }
  },
  
  player_c_low_neuroticism: {
    personality: { O: 3.0, C: 4.0, E: 3.5, A: 3.5, N: 1.8 },
    reduction_factor: 0.75,
    perceived_tension: 5.25,
    breaking_point: 8.5,
    
    status: "STRESSED BUT MANAGING",
    
    narrative: `
      Week 8. Busy week.
      
      Review coming up. Need to prep.
      Rent's a bit short - should pick up extra gig.
      Sarah's been quiet - maybe check in with her.
      
      Three things to handle. Okay. One at a time.
      
      You make a list. Prioritize. Start tackling.
      
      This is manageable. 5/10.
      You've been through worse.
    `,
    
    gameplay_state: {
      emotional_capacity: 6.5,
      options_locked: "None - all choices available",
      npcs_noticing: "You seem fine to them",
      strength: "Calm under pressure helps others feel calm too"
    }
  },
  
  key_insight: "Same external situation, vastly different internal experience based on personality."
};
```

---

## Hook Point Examples by Type

### Complete Examples

```javascript
const HOOK_EXAMPLES = {
  // SHORT-TERM QUESTION (2-4 weeks)
  portfolio_approval: {
    week_intro: 8,
    week_resolve: 10,
    
    intro_card: "You email the portfolio to the gallery owner. 'I'll review it and get back to you soon.' Soon. What does that mean?",
    
    development_cards: [
      { week: 9, content: "No response yet. You refresh your email for the 15th time today." }
    ],
    
    resolution_options: [
      {
        type: "positive",
        card: "Email from gallery: 'Love the work. Let's set up a meeting.' Your hands shake as you read it.",
        new_hooks: ["Gallery meeting scheduled (promise, 2 weeks)"]
      },
      {
        type: "negative",
        card: "Email from gallery: 'The work is good, but not quite what we're looking for right now.' Your stomach sinks.",
        new_hooks: ["How to improve portfolio? (question, 4 weeks)"]
      }
    ]
  },
  
  // MEDIUM-TERM THREAT (4-8 weeks)
  career_performance_review: {
    week_intro: 6,
    week_resolve: 14,
    
    intro_card: "Boss mentions 'quarterly performance reviews coming up.' She doesn't make eye contact.",
    
    development_cards: [
      { week: 9, content: "Colleague whispers: 'I heard they're cutting positions.' You try not to panic." },
      { week: 11, content: "Email arrives: 'Performance Review scheduled for Week 14.' Two weeks." },
      { week: 13, content: "Tomorrow. The review is tomorrow. You can't sleep." }
    ],
    
    resolution_decisive_decision: true,
    resolution_week: 14
  },
  
  // LONG-TERM MYSTERY (12-24 weeks)
  sarah_grief_mystery: {
    week_intro: 4,
    week_resolve: 24,
    
    clue_trail: [
      { week: 4, clue: "Sarah mentions David in passing" },
      { week: 9, clue: "Photograph glimpsed, quickly hidden" },
      { week: 14, clue: "Sarah sad on specific date" },
      { week: 18, clue: "Partial reveal: was engaged" },
      { week: 24, clue: "Full reveal: David died, still grieving" }
    ],
    
    tension_pattern: "Low background (0.2-0.3) with spikes on clues (0.5-0.6)",
    player_agency: "Can push for info (Sarah deflects) or wait",
    payoff: "Recontextualizes all of Sarah's behavior, deepens relationship"
  }
};
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Tension System (v1.1 Foundation)
- [x] No FOMO mechanics - hooks create intrigue, not anxiety
- [x] No real-time pressure - all tensions are in-world deadlines
- [x] Paused time for decisions - high-tension moments don't pressure player
- [x] Breathing room built in - tension curves have valleys
- [x] Player agency maintained - can pursue or ignore most hooks
- [x] 2-5 active hooks at any time (sweet spot: 3)
- [x] Hook types: question, promise, threat, opportunity, mystery
- [x] 3-act tension curves (Act 1: 0.3-0.5, Act 2: 0.5-0.8, Act 3: 0.8→1.0→0.2)

### ✅ Master Truths v1.2: Personality-Based Tension *(NEW - Gap 5.1)*
- [x] **Objective vs Subjective Tension Tracking**
  - Objective: What's actually happening (0.0-1.0 universal)
  - Subjective: What player experiences (personality-filtered)
  - Differential: perceived - objective
- [x] **Neuroticism-Based Amplification/Reduction**
  - High neuroticism (3.5+): 1.4-1.8x amplification
  - Low neuroticism (<2.5): 0.65-0.85x reduction
  - Narrative reflects perceived tension, not objective
- [x] **Threshold Variance by Personality**
  - High resilience: Breaking point 8.5 (low N, high C, high A)
  - Moderate resilience: Breaking point 7.0 (average traits)
  - Low resilience: Breaking point 5.5 (high N, low C)
- [x] **Tension Differential Tracking**
  - Track both objective and perceived weekly
  - Show differential: +0.3, 0.0, -0.15
  - NPCs react to differential (may offer perspective or warning)

### ✅ Master Truths v1.2: Tension Components

**Tension Perception System:**
1. **Objective Tension:** Situation severity independent of personality
2. **Personality Modifier:** Amplification/reduction based on neuroticism
3. **Perceived Tension:** What player actually experiences (narrative shows this)
4. **Differential:** Gap between perception and reality
5. **Breaking Point:** Varies by personality (4.0-9.0 range, typically 5.5-8.5)

**High Neuroticism Effects:**
- Amplification: 1.4-1.8x multiplier on objective tension
- Behavioral: Sleep affected, intrusive thoughts, stress spillover
- Narrative: "Everything feels like too much" (anxious tone)
- Meter impact: Mental -2, Physical -1
- Rumination cards appear

**Low Neuroticism Effects:**
- Reduction: 0.65-0.85x multiplier on objective tension
- Behavioral: Sleep unaffected, calm approach, proportional response
- Narrative: "This is manageable" (calm tone)
- Meter impact: None - stays stable
- Handles pressure well

**Breaking Point Calculation:**
- Base: 7.0
- High neuroticism (4.0+): -2.0
- Low neuroticism (≤2.0): +1.5
- High conscientiousness (4.0+): +0.5
- Low conscientiousness (≤2.0): -0.5
- High agreeableness (4.0+): +0.5
- Low emotional meter (≤3): -1.0
- High emotional meter (≥7): +0.5
- Final range: 4.0-9.0

**NPC Reactions to Differential:**
- High positive differential: "You're spiraling a bit. It's not as bad as it feels." (Level 3+)
- High negative differential: "You seem really chill. But it's kind of serious." (Level 3+)

### ✅ Integrated Example
Same situation (objective tension 7.0) produces:
- High neuroticism player: Perceived 11.2 (capped 10.0), "BEYOND BREAKING POINT"
- Moderate neuroticism player: Perceived 7.0, "AT BREAKING POINT"
- Low neuroticism player: Perceived 5.25, "STRESSED BUT MANAGING"

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~475 lines** of new v1.2 personality-based tension mechanics
2. **Objective vs subjective tension tracking** with differential
3. **Neuroticism amplification/reduction formulas** (1.4-1.8x / 0.65-0.85x)
4. **Breaking point calculation** varying by personality (5.5-8.5 typical range)
5. **Narrative voice adaptation** to perceived tension
6. **NPC differential awareness** and perspective offering
7. **Integrated example** showing 3 personality types with same situation

**Design Principles:**
- Tension is subjective, not objective
- High neuroticism amplifies everything (realistic anxiety representation)
- Low neuroticism provides calm perspective (realistic resilience)
- Narrative reflects player's experience, not external reality
- NPCs notice when perception diverges from reality
- Breaking points vary widely by personality composition
- Same situation produces vastly different internal experiences

**References:**
- See `01-emotional-authenticity.md` for cross-system integration
- See `02-system-by-system-enhancement.md` for Gap 5.1 specifications (lines 700-781)
- See `14-emotional-state-mechanics.md` for emotional capacity and circumstance stacking
- See `30-decisive-decision-templates.md` for personality-based option filtering
- See `31-narrative-arc-scaffolding.md` for tension integration with 3-act structure
- See `32-event-generation-rules.md` for tension-appropriate event generation
- See `36-stakes-escalation-mechanics.md` for how stakes create tension

---

**This specification enables developers to implement the complete tension maintenance system with personality-based perception, objective/subjective tracking, neuroticism modifiers, dynamic threshold calculation, and narrative voice adaptation to create authentic, personalized tension experiences that respect human psychological limitations.**
