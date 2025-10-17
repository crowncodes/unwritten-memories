# Turn Structure V2: Just-in-Time Card Generation

**Document Status**: V3 Canonical Reference  
**Last Updated**: October 17, 2025  
**Authority Level**: Master Truth

---

## 1. Core Philosophy: Fluid Time, Dynamic Generation

**The V1 Problem:**
- Rigid "Morning/Afternoon/Evening" phases
- Pre-generated static deck
- Time felt gamified, not authentic

**The V2 Solution:**
- **Fluid time progression** based on actual activity duration
- **Just-in-Time generation** from Master Templates via CFP
- **Predictive pre-fetching** to mask cloud latency
- **Adaptive pacing** where AI decides zoom vs. montage

**The Result:**
> Days feel like days. Cards are unique every time. Players manage a life, not fill slots.

---

## 2. The Contextually Filtered Pool (CFP)

### Critical Understanding

**The CFP is NOT a deck of cards. It is a dynamic weighted probability list of Master Templates.**

```javascript
const CFP = {
  type: "Weighted probability distribution",
  contains: "Master Template IDs + current probability weights",
  updates: "Incrementally when affected variables change",
  size: "~50-200 templates at any given time"
};
```

### CFP Structure

```javascript
{
  templates: [
    {
      id: "ACT_Connect_Informal_Social",
      base_probability: 0.15,
      current_weight: 0.28,  // Modified by context
      
      modifiers_active: {
        "weekend": +0.25,
        "LONELY_state": +0.40,
        "neglected_relationship": +0.60
      },
      
      calculation: "0.15 * (1 + 0.25 + 0.40 + 0.60) = 0.3375 (normalized to 0.28)"
    },
    
    {
      id: "ACT_Work_On_Project",
      base_probability: 0.25,
      current_weight: 0.15,
      
      modifiers_active: {
        "weekend": -0.40,
        "CURIOUS_state": +0.10
      },
      
      calculation: "0.25 * (1 - 0.40 + 0.10) = 0.175 (normalized to 0.15)"
    }
    
    // ... 50-200 templates total
  ],
  
  total_probability_mass: 1.0  // Always normalized
}
```

### Incremental Update Strategy

**Problem:** Recalculating 300 templates every state change is expensive.

**Solution:** Only update templates affected by the specific change.

```javascript
const UPDATE_STRATEGY = {
  
  emotional_state_change: {
    trigger: "Capacity crosses threshold or state card applied",
    
    affected_templates: "Query: templates with emotional_state modifiers",
    
    process: [
      "1. Identify which templates reference this emotional state",
      "2. Recalculate only those template weights",
      "3. Renormalize total probability mass"
    ],
    
    typical_count: "15-30 templates affected",
    performance: "< 5ms"
  },
  
  time_of_day_change: {
    trigger: "Time crosses category boundary (morning → afternoon)",
    
    affected_templates: "Query: templates with temporal modifiers",
    
    typical_count: "40-60 templates affected",
    performance: "< 8ms"
  },
  
  relationship_interaction: {
    trigger: "Card with specific NPC resolves",
    
    affected_templates: "Query: templates referencing that NPC + social category",
    
    typical_count: "10-20 templates affected",
    performance: "< 3ms"
  },
  
  financial_status_change: {
    trigger: "Money crosses threshold or financial crisis triggered",
    
    affected_templates: "Query: templates with money costs or financial modifiers",
    
    typical_count: "20-35 templates affected",
    performance: "< 5ms"
  }
};
```

### CFP Optimization Rules

**Template Metadata for Optimization:**

```json
{
  "meta": {
    "id": "ACT_Connect_Informal_Social",
    "update_triggers": [
      "emotional_state",
      "relationship_status",
      "temporal",
      "financial_minor"
    ]
  }
}
```

**Update Engine:**
```javascript
function onGameStateChange(changeType, changeData) {
  // Get templates affected by this specific change
  const affectedTemplates = templateIndex.query({
    update_triggers: changeType
  });
  
  // Recalculate only affected weights
  affectedTemplates.forEach(template => {
    template.current_weight = calculateWeight(template, gameState);
  });
  
  // Renormalize probability mass
  normalizeCFP();
}
```

---

## 3. The 7-Card Hand: Volitional Actions

### Hand Composition Strategy

```javascript
const HAND_COMPOSITION = {
  size: 7,  // Constant
  
  composition: {
    obligations: {
      count: "1-2 cards",
      source: "Routine templates (auto-appear based on schedule)",
      examples: ["Pay Rent", "Weekly Team Meeting", "Call Mom (Sunday)"],
      generation: "Tier 1 (instant, local)",
      note: "These aren't drawn—they appear when due"
    },
    
    contextual_actions: {
      count: "5-6 cards",
      source: "Weighted draw from CFP",
      generation: "Mix of Tier 1 (3-4 cards) and Tier 2 (2-3 cards)",
      diversity_rules: [
        "No duplicate templates in single hand",
        "At least 1 social option (if NPCs available)",
        "At least 1 aspiration-related (if active aspiration)",
        "Balance high/low energy activities"
      ]
    }
  },
  
  generation_timing: {
    session_start: "Generate full 7-card hand",
    replenishment: "Predictive pre-fetching during gameplay"
  }
};
```

### Hand Diversity Algorithm

```javascript
function drawHand(cfp, gameState) {
  const hand = [];
  
  // Step 1: Add obligations
  const obligations = getScheduledObligations(gameState.time);
  hand.push(...obligations);
  
  // Step 2: Fill remaining slots with diverse draws
  const remaining = 7 - hand.length;
  const drawn = [];
  
  for (let i = 0; i < remaining; i++) {
    const candidate = weightedDraw(cfp, {
      exclude: drawn,  // No duplicates
      prefer_diversity: {
        energy_levels: balanceEnergySpread(drawn),
        categories: balanceCategories(drawn),
        npc_variety: balanceNPCs(drawn)
      }
    });
    
    drawn.push(candidate);
  }
  
  // Step 3: Instantiate (mix Tier 1/2 based on template tier)
  const instances = await instantiateCards(drawn, gameState);
  
  hand.push(...instances);
  return hand;
}
```

---

## 4. Predictive Pre-Fetching: Masking Tier 2 Latency

### The Latency Problem

**Tier 2 generation via EWR-Light takes 1-3 seconds.**

**Player decision time: 5-15 seconds per card.**

**Solution: Pre-fetch during player's decision time.**

### Pre-Fetch Architecture

```javascript
const PREFETCH_SYSTEM = {
  
  trigger_condition: "Hand size drops to 4 cards remaining",
  
  timing: {
    observation: "Player plays card → Hand drops to 6",
    action: "No pre-fetch yet",
    
    observation: "Player plays card → Hand drops to 5",
    action: "No pre-fetch yet",
    
    observation: "Player plays card → Hand drops to 4",
    action: "TRIGGER PRE-FETCH",
    
    reason: "By the time player decides on next card, fetch will complete"
  },
  
  process: {
    step_1: {
      action: "Client requests CFP update from server",
      payload: "Current game state snapshot",
      latency: "50-100ms"
    },
    
    step_2: {
      action: "Server recalculates CFP incrementally",
      process: "Update only templates affected by last action",
      latency: "< 10ms"
    },
    
    step_3: {
      action: "Server performs weighted draw for 3-4 templates",
      process: "Apply hand diversity rules",
      latency: "< 5ms"
    },
    
    step_4: {
      action: "Server instantiates via Tier 1 or Tier 2",
      tier_1: "Instant (0ms)",
      tier_2: "1-3 seconds (parallel EWR-Light calls)",
      optimization: "Batch 3-4 generations in single EWR call"
    },
    
    step_5: {
      action: "Instances sent to client and held in buffer",
      storage: "Pre-fetch buffer (3-4 cards ready)",
      status: "Ready for hand replenishment"
    }
  },
  
  latency_masking: {
    player_decision_time: "5-15 seconds typical",
    prefetch_completion: "1-3 seconds",
    buffer_available_by: "Well before player plays next card",
    player_experience: "Instant card appearance"
  },
  
  edge_case_rapid_play: {
    scenario: "Player plays cards rapidly (< 2 seconds between)",
    detection: "Buffer empty when replenishment needed",
    fallback_strategy: [
      "Option 1: Use Tier 1 instant generation for that card",
      "Option 2: Show 'Drawing...' indicator briefly (< 1s)",
      "Option 3: Pull from emergency Tier 1 pool"
    ],
    frequency: "Rare (< 5% of sessions)"
  }
};
```

### Batch Generation Optimization

**Problem:** Calling EWR-Light 3 separate times = 3x cost.

**Solution:** Batch generate 3-4 cards in single EWR call.

```javascript
const BATCH_GENERATION = {
  
  input_to_ewr: {
    templates: [
      {id: "ACT_Connect_Informal_Social", context: {...}},
      {id: "ACT_Creative_Work", context: {...}},
      {id: "ACT_Explore_Location", context: {...}}
    ],
    
    shared_context: {
      character_state: {...},
      time_of_day: "afternoon",
      recent_events: [...]
    }
  },
  
  ewr_process: {
    step_1: "Load shared context once",
    step_2: "Generate 3 instances sequentially using same loaded context",
    step_3: "Return all 3 instances in single response"
  },
  
  cost_savings: {
    naive: "3 separate calls × 500 tokens each = 1500 tokens",
    batched: "1 call with 700 tokens total (shared context)",
    savings: "~50% reduction in tokens + faster latency"
  }
};
```

---

## 5. Turn Flow: Fluid Time Progression

### The Complete Turn Cycle

```javascript
const TURN_FLOW = {
  
  // ═══════════════════════════════════════════════════════════
  // SESSION START
  // ═══════════════════════════════════════════════════════════
  session_start: {
    step_1: "Load current game state",
    step_2: "ENGINE_PERSONALITY calculates emotional state",
    step_3: "Build CFP (initial full calculation)",
    step_4: "Draw 7-card hand (mix Tier 1 + pre-fetched Tier 2)",
    step_5: "Display game board",
    
    display_elements: {
      time: "Tuesday, Week 5, 2:30 PM",
      energy: "5/8",
      money: "$1,247",
      emotional_state: "CURIOUS / MOTIVATED",
      character_state_panel: ["STATE: Motivated Streak (3 days)"],
      hand: ["7 cards displayed"]
    }
  },
  
  // ═══════════════════════════════════════════════════════════
  // CARD SELECTION
  // ═══════════════════════════════════════════════════════════
  player_selects_card: {
    step_1: "Player clicks/taps card",
    
    step_2: "Show detailed preview modal",
    preview_contains: {
      full_narrative: "Complete card description",
      costs: "Time (1.5 hours), Energy (1), Money ($8), Capacity (1)",
      time_after: "Will be 4:00 PM after this",
      energy_after: "Will be 4/8 after this",
      potential_outcomes: [
        "70%: Pleasant connection (Social +2)",
        "20%: Meaningful moment (Social +3, Memory)",
        "10%: Awkward (Social +0)"
      ],
      special_notes: "Sarah has been stressed lately..."
    },
    
    step_3: "Player confirms or cancels",
    confirmation: "Play this card"
  },
  
  // ═══════════════════════════════════════════════════════════
  // CARD RESOLUTION
  // ═══════════════════════════════════════════════════════════
  card_resolution: {
    
    immediate_effects: {
      deduct_costs: "Time +1.5hr, Energy -1, Money -$8",
      advance_time: "2:30 PM → 4:00 PM",
      update_ui: "Show new time/energy/money"
    },
    
    narrative_generation: {
      tier_1_instant: {
        process: "Simple template fill",
        latency: "< 50ms",
        display: "Card flips immediately to outcome"
      },
      
      tier_2_cloud: {
        process: "EWR-Light generates narrative WITH Priming metadata",
        priming_injection: {
          analyze: "Current game state for latent tensions",
          embed: "LatentTensions, PotentialHooks, Stakes, ResonantMemories, VolatilityIndex",
          modify: "Outcome probabilities based on context (EWR has full creative control)",
          invisible: "Player doesn't see metadata, feels it through narrative"
        },
        typical_latency: "< 1 second (often pre-fetched partial)",
        display: "Brief 'Generating...' if not cached",
        fallback: "Show simple text immediately, enrich async",
        output: "Narrative + invisible Priming metadata"
      },
      
      tier_3_heavy: {
        process: "Full EWR with semantic analysis, fusion detection, Memory Facets",
        latency: "5-10 seconds",
        display: "NARRATIVE INTERLUDE (see Section 8)",
        triggers: ["Major event", "Evolution", "Fusion opportunity detected"]
      }
    },
    
    outcome_determination: {
      roll_success: "Based on template success_spectrum + modifiers",
      apply_effects: "Update meters, relationships, skills",
      check_special_triggers: [
        "Did this create evolution opportunity?",
        "Did this unlock fusion?",
        "Did this trigger event?"
      ]
    },
    
    state_updates: {
      engine_personality: "Recalculate emotional state if threshold crossed",
      engine_memory: "Archive if memory_weight >= 5",
      graph_db: "Update relationship bond, location association",
      vector_db: "Store semantic embedding for pattern detection"
    },
    
    cfp_incremental_update: {
      triggered_by: "Card resolution changed game state",
      process: "Update only affected templates",
      typical_scope: "10-30 templates",
      performance: "< 5ms"
    }
  },
  
  // ═══════════════════════════════════════════════════════════
  // HAND REPLENISHMENT
  // ═══════════════════════════════════════════════════════════
  replenishment: {
    hand_before: 6,  // One card played
    
    check_prefetch_buffer: {
      if_ready: {
        action: "Instantly add pre-fetched card to hand",
        latency: "0ms",
        player_experience: "Seamless"
      },
      
      if_empty: {
        action: "Show 'Drawing...' briefly",
        fallback: "Use Tier 1 instant generation",
        latency: "< 500ms",
        frequency: "< 5% of replenishments"
      }
    },
    
    hand_after: 7,
    
    trigger_new_prefetch: {
      condition: "If hand dropped to 4 during play",
      action: "Start fetching next batch"
    }
  },
  
  // ═══════════════════════════════════════════════════════════
  // LOOP CONTINUES
  // ═══════════════════════════════════════════════════════════
  next_turn: {
    state: "Ready for next card selection",
    time: "4:00 PM",
    energy: "4/8",
    hand: "7 cards (mix of played-before + newly drawn)"
  }
};
```

---

## 6. Time Boundaries & Transitions

### End of Day

```javascript
const END_OF_DAY = {
  
  triggers: [
    "Time reaches 11:00 PM",
    "Energy depleted to 0 (optional continue with debt)",
    "Player manually chooses 'End Day'"
  ],
  
  process: {
    step_1_summary: {
      display: "Day Summary Modal",
      contents: {
        meters_today: "Social +5, Emotional +3, Physical -2",
        relationships: "Sarah +0.15 trust, Marcus +0.02 bond",
        aspirations: "Get Promoted: 52% → 67%",
        memories_created: ["Sarah's Doubt"],
        money_spent: "$42",
        time_summary: "Played 8 cards across 14 hours"
      }
    },
    
    step_2_archive: {
      action: "Compress day into archive entry",
      vector_embedding: "Create semantic summary for queries",
      memory_weight: "High-weight moments preserved separately"
    },
    
    step_3_overnight_processing: {
      meters: {
        energy: "Restore to base (modified by sleep quality)",
        capacity: "Slow recovery (+0.1 if no crisis)",
        social: "Decay -1 (natural entropy)"
      },
      
      obligations: "Queue next day's scheduled routines",
      
      skills: "Apply XP earned today, check rust timers"
    },
    
    step_4_next_day_start: {
      time_determination: {
        normal_day: "6:00 AM wake",
        weekend: "8:00 AM wake",
        after_crisis: "10:00 AM (exhausted)",
        after_party: "11:00 AM (hungover)",
        method: "Context-aware via ENGINE_PERSONALITY"
      },
      
      initial_state: "Generate morning emotional state",
      
      hand: "Draw fresh 7-card hand from updated CFP"
    }
  }
};
```

### End of Week

```javascript
const END_OF_WEEK = {
  trigger: "Sunday 11:00 PM",
  
  process: {
    step_1_review: {
      display: "Week Review Modal",
      contents: {
        aspirations: "Progress breakdown across all active goals",
        relationships: "Who you spent time with, who you neglected",
        finances: "Income vs. expenses, rent paid",
        skills: "XP gained per skill, rust warnings",
        highlight_moments: "3-5 memorable moments from week"
      }
    },
    
    step_2_weekly_processing: {
      finances: "Deduct rent, apply income",
      skills: "Check rust timers (Week 4 = first rust warning)",
      routines: "Evaluate consistency (perk tracking)",
      relationships: "Flag neglected relationships (> 2 weeks no contact)",
      
      ewr_narrative_analysis: {
        trigger: "Every Sunday after day summary",
        note: "See 05-story-weaver-ai.md Section 10 for full details",
        
        facet_review: {
          process: "EWR analyzes all Memory Facets from the week",
          focus: "Observational Facets (intrigue hooks)",
          
          examples: [
            "Sarah's nervous phone checking (3 occurrences)",
            "Marcus avoiding vulnerability topics (5 times)",
            "Unexplained package deliveries (2 mentions)"
          ]
        },
        
        pattern_detection: {
          process: "Identify unresolved tensions, emerging conflicts",
          threshold: "2+ Observational Facets with matching pattern_id OR overlapping tags",
          
          output: {
            detected_patterns: [
              {
                pattern: "Sarah's Secrecy",
                facets: 3,
                weeks: 3,
                confidence: "high",
                trajectory: "escalating"
              }
            ]
          }
        },
        
        hook_generation: {
          process: "Generate event seeds for next week",
          probability: "30-50% that detected pattern becomes event",
          
          examples: [
            {
              pattern: "Sarah's secrecy",
              decision: "GENERATE EVENT",
              event: "EVT_The_Suspicious_Text_Message (Strand 3)",
              priming: "High VolatilityIndex, stakes = 'friendship at risk'"
            },
            {
              pattern: "Marcus avoidance",
              decision: "BOOST TEMPLATES",
              action: "Increase CFP weight for 'Reach Out to Marcus' templates",
              priming: "Moderate VolatilityIndex, 'he's pulling away'"
            }
          ]
        },
        
        stakes_escalation: {
          process: "Modify CFP probabilities to surface relevant templates",
          
          example: {
            detected: "Player neglecting 'Learn Spanish' aspiration (no progress in 3 weeks)",
            action: "Generate Strand 3 event: 'Last Chance to Register'",
            stakes: "Sign up by Friday or lose opportunity for 6 months"
          }
        },
        
        pacing_awareness: {
          note: "Respects Pacing Specialist's recommendations",
          
          if_high_event_density: "HOLD generated events, boost low-stakes templates instead",
          if_character_vulnerable: "DO NOT generate crises, generate support opportunities",
          if_story_flat: "ESCALATE patterns aggressively into events"
        }
      }
    },
    
    step_3_preview: {
      display: "Next Week Preview",
      contents: {
        scheduled_obligations: "Upcoming meetings, deadlines",
        queued_events: "Potential events EWR might trigger",
        aspiration_milestones: "Expected next beats"
      }
    }
  }
};
```

### End of Season

```javascript
const END_OF_SEASON = {
  trigger: "Week 12/24/36 (player-chosen season length)",
  
  process: {
    step_1_climax: {
      display: "Season Climax Sequence",
      process: "EWR-Heavy generates resolution for each active aspiration",
      latency: "10-20 seconds (Narrative Interlude justified)",
      outcome: "Success/Failure/Mixed for each goal"
    },
    
    step_2_archive_creation: {
      action: "Generate 'Season Book'",
      process: "EWR queries archive, creates coherent narrative",
      structure: "3-act structure, thematic analysis",
      output: "2000-5000 word mini-novel",
      player_experience: "The story of their season"
    },
    
    step_3_character_evolution: {
      perks_earned: "Based on behavioral patterns detected",
      skills_mastered: "Check if any skills reached Level 10",
      relationships_evolved: "Journey Beats completed → level ups",
      cherished_memories: "Count of fully evolved cards"
    },
    
    step_4_next_season: {
      choose_aspirations: "Player selects 3-5 new goals",
      life_direction_check: "Option to pivot direction",
      life_phase_transition: "Check if ready for new phase (Young Adult → Settled Adult)"
    }
  }
};
```

---

## 6.5. Fusion Event Flow

**Context:** Fusion occurs DURING Tier 3 high-intensity events, not as a standalone action. This section documents the detection and execution flow.

```javascript
const FUSION_EVENT_FLOW = {
  
  trigger: "High-intensity Tier 3 event detects fusion opportunity",
  
  detection_phase: {
    phase_1_event_begins: {
      example: "EVT_Breakup (Tier 3) starts at Café Luna with Sarah",
      context: "High emotional intensity, location significance, relationship depth"
    },
    
    phase_2_semantic_resonance_check: {
      system: "ENGINE_WRITERS_ROOM (Tier 3)",
      action: "Perform deep Vector DB semantic search",
      query: "Which memories/items/locations are semantically close to this catalyst?",
      
      search_targets: [
        "Recent memories involving Sarah, café, vulnerability",
        "Items present in scene or associated with Sarah",
        "Location significance (Café Luna history)",
        "Related emotions (doubt, support, intimacy)"
      ],
      
      example_results: {
        high_resonance: [
          "mem_sarah_doubt_cafe_luna (0.92 similarity)",
          "ITEM_Coffee_Mug (present in scene)",
          "LOC_Cafe_Luna (0.88 location significance)"
        ],
        medium_resonance: [
          "mem_first_coffee_with_sarah (0.74 similarity)"
        ]
      }
    },
    
    phase_3_symbolic_potential_evaluation: {
      process: "Evaluate if concepts cluster tightly around catalyst",
      
      criteria: {
        thematic_tag_alignment: {
          check: "Do fusion_tags overlap meaningfully?",
          example: {
            mem_sarah_doubt: ["intimacy_building", "vulnerability", "cafe_significance"],
            ITEM_Coffee_Mug: ["everyday_object", "gift_potential", "emotional_anchor"],
            LOC_Cafe_Luna: ["sanctuary", "ritual_space", "relationship_anchor"],
            EVT_Breakup: ["loss", "transformation", "ending"],
            
            overlap: ["emotional_anchor", "relationship_significance", "cafe_context"],
            assessment: "HIGH—concepts converge meaningfully"
          }
        },
        
        contextual_co_occurrence: {
          check: "Are these elements present/relevant in this moment?",
          example: "Mug is in scene, location is event setting, memory is recent"
        },
        
        emotional_intensity: {
          check: "Is catalyst intense enough to justify fusion?",
          threshold: "Tier 3 required, high volatility index"
        }
      }
    },
    
    phase_4_fusion_decision: {
      if_threshold_met: {
        confidence: "> 0.75 (high)",
        action: "Trigger fusion, initiate Narrative Interlude"
      },
      
      if_threshold_not_met: {
        confidence: "< 0.75",
        action: "Event proceeds normally without fusion",
        note: "Better to miss fusion than force one"
      }
    }
  },
  
  if_fusion_triggered: {
    narrative_interlude: {
      required: true,
      visual: "Memory web animation, 'A connection sparks...'",
      duration: "5-8 seconds"
    },
    
    parallel_processing: {
      thread_1: {
        task: "Generate fusion narrative",
        output: "How Sarah's mug becomes a symbolic artifact",
        latency: "3-5s"
      },
      
      thread_2: {
        task: "Create fused entity with properties + Memory Facets",
        output: "ARTIFACT_The_Breakup_Mug with mechanics and memories",
        latency: "5-8s"
      },
      
      thread_3: {
        task: "Queue unique art generation",
        output: "Watercolor mug with ghosted memories",
        async: true
      }
    },
    
    output: "New L3 entity added to game state",
    
    example_fusion_output: {
      entity_type: "ARTIFACT_Symbolic_Memory",
      id: "artifact_the_breakup_mug",
      name: "The Breakup Mug",
      
      fusion_narrative: `Sarah slid her favorite mug across the table. 
                        'Keep it,' she said. 'Remember me.' 
                        Then she left. You're still holding it.`,
      
      properties: {
        mechanical: "-0.5 Capacity when in inventory (painful reminder)",
        memory_resonance: "Triggers Sarah memories when seeing coffee",
        
        memory_facets: {
          primary: "The day Sarah gave me her mug and walked away",
          sensory: [
            "The sound of ceramic sliding across wood",
            "The warmth still in the handle from her hands"
          ],
          observational: [
            "Why did she give it to me? What was she really saying?"
          ]
        }
      },
      
      future_evolution_potential: [
        "Let go of the mug (closure ritual)",
        "Return the mug to Sarah (reconciliation hook)",
        "Break the mug (dramatic catharsis)"
      ]
    }
  },
  
  if_no_fusion: {
    outcome: "Event proceeds normally",
    note: "High-intensity event still generates Memory Facets, just no fusion"
  },
  
  timing_note: {
    critical: "Fusion detection happens DURING Tier 3 event, not after",
    player_experience: "Seamless—interlude flows naturally from event intensity",
    frequency: "2-5 fusions per season (rare and meaningful)"
  }
};
```

### Fusion vs. Normal Tier 3 Event

**Normal Tier 3 Event (No Fusion):**
```
1. Event triggers (EVT_Breakup)
2. Narrative Interlude (5-8s)
   └─> Generate event outcome narrative
   └─> Generate Memory Facets
3. Return to game with outcome
4. Memory archived
```

**Tier 3 Event WITH Fusion:**
```
1. Event triggers (EVT_Breakup at Café Luna)
2. Fusion detection (semantic resonance check)
3. Fusion threshold met → Extended Narrative Interlude (5-10s)
   └─> Generate event outcome narrative
   └─> Generate fusion narrative
   └─> Generate Memory Facets for BOTH event and fusion
   └─> Create fused entity (ARTIFACT_The_Breakup_Mug)
4. Return to game with outcome + new artifact
5. Both memories archived
```

---

## 7. Special Cases: Time Manipulation

### Multi-Day Fast-Forward

```javascript
const TIME_FAST_FORWARD = {
  
  triggers: [
    "Specific card effect (Hospital Stay, Work Trip, Vacation)",
    "Event forces time skip (Waiting Period, Recovery Time)"
  ],
  
  flow: {
    step_1_warning: {
      display: "Modal with clear warning",
      message: "This will advance time by 5 days. Obligations will be skipped. Continue?",
      options: ["Confirm", "Cancel"]
    },
    
    step_2_summary_generation: {
      tier: "Tier 2 (EWR-Light)",
      prompt: "Generate summary narrative of these 5 days",
      context: "Why time skipped, what happened during",
      output: "2-3 paragraph summary"
    },
    
    step_3_resource_calculation: {
      meters: "Calculate net change over period",
      money: "Apply daily costs (rent prorated, expenses)",
      relationships: "Apply decay for neglected NPCs",
      skills: "No XP gain during skip"
    },
    
    step_4_resume: {
      time: "Advance to end of skip period",
      state: "Recalculate emotional state post-skip",
      cfp: "Full recalculation (context changed significantly)",
      hand: "Draw fresh hand for return to normal play"
    }
  },
  
  example: {
    trigger: "Card: Hospital Stay (5 days)",
    warning: "You'll be hospitalized for 5 days. Rent will be due during this time. Continue?",
    
    narrative: `
      The next five days blur together. Hospital routines, tests, medications.
      Sarah visits on day three—she brings your favorite book. Marcus texts
      every day but doesn't visit. The doctors say you can go home on day six.
      You're exhausted but recovering.
      
      Time advanced: 5 days
      Energy: 3/8 (still recovering)
      Money: -$1,200 (rent + medical bills)
      Emotional: -3 (stressful experience)
      Sarah trust: +0.10 (she showed up)
      Marcus trust: -0.05 (you notice he didn't)
      
      Memory created: "The Hospital Stay"
    `,
    
    resume_time: "Saturday, 2:00 PM (just got home)"
  }
};
```

---

## 8. The Narrative Interlude: Embracing Tier 3 Latency

### Design Philosophy

**Problem:** Tier 3 (EWR-Heavy) takes 5-10 seconds.

**Traditional Solution:** Show loading spinner (feels broken).

**Unwritten Solution:** Make latency diegetic and thematic.

### The Narrative Interlude Experience

```javascript
const NARRATIVE_INTERLUDE = {
  
  when_triggered: [
    "Major Catalytic Event (Strand 3)",
    "Card Evolution (to Cherished with transformative moment)",
    "Fusion Opportunity detected", // ← NEW: Always triggers interlude
    "Life Direction milestone",
    "Season climax"
  ],
  
  parallel_threads: {
    thread_1_dialogue: {
      system: "Local dialogue LLM",
      task: "Generate fusion/evolution narrative moment",
      output: "How concepts merge, what it means emotionally",
      latency: "3-5s typical"
    },
    
    thread_2_ewr_processing: {
      system: "ENGINE_WRITERS_ROOM (Tier 3)",
      tasks: [
        "Deep semantic analysis",
        "Generate Memory Facets (Primary, Sensory, Observational)",
        "Calculate narrative implications",
        "Queue potential follow-up events",
        "Check for related card evolutions",
        "Update relationship depths"
      ],
      latency: "5-8s typical"
    },
    
    thread_3_art_generation: {
      system: "Image generation API",
      task: "Generate unique art for evolved/fused card",
      latency: "5-30s (continues after interlude if needed)",
      note: "Started during interlude, may complete after"
    }
  },
  
  synchronization: {
    interlude_duration: "Max of Thread 1 and 2 (typically 5-8s)",
    art_handling: "Async - appears when ready, not blocking",
    player_experience: "Thematic pause, all critical data ready at end"
  },
  
  visual_design: {
    transition: "Gentle fade from game board to interlude screen",
    
    elements: {
      background: "Stylized, abstract memory web visual",
      animation: "Connecting dots, flowing particles",
      text: "Reflective, thematic (not 'Loading...')",
      typography: "Serif, literary aesthetic",
      music: "Ambient, contemplative"
    },
    
    text_examples: [
      "A connection sparks...",
      "Something shifts. You'll remember this.",
      "Life takes an unexpected turn...",
      "In this moment, everything changes.",
      "Time slows. This matters.",
      "Suddenly, this means something more."
    ],
    
    duration: "5-10 seconds (actual EWR-Heavy processing time)",
    feel: "Diegetic pause, not technical loading"
  },
  
  player_psychology: {
    signal: "Something significant is happening",
    anticipation: "Builds tension before major moment",
    immersion: "Fits game's introspective, literary theme",
    no_frustration: "Feels intentional, not broken"
  },
  
  examples: [
    {
      trigger: "Sarah's vulnerability breakthrough during coffee",
      interlude_text: "She's telling you something she's never told anyone. The air changes. This is a moment you'll remember.",
      duration: "6 seconds",
      ewr_processing: [
        "Generate unique outcome narrative",
        "Check evolution trigger criteria",
        "Calculate deep relationship impact",
        "Create cherished memory entry",
        "Update vector embeddings"
      ],
      outcome: "Cherished memory created, relationship level up, new dialogue unlocked"
    },
    
    {
      trigger: "Health crisis event triggered",
      interlude_text: "Your body is trying to tell you something. You've been ignoring the signs too long.",
      duration: "8 seconds",
      ewr_processing: [
        "Generate crisis narrative with context",
        "Determine severity based on recent state",
        "Calculate multi-day consequences",
        "Identify which NPCs will react",
        "Create branching choice framework"
      ],
      outcome: "Major event with 4 choices, 5-day time skip, multiple relationship impacts"
    },
    
    {
      trigger: "Evolution: Coffee with Sarah → Tuesday Afternoons at Café Luna",
      interlude_text: "This place means something now. This moment will stay with you.",
      duration: "7 seconds",
      ewr_processing: [
        "Generate cherished memory narrative",
        "Create unique card art prompt",
        "Calculate new mechanical benefits",
        "Update memory resonance triggers",
        "Create symbolic tags for fusion"
      ],
      outcome: "Cherished card replaces generic, golden border, reduced costs, high resonance"
    }
  ],
  
  frequency: {
    target: "2-4 times per session (30-60 min play)",
    too_frequent: "Would feel disruptive",
    too_rare: "Would lose dramatic impact",
    balance: "Reserve for genuinely significant moments"
  }
};
```

---

## 9. State Cards: Parallel System

### Critical Distinction

**State Cards are NOT in the hand. They are passive modifiers displayed separately.**

```javascript
const STATE_CARD_SYSTEM = {
  
  nature: "Hybrid: Procedurally triggered, AI-instantiated",
  
  detection_triggers: {
    engine_capacity: {
      example: "Capacity < 3.0 for 2 weeks",
      triggers: "STATE_Burnout"
    },
    
    engine_personality: {
      example: "High Neuroticism + major stressor",
      triggers: "STATE_Anxious"
    },
    
    event_resolution: {
      example: "Breakup event resolves",
      triggers: "STATE_Heartbroken"
    },
    
    threshold_crossing: {
      example: "Energy debt reaches -2",
      triggers: "STATE_Exhausted"
    }
  },
  
  instantiation: {
    tier: "2 or 3 (depending on complexity)",
    
    tier_2_simple: {
      examples: ["STATE_Tired", "STATE_Motivated"],
      process: "Quick EWR-Light generation with context",
      latency: "< 2 seconds"
    },
    
    tier_3_complex: {
      examples: ["STATE_Burnout", "STATE_Grieving"],
      process: "Full EWR-Heavy with deep context analysis",
      latency: "5-8 seconds",
      display: "Narrative Interlude justified"
    }
  },
  
  ui_treatment: {
    location: "Character State Panel (separate from hand)",
    visual: "Different card style (darker, no action button)",
    interaction: "Hover to see details and resolution conditions",
    max_visible: "3-5 state cards at once",
    stacking: "Effects multiply when multiple active"
  },
  
  example_flow: {
    detection: "mental_meter < 3 for 21 days",
    template: "STATE_Burnout",
    
    context_gathered: {
      cause: "Overwork + neglecting rest + high aspiration pressure",
      personality: "High Conscientiousness (won't stop pushing)",
      recent_events: ["Worked late 12 of last 14 days"],
      ignored_warnings: ["Declined rest cards 8 times"]
    },
    
    ewr_generation: {
      tier: 3,
      narrative_interlude: "Your body is trying to tell you something...",
      
      generated_instance: {
        title: "STATE: Burnout",
        
        description: `You've been pushing too hard for too long. 
        Everything feels heavy. Your body aches. 
        Sleep doesn't help anymore.`,
        
        mechanical_effects: [
          "All activities +1 Energy cost",
          "Success rates -15%",
          "High-Energy activities hidden from CFP",
          "Aspiration progress halted until resolved"
        ],
        
        resolution_conditions: [
          "Play 3 Rest cards over next week",
          "Allow 2 weeks to pass with minimal activity",
          "OR: Trigger health crisis (forced resolution)"
        ],
        
        visual: {
          frame: "Dark, heavy border",
          art: "Abstract representation of exhaustion",
          position: "Top of Character State panel"
        }
      }
    }
  }
};
```

---

## 10. Art Generation: Asynchronous Pipeline

```javascript
const ART_GENERATION = {
  
  philosophy: "Art NEVER blocks gameplay",
  
  flow: {
    card_instantiated: {
      immediate_display: {
        text: "Full narrative visible immediately",
        art: "Template category placeholder",
        playable: "Card is fully playable with placeholder"
      },
      
      art_request_queued: {
        priority_tier_1: "Use pre-rendered template art (no generation needed)",
        priority_tier_2: "Queue medium-priority generation",
        priority_tier_3: "Queue high-priority generation (cherished, events)"
      }
    },
    
    art_generation: {
      service: "Image generation API",
      input: {
        prompt: "Generated from template + context",
        style: "Consistent art style (watercolor, impressionistic)",
        composition: "Character-focused or location-focused"
      },
      
      latency: "5-30 seconds (doesn't matter—async)",
      
      completion: {
        delivery: "Server pushes completed art to client",
        update: "Fade in over placeholder smoothly",
        timing: "Could be while card still in hand or after played",
        player_experience: "Delightful surprise when art appears"
      }
    },
    
    caching: {
      generic_instances: "Art cached and reused",
      personalized_instances: "Unique art generated once, then cached",
      cherished_instances: "Always unique, never reused"
    }
  },
  
  evolution_visual_progression: {
    generic: {
      art_source: "Template category placeholder",
      frame: "Standard",
      example: "Generic coffee shop scene"
    },
    
    personalized: {
      art_source: "Unique generation (NPC + location specific)",
      frame: "Standard with name plate",
      example: "Sarah at Café Luna, recognizable details"
    },
    
    cherished: {
      art_source: "Unique generation with special composition",
      frame: "Golden/glowing border",
      visual_treatment: "Soft glow, special effects",
      example: "Sarah at window seat with golden afternoon light, intimate framing"
    }
  },
  
  cost_optimization: {
    avoid_generation: "Use template art for Tier 1 whenever possible",
    batch_generation: "Queue multiple art requests, process in batch",
    cache_aggressively: "Store all generated art permanently",
    progressive_enhancement: "Placeholder → Good art → Great art (optional upgrade)"
  }
};
```

---

## 11. Performance Targets & Monitoring

### Target Metrics

| Metric | Target | Acceptable | Unacceptable |
|--------|--------|------------|--------------|
| **CFP Incremental Update** | < 5ms | < 10ms | > 15ms |
| **Hand Replenishment (buffered)** | 0ms (instant) | < 100ms | > 500ms |
| **Tier 1 Generation** | < 50ms | < 100ms | > 200ms |
| **Tier 2 Generation** | 1-2s | 2-3s | > 4s |
| **Tier 3 Generation** | 5-8s | 8-10s | > 12s |
| **Pre-fetch Success Rate** | > 95% | > 90% | < 85% |

### Monitoring Strategy

```javascript
const PERFORMANCE_MONITORING = {
  
  metrics_to_track: {
    cfp_updates: {
      measure: "Update latency per change type",
      alert_if: "Any update type > 10ms average",
      action: "Optimize template indexing"
    },
    
    prefetch_buffer_hits: {
      measure: "% of replenishments served from buffer",
      alert_if: "Hit rate < 90%",
      action: "Adjust prefetch trigger timing"
    },
    
    ewr_latency: {
      measure: "P50, P95, P99 latency per tier",
      alert_if: "P95 Tier 2 > 3s OR P95 Tier 3 > 10s",
      action: "Optimize prompts, check infrastructure"
    },
    
    stale_hands: {
      measure: "Player reports 'same cards every time'",
      alert_if: "Duplicate template in hand > 20% across session",
      action: "Tune CFP probability distribution"
    }
  },
  
  player_experience_metrics: {
    perceived_latency: {
      measure: "Time from card selection to outcome display",
      target: "< 2 seconds perceived (even if Tier 2 processing)",
      method: "Show immediate feedback, enrich async"
    },
    
    narrative_interlude_acceptance: {
      measure: "Player sentiment about 5-10s pauses",
      target: "> 80% find it thematic/appropriate",
      method: "Survey + session recording analysis"
    }
  }
};
```

---

## 12. Complete Turn Example

### Full Walkthrough: One Card Played

```
// ═══════════════════════════════════════════════════════════
// STARTING STATE
// ═══════════════════════════════════════════════════════════

Game State:
  Time: Tuesday, Week 5, 2:30 PM
  Energy: 5/8
  Money: $1,247
  Emotional State: CURIOUS / MOTIVATED
  Location: Home
  
  Character State Panel:
    - STATE: Motivated Streak (3 days remaining)
  
  Hand (7 cards):
    1. Work on Photography Portfolio (Tier 2)
    2. Coffee with Sarah at Café Luna (Tier 2) ← PLAYER SELECTS
    3. Quick Gym Session (Tier 1)
    4. Research Spanish Classes (Tier 1)
    5. Call Marcus (Tier 2)
    6. Take a Nap (Tier 1)
    7. Scroll Social Media (Tier 1)
  
  Pre-fetch Buffer: 3 cards ready (from previous pre-fetch)

// ═══════════════════════════════════════════════════════════
// PLAYER SELECTS: Coffee with Sarah
// ═══════════════════════════════════════════════════════════

Preview Modal Shown:
  Title: Coffee with Sarah at Café Luna
  
  Narrative: "You sit at your usual spot by the window. Sarah arrives 
  ten minutes late, apologizing. She looks tired..."
  
  Costs:
    Time: 1.5 hours (will be 4:00 PM)
    Energy: 1 (will be 4/8)
    Money: $8 (will be $1,239)
    Emotional Capacity: 1
  
  Potential Outcomes:
    70%: Pleasant connection (Social +2)
    20%: Meaningful moment (Social +3, Memory)
    10%: Awkward (Social +0)
  
  Special Note: "Sarah has been stressed lately. She might open up."
  
Player Clicks: [PLAY THIS CARD]

// ═══════════════════════════════════════════════════════════
// RESOLUTION BEGINS
// ═══════════════════════════════════════════════════════════

Immediate Effects (< 50ms):
  ✓ Time: 2:30 PM → 4:00 PM
  ✓ Energy: 5 → 4
  ✓ Money: $1,247 → $1,239
  ✓ UI updates displayed
  ✓ Card removed from hand

Narrative Generation (Tier 2):
  Status: This instance was pre-fetched (partial context)
  Latency: < 1 second (completing generation)
  Display: Brief "..." indicator, then full narrative appears
  
  [NARRATIVE DISPLAYED]
  
  "COFFEE WITH SARAH AT CAFÉ LUNA
  
  You sit at your usual spot by the window. Sarah arrives ten minutes 
  late, apologizing. She looks tired. The coffee comes, and she wraps 
  her hands around the mug like she's cold.
  
  'Can I tell you something?' she says quietly. 'I don't think I can 
  do this anymore. The café, the dream... I don't know if I'm brave enough.'
  
  The afternoon light goes golden. You listen. Really listen. And you 
  tell her the truth: that you see her, that you believe in her, that 
  doubt doesn't mean she's wrong—it means she cares.
  
  When you leave, something has shifted. This was important."

Outcome Roll:
  Template outcome: Breakthrough Vulnerability (20% chance - player got lucky)
  
Effects Applied:
  Meters:
    Social: +3
    Emotional: +3
  
  Relationship:
    Sarah trust: +0.15
    Sarah bond: +0.08
    Sarah intimacy_deepened: true
  
  Memory Created:
    Title: "Sarah's Doubt"
    Weight: 8 (high)
    Tags: ["vulnerability_shared", "trust_milestone", "defining_moment"]

// ═══════════════════════════════════════════════════════════
// EVOLUTION CHECK (Tier 3 Triggered)
// ═══════════════════════════════════════════════════════════

ENGINE_WRITERS_ROOM Analysis:
  Pattern Detected:
    ✓ 3rd instance of coffee at this location with Sarah
    ✓ Breakthrough outcome just occurred
    ✓ Transformative moment criteria met
    ✓ Relationship depth sufficient (trust 0.75)
    ✓ Both characters emotionally receptive
  
  Assessment: QUALIFIES FOR CHERISHED EVOLUTION
  
NARRATIVE INTERLUDE TRIGGERED:

  [Screen fades to memory web animation]
  
  Text Displayed: "This place means something now. This moment will 
  stay with you."
  
  Duration: 6 seconds
  
  EWR-Heavy Processing:
    - Generate cherished memory narrative
    - Calculate new mechanical benefits
    - Create unique art prompt
    - Update memory resonance triggers
    - Create symbolic fusion tags
  
  [Screen fades back to game board]

Evolution Complete:
  New Card Created:
    Title: "Tuesday Afternoons at Café Luna (with Sarah)"
    State: CHERISHED
    
    Description: "Your ritual. Where she told you her doubts and you 
    became her believer. The light comes through the window the same way 
    every time. The barista knows your order. This place is sacred."
    
    Visual: Golden border, unique art showing window seat with golden light
    
    Mechanical Changes:
      Energy Cost: 0 (from 1) - it's restorative now
      Emotional Capacity Cost: 0.5 (from 1) - comfortable and safe
      Capacity Restore: +0.3 - actively healing
      Memory Resonance: HIGH - triggers callbacks in future events
    
    Special Properties:
      - Cannot be discarded
      - Appears in Season Novel as chapter-level scene
      - Referenced in future Sarah interactions
      - Available in CFP with high weight when Sarah available

// ═══════════════════════════════════════════════════════════
// STATE UPDATES
// ═══════════════════════════════════════════════════════════

Emotional State Recalculation:
  Before: CURIOUS / MOTIVATED
  After: CONFIDENT / GRATEFUL
  Reason: Breakthrough moment + emotional +3 = positive shift

CFP Incremental Update:
  Triggered by: emotional_state_change + relationship_interaction
  
  Templates Affected: 23
    Examples:
      - ACT_Vulnerability_Share: +40% (trust established)
      - ACT_Connect_Informal_Social: -30% (just fulfilled)
      - ACT_Support_Friend: +60% (natural next step)
  
  Performance: 4ms

Archive Update:
  Memory Stored: "Sarah's Doubt"
  Vector Embedding: Generated for semantic search
  Memory Resonance: Active
  Will Appear In Season Novel: Yes (chapter-level)

// ═══════════════════════════════════════════════════════════
// HAND REPLENISHMENT
// ═══════════════════════════════════════════════════════════

Hand Before: 6 cards remaining
Pre-fetch Buffer: 2 cards ready (1 was just consumed)

New Card Added From Buffer:
  Card: "Support Sarah with Business Plan"
  Source: Pre-fetched (was ready in buffer)
  Latency: 0ms (instant)
  Note: This card unlocked by breakthrough moment

Hand After (7 cards):
  1. Work on Photography Portfolio
  2. Quick Gym Session
  3. Research Spanish Classes
  4. Call Marcus
  5. Take a Nap
  6. Scroll Social Media
  7. Support Sarah with Business Plan ← NEW (from buffer)

Pre-fetch Buffer Status:
  Remaining: 1 card
  Trigger: Hand still > 4, no new pre-fetch needed yet

// ═══════════════════════════════════════════════════════════
// READY FOR NEXT TURN
// ═══════════════════════════════════════════════════════════

Current State:
  Time: Tuesday, 4:00 PM
  Energy: 4/8
  Money: $1,239
  Emotional State: CONFIDENT / GRATEFUL
  
  Character State Panel:
    - STATE: Motivated Streak (3 days)
  
  Hand: 7 cards (ready for next selection)
  
  Player Decision: What next?
  
  Typical Decision Time: 8-12 seconds
  Pre-fetch Will Complete: Well before next card played
  Player Experience: Seamless, instant replenishment

// ═══════════════════════════════════════════════════════════
// PERFORMANCE SUMMARY
// ═══════════════════════════════════════════════════════════

Total Turn Latency (player-perceived):
  Card selection to outcome: 1.2 seconds
  Evolution interlude: 6 seconds (justified by narrative)
  Hand replenishment: 0ms (instant from buffer)
  
  Player Experience: Smooth, responsive, thematic

Backend Performance:
  CFP update: 4ms ✓
  Tier 2 generation: 900ms (pre-fetched) ✓
  Tier 3 evolution: 6.2s ✓
  Pre-fetch buffer hit: Yes ✓
  
  All Targets Met: ✓
```

---

## 13. Turn Structure Design Principles

### ✅ Design Decisions Summary

**Generation Timing:** Hybrid Dynamic
- Tier 1: Instant local generation (routines)
- Tier 2: Cloud-based (1-3s, masked by pre-fetching)
- Tier 3: Cloud-based heavy (5-10s, Narrative Interlude)

**CFP Updates:** Incremental Only
- Only recalculate affected templates
- Typical update: 10-30 templates in < 5ms
- Full recalculation only on major state shifts

**Pre-fetching:** Aggressive
- Trigger when hand drops to 4 cards
- Batch generate 3-4 cards per EWR call
- Target: > 95% buffer hit rate

**State Cards:** Separate System
- Not in hand, displayed in Character State Panel
- Hybrid: Procedural trigger + AI instantiation
- Never block gameplay

**Art Generation:** Fully Asynchronous
- Never blocks gameplay
- Placeholder → Unique art fade-in
- Could appear while card still in hand

**Time Progression:** Fluid
- Cards advance time by their duration
- No rigid phases
- Multi-day skips possible

**Narrative Interludes:** Embrace Latency
- Transform technical constraint into thematic feature
- Only for Tier 3 (genuinely significant moments)
- Target: 2-4 per session

---

## 14. Cross-Reference Map

**Related Documents:**
- `08-template-spec.md` - Master Template structure and CFP rules
- `10-validating-template-design.md` - Testing and quality assurance
- `04-gameplay-loop.md` - High-level gameplay rhythm
- `06-growth-and-progression.md` - Evolution and Journey Beat mechanics

**Core Systems:**
- `ENGINE_WRITERS_ROOM` - Narrative generation (Tier 2/3)
- `ENGINE_PERSONALITY` - Emotional state calculation
- `ENGINE_CAPACITY` - Receptivity and perception gates
- `ENGINE_MEMORY` - Archive queries and pattern detection

---

## The Turn Structure Promise

**What This Architecture Achieves:**

✅ **Seamless Just-in-Time generation** - Cards instantiated on-demand, feel unique every time  
✅ **Masked cloud latency** - Pre-fetching eliminates perceived wait  
✅ **Optimized performance** - Incremental CFP updates, < 5ms typical  
✅ **Thematic latency handling** - Tier 3 delays become dramatic pauses  
✅ **Fluid time progression** - Days feel like days, not game boards  
✅ **Non-blocking art** - Asynchronous generation never disrupts flow  

**The Ultimate Goal:**

> By implementing this turn structure, we create a gameplay experience that feels **alive and responsive**—where every card is contextually relevant, narratively unique, and arrives exactly when the player needs it, without technical friction breaking immersion.

**This is not a card shuffler. This is a just-in-time life story generator.**

