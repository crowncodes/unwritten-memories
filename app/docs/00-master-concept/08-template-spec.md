# Master Template Specification V2

**Document Status**: V3 Canonical Reference  
**Last Updated**: October 17, 2025  
**Authority Level**: Master Truth

---

## ⚠️ Critical: Anti-Gamification Mandate

**Before designing any template, internalize this principle:**

> **IF A COUNTER OR THRESHOLD CAN BE EXPLOITED BY REPETITION WITHOUT MEANING, IT VIOLATES THE DESIGN.**

All progression must be assessed by `ENGINE_WRITERS_ROOM` based on **qualitative criteria** (personality compatibility, emotional states, interaction quality, narrative context)—NOT arbitrary numerical thresholds.

**The Anti-Pattern:**
```javascript
// ❌ FORBIDDEN
if (interactions_count >= 16 && vulnerability_shared) {
  evolve_to_cherished();
}
```

**The Correct Pattern:**
```javascript
// ✅ CORRECT
ENGINE_WRITERS_ROOM.assess({
  interaction_history: vector_db.query("interactions_with_npc"),
  quality_indicators: ["emotional_depth", "reciprocity", "consistency"],
  transformative_moments: memory_db.query("vulnerability_shared"),
  personality_compatibility: calculate_compatibility(char, npc),
  current_receptivity: [char.capacity, npc.capacity]
}).then(assessment => {
  if (assessment.qualifies_as_deep_bond) {
    evolve_to_cherished();
  }
});
```

---

## 1. The Three-Layer Architecture

### Overview: DNA → Template → Instance

```
L1: GAMEPLAY DNA (The Concepts)
    ↓ implements
L2: MASTER TEMPLATES (The Archetypes)  ← This document specifies these
    ↓ instantiates via context
L3: CONTEXTUAL INSTANCES (The Cards/Events)
```

**Core Principle:** "Unwritten" does not use static decks. Cards are **generated on-demand** from Master Templates based on current game state.

---

## 2. Layer 1: Gameplay DNA (The Foundation)

**Nature:** Immutable, abstract building blocks that define the **boundaries and logic** of the simulation.

**Purpose:** Establishes the universal categories of human experience that the game can model.

### The Seven Strands

| Strand | Name | Concept | Manifests As |
|--------|------|---------|--------------|
| **1** | The Psyche | Internal mental/emotional states | State Cards (passive modifiers) |
| **2** | Volitional Actions | Intentional activities the character chooses | Action Cards (7-card hand) |
| **3** | Catalytic Events | External forces that disrupt or accelerate | System-triggered Situation Cards |
| **4** | Narrative Structure | Core motivation that shapes the life story | Life Directions, Aspirations |
| **5** | Social Connection | Relationships and interpersonal dynamics | NPCs (Graph DB entities) |
| **6** | Spatial Awareness | Physical locations and their meaning | Locations (Graph DB entities) |
| **7** | Progression & Artifacts | Skills, items, perks, growth | System Cards (persistent elements) |

**Key Insight:** DNA Strands are **categories**, not content. They define *what can exist*, not *what does exist*.

**Cross-Reference:** See `master_truths_canonical_spec_v_1_2.md` for detailed DNA Strand specifications.

---

## 3. Layer 2: Master Templates (The Design Artifact)

**Nature:** Specific implementations of DNA concepts. These are the **~300 designed archetypes** that define the game's scope.

**Purpose:** Provides the rules and parameters for generating infinite unique Contextual Instances.

### What a Master Template Contains

A Master Template is a structured specification that includes:

1. **Identity** - Unique ID, DNA strand mapping, tier classification
2. **Narrative DNA** - Core fantasy, emotional palette, thematic tags
3. **Contextual Filtering Rules** - When this template enters the CFP (Contextually Filtered Pool)
4. **Instantiation Rules** - How to generate Layer 3 instances from this template
5. **Cost Structure** - Qualitative rules for resource costs with modifiers
6. **Outcome Space** - Qualitative spectrums (not binary success/failure)
7. **Evolution System** - How instances transform through meaningful experiences
8. **Fusion Potential** - How this template combines with others

---

## 4. Master Template JSON Schema

### Complete Template Structure

```json
{
  "meta": {
    "id": "ACT_Connect_Informal_Social",
    "dna_strand": "strand_2_volition",
    "archetype": "Social Connection - Low Stakes",
    "tier": "action",
    "version": "1.0.0",
    "author": "Design Team",
    "last_updated": "2025-10-17"
  },
  
  "narrative": {
    "core_fantasy": "The comfort of easy connection with someone you trust",
    "emotional_palette": ["warmth", "presence", "relaxation", "safety"],
    
    "thematic_tags": [
      "routine_building",
      "vulnerability_safe",
      "decompression",
      "familiarity"
    ],
    
    "symbolic_potential": {
      "objects": ["coffee_cups", "favorite_seats", "shared_laughter"],
      "locations": ["cafes", "parks", "familiar_spaces"],
      "rituals": ["tuesday_tradition", "after_work_debrief"]
    },
    
    "narrative_hooks": [
      "Opportunity for unexpected encounter",
      "Setting for vulnerable conversation",
      "Routine that can be disrupted for drama",
      "Location where significant decision can be made"
    ]
  },
  
  "cfp_rules": {
    "base_probability": 0.15,
    
    "required_conditions": [
      {
        "type": "relationship_exists",
        "criteria": "level >= 2 (Friends or closer)"
      },
      {
        "type": "relationship_quality",
        "criteria": "trust >= 0.4"
      },
      {
        "type": "location_available",
        "criteria": "social_informal_space accessible"
      }
    ],
    
    "blocking_conditions": [
      {
        "type": "emotional_state",
        "value": "OVERWHELMED",
        "reason": "Too drained for social interaction"
      },
      {
        "type": "relationship_status",
        "value": "recent_conflict",
        "reason": "Timing not right after fight"
      },
      {
        "type": "financial_crisis",
        "value": "active",
        "reason": "Spending $8 feels wrong during crisis"
      }
    ],
    
    "probability_modifiers": {
      "emotional_states": {
        "CURIOUS": "+30%",
        "LONELY": "+40%",
        "CONFIDENT": "+20%",
        "EXHAUSTED": "-50%",
        "ANXIOUS": "-20%"
      },
      
      "temporal": {
        "weekend": "+25%",
        "friday_evening": "+40%",
        "monday_morning": "-30%"
      },
      
      "personality": {
        "extraversion_high": "+25%",
        "extraversion_low": "-15%",
        "openness_high": "+10%"
      },
      
      "context": {
        "neglected_relationship": "+60%",
        "recent_stressor": "+30%",
        "aspiration_pressure_high": "-20%"
      }
    },
    
    "optimization_notes": {
      "update_frequency": "Only when affected variables change",
      "affected_by": [
        "emotional_state_change",
        "relationship_interaction",
        "time_category_change",
        "financial_status_change"
      ],
      "performance": "Incremental recalculation only"
    }
  },
  
  "narrative_priming": {
    "priming_potential": {
      "latent_tensions": [
        "Sarah is hiding financial troubles",
        "Sarah feeling pressure from family",
        "Unspoken tension about future plans"
      ],
      
      "potential_hooks": [
        "Sarah mentions something cryptic then changes subject",
        "Someone interrupts with news that changes mood",
        "Observation that hints at Sarah's hidden stress"
      ],
      
      "stakes_categories": [
        "friendship_at_crossroads",
        "vulnerability_opportunity",
        "trust_test"
      ],
      
      "volatility_factors": [
        "recent_relationship_tension",
        "character_capacity_vulnerable",
        "npc_capacity_vulnerable",
        "narrative_arc_climax_approaching"
      ]
    },
    
    "priming_modifiers": {
      "high_volatility_conditions": {
        "condition": "VolatilityIndex > 0.7",
        "effect": "Breakthrough outcomes +30-50%, Failure outcomes +10-20%",
        "note": "EWR has full creative control—these are guidelines, not hard rules"
      },
      
      "medium_volatility_conditions": {
        "condition": "VolatilityIndex 0.4-0.7",
        "effect": "Breakthrough outcomes +10-20%, Failure outcomes +5-10%"
      },
      
      "low_volatility_conditions": {
        "condition": "VolatilityIndex < 0.4",
        "effect": "Outcome probabilities remain near base template values"
      }
    },
    
    "resonant_memory_triggers": [
      "previous_vulnerability_moments_with_sarah",
      "shared_difficulties_discussed",
      "promises_made_to_support",
      "locations_with_emotional_weight"
    ]
  },
  
  "instantiation": {
    "tier": 2,
    "ewr_mode": "light",
    "target_latency": "1-3 seconds",
    "fallback_tier": 1,
    
    "required_context": [
      "npc_identity",
      "npc_personality",
      "npc_current_capacity",
      "location_specific",
      "relationship_history",
      "character_emotional_state",
      "time_of_day",
      "recent_life_events",
      "narrative_priming_analysis"
    ],
    
    "generation_strategy": "relational_narrative",
    
    "prompt_framework": {
      "instruction": "Generate a specific instance of an informal social connection. This should feel natural, grounded, and capture the unique dynamic between these two people at this moment in their lives.",
      
      "tone": "Warm, observational, notice small details that reveal relationship depth",
      
      "structure": {
        "title": "[Activity] with [NPC] at [Location]",
        "description": "2-3 sentences. Present tense. Sensory details. Emotional subtext.",
        "outcome_preview": "What this moment offers (connection, support, levity)"
      },
      
      "context_injection": {
        "character_state": "Include current emotional capacity and recent stressors",
        "npc_state": "Include NPC's current life situation if known",
        "location_meaning": "Reference if location has history",
        "relationship_status": "Reflect current intimacy level in tone"
      },
      
      "quality_criteria": [
        "Feels specific to these two people",
        "Reflects current emotional states",
        "Includes sensory grounding",
        "Hints at deeper context without exposition"
      ]
    },
    
    "cost_optimization": {
      "token_budget": "~500 tokens max for T2",
      "caching_strategy": "Cache NPC/location descriptions",
      "batch_generation": "Generate 3-4 instances per EWR call"
    }
  },
  
  "costs": {
    "base": {
      "time": {"min": 60, "max": 120, "unit": "minutes"},
      "energy": {"base": 1, "unit": "points"},
      "money": {"min": 5, "max": 20, "optional": true},
      "emotional_capacity": {"base": 1, "unit": "points"}
    },
    
    "personality_modifiers": {
      "extraversion": {
        "high": {"energy": -0.5, "narrative_tone": "energizing"},
        "low": {"energy": +0.5, "narrative_tone": "draining"}
      },
      
      "neuroticism": {
        "high": {"emotional_capacity": +0.5, "narrative_tone": "anxious_performance"},
        "low": {"emotional_capacity": -0.3, "narrative_tone": "relaxed"}
      }
    },
    
    "contextual_modifiers": {
      "emotional_state": {
        "OVERWHELMED": {"energy": +1, "emotional_capacity": +1},
        "CONFIDENT": {"emotional_capacity": -0.5}
      },
      
      "relationship_depth": {
        "level_5_plus": {"emotional_capacity": -0.5, "feels_restorative": true}
      }
    }
  },
  
  "outcomes": {
    "note": "Outcomes are qualitative spectrums, not discrete tiers. Success depends on personality compatibility, emotional states, and context.",
    
    "success_spectrum": [
      {
        "tier": "pleasant_but_forgettable",
        "probability_base": 0.5,
        "conditions": "Default outcome when no special conditions met",
        
        "effects": {
          "meters": {"social": +1, "emotional": +1},
          "relationship": {"trust": +0.02, "bond": +0.01}
        },
        
        "narrative_tone": "Nice, but routine. Life continues.",
        "memory_weight": 2,
        "archive_treatment": "Compressed in daily summary"
      },
      
      {
        "tier": "meaningful_connection",
        "probability_base": 0.3,
        "conditions": [
          "Both characters emotionally available (Capacity > 4.0)",
          "OR: Recent stressor creates opening for support"
        ],
        
        "effects": {
          "meters": {"social": +2, "emotional": +2},
          "relationship": {"trust": +0.05, "bond": +0.03}
        },
        
        "narrative_tone": "Genuine moment. They really saw you.",
        "memory_weight": 5,
        "archive_treatment": "Preserved as distinct memory",
        
        "unlock_potential": {
          "fusion_opportunity": true,
          "evolution_check": "ENGINE_WRITERS_ROOM assesses pattern"
        }
      },
      
      {
        "tier": "breakthrough_vulnerability",
        "probability_base": 0.15,
        
        "required_conditions": [
          {
            "type": "relationship_quality",
            "criteria": "trust >= 0.6"
          },
          {
            "type": "emotional_receptivity",
            "criteria": "Both characters Capacity >= 4.5"
          },
          {
            "type": "timing",
            "criteria": "Natural vulnerability opening exists"
          }
        ],
        
        "assessment_method": "ENGINE_WRITERS_ROOM evaluates readiness",
        "cannot_be_forced": true,
        
        "effects": {
          "meters": {"social": +3, "emotional": +3},
          "relationship": {
            "trust": +0.15,
            "bond": +0.08,
            "intimacy_deepened": true,
            "journey_beat": "Vulnerability Moment achieved"
          }
        },
        
        "narrative_tone": "They told you something they've never told anyone. The air changed.",
        "memory_weight": 9,
        "archive_treatment": "Major memory, chapter-level significance",
        
        "memory_facets": {
          "primary": {
            "generation_prompt": "Core emotional takeaway—what this vulnerability moment meant",
            "weight": "8-9 (high significance)",
            "visibility": "Player-visible in Archive UI",
            "example": "Sarah shared her deep doubts about the café. I supported her. We connected."
          },
          
          "sensory": {
            "generation_prompt": "2-3 specific ambient details that anchor this memory",
            "weight": "3-5 per facet",
            "visibility": "Backend only—for future resonance triggers",
            "triggers": ["visual cues", "sounds", "physical sensations", "location ambiance"],
            "examples": [
              "The way the afternoon light hit the window",
              "The weight of the ceramic mug in your hands",
              "The sound of her voice when she said 'I don't think I can do this'"
            ]
          },
          
          "observational": {
            "generation_prompt": "1-2 noticed details that hold future narrative potential",
            "weight": "4-6 per facet",
            "visibility": "Backend only—for Weekly EWR Analysis",
            "intrigue_tags": ["hook", "mystery", "unresolved", "foreshadowing"],
            "examples": [
              "Sarah kept checking her phone nervously before she opened up. Who was texting her?",
              "She mentioned her family in Seattle almost wistfully. Does she want to go back?"
            ],
            "pattern_tracking": "Assign pattern_id for cross-week correlation"
          }
        },
        
        "unlock_potential": {
          "evolution_immediate": "If pattern + transformative moment criteria met",
          "fusion_unlock": ["vulnerability_shared", "trust_milestone"],
          "creates_memory": "Defining moment in relationship"
        }
      }
    ],
    
    "failure_spectrum": [
      {
        "tier": "awkward_but_harmless",
        "probability_base": 0.1,
        
        "effects": {
          "meters": {"social": 0, "emotional": -1},
          "relationship": {"trust": 0}
        },
        
        "narrative_tone": "Conversation fell flat. You both checked your phones.",
        "memory_weight": 1
      },
      
      {
        "tier": "unintentional_hurt",
        "probability_base": 0.05,
        
        "conditions": [
          "Character Capacity < 3.0 (too drained to be present)",
          "OR: Unresolved relationship tension exists"
        ],
        
        "effects": {
          "meters": {"social": -2, "emotional": -2},
          "relationship": {"trust": -0.05, "tension": +0.1}
        },
        
        "narrative_tone": "You said something wrong. They pulled back.",
        "memory_weight": 6,
        "archive_treatment": "Preserved (negative moments create story)",
        
        "triggers_event": {
          "template": "EVT_Relationship_Tension",
          "probability": 0.3
        }
      }
    ]
  },
  
  "evolution": {
    "stages": ["generic", "personalized", "cherished"],
    "note": "Evolution is assessed by ENGINE_WRITERS_ROOM based on qualitative patterns, NOT fixed thresholds.",
    
    "generic_to_personalized": {
      "trigger_type": "pattern_detection",
      
      "assessment_method": {
        "engine": "ENGINE_WRITERS_ROOM",
        "process": "Semantic analysis of interaction history via Vector DB",
        "evaluates": [
          "Consistency of connection (not count, but quality pattern)",
          "Emotional reciprocity established",
          "Comfort level reached between both parties",
          "Personality compatibility demonstrated",
          "Natural rhythm developed"
        ]
      },
      
      "qualitative_indicators": [
        "Characters reference shared experiences naturally",
        "Conversation flows without effort",
        "Both parties initiate contact",
        "Small rituals have formed (usual table, usual order)",
        "Comfort with silence"
      ],
      
      "timing_examples": {
        "high_compatibility": "May happen after 2-3 interactions",
        "neutral_compatibility": "May take 15-20 interactions",
        "low_compatibility": "May never happen despite many interactions",
        "note": "Interaction count is correlation, not causation"
      },
      
      "forbidden_pattern": {
        "bad": "if (interaction_count >= 8) { evolve(); }",
        "correct": "if (ENGINE_WRITERS_ROOM.detects_familiarity_pattern()) { evolve(); }"
      },
      
      "transformation": {
        "title_evolves": "Coffee with Friend → Coffee with Sarah",
        "narrative_shift": "This has become your spot. She's not just 'a friend' anymore.",
        
        "new_effects": {
          "costs_reduced": {"emotional_capacity": -0.5},
          "memory_weight_baseline": 4,
          "relationship_bonding": "+5%"
        }
      }
    },
    
    "personalized_to_cherished": {
      "trigger_type": "transformative_moment",
      
      "assessment_method": {
        "engine": "ENGINE_WRITERS_ROOM (Tier 3 - Heavy)",
        "process": "Deep semantic analysis + narrative weight calculation",
        "evaluates": [
          "Breakthrough outcome occurred during instance",
          "Journey Beat achieved (Vulnerability Moment or Crisis Support)",
          "Emotional significance evident in both parties",
          "Memory resonance potential high",
          "Relationship reached new depth"
        ]
      },
      
      "required_conditions": [
        {
          "type": "qualitative_moment",
          "description": "A transformative experience happened during this activity"
        },
        {
          "type": "emotional_receptivity",
          "description": "Both characters were emotionally present and available"
        },
        {
          "type": "relationship_depth",
          "description": "Bond has reached level where this matters deeply"
        }
      ],
      
      "examples_of_transformative_moments": [
        "Vulnerability shared that deepened trust",
        "Decision made together that affected life path",
        "Support given during crisis that proved bond",
        "Revelation experienced that changed perspective",
        "Ritual interrupted by major event, became memorial"
      ],
      
      "timing_note": "One profound conversation at 3 AM can trigger this. Twenty surface-level meetings won't.",
      
      "transformation": {
        "becomes_unique_memory": true,
        "title_example": "Tuesday Afternoons at Café Luna",
        "narrative_shift": "This place, this time, this person—it's sacred now. A ritual that grounds you.",
        
        "new_effects": {
          "costs_reduced": {"energy": -1, "emotional_capacity": -1},
          "capacity_restore": +0.3,
          "memory_resonance": "high",
          "referenced_in_future": true,
          "appears_in_season_novel": "Chapter-level scene"
        },
        
        "visual_treatment": {
          "card_frame": "Golden/special border",
          "art_style": "Unique, personalized illustration",
          "ui_indicator": "Cannot be discarded"
        }
      }
    },
    
    "can_exist_simultaneously": true,
    "note_on_coexistence": "Generic instance can still appear in CFP while Personalized/Cherished versions exist. Player chooses which relationship to engage."
  },
  
  "fusion": {
    "tier_requirement": "TIER_3_ONLY",
    "detection_method": "Semantic resonance via Vector DB during high-intensity Tier 3 events",
    "narrative_interlude": "REQUIRED (5-10s parallel processing)",
    
    "timing_clarification": {
      "when_detected": "During Tier 3 high-intensity events ONLY",
      "not_standalone": "Fusion doesn't happen during routine Tier 2 cards",
      "catalyst_required": "Must occur within context of major emotional event"
    },
    
    "symbolic_tags": [
      "intimacy_building",
      "routine_formation",
      "stress_relief",
      "emotional_support",
      "conversation_opportunity",
      "vulnerability",
      "location_significance"
    ],
    
    "combines_well_with": {
      "high_intensity_events": [
        "EVT_Breakup",
        "EVT_Death",
        "EVT_Breakthrough",
        "EVT_Life_Direction_Shift",
        "ACT_Evolution_to_Cherished (with transformative moment)"
      ],
      "note": "Fusion occurs DURING these Tier 3 events, not as separate action"
    },
    
    "fusion_detection": {
      "engine": "ENGINE_WRITERS_ROOM (Tier 3 - Heavy)",
      "process": "Deep semantic analysis via Vector DB during Tier 3 event",
      "criteria": [
        "Thematic tags align (symbolic_potential overlap)",
        "Contextual co-occurrence (present in scene)",
        "Emotional intensity sufficient (Tier 3 catalyst)",
        "Semantic clustering tight (high Vector DB similarity)"
      ],
      "threshold": "HIGH—better to miss fusion than force it"
    },
    
    "parallel_processing_during_narrative_interlude": {
      "thread_1_dialogue": {
        "system": "Local dialogue LLM",
        "task": "Generate fusion narrative—how concepts merge",
        "latency": "3-5 seconds"
      },
      
      "thread_2_ewr": {
        "system": "ENGINE_WRITERS_ROOM (Tier 3)",
        "tasks": [
          "Create fused entity with new properties",
          "Generate Memory Facets for fusion moment",
          "Calculate narrative implications",
          "Queue follow-up events",
          "Check for related card evolutions"
        ],
        "latency": "5-8 seconds"
      },
      
      "thread_3_art": {
        "system": "Image generation API",
        "task": "Generate unique art showing symbolic fusion",
        "latency": "5-30 seconds",
        "note": "May complete after interlude, fades in when ready"
      },
      
      "synchronization": {
        "interlude_duration": "Max of Thread 1 and 2 (typically 5-8s)",
        "player_returns": "When dialogue + entity properties ready",
        "art_async": "Appears when ready, not blocking"
      }
    },
    
    "fusion_examples": [
      {
        "catalyst": "EVT_Breakup (Tier 3)",
        "context": "Occurs at Café Luna, Sarah gives you her mug",
        "components": [
          "mem_sarah_doubt_cafe_luna",
          "ITEM_Coffee_Mug (present in scene)",
          "LOC_Cafe_Luna (event location)"
        ],
        "fusion_detection": "Vector DB finds high resonance (all cafe-related, emotional_anchor tags)",
        "fusion_output": "ARTIFACT_The_Breakup_Mug",
        "narrative": "Sarah slid her favorite mug across the table. 'Keep it,' she said. 'Remember me.' Then she left. You're still holding it.",
        "mechanical_effect": "-0.5 Capacity when in inventory (painful reminder)",
        "memory_facets": {
          "primary": "The day Sarah gave me her mug and walked away",
          "sensory": ["Sound of ceramic sliding", "Warmth in the handle"],
          "observational": ["Why did she give it to me? What was she really saying?"]
        },
        "narrative_interlude_triggered": "Yes—'A connection sparks... This will stay with you.'"
      },
      {
        "catalyst": "ACT_Connect_Informal_Social → Cherished Evolution (Tier 3)",
        "context": "Transformative breakthrough during coffee ritual",
        "components": [
          "This template (evolving to Cherished)",
          "LOC_Cafe_Luna",
          "mem_multiple_shared_moments"
        ],
        "fusion_detection": "Pattern + transformative moment + location significance",
        "fusion_output": "CHERISHED_Tuesday_Afternoons_at_Cafe_Luna",
        "narrative": "This place, this time, this person—it's sacred now.",
        "mechanical_effect": "Costs reduced, Capacity restored, memory resonance HIGH",
        "narrative_interlude_triggered": "Yes—'This moment will stay with you.'"
      },
      {
        "catalyst": "EVT_Career_Decision (Tier 3)",
        "context": "Major life choice made during cherished ritual",
        "components": [
          "CHERISHED_Tuesday_Afternoons_at_Cafe_Luna",
          "EVT_Career_Decision"
        ],
        "fusion_detection": "Sacred location + life-changing decision",
        "fusion_output": "LOCATION_Cafe_Luna_Decision_Memorial",
        "narrative": "This is the table where you decided to quit your job. The place where everything changed.",
        "mechanical_effect": "Location gains 'Decision Memorial' tag, always triggers memory",
        "narrative_interlude_triggered": "Yes"
      }
    ]
  },
  
  "related_templates": [
    "LOC_Base_Community_Hub",
    "CHAR_Base_Friend",
    "EVT_Base_Relationship_Deepening",
    "ACT_Vulnerability_Share",
    "STATE_Lonely"
  ],
  
  "design_notes": {
    "target_experience": "This should feel like spending time with someone who matters, where the relationship is strong enough that you can just *be* without performance.",
    
    "anti_patterns": [
      "Don't make this feel transactional",
      "Don't gate evolution behind repetition without meaning",
      "Don't make every instance feel identical"
    ],
    
    "success_criteria": [
      "Player wants to prioritize this over 'optimal' choices",
      "Evolution feels earned and special",
      "Cherished version is genuinely different experience"
    ],
    
    "balance_notes": {
      "cfp_weight_testing": "Monitor probability in playtests to prevent stale hands",
      "cost_tuning": "Ensure introverts aren't punished, just experience differently",
      "outcome_distribution": "Most should be pleasant-but-forgettable; breakthroughs rare"
    }
  },
  
  "production_metadata": {
    "creation_date": "2025-10-17",
    "last_modified": "2025-10-17",
    "version_history": [
      {
        "version": "1.0.0",
        "date": "2025-10-17",
        "changes": "Initial template creation with anti-gamification refinements"
      }
    ],
    "assigned_designer": "Core Design Team",
    "review_status": "Approved",
    "implementation_status": "Specification Complete",
    "test_scenarios_defined": false
  }
}
```

**⚠️ Note on "Tier" Terminology:**

This template uses "tier" in two different contexts:

1. **`meta.tier`**: Card Type Classification (Seven-Tier Structure)
   - Values: `"foundation"`, `"quest"`, `"routine"`, `"action"`, `"catalyst"`, `"system"`, `"living_world"`
   - Refers to: Which of the seven card categories this template belongs to (see `02-card-system-architecture.md`)
   - Example: This template is tier `"action"` (Tier 4: Activity Cards in the 7-card hand)

2. **`instantiation.tier`**: Generation Complexity (Tiered Generation Strategy)
   - Values: `1`, `2`, or `3`
   - Refers to: Which generation tier is used to instantiate this template
   - Tier 1 = Local/instant (<100ms), Tier 2 = Cloud EWR-Light (1-3s), Tier 3 = Cloud EWR-Heavy (5-10s)
   - Example: This template uses tier `2` (EWR-Light generation)

---

## 5. Parallel Processing in Narrative Interludes

**Context:** When Fusion or Cherished Evolution occurs (Tier 3 events), the system triggers a **Narrative Interlude** lasting 5-10 seconds. This section documents how that time is utilized efficiently.

### The Three Parallel Threads

```javascript
const NARRATIVE_INTERLUDE_PROCESSING = {
  
  trigger_conditions: [
    "Fusion opportunity detected during Tier 3 event",
    "Card Evolution to Cherished with transformative moment",
    "Major Catalytic Event resolution",
    "Season climax sequence"
  ],
  
  parallel_threads: {
    
    thread_1_dialogue_generation: {
      system: "Local dialogue LLM (on-device or fast cloud)",
      task: "Generate fusion/evolution narrative moment",
      input: {
        "fusion_components": ["mem_id", "item_id", "location_id"],
        "emotional_context": "Current character state + catalyst",
        "style": "Literary, intimate, shows how concepts merge"
      },
      latency: "3-5 seconds typical",
      output: "Narrative text player will read",
      example: `Sarah slid her favorite mug across the table. 
               'Keep it,' she said. 'Remember me.' 
               Then she left. You're still holding it.`
    },
    
    thread_2_ewr_heavy_processing: {
      system: "ENGINE_WRITERS_ROOM (Tier 3)",
      tasks: [
        "Create fused entity with new L3 properties",
        "Generate Memory Facets (Primary, Sensory, Observational)",
        "Calculate narrative implications (relationship impacts)",
        "Queue potential follow-up events",
        "Check for related card evolutions",
        "Update symbolic tags for future fusion detection"
      ],
      latency: "5-8 seconds typical",
      output: "Fused entity data structure + Memory Object",
      cost: "$0.015-$0.025 per fusion"
    },
    
    thread_3_art_generation: {
      system: "Image generation API (async)",
      task: "Generate unique art showing symbolic fusion",
      input: {
        "prompt": "Generated from fused entity description",
        "style": "Consistent art style (watercolor impressionistic)",
        "composition": "Focus on symbolic meaning"
      },
      latency: "5-30 seconds (highly variable)",
      handling: "Async—continues after interlude if needed",
      note: "Art fades in when ready, never blocks gameplay"
    }
  },
  
  synchronization: {
    critical_path: "Thread 1 + Thread 2 must complete",
    interlude_duration: "Max of Thread 1 and Thread 2 (typically 5-8s)",
    
    when_threads_complete: {
      thread_1_ready: "Narrative text generated",
      thread_2_ready: "Fused entity properties calculated",
      action: "End interlude, show narrative + new card"
    },
    
    thread_3_art_handling: {
      if_ready_in_time: "Display with full card immediately",
      if_not_ready: {
        placeholder: "Template-category placeholder art shown",
        async_update: "Art fades in when generation completes",
        player_impact: "Delightful surprise, not blocking"
      }
    }
  },
  
  player_experience: {
    visual: "Memory web animation, thematic text overlay",
    feeling: "Witnessing profound moment crystallize",
    no_frustration: "Feels intentional, not 'loading'",
    outcome: "Returns to game with new unique entity"
  }
};
```

### Why Parallel Processing Matters

**Without Parallelization:**
```
Thread 1 (dialogue):  5s
Thread 2 (EWR):      8s
Thread 3 (art):     20s
─────────────────────────
Total:              33s (unacceptable)
```

**With Parallelization:**
```
Thread 1 (dialogue):  ████████░░░░░░░░░░░░░░░░░ (5s)
Thread 2 (EWR):      ████████████████░░░░░░░░░ (8s) ← Critical path
Thread 3 (art):      ████████████████████████████████ (20s, async)
─────────────────────────
Interlude duration:  8s (acceptable)
Art appears:         +12s later (non-blocking)
```

### Cost Optimization

**Tier 3 Fusion/Evolution Processing Breakdown:**

```json
{
  "per_fusion_event": {
    "dialogue_generation": "$0.008",
    "ewr_heavy_processing": "$0.015",
    "memory_facets_generation": "$0.005",
    "fusion_detection_overhead": "$0.003",
    "art_generation": "$0.025 (separate async)",
    
    "total_blocking": "$0.031 (dialogue + EWR + facets + detection)",
    "total_with_art": "$0.056"
  },
  
  "frequency_expectations": {
    "fusions_per_season": "2-5",
    "evolutions_to_cherished_per_season": "3-6",
    "total_tier_3_interludes_per_season": "5-11",
    
    "cost_per_season_tier_3": "$0.31 - $0.62 (without art)",
    "cost_per_season_with_art": "$0.56 - $1.12 (with art)"
  },
  
  "optimization_strategies": [
    "Batch Memory Facet generation with outcome",
    "Cache symbolic tag embeddings",
    "Reuse art for similar fusions (with variations)",
    "Progressive enhancement: good art → great art"
  ]
}
```

### Implementation Notes

**Critical Requirements:**

1. **Thread Safety**: All three threads write to separate data structures, merged at end
2. **Timeout Handling**: If Thread 1 or 2 exceeds 10s, show fallback text and continue
3. **Art Failure Handling**: If art generation fails, placeholder remains (game continues)
4. **Cancellation**: If player force-quits during interlude, save partial state safely

**Testing Scenarios:**

- Fusion during low battery (art generation may be slower)
- Network interruption during Thread 2 (EWR) processing
- Multiple fusions in rapid succession (< 1 minute apart)
- Player backgrounding app during interlude

---

## 6. Template Design Checklist

Before submitting a Master Template, verify:

### ✅ Anti-Gamification Compliance

- [ ] No fixed numerical thresholds for evolution (e.g., "must do X times")
- [ ] All progression uses `ENGINE_WRITERS_ROOM` qualitative assessment
- [ ] Evolution criteria are contextual (personality, capacity, timing matter)
- [ ] Grinding cannot bypass meaningful progression
- [ ] Assessment criteria documented in plain language

### ✅ CFP Optimization

- [ ] `update_frequency` specified (which variables trigger recalculation)
- [ ] Incremental update strategy documented
- [ ] Base probability set appropriately for frequency expectation
- [ ] Blocking conditions prevent inappropriate appearances
- [ ] Probability modifiers are reasonable (avoid extreme spikes)

### ✅ Instantiation Quality

- [ ] Appropriate tier selected (1/2/3 based on narrative complexity)
- [ ] Required context clearly defined
- [ ] Prompt framework provides quality criteria
- [ ] Token budget specified for cost optimization
- [ ] Fallback strategy defined for tier degradation

### ✅ Outcome Design

- [ ] Success spectrum has multiple tiers (not binary)
- [ ] Failure outcomes create narrative opportunities
- [ ] Most common outcome is pleasant-but-routine
- [ ] Breakthrough outcomes have meaningful unlock potential
- [ ] Memory weights assigned appropriately

### ✅ Evolution System

- [ ] Each stage has qualitative assessment criteria
- [ ] Timing examples show variability based on context
- [ ] Transformation is mechanically and narratively significant
- [ ] "Cannot be forced" principle maintained
- [ ] Visual/UI treatment specified for each stage

### ✅ Production Readiness

- [ ] All required JSON fields populated
- [ ] Related templates cross-referenced
- [ ] Design notes explain intent
- [ ] Balance considerations documented
- [ ] Test scenarios identified

---

## 6. Internal Tooling Requirements

### CFP Visualization Tool

**Purpose:** Allow designers to see real-time probability weights across templates.

**Features:**
- Live game state simulator
- Template probability heatmap
- "What if" scenario testing
- Stale hand detection
- Export probability flow diagrams

### Template Editor

**Purpose:** Structured editor for creating/editing Master Templates.

**Features:**
- JSON schema validation
- Anti-gamification checker (flags numerical thresholds)
- Duplicate field detection
- Cross-reference validator
- Version control integration

### EWR Cost Estimator

**Purpose:** Predict operational costs for template generation.

**Features:**
- Token usage estimation per template
- Tier 2 vs Tier 3 cost comparison
- Batch generation optimization suggestions
- Caching opportunity identification
- Monthly cost projection

### Evolution Simulator

**Purpose:** Test evolution pathways with various personality/context combinations.

**Features:**
- Personality profile builder
- Interaction history simulator
- Qualitative assessment preview
- Evolution timing prediction
- Edge case identification

---

## 7. Tier Selection Guidelines

| Tier | When to Use | Latency | Cost | Example Templates |
|------|-------------|---------|------|-------------------|
| **Tier 1 (Local)** | Routine, low-narrative-complexity actions | < 100ms | None | Work tasks, routines, simple activities |
| **Tier 2 (EWR-Light)** | Personalized social/creative actions | 1-3s | Low | Social connections, creative work, exploration |
| **Tier 3 (EWR-Heavy)** | Major events, evolutions, fusions | 5-10s | High | Catalytic events, breakthroughs, cherished evolutions |

**Optimization Strategy:** Default to Tier 2 for most templates. Use Tier 1 for templates that appear frequently and have low narrative variance. Reserve Tier 3 for moments that justify the "Narrative Interlude" experience.

---

## 8. Common Pitfalls

### ❌ Pitfall 1: Hidden Numerical Thresholds

**Bad:**
```json
"generic_to_personalized": {
  "conditions": ["familiarity_score >= 0.7"]
}
```

**Why:** "Familiarity score" is just a counter in disguise.

**Good:**
```json
"generic_to_personalized": {
  "assessment": "ENGINE_WRITERS_ROOM analyzes interaction history semantically",
  "criteria": ["comfort_pattern", "reciprocity", "consistency"]
}
```

### ❌ Pitfall 2: Over-Complex CFP Modifiers

**Bad:**
```json
"probability_modifiers": {
  "every_possible_variable": "different_modifier"
}
```

**Why:** Creates balancing nightmare and performance issues.

**Good:** Focus on 3-5 most impactful variables per template.

### ❌ Pitfall 3: Binary Outcomes

**Bad:**
```json
"outcomes": {
  "success": {...},
  "failure": {...}
}
```

**Why:** Life isn't binary. Most outcomes should be mixed.

**Good:** Use spectrums with 3-5 tiers, emphasizing "pleasant but forgettable" as most common.

### ❌ Pitfall 4: Identical Instances

**Bad:** Using Tier 1 for templates that should feel unique every time.

**Why:** Breaks immersion when "Coffee with Sarah" has identical text every instance.

**Good:** Use Tier 2 for social/creative templates to ensure narrative variety.

---

## 9. Template Production Pipeline

```
1. CONCEPT
   └─> Designer drafts template concept
   
2. SCHEMA
   └─> Populate JSON using Template Editor tool
   
3. VALIDATION
   └─> Anti-gamification checker
   └─> Schema validator
   └─> Cross-reference checker
   
4. SIMULATION
   └─> CFP Visualizer (check for stale hands)
   └─> Evolution Simulator (test pathways)
   └─> Cost Estimator (verify tier assignment)
   
5. REVIEW
   └─> Design team reviews
   └─> Approve or request revisions
   
6. IMPLEMENTATION
   └─> Engineering implements template
   └─> QA validates generation quality
   
7. BALANCING
   └─> Playtest monitoring
   └─> CFP weight adjustments
   └─> Outcome probability tuning
```

---

## 10. Cross-Reference Map

**Related Documents:**
- `07-genesis-plan.md` - Phased template creation roadmap
- `09-turn-structure.md` - How templates instantiate during gameplay
- `10-validating-template-design.md` - Quality assurance framework
- `06-growth-and-progression.md` - Evolution and Journey Beat mechanics
- `master_truths_canonical_spec_v_1_2.md` - DNA Strand specifications

**Core Systems:**
- `ENGINE_WRITERS_ROOM` - Qualitative assessment and instantiation
- `ENGINE_PERSONALITY` - OCEAN modifiers and perceptual filtering
- `ENGINE_CAPACITY` - Emotional bandwidth and receptivity
- `ENGINE_MEMORY` - Vector DB queries and pattern detection

---

## The Template Specification Promise

**What This Structure Achieves:**

✅ **Anti-gamification enforced** - No hidden counters, qualitative assessment mandatory  
✅ **Scalable production** - 300+ templates designed with consistent structure  
✅ **Performance optimized** - Incremental CFP updates, tier-appropriate generation  
✅ **Cost-effective** - Token budgets and batch generation strategies  
✅ **Maintainable** - Modify template once, affects all instances  
✅ **AI-native** - Built for `ENGINE_WRITERS_ROOM` from ground up  

**The Ultimate Goal:**

> By following this specification, we create Master Templates that generate **infinite unique experiences** through contextual instantiation—where progression emerges from authentic emotional experiences assessed by sophisticated AI, not arbitrary numerical gates.

**This is not a card game. This is a life story simulation engine.**

