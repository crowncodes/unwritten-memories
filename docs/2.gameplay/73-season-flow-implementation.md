# Season Flow & Inter-Season Transitions - Complete Specification

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete flow from season end → inter-season transition → new season start with capacity recovery, memory consolidation, emotional state carry-over, and quality validation

**References:**
- **Design Philosophy:** `1.concept/15-progression-phases.md` (season structure)
- **Season Structure:** `40-season-structure-spec.md` (12/24/36 weeks)
- **Continuity:** `1.concept/22-multi-lifetime-continuity.md` (multi-season tracking)
- **Novel Generation:** `6.monetization/novel-generation-integration.md` (archive creation)

---

## Overview

**Core Mechanic:** Seasons are **chapters of ONE character's life**, not separate playthroughs. After completing a season, players can **continue with the same character** in a new season, carrying over ALL progress (relationships, skills, memories, personality evolution). 

**Time Skip System:** Between seasons, time can fast-forward (1 week to 10+ years) with the game automatically generating what happened during the skip based on the new aspiration choice.

**Life Bookshelf:** Each character has their own "bookshelf" of novels (one per season), with a **maximum of 8 seasons** (10 with premium Essence purchase).

**Compliance:** This is a **LIFE SIMULATION**, not a roguelike. Characters persist across multiple seasons until the player chooses to retire them or reaches the season limit.

---

## Season End → New Season Flow

### Complete Transition Process

```
SEASON COMPLETE
├─ Week 12/24/36 (or early completion)
├─ Aspiration resolved (success/partial/failure)
├─ Final week narrative + resolution
└─ Season metrics calculated

↓

SEASON ARCHIVE GENERATION (2-3 minutes processing)
├─ Novel generation begins (background process)
├─ Generate 8,000-60,000 word novel (based on season length)
├─ Add to character's Life Bookshelf
├─ Season marked as "archived"
└─ Notify player when novel ready

↓

INTER-SEASON REFLECTION (Player sees this)
┌────────────────────────────────────────┐
│ SEASON 3 COMPLETE: "THE PHOTOGRAPHER" │
├────────────────────────────────────────┤
│ Duration: 24 weeks (6 months)          │
│ Aspiration: Launch Photography Business│
│ Result: SUCCESS                        │
│                                        │
│ Your Story This Season:                │
│ • Quit corporate job                   │
│ • Launched business                    │
│ • First 3 paid clients                 │
│ • Deepened friendship with Sarah       │
│ • Overcame financial crisis            │
│                                        │
│ Character Growth:                      │
│ • Confidence: 0.68 → 0.85             │
│ • Photography Skill: 4 → 7            │
│ • Extraversion: 2.3 → 3.1             │
│                                        │
│ Novel Status: Generating... (15%)      │
│                                        │
│ [Continue This Character's Story] →    │
│ [Retire This Character]                │
│ [View Archive]                         │
└────────────────────────────────────────┘

↓ Player chooses "Continue"

NEW SEASON ASPIRATION SELECTION
┌────────────────────────────────────────┐
│ WHAT'S NEXT FOR YOUR STORY?           │
├────────────────────────────────────────┤
│ Season 4 begins...                     │
│                                        │
│ Current State:                         │
│ • Age 29 → 30                         │
│ • Photography business established     │
│ • Sarah (Close Friend, Trust 0.78)    │
│ • Marcus (Best Friend, Trust 0.85)    │
│ • Money: $2,400                       │
│                                        │
│ CHOOSE YOUR NEXT CHAPTER:              │
│                                        │
│ 🔼 BUILD ON SUCCESS                   │
│ ○ Grow Photography Business           │
│   "Scale to next level"               │
│   Time Skip: 1 year (business matures)│
│                                        │
│ ○ Become Wedding Photographer         │
│   "Specialize and dominate niche"     │
│   Time Skip: 6 months (build portfolio)│
│                                        │
│ 🔄 RELATED PIVOT                      │
│ ○ Open Creative Studio with Sarah     │
│   "Partnership opportunity"           │
│   Time Skip: 3 months (planning phase)│
│                                        │
│ ○ Teach Photography Workshops         │
│   "Share your craft"                  │
│   Time Skip: 1 year (establish rep)   │
│                                        │
│ 🌀 MAJOR LIFE CHANGE                  │
│ ○ Business Failed - Find New Path     │
│   "Photography didn't work out"       │
│   Time Skip: 3 years (recovery + pivot)│
│                                        │
│ ○ Start Family / Major Life Shift     │
│   "Different priorities now"          │
│   Time Skip: 2-5 years (life changes) │
│                                        │
│ [Select Aspiration] →                  │
└────────────────────────────────────────┘

↓ Player selects aspiration with time skip

TIME SKIP GENERATION (Processing 1-2 minutes)
├─ Generate intervening narrative
├─ Calculate world evolution
├─ Age all NPCs
├─ Update relationships based on contact
├─ Generate filler context
└─ Set up new season starting state

↓

TIME SKIP NARRATIVE (Player sees)
┌────────────────────────────────────────┐
│ TIME SKIP: 1 YEAR                     │
├────────────────────────────────────────┤
│ [AI-GENERATED NARRATIVE]               │
│                                        │
│ A year passes. Your business grows     │
│ steadily—not explosively, but solidly. │
│ You've shot 47 weddings, countless     │
│ portraits. Your style is developing.   │
│                                        │
│ Sarah opened her bookshop last spring. │
│ You were there for the opening, tears  │
│ in her eyes. You see each other less   │
│ now—both busy building dreams—but the  │
│ friendship is bedrock.                 │
│                                        │
│ Marcus got engaged. You were the best  │
│ man. The wedding is next month.        │
│                                        │
│ Your apartment is nicer now. You can   │
│ afford it. The anxiety about money has │
│ eased. You're not rich, but you're     │
│ making it work.                        │
│                                        │
│ You're 30 now. When did that happen?  │
│                                        │
│ A new question emerges...              │
│ [Continue to Season 4] →               │
└────────────────────────────────────────┘

↓

NEW SEASON BEGINS
├─ Season 4, Week 1 starts
├─ All context from Season 3 + time skip available
├─ Character is 1 year older
├─ Relationships updated (Sarah still close, Marcus engaged)
├─ Skills retained (Photography: 7 → 8 from year of practice)
├─ New aspiration: "Become Wedding Photographer"
└─ Choose season length (12/24/36 weeks)
```

---

## Time Skip System

### How Time Skips Work

```javascript
interface TimeSkip {
  duration_weeks: number;           // 1 week to 500+ weeks
  duration_display: string;         // "3 months", "2 years", "5 years"
  
  trigger: "new_aspiration_selected";
  calculated_from: {
    new_aspiration_type: string,
    previous_season_outcome: string,
    logical_gap_needed: number
  };
  
  generated_content: {
    narrative_summary: string,      // 500-1500 words
    world_evolution: WorldState,
    npc_life_events: NPCEvent[],
    character_changes: CharacterDelta,
    new_starting_state: GameState
  };
}
```

### Time Skip Duration by Aspiration Type

```javascript
const TIME_SKIP_LOGIC = {
  continue_same_trajectory: {
    examples: [
      "Grow existing business",
      "Master current skill further",
      "Deepen existing relationship"
    ],
    typical_skip: "3-12 months",
    reasoning: "Short maturation period needed"
  },
  
  related_pivot: {
    examples: [
      "Pivot photography to weddings",
      "Open studio with partner",
      "Teach workshops alongside practice"
    ],
    typical_skip: "6-18 months",
    reasoning: "Time to establish new direction while building on existing"
  },
  
  moderate_change: {
    examples: [
      "Career change to adjacent field",
      "Move to new city",
      "Major relationship shift"
    ],
    typical_skip: "1-3 years",
    reasoning: "Significant transition time needed"
  },
  
  major_pivot: {
    examples: [
      "Complete career change",
      "Failed business → recovery",
      "Major life crisis → rebuilding"
    ],
    typical_skip: "2-5 years",
    reasoning: "Recovery, retraining, or major life restructuring"
  },
  
  life_phase_shift: {
    examples: [
      "Start family after career focus",
      "Return to passion after family years",
      "Retirement transition"
    ],
    typical_skip: "5-10 years",
    reasoning: "Different life phase with different priorities"
  }
};
```

### Example Time Skip Calculations

```javascript
// EXAMPLE 1: Building on success
const SKIP_EXAMPLE_1 = {
  previous_season: {
    aspiration: "Launch Photography Business",
    outcome: "SUCCESS",
    season_end_state: {
      age: 29,
      business_status: "just_launched",
      money: 2400,
      key_relationships: ["Sarah (Level 4)", "Marcus (Level 5)"]
    }
  },
  
  new_aspiration: "Become Premier Wedding Photographer",
  
  calculated_skip: {
    duration: "1 year",
    reasoning: "Need time for business to mature, build portfolio, establish reputation",
    
    narrative_generated: `
      A year of grinding. Weddings every weekend in summer. 
      Portraits during the week. Your Instagram grows. Word of mouth.
      The business is real now. Not just surviving—thriving.
    `,
    
    world_changes: {
      character: {
        age: 29 → 30,
        photography_skill: 7 → 8,
        business_skill: 3 → 5,
        money: 2400 → 8500,
        confidence: 0.85 → 0.92
      },
      npcs: {
        sarah: {
          age: 28 → 29,
          status: "Opened bookshop (6 months ago)",
          relationship_level: 4 (maintained),
          trust: 0.78 → 0.82,
          life_event: "Bookshop successful"
        },
        marcus: {
          age: 29 → 30,
          status: "Got engaged",
          relationship_level: 5 (maintained),
          life_event: "Wedding planned for next month"
        }
      }
    }
  }
};

// EXAMPLE 2: Major pivot after failure
const SKIP_EXAMPLE_2 = {
  previous_season: {
    aspiration: "Launch Photography Business",
    outcome: "FAILURE",
    season_end_state: {
      age: 29,
      business_status: "failed",
      money: 400,
      emotional_state: "DISCOURAGED",
      debt: 5000
    }
  },
  
  new_aspiration: "Find New Meaning - Explore Different Path",
  
  calculated_skip: {
    duration: "3 years",
    reasoning: "Need time to recover, pay debt, rebuild confidence, explore new direction",
    
    narrative_generated: `
      Three years. They blur together in retrospect.
      
      You went back to corporate. Hated it. Paid off the debt though.
      Therapy helped. Slowly. The shame of failing faded into... acceptance.
      
      Sarah's bookshop thrived. You watched from the sidelines, happy for her
      but quietly wondering why it worked for her and not for you.
      
      Marcus got married. Had a kid. You're Uncle Alex now.
      
      You're 32. Photography equipment sits in a closet. Maybe someday.
      But right now? You need to figure out what's actually next.
    `,
    
    world_changes: {
      character: {
        age: 29 → 32,
        photography_skill: 7 → 6,      // Atrophy
        money: 400 → 3200,
        confidence: 0.85 → 0.65,        // Damaged by failure
        neuroticism: 3.2 → 3.8,         // Increased from trauma
        debt: 0                          // Paid off
      },
      npcs: {
        sarah: {
          age: 28 → 31,
          status: "Successful bookshop owner (3 years)",
          relationship_level: 4 → 3,    // Drifted slightly
          trust: 0.78 → 0.72,
          life_event: "Business thriving, considering expansion"
        },
        marcus: {
          age: 29 → 32,
          status: "Married, 1-year-old daughter",
          relationship_level: 5 (maintained through effort),
          life_event: "Became father, you're Uncle Alex"
        }
      }
    }
  }
};
```

---

## Master Truths v1.2: Capacity Recovery at Phase Transitions *(NEW)*

### Major Life Transitions Provide Partial Recovery

**Core Principle:** Moving from Season 3 → Season 4 (even with short time skip) provides emotional capacity recovery. New chapter = renewed energy.

```javascript
function calculateCapacityRecoveryAtTransition(playerState, timeSkip, newAspiration) {
  const recovery = {
    season_end_capacity: playerState.capacity.value,
    
    // BASE RECOVERY: Time off provides rest
    time_based_recovery: calculateTimeRecovery(timeSkip.duration_weeks),
    
    // TRANSITION RECOVERY: New chapter provides fresh start
    transition_recovery: calculateTransitionRecovery(timeSkip.type, newAspiration),
    
    // TOTAL RECOVERY
    total_recovery: 0,
    
    new_season_capacity: 0
  };
  
  // Time-based recovery
  if (timeSkip.duration_weeks <= 4) {
    recovery.time_based_recovery = 1.0;  // 1 month = +1.0 capacity
  } else if (timeSkip.duration_weeks <= 26) {
    recovery.time_based_recovery = 2.0;  // 6 months = +2.0 capacity
  } else if (timeSkip.duration_weeks <= 104) {
    recovery.time_based_recovery = 2.5;  // 2 years = +2.5 capacity
  } else {
    recovery.time_based_recovery = 3.0;  // 5+ years = +3.0 capacity (max)
  }
  
  // Transition-based recovery
  switch (timeSkip.type) {
    case "continue_same_trajectory":
      recovery.transition_recovery = 0.5;  // Minimal fresh start
      break;
    case "related_pivot":
      recovery.transition_recovery = 1.0;  // Moderate fresh start
      break;
    case "moderate_change":
      recovery.transition_recovery = 1.5;  // Significant reset
      break;
    case "major_pivot":
      recovery.transition_recovery = 2.0;  // Major life reset
      break;
    case "life_phase_shift":
      recovery.transition_recovery = 2.5;  // Complete reset
      break;
  }
  
  // Total recovery
  recovery.total_recovery = recovery.time_based_recovery + recovery.transition_recovery;
  
  // New season capacity (capped at 8.0)
  recovery.new_season_capacity = Math.min(8.0, 
    playerState.capacity.value + recovery.total_recovery
  );
  
  // BUT: Persistent stressors carry over
  if (playerState.persistent_stressors && playerState.persistent_stressors.length > 0) {
    recovery.stressor_penalty = playerState.persistent_stressors.length * 0.5;
    recovery.new_season_capacity -= recovery.stressor_penalty;
    recovery.note = `${playerState.persistent_stressors.length} persistent stressors reduce recovery`;
  }
  
  return recovery;
}
```

### Example: Capacity Recovery Scenarios

```javascript
// SCENARIO 1: Short pivot after successful season
const RECOVERY_EXAMPLE_1 = {
  season_3_end: {
    capacity: 4.5,  // Ended season exhausted
    persistent_stressors: []  // No ongoing issues
  },
  
  time_skip: {
    duration_weeks: 26,  // 6 months
    type: "related_pivot"
  },
  
  recovery_calculation: {
    time_based: 2.0,  // 6 months off
    transition_based: 1.0,  // Related pivot
    total: 3.0,
    
    new_capacity: 4.5 + 3.0 = 7.5  // ✓ Fresh start!
  },
  
  narrative: "Six months pass. The break did you good. You feel ready for this new chapter."
};

// SCENARIO 2: Major pivot after failure with lingering issues
const RECOVERY_EXAMPLE_2 = {
  season_3_end: {
    capacity: 2.0,  // Ended in crisis
    persistent_stressors: ["financial_pressure", "confidence_damage"]
  },
  
  time_skip: {
    duration_weeks: 156,  // 3 years
    type: "major_pivot"
  },
  
  recovery_calculation: {
    time_based: 2.5,  // 3 years
    transition_based: 2.0,  // Major pivot
    total: 4.5,
    stressor_penalty: -1.0,  // 2 stressors × 0.5
    
    new_capacity: 2.0 + 4.5 - 1.0 = 5.5  // Recovered, but scars remain
  },
  
  narrative: "Three years. Time heals, but not completely. The debt is gone, but the fear of failure lingers. You're functional again. That's something."
};
```

---

## Master Truths v1.2: Memory Consolidation Triggers *(NEW)*

### Select High-Resonance Memories for Permanent Storage

**Core Principle:** Season transitions trigger memory consolidation. Only high-emotional-weight moments (≥8.0) are preserved in full detail.

```javascript
function consolidateSeasonMemories(seasonState, memoryDatabase) {
  const consolidation = {
    season_number: seasonState.season_number,
    
    // All memories from season
    total_memories: memoryDatabase.filter(m => m.season === seasonState.season_number).length,
    
    // High-value memories to preserve
    preserved_memories: [],
    
    // Routine memories to compress
    compressed_memories: [],
    
    // Criteria
    preservation_criteria: {
      emotional_weight_threshold: 8.0,
      relationship_milestone: true,
      trauma_marker: true,
      phase_transition: true,
      decisive_decision: true
    }
  };
  
  memoryDatabase
    .filter(m => m.season === seasonState.season_number)
    .forEach(memory => {
      let shouldPreserve = false;
      
      // Check criteria
      if (memory.emotional_weight >= 8.0) shouldPreserve = true;
      if (memory.relationship_milestone) shouldPreserve = true;
      if (memory.trauma_marker) shouldPreserve = true;
      if (memory.phase_transition) shouldPreserve = true;
      if (memory.decisive_decision) shouldPreserve = true;
      
      if (shouldPreserve) {
        consolidation.preserved_memories.push({
          memory_id: memory.id,
          emotional_weight: memory.emotional_weight,
          resonance_factors: memory.resonance_factors || [],
          full_narrative: memory.narrative,
          preservation_reason: determinePreservationReason(memory)
        });
      } else {
        consolidation.compressed_memories.push({
          memory_id: memory.id,
          emotional_weight: memory.emotional_weight,
          compressed_summary: generateCompressedSummary(memory)
        });
      }
    });
  
  consolidation.preservation_rate = 
    consolidation.preserved_memories.length / consolidation.total_memories;
  
  return consolidation;
}
```

### Memory Consolidation Example

```
SEASON 3 END: Memory Consolidation

Total memories: 47
High-value memories preserved: 8
Routine memories compressed: 39

PRESERVED MEMORIES (Full Detail):
─────────────────────────────────────────
1. Week 14: Collapsed During Wedding Shoot
   Emotional Weight: 10.0 (MAXIMUM)
   Trauma Marker: HEALTH_CRISIS
   Reason: Past trauma trigger potential
   
2. Week 18: Sarah Reveals David's Death
   Emotional Weight: 9.5
   Relationship Milestone: Level 2 → 3
   Reason: Emotional growth callback potential
   
3. Week 22: Quit Corporate Job
   Emotional Weight: 9.0
   Phase Transition: Career change
   Reason: Major life decision
   
4. Week 24: First Paid Client
   Emotional Weight: 8.5
   Aspiration Milestone: Business launch
   Reason: Confidence breakthrough
   
[4 more preserved...]

COMPRESSED MEMORIES (Summary Only):
─────────────────────────────────────────
39 routine interactions compressed:
• 12 routine work days
• 8 casual social meetings
• 7 errands/chores
• 12 practice sessions

Preserved: 17% of memories (8/47)
Compression Ratio: 83%
```

---

## Master Truths v1.2: Emotional State Carry-Over Rules *(NEW)*

### How Emotional States Persist Across Time Skips

**Core Principle:** Acute emotional states (OVERWHELMED, EXCITED) decay during time skip. Chronic states (patterns, trauma) persist.

```javascript
function calculateEmotionalStateCarryOver(seasonEndState, timeSkip) {
  const carryOver = {
    season_end_state: seasonEndState.emotional_state,
    time_skip_duration: timeSkip.duration_weeks,
    
    // Acute states decay
    acute_decay_rate: calculateDecayRate(timeSkip.duration_weeks),
    
    // Chronic patterns persist
    chronic_patterns: seasonEndState.chronic_patterns || [],
    
    // New season emotional state
    new_season_state: null
  };
  
  // ACUTE EMOTIONAL STATES (decay over time)
  const acuteStates = [
    "EXCITED", "OVERWHELMED", "ANXIOUS", "ELATED", 
    "DISCOURAGED", "EXHAUSTED", "RESTLESS"
  ];
  
  if (acuteStates.includes(carryOver.season_end_state)) {
    // Acute states decay completely after 4+ weeks
    if (timeSkip.duration_weeks >= 4) {
      carryOver.new_season_state = "CONTENT";  // Return to baseline
      carryOver.note = `${carryOver.season_end_state} faded during time skip`;
    } else {
      carryOver.new_season_state = carryOver.season_end_state;
      carryOver.note = `${carryOver.season_end_state} persists (short skip)`;
    }
  } else {
    // CHRONIC PATTERNS (persist across time)
    carryOver.new_season_state = carryOver.season_end_state;
    carryOver.note = `Chronic pattern persists`;
  }
  
  // TRAUMA MARKERS persist indefinitely
  if (seasonEndState.trauma_markers && seasonEndState.trauma_markers.length > 0) {
    carryOver.trauma_persistence = seasonEndState.trauma_markers.map(trauma => ({
      trauma_type: trauma.type,
      origin_season: trauma.season,
      still_active: true,
      resonance_weight: 0.95  // Can trigger during new season
    }));
  }
  
  return carryOver;
}
```

---

## Master Truths v1.2: Tension Arc Completion Validation *(NEW)*

### Validate All Hooks Resolved Before Season End

**Core Principle:** Season cannot end with unresolved tension hooks. All planted hooks must either pay off or be explicitly abandoned.

```javascript
function validateTensionArcCompletion(seasonState, activeHooks) {
  const validation = {
    season_number: seasonState.season_number,
    
    hooks_planted_this_season: 0,
    hooks_resolved: 0,
    hooks_unresolved: [],
    
    arc_complete: false,
    warnings: []
  };
  
  // Check all hooks from this season
  const seasonHooks = activeHooks.filter(h => h.season_planted === seasonState.season_number);
  validation.hooks_planted_this_season = seasonHooks.length;
  
  seasonHooks.forEach(hook => {
    if (hook.status === "resolved") {
      validation.hooks_resolved++;
    } else {
      validation.hooks_unresolved.push({
        hook_id: hook.hook_id,
        hook_type: hook.hook_type,
        weeks_active: seasonState.week_number - hook.week_planted,
        issue: "Hook planted but never paid off"
      });
    }
  });
  
  // Check hooks from PREVIOUS seasons
  const carryOverHooks = activeHooks.filter(h => 
    h.season_planted < seasonState.season_number &&
    h.status !== "resolved"
  );
  
  carryOverHooks.forEach(hook => {
    validation.hooks_unresolved.push({
      hook_id: hook.hook_id,
      hook_type: hook.hook_type,
      seasons_active: seasonState.season_number - hook.season_planted,
      issue: "Multi-season hook never resolved"
    });
  });
  
  // VALIDATION
  validation.arc_complete = validation.hooks_unresolved.length === 0;
  
  if (!validation.arc_complete) {
    validation.warnings.push({
      level: "CRITICAL",
      message: `${validation.hooks_unresolved.length} unresolved tension hooks`,
      action_required: "MUST resolve or explicitly abandon before season end",
      hooks: validation.hooks_unresolved.map(h => h.hook_id)
    });
  }
  
  return validation;
}
```

---

## Master Truths v1.2: Novel-Quality Season Validation *(NEW)*

### Validate Entire Season Meets v1.2 Thresholds

**Core Principle:** Before archiving season as novel, validate emotional authenticity, tension, and dramatic irony across entire season.

```javascript
function validateSeasonQuality(seasonState, memoryDatabase, hookTracking) {
  const validation = {
    season_number: seasonState.season_number,
    total_weeks: seasonState.week_number,
    
    scores: {
      emotional_authenticity: 0,
      tension_building: 0,
      dramatic_irony: 0,
      hook_effectiveness: 0,
      overall_quality: 0
    },
    
    thresholds: {
      emotional_authenticity: 0.70,  // Season-level
      tension_building: 0.65,
      dramatic_irony: 0.55,  // When applicable
      hook_effectiveness: 0.70,
      overall_minimum: 0.70
    },
    
    passes: false,
    suitable_for_archive: false
  };
  
  // SCORE 1: Emotional Authenticity (average across all weeks)
  const weeklyAuthenticityScores = seasonState.weeks.map(w => w.quality_scores.emotional_authenticity);
  validation.scores.emotional_authenticity = 
    weeklyAuthenticityScores.reduce((sum, s) => sum + s, 0) / weeklyAuthenticityScores.length;
  
  // SCORE 2: Tension Building (hook progression)
  const hookStats = {
    total_planted: hookTracking.hooks_planted,
    total_resolved: hookTracking.hooks_resolved,
    average_quality: hookTracking.hooks_resolved.reduce((sum, h) => sum + h.payoff_quality, 0) / hookTracking.hooks_resolved.length
  };
  
  validation.scores.tension_building = hookStats.average_quality;
  validation.scores.hook_effectiveness = hookStats.total_resolved / hookStats.total_planted;
  
  // SCORE 3: Dramatic Irony (when present)
  const ironyMoments = seasonState.weeks.flatMap(w => w.dramatic_irony_moments || []);
  if (ironyMoments.length > 0) {
    validation.scores.dramatic_irony = 
      ironyMoments.reduce((sum, m) => sum + m.irony_score, 0) / ironyMoments.length;
  } else {
    validation.scores.dramatic_irony = "N/A";  // No irony this season
  }
  
  // OVERALL QUALITY
  const ironyScore = validation.scores.dramatic_irony === "N/A" ? 0.65 : validation.scores.dramatic_irony;
  validation.scores.overall_quality = 
    (validation.scores.emotional_authenticity * 0.35) +
    (validation.scores.tension_building * 0.25) +
    (ironyScore * 0.20) +
    (validation.scores.hook_effectiveness * 0.20);
  
  // VALIDATION
  validation.passes = 
    validation.scores.emotional_authenticity >= validation.thresholds.emotional_authenticity &&
    validation.scores.tension_building >= validation.thresholds.tension_building &&
    validation.scores.hook_effectiveness >= validation.thresholds.hook_effectiveness &&
    validation.scores.overall_quality >= validation.thresholds.overall_minimum;
  
  validation.suitable_for_archive = validation.passes;
  
  if (!validation.passes) {
    validation.quality_issues = [];
    
    if (validation.scores.emotional_authenticity < 0.70) {
      validation.quality_issues.push({
        category: "emotional_authenticity",
        score: validation.scores.emotional_authenticity,
        issue: "Below 0.70 threshold - NPCs may not have respected capacity limits"
      });
    }
    
    if (validation.scores.hook_effectiveness < 0.70) {
      validation.quality_issues.push({
        category: "hook_effectiveness",
        score: validation.scores.hook_effectiveness,
        issue: "Too many abandoned hooks - less than 70% resolved"
      });
    }
  }
  
  return validation;
}
```

---

## Life Bookshelf System

### Character Lifecycle

```javascript
interface CharacterLifecycle {
  character_id: string;
  character_name: string;
  starting_age: number;
  
  life_bookshelf: {
    character_name: string,
    total_seasons: number,
    max_seasons: 8,                  // Base limit
    premium_unlocked: false,          // +2 seasons if true (max 10)
    
    novels: Novel[],                  // One per season
    total_word_count: number,
    average_words_per_season: 15000
  };
  
  status: "active" | "retired" | "completed";
}
```

### Season Limits

```javascript
const SEASON_LIMITS = {
  free_base: {
    max_seasons: 8,
    rationale: "8 seasons × ~15k words = 120k word novel (full book)"
  },
  
  premium_essence: {
    cost_per_additional_season: 500,  // Essence
    max_additional: 2,
    total_max: 10,
    rationale: "Allow epic 10-season sagas for dedicated players"
  },
  
  enforcement: {
    at_season_8_complete: {
      message: "You've completed 8 seasons with this character!",
      options: [
        {
          action: "retire_character",
          result: "Character retired, bookshelf archived, can view anytime"
        },
        {
          action: "purchase_season_9",
          cost: 500,
          result: "Unlock Season 9"
        }
      ]
    },
    
    at_season_10_complete: {
      message: "This is the final season for this character.",
      result: "Character MUST be retired (no more seasons possible)",
      reasoning: "10 seasons = 150k words = epic saga. Time for closure."
    }
  }
};
```

### Life Bookshelf Display

```
┌────────────────────────────────────────┐
│ ALEX CHEN'S LIFE BOOKSHELF            │
├────────────────────────────────────────┤
│ Age 28 → 33 (5 years)                 │
│ 4 Seasons Completed | 4 Remaining     │
│                                        │
│ 📕 Season 1: "Finding My Feet"        │
│    12 weeks | 8,200 words             │
│    Aspiration: Creative Awakening      │
│                                        │
│ 📘 Season 2: "The First Steps"        │
│    24 weeks | 22,400 words            │
│    Aspiration: Learn Photography       │
│                                        │
│ 📗 Season 3: "The Photographer"        │
│    24 weeks | 24,800 words            │
│    Aspiration: Launch Business         │
│                                        │
│ 📙 Season 4: "Wedding Season"          │
│    36 weeks | 48,200 words            │
│    Aspiration: Premier Wedding Photog  │
│                                        │
│ 📓 Season 5: IN PROGRESS...           │
│    Week 8 of 24                        │
│    Aspiration: Creative Studio w/ Sarah│
│                                        │
│ Total Story: 103,600 words so far      │
│                                        │
│ [Continue Season 5] →                  │
│ [Read Any Novel]                       │
│ [Character Stats]                      │
│ [Share Bookshelf]                      │
└────────────────────────────────────────┘
```

---

## Character Retirement

### When Characters End

```javascript
const CHARACTER_ENDINGS = {
  voluntary_retirement: {
    trigger: "Player chooses to retire character",
    timing: "After any season complete",
    effects: {
      bookshelf: "Archived, can view anytime",
      character: "Marked as 'retired', shows final age/state",
      new_character: "Can create new character for new story"
    }
  },
  
  season_limit_reached: {
    trigger: "Season 10 complete (max limit)",
    timing: "Automatic after Season 10 ends",
    effects: {
      final_season: "Season 10 must include narrative closure",
      bookshelf: "Complete 10-volume saga archived",
      character: "Permanently completed",
      achievement: "Epic Saga achievement unlocked"
    }
  },
  
  character_death: {
    trigger: "Optional narrative choice in late seasons",
    timing: "Player can choose 'final season' with death",
    effects: {
      narrative: "Season ends with character's death/passing",
      bookshelf: "Complete with epilogue",
      emotional_weight: "High - designed for catharsis"
    },
    note: "Optional - players don't have to choose this"
  }
};
```

### Retirement Flow

```
SEASON 6 COMPLETE
↓
INTER-SEASON MENU
┌────────────────────────────────────────┐
│ CONTINUE ALEX'S STORY?                │
├────────────────────────────────────────┤
│ You've completed 6 of 8 seasons.      │
│                                        │
│ Alex is now 34 years old.             │
│ • 6-volume life story (95k words)     │
│ • Photography business established     │
│ • Creative studio with Sarah thriving │
│ • Deep friendships maintained          │
│                                        │
│ OPTIONS:                               │
│                                        │
│ [Continue to Season 7] →              │
│ Choose new aspiration, 2 seasons left │
│                                        │
│ [Retire This Character]                │
│ End Alex's story here. Bookshelf       │
│ archived. Can create new character.    │
│                                        │
│ [Purchase +2 Seasons] 500 Essence     │
│ Unlock Seasons 9-10 for epic finale    │
└────────────────────────────────────────┘
```

---

## Multi-Character System

### Players Can Have Multiple Characters

```javascript
const MULTI_CHARACTER_SYSTEM = {
  max_active_characters: 3,           // Can work on 3 life stories simultaneously
  
  character_slots: [
    {
      slot: 1,
      character: "Alex Chen",
      current_season: 5,
      max_seasons: 8,
      status: "active",
      bookshelf_words: 103600
    },
    {
      slot: 2,
      character: "Maya Rodriguez",
      current_season: 2,
      max_seasons: 8,
      status: "active",
      bookshelf_words: 18400
    },
    {
      slot: 3,
      character: "Empty",
      status: "available"
    }
  ],
  
  switching: {
    can_switch: "Anytime between seasons",
    cannot_switch: "Mid-season (must complete current season first)",
    context: "Each character maintains their own complete context"
  },
  
  premium_benefits: {
    plus_tier: {
      max_active_characters: 5,
      season_limit_per_character: 8
    },
    ultimate_tier: {
      max_active_characters: 10,
      season_limit_per_character: 10
    }
  }
};
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Season Mechanics (v1.1 Foundation)
- [x] Seasons are chapters of ONE character's life (not separate playthroughs)
- [x] Full continuity between seasons (all memories, relationships, skills carry over)
- [x] Time skips auto-generate intervening narrative
- [x] Life Bookshelf: max 8 seasons base (10 with premium)
- [x] Each season generates one novel for the bookshelf
- [x] Players can have multiple characters (3 active, 5/10 with premium)
- [x] Time skip logic by aspiration type (continue trajectory, pivot, major change, life phase shift)
- [x] Character retirement system (voluntary or season limit reached)

### ✅ Master Truths v1.2: Capacity Recovery at Phase Transitions
- [x] **Capacity Recovery Calculation** (~60 lines)
  - Time-based recovery (1 week to 5+ years, +1.0 to +3.0)
  - Transition-based recovery (0.5 to 2.5 by pivot type)
  - Combined recovery calculation (capped at 8.0)
  - Persistent stressor penalty (-0.5 per stressor)
- [x] **Two Recovery Examples** (success vs. failure paths)
- [x] **New Season Capacity** calculated and displayed
- [x] **Narrative Integration** (recovery reflected in time skip text)

### ✅ Master Truths v1.2: Memory Consolidation Triggers
- [x] **Memory Consolidation System** (~55 lines)
  - Emotional weight threshold (≥8.0 preserved)
  - Relationship milestones preserved
  - Trauma markers preserved
  - Phase transitions preserved
  - Decisive decisions preserved
  - Routine memories compressed (83% typical)
- [x] **Preservation Rate Tracking** (17% typical)
- [x] **Full vs. Compressed Memory Storage**
- [x] **Consolidation Report Display** at season end

### ✅ Master Truths v1.2: Emotional State Carry-Over Rules
- [x] **State Carry-Over Logic** (~45 lines)
  - Acute emotional states decay (4+ weeks = return to baseline)
  - Chronic patterns persist indefinitely
  - Trauma markers persist with 0.95 resonance weight
  - New season emotional state calculated
- [x] **State Classification** (acute vs. chronic)
- [x] **Trauma Persistence** system
- [x] **Decay Timeline** (short skip vs. long skip)

### ✅ Master Truths v1.2: Tension Arc Completion Validation
- [x] **Arc Completion Validator** (~55 lines)
  - Check all hooks from current season
  - Check carry-over hooks from previous seasons
  - Identify unresolved hooks
  - Warning system for incomplete arcs
  - Action required before season end
- [x] **Hook Resolution Rate** tracking
- [x] **Multi-Season Hook Validation**
- [x] **Critical Warnings** for unresolved hooks

### ✅ Master Truths v1.2: Novel-Quality Season Validation
- [x] **Season Quality Scoring** (~85 lines)
  - Emotional Authenticity Score (average across weeks, threshold 0.70)
  - Tension Building Score (hook payoff quality, threshold 0.65)
  - Dramatic Irony Score (when present, threshold 0.55)
  - Hook Effectiveness Score (resolution rate, threshold 0.70)
  - Overall Quality Score (weighted formula, threshold 0.70)
- [x] **Multi-Week Aggregation** of quality metrics
- [x] **Quality Issue Identification** when below thresholds
- [x] **Archive Suitability** determination

### ✅ Cross-References
- [x] Links to `71-daily-turn-flow-detailed.md` (turn-level v1.2 mechanics)
- [x] Links to `72-weekly-cycle-implementation.md` (week-level v1.2 tracking)
- [x] Links to `74-multi-season-continuity-spec.md` (memory resonance, hook persistence)
- [x] Links to `40-season-structure-spec.md` (season length specs)
- [x] Links to `master_truths_canonical_spec_v_1_2.md` Sections 16 & 17
- [x] This doc cites **Truths v1.2** at the top

**Total v1.2 Enhancements:** ~300 lines of season transition v1.2 mechanics

**Key Clarifications:**
- This is **NOT a roguelike** - characters persist across multiple seasons
- **NOT like Reigns** - not disposable playthroughs
- **IS like The Sims** - one character, multiple life chapters
- **IS like Crusader Kings** - generational storytelling (but within one life)

**References:**
- See `40-season-structure-spec.md` for season length details (12/24/36 weeks)
- See `1.concept/22-multi-lifetime-continuity.md` for context tracking across seasons
- See `71-daily-turn-flow-detailed.md` for turn-by-turn gameplay with v1.2 mechanics
- See `72-weekly-cycle-implementation.md` for within-season week-level flow with v1.2 tracking
- See `74-multi-season-continuity-spec.md` for memory resonance and hook persistence
- See `6.monetization/novel-generation-integration.md` for bookshelf creation
- See `master_truths_canonical_spec_v_1_2.md` Section 16 (Emotional Authenticity)
- See `master_truths_canonical_spec_v_1_2.md` Section 17 (Novel-Quality Narratives)

---

**This specification enables developers to implement the complete season-to-season flow with capacity recovery at transitions, memory consolidation, emotional state carry-over, tension arc validation, novel-quality season validation, time skips, life bookshelf, and character lifecycle management that meets Master Truths v1.2 standards.**

