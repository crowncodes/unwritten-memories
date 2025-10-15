# Card Fusion System - Complete Implementation

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete system for combining evolved cards into new fusions that create emergent narrative

**References:**
- **Base Cards:** `20-base-card-catalog.md` (all ~480 starting cards)
- **Evolution:** `21-card-evolution-mechanics.md` (how cards evolve before fusing)
- **Design Philosophy:** `1.concept/14-fusion-combinations.md` (WHY fusion matters)

---

## Overview

**Card Fusion** occurs when 2+ cards are played together in the same context, creating a new card that remembers the combination. "Sarah" + "Coffee" + "Joy" → "Perfect Afternoon with Sarah at Café Luna."

**Core Principle:** Fusions are memory compounds. Individual experiences combine into richer, more specific memories.

**Compliance:** Fusions respect canonical systems and create novel-worthy narrative beats that enhance Life Bookshelf generation.

---

## Fusion System Architecture

### Five Fusion Types

```typescript
interface FusionSystem {
  simple_fusion: {
    cards_required: 2,
    common: true,
    example: "Character + Activity → Personalized Activity"
  };
  
  complex_fusion: {
    cards_required: 3,
    uncommon: true,
    example: "Character + Activity + Emotion → Colored Memory"
  };
  
  chain_fusion: {
    cards_required: "evolved_card + new_card",
    creates_progression: true,
    example: "Coffee Ritual + Crisis → Support System"
  };
  
  legendary_fusion: {
    cards_required: "specific_sequence",
    very_rare: true,
    example: "5-card sequence → Legendary Memory"
  };
  
  conditional_fusion: {
    cards_required: "cards + context",
    context_dependent: true,
    example: "Character + Location + Seasonal Event"
  };
}
```

---

## Master Truths v1.2: Emotional Authenticity in Fusions *(NEW)*

### Capacity-Aware Fusion Validation

Fusions now check emotional capacity before allowing combination:

```javascript
const CAPACITY_AWARE_FUSION = {
  // EXAMPLE: Supporting friend through crisis requires capacity
  fusion_attempt: {
    cards: ["Sarah (Level 3)", "Support During Crisis"],
    player_capacity: 3.5,              // Current capacity (0-10 scale)
    
    fusion_requirements: {
      min_capacity: 5.0,                // Need 5.0+ to provide real support
      capacity_consumed: 2.5             // Will reduce capacity by 2.5
    },
    
    validation_result: "BLOCKED - Insufficient capacity",
    
    narrative: `
      Sarah needs you. But you're barely holding it together yourself. 
      You can't give what you don't have right now.
    `,
    
    alternatives: [
      {
        option: "Limited Support",
        min_capacity: 2.0,
        narrative: "You show up, but you're not fully present. Sarah notices.",
        effects: {
          trust: +0.05,                 // Less effective
          sarah_capacity: +0.5,         // Barely helps
          guilt: +1                     // Feel bad for not doing more
        }
      },
      {
        option: "Ask for Help",
        min_capacity: 1.0,
        narrative: "You tell Sarah you can't be there alone. You call Marcus.",
        effects: {
          trust: +0.10,                 // Honesty appreciated
          marcus_relationship: +0.15,   // Marcus steps up
          three_way_support_network: true
        }
      }
    ]
  }
};
```

### Memory Resonance in Fusion Outcomes

Fusions consider past experiences, affecting emotional weight:

```javascript
const MEMORY_RESONANT_FUSION = {
  // EXAMPLE: Hospital visit triggers past trauma
  fusion: {
    cards: ["Visit Hospital", "Support Marcus After Accident"],
    
    player_memory_check: {
      has_hospital_trauma: true,        // Player has trauma memory
      trauma_type: "collapsed_at_work_hospitalized_week_8",
      resonance_weight: 0.75            // 25% penalty
    },
    
    fusion_outcome_modified: {
      base_narrative: "Visit Marcus at hospital. Be supportive friend.",
      
      trauma_modified_narrative: `
        The hospital. That smell. Fluorescent lights. You remember waking 
        up here after you collapsed. Marcus's scared face above you.
        
        Now you're here FOR Marcus. Full circle. You can do this. But it's hard.
      `,
      
      trauma_effects: {
        anxiety_triggered: "ANXIOUS state activates",
        comfort_zone_cost: +2,          // Extra courage required
        memory_weight: 9,               // Highly significant (trauma + support)
        emotional_growth_opportunity: true,
        
        success_modifier: -0.15,        // Harder to be fully present
        capacity_cost: +1.0             // Costs more emotionally
      },
      
      growth_callback: `
        IF player successfully supports Marcus despite trauma:
        - Overcome hospital fear (partial)
        - Gain confidence (+0.15)
        - Memory: "I was there for him, even though it was hard"
        - Future hospital visits: resonance_weight improves to 0.90
      `
    }
  }
};
```

### Circumstance Stacking Effects on Fusions

Multiple stressors compound, affecting fusion quality:

```javascript
const STACKING_FUSION_PENALTIES = {
  player_state: {
    active_stressors: [
      "work_deadline_looming",
      "physical_meter_low_2",
      "money_concerns",
      "family_conflict_unresolved"
    ],
    stressor_count: 4,
    stacking_penalty: -0.20            // 4 stressors = -20% fusion quality
  },
  
  fusion_attempt: {
    cards: ["Deep Conversation with Sarah", "Emotional Opening"],
    
    ideal_outcome: {
      trust: +0.15,
      vulnerability_shared: true,
      memory_weight: 8,
      narrative: "Meaningful conversation. Real connection."
    },
    
    stacking_modified_outcome: {
      trust: +0.08,                     // 47% less effective
      vulnerability_shared: "partial",
      memory_weight: 6,                 // Less significant
      
      narrative: `
        Coffee with Sarah. She's opening up, but you're distracted. Work 
        deadline tomorrow. Rent's due. Mom called again (you didn't answer).
        
        You try to focus on Sarah, but she can tell your mind is elsewhere.
        "Are you okay?" she asks. You say yes. But you're not.
      `,
      
      effects: {
        sarah_notices_distraction: true,
        opportunity_partially_missed: "Could have been a Level 3→4 moment",
        sarah_concerned: "Are you taking care of yourself?"
      }
    },
    
    design_note: "Circumstance stacking creates AUTHENTIC limitation - can't be fully present when overwhelmed"
  }
};
```

### Novel-Worthiness Flags

Fusions automatically flag content for Life Bookshelf generation:

```javascript
const NOVEL_WORTHY_DETECTION = {
  // Automatic flagging based on fusion characteristics
  
  fusion_analysis: {
    emotional_weight: 9,              // 0-10 scale (8+ = novel-worthy)
    relationship_significance: "high", // Major relationship moment
    breakthrough_moment: true,         // Breakthrough/crisis/celebration
    
    // NOVEL-WORTHINESS FLAGS (NEW - v1.2)
    novel_worthy: true,               // Include in Life Bookshelf
    chapter_priority: "high",         // Featured prominently
    narrative_weight: 0.92,           // 0.0-1.0 quality score
    
    quality_metrics: {
      authenticity: 0.88,             // ≥ 0.7 required
      tension: 0.75,                  // ≥ 0.6 required
      hooks: 0.80,                    // ≥ 0.6 required
      overall: 0.81                   // ≥ 0.7 required
    }
  },
  
  flagging_criteria: {
    // Automatically flagged as novel-worthy if ANY:
    emotional_weight_8_plus: true,              // Weight ≥ 8
    breakthrough_or_crisis: true,               // Major moment type
    relationship_level_up: true,                // Level 3→4, 4→5
    legendary_fusion_step: true,                // Part of legendary sequence
    permanent_life_change: true,                // Job change, move, etc.
    
    // Quality thresholds must ALSO pass:
    authenticity_minimum: 0.7,
    tension_minimum: 0.6,
    hooks_minimum: 0.6,
    overall_minimum: 0.7
  },
  
  examples: {
    novel_worthy_fusion: {
      name: "Marcus Saved My Life (Hospital Crisis)",
      emotional_weight: 10,
      novel_worthy: true,
      chapter_priority: "climax",     // Major story beat
      narrative_weight: 0.95,
      tags: ["crisis", "support", "friendship", "vulnerability"],
      
      novel_chapter_excerpt: `
        "I collapsed during the wedding shoot. The floor rushing up. 
        Marcus's terrified face above me in the ER..."
      `
    },
    
    not_novel_worthy_fusion: {
      name: "Coffee with Sarah (Routine)",
      emotional_weight: 5,            // Below threshold
      novel_worthy: false,            // Not included in novel
      narrative_weight: 0.65,         // Authentic but routine
      
      note: "Pleasant moments matter for gameplay but don't all need novel chapters"
    }
  }
};
```

### Tension Injection Through Fusion

Fusions create narrative hooks based on relationship level:

```javascript
const TENSION_INJECTION_FUSIONS = {
  // Level 3 Friend: 50% chance of tension element
  fusion_with_tension: {
    cards: ["Coffee with Sarah (Level 3)", "Weekly Ritual"],
    tension_roll: 0.48,                 // Rolled < 0.50, tension triggers
    
    baseline_fusion: "Comfortable coffee ritual. Pleasant conversation.",
    
    tension_injected_fusion: {
      type: "mystery_hook",
      
      narrative: `
        Tuesday coffee. Sarah seems... different. Distracted. Keeps checking 
        her phone. "Everything okay?" you ask.
        
        "Yeah, just... something I need to figure out. I'll tell you soon, 
        I promise." She forces a smile.
        
        You notice her hands are shaking slightly.
      `,
      
      creates_question: "What's going on with Sarah?",
      foreshadowing: "Anniversary of David's death approaching (2 weeks)",
      
      future_impact: "Sets up vulnerability moment for Level 3→4 evolution"
    }
  },
  
  // Level 5 Best Friend: Nearly every interaction has layers
  level_5_tension: {
    cards: ["Sarah (Level 5)", "Regular Check-in"],
    tension_frequency: 0.85,            // 85% chance at Level 5
    
    fusion_with_complexity: {
      narrative: `
        Sarah at the bookshop. Business is struggling—down 30% this quarter. 
        She hasn't told you how bad it is, but you can see it in the numbers.
        
        "We'll figure it out," she says. But you're both co-owners. If the 
        bookshop fails, you both lose your investment. That's $20,000 for you.
        $23,000 for her (everything she had).
        
        Stakes are real. Best friend or not.
      `,
      
      tension_types: ["stakes_escalation", "dramatic_irony"],
      
      player_knowledge: "You know the financials are bad",
      sarah_knowledge: "She doesn't know YOU know",
      
      creates_decision: "Do you bring it up? Let her tell you when ready?"
    }
  }
};
```

---

## SIMPLE FUSIONS (2 Cards)

### Character + Activity Fusions

**Most Common Fusion Type**

```javascript
const CHARACTER_ACTIVITY_FUSION = {
  formula: "Character Card + Activity Card = Memory-Infused Character Card",
  
  requirements: {
    character_level: { min: 1 },       // Must have met character
    activity_compatible: true,         // Activity fits character personality
    resources_available: true          // Player can afford activity
  },
  
  example_fusion_tree: {
    level_1_stranger: {
      base_cards: ["Sarah Anderson (Level 1)", "Coffee Meetup"],
      
      fusion_result: {
        name: "Coffee with Sarah",
        tier: 4,
        category: "social_activity",
        
        narrative: `
          Grab coffee with Sarah at Café Luna. She orders chai latte, extra foam.
          You're getting to know each other.
        `,
        
        costs: {
          time: 1.5,
          money: 12,
          energy: -1                     // Restores energy
        },
        
        effects: {
          relationship_sarah: { trust: +0.05, social_capital: +1 },
          emotional_meter: +1,
          social_meter: +1
        },
        
        memory_created: {
          title: "First real conversation with Sarah",
          emotional_weight: 4,
          contains: ["Sarah's love of books", "Shy smile", "Chai latte preference"]
        },
        
        unlocks: ["Ask Sarah about books", "Invite Sarah to gallery"]
      }
    },
    
    level_2_acquaintance: {
      fusion: "Coffee with Sarah + Tech Conference",
      
      result: {
        name: "Deep Conversation with Sarah",
        
        narrative: `
          Coffee with Sarah has evolved. You're past small talk now. Today she 
          shared her dream: opening a bookshop. You could see how much it means to her.
        `,
        
        effects: {
          relationship_sarah: { trust: +0.10, level_progress: 0.3 },
          emotional_weight: 6,
          vulnerability_unlocked: true
        },
        
        memory_created: {
          title: "Sarah's bookshop dream",
          significance: "major",
          future_impact: "Can support this aspiration"
        }
      }
    },
    
    level_3_friend: {
      fusion: "Deep Conversation + Crisis Support",
      
      result: {
        name: "Sarah - Crisis Support System",
        
        narrative: `
          Sarah called you at 2 AM. Panic attack. You drove across town. Sat with 
          her until dawn. She told you about David. You're one of the few who knows.
          
          This friendship is real now.
        `,
        
        effects: {
          relationship_sarah: { trust: +0.25, level: 4 },
          emotional_weight: 9,
          mutual_support_unlocked: true
        },
        
        permanent_bond: "Emergency support available",
        carries_across_seasons: true
      }
    }
  }
};
```

---

### Character + Location Fusions

```javascript
const CHARACTER_LOCATION_FUSION = {
  formula: "Character + Location = Personalized Place",
  
  example: {
    base_cards: ["Sarah (Level 3)", "Café Luna (20+ visits)"],
    
    fusion_result: {
      name: "Café Luna - Sarah's Corner",
      tier: 7,
      
      narrative: `
        Café Luna isn't just a café anymore. It's where you and Sarah have had 
        coffee 20+ times. The window seat is "yours." Maya the barista knows to 
        make two chai lattes when she sees you arrive.
        
        This place has history now.
      `,
      
      mechanical_benefits: {
        meeting_sarah_here: "+10% conversation quality",
        comfort_bonus: +2,
        routine_efficiency: "Saves 0.5 hours when meeting here",
        emotional_anchor: "Stable location during crisis"
      },
      
      unlocks: [
        "Introduce other friends here",
        "Work on projects here together",
        "This location features in novel chapters"
      ],
      
      memory_accumulation: {
        first_meeting: "Week 3",
        ritual_established: "Week 10",
        major_conversations: 8,
        crisis_support: 2,
        celebrations: 3
      }
    }
  }
};
```

---

### Activity + Emotion Fusions

```javascript
const ACTIVITY_EMOTION_FUSION = {
  formula: "Activity + Emotion = Colored Experience",
  
  examples: {
    photography_joy: {
      cards: ["Work on Portfolio", "JOYFUL state"],
      
      fusion: "Inspired Photography Session",
      
      effects: {
        skill_gain: "+50% bonus",
        portfolio_quality: "+1",
        aspiration_progress: "+10%",
        memory: "The day everything clicked"
      }
    },
    
    photography_anxiety: {
      cards: ["Work on Portfolio", "ANXIOUS state"],
      
      fusion: "Anxious Photography Session",
      
      effects: {
        skill_gain: "+0% (no progress)",
        frustration: +1,
        self_doubt: +0.1,
        memory: "Struggled with imposter syndrome"
      },
      
      can_trigger: "Crisis of confidence event"
    },
    
    exercise_melancholy: {
      cards: ["Evening Run", "MELANCHOLY state"],
      
      fusion: "Processing Run",
      
      effects: {
        physical: +1,
        emotional: +2,                   // Running helps process emotions
        clarity: "Gains perspective on problems",
        memory: "The run that helped me think"
      }
    }
  },
  
  design_principle: "Emotional state colors how activities are experienced and remembered"
};
```

---

## COMPLEX FUSIONS (3 Cards)

### Triple Card Combinations

```javascript
const COMPLEX_TRIPLE_FUSIONS = {
  character_activity_emotion: {
    formula: "Character + Activity + Emotion = Landmark Memory",
    
    example_perfect_day: {
      cards: ["Sarah (Level 3)", "Coffee at Café Luna", "JOYFUL"],
      
      fusion_result: {
        name: "Perfect Afternoon with Sarah",
        tier: 5,
        rarity: "uncommon",
        
        narrative: `
          Tuesday. 3 PM. Café Luna. Sarah.
          
          You don't remember what you talked about, exactly. Books, probably. 
          Her bookshop plans. Your photography. The usual.
          
          But you remember laughing. The way the light hit her face through the 
          window. How time stopped being a thing that mattered.
          
          Perfect afternoons don't announce themselves. You only realize it later.
        `,
        
        effects: {
          relationship_sarah: { trust: +0.15, emotional_bond: +0.2 },
          emotional_meter: +3,
          memory_weight: 8,
          happiness_boost: "Lasts 1 week"
        },
        
        creates: {
          new_card: "Recall Perfect Afternoon (Comfort Zone restore card)",
          tradition_strengthened: "Tuesday coffee ritual now sacred",
          novel_chapter_moment: true
        }
      }
    },
    
    example_crisis_support: {
      cards: ["Marcus (Level 4)", "Hospital Visit", "WORRIED"],
      
      fusion_result: {
        name: "Marcus at the Hospital",
        tier: 5,
        
        narrative: `
          You collapsed. You woke up to Marcus's face above you. He looked 
          terrified.
          
          "You scared the shit out of me," he said, voice shaking.
          
          He'd dropped everything. Driven you to the ER. Called Sarah. Stayed 
          until 3 AM even though he had work at 7.
          
          You realize: This man would do anything for you. And you would for him.
        `,
        
        effects: {
          relationship_marcus: { trust: 1.0, level: 5 },
          permanent_bond: "Best friend for life",
          emotional_weight: 10,
          creates_obligation: "You owe him everything"
        },
        
        unlocks: {
          emergency_support: "Marcus always available in crisis",
          reciprocal_support: "Your turn to be there for him"
        }
      }
    }
  },
  
  character_location_time: {
    formula: "Character + Location + Time = Ritual Formation",
    
    example: {
      cards: ["Sarah", "Café Luna", "Tuesday 3 PM (10+ times)"],
      
      fusion: "Sacred Tuesday Ritual",
      
      becomes: "Unbreakable routine with significant emotional weight"
    }
  }
};
```

---

## CHAIN FUSIONS (Evolved Card + New Card)

### Progressive Evolution Through Fusion

```javascript
const CHAIN_FUSION_SYSTEM = {
  principle: "Evolved cards can fuse with new cards to create deeper evolutions",
  
  photography_chain_example: {
    stage_1: {
      base: "Work on Portfolio",
      evolution: "After 10 uses → 'Portfolio Sessions (Your Style Emerging)'"
    },
    
    stage_2: {
      chain_fusion: "Portfolio Sessions + Creative Breakthrough Event",
      result: "Signature Style Portfolio Work",
      effects: {
        skill_bonus: "+30%",
        unlocks: "Professional tier work",
        portfolio_value: "+3"
      }
    },
    
    stage_3: {
      chain_fusion: "Signature Style Work + Gallery Owner NPC",
      result: "Gallery-Quality Portfolio Development",
      effects: {
        career_path_opens: "Professional photographer",
        unlocks_aspiration: "Gallery Showing"
      }
    },
    
    stage_4: {
      chain_fusion: "Gallery-Quality Work + First Gallery Show",
      result: "Recognized Artist",
      effects: {
        reputation: +5,
        professional_status: true,
        income_stream: "Art sales",
        life_direction_fulfilled: "Creative Fulfillment achieved"
      }
    }
  },
  
  relationship_chain_example: {
    stage_1: {
      fusion: "Sarah + Coffee → Coffee with Sarah"
    },
    
    stage_2: {
      fusion: "Coffee with Sarah (10x) → Our Tuesday Ritual"
    },
    
    stage_3: {
      fusion: "Tuesday Ritual + Vulnerability Moment → Deep Trust"
    },
    
    stage_4: {
      fusion: "Deep Trust + Crisis Support → Unbreakable Bond"
    },
    
    stage_5: {
      fusion: "Unbreakable Bond + Business Collaboration → Life Partners"
    }
  }
};
```

---

## LEGENDARY FUSIONS (Specific Sequences)

### Ultra-Rare Multi-Step Fusions

```javascript
const LEGENDARY_FUSIONS = {
  definition: "Specific sequence of fusions over extended time creating ultimate cards",
  
  rarity: "< 5% of players will complete",
  
  example_creative_fulfillment_legendary: {
    name: "CREATIVE LEGACY",
    requirements: {
      time: "minimum 100+ weeks",
      seasons: "spanning 3+ seasons",
      specific_sequence: true
    },
    
    fusion_sequence: [
      {
        step: 1,
        fusion: "Pursue Creative Fulfillment + Work on Art (50+ times)",
        result: "Dedicated Artist"
      },
      {
        step: 2,
        fusion: "Dedicated Artist + Creative Breakthrough",
        result: "Signature Style Developed"
      },
      {
        step: 3,
        fusion: "Signature Style + Gallery Showing",
        result: "Recognized Artist"
      },
      {
        step: 4,
        fusion: "Recognized Artist + Teaching Workshops",
        result: "Master Teaching Apprentices"
      },
      {
        step: 5,
        fusion: "Master + International Recognition",
        result: "CREATIVE LEGACY ACHIEVED",
        
        effects: {
          permanent_achievement: true,
          life_direction_mastery: "Creative Fulfillment 100%",
          unlocks: ["Mentor new artists", "Legacy building aspirations"],
          novel_significance: "Major life accomplishment chapter",
          carries_across_all_future_seasons: true
        }
      }
    ],
    
    legendary_card_benefits: {
      all_creative_activities: "+50% success",
      reputation_permanent: 10,
      income_stable: true,
      npc_recognition: "NPCs recognize your legendary status",
      new_npcs_attracted: "Aspiring artists seek you out"
    }
  },
  
  example_relationship_legendary: {
    name: "SOULMATE BOND",
    
    fusion_sequence: [
      "First Meeting → Acquaintance (6+ interactions)",
      "Acquaintance → Friend (16+ interactions, vulnerability shared)",
      "Friend → Close Friend (31+ interactions, crisis survived together)",
      "Close Friend → Best Friend (76+ interactions, years together)",
      "Best Friend + Life Partner Decision → SOULMATE BOND"
    ],
    
    legendary_effects: {
      relationship_level: 5,
      trust: 1.0,
      unbreakable: true,
      emergency_support: "Always available",
      life_integration: "Major life decisions always consider them",
      novel_co_protagonist: "They feature as co-protagonist in Life Bookshelf"
    }
  }
};
```

---

## CONDITIONAL FUSIONS (Context-Dependent)

### Fusions Requiring Specific Conditions

```javascript
const CONDITIONAL_FUSIONS = {
  seasonal_fusions: {
    formula: "Cards + Seasonal Context = Special Memory",
    
    examples: {
      winter_first_snow: {
        conditions: {
          cards: ["Character (Level 3+)", "Outdoor Activity"],
          season: "Winter",
          weather: "First snow of season"
        },
        
        fusion: "First Snow Memory",
        
        narrative: "The first snow. You and Sarah at the park. Magic in the ordinary.",
        
        effects: {
          emotional_weight: 8,
          seasonal_tradition_starts: "Becomes annual memory",
          carries_across_years: true
        }
      },
      
      anniversary_fusion: {
        conditions: {
          cards: ["Character", "Location"],
          trigger: "52 weeks since first meeting"
        },
        
        fusion: "Anniversary Reflection",
        
        narrative: "One year since you met Sarah at this café. Hard to imagine life without her now.",
        
        creates_new_card: "Annual Anniversary Tradition"
      }
    }
  },
  
  crisis_fusions: {
    formula: "Cards + Crisis Event = Transformative Memory",
    
    examples: {
      support_during_collapse: {
        conditions: {
          cards: ["Character (Level 3+)", "Crisis: Collapse"],
          player_state: "Vulnerable"
        },
        
        fusion: "[Character] Saved Me",
        
        permanent_bond: true,
        trust: "maxes out",
        novel_chapter_worthy: true
      }
    }
  },
  
  aspiration_fusions: {
    formula: "Cards + Aspiration Completion = Achievement Memory",
    
    examples: {
      business_launch_success: {
        conditions: {
          cards: ["Character (Supporter)", "Aspiration: Launch Business"],
          result: "Success"
        },
        
        fusion: "We Did It Together",
        
        creates: {
          permanent_partnership: true,
          business_co_founder: "Character becomes business partner",
          new_arc: "Shared business growth"
        }
      }
    }
  }
};
```

---

## Fusion Mechanics & Rules

### When Fusions Occur

```javascript
const FUSION_TRIGGERS = {
  automatic_fusions: {
    trigger: "Cards played together in same turn",
    requires_proximity: true,
    
    examples: [
      "Playing 'Coffee' then 'Sarah' in same afternoon → Auto-fuses",
      "Playing 'Run' while in MELANCHOLY state → Auto-fuses"
    ]
  },
  
  threshold_fusions: {
    trigger: "Repetition reaches threshold",
    
    examples: [
      "10th time playing 'Coffee with Sarah' → Ritual fusion",
      "50th visit to location → Landmark fusion"
    ]
  },
  
  event_triggered_fusions: {
    trigger: "Specific event occurs during card play",
    
    examples: [
      "Playing 'Sarah' when Crisis Event triggers → Crisis fusion",
      "Playing 'Work' during Breakthrough Event → Breakthrough fusion"
    ]
  }
};
```

---

### Fusion Memory & Persistence

```javascript
interface FusionMemory {
  fusion_id: string;
  origin_cards: string[];               // Cards that created fusion
  fusion_type: "simple" | "complex" | "chain" | "legendary" | "conditional";
  
  created_week: number;
  created_season: number;
  
  narrative_context: {
    player_emotional_state: string,
    active_aspiration: string,
    location: string,
    significant_events_nearby: string[]
  };
  
  emotional_weight: number;              // 0-10
  novel_significance: number;            // How much this features in generated novel
  
  carries_across_seasons: boolean;       // Most fusions persist Season 1 → Season 8
  
  evolution_history: {
    base_state: CardState,
    evolution_stages: EvolutionEvent[],
    current_state: CardState
  };
}
```

---

## Fusion Possibility Space

### Mathematical Combinations

```
BASE CARDS:                    ~480 cards
EVOLVED VARIATIONS:            ~10,000+ (AI-generated unique evolutions)
SIMPLE FUSIONS (2-card):       ~50,000 possible combinations
COMPLEX FUSIONS (3-card):      ~500,000 possible combinations
CHAIN FUSIONS:                 ~100,000 possible progressions
LEGENDARY FUSIONS:             ~50 ultra-rare achievements

TOTAL POSSIBILITY SPACE:       ~650,000+ unique fusions

PER PLAYTHROUGH REALITY:       ~500-1000 fusions created (0.15% of possibility space)
UNIQUENESS:                    Every player deck is entirely unique
```

---

## Fusion Balance & Design

### Design Principles

```javascript
const FUSION_DESIGN_PRINCIPLES = {
  earned_not_random: {
    principle: "Fusions require player action, not RNG",
    implementation: "Specific cards + specific context = predictable fusion"
  },
  
  memorable_not_mechanical: {
    principle: "Fusions create story moments, not just stat bonuses",
    implementation: "Each fusion has narrative weight and novel significance"
  },
  
  permanent_not_reversible: {
    principle: "Fusions are commitments (like life choices)",
    implementation: "Cannot undo fusions - they're part of your story"
  },
  
  personal_not_generic: {
    principle: "Your fusions are unique to your playthrough",
    implementation: "AI generates personalized narratives for each fusion"
  },
  
  cumulative_not_isolated: {
    principle: "Fusions build on each other across seasons",
    implementation: "Chain fusions create progression over 8-10 seasons"
  }
};
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
- ✅ Capacity-aware fusion validation (blocks fusions when capacity too low)
- ✅ Memory resonance in fusion outcomes (trauma/growth callbacks)
- ✅ Circumstance stacking effects (-20% fusion quality when overwhelmed)
- ✅ Tension injection through fusions (mystery hooks, stakes, dramatic irony)
- ✅ Alternatives offered when capacity insufficient

**References:**
- See `20-base-card-catalog.md` for all cards that can fuse
- See `21-card-evolution-mechanics.md` for how cards evolve before fusing
- See `13-meter-effects-tables.md` for emotional capacity calculations
- See `14-emotional-state-mechanics.md` for emotional state effects
- See `01-emotional-authenticity.md` for v1.2 authenticity systems

---

**This specification enables developers to implement the complete card fusion system with simple/complex/chain/legendary fusions, capacity-aware validation, memory resonance, circumstance stacking, tension injection, and memory persistence that creates emotionally authentic, novel-worthy player stories across multiple seasons.**

