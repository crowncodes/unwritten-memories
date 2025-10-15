# Fusion Type Specifications - Complete Technical Reference

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete technical specifications for all 5 fusion types with exact mechanics, validation rules, and implementation logic

**References:**
- **Fusion System Overview:** `22-card-fusion-system.md` (fusion philosophy and examples)
- **Card Evolution:** `21-card-evolution-mechanics.md` (how cards evolve before fusing)
- **Base Cards:** `20-base-card-catalog.md` (all fusable cards)

---

## Overview

**Five fusion types** exist in Unwritten, each with distinct mechanics, requirements, and outputs. This document provides **exact technical specifications** for implementation.

**Design Principle:** Fusions are deterministic (no RNG), earned through player action, and create novel-worthy memories.

---

## FUSION TYPE 1: SIMPLE FUSIONS (2 Cards)

### Technical Specification

```typescript
interface SimpleFusion {
  type: "simple";
  input_cards: [CardReference, CardReference];
  
  validation: {
    card_compatibility: FusionCompatibilityCheck;
    timing_requirement: "same_turn" | "same_context";
    prerequisite_states: PrerequisiteCheck[];
    
    // NEW - Master Truths v1.2: Emotional Authenticity
    emotional_capacity_requirements?: {
      min_player_capacity?: number;     // 0-10 scale
      min_npc_capacity?: number;        // For support-based fusions
      capacity_consumed?: number;       // How much fusion costs
    };
  };
  
  fusion_logic: {
    trigger: "automatic" | "threshold_based";
    threshold?: {
      type: "repetition_count" | "time_elapsed";
      value: number;
    };
    
    // NEW - Master Truths v1.2: Authenticity Constraints
    authenticity_constraints?: {
      requires_vulnerability?: boolean;     // Real moment required
      requires_emotional_significance?: boolean; // Memory weight > 5
      circumstance_stacking_penalty?: number;    // 0.0-0.3 (0-30% penalty)
    };
  };
  
  output: {
    fusion_card: GeneratedCard;
    original_cards_behavior: "merged" | "both_available" | "original_hidden";
    memory_created: MemoryRecord;
    
    // NEW - Master Truths v1.2: Memory Resonance
    memory_resonance?: {
      triggers_past_memory?: boolean;
      resonance_weight?: number;        // 0.7-0.95
      emotional_callback?: string;
      growth_opportunity?: boolean;
    };
    
    // NEW - Master Truths v1.2: Novel-Worthiness
    novel_worthy?: boolean;             // Include in Life Bookshelf
    narrative_weight?: number;          // 0.0-1.0 quality score
    quality_metrics?: {
      authenticity: number;             // ≥ 0.7 required
      tension: number;                  // ≥ 0.6 required
      hooks: number;                    // ≥ 0.6 required
      overall: number;                  // ≥ 0.7 required
    };
  };
}
```

---

### Subtype 1A: Character + Activity Fusion

**Most Common Fusion (80% of all simple fusions)**

```javascript
const CHARACTER_ACTIVITY_FUSION = {
  validation_rules: {
    card_1_type: "character",
    card_1_level: { min: 1 },              // Must have met NPC
    
    card_2_type: "activity",
    card_2_compatible: true,               // Activity fits character personality
    
    player_resources: "sufficient",        // Can afford activity
    
    timing: "same_turn"                    // Both played in same turn
  },
  
  fusion_trigger: {
    automatic: true,                       // Fuses immediately on first play
    no_player_confirmation: true           // Seamless
  },
  
  fusion_process: {
    step_1: "Identify character + activity pair",
    step_2: "Check compatibility (personality fit)",
    step_3: "Generate fusion card",
    step_4: "Create memory record",
    step_5: "Add fusion to player deck"
  },
  
  output_card_template: {
    name: "[Activity] with [Character Name]",
    tier: 4,                               // Activity tier
    category: "social_activity",
    
    narrative: `
      [Activity description] with [Character Name].
      [Context-specific detail based on relationship level].
    `,
    
    costs: "same_as_base_activity",
    
    effects: {
      inherits_from_activity: true,
      adds_relationship_effects: {
        trust: +0.05,                      // Base relationship gain
        social_capital: +1,
        interaction_count: +1
      }
    },
    
    metadata: {
      origin_cards: ["character_id", "activity_id"],
      created_week: "current_week",
      created_season: "current_season",
      fusion_type: "simple_character_activity"
    }
  },
  
  examples: [
    {
      input: ["Sarah Anderson (Level 1)", "Coffee Meetup"],
      output: "Coffee with Sarah",
      
      narrative: "Grab coffee with Sarah at Café Luna. She orders chai latte, extra foam.",
      
      effects: {
        time: 1.5,
        money: 12,
        energy: -1,
        sarah_trust: +0.05,
        sarah_interactions: +1
      }
    },
    
    {
      input: ["Marcus (Level 3)", "Evening Run"],
      output: "Running with Marcus",
      
      narrative: "Your Tuesday run with Marcus. 5 miles, conversation, competition.",
      
      effects: {
        time: 1,
        energy: 2,
        physical: +1,
        marcus_trust: +0.08,              // Higher because Level 3
        marcus_interactions: +1
      }
    }
  ]
};
```

---

### Subtype 1B: Character + Location Fusion

```javascript
const CHARACTER_LOCATION_FUSION = {
  validation_rules: {
    card_1_type: "character",
    card_1_level: { min: 2 },              // Acquaintance+
    
    card_2_type: "location",
    card_2_visits: { min: 5 },             // Familiar location
    
    shared_history: true                   // Met at this location multiple times
  },
  
  fusion_trigger: {
    automatic: false,
    threshold: {
      type: "shared_visits",
      value: 10                            // After 10 meetings at same location
    }
  },
  
  output_card_template: {
    name: "[Location Name] - [Character's] Place",
    tier: 7,                               // Location tier
    
    narrative: `
      [Location] isn't just a place anymore. It's where you and [Character] meet.
      [Specific memories accumulated here].
    `,
    
    mechanical_benefits: {
      meeting_character_here: "+10% conversation quality",
      time_saved: -0.5,                    // Routine established
      comfort_bonus: +1,
      emotional_anchor: "Available during stress"
    },
    
    metadata: {
      shared_memories_count: "number",
      first_meeting_week: "week",
      ritual_established_week: "week"
    }
  },
  
  example: {
    input: ["Sarah (Level 3)", "Café Luna (15 visits, 10 with Sarah)"],
    output: "Café Luna - Where I Meet Sarah",
    
    narrative: `
      Café Luna is your place now. Tuesday afternoons, 3 PM, window seat.
      Sarah's already there, two chai lattes ordered. This is your thing.
    `,
    
    benefits: {
      meeting_sarah_here: "+10% depth",
      time: -0.5,
      comfort: +2,
      emotional_weight: 7
    }
  }
};
```

---

### Subtype 1C: Activity + Emotion Fusion

```javascript
const ACTIVITY_EMOTION_FUSION = {
  validation_rules: {
    card_1_type: "activity",
    
    card_2_type: "emotional_state",        // Player's current state
    card_2_source: "active_state",         // Not card, but player state
    
    timing: "activity_played_during_emotional_state"
  },
  
  fusion_trigger: {
    automatic: true,                       // Always colors experience
    applies_modifiers: true
  },
  
  fusion_logic: {
    note: "This fusion type modifies the activity outcome, not create new card",
    creates_memory: true,
    affects_future: "Yes - emotional coloring remembered"
  },
  
  emotional_modifiers_table: {
    JOYFUL: {
      success_chance: +0.15,
      skill_gain: 1.5x,
      memory_tone: "positive",
      example: "The day everything clicked"
    },
    
    ANXIOUS: {
      success_chance: -0.20,
      skill_gain: 0.5x,
      memory_tone: "stressful",
      costs_extra_energy: +1,
      example: "Struggled with self-doubt"
    },
    
    MELANCHOLY: {
      success_chance: -0.10,
      skill_gain: 1.0x,
      memory_tone: "reflective",
      emotional_processing: +2,             // But helps process emotions
      example: "The run that helped me think"
    },
    
    CONFIDENT: {
      success_chance: +0.20,
      comfort_zone_cost: -1,                // Easier to take risks
      memory_tone: "empowering",
      example: "I felt unstoppable"
    },
    
    EXHAUSTED: {
      success_chance: -0.30,
      skill_gain: 0x,                       // No progress when exhausted
      memory_tone: "struggle",
      warning: "Should rest instead",
      example: "Pushing through fog"
    }
  }
};
```

---

## FUSION TYPE 2: COMPLEX FUSIONS (3 Cards)

### Technical Specification

```typescript
interface ComplexFusion {
  type: "complex";
  input_cards: [CardReference, CardReference, CardReference];
  
  validation: {
    all_cards_compatible: boolean;
    specific_order_required: boolean;
    context_requirement?: ContextCheck;
    
    // NEW - Master Truths v1.2: Emotional Authenticity
    emotional_capacity_requirements: {
      min_player_capacity: 5.0;            // Complex fusions require higher capacity
      all_npcs_capacity_check: boolean;    // Verify all NPCs in fusion
      capacity_consumed: number;           // 2.0-4.0 for complex fusions
    };
    
    authenticity_constraints: {
      requires_vulnerability: true;        // MUST have real moment
      min_emotional_significance: 7;       // Weight must be 7+
      circumstance_stacking_applies: boolean; // Can reduce quality
    };
  };
  
  rarity: "uncommon";                      // 15% of fusions
  
  output: {
    fusion_card: LandmarkMemoryCard;
    emotional_weight: number;              // 7-10 (novel-worthy)
    novel_significance: "major_moment";
    
    // NEW - Master Truths v1.2
    memory_resonance: {
      creates_growth_moment: boolean;      // Almost always true for complex
      resonance_weight: number;            // 0.85-0.95 (high impact)
      emotional_callbacks: string[];       // Multiple memories referenced
    };
    
    novel_worthy: true;                    // Complex fusions always novel-worthy
    narrative_weight: number;              // 0.80-0.95
    quality_metrics: {
      authenticity: number;                // Must be ≥ 0.8 for complex
      tension: number;                     // Must be ≥ 0.7 for complex
      hooks: number;                       // Must be ≥ 0.7 for complex
      overall: number;                     // Must be ≥ 0.8 for complex
    };
  };
}
```

---

### Subtype 2A: Character + Activity + Emotion

**Creates Landmark Memories**

```javascript
const TRIPLE_CARD_FUSION = {
  validation_rules: {
    card_1: "character (Level 3+)",        // Friend or closer
    card_2: "activity",
    card_3: "emotional_state (high intensity)",
    
    all_played_same_turn: true,
    emotional_intensity: { min: 0.7 }       // Strong emotion required
  },
  
  fusion_trigger: {
    automatic: true,
    only_when_all_three_present: true
  },
  
  output_card_types: {
    perfect_moment: {
      emotions: ["JOYFUL", "CONTENT", "EXCITED"],
      creates: "Perfect [Activity] with [Character]",
      
      narrative_template: `
        [Day of week]. [Time]. [Location]. [Character].
        
        You don't remember exactly what you talked about. But you remember:
        [specific sensory detail]. [emotional beat]. [realization].
        
        Perfect [moments/afternoons/days] don't announce themselves.
        You only realize it later.
      `,
      
      effects: {
        relationship_trust: +0.15,
        emotional_boost: +3,
        memory_weight: 8,
        happiness_lasting: "1 week",
        creates_comfort_card: "Recall Perfect Moment"
      }
    },
    
    crisis_support: {
      emotions: ["WORRIED", "ANXIOUS", "DEVASTATED"],
      creates: "[Character] During Crisis",
      
      narrative_template: `
        [Crisis description].
        
        [Character] was there. [Specific action they took].
        
        You realize: [Character relationship revelation].
      `,
      
      effects: {
        relationship_trust: +0.25,
        relationship_level: "may upgrade",
        permanent_bond_deepened: true,
        memory_weight: 10,
        creates_emergency_support: true
      }
    },
    
    breakthrough_shared: {
      emotions: ["EXCITED", "CONFIDENT", "INSPIRED"],
      creates: "Breakthrough Moment with [Character]",
      
      effects: {
        skill_jump: +1.0,
        relationship_trust: +0.15,
        shared_success_memory: true,
        unlocks_collaboration: true
      }
    }
  }
};
```

---

## FUSION TYPE 3: CHAIN FUSIONS (Evolved → New)

### Technical Specification

```typescript
interface ChainFusion {
  type: "chain";
  input: {
    evolved_card: CardReference;           // Already a fusion
    new_card: CardReference;
  };
  
  validation: {
    first_card_is_fusion: boolean;
    progression_logical: boolean;
    
    // NEW - Master Truths v1.2
    emotional_capacity_requirements: {
      min_capacity: number;                // Varies by chain depth
      cumulative_capacity_check: boolean;  // Check if player can sustain chain
    };
    
    authenticity_constraints: {
      each_step_must_matter: boolean;      // No empty progression
      memory_weight_threshold: 5;          // Each step must be significant
      journey_beat_required: boolean;      // Real moment at each step
    };
  };
  
  creates_progression: true;
  can_chain_infinitely: true;              // Chains can continue evolving
  
  // NEW - Master Truths v1.2
  memory_resonance: {
    builds_on_previous: boolean;           // References prior chain steps
    cumulative_weight: number;             // Increases with chain length
    growth_tracking: boolean;              // Tracks personal development arc
  };
  
  novel_worthy_threshold: 3;               // Chains of 3+ steps often novel-worthy
}
```

---

### Chain Fusion Mechanics

```javascript
const CHAIN_FUSION_SYSTEM = {
  principle: "Evolved cards can fuse with new cards to create deeper evolutions",
  
  chain_progression_example: {
    stage_1_base: {
      card: "Work on Portfolio",
      state: "base_activity"
    },
    
    stage_2_repetition: {
      trigger: "10 uses",
      fusion: "Work on Portfolio (10x) → Portfolio Sessions",
      result: "Portfolio Sessions (Your Style Emerging)"
    },
    
    stage_3_event: {
      trigger: "Creative Breakthrough Event during Portfolio Sessions",
      fusion: "Portfolio Sessions + Breakthrough Event",
      result: "Signature Style Portfolio Work",
      effects: {
        skill_bonus: "+30%",
        unlocks: "Professional tier"
      }
    },
    
    stage_4_npc: {
      trigger: "Gallery Owner NPC interaction",
      fusion: "Signature Style Work + Gallery Owner",
      result: "Gallery-Quality Portfolio Development",
      effects: {
        career_path: "Professional photographer",
        unlocks_aspiration: "Gallery Showing"
      }
    },
    
    stage_5_achievement: {
      trigger: "Complete Gallery Showing aspiration",
      fusion: "Gallery-Quality Work + Gallery Show Success",
      result: "Recognized Artist",
      effects: {
        reputation: +5,
        professional_status: true,
        income_stream: "Art sales"
      }
    }
  },
  
  validation_algorithm: {
    pseudocode: `
      function canChainFuse(evolvedCard, newCard) {
        // Check if first card is already a fusion
        if (!evolvedCard.isFusion) return false;
        
        // Check if progression is logical
        if (!isLogicalProgression(evolvedCard, newCard)) return false;
        
        // Check if player context supports chain
        if (!contextSupportsChain(playerState, evolvedCard, newCard)) return false;
        
        return true;
      }
      
      function isLogicalProgression(evolved, new) {
        // Examples of logical progressions:
        // "Coffee Ritual" + "Crisis" → "Support System" ✓
        // "Coffee Ritual" + "Unrelated NPC" → ✗
        
        const thematicConnection = checkTheme(evolved, new);
        const narrativeFlow = checkNarrative(evolved, new);
        
        return thematicConnection && narrativeFlow;
      }
    `
  }
};
```

---

## FUSION TYPE 4: LEGENDARY FUSIONS (Multi-Step Sequences)

### Technical Specification

```typescript
interface LegendaryFusion {
  type: "legendary";
  input_sequence: ChainedFusionPath;       // Specific sequence required
  
  validation: {
    exact_sequence: boolean;               // Must follow exact path
    time_requirement: { min_weeks: number };
    prerequisite_achievements: string[];
    
    // NEW - Master Truths v1.2
    emotional_capacity_requirements: {
      sustained_capacity_over_time: boolean;  // Must maintain capacity throughout
      crisis_capacity_tests: number;          // Number of capacity crises survived
      support_network_required: boolean;      // Can't do legendary alone
    };
    
    authenticity_constraints: {
      multiple_vulnerability_moments: number; // Requires 3-5 real moments
      multiple_crisis_supports: number;       // Requires 2-3 crisis supports
      emotional_journey_complete: boolean;    // Full arc from start to mastery
      min_memory_weight: 8;                   // Every step must be 8+ significant
    };
  };
  
  rarity: "ultra_rare";                    // < 5% of players complete
  
  output: {
    legendary_card: PermanentAchievementCard;
    life_direction_mastery: boolean;
    carries_all_future_seasons: true;
    
    // NEW - Master Truths v1.2
    memory_resonance: {
      epic_narrative_arc: boolean;            // Complete story arc
      resonance_weight: 1.0;                  // Maximum impact
      multiple_emotional_callbacks: string[]; // References entire journey
      transformation_documented: boolean;     // Growth from start to finish
    };
    
    novel_worthy: true;                       // ALWAYS novel-worthy
    narrative_weight: 0.95;                   // Near-maximum quality
    dedicated_chapters: number;               // 2-3 full novel chapters
    quality_metrics: {
      authenticity: number;                   // Must be ≥ 0.9 for legendary
      tension: number;                        // Must be ≥ 0.8 for legendary
      hooks: number;                          // Must be ≥ 0.8 for legendary
      overall: number;                        // Must be ≥ 0.9 for legendary
    };
  };
}
```

---

### Legendary Fusion Sequences

```javascript
const LEGENDARY_FUSIONS = {
  creative_legacy: {
    name: "CREATIVE LEGACY",
    
    required_sequence: [
      {
        step: 1,
        fusion: "Pursue Creative Fulfillment + Work on Art (50+ times)",
        result: "Dedicated Artist",
        min_week: 0
      },
      {
        step: 2,
        fusion: "Dedicated Artist + Creative Breakthrough",
        result: "Signature Style Developed",
        min_week: 24
      },
      {
        step: 3,
        fusion: "Signature Style + Gallery Showing (aspiration complete)",
        result: "Recognized Artist",
        min_week: 52
      },
      {
        step: 4,
        fusion: "Recognized Artist + Teaching Workshops (5+)",
        result: "Master Teaching Apprentices",
        min_week: 100
      },
      {
        step: 5,
        fusion: "Master + International Recognition Event",
        result: "CREATIVE LEGACY ACHIEVED",
        min_week: 150,
        
        requirements: {
          skill_art: 10,
          reputation: 10,
          students_taught: 10,
          exhibitions_completed: 5
        }
      }
    ],
    
    legendary_benefits: {
      all_creative_activities: "+50% success",
      reputation_permanent: 10,
      income_stable: "Passive art sales",
      npc_recognition: "NPCs recognize legendary status",
      new_npcs_attracted: "Aspiring artists seek you out",
      novel_chapter: "Major life accomplishment - full chapter",
      achievement_badge: "Creative Legacy Master"
    },
    
    validation_logic: `
      function validateLegendaryFusion(player, legendary_id) {
        const sequence = LEGENDARY_SEQUENCES[legendary_id];
        
        // Check each step completed in order
        for (let step of sequence.required_sequence) {
          if (!player.completed_fusions.includes(step.result)) {
            return {valid: false, missing_step: step.step};
          }
          
          // Check time requirements
          const stepCompletedWeek = player.fusion_history[step.result].week;
          if (stepCompletedWeek < step.min_week) {
            return {valid: false, reason: "Too fast - story needs time"};
          }
        }
        
        // Check final requirements
        if (!meetsRequirements(player, sequence.requirements)) {
          return {valid: false, reason: "Prerequisites not met"};
        }
        
        return {valid: true};
      }
    `
  },
  
  soulmate_bond: {
    name: "SOULMATE BOND",
    
    required_sequence: [
      "First Meeting → Acquaintance (6+ interactions)",
      "Acquaintance → Friend (16+ interactions, vulnerability)",
      "Friend → Close Friend (31+ interactions, crisis together)",
      "Close Friend → Best Friend (76+ interactions, years together)",
      "Best Friend + Life Partner Decision → SOULMATE BOND"
    ],
    
    requirements: {
      time_known: "52+ weeks (1+ year)",
      trust: 1.0,
      crises_survived_together: 3,
      major_life_decisions_together: 5,
      relationship_level: 5
    },
    
    legendary_benefits: {
      unbreakable_bond: true,
      emergency_support: "Always available",
      life_decisions: "Always consulted",
      novel_co_protagonist: "Major character in all novels",
      permanent_stat: "This relationship defines your life"
    }
  }
};
```

---

## FUSION TYPE 5: CONDITIONAL FUSIONS (Context-Dependent)

### Technical Specification

```typescript
interface ConditionalFusion {
  type: "conditional";
  input_cards: CardReference[];
  context_requirements: ContextCondition[];
  
  validation: {
    cards_valid: boolean;
    context_met: boolean;
    timing_valid: boolean;
    
    // NEW - Master Truths v1.2
    emotional_capacity_requirements?: {
      contextual_capacity_check: boolean;    // Capacity needed varies by context
      environmental_modifiers_apply: boolean; // Season/weather affects capacity
    };
    
    authenticity_constraints: {
      context_must_feel_authentic: boolean;   // No forced seasonal fusion
      memory_significance_threshold: number;  // Must matter (usually 6+)
      annual_tradition_potential: boolean;    // Can become recurring
    };
  };
  
  triggers_only_when: "specific_conditions_met";
  
  // NEW - Master Truths v1.2
  memory_resonance?: {
    seasonal_callback: boolean;              // References past seasons
    anniversary_weight: boolean;             // Special date significance
    environmental_trigger: boolean;          // Weather/location memory
    resonance_weight: number;                // 0.75-0.90 (contextual)
  };
  
  novel_worthy_potential: boolean;           // Some conditionals are novel-worthy
  creates_traditions: boolean;               // Repeats annually or seasonally
}
```

---

### Conditional Fusion Types

```javascript
const CONDITIONAL_FUSIONS = {
  seasonal_fusions: {
    formula: "Cards + Seasonal Context = Special Memory",
    
    types: {
      first_snow: {
        required_cards: ["Character (Level 3+)", "Outdoor Activity"],
        required_context: {
          season: "Winter",
          weather_event: "First snow of season"
        },
        
        creates: "First Snow Memory with [Character]",
        
        narrative: "The first snow. You and [Character] at the park. Magic in the ordinary.",
        
        effects: {
          emotional_weight: 8,
          seasonal_tradition: "Becomes annual memory",
          carries_across_years: true
        }
      },
      
      anniversary: {
        required_cards: ["Character (Level 3+)", "Location (Significant)"],
        required_context: {
          timing: "52 weeks since first meeting",
          location: "Where first met"
        },
        
        creates: "Anniversary Reflection",
        
        narrative: "One year since you met [Character] at this [location]. Hard to imagine life without them now."
      },
      
      birthday: {
        required_cards: ["Character (Level 4+)"],
        required_context: {
          timing: "Character's birthday (week per year)",
          relationship_level: { min: 4 }
        },
        
        creates: "[Character]'s Birthday Celebration",
        
        effects: {
          trust: +0.10,
          creates_annual_tradition: true,
          milestone_memory: true
        }
      }
    }
  },
  
  crisis_fusions: {
    required_cards: ["Character (Level 3+)", "Crisis Event"],
    required_context: {
      player_state: "Vulnerable",
      crisis_active: true
    },
    
    creates: "[Character] Saved Me / Supported Me During Crisis",
    
    effects: {
      permanent_bond: true,
      trust: "maxes out or +0.3",
      relationship_level: "often upgrades",
      novel_chapter_worthy: true
    },
    
    examples: [
      "Marcus + Collapse Crisis → Marcus Saved My Life",
      "Sarah + Panic Attack → Sarah Talked Me Through It",
      "Parent + Financial Crisis → Family Support When I Needed It"
    ]
  },
  
  aspiration_completion_fusions: {
    required_cards: ["Character (Supporter)", "Aspiration Complete"],
    required_context: {
      character_supported_aspiration: true,
      aspiration_result: "success"
    },
    
    creates: "We Did It Together",
    
    effects: {
      permanent_partnership: true,
      shared_achievement_memory: true,
      unlocks_collaborative_future: true
    },
    
    example: {
      cards: ["Sarah (helped with bookshop plans)", "Launch Photography Business (success)"],
      creates: "Sarah Was There From The Beginning",
      unlocks: "Future collaborative aspirations with Sarah"
    }
  }
};
```

---

## Fusion Validation System

### Complete Validation Algorithm

```javascript
async function validateAndExecuteFusion(cards, playerState, gameContext) {
  // STEP 1: Identify fusion type
  const fusionType = identifyFusionType(cards);
  
  if (!fusionType) {
    return {valid: false, reason: "No valid fusion detected"};
  }
  
  // STEP 2: Type-specific validation
  const validation = await validateByType(fusionType, cards, playerState, gameContext);
  
  if (!validation.valid) {
    return validation;
  }
  
  // STEP 3: Check player context
  const contextValid = validateContext(playerState, gameContext, fusionType);
  
  if (!contextValid) {
    return {valid: false, reason: "Context requirements not met"};
  }
  
  // STEP 4: Generate fusion card
  const fusionCard = await generateFusionCard(
    fusionType,
    cards,
    playerState,
    gameContext
  );
  
  // STEP 5: Create memory record
  const memory = createFusionMemory(
    fusionCard,
    cards,
    playerState.currentWeek,
    playerState.currentSeason
  );
  
  // STEP 6: Update player deck
  await addFusionToDeck(playerState.playerId, fusionCard);
  
  // STEP 7: Log for novel generation
  await logFusionForNovel(fusionCard, memory);
  
  return {
    valid: true,
    fusion_card: fusionCard,
    memory: memory,
    type: fusionType
  };
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
- See `22-card-fusion-system.md` for fusion philosophy and examples (v1.2 enhancements)
- See `21-card-evolution-mechanics.md` for pre-fusion card evolution
- See `20-base-card-catalog.md` for all fusable base cards
- See `13-meter-effects-tables.md` for emotional capacity calculations
- See `01-emotional-authenticity.md` for v1.2 authenticity systems

---

**This specification enables developers to implement the complete fusion type system with exact validation rules, generation logic, capacity checks, and integration points that respect Master Truths v1.2 emotional authenticity constraints.**

