# System-by-System Enhancement Plan
## Detailed Analysis of Required Changes

**Compliance:** `master_truths_canonical_spec_v_1_2.md` (v1.2)  
**Date:** October 14, 2025  
**Purpose:** Specific enhancement recommendations for each gameplay document to achieve emotional authenticity

---

## Document 1: `14-emotional-state-mechanics.md`

### Current Strengths
- ✅ 20 emotional states well-defined
- ✅ OCEAN personality baseline exists
- ✅ Card appeal multipliers comprehensive
- ✅ State transition logic solid

### Critical Gaps

#### Gap 1.1: Memory-Triggered State Changes
**Current:** States determined by meters + recent events + personality
**Missing:** Past trauma/joy memories triggering states

**Add After Line 622 (end of determineEmotionalStates function):**
```javascript
// STEP 6: MEMORY TRIGGERS (NEW)
const triggeredMemories = checkForTriggeredMemories(
  character,
  currentContext.date,
  currentContext.location,
  currentContext.presentNPCs
);

if (triggeredMemories.length > 0) {
  triggeredMemories.forEach(memory => {
    if (memory.emotional_weight > 0.7) {
      if (memory.valence < -0.5) {
        // Painful memory triggered
        primaryState = blendState(primaryState, "MELANCHOLY", memory.weight);
        logEmotionalEcho({
          memory: memory.title,
          trigger: `${currentContext.location} reminds you of...`,
          affects_cards: applyMemoryFilter(availableCards, memory)
        });
      } else if (memory.valence > 0.5) {
        // Joyful memory triggered
        primaryState = blendState(primaryState, "GRATEFUL", memory.weight * 0.5);
      }
    }
  });
}
```

#### Gap 1.2: Circumstance Stacking
**Current:** States don't account for multiple simultaneous stressors
**Missing:** "Everything happening at once" compounding effect

**Add New Section After Line 830 (end of updateEmotionalStates):**
```javascript
// ENHANCEMENT: CIRCUMSTANCE STACKING
function applyCircumstanceStacking(state, character, activeStressors) {
  const stressorTypes = {
    work: activeStressors.workPressure > 7,
    money: character.meters.money < 200 && character.rentDue <= 7,
    relationship: activeStressors.relationshipTension.length >= 2,
    health: character.meters.physical < 4,
    family: activeStressors.familyCrisis === true
  };
  
  const activeCount = Object.values(stressorTypes).filter(v => v).length;
  
  if (activeCount >= 3) {
    // "When it rains, it pours"
    intensity = Math.min(1.0, intensity * (1 + activeCount * 0.15));
    
    if (character.personality.neuroticism > 4.0) {
      // High neuroticism + multiple stressors = overwhelm risk
      primaryState = "OVERWHELMED";
      intensity = 0.9;
      
      narrativeContext = `
        Everything is happening at once:
        ${activeCount} major stressors active simultaneously.
        
        For someone with your anxiety levels, this compounds fast.
        What would be manageable one-at-a-time becomes overwhelming.
      `;
    }
  }
  
  return { state: primaryState, intensity, narrativeContext };
}
```

#### Gap 1.3: Environmental/Seasonal Modifiers
**Current:** No weather, season, or environmental context
**Missing:** Winter blues, rainy day mood, seasonal affect

**Add New Section After Line 509 (end of NEUTRAL_STATES):**
```javascript
// ENVIRONMENTAL MODIFIERS
const ENVIRONMENTAL_STATE_MODIFIERS = {
  seasonal: {
    winter: {
      affects: ["MELANCHOLY", "REFLECTIVE"],
      multiplier: 1.3,
      applies_if: "neuroticism > 3.0 OR openness > 4.0",
      narrative: "Winter affects you. Always has."
    },
    spring: {
      affects: ["INSPIRED", "HOPEFUL"],
      multiplier: 1.2,
      applies_if: "openness > 3.5",
      narrative: "Something about spring makes everything feel possible."
    }
  },
  
  weather: {
    rainy: {
      affects: ["MELANCHOLY", "REFLECTIVE", "PEACEFUL"],
      multiplier: 1.2,
      applies_if: "openness > 3.0",
      narrative: "Rainy days. You've always liked them. Contemplative."
    },
    first_snow: {
      affects: ["NOSTALGIC", "PEACEFUL"],
      multiplier: 1.5,
      triggers_memory_search: true,
      narrative: "First snow. Memories surface."
    }
  },
  
  anniversary_dates: {
    grief_anniversary: {
      detection: "Check memory archive for loss events",
      affects: ["MELANCHOLY", "NUMB"],
      multiplier: 2.0,
      narrative: "Something about today feels heavy. Then you remember..."
    },
    joy_anniversary: {
      detection: "Check memory archive for breakthrough/celebration events",
      affects: ["GRATEFUL", "NOSTALGIC"],
      multiplier: 1.5,
      narrative: "One year ago today..."
    }
  }
};
```

---

## Document 2: `21-card-evolution-mechanics.md`

### Current Strengths
- ✅ Relationship-driven evolution well-defined
- ✅ Time-based evolution solid
- ✅ Event-based evolution exists

### Critical Gaps

#### Gap 2.1: Emotional Journey Tracking
**Current:** Evolution based on repetition/time
**Missing:** Cards evolve based on emotional significance

**Add After Line 496 (end of Activity Card Evolution section):**
```javascript
// ENHANCEMENT: EMOTIONAL SIGNIFICANCE EVOLUTION
const EMOTIONAL_JOURNEY_EVOLUTION = {
  principle: "Cards that were present during emotional milestones evolve faster and differently",
  
  triggers: {
    breakthrough_association: {
      trigger: "Card used during breakthrough moment",
      requirement: "Activity present when major insight/success occurred",
      
      example: {
        base: "Work on Portfolio (generic activity)",
        context: "Week 12: Creative breakthrough while working on portfolio",
        evolved: "Portfolio Sessions - Where It All Clicked",
        
        narrative: `
          Week 12. The cafe. 2 AM coffee. Your laptop screen.
          
          This is where it happened. Where your style emerged.
          Where everything you'd been working toward suddenly made sense.
          
          This activity will forever be linked to that moment.
          The moment you became who you were trying to become.
        `,
        
        emotional_weight: 10,
        novel_chapter_worthy: true,
        carries_transformation_memory: true
      }
    },
    
    crisis_support: {
      trigger: "Card used to cope during crisis",
      requirement: "Activity helped player survive difficult period",
      
      example: {
        base: "Evening Run (routine exercise)",
        context: "Weeks 14-18: Used running to process grief, anxiety, overwhelm",
        evolved: "The Run That Saved Me",
        
        narrative: `
          When everything was falling apart, this was the thing that kept you sane.
          
          Week 14: Ran to escape the anxiety.
          Week 16: Ran to process the loss.
          Week 18: Ran because it was the only thing that helped.
          
          Some activities become survival mechanisms.
          This is one of them.
        `,
        
        emotional_weight: 9,
        therapeutic_association: true,
        becomes_comfort_zone_anchor: true
      }
    },
    
    parallel_significance: {
      trigger: "Card present during multiple major life events",
      requirement: "Activity used across 3+ major moments",
      
      example: {
        base: "Coffee with Sarah (social activity)",
        context: "Present during: breakup processing (W8), job offer celebration (W12), grief support (W16), breakthrough planning (W20)",
        evolved: "Coffee with Sarah - Where Life Happens",
        
        narrative: `
          This isn't just coffee anymore.
          
          This is where you processed the breakup.
          Where you celebrated the job offer.
          Where Sarah held space for your grief.
          Where you planned your next chapter.
          
          Some rituals become containers for your entire life.
          Tuesday, 3 PM, Cafe Luna, Sarah.
          Everything important happens here.
        `,
        
        emotional_weight: 10,
        life_anchor_card: true,
        carries_multiple_memories: true
      }
    }
  },
  
  tracking_system: {
    per_card_history: {
      emotional_states_during_use: EmotionalState[],
      parallel_life_events: string[],
      memories_created: Memory[],
      breakthrough_moments: boolean[],
      crisis_moments: boolean[],
      celebration_moments: boolean[]
    },
    
    evolution_weight_calculation: `
      traditional_weight = (uses / 10) + (relationship_level / 5)
      emotional_weight = (breakthrough_moments * 3) + 
                        (crisis_moments * 2) + 
                        (parallel_significance * 1.5)
      
      if (emotional_weight >= traditional_weight * 0.5) {
        // Emotional significance high enough to trigger early evolution
        evolve_with_emotional_narrative = true
      }
    `
  }
};
```

#### Gap 2.2: Trauma/Growth Markers
**Current:** Cards are neutral containers
**Missing:** Cards carry emotional associations (healing, trauma, transformation)

**Add New Section After Line 723 (end of Evolution Tracking):**
```javascript
// TRAUMA & GROWTH MARKERS
const EMOTIONAL_ASSOCIATION_SYSTEM = {
  card_emotional_flags: {
    HEALING: "This activity helped me recover",
    TRAUMA: "This activity is associated with pain",
    TRANSFORMATION: "This activity was present when I changed",
    COMFORT: "This activity is my safe space",
    GROWTH: "This activity pushed me to grow",
    AVOIDANCE: "I avoid this because of what it reminds me of"
  },
  
  affects_gameplay: {
    healing_cards: {
      behavior: "Appear more when player emotional/mental meters low",
      narrative: "You know this helps. You've been here before.",
      effectiveness: "+20% emotional recovery"
    },
    
    trauma_cards: {
      behavior: "May trigger memory echoes, player can choose to avoid",
      narrative: "This reminds you of... [painful memory]. Still hard.",
      choice: "Face it or avoid it",
      facing_consequences: "Gradual healing, but painful",
      avoiding_consequences: "No immediate pain, but issue persists"
    },
    
    transformation_cards: {
      behavior: "Carry permanent significance, referenced in novel",
      narrative: "This is where everything changed.",
      never_becomes_routine: true,
      always_emotionally_weighted: true
    }
  }
};
```

---

## Document 3: `30-decisive-decision-templates.md`

### Current Strengths
- ✅ Emotional echoes system exists
- ✅ Pattern tracking present
- ✅ Time pauses (no FOMO)

### Critical Gaps

#### Gap 3.1: OCEAN-Based Option Availability
**Current:** All players see all options
**Missing:** Some options should be gated/modified by personality

**Add After Line 235 (end of decision_card template):**
```javascript
// PERSONALITY-BASED OPTION MODIFIERS
personality_modifiers: {
  option_id: string,
  
  accessibility: {
    requires_trait: {
      trait: "openness" | "conscientiousness" | "extraversion" | "agreeableness" | "neuroticism",
      threshold: number,
      comparison: ">=" | "<=" | "between",
      why: string
    }[],
    
    locked_if_trait: {
      trait: string,
      threshold: number,
      reason: string,
      alternative_shown: boolean
    }
  },
  
  difficulty_modifier: {
    trait_challenged: string,             // "Low agreeableness = confrontation easier"
    comfort_zone_cost_multiplier: number, // 1.0 = normal, 2.0 = very hard for this personality
    
    internal_narrative: {
      easy_for_you: string,               // "This comes naturally to you"
      hard_for_you: string,               // "Everything in you resists this"
      very_hard_for_you: string           // "This goes against everything you are"
    }
  },
  
  personality_specific_consequences: {
    if_high_neuroticism: {
      post_decision_anxiety: boolean,
      rumination_cards: string[],
      regret_multiplier: number
    },
    
    if_low_agreeableness: {
      confrontation_bonus: number,
      social_cost_reduction: number,
      guilt_reduction: number
    },
    
    if_high_conscientiousness: {
      preparation_available: boolean,
      planning_reduces_risk: boolean,
      decision_delay_option: string
    }
  }
}
```

#### Gap 3.2: Current Capacity Gating
**Current:** Decisions available regardless of player state
**Missing:** Some options too emotionally demanding when drained

**Add After Line 214 (in display_context section):**
```javascript
// EMOTIONAL CAPACITY CHECKING
emotional_capacity_system: {
  current_capacity: calculateCapacity(
    player.meters.mental,
    player.meters.emotional,
    player.burnout_accumulation,
    countActiveStressors(player.current_circumstances)
  ),
  
  option_requirements: {
    option_id: string,
    emotional_demand: 0-10,
    
    locked_if_capacity_below: number,
    locked_reason: string,
    
    example: {
      option: "Have difficult confrontation with friend",
      requires_capacity: 7,
      current_capacity: 4,
      
      locked: true,
      locked_reason: `
        You don't have it in you right now.
        
        Between work stress (8/10), money anxiety (7/10), and exhaustion,
        you're at 4/10 emotional capacity.
        
        This conversation requires 7/10. You'd say things you'd regret.
        
        [Alternative: Rest for 1 week, then have conversation at higher capacity]
      `,
      
      delayed_option: "Take a week to recover, then address this",
      delay_consequences: "Issue persists but you're in better state to handle it"
    }
  },
  
  capacity_recovery_options: [
    "Take a mental health day (recover 2 capacity points)",
    "Talk to therapist/friend (recover 1 capacity point, process stressors)",
    "Rest and self-care for 1 week (full capacity restoration)"
  ]
}
```

#### Gap 3.3: Environmental/Circumstantial Context
**Current:** Decisions happen in vacuum
**Missing:** "Also dealing with X, Y, Z" context

**Add New Section Before Line 1152 (before Compliance Checklist):**
```javascript
// CIRCUMSTANTIAL PRESSURE MODIFIERS
const DECISION_WITH_PARALLEL_STRESSORS = {
  base_decision: "Career vs Friend choice",
  
  parallel_circumstances: {
    work_deadline: "Major project due in 3 days",
    financial_stress: "Rent due in 5 days, $180 short",
    health_concern: "Haven't slept well in a week",
    relationship_strain: "Partner upset about something else",
    family_crisis: "Mom in hospital"
  },
  
  context_display: {
    before_options: `
      [Before presenting the choice]
      
      Everything is happening at once right now:
      
      • Work: ${parallel_circumstances.work_deadline}
      • Money: ${parallel_circumstances.financial_stress}
      • Health: ${parallel_circumstances.health_concern}
      • Home: ${parallel_circumstances.relationship_strain}
      • Family: ${parallel_circumstances.family_crisis}
      
      And now this decision.
      
      On a good week, this would be hard.
      This is not a good week.
    `,
    
    affects_perception: {
      stress_amplification: 1.5,
      decision_feels_harder: true,
      capacity_reduced: true,
      some_options_locked: true
    },
    
    npc_may_notice: {
      if_relationship_level: ">= 3",
      dialogue: `
        [${npc_name} looks at you]
        "You look like hell. What else is going on?"
        [You could tell them about everything else, or keep it in]
      `,
      
      if_share_context: {
        npc_reaction: "May offer to help with parallel stressors",
        reduces_immediate_pressure: true,
        deepens_relationship: true
      }
    }
  }
};
```

---

## Document 4: `33-dialogue-generation-templates.md`

### Current Strengths
- ✅ Relationship-level dialogue well-defined
- ✅ Personality affects speech patterns
- ✅ Memory callback system exists

### Critical Gaps

#### Gap 4.1: NPC Observes Player State
**Current:** NPCs respond to relationship level only
**Missing:** NPCs notice exhaustion, stress, mood

**Add After Line 289 (end of Level 3 dialogue):**
```javascript
// NPC OBSERVATIONAL AWARENESS
const NPC_NOTICES_PLAYER_STATE = {
  physical_observation: {
    trigger: "player.meters.physical <= 3 AND relationship.level >= 2",
    
    dialogue_modifications: {
      greeting_replaced: {
        normal: "Hey! How's it going?",
        concerned: `[${npc_name} frowns when they see you]
                    "You look exhausted. When's the last time you slept properly?"`
      },
      
      conversation_tone: "supportive_not_demanding",
      offers_help: true,
      may_insist_on_rest: "if relationship.level >= 4",
      
      example: {
        sarah_level_4: `
          [Sarah takes one look at you and shakes her head]
          "Nope. We're not doing this."
          "You look like you haven't slept in days."
          [She signals the barista]
          "Cancel my order. We're getting you home."
          
          She's not asking. She's telling.
          That's what best friends do.
        `
      }
    }
  },
  
  emotional_observation: {
    trigger: "player.emotional_state IN ['DEVASTATED', 'OVERWHELMED', 'NUMB'] AND relationship.level >= 3",
    
    npc_response: {
      immediate_concern: true,
      drops_normal_conversation: true,
      focuses_on_player: true,
      
      dialogue: `
        [${npc_name} stops mid-sentence]
        "Hey. What's wrong?"
        [They can see it on your face before you say anything]
        "Talk to me."
      `,
      
      personality_modifications: {
        high_agreeableness: "Gentle, patient, validates feelings",
        low_agreeableness: "Direct, problem-solving, 'what do you need'",
        high_extraversion: "Physically present, offers distraction or company",
        low_extraversion: "Gives space if needed, quiet support"
      }
    }
  },
  
  contextual_awareness: {
    npc_knows_about: {
      work_crisis: boolean,
      financial_stress: boolean,
      relationship_problems: boolean,
      family_issues: boolean,
      health_concerns: boolean
    },
    
    if_aware_of_stressor: {
      acknowledges_in_conversation: true,
      doesn't_pretend_everything_fine: true,
      
      example: `
        [Sarah sits down, doesn't ask how you are]
        "How's the work nightmare? Still hell?"
        [Sees your face]
        "Yeah. Thought so."
        [Pushes coffee toward you]
        "Want to talk about it or want distraction?"
      `,
      
      offers_choice: "Support vs distraction",
      respects_player_need: true
    }
  }
};
```

#### Gap 4.2: Environmental Context in Dialogue
**Current:** Dialogue ignores location, weather, season
**Missing:** "Look at the snow" moments, seasonal references

**Add After Line 545 (end of Memory Callback Dialogue):**
```javascript
// ENVIRONMENTAL CONTEXT DIALOGUE
const ENVIRONMENTALLY_AWARE_DIALOGUE = {
  seasonal_references: {
    first_snow: {
      personality_filter: "openness > 3.5 OR nostalgia-prone",
      
      dialogue_options: [
        {
          npc_personality: "high_openness",
          dialogue: `
            [${npc_name} looks out window at falling snow]
            "First snow. God, I love this."
            [Pause, watching]
            "Want to walk? Coffee can wait."
          `,
          creates_spontaneous_activity: "Walk in first snow",
          memory_worthy: true
        }
      ]
    },
    
    anniversary_location: {
      trigger: "current_location === relationship.first_meeting_location AND weeks_since_meeting % 52 === 0",
      
      dialogue: `
        [${npc_name} looks around ${location}]
        "${years_ago} years. Can you believe it?"
        [Gestures to table]
        "This exact table. You were so nervous ordering coffee."
        [They laugh]
        "Look at us now."
      `,
      
      emotional_weight: 8,
      reinforces_bond: true
    }
  },
  
  weather_context: {
    rainy_day: {
      personality_affects: "high_openness = enjoys, low_extraversion = prefers staying in",
      
      dialogue_modifications: [
        {
          extraversion: "high",
          dialogue: "[Looks out at rain] Perfect day to be inside with coffee and conversation."
        },
        {
          extraversion: "low",
          dialogue: "[Notices rain] Good day to stay in. I'm glad you're here."
        }
      ]
    }
  },
  
  time_of_day_context: {
    late_night_vulnerability: {
      trigger: "time_of_day === 'late_night' AND relationship.level >= 3",
      
      effect: "Conversations become more vulnerable, guards down",
      
      dialogue: `
        [2 AM. ${location}. Just you and ${npc_name}]
        "Can I tell you something? It's late. Maybe that's why I can say it."
        [Pause]
        "I don't usually talk about this..."
      `,
      
      enables_vulnerability: true,
      feels_more_honest: true,
      creates_significant_memory: true
    }
  }
};
```

---

## Document 5: `35-tension-maintenance-system.md`

### Current Strengths
- ✅ Hook point system solid
- ✅ Mystery scaffolding good
- ✅ Tension curves defined

### Critical Gaps

#### Gap 5.1: Personality-Based Tension Thresholds
**Current:** Universal tension levels
**Missing:** High vs low neuroticism experience tension differently

**Add After Line 442 (end of adjustTensionIfNeeded):**
```javascript
// PERSONALITY-BASED TENSION PERCEPTION
const PERSONALIZED_TENSION = {
  objective_vs_subjective: {
    principle: "Same situation creates different tension for different personalities",
    
    example: {
      situation: "Job performance review in 2 weeks",
      objective_tension: 6.0,
      
      high_neuroticism_player: {
        perceived_tension: 9.0,
        amplification_factor: 1.5,
        internal_experience: `
          Two weeks. The review is in two weeks.
          
          You can't stop thinking about it.
          Every small mistake at work feels like evidence.
          Your anxiety amplifies everything.
          
          To you, this feels like 9/10. To someone else? Maybe 6/10.
          But you've never been someone else.
        `,
        
        sleep_affected: true,
        intrusive_thoughts: true,
        stress_spillover: "affects other life areas"
      },
      
      low_neuroticism_player: {
        perceived_tension: 4.5,
        reduction_factor: 0.75,
        internal_experience: `
          Performance review in two weeks. Okay.
          
          You're not worried. Maybe you should be?
          But you've never been good at anxiety.
          You'll prepare, do your best, and see what happens.
          
          To you, this feels manageable. Maybe 4/10.
          You know people who'd be panicking right now.
          You're just... not.
        `,
        
        calm_approach: true,
        proportional_response: true
      }
    }
  },
  
  threshold_variance: {
    breaking_point_personality: {
      high_resilience: {
        traits: "low_neuroticism + high_conscientiousness + high_agreeableness",
        tension_threshold: 8.5,
        narrative: "You can handle a lot. Always have. It takes a lot to break you."
      },
      
      low_resilience: {
        traits: "high_neuroticism + low_conscientiousness + low_emotional_meter",
        tension_threshold: 5.5,
        narrative: "You hit your limit faster than most. Not weakness. Just how you're wired."
      }
    }
  },
  
  tension_tracking: {
    objective: "What's actually happening",
    perceived: "What player experiences",
    differential: "perceived - objective",
    
    narrative_reflects_perception: true,
    
    example: {
      low_differential: "Your perception matches reality",
      high_positive_differential: "Your anxiety makes everything feel worse",
      high_negative_differential: "You might be underestimating this"
    }
  }
};
```

---

## Implementation Priority Order

### Immediate (Phase 1 - Week 1-2)
1. **Emotional State Mechanics** - Memory triggers, circumstance stacking
2. **Decisive Decisions** - OCEAN-based option filtering, capacity gating
3. **Card Evolution** - Emotional journey tracking

### High Priority (Phase 2 - Week 3-4)
4. **Dialogue Generation** - NPC observational awareness
5. **Card Fusion** - Emotional significance thresholds
6. **Tension Maintenance** - Personality-based perception

### Medium Priority (Phase 3 - Week 5-6)
7. **Event Generation** - Circumstance awareness
8. **Narrative Arcs** - Emotional journey mapping
9. **Stakes Escalation** - Personal meaning integration

### Integration (Phase 4 - Week 7-8)
10. Cross-system coherence checking
11. Novel-worthiness scoring
12. Authenticity validation

---

## Next Actions

1. **Review** this detailed plan
2. **Select** first system to enhance (recommend: Emotional State Mechanics)
3. **Create** specific implementation spec for selected system
4. **Build** foundation services (EmotionalContextService, PersonalityResponseEngine)
5. **Begin** systematic enhancement

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
- [x] **Dramatic irony mechanics used when knowledge gaps exist (score ≥ 0.6)**
- [x] **Memory resonance factors applied to recall (weights: 0.7-0.95)**
- [x] **Novel-quality thresholds met (≥ 0.7 overall; authenticity ≥ 0.7; tension ≥ 0.6; hooks ≥ 0.6)**
- [x] This doc cites **Truths v1.2** at the top

---

**This plan provides exact locations and specifications for enhancing each system to achieve the goal: emotionally authentic, personality-driven, contextually aware gameplay that generates novel-worthy narratives.**

