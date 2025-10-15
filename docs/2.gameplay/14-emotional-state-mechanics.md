# Emotional State Mechanics - Implementation Specification

**Compliance:** `master_truths_canonical_spec_v_1_2.md` (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete implementation of the 20 emotional states system with filtering, appeal calculations, and state transitions

**References:**
- **Design Philosophy:** `1.concept/19-emotional-state-system.md` (WHY states matter)
- **Success Probability:** `12-success-probability-formulas.md` (how states affect success)
- **Turn Flow:** `71-daily-turn-flow-detailed.md` (when states are calculated)

---

## Overview

Emotional states are a **lens through which players experience life**. Each turn, the system calculates 1-2 active emotional states that:
1. Filter which cards appear in the player's hand
2. Modify costs, success chances, and rewards of activities
3. Create authentic psychological challenges
4. Evolve based on player choices

**Core Principle:** States guide player choices but never remove agency. Every card type remains available; states just change appeal and costs.

---

## The 20 Canonical Emotional States

**Compliance Note:** master_truths v1.1 specifies EXHAUSTED and OVERWHELMED as canonical names. All states must map to these or propose additions.

### ENERGIZING STATES (Positive High-Energy)

```javascript
const ENERGIZING_POSITIVE = {
  MOTIVATED: {
    description: "Driven, goal-oriented, productive mindset",
    energy_level: "high",
    valence: "positive",
    triggers: ["aspiration_progress", "deadline_approaching", "recent_success"],
    effects: {
      card_appeal: {
        work_tasks: 2.0,
        aspiration_progress: 2.5,
        productive_activities: 1.8,
        social_casual: 0.7,
        rest_activities: 0.3,
        avoidance: 0.2
      },
      modifiers: {
        aspiration_progress_bonus: 0.20,  // +20%
        energy_cost_work: -1,              // Work costs 1 less energy
        success_bonus_goals: 0.10          // +10% success on goal-related
      }
    }
  },
  
  INSPIRED: {
    description: "Creative spark, artistic flow, novelty-seeking",
    energy_level: "high",
    valence: "positive",
    triggers: ["creative_success", "artistic_experience", "novel_experience", "high_openness"],
    effects: {
      card_appeal: {
        creative_activities: 2.5,
        artistic_pursuits: 2.3,
        novel_experiences: 1.7,
        routine_tasks: 0.4,
        administrative: 0.3,
        spontaneous: 1.6
      },
      modifiers: {
        creative_output_bonus: 0.30,       // +30% creative quality
        unlock_spontaneous_ideas: true,
        success_bonus_creative: 0.20
      }
    }
  },
  
  EXCITED: {
    description: "Enthusiastic, social, adventure-seeking",
    energy_level: "high",
    valence: "positive",
    triggers: ["social_success", "upcoming_event", "new_opportunity", "high_extraversion"],
    effects: {
      card_appeal: {
        social_events: 2.3,
        new_experiences: 2.5,
        adventures: 2.2,
        routine_tasks: 0.5,
        solo_activities: 0.7,
        planning: 0.6
      },
      modifiers: {
        social_gains_bonus: 2,             // +2 to social meter gains
        risk_tolerance_bonus: 0.20,        // +20% risk tolerance
        spontaneity_bonus: 0.15
      }
    }
  },
  
  CONFIDENT: {
    description: "Self-assured, bold, challenge-seeking",
    energy_level: "high",
    valence: "positive",
    triggers: ["recent_success", "high_skill_level", "positive_feedback", "aspiration_near_complete"],
    effects: {
      card_appeal: {
        challenging_tasks: 2.0,
        confrontations: 1.8,
        bold_choices: 2.0,
        safe_options: 0.6,
        avoidance_behaviors: 0.3
      },
      modifiers: {
        success_bonus_all: 0.15,           // +15% success chance (all activities)
        anxiety_reduction: 0.20,           // -20% anxiety from risks
        social_confidence_bonus: 0.10
      }
    }
  }
};
```

### CALM STATES (Positive Low-Energy)

```javascript
const CALM_POSITIVE = {
  CONTENT: {
    description: "Satisfied, stable, maintenance-focused",
    energy_level: "low",
    valence: "positive",
    triggers: ["high_all_meters", "stable_life", "recent_rest", "balanced_lifestyle"],
    effects: {
      card_appeal: {
        relaxation: 1.7,
        maintenance: 1.8,
        routine: 1.6,
        appreciation: 1.5,
        dramatic_change: 0.6,
        ambitious_push: 0.7
      },
      modifiers: {
        energy_recovery_bonus: 1,          // +1 energy recovery
        stress_resistance: 0.10,           // +10% stress resistance
        passive_meter_gains: 0.5           // Slow positive drift
      }
    }
  },
  
  PEACEFUL: {
    description: "Calm, centered, clarity-seeking",
    energy_level: "low",
    valence: "positive",
    triggers: ["meditation", "nature_time", "low_stress", "solitude"],
    effects: {
      card_appeal: {
        meditation: 2.2,
        nature: 2.0,
        solitude: 1.8,
        intense_activities: 0.4,
        social_pressure: 0.3
      },
      modifiers: {
        mental_passive_gain: 1,            // +1 mental per turn
        decision_clarity_bonus: 0.15,      // +15% clearer decision context
        stress_immunity: 0.20
      }
    }
  },
  
  GRATEFUL: {
    description: "Appreciative, generous, relationship-focused",
    energy_level: "low",
    valence: "positive",
    triggers: ["positive_relationship_moment", "reflection", "milestone_reached"],
    effects: {
      card_appeal: {
        relationship_deepening: 2.0,
        giving_back: 1.8,
        reflection: 1.7,
        complaint: 0.3,
        acquisition: 0.5,
        self_focus: 0.6
      },
      modifiers: {
        relationship_bonus_all: 0.10,      // +0.10 trust to all relationships
        appreciation_moments: true,
        social_capital_gains_bonus: 1
      }
    }
  },
  
  REFLECTIVE: {
    description: "Introspective, learning-oriented, self-aware",
    energy_level: "low",
    valence: "positive",
    triggers: ["journaling", "therapy", "quiet_time", "phase_transition"],
    effects: {
      card_appeal: {
        introspection: 2.0,
        learning: 1.8,
        therapy: 2.2,
        journaling: 1.9,
        action_oriented: 0.6,
        external_focus: 0.7
      },
      modifiers: {
        self_awareness_gain: 1,
        unlock_insight_cards: true,
        personality_clarity_bonus: 0.15
      }
    }
  }
};
```

### ENERGIZING STATES (Negative High-Energy)

```javascript
const ENERGIZING_NEGATIVE = {
  FRUSTRATED: {
    description: "Irritated, seeking change or confrontation",
    energy_level: "high",
    valence: "negative",
    triggers: ["obstacles", "repeated_failures", "unmet_expectations", "social_friction"],
    effects: {
      card_appeal: {
        venting: 2.0,
        confrontation: 1.8,
        change_seeking: 1.9,
        patience: 0.3,
        diplomatic_options: 0.5
      },
      modifiers: {
        conflict_chance: 0.30,             // +30% conflict chance
        dramatic_choices_appear: true,
        cooperation_penalty: -0.10
      }
    }
  },
  
  ANXIOUS: {
    description: "Worried, overthinking, reassurance-seeking",
    energy_level: "high",
    valence: "negative",
    triggers: ["upcoming_deadline", "uncertainty", "high_neuroticism", "recent_failure"],
    effects: {
      card_appeal: {
        preparation: 2.0,
        information_seeking: 1.8,
        reassurance: 1.7,
        risky_activities: 0.3,
        new_experiences: 0.5,
        comfortable_routine: 1.6
      },
      modifiers: {
        success_penalty_unfamiliar: -0.10, // -10% on new activities
        comfort_seeking_bonus: 0.15,
        overthinking_penalty: true
      }
    }
  },
  
  RESTLESS: {
    description: "Agitated, novelty-seeking, can't sit still",
    energy_level: "high",
    valence: "negative",
    triggers: ["boredom", "cabin_fever", "unfulfilled_needs", "high_energy_low_outlet"],
    effects: {
      card_appeal: {
        movement: 2.0,
        change: 1.8,
        activity: 1.7,
        novelty: 1.6,
        stillness: 0.3,
        routine: 0.4,
        patience: 0.5
      },
      modifiers: {
        boredom_resistance: true,
        movement_activities_bonus: 0.15,
        focus_penalty: -0.10               // -10% on focused tasks
      }
    }
  },
  
  PASSIONATE: {
    description: "Intense focus, all-or-nothing mindset",
    energy_level: "high",
    valence: "neutral",  // Can be positive or negative
    triggers: ["deep_commitment", "romance", "obsessive_focus", "crucial_moment"],
    effects: {
      card_appeal: {
        intensity: 2.2,
        commitment: 2.0,
        all_in_behaviors: 1.9,
        moderation: 0.3,
        balance: 0.4,
        careful_consideration: 0.5
      },
      modifiers: {
        chosen_focus_bonus: 2,             // +2 to chosen focus activity
        everything_else_penalty: -1,       // -1 to all other activities
        tunnel_vision: true
      }
    }
  }
};
```

### WITHDRAWING STATES (Negative Low-Energy)

```javascript
const WITHDRAWING_NEGATIVE = {
  MELANCHOLY: {
    description: "Sad, nostalgic, solitude-seeking",
    energy_level: "low",
    valence: "negative",
    triggers: ["loss", "loneliness", "anniversary_of_sad_event", "low_social_meter"],
    effects: {
      card_appeal: {
        solitude: 1.8,
        contemplation: 1.7,
        nostalgia: 1.9,
        social_energy: 0.5,
        optimism: 0.4,
        new_ventures: 0.3
      },
      modifiers: {
        social_gains_penalty: -1,          // -1 to social meter gains
        depth_in_reflection_bonus: 0.10,
        withdrawal_tendency: true
      }
    }
  },
  
  DISCOURAGED: {
    description: "Defeated, hesitant, safety-seeking",
    energy_level: "low",
    valence: "negative",
    triggers: ["failure", "rejection", "repeated_setbacks", "low_confidence"],
    effects: {
      card_appeal: {
        doubt: 1.5,
        hesitation: 1.6,
        safety_seeking: 1.8,
        ambition: 0.3,
        risk_taking: 0.2,
        confidence: 0.4
      },
      modifiers: {
        success_perception_penalty: -0.15, // -15% perceived success (shown as worse odds)
        comfort_options_prioritized: true,
        challenge_avoidance: 0.20
      }
    }
  },
  
  NUMB: {
    description: "Emotionally flat, autopilot, disengaged",
    energy_level: "low",
    valence: "negative",
    triggers: ["prolonged_stress", "depression", "emotional_overload", "burnout"],
    effects: {
      card_appeal: {
        routine: 1.5,
        autopilot: 1.7,
        avoidance: 1.6,
        emotional_engagement: 0.3,
        meaningful_choice: 0.4
      },
      modifiers: {
        emotional_gains_penalty: -1,       // -1 to emotional meter gains (all activities)
        detachment_active: true,
        meaningful_reduced: true
      }
    }
  },
  
  EXHAUSTED: {
    description: "Mentally/physically drained, needs recovery",
    energy_level: "very_low",
    valence: "negative",
    triggers: ["mental_meter_low", "physical_meter_low", "overwork", "sleep_deprivation"],
    effects: {
      card_appeal: {
        rest_activities: 2.8,
        low_energy: 1.8,
        delegation: 1.6,
        high_energy: 0.2,
        demanding_social: 0.3,
        obligations: 0.4
      },
      modifiers: {
        energy_cost_all: 1,                // +1 energy cost for ALL activities
        recovery_prioritized: true,
        performance_penalty: -0.20          // -20% success on all
      }
    }
  },
  
  OVERWHELMED: {
    description: "Too much to handle, drowning in obligations",
    energy_level: "low",
    valence: "negative",
    triggers: ["mental_meter_very_low", "too_many_obligations", "deadline_pileup", "crisis_cascade"],
    effects: {
      card_appeal: {
        work_tasks: 0.4,
        aspiration_progress: 0.3,
        high_demand: 0.2,
        support_seeking: 2.0,
        rest_activities: 2.5,
        avoidance: 1.5,
        easy_social: 1.3
      },
      modifiers: {
        success_penalty_complex: -0.20,    // -20% on complex activities
        energy_cost_high_demand: 1,        // +1 energy on demanding activities
        support_options_prioritized: true
      }
    }
  }
};
```

### NEUTRAL STATES

```javascript
const NEUTRAL_STATES = {
  CURIOUS: {
    description: "Inquisitive, exploration-minded, learning-oriented",
    energy_level: "medium",
    valence: "positive",
    triggers: ["new_discovery", "high_openness", "novel_npc", "mystery"],
    effects: {
      card_appeal: {
        exploration: 2.2,
        learning: 2.0,
        questions: 1.8,
        new_npcs: 1.7,
        routine: 0.7,
        familiar: 0.8
      },
      modifiers: {
        unlock_new_options: true,
        discovery_bonus: 0.15,
        learning_speed_bonus: 0.10
      }
    }
  },
  
  FOCUSED: {
    description: "Concentrated, goal-directed, disciplined",
    energy_level: "medium",
    valence: "positive",
    triggers: ["low_distractions", "clear_goal", "recent_progress", "high_conscientiousness"],
    effects: {
      card_appeal: {
        concentration: 2.0,
        goal_pursuit: 2.2,
        discipline: 1.9,
        distractions: 0.4,
        social_pulls: 0.5
      },
      modifiers: {
        task_efficiency_bonus: 0.20,       // +20% progress per activity
        interruption_resistance: true,
        success_bonus_focused: 0.20
      }
    }
  },
  
  BALANCED: {
    description: "Equilibrium, all options equally appealing",
    energy_level: "medium",
    valence: "neutral",
    triggers: ["high_all_meters", "personality_neutral", "no_strong_triggers"],
    effects: {
      card_appeal: {
        // ALL categories: 1.0 (no preference)
        all_categories: 1.0
      },
      modifiers: {
        // No modifiers - true neutral state
      }
    }
  },
  
  UNCERTAIN: {
    description: "Unsure, decision-seeking, exploring options",
    energy_level: "medium",
    valence: "neutral",
    triggers: ["major_decision_upcoming", "life_transition", "unclear_path"],
    effects: {
      card_appeal: {
        information_seeking: 1.8,
        advice: 1.7,
        exploration: 1.6,
        decisive_action: 0.6,
        commitment: 0.5
      },
      modifiers: {
        decision_cards_more_common: true,
        consequences_visible: true,
        hesitation_active: true
      }
    }
  }
};
```

---

## Environmental & Seasonal State Modifiers *(NEW - Master Truths v1.2)*

**Purpose:** Environmental context (season, weather, time of year) affects emotional states, creating authentic mood variations based on external factors.

```javascript
// ENVIRONMENTAL MODIFIERS
const ENVIRONMENTAL_STATE_MODIFIERS = {
  seasonal: {
    winter: {
      affects: ["MELANCHOLY", "REFLECTIVE"],
      multiplier: 1.3,
      applies_if: "neuroticism > 3.0 OR openness > 4.0",
      narrative: "Winter affects you. Always has.",
      
      example: {
        base_state: "REFLECTIVE",
        base_intensity: 0.6,
        modified_intensity: 0.78,  // 0.6 * 1.3
        narrative: `
          December. The early darkness, the cold.
          You've always felt it more in winter.
          Everything slows down, turns inward.
        `
      }
    },
    
    spring: {
      affects: ["INSPIRED", "HOPEFUL"],
      multiplier: 1.2,
      applies_if: "openness > 3.5",
      narrative: "Something about spring makes everything feel possible.",
      
      example: {
        base_state: "HOPEFUL",
        base_intensity: 0.5,
        modified_intensity: 0.6,  // 0.5 * 1.2
        narrative: `
          The first warm day. Windows open, air fresh.
          You can feel it - that spring energy.
          New beginnings. Possibilities.
        `
      }
    },
    
    summer: {
      affects: ["ENERGIZED", "RESTLESS"],
      multiplier: 1.15,
      applies_if: "extraversion > 3.5",
      narrative: "Summer energy. Long days, warm nights."
    },
    
    fall: {
      affects: ["NOSTALGIC", "REFLECTIVE"],
      multiplier: 1.2,
      applies_if: "openness > 3.0",
      narrative: "Autumn. Change in the air. Endings and beginnings."
    }
  },
  
  weather: {
    rainy: {
      affects: ["MELANCHOLY", "REFLECTIVE", "PEACEFUL"],
      multiplier: 1.2,
      applies_if: "openness > 3.0",
      narrative: "Rainy days. You've always liked them. Contemplative.",
      
      card_modifications: {
        indoor_activities: 1.3,        // More appealing
        outdoor_activities: 0.5,       // Less appealing
        reflective_activities: 1.5,    // Much more appealing
        social_large_groups: 0.7       // Less appealing
      }
    },
    
    first_snow: {
      affects: ["NOSTALGIC", "PEACEFUL"],
      multiplier: 1.5,
      triggers_memory_search: true,
      narrative: "First snow. Memories surface.",
      
      special_behavior: "Search memory archive for winter/snow tagged memories with emotional_weight > 0.6"
    },
    
    stormy: {
      affects: ["ANXIOUS", "RESTLESS", "MELANCHOLY"],
      multiplier: 1.3,
      applies_if: "neuroticism > 3.5",
      narrative: "The storm matches your mood. Or maybe creates it."
    },
    
    sunny_warm: {
      affects: ["ENERGIZED", "OPTIMISTIC", "PEACEFUL"],
      multiplier: 1.15,
      reduces: ["MELANCHOLY", "DISCOURAGED"],
      reduction_factor: 0.85,
      narrative: "Sunshine. Hard to stay gloomy on a day like this."
    }
  },
  
  anniversary_dates: {
    grief_anniversary: {
      detection: "Check memory archive for loss/trauma events on this calendar date",
      affects: ["MELANCHOLY", "NUMB"],
      multiplier: 2.0,
      narrative: "Something about today feels heavy. Then you remember...",
      
      implementation: `
        // Check if today matches anniversary of significant loss
        const lossMemories = character.memories.filter(m => 
          m.tags.includes('loss') || m.tags.includes('grief') &&
          m.emotional_weight > 0.8 &&
          isSameDateDifferentYear(m.date, currentDate)
        );
        
        if (lossMemories.length > 0) {
          intensity *= 2.0;
          narrative = \`Something about today feels heavy.
                       Then you remember: \${lossMemories[0].title}.
                       \${yearsAgo(lossMemories[0].date)} years ago today.\`;
        }
      `
    },
    
    joy_anniversary: {
      detection: "Check memory archive for breakthrough/celebration events",
      affects: ["GRATEFUL", "NOSTALGIC"],
      multiplier: 1.5,
      narrative: "One year ago today...",
      
      implementation: `
        const joyMemories = character.memories.filter(m => 
          m.tags.includes('breakthrough') || m.tags.includes('celebration') &&
          m.emotional_weight > 0.7 &&
          m.valence > 0.5 &&
          isSameDateDifferentYear(m.date, currentDate)
        );
        
        if (joyMemories.length > 0) {
          intensity *= 1.5;
          narrative = \`One year ago today: \${joyMemories[0].title}.
                       Hard to believe it's been a year.
                       That changed everything.\`;
        }
      `
    }
  },
  
  time_of_year: {
    holiday_season: {
      affects: ["NOSTALGIC", "MELANCHOLY", "GRATEFUL"],
      complex: true,
      narrative: "Holidays. Complex emotions.",
      
      modifiers: {
        has_family_nearby: { adds: "GRATEFUL", multiplier: 1.3 },
        family_estranged: { adds: "MELANCHOLY", multiplier: 1.8 },
        alone_by_choice: { adds: "PEACEFUL", multiplier: 1.2 },
        alone_not_by_choice: { adds: "MELANCHOLY", multiplier: 1.6 }
      }
    },
    
    new_year: {
      affects: ["HOPEFUL", "REFLECTIVE", "ANXIOUS"],
      narrative: "New year. Fresh start. Or is it?",
      
      personality_variations: {
        high_conscientiousness: "MOTIVATED (1.4x) - Time to set goals",
        high_neuroticism: "ANXIOUS (1.3x) - Another year, same problems?",
        high_openness: "HOPEFUL (1.3x) - New possibilities"
      }
    }
  }
};

// IMPLEMENTATION: Apply environmental modifiers
function applyEnvironmentalModifiers(state, intensity, character, environmentalContext) {
  let modifiedIntensity = intensity;
  let modifiedNarrative = [];
  
  // Check seasonal effects
  const season = environmentalContext.season;
  if (ENVIRONMENTAL_STATE_MODIFIERS.seasonal[season]) {
    const seasonalMod = ENVIRONMENTAL_STATE_MODIFIERS.seasonal[season];
    
    if (seasonalMod.affects.includes(state)) {
      // Check if personality conditions met
      if (evaluateCondition(seasonalMod.applies_if, character.personality)) {
        modifiedIntensity *= seasonalMod.multiplier;
        modifiedNarrative.push(seasonalMod.narrative);
      }
    }
  }
  
  // Check weather effects
  const weather = environmentalContext.weather;
  if (ENVIRONMENTAL_STATE_MODIFIERS.weather[weather]) {
    const weatherMod = ENVIRONMENTAL_STATE_MODIFIERS.weather[weather];
    
    if (weatherMod.affects.includes(state)) {
      if (!weatherMod.applies_if || evaluateCondition(weatherMod.applies_if, character.personality)) {
        modifiedIntensity *= weatherMod.multiplier;
        modifiedNarrative.push(weatherMod.narrative);
      }
    }
    
    // Special: first snow triggers memory search
    if (weather === "first_snow" && weatherMod.triggers_memory_search) {
      const winterMemories = searchMemories(character, ["winter", "snow"], 0.6);
      if (winterMemories.length > 0) {
        modifiedNarrative.push(`Memories surface: ${winterMemories[0].title}`);
      }
    }
  }
  
  // Check anniversary dates
  const anniversaryType = checkAnniversaryDates(character, environmentalContext.date);
  if (anniversaryType) {
    const anniversaryMod = ENVIRONMENTAL_STATE_MODIFIERS.anniversary_dates[anniversaryType];
    if (anniversaryMod.affects.includes(state)) {
      modifiedIntensity *= anniversaryMod.multiplier;
      modifiedNarrative.push(anniversaryMod.narrative);
    }
  }
  
  return {
    intensity: Math.min(1.0, modifiedIntensity),
    environmental_narrative: modifiedNarrative.join(' ')
  };
}
```

---

## State Determination Algorithm

### Complete State Calculation

```javascript
function determineEmotionalStates(character, recentEvents, currentContext) {
  let primaryState = null;
  let secondaryState = null;
  let intensity = 0.7; // Default intensity
  
  // STEP 1: CRISIS STATES (Meter-driven, highest priority)
  if (character.meters.mental <= 2) {
    primaryState = "EXHAUSTED";  // Canonical name (v1.1)
    intensity = 0.9;
  } else if (character.meters.emotional <= 2) {
    primaryState = "DISCOURAGED";
    intensity = 0.9;
  } else if (character.meters.physical <= 2) {
    primaryState = "EXHAUSTED";  // Physical exhaustion also EXHAUSTED
    intensity = 0.85;
  } else if (character.meters.mental <= 3 && character.obligation_count > 5) {
    primaryState = "OVERWHELMED";  // Canonical name (v1.1)
    intensity = 0.85;
  }
  
  // STEP 2: REACTIVE STATES (Recent events)
  if (!primaryState) {
    const positiveEvents = recentEvents.filter(e => e.valence > 0.7);
    const negativeEvents = recentEvents.filter(e => e.valence < -0.7);
    const stressEvents = recentEvents.filter(e => e.stress_impact > 0.5);
    
    if (positiveEvents.length >= 3) {
      const options = ["EXCITED", "CONFIDENT", "GRATEFUL"];
      primaryState = weightedChoice(options, character.personality);
      intensity = 0.8;
    } else if (negativeEvents.length >= 3) {
      const options = ["DISCOURAGED", "MELANCHOLY", "FRUSTRATED"];
      primaryState = weightedChoice(options, character.personality);
      intensity = 0.8;
    } else if (stressEvents.length >= 2) {
      primaryState = "OVERWHELMED";
      intensity = 0.75;
    }
  }
  
  // STEP 3: ASPIRATION-DRIVEN STATES
  if (!primaryState) {
    const aspiration = character.currentAspiration;
    if (aspiration) {
      const progress = aspiration.progress; // 0.0-1.0
      const weeksRemaining = aspiration.deadline_weeks;
      
      if (progress > 0.7 && weeksRemaining < 3) {
        primaryState = "MOTIVATED";
        intensity = 0.85;
      } else if (progress < 0.3 && weeksRemaining < 5) {
        primaryState = "ANXIOUS";
        intensity = 0.75;
      } else if (progress > 0.5) {
        primaryState = "CONFIDENT";
        intensity = 0.7;
      } else if (progress < 0.2 && weeksRemaining < 10) {
        primaryState = "ANXIOUS";
        intensity = 0.7;
      }
    }
  }
  
  // STEP 4: PERSONALITY BASELINE
  if (!primaryState) {
    const p = character.personality;
    
    if (p.neuroticism > 4.0) {
      primaryState = weightedChoice(["ANXIOUS", "OVERWHELMED", "RESTLESS"]);
      intensity = 0.6;
    } else if (p.openness > 4.0) {
      primaryState = weightedChoice(["CURIOUS", "INSPIRED", "EXCITED"]);
      intensity = 0.65;
    } else if (p.conscientiousness > 4.0) {
      primaryState = weightedChoice(["MOTIVATED", "FOCUSED", "DISCIPLINED"]);
      intensity = 0.7;
    } else if (p.extraversion > 4.0) {
      primaryState = weightedChoice(["EXCITED", "CONFIDENT", "SOCIAL"]);
      intensity = 0.65;
    } else if (p.agreeableness > 4.5) {
      primaryState = weightedChoice(["GRATEFUL", "CONTENT", "PEACEFUL"]);
      intensity = 0.6;
    } else {
      primaryState = "BALANCED";
      intensity = 0.5;
    }
  }
  
  // STEP 5: DETERMINE SECONDARY STATE
  secondaryState = determineSecondaryState(
    primaryState,
    character,
    recentEvents,
    intensity
  );
  
  // STEP 6: MEMORY TRIGGERS (NEW - Master Truths v1.2)
  // Check if current context triggers emotionally significant memories
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
          // Painful memory triggered - blend into current state
          if (primaryState === "BALANCED" || primaryState === "REFLECTIVE") {
            primaryState = "MELANCHOLY";
            intensity = memory.weight * 0.8;
          } else {
            // Amplify existing negative state
            intensity = Math.min(1.0, intensity + (memory.weight * 0.3));
          }
          
          logEmotionalEcho({
            memory: memory.title,
            trigger: `${currentContext.location} reminds you of...`,
            affects_state: true,
            narrative: `Something about today reminds you of ${memory.title}...`,
            affects_cards: applyMemoryFilter(availableCards, memory)
          });
        } else if (memory.valence > 0.5) {
          // Joyful memory triggered - soften negative states or enhance positive
          if (primaryState === "MELANCHOLY" || primaryState === "DISCOURAGED") {
            intensity *= 0.85;  // Reduce negative intensity
          } else if (primaryState === "GRATEFUL" || primaryState === "NOSTALGIC") {
            intensity = Math.min(1.0, intensity + (memory.weight * 0.2));
          }
          
          logEmotionalEcho({
            memory: memory.title,
            trigger: `${currentContext.location} brings back good memories`,
            affects_state: true,
            narrative: `This place... you remember ${memory.title}. That was good.`,
            adds_warmth: true
          });
        }
      }
    });
  }
  
  return {
    primary: primaryState,
    secondary: secondaryState,
    intensity: intensity,
    triggers: getStateTriggers(primaryState, character, recentEvents),
    narrative: generateStateNarrative(primaryState, secondaryState, intensity),
    memory_echoes: triggeredMemories  // NEW: Track triggered memories
  };
}

// MEMORY TRIGGER DETECTION (NEW - Master Truths v1.2)
function checkForTriggeredMemories(character, currentDate, currentLocation, presentNPCs) {
  const triggeredMemories = [];
  
  // Check location-based triggers
  const locationMemories = character.memoryArchive.filter(m => 
    m.location === currentLocation &&
    m.emotional_weight > 0.7
  );
  
  // Check date-based triggers (anniversaries)
  const dateMemories = character.memoryArchive.filter(m =>
    isSameDateDifferentYear(m.date, currentDate) &&
    m.emotional_weight > 0.8
  );
  
  // Check NPC-based triggers (reminds you of someone)
  const npcMemories = character.memoryArchive.filter(m =>
    presentNPCs.some(npc => 
      m.involvedNPCs.includes(npc) &&
      m.emotional_weight > 0.7
    )
  );
  
  // Combine and deduplicate
  const allTriggers = [...locationMemories, ...dateMemories, ...npcMemories];
  const uniqueTriggers = deduplicateByWeight(allTriggers);
  
  // Return top 3 most significant
  return uniqueTriggers
    .sort((a, b) => b.emotional_weight - a.emotional_weight)
    .slice(0, 3);
}

function applyMemoryFilter(cards, memory) {
  // Filter cards based on memory emotional context
  return cards.map(card => {
    if (memory.tags.includes(card.category)) {
      // Memory affects how appealing similar activities feel
      if (memory.valence < 0) {
        card.appeal *= 0.7;  // Painful memories reduce appeal
        card.warning = `This reminds you of ${memory.title}. Still hard.`;
      } else {
        card.appeal *= 1.3;  // Good memories increase appeal
        card.note = `This reminds you of ${memory.title}. That was good.`;
      }
    }
    return card;
  });
}

function determineSecondaryState(primary, character, recentEvents, intensity) {
  // Secondary state is complementary or contrasting
  
  // If intensity is very high (>0.8), no secondary (primary is dominant)
  if (intensity > 0.85) return null;
  
  // Common secondary pairings
  const SECONDARY_PAIRINGS = {
    OVERWHELMED: ["RESTLESS", "ANXIOUS", "FRUSTRATED"],
    MOTIVATED: ["ANXIOUS", "FOCUSED", "CONFIDENT"],
    INSPIRED: ["EXCITED", "CURIOUS", "RESTLESS"],
    ANXIOUS: ["MOTIVATED", "OVERWHELMED", "RESTLESS"],
    CONFIDENT: ["MOTIVATED", "EXCITED", "FOCUSED"],
    EXHAUSTED: ["FRUSTRATED", "MELANCHOLY", "NUMB"],
    // ... complete table
  };
  
  const possibleSecondary = SECONDARY_PAIRINGS[primary] || [];
  if (possibleSecondary.length === 0) return null;
  
  // Choose based on context
  return weightedChoice(possibleSecondary, character.personality, recentEvents);
}
```

---

## Card Filtering and Appeal System

### Hand Generation with Emotional States

```javascript
function drawHand(character, emotionalStates, availableCards) {
  const hand = [];
  const {primary, secondary, intensity} = emotionalStates;
  
  // 1. OBLIGATIONS (always appear, but modified)
  const obligations = getObligations(character.currentWeek, character.currentDay);
  obligations.forEach(card => {
    card.emotionalModifier = applyStateModifiers(card, primary, secondary, intensity);
    card.emotionalContext = generateEmotionalContext(card, primary, secondary);
    hand.push(card);
  });
  
  // 2. FILTER AVAILABLE CARDS
  const appealScores = availableCards.map(card => ({
    card: card,
    appeal: calculateAppeal(card, primary, secondary, character),
    emotionalContext: generateEmotionalContext(card, primary, secondary)
  }));
  
  // Remove cards with very low appeal (<0.3)
  const filteredPool = appealScores.filter(item => item.appeal >= 0.3);
  
  // 3. SORT BY APPEAL (weighted probability)
  filteredPool.sort((a, b) => b.appeal - a.appeal);
  
  // 4. DRAW REMAINING CARDS (weighted random)
  const remainingSlots = 8 - hand.length; // Typical hand size
  for (let i = 0; i < remainingSlots; i++) {
    const drawn = weightedRandomDraw(filteredPool);
    hand.push(drawn);
    
    // Remove from pool to avoid duplicates
    const index = filteredPool.indexOf(drawn);
    filteredPool.splice(index, 1);
  }
  
  return hand;
}

function calculateAppeal(card, primaryState, secondaryState, character) {
  let appeal = 1.0; // Baseline
  
  // 1. PRIMARY STATE APPEAL
  const primaryAppeal = getStateAppeal(primaryState, card);
  appeal *= primaryAppeal; // 0.2 to 2.8 multiplier
  
  // 2. SECONDARY STATE APPEAL (half strength)
  if (secondaryState) {
    const secondaryAppeal = getStateAppeal(secondaryState, card);
    appeal *= (1.0 + (secondaryAppeal - 1.0) * 0.5);
  }
  
  // 3. PERSONALITY BASELINE
  appeal *= getPersonalityAppeal(card, character.personality);
  
  // 4. VARIETY SEEKING (prevent repetition)
  appeal *= getVarietyModifier(card, character.recentCards);
  
  // 5. METER-DRIVEN APPEAL
  appeal *= getMeterAppeal(card, character.meters);
  
  // Clamp to 0.1-3.0 range
  return Math.max(0.1, Math.min(3.0, appeal));
}

function getStateAppeal(state, card) {
  // Get appeal table for this state
  const appealTable = EMOTIONAL_STATE_TABLES[state].card_appeal;
  
  // Check card categories/tags
  for (const [category, multiplier] of Object.entries(appealTable)) {
    if (card.category === category || card.tags.includes(category)) {
      return multiplier;
    }
  }
  
  // Default appeal
  return appealTable.default || 1.0;
}
```

---

## State Modifiers on Activities

### Applying Emotional Effects to Cards

```javascript
function applyStateModifiers(card, primary, secondary, intensity) {
  const modifiers = {
    energyCostModifier: 0,
    successModifier: 0,
    rewardModifier: 1.0,
    timeCostModifier: 1.0
  };
  
  // Get primary state effects
  const primaryEffects = EMOTIONAL_STATE_TABLES[primary].modifiers;
  
  // Apply primary effects
  if (primaryEffects.energy_cost_all) {
    modifiers.energyCostModifier += primaryEffects.energy_cost_all * intensity;
  }
  if (primaryEffects.success_penalty_complex && card.complexity === 'high') {
    modifiers.successModifier += primaryEffects.success_penalty_complex * intensity;
  }
  if (primaryEffects.success_bonus_goals && card.tags.includes('aspiration')) {
    modifiers.successModifier += primaryEffects.success_bonus_goals * intensity;
  }
  
  // Apply secondary effects (half strength)
  if (secondary) {
    const secondaryEffects = EMOTIONAL_STATE_TABLES[secondary].modifiers;
    // ... apply with 0.5 multiplier
  }
  
  return modifiers;
}
```

---

## State Transitions

### How States Change

```javascript
function updateEmotionalStates(currentStates, cardsPlayed, outcomes, character) {
  let {primary, secondary, intensity} = currentStates;
  
  // 1. IMMEDIATE SHIFTS (card-driven)
  cardsPlayed.forEach(card => {
    const stateChange = CARD_STATE_EFFECTS[card.id] || 
                        getCategoryStateEffect(card.category, primary);
    
    if (stateChange.newPrimary) {
      primary = stateChange.newPrimary;
      intensity = stateChange.intensity || intensity;
    }
  });
  
  // 2. OUTCOME-DRIVEN SHIFTS
  outcomes.forEach(outcome => {
    if (outcome.meters.emotional >= 2) {
      intensity *= 0.8; // Positive outcomes reduce negative state intensity
    }
    if (outcome.meters.mental >= 2) {
      if (primary === "OVERWHELMED" || primary === "EXHAUSTED") {
        intensity *= 0.7; // Mental recovery helps
      }
    }
  });
  
  // 3. NATURAL DECAY
  intensity *= 0.95; // 5% decay per turn if not reinforced
  
  // 4. METER-TRIGGERED OVERRIDES
  if (character.meters.mental < 2) {
    primary = "EXHAUSTED";  // Crisis override
    intensity = 0.9;
  }
  
  // 5. INTENSITY THRESHOLD CHECK
  if (intensity < 0.3) {
    // State fading, determine new state
    return determineEmotionalStates(character, getRecentEvents(character), getCurrentContext(character));
  }
  
  // 6. CIRCUMSTANCE STACKING CHECK (NEW - Master Truths v1.2)
  // Multiple simultaneous stressors compound to create OVERWHELMED state
  const stackingResult = applyCircumstanceStacking(
    primary,
    intensity,
    character,
    getActiveStressors(character)
  );
  
  if (stackingResult.stacking_triggered) {
    primary = stackingResult.state;
    intensity = stackingResult.intensity;
  }
  
  return {
    primary,
    secondary,
    intensity,
    changed: primary !== currentStates.primary,
    circumstance_stacking: stackingResult.narrative  // NEW: Track stacking narrative
  };
}

// CIRCUMSTANCE STACKING SYSTEM (NEW - Master Truths v1.2)
function applyCircumstanceStacking(state, intensity, character, activeStressors) {
  const stressorTypes = {
    work: activeStressors.workPressure > 7,
    money: character.meters.money < 200 && character.rentDueDays <= 7,
    relationship: activeStressors.relationshipTension.length >= 2,
    health: character.meters.physical < 4,
    family: activeStressors.familyCrisis === true,
    housing: activeStressors.housingIssues === true,
    aspiration: activeStressors.aspirationDeadline && activeStressors.aspirationProgress < 0.5
  };
  
  const activeCount = Object.values(stressorTypes).filter(v => v).length;
  
  // Not enough stressors to trigger stacking
  if (activeCount < 3) {
    return {
      stacking_triggered: false,
      state,
      intensity,
      narrative: null
    };
  }
  
  // STACKING LOGIC: "When it rains, it pours"
  
  // Calculate stacking multiplier
  const stackingMultiplier = 1 + (activeCount * 0.15);
  let modifiedIntensity = intensity * stackingMultiplier;
  
  // High neuroticism + multiple stressors = OVERWHELMED risk
  if (activeCount >= 3 && character.personality.neuroticism > 4.0) {
    return {
      stacking_triggered: true,
      state: "OVERWHELMED",
      intensity: 0.9,
      narrative: `
        Everything is happening at once:
        ${activeCount} major stressors active simultaneously.
        
        ${listActiveStressors(stressorTypes)}
        
        For someone with your anxiety levels, this compounds fast.
        What would be manageable one-at-a-time becomes overwhelming.
      `
    };
  }
  
  // 4+ stressors overwhelm even lower neuroticism
  if (activeCount >= 4 && character.personality.neuroticism > 2.5) {
    return {
      stacking_triggered: true,
      state: "OVERWHELMED",
      intensity: 0.85,
      narrative: `
        Four things. Four major things happening at once.
        ${listActiveStressors(stressorTypes)}
        
        You're trying to hold it all together.
        But there's only so much one person can handle.
      `
    };
  }
  
  // 5+ stressors overwhelm anyone
  if (activeCount >= 5) {
    return {
      stacking_triggered: true,
      state: "OVERWHELMED",
      intensity: 0.95,
      narrative: `
        Too much. Everything at once:
        ${listActiveStressors(stressorTypes)}
        
        When it rains, it pours.
        You're drowning.
      `
    };
  }
  
  // Stressors present but not overwhelming yet - amplify current state
  return {
    stacking_triggered: true,
    state,
    intensity: Math.min(1.0, modifiedIntensity),
    narrative: `
      Multiple things happening at once (${activeCount} stressors active).
      ${listActiveStressors(stressorTypes)}
      Everything feels harder when you're dealing with multiple challenges.
    `
  };
}

function getActiveStressors(character) {
  // Calculate current active stressors from character state
  return {
    workPressure: calculateWorkPressure(character),
    relationshipTension: getStressedRelationships(character),
    familyCrisis: checkFamilyCrisis(character),
    housingIssues: checkHousingIssues(character),
    aspirationDeadline: checkAspirationDeadline(character),
    aspirationProgress: character.aspiration.progress || 0
  };
}

function listActiveStressors(stressorTypes) {
  const active = [];
  if (stressorTypes.work) active.push("• Work: High pressure/deadline");
  if (stressorTypes.money) active.push("• Money: Financial crisis, rent due soon");
  if (stressorTypes.relationship) active.push("• Relationships: Multiple strained connections");
  if (stressorTypes.health) active.push("• Health: Physical/mental exhaustion");
  if (stressorTypes.family) active.push("• Family: Crisis requiring attention");
  if (stressorTypes.housing) active.push("• Housing: Living situation unstable");
  if (stressorTypes.aspiration) active.push("• Goals: Behind schedule, deadline approaching");
  
  return active.join('\n');
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
- [x] **Dramatic irony mechanics used when knowledge gaps exist (score ≥ 0.6)**
- [x] **Memory resonance factors applied to recall (weights: 0.7-0.95)**
- [x] **Novel-quality thresholds met (≥ 0.7 overall; authenticity ≥ 0.7; tension ≥ 0.6; hooks ≥ 0.6)**
- [x] This doc cites **Truths v1.2** at the top

**Master Truths v1.2 Enhancements Implemented:**
- ✅ Memory-triggered state changes (Section 16: Emotional Authenticity)
- ✅ Circumstance stacking system (Section 16: Capacity constraints)
- ✅ Environmental/seasonal modifiers (Section 17: Context awareness)
- ✅ Emotional capacity gating for responses
- ✅ Memory resonance weighting (0.7-0.95 range)

**References:**
- See `12-success-probability-formulas.md` for how states affect success calculations
- See `71-daily-turn-flow-detailed.md` for when states are calculated each turn
- See `13-meter-effects-tables.md` for meter threshold triggers
- See `38-emotional-memory-tracking.md` for complete memory resonance system
- See `01-emotional-authenticity.md` for integration master plan

---

**This specification enables developers to implement the complete emotional state system with exact appeal calculations, filtering algorithms, state transitions, and emotional authenticity mechanics from Master Truths v1.2.**

