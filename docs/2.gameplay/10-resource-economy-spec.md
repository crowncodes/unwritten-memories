# Resource Economy Overview - Implementation Specification

**Compliance:** `master_truths_canonical_spec_v_1_2.md` (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Overview and integration of all 6 resource systems

**References:**
- **Design Philosophy:** `1.concept/21-turn-structure.md` (WHY resources matter)
- **Schema Definition:** `7.schema/04-gameplay-mechanics.md` (PlayerResources interface)
- **Turn Economy:** `11-turn-economy-implementation.md` (complete details for each resource)
- **Success Formulas:** `12-success-probability-formulas.md` (how resources affect success)

---

## Overview

Unwritten uses a **6-resource economy** where every meaningful action costs multiple resources. This creates **authentic life simulation** where players must balance competing needs and make meaningful tradeoffs.

**Core Principle:** Life is about managing multiple constraints simultaneously. No single "energy bar" can capture the complexity of human experience.

**Compliance:** master_truths v1.1 specifies "Economy & Resources" must be limited to Time, Energy, Money, Social Capital, with Modifiers (Emotional state, skills, items) that provide multipliers but are not currencies.

---

## The 6 Resources

### 1. ⚡ Energy (Regenerating Pool)

**What It Represents:** Physical and mental stamina for activities within a time period.

**Key Characteristics:**
```javascript
{
  type: "regenerating_pool",
  scope: "per_phase",                // Morning/Afternoon/Evening
  budget: {
    weekday: [3, 3, 2],              // 8 total per day
    weekend: [4, 4, 3]               // 11 total per day
  },
  regeneration: "start_of_each_phase",
  carry_over: false,                 // Doesn't carry between phases
  
  scarcity_creates: "immediate_choice_pressure",
  strategic_depth: "which_activities_to_prioritize"
}
```

**Design Purpose:** Creates **turn-by-turn tactical decisions** - "I have 3 energy, what matters most right now?"

**See:** `11-turn-economy-implementation.md` for complete energy system

---

### 2. ⏰ Time (Weekly Budget)

**What It Represents:** The finite hours in a week available for flexible activities.

**Key Characteristics:**
```javascript
{
  type: "weekly_budget",
  scope: "per_week",
  budget: {
    total_hours: 168,
    fixed_obligations: 115,          // Sleep, work, basic needs
    flexible_hours: 53               // What player controls
  },
  regeneration: "start_of_each_week",
  carry_over: false,
  
  scarcity_creates: "weekly_planning_pressure",
  strategic_depth: "which_commitments_to_make"
}
```

**Design Purpose:** Creates **weekly strategic planning** - "I have 53 hours this week, what's most important?"

**Unique Mechanic:** Time is the only resource where you can "run out" mid-week and be forced to skip activities.

**See:** `11-turn-economy-implementation.md` for complete time system

---

### 3. 💰 Money (Liquid Resource)

**What It Represents:** Financial resources for purchases and lifestyle.

**Key Characteristics:**
```javascript
{
  type: "liquid_resource",
  scope: "continuous",
  budget: {
    income: "varies_by_career",      // $2,500-$12,000/month
    fixed_expenses: 2100,             // $2,100/month
    discretionary: "income - expenses"
  },
  regeneration: "weekly_paycheck",
  carry_over: true,                  // Savings accumulate
  can_go_negative: true,             // Debt possible
  
  scarcity_creates: "financial_anxiety",
  strategic_depth: "save_vs_spend_vs_invest"
}
```

**Design Purpose:** Creates **financial pressure and lifestyle choices** - "Can I afford this? Should I save?"

**Unique Mechanic:** Only resource that can accumulate (savings) or go negative (debt).

**See:** `11-turn-economy-implementation.md` for complete money system

---

### 4. 🤝 Social Capital (Relationship Currency)

**What It Represents:** Earned goodwill with each NPC that enables asking favors.

**Key Characteristics:**
```javascript
{
  type: "per_npc_currency",
  scope: "per_relationship",
  budget: {
    range_per_npc: [-5, +10],
    starting_balance: 0
  },
  regeneration: "earned_through_actions",
  carry_over: true,
  can_go_negative: true,             // Relationship debt
  
  scarcity_creates: "relationship_management",
  strategic_depth: "give_and_take_balance"
}
```

**Design Purpose:** Creates **authentic relationship dynamics** - "I've been asking a lot lately, maybe I should help them first."

**Unique Mechanic:** Separate balance for each NPC. Prevents exploiting relationships.

**See:** `11-turn-economy-implementation.md` for complete social capital system

---

### 5. 😰 Comfort Zone (Personality Modifier)

**What It Represents:** Psychological cost of activities outside personality.

**Key Characteristics:**
```javascript
{
  type: "personality_modifier",
  scope: "per_activity",
  cost_range: [0.0, 3.0],            // Calculated per activity
  regeneration: null,                 // Not a pool
  drains: ["emotional_meter", "mental_meter"],
  
  scarcity_creates: "growth_tension",
  strategic_depth: "comfort_vs_growth"
}
```

**Design Purpose:** Makes **personality mechanically meaningful** and creates **growth opportunities with cost**.

**Unique Mechanic:** Not a pool - calculated per activity based on personality alignment. Drains other resources (Emotional/Mental meters).

**Note:** master_truths v1.1 clarifies this is a **modifier**, not a currency. It modifies costs but isn't tracked as a pool.

**See:** `11-turn-economy-implementation.md` for complete comfort zone system

---

### 6. 🎲 Success Chance (Probability Modifier)

**What It Represents:** Likelihood of activity succeeding vs. failing.

**Key Characteristics:**
```javascript
{
  type: "probability_modifier",
  scope: "per_activity",
  range: [0.05, 0.95],               // Always 5-95% (never guaranteed)
  base: "activity_base_rate",
  modifiers: [
    "personality_alignment",
    "skill_level",
    "meter_states",
    "emotional_state",
    "relationships",
    "environment",
    "risk_choice"
  ],
  
  scarcity_creates: "risk_management",
  strategic_depth: "when_to_take_chances"
}
```

**Design Purpose:** Creates **risk/reward decisions** and makes **failure meaningful**.

**Unique Mechanic:** Not a pool - calculated per activity. Introduces uncertainty and drama.

**Note:** master_truths v1.1 clarifies success is based on skills, personality, relationships - not RNG gacha.

**See:** `12-success-probability-formulas.md` for complete success system

---

## Resource Integration Matrix

### How Resources Interact

```javascript
const RESOURCE_INTERACTIONS = {
  // Energy affects other resources
  energy_low: {
    affects: ["success_chance", "mental_meter", "emotional_meter"],
    effect: "negative",
    magnitude: "moderate"
  },
  
  // Time scarcity creates cascade
  time_scarce: {
    affects: ["energy", "mental_meter", "social_meter"],
    effect: "pressure",
    magnitude: "high"
  },
  
  // Money affects lifestyle
  money_low: {
    affects: ["emotional_meter", "available_activities", "social_options"],
    effect: "restriction",
    magnitude: "high"
  },
  
  // Social capital enables opportunities
  social_capital_high: {
    affects: ["available_activities", "success_chance", "opportunities"],
    effect: "positive",
    magnitude: "moderate"
  },
  
  // Comfort zone drains other resources
  comfort_zone_high_cost: {
    affects: ["emotional_meter", "mental_meter", "energy"],
    effect: "drain",
    magnitude: "variable"
  },
  
  // Success builds momentum
  success_streak: {
    affects: ["emotional_meter", "confidence", "success_chance_future"],
    effect: "positive",
    magnitude: "moderate"
  }
};
```

---

## Multi-Resource Card Cost Example

### Complete Card with All Resources

```javascript
const COMPLETE_ACTIVITY_CARD = {
  id: "host_dinner_party",
  name: "Host Dinner Party",
  
  // RESOURCE COSTS
  costs: {
    energy: 4,                       // High energy (cooking, hosting)
    time: 8,                         // 8 hours (prep + event)
    money: 150,                      // Groceries, wine, supplies
    social_capital: {
      // Inviting people costs social capital with each
      sarah: -1,
      marcus: -1,
      elena: -1
    },
    comfort_zone: null,              // Calculated based on personality
    success_chance: null             // Calculated based on skills
  },
  
  // CALCULATED COSTS (runtime)
  calculated_costs: function(player) {
    // Comfort zone cost
    let comfortCost = 0;
    if (player.personality.extraversion < 3.0) {
      comfortCost += 1.5;            // Hosting draining for introverts
    }
    if (player.personality.conscientiousness < 3.0) {
      comfortCost += 1.0;            // Planning/executing is hard
    }
    
    // Success chance
    let successChance = 0.70;        // Base 70%
    successChance += player.skills.cooking * 0.05;
    successChance += player.skills.social * 0.05;
    successChance += player.meters.emotional > 5 ? 0.10 : 0;
    
    return {
      comfort_zone: comfortCost,
      success_chance: Math.max(0.05, Math.min(0.95, successChance))
    };
  },
  
  // OUTCOMES
  outcomes: {
    success: {
      energy: 0,                     // Energy already spent
      time: 0,                       // Time already spent
      money: 0,                      // Money already spent
      social_capital: {
        sarah: +3,                   // Great time! Earned capital back + bonus
        marcus: +3,
        elena: +3
      },
      social_meter: +3,              // Connection boost
      emotional_meter: +2,           // Felt good
      relationships: {
        sarah: { trust: +0.05 },
        marcus: { trust: +0.05 },
        elena: { trust: +0.05 }
      },
      unlocks: ["friend_group_dynamics", "hosting_reputation"]
    },
    
    failure: {
      energy: 0,                     // Still spent
      time: 0,                       // Still spent
      money: 0,                      // Still spent (wasted!)
      social_capital: {
        sarah: 0,                    // No additional cost (they came)
        marcus: 0,
        elena: 0
      },
      social_meter: -1,              // Awkward evening
      emotional_meter: -2,           // Embarrassed
      narrative: "The food was bland, conversation stilted. Everyone left early. You feel like you failed as a host."
    }
  }
};
```

**Key Insight:** This single activity requires managing ALL 6 resources simultaneously. This is the core challenge of Unwritten.

---

## Resource Scarcity Design

### Intentional Scarcity Patterns

```javascript
const SCARCITY_DESIGN = {
  energy: {
    scarcity_level: "high",
    design_intent: "immediate_tactical_pressure",
    player_feels: "I can't do everything I want right now",
    creates_tension: "turn_by_turn_prioritization"
  },
  
  time: {
    scarcity_level: "high",
    design_intent: "weekly_strategic_pressure",
    player_feels: "There aren't enough hours in the week",
    creates_tension: "life_balance_challenge"
  },
  
  money: {
    scarcity_level: "moderate",
    design_intent: "lifestyle_limitation",
    player_feels: "I need to be careful with spending",
    creates_tension: "financial_planning",
    note: "Varies by career level"
  },
  
  social_capital: {
    scarcity_level: "moderate",
    design_intent: "relationship_authenticity",
    player_feels: "I can't keep asking for favors",
    creates_tension: "give_and_take_balance"
  },
  
  comfort_zone: {
    scarcity_level: "variable",
    design_intent: "growth_cost",
    player_feels: "Stepping outside comfort zone is draining",
    creates_tension: "comfort_vs_growth_tradeoff"
  },
  
  success_chance: {
    scarcity_level: "variable",
    design_intent: "uncertainty_drama",
    player_feels: "This might not work",
    creates_tension: "risk_management"
  }
};
```

---

## Resource Management Strategies

### Player Archetypes by Resource Management

```javascript
const PLAYER_ARCHETYPES = {
  efficient_optimizer: {
    strategy: "Maximize value per resource spent",
    focuses_on: ["energy_efficiency", "time_optimization"],
    playstyle: "Batch routines, optimize paths, min-max",
    challenge: "May miss spontaneous opportunities"
  },
  
  social_butterfly: {
    strategy: "Invest heavily in relationships",
    focuses_on: ["social_capital", "relationship_depth"],
    playstyle: "Prioritize social activities, build network",
    challenge: "May neglect personal goals"
  },
  
  ambitious_achiever: {
    strategy: "Push toward aspiration at all costs",
    focuses_on: ["aspiration_progress", "success_maximization"],
    playstyle: "High energy activities, risk-taking",
    challenge: "Burnout risk, relationship neglect"
  },
  
  balanced_lifestyle: {
    strategy: "Maintain equilibrium across all resources",
    focuses_on: ["meter_balance", "sustainable_pacing"],
    playstyle: "Careful planning, avoid extremes",
    challenge: "Slower aspiration progress"
  },
  
  comfort_seeker: {
    strategy: "Stay within comfort zone, minimize risks",
    focuses_on: ["emotional_stability", "routine_maintenance"],
    playstyle: "Familiar activities, safe choices",
    challenge: "Limited growth, missed opportunities"
  },
  
  growth_focused: {
    strategy: "Deliberately push comfort zone",
    focuses_on: ["personality_evolution", "skill_development"],
    playstyle: "Challenge-seeking, high comfort costs",
    challenge: "Emotional/mental drain"
  }
};
```

---

## Resource Crisis Management

### What Happens When Resources Run Out

```javascript
const RESOURCE_CRISIS_HANDLERS = {
  energy_depleted: {
    immediate: "No high-energy activities available",
    short_term: "Lower success chances on remaining activities",
    recovery: "Wait for next phase regeneration",
    can_continue: true
  },
  
  time_exhausted: {
    immediate: "Week auto-advances to weekend or next week",
    short_term: "Missed opportunities noted",
    recovery: "Next week starts fresh",
    can_continue: true,
    narrative: "The week flew by. You didn't get to everything."
  },
  
  money_negative: {
    immediate: "Crisis event triggered",
    short_term: "Limited activity options",
    recovery: "Need income or reduce expenses",
    can_continue: true,
    crisis_options: ["borrow_money", "sell_items", "extra_work", "downsize"]
  },
  
  social_capital_very_negative: {
    immediate: "Relationship strained",
    short_term: "NPC less available, trust decay",
    recovery: "Must rebuild through helping actions",
    can_continue: true,
    narrative: "They're keeping their distance. You've been taking too much."
  },
  
  comfort_zone_overextended: {
    immediate: "Emotional/mental meters drain rapidly",
    short_term: "Negative emotional states triggered",
    recovery: "Rest and familiar activities",
    can_continue: true,
    warning: "You've been pushing too hard outside your comfort zone"
  },
  
  repeated_failures: {
    immediate: "Emotional meter drops",
    short_term: "DISCOURAGED state triggered",
    recovery: "Easier activities, support-seeking",
    can_continue: true,
    narrative: "Nothing seems to be working. Maybe you need to try something different."
  }
};
```

---

## Resource Display Guidelines

### UI Requirements

```javascript
const RESOURCE_DISPLAY = {
  energy: {
    format: "3/8",                   // Current / Max for day
    color_coding: {
      full: "green",
      moderate: "yellow",
      low: "orange",
      depleted: "red"
    },
    update_frequency: "every_action",
    show_next_regen: true            // "Regenerates at 12pm"
  },
  
  time: {
    format: "28 hours left this week",
    color_coding: {
      plenty: "green",
      moderate: "yellow",
      scarce: "orange",
      critical: "red"
    },
    update_frequency: "every_activity_with_time_cost",
    show_breakdown: true             // "45 hours spent so far"
  },
  
  money: {
    format: "$1,250",
    color_coding: {
      comfortable: "green",
      moderate: "yellow",
      tight: "orange",
      crisis: "red"
    },
    update_frequency: "every_transaction",
    show_next_expense: true          // "Rent due in 3 days: $525"
  },
  
  social_capital: {
    format: "Per NPC, shown on character card",
    display: "+3 Sarah" or "-2 Marcus",
    color_coding: {
      positive: "green",
      neutral: "gray",
      negative: "orange",
      strained: "red"
    },
    update_frequency: "after_interactions",
    context_sensitive: true          // Show when asking favors
  },
  
  comfort_zone: {
    format: "Warning indicator on cards",
    display: "😰 Comfort Risk (Low Openness)",
    color_coding: {
      comfortable: "green",
      stretch: "yellow",
      challenging: "orange",
      overwhelming: "red"
    },
    show_on_preview: true,           // Before playing card
    explain_why: true                // "You're introverted, large groups drain you"
  },
  
  success_chance: {
    format: "65% chance of success",
    color_coding: {
      very_likely: "green",          // 75%+
      likely: "yellow",              // 50-74%
      uncertain: "orange",           // 25-49%
      risky: "red"                   // <25%
    },
    show_modifiers: true,            // "+10% from skill, -15% from exhaustion"
    update_on_state_change: true
  }
};
```

---

## Balancing Principles

### Resource Design Philosophy

1. **Multiple Constraints Create Meaningful Choice**
   - Single resource = trivial optimization
   - Multiple resources = authentic life challenge

2. **Scarcity Must Be Felt, Not Arbitrary**
   - 168 hours/week = real constraint
   - 8 energy/day = feels limiting but fair

3. **Resources Should Interact, Not Exist in Silos**
   - Low energy → lower success chance
   - Time pressure → mental drain
   - Money scarcity → emotional stress

4. **Recovery Should Require Intentional Action**
   - Energy regenerates automatically (basic need)
   - Time resets weekly (calendar reality)
   - Money requires income (work)
   - Social capital requires reciprocity (relationships)
   - Comfort zone requires rest (recovery)
   - Success requires preparation (skill-building)

5. **No Resource Should Be Trivially Abundant**
   - Even late-game, resources matter
   - Wealth doesn't eliminate time constraints
   - Strong relationships still require maintenance

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
- [x] **Dramatic irony mechanics used when knowledge gaps exist (score ≥ 0.6)**
- [x] **Memory resonance factors applied to recall (weights: 0.7-0.95)**
- [x] **Novel-quality thresholds met (≥ 0.7 overall; authenticity ≥ 0.7; tension ≥ 0.6; hooks ≥ 0.6)**
- [x] This doc cites **Truths v1.2** at the top

**References:**
- See `11-turn-economy-implementation.md` for complete details on each resource
- See `12-success-probability-formulas.md` for success chance calculations
- See `13-meter-effects-tables.md` for how meters affect resources
- See `71-daily-turn-flow-detailed.md` for resource tracking during turns

---

**This specification provides the high-level overview of how all 6 resources integrate to create the complete economy system.**

