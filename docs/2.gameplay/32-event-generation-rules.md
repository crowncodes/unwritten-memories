# Event Generation Rules - Implementation Specification

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete event generation system with frequency, mix, timing rules, and emotional capacity awareness

**References:**
- **Design Philosophy:** `1.concept/21-turn-structure.md` (WHY events matter)
- **Narrative Arc:** `31-narrative-arc-scaffolding.md` (arc-driven events)
- **Weekly Cycle:** `72-weekly-cycle-implementation.md` (event placement)
- **Schema Definition:** `7.schema/05-narrative-system.md` (Event interfaces)

---

## Overview

Events are **narrative beats that interrupt routine** to create story, introduce opportunities/challenges, and drive emotional engagement. The system generates events based on narrative arc, emotional state, relationship status, and player choices.

**Core Principle:** Events should feel organic and consequential, not random. Every event should serve narrative or relationship progression.

**Compliance:** master_truths v1.2 specifies events are content-driven, not RNG gacha mechanics, and must respect emotional capacity and circumstance stacking limits.

---

## Event Categories

### 8 Core Event Types

```typescript
enum EventCategory {
  SOCIAL = "social",               // Relationship-driven
  ASPIRATION = "aspiration",       // Goal-related
  CAREER = "career",               // Work/professional
  CRISIS = "crisis",               // Problems requiring response
  OPPORTUNITY = "opportunity",     // Positive openings
  RELATIONSHIP = "relationship",   // NPC-initiated
  MILESTONE = "milestone",         // Achievement moments
  MYSTERY_HOOK = "mystery_hook"    // Tension injection (NEW)
}

interface Event {
  id: string;
  category: EventCategory;
  title: string;
  narrative: string;
  
  // Timing
  trigger_conditions: TriggerCondition[];
  scheduled_week: number | null;
  scheduled_day: string | null;
  scheduled_phase: "morning" | "afternoon" | "evening" | null;
  
  // Requirements
  requires_npcs: NPC[];
  requires_location: Location | null;
  requires_resources: ResourceRequirement[];
  
  // Consequences
  outcomes: EventOutcome[];
  creates_decisions: boolean;
  advances_arc: boolean;
  
  // Meta
  weight: number;                  // Narrative importance 0.0-1.0
  emotional_impact: EmotionalImpact;
  one_time: boolean;
  
  // NEW: Tension Systems
  is_mystery_hook?: boolean;       // Creates curiosity/tension
  mystery_thread_id?: string;      // Links to mystery system
  ticking_clock?: TickingClock;    // Time pressure mechanic
  is_cliffhanger?: boolean;        // End-of-period hook
}
```

---

## Event Frequency by Season Length

### Baseline Frequency Targets

```javascript
const EVENT_FREQUENCY_BY_SEASON = {
  standard_12_week: {
    total_events: "8-12",
    events_per_week: 0.83,         // ~5 events per 6 weeks
    
    breakdown: {
      social: 4,                   // 33%
      aspiration: 3,               // 25%
      career: 2,                   // 17%
      crisis: 1,                   // 8%
      opportunity: 2,              // 17%
      relationship: 2,             // (overlap with social)
      milestone: 1                 // (arc milestones)
    },
    
    pacing: {
      weeks_1_3: 2,                // Act I: Setup events
      weeks_4_9: 6,                // Act II: Peak activity
      weeks_10_12: 2               // Act III: Resolution
    }
  },
  
  extended_24_week: {
    total_events: "18-24",
    events_per_week: 0.88,
    
    breakdown: {
      social: 8,
      aspiration: 6,
      career: 4,
      crisis: 3,
      opportunity: 4,
      relationship: 5,
      milestone: 2
    },
    
    pacing: {
      weeks_1_6: 4,
      weeks_7_18: 14,
      weeks_19_24: 4
    }
  },
  
  epic_36_week: {
    total_events: "30-40",
    events_per_week: 1.0,
    
    breakdown: {
      social: 12,
      aspiration: 10,
      career: 6,
      crisis: 5,
      opportunity: 7,
      relationship: 8,
      milestone: 3
    },
    
    pacing: {
      weeks_1_9: 6,
      weeks_10_27: 24,
      weeks_28_36: 8
    }
  }
};
```

---

## NEW: Tension Maintenance Systems

### Hook Points System (Every 2-3 Weeks)

**Purpose:** Inject tension and curiosity between major narrative beats to prevent "pleasant but boring" periods.

```javascript
const MYSTERY_HOOK_SYSTEM = {
  frequency: {
    min_weeks_between: 2,
    max_weeks_between: 3,
    total_per_season: {
      standard_12w: "4-5 hooks",
      extended_24w: "8-10 hooks",
      epic_36w: "12-15 hooks"
    }
  },
  
  hook_types: {
    mystery_planted: {
      description: "Plant intriguing question without answer",
      examples: [
        "Sarah mentions someone named 'David' but changes subject quickly",
        "You notice Marcus has been taking mysterious phone calls",
        "Your boss keeps having closed-door meetings about 'the project'"
      ],
      narrative_purpose: "Create curiosity about what's happening"
    },
    
    revelation_partial: {
      description: "Reveal half of a secret or mystery",
      examples: [
        "Find old letters in Sarah's handwriting, but to someone else",
        "Overhear part of conversation: '...can't tell them yet...'",
        "Discover Marcus knows more about your situation than he's saying"
      ],
      narrative_purpose: "Deepen existing mystery, raise stakes"
    },
    
    opportunity_threatened: {
      description: "Something you want might disappear",
      examples: [
        "Dream apartment gets another offer - 48 hours to decide",
        "Gallery slot available but only if you commit by Friday",
        "Sarah mentions she might be moving out of state"
      ],
      narrative_purpose: "Create urgency without forced pressure"
    },
    
    relationship_shift: {
      description: "Sudden unexplained change in NPC behavior",
      examples: [
        "Sarah suddenly distant after weeks of closeness",
        "Marcus uncharacteristically cold this morning",
        "Your mentor cancels meeting without explanation"
      ],
      narrative_purpose: "Create tension in relationships, foreshadow conflict"
    },
    
    external_pressure: {
      description: "Outside force creates new tension",
      examples: [
        "Deadline approaches: wedding season ends in 6 weeks",
        "Competitor emerges in your space",
        "Rent increase notice - need more income"
      ],
      narrative_purpose: "Add time pressure and stakes"
    }
  },
  
  placement_rules: {
    between_major_beats: true,
    avoid_during_decisive_decisions: true,
    max_active_hooks: 3,
    all_must_connect_to: ["main_aspiration", "major_relationships", "season_arc"],
    never_random: "Every hook serves the larger narrative"
  },
  
  resolution_timing: {
    plant_to_reveal: "3-8 weeks typical",
    some_never_resolve: "Mystery can carry to next season",
    escalation: "Each hook should raise questions or stakes"
  }
};
```

---

### Ticking Clock Mechanics

**Purpose:** Create in-world urgency that makes consequences feel real and choices weighted.

```javascript
const TICKING_CLOCK_SYSTEM = {
  types: {
    aspiration_deadline: {
      description: "Goal has natural time window",
      examples: [
        {
          aspiration: "Become Wedding Photographer",
          clock: "Wedding season (May-October)",
          urgency: "Miss it and wait a full year",
          escalation: "Fewer weekends available as season progresses"
        },
        {
          aspiration: "Launch Business",
          clock: "Savings running out",
          urgency: "6 months runway, then need income",
          escalation: "Savings decrease weekly, anxiety increases"
        }
      ],
      implementation: "Display countdown, escalating pressure events"
    },
    
    relationship_clock: {
      description: "NPC life changes create windows",
      examples: [
        {
          npc: "Sarah",
          clock: "Lease expires in 8 weeks",
          urgency: "She might move away if you don't deepen bond",
          escalation: "Moving talk increases, apartment hunting begins"
        },
        {
          npc: "Mentor",
          clock: "Retiring in 12 weeks",
          urgency: "Learn from them while you can",
          escalation: "Availability decreases as retirement approaches"
        }
      ],
      implementation: "NPC mentions time pressure, makes life decisions"
    },
    
    health_crisis_clock: {
      description: "Symptoms worsen without treatment",
      examples: [
        {
          crisis: "Exhaustion → Burnout",
          progression: [
            "Week 1: Tired often",
            "Week 2: Coffee not helping",
            "Week 3: Hands shake, focus difficult",
            "Week 4: Collapse during important moment"
          ],
          urgency: "Address it or suffer major consequence",
          intervention: "Rest/therapy can reset clock"
        }
      ],
      implementation: "Foreshadowing cards, escalating symptoms, crisis event"
    },
    
    opportunity_window: {
      description: "Chance available for limited time",
      examples: [
        "Gallery showing - submit by end of month",
        "Job opening - applications close Friday",
        "Partnership offer - need answer in 2 weeks"
      ],
      implementation: "Clear deadline display, opportunity closes if missed"
    }
  },
  
  display_rules: {
    show_countdown: "In-world time only (never real-time)",
    urgency_copy: "Focus on stakes, not anxiety",
    good_example: "'Wedding season ends in 6 weeks - this is your chance'",
    bad_example: "'⏰ 6 WEEKS LEFT! DON'T MISS OUT!' (too FOMO-y)",
    player_agency: "Can choose to let clock expire (consequence but not punishment)"
  },
  
  compliance: {
    no_real_time_pressure: true,
    no_fomo_mechanics: true,
    always_in_world_logic: true,
    master_truths_v1_1: "Clocks create stakes, not anxiety"
  }
};
```

---

### Mystery Thread Tracking System

**Purpose:** Create "information debt" that makes players curious about what happens next.

```javascript
const MYSTERY_THREAD_SYSTEM = {
  max_active_per_season: 3,       // Prevents scattered/unfocused feeling
  
  thread_lifecycle: {
    plant: {
      when: "Weeks 2-8 (early season)",
      how: "Intriguing mention, unexplained behavior, partial information",
      examples: [
        "Sarah mentions 'David' but won't explain who he is",
        "Marcus warns you about something but won't say what",
        "Your boss hints at 'changes coming'"
      ]
    },
    
    develop: {
      when: "Every 3-5 weeks after plant",
      how: "Additional clues, deepening mystery, raising stakes",
      clue_schedule: [
        "Week 2: Plant initial mystery",
        "Week 5: First clue (partial reveal)",
        "Week 8: Second clue (stakes raised)",
        "Week 11: Third clue (tension peak)",
        "Week 15: Partial revelation",
        "Week 22: Full revelation"
      ],
      examples: [
        "Week 2: Sarah mentions David",
        "Week 5: See photo of Sarah with unknown man",
        "Week 8: Friend mentions Sarah was engaged once",
        "Week 11: Sarah cries when wedding topic comes up",
        "Week 15: Learn David died in accident",
        "Week 22: Sarah tells full story, explains fear of commitment"
      ]
    },
    
    reveal: {
      when: "Aligned with narrative arc (usually Act II climax or Act III)",
      how: "Major conversation, decisive decision, dramatic moment",
      emotional_payoff: "Mystery should illuminate character or advance arc",
      impact: "Revelation changes player understanding or creates new choices"
    }
  },
  
  mystery_types: {
    character_secret: {
      description: "NPC hiding something about their past/present",
      examples: [
        "Sarah's past with David (dead fiancé)",
        "Marcus's financial troubles he's hiding",
        "Your boss's real reason for hiring you"
      ],
      payoff: "Deepens relationship, creates empathy or conflict"
    },
    
    hidden_motivation: {
      description: "Why NPC acts certain way",
      examples: [
        "Why Sarah is emotionally distant despite liking you",
        "Why Marcus keeps trying to set you up with people",
        "Why your mentor is pushing you so hard"
      ],
      payoff: "Recontextualizes past interactions, adds depth"
    },
    
    upcoming_reveal: {
      description: "Something will happen, player doesn't know what",
      examples: [
        "Sarah has been planning something big",
        "Your company is being sold (you don't know yet)",
        "Marcus is moving away (hasn't told you)"
      ],
      payoff: "Creates anticipation, makes reveal more impactful"
    }
  },
  
  connection_rule: {
    all_mysteries_must: "Connect to main aspiration OR major relationship",
    never: "Random mystery unrelated to player's story",
    focus: "2-3 mysteries maximum keeps narrative focused",
    example_good: "Sarah's fear of commitment mystery connects to romance aspiration",
    example_bad: "Random stranger's mystery unconnected to any arc"
  },
  
  tracking_data: {
    mystery_id: "unique_identifier",
    planted_week: number,
    clues_revealed: Clue[],
    next_clue_week: number,
    reveal_week: number,
    connected_to: "aspiration_id OR npc_id",
    emotional_weight: 0.0-1.0,
    player_aware: boolean
  }
};
```

---

### Micro-Cliffhanger System

**Purpose:** Create small hooks at natural stopping points to maintain engagement.

```javascript
const MICRO_CLIFFHANGER_SYSTEM = {
  placement: {
    day_end: {
      frequency: "20% of days",
      timing: "After evening phase, before sleep",
      examples: [
        "Your phone buzzes with Sarah's name as you're falling asleep",
        "Email notification: 'We need to talk' from your boss",
        "Text from unknown number: 'I saw what you did'",
        "Notification: Someone commented on your portfolio"
      ],
      purpose: "Small curiosity hook, answered next morning"
    },
    
    week_end: {
      frequency: "40% of weeks",
      timing: "After week recap, before next week",
      examples: [
        "Monday morning, your boss wants to see you first thing",
        "Sarah mentioned she has 'something important' to discuss next week",
        "You notice your bank account is lower than expected",
        "Message waiting: 'Call me when you get this'"
      ],
      purpose: "Medium curiosity hook, answered early next week"
    },
    
    turn_end: {
      frequency: "10% of turns (selective use)",
      timing: "After action resolution",
      examples: [
        "The email you've been dreading finally arrives",
        "As you leave, you hear your name mentioned",
        "Sarah's expression changes - something just occurred to her",
        "Your phone rings. It's the gallery owner."
      ],
      purpose: "Immediate curiosity, answered next turn or phase"
    }
  },
  
  design_principles: {
    small_hooks: "Not major cliffhangers, just curiosity nudges",
    quick_resolution: "Answered soon (hours to days in-game)",
    no_anxiety: "Intrigue, not stress",
    optional: "Selective use, not every stopping point",
    narrative_relevant: "Always connected to active storylines"
  },
  
  examples_by_type: {
    relationship: [
      "Sarah seems upset. She's typing... then stops. Then types again.",
      "Marcus: 'Hey, can we talk tomorrow? It's important.'",
      "Three missed calls from [NPC]. No voicemail."
    ],
    
    aspiration: [
      "Email subject: 'Your Portfolio Submission'",
      "The client you've been waiting for just walked into the coffee shop",
      "Notification: Someone bid higher on your dream location"
    ],
    
    mystery: [
      "You find a note in your jacket: 'Ask Sarah about David'",
      "Marcus quickly closes his laptop when you approach",
      "Voicemail from unknown number, mostly static, one word clear: your name"
    ],
    
    crisis: [
      "Your card is declined. That's... never happened before.",
      "Your body feels off. Really off. This isn't just tiredness.",
      "Email from HR: 'Meeting scheduled - 9am Monday'"
    ]
  },
  
  implementation: {
    show_as: "Final card of the session OR post-phase notification",
    visual_style: "Distinct 'cliffhanger' card style",
    no_player_action: "Just information, no choice yet",
    resolution: "Becomes event/card in next session",
    skippable: "Not mandatory tension - player can ignore if desired"
  }
};
```

---

## Event Generation Algorithm

### Dynamic Event Selection

```javascript
function generateEventForWeek(gameState, week_number) {
  const { player, season, narrative_arc } = gameState;
  
  // 1. CHECK FOR MANDATORY NARRATIVE EVENTS
  const narrative_event = checkNarrativeBeat(narrative_arc, week_number);
  if (narrative_event) {
    return [narrative_event]; // Decisive decisions or major beats
  }
  
  // 2. NEW: CHECK FOR HOOK POINT (every 2-3 weeks)
  const weeks_since_last_hook = week_number - player.last_hook_week;
  if (weeks_since_last_hook >= 2 && shouldInjectHook(narrative_arc, player)) {
    const hook_event = generateMysteryHook(player, week_number);
    if (hook_event) {
      player.last_hook_week = week_number;
      return [hook_event];
    }
  }
  
  // 3. NEW: CHECK FOR MYSTERY THREAD CLUE
  const mystery_clue = checkMysteryThreadSchedule(player, week_number);
  if (mystery_clue) {
    return [mystery_clue];
  }
  
  // 4. CALCULATE EVENT POOL
  const available_events = getAvailableEvents(player, week_number);
  
  // 5. WEIGHT EVENTS BY CONTEXT
  const weighted_events = available_events.map(event => {
    let weight = event.base_weight;
    
    // Narrative arc modifiers
    if (narrative_arc.current_act === 2) {
      if (event.category === "crisis") weight *= 1.5;
      if (event.category === "opportunity") weight *= 0.8;
    }
    
    // Emotional state modifiers
    if (player.emotional_state.primary === "DISCOURAGED") {
      if (event.category === "opportunity") weight *= 1.5; // Offer hope
      if (event.category === "crisis") weight *= 0.5;     // Ease up
    }
    
    // Relationship modifiers
    player.relationships.forEach(rel => {
      if (rel.weeks_since_interaction > 2) {
        if (event.involves_npc === rel.npc_id) {
          weight *= 2.0; // Prioritize neglected relationships
        }
      }
    });
    
    // Aspiration progress modifiers
    if (player.aspiration.progress < 30 && week_number > season.weeks * 0.5) {
      if (event.category === "aspiration") weight *= 2.0; // Help catch up
    }
    
    // Meter state modifiers
    if (player.meters.social < 4) {
      if (event.category === "social") weight *= 1.8; // Encourage connection
    }
    
    return { ...event, weighted_score: weight };
  });
  
  // 4. SELECT EVENTS (1-2 per week typically)
  const selected_events = selectTopEvents(weighted_events, 1, 2);
  
  // 5. SCHEDULE EVENT TIMING
  selected_events.forEach(event => {
    event.day = selectDayForEvent(event, week_number);
    event.phase = selectPhaseForEvent(event);
  });
  
  return selected_events;
}
```

---

## Event Types - Detailed Breakdown

### 1. Social Events

**Purpose:** Build relationships, create memorable moments, test social meters

```javascript
const SOCIAL_EVENT_TEMPLATES = {
  party: {
    title: "Party Invitation",
    trigger: "relationship_level >= 2 AND social_meter >= 5",
    narrative: "{NPC} invites you to {event_type} this {day_of_week}.",
    
    options: [
      {
        id: "attend",
        label: "Attend the party",
        costs: { energy: 2, time: 4, money: 20 },
        outcomes: {
          social_meter: +2,
          relationships: { [npc]: { trust: +0.04, social_capital: +2 } },
          emotional: +1
        }
      },
      {
        id: "decline",
        label: "Politely decline",
        costs: { social_capital: -1 },
        outcomes: {
          relationships: { [npc]: { trust: -0.02 } },
          emotional: -0.5
        }
      }
    ],
    
    variations: ["birthday_party", "house_warming", "game_night", "dinner_party"],
    frequency: 0.4                   // 40% chance per week
  },
  
  spontaneous_hangout: {
    title: "Spontaneous Invitation",
    trigger: "relationship_level >= 2",
    narrative: "{NPC} texts: 'Hey, want to grab {activity} in an hour?'",
    
    options: [
      {
        id: "accept",
        label: "\"Yes! See you soon\"",
        costs: { energy: 1, time: 2, money: 15 },
        outcomes: {
          relationships: { [npc]: { trust: +0.03, social_capital: +1 } },
          emotional: +1,
          creates_memory: true
        }
      },
      {
        id: "decline_friendly",
        label: "\"Can't today, rain check?\"",
        costs: {},
        outcomes: {
          relationships: { [npc]: { trust: 0 } }
        }
      },
      {
        id: "decline_harsh",
        label: "Leave on read / ignore",
        costs: {},
        outcomes: {
          relationships: { [npc]: { trust: -0.05, social_capital: -2 } }
        }
      }
    ],
    
    variations: ["coffee", "drinks", "lunch", "walk", "movie"],
    frequency: 0.6
  },
  
  group_event: {
    title: "Group Activity",
    trigger: "multiple_relationships >= 2 AND social_meter >= 6",
    narrative: "Several friends are planning {activity}. Want to join?",
    
    options: [
      {
        id: "organize",
        label: "Take the lead organizing",
        costs: { energy: 3, time: 6, money: 40, comfort_zone: 1.0 },
        outcomes: {
          social_meter: +3,
          relationships: { multiple: { trust: +0.05, social_capital: +3 } },
          emotional: +2,
          unlocks: ["leadership_activities"]
        }
      },
      {
        id: "attend",
        label: "Just attend",
        costs: { energy: 2, time: 4, money: 25 },
        outcomes: {
          social_meter: +2,
          relationships: { multiple: { trust: +0.03, social_capital: +1 } }
        }
      },
      {
        id: "decline",
        label: "Skip it",
        costs: {},
        outcomes: {
          relationships: { multiple: { trust: -0.01 } }
        }
      }
    ],
    
    frequency: 0.3
  }
};
```

---

### 2. Aspiration Events

**Purpose:** Drive goal progress, introduce challenges, create momentum

```javascript
const ASPIRATION_EVENT_TEMPLATES = {
  breakthrough_opportunity: {
    title: "Breakthrough Opportunity",
    trigger: "aspiration_progress >= 40 AND aspiration_progress < 70",
    narrative: "An opportunity appears that could significantly advance your {aspiration_name}.",
    
    options: [
      {
        id: "seize",
        label: "Seize the opportunity",
        costs: { energy: 4, time: 8, money: variable },
        success_chance: 0.65,
        outcomes: {
          success: { aspiration_progress: +15, emotional: +3 },
          failure: { aspiration_progress: +5, emotional: -1 }
        }
      },
      {
        id: "prepare_first",
        label: "Prepare before committing",
        costs: { energy: 2, time: 4 },
        outcomes: {
          unlocks: ["better_opportunity_next_week"]
        }
      },
      {
        id: "decline",
        label: "Not ready yet",
        costs: {},
        outcomes: {
          aspiration_progress: 0,
          emotional: -0.5,
          missed_opportunity: true
        }
      }
    ],
    
    frequency: 0.3,
    weight: 0.8
  },
  
  skill_challenge: {
    title: "Skill Test",
    trigger: "aspiration_requires_skill AND skill_level < 5",
    narrative: "You realize your {skill_name} skills aren't quite where they need to be for {aspiration_name}.",
    
    options: [
      {
        id: "intensive_practice",
        label: "Dedicate the week to practice",
        costs: { energy: 8, time: 15, money: 50 },
        outcomes: {
          skill_gain: 1.5,
          aspiration_progress: +5,
          mental_meter: -1
        }
      },
      {
        id: "find_mentor",
        label: "Seek mentorship",
        costs: { energy: 2, time: 4, social_capital: 2 },
        outcomes: {
          unlocks: ["mentor_relationship"],
          skill_gain: 0.5,
          relationship_new: true
        }
      },
      {
        id: "workaround",
        label: "Find a workaround",
        costs: { energy: 3, time: 6 },
        success_chance: 0.50,
        outcomes: {
          success: { aspiration_progress: +8, creative_bonus: true },
          failure: { aspiration_progress: 0, emotional: -2 }
        }
      }
    ],
    
    frequency: 0.4
  },
  
  setback: {
    title: "Aspiration Setback",
    trigger: "aspiration_progress >= 30 AND week_in_act_2",
    narrative: "A setback threatens your progress on {aspiration_name}.",
    
    event_type: "complication",
    
    options: [
      {
        id: "push_through",
        label: "Work twice as hard",
        costs: { energy: 6, time: 12 },
        outcomes: {
          aspiration_progress: +5,         // Recover some progress
          mental_meter: -2,               // But at cost
          emotional_meter: -1
        }
      },
      {
        id: "adapt",
        label: "Adapt your approach",
        costs: { energy: 4, time: 8 },
        outcomes: {
          aspiration_progress: +3,
          unlocks: ["alternative_path"],
          creative_growth: true
        }
      },
      {
        id: "take_break",
        label: "Take a step back and reassess",
        costs: { energy: 0, time: 0 },
        outcomes: {
          aspiration_progress: 0,
          emotional_meter: +1,            // Reduce pressure
          next_week_bonus: +10            // Better positioned next week
        }
      }
    ],
    
    frequency: 0.3,
    weight: 0.7
  }
};
```

---

### 3. Career Events

**Purpose:** Create work-life balance tension, career progression, income changes

```javascript
const CAREER_EVENT_TEMPLATES = {
  overtime_request: {
    title: "Overtime Request",
    trigger: "has_career AND week_in_season",
    narrative: "Your boss asks you to work overtime this week. Big project deadline.",
    
    options: [
      {
        id: "accept",
        label: "Work the extra hours",
        costs: { energy: 6, time: 15 },
        outcomes: {
          money: +200,
          career_reputation: +1,
          mental_meter: -1,
          aspiration_progress: -5,      // Less time for personal goals
          relationship_neglect: true
        }
      },
      {
        id: "decline",
        label: "Prioritize personal time",
        costs: {},
        outcomes: {
          career_reputation: -1,
          emotional_meter: +1,
          aspiration_progress: +5,       // More time for goals
          boss_relationship: { trust: -0.03 }
        }
      },
      {
        id: "negotiate",
        label: "Offer a compromise",
        costs: { comfort_zone: 1.5 },    // Assertiveness required
        success_chance: 0.60,
        outcomes: {
          success: {
            money: +100,
            career_reputation: +2,       // Impressed by negotiation
            energy: -3,
            time: -8                     // Moderate overtime
          },
          failure: {
            career_reputation: -1,
            emotional: -1
          }
        }
      }
    ],
    
    frequency: 0.3
  },
  
  promotion_opportunity: {
    title: "Promotion Opportunity",
    trigger: "career_tenure >= 12_weeks AND career_reputation >= 3",
    narrative: "Your manager mentions a promotion opportunity. Interested?",
    
    options: [
      {
        id: "pursue",
        label: "Pursue the promotion",
        costs: { energy: 8, time: 20, comfort_zone: 2.0 },
        success_chance: function(player) {
          return 0.50 + (player.career.reputation * 0.05) + (player.skills.leadership * 0.05);
        },
        outcomes: {
          success: {
            career_level: +1,
            money_weekly: +300,
            emotional: +3,
            unlocks: ["senior_role_activities"]
          },
          failure: {
            emotional: -2,
            career_reputation: -0.5,
            next_opportunity_delayed: 12  // 12 weeks
          }
        }
      },
      {
        id: "decline",
        label: "Not ready for more responsibility",
        costs: {},
        outcomes: {
          emotional: 0,
          career_reputation: 0,
          opportunity_lost: true
        }
      }
    ],
    
    frequency: 0.1,                      // Rare
    weight: 0.9                          // But important
  }
};
```

---

### 4. Crisis Events

**Purpose:** Create pressure, force difficult decisions, test relationships

```javascript
const CRISIS_EVENT_TEMPLATES = {
  financial_emergency: {
    title: "Unexpected Expense",
    trigger: "money < 1000 OR random_chance",
    narrative: "{crisis_type} requires immediate payment.",
    
    crisis_types: [
      "Car repair ($800)",
      "Medical bill ($600)",
      "Laptop broken ($1200)",
      "Pet emergency ($500)"
    ],
    
    options: [
      {
        id: "pay_immediately",
        label: "Pay from savings",
        costs: { money: variable },
        available_if: "money >= crisis_cost",
        outcomes: {
          crisis_resolved: true,
          emotional: -1,
          financial_stress: true
        }
      },
      {
        id: "borrow_from_friend",
        label: "Borrow from {NPC}",
        costs: { social_capital: 5, comfort_zone: 2.0 },
        available_if: "has_close_friend",
        outcomes: {
          money: +variable,
          relationships: { [npc]: { trust: +0.05, debt: variable } },
          emotional: -0.5
        }
      },
      {
        id: "work_extra",
        label: "Pick up extra shifts",
        costs: { energy: 8, time: 20 },
        outcomes: {
          money: +variable,
          mental_meter: -2,
          aspiration_progress: -8,
          crisis_resolved: true
        }
      },
      {
        id: "delay_payment",
        label: "Try to delay payment",
        costs: {},
        success_chance: 0.30,
        outcomes: {
          success: { crisis_delayed: 2_weeks },
          failure: { crisis_worsens: true, cost_increases: 1.3 }
        }
      }
    ],
    
    frequency: 0.15,
    weight: 0.8
  },
  
  relationship_crisis: {
    title: "Relationship in Trouble",
    trigger: "relationship_level >= 3 AND weeks_neglected >= 3",
    narrative: "{NPC} is hurt and distant. You've been neglecting the friendship.",
    
    options: [
      {
        id: "prioritize_repair",
        label: "Drop everything to repair this",
        costs: { energy: 4, time: 8, aspiration_progress: -5 },
        outcomes: {
          relationships: { [npc]: { trust: +0.10, social_capital: +5 } },
          emotional: +2,
          relationship_saved: true
        }
      },
      {
        id: "sincere_apology",
        label: "Have an honest conversation",
        costs: { energy: 2, time: 3, comfort_zone: 1.5 },
        success_chance: 0.70,
        outcomes: {
          success: {
            relationships: { [npc]: { trust: +0.08, social_capital: +3 } },
            emotional: +1
          },
          failure: {
            relationships: { [npc]: { trust: -0.05, level: -1 } },
            emotional: -2
          }
        }
      },
      {
        id: "let_it_fade",
        label: "Let the friendship fade",
        costs: {},
        outcomes: {
          relationships: { [npc]: { level: -1, status: "drifted_apart" } },
          emotional: -1,
          social_meter: -2
        }
      }
    ],
    
    frequency: 0.2,
    weight: 0.9
  }
};
```

---

## Event Weighting System

### Dynamic Weight Calculation

```javascript
function calculateEventWeight(event, player, gameState) {
  let weight = event.base_weight;
  
  // 1. NARRATIVE ARC MODIFIERS
  const act = gameState.narrative_arc.current_act;
  if (act === 1 && event.introduces_new_elements) weight *= 1.5;
  if (act === 2 && event.creates_conflict) weight *= 1.8;
  if (act === 3 && event.resolves_threads) weight *= 2.0;
  
  // 2. EMOTIONAL STATE MODIFIERS
  const emotional_modifiers = {
    "DISCOURAGED": {
      opportunity: 1.5,
      crisis: 0.5,
      social: 1.3
    },
    "OVERWHELMED": {
      crisis: 0.3,
      social: 0.7,
      aspiration: 0.6
    },
    "MOTIVATED": {
      aspiration: 1.5,
      opportunity: 1.4,
      career: 1.2
    }
  };
  
  const modifier = emotional_modifiers[player.emotional_state.primary]?.[event.category];
  if (modifier) weight *= modifier;
  
  // 3. METER STATE MODIFIERS
  if (player.meters.social < 4 && event.category === "social") weight *= 1.8;
  if (player.meters.mental < 4 && event.category === "crisis") weight *= 0.4;
  
  // 4. RELATIONSHIP NEGLECT MODIFIERS
  if (event.involves_npc) {
    const rel = player.relationships.find(r => r.npc_id === event.involves_npc);
    if (rel && rel.weeks_since_interaction > 2) {
      weight *= (1 + (rel.weeks_since_interaction * 0.3));
    }
  }
  
  // 5. ASPIRATION PROGRESS MODIFIERS
  const progress_ratio = player.aspiration.progress / 100;
  const weeks_remaining = player.season.weeks_total - player.season.current_week;
  const weeks_ratio = weeks_remaining / player.season.weeks_total;
  
  if (progress_ratio < weeks_ratio && event.category === "aspiration") {
    weight *= 1.5; // Behind schedule, prioritize aspiration events
  }
  
  // 6. RECENCY MODIFIERS (avoid repetition)
  const recent_events = getRecentEvents(player, 3); // Last 3 weeks
  const same_category_count = recent_events.filter(e => e.category === event.category).length;
  if (same_category_count > 0) {
    weight *= Math.pow(0.7, same_category_count); // Diminishing returns
  }
  
  return weight;
}
```

---

## Master Truths v1.2: Capacity-Aware Event Generation *(NEW)*

### Emotional Capacity Checking Before Heavy Events

**Purpose:** Prevent overwhelming players who are already at low capacity - respect human limitations.

```javascript
const CAPACITY_AWARE_FILTERING = {
  capacity_thresholds: {
    high: 7.0,              // Healthy state
    moderate: 5.0,          // Manageable stress
    low: 3.0,               // Struggling
    critical: 2.0           // Near breaking point
  },
  
  event_capacity_requirements: {
    crisis: {
      min_capacity: 3.0,
      description: "Crisis events require emotional resources to handle",
      if_below: "Defer crisis or reduce severity"
    },
    
    aspiration_breakthrough: {
      min_capacity: 4.0,
      description: "Major opportunities require energy to seize",
      if_below: "Offer smaller, manageable opportunities instead"
    },
    
    relationship_conflict: {
      min_capacity: 3.5,
      description: "Conflicts require capacity to navigate",
      if_below: "Offer support events instead of conflict"
    },
    
    social_intensive: {
      min_capacity: 4.5,
      description: "Group events or parties require social energy",
      if_below: "Offer one-on-one hangouts instead"
    },
    
    multiple_events_same_week: {
      min_capacity: 6.0,
      description: "Multiple events in one week require buffer capacity",
      if_below: "Limit to 1 event per week"
    }
  },
  
  filtering_logic: function(event, player_capacity) {
    // Check if player has capacity for this event
    const required_capacity = this.event_capacity_requirements[event.intensity_type]?.min_capacity || 2.0;
    
    if (player_capacity < required_capacity) {
      // Event too heavy - filter or modify
      return {
        allow: false,
        reason: `Player capacity ${player_capacity.toFixed(1)} below required ${required_capacity.toFixed(1)}`,
        alternative: this.findAlternativeEvent(event, player_capacity)
      };
    }
    
    return { allow: true };
  },
  
  alternatives_when_low_capacity: {
    instead_of_crisis: [
      "Support from friend (capacity boost)",
      "Small victory (morale boost)",
      "Peaceful moment (recovery opportunity)"
    ],
    
    instead_of_breakthrough: [
      "Incremental progress event",
      "Skill practice opportunity",
      "Mentor advice (preparation for future)"
    ],
    
    instead_of_conflict: [
      "Supportive conversation",
      "Friend notices you're struggling",
      "NPC offers help without judgment"
    ]
  }
};
```

---

### Capacity-Modified Event Selection

```javascript
function selectEventsWithCapacityAwareness(available_events, player) {
  const capacity = player.emotional_capacity;
  const filtered_events = [];
  
  available_events.forEach(event => {
    // Check capacity requirement
    const capacity_check = CAPACITY_AWARE_FILTERING.filtering_logic(event, capacity);
    
    if (capacity_check.allow) {
      filtered_events.push(event);
    } else {
      // Try to find alternative
      const alternative = capacity_check.alternative;
      if (alternative) {
        console.log(`Replaced ${event.title} with ${alternative.title} due to low capacity`);
        filtered_events.push(alternative);
      } else {
        console.log(`Skipped ${event.title}: ${capacity_check.reason}`);
      }
    }
  });
  
  // Further limit event count based on capacity
  let max_events = 2;  // Default
  if (capacity < 3.0) max_events = 1;      // Low capacity: max 1 event/week
  if (capacity < 5.0) max_events = 1;      // Moderate: still 1 event/week
  if (capacity >= 7.0) max_events = 3;     // High capacity: can handle more
  
  return filtered_events.slice(0, max_events);
}
```

---

## Master Truths v1.2: Circumstance Stacking Limits *(NEW)*

### Parallel Stressor Tracking and Prevention

**Purpose:** Prevent more than 5 simultaneous stressors - realistic constraint on human stress tolerance.

```javascript
const STRESSOR_TRACKING_SYSTEM = {
  max_active_stressors: 5,
  
  stressor_categories: {
    work_pressure: {
      examples: ["Overtime demanded", "Performance review", "Project deadline"],
      typical_duration: "2-4 weeks"
    },
    
    financial_stress: {
      examples: ["Low money", "Unexpected expense", "Rent due soon"],
      typical_duration: "1-3 weeks"
    },
    
    health_crisis: {
      examples: ["Low physical meter", "Exhaustion", "Injury/illness"],
      typical_duration: "2-6 weeks"
    },
    
    relationship_tension: {
      examples: ["Friend conflict", "Partner strain", "Family issue"],
      typical_duration: "3-8 weeks"
    },
    
    aspiration_setback: {
      examples: ["Behind schedule", "Opportunity lost", "Skill inadequacy"],
      typical_duration: "2-6 weeks"
    },
    
    time_crunch: {
      examples: ["Multiple deadlines", "Overcommitted", "No free time"],
      typical_duration: "1-4 weeks"
    },
    
    emotional_overwhelm: {
      examples: ["Capacity < 3.0", "Multiple conflicts", "Crisis fatigue"],
      typical_duration: "2-8 weeks"
    }
  },
  
  tracking_structure: {
    active_stressors: [
      {
        id: "stressor_uuid",
        category: "work_pressure",
        description: "Major project deadline in 2 weeks",
        started_week: 8,
        expected_resolution_week: 10,
        capacity_drain: -0.5,         // Per week
        compounds_with: ["time_crunch", "aspiration_setback"]
      }
      // ... more stressors
    ],
    
    total_count: number,
    total_capacity_drain: number,     // Sum of all drains
    overwhelmed_state: boolean        // True if count >= 4
  },
  
  stressor_limit_enforcement: function(potential_new_stressor, current_stressors) {
    const active_count = current_stressors.length;
    
    // Hard limit: 5 stressors
    if (active_count >= this.max_active_stressors) {
      return {
        allow: false,
        reason: "Maximum stressor limit reached (5)",
        message: "Player already OVERWHELMED - no new stressors",
        recommendation: "Offer support/resolution events instead"
      };
    }
    
    // Soft limit: 4 stressors (warn, but can add one more)
    if (active_count >= 4) {
      return {
        allow: true,
        warning: "Player at 4 stressors - approaching OVERWHELMED",
        capacity_check: "Next stressor should be final until resolution",
        narrative_flag: "This is the breaking point - dramatic consequences likely"
      };
    }
    
    // Check for compounding stressors
    const compounds = current_stressors.some(s => 
      potential_new_stressor.compounds_with?.includes(s.category)
    );
    
    if (compounds && active_count >= 3) {
      return {
        allow: false,
        reason: "New stressor would compound with existing - too much",
        recommendation: "Wait for resolution of one existing stressor first"
      };
    }
    
    return { allow: true };
  },
  
  automatic_resolution_triggers: {
    when_count_reaches_5: {
      action: "Force resolution of oldest/least-important stressor",
      reason: "Prevent permanent OVERWHELMED state",
      example: "Work deadline passes, financial crisis resolved by friend's help"
    },
    
    when_capacity_below_2: {
      action: "Trigger intervention event",
      reason: "Player near breakdown - friends/NPCs step in",
      example: "Marcus: 'I'm worried about you. Let me help.'"
    },
    
    weekly_check: {
      action: "Age out stressors past expected resolution",
      reason: "Don't let stressors linger forever",
      example: "Project finished, deadline passed, crisis naturally resolves"
    }
  }
};
```

---

### Circumstance-Aware Event Selection

```javascript
function generateEventWithCircumstanceAwareness(gameState) {
  const player = gameState.player;
  const stressors = player.active_stressors;
  const capacity = player.emotional_capacity;
  
  // 1. COUNT ACTIVE STRESSORS
  const stressor_count = stressors.length;
  
  console.log(`Active stressors: ${stressor_count}/5`);
  console.log(`Player capacity: ${capacity.toFixed(1)}/10`);
  
  // 2. CHECK IF AT STRESSOR LIMIT
  if (stressor_count >= 5) {
    console.log("⚠️ STRESSOR LIMIT REACHED - Only resolution events allowed");
    return generateResolutionEvent(stressors);
  }
  
  // 3. CHECK IF OVERWHELMED (4+ stressors or capacity < 3.0)
  const overwhelmed = stressor_count >= 4 || capacity < 3.0;
  
  if (overwhelmed) {
    console.log("⚠️ PLAYER OVERWHELMED - Prioritizing support/resolution");
    
    // 80% chance of support/resolution event
    if (Math.random() < 0.8) {
      return generateSupportEvent(player);
    }
    
    // 20% chance of manageable event (but no new stressors)
    return generateLowIntensityEvent(player);
  }
  
  // 4. NORMAL EVENT GENERATION
  const available_events = getAvailableEvents(player);
  
  // Filter events that would create new stressors
  const filtered_events = available_events.filter(event => {
    if (event.creates_new_stressor) {
      const stressor_check = STRESSOR_TRACKING_SYSTEM.stressor_limit_enforcement(
        event.stressor_data,
        stressors
      );
      
      if (!stressor_check.allow) {
        console.log(`Filtered out ${event.title}: ${stressor_check.reason}`);
        return false;
      }
    }
    
    return true;
  });
  
  // 5. SELECT EVENT
  return selectEvent(filtered_events, player);
}
```

---

### Support Events (Capacity Recovery)

```javascript
const SUPPORT_EVENT_TEMPLATES = {
  friend_intervention: {
    title: "Friend Reaches Out",
    trigger: "capacity < 3.0 OR stressor_count >= 4",
    category: "support",
    
    narrative: function(player, npc) {
      return `
        ${npc.name} texts: "Hey, I've been thinking about you. You okay? 
        Want to grab coffee? My treat."
        
        [${npc.name}'s Agreeableness: ${npc.personality.agreeableness.toFixed(1)} - they notice when you're struggling]
      `;
    },
    
    options: [
      {
        id: "accept_support",
        label: "\"I'd love that. Thanks for checking in.\"",
        costs: { time: 2, energy: 1 },
        outcomes: {
          capacity_boost: +1.5,
          emotional: +2,
          relationships: { [npc]: { trust: +0.10 } },
          narrative: "Honest conversation. They listen. No judgment. You feel lighter."
        }
      },
      {
        id: "deflect",
        label: "\"I'm fine, really. Just busy.\"",
        costs: {},
        outcomes: {
          capacity_boost: 0,
          relationships: { [npc]: { trust: -0.02 } },
          narrative: "They don't believe you, but they don't push. For now."
        }
      }
    ],
    
    frequency: "triggered_by_capacity_threshold",
    replaces: "crisis_events_when_overwhelmed"
  },
  
  unexpected_victory: {
    title: "Small Win",
    trigger: "capacity < 4.0 AND recent_setbacks > 0",
    category: "support",
    
    narrative: "Something goes right. Not a huge victory, but a genuine win. You needed this.",
    
    outcomes: {
      capacity_boost: +1.0,
      emotional: +2,
      aspiration_progress: +5,
      narrative: "Proof that you're not failing at everything. A breath of fresh air."
    },
    
    examples: [
      "Client emails: 'Love your work. When can we book you?'",
      "Boss: 'Good job on that project. Really solid work.'",
      "Your photo gets 100+ likes and genuine compliments",
      "Friend: 'You inspired me to try this too. Thank you.'"
    ],
    
    frequency: "when_player_needs_hope"
  },
  
  forced_rest: {
    title: "Your Body Makes the Choice",
    trigger: "physical_meter <= 2 AND capacity < 2.5",
    category: "support",
    
    narrative: `
      You wake up and your body refuses to cooperate. Not sick, exactly. 
      Just... done. Exhausted. Empty.
      
      You're taking today off. Your body decided for you.
    `,
    
    outcomes: {
      day_lost: true,
      physical_meter: +2,
      capacity_boost: +1.0,
      aspiration_progress: 0,
      narrative: "Sometimes rest isn't optional. Sometimes you need to listen."
    },
    
    frequency: "triggered_by_health_crisis"
  }
};
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Vocabulary & Scales (Section 2)
- [x] Emotional capacity (0-10 scale) integrated into event filtering
- [x] OCEAN traits influence event weighting
- [x] Meters (0-10 scale) affect event selection
- [x] Emotional states modify event priorities

### ✅ Turn Structure (Section 4)
- [x] Decisive decisions pause time (special events)
- [x] Turn economy respected in event placement
- [x] No anxiety-inducing real-time pressure
- [x] Ticking clocks use in-world time only

### ✅ Narrative Structure (Section 5)
- [x] Events serve narrative/relationship progression
- [x] Events aligned with 3-act structure
- [x] Hook points placed between major beats (2-3 weeks)
- [x] Mystery threads limited to 2-3 max

### ✅ Emotional Authenticity (Section 16) *(NEW in v1.2)*
- [x] **Capacity-Aware Event Filtering:** Events require minimum capacity (3.0-6.0 range)
- [x] **Event Alternatives:** Low-capacity players get support events instead of crises
- [x] **Event Count Limits:** Max events per week based on capacity (1-3 events)
- [x] **Stressor Tracking:** Active stressors tracked with categories and durations
- [x] **Stressor Limit Enforcement:** Hard limit of 5 simultaneous stressors
- [x] **Automatic Resolution:** Stressors force-resolved at limit to prevent permanent OVERWHELMED
- [x] **Support Event Triggers:** Friend intervention, small wins, forced rest when capacity < 3.0

### ✅ Novel-Quality Narrative (Section 17) *(NEW in v1.2)*
- [x] **Hook Points System:** Tension maintained every 2-3 weeks
- [x] **Mystery Thread Tracking:** Max 3 active mysteries per season
- [x] **Ticking Clock Mechanics:** In-world urgency without FOMO
- [x] **Micro-Cliffhangers:** Strategic use at day/week/turn ends (selective, not every time)
- [x] **Tension Injection Types:** 5 types (mystery, revelation, opportunity, relationship shift, external pressure)

### ✅ Event Generation Quality
- [x] Events content-driven, not RNG gacha
- [x] Event frequency scaled to season length (12w/24w/36w)
- [x] Dynamic weighting by context (act, emotional state, relationships)
- [x] Recency filtering prevents repetition
- [x] Relationship neglect prioritizes re-engagement

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~420 lines** of new v1.2 content
2. **Capacity-Aware Filtering:** Events check player capacity before generation
3. **Stressor Limit System:** Maximum 5 simultaneous stressors with tracking
4. **Circumstance-Aware Selection:** Events adjusted based on active stressors
5. **Support Event Templates:** 3 types of capacity recovery events
6. **Automatic Interventions:** System prevents permanent overwhelmed state

**Design Principles:**
- Respect human limitations (no more than 5 stressors)
- Offer support when capacity low (don't pile on)
- Track and resolve stressors naturally over time
- Replace crises with support events when overwhelmed
- Tension serves narrative, never random drama
- All hooks connect to main aspiration or relationships

**References:**
- See `01-emotional-authenticity.md` for cross-system integration overview
- See `02-system-by-system-enhancement.md` for detailed gap analysis
- See `14-emotional-state-mechanics.md` for emotional capacity system
- See `31-narrative-arc-scaffolding.md` for arc-driven events and capacity curves
- See `30-decisive-decision-templates.md` for major decision events
- See `72-weekly-cycle-implementation.md` for event placement
- See `35-tension-maintenance-system.md` for complete hook point and mystery implementation

---

**This specification enables developers to implement the complete event generation system with capacity-aware filtering, stressor limit enforcement, and circumstance-aware selection that respects human limitations and creates authentic emotional experiences.**

