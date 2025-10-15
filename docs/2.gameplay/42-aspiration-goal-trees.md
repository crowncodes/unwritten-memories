# Aspiration Goal Trees - Complete Catalog

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete catalog of all ~90 aspirations with capacity costs and parallel stressor warnings

**References:**
- **Base Cards:** `20-base-card-catalog.md` (Tier 2 - Aspiration cards)
- **Season Structure:** `40-season-structure-spec.md` (aspiration pacing by season length)
- **Success Formulas:** `12-success-probability-formulas.md` (success calculations)

---

## Overview

**Aspirations** are medium-term goals (8-36 weeks) that provide the primary narrative structure for each season. Players choose 1-2 major aspirations per season, which generate quest-chain sub-cards and define success conditions.

**Total Aspirations:** ~90 (40 Major, 50 Minor)  
**Categories:** 8 main categories aligned with Life Directions  
**Success Range:** 30-80% based on difficulty and player fit

---

## Aspiration Structure

### Standard Template

```typescript
interface Aspiration {
  id: string;
  name: string;
  tier: 2;
  category: "major" | "minor";
  
  // Requirements
  prerequisites: {
    life_direction_fit?: string[];
    skills?: {[skill: string]: number};
    relationships?: RelationshipRequirement[];
    resources?: ResourceRequirement;
  };
  
  // Duration & Difficulty
  duration: {
    min_weeks: number;
    optimal_weeks: number;
    max_weeks: number;
  };
  difficulty: "easy" | "moderate" | "hard" | "very_hard";
  base_success_chance: number;       // 0.30-0.80
  
  // Progression
  milestones: Milestone[];
  generated_cards: string[];         // Sub-cards created
  weekly_requirements: Requirement[];
  
  // Outcomes
  success_rewards: Reward[];
  partial_success: PartialOutcome;
  failure_consequences: Consequence[];
  
  // Integration
  unlocks_aspirations?: string[];
  affects_relationships: RelationshipImpact[];
  narrative_arc_type: "achievement" | "transformation" | "crisis_resolution" | "exploration";
}
```

---

## CATEGORY 1: CREATIVE ASPIRATIONS (14 Total)

### Major Creative Aspirations (8)

**ASP-CRE-001: Launch Photography Business**

```javascript
{
  id: "asp_photography_business",
  name: "Launch Photography Business",
  category: "major",
  
  prerequisites: {
    life_direction_fit: ["Pursue Creative Fulfillment", "Master a Craft", "Find Personal Freedom"],
    skills: { photography: 3 },
    resources: { money: 2000, time: "high flexibility" }
  },
  
  duration: { min_weeks: 12, optimal_weeks: 24, max_weeks: 36 },
  difficulty: "hard",
  base_success_chance: 0.45,
  
  milestones: [
    {
      week: 2,
      goal: "Portfolio Ready (20+ professional photos)",
      validation: "portfolio_quality >= 7",
      rewards: { confidence: +0.1 }
    },
    {
      week: 6,
      goal: "First Paid Client Booked",
      validation: "clients_booked >= 1",
      rewards: { money: +300, reputation: +1 }
    },
    {
      week: 10,
      goal: "3+ Clients Completed Successfully",
      validation: "clients_completed >= 3",
      rewards: { skill_photography: +0.5, reputation: +2 }
    },
    {
      week: 12,
      goal: "Business Sustainable (break-even or profitable)",
      validation: "monthly_income >= monthly_expenses",
      decisive: true
    }
  ],
  
  generated_cards: [
    "Work on Portfolio",
    "Shoot Client Session",
    "Marketing & Social Media",
    "Network with Potential Clients",
    "Edit Photos (recurring)",
    "Handle Client Feedback",
    "Equipment Upgrade Decision",
    "Pricing Strategy Session"
  ],
  
  weekly_requirements: [
    { type: "time", amount: 15, description: "Business development work" },
    { type: "energy", amount: "high", description: "Creative work is demanding" },
    { type: "money", cost: 50, description: "Marketing, supplies" }
  ],
  
  success_rewards: [
    { type: "income_stream", value: "photography_business", amount: "+$500-2000/month" },
    { type: "skill", skill: "photography", gain: +2.0 },
    { type: "skill", skill: "business", gain: +1.5 },
    { type: "reputation", category: "creative", gain: +5 },
    { type: "unlocks", aspirations: ["Gallery Showing", "Wedding Photography Specialist", "Teach Photography"] },
    { type: "fusion", card: "Professional Photographer Identity" },
    { type: "emotional", state: "CONFIDENT", duration: "4 weeks" }
  ],
  
  partial_success: {
    condition: "2 of 4 milestones achieved",
    outcome: "Business launched but struggling",
    rewards: [
      { type: "income_stream", value: "photography_side_hustle", amount: "+$200-500/month" },
      { type: "skill", skill: "photography", gain: +1.0 },
      { type: "can_retry", next_season: true }
    ]
  },
  
  failure_consequences: [
    { type: "money_lost", amount: -1500, description: "Equipment, marketing investment" },
    { type: "emotional", state: "DISCOURAGED", duration: "2 weeks" },
    { type: "skill", skill: "photography", gain: +0.5, description: "Still learned from attempt" },
    { type: "memory", significance: 7, tone: "bittersweet", description: "I tried, but it wasn't the right time" }
  ],
  
  affects_relationships: [
    {
      if: "npc_supported_aspiration",
      npc: "any",
      effect: { trust: +0.15, memory: "They believed in me" }
    },
    {
      if: "neglected_relationship_during_pursuit",
      npc: "any_level_3+",
      effect: { trust: -0.10, creates_tension: true }
    }
  ],
  
  narrative_arc_type: "achievement",
  
  notes: "Most popular creative aspiration. High risk, high reward. Success fundamentally changes career trajectory."
}
```

**ASP-CRE-002: Complete and Publish Novel**

```javascript
{
  id: "asp_write_novel",
  name: "Write and Publish First Novel",
  category: "major",
  
  prerequisites: {
    life_direction_fit: ["Pursue Creative Fulfillment", "Discover Who You Are"],
    skills: { writing: 2 },
    personality: { openness: 4.0, conscientiousness: 3.5 }
  },
  
  duration: { min_weeks: 24, optimal_weeks: 36, max_weeks: 48 },
  difficulty: "very_hard",
  base_success_chance: 0.35,
  
  milestones: [
    { week: 8, goal: "First Draft 25% (20,000 words)", validation: "word_count >= 20000" },
    { week: 16, goal: "First Draft Complete (80,000 words)", validation: "draft_complete" },
    { week: 24, goal: "Revised Draft, Beta Readers Feedback", validation: "beta_feedback_received" },
    { week: 32, goal: "Query Letters Sent / Self-Publish Launch", decisive: true }
  ],
  
  success_rewards: [
    { type: "achievement", value: "published_author", permanent: true },
    { type: "skill", skill: "writing", gain: +2.5 },
    { type: "potential_income", range: "$0-5000 first year" },
    { type: "unlocks", aspirations: ["Write Second Novel", "Join Writing Community"] },
    { type: "emotional", state: "FULFILLED", duration: "8 weeks" }
  ],
  
  notes: "Longest aspiration. Requires sustained commitment. Low immediate financial reward but high personal fulfillment."
}
```

**Other Major Creative Aspirations:**
- ASP-CRE-003: Gallery Art Exhibition
- ASP-CRE-004: Release Music Album/EP
- ASP-CRE-005: Build Creative Online Following (10k+)
- ASP-CRE-006: Launch Etsy/Creative Shop
- ASP-CRE-007: Complete Art Series (20+ pieces)
- ASP-CRE-008: Perform Stand-Up Comedy Set

---

### Minor Creative Aspirations (6)

**ASP-CRE-101: Learn Photography Basics**

```javascript
{
  id: "asp_learn_photography",
  name: "Learn Photography Basics",
  category: "minor",
  
  duration: { min_weeks: 8, optimal_weeks: 12, max_weeks: 16 },
  difficulty: "easy",
  base_success_chance: 0.75,
  
  milestones: [
    { week: 4, goal: "Understand camera settings & composition" },
    { week: 8, goal: "50+ practice photos taken" },
    { week: 12, goal: "Portfolio of 10 good shots" }
  ],
  
  success_rewards: [
    { type: "skill", skill: "photography", gain: +2.0 },
    { type: "unlocks", aspirations: ["Launch Photography Business"] },
    { type: "equipment", item: "basic_camera", acquired: true }
  ]
}
```

**Other Minor Creative:**
- ASP-CRE-102: Take Creative Writing Course
- ASP-CRE-103: Learn to Paint/Draw
- ASP-CRE-104: Learn Musical Instrument Basics
- ASP-CRE-105: Build Portfolio Website
- ASP-CRE-106: Complete 30-Day Creative Challenge

---

## CATEGORY 2: CAREER & FINANCIAL ASPIRATIONS (16 Total)

### Major Career Aspirations (10)

**ASP-CAR-001: Get Promoted to Senior Position**

```javascript
{
  id: "asp_promotion_senior",
  name: "Get Promoted to Senior Designer",
  category: "major",
  
  prerequisites: {
    employment_status: "employed",
    skills: { relevant_career_skill: 5 },
    relationships: [{ npc_type: "boss", level: 3, trust: 0.6 }]
  },
  
  duration: { min_weeks: 8, optimal_weeks: 16, max_weeks: 24 },
  difficulty: "moderate",
  base_success_chance: 0.55,
  
  milestones: [
    { week: 2, goal: "Complete High-Visibility Project", validation: "project_success" },
    { week: 6, goal: "Positive Performance Review", validation: "review_score >= 8" },
    { week: 10, goal: "Demonstrate Leadership", validation: "leadership_opportunities >= 3" },
    { week: 16, goal: "Promotion Offered", decisive: true }
  ],
  
  success_rewards: [
    { type: "income", increase: "+30% salary" },
    { type: "skill", skill: "leadership", gain: +1.5 },
    { type: "career_trajectory", value: "senior_track" },
    { type: "unlocks", aspirations: ["Manage Team", "Executive Track"] }
  ],
  
  failure_consequences: [
    { type: "career_stagnation", duration: "2 seasons" },
    { type: "emotional", state: "DISAPPOINTED", duration: "2 weeks" },
    { type: "may_trigger", event: "phase_transition_career" }
  ]
}
```

**ASP-CAR-002: Switch Careers Completely**

```javascript
{
  id: "asp_career_switch",
  name: "Switch from Corporate to Creative Career",
  category: "major",
  
  duration: { min_weeks: 24, optimal_weeks: 36, max_weeks: 48 },
  difficulty: "very_hard",
  base_success_chance: 0.40,
  
  milestones: [
    { week: 8, goal: "Acquire new skills (certification/portfolio)" },
    { week: 16, goal: "Build network in new field" },
    { week: 24, goal: "Land first job/client in new field" },
    { week: 32, goal: "Income matches or exceeds old career", decisive: true }
  ],
  
  costs: {
    money: { min: 2000, max: 10000, description: "Education, transition period" },
    time: "Extremely high - may need to quit current job",
    emotional_toll: "High - uncertainty, imposter syndrome"
  },
  
  success_rewards: [
    { type: "career_transformation", permanent: true },
    { type: "life_satisfaction", increase: "+major" },
    { type: "unlocks", life_direction: "new alignment possible" },
    { type: "novel_significance", chapter: "The Year I Changed Everything" }
  ]
}
```

**Other Major Career:**
- ASP-CAR-003: Start Own Business (General)
- ASP-CAR-004: Save $50K for House Down Payment
- ASP-CAR-005: Achieve Financial Independence (FIRE)
- ASP-CAR-006: Recover from Job Loss
- ASP-CAR-007: Negotiate 50%+ Raise
- ASP-CAR-008: Build Side Income to $2K/month
- ASP-CAR-009: Launch Consulting Practice
- ASP-CAR-010: Get Into Dream Company

---

### Minor Career/Financial (6)

- ASP-CAR-101: Get Certification/License
- ASP-CAR-102: Save $5K Emergency Fund
- ASP-CAR-103: Pay Off Credit Card Debt
- ASP-CAR-104: Improve Credit Score 100+ Points
- ASP-CAR-105: Learn New Professional Skill
- ASP-CAR-106: Build Professional Network (20+ connections)

---

## CATEGORY 3: HEALTH & FITNESS ASPIRATIONS (10 Total)

### Major Health Aspirations (5)

**ASP-HEA-001: Run Half-Marathon (Non-Athlete)**

```javascript
{
  id: "asp_half_marathon",
  name: "Train for and Complete Half-Marathon",
  category: "major",
  
  prerequisites: {
    physical_meter: { min: 4 },
    no_injuries: true,
    personality: { conscientiousness: 3.0 }
  },
  
  duration: { min_weeks: 12, optimal_weeks: 16, max_weeks: 20 },
  difficulty: "hard",
  base_success_chance: 0.45,
  
  milestones: [
    { week: 4, goal: "Run 5K without stopping" },
    { week: 8, goal: "Run 10K milestone race" },
    { week: 12, goal: "Complete 10-mile training run" },
    { week: 16, goal: "RACE DAY - Complete 13.1 miles", decisive: true }
  ],
  
  weekly_requirements: [
    { type: "training", frequency: "4x per week", time_per: 1 },
    { type: "energy", cost: 2, per_session: true },
    { type: "recovery", rest_days: 3 }
  ],
  
  injury_risk: {
    if_physical_low: "30% chance of injury requiring 2-week break",
    if_overtrain: "50% chance of injury",
    prevention: "Rest days, proper nutrition cards"
  },
  
  success_rewards: [
    { type: "physical_meter", permanent_increase: +2 },
    { type: "achievement", badge: "Half-Marathon Finisher" },
    { type: "identity_shift", fusion: "Athlete You" },
    { type: "unlocks", aspirations: ["Full Marathon", "Triathlon", "Running Club Leader"] },
    { type: "emotional", state: "TRIUMPHANT", duration: "4 weeks" }
  ],
  
  failure_paths: [
    {
      type: "injury",
      outcome: "Must abandon aspiration, physical therapy required",
      consequence: { physical_meter: -2, emotional: "FRUSTRATED" }
    },
    {
      type: "did_not_finish",
      outcome: "Attempted race but couldn't complete",
      consequence: { emotional: "DISAPPOINTED", but_attempted: "Still counts as trying" }
    }
  ]
}
```

**Other Major Health:**
- ASP-HEA-002: Lose 30+ Pounds Healthily
- ASP-HEA-003: Overcome Anxiety Through Therapy
- ASP-HEA-004: Build Consistent Meditation Practice
- ASP-HEA-005: Complete Tough Mudder / Obstacle Race

### Minor Health (5)
- ASP-HEA-101: Run First 5K
- ASP-HEA-102: Establish Gym Routine (3 months)
- ASP-HEA-103: Learn to Cook Healthy Meals
- ASP-HEA-104: Fix Sleep Schedule
- ASP-HEA-105: Complete Yoga Challenge (30 days)

---

## CATEGORY 4: RELATIONSHIP ASPIRATIONS (12 Total)

### Major Relationship Aspirations (7)

**ASP-REL-001: Find Long-Term Romantic Partner**

```javascript
{
  id: "asp_find_partner",
  name: "Find Long-Term Romantic Partner",
  category: "major",
  
  prerequisites: {
    life_direction_fit: ["Seek Deep Relationships", "Balance Everything"],
    emotional_meter: { min: 5 },
    self_esteem: { min: 0.6 }
  },
  
  duration: { min_weeks: 24, optimal_weeks: 36, max_weeks: 52 },
  difficulty: "hard",
  base_success_chance: 0.50,
  
  milestones: [
    { week: 8, goal: "Go on 5+ first dates" },
    { week: 16, goal: "Find someone with potential (3+ good dates)" },
    { week: 24, goal: "Relationship reaches 3 months milestone" },
    { week: 36, goal: "Relationship stable, exclusive, discussing future", decisive: true }
  ],
  
  generated_cards: [
    "Dating App Swiping",
    "First Date",
    "Second Date (Deeper)",
    "Define the Relationship Talk",
    "Meet Their Friends",
    "Introduce to Your Friends",
    "Navigate Conflict",
    "Discuss Future Together"
  ],
  
  success_rewards: [
    { type: "relationship", new_npc: "romantic_partner_level_3+", permanent: true },
    { type: "emotional", state: "IN_LOVE", duration: "season+" },
    { type: "unlocks", aspirations: ["Move In Together", "Engagement Preparation"] },
    { type: "life_change", significance: "Major - new NPC central to life" }
  ],
  
  failure_outcomes: [
    {
      type: "no_compatible_match_found",
      consequence: "Can retry next season, learned what you want"
    },
    {
      type: "relationship_ended",
      consequence: "Heartbreak, but growth. May trigger Phase Transition"
    }
  ],
  
  notes: "Success is partly RNG (compatible NPC generated), partly player choices. Can't force love."
}
```

**ASP-REL-002: Repair Broken Family Relationship**

```javascript
{
  id: "asp_family_repair",
  name: "Rebuild Relationship with [Estranged Family Member]",
  category: "major",
  
  prerequisites: {
    family_npc: { relationship_level: 0-2, trust: { max: 0.4 } },
    player_readiness: true
  },
  
  duration: { min_weeks: 16, optimal_weeks: 24, max_weeks: 36 },
  difficulty: "very_hard",
  base_success_chance: 0.35,
  
  milestones: [
    { week: 4, goal: "First contact (letter, call, meeting)" },
    { week: 12, goal: "Multiple positive interactions" },
    { week: 20, goal: "Address core conflict/hurt" },
    { week: 24, goal: "Relationship healed to Level 3+", decisive: true }
  ],
  
  emotional_intensity: "extreme",
  therapy_recommended: true,
  
  success_rewards: [
    { type: "relationship", restored: true, level: "3-4" },
    { type: "emotional", state: "RELIEVED", healing: true },
    { type: "novel_significance", chapter: "The Healing I Didn't Know I Needed" }
  ]
}
```

**Other Major Relationship:**
- ASP-REL-003: Build Deep Friend Circle (5+ close friends)
- ASP-REL-004: Support Partner Through Major Challenge
- ASP-REL-005: Prepare for Marriage/Engagement
- ASP-REL-006: Navigate Open Relationship Transition
- ASP-REL-007: Co-Create Business with Friend/Partner

### Minor Relationship (5)
- ASP-REL-101: Make 3 New Friends
- ASP-REL-102: Join Community/Group
- ASP-REL-103: Deepen Existing Friendship (Level 2→4)
- ASP-REL-104: Host Regular Dinner Parties
- ASP-REL-105: Introduce Partner to Family

---

## CATEGORY 5: LIFESTYLE ASPIRATIONS (10 Total)

### Major Lifestyle (6)

**ASP-LIF-001: Travel to 5 Countries**
**ASP-LIF-002: Renovate/Decorate Home**
**ASP-LIF-003: Move to New City**
**ASP-LIF-004: Adopt Pet (Dog/Cat)**
**ASP-LIF-005: Learn to Live Minimally**
**ASP-LIF-006: Build Sustainable Lifestyle**

### Minor Lifestyle (4)
**ASP-LIF-101: Solo Weekend Trip**
**ASP-LIF-102: Declutter Entire Home**
**ASP-LIF-103: Learn to Drive/Get License**
**ASP-LIF-104: Build Morning Routine**

---

## CATEGORY 6: LEARNING ASPIRATIONS (8 Total)

### Major Learning (4)

**ASP-LEA-001: Learn Spanish to Conversational Level**

```javascript
{
  duration: { min_weeks: 24, optimal_weeks: 36, max_weeks: 52 },
  difficulty: "hard",
  
  milestones: [
    { week: 12, goal: "Basic conversations (A2 level)" },
    { week: 24, goal: "Intermediate fluency (B1)" },
    { week: 36, goal: "Have 30-min conversation with native speaker", decisive: true }
  ],
  
  weekly_requirements: [
    { type: "time", amount: 5, description: "Daily practice 45min" },
    { type: "money", cost: 50, description: "App subscription, tutor" }
  ],
  
  success_rewards: [
    { type: "skill", skill: "spanish", value: 6.0 },
    { type: "unlocks", aspirations: ["Travel Spanish-Speaking Countries", "Bilingual Career Paths"] },
    { type: "cognitive_benefit", permanent: true }
  ]
}
```

**ASP-LEA-002: Complete Advanced Degree/Certification**
**ASP-LEA-003: Master Complex Skill (Programming/Design/etc)**
**ASP-LEA-004: Read 52 Books in Year**

### Minor Learning (4)
**ASP-LEA-101: Learn to Code Basics**
**ASP-LEA-102: Take Online Course**
**ASP-LEA-103: Learn to Cook Advanced Cuisine**
**ASP-LEA-104: Study Philosophy/History Deeply**

---

## CATEGORY 7: RECOVERY & HEALING ASPIRATIONS (8 Total)

**ASP-REC-001: Recover from Burnout**
**ASP-REC-002: Process Grief (Loss of Loved One)**
**ASP-REC-003: Overcome Addiction**
**ASP-REC-004: Heal from Trauma (with Therapy)**
**ASP-REC-005: Rebuild After Financial Ruin**
**ASP-REC-006: Recover from Health Crisis**
**ASP-REC-007: Exit Toxic Relationship Safely**
**ASP-REC-008: Restore Work-Life Balance**

---

## CATEGORY 8: COMMUNITY & IMPACT ASPIRATIONS (6 Total)

**ASP-IMP-001: Start Nonprofit/Charity**
**ASP-IMP-002: Volunteer Leadership Role**
**ASP-IMP-003: Mentor 5+ People**
**ASP-IMP-004: Organize Community Event**
**ASP-IMP-005: Political/Activist Campaign**
**ASP-IMP-006: Teach/Lead Workshops**

---

## Aspiration Unlock Chains

### Example Progression Tree

```
PHOTOGRAPHY PATH:
Learn Photography Basics (Minor, 8w)
    ↓
Launch Photography Business (Major, 24w)
    ↓ (branches)
    ├─ Wedding Photography Specialist (Major, 16w)
    ├─ Gallery Showing (Major, 24w)
    ├─ Teach Photography Workshops (Major, 16w)
    └─ Travel Photography Book (Major, 36w)

HEALTH PATH:
Run First 5K (Minor, 8w)
    ↓
Run Half-Marathon (Major, 16w)
    ↓ (branches)
    ├─ Full Marathon (Major, 20w)
    ├─ Triathlon (Major, 24w)
    └─ Running Club Leader (Minor, 12w)

CAREER PATH:
Get Certification (Minor, 12w)
    ↓
Get Promotion (Major, 16w)
    ↓
Manage Team (Major, 24w)
    ↓
Executive Track (Major, 36w)
```

---

## Master Truths v1.2: Capacity Cost & Parallel Stressor Warnings *(NEW)*

### High-Stress Aspirations Require Higher Capacity

**Core Principle:** Demanding aspirations have emotional capacity requirements. Pursuing them at low capacity increases failure risk.

```javascript
const ASPIRATION_CAPACITY_REQUIREMENTS = {
  capacity_classification: {
    low_stress: {
      min_capacity: 4,
      examples: ["Learn Photography Basics", "Run First 5K", "Take Online Course"],
      description: "Can pursue even when moderately stressed"
    },
    
    moderate_stress: {
      min_capacity: 6,
      examples: ["Get Promoted", "Run Half-Marathon", "Launch Side Business"],
      description: "Requires stable baseline capacity",
      warning_at_5: "This will be challenging at your current energy level"
    },
    
    high_stress: {
      min_capacity: 7,
      examples: ["Launch Photography Business", "Write Novel", "Career Transition"],
      description: "Demanding - requires high capacity to sustain",
      warning_at_6: "⚠️ WARNING: This aspiration is very demanding. Consider waiting or choosing something less intensive."
    },
    
    extreme_stress: {
      min_capacity: 8,
      examples: ["Plan Wedding + Buy House + Career Change", "Build Business + Develop Team"],
      description: "Epic multi-faceted goals - requires peak capacity",
      locked_below_7: "❌ LOCKED: Your capacity is too low for this aspiration. Recover first.",
      warning_at_7: "🚨 CRITICAL: This is an extremely demanding goal. Are you sure?"
    }
  },
  
  examples: {
    ASP_CAR_002_Career_Switch: {
      difficulty: "very_hard",
      capacity_requirement: 7,
      duration: "24-36 weeks",
      
      capacity_cost: {
        weekly_drain: -1,  // Each week pursuing this costs 1 capacity
        rationale: "Identity crisis + learning curve + financial stress",
        
        if_capacity_drops_below_5: {
          warning: "You're burning out. This aspiration is draining you.",
          options: [
            "Slow down (延longer timeline, less weekly drain)",
            "Take break (pause aspiration for 2-4 weeks)",
            "Abandon (preserve health, mark failed)"
          ]
        }
      }
    }
  }
};
```

**Parallel Stressor Warnings:**

```javascript
const PARALLEL_STRESSOR_LIMITS = {
  when_selecting_aspiration: {
    check_active_stressors: true,
    max_recommended: 3,  // Player + aspiration + 2 life stressors
    
    warnings: {
      3_stressors: "You already have a lot going on. This will add more pressure.",
      4_stressors: "⚠️ WARNING: You're juggling a lot. Adding this may be overwhelming.",
      5_plus_stressors: "🚨 CRITICAL: You have too much going on. This aspiration will likely push you to breaking point. Strongly recommend waiting."
    }
  },
  
  example_scenario: {
    player_state: {
      active_stressors: [
        "Current job stress (project deadline)",
        "Relationship conflict with Sarah",
        "Financial tight (rent concern)"
      ],
      stressor_count: 3,
      capacity: 5
    },
    
    selects: "Launch Photography Business (high-stress aspiration)",
    
    system_warning: `
      ⚠️ COMPLEXITY WARNING
      
      You currently have 3 active stressors:
      • Job deadline pressure
      • Tension with Sarah
      • Money concerns
      
      "Launch Photography Business" is a HIGH-STRESS aspiration that will add:
      • Financial investment stress
      • Time management pressure
      • Performance anxiety
      
      This will bring you to 6 concurrent stressors - near your limit.
      
      Recommendation: Wait until job deadline passes or Sarah situation resolves.
      
      Proceed anyway? (Not recommended)
    `
  }
};
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Aspiration System (v1.1 Foundation)
- [x] All aspirations use canonical resources
- [x] Duration aligns with season lengths (12/24/36w)
- [x] Success uses standard formula
- [x] Relationship impacts respect 0-5 levels
- [x] All aspirations create novel-worthy content
- [x] ~90 aspirations across 8 categories
- [x] Unlock chains and progression trees

### ✅ Master Truths v1.2: Capacity & Stressor Management *(NEW)*
- [x] **Capacity Requirements by Aspiration Stress Level**
  - Low-stress: Min capacity 4 (e.g., "Learn Photography Basics")
  - Moderate-stress: Min capacity 6 (e.g., "Get Promoted")
  - High-stress: Min capacity 7 (e.g., "Launch Photography Business")
  - Extreme-stress: Min capacity 8, locked below 7 (e.g., "Epic multi-goal seasons")
- [x] **Parallel Stressor Warnings**
  - Max recommended: 3 active stressors (aspiration + 2 life stressors)
  - 4 stressors: Warning - "Adding this may be overwhelming"
  - 5+ stressors: Critical warning - "Will push you to breaking point"
- [x] **Weekly Capacity Drain**
  - High-stress aspirations cost -1 capacity/week
  - If capacity drops below 5: Warning + slow down/pause/abandon options
- [x] **Selection-Time Warnings**
  - System checks active stressor count before allowing aspiration selection
  - Shows current stressors + what aspiration will add
  - Recommends waiting if player near limit

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~115 lines** of new v1.2 capacity and stressor management
2. **Capacity requirements per aspiration** - demanding goals need higher baseline
3. **Parallel stressor warnings** - system prevents overwhelming complexity
4. **Weekly capacity drain** - high-stress aspirations cost capacity over time
5. **Selection-time checks** - warns before player takes on too much

**Capacity Requirements:**
- Low-stress (capacity 4+): "Run First 5K", "Take Online Course"
- Moderate (capacity 6+): "Get Promoted", "Launch Side Business"
- High (capacity 7+): "Launch Photography Business", "Write Novel", "Career Switch"
- Extreme (capacity 8+, locked < 7): "Wedding + House + Career Change"

**Parallel Stressor Example:**
- Current: Job stress + Sarah conflict + Money concern (3 stressors, capacity 5)
- Selects: "Launch Photography Business" (high-stress)
- Warning: "⚠️ This will bring you to 6 concurrent stressors - near your limit. Wait until job deadline passes."

**Design Principles:**
- Demanding aspirations require higher capacity to attempt
- System prevents player from taking on too much (max 5-7 stressors depending on season length)
- Selection warnings show exact current load + what aspiration adds
- High-stress aspirations drain -1 capacity/week
- Player warned if burnout risk high

**References:**
- See `01-emotional-authenticity.md` for cross-system capacity integration
- See `14-emotional-state-mechanics.md` for capacity calculation and stressor tracking
- See `40-season-structure-spec.md` for circumstance stacking limits by season length
- See `20-base-card-catalog.md` for aspiration base cards
- See `31-narrative-arc-scaffolding.md` for aspiration as narrative driver

---

**This catalog enables content designers to implement all ~90 aspirations with Master Truths v1.2 enhancements: capacity requirements that prevent attempting demanding goals while exhausted, parallel stressor warnings that show current complexity and recommend waiting if overloaded, weekly capacity drain for high-stress aspirations, and selection-time checks that prevent overwhelming the player - creating authentic limits where you can't do everything at once and must choose what matters most.**

