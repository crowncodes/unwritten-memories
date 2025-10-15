# Emotional Memory Tracking - Implementation Specification

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** System with Master Truths v1.2 memory resonance factors, recall priority, and emotional weight calculations

**References:**
- **Design Philosophy:** `1.concept/16-archive-persistence.md` (memory system philosophy)
- **Multi-Season:** `1.concept/22-multi-lifetime-continuity.md` (multi-season memory)
- **Decision System:** `30-decisive-decision-templates.md` (decision context)
- **Season Flow:** `73-season-flow-implementation.md` (memory across seasons)

---

## Overview

**The Problem:** Past decisions and emotional moments can feel disconnected from current gameplay. Players forget what happened 20 weeks ago. Emotional beats don't resonate because there's no connection to similar past experiences.

**The Solution:** "Emotional Echoes" - automatically surface relevant past memories during current emotionally significant moments. Make the past feel present and continuous.

**Core Principle:** Your character remembers. Past emotional experiences inform current moments, creating depth and continuity that feels like a real life being lived.

**Compliance:** master_truths v1.1 requires multi-season continuity where past seasons remain relevant to current experience.

---

## Emotional Echo System

### What Are Emotional Echoes?

**Definition:** Past high-emotion moments that resurface during similar current situations, adding context and emotional weight to present decisions.

**Implementation:** When player faces certain triggers (stress, success, choice, relationship moment), system searches memory for similar past experiences and surfaces 1-2 relevant memories.

---

### Emotional Echo Structure

```javascript
interface EmotionalEcho {
  echo_id: string;
  
  // Trigger conditions
  trigger_context: TriggerContext;
  trigger_emotion: EmotionType;
  trigger_situation: SituationType;
  
  // Source memory
  source_memory: Memory;
  memory_week: number;
  memory_season: number | null;      // null if same season
  time_ago: string;                   // "3 months ago", "Last year"
  
  // Echo content
  echo_type: "flashback" | "thought" | "feeling" | "comparison";
  echo_text: string;
  
  // Impact
  affects_current_moment: boolean;
  provides_context: boolean;
  emotional_weight: number;           // 0.0-1.0
  
  // Player experience
  display_as: "card" | "thought_overlay" | "decision_context";
  skippable: boolean;
}
```

---

## Trigger Contexts

### When Emotional Echoes Surface

```javascript
const EMOTIONAL_ECHO_TRIGGERS = {
  during_stress: {
    description: "Recall past similar stress and how you handled it",
    
    trigger_conditions: {
      emotional_state: ["OVERWHELMED", "EXHAUSTED", "DISCOURAGED"],
      or_meter_state: "mental < 3 OR emotional < 3",
      or_crisis: "active_crisis_event"
    },
    
    search_for_memories: {
      similar_emotions: ["OVERWHELMED", "EXHAUSTED", "DISCOURAGED", "ANXIOUS"],
      similar_situations: ["previous_crisis", "health_crisis", "financial_crisis"],
      minimum_weight: 6,
      time_range: "any - can be from years ago"
    },
    
    examples: [
      {
        current_situation: {
          week: 14,
          context: "Physical meter 2, working too hard, exhausted",
          player_state: "OVERWHELMED"
        },
        
        surfaced_memory: {
          from: "Season 1, Week 18",
          memory: "The last time you burned out - collapsed at work, hospitalized",
          time_ago: "2 years ago"
        },
        
        echo_text: `
          You're sitting at your desk. Hands shaking. Coffee not helping.
          
          This feels familiar.
          
          *Two years ago. Different job, same exhaustion. You pushed through. 
          Kept pushing. Until your body gave out.*
          
          *Hospital room. Marcus sitting next to you: "You scared us. Promise 
          you'll never do this again."*
          
          You promised. And here you are. Again.
          
          Same path. Same choices. Is this who you are?
        `,
        
        impact: {
          provides_context: "Reminds player of past consequences",
          emotional_weight: "Heavy - you've been here before",
          affects_decision: "More likely to slow down if they remember past crisis"
        }
      },
      {
        current_situation: {
          week: 8,
          context: "Financial crisis - can't pay rent",
          player_state: "ANXIOUS"
        },
        
        surfaced_memory: {
          from: "Season 2, Week 12",
          memory: "Last financial crisis - had to borrow from Marcus, felt shame",
          time_ago: "18 months ago"
        },
        
        echo_text: `
          Account balance: $487. Rent: $1200. You've been here before.
          
          *18 months ago. Same panic. Same calculator. Same sinking feeling.*
          
          *You borrowed from Marcus. He was kind. You were grateful. But that 
          awkwardness... not asking for help again. Not if you can avoid it.*
          
          What are your options this time?
        `,
        
        impact: {
          informs_choice: "Player remembers borrowing from Marcus before",
          emotional_context: "Already experienced that option and its consequences",
          might_choose_differently: "Might try different solution this time"
        }
      }
    ]
  },
  
  during_success: {
    description: "Remember who believed in you when no one else did",
    
    trigger_conditions: {
      event_type: "success_moment",
      examples: ["gallery_showing", "business_launch", "promotion", "aspiration_complete"]
    },
    
    search_for_memories: {
      similar_emotions: ["HOPEFUL", "MOTIVATED", "UNCERTAIN"],
      npc_support_memories: true,
      early_season_memories: true,
      minimum_weight: 5
    },
    
    examples: [
      {
        current_situation: {
          week: 20,
          context: "Gallery showing opening night - your photography is displayed",
          player_state: "JOYFUL but NERVOUS"
        },
        
        surfaced_memory: {
          from: "Week 4, same season",
          memory: "Sarah seeing your photos for first time, saying 'These are beautiful. You could really do this.'",
          time_ago: "4 months ago"
        },
        
        echo_text: `
          Gallery lights. Your photos on walls. People looking at YOUR work.
          
          *Four months ago. Sarah's apartment. Showing her your portfolio, 
          nervous, uncertain.*
          
          *Sarah: "These are beautiful. You could really do this. I mean it."*
          
          *You weren't sure. She was.*
          
          And here you are. She was right.
          
          You scan the room. There she is. Smiling. She knew before you did.
        `,
        
        impact: {
          emotional_payoff: "Success feels earned because you remember the journey",
          relationship_deepened: "Remember who supported you at the start",
          gratitude_moment: "Want to thank Sarah, acknowledge her belief in you"
        }
      }
    ]
  },
  
  during_choice: {
    description: "Past similar decisions and their outcomes haunt current choice",
    
    trigger_conditions: {
      event_type: "decisive_decision",
      or_major_choice: true
    },
    
    search_for_memories: {
      similar_decision_type: true,
      regret_tagged_memories: true,
      success_tagged_memories: true,
      minimum_weight: 7
    },
    
    examples: [
      {
        current_situation: {
          week: 18,
          decision: "Work overtime for bonus OR attend friend's important event",
          dilemma: "Career vs. relationship - which matters more?"
        },
        
        surfaced_memory: {
          from: "Season 1, Week 8",
          memory: "Chose work over Sarah's bookshop opening - she was hurt, relationship damaged",
          time_ago: "3 years ago",
          tagged: "regret"
        },
        
        echo_text: `
          DECISION: Work overtime for $1500 bonus OR Sarah's engagement party
          
          *You've made this choice before.*
          
          *Three years ago. Sarah's bookshop opening. You promised you'd be there. 
          Then your boss offered overtime. You chose work.*
          
          *Sarah's face when you texted: "Something came up at work. So sorry."*
          
          *The money was nice. But you still remember that look. The photos on 
          Instagram - everyone there except you. The way things were different 
          after that.*
          
          Work or life. Career or people. You've been here before.
          
          How did that work out last time?
        `,
        
        impact: {
          provides_context: "Remember consequences of similar past choice",
          creates_weight: "This decision carries history",
          might_choose_differently: "Learned from past regret"
        },
        
        display_in_decision: {
          show_as_context: true,
          placement: "Before choice options presented",
          reminder: "Past experiences inform present choices"
        }
      },
      {
        current_situation: {
          week: 22,
          decision: "Take safe job offer OR pursue risky business venture"
        },
        
        surfaced_memory: {
          from: "Season 2, Week 16",
          memory: "Last time you played it safe, felt regret for not taking risk",
          time_ago: "2 years ago",
          tagged: "regret, opportunity_missed"
        },
        
        echo_text: `
          DECISION: Safe $75k job OR Launch photography business
          
          *Two years ago. Similar choice. Dream vs. security.*
          
          *You chose security. Stayed at corporate job. Paid the bills. Played 
          it safe.*
          
          *And you regretted it. Every. Single. Day.*
          
          *Watched other photographers succeed. Watched your portfolio gather 
          dust. Watched the dream shrink.*
          
          Here's the choice again. Different context. Same fear.
          
          What did playing it safe cost you last time?
        `,
        
        impact: {
          learned_from_past: "Safety led to regret last time",
          might_take_risk: "Past informs present - maybe choose differently",
          emotional_weight: "Can't make same mistake twice"
        }
      }
    ]
  },
  
  during_relationship_moment: {
    description: "Recall formative moment with that person",
    
    trigger_conditions: {
      event_type: "relationship_milestone",
      examples: ["level_up", "confrontation", "vulnerable_conversation", "betrayal", "reunion"]
    },
    
    search_for_memories: {
      filter_by_npc: "specific_npc_only",
      early_relationship_memories: true,
      high_emotion_moments: true,
      minimum_weight: 6
    },
    
    examples: [
      {
        current_situation: {
          week: 22,
          context: "Sarah finally opens up about David's death",
          relationship_milestone: "Level 4 → Level 5 (soulmate)"
        },
        
        surfaced_memory: {
          from: "Week 2, same season",
          memory: "First time meeting Sarah at café, she mentioned David and changed subject",
          time_ago: "5 months ago"
        },
        
        echo_text: `
          Sarah is crying. Telling you about David. Finally.
          
          *Five months ago. Different café, same Sarah. She mentioned his name 
          once - just once - and you saw pain flash across her face before she 
          changed the subject.*
          
          *You wondered who David was. What happened. Why she wouldn't talk about it.*
          
          *All these months. All the times she pulled away. All the distance 
          that felt personal but wasn't.*
          
          It all makes sense now.
          
          *First date. Week 2. Mystery planted. Week 22. Mystery revealed.*
          
          Five months to trust you with this. Five months you've been waiting 
          without realizing you were waiting.
        `,
        
        impact: {
          recontextualizes_relationship: "Entire friendship/romance makes sense retroactively",
          emotional_payoff: "Mystery resolved, depth revealed",
          relationship_deepened: "Trust earned over months pays off"
        }
      }
    ]
  }
};
```

---

## Memory Tagging System

### High-Emotion Moments Auto-Tagged

```javascript
interface MemoryTag {
  memory_id: string;
  
  // Automatic tags (generated by system)
  emotional_weight: number;            // 0-10
  emotion_type: EmotionType[];         // Multiple emotions possible
  situation_type: SituationType[];
  
  // Context tags
  season: number;
  week: number;
  npcs_involved: string[];
  
  // Echo eligibility
  echo_eligible: boolean;
  echo_priority: number;                // Higher = more likely to surface
  
  // Manual tags (designer-specified)
  special_tags: SpecialTag[];
}

const SPECIAL_TAGS = {
  regret: "Player expressed/felt regret about this choice",
  success: "Major achievement or victory",
  failure: "Major setback or failure",
  relationship_defining: "Changed dynamic with NPC",
  life_changing: "Major life event",
  lesson_learned: "Character grew from this",
  opportunity_missed: "Passed up significant chance",
  trauma: "Painful experience with lasting impact"
};
```

---

### Auto-Tagging Rules

```javascript
const AUTO_TAGGING_RULES = {
  emotional_weight_calculation: {
    decisive_decision: "weight 8-10 (always high)",
    crisis_event: "weight 7-9",
    relationship_milestone: "weight 6-8",
    success_moment: "weight 6-8",
    failure_moment: "weight 7-9",
    routine_event: "weight 1-3"
  },
  
  echo_eligibility: {
    minimum_weight: 5,
    exceptions: [
      "First interaction with major NPC (always eligible, even if weight 4)",
      "Decisive decisions (always eligible)",
      "Crisis events (always eligible)"
    ]
  },
  
  echo_priority_factors: {
    recency: "More recent = lower priority (let time pass first)",
    relevance: "More similar to current situation = higher priority",
    emotional_resonance: "Higher weight = higher priority",
    npc_match: "Same NPC involved = much higher priority"
  }
};
```

---

## Multi-Season Memory Persistence

### Memories Echo Across Seasons

**Key Feature:** Season 2 decisions can resurface in Season 5. Character remembers their entire life.

```javascript
const MULTI_SEASON_ECHO_SYSTEM = {
  memory_scope: "All past seasons accessible",
  
  time_references: {
    same_season: "3 months ago",
    last_season: "Last year",
    two_seasons_ago: "2 years ago",
    many_seasons_ago: "Years ago"
  },
  
  examples: [
    {
      current_situation: "Season 5, Week 10 - Considering marriage proposal",
      
      echo_from_season_2: {
        memory: "Season 2 decisive decision - Chose career over relationship, person left",
        time_ago: "4 years ago",
        echo_text: `
          You're holding the ring box. [NPC] is waiting for an answer.
          
          *Four years ago. Different person. Similar choice.*
          
          *You chose your career. They left. You told yourself it was the right 
          choice. That relationships could wait. That there would be others.*
          
          *There were others. But that decision... you think about it more than 
          you admit.*
          
          What if this time you choose differently?
        `
      },
      
      impact: "Past season's decision informs current major life choice",
      continuity: "Character's life feels continuous across years"
    },
    {
      current_situation: "Season 7, Week 4 - Physical health low, overworking",
      
      echo_from_season_1: {
        memory: "Season 1 health crisis - Collapsed at work, hospitalized",
        time_ago: "8 years ago",
        echo_text: `
          Hands shaking. Coffee not helping. You've been here before.
          
          *Eight years ago. Younger. More reckless. Same pattern.*
          
          *You promised yourself after that hospital stay: Never again.*
          
          *And yet.*
          
          Patterns. You fall back into them. Even knowing better.
        `
      },
      
      impact: "Long-term pattern recognition - character sees their own recurring issues",
      growth: "Player can choose to break pattern this time, showing character evolution"
    }
  ],
  
  implementation: {
    archive_integration: true,
    novel_references: "Echoes can reference moments that became novel chapters",
    compressed_memories: "Older memories may be summary form (50:1 compression) but still accessible",
    emotional_core_preserved: "High-weight memories always preserved in detail"
  }
};
```

---

## Implementation Guidelines

### Echo Generation Algorithm

```javascript
function generateEmotionalEcho(currentContext) {
  // 1. Identify trigger type
  const triggerType = identifyTrigger(currentContext);
  if (!triggerType) return null;
  
  // 2. Search memory for relevant experiences
  const relevantMemories = searchMemories({
    trigger: triggerType,
    emotion_match: currentContext.emotion,
    situation_match: currentContext.situation,
    npc_match: currentContext.npcs,
    minimum_weight: 5,
    time_range: "all_seasons"
  });
  
  if (relevantMemories.length === 0) return null;
  
  // 3. Prioritize memories
  const prioritizedMemories = prioritizeByRelevance(relevantMemories, currentContext);
  
  // 4. Select best match (1-2 memories max)
  const selectedMemory = prioritizedMemories[0];
  
  // 5. Generate echo text
  const echoText = generateEchoNarrative({
    current: currentContext,
    past: selectedMemory,
    time_gap: calculateTimeGap(selectedMemory.week, selectedMemory.season),
    connection: identifyConnection(currentContext, selectedMemory)
  });
  
  // 6. Create echo
  return {
    echo_id: generateID(),
    source_memory: selectedMemory,
    echo_text: echoText,
    trigger_context: currentContext,
    display_as: determineDisplay(currentContext.event_type),
    emotional_weight: selectedMemory.emotional_weight * relevanceScore
  };
}
```

---

### Display Methods

```javascript
const ECHO_DISPLAY_METHODS = {
  flashback_card: {
    when: "Major decision or crisis",
    format: "Full card with narrative",
    skippable: false,
    example: "During decisive decision, show full memory of similar past choice"
  },
  
  thought_overlay: {
    when: "Routine moments with emotional relevance",
    format: "Brief italicized thought",
    skippable: true,
    example: "*You've been here before. Last time didn't end well.*"
  },
  
  decision_context: {
    when: "Decisive decisions",
    format: "Additional context section showing relevant past",
    placement: "Before options presented",
    example: "Last time you chose work over relationships..."
  },
  
  conversation_reference: {
    when: "NPC references past event",
    format: "NPC brings up memory in dialogue",
    example: "Marcus: 'Remember when you collapsed at work? Don't do that again.'"
  }
};
```

---

## Regret System Integration

### Tracking Regret Across Time

```javascript
const REGRET_TRACKING = {
  identification: {
    player_expresses_regret: "Direct choice like 'I regret that'",
    negative_outcome: "Choice led to bad consequences player saw",
    opportunity_missed: "Watched someone else succeed at what you passed up",
    relationship_damaged: "Choice hurt important relationship"
  },
  
  regret_tag_added: {
    to_memory: true,
    increases_echo_priority: true,
    triggers_later_references: "NPCs or situations reference the regret"
  },
  
  regret_callbacks: {
    frequency: "Appropriate moments only, not constant",
    examples: [
      "Similar choice appears - remember regret from last time",
      "Anniversary of regretted decision",
      "See consequences of that choice still affecting life",
      "NPC brings it up in conversation"
    ]
  },
  
  example: {
    regretted_decision: "Season 2, Week 8 - Chose work over Sarah's bookshop opening",
    
    callbacks_over_time: [
      "Season 2, Week 20: See Sarah's bookshop, feel pang of regret that you weren't there for opening",
      "Season 3, Week 5: Similar work vs. friend choice appears, remember last regret",
      "Season 4, Week 12: Sarah mentions opening day, you feel guilt",
      "Season 6, Week 18: Decisive decision - this time choose friend over work, break pattern"
    ]
  }
};
```

---

## Master Truths v1.2: Memory Resonance Factors *(NEW)*

### Five Resonance Types with Weighted Recall

**Core Principle:** Not all memories surface equally. Master Truths v1.2 Section 17 defines 5 resonance types with specific weights (0.7-0.95) that amplify memory recall probability.

```javascript
const MEMORY_RESONANCE_SYSTEM = {
  purpose: "Determine which memories surface and when based on emotional resonance",
  threshold: "Base memory weight 5+ to be echo-eligible, resonance factors multiply likelihood",
  
  resonance_types: {
    
    type_1_past_trauma_trigger: {
      weight: 0.95,  // Highest resonance
      description: "Current situation mirrors past traumatic experience",
      
      trigger_conditions: {
        similar_stressor_type: true,
        similar_emotional_state: true,
        similar_circumstances: true
      },
      
      example: {
        past_memory: {
          season: 1,
          week: 18,
          event: "Burnout collapse - hospitalized after overworking",
          emotional_weight: 9,
          tagged: ["trauma", "health_crisis", "regret"]
        },
        
        current_situation: {
          season: 3,
          week: 14,
          state: "Physical meter 2, working 70 hours/week, exhausted",
          stressor_match: "Health neglect + overwork pattern"
        },
        
        resonance_calculation: {
          base_memory_weight: 9,
          situation_similarity: 0.95,
          trauma_amplification: 0.95,
          
          recall_probability: "base * similarity * amplification",
          final_probability: 9 * 0.95 * 0.95 = 8.12,  // Very high
          
          surfaces_as: "Vivid flashback, warning signal"
        },
        
        echo_text: `
          Hands shaking. Coffee not helping. This feels familiar.
          
          *Two years ago. Hospital bed. Marcus's face. "Promise you won't do this again."*
          
          You promised. And here you are. Same pattern. Same choices.
          
          Your body remembers what your mind tried to forget.
        `
      },
      
      gameplay_effect: "Strong warning, player likely to change behavior if they remember trauma"
    },
    
    type_2_emotional_growth_callback: {
      weight: 0.85,
      description: "Current situation allows applying lesson learned from past experience",
      
      trigger_conditions: {
        similar_decision_type: true,
        past_mistake_available_to_correct: true,
        player_expressed_regret_previously: true
      },
      
      example: {
        past_memory: {
          season: 2,
          week: 8,
          event: "Chose work over Sarah's bookshop opening - regret",
          emotional_weight: 7,
          tagged: ["regret", "opportunity_missed", "relationship_damage"]
        },
        
        current_situation: {
          season: 3,
          week: 18,
          state: "Decision: Work overtime OR attend Sarah's engagement party"
        },
        
        resonance_calculation: {
          base_memory_weight: 7,
          decision_similarity: 0.90,
          growth_opportunity: 0.85,
          
          recall_probability: 7 * 0.90 * 0.85 = 5.36,  // High
          
          surfaces_as: "Reflective echo, chance to choose differently"
        },
        
        echo_text: `
          Work or Sarah. You've been here before.
          
          *Two years ago. Her bookshop opening. You chose work.*
          
          *The money was nice. But you still remember that look.*
          *The way things were different after that.*
          
          This is your chance to learn. To choose differently.
          
          What do you want to be? The person who chose work? Or the person who learned?
        `,
        
        player_choice_moment: true,
        demonstrates_growth_if: "Player chooses Sarah this time"
      },
      
      gameplay_effect: "Creates growth moment, shows character evolution across seasons"
    },
    
    type_3_relationship_milestone_echo: {
      weight: 0.80,
      description: "Current milestone triggers memory of relationship origin or formative moment",
      
      trigger_conditions: {
        relationship_event: ["level_up", "major_reveal", "confrontation", "celebration"],
        npc_match: true,
        early_relationship_memory: true
      },
      
      example: {
        past_memory: {
          season: 1,
          week: 2,
          event: "First meeting with Sarah at café, she mentioned David briefly",
          emotional_weight: 6,
          tagged: ["relationship_defining", "mystery_planted"]
        },
        
        current_situation: {
          season: 1,
          week: 22,
          state: "Sarah finally opens up completely about David's death",
          relationship_milestone: "Level 3 → Level 4"
        },
        
        resonance_calculation: {
          base_memory_weight: 6,
          npc_match: 1.0,  // Same NPC
          milestone_significance: 0.80,
          
          recall_probability: 6 * 1.0 * 0.80 = 4.8,  // Moderate-high
          
          surfaces_as: "Contextual callback, narrative payoff"
        },
        
        echo_text: `
          Sarah is crying. Telling you about David. Finally.
          
          *Twenty weeks ago. This café. Different table, same Sarah.*
          *She mentioned his name once. Pain flashed across her face.*
          *Then she changed the subject.*
          
          *All these weeks. All the times she pulled away.*
          *It was never about you.*
          
          Twenty weeks to trust you with this. Twenty weeks you've been waiting 
          without knowing you were waiting.
        `,
        
        narrative_payoff: "Recontextualizes entire relationship, emotional release"
      },
      
      gameplay_effect: "Deepens relationship moments, shows relationship journey"
    },
    
    type_4_success_origin_recall: {
      weight: 0.75,
      description: "During success, remember who believed when you didn't",
      
      trigger_conditions: {
        current_success: true,
        past_support_moment: true,
        early_encouragement_memory: true
      },
      
      example: {
        past_memory: {
          season: 1,
          week: 4,
          event: "Sarah: 'These photos are beautiful. You could really do this.'",
          emotional_weight: 5,
          tagged: ["encouragement", "relationship_moment", "aspiration_support"]
        },
        
        current_situation: {
          season: 1,
          week: 20,
          state: "Gallery showing success - your photos on walls, people admiring"
        },
        
        resonance_calculation: {
          base_memory_weight: 5,
          success_trigger: 0.90,
          gratitude_amplification: 0.75,
          
          recall_probability: 5 * 0.90 * 0.75 = 3.38,  // Moderate
          
          surfaces_as: "Gratitude moment, emotional recognition"
        },
        
        echo_text: `
          Gallery lights. Your photos on walls. People looking at YOUR work.
          
          *Four months ago. Sarah's apartment. Nervous, uncertain.*
          *Sarah: "These are beautiful. You could really do this. I mean it."*
          
          *You weren't sure. She was.*
          
          And here you are. She was right.
          
          You scan the room. There she is. Smiling. She knew before you did.
        `,
        
        creates_gratitude: true,
        relationship_deepened: "Want to thank Sarah, acknowledge her belief"
      },
      
      gameplay_effect: "Makes success feel earned, acknowledges support network"
    },
    
    type_5_parallel_situation_pattern: {
      weight: 0.70,  // Lowest resonance
      description: "Current situation vaguely similar to past experience",
      
      trigger_conditions: {
        situation_type_match: true,
        emotional_parallels: true,
        not_exact_match: true
      },
      
      example: {
        past_memory: {
          season: 2,
          week: 12,
          event: "Financial crisis - had to borrow from Marcus, felt shame",
          emotional_weight: 6,
          tagged: ["financial_stress", "asking_for_help", "shame"]
        },
        
        current_situation: {
          season: 3,
          week: 8,
          state: "Different financial crisis - rent short again"
        },
        
        resonance_calculation: {
          base_memory_weight: 6,
          situation_similarity: 0.75,
          pattern_recognition: 0.70,
          
          recall_probability: 6 * 0.75 * 0.70 = 3.15,  // Low-moderate
          
          surfaces_as: "Brief thought, pattern awareness"
        },
        
        echo_text: `
          Account balance: $487. Rent: $1200. You've been here before.
          
          *18 months ago. Same panic. Same calculator.*
          *You borrowed from Marcus. He was kind. But that awkwardness...*
          
          What are your options this time?
        `,
        
        informs_choice: "Player remembers past solution and its consequences"
      },
      
      gameplay_effect: "Creates continuity, shows life patterns"
    }
  },
  
  design_principle: "Higher resonance = stronger memory recall. Trauma and growth highest, patterns lowest."
};
```

---

## Master Truths v1.2: Resonance Calculation Examples *(NEW)*

### Step-by-Step Memory Recall Probability

```javascript
const RESONANCE_CALCULATION_SYSTEM = {
  
  formula: "recall_probability = base_weight * situation_match * resonance_factor",
  
  threshold: "recall_probability >= 3.0 to surface as echo",
  
  example_1_high_resonance: {
    memory: {
      event: "Season 1, Week 18: Burnout collapse",
      base_weight: 9,
      type: "trauma"
    },
    
    current_context: {
      week: "Season 3, Week 14",
      situation: "Physical meter 2, overworking again",
      similarity: 0.95  // Very similar
    },
    
    calculation: {
      base_weight: 9,
      situation_match: 0.95,
      resonance_factor: 0.95,  // Type 1: Past trauma trigger
      
      recall_probability: 9 * 0.95 * 0.95,
      final_score: 8.12,
      
      result: "SURFACES - Very high probability, vivid flashback"
    }
  },
  
  example_2_moderate_resonance: {
    memory: {
      event: "Season 1, Week 4: Sarah encourages photography",
      base_weight: 5,
      type: "support_moment"
    },
    
    current_context: {
      week: "Season 1, Week 20",
      situation: "Gallery success, celebrating achievement",
      similarity: 0.90
    },
    
    calculation: {
      base_weight: 5,
      situation_match: 0.90,
      resonance_factor: 0.75,  // Type 4: Success origin recall
      
      recall_probability: 5 * 0.90 * 0.75,
      final_score: 3.38,
      
      result: "SURFACES - Moderate probability, gratitude moment"
    }
  },
  
  example_3_low_resonance_no_surface: {
    memory: {
      event: "Season 2, Week 6: Routine coffee with Sarah",
      base_weight: 3,
      type: "routine"
    },
    
    current_context: {
      week: "Season 3, Week 10",
      situation: "Another coffee date, nothing special",
      similarity: 0.80
    },
    
    calculation: {
      base_weight: 3,
      situation_match: 0.80,
      resonance_factor: 0.70,  // Type 5: Parallel situation
      
      recall_probability: 3 * 0.80 * 0.70,
      final_score: 1.68,
      
      result: "DOES NOT SURFACE - Below 3.0 threshold, too routine"
    }
  },
  
  example_4_high_weight_low_match: {
    memory: {
      event: "Season 1, Week 12: Traumatic breakup",
      base_weight: 8,
      type: "relationship_trauma"
    },
    
    current_context: {
      week: "Season 3, Week 15",
      situation: "Starting new relationship, unrelated to breakup",
      similarity: 0.40  // Not very similar
    },
    
    calculation: {
      base_weight: 8,
      situation_match: 0.40,
      resonance_factor: 0.95,  // Type 1: Trauma (but low match)
      
      recall_probability: 8 * 0.40 * 0.95,
      final_score: 3.04,
      
      result: "BARELY SURFACES - Just above threshold, brief thought"
    }
  }
};
```

---

## Master Truths v1.2: Memory Recall Priority System *(NEW)*

### When Multiple Memories Could Surface, Which One?

**Core Principle:** If multiple memories meet threshold, prioritize by: Resonance > Recency > Emotional Weight > NPC Match

```javascript
const MEMORY_RECALL_PRIORITY = {
  
  decision_algorithm: function(eligibleMemories, currentContext) {
    // Step 1: Calculate recall probability for all eligible memories
    const scored_memories = eligibleMemories.map(memory => ({
      ...memory,
      recall_score: calculateRecallProbability(memory, currentContext)
    }));
    
    // Step 2: Filter by threshold
    const above_threshold = scored_memories.filter(m => m.recall_score >= 3.0);
    
    if (above_threshold.length === 0) return null;
    if (above_threshold.length === 1) return above_threshold[0];
    
    // Step 3: Multiple memories eligible - prioritize
    const prioritized = above_threshold.sort((a, b) => {
      // Priority 1: Recall score (highest)
      if (Math.abs(a.recall_score - b.recall_score) > 0.5) {
        return b.recall_score - a.recall_score;
      }
      
      // Priority 2: Recency (more recent = lower priority, want meaningful not just recent)
      const recency_diff = (currentContext.week - a.week) - (currentContext.week - b.week);
      if (Math.abs(recency_diff) > 10) {
        return recency_diff;  // Older memory preferred if scores similar
      }
      
      // Priority 3: Emotional weight (higher weight)
      if (Math.abs(a.emotional_weight - b.emotional_weight) > 1) {
        return b.emotional_weight - a.emotional_weight;
      }
      
      // Priority 4: NPC match (same NPC involved)
      if (currentContext.npc && a.npcs_involved.includes(currentContext.npc) && !b.npcs_involved.includes(currentContext.npc)) {
        return -1;
      }
      
      return 0;
    });
    
    return prioritized[0];
  },
  
  example_prioritization: {
    context: {
      week: 24,
      situation: "Decision: Career vs friend",
      npc: "Sarah"
    },
    
    eligible_memories: [
      {
        id: "memory_1",
        event: "Week 8: Chose work over Sarah's bookshop opening",
        week: 8,
        emotional_weight: 7,
        resonance_type: "emotional_growth_callback",
        resonance_factor: 0.85,
        npcs_involved: ["Sarah"],
        
        recall_score: 7 * 0.95 * 0.85 = 5.65
      },
      {
        id: "memory_2",
        event: "Week 12: Chose work over Marcus's birthday",
        week: 12,
        emotional_weight: 6,
        resonance_type: "parallel_situation",
        resonance_factor: 0.70,
        npcs_involved: ["Marcus"],
        
        recall_score: 6 * 0.85 * 0.70 = 3.57
      },
      {
        id: "memory_3",
        event: "Week 20: Successful work project after sacrifice",
        week: 20,
        emotional_weight: 5,
        resonance_type: "parallel_situation",
        resonance_factor: 0.70,
        npcs_involved: [],
        
        recall_score: 5 * 0.75 * 0.70 = 2.63  // Below threshold
      }
    ],
    
    prioritization_process: {
      step_1: "Memory 3 filtered out (below 3.0 threshold)",
      step_2: "Memory 1 vs Memory 2",
      step_3: "Memory 1 wins: Higher recall score (5.65 vs 3.57)",
      step_4: "Also: NPC match (Sarah), higher emotional weight, growth opportunity",
      
      selected_memory: "memory_1",
      
      surfaces_as: `
        DECISION: Career vs Sarah
        
        *You've been here before.*
        
        *Week 8. Sarah's bookshop opening. You chose work.*
        *The money was nice. But you still remember that look.*
        
        Work or Sarah. What did you choose last time? How did that work out?
      `
    }
  },
  
  edge_cases: {
    too_many_memories: {
      situation: "Player has 5+ memories all above threshold",
      solution: "Limit to top 2 memories maximum, show sequentially if needed"
    },
    
    recent_memories: {
      situation: "Memory from last week surfaces",
      solution: "Reduce priority unless very high resonance (trauma/growth)",
      rationale: "Player remembers recent events naturally, echoes are for older memories"
    },
    
    season_boundaries: {
      situation: "Memory from past season",
      solution: "Add 'time ago' context ('2 years ago')",
      bonus: "Cross-season memories feel more profound due to time passed"
    }
  },
  
  frequency_limits: {
    max_echoes_per_week: 2,
    min_weeks_between_echoes: 2,
    never_during: ["Act III climax", "decision already overwhelming"],
    
    rationale: "Echoes are powerful, overuse dilutes impact"
  }
};
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Memory System (v1.1 Foundation)
- [x] Multi-season memory persistence (memories carry across character's life)
- [x] High-emotion moments (weight 7+) automatically tracked
- [x] Echoes surface during appropriate triggers (not random)
- [x] Past decisions remain relevant to present choices
- [x] Character growth visible through pattern recognition
- [x] Novel generation integrates emotional echoes
- [x] Regret system creates meaningful long-term consequences
- [x] Memory tagging system (trauma, success, failure, etc.)
- [x] Emotional echo structure with context and impact

### ✅ Master Truths v1.2: Memory Resonance Enhancements *(NEW)*
- [x] **Five Resonance Types with Weights (0.7-0.95)**
  - Type 1: Past Trauma Trigger (0.95) - highest resonance
  - Type 2: Emotional Growth Callback (0.85) - learn from mistakes
  - Type 3: Relationship Milestone Echo (0.80) - origin callbacks
  - Type 4: Success Origin Recall (0.75) - gratitude moments
  - Type 5: Parallel Situation Pattern (0.70) - lowest resonance
- [x] **Resonance Calculation Formula**
  - recall_probability = base_weight * situation_match * resonance_factor
  - Threshold: ≥ 3.0 to surface as echo
  - Example: Trauma (9 * 0.95 * 0.95 = 8.12) SURFACES
  - Example: Routine (3 * 0.80 * 0.70 = 1.68) DOES NOT SURFACE
- [x] **Memory Recall Priority System**
  - Priority 1: Recall score (highest wins)
  - Priority 2: Recency (older preferred for similar scores)
  - Priority 3: Emotional weight (higher wins)
  - Priority 4: NPC match (same NPC preferred)
  - Frequency limits: Max 2 echoes/week, min 2 weeks between

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~550 lines** of new v1.2 memory mechanics
2. **5 resonance types** - trauma (0.95), growth (0.85), relationship (0.80), success (0.75), pattern (0.70)
3. **Resonance calculations** - base_weight * situation_match * resonance_factor ≥ 3.0
4. **Priority algorithm** - handles multiple eligible memories with 4-tier prioritization
5. **Comprehensive examples** - trauma flashback (8.12), growth callback (5.36), routine ignored (1.68)
6. **Frequency limits** - prevents echo fatigue (max 2/week, min 2 weeks between)

**Five Resonance Types:**
1. **Past Trauma Trigger (0.95)** - "Hospital bed. Marcus's face. 'Promise you won't do this again.'"
2. **Emotional Growth Callback (0.85)** - "Work or Sarah. You've been here before. Choose differently this time?"
3. **Relationship Milestone Echo (0.80)** - "Twenty weeks to trust you. Twenty weeks you've been waiting."
4. **Success Origin Recall (0.75)** - "Sarah: 'You could really do this.' She knew before you did."
5. **Parallel Situation Pattern (0.70)** - "You've been here before. 18 months ago. Same panic."

**Calculation Examples:**
- Trauma: 9 * 0.95 * 0.95 = 8.12 (SURFACES - vivid flashback)
- Growth: 7 * 0.90 * 0.85 = 5.36 (SURFACES - reflective echo)
- Success: 5 * 0.90 * 0.75 = 3.38 (SURFACES - gratitude moment)
- Pattern: 6 * 0.75 * 0.70 = 3.15 (SURFACES - brief thought)
- Routine: 3 * 0.80 * 0.70 = 1.68 (DOES NOT SURFACE - below threshold)

**Priority System:**
When multiple memories eligible:
1. Highest recall score wins
2. Older memory preferred (if scores within 0.5)
3. Higher emotional weight wins (if recency similar)
4. NPC match preferred (if all else equal)

**Design Principles:**
- Memories make character feel continuous across years
- Past informs present, creating emotional weight
- Echoes are contextual, not constant (maintains impact)
- Trauma and growth memories surface most strongly
- Regrets can be revisited and potentially resolved
- Multi-season continuity shows character evolution
- High-weight memories preserved forever

**References:**
- See `01-emotional-authenticity.md` for cross-system integration and memory resonance in broader context
- See `12-success-probability-formulas.md` for memory resonance modifiers in success calculations
- See `30-decisive-decision-templates.md` for decision context integration
- See `31-narrative-arc-scaffolding.md` for emotional beat placement
- See `1.concept/16-archive-persistence.md` for memory system philosophy
- See `1.concept/22-multi-lifetime-continuity.md` for multi-season tracking
- See `73-season-flow-implementation.md` for memory across season transitions

---

**This specification enables developers to implement emotional memory tracking with Master Truths v1.2 enhancements: 5 weighted resonance types (0.7-0.95) that determine which memories surface when, precise recall probability calculations with ≥ 3.0 threshold, and a 4-tier priority system for handling multiple eligible memories - creating continuity across seasons where past decisions continuously inform present choices with authentic emotional weight.**

