# Multi-Season Continuity System - Complete Implementation

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete system for maintaining continuity, memory, and consistency across 8-10 seasons with emotional resonance, dramatic irony tracking, and quality validation

**References:**
- **Multi-Season Design:** `1.concept/22-multi-lifetime-continuity.md` (philosophy)
- **Season Flow:** `73-season-flow-implementation.md` (inter-season transitions)
- **Card Evolution:** `21-card-evolution-mechanics.md` (cross-season card persistence)

---

## Overview

**Unwritten is a multi-season life simulation** where ONE character lives through 8-10 complete seasons (each season = 12/24/36 weeks). The continuity system ensures that Sarah from Season 1 is the same Sarah in Season 8—with all accumulated history, evolved relationships, and shared memories intact.

**Challenge:** Maintain **consistency** and **meaningful evolution** across 200-360 weeks without:
- Contradictions (Sarah can't forget major events)
- Narrative bloat (can't store every detail)
- Performance issues (memory footprint must stay reasonable)

**Solution:** Four-tier context system with intelligent compression.

---

## Four-Tier Context Architecture

### Tier Structure

```typescript
interface MultiSeasonContext {
  tier_1_active: {
    scope: "Last 12 weeks (current season tail)",
    detail_level: "Complete - every card play, every conversation",
    size: "~2MB",
    query_speed: "Instant",
    used_for: "Immediate continuity, recent references"
  };
  
  tier_2_recent: {
    scope: "Previous 2-3 seasons (24-72 weeks)",
    detail_level: "High - major events, relationship milestones, decisions",
    size: "~5MB",
    query_speed: "Very fast",
    used_for: "Recent history references, relationship context"
  };
  
  tier_3_compressed: {
    scope: "All earlier seasons (seasons 1-5 when in season 8)",
    detail_level: "Heavily compressed - 50:1 ratio",
    compression_strategy: "Keep defining moments, discard routine",
    size: "~5-10MB",
    query_speed: "Fast",
    used_for: "Long-term character arc, major life events"
  };
  
  tier_4_canonical_state: {
    scope: "Current state snapshot",
    detail_level: "Complete current character sheet",
    size: "~1MB",
    query_speed: "Instant",
    used_for: "What is true NOW"
  };
  
  canonical_facts: {
    scope: "Immutable truths that never change",
    detail_level: "Complete fact database",
    size: "~2MB",
    query_speed: "Instant",
    used_for: "Preventing contradictions"
  };
}
```

**Total Memory Footprint:** ~15-20MB for complete 8-10 season character

---

## TIER 1: ACTIVE CONTEXT (Last 12 Weeks)

### Complete Detail Storage

```javascript
const TIER_1_ACTIVE = {
  scope: "Last 12 weeks",
  detail_level: "Complete - every card play, every conversation",
  
  contains: {
    current_season: {
      season_number: 8,
      season_title: "The Bookshop Opening",
      season_length_selected: 36,            // Player chose Epic
      weeks_in_season: 36,
      current_week: 28,
      aspiration: "Open bookshop with Sarah",
      act: 2                                 // Act II of three-act structure
    },
    
    every_turn: [
      {
        week: 28,
        day: 3,
        turn: "afternoon",
        cards_played: ["Work on Bookshop Plans", "Coffee with Sarah"],
        outcome: {
          success: true,
          progress: "+5% aspiration",
          sarah_trust: +0.05,
          narrative: "Finalized the layout. Sarah loved your ideas."
        },
        emotional_state: "EXCITED",
        meters: { physical: 6, mental: 7, social: 8, emotional: 8 }
      }
      // ... every single turn for 12 weeks
    ],
    
    all_conversations: [
      {
        week: 27,
        npc: "Sarah",
        topic: "Bookshop name brainstorming",
        depth_level: 8,
        reveals: "Sarah wants to honor David by including poetry section",
        memory_significance: 9
      }
      // ... every conversation
    ],
    
    relationship_changes: {
      sarah: {
        level: 5,
        trust: 0.98,
        interactions_this_period: 47,
        major_moments: [
          "Week 25: Sarah asked you to be co-owner",
          "Week 27: Shared David memory again",
          "Week 28: Finalized partnership contract"
        ]
      },
      marcus: {
        level: 4,
        trust: 0.85,
        interactions_this_period: 12,
        major_moments: [
          "Week 26: Marcus helped with construction"
        ]
      }
    },
    
    skill_progression: {
      business_management: { start: 3.2, current: 4.1, gain: +0.9 },
      photography: { current: 7.8 },       // Stable
      design: { start: 4.5, current: 5.2, gain: +0.7 }
    },
    
    financial_tracking: {
      week_20_balance: 8500,
      week_28_balance: 3200,
      major_expenses: [
        { week: 22, item: "Bookshop lease deposit", amount: -3000 },
        { week: 25, item: "Renovation costs", amount: -2500 }
      ]
    }
  },
  
  query_examples: {
    "What did Sarah say about David recently?": "Week 27 - wants poetry section to honor him",
    "How much money have I spent on bookshop?": "$5,500 in last 8 weeks",
    "When did Marcus last help?": "Week 26 - construction help"
  },
  
  used_for: [
    "Immediate conversation continuity",
    "Recent event references",
    "Short-term consequence tracking",
    "NPC memory of recent interactions"
  ]
};
```

---

## TIER 2: RECENT HISTORY (Previous 2-3 Seasons)

### High Detail with Event Filtering

```javascript
const TIER_2_RECENT = {
  scope: "Seasons 6-7 (previous 48 weeks before current season)",
  detail_level: "High - major events, decisions, milestones",
  
  contains: {
    season_6: {
      season_title: "Starting Over",
      season_length: 24,
      aspiration: "Recover from career burnout, find new path",
      result: "Partial success - discovered love of design",
      
      defining_moments: [
        {
          week: 6,
          event: "Quit corporate job (phase transition)",
          choice: "Take time to figure it out",
          consequence: "Financial stress but emotional relief"
        },
        {
          week: 12,
          event: "First freelance design client (breakthrough)",
          significance: "Realized I could do this full-time"
        },
        {
          week: 18,
          event: "Sarah suggested bookshop collaboration",
          significance: "Planted seed for Season 8 aspiration"
        },
        {
          week: 22,
          event: "Marcus intervention about money stress",
          significance: "Trust deepened, borrowed $2000"
        }
      ],
      
      relationship_evolution: {
        sarah: {
          level_start: 4,
          level_end: 4,
          trust_start: 0.80,
          trust_end: 0.92,
          major_milestones: [
            "Week 18: Proposed bookshop idea",
            "Week 24: Committed to partnership"
          ]
        },
        marcus: {
          level_start: 4,
          level_end: 5,                      // Upgraded during crisis
          major_milestone: "Week 22: Loan during financial crisis"
        }
      },
      
      skill_changes: {
        design: { start: 2.1, end: 4.5, gain: +2.4 },
        photography: { start: 7.5, end: 7.8, gain: +0.3 }
      },
      
      financial_summary: {
        started_with: 12000,
        ended_with: 5500,
        major_changes: "Quit job, freelance income variable"
      }
    },
    
    season_7: {
      season_title: "Building the Foundation",
      season_length: 24,
      aspiration: "Establish freelance design business",
      result: "Success - sustainable income, ready for next step",
      
      defining_moments: [
        {
          week: 8,
          event: "First $5k month freelancing",
          significance: "Financial viability proven"
        },
        {
          week: 16,
          event: "Sarah found potential bookshop location",
          significance: "Made it real, not just a dream"
        },
        {
          week: 20,
          event: "Decided to pursue bookshop in Season 8",
          significance: "Major life decision made"
        }
      ],
      
      relationship_evolution: {
        sarah: {
          level_start: 4,
          level_end: 5,                      // Best friend status
          trust_start: 0.92,
          trust_end: 0.95,
          major_milestone: "Week 20: Committed to shared dream"
        }
      }
    }
  },
  
  query_examples: {
    "When did I quit my job?": "Season 6, Week 6",
    "How did Sarah and I decide on the bookshop?": "S6W18 she suggested, S7W20 we committed",
    "What's my history with Marcus helping financially?": "S6W22 he loaned me $2000"
  },
  
  compression_rules: {
    keep: "Defining moments, major decisions, relationship milestones, skill jumps",
    discard: "Routine turns, repeated activities, minor conversations"
  }
};
```

---

## TIER 3: COMPRESSED HISTORY (All Earlier Seasons)

### Heavy Compression (50:1 Ratio)

```javascript
const TIER_3_COMPRESSED = {
  scope: "Seasons 1-5 (first 5 seasons, ~120-150 weeks)",
  detail_level: "Heavily compressed - 50:1 ratio",
  compression_strategy: "Keep defining moments, discard routine",
  
  contains: {
    season_1: {
      title: "Finding My Footing",
      length: 12,
      aspiration: "Get promoted at corporate job",
      result: "Success",
      
      character_defining_moments: [
        {
          week: 3,
          event: "Met Sarah at Café Luna",
          significance: 10,
          why_preserved: "First meeting with major character"
        },
        {
          week: 6,
          event: "Marcus became close friend",
          significance: 9,
          why_preserved: "Core relationship established"
        },
        {
          week: 11,
          event: "Got promotion",
          significance: 7,
          why_preserved: "Aspiration success"
        }
      ],
      
      end_state: {
        relationships: { sarah: 2, marcus: 3 },
        skills: { corporate_work: 5.2, photography: 2.1 },
        money: 8500,
        life_direction: "Achieve Financial Security"
      },
      
      discarded_detail: "~95% of routine turns, minor conversations",
      preserved: "3 defining moments that shape future seasons"
    },
    
    season_2: {
      title: "The Photography Dream",
      length: 24,
      aspiration: "Launch photography business",
      result: "Partial success",
      
      character_defining_moments: [
        {
          week: 8,
          event: "Sarah revealed David story",
          significance: 10,
          why_preserved: "Major relationship milestone + mystery solved"
        },
        {
          week: 14,
          event: "Collapsed during wedding shoot (health crisis)",
          significance: 10,
          why_preserved: "Life-changing event, permanent impact"
        },
        {
          week: 18,
          event: "Chose to continue photography despite setback",
          significance: 8,
          why_preserved: "Defining choice about life direction"
        }
      ],
      
      phase_transition: {
        week: 14,
        type: "Health crisis",
        choice: "Put health first, slow down",
        lasting_impact: "Changed relationship with work/life balance"
      }
    },
    
    season_3: {
      title: "Finding Balance",
      length: 24,
      
      character_defining_moments: [
        {
          week: 12,
          event: "Sarah opened bookshop (her aspiration)",
          significance: 9,
          why_preserved: "Major NPC arc, affects future"
        }
      ]
    },
    
    season_4: {
      title: "Corporate Burnout",
      length: 12,
      
      character_defining_moments: [
        {
          week: 8,
          event: "Realized corporate life wasn't sustainable",
          significance: 9,
          why_preserved: "Seeds of Season 6 transition"
        }
      ]
    },
    
    season_5: {
      title: "The Slow Unraveling",
      length: 24,
      
      phase_transition: {
        week: 20,
        type: "Career devastation - severe burnout",
        choice: "Quit and figure it out",
        lasting_impact: "Led to Season 6 recovery arc"
      }
    }
  },
  
  query_examples: {
    "When did I first meet Sarah?": "Season 1, Week 3 at Café Luna",
    "What happened with the wedding shoot?": "Season 2, Week 14 - collapsed due to health neglect",
    "When did Sarah open her bookshop?": "Season 3, Week 12"
  },
  
  compression_algorithm: {
    pseudocode: `
      function compressSeasonHistory(season_data, time_since_season) {
        const preservation_score = [];
        
        for (const event of season_data.all_events) {
          let score = 0;
          
          // Score based on significance
          score += event.emotional_weight * 10;
          score += event.relationship_milestone ? 20 : 0;
          score += event.phase_transition ? 30 : 0;
          score += event.references_in_future_seasons * 5;
          score += event.novel_chapter_material ? 15 : 0;
          
          // Decay over time (but not too much)
          score *= (1 - (time_since_season * 0.05));
          
          preservation_score.push({event, score});
        }
        
        // Keep top 5-10 moments per season
        preservation_score.sort((a, b) => b.score - a.score);
        const preserved = preservation_score.slice(0, 10);
        
        return {
          preserved_moments: preserved,
          end_state_snapshot: season_data.final_state,
          total_compression: calculate_ratio(season_data.size, preserved.size)
        };
      }
    `
  }
};
```

---

## TIER 4: CANONICAL STATE (Current Snapshot)

### Complete Current Character Sheet

```javascript
const TIER_4_CANONICAL_STATE = {
  scope: "What is true RIGHT NOW",
  detail_level: "Complete current state",
  
  contains: {
    character_identity: {
      name: "Alex Chen",
      age: 33,                               // Started at 28, 5 years lived
      current_season: 8,
      seasons_completed: 7,
      total_weeks_lived: 172
    },
    
    current_life_direction: {
      active: "Seek Deep Relationships",     // Shifted from Financial Security in S6
      history: [
        { seasons: "1-3", direction: "Achieve Financial Security" },
        { seasons: "4-5", direction: "Same but wavering" },
        { seasons: "6-8", direction: "Seek Deep Relationships" }
      ]
    },
    
    current_aspirations: {
      major: "Open bookshop with Sarah",
      progress: 78,                          // 78% complete
      weeks_in: 28,
      weeks_total: 36
    },
    
    current_relationships: {
      sarah: {
        level: 5,
        trust: 0.98,
        role: "Best friend & business partner",
        total_interactions: 287,
        first_met: { season: 1, week: 3 },
        major_milestones_count: 18,
        current_status: "Opening bookshop together"
      },
      marcus: {
        level: 5,
        trust: 0.91,
        role: "Best friend",
        total_interactions: 156,
        first_met: { season: 1, week: 5 },
        saved_your_life: true,               // S2W14 collapse
        current_status: "Supportive, checks in weekly"
      },
      // ... all active NPCs
    },
    
    current_skills: {
      photography: 7.8,
      design: 5.2,
      business_management: 4.1,
      writing: 3.5,
      // ... all acquired skills
    },
    
    current_meters: {
      physical: 6,
      mental: 7,
      social: 8,
      emotional: 8
    },
    
    current_resources: {
      money: 3200,
      energy: 2,
      time_this_week: 12,                    // hours remaining
      social_capital: 8
    },
    
    current_emotional_state: {
      primary: "EXCITED",
      secondary: "ANXIOUS",
      intensity: 0.7,
      duration: "3 weeks"
    },
    
    personality_current: {
      openness: 4.5,                         // Evolved from 4.2 baseline
      conscientiousness: 3.8,                // Evolved from 4.5 (less rigid post-burnout)
      extraversion: 3.9,                     // Evolved from 3.1
      agreeableness: 4.6,                    // Evolved from 4.3
      neuroticism: 3.2                       // Evolved from 3.7 (therapy + growth)
    },
    
    permanent_achievements: [
      "Survived health crisis (S2)",
      "Made it through burnout (S6)",
      "Best friend bond with Sarah and Marcus",
      "Creative Legacy (partial - working on it)"
    ],
    
    active_cards_in_deck: 287,               // Includes all evolved/fused cards
    
    life_bookshelf: {
      seasons_complete: 7,
      novels_generated: 7,
      total_word_count: 98000,
      average_per_season: 14000
    }
  },
  
  used_for: [
    "AI generation context (personality, relationships)",
    "Consistency checking",
    "New event generation",
    "Success probability calculations"
  ]
};
```

---

## CANONICAL FACTS DATABASE

### Immutable Truths

```javascript
const CANONICAL_FACTS = {
  scope: "Facts that can NEVER change",
  prevents: "Contradictions",
  
  immutable_truths: {
    character_history: [
      "Sarah's fiancé David died 2 years before Season 1",
      "Player met Sarah at Café Luna, Season 1 Week 3",
      "Player collapsed during wedding shoot, Season 2 Week 14",
      "Marcus loaned player $2000 during crisis, Season 6 Week 22",
      "Player quit corporate job, Season 6 Week 6"
    ],
    
    npc_backstories: {
      sarah: {
        david_died: "2 years before game start",
        bookshop_dream: "Revealed Season 2 Week 18",
        opened_bookshop: "Season 3 Week 12",
        personality_type: "Reserved creative, OCEAN [4.3, 4.8, 2.3, 4.5, 3.6]"
      },
      marcus: {
        personality_type: "Supportive extrovert, OCEAN [4.1, 3.9, 4.7, 4.8, 2.8]",
        always_shows_up: true,
        helped_during_collapse: "Season 2 Week 14"
      }
    },
    
    world_rules: {
      cafe_luna_location: "Arts district, window seat preference",
      player_apartment: "2-bedroom, downtown",
      current_city: "Portland"
    },
    
    timeline_anchors: [
      { season: 1, week: 3, event: "Met Sarah", immutable: true },
      { season: 2, week: 14, event: "Collapsed", immutable: true },
      { season: 6, week: 6, event: "Quit job", immutable: true }
    ]
  },
  
  validation_use: {
    before_generating_content: "Check against canonical facts",
    example_check: {
      proposed_event: "Sarah mentions she's never been to Café Luna",
      canonical_fact: "Sarah and player met at Café Luna S1W3",
      result: "REJECT - contradiction"
    }
  }
};
```

---

## Memory Query System

### Intelligent Context Retrieval

```javascript
async function queryMultiSeasonContext(query, playerState) {
  const results = {
    tier_1_matches: [],
    tier_2_matches: [],
    tier_3_matches: [],
    canonical_facts: []
  };
  
  // STEP 1: Check canonical facts first
  results.canonical_facts = await searchCanonicalFacts(query);
  
  // STEP 2: Search Tier 1 (active context)
  if (needsRecentDetail(query)) {
    results.tier_1_matches = await searchTier1(query, playerState.tier1_context);
  }
  
  // STEP 3: Search Tier 2 (recent history)
  if (needsRecentHistoryContext(query)) {
    results.tier_2_matches = await searchTier2(query, playerState.tier2_context);
  }
  
  // STEP 4: Search Tier 3 (compressed history)
  if (needsLongTermContext(query)) {
    results.tier_3_matches = await searchTier3(query, playerState.tier3_context);
  }
  
  // STEP 5: Synthesize answer
  const answer = synthesizeAnswer(results, query);
  
  return answer;
}

// Example queries:
const EXAMPLE_QUERIES = {
  query_1: {
    question: "What did Sarah say about David recently?",
    searches: "Tier 1 (last 12 weeks)",
    answer: "Week 27: Wants poetry section in bookshop to honor him"
  },
  
  query_2: {
    question: "When did I first meet Sarah?",
    searches: "Canonical facts + Tier 3",
    answer: "Season 1, Week 3 at Café Luna (5 years ago)"
  },
  
  query_3: {
    question: "What's the history of my business partnership with Sarah?",
    searches: "All tiers",
    answer: "S2W18: She mentioned bookshop dream. S6W18: Suggested partnership. S7W20: Committed. S8 (current): Opening together."
  }
};
```

---

## Performance & Storage

### Memory Optimization

```javascript
const MEMORY_PERFORMANCE = {
  total_size_8_10_seasons: {
    tier_1_current: "2MB (12 weeks)",
    tier_2_recent: "5MB (48-72 weeks)",
    tier_3_compressed: "5-10MB (5-7 seasons compressed 50:1)",
    tier_4_state: "1MB (current snapshot)",
    canonical_facts: "2MB (all immutable truths)",
    total: "~15-20MB for complete 8-10 season character"
  },
  
  query_performance: {
    tier_1_query: "< 10ms (in-memory hash)",
    tier_2_query: "< 50ms (indexed search)",
    tier_3_query: "< 100ms (compressed search)",
    canonical_facts: "< 5ms (hash lookup)"
  },
  
  storage_strategy: {
    active_session: "All tiers in RAM",
    save_to_disk: "Compressed binary format",
    cloud_sync: "Incremental updates only",
    
    disk_size: "~5-10MB compressed per character"
  }
};
```

---

## Novel Generation Integration

### Using Multi-Season Context for Book Generation

```javascript
async function generateUnwrittenshelfNovel(season_number, playerState) {
  // Pull context from appropriate tiers
  const context = {
    season_detail: await getTier1Or2ForSeason(season_number),
    earlier_seasons_context: await getTier3Highlights(),
    canonical_facts: await getCanonicalFacts(),
    current_relationships: await getTier4Relationships()
  };
  
  // Generate novel with full continuity
  const novel = await aiGenerateNovel({
    season_data: context.season_detail,
    character_history: context.earlier_seasons_context,
    immutable_facts: context.canonical_facts,
    relationship_state: context.current_relationships,
    
    requirements: {
      no_contradictions: true,
      references_past_seasons: true,
      maintains_character_voice: true,
      reflects_personality_evolution: true
    }
  });
  
  return novel;
}
```

---

## Master Truths v1.2: Memory Resonance Factor System *(NEW)*

### Purpose: Emotional Recall Priority

**Core Principle:** Memories surface based on emotional resonance with current situation, not just recency. A traumatic memory from Season 2 can be more relevant than yesterday's routine conversation.

```javascript
const MEMORY_RESONANCE_SYSTEM = {
  purpose: "Determine which memories surface and when based on emotional resonance",
  threshold: "Base memory weight 5+ to be echo-eligible, resonance factors multiply likelihood",
  
  resonance_types: {
    
    type_1_same_emotion_different_context: {
      weight: 0.8,
      description: "Both memories involve same emotion (joy/sadness/anger) but different contexts",
      
      example: {
        past_memory: {
          season: 2,
          event: "Achievement joy - first client success",
          emotion: "EXCITED",
          context: "career"
        },
        current_situation: {
          season: 8,
          event: "Achievement joy - bookshop opening",
          emotion: "EXCITED",
          context: "business_partnership"
        },
        resonance_trigger: "Same pride/accomplishment feeling, different domain",
        narrative_effect: "You remember how it felt when you landed your first client... that same electricity runs through you now."
      },
      
      usage: "Shows emotional patterns across life - player consistently feels X in Y situations",
      quality_impact: "Creates coherent emotional through-line"
    },
    
    type_2_opposite_emotion_growth: {
      weight: 0.9,
      description: "Memory of past struggle, current situation is triumph - shows character growth",
      
      example: {
        past_memory: {
          season: 5,
          event: "Burnout crisis - couldn't handle work pressure",
          emotion: "OVERWHELMED",
          capacity: 1.5
        },
        current_situation: {
          season: 8,
          event: "Successfully managing bookshop launch pressure",
          emotion: "CONFIDENT",
          capacity: 7.5
        },
        resonance_trigger: "Similar stressor type (business pressure) but opposite outcome",
        narrative_effect: "Three years ago, this would have broken you. You would have spiraled. But now? You've got this."
      },
      
      usage: "Highlights character development - same trigger, different response",
      quality_impact: "Powerful contrast showing growth"
    },
    
    type_3_past_trauma_current_trigger: {
      weight: 0.95,  // HIGHEST resonance
      description: "Current situation mirrors past traumatic experience - authentic anxiety response",
      
      example: {
        past_memory: {
          season: 2,
          event: "Collapsed during wedding shoot due to health neglect",
          emotion: "TERRIFIED",
          trauma_marker: "HEALTH_CRISIS",
          lasting_impact: "Fear of pushing too hard"
        },
        current_situation: {
          season: 8,
          event: "Exhausted after 70-hour work week preparing bookshop",
          physical_meter: 3,
          mental_meter: 3
        },
        resonance_trigger: "Low meters + overwork = mirrors collapse conditions",
        narrative_effect: "Your hands shake slightly. You remember the hospital. The fluorescent lights. Marcus's terrified face. You can't do that again. You won't."
      },
      
      usage: "Creates authentic PTSD-like responses - trauma doesn't just vanish",
      quality_impact: "Deeply realistic emotional continuity"
    },
    
    type_4_past_joy_current_sadness: {
      weight: 0.85,
      description: "Memory of happy time, current situation shows loss/change - poignant contrast",
      
      example: {
        past_memory: {
          season: 3,
          event: "Coffee with Sarah every Tuesday at Café Luna",
          emotion: "CONTENT",
          ritual_significance: 9
        },
        current_situation: {
          season: 8,
          event: "Sarah too busy with bookshop prep - haven't met in 3 weeks",
          emotion: "LONELY",
          social_meter: 4
        },
        resonance_trigger: "Loss of ritual that used to bring comfort",
        narrative_effect: "You walk past Café Luna. Your usual table is occupied by strangers. When did Tuesdays stop being sacred?"
      },
      
      usage: "Shows bittersweet reality of life changes - growth has costs",
      quality_impact: "Literary-quality emotional complexity"
    },
    
    type_5_emotional_growth_callback: {
      weight: 0.7,
      description: "Memory of struggling with emotion, now handling it better - validates progress",
      
      example: {
        past_memory: {
          season: 4,
          event: "Couldn't ask for help due to pride/fear",
          emotion: "ISOLATED",
          pattern: "self_reliance_to_fault"
        },
        current_situation: {
          season: 8,
          event: "Asks Marcus for help naturally",
          emotion: "CONNECTED",
          capacity: 6.0
        },
        resonance_trigger: "Same vulnerability need, different response",
        narrative_effect: "Four years ago, you would have suffered in silence. But you've learned. You pick up the phone."
      },
      
      usage: "Rewards player for character development - you're not the same person",
      quality_impact: "Satisfying emotional payoff"
    }
  }
};
```

### Resonance Calculation

```javascript
function calculateMemoryResonance(memory, currentContext, playerState) {
  let resonanceScore = 0.0;
  const factors = [];
  
  // BASE: Memory emotional weight (5-10 scale)
  const baseWeight = memory.emotional_weight;  // 5+ eligible for recall
  
  // FACTOR 1: Same emotion, different context
  if (sameEmotionDifferentContext(memory, currentContext)) {
    resonanceScore += 0.8;
    factors.push("same_emotion_different_context");
  }
  
  // FACTOR 2: Opposite emotion, growth opportunity
  if (oppositeEmotionGrowth(memory, currentContext)) {
    resonanceScore += 0.9;
    factors.push("opposite_emotion_growth");
  }
  
  // FACTOR 3: Past trauma, current trigger (HIGHEST)
  if (pastTraumaTrigger(memory, currentContext)) {
    resonanceScore += 0.95;
    factors.push("past_trauma_trigger");
  }
  
  // FACTOR 4: Past joy, current sadness
  if (pastJoyCurrentSadness(memory, currentContext)) {
    resonanceScore += 0.85;
    factors.push("past_joy_current_sadness");
  }
  
  // FACTOR 5: Emotional growth callback
  if (emotionalGrowthCallback(memory, currentContext, playerState)) {
    resonanceScore += 0.7;
    factors.push("emotional_growth_callback");
  }
  
  // RECENCY: Decay factor (older memories slightly less likely)
  const seasonsSince = currentContext.season - memory.season;
  const recencyDecay = Math.max(0.5, 1.0 - (seasonsSince * 0.05));  // 5% per season
  
  // FINAL SCORE
  const finalScore = baseWeight * resonanceScore * recencyDecay;
  
  return {
    memory_id: memory.id,
    base_weight: baseWeight,
    resonance_score: resonanceScore,
    recency_decay: recencyDecay,
    final_score: finalScore,
    resonance_factors: factors,
    should_surface: finalScore >= 6.0  // Threshold for auto-surfacing
  };
}
```

### Memory Recall Priority Example

```javascript
const RECALL_EXAMPLE = {
  current_context: {
    season: 8,
    week: 28,
    situation: "Exhausted after long work week, physical meter 3",
    emotional_state: "EXHAUSTED",
    active_stressors: ["work_overload", "partner_tension"]
  },
  
  memory_candidates: [
    {
      memory_id: "S8W25_coffee_sarah",
      season: 8,
      weeks_ago: 3,
      emotional_weight: 5,
      emotion: "CONTENT",
      content: "Coffee with Sarah, nice conversation",
      
      resonance_calculation: {
        base_weight: 5,
        resonance_types: [],  // No resonance with current exhaustion
        resonance_score: 0.0,
        recency_decay: 1.0,
        final_score: 5.0,
        should_surface: false  // Below 6.0 threshold
      }
    },
    
    {
      memory_id: "S2W14_collapse",
      season: 2,
      weeks_ago: 144,  // 6 seasons * 24 weeks
      emotional_weight: 10,  // MAXIMUM - traumatic event
      emotion: "TERRIFIED",
      trauma_marker: "HEALTH_CRISIS",
      content: "Collapsed during wedding shoot, hospitalized",
      
      resonance_calculation: {
        base_weight: 10,
        resonance_types: ["past_trauma_trigger"],  // Current exhaustion mirrors collapse
        resonance_score: 0.95,  // Type 3 - past trauma
        recency_decay: 0.7,  // 6 seasons old = 70% weight
        final_score: 10 * 0.95 * 0.7 = 6.65,
        should_surface: true  // ✓ Above 6.0 threshold
      }
    },
    
    {
      memory_id: "S4W8_couldn't_ask_help",
      season: 4,
      weeks_ago: 96,  // 4 seasons ago
      emotional_weight: 7,
      emotion: "ISOLATED",
      pattern: "self_reliance_to_fault",
      content: "Needed help, couldn't ask, suffered alone",
      
      resonance_calculation: {
        base_weight: 7,
        resonance_types: ["emotional_growth_callback"],  // IF player now asks for help
        resonance_score: 0.7,  // Type 5 - growth callback
        recency_decay: 0.8,  // 4 seasons old = 80% weight
        final_score: 7 * 0.7 * 0.8 = 3.92,
        should_surface: false  // Below threshold (unless player asks for help)
      }
    }
  ],
  
  surfaced_memory: {
    memory_id: "S2W14_collapse",
    final_score: 6.65,
    narrative_integration: `
      Your hands ache. Your head pounds. You've been pushing too hard this week.
      
      A flash: fluorescent hospital lights. Marcus's face, pale with fear. "You 
      collapsed," he said. "You just... fell."
      
      That was six years ago. But your body remembers. Your hands shake slightly 
      as you close the laptop. Not again. You won't do that to yourself again.
      
      You text Marcus: "Can you come over? I need to talk."
    `,
    
    player_choice_influenced: true,
    // Memory surfaces → player more likely to ask for help (growth)
  }
};
```

---

## Master Truths v1.2: Tension Hook Persistence *(NEW)*

### Cross-Season Hook Tracking

**Core Principle:** Tension hooks planted in Season 2 can pay off in Season 5. Information debt is tracked across entire character lifecycle.

```javascript
const TENSION_HOOK_DATABASE = {
  purpose: "Track all planted hooks, ensure payoffs, maintain information debt",
  
  hook_structure: {
    hook_id: "unique_identifier",
    season_planted: 2,
    week_planted: 14,
    hook_type: "mystery_hook | partial_reveal | contradiction | stakes_escalation",
    
    content: {
      what_was_said: "Sarah mentions 'David' then changes subject, hands shake",
      information_gaps: [
        "Who is David?",
        "Why does Sarah get emotional?",
        "What happened to David?"
      ],
      tension_score: 0.85,
      player_curiosity_generated: true
    },
    
    payoff_timeline: {
      expected: "2-4 weeks",
      actual: null,  // Filled when paid off
      overdue: false,
      payoff_season: null,
      payoff_week: null
    },
    
    status: "planted | overdue | resolved | abandoned",
    
    narrative_continuity: {
      references_count: 3,  // How many times referenced before payoff
      builds_tension: true,
      player_engagement_high: true
    }
  }
};
```

### Hook Lifecycle Example

```javascript
const HOOK_LIFECYCLE_SARAH_DAVID = {
  // PLANTING (Season 2, Week 14)
  planting: {
    hook_id: "sarah_david_mystery",
    season: 2,
    week: 14,
    card: "Coffee with Sarah",
    
    dialogue: `
      "So I was thinking about the bookshop idea..."
      
      She pauses, traces the rim of her coffee cup.
      
      "David always said I should do it. He believed in me more than—"
      
      Her voice catches. She shakes her head quickly.
      
      "Sorry. Anyway. What do you think about the location?"
    `,
    
    planted_information_debt: [
      "Who is David?",
      "Past or present tense? (said/says)",
      "Why the emotional reaction?",
      "How does David relate to bookshop dream?"
    ],
    
    tension_score: 0.75,
    expected_payoff: "2-4 weeks"
  },
  
  // BUILDING (Season 2, Weeks 15-17)
  building: [
    {
      week: 15,
      card: "Gallery opening with Sarah",
      dialogue: "Sarah gets quiet when couple kisses nearby. You notice.",
      adds_information: "Possible romantic connection to David?",
      tension_score: 0.80
    },
    {
      week: 17,
      card: "Help Sarah move",
      dialogue: "You see framed photo of Sarah with man, face-down on shelf. She doesn't explain.",
      adds_information: "Visual confirmation - significant person",
      tension_score: 0.85
    }
  ],
  
  // PAYOFF (Season 2, Week 18)
  payoff: {
    week: 18,
    card: "Late night conversation with Sarah (Level 3 milestone)",
    
    dialogue: `
      "David was my fiancé."
      
      She says it quietly, looking at her hands.
      
      "He died. Two years before I met you. Car accident. Stupid, random, 
      senseless. One day he was there, planning our future. The next..."
      
      She's silent for a long time.
      
      "The bookshop was our dream. We were going to do it together. And now... 
      I don't know. Maybe I'm holding onto something that died with him. 
      Or maybe it's my way of keeping him alive. I don't know."
    `,
    
    information_debt_resolved: [
      "✓ Who is David? → Fiancé",
      "✓ Past/present? → Died 2 years before Season 1",
      "✓ Emotional reaction? → Grief, loss",
      "✓ Bookshop connection? → Their shared dream"
    ],
    
    tension_resolution_score: 0.90,
    emotional_impact: 9.5,
    relationship_milestone: "Level 2 → Level 3",
    trust_gain: +0.35,
    
    creates_new_context: "All future Sarah interactions now carry weight of David's memory"
  },
  
  // LONG-TERM IMPACT (Seasons 3-8)
  long_term_resonance: {
    season_3_week_12: {
      event: "Sarah opens bookshop",
      david_callback: "She dedicates poetry section to David's memory",
      resonance_weight: 0.95  // Past joy, current bittersweet
    },
    
    season_8_week_28: {
      event: "Player and Sarah open bookshop together",
      david_callback: `
        "You know what's beautiful?" Sarah says, looking at the finished shop. 
        "This started as David's and my dream. And now it's yours and mine. 
        I think he'd like that. That it didn't die with him."
      `,
      resonance_weight: 0.9,  // Emotional growth callback
      narrative_payoff: "Full circle - dream fulfilled differently than planned"
    }
  },
  
  total_lifecycle: {
    seasons_tracked: 7,  // S2 → S8
    total_references: 8,
    payoff_quality: 0.92,
    narrative_coherence: 0.95,
    emotional_resonance: 0.93,
    overall_hook_quality: 0.93  // Excellent multi-season arc
  }
};
```

### Hook Tracking Database

```javascript
const ACTIVE_HOOKS_DATABASE = {
  character_id: "alex_chen_001",
  
  all_hooks: [
    {
      hook_id: "sarah_david_mystery",
      status: "resolved",
      season_planted: 2,
      season_resolved: 2,
      weeks_active: 4,
      quality_score: 0.93
    },
    {
      hook_id: "marcus_job_secret",
      status: "planted",
      season_planted: 7,
      week_planted: 15,
      expected_payoff: "2-4 weeks",
      current_week: 28,
      weeks_active: 13,
      overdue: true,  // ⚠️ Past expected payoff
      player_curiosity: 0.65,
      action_required: "Must pay off in Season 8 or abandon"
    },
    {
      hook_id: "bookshop_financial_tension",
      status: "planted",
      season_planted: 8,
      week_planted: 20,
      expected_payoff: "5-8 weeks",
      current_week: 28,
      weeks_active: 8,
      overdue: false,
      player_curiosity: 0.80
    }
  ],
  
  validation: {
    total_planted: 3,
    total_resolved: 1,
    total_overdue: 1,
    average_quality: 0.93,
    
    warnings: [
      "⚠️ Hook 'marcus_job_secret' overdue - pay off or abandon"
    ]
  }
};
```

---

## Master Truths v1.2: Dramatic Irony Knowledge Tracking *(NEW)*

### Dual Knowledge Base System

**Core Principle:** Track what player knows separately from what character knows. Knowledge gaps = dramatic irony opportunities.

```javascript
const KNOWLEDGE_TRACKING_SYSTEM = {
  purpose: "Enable 'yelling at screen' tension through information asymmetry",
  
  dual_knowledge_bases: {
    
    player_knowledge: {
      scope: "Everything player has witnessed, heard, discovered",
      includes: [
        "Direct interactions",
        "Overheard conversations",
        "Visual observations",
        "NPC secrets revealed to player",
        "Witnessed events character wasn't present for"
      ],
      
      example_entries: [
        {
          knowledge_id: "npc_marcus_job_loss",
          learned_season: 7,
          learned_week: 22,
          source: "Overheard Marcus's phone call",
          content: "Marcus lost job 2 weeks ago, hasn't told anyone",
          emotional_weight: 8,
          affects_npcs: ["marcus"],
          character_knows: false  // ← KEY: Character doesn't know this
        },
        {
          knowledge_id: "sarah_considering_moving",
          learned_season: 8,
          learned_week: 15,
          source: "Saw apartment listings on Sarah's tablet",
          content: "Sarah researching Seattle apartments",
          emotional_weight: 9,
          affects_npcs: ["sarah"],
          character_knows: false  // ← Dramatic irony opportunity
        }
      ]
    },
    
    character_knowledge: {
      scope: "What character has directly experienced or been told",
      includes: [
        "Direct conversations",
        "Explicit reveals",
        "Personal experiences",
        "Information character was present for"
      ],
      
      example_entries: [
        {
          knowledge_id: "sarah_stressed_about_bookshop",
          learned_season: 8,
          learned_week: 20,
          source: "Sarah told character directly",
          content: "Financial pressure from bookshop prep",
          emotional_weight: 7,
          player_knows: true  // ← Both know this
        }
      ]
    }
  }
};
```

### Knowledge Gap Detection

```javascript
function detectKnowledgeGaps(playerKnowledge, characterKnowledge, currentContext) {
  const gaps = [];
  
  // Check each piece of player knowledge
  playerKnowledge.forEach(knowledge => {
    // Does character also know this?
    const characterKnows = characterKnowledge.some(ck => ck.knowledge_id === knowledge.knowledge_id);
    
    if (!characterKnows) {
      // KNOWLEDGE GAP DETECTED
      const gap = {
        knowledge_id: knowledge.knowledge_id,
        content: knowledge.content,
        emotional_weight: knowledge.emotional_weight,
        affects_npcs: knowledge.affects_npcs,
        
        // Calculate dramatic irony score
        irony_score: calculateIronyScore(knowledge, currentContext),
        
        // Determine if usable
        usable_now: isUsableForIrony(knowledge, currentContext)
      };
      
      gaps.push(gap);
    }
  });
  
  return gaps;
}

function calculateIronyScore(knowledge, context) {
  let score = 0.0;
  
  // Factor 1: Knowledge clarity (0.0-0.3)
  // How clear is the information?
  const clarity = knowledge.emotional_weight / 10;  // 0.0-1.0
  score += clarity * 0.25;
  
  // Factor 2: Tension created (0.0-0.3)
  // How much tension does the gap create?
  const tensionLevel = calculateTensionFromGap(knowledge, context);
  score += tensionLevel * 0.30;
  
  // Factor 3: Emotional weight (0.0-0.2)
  // How much does this matter?
  score += (knowledge.emotional_weight / 10) * 0.20;
  
  // Factor 4: Player investment (0.0-0.15)
  // Does player care about affected NPCs?
  const investment = calculatePlayerInvestment(knowledge.affects_npcs, context);
  score += investment * 0.15;
  
  // Factor 5: Timing quality (0.0-0.1)
  // Is this the right moment to use it?
  const timing = calculateTimingQuality(knowledge, context);
  score += timing * 0.10;
  
  return Math.min(1.0, score);
}
```

### Dramatic Irony Example

```javascript
const IRONY_EXAMPLE_MARCUS_JOB = {
  // KNOWLEDGE GAP
  player_knows: {
    knowledge_id: "marcus_job_loss",
    content: "Marcus lost job 2 weeks ago, hiding it from everyone",
    source: "Overheard phone call in Week 22",
    emotional_weight: 8,
    marcus_capacity: 3.5  // Marcus is struggling
  },
  
  character_knows: {
    // Character does NOT know Marcus lost job
    // Character believes: Marcus is employed, stable, available
  },
  
  // CURRENT SITUATION (Week 28)
  scenario: {
    card: "Ask Marcus for financial advice about bookshop",
    player_needs: "Advice on managing startup costs",
    marcus_visible_state: "Seems fine, enthusiastic",
    marcus_actual_state: "Capacity 3.5, secretly broke, can't help"
  },
  
  // DRAMATIC IRONY CALCULATION
  irony_score_calculation: {
    knowledge_clarity: 0.80 * 0.25 = 0.20,  // Player clearly knows
    tension_created: 0.85 * 0.30 = 0.255,   // High tension
    emotional_weight: 0.80 * 0.20 = 0.16,   // Significant matter
    player_investment: 0.90 * 0.15 = 0.135, // Close friend (Level 5)
    timing_quality: 0.75 * 0.10 = 0.075,    // Good moment
    
    total_irony_score: 0.825,  // ✓ Above 0.6 threshold
    use_dramatic_irony: true
  },
  
  // THREE RESPONSE OPTIONS
  response_options: {
    
    option_1_tone_deaf: {
      type: "TONE_DEAF",
      dialogue: "Marcus, I need your advice on managing money for the bookshop. You're always so good with finances!",
      
      marcus_internal_reaction: "God. If only they knew. I can't even manage my own finances right now. But I can't tell them. I can't burden them when they're already stressed.",
      
      marcus_response: `
        [Forced smile] "Of course! Let me think..."
        
        [He gives generic advice, but you notice his hands fidget]
        
        "Just... be careful with debt. Don't overextend."
        
        [There's something off about his tone, but you can't place it]
      `,
      
      player_overlay_shown: true,
      overlay_text: "(You know Marcus lost his job... but your character doesn't. They're asking for financial advice from someone secretly broke.)",
      
      relationship_impact: -0.5,  // Minor strain - Marcus feels guilt
      marcus_capacity_drain: -0.5,  // Pretending is exhausting
      tension_created: 0.85,
      player_experience: "Uncomfortable dramatic irony - want to help but can't break character knowledge"
    },
    
    option_2_misguided: {
      type: "WELL_INTENTIONED_BUT_MISGUIDED",
      dialogue: "Actually, forget the financial stuff. You seem stressed lately. Everything okay?",
      
      marcus_internal_reaction: "They noticed. Crap. Do I tell them? I don't want to burden them. They've got so much going on.",
      
      marcus_response: `
        [Pause] "I'm... yeah. Just busy. Work has been intense."
        
        [He's lying. You can tell. But he's not ready to share.]
        
        "I'm okay. Really. Let's talk about your bookshop."
      `,
      
      player_overlay_shown: true,
      overlay_text: "(You sense something's wrong, but you don't know about the job loss.)",
      
      relationship_impact: -0.2,  // Small strain - push but respect boundary
      marcus_capacity: 3.5,  // Unchanged - you tried but didn't force
      tension_maintained: 0.75,
      opens_future_reveal: true  // Marcus might tell you next week
    },
    
    option_3_growth: {
      type: "GROWTH_CHOICE",
      dialogue: "Marcus. I know something's wrong. You don't have to tell me if you're not ready. But I'm here when you are.",
      
      marcus_internal_reaction: "They know. Or at least, they know something is off. And they're... not pushing. They're just... there. Maybe I can tell them.",
      
      marcus_response: `
        [Long pause. His shoulders sag.]
        
        "I lost my job. Two weeks ago. Haven't told anyone. Not even my family."
        
        [His voice cracks slightly]
        
        "I've been pretending everything is fine. Going to 'work' every day, 
        sitting in cafes, applying to jobs. Coming home exhausted from the 
        performance. And I just... I couldn't admit it. Especially not to you, 
        when you're about to start this amazing thing."
        
        [He looks at you, vulnerable]
        
        "I'm sorry I didn't tell you sooner."
      `,
      
      player_overlay_shown: false,  // Character breaks through to truth
      
      relationship_impact: +0.8,  // Major trust gain - safe to be vulnerable
      marcus_capacity: 3.5 → 5.0,  // Immediate relief from sharing
      tension_resolved: true,
      dramatic_irony_payoff: 0.95,  // Excellent payoff
      player_experience: "Satisfying - helped Marcus feel safe enough to share"
    }
  },
  
  // VALIDATION
  quality_scores: {
    irony_score: 0.825,  // ✓ Above 0.6 threshold
    tension_created: 0.85,
    emotional_authenticity: 0.90,  // Marcus's struggle feels real
    capacity_constrained: true,  // Marcus at 3.5 can't provide full support
    player_agency: true,  // Three meaningful choices
    
    overall_dramatic_irony_quality: 0.88  // Excellent use of knowledge gap
  }
};
```

---

## Master Truths v1.2: Capacity History Tracking *(NEW)*

### Why Track Capacity Over Time

**Core Principle:** Capacity patterns reveal character traits. Someone who consistently drops to 2.0 during Q4 work crunch needs different support than someone who maintains 7.0.

```javascript
const CAPACITY_HISTORY_SYSTEM = {
  purpose: "Track capacity patterns to predict future needs and validate authenticity",
  
  tracking_structure: {
    character_id: "alex_chen_001",
    
    capacity_snapshots: [
      {
        season: 2,
        week: 14,
        capacity: 1.5,
        context: "Health crisis - collapsed during wedding shoot",
        duration: "4 weeks",
        recovery_to: 6.0,
        recovery_time: "6 weeks",
        lasting_impact: "Developed fear of overwork",
        pattern_marker: "BURNOUT_CYCLE_START"
      },
      {
        season: 5,
        week: 20,
        capacity: 1.0,
        context: "Severe corporate burnout - quit job",
        duration: "8 weeks",
        recovery_to: 5.5,
        recovery_time: "12 weeks",
        lasting_impact: "Changed relationship with work/life balance",
        pattern_marker: "BURNOUT_CYCLE_REPEAT"
      },
      {
        season: 8,
        week: 28,
        capacity: 4.5,
        context: "Bookshop prep stress - catching early warning signs",
        duration: "2 weeks so far",
        recovery_plan: "Asking for help, setting boundaries",
        pattern_marker: "BURNOUT_PREVENTION_GROWTH"
      }
    ],
    
    identified_patterns: {
      burnout_cycle: {
        frequency: "Every 3-4 seasons",
        trigger: "High work pressure + perfectionism",
        typical_capacity_drop: "7.0 → 1.5",
        recovery_time: "8-12 weeks",
        
        growth_trajectory: {
          season_2: "Didn't see it coming, crashed hard",
          season_5: "Saw warning signs too late, crashed anyway",
          season_8: "Catching early, asking for help, preventing crash"
        }
      },
      
      seasonal_baseline: {
        typical_range: "5.5-7.5",
        high_periods: "Spring/Summer (6.5-7.5 avg)",
        low_periods: "Fall/Winter (5.0-6.0 avg)",
        reason: "Seasonal affective patterns"
      }
    }
  }
};
```

### Predictive Capacity Modeling

```javascript
function predictFutureCapacity(capacityHistory, currentContext) {
  const patterns = identifyPatterns(capacityHistory);
  
  // Check for known pattern triggers
  const predictions = {
    next_2_weeks: {
      expected_capacity: 4.0,  // Based on current trajectory
      confidence: 0.75,
      risk_factors: [
        "Bookshop opening stress",
        "Multiple deadlines converging",
        "Q4 seasonal dip pattern"
      ],
      
      warning: "⚠️ Pattern match: Similar to S2W12 (pre-collapse). Recommend intervention.",
      
      interventions: [
        "Ask for help before capacity drops further",
        "Delegate bookshop tasks to Sarah",
        "Schedule rest days",
        "Set clear boundaries"
      ]
    },
    
    intervention_impact: {
      if_no_action: {
        predicted_capacity_week_30: 2.5,
        risk_level: "HIGH",
        likely_outcome: "Burnout repeat"
      },
      if_intervention: {
        predicted_capacity_week_30: 5.0,
        risk_level: "MODERATE",
        likely_outcome: "Sustainable pace"
      }
    }
  };
  
  return predictions;
}
```

### NPC Capacity History

```javascript
const NPC_CAPACITY_TRACKING = {
  npc_id: "sarah",
  
  capacity_history: [
    {
      season: 3,
      weeks: "1-12",
      avg_capacity: 7.5,
      context: "Bookshop opening (her own) - thriving",
      high_point: 9.0
    },
    {
      season: 7,
      weeks: "15-24",
      avg_capacity: 5.5,
      context: "Financial pressure + relationship tension",
      low_point: 4.0
    },
    {
      season: 8,
      weeks: "20-28",
      avg_capacity: 6.0,
      context: "Partnership bookshop prep - moderate stress",
      fluctuating: true
    }
  ],
  
  baseline_capacity: 6.5,  // Sarah's typical stable state
  
  support_availability_prediction: {
    current_week: 28,
    sarah_capacity: 6.0,
    
    can_support_levels: "Up to 4.0 (capacity 6.0 - 2 rule)",
    
    availability: {
      low_stress_chat: "YES - available",
      moderate_emotional_support: "YES - available",
      crisis_intervention: "NO - insufficient capacity",
      practical_help: "YES - available"
    }
  }
};
```

---

## Master Truths v1.2: Quality Validation Across Tiers *(NEW)*

### Multi-Tier Quality Scoring

**Core Principle:** Even compressed memories (Tier 3) must maintain emotional authenticity and narrative coherence.

```javascript
const MULTI_TIER_QUALITY_VALIDATION = {
  purpose: "Ensure v1.2 standards maintained across all memory tiers",
  
  tier_1_active_validation: {
    scope: "Last 12 weeks - full detail",
    
    quality_checks: {
      emotional_authenticity: {
        threshold: 0.85,  // Higher for active tier
        checks: [
          "Every NPC response constrained by current capacity",
          "No characters providing support beyond capacity + 2",
          "Authentic limitations acknowledged",
          "Growth choices available"
        ]
      },
      
      tension_maintenance: {
        threshold: 0.75,
        checks: [
          "Active hooks tracked and building",
          "Mystery elements maintained",
          "Stakes clear and escalating",
          "Information debt managed"
        ]
      },
      
      dramatic_irony: {
        threshold: 0.60,
        checks: [
          "Knowledge gaps scored when present",
          "Irony opportunities utilized (score ≥ 0.6)",
          "Player overlays shown when appropriate",
          "Tone-deaf/misguided/growth options provided"
        ]
      },
      
      numerical_grounding: {
        threshold: 1.0,  // REQUIRED
        checks: [
          "All trust impacts have formulas",
          "All capacity values have calculations",
          "Qualitative anchors referenced",
          "Validation confirms narrative matches numbers"
        ]
      }
    },
    
    example_validation: {
      interaction_id: "S8W28_sarah_stressed_convo",
      
      validation_checks: {
        sarah_capacity: 4.5,
        sarah_can_support: "Up to 2.5 need level",
        player_need_level: 6.0,
        
        authenticity_check: "Sarah response shows limitations? YES ✓",
        dialogue: "I want to help, but I'm barely keeping it together myself...",
        authenticity_score: 0.85,
        
        tension_check: "Active hook referenced? YES ✓",
        hook_referenced: "bookshop_financial_tension",
        tension_score: 0.80,
        
        numerical_grounding: {
          relationship_impact: -0.3,
          formula: "base -0.4 × personality 0.7 × urgency 1.0 = -0.28 → -0.3",
          tier: "MINOR HARM",
          validated: true
        },
        
        overall_quality: 0.82  // ✓ Above 0.7 threshold
      }
    }
  },
  
  tier_2_recent_validation: {
    scope: "Seasons 6-7 - high detail",
    
    quality_checks: {
      emotional_authenticity: 0.78,  // Slightly lower, still high
      tension_maintenance: 0.70,
      dramatic_irony: 0.55,  // When applicable
      defining_moments_preserved: true
    },
    
    compression_rules: {
      keep: "Moments that scored ≥ 0.75 on authenticity",
      keep: "All tension hook plantings and payoffs",
      keep: "All dramatic irony moments (score ≥ 0.6)",
      keep: "All capacity crisis moments",
      discard: "Routine interactions < 0.5 quality"
    }
  },
  
  tier_3_compressed_validation: {
    scope: "Seasons 1-5 - heavily compressed (50:1)",
    
    quality_checks: {
      emotional_authenticity: 0.72,  // Still above 0.7 threshold!
      narrative_coherence: 0.85,
      no_contradictions: true,
      character_voice_consistent: true
    },
    
    compression_preservation: {
      principle: "Only preserve moments that passed v1.2 thresholds",
      
      preserved_moments_criteria: {
        emotional_weight: "≥ 8.0",
        authenticity_score: "≥ 0.75",
        tension_score: "≥ 0.70",
        relationship_milestone: true,
        trauma_marker: true,
        phase_transition: true
      },
      
      example_preserved: {
        moment_id: "S2W14_collapse",
        why_preserved: [
          "Emotional weight: 10.0 (maximum)",
          "Authenticity: 0.90 (high)",
          "Trauma marker: HEALTH_CRISIS",
          "Phase transition: Changed work relationship",
          "Referenced in: S5, S8 (long-term resonance)"
        ],
        compression_result: "Full detail preserved despite 50:1 compression"
      },
      
      example_discarded: {
        moment_id: "S3W8_routine_coffee",
        why_discarded: [
          "Emotional weight: 4.0 (below threshold)",
          "Authenticity: 0.60 (routine)",
          "No tension hooks",
          "No long-term significance",
          "Never referenced again"
        ],
        compression_result: "Discarded - routine interaction"
      }
    }
  }
};
```

### Season-End Quality Report

```javascript
const SEASON_QUALITY_REPORT = {
  season: 8,
  weeks: 36,
  character: "alex_chen_001",
  
  overall_scores: {
    emotional_authenticity: 0.82,
    tension_building: 0.78,
    dramatic_irony: 0.73,  // When applicable
    hook_effectiveness: 0.85,
    numerical_grounding: 0.95,
    
    overall_quality: 0.81  // ✓ PASS (≥ 0.7 required)
  },
  
  breakdown_by_act: {
    act_1_setup: {
      weeks: "1-12",
      quality: 0.75,
      strengths: ["Strong hook planting", "Clear capacity tracking"],
      weaknesses: ["Some dramatic irony opportunities missed"]
    },
    act_2_complications: {
      weeks: "13-27",
      quality: 0.83,
      strengths: ["Excellent tension escalation", "Perfect capacity authenticity"],
      weaknesses: ["None significant"]
    },
    act_3_resolution: {
      weeks: "28-36",
      quality: 0.85,
      strengths: ["Satisfying hook payoffs", "Strong emotional authenticity"],
      weaknesses: ["None"]
    }
  },
  
  notable_moments: [
    {
      week: 18,
      interaction: "Sarah reveals bookshop partnership stress",
      quality_score: 0.92,
      why_notable: "Perfect capacity-constrained authenticity + dramatic irony use"
    },
    {
      week: 28,
      interaction: "Marcus job loss reveal",
      quality_score: 0.95,
      why_notable: "Excellent dramatic irony payoff after 6-week buildup"
    }
  ],
  
  areas_for_improvement: [
    "More consistent dramatic irony utilization (73% vs 80% target)",
    "Some minor numerical grounding missing in weeks 8-10"
  ],
  
  recommendation: "ARCHIVE - Quality exceeds threshold, suitable for permanent storage"
};
```

---

## Master Truths v1.2: Numerical Grounding in Canonical Facts *(NEW)*

### Why Store Formulas, Not Just Numbers

**Core Principle:** Every numerical assignment must be traceable, calculable, and validated against qualitative anchors.

```javascript
const NUMERICAL_GROUNDING_DATABASE = {
  purpose: "Store every number with derivation, anchor, and validation",
  
  canonical_fact_structure: {
    fact_id: "unique_identifier",
    type: "trust_impact | capacity_value | meter_change | quality_score",
    
    numerical_value: 0.0,  // The actual number
    
    derivation: {
      formula: "string representation of calculation",
      factors: {
        base: 0.0,
        personality_modifier: 0.0,
        urgency_multiplier: 0.0,
        trust_modifier: 0.0,
        capacity_factor: 0.0
      },
      calculation_steps: ["step 1", "step 2", "step 3"]
    },
    
    qualitative_anchor: {
      tier: "MINOR HARM | MODERATE HARM | MAJOR HARM | etc.",
      narrative_markers: ["string 1", "string 2"],
      expected_dialogue: "What NPC should say/feel",
      recovery_time: "estimated recovery duration"
    },
    
    validation: {
      does_narrative_match_number: boolean,
      does_dialogue_match_tier: boolean,
      reasoning: "Why this is correct"
    },
    
    context: {
      season: 0,
      week: 0,
      interaction: "description",
      npcs_involved: ["npc_id"],
      circumstances: "context description"
    },
    
    immutable: boolean  // Cannot be changed once set
  }
};
```

### Example: Trust Impact Storage

```javascript
const TRUST_IMPACT_EXAMPLE = {
  fact_id: "S6W22_marcus_loan_trust",
  type: "trust_impact",
  
  numerical_value: +0.85,
  
  derivation: {
    formula: "base × personality × urgency × relationship = +0.85",
    factors: {
      base_positive: +0.6,  // Significant help
      marcus_agreeableness: 1.2,  // High (0.8) amplifies positive
      urgency_multiplier: 1.5,  // Important (not crisis, but significant)
      existing_trust: 1.0  // Moderate trust (0.7), no cushioning needed
    },
    calculation_steps: [
      "Base: +0.6 (loaning money during financial crisis = significant)",
      "Personality: 0.8 agreeableness → 1.2x amplifier for positive acts",
      "Urgency: 2x (important financial need, not immediate crisis)",
      "Trust: 0.7 existing → 1.0x (no modifier)",
      "Result: +0.6 × 1.2 × 1.5 × 1.0 = +1.08 → capped at +1.0",
      "BUT player capacity 3.5 limited ability to fully appreciate",
      "Final: +0.85"
    ]
  },
  
  qualitative_anchor: {
    tier: "SIGNIFICANT POSITIVE (+0.5 to +0.8)",
    narrative_markers: [
      "You really came through for me",
      "Thank you so much",
      "Visible gratitude"
    ],
    expected_dialogue: "Marcus, you didn't have to do this. I... thank you. Really. This means everything.",
    recovery_time: "N/A - positive gain"
  },
  
  validation: {
    does_narrative_match_number: true,
    does_dialogue_match_tier: true,
    reasoning: "+0.85 is SIGNIFICANT POSITIVE tier. Dialogue shows deep gratitude without being melodramatic. Player capacity 3.5 prevents full +1.0 appreciation but still major positive."
  },
  
  context: {
    season: 6,
    week: 22,
    interaction: "Marcus loans $2000 during financial crisis",
    npcs_involved: ["marcus"],
    circumstances: "Player capacity 3.5 (low), desperate financial situation, Marcus risking his own stability to help",
    
    player_state: {
      capacity: 3.5,
      physical_meter: 5,
      mental_meter: 4,
      emotional_meter: 3,
      money: 400,
      debt: 5000
    },
    
    marcus_state: {
      capacity: 6.5,
      willing_to_help: true,
      own_financial_risk: "moderate"
    }
  },
  
  immutable: true,  // This is a defining moment - cannot be changed
  
  long_term_impact: {
    seasons_3_8: "Referenced multiple times as proof of Marcus's reliability",
    resonance_weight: 0.90  // Significant positive memory
  }
};
```

### Example: Capacity Value Storage

```javascript
const CAPACITY_VALUE_EXAMPLE = {
  fact_id: "S8W28_player_capacity",
  type: "capacity_value",
  
  numerical_value: 4.85,
  
  derivation: {
    formula: "(emo × 0.5) + (mental × 0.3) + (phys × 0.15) + (social × 0.05) - stacking_penalty",
    factors: {
      emotional_meter: 6,
      mental_meter: 5,
      physical_meter: 7,
      social_meter: 6,
      
      weighted_sum: "(6 × 0.5) + (5 × 0.3) + (7 × 0.15) + (6 × 0.05) = 5.85",
      
      active_stressors: {
        bookshop_deadline: true,
        financial_pressure: true,
        count: 2
      },
      stacking_penalty: 1.0  // 2 stressors = -1.0
    },
    calculation_steps: [
      "Emotional (primary): 6 × 0.50 = 3.0",
      "Mental (secondary): 5 × 0.30 = 1.5",
      "Physical (tertiary): 7 × 0.15 = 1.05",
      "Social (minor): 6 × 0.05 = 0.3",
      "Base sum: 5.85",
      "Stressors: 2 active = -1.0 penalty",
      "Final: 5.85 - 1.0 = 4.85"
    ]
  },
  
  qualitative_anchor: {
    tier: "LOW/MODERATE BORDER (4-5 range)",
    narrative_markers: [
      "I'm tired",
      "I want to help but I can't",
      "Present but limited"
    ],
    behavioral_signs: [
      "Short responses",
      "Apologizes for not being enough",
      "Sets clear boundaries"
    ],
    support_capacity: "Up to 2.85 need level (capacity - 2 rule)"
  },
  
  validation: {
    does_narrative_match_number: true,
    does_behavior_match_tier: true,
    reasoning: "4.85 is LOW/MODERATE border. Character shows fatigue, can provide basic support but not deep processing. Matches tier expectations."
  },
  
  context: {
    season: 8,
    week: 28,
    situation: "Bookshop opening in 2 weeks, financial pressure, exhausted",
    recent_events: [
      "70-hour work week",
      "Argument with Sarah about money",
      "Deadline stress"
    ]
  },
  
  immutable: false,  // Capacity changes - snapshot for this moment
  
  trajectory: {
    week_26: 6.0,  // Two weeks ago
    week_27: 5.5,  // Last week
    week_28: 4.85,  // Current - declining
    predicted_week_29: 4.0,  // If no intervention
    warning: "⚠️ Capacity declining - intervention recommended"
  }
};
```

### Validation Query System

```javascript
async function validateNumericalAssignment(assignment) {
  // Check 1: Formula exists and is calculable
  if (!assignment.derivation || !assignment.derivation.formula) {
    return {
      valid: false,
      error: "Missing derivation formula"
    };
  }
  
  // Check 2: Qualitative anchor exists
  if (!assignment.qualitative_anchor || !assignment.qualitative_anchor.tier) {
    return {
      valid: false,
      error: "Missing qualitative anchor"
    };
  }
  
  // Check 3: Narrative matches number
  const narrativeMatch = validateNarrativeMatch(
    assignment.numerical_value,
    assignment.qualitative_anchor,
    assignment.context
  );
  
  if (!narrativeMatch.matches) {
    return {
      valid: false,
      error: `Narrative mismatch: ${narrativeMatch.reason}`
    };
  }
  
  // Check 4: Number in valid range
  const range = getRangeForType(assignment.type);
  if (assignment.numerical_value < range.min || assignment.numerical_value > range.max) {
    return {
      valid: false,
      error: `Value ${assignment.numerical_value} out of range ${range.min}-${range.max}`
    };
  }
  
  // All checks pass
  return {
    valid: true,
    quality_score: calculateValidationQuality(assignment)
  };
}
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Multi-Season System (v1.1 Foundation)
- [x] Multi-season support (8-10 seasons)
- [x] Relationship persistence across seasons
- [x] Card evolution carries forward
- [x] No contradictions (canonical facts system)
- [x] Novel generation support (Life Bookshelf)

### ✅ Master Truths v1.2: Memory Resonance System
- [x] **5 Resonance Types Implemented** (weights 0.7-0.95)
  - Same emotion, different context (0.8)
  - Opposite emotion, growth opportunity (0.9)
  - Past trauma, current trigger (0.95 - highest)
  - Past joy, current sadness (0.85)
  - Emotional growth callback (0.7)
- [x] **Resonance Calculation Formula** with recency decay
- [x] **Memory Recall Priority** based on resonance + recency
- [x] **Narrative Integration** of surfaced memories
- [x] **Threshold:** Base weight 5+ eligible, final score 6.0+ surfaces

### ✅ Master Truths v1.2: Tension Hook Persistence
- [x] **Cross-Season Hook Tracking** (S2 hooks → S5 payoffs)
- [x] **Information Debt Database** with gap tracking
- [x] **Hook Lifecycle Management** (planting → building → payoff)
- [x] **Payoff Timeline Tracking** (2-4 weeks, 5-8 weeks, season_end)
- [x] **Hook Status Monitoring** (planted | overdue | resolved | abandoned)
- [x] **Quality Scoring** per hook (tension, payoff, coherence)
- [x] **Long-Term Resonance** callbacks across seasons

### ✅ Master Truths v1.2: Dramatic Irony Knowledge Tracking
- [x] **Dual Knowledge Bases** (player vs. character knowledge)
- [x] **Knowledge Gap Detection** algorithm
- [x] **Irony Score Calculation** (≥ 0.6 threshold for use)
  - Knowledge clarity (0.25 weight)
  - Tension created (0.30 weight)
  - Emotional weight (0.20 weight)
  - Player investment (0.15 weight)
  - Timing quality (0.10 weight)
- [x] **Three Response Types** (tone-deaf, misguided, growth)
- [x] **Player Overlays** showing knowledge gaps
- [x] **Capacity-Limited Perception** integration

### ✅ Master Truths v1.2: Capacity History Tracking
- [x] **Capacity Snapshots** at key moments
- [x] **Pattern Identification** (burnout cycles, seasonal trends)
- [x] **Predictive Modeling** for future capacity
- [x] **Intervention Recommendations** based on patterns
- [x] **NPC Capacity History** tracking
- [x] **Support Availability Prediction** (capacity - 2 rule)

### ✅ Master Truths v1.2: Quality Validation Across Tiers
- [x] **Tier 1 Validation** (active context - threshold 0.85 authenticity)
- [x] **Tier 2 Validation** (recent history - threshold 0.78 authenticity)
- [x] **Tier 3 Validation** (compressed - threshold 0.72 authenticity)
- [x] **Compression Rules** preserve high-quality moments only
- [x] **Season-End Quality Report** with scores per act
- [x] **Multi-Tier Consistency** maintained across compression

### ✅ Master Truths v1.2: Numerical Grounding
- [x] **Formula Storage** for every numerical assignment
- [x] **Qualitative Anchors** referenced for all numbers
- [x] **Validation System** (narrative matches number)
- [x] **Trust Impact Storage** with full derivation
- [x] **Capacity Value Storage** with calculation steps
- [x] **Canonical Fact Immutability** for defining moments
- [x] **Validation Query System** enforces grounding

### ✅ Cross-References
- [x] Links to Master Truths v1.2 concepts throughout
- [x] References `NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md`
- [x] Integrates with `21-card-evolution-mechanics.md`
- [x] Connects to `73-season-flow-implementation.md`
- [x] This doc cites **Truths v1.2** at the top

**References:**
- See `1.concept/22-multi-lifetime-continuity.md` for design philosophy
- See `73-season-flow-implementation.md` for inter-season transitions
- See `21-card-evolution-mechanics.md` for cross-season card evolution
- See `master_truths_canonical_spec_v_1_2.md` Section 16 (Emotional Authenticity)
- See `master_truths_canonical_spec_v_1_2.md` Section 17 (Novel-Quality Narratives)
- See `NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md` for qualitative anchors

---

**This specification enables developers to implement the complete multi-season continuity system with emotional resonance, dramatic irony tracking, capacity history, quality validation, and numerical grounding that make 8-10 season character lifecycles feel coherent, authentic, and novel-quality across all memory tiers.**

