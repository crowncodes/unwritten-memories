# Season Structure Specification - Implementation

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete implementation spec for 12/24/36 week season system with emotional capacity arcs and burnout tracking

**References:**
- **Design Philosophy:** `1.concept/15-progression-phases.md` (WHY seasons matter)
- **Schema Definition:** `7.schema/05-narrative-system.md` (SeasonState interface)
- **Narrative Arc:** `31-narrative-arc-scaffolding.md` (3-act structure)
- **Decision Templates:** `30-decisive-decision-templates.md` (decisive moments)

---

## Overview

**Seasons** are complete 3-act story arcs that structure gameplay into meaningful chapters. Players choose season length (**12, 24, or 36 weeks**) at season start based on their aspiration and desired story depth.

**Core Principle:** Fixed lengths enable content balancing while player choice provides narrative flexibility. Content density adjusts to match chosen length.

**Multi-Season Context:** Each season is ONE CHAPTER in a character's life story. Characters persist across **8-10 seasons** (Life Bookshelf), with all relationships, skills, and memories carrying forward. See `73-season-flow-implementation.md` for complete multi-season system.

**Compliance:** master_truths v1.1 specifies "Season: 12, 24, or 36 weeks (player selects at season start based on aspiration complexity and desired depth)"

---

## Season Length Options

### The Three Lengths

```typescript
type SeasonLength = 12 | 24 | 36;

interface SeasonChoice {
  length: SeasonLength;
  display_name: "Standard" | "Extended" | "Epic";
  aspiration_complexity: "simple" | "moderate" | "complex";
  recommended_for: string[];
  story_type: "focused" | "layered" | "saga";
}
```

---

### Standard Season (12 Weeks)

**Duration:** 12 weeks (3 months)  
**Turns:** 252 turns (12 weeks × 7 days × 3 turns/day)  
**Story Type:** Focused single-goal arc

**Best For:**
- Simple, focused aspirations ("Learn to cook Italian food")
- Single-relationship deepening
- Skill acquisition (one skill to Level 5)
- Career milestone (get promotion)
- Clear win condition

**Story Structure:**
```javascript
const STANDARD_SEASON_STRUCTURE = {
  act_1_setup: {
    weeks: "1-3",
    turns: 63,
    goals: [
      "Establish aspiration",
      "Introduce key NPCs (1-2)",
      "Set up routine",
      "Plant first seeds"
    ]
  },
  
  act_2_complications: {
    weeks: "4-9",
    turns: 126,
    goals: [
      "2-3 complications",
      "1-2 decisive decisions",
      "Midpoint crisis or opportunity",
      "Relationship development"
    ]
  },
  
  act_3_resolution: {
    weeks: "10-12",
    turns: 63,
    goals: [
      "Climax decision",
      "Resolution of main arc",
      "Consequences play out",
      "Setup next season"
    ]
  }
};
```

**Content Density:**
```javascript
{
  routine_batching: "heavy",           // 3-4 day batches common
  event_frequency: "focused",          // 1-2 major events
  decisive_decisions: 2,               // Exactly 2 major decisions
  complications: "2-3",
  npc_count: "2-4 primary NPCs",
  subplot_count: 0,                    // No subplots - single focus
  
  pacing: {
    weeks_1_3: "gentle",               // Learning the ropes
    weeks_4_6: "steady",               // Building momentum
    weeks_7_9: "intense",              // Main push
    weeks_10_12: "climactic"           // Resolution sprint
  }
}
```

**Novel Generation:**
- **Output:** Short story (8,000-12,000 words)
- **Chapters:** 3 chapters (one per act)
- **Style:** Tight, focused narrative

**Example Standard Aspirations:**
- "Open Etsy Shop" (single business goal)
- "Run First 5K" (fitness milestone)
- "Learn Spanish Basics" (language goal)
- "Plan Perfect Anniversary" (relationship event)
- "Get Promoted to Senior Designer" (career step)

---

### Extended Season (24 Weeks)

**Duration:** 24 weeks (6 months)  
**Turns:** 504 turns (24 weeks × 7 days × 3 turns/day)  
**Story Type:** Complex multi-path arc

**Best For:**
- Moderate complexity aspirations ("Start photography business")
- Multiple relationship arcs (2-3 NPCs)
- Career transition (change fields)
- Complex skill development (2-3 skills to Level 5)
- Competing priorities

**Story Structure:**
```javascript
const EXTENDED_SEASON_STRUCTURE = {
  act_1_setup: {
    weeks: "1-6",
    turns: 126,
    goals: [
      "Establish main aspiration + 1 subplot",
      "Introduce key NPCs (3-5)",
      "Set up routines and constraints",
      "Plant multiple seeds"
    ]
  },
  
  act_2_complications: {
    weeks: "7-18",
    turns: 252,
    goals: [
      "4-6 complications",
      "2-4 decisive decisions",
      "Midpoint crisis (major)",
      "Competing priorities emerge",
      "Relationship conflicts/deepening",
      "Skill progression challenges"
    ]
  },
  
  act_3_resolution: {
    weeks: "19-24",
    turns: 126,
    goals: [
      "Multiple climax decisions",
      "Main arc + subplot resolution",
      "Long-term consequences",
      "Character growth evident",
      "Setup next season or phase"
    ]
  }
};
```

**Content Density:**
```javascript
{
  routine_batching: "moderate",        // 2-3 day batches
  event_frequency: "rich",             // 3-5 major events
  decisive_decisions: "3-4",           // Multiple major decisions
  complications: "4-6",
  npc_count: "4-6 primary NPCs",
  subplot_count: 1,                    // One subplot alongside main
  
  pacing: {
    weeks_1_6: "exploratory",          // Wide possibilities
    weeks_7_12: "building",            // Momentum gathering
    weeks_13_18: "intense",            // Multiple conflicts
    weeks_19_24: "climactic_extended"  // Extended resolution
  }
}
```

**Novel Generation:**
- **Output:** Novella (20,000-35,000 words)
- **Chapters:** 8-12 chapters (multiple per act)
- **Style:** Layered narrative with subplots

**Example Extended Aspirations:**
- "Launch Photography Business" (business + skill + marketing)
- "Navigate Relationship Crisis" (multiple relationship arcs)
- "Career Change to UX Design" (education + networking + job hunt)
- "Train for Half Marathon + Improve Diet" (dual health goals)
- "Write and Publish Novel" (creative + business goal)

---

### Epic Season (36 Weeks)

**Duration:** 36 weeks (9 months)  
**Turns:** 756 turns (36 weeks × 7 days × 3 turns/day)  
**Story Type:** Transformational saga

**Best For:**
- Complex multi-faceted aspirations ("Build sustainable lifestyle")
- Major life transitions (marriage planning + career change)
- Multiple deep relationships (3-5 NPCs)
- Comprehensive transformation (personality evolution)
- Multi-stage goals with dependencies

**Story Structure:**
```javascript
const EPIC_SEASON_STRUCTURE = {
  act_1_setup: {
    weeks: "1-9",
    turns: 189,
    goals: [
      "Establish main aspiration + 2 subplots",
      "Introduce extensive cast (5-8 NPCs)",
      "Complex routine establishment",
      "Multiple threads planted",
      "World-building"
    ]
  },
  
  act_2_complications: {
    weeks: "10-27",
    turns: 378,
    goals: [
      "6-10 complications",
      "4-6 decisive decisions",
      "Multiple midpoint crises",
      "Cascading consequences",
      "Deep relationship development",
      "Personality evolution visible",
      "Multiple competing arcs"
    ]
  },
  
  act_3_resolution: {
    weeks: "28-36",
    turns: 189,
    goals: [
      "Epic climax decision",
      "Multiple arc resolutions",
      "Character transformation evident",
      "Long-term legacy established",
      "Major life change",
      "Phase transition possible"
    ]
  }
};
```

**Content Density:**
```javascript
{
  routine_batching: "light",           // 1-2 day batches (more granular)
  event_frequency: "saga",             // 6-10 major events
  decisive_decisions: "5-7",           // Many major decisions
  complications: "8-12",
  npc_count: "6-10 primary NPCs",
  subplot_count: "2-3",                // Multiple subplots
  
  pacing: {
    weeks_1_9: "epic_setup",           // Extensive world-building
    weeks_10_18: "rising_action",      // Multiple threads developing
    weeks_19_27: "peak_intensity",     // Maximum complexity
    weeks_28_36: "grand_resolution"    // Satisfying wrap-up
  },
  
  special_features: {
    personality_evolution: true,       // Character changes significantly
    phase_transition: "possible",      // May trigger new phase
    legacy_building: true,             // Long-term impact
    transformational: true
  }
}
```

**Novel Generation:**
- **Output:** Novel (40,000-60,000 words)
- **Chapters:** 15-20 chapters
- **Style:** Epic saga with multiple threads

**Example Epic Aspirations:**
- "Plan Wedding + Buy House + Career Transition" (life overhaul)
- "Build Sustainable Business + Develop Team" (entrepreneurship saga)
- "Overcome Anxiety + Build Social Network + Find Purpose" (personal transformation)
- "Master Craft + Compete Professionally + Build Reputation" (mastery journey)
- "Navigate Polyamorous Relationships + Self-Discovery" (complex relationship saga)

---

## Season Selection Process

### Player Choice Interface

**When:** At the start of each new season (after character creation or previous season end)

```javascript
interface SeasonSelectionUI {
  aspiration: Aspiration;              // Already chosen
  
  season_length_options: [
    {
      length: 12,
      label: "Standard (12 weeks)",
      subtitle: "Fast-paced, focused story",
      best_for: "Single focused goal",
      time_commitment: "~15-20 hours gameplay",
      difficulty: "Easier to complete",
      example_outcomes: [
        "Launch Etsy shop with 10 sales",
        "Get promoted at work",
        "Learn Italian cooking basics"
      ]
    },
    {
      length: 24,
      label: "Extended (24 weeks)",
      subtitle: "Deeper development, complications",
      best_for: "Complex goal + life balance",
      time_commitment: "~30-40 hours gameplay",
      difficulty: "Moderate - requires planning",
      example_outcomes: [
        "Start photography business + 5 clients",
        "Navigate relationship crisis + rebuild trust",
        "Career transition with network building"
      ]
    },
    {
      length: 36,
      label: "Epic (36 weeks)",
      subtitle: "Multi-arc saga, major life changes",
      best_for: "Transformational journey",
      time_commitment: "~45-60 hours gameplay",
      difficulty: "Challenging - many moving parts",
      example_outcomes: [
        "Plan wedding + buy house + career change",
        "Build business + develop team + market presence",
        "Personal transformation + new identity"
      ]
    }
  ],
  
  recommendation: {
    based_on: [
      "aspiration_complexity",
      "player_history",
      "available_time"
    ],
    suggested_length: 24,
    reason: "This aspiration involves multiple skills and relationships - Extended gives room to develop both without feeling rushed."
  },
  
  can_change: false,                   // Once chosen, locked in
  early_completion: true,              // But can end early if goal achieved
  abandonment: true                    // Or abandon if impossible
}
```

---

## Content Scaling System

### How Content Adapts to Length

```javascript
function generateSeasonContent(aspiration, seasonLength) {
  const baseComplexity = aspiration.complexity_score; // 1.0-10.0
  
  // Calculate content density
  const contentDensity = {
    12: {
      routine_batch_size: 3,           // Batch 3 days at a time
      events_per_week: 0.5,            // 1 event every 2 weeks
      decision_frequency: 6,           // 1 decisive decision every 6 weeks
      complication_rate: 0.25,         // 1 complication every 4 weeks
      npc_interaction_frequency: 0.8   // 80% of possible interactions
    },
    24: {
      routine_batch_size: 2,
      events_per_week: 0.75,           // 3 events per month
      decision_frequency: 6,           // 1 decisive decision every 6 weeks (4 total)
      complication_rate: 0.4,          // ~1 complication every 2.5 weeks
      npc_interaction_frequency: 0.9
    },
    36: {
      routine_batch_size: 1,           // More granular
      events_per_week: 1.0,            // 1 event per week
      decision_frequency: 6,           // 1 decisive decision every 6 weeks (6 total)
      complication_rate: 0.5,          // ~1 complication every 2 weeks
      npc_interaction_frequency: 1.0   // All possible interactions
    }
  }[seasonLength];
  
  // Generate season plan
  return {
    total_weeks: seasonLength,
    total_turns: seasonLength * 21,  // 7 days × 3 turns
    
    act_structure: calculateActStructure(seasonLength),
    event_schedule: generateEventSchedule(contentDensity, seasonLength),
    decision_points: generateDecisionPoints(contentDensity, seasonLength, aspiration),
    complication_schedule: generateComplications(contentDensity, seasonLength),
    
    npc_arc_plans: generateNPCArcs(aspiration.involved_npcs, seasonLength),
    skill_progression_plan: generateSkillPlan(aspiration.required_skills, seasonLength),
    
    early_completion_threshold: seasonLength * 0.75  // Can complete after 75% if goal met
  };
}
```

---

## Act Structure by Length

### Standard (12 Weeks) - 3-Act Simple

```
ACT I: SETUP (Weeks 1-3)
├─ Week 1: Aspiration selection + character setup
├─ Week 2: First steps + routine establishment
└─ Week 3: First complication emerges

ACT II: COMPLICATIONS (Weeks 4-9)
├─ Week 4-5: Complication #1 develops
├─ Week 6: DECISIVE DECISION #1 (midpoint)
├─ Week 7-8: Complication #2 + consequences
└─ Week 9: Crisis point

ACT III: RESOLUTION (Weeks 10-12)
├─ Week 10-11: DECISIVE DECISION #2 (climax)
└─ Week 12: Resolution + season wrap

PACING: Fast, tight, focused
DECISION COUNT: 2 major decisions
COMPLICATION COUNT: 2-3
```

### Extended (24 Weeks) - 3-Act Layered

```
ACT I: SETUP (Weeks 1-6)
├─ Week 1-2: Aspiration + routine + cast intro
├─ Week 3-4: Multiple threads planted
├─ Week 5-6: First complications + subplot intro

ACT II: COMPLICATIONS (Weeks 7-18)
├─ Week 7-9: Complication #1-2 develop
├─ Week 10-12: DECISIVE DECISION #1 (early midpoint)
├─ Week 13-15: Consequences + Complication #3-4
├─ Week 16-18: DECISIVE DECISION #2 (late midpoint) + Crisis

ACT III: RESOLUTION (Weeks 19-24)
├─ Week 19-21: DECISIVE DECISION #3 (climax)
├─ Week 22-23: Multiple thread resolution
└─ Week 24: Epilogue + setup

PACING: Steady build with breathing room
DECISION COUNT: 3-4 major decisions
COMPLICATION COUNT: 4-6
```

### Epic (36 Weeks) - 3-Act Saga

```
ACT I: SETUP (Weeks 1-9)
├─ Week 1-3: Aspiration + world-building + extensive cast
├─ Week 4-6: Multiple threads + subplots planted
├─ Week 7-9: Early complications + character establishment

ACT II: COMPLICATIONS (Weeks 10-27)
├─ Week 10-13: Complication #1-2 + subplot development
├─ Week 14-16: DECISIVE DECISION #1 (early midpoint)
├─ Week 17-20: Consequences + Complication #3-5
├─ Week 21-23: DECISIVE DECISION #2 (middle midpoint)
├─ Week 24-27: Major crisis + DECISIVE DECISION #3 (late midpoint)

ACT III: RESOLUTION (Weeks 28-36)
├─ Week 28-31: DECISIVE DECISION #4-5 (dual climaxes)
├─ Week 32-34: Multiple arc resolutions
├─ Week 35-36: Transformation evident + legacy + setup

PACING: Epic scope with room to breathe
DECISION COUNT: 5-7 major decisions
COMPLICATION COUNT: 8-12
```

---

## Early Completion System

### Can End Season Early

```javascript
interface EarlyCompletionCheck {
  minimum_weeks_elapsed: number;       // 75% of chosen length
  aspiration_complete: boolean;        // Goal achieved
  major_arcs_resolved: boolean;        // No loose threads
  player_initiated: boolean;           // Player must choose to end
  
  consequences: {
    novel_generation: "shorter",       // Novel will be shorter than expected
    xp_bonus: number,                  // Bonus for early completion
    efficiency_achievement: boolean,   // "Ahead of Schedule" achievement
    remaining_weeks_banked: false      // Can't save weeks for next season
  };
}

// Example
const earlyCompletionExample = {
  chosen_length: 24,
  weeks_elapsed: 19,
  aspiration_status: "COMPLETE",
  
  check: {
    minimum_met: true,                 // 19 > 18 (75% of 24)
    goal_achieved: true,
    player_wants_to_end: true
  },
  
  result: {
    season_ends_at_week: 19,
    novel_length: "~25,000 words",     // Shorter than full 24w novel
    achievement: "Ahead of Schedule",
    next_season_unlocked: true
  }
};
```

---

## Season Abandonment

### Can Abandon If Impossible

```javascript
interface SeasonAbandonment {
  trigger: "aspiration_impossible" | "player_choice" | "life_crisis";
  minimum_weeks_before_abandon: 4;     // Must play at least 4 weeks
  
  consequences: {
    aspiration_marked_failed: true,
    emotional_impact: -3,              // Significant emotional hit
    memory_persists: true,             // Failure remembered
    novel_generated: "abandoned_arc",   // Shorter "failed attempt" narrative
    next_season_affected: true,        // Starts in DISCOURAGED state
    
    no_penalty: {
      xp: "full_for_weeks_played",     // Don't penalize XP
      relationships: "maintained",      // Relationships don't decay
      skills: "retained"                // Skills don't regress
    }
  };
}
```

---

## What Happens After a Season Ends?

**After completing a season (week 12/24/36 or early completion):**

```
SEASON COMPLETE
↓
NOVEL GENERATION (2-3 min background process)
├─ 8k-60k words generated
├─ Added to character's Life Bookshelf
└─ Season archived

↓
PLAYER CHOICE
├─ [Continue to Next Season] → Choose new aspiration + time skip
├─ [Retire Character] → Archive bookshelf, start new character
└─ [View Archive] → Read completed novels

↓ If continuing...
INTER-SEASON TRANSITION
├─ Select new aspiration
├─ Time skip (1 week to 10+ years)
├─ Auto-generated narrative for time skip
├─ All progress carries forward (relationships, skills, memories)
└─ New season begins (Season N+1)
```

**Season Limits:**
- Base: **8 seasons per character** (120k words typical)
- Premium: **+2 seasons** (500 Essence, max 10 total)
- At limit: Character MUST be retired

**Complete details:** See `73-season-flow-implementation.md` for full inter-season flow, time skip mechanics, Life Bookshelf system, and character retirement.

---

## Master Truths v1.2: Emotional Capacity Arcs by Season Length *(NEW)*

### Capacity Fluctuates Throughout Season

**Core Principle:** Player emotional capacity naturally fluctuates across the season arc. Longer seasons have more dramatic capacity arcs with higher burnout risk.

```javascript
const CAPACITY_ARCS_BY_SEASON_LENGTH = {
  standard_12_week: {
    typical_capacity_arc: {
      weeks_1_3: { capacity: 7-8, state: "Fresh start, excited, high energy" },
      weeks_4_6: { capacity: 6-7, state: "Steady work, managing well" },
      weeks_7_9: { capacity: 5-6, state: "Push phase, some fatigue building" },
      weeks_10_12: { capacity: 6-7, state: "Final sprint, end in sight provides boost" },
      
      risk_profile: "LOW - Short enough to push through without burnout",
      burnout_risk: "10-15%",
      
      if_player_overworks: {
        weeks_7_9: { capacity: 3-4, state: "Exhaustion setting in" },
        weeks_10_12: { capacity: 2-3, state: "May collapse during final push" }
      }
    }
  },
  
  extended_24_week: {
    typical_capacity_arc: {
      weeks_1_6: { capacity: 7-8, state: "Strong start, building momentum" },
      weeks_7_12: { capacity: 6-7, state: "Sustained effort, some fatigue" },
      weeks_13_18: { capacity: 5-6, state: "Midpoint slump - 'When will this end?'" },
      weeks_19_24: { capacity: 4-6, state: "Varies - either rallying or breaking" },
      
      risk_profile: "MODERATE - Long enough that rest breaks are mandatory",
      burnout_risk: "30-40%",
      
      critical_rest_windows: [
        { week: 8, reason: "Before midpoint push" },
        { week: 16, reason: "After major complication" }
      ],
      
      if_player_overworks: {
        weeks_13_18: { capacity: 3-4, state: "Serious exhaustion, mistakes increasing" },
        weeks_19_24: { capacity: 1-3, state: "HIGH BURNOUT RISK - may trigger crisis" }
      }
    }
  },
  
  epic_36_week: {
    typical_capacity_arc: {
      weeks_1_9: { capacity: 7-8, state: "Epic scope, big ambitions, motivated" },
      weeks_10_18: { capacity: 6-7, state: "Long haul reality setting in" },
      weeks_19_27: { capacity: 5-6, state: "Exhaustion accumulating, 'So much left'" },
      weeks_28_36: { capacity: 4-7, state: "Either second wind or complete burnout" },
      
      risk_profile: "HIGH - Marathon not sprint, burnout almost guaranteed without management",
      burnout_risk: "60-75%",
      
      mandatory_rest_weeks: [
        { week: 9, reason: "End of Act 1 recovery" },
        { week: 18, reason: "Midpoint crisis recovery" },
        { week: 27, reason: "Pre-climax recovery" }
      ],
      
      if_player_overworks: {
        weeks_19_27: { capacity: 2-4, state: "Severe burnout, performance declining" },
        weeks_28_36: { capacity: 1-2, state: "CRISIS - may force season abandonment" }
      }
    }
  }
};
```

**Capacity Recovery Opportunities:**

```javascript
const SEASON_CAPACITY_MANAGEMENT = {
  natural_recovery_points: {
    season_12_week: [
      { week: 6, event: "Midpoint break", recovery: +1 },
      { week: 12, event: "Season complete", full_recovery: true }
    ],
    
    season_24_week: [
      { week: 6, event: "Act 1 complete", recovery: +1 },
      { week: 12, event: "Midpoint check-in", recovery: +1 },
      { week: 18, event: "Crisis resolved", recovery: +2 },
      { week: 24, event: "Season complete", full_recovery: true }
    ],
    
    season_36_week: [
      { week: 9, event: "Act 1 complete", recovery: +1 },
      { week: 18, event: "Midpoint milestone", recovery: +1 },
      { week: 27, event: "Act 2 complete", recovery: +2 },
      { week: 36, event: "Season complete", full_recovery: true }
    ]
  },
  
  player_agency: {
    can_rest_early: true,
    cost: "Slower aspiration progress",
    benefit: "Prevents burnout, maintains quality of life",
    
    warning_system: {
      capacity_5: "You're getting tired. Consider slowing down.",
      capacity_3: "⚠️ WARNING: You're exhausted. Rest soon or face consequences.",
      capacity_1: "🚨 CRITICAL: Burnout imminent. Rest immediately or crisis will occur."
    }
  }
};
```

---

## Master Truths v1.2: Circumstance Stacking Progression *(NEW)*

### Stressors Accumulate Over Season

**Core Principle:** As season progresses, active stressors tend to accumulate. Each new complication adds to the stack.

```javascript
const CIRCUMSTANCE_STACKING_BY_SEASON = {
  standard_12_week: {
    max_concurrent_stressors: 3,
    typical_progression: {
      weeks_1_3: { stressors: 1, example: "New aspiration challenge" },
      weeks_4_6: { stressors: 2, example: "Aspiration + relationship tension" },
      weeks_7_9: { stressors: 2-3, example: "Aspiration + relationship + financial concern" },
      weeks_10_12: { stressors: 2-3, example: "Climax - multiple stakes at once" }
    },
    
    stacking_limit: "System prevents more than 3 active for Standard season",
    rationale: "Too short for overwhelming complexity"
  },
  
  extended_24_week: {
    max_concurrent_stressors: 5,
    typical_progression: {
      weeks_1_6: { stressors: 1-2, example: "Setting up challenges" },
      weeks_7_12: { stressors: 3, example: "Multiple threads developing" },
      weeks_13_18: { stressors: 4-5, example: "Peak complexity - everything at once" },
      weeks_19_24: { stressors: 3-4, example: "Resolution phase - some resolve, some intensify" }
    },
    
    peak_intensity: "Weeks 13-18 designed to feel overwhelming",
    player_feels: "I'm juggling too much - something has to give"
  },
  
  epic_36_week: {
    max_concurrent_stressors: 7,
    typical_progression: {
      weeks_1_9: { stressors: 2-3, example: "Multiple aspirations + life areas" },
      weeks_10_18: { stressors: 4-5, example: "Complexity building" },
      weeks_19_27: { stressors: 5-7, example: "PEAK - everything happening at once" },
      weeks_28_36: { stressors: 3-5, example: "Resolution - systematic cleanup" }
    },
    
    peak_intensity: "Weeks 19-27 are THE GAUNTLET",
    player_feels: "Life is completely overwhelming. This is too much.",
    
    design_intent: "Epic seasons should feel EPIC - testing player's limits"
  }
};
```

**Stressor Management:**

```javascript
const STRESSOR_ACCUMULATION = {
  how_stressors_stack: {
    stressor_1: { capacity_cost: -1, manageable: true },
    stressor_2: { capacity_cost: -1.5, getting_hard: true },
    stressor_3: { capacity_cost: -2, challenging: true },
    stressor_4: { capacity_cost: -2.5, very_difficult: true },
    stressor_5: { capacity_cost: -3, overwhelming: true },
    stressor_6plus: { capacity_cost: -4, breaking_point: "Crisis likely" }
  },
  
  example_36_week_stacking: {
    week_0: { capacity: 8, stressors: 0, state: "Fresh" },
    week_10: { capacity: 7, stressors: 2, state: "Managing: Aspiration + Job stress" },
    week_15: { capacity: 6, stressors: 3, state: "Challenging: + Relationship conflict" },
    week_20: { capacity: 4, stressors: 5, state: "Struggling: + Health declining + Financial worry" },
    week_25: { capacity: 2, stressors: 6, state: "Breaking: + Friend needs support too" },
    week_30: { capacity: 3, stressors: 4, state: "Some resolved, still exhausted" }
  }
};
```

---

## Master Truths v1.2: Burnout Accumulation Tracking *(NEW)*

### Burnout Builds Over Time Without Rest

**Core Principle:** Each week working at low capacity increases burnout accumulation. High burnout changes ending options.

```javascript
const BURNOUT_TRACKING_SYSTEM = {
  burnout_meter: {
    range: "0-100",
    threshold_effects: {
      0_25: "Healthy - no burnout",
      26_50: "Mild fatigue - recoverable with rest",
      51_75: "Moderate burnout - performance declining",
      76_100: "Severe burnout - crisis imminent"
    }
  },
  
  accumulation_rate: {
    working_at_capacity_8plus: 0,  // No burnout accumulation
    working_at_capacity_6_7: "+2 per week",
    working_at_capacity_4_5: "+5 per week",
    working_at_capacity_2_3: "+10 per week",
    working_at_capacity_0_1: "+20 per week"
  },
  
  recovery_rate: {
    rest_week: "-15 burnout",
    normal_capacity_8: "-5 per week",
    therapy: "-10 additional per week"
  },
  
  season_end_consequences: {
    burnout_0_25: {
      outcome: "Healthy completion",
      next_season_start: "Full capacity (8)",
      no_penalties: true
    },
    
    burnout_26_50: {
      outcome: "Tired but functional",
      next_season_start: "Reduced capacity (6)",
      recovery_time: "2-4 weeks"
    },
    
    burnout_51_75: {
      outcome: "Burnout evident in season ending",
      next_season_start: "Low capacity (4)",
      forced_recovery: "Must take 4-week break before new aspiration",
      narrative: "You achieved your goal... but at what cost?"
    },
    
    burnout_76_100: {
      outcome: "SEVERE - May force season ending early",
      options: [
        "Abandon aspiration to recover",
        "Push through (50% chance of health crisis)",
        "Take 4-week recovery mid-season"
      ],
      next_season_impossible: "Cannot start new season until burnout < 50",
      permanent_effects: "High burnout leaves scars"
    }
  }
};
```

**Example Burnout Progression (36-week season):**

```javascript
const BURNOUT_EXAMPLE = {
  weeks_1_10: {
    capacity: 7-8,
    burnout: 0,
    state: "Healthy, sustainable"
  },
  
  weeks_11_20: {
    capacity: 5-6,
    burnout: 20,  // +2/week × 10 weeks
    state: "Mild fatigue, still fine"
  },
  
  weeks_21_28: {
    capacity: 3-4,
    burnout: 60,  // +5/week × 8 weeks
    state: "MODERATE BURNOUT - performance declining",
    warning: "⚠️ You're burning out. Rest or face consequences."
  },
  
  weeks_29_32: {
    capacity: 2,
    burnout: 100,  // +10/week × 4 weeks
    state: "SEVERE BURNOUT - crisis triggered",
    
    forced_event: {
      title: "The Breaking Point",
      narrative: `
        You can't do this anymore. You physically cannot.
        
        32 weeks of pushing. 32 weeks of "just a bit more."
        32 weeks of ignoring every signal your body sent.
        
        Something has to give. Either you stop, or your body stops you.
      `,
      
      options: [
        "Take immediate 4-week medical leave (lose progress, recover)",
        "Push to finish (collapse likely, health crisis guaranteed)",
        "Abandon season (preserve health, mark aspiration failed)"
      ]
    }
  }
};
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Season System (v1.1 Foundation)
- [x] Season lengths: 12, 24, or 36 weeks (player choice at season start)
- [x] Players can end seasons early if goals complete ahead of schedule
- [x] Each season is complete 3-act arc
- [x] Decisive decisions pause time (no real-time pressure)
- [x] Season selection is meaningful choice with clear tradeoffs
- [x] Characters persist across 8-10 seasons (Life Bookshelf)
- [x] Content density adjusts to season length
- [x] Early completion and abandonment systems

### ✅ Master Truths v1.2: Capacity & Burnout Tracking *(NEW)*
- [x] **Emotional Capacity Arcs by Season Length**
  - 12-week: Capacity 7-8 → 6-7 → 5-6 → 6-7 (LOW burnout risk: 10-15%)
  - 24-week: Capacity 7-8 → 6-7 → 5-6 → 4-6 (MODERATE risk: 30-40%)
  - 36-week: Capacity 7-8 → 6-7 → 5-6 → 4-7 (HIGH risk: 60-75%)
- [x] **Natural Capacity Recovery Points**
  - 12-week: Week 6 (+1), Week 12 (full recovery)
  - 24-week: Weeks 6, 12, 18, 24 (incremental recovery)
  - 36-week: Weeks 9, 18, 27, 36 (mandatory rest windows)
- [x] **Circumstance Stacking Progression**
  - 12-week: Max 3 concurrent stressors
  - 24-week: Max 5 concurrent stressors (peak weeks 13-18)
  - 36-week: Max 7 concurrent stressors (weeks 19-27 "THE GAUNTLET")
- [x] **Burnout Accumulation System (0-100 meter)**
  - Capacity 8+: No burnout accumulation
  - Capacity 6-7: +2 burnout/week
  - Capacity 4-5: +5 burnout/week
  - Capacity 2-3: +10 burnout/week
  - Capacity 0-1: +20 burnout/week
- [x] **Season End Consequences by Burnout**
  - 0-25: Healthy completion, next season start at capacity 8
  - 26-50: Tired but functional, start at capacity 6
  - 51-75: Burnout evident, forced 4-week recovery, start at capacity 4
  - 76-100: SEVERE - may force abandonment, cannot start new season until < 50

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~310 lines** of new v1.2 capacity and burnout mechanics
2. **Capacity arcs per season length** - longer seasons = higher burnout risk
3. **Circumstance stacking progression** - stressors accumulate, max varies by season
4. **Burnout tracking (0-100)** - accumulates faster at low capacity
5. **Season end burnout consequences** - affects next season starting capacity
6. **Warning systems** - capacity 5, 3, 1 trigger escalating warnings

**Capacity Arc Examples:**
- 12-week Standard: "Short enough to push through" - 10-15% burnout risk
- 24-week Extended: "Rest breaks mandatory" - 30-40% burnout risk, critical windows weeks 8, 16
- 36-week Epic: "Marathon not sprint" - 60-75% burnout risk, weeks 19-27 are "THE GAUNTLET"

**Circumstance Stacking:**
- 12-week: Max 3 stressors ("Too short for overwhelming complexity")
- 24-week: Max 5 stressors (Weeks 13-18 "Peak complexity - everything at once")
- 36-week: Max 7 stressors (Weeks 19-27 "Life is completely overwhelming")

**Burnout Accumulation:**
- Working at capacity 8: 0 burnout/week (sustainable)
- Working at capacity 6: +2 burnout/week (mild fatigue)
- Working at capacity 4: +5 burnout/week (moderate burnout)
- Working at capacity 2: +10 burnout/week (severe burnout)
- Working at capacity 0: +20 burnout/week (critical)

**Season End Examples:**
- Burnout 20: "Healthy! Full recovery. Start next season at capacity 8."
- Burnout 45: "Tired. Start next season at capacity 6. Need 2-4 week recovery."
- Burnout 65: "Burnout evident. Forced 4-week break. Start at capacity 4. 'You achieved your goal... but at what cost?'"
- Burnout 95: "SEVERE. Options: Abandon / Push (50% health crisis) / Take medical leave. Cannot start new season until burnout < 50."

**Design Principles:**
- Longer seasons = exponentially higher burnout risk
- Epic (36w) seasons are marathons requiring rest management
- Circumstance stacking peaks mid-season for maximum drama
- Burnout has lasting consequences (affects next season)
- Player warned before crisis (capacity 5 → 3 → 1 warnings)
- High burnout may force season abandonment or health crisis

**References:**
- See `01-emotional-authenticity.md` for cross-system capacity integration
- See `14-emotional-state-mechanics.md` for capacity calculation and circumstance stacking rules
- See `30-decisive-decision-templates.md` for decision scaffolding with capacity gating
- See `31-narrative-arc-scaffolding.md` for 3-act structure details with capacity considerations
- See `73-season-flow-implementation.md` for inter-season transitions and multi-season flow
- See `1.concept/15-progression-phases.md` for philosophy

---

**This specification enables developers to implement the complete season system with Master Truths v1.2 enhancements: emotional capacity arcs that vary dramatically by season length (12w low risk vs 36w high risk), circumstance stacking progression where stressors accumulate to peak mid-season, burnout tracking (0-100 meter) that accumulates faster at low capacity with lasting consequences for future seasons, and season-ending outcomes that reflect the toll of pushing too hard - creating authentic long-term consequences where achieving goals at the cost of health affects the player's next chapter.**

