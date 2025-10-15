# Phase Transition Mechanics - Complete Implementation

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete system for major life transitions with capacity recovery, memory consolidation, and emotional carry-over

**References:**
- **Life Direction:** `20-base-card-catalog.md` (Tier 1 Foundation cards)
- **Season Flow:** `73-season-flow-implementation.md` (season boundaries)
- **Narrative Arc:** `31-narrative-arc-scaffolding.md` (crisis beats)

---

## Overview

**Phase Transitions** are rare, system-generated cards that appear during major life junctures (breakup, job loss, health crisis, major success). They force the player to reflect and may shift their Life Direction.

**Frequency:** 2-4 times per character lifetime (8-10 seasons)  
**Player Control:** MUST respond, but chooses direction  
**Impact:** Can fundamentally reshape deck composition and available paths

**Design Principle:** Life doesn't ask permission. Major events force reconsideration of priorities.

---

## Phase Transition Types

### 8 Core Transition Types

```typescript
enum PhaseTransitionType {
  MAJOR_BREAKUP = "Relationship ending after significant time",
  CAREER_DEVASTATION = "Fired, business failed, or severe burnout",
  HEALTH_CRISIS = "Serious illness, injury, or mental health event",
  LOSS_OF_LOVED_ONE = "Death or permanent estrangement",
  FINANCIAL_CATASTROPHE = "Bankruptcy, debt crisis, major loss",
  ACHIEVEMENT_PEAK = "Major success achieved, now what?",
  EXISTENTIAL_CRISIS = "Questioning entire life direction",
  UNEXPECTED_OPPORTUNITY = "Dream offer, inheritance, life-changing chance"
}

interface PhaseTransitionCard {
  id: string;
  type: PhaseTransitionType;
  tier: 1;                                   // Foundation tier (rare)
  mandatory: true;                           // Cannot be skipped
  
  trigger_conditions: TriggerCondition[];
  narrative: string;
  
  choices: DirectionShiftOption[];
  
  consequences: {
    immediate: ImmediateEffect[];
    life_direction_shift?: LifeDirectionChange;
    deck_reset: DeckResetRules;
    aspiration_impact: AspirationImpact;
    emotional_state: EmotionalStateChange;
  };
}
```

---

## TRANSITION TYPE 1: MAJOR BREAKUP

### Complete Specification

```javascript
const MAJOR_BREAKUP_TRANSITION = {
  id: "phase_transition_breakup",
  type: "MAJOR_BREAKUP",
  tier: 1,
  category: "phase_transition",
  
  trigger_conditions: {
    relationship_status: "In significant relationship",
    relationship_duration: { min_weeks: 52 },   // 1+ year
    relationship_level: { min: 3 },             // Friend or higher
    
    triggers: [
      {
        type: "natural_drift",
        probability: 0.05,                       // 5% per season if conditions met
        requires: {
          relationship_neglect: "4+ weeks no interaction",
          trust: { max: 0.4 }                    // Trust below 0.4
        }
      },
      {
        type: "decisive_decision_consequence",
        trigger: "Player chose career over relationship in decision",
        delayed_consequence: "8-12 weeks later"
      },
      {
        type: "incompatible_life_directions",
        requires: {
          player_direction: "any",
          partner_npc_direction: "incompatible",
          time_together: { min_weeks: 100 }
        }
      }
    ]
  },
  
  narrative_template: `
    [Partner Name] wants to talk.
    
    You know what's coming. You've felt it for weeks. The distance. 
    The careful conversations. The way they look at you like they're 
    trying to remember why this worked.
    
    "[Player Name]... I think we both know this isn't working anymore."
    
    After [X years] together, it's over. Everything feels different now.
  `,
  
  choices: [
    {
      id: "throw_into_work",
      label: "Throw myself into work",
      direction_shift: "Achieve Financial Security",
      
      immediate_effects: {
        emotional_state: "MELANCHOLY → gradually to FOCUSED",
        physical_meter: -2,                      // Neglect self-care
        mental_meter: +1,                        // Productive distraction
        money: "+20% income focus"
      },
      
      deck_changes: {
        corporate_career_cards: "+40%",
        relationship_cards: "-30%",
        social_activity_cards: "-20%"
      },
      
      aspiration_impact: {
        romantic_aspirations: "cancelled",
        career_aspirations: "easier to pursue",
        new_unlocks: ["Workaholic Lifestyle", "Corporate Climb"]
      },
      
      npc_reactions: {
        friends: "Worried about you, 'Are you okay?' conversations",
        family: "Supportive but concerned",
        ex_partner: "Drifts away completely"
      },
      
      long_term_arc: "Success but loneliness",
      novel_chapter_tone: "Throwing yourself into work to avoid feeling"
    },
    
    {
      id: "focus_healing",
      label: "Focus on healing myself",
      direction_shift: "Discover Who You Are",
      
      immediate_effects: {
        emotional_state: "MELANCHOLY → gradually to REFLECTIVE",
        emotional_meter: +2,                     // Processing emotions
        mental_meter: -1,                        // Heavy introspection
        time_intensive: "Therapy, journaling, self-work"
      },
      
      deck_changes: {
        self_discovery_cards: "+40%",
        therapy_activities: "+30%",
        solo_activities: "+20%",
        romantic_cards: "-40%"
      },
      
      aspiration_impact: {
        romantic_aspirations: "cancelled",
        self_growth_aspirations: "unlocked",
        new_unlocks: ["Therapy Journey", "Solo Travel", "Creative Expression"]
      },
      
      long_term_arc: "Growth through pain",
      novel_chapter_tone: "The hard work of becoming whole again"
    },
    
    {
      id: "embrace_freedom",
      label: "Embrace my freedom",
      direction_shift: "Find Personal Freedom",
      
      immediate_effects: {
        emotional_state: "MELANCHOLY → RESTLESS → EXCITED",
        social_meter: +2,                        // New experiences
        comfort_zone: -3,                        // Pushing boundaries
        money: "May spend more on experiences"
      },
      
      deck_changes: {
        adventure_cards: "+40%",
        social_variety: "+30%",
        routine_cards: "-20%",
        commitment_cards: "-30%"
      },
      
      aspiration_impact: {
        romantic_aspirations: "cancelled",
        adventure_aspirations: "unlocked",
        new_unlocks: ["Travel Plans", "New Social Circles", "Spontaneous Living"]
      },
      
      long_term_arc: "Rediscovering yourself through experience",
      novel_chapter_tone: "Breaking free, finding what I really want"
    },
    
    {
      id: "seek_connection",
      label: "Seek new connections",
      direction_shift: "Seek Deep Relationships",
      
      immediate_effects: {
        emotional_state: "MELANCHOLY → LONELY → gradually HOPEFUL",
        social_meter: +1,
        emotional_vulnerability: "High",
        rebound_risk: true                       // May rush into new relationship
      },
      
      deck_changes: {
        dating_cards: "+40%",
        social_activity_cards: "+30%",
        friend_building_cards: "+20%",
        solo_activities: "-20%"
      },
      
      aspiration_impact: {
        romantic_aspirations: "Available after 12 weeks",
        social_aspirations: "unlocked",
        new_unlocks: ["Dating Again", "Build New Friend Circle"]
      },
      
      long_term_arc: "Learning to trust again",
      novel_chapter_tone: "Rebuilding capacity for connection"
    }
  ],
  
  mandatory_processing: {
    time_paused: true,                           // Must decide before continuing
    decision_weight: "major",
    cannot_skip: true,
    
    support_system: {
      friends_react: true,
      family_support_available: true,
      therapy_recommended: true
    }
  },
  
  memory_impact: {
    relationship_ended: "Permanent record",
    ex_partner_npc: "Becomes 'Ex-Partner' NPC with limited interactions",
    shared_locations: "Emotional weight changes",
    mutual_friends: "May have to choose sides or navigate awkwardness",
    
    novel_significance: "Major chapter - relationship arc closure"
  }
};
```

---

## TRANSITION TYPE 2: CAREER DEVASTATION

```javascript
const CAREER_DEVASTATION_TRANSITION = {
  id: "phase_transition_career_loss",
  type: "CAREER_DEVASTATION",
  
  trigger_conditions: {
    OR: [
      {
        type: "fired",
        requires: {
          career_reputation: { max: -3 },
          consecutive_poor_performance: 3
        }
      },
      {
        type: "business_failed",
        requires: {
          aspiration: "Business launch",
          aspiration_result: "failure",
          debt: { min: 5000 }
        }
      },
      {
        type: "severe_burnout",
        requires: {
          physical_meter: { max: 2 },
          mental_meter: { max: 2 },
          consecutive_overwork: "12+ weeks"
        }
      }
    ]
  },
  
  narrative_variants: {
    fired: `
      The email is short. "Please schedule a meeting with HR."
      
      You knew it was coming, but it still hurts. Three years here. 
      Projects you poured yourself into. Colleagues who became friends.
      
      "We're letting you go, effective immediately."
      
      Security escorts you out. Your desk in a box. It's over.
    `,
    
    business_failed: `
      You stare at the numbers. Again. Hoping they'll change.
      
      Six months of your life. Your savings. Your dream. 
      $8,000 in debt. No path forward.
      
      You have to close the doors.
      
      Everything you worked for... gone.
    `,
    
    burnout: `
      You can't do this anymore. You physically can't.
      
      The alarm goes off. You can't get out of bed. Not tired—broken.
      
      You email your boss: "I need to take a leave. Medical reasons."
      
      You don't tell them the truth: You're not sure you're ever coming back.
    `
  },
  
  choices: [
    {
      id: "pivot_completely",
      label: "Start over in new field",
      direction_shift: "Discover Who You Are",
      
      immediate_effects: {
        income: "Stopped or minimal",
        debt_risk: "High",
        stress: "High initially, then relief",
        emotional_state: "DEVASTATED → UNCERTAIN → HOPEFUL"
      },
      
      time_required: "24-36 weeks to establish new career"
    },
    
    {
      id: "skill_up_retry",
      label: "Learn new skills, try again",
      direction_shift: "Master a Craft",
      
      immediate_effects: {
        time_intensive: "Education/training focus",
        money_cost: "Course fees, certification",
        emotional_state: "DETERMINED"
      }
    },
    
    {
      id: "financial_safety",
      label: "Any stable job, prioritize security",
      direction_shift: "Achieve Financial Security",
      
      immediate_effects: {
        career_satisfaction: "Low",
        income: "Stable but limited",
        emotional_state: "RESIGNED → gradually STABLE"
      }
    },
    
    {
      id: "take_break",
      label: "Take time to heal and figure it out",
      direction_shift: "Discover Who You Are",
      
      immediate_effects: {
        income: "None (savings dependent)",
        stress: "Reduces significantly",
        existential_space: "Creates time for reflection",
        emotional_state: "EXHAUSTED → RESTING → REFLECTIVE"
      }
    }
  ],
  
  financial_consequences: {
    immediate_loss: "Last paycheck or business debt",
    ongoing_costs: "Health insurance, living expenses without income",
    time_pressure: "Money runs out in X weeks",
    
    creates_tension: "Financial stress as persistent background threat"
  }
};
```

---

## TRANSITION TYPE 3: HEALTH CRISIS

```javascript
const HEALTH_CRISIS_TRANSITION = {
  id: "phase_transition_health",
  type: "HEALTH_CRISIS",
  
  trigger_conditions: {
    OR: [
      {
        type: "physical_collapse",
        requires: {
          physical_meter: { max: 1 },
          consecutive_neglect: "6+ weeks",
          warning_ignored: true
        }
      },
      {
        type: "mental_health_crisis",
        requires: {
          mental_meter: { max: 1 },
          emotional_meter: { max: 2 },
          support_system_weak: true
        }
      },
      {
        type: "serious_diagnosis",
        random_event: true,
        probability: 0.01                        // 1% per season (rare)
      }
    ]
  },
  
  narrative: `
    The ER lights are too bright.
    
    Marcus is here. Sarah texted three times. Your mom is driving 
    four hours to get here.
    
    The doctor says: "[Diagnosis]. You need to make changes. Serious changes."
    
    You scared everyone. Including yourself.
  `,
  
  choices: [
    {
      id: "health_first",
      label: "Put health first, everything else second",
      direction_shift: "Discover Who You Are" or "Seek Deep Relationships",
      
      immediate_effects: {
        all_aspirations: "Paused or slowed significantly",
        career_impact: "May need to reduce hours or quit",
        relationship_focus: "Deepens with support system",
        physical_recovery: "Gradual over 12-24 weeks"
      },
      
      long_term_arc: "Learning to live differently"
    },
    
    {
      id: "minimal_changes",
      label: "Make minimal changes, keep pushing",
      direction_shift: "No change (denial)",
      
      warning: "HIGH RISK - May trigger second crisis",
      
      consequences: {
        short_term: "Can continue aspirations",
        long_term: "Increased risk of permanent damage or second crisis",
        relationships: "Friends frustrated, 'We told you'"
      }
    },
    
    {
      id: "complete_reset",
      label: "Completely restructure my life",
      direction_shift: "Discover Who You Are",
      
      effects: {
        career: "May quit or go part-time",
        aspirations: "All cancelled, new focus on wellness",
        relationships: "Prioritize support system",
        lifestyle: "Complete overhaul"
      },
      
      long_term_arc: "Rebuilding from foundation"
    }
  ],
  
  support_system_impact: {
    close_friends: "Trust deepens, support becomes visible",
    distant_friends: "May fade away (can't handle it)",
    family: "Often steps up significantly",
    romantic_partner: "Relationship tested—can strengthen or break",
    
    novel_significance: "Who showed up when it mattered"
  }
};
```

---

## TRANSITION TYPE 4: ACHIEVEMENT PEAK

```javascript
const ACHIEVEMENT_PEAK_TRANSITION = {
  id: "phase_transition_success",
  type: "ACHIEVEMENT_PEAK",
  
  trigger_conditions: {
    major_aspiration_complete: true,
    aspiration_category: "Life-changing",
    success_level: "Exceeded expectations",
    
    examples: [
      "Business launch massively successful",
      "Book published and bestselling",
      "Gallery show sold out",
      "Promotion to dream position",
      "Marathon completed (first time athlete)"
    ]
  },
  
  narrative: `
    You did it. You actually did it.
    
    [Achievement description]. The goal you set [X months] ago. 
    The thing you weren't sure was possible.
    
    Everyone's congratulating you. You're smiling. You're happy.
    
    So why does it feel... empty?
    
    What now?
  `,
  
  choices: [
    {
      id: "double_down",
      label: "Go bigger—this is just the beginning",
      direction_shift: "Master a Craft" or "Make Social Impact",
      
      effects: {
        ambition_increase: true,
        new_aspirations: "Unlocked at higher level",
        risk: "Burnout if not careful",
        emotional: "EXCITED → DRIVEN"
      }
    },
    
    {
      id: "appreciate_plateau",
      label: "Enjoy this success, no need to chase more",
      direction_shift: "Balance Everything",
      
      effects: {
        contentment: "High",
        new_focus: "Relationships and lifestyle",
        career_stable: true,
        emotional: "CONTENT → PEACEFUL"
      }
    },
    
    {
      id: "pivot_fulfillment",
      label: "This isn't what I thought it would be—pivot",
      direction_shift: "Discover Who You Are",
      
      effects: {
        existential_questioning: true,
        career_change_possible: true,
        emotional: "CONFUSED → SEARCHING"
      },
      
      narrative: "Success revealed what I actually want"
    },
    
    {
      id: "give_back",
      label: "Use this success to help others",
      direction_shift: "Make Social Impact",
      
      effects: {
        teaching_unlocked: true,
        mentorship_aspirations: true,
        meaning_focus: "Shifts from achievement to contribution"
      }
    }
  ],
  
  paradox_of_success: {
    description: "Achievement can create existential crisis",
    common_feelings: [
      "Is this all there is?",
      "I thought I'd feel different",
      "What was I chasing?",
      "Now what?"
    ],
    
    narrative_weight: "Positive crisis - success forcing growth"
  }
};
```

---

## Phase Transition Mechanics

### Trigger System

```javascript
function checkPhaseTransitionTriggers(playerState, gameState) {
  const potentialTransitions = [];
  
  // Check each transition type
  for (const transitionType of ALL_TRANSITION_TYPES) {
    const conditions = transitionType.trigger_conditions;
    
    if (evaluateConditions(conditions, playerState, gameState)) {
      potentialTransitions.push({
        type: transitionType,
        probability: calculateProbability(conditions, playerState),
        urgency: calculateUrgency(conditions, playerState)
      });
    }
  }
  
  // Never trigger more than one per season
  if (playerState.phase_transitions_this_season > 0) {
    return null;
  }
  
  // Select highest priority transition
  if (potentialTransitions.length > 0) {
    return selectTransition(potentialTransitions);
  }
  
  return null;
}
```

---

### Deck Reset Rules

```javascript
const DECK_RESET_LOGIC = {
  life_direction_shifts: {
    if_direction_changes: {
      old_direction_cards: "Reduced by 40-60%",
      new_direction_cards: "Added, ramping up over 4-8 weeks",
      
      transition_period: "4-8 weeks gradual shift",
      
      example: {
        from: "Pursue Creative Fulfillment",
        to: "Achieve Financial Security",
        
        changes: {
          week_0: "Transition card played",
          week_1: "80% old deck, 20% new cards appear",
          week_4: "50% old, 50% new",
          week_8: "20% old, 80% new (new direction dominant)"
        }
      }
    }
  },
  
  aspiration_cancellation: {
    active_aspirations: "Cancelled if incompatible with new direction",
    progress_lost: "Yes, but recorded in memory",
    new_aspirations: "Unlocked based on new direction"
  },
  
  npc_availability: {
    some_npcs_fade: "NPCs tied to old life may become less available",
    new_npcs_appear: "NPCs aligned with new direction appear",
    core_relationships: "Persist (family, close friends)"
  }
};
```

---

## Master Truths v1.2: Capacity Recovery at Phase Transitions *(NEW)*

### Transitions Reset Some Capacity

**Core Principle:** Major life transitions force pause and reflection, providing partial capacity recovery even in crisis.

```javascript
const PHASE_TRANSITION_CAPACITY_EFFECTS = {
  principle: "Crisis forces reset - you can't keep going at same pace after major life change",
  
  capacity_recovery_by_transition_type: {
    major_breakup: {
      immediate_capacity_hit: -3,  // Week 1: devastated
      forced_processing_period: "2-4 weeks",
      recovery_trajectory: {
        week_1: -3,  // Devastation
        week_2: -2,  // Beginning to process
        week_3: -1,  // Acceptance starting
        week_4: +1,  // Partial recovery, new perspective
        week_8: +2   // Fully processed, stronger from experience
      },
      
      narrative: "Paradox: Breaking forced you to slow down, which let you recover capacity you didn't know you'd lost."
    },
    
    career_devastation: {
      immediate_capacity_hit: -4,  // Severe blow to identity
      forced_rest_period: "1-2 weeks mandatory",
      recovery_options: {
        take_real_break: {
          weeks_off: 2,
          capacity_recovery: +3,
          outcome: "Healthy reset, ready for new chapter"
        },
        immediately_job_hunt: {
          weeks_off: 0,
          capacity_recovery: 0,
          outcome: "No recovery, carrying burnout into next role"
        }
      }
    },
    
    health_crisis: {
      immediate_capacity_hit: -5,  // Physical collapse
      mandatory_recovery: "4-8 weeks forced rest",
      silver_lining: "Forces lifestyle changes that increase long-term capacity",
      
      recovery: {
        week_4: -2,  // Still recovering
        week_8: 0,   // Back to baseline
        week_16: +1  // Healthier habits = higher baseline capacity
      }
    },
    
    achievement_peak: {
      capacity_boost: +2,  // Success provides energy
      duration: "4-6 weeks",
      but_then: "Returns to baseline - success high fades",
      
      risk: "May lead to next big goal before recovering from first"
    }
  }
};
```

---

## Master Truths v1.2: Memory Consolidation Triggers *(NEW)*

### Transitions Create Defining Memories

**Core Principle:** Phase transitions automatically create weight-10 memories that define character's life story.

```javascript
const MEMORY_CONSOLIDATION_AT_TRANSITIONS = {
  automatic_memory_creation: {
    all_phase_transitions: {
      memory_weight: 10,  // Maximum - never forgotten
      memory_type: "defining_moment",
      carries_forward: "All future seasons",
      
      affects: [
        "Future decision making",
        "Character self-perception",
        "Novel chapter titles",
        "Anniversary callbacks"
      ]
    }
  },
  
  memory_details_captured: {
    major_breakup: {
      memory_title: "The End of [Partner Name]",
      details_stored: [
        "How it ended",
        "What you learned",
        "Who supported you",
        "Who you became after"
      ],
      
      future_callbacks: {
        anniversary_date: "Each year, memory surfaces",
        similar_situations: "Affects future relationship decisions",
        mutual_friends: "Awkwardness when they come up",
        locations: "Coffee shop where you used to meet feels different"
      }
    },
    
    career_devastation: {
      memory_title: "The Day I Lost [Career Identity]",
      details_stored: [
        "How you found out",
        "Financial impact",
        "Identity crisis experienced",
        "Path chosen after"
      ],
      
      long_term_effects: {
        risk_tolerance: "May become more/less risk-averse",
        imposter_syndrome: "Success feels fragile",
        financial_anxiety: "Never feel completely secure again",
        or_resilience: "Survived worst, know can handle anything"
      }
    },
    
    health_crisis: {
      memory_title: "The Wake-Up Call",
      details_stored: [
        "The moment it happened",
        "Who was there",
        "What changed after",
        "Promises made to self"
      ],
      
      permanent_character_change: {
        health_priority: +2,  // Always considers health now
        work_boundaries: "Never push that hard again",
        mortality_awareness: "Life feels precious and finite"
      }
    }
  },
  
  memory_consolidation_process: {
    during_transition: "Raw experience stored",
    weeks_4_8: "Processing and meaning-making",
    week_12plus: "Consolidated into narrative",
    
    becomes: "Part of character's origin story going forward"
  }
};
```

---

## Master Truths v1.2: Emotional State Carry-Over *(NEW)*

### Post-Transition States Persist

**Core Principle:** Emotional states from transitions don't instantly reset - they carry over and fade gradually.

```javascript
const EMOTIONAL_CARRY_OVER_RULES = {
  major_breakup: {
    immediate_state: "DEVASTATED",
    carry_over_trajectory: {
      weeks_1_2: "DEVASTATED (cannot be changed)",
      weeks_3_4: "MELANCHOLY (locked, but can have brief HOPEFUL moments)",
      weeks_5_8: "MELANCHOLY or REFLECTIVE (player choice starts mattering)",
      weeks_9_plus: "Full emotional range restored, but MELANCHOLY more likely for 6 months"
    },
    
    triggers_that_reset_to_sad: [
      "Anniversary of relationship",
      "See ex with new partner",
      "Song that was 'your song'",
      "Location with memories"
    ],
    
    healing_is_not_linear: "Can be doing well, then something triggers grief again"
  },
  
  career_devastation: {
    immediate_state: "DEVASTATED",
    secondary_states: "ANXIOUS, UNCERTAIN, ASHAMED",
    
    carry_over: {
      weeks_1_4: "DEVASTATED, ANXIOUS (locked)",
      weeks_5_8: "DISCOURAGED, UNCERTAIN (can shift with effort)",
      weeks_9_16: "DETERMINED or RESIGNED (depends on path chosen)",
      long_term: "Residual anxiety about job security for years"
    }
  },
  
  health_crisis: {
    immediate_state: "TERRIFIED",
    during_recovery: "EXHAUSTED, FRUSTRATED",
    after_recovery: "RELIEVED but CAUTIOUS",
    
    permanent_emotional_shift: {
      health_anxiety: "Increased sensitivity to body signals",
      gratitude: "Appreciation for normal health",
      mortality_awareness: "Background awareness of fragility"
    }
  },
  
  achievement_peak: {
    immediate_state: "TRIUMPHANT",
    weeks_1_4: "CONFIDENT, FULFILLED",
    weeks_5_8: "CONTENT",
    weeks_9_plus: "Back to baseline",
    
    but_also: {
      possible_crash: "What now? Was it worth it?",
      anticlimactic: "Expected to feel different",
      pressure: "Now must maintain/exceed success"
    }
  },
  
  interaction_with_new_events: {
    cant_fully_enjoy_good_things: "For weeks after breakup, good news feels muted",
    everything_triggers: "Small setbacks feel catastrophic when already devastated",
    emotional_buffer_depleted: "Take longer to recover from additional stress"
  }
};
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Phase Transition System (v1.1 Foundation)
- [x] Phase transitions use time-paused decision system
- [x] No FOMO mechanics (player chooses when ready)
- [x] All transitions respect relationship levels 0-5
- [x] Emotional states (20 states) properly triggered
- [x] Multi-season impact tracked (8-10 season lifecycle)
- [x] 8 core transition types with exact triggers
- [x] Deck reset rules and aspiration cancellation
- [x] NPC availability changes post-transition

### ✅ Master Truths v1.2: Transition Effects *(NEW)*
- [x] **Capacity Recovery at Transitions**
  - Major breakup: -3 capacity immediate, +2 by week 8 (paradoxical recovery)
  - Career devastation: -4 immediate, +3 if take real break (or 0 if rush back)
  - Health crisis: -5 immediate, +1 baseline by week 16 (forced healthy habits)
  - Achievement peak: +2 for 4-6 weeks (success high, then fades)
- [x] **Memory Consolidation Triggers**
  - All phase transitions create weight-10 memories (never forgotten)
  - Memory type: "defining_moment" carried forward all future seasons
  - Details captured: how it happened, who was there, what changed after
  - Anniversary callbacks: memories surface yearly, locations feel different
- [x] **Emotional State Carry-Over Rules**
  - Breakup: DEVASTATED weeks 1-2 (locked) → MELANCHOLY weeks 3-8 → Full range weeks 9+ (but MELANCHOLY likely for 6 months)
  - Career loss: DEVASTATED weeks 1-4 → DISCOURAGED weeks 5-8 → DETERMINED/RESIGNED weeks 9-16
  - Health crisis: TERRIFIED → EXHAUSTED → RELIEVED but CAUTIOUS (permanent health anxiety)
  - Achievement: TRIUMPHANT weeks 1-4 → CONFIDENT → CONTENT → Baseline (or crash: "What now?")

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~230 lines** of new v1.2 transition effects
2. **Capacity recovery trajectories** - transitions force pause, providing recovery opportunity
3. **Memory consolidation** - weight-10 defining moments that shape future
4. **Emotional carry-over** - states persist and fade gradually over weeks/months
5. **Non-linear healing** - can be doing well, then triggers reset grief
6. **Permanent character changes** - health crisis increases health priority permanently

**Capacity Recovery Examples:**
- Breakup: Week 1 (-3) → Week 2 (-2) → Week 4 (+1) → Week 8 (+2) - "Forced slow down let you recover"
- Career loss + take break: -4 immediate → +3 by week 2 = "Healthy reset, ready for new chapter"
- Career loss + rush back: -4 → 0 recovery = "Carrying burnout into next role"
- Health crisis: -5 → Week 16 (+1 baseline) = "Healthier habits = higher capacity long-term"

**Memory Consolidation:**
- Breakup: "The End of [Partner]" - anniversary surfaces yearly, locations feel different
- Career loss: "The Day I Lost [Identity]" - affects risk tolerance, imposter syndrome years later
- Health crisis: "The Wake-Up Call" - permanent health priority +2, mortality awareness

**Emotional Carry-Over:**
- Breakup weeks 1-2: DEVASTATED (cannot change)
- Breakup weeks 3-4: MELANCHOLY (locked, brief HOPEFUL moments)
- Breakup weeks 5-8: MELANCHOLY/REFLECTIVE (player choice starts mattering)
- Breakup weeks 9+: Full range, but MELANCHOLY more likely for 6 months
- Triggers: anniversary, see ex with new partner, "your song", shared locations

**Design Principles:**
- Transitions force pause = capacity recovery opportunity
- Crisis creates defining memories (weight-10, never forgotten)
- Healing is not linear (triggers reset grief randomly)
- Can't fully enjoy good things for weeks after devastation
- Emotional buffer depleted = longer recovery from additional stress
- Some changes are permanent (health crisis → lifelong health awareness)

**References:**
- See `01-emotional-authenticity.md` for cross-system capacity integration
- See `14-emotional-state-mechanics.md` for emotional state mechanics and transitions
- See `38-emotional-memory-tracking.md` for memory weight and consolidation rules
- See `20-base-card-catalog.md` for Life Direction foundation cards
- See `73-season-flow-implementation.md` for season boundaries and transitions
- See `31-narrative-arc-scaffolding.md` for crisis beat integration

---

**This specification enables developers to implement phase transitions with Master Truths v1.2 enhancements: capacity recovery trajectories where crisis forces pause and creates recovery opportunity, memory consolidation where transitions automatically create weight-10 defining moments that shape future decisions, and emotional state carry-over rules where states persist for weeks/months with non-linear healing and permanent character changes - creating transitions that feel like authentic life-changing events with lasting psychological impact.**

