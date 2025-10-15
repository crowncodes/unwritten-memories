# Card Evolution Mechanics - Complete Implementation

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete system for how generic base cards evolve into personalized, unique variations through play

**References:**
- **Base Cards:** `20-base-card-catalog.md` (all ~480 starting cards)
- **Fusion System:** `22-card-fusion-system.md` (combining evolved cards)
- **Design Philosophy:** `1.concept/12-card-evolution.md` (WHY evolution matters)
- **AI System:** `3.ai/README.md` (TensorFlow Lite inference for personality)

---

## Overview

**Card Evolution** transforms generic base cards into personalized variations unique to each playthrough. A "Coffee with Friend" card evolves into "Tuesday Coffee with Sarah at Café Luna Where She Told Me Her Dream."

**Core Principle:** Cards are memory units. Evolution = memory formation. Generic experience → specific memory → landmark moment.

**Compliance:** Evolution uses canonical systems (relationships 0-5, personality OCEAN, emotional states) and creates novel-worthy content for Life Bookshelf generation.

---

## Evolution System Architecture

### Three Evolution Dimensions

```typescript
interface CardEvolution {
  // DIMENSION 1: Relationship-Based (NPCs)
  relationship_evolution: {
    trigger: "interaction_count" | "trust_threshold" | "decisive_moment",
    depth_levels: [0, 1, 2, 3, 4, 5],            // Matches relationship levels
    reveals_personality: boolean,
    unlocks_deeper_interactions: boolean
  };
  
  // DIMENSION 2: Time-Based (Locations, Activities)
  temporal_evolution: {
    trigger: "repetition_count" | "time_elapsed" | "seasonal",
    stages: ["generic", "familiar", "routine", "tradition", "landmark"],
    emotional_weight_accumulates: boolean
  };
  
  // DIMENSION 3: Event-Based (Crisis, Breakthrough)
  narrative_evolution: {
    trigger: "crisis" | "breakthrough" | "phase_transition",
    creates_new_cards: boolean,
    permanent_change: boolean,
    arc_impact: string
  };
}
```

---

## Master Truths v1.2: Emotional Authenticity in Evolution *(NEW)*

### Emotional Significance Tracking

Card evolution now tracks **WHY** evolution happens, not just mechanical triggers:

```javascript
interface EmotionalEvolution {
  // MECHANICAL TRIGGER (v1.1)
  mechanical_requirement: {
    interactions: 16,
    trust: 0.6,
    weeks_known: 6
  };
  
  // EMOTIONAL SIGNIFICANCE (v1.2 - NEW)
  emotional_trigger: {
    vulnerability_shared: boolean;        // Did something REAL happen?
    emotional_capacity_moment: boolean;   // Was support given/received?
    memory_significance: number;          // 0-10 scale
    authentic_connection: boolean;        // Felt real vs going through motions
  };
  
  // Evolution requires BOTH mechanical AND emotional criteria
  evolution_blocked_if: {
    only_mechanical: "16 shallow interactions don't create friendship",
    no_vulnerability: "Can't reach Level 3 without sharing something real",
    low_significance: "Memories must matter (weight > 5) to evolve"
  };
}

// EXAMPLE: Level 2 → Level 3 Evolution Blocked
const EVOLUTION_CHECK = {
  sarah_level_2: {
    interactions: 18,              // ✓ Meets mechanical requirement (16+)
    trust: 0.62,                   // ✓ Meets trust requirement (0.6+)
    weeks_known: 8,                // ✓ Meets time requirement (6+)
    
    // But...
    vulnerability_shared: false,   // ✗ No real moments yet
    memory_significance: 4.2,      // ✗ Below threshold (need 5.0+)
    
    result: "EVOLUTION BLOCKED",
    
    narrative: `
      You've had coffee with Sarah 18 times. You know her coffee order. 
      You know she likes books. But you don't really KNOW her yet. She 
      hasn't opened up. Neither have you.
      
      This is acquaintance territory, not friendship.
    `,
    
    unlock_requirement: `
      Trigger vulnerability: Share something personal, or be there during 
      a difficult moment. Create a memory that matters.
    `
  },
  
  // After vulnerability moment
  sarah_level_2_after_vulnerability: {
    interactions: 19,              // Added one more interaction
    trust: 0.68,                   // Jumped from 0.62
    
    // The difference:
    vulnerability_shared: true,    // ✓ Sarah shared about David
    memory_significance: 8.1,      // ✓ This memory MATTERS
    authentic_connection: true,    // ✓ Real moment
    
    result: "EVOLUTION TO LEVEL 3",
    
    narrative: `
      Coffee with Sarah, week 9. But this time is different. She tells you 
      about David—her fiancé who died two years ago. The bookshop was their 
      dream. She's never told anyone at the café before.
      
      You realize: She trusts you. This is friendship now.
    `
  }
};
```

### Capacity-Aware Evolution

NPCs evolve based on **emotional capacity** to deepen relationships:

```javascript
const CAPACITY_AWARE_EVOLUTION = {
  principle: "NPCs can't deepen relationships when emotionally depleted",
  
  sarah_wants_to_evolve: {
    mechanical_requirements: "✓ All met (20 interactions, trust 0.72)",
    player_ready: true,
    
    // But...
    sarah_emotional_capacity: 2.8,    // Very low (0-10 scale)
    sarah_stressors: [
      "job_stress",
      "anniversary_of_david_death_approaching",
      "financial_worries"
    ],
    
    result: "EVOLUTION DELAYED",
    
    narrative: `
      You can tell Sarah's struggling. She's more distant lately. Distracted. 
      You want to ask what's wrong, but the timing feels off. She needs space.
    `,
    
    gameplay_effect: {
      level_up_delayed: "2-4 weeks",
      requires_player_support: "Help Sarah through stressors first",
      capacity_threshold: "Sarah needs capacity > 5.0 to evolve to Level 4"
    }
  },
  
  // After player helps Sarah through crisis
  sarah_after_support: {
    sarah_emotional_capacity: 6.5,    // Recovered
    stressors_resolved: "Player helped with anniversary grief",
    
    result: "EVOLUTION TO LEVEL 4 UNLOCKED",
    
    narrative: `
      The anniversary passed. You were there for Sarah—didn't push, just 
      present. She texts you: "Thank you for last week. I needed that. 
      Coffee Tuesday?"
      
      But this time when you meet, something's different. She's lighter. 
      "You're one of the only people who gets it," she says. "I trust you."
      
      Close friend. Not just friend anymore.
    `,
    
    permanent_effect: "Crisis deepened bond faster than normal progression"
  }
};
```

### Journey Tracking vs Mechanical Triggers

Evolution tracks the **narrative journey**, not just counters:

```javascript
const JOURNEY_BASED_EVOLUTION = {
  // OLD WAY (v1.1): Pure mechanical
  mechanical_only: {
    sarah_level_0_to_5_path: [
      "0 → 1: First meeting",
      "1 → 2: 6 interactions",
      "2 → 3: 16 interactions, trust 0.6",
      "3 → 4: 31 interactions, trust 0.8",
      "4 → 5: 76 interactions, trust 0.95"
    ],
    problem: "Feels like grinding. No narrative meaning."
  },
  
  // NEW WAY (v1.2): Journey beats + mechanical
  journey_based: {
    sarah_level_0_to_5_journey: [
      {
        stage: "0 → 1: First Meeting",
        mechanical: "1 interaction",
        journey_beat: "Noticed each other, conversation sparked",
        emotional_weight: 4
      },
      {
        stage: "1 → 2: Growing Familiarity", 
        mechanical: "6 interactions, 2-4 weeks",
        journey_beat: "Coffee ritual forming, learning preferences",
        emotional_weight: 5
      },
      {
        stage: "2 → 3: Real Friendship Forms",
        mechanical: "16 interactions, trust 0.6, 6+ weeks",
        journey_beat: "Vulnerability shared, trust earned, real connection",
        required_moment: "MUST have vulnerability beat (can't skip)",
        emotional_weight: 7
      },
      {
        stage: "3 → 4: Close Friends",
        mechanical: "31 interactions, trust 0.8, 12+ weeks",
        journey_beat: "Crisis survived together OR major life support",
        required_moment: "MUST have crisis/support beat",
        emotional_weight: 9
      },
      {
        stage: "4 → 5: Best Friend / Life Partner",
        mechanical: "76 interactions, trust 0.95, 1+ year",
        journey_beat: "Years together, multiple crises, unbreakable bond",
        required_moments: [
          "Multiple vulnerability moments",
          "Multiple crisis supports",
          "Life decisions made together"
        ],
        emotional_weight: 10
      }
    ],
    
    enforcement: "Mechanical + Journey both required. Can't level up without BOTH."
  }
};
```

### Enhanced Character Depth Through Authenticity

NPCs reveal depth **only when appropriate** to relationship level:

```javascript
const AUTHENTIC_REVEAL_PACING = {
  sarah_backstory_revelation: {
    // WHAT PLAYER KNOWS AT EACH LEVEL
    
    level_1_stranger: {
      revealed: [
        "Works at café",
        "Loves books",
        "Quiet, reserved",
        "Freckles, cerulean scarf"
      ],
      hidden: "Everything about David, bookshop dream, grief, fears"
    },
    
    level_2_acquaintance: {
      revealed: [
        ...level_1,
        "Wants to open bookshop someday",
        "Saving money",
        "Has specific coffee ritual (chai, extra foam, Tuesdays)",
        "Writes poetry (saw notebook)"
      ],
      partially_revealed: [
        "Mentions 'someone special' died (doesn't elaborate)",
        "Gets sad around certain dates (doesn't explain)"
      ],
      hidden: "David's name, how he died, depth of grief"
    },
    
    level_3_friend: {
      revealed: [
        ...level_2,
        "David was her fiancé",
        "He died 2 years ago in car accident",
        "Bookshop was THEIR dream",
        "Still processing grief"
      ],
      partially_revealed: [
        "Has panic attacks sometimes (mentioned once)",
        "Complicated relationship with family (touched on)"
      ],
      hidden: "Full trauma details, family estrangement reasons"
    },
    
    level_4_close_friend: {
      revealed: [
        ...level_3,
        "Full David story (wedding was 3 weeks away)",
        "Panic attacks happen on Thursdays (day of accident)",
        "Family blamed her for not stopping David that day",
        "Hasn't spoken to mother in 18 months"
      ],
      hidden: "Deep fear: 'What if I never love again?'"
    },
    
    level_5_best_friend: {
      revealed: "EVERYTHING. No secrets.",
      including: [
        "Deepest fear: dying alone",
        "Guilt: sometimes angry at David for dying",
        "Hope: maybe ready to try loving again",
        "You know her better than anyone"
      ]
    }
  },
  
  v1_2_enforcement: {
    rule: "NPCs NEVER reveal inappropriately deep information",
    examples: {
      bad: "Level 1 Sarah immediately tells you about dead fiancé",
      good: "Level 1 Sarah mentions she likes books, nothing personal yet",
      
      bad: "Level 2 Sarah shares deepest trauma in casual conversation",
      good: "Level 2 Sarah hints at loss, doesn't elaborate, creates mystery",
      
      bad: "Level 3 instantly unlocks all backstory",
      good: "Level 3 reveals David's existence, but more mysteries remain"
    },
    
    design_principle: "Depth is EARNED through time, vulnerability, and emotional capacity"
  }
};
```

---

## Character Card Evolution (Relationship-Driven)

### Complete Evolution Path

```javascript
const CHARACTER_EVOLUTION_STAGES = {
  stage_0_not_met: {
    card_state: "Generic stranger card (archetype only)",
    
    example: {
      name: "Stranger at Coffee Shop",
      level: 0,
      art: "[Generic silhouette]",
      narrative: "Someone sitting alone at the café. Reading a book.",
      personality: "Unknown",
      options: ["Approach", "Ignore"]
    },
    
    available_interactions: ["first_meeting_only"]
  },
  
  stage_1_first_meeting: {
    trigger: {
      action: "Player chooses to interact",
      ai_generates: "Complete NPC with personality, name, appearance"
    },
    
    evolution_process: {
      inputs: {
        player_personality: "OCEAN scores",
        player_emotional_state: "Current state",
        player_life_direction: "Active direction",
        interaction_quality: "Positive/neutral/negative",
        context: "Location, time, player's current aspiration"
      },
      
      ai_outputs: {
        npc_name: "Procedurally generated or from name pool",
        npc_personality: "OCEAN scores (balanced against player for chemistry)",
        npc_appearance: "Physical features, style, key details",
        npc_backstory_seed: "Mystery hooks for long-term reveals",
        dialogue_sample: "First words spoken",
        compatibility_score: 0.0-1.0,
        portrait_generation: "Text prompt for image generation"
      }
    },
    
    card_after_evolution: {
      name: "Sarah Anderson",
      level: 1,                          // Stranger
      trust: 0.1,
      interactions: 1,
      
      art: "[AI-generated portrait: Young woman, freckles, cerulean scarf, warm smile]",
      
      narrative: `
        Barista at Café Luna. Noticed you were reading Murakami and 
        started a conversation. Has freckles, wears a cerulean scarf.
      `,
      
      personality_revealed: {
        openness: 4.3,                   // Partial reveal
        agreeableness: 4.6,              // Observable traits visible
        neuroticism: 3.9                 // Deeper traits hidden until later
      },
      
      mystery_planted: "Mentions 'books are safer than people' (why?)",
      
      unlocks: [
        "Coffee with Sarah (activity)",
        "Ask about books (conversation)",
        "Invite to gallery opening (if player is creative)"
      ]
    }
  },
  
  stage_2_acquaintance: {
    trigger: {
      interactions: 6,                   // 6-15 interactions
      trust: 0.3,
      time: "2-6 weeks"
    },
    
    evolution_changes: {
      narrative_updates: "More specific, references past interactions",
      personality_depth: "More traits revealed",
      backstory_hints: "Mystery clues dropped",
      
      example_narrative: `
        Sarah Chen. You've had coffee with her five times now. Always 
        orders chai latte, extra foam. She's quieter on Mondays. Lights 
        up when talking about books, especially poetry. You still don't 
        know much about her life outside the café.
      `
    },
    
    unlocked_interactions: [
      "Deeper conversations",
      "Ask about her week",
      "Share something personal",
      "Invite to longer activity (dinner, movie)"
    ],
    
    relationship_status: "Becoming friends",
    emotional_weight: "Building significance"
  },
  
  stage_3_friend: {
    trigger: {
      interactions: 16,                  // 16-30 interactions
      trust: 0.6,
      vulnerability_moment: true,        // Player or NPC shared something real
      time: "6-12 weeks"
    },
    
    evolution_changes: {
      personality_complete: "All OCEAN traits revealed",
      backstory_major_reveal: "First major mystery clue",
      emotional_depth: "NPC expresses genuine care",
      
      example_narrative: `
        Sarah Chen, Level 3 Friend (Trust: 0.68)
        
        "You know that dream I mentioned? Opening a bookshop? I'm serious 
        about it. I've been saving. I have $12,000. It's not enough, but... 
        it's a start."
        
        She looks at you like this matters. Like your opinion matters.
        
        MEMORIES TOGETHER: 18
        - Week 3: First real conversation about literature
        - Week 8: Coffee ritual established (Tuesdays)
        - Week 12: She opened up about feeling stuck in her job
        - Week 16: You supported her through rough week
      `
    },
    
    unlocked_systems: {
      deeper_activities: [
        "Weekend hangouts",
        "Help with her projects",
        "Introduce to your friends",
        "Deep vulnerable conversations"
      ],
      
      fusion_opportunities: [
        "Sarah + Business Planning = Collaborate on bookshop",
        "Sarah + Crisis = Be there during hard times",
        "Sarah + Joy = Celebrate successes together"
      ],
      
      arc_potential: "Sarah's bookshop could become major aspiration"
    }
  },
  
  stage_4_close_friend: {
    trigger: {
      interactions: 31,                  // 31-75 interactions
      trust: 0.80,
      crisis_survived_together: true,
      time: "12-24+ weeks"
    },
    
    evolution_changes: {
      backstory_fully_revealed: "Who is David? (David was her fiancé who died)",
      role_in_life: "Major character in player's story",
      mutual_support: "Reciprocal deep trust",
      
      example_narrative: `
        Sarah Chen, Level 4 Close Friend (Trust: 0.87)
        
        Today is August 14. She told you what that means: David's birthday. 
        He died two years ago. They were planning the wedding.
        
        "You're one of the only people I've told. Thank you for being patient 
        with me. For not pushing. For just... being here."
        
        You realize: This friendship has become foundational to your life.
        
        MEMORIES TOGETHER: 47
        - Week 3: First meeting
        - Week 18: She shared her bookshop dream
        - Week 28: Crisis: You helped when she had panic attack
        - Week 35: She finally told you about David
        - Week 42: You supported bookshop opening
      `
    },
    
    gameplay_integration: {
      appears_in_major_decisions: true,
      affects_life_direction_choices: true,
      emergency_support_available: "Call Sarah anytime",
      bookshop_location_unlocked: true
    }
  },
  
  stage_5_best_friend_soulmate: {
    trigger: {
      interactions: 76+,
      trust: 0.95,
      years_known: 1+,
      survived_multiple_crises: true
    },
    
    final_evolution: {
      role: "Life partner (platonic or romantic depending on player choice)",
      narrative_weight: "Major character in Life Bookshelf novels",
      permanent_bond: "Cannot lose this relationship (short of catastrophic choices)",
      
      example_narrative: `
        Sarah Chen, Level 5 Best Friend (Trust: 0.98)
        
        The bookshop is thriving. You were there from the beginning—the 
        planning, the loan applications, the renovation, the opening night.
        
        She named the poetry section after you.
        
        Some people come into your life and change everything. Sarah is 
        one of those people.
        
        MEMORIES TOGETHER: 94
        [Complete relationship history—every major moment documented]
      `
    }
  }
};
```

---

## Location Card Evolution (Time & Repetition-Driven)

### Evolution Through Familiarity

```javascript
const LOCATION_EVOLUTION = {
  base_card: {
    name: "Coffee Shop",
    tier: 7,
    state: "generic",
    
    art: "[Stock image: Generic café interior]",
    narrative: "A café. Decent coffee. Tables available.",
    
    unlocked_activities: [
      "Get coffee (basic)",
      "Work on laptop",
      "Meet someone here"
    ]
  },
  
  after_5_visits: {
    evolution_trigger: "Repetition establishes familiarity",
    
    name: "Café Luna (Your Usual Spot)",
    state: "familiar",
    
    art: "[More specific: Your preferred corner, window seat visible]",
    
    narrative: `
      Café Luna. You know the barista's name now (Maya). She remembers 
      your order. The window seat is usually free in the afternoons.
    `,
    
    mechanical_benefits: {
      time_cost: -0.5,                   // Slightly faster (know the routine)
      comfort_bonus: +1,                 // Feels safe
      success_rate: +0.05                // Familiar environment boost
    },
    
    unlocked_activities: [
      "Your usual order (quick)",
      "Window seat guaranteed",
      "Chat with Maya (barista relationship begins)"
    ]
  },
  
  after_15_visits: {
    evolution_trigger: "Location becomes routine",
    
    name: "Café Luna - Where You Think Best",
    state: "routine",
    
    art: "[Personalized: Your corner, your mug, your view]",
    
    narrative: `
      Café Luna is your place now. Tuesday afternoons especially. The light 
      through the window at 3 PM. Maya brings your chai without asking.
      
      This is where you figured out the portfolio layout. Where Sarah first 
      told you about the bookshop dream. Where you write.
    `,
    
    mechanical_benefits: {
      time_cost: -1,
      comfort_bonus: +2,
      creativity_boost: +0.1,            // Productive environment
      relationship_meetings_better: "Friends enjoy this spot because you do"
    },
    
    emotional_attachment: 6              // 0-10 scale
  },
  
  after_50_visits_plus_landmark_moment: {
    evolution_trigger: "Repetition + major memory created here",
    
    name: "Café Luna - Where Everything Changed",
    state: "landmark",
    
    art: "[Highly personalized: Rich detail, emotional lighting, YOUR café]",
    
    narrative: `
      Café Luna. Your café.
      
      This is where you first met Sarah (Week 3). Where Marcus talked you 
      out of quitting photography (Week 14). Where you decided to launch 
      your business (Week 22).
      
      Maya retired last month. The new barista doesn't know your order, 
      but that's okay. This place has too many memories to abandon now.
      
      Your corner. Your window. Your 3 PM light. Your decisions.
    `,
    
    mechanical_benefits: {
      time_cost: -1,
      comfort_bonus: +3,
      all_activities_here: "+10% success",
      emotional_anchor: "Returns here during crisis for stability"
    },
    
    emotional_attachment: 10,            // Maximum
    
    novel_worthy: true,
    chapter_potential: "This location gets mentioned in every season's novel"
  }
};
```

---

## Activity Card Evolution (Ritual Formation)

### From Action to Tradition

```javascript
const ACTIVITY_EVOLUTION = {
  first_use: {
    card: "Coffee with Sarah",
    state: "new_activity",
    
    narrative: "Grab coffee with Sarah. See how she's doing.",
    
    effects: {
      time: 1.5,
      energy: -1,                        // Restores 1
      relationship_trust: +0.05,
      generic_positive: true
    }
  },
  
  third_use: {
    evolution_trigger: "Pattern emerging",
    
    card: "Our Tuesday Coffee",
    state: "emerging_ritual",
    
    narrative: "Tuesday coffee with Sarah. It's becoming a thing. You both look forward to it.",
    
    effects: {
      time: 1.5,
      energy: -1,
      relationship_trust: +0.08,         // Stronger bond
      comfort: +1,                       // Anticipation feels good
      emotional_benefit: "Stability through routine"
    },
    
    skipping_consequences: "Sarah texts: 'No coffee today? Everything okay?'"
  },
  
  tenth_use: {
    evolution_trigger: "Ritual established",
    
    card: "Tuesday Coffee at Café Luna with Sarah",
    state: "ritual",
    
    narrative: `
      It's Tuesday. 3 PM. Café Luna. Sarah is already there, window seat, 
      two chai lattes ordered. She smiles when you walk in.
      
      This is your thing now. Has been for weeks.
    `,
    
    effects: {
      time: 1.5,
      energy: -2,                        // Even more restorative
      relationship_trust: +0.10,
      comfort: +2,
      emotional: +1,
      weekly_anchor: "Provides structure to week"
    },
    
    skipping_consequences: {
      must_explain: true,
      sarah_trust: -0.05,
      emotional_cost: "Breaking ritual feels wrong",
      makeup_required: "Need to reschedule or explain"
    }
  },
  
  twentieth_use_plus_landmark: {
    evolution_trigger: "Ritual + major moment occurred during it",
    
    card: "Tuesday Coffee - Where Sarah Told Me Everything",
    state: "tradition_landmark",
    
    narrative: `
      Tuesday. 3 PM. Café Luna. Sarah. Chai.
      
      This is where she told you about David. Where you supported her 
      through the panic attack. Where she shared the bookshop dream. 
      Where you've laughed, cried, planned, dreamed.
      
      Some rituals become sacred. This is one of them.
    `,
    
    effects: {
      time: 1.5,
      energy: -2,
      relationship_trust: +0.15,         // Deep bond reinforcement
      comfort: +3,
      emotional: +2,
      memory_weight: 9,                  // Novel-worthy
      unbreakable_bond: "This tradition is part of your story"
    },
    
    novel_chapter_material: true,
    carries_across_seasons: true         // Will be referenced in future seasons
  }
};
```

---

## Event-Based Evolution (Crisis & Breakthrough)

### Permanent Character/World Changes

```javascript
const EVENT_BASED_EVOLUTION = {
  crisis_evolution: {
    trigger: "Major crisis card resolves",
    
    example_collapse_crisis: {
      base_state: {
        physical_meter: 0,
        weeks_ignored_health: 6,
        crisis_card: "You collapsed during wedding shoot"
      },
      
      evolution_aftermath: {
        new_cards_created: [
          {
            name: "Remember When I Collapsed",
            type: "memory_card",
            tier: 5,
            
            appears_when: "Physical meter drops below 4",
            
            narrative: `
              You remember the wedding. The floor rushing up. Waking up 
              to Marcus's scared face. The hospital. The shame.
              
              You promised yourself: Never again.
            `,
            
            effects: {
              warning_system: "Prevents second collapse",
              emotional_reminder: "Motivates self-care",
              relationship_reminder: "Marcus saved you that day"
            }
          }
        ],
        
        character_evolution: {
          marcus_card_evolution: "Marcus, Who Saved My Life",
          sarah_card_evolution: "Sarah, Who Brought Food to Hospital",
          
          trust_permanent_changes: {
            marcus: +0.3,
            sarah: +0.15
          },
          
          relationship_dynamics_shift: "Friends become protective"
        },
        
        world_state_changes: {
          reputation: -3,                // Photography reputation damaged
          unlocked_aspirations: ["Recovery and Reflection", "Rebuild Reputation"],
          closed_paths: ["Immediate business scaling"]
        }
      }
    }
  },
  
  breakthrough_evolution: {
    trigger: "Breakthrough event card resolves",
    
    example_creative_breakthrough: {
      base_state: {
        skill_photography: 7,
        consistent_practice: "10+ weeks",
        mental_meter: 8,
        breakthrough_card: "Creative Breakthrough"
      },
      
      evolution_aftermath: {
        new_cards_created: [
          {
            name: "Your Signature Style",
            type: "perk_card",
            tier: 6,
            
            narrative: "You found it. The thing that makes your work *yours*.",
            
            effects: {
              all_photography: "+20% success",
              portfolio_value: +2,
              unique_selling_point: true,
              npc_recognition: "Gallery owners notice your work"
            }
          }
        ],
        
        skill_jump: {
          photography: 7 → 8,            // Full level instantly
          confidence: +0.3,
          unlocks: "Master-tier photography activities"
        },
        
        aspiration_acceleration: {
          active_aspirations: "+25% progress",
          new_aspirations_unlocked: ["Gallery Showing", "Teach Workshops"]
        }
      }
    }
  }
};
```

---

## AI Evolution Generation System

### Technical Implementation

```javascript
async function evolveCard(baseCard, evolutionContext) {
  const evolutionRequest = {
    card_id: baseCard.id,
    card_tier: baseCard.tier,
    evolution_trigger: evolutionContext.trigger,
    
    player_context: {
      personality: playerCharacter.personality,
      emotional_state: playerCharacter.currentEmotionalState,
      life_direction: playerCharacter.activeLifeDirection,
      aspiration: playerCharacter.activeAspiration,
      
      interaction_history: evolutionContext.interactions,
      relationship_level: evolutionContext.relationshipLevel,
      trust_score: evolutionContext.trustScore
    },
    
    narrative_context: {
      current_week: gameState.currentWeek,
      current_season: gameState.currentSeason,
      recent_events: gameState.recentMajorEvents,
      active_arcs: gameState.activeNarrativeArcs
    },
    
    constraints: {
      art_style: playerPreferences.artStyle,
      personality_archetype: baseCard.archetype || "balanced",
      narrative_role: determineNarrativeRole(evolutionContext),
      compatibility_target: calculateCompatibilityTarget(playerCharacter)
    }
  };
  
  // Run TensorFlow Lite inference
  const aiGeneration = await tensorflowLiteModel.generate(evolutionRequest);
  
  // Create evolved card
  const evolvedCard = {
    ...baseCard,
    
    // AI-generated content
    name: aiGeneration.generated_name,
    narrative: aiGeneration.generated_narrative,
    personality: aiGeneration.personality_scores,
    appearance: aiGeneration.appearance_details,
    backstory_seed: aiGeneration.mystery_hook,
    
    // Evolution metadata
    evolution_stage: evolutionContext.stage,
    evolution_history: [
      ...baseCard.evolution_history || [],
      {
        week: gameState.currentWeek,
        trigger: evolutionContext.trigger,
        player_choice: evolutionContext.playerAction
      }
    ],
    
    // Updated mechanics
    unlocked_interactions: aiGeneration.unlocked_activities,
    fusion_potential: calculateFusionPotential(evolvedCard, gameState),
    
    // Memory storage
    stored_interactions: evolutionContext.interactions,
    emotional_weight: calculateEmotionalWeight(evolutionContext)
  };
  
  // Generate portrait if character card
  if (baseCard.tier === 7 && baseCard.category === "character") {
    evolvedCard.portrait_url = await generatePortrait(aiGeneration.portrait_prompt);
  }
  
  // Save to player deck
  await saveEvolvedCard(evolvedCard, playerCharacter.id);
  
  // Log for novel generation
  await logEvolutionForNovel(evolvedCard, evolutionContext);
  
  return evolvedCard;
}
```

---

## Evolution Tracking & Memory

### Persistence Across Seasons

```javascript
interface EvolutionMemory {
  card_id: string;
  evolution_timeline: EvolutionEvent[];
  current_state: CardState;
  emotional_weight: number;              // 0-10
  novel_significance: number;            // How much this features in generated novel
  
  carries_across_seasons: boolean;       // Sarah persists Season 1 → Season 8
  
  cross_season_references: {
    first_appeared: { season: 1, week: 3 },
    major_moments: [
      { season: 1, week: 18, event: "Shared bookshop dream" },
      { season: 2, week: 8, event: "Revealed David story" },
      { season: 3, week: 12, event: "Opened bookshop together" }
    ],
    current_status: { season: 4, week: 6, state: "Best friend, business partner" }
  }
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

**Master Truths v1.2 Enhancements Implemented:**
- ✅ Emotional significance tracking (vulnerability required for evolution)
- ✅ Capacity-aware evolution (NPCs can't deepen when depleted)
- ✅ Journey tracking vs mechanical triggers (both required)
- ✅ Enhanced character depth (appropriate reveals per level)
- ✅ Evolution blocked without authentic connection moments

**References:**
- See `20-base-card-catalog.md` for all base cards that can evolve
- See `22-card-fusion-system.md` for combining evolved cards
- See `13-meter-effects-tables.md` for emotional capacity calculations
- See `14-emotional-state-mechanics.md` for emotional state effects  
- See `01-emotional-authenticity.md` for v1.2 authenticity systems

---

**This specification enables developers to implement the complete card evolution system with AI-generated personalization, emotionally authentic relationship progression, capacity-aware evolution, journey-based leveling, and multi-season memory persistence that creates unique, novel-worthy player stories.**

