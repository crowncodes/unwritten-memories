# Narrative Arc Scaffolding - Implementation Specification

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete 3-act structure implementation for seasons with exact timing, event sequencing, and emotional journey mapping

**References:**
- **Design Philosophy:** `1.concept/15-progression-phases.md` (WHY 3-act structure)
- **Schema Definition:** `7.schema/05-narrative-system.md` (Arc interfaces)
- **Season Structure:** `40-season-structure-spec.md` (12/24/36 week systems)
- **Decision Templates:** `30-decisive-decision-templates.md` (decisive moments)

---

## Overview

Every season follows a **3-act dramatic structure** (Setup → Complications → Resolution) with timing adjusted to season length. The system generates appropriately paced narrative beats, complications, and decisive moments based on the chosen aspiration and season length.

**Core Principle:** Every season should feel like a complete story with setup, conflict, climax, and resolution.

**Multi-Season Context:** This 3-act structure applies to EACH season individually. A character lives through **8-10 seasons** total (their Life Bookshelf), with each season being one complete story arc. Between seasons, time can skip forward (months to years) with auto-generated narrative. See `73-season-flow-implementation.md` for complete lifecycle.

**Compliance:** master_truths v1.2 specifies seasons are complete 3-act story arcs with decisive decisions that pause time, emotional capacity curves, and memory resonance threading.

---

## 3-Act Structure Definition

### Universal Template

```typescript
interface ThreeActStructure {
  act_1_setup: {
    percentage: number;              // % of season
    weeks: [number, number];         // Week range
    purpose: "establish_world_and_goal";
    key_elements: string[];
  };
  
  act_2_complications: {
    percentage: number;
    weeks: [number, number];
    purpose: "escalate_conflict_and_challenge";
    key_elements: string[];
  };
  
  act_3_resolution: {
    percentage: number;
    weeks: [number, number];
    purpose: "climax_and_resolution";
    key_elements: string[];
  };
}
```

---

## Act Structure by Season Length

### Standard (12 Weeks) - 3/6/3 Split

```javascript
const STANDARD_12_WEEK_ARC = {
  total_weeks: 12,
  total_turns: 252,                  // 12 weeks × 21 turns/week
  
  act_1_setup: {
    percentage: 0.25,                // 25% of season
    weeks: [1, 3],
    turns: 63,
    
    purpose: "Establish aspiration, routine, and stakes",
    
    key_elements: [
      "aspiration_selection",
      "starting_situation_established",
      "key_npcs_introduced",
      "first_steps_taken",
      "routine_established",
      "first_seeds_of_complication"
    ],
    
    narrative_beats: [
      {
        week: 1,
        beat: "NEW_BEGINNING",
        description: "Season opens. Aspiration chosen. Hope and uncertainty."
      },
      {
        week: 2,
        beat: "FIRST_STEPS",
        description: "Initial actions taken. Learning the challenge."
      },
      {
        week: 3,
        beat: "FIRST_OBSTACLE",
        description: "First hint that this won't be easy."
      }
    ],
    
    complications: 0,                // No major complications yet
    decisive_decisions: 0
  },
  
  act_2_complications: {
    percentage: 0.50,                // 50% of season
    weeks: [4, 9],
    turns: 126,
    
    purpose: "Escalate challenges, introduce conflicts, build tension",
    
    key_elements: [
      "complications_emerge",
      "competing_priorities",
      "relationship_tests",
      "skill_challenges",
      "midpoint_crisis",
      "commitment_tested"
    ],
    
    narrative_beats: [
      {
        week: 4,
        beat: "COMPLICATION_1",
        description: "First major obstacle appears."
      },
      {
        week: 5,
        beat: "COMPLICATION_DEEPENS",
        description: "Problem more complex than expected."
      },
      {
        week: 6,
        beat: "DECISIVE_DECISION_1",
        description: "First major choice. Commit or pivot?"
      },
      {
        week: 7,
        beat: "CONSEQUENCES",
        description: "Choice consequences play out."
      },
      {
        week: 8,
        beat: "COMPLICATION_2",
        description: "New challenge emerges."
      },
      {
        week: 9,
        beat: "CRISIS_POINT",
        description: "Everything comes to a head."
      }
    ],
    
    complications: 2,                // 2 major complications
    decisive_decisions: 1,           // 1 major decision at midpoint
    
    midpoint: {
      week: 6,
      type: "decisive_decision",
      purpose: "Test commitment to aspiration",
      stakes: "Can abandon or double down"
    }
  },
  
  act_3_resolution: {
    percentage: 0.25,                // 25% of season
    weeks: [10, 12],
    turns: 63,
    
    purpose: "Climax, resolution, and wrap-up",
    
    key_elements: [
      "final_push",
      "climactic_decision",
      "aspiration_outcome",
      "relationship_resolution",
      "character_growth_evident",
      "setup_next_season"
    ],
    
    narrative_beats: [
      {
        week: 10,
        beat: "FINAL_PUSH",
        description: "Last sprint toward goal."
      },
      {
        week: 11,
        beat: "CLIMAX_DECISION",
        description: "The biggest choice. Define the outcome."
      },
      {
        week: 12,
        beat: "RESOLUTION",
        description: "Outcome clear. Reflection and transition."
      }
    ],
    
    complications: 0,                // Resolving, not complicating
    decisive_decisions: 1,           // Climax decision
    
    climax: {
      week: 11,
      type: "decisive_decision",
      purpose: "Determine aspiration outcome",
      stakes: "Success, partial success, or transformation"
    }
  }
};
```

---

### Extended (24 Weeks) - 6/12/6 Split

```javascript
const EXTENDED_24_WEEK_ARC = {
  total_weeks: 24,
  total_turns: 504,
  
  act_1_setup: {
    percentage: 0.25,
    weeks: [1, 6],
    turns: 126,
    
    purpose: "Establish complex world with multiple threads",
    
    key_elements: [
      "aspiration_and_subplot_established",
      "extensive_cast_introduced",
      "multiple_threads_planted",
      "routine_and_constraints_set",
      "stakes_escalated_gradually"
    ],
    
    narrative_beats: [
      { week: 1, beat: "NEW_BEGINNING" },
      { week: 2, beat: "WORLD_BUILDING" },
      { week: 3, beat: "SUBPLOTS_INTRODUCED" },
      { week: 4, beat: "FIRST_STEPS" },
      { week: 5, beat: "COMPLEXITY_EMERGES" },
      { week: 6, beat: "FIRST_COMPLICATION" }
    ],
    
    complications: 1,                // Early complication
    decisive_decisions: 0
  },
  
  act_2_complications: {
    percentage: 0.50,
    weeks: [7, 18],
    turns: 252,
    
    purpose: "Escalate multiple threads, interweave conflicts",
    
    key_elements: [
      "competing_priorities_intensify",
      "relationship_conflicts",
      "skill_challenges",
      "multiple_decisive_decisions",
      "cascading_consequences",
      "subplot_intersects_main_arc"
    ],
    
    narrative_beats: [
      { week: 7, beat: "COMPLICATION_2" },
      { week: 8, beat: "PRESSURE_BUILDS" },
      { week: 9, beat: "COMPLICATION_3" },
      { week: 10, beat: "DECISIVE_DECISION_1" },
      { week: 11, beat: "CONSEQUENCES_RIPPLE" },
      { week: 12, beat: "MIDPOINT_CRISIS" },
      { week: 13, beat: "COMPLICATION_4" },
      { week: 14, beat: "THREADS_INTERWEAVE" },
      { week: 15, beat: "DECISIVE_DECISION_2" },
      { week: 16, beat: "TENSION_PEAK" },
      { week: 17, beat: "COMPLICATION_5" },
      { week: 18, beat: "PRE_CLIMAX_CRISIS" }
    ],
    
    complications: 5,                // More complications
    decisive_decisions: 3,           // Multiple major decisions
    
    midpoints: [
      {
        week: 10,
        type: "decisive_decision",
        purpose: "First major commitment test"
      },
      {
        week: 15,
        type: "decisive_decision",
        purpose: "Relationship or aspiration choice"
      }
    ]
  },
  
  act_3_resolution: {
    percentage: 0.25,
    weeks: [19, 24],
    turns: 126,
    
    purpose: "Resolve multiple threads, climax, epilogue",
    
    key_elements: [
      "multiple_climactic_moments",
      "main_arc_resolution",
      "subplot_resolution",
      "relationship_outcomes",
      "character_transformation",
      "epilogue_and_setup"
    ],
    
    narrative_beats: [
      { week: 19, beat: "FINAL_PUSH_BEGINS" },
      { week: 20, beat: "SUBPLOT_RESOLVES" },
      { week: 21, beat: "CLIMAX_DECISION_1" },
      { week: 22, beat: "CLIMAX_DECISION_2" },
      { week: 23, beat: "RESOLUTION_UNFOLDS" },
      { week: 24, beat: "EPILOGUE" }
    ],
    
    complications: 0,
    decisive_decisions: 2,           // Multiple climax decisions
    
    climaxes: [
      {
        week: 21,
        type: "decisive_decision",
        purpose: "Resolve main aspiration"
      },
      {
        week: 22,
        type: "decisive_decision",
        purpose: "Resolve key relationship"
      }
    ]
  }
};
```

---

### Epic (36 Weeks) - 9/18/9 Split

```javascript
const EPIC_36_WEEK_ARC = {
  total_weeks: 36,
  total_turns: 756,
  
  act_1_setup: {
    percentage: 0.25,
    weeks: [1, 9],
    turns: 189,
    
    purpose: "Establish epic scope with extensive world-building",
    
    key_elements: [
      "main_aspiration_and_multiple_subplots",
      "extensive_cast_8_plus_npcs",
      "complex_world_with_factions",
      "multiple_threads_planted",
      "long_term_stakes_established"
    ],
    
    narrative_beats: [
      { week: 1, beat: "EPIC_OPENING" },
      { week: 2, beat: "WORLD_BUILDING" },
      { week: 3, beat: "CAST_INTRODUCTION" },
      { week: 4, beat: "SUBPLOTS_PLANTED" },
      { week: 5, beat: "COMPLEXITY_DEEPENS" },
      { week: 6, beat: "FIRST_STEPS" },
      { week: 7, beat: "EARLY_CHALLENGE" },
      { week: 8, beat: "THREADS_INTERWEAVE" },
      { week: 9, beat: "INCITING_INCIDENT" }
    ],
    
    complications: 2,
    decisive_decisions: 0
  },
  
  act_2_complications: {
    percentage: 0.50,
    weeks: [10, 27],
    turns: 378,
    
    purpose: "Escalate multiple interwoven threads to saga-level complexity",
    
    key_elements: [
      "multiple_cascading_complications",
      "relationship_web_complexity",
      "competing_arcs_intersect",
      "personality_evolution_visible",
      "multiple_crises",
      "5_plus_decisive_decisions"
    ],
    
    // 18 weeks of escalating action
    narrative_structure: "Three 6-week mini-arcs within Act II",
    
    mini_arcs: [
      {
        weeks: [10, 15],
        theme: "Early complications and first major decisions",
        decisive_decisions: 2,
        complications: 3
      },
      {
        weeks: [16, 21],
        theme: "Midpoint crisis and cascading consequences",
        decisive_decisions: 2,
        complications: 4
      },
      {
        weeks: [22, 27],
        theme: "Pre-climax tension and final complications",
        decisive_decisions: 2,
        complications: 5
      }
    ],
    
    total_complications: 12,
    total_decisive_decisions: 6
  },
  
  act_3_resolution: {
    percentage: 0.25,
    weeks: [28, 36],
    turns: 189,
    
    purpose: "Epic multi-thread resolution with transformation evident",
    
    key_elements: [
      "multiple_climactic_sequences",
      "all_arcs_resolve",
      "character_transformation_complete",
      "legacy_established",
      "epilogue_shows_new_life"
    ],
    
    narrative_beats: [
      { week: 28, beat: "FINAL_PUSH" },
      { week: 29, beat: "SUBPLOT_1_CLIMAX" },
      { week: 30, beat: "SUBPLOT_2_CLIMAX" },
      { week: 31, beat: "MAIN_ARC_CLIMAX_1" },
      { week: 32, beat: "MAIN_ARC_CLIMAX_2" },
      { week: 33, beat: "RESOLUTION_BEGINS" },
      { week: 34, beat: "RESOLUTION_DEEPENS" },
      { week: 35, beat: "TRANSFORMATION_EVIDENT" },
      { week: 36, beat: "EPILOGUE_NEW_NORMAL" }
    ],
    
    complications: 0,
    decisive_decisions: 3,
    
    climax_sequence: {
      weeks: [31, 32],
      description: "2-week climax sequence with multiple decisions"
    }
  }
};
```

---

## Master Truths v1.2: Emotional Journey Mapping *(NEW)*

### Emotional Capacity Curves Across Acts

**Purpose:** Track how emotional capacity fluctuates through the 3-act structure, creating realistic emotional arcs.

```javascript
const EMOTIONAL_JOURNEY_TEMPLATES = {
  standard_12_week_journey: {
    act_1_setup: {
      weeks: [1, 3],
      
      emotional_trajectory: {
        starting_capacity: 7.0,           // Fresh start, hopeful
        ending_capacity: 6.5,             // Slight decrease as reality sets in
        capacity_curve: "gentle_decline",
        
        emotional_state_progression: [
          { week: 1, state: "HOPEFUL", reason: "New beginning, possibility" },
          { week: 2, state: "MOTIVATED", reason: "Taking first steps" },
          { week: 3, state: "CAUTIOUS", reason: "First obstacles appear" }
        ]
      },
      
      stressor_profile: {
        stressor_count_range: [1, 2],     // Light stress
        typical_stressors: ["learning_curve", "time_management"],
        capacity_drain_rate: -0.2         // Per week
      },
      
      narrative_notes: "Act 1 is about hope tempered by reality"
    },
    
    act_2_complications: {
      weeks: [4, 9],
      
      emotional_trajectory: {
        starting_capacity: 6.5,
        ending_capacity: 3.5,             // Significant decline
        capacity_curve: "steady_decline_with_spikes",
        
        low_point: {
          week: 8,
          capacity: 2.8,
          state: "OVERWHELMED",
          reason: "Crisis point before climax"
        },
        
        emotional_state_progression: [
          { week: 4, state: "CHALLENGED", reason: "First major complication" },
          { week: 5, state: "STRESSED", reason: "Complexity deepens" },
          { week: 6, state: "CONFLICTED", reason: "Decisive decision" },
          { week: 7, state: "ANXIOUS", reason: "Consequences uncertain" },
          { week: 8, state: "OVERWHELMED", reason: "Everything compounds" },
          { week: 9, state: "DETERMINED", reason: "Commitment to push through" }
        ]
      },
      
      stressor_profile: {
        stressor_count_range: [2, 5],     // Peak stress
        peak_stressor_week: 8,
        typical_stressors: [
          "competing_priorities",
          "relationship_tension",
          "resource_scarcity",
          "skill_inadequacy",
          "time_pressure"
        ],
        capacity_drain_rate: -0.5,        // Faster decline
        recovery_opportunities: [
          { week: 7, type: "support_from_npc", capacity_gain: +1.0 }
        ]
      },
      
      narrative_notes: "Act 2 is the emotional crucible - drain capacity to create stakes"
    },
    
    act_3_resolution: {
      weeks: [10, 12],
      
      emotional_trajectory: {
        starting_capacity: 3.5,
        ending_capacity: 7.5,             // Recovery + growth
        capacity_curve: "recovery_and_resolution",
        
        climax: {
          week: 11,
          capacity_required: 4.0,         // Must have minimum capacity for climax
          capacity_if_below: "locked_options_or_failure",
          post_climax_boost: +2.0         // Victory or closure provides relief
        },
        
        emotional_state_progression: [
          { week: 10, state: "FOCUSED", reason: "Final push clarity" },
          { week: 11, state: "INTENSE", reason: "Climactic moment" },
          { week: 12, state: "RELIEVED" or "TRANSFORMED", reason: "Resolution achieved" }
        ]
      },
      
      stressor_profile: {
        stressor_count_range: [1, 2],     // Resolution phase
        stressors_resolving: true,
        capacity_drain_rate: 0.0,         // Stable
        recovery_rate: +1.5,              // Active recovery
        final_boost: +2.0                 // Sense of accomplishment
      },
      
      narrative_notes: "Act 3 is recovery and transformation - earned catharsis"
    }
  },
  
  // Extended journey has deeper lows and higher peaks
  extended_24_week_journey: {
    act_1_setup: {
      weeks: [1, 6],
      emotional_trajectory: {
        starting_capacity: 7.5,
        ending_capacity: 6.8,
        capacity_curve: "gradual_decline",
        lowest_point: 6.2
      },
      stressor_profile: {
        stressor_count_range: [1, 3],
        capacity_drain_rate: -0.15
      }
    },
    
    act_2_complications: {
      weeks: [7, 18],
      emotional_trajectory: {
        starting_capacity: 6.8,
        ending_capacity: 2.5,             // Lower than 12w
        capacity_curve: "wave_pattern_declining",
        
        valleys: [
          { week: 10, capacity: 4.5, reason: "First decision consequences" },
          { week: 15, capacity: 3.2, reason: "Midpoint crisis" },
          { week: 18, capacity: 2.5, reason: "Pre-climax breakdown" }
        ],
        
        recovery_moments: [
          { week: 12, capacity_gain: +0.8, reason: "Brief respite" },
          { week: 16, capacity_gain: +0.5, reason: "Small victory" }
        ]
      },
      stressor_profile: {
        stressor_count_range: [2, 6],
        peak_weeks: [10, 15, 18],
        capacity_drain_rate: -0.4
      }
    },
    
    act_3_resolution: {
      weeks: [19, 24],
      emotional_trajectory: {
        starting_capacity: 2.5,
        ending_capacity: 8.0,             // Higher than start (growth)
        capacity_curve: "recovery_with_transformation",
        climax_boost: +2.5
      },
      stressor_profile: {
        recovery_rate: +1.2,
        final_transformation_boost: +3.0
      }
    }
  },
  
  // Epic journey has extreme swings
  epic_36_week_journey: {
    act_1_setup: {
      weeks: [1, 9],
      emotional_trajectory: {
        starting_capacity: 8.0,           // Epic fresh start
        ending_capacity: 7.0,
        capacity_curve: "slow_decline_with_excitement"
      }
    },
    
    act_2_complications: {
      weeks: [10, 27],
      emotional_trajectory: {
        starting_capacity: 7.0,
        ending_capacity: 2.0,             // Near breakdown
        capacity_curve: "dramatic_waves",
        
        crisis_points: [
          { week: 15, capacity: 3.5, state: "STRESSED" },
          { week: 21, capacity: 2.8, state: "OVERWHELMED" },
          { week: 27, capacity: 2.0, state: "BREAKING_POINT" }
        ]
      },
      stressor_profile: {
        stressor_count_range: [3, 8],
        epic_complexity: true,
        capacity_drain_rate: -0.35
      }
    },
    
    act_3_resolution: {
      weeks: [28, 36],
      emotional_trajectory: {
        starting_capacity: 2.0,
        ending_capacity: 9.0,             // Epic transformation
        capacity_curve: "heroic_recovery",
        climax_sequence_boost: +3.5,
        transformation_evident: true
      }
    }
  }
};
```

---

### Capacity-Aware Beat Placement

```javascript
function placeBeatsWithCapacityAwareness(arcTemplate, player) {
  const beats = generateNarrativeBeats(arcTemplate);
  const capacityTrack = initializeCapacityTracking(player.current_capacity);
  
  beats.forEach(beat => {
    // Estimate capacity at beat week
    const estimated_capacity = calculateCapacityAtWeek(
      capacityTrack, 
      beat.week, 
      arcTemplate
    );
    
    // Adjust beat based on capacity
    if (beat.beat_type === "DECISIVE_DECISION") {
      beat.capacity_context = {
        estimated_capacity: estimated_capacity,
        min_required: 3.0,
        locked_options_if_below: 2.5,
        narrative_acknowledgment: `
          Your capacity: ${estimated_capacity.toFixed(1)}/10
          ${estimated_capacity < 3.0 ? "You're struggling. Some options may be unavailable." : ""}
        `
      };
    }
    
    if (beat.beat_type === "COMPLICATION") {
      beat.capacity_impact = {
        drain: calculateDrain(beat.complication_type),
        affects_future_weeks: true,
        compounds_with_existing: estimated_capacity < 4.0
      };
    }
    
    // If capacity too low for planned beat, adjust or add support
    if (estimated_capacity < 2.0 && beat.intensity > 0.7) {
      // Insert support beat before high-intensity beat
      insertSupportBeat(beats, beat.week - 1, {
        type: "NPC_SUPPORT",
        capacity_boost: +1.5,
        narrative: "Friend offers help at critical moment"
      });
    }
  });
  
  return beats;
}
```

---

## Master Truths v1.2: Memory Resonance Threading *(NEW)*

### Memory Callbacks Across Acts and Seasons

**Purpose:** Past experiences echo through current narrative, creating emotional continuity and depth.

```javascript
const MEMORY_RESONANCE_SYSTEM = {
  within_season_resonance: {
    description: "Memories from earlier in same season affect current narrative",
    
    examples: [
      {
        act: 2,
        week: 8,
        memory_callback: {
          references_week: 2,
          original_event: "First excited steps toward photography goal",
          current_context: "Now struggling, exhausted, questioning choice",
          
          resonance_card: `
            You're editing photos at 2am. Eyes burning. Coffee cold.
            
            You remember Week 2. How excited you were. How this felt like 
            possibility, not exhaustion.
            
            *Flashback: "This is going to change everything!" you told Marcus.*
            
            That version of you had no idea how hard this would be.
            
            Was that excitement naive? Or was it the truth you're losing sight of?
          `,
          
          emotional_weight: 0.85,
          affects_player_state: {
            if_low_capacity: "Increases doubt, might trigger crisis",
            if_moderate_capacity: "Bittersweet reflection, reaffirms commitment"
          }
        }
      },
      {
        act: 3,
        week: 11,
        memory_callback: {
          references_week: 6,
          original_event: "Decisive decision - chose photography over work",
          current_context: "Gallery show tonight - payoff moment",
          
          resonance_card: `
            Gallery opening in 2 hours. Your photos on the walls.
            
            You remember that decision. Week 6. The wedding shoot vs. work.
            You chose the shoot. Boss was furious.
            
            *Flashback: Staring at two phone messages, heart pounding.*
            
            You made your choice. It cost you the promotion. Strained that relationship.
            
            But tonight... tonight you're here. Your work. Your name.
            
            Was it worth it? You're about to find out.
          `,
          
          emotional_weight: 0.95,
          creates_catharsis: true,
          validates_past_choice: "conditional_on_outcome"
        }
      }
    ]
  },
  
  cross_season_resonance: {
    description: "Memories from past seasons echo into current narrative",
    
    examples: [
      {
        current_season: 3,
        references_season: 1,
        current_week: 8,
        
        memory_callback: {
          original_season_event: "Season 1: Failed first aspiration, gave up",
          current_context: "Season 3: Similar moment of wanting to quit",
          
          resonance_card: `
            You want to quit. The thought is clear, sharp, tempting.
            
            You've been here before.
            
            *Memory: Season 1. Different aspiration, same feeling.*
            *You quit. You told yourself it was pragmatic. Mature.*
            *But you've regretted it for two years.*
            
            This moment feels identical. The exhaustion. The doubt. The exit door.
            
            Last time you took it. You know how that story ends.
            
            Do you make the same choice again?
          `,
          
          emotional_weight: 0.9,
          pattern_awareness: true,
          affects_decision: {
            adds_option: "\"Not this time\" (Break pattern, push through)",
            option_difficulty_modifier: -0.15,  // Easier - learned from past
            character_growth_moment: true
          },
          
          if_repeats_pattern: {
            regret_compounded: true,
            pattern_strength: "becomes_defining_trait",
            novel_theme: "The person who gives up"
          },
          
          if_breaks_pattern: {
            character_growth: +0.3,
            confidence_boost: true,
            novel_theme: "The person who learned"
          }
        }
      },
      {
        current_season: 5,
        references_season: 2,
        current_week: 14,
        
        memory_callback: {
          original_season_event: "Season 2: Neglected Sarah, she moved away",
          current_context: "Season 5: New close friend showing same warning signs",
          
          resonance_card: `
            Marcus's last three texts went unanswered. You've been busy. 
            He understands, right?
            
            You've been here before.
            
            *Memory: Season 2. Sarah's texts getting shorter. Then stopping.*
            *By the time you noticed, she'd moved. 1,200 miles away.*
            *You still regret it.*
            
            Marcus's text from yesterday: "Miss you. Hope you're okay."
            
            Same pattern. Different person. Same chance to lose someone who matters.
            
            Do you learn from the past, or repeat it?
          `,
          
          emotional_weight: 0.95,
          pattern_recognition: "explicit",
          trauma_trigger: true,           // Losing Sarah was painful
          
          affects_decision: {
            unlocks_option: "\"Not again\" (Prioritize Marcus immediately)",
            urgency_increased: true,
            capacity_boost: +0.5,         // Fear of loss energizes
            prevents_same_mistake: true
          },
          
          if_ignores_warning: {
            history_repeats: true,
            marcus_outcome: "similar_to_sarah_loss",
            regret_weight: 10,            // Maximum
            novel_theme: "The patterns we can't break"
          }
        }
      }
    ]
  },
  
  memory_placement_rules: {
    frequency: {
      within_season: "2-4 callbacks per season",
      cross_season: "1-2 major callbacks per season"
    },
    
    timing: {
      within_season: "Act 2 (parallel moment) or Act 3 (reflection)",
      cross_season: "Similar emotional/situational context"
    },
    
    triggers: {
      automatic: [
        "Similar decision type in similar context",
        "Same NPC archetype (e.g., close friend drift)",
        "Repeated failure pattern",
        "Anniversary of major event"
      ],
      
      player_initiated: [
        "Player reviews past seasons in Life Bookshelf",
        "Player encounters same NPC from past season",
        "Player visits same location"
      ]
    },
    
    emotional_requirements: {
      min_original_weight: 7,           // Only significant memories
      similar_emotional_context: true,
      player_capacity_aware: true       // Don't overwhelm if capacity < 3
    }
  },
  
  integration_with_novel_generation: {
    memory_callbacks_in_chapters: true,
    flashback_scenes: "Formatted distinctly",
    pattern_themes: "Tracked across Life Bookshelf",
    
    example_chapter_structure: `
      Chapter 12: The Decision (Again)
      
      [Present narrative]
      You stare at the email. Another opportunity. Another risk.
      
      [Flashback - italicized]
      *Two years ago. Different email. Same feeling.*
      *You played it safe then. You've regretted it ever since.*
      
      [Present narrative]
      This time could be different.
      This time, you know the cost of caution.
      
      [Pattern recognition]
      You've been here before. The question is: have you learned?
    `
  }
};
```

---

### Memory Weight Decay and Amplification

```javascript
const MEMORY_RESONANCE_WEIGHTS = {
  decay_over_time: {
    base_formula: "original_weight × (0.95 ^ weeks_elapsed)",
    
    exceptions: [
      {
        condition: "Trauma or peak positive experience (weight 9-10)",
        decay_rate: 0.98,              // Slower decay
        note: "Profound memories persist"
      },
      {
        condition: "Referenced in current season",
        effect: "Reset decay, +0.1 weight boost",
        note: "Recalled memories strengthen"
      }
    ]
  },
  
  amplification_triggers: {
    similar_context: {
      description: "Current situation mirrors past memory",
      weight_multiplier: 1.3,
      examples: [
        "Facing same decision type",
        "Similar relationship dynamic",
        "Parallel career moment"
      ]
    },
    
    trauma_trigger: {
      description: "Current situation activates past trauma",
      weight_multiplier: 1.5,
      emotional_impact: "intense",
      examples: [
        "Risk of repeating painful loss",
        "Similar betrayal context",
        "Parallel failure scenario"
      ]
    },
    
    growth_callback: {
      description: "Proof of how far you've come",
      weight_multiplier: 1.2,
      emotional_valence: "positive",
      examples: [
        "Now succeeding where you once failed",
        "Handling easily what once overwhelmed",
        "Breaking pattern you once repeated"
      ]
    }
  }
};
```

---

## Arc Beat Generation System

### Dynamic Beat Placement

```javascript
function generateNarrativeBeats(aspiration, seasonLength, player) {
  const arcTemplate = getArcTemplate(seasonLength); // 12/24/36
  const beats = [];
  
  // Act I beats
  arcTemplate.act_1_setup.narrative_beats.forEach(beatTemplate => {
    beats.push({
      week: beatTemplate.week,
      beat_type: beatTemplate.beat,
      content: generateBeatContent(beatTemplate, aspiration, player),
      act: 1,
      mandatory: true
    });
  });
  
  // Act II beats (with complication insertion)
  const complications = generateComplications(aspiration, arcTemplate.act_2_complications.complications);
  const decisiveDecisions = generateDecisiveDecisions(aspiration, arcTemplate.act_2_complications.decisive_decisions);
  
  // Distribute complications across Act II
  const act2Weeks = arcTemplate.act_2_complications.weeks;
  const weeksPerComplication = (act2Weeks[1] - act2Weeks[0]) / complications.length;
  
  complications.forEach((complication, index) => {
    const weekPlacement = Math.floor(act2Weeks[0] + (weeksPerComplication * index));
    beats.push({
      week: weekPlacement,
      beat_type: "COMPLICATION",
      content: complication,
      act: 2,
      mandatory: true,
      intensity: calculateIntensity(index, complications.length)
    });
  });
  
  // Insert decisive decisions at key moments
  decisiveDecisions.forEach((decision, index) => {
    const weekPlacement = calculateDecisionPlacement(act2Weeks, index, decisiveDecisions.length);
    beats.push({
      week: weekPlacement,
      beat_type: "DECISIVE_DECISION",
      content: decision,
      act: 2,
      mandatory: true,
      pauses_time: true,
      intensity: 0.9
    });
  });
  
  // Act III beats
  arcTemplate.act_3_resolution.narrative_beats.forEach(beatTemplate => {
    beats.push({
      week: beatTemplate.week,
      beat_type: beatTemplate.beat,
      content: generateBeatContent(beatTemplate, aspiration, player),
      act: 3,
      mandatory: true
    });
  });
  
  // Sort by week
  beats.sort((a, b) => a.week - b.week);
  
  return beats;
}
```

---

## Complication Types

### 7 Complication Categories

```javascript
const COMPLICATION_TYPES = {
  resource_scarcity: {
    description: "Not enough time/money/energy",
    examples: [
      "Unexpected expense drains savings",
      "Project takes 3x longer than expected",
      "Physical health crisis limits energy"
    ],
    typical_placement: "early_to_mid_act_2"
  },
  
  competing_priorities: {
    description: "Multiple important things demand attention",
    examples: [
      "Job demands increase same week as aspiration deadline",
      "Family crisis during critical project phase",
      "Two important relationships need attention simultaneously"
    ],
    typical_placement: "mid_act_2"
  },
  
  skill_inadequacy: {
    description: "Realize you lack necessary skills",
    examples: [
      "Portfolio work reveals design gaps",
      "Public speaking more terrifying than anticipated",
      "Technical skills insufficient for next level"
    ],
    typical_placement: "early_act_2"
  },
  
  relationship_conflict: {
    description: "Important relationship tested or damaged",
    examples: [
      "Partner resents time spent on aspiration",
      "Mentor disappointed in your progress",
      "Friend feels neglected"
    ],
    typical_placement: "mid_to_late_act_2"
  },
  
  external_obstacle: {
    description: "World throws unexpected challenge",
    examples: [
      "Competitor enters your space",
      "Market conditions change",
      "Key opportunity falls through",
      "Equipment breaks, location closes"
    ],
    typical_placement: "any_point_act_2"
  },
  
  internal_doubt: {
    description: "Self-sabotage or crisis of confidence",
    examples: [
      "Impostor syndrome paralyzes progress",
      "Question if aspiration is right path",
      "Fear of success/failure creates avoidance"
    ],
    typical_placement: "late_act_2_or_act_3"
  },
  
  betrayal_or_loss: {
    description: "Significant setback from person or event",
    examples: [
      "Trusted person sabotages efforts",
      "Major loss (death, breakup, firing)",
      "Stolen work, broken promise"
    ],
    typical_placement: "late_act_2",
    severity: "high"
  }
};
```

---

## Foreshadowing System

### Planting Seeds for Future Beats

```javascript
function generateForeshadowing(upcoming_beat, weeks_ahead) {
  const foreshadowing_events = [];
  
  // Foreshadow complications 2-4 weeks ahead
  if (upcoming_beat.beat_type === "COMPLICATION") {
    const hints = [
      {
        weeks_before: 4,
        hint_type: "subtle_mention",
        content: "NPC mentions potential issue in passing",
        example: "Mirror reflection looks tired (4 weeks before health crisis)"
      },
      {
        weeks_before: 3,
        hint_type: "subtle_mention",
        content: "NPC mentions potential issue in passing",
        example: "Sarah seems distracted lately (3 weeks before relationship conflict)"
      },
      {
        weeks_before: 2,
        hint_type: "warning_sign",
        content: "First small sign of problem appears",
        example: "Coffee isn't helping anymore (2 weeks before collapse)"
      },
      {
        weeks_before: 1,
        hint_type: "clear_foreshadowing",
        content: "Problem is coming, prepare or ignore",
        example: "Hands shake slightly during important moment (1 week before crisis)"
      }
    ];
    
    return hints.filter(h => h.weeks_before <= weeks_ahead);
  }
  
  // Foreshadow decisive decisions 2-4 weeks ahead
  if (upcoming_beat.beat_type === "DECISIVE_DECISION") {
    const hints = [
      {
        weeks_before: 4,
        hint_type: "thematic_setup",
        content: "Introduce themes/values that decision will test"
      },
      {
        weeks_before: 2,
        hint_type: "situation_building",
        content: "Build situation that will force decision"
      },
      {
        weeks_before: 1,
        hint_type: "anticipation",
        content: "Tension rises, decision looms"
      }
    ];
    
    return hints.filter(h => h.weeks_before <= weeks_ahead);
  }
  
  // NEW: Foreshadow crisis events with escalating symptoms
  if (upcoming_beat.beat_type === "CRISIS") {
    const crisis_foreshadowing = generateCrisisForeshadowing(upcoming_beat, weeks_ahead);
    return crisis_foreshadowing;
  }
  
  return [];
}

// NEW: Enhanced crisis foreshadowing with physical/emotional symptoms
function generateCrisisForeshadowing(crisis_event, weeks_ahead) {
  const foreshadowing_cards = {
    health_crisis: [
      {
        weeks_before: 4,
        card_text: "You catch your reflection in the mirror. You look... tired. Really tired.",
        weight: 0.3,
        ignorable: true
      },
      {
        weeks_before: 2,
        card_text: "Your usual coffee isn't helping anymore. Three cups and you still feel foggy.",
        weight: 0.6,
        ignorable: true,
        meter_hint: "Physical meter low"
      },
      {
        weeks_before: 1,
        card_text: "Your hands shake slightly during an important moment. You notice. Others might too.",
        weight: 0.8,
        ignorable: false,
        urgent: true
      }
    ],
    
    relationship_crisis: [
      {
        weeks_before: 3,
        card_text: "Sarah seems distant lately. Probably just busy.",
        weight: 0.4,
        ignorable: true
      },
      {
        weeks_before: 2,
        card_text: "Third canceled plan in a row. Sarah apologizes but seems... off.",
        weight: 0.6,
        ignorable: false
      },
      {
        weeks_before: 1,
        card_text: "Sarah's texts are shorter now. Less warm. Something's changed.",
        weight: 0.8,
        ignorable: false,
        confrontation_coming: true
      }
    ],
    
    financial_crisis: [
      {
        weeks_before: 3,
        card_text: "Rent is due next month. You should have enough... probably.",
        weight: 0.3,
        ignorable: true
      },
      {
        weeks_before: 2,
        card_text: "Check account balance. Lower than expected. Where did it all go?",
        weight: 0.6,
        ignorable: false
      },
      {
        weeks_before: 1,
        card_text: "Calculator out. Bills listed. Math isn't working. You're short.",
        weight: 0.9,
        ignorable: false,
        urgent: true
      }
    ],
    
    career_crisis: [
      {
        weeks_before: 4,
        card_text: "Boss seems less warm lately. Probably imagining it.",
        weight: 0.2,
        ignorable: true
      },
      {
        weeks_before: 2,
        card_text: "You're not invited to the planning meeting. That's... unusual.",
        weight: 0.5,
        ignorable: false
      },
      {
        weeks_before: 1,
        card_text: "Email from HR: 'Please schedule a meeting.' No details.",
        weight: 0.9,
        ignorable: false,
        urgent: true
      }
    ]
  };
  
  const crisis_type = crisis_event.crisis_category;
  const relevant_cards = foreshadowing_cards[crisis_type] || [];
  
  return relevant_cards.filter(card => card.weeks_before <= weeks_ahead);
}
```

---

## NEW: Stakes Escalation System

### Consequence Chains (Interconnected Stakes)

**Purpose:** Make consequences feel dramatic and interconnected - neglecting one area creates crises in others.

```javascript
const CONSEQUENCE_CHAINS = {
  health_neglect_chain: {
    trigger: "Physical meter < 3 for 3+ consecutive weeks",
    
    progression: [
      {
        week: 0,
        symptom: "Constant fatigue, reduced performance",
        affects: ["Aspiration progress slower", "Less energy for social"]
      },
      {
        week: 2,
        symptom: "Visible exhaustion, friends notice",
        affects: ["NPCs express concern", "Relationship conversations shift"],
        dramatic_moment: "Marcus: 'Are you okay? You don't look well.'"
      },
      {
        week: 3,
        crisis: "Public collapse during important moment",
        ripple_effects: {
          career: "Miss crucial work presentation → reputation damage",
          aspiration: "Can't shoot wedding (already booked) → lose client + deposit",
          relationships: "Friends scared, intervention discussion",
          financial: "Medical bills + lost income"
        },
        dramatic_consequence: true,
        story_worthy: "Chapter-level event in novel generation"
      }
    ],
    
    example: "Neglect physical health → Collapse at wedding shoot → Lose client, friends intervene, career damaged"
  },
  
  relationship_neglect_chain: {
    trigger: "Major NPC (Level 3+) not interacted with for 4+ weeks",
    
    progression: [
      {
        week: 0,
        symptom: "NPC stops reaching out first",
        affects: ["Fewer social invitations", "Relationship cooling"]
      },
      {
        week: 2,
        symptom: "NPC makes plans without you",
        affects: ["See NPC's life progressing", "Realize you're drifting"],
        dramatic_moment: "See photos of Sarah's party you weren't invited to"
      },
      {
        week: 4,
        crisis: "NPC makes major life decision without you",
        ripple_effects: {
          relationship: "Sarah moves away OR gets engaged OR opens business",
          emotional: "Regret, loss, realization of what you lost",
          aspiration: "If NPC was connected to aspiration, that path closes",
          life_trajectory: "Permanent change - NPC's role in life shifts"
        },
        dramatic_consequence: true,
        story_worthy: "Major relationship beat - 'The Friend I Lost'"
      }
    ],
    
    example: "Neglect Sarah for career → She moves away → Lose close friend + opportunities she represented"
  },
  
  career_neglect_chain: {
    trigger: "Career reputation < 0 OR 3+ missed work obligations",
    
    progression: [
      {
        week: 0,
        symptom: "Boss less friendly, fewer opportunities offered",
        affects: ["Promotion track stalled", "Excluded from key projects"]
      },
      {
        week: 2,
        symptom: "Reputation damage spreads",
        affects: ["Colleagues distance", "Performance review warning"],
        dramatic_moment: "Overhear: 'They used to be so reliable. What happened?'"
      },
      {
        week: 3,
        crisis: "Blamed for team failure OR put on performance plan",
        ripple_effects: {
          career: "No future promotions at this company",
          financial: "Bonus revoked, raise cancelled",
          aspiration: "If career funds aspiration, that timeline extends",
          emotional: "Stress, shame, questioning competence",
          reputation: "Industry reputation damaged (affects job hunting)"
        },
        dramatic_consequence: true,
        permanent_impact: "This company path effectively closed"
      }
    ],
    
    example: "Skip work for aspiration → Blamed for project failure → Career path blocked, must job hunt"
  },
  
  financial_crisis_chain: {
    trigger: "Money < $500 with rent/bills due within 2 weeks",
    
    progression: [
      {
        week: 0,
        symptom: "Anxiety about money, start counting pennies",
        affects: ["Can't accept social invitations that cost money", "Aspiration spending stops"]
      },
      {
        week: 1,
        crisis: "Can't pay rent OR critical expense (car, medical, equipment)",
        ripple_effects: {
          housing: "Eviction notice OR need to move OR borrow from friends",
          relationships: "Uncomfortable asking for help OR resentment if refused",
          aspiration: "Can't afford necessary equipment/supplies",
          health: "Skip medical treatment OR cheap unhealthy food",
          career: "Might need second job, less time for primary goals",
          emotional: "Stress, shame, fear"
        },
        multiple_areas_affected: true,
        dramatic_consequence: "Crisis ripples into EVERY life area"
      }
    ],
    
    example: "Overspend on aspiration → Can't pay rent → Borrow from Sarah (affects relationship) + second job (affects aspiration progress)"
  },
  
  aspiration_neglect_chain: {
    trigger: "Aspiration progress < 30% by midpoint (week 6 in 12w season)",
    
    progression: [
      {
        week: 0,
        symptom: "Behind schedule, pressure mounting",
        affects: ["Self-doubt increases", "Opportunities feel out of reach"]
      },
      {
        week: 2,
        crisis: "Aspiration-related NPC gives opportunity to someone else",
        ripple_effects: {
          aspiration: "Major setback, harder path forward",
          relationship: "Mentor disappointed OR friend succeeds where you stalled",
          emotional: "Regret, envy, motivation crisis",
          identity: "Question if this is really your path"
        },
        dramatic_moment: "Watch someone else succeed at what you wanted",
        story_worthy: "Failure beat - 'The Opportunity I Lost'"
      }
    ],
    
    example: "Focus on career, neglect photography aspiration → Friend gets gallery show → Realize you let dream slip away"
  }
};
```

---

### Dramatic Consequences (Not Just Stat Penalties)

**Principle:** Consequences should create story-worthy moments, not just -2 to a meter.

```javascript
const DRAMATIC_CONSEQUENCE_EXAMPLES = {
  stat_penalty_vs_story_moment: {
    bad_example: {
      consequence: "Physical meter -2",
      why_weak: "Just a number, not memorable, no story"
    },
    
    good_example: {
      consequence: "You collapse during the wedding ceremony you're photographing",
      ripple_effects: [
        "Client furious - no refund, no recommendation",
        "Bride posts negative review",
        "Sarah and Marcus rush you to hospital (relationship moment)",
        "Wake up to realize you've been ignoring your body for weeks",
        "Photography career damaged before it really started"
      ],
      why_strong: "Story-worthy scene, multiple areas affected, memorable moment",
      novel_chapter: "Could be a chapter: 'The Day Everything Collapsed'"
    }
  },
  
  relationship_consequences: {
    weak: "Sarah trust -0.2",
    strong: "Sarah stops reaching out. Weeks pass. You see on social media she opened her bookshop - the dream she talked to you about - and you weren't there.",
    impact: "Genuine loss, not just a number"
  },
  
  career_consequences: {
    weak: "Career reputation -1",
    strong: "Your colleague presents YOUR idea in the meeting you skipped. Gets praised. Gets YOUR promotion. You watch, silent.",
    impact: "Concrete moment of loss with lasting effects"
  },
  
  aspiration_consequences: {
    weak: "Aspiration progress -10%",
    strong: "The gallery contact you've been building a relationship with emails: 'We filled the slot with another photographer. Maybe next year.' Next year.",
    impact: "Opportunity missed, timeline extended, regret"
  }
};
```

---

## NEW: Dramatic Irony System

### NPC Perspective Reveals

**Purpose:** Show what NPCs think/plan that player doesn't know, creating anticipation and emotional investment.

```javascript
const DRAMATIC_IRONY_BEATS = {
  frequency: "1-2 times per season per major NPC",
  placement: "Strategic - mid Act II or before major revelations",
  
  types: {
    npc_pov_card: {
      description: "Show scene from NPC's perspective",
      
      examples: [
        {
          week: 10,
          npc: "Sarah",
          card_title: "What Sarah Is Really Thinking",
          content: `
            [Sarah's POV]
            
            You're sitting across from [Player Name] at coffee. They're talking 
            about the photography gig, excited. You smile and nod.
            
            But you're thinking about David. Today is his birthday. Would have been 
            his 31st. And [Player Name] has no idea why you've been so distant lately.
            
            You want to tell them. You're just... not ready. Not yet.
            
            [Player Name]: "You okay? You seem distracted."
            You: "I'm fine. Just tired."
            
            You're not fine. But maybe someday you will be.
          `,
          player_knowledge: "Sarah is distant for unknown reason",
          revealed: "Sarah is grieving, it's not about the player",
          emotional_effect: "Empathy, understanding, patience",
          affects_future: "Player knows to give Sarah space, not take it personally"
        },
        {
          week: 14,
          npc: "Marcus",
          card_title: "What Marcus Sees",
          content: `
            [Marcus's POV]
            
            You watch [Player Name] across the table. They're animated, talking about 
            how close they are to the goal. "Just need to push a bit harder," they say.
            
            You notice what they don't: the dark circles, the third coffee, the way 
            their hands shake slightly when they reach for their phone.
            
            You've been talking to Sarah about it. Both worried. Neither knows how to 
            bring it up without sounding like you're nagging.
            
            [Player Name]: "I'm fine, really."
            You: "Yeah. Just... don't burn out, okay?"
            
            You don't think they're listening. You're afraid of what comes next.
          `,
          player_knowledge: "Marcus seems concerned sometimes",
          revealed: "Marcus has been discussing intervention with Sarah",
          emotional_effect: "Realization friends care deeply, wake-up call",
          foreshadows: "Week 16 intervention conversation"
        }
      ]
    },
    
    secret_revealed_to_player: {
      description: "Player learns something NPCs don't know player knows",
      
      examples: [
        {
          week: 12,
          npc: "Your Boss",
          card_title: "What You Weren't Supposed to Hear",
          content: `
            You're getting coffee in the break room. Your boss is on the phone 
            in the next room, door slightly ajar.
            
            Boss: "...yes, I think [Player Name] has potential, but they've been 
            distracted lately. If they don't step up soon... well, we have other 
            options for the position."
            
            Pause.
            
            Boss: "I'll give them until end of quarter. Then we'll make a call."
            
            You freeze, coffee halfway to your lips. They don't know you heard.
            
            End of quarter. That's six weeks.
          `,
          player_knowledge_change: "Boss is evaluating you, 6 week deadline exists",
          boss_knowledge: "Thinks evaluation is private",
          creates_tension: "Player has info they 'shouldn't' have",
          affects_decisions: "Can act on this knowledge or pretend ignorance",
          ticking_clock: "6 weeks to prove yourself"
        }
      ]
    },
    
    contradiction_moment: {
      description: "NPC acts against established pattern, reveals hidden depth",
      
      examples: [
        {
          week: 16,
          npc: "Sarah",
          card_title: "Sarah's Unexpected Risk",
          content: `
            You've known Sarah for months. Careful Sarah. Reserved Sarah. 
            Sarah who plans everything.
            
            Today she texts: "I did something crazy. Quit my job. Opening the bookshop 
            next month. I know it's reckless but... I'm tired of being scared."
            
            You stare at your phone. This is the woman who took 3 months to decide 
            on a haircut.
            
            But maybe you don't know her as well as you thought.
          `,
          established_pattern: "Sarah is cautious, risk-averse, careful",
          contradiction: "Takes huge financial/career risk suddenly",
          reveals: "Sarah has been fighting fear since David died, finally breaking through",
          player_reaction: "Surprised, inspired, or worried",
          character_depth: "Sarah is more complex than 'the reserved friend'"
        },
        {
          week: 18,
          npc: "Marcus",
          card_title: "The Fight",
          content: `
            Marcus has been your biggest supporter. Always. Through everything.
            
            Today he's not.
            
            Marcus: "I think you're making a mistake. I think you're sacrificing 
            too much for this. And I think you don't want to hear it, but I'm going 
            to say it anyway."
            
            You've never heard him like this. Sharp. Frustrated. Disappointed.
            
            Marcus: "I support you. Always will. But I'm not going to pretend this 
            is healthy anymore."
            
            He's your friend. That's why he's saying it. You know that.
            
            But it still hurts.
          `,
          established_pattern: "Marcus is supportive, encouraging, positive",
          contradiction: "Confronts you, expresses disappointment",
          reveals: "Marcus has limits, values honesty over comfort",
          player_reaction: "Hurt but possibly needed wake-up call",
          character_depth: "Marcus's support has boundaries, which makes it more real"
        }
      ]
    }
  },
  
  placement_rules: {
    timing: "Mid Act II (weeks 10-18 in 24w season)",
    frequency: "1-2 per major NPC per season",
    avoid: "Don't overuse - loses impact if every session",
    purpose: "Create empathy, reveal depth, foreshadow major beats"
  },
  
  integration_with_mysteries: {
    can_reveal_clues: true,
    example: "Sarah POV card reveals David without player character knowing",
    creates_anticipation: "Player knows more than character, waits for revelation"
  }
};
```

---

## Arc Pacing Calculator

### Ensure Good Dramatic Rhythm

```javascript
function calculateArcPacing(beats, seasonLength) {
  const pacing = {
    weeks: [],
    intensity_curve: [],
    breathing_room: []
  };
  
  beats.forEach((beat, index) => {
    const week = beat.week;
    
    // Calculate intensity (0.0-1.0)
    let intensity = 0.5; // baseline
    
    if (beat.act === 1) {
      intensity = 0.3 + (index / beats.filter(b => b.act === 1).length) * 0.3;
    } else if (beat.act === 2) {
      const act2Progress = (week - beats.find(b => b.act === 2).week) / 
                           (beats.filter(b => b.act === 2).length);
      intensity = 0.6 + (act2Progress * 0.3);
    } else if (beat.act === 3) {
      const act3Progress = (week - beats.find(b => b.act === 3).week) / 
                           (beats.filter(b => b.act === 3).length);
      intensity = 0.9 - (act3Progress * 0.2); // Drop after climax
    }
    
    // Decisive decisions are peak intensity
    if (beat.beat_type === "DECISIVE_DECISION") {
      intensity = Math.max(intensity, 0.85);
    }
    
    pacing.weeks.push(week);
    pacing.intensity_curve.push(intensity);
    
    // Check for breathing room
    const previousBeat = beats[index - 1];
    if (previousBeat && (week - previousBeat.week) > 2) {
      pacing.breathing_room.push({
        weeks: [previousBeat.week + 1, week - 1],
        duration: week - previousBeat.week - 1,
        purpose: "Recovery and integration time"
      });
    }
  });
  
  // Validate pacing
  const validation = validatePacing(pacing, seasonLength);
  
  return { pacing, validation };
}

function validatePacing(pacing, seasonLength) {
  const issues = [];
  
  // Check for intensity plateaus (boring)
  const plateaus = findPlateaus(pacing.intensity_curve);
  if (plateaus.length > 0) {
    issues.push({
      type: "plateau",
      message: "Intensity plateaus detected",
      weeks: plateaus
    });
  }
  
  // Check for too-rapid escalation (exhausting)
  const rapidSpikes = findRapidSpikes(pacing.intensity_curve);
  if (rapidSpikes.length > 0) {
    issues.push({
      type: "rapid_escalation",
      message: "Intensity escalates too quickly",
      weeks: rapidSpikes
    });
  }
  
  // Check for adequate breathing room
  const totalBreathingWeeks = pacing.breathing_room.reduce((sum, br) => sum + br.duration, 0);
  const breathingPercentage = totalBreathingWeeks / seasonLength;
  
  if (breathingPercentage < 0.15) {
    issues.push({
      type: "insufficient_breathing_room",
      message: "Not enough recovery time between beats",
      recommendation: "Add 2-3 week gaps between major beats"
    });
  }
  
  return {
    valid: issues.length === 0,
    issues
  };
}
```

---

## Multi-Season Narrative Continuity

**Important:** This 3-act structure is for ONE season. Characters live through **8-10 seasons** total.

**Between Seasons:**
```
SEASON N ENDS (3-act arc complete)
↓
TIME SKIP (auto-generated narrative)
├─ Duration: 1 week to 10+ years
├─ Narrative bridges the gap
└─ World evolves logically
↓
SEASON N+1 BEGINS (new 3-act arc)
├─ New aspiration
├─ All relationships/skills carry forward
├─ References past season arcs
└─ New 3-act structure begins
```

**Narrative Implications:**
- Past season arcs can be referenced in new seasons
- NPCs age and evolve between seasons
- Decisive decisions from Season 1 might echo in Season 5
- Character transformation is visible across seasons
- Life Bookshelf creates one continuous saga (8-10 novels)

**Complete details:** See `73-season-flow-implementation.md` for inter-season narrative generation and continuity tracking.

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Vocabulary & Scales (Section 2)
- [x] Emotional capacity (0-10 scale) integrated into arc structure
- [x] OCEAN traits influence arc placement and beat intensity
- [x] Meters (0-10 scale) affect beat outcomes
- [x] Emotional states (20 states) progress logically through acts

### ✅ Turn Structure (Section 4)
- [x] Decisive decisions pause time (no FOMO)
- [x] Turn economy respected in beat placement
- [x] No anxiety-inducing real-time pressure

### ✅ Narrative Structure (Section 5)
- [x] Seasons are complete 3-act story arcs
- [x] Act structure scales to season length (12/24/36 weeks)
- [x] Foreshadowing provides 2-4 week preparation time
- [x] Pacing validated to avoid exhaustion
- [x] Breathing room built into structure (15%+ of season)

### ✅ Emotional Authenticity (Section 16) *(NEW in v1.2)*
- [x] **Emotional Journey Mapping:** Capacity curves defined per act (7.0 → 3.5 → 7.5 in 12w)
- [x] **Capacity Fluctuation Patterns:** Expected drain rates and recovery per arc phase
- [x] **Stressor Profiles:** Expected stressor counts per act (1-2 in Act 1, 2-5 in Act 2)
- [x] **Capacity-Aware Beat Placement:** Beats adjust based on estimated capacity
- [x] **Support Insertion:** NPC support beats added when capacity critically low
- [x] **Climax Requirements:** Minimum capacity (4.0) required for climax options

### ✅ Novel-Quality Narrative (Section 17) *(NEW in v1.2)*
- [x] **Memory Resonance Threading:** Within-season callbacks (2-4 per season)
- [x] **Cross-Season Callbacks:** Past season memories echo (1-2 major per season)
- [x] **Pattern Recognition:** Explicit tracking of repeated choices across seasons
- [x] **Memory Weight Decay:** Formula for memory persistence over time
- [x] **Trauma Triggers:** High-weight memories amplified in similar contexts (1.5x)
- [x] **Growth Callbacks:** Proof-of-progress moments (1.2x weight)
- [x] **Novel Integration:** Memory callbacks formatted as flashbacks in chapters

### ✅ AI Personality Integration (Section 13)
- [x] OCEAN traits influence complication intensity
- [x] Personality affects beat placement appropriateness
- [x] Character growth tracked across acts and seasons

### ✅ Archive & Persistence (Section 12)
- [x] Characters persist across 8-10 seasons (multi-season arcs)
- [x] Inter-season narrative continuity maintained
- [x] Memory system tracks across Life Bookshelf
- [x] Pattern tracking across character lifetime

### ✅ Multi-Season Continuity
- [x] 3-act structure applies to each season individually
- [x] Time skips between seasons with auto-generated narrative
- [x] Past season arcs referenced in new seasons
- [x] NPCs age and evolve between seasons
- [x] Decisive decisions from Season 1 can echo in Season 5+

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~560 lines** of new v1.2 content
2. **Emotional Journey Mapping:** Complete capacity curves for all three season lengths
3. **Capacity Fluctuation Patterns:** Expected trajectories from setup through resolution
4. **Memory Resonance Threading:** Within-season and cross-season callback systems
5. **Capacity-Aware Beat Placement:** Dynamic adjustment based on player state
6. **Pattern Recognition:** Explicit tracking of repeated choices across lifetime

**Design Principles:**
- Emotional capacity creates realistic constraint and stakes
- Memory resonance creates continuity and character depth
- Pattern recognition enables growth or stagnation narratives
- Stakes escalation creates drama, not just stat penalties
- Foreshadowing makes crises feel earned, not arbitrary
- Dramatic irony creates empathy and anticipation
- All tension serves 3-act structure and emotional authenticity

**References:**
- See `01-emotional-authenticity.md` for cross-system integration overview
- See `02-system-by-system-enhancement.md` for detailed gap analysis
- See `03-integrated-example.md` for concrete walkthrough
- See `14-emotional-state-mechanics.md` for emotional state system
- See `30-decisive-decision-templates.md` for decision scaffolding
- See `40-season-structure-spec.md` for season length details
- See `73-season-flow-implementation.md` for inter-season transitions
- See `35-tension-maintenance-system.md` for complete hook point and mystery systems

---

**This specification enables developers to implement the complete 3-act narrative structure with emotional journey mapping, capacity-aware beat placement, and memory resonance threading that creates authentic emotional arcs and multi-season character depth.**

