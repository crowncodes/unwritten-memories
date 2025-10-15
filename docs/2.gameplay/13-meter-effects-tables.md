# Meter Effects Tables - Implementation Specification

**Compliance:** `master_truths_canonical_spec_v_1_2.md` (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete threshold effects for all 4 meters at each level (0-10)

**References:**
- **Design Philosophy:** `1.concept/21-turn-structure.md` (WHY meters exist)
- **Schema Definition:** `7.schema/04-gameplay-mechanics.md` (MeterState interface)
- **Success Formulas:** `12-success-probability-formulas.md` (meter modifiers)
- **Emotional States:** `14-emotional-state-mechanics.md` (meter-triggered states)

---

## Overview

The **4 core meters** (Physical, Mental, Social, Emotional) track character well-being on a 0-10 scale. Each meter level has **specific gameplay effects** that influence card costs, success chances, emotional states, and available activities.

**NEW - Master Truths v1.2:** Each meter level now also determines **Emotional Capacity** (0-10 continuous scale) - a character's ability to provide emotional support to others and handle emotional demands.

**Core Principle:** Meters create authentic life simulation challenge - ignoring needs has consequences, maintaining balance requires effort.

---

## Emotional Capacity System *(NEW - Master Truths v1.2)*

**What is Emotional Capacity?**

Emotional Capacity (0.0-10.0 continuous scale) represents a character's current ability to:
- Provide emotional support to others
- Handle emotionally demanding situations
- Respond to player emotional needs
- Maintain emotional availability

**Key Rule from Master Truths v1.2, Section 16:**
> "NPCs can only provide support when their Capacity ≥ (player_emotional_need + 2). A struggling NPC at Capacity 4.0 cannot adequately support a player at need level 4.0—they'd need Capacity 6.0+"

### Emotional Capacity Calculation

```javascript
function calculateEmotionalCapacity(meters, activeStressors) {
  // Base capacity derived from meters
  let capacity = 0;
  
  // EMOTIONAL METER: Primary driver (50% weight)
  capacity += meters.emotional * 0.50;
  
  // MENTAL METER: Secondary driver (30% weight)
  capacity += meters.mental * 0.30;
  
  // PHYSICAL METER: Tertiary driver (15% weight)
  capacity += meters.physical * 0.15;
  
  // SOCIAL METER: Minor driver (5% weight)
  capacity += meters.social * 0.05;
  
  // Apply circumstance stacking penalty
  const stackingPenalty = calculateStackingPenalty(activeStressors);
  capacity -= stackingPenalty;
  
  // Clamp to 0.0-10.0 range
  return Math.max(0.0, Math.min(10.0, capacity));
}

// CIRCUMSTANCE STACKING PENALTY
function calculateStackingPenalty(activeStressors) {
  const stressorCount = countActiveStressors(activeStressors);
  
  // Each stressor beyond first reduces capacity
  if (stressorCount <= 1) return 0;
  if (stressorCount === 2) return 1.0;  // -1.0 capacity
  if (stressorCount === 3) return 2.5;  // -2.5 capacity
  if (stressorCount === 4) return 4.0;  // -4.0 capacity
  if (stressorCount >= 5) return 6.0;   // -6.0 capacity (near zero)
  
  return 0;
}

function countActiveStressors(stressors) {
  let count = 0;
  if (stressors.workPressure > 7) count++;
  if (stressors.moneyStress) count++;
  if (stressors.relationshipTension.length >= 2) count++;
  if (stressors.healthIssues) count++;
  if (stressors.familyCrisis) count++;
  if (stressors.housingIssues) count++;
  if (stressors.aspirationDeadline && stressors.aspirationProgress < 0.5) count++;
  
  return count;
}
```

### Emotional Capacity Thresholds & Effects

```javascript
const CAPACITY_THRESHOLDS = {
  "0.0-2.0": {
    state: "DEPLETED",
    description: "Emotionally unavailable - cannot support anyone",
    gameplay: {
      can_provide_support: false,
      dialogue_limited: true,
      interaction_quality: "minimal",
      may_need_support: true,
      response_pattern: "withdrawn"
    },
    narrative: "They can barely hold it together. Don't ask them for emotional support right now."
  },
  
  "2.1-4.0": {
    state: "LOW",
    description: "Struggling - can only handle light emotional needs",
    gameplay: {
      can_support_needs_up_to: 2.0,  // Need + 2 rule: can support needs ≤ 2.0
      dialogue_available: "limited",
      interaction_quality: "strained",
      response_pattern: "distracted"
    },
    narrative: "They're managing, but barely. They can listen, but not much more."
  },
  
  "4.1-6.0": {
    state: "MODERATE",
    description: "Stable - can provide moderate support",
    gameplay: {
      can_support_needs_up_to: 4.0,  // Can support needs ≤ 4.0
      dialogue_available: "normal",
      interaction_quality: "present",
      response_pattern: "engaged"
    },
    narrative: "They're doing okay. They can be there for you, within reason."
  },
  
  "6.1-8.0": {
    state: "HIGH",
    description: "Thriving - can provide strong support",
    gameplay: {
      can_support_needs_up_to: 6.0,  // Can support needs ≤ 6.0
      dialogue_available: "full",
      interaction_quality: "strong",
      response_pattern: "supportive",
      may_offer_unprompted_help: true
    },
    narrative: "They're in a good place. They have energy to support you."
  },
  
  "8.1-10.0": {
    state: "PEAK",
    description: "Flourishing - exceptional emotional availability",
    gameplay: {
      can_support_needs_up_to: 8.0,  // Can support needs ≤ 8.0
      dialogue_available: "exceptional",
      interaction_quality: "transformative",
      response_pattern: "deeply_present",
      offers_unprompted_help: true,
      crisis_intervention_available: true
    },
    narrative: "They're radiating stability. They can hold space for whatever you need."
  }
};
```

### Support Availability Check

```javascript
function canProvideSupport(npcCapacity, playerEmotionalNeed) {
  // Master Truths v1.2 Rule: Capacity must be ≥ (need + 2)
  const requiredCapacity = playerEmotionalNeed + 2.0;
  
  if (npcCapacity >= requiredCapacity) {
    return {
      available: true,
      quality: getSupport Quality(npcCapacity, requiredCapacity),
      message: `They have the emotional bandwidth to help (Capacity: ${npcCapacity.toFixed(1)})`
    };
  } else {
    return {
      available: false,
      shortfall: requiredCapacity - npcCapacity,
      message: `They're struggling too much right now (Capacity: ${npcCapacity.toFixed(1)}, you need ${requiredCapacity.toFixed(1)})`,
      alternative: "Maybe check on them instead?"
    };
  }
}

function getSupportQuality(npcCapacity, requiredCapacity) {
  const buffer = npcCapacity - requiredCapacity;
  
  if (buffer >= 3.0) return "exceptional";  // Way more than enough
  if (buffer >= 1.5) return "strong";       // Comfortable margin
  if (buffer >= 0.5) return "adequate";     // Enough
  return "minimal";                          // Just barely enough
}
```

---

## The 4 Meters

```typescript
interface PlayerMeters {
  physical: MeterState;   // Physical health, energy, fitness
  mental: MeterState;     // Cognitive capacity, focus, burnout
  social: MeterState;     // Connection, belonging, loneliness
  emotional: MeterState;  // Mood, stability, fulfillment
}

interface MeterState {
  current: RangedInt<0, 10>;
  threshold_effects: ThresholdEffect[];
  passive_change_rate: number;  // -1.0 to +1.0 per week
  last_critical_event?: GameTime;
}
```

---

## Physical Meter (0-10)

**Purpose:** Tracks physical health, energy levels, and body maintenance.

### Level 0-1: PHYSICAL CRISIS ⚠️ CRITICAL

**State Name:** "Physically Broken"

**Gameplay Effects:**
```javascript
{
  energy_max_modifier: -3,              // Max energy reduced by 3
  all_physical_activities_blocked: true, // Can't do physical activities
  success_penalty_all: -0.30,            // -30% success on ALL activities
  forced_rest_activities: true,          // Only rest activities available
  crisis_event_triggered: "HEALTH_BREAKDOWN",
  
  emotional_state_forced: "EXHAUSTED",
  emotional_penalty: -2,                 // -2 emotional meter
  
  card_filtering: {
    physical_activities: 0.0,            // Completely filtered out
    rest_activities: 3.0,                // Heavily prioritized
    medical_activities: 2.5,             // Appear frequently
    obligations: 0.3                     // Reduced (but may still appear)
  }
}
```

**Narrative Context:**
```
"Your body has given up. You can barely get out of bed. Everything 
hurts. You've pushed too hard for too long. This is a crisis."
```

**How to Recover:**
- Must spend 2-3 full days resting
- Medical intervention may be required
- Cannot pursue aspirations until recovered
- Takes 1-2 weeks minimum to recover to Level 4+

---

### Level 2-3: PHYSICAL LOW ⚠️ WARNING

**State Name:** "Physically Exhausted"

**Gameplay Effects:**
```javascript
{
  energy_max_modifier: -1,              // Max energy reduced by 1
  physical_activities_penalty: -0.20,   // -20% success on physical
  energy_cost_physical: +1,             // Physical activities cost +1 energy
  
  emotional_state_likely: "EXHAUSTED",
  emotional_penalty: -1,
  
  card_filtering: {
    high_energy_activities: 0.4,        // Reduced appeal
    rest_activities: 1.8,               // Increased appeal
    physical_activities: 0.6            // Reduced appeal
  },
  
  warning_message: "You're running your body into the ground. Rest soon."
}
```

**Triggers:**
- Appears after 1-2 weeks of neglect
- Working 60+ hours/week
- No exercise or sleep for extended period

**Recovery:**
- 2-3 rest activities needed
- One full weekend of recovery
- Exercise paradoxically helps (gentle activity)

---

### Level 4-6: PHYSICAL NORMAL ✅ BASELINE

**State Name:** "Physically Stable"

**Gameplay Effects:**
```javascript
{
  // No modifiers - this is the baseline
  energy_max_modifier: 0,
  success_modifier: 0,
  
  card_filtering: {
    all_categories: 1.0  // No filtering
  }
}
```

**Maintenance:**
- Regular sleep (appears as routine)
- Occasional exercise
- Balanced food/rest
- This is the "default" state most players aim for

---

### Level 7-8: PHYSICAL HIGH ✅ STRONG

**State Name:** "Physically Energized"

**Gameplay Effects:**
```javascript
{
  energy_max_modifier: +1,              // Max energy increased by 1
  physical_activities_bonus: +0.10,     // +10% success on physical
  energy_cost_physical: -1,             // Physical activities cost -1 energy
  
  emotional_boost: +1,                  // +1 emotional meter (feel good)
  
  card_filtering: {
    physical_activities: 1.5,           // Increased appeal
    athletic_activities: 1.7,           // Even more appealing
    rest_activities: 0.7                // Slightly less appealing
  },
  
  unlocks: ["advanced_physical_activities", "athletic_challenges"]
}
```

**How to Achieve:**
- Regular exercise (3-4x/week)
- Good sleep routine
- Healthy eating habits
- Active lifestyle cards

---

### Level 9-10: PHYSICAL PEAK ✅ OPTIMAL

**State Name:** "Peak Physical Condition"

**Gameplay Effects:**
```javascript
{
  energy_max_modifier: +2,              // Max energy increased by 2
  physical_activities_bonus: +0.20,     // +20% success on physical
  energy_cost_physical: -1,
  physical_damage_resistance: 0.5,      // Slower decay
  
  emotional_boost: +2,
  mental_boost: +1,                     // Physical health helps mental
  
  card_filtering: {
    physical_activities: 1.8,
    athletic_challenges: 2.0,
    endurance_activities: 1.9
  },
  
  unlocks: ["elite_physical_activities", "competition_cards"],
  
  achievement: "Physical Peak",
  rare_state: true  // Hard to maintain
}
```

**How to Achieve:**
- Sustained athletic training
- Athlete lifestyle
- Optimal sleep, nutrition, exercise
- Difficult to maintain long-term

**Maintenance Challenge:**
- Requires 4-5 hours/week dedicated exercise
- Easily drops if neglected
- Competes with other priorities

---

## Mental Meter (0-10)

**Purpose:** Tracks cognitive capacity, focus, stress, and burnout.

### Level 0-1: MENTAL CRISIS ⚠️ CRITICAL

**State Name:** "Burned Out / Breakdown"

**Gameplay Effects:**
```javascript
{
  energy_cost_all_cognitive: +2,        // All cognitive tasks cost +2 energy
  success_penalty_cognitive: -0.30,     // -30% success on mental tasks
  focus_impossible: true,               // Cannot do focused work
  
  crisis_event_triggered: "MENTAL_BREAKDOWN",
  emotional_state_forced: "NUMB" or "OVERWHELMED",
  emotional_penalty: -3,
  
  card_filtering: {
    work_activities: 0.2,               // Work nearly impossible
    cognitive_tasks: 0.1,               // Thinking is hard
    therapy_activities: 2.5,            // Therapy prioritized
    rest_activities: 2.0,
    avoidance_tempting: 1.8             // Escape behaviors appealing
  },
  
  forced_decisions: ["take_medical_leave", "therapy_intervention", "quit_job"]
}
```

**Narrative Context:**
```
"You can't think straight. Every task feels insurmountable. You're 
forgetting things. Your mind is fog. This is burnout."
```

**Recovery:**
- Minimum 2-4 weeks of reduced obligations
- Therapy or professional help recommended
- Cannot push through - must address
- May require life changes (quit job, end relationship, etc.)

---

### Level 2-3: MENTAL LOW ⚠️ WARNING

**State Name:** "Mentally Exhausted / Foggy"

**Gameplay Effects:**
```javascript
{
  energy_cost_cognitive: +1,
  success_penalty_cognitive: -0.15,     // -15% on mental tasks
  focus_duration_reduced: 0.5,          // Can only focus half as long
  
  emotional_state_likely: "OVERWHELMED" or "EXHAUSTED",
  emotional_penalty: -1,
  
  card_filtering: {
    complex_tasks: 0.5,
    work_activities: 0.7,
    rest_activities: 1.6,
    simple_tasks: 1.3                   // Simple tasks more appealing
  },
  
  warning_message: "You're mentally drained. Everything feels harder."
}
```

**Triggers:**
- Working long hours (50+/week)
- High-stress situations
- Decision fatigue
- Insufficient rest

---

### Level 4-6: MENTAL NORMAL ✅ BASELINE

**State Name:** "Mentally Stable"

**Gameplay Effects:**
```javascript
{
  // No modifiers - baseline
  success_modifier: 0,
  energy_cost_modifier: 0,
  
  card_filtering: {
    all_categories: 1.0
  }
}
```

---

### Level 7-8: MENTAL HIGH ✅ SHARP

**State Name:** "Mentally Sharp / Clear"

**Gameplay Effects:**
```javascript
{
  success_bonus_cognitive: +0.15,       // +15% on mental tasks
  energy_cost_cognitive: -1,            // Cognitive tasks easier
  focus_duration_bonus: 1.5,            // Can focus 50% longer
  
  emotional_boost: +1,
  
  card_filtering: {
    cognitive_tasks: 1.6,
    learning_activities: 1.8,
    creative_work: 1.7,
    complex_projects: 1.5
  },
  
  unlocks: ["advanced_cognitive_activities", "deep_work_sessions"]
}
```

**How to Achieve:**
- Good sleep (7-8 hours)
- Regular breaks
- Stress management
- Cognitive rest activities (meditation, nature, etc.)

---

### Level 9-10: MENTAL PEAK ✅ OPTIMAL

**State Name:** "Peak Mental Clarity / Flow State"

**Gameplay Effects:**
```javascript
{
  success_bonus_cognitive: +0.25,       // +25% on mental tasks
  energy_cost_cognitive: -1,
  focus_duration_bonus: 2.0,            // Double focus duration
  
  emotional_boost: +2,
  creative_bonus: +0.20,                // +20% creative output
  
  emotional_state_likely: "FOCUSED" or "INSPIRED",
  
  card_filtering: {
    cognitive_tasks: 2.0,
    deep_work: 2.2,
    creative_projects: 2.0,
    learning: 1.9
  },
  
  unlocks: ["elite_cognitive_challenges", "breakthrough_projects"],
  
  special_effects: {
    flow_state_possible: true,
    breakthrough_chance: +0.15,
    innovation_bonus: true
  }
}
```

**How to Achieve:**
- Sustained cognitive health practices
- Regular meditation or mindfulness
- Excellent sleep hygiene
- Low stress lifestyle
- Difficult to maintain

---

## Social Meter (0-10)

**Purpose:** Tracks social connection, belonging, and loneliness.

### Level 0-1: SOCIAL CRISIS ⚠️ CRITICAL

**State Name:** "Completely Isolated / Socially Broken"

**Gameplay Effects:**
```javascript
{
  social_activities_penalty: -0.25,     // -25% success on social
  relationship_trust_decay: 0.05,       // -0.05 trust/week with all NPCs
  new_relationship_blocked: true,       // Can't form new relationships
  
  crisis_event_triggered: "ISOLATION_CRISIS",
  emotional_state_forced: "MELANCHOLY" or "NUMB",
  emotional_penalty: -3,
  mental_penalty: -1,                   // Isolation affects mental health
  
  card_filtering: {
    social_activities: 0.3,             // Social feels impossible
    solitude_activities: 2.0,           // Withdrawal appealing
    reconnection_activities: 1.8,       // System tries to help
    avoidance: 1.6
  },
  
  warning_message: "You've cut yourself off completely. The loneliness is crushing."
}
```

**Narrative Context:**
```
"You haven't talked to anyone in weeks. Everyone has stopped reaching 
out. You're alone. Completely alone."
```

**Recovery:**
- Requires deliberate reconnection
- May need therapy
- Relationships may have degraded significantly
- 3-4 weeks minimum to recover

---

### Level 2-3: SOCIAL LOW ⚠️ WARNING

**State Name:** "Lonely / Disconnected"

**Gameplay Effects:**
```javascript
{
  social_activities_penalty: -0.10,
  relationship_trust_decay: 0.02,       // -0.02 trust/week
  
  emotional_state_likely: "MELANCHOLY" or "DISCOURAGED",
  emotional_penalty: -1,
  
  card_filtering: {
    social_activities: 0.7,
    solitude: 1.4,
    reconnection: 1.5,
    easy_social: 1.3                    // Low-pressure social appealing
  },
  
  warning_message: "You're feeling isolated. When did you last really connect with someone?"
}
```

**Triggers:**
- 2+ weeks without meaningful social interaction
- Relationship neglect
- Moving to new city
- After breakup or loss

---

### Level 4-6: SOCIAL NORMAL ✅ BASELINE

**State Name:** "Socially Connected"

**Gameplay Effects:**
```javascript
{
  // No modifiers - baseline
  success_modifier: 0,
  
  card_filtering: {
    all_categories: 1.0
  }
}
```

**Maintenance:**
- Weekly social interactions
- Maintain 2-3 active friendships
- Attend occasional events

---

### Level 7-8: SOCIAL HIGH ✅ THRIVING

**State Name:** "Socially Thriving / Well-Connected"

**Gameplay Effects:**
```javascript
{
  social_activities_bonus: +0.15,       // +15% success on social
  relationship_formation_bonus: +0.10,  // Easier to form new bonds
  social_capital_generation: +1,        // +1 social capital per interaction
  
  emotional_boost: +1,
  
  card_filtering: {
    social_activities: 1.6,
    group_events: 1.7,
    networking: 1.8,
    new_people: 1.5
  },
  
  unlocks: ["advanced_social_activities", "large_events", "networking_opportunities"]
}
```

**How to Achieve:**
- Regular social engagement (2-3x/week)
- Multiple active friendships
- Social variety (different groups)
- Balanced social calendar

---

### Level 9-10: SOCIAL PEAK ✅ OPTIMAL

**State Name:** "Social Butterfly / Community Leader"

**Gameplay Effects:**
```javascript
{
  social_activities_bonus: +0.25,
  relationship_formation_bonus: +0.20,
  social_capital_generation: +2,
  influence_bonus: true,
  
  emotional_boost: +2,
  
  card_filtering: {
    social_activities: 2.0,
    leadership_opportunities: 2.2,
    community_building: 1.9,
    large_social_events: 2.0
  },
  
  unlocks: ["elite_social_activities", "community_leadership", "social_influence"],
  
  special_effects: {
    magnetic_personality: true,
    can_introduce_npcs: true,
    social_catalyst: true
  }
}
```

**How to Achieve:**
- Very active social life
- Central in multiple social circles
- Regular hosting/organizing
- Strong relationship network (5+ Level 3+ NPCs)

---

## Emotional Meter (0-10)

**Purpose:** Tracks emotional well-being, fulfillment, and mood stability.

### Level 0-1: EMOTIONAL CRISIS ⚠️ CRITICAL

**State Name:** "Emotionally Shattered / Despair"

**Gameplay Effects:**
```javascript
{
  success_penalty_all: -0.20,           // -20% on ALL activities
  emotional_resilience: 0.0,            // No resilience
  negative_spirals_likely: true,
  
  crisis_event_triggered: "EMOTIONAL_CRISIS",
  emotional_state_forced: "NUMB" or "MELANCHOLY" or "DEVASTATED",
  
  physical_penalty: -1,                 // Depression affects body
  mental_penalty: -2,                   // Depression affects mind
  social_penalty: -1,                   // Hard to connect
  
  card_filtering: {
    meaningful_activities: 0.3,
    joy_activities: 0.2,                // Nothing feels good
    therapy_activities: 2.5,
    support_seeking: 2.0,
    avoidance: 1.9,
    self_harm_risk: 1.5                 // Dangerous behaviors
  },
  
  forced_decisions: ["seek_therapy", "crisis_intervention", "support_network"]
}
```

**Narrative Context:**
```
"Nothing matters. Nothing brings joy. The weight is unbearable. 
You need help. Now."
```

**Recovery:**
- Requires professional help
- May need medication
- Strong support network critical
- 4-8 weeks minimum recovery
- May require major life changes

**Safety Note:**
- Game should provide crisis resources
- Real mental health hotlines
- Encourage seeking help

---

### Level 2-3: EMOTIONAL LOW ⚠️ WARNING

**State Name:** "Emotionally Struggling / Discouraged"

**Gameplay Effects:**
```javascript
{
  success_penalty_all: -0.10,
  emotional_resilience: 0.3,            // Low resilience
  
  emotional_state_likely: "DISCOURAGED" or "MELANCHOLY" or "FRUSTRATED",
  
  physical_penalty: -0.5,
  
  card_filtering: {
    challenging_activities: 0.6,
    comfort_seeking: 1.7,
    support_activities: 1.6,
    joy_activities: 0.8,                // Hard to enjoy things
    avoidance: 1.4
  },
  
  warning_message: "You're really struggling emotionally. Consider reaching out for support."
}
```

**Triggers:**
- Major loss or disappointment
- Prolonged stress
- Neglecting emotional needs
- Relationship problems
- Aspiration failures

---

### Level 4-6: EMOTIONAL NORMAL ✅ BASELINE

**State Name:** "Emotionally Stable"

**Gameplay Effects:**
```javascript
{
  // No modifiers - baseline
  emotional_resilience: 0.7,
  
  card_filtering: {
    all_categories: 1.0
  }
}
```

**Maintenance:**
- Balance in life areas
- Some fulfilling activities
- Healthy relationships
- Occasional joy/pleasure

---

### Level 7-8: EMOTIONAL HIGH ✅ FLOURISHING

**State Name:** "Emotionally Fulfilled / Content"

**Gameplay Effects:**
```javascript
{
  success_bonus_all: +0.10,             // +10% on ALL activities
  emotional_resilience: 1.0,            // Full resilience
  stress_resistance: +0.15,             // +15% stress resistance
  
  physical_boost: +1,                   // Happiness helps health
  
  card_filtering: {
    meaningful_activities: 1.6,
    joy_activities: 1.7,
    growth_activities: 1.6,
    connection_activities: 1.5
  },
  
  unlocks: ["fulfillment_activities", "peak_experiences"]
}
```

**How to Achieve:**
- Progress on aspirations
- Healthy relationships
- Work-life balance
- Regular joy/pleasure
- Sense of purpose

---

### Level 9-10: EMOTIONAL PEAK ✅ OPTIMAL

**State Name:** "Peak Fulfillment / Joyful"

**Gameplay Effects:**
```javascript
{
  success_bonus_all: +0.15,
  emotional_resilience: 1.5,            // Extra resilience buffer
  stress_immunity: 0.25,                // 25% stress immunity
  
  physical_boost: +2,
  mental_boost: +1,
  social_boost: +1,
  
  emotional_state_likely: "JOYFUL" or "INSPIRED" or "GRATEFUL",
  
  card_filtering: {
    all_positive_activities: 1.5,
    peak_experiences: 2.0,
    giving_back: 1.8,
    creative_expression: 1.9
  },
  
  unlocks: ["transcendent_experiences", "life_peak_moments"],
  
  special_effects: {
    spreads_joy: true,                  // Boosts other NPCs
    attracts_positive: true,
    transformative_potential: true
  }
}
```

**How to Achieve:**
- Deep fulfillment across all areas
- Strong sense of purpose
- Healthy relationships
- Regular peak experiences
- Life alignment
- Rare and special state

---

## Emotional Capacity Recovery *(NEW - Master Truths v1.2)*

**How Characters Recover Capacity:**

Emotional capacity recovers through:
1. **Meter improvement** (primary driver - see capacity formula above)
2. **Stressor resolution** (removes stacking penalty)
3. **Rest and recovery activities**
4. **Receiving support from others** (if available)

### Capacity Recovery Rates

```javascript
const CAPACITY_RECOVERY = {
  meter_improvement: {
    rate: "automatic",
    calculation: "Recalculated each turn based on current meters",
    example: "Emotional meter 4→6 increases capacity by ~1.0"
  },
  
  stressor_resolution: {
    single_stressor_resolved: +1.0,  // Removes stacking penalty
    major_crisis_resolved: +2.5,
    all_stressors_cleared: "Full capacity restored"
  },
  
  rest_activities: {
    "Take Mental Health Day": { capacity: +0.5, requires: "time" },
    "Full Weekend Off": { capacity: +1.0, requires: "2 days" },
    "Therapy Session": { capacity: +1.5, requires: "time + $150" },
    "Vacation Week": { capacity: +3.0, requires: "1 week + money" }
  },
  
  receiving_support: {
    "Light Support (coffee chat)": { capacity: +0.5 },
    "Deep Conversation": { capacity: +1.0 },
    "Crisis Support": { capacity: +2.0, requires: "high_capacity_npc" },
    note: "Support only works if NPC has sufficient capacity"
  }
};
```

### Circumstance Stacking and Capacity

```javascript
// EXAMPLE: How Multiple Stressors Compound

const BASE_METERS = {
  emotional: 6,  // Decent
  mental: 5,     // Okay
  physical: 7,   // Good
  social: 6      // Decent
};

// WITHOUT STACKING (1 stressor)
const capacity_1_stressor = 
  (6 * 0.50) +  // Emotional: 3.0
  (5 * 0.30) +  // Mental: 1.5
  (7 * 0.15) +  // Physical: 1.05
  (6 * 0.05) -  // Social: 0.3
  0;            // No stacking penalty
// = 5.85 capacity (MODERATE - can support needs ≤ 3.85)

// WITH 3 STRESSORS (work + money + relationship)
const capacity_3_stressors = 
  (6 * 0.50) +
  (5 * 0.30) +
  (7 * 0.15) +
  (6 * 0.05) -
  2.5;          // -2.5 stacking penalty
// = 3.35 capacity (LOW - can only support needs ≤ 1.35)

// WITH 5 STRESSORS (everything at once)
const capacity_5_stressors = 
  (6 * 0.50) +
  (5 * 0.30) +
  (7 * 0.15) +
  (6 * 0.05) -
  6.0;          // -6.0 stacking penalty
// = -0.15 → 0.0 capacity (DEPLETED - cannot support anyone)

// THE BREAKING POINT:
// Same meters, but stress compounds exponentially.
// This is "when it rains, it pours" made mechanical.
```

### Narrative Example: Capacity in Action

```javascript
// SCENARIO: Player seeks support from Sarah

const PLAYER_STATE = {
  emotionalNeed: 6.0,  // High need (crisis level)
  situation: "Just lost job, relationship ending"
};

const SARAH_STATE = {
  meters: { emotional: 7, mental: 6, physical: 8, social: 7 },
  activeStressors: 0  // Doing well
};

// Calculate Sarah's capacity
const sarahCapacity = 
  (7 * 0.50) +  // 3.5
  (6 * 0.30) +  // 1.8
  (8 * 0.15) +  // 1.2
  (7 * 0.05) -  // 0.35
  0;            // No stacking
// = 6.85 capacity

// Check if Sarah can help
const requiredCapacity = 6.0 + 2.0;  // 8.0 required

if (6.85 < 8.0) {
  return {
    available: false,
    message: `
      Sarah wants to help. She really does.
      But she's not in a place where she can hold space for this.
      She's stable, but you need someone with more bandwidth.
      
      (Her capacity: 6.85, you need: 8.0)
      
      Maybe try Marcus? He's been doing really well lately.
    `
  };
}
```

---

## Cross-Meter Effects

### Multiple Meters Low

When 2+ meters are in warning/crisis:

```javascript
const MULTIPLE_LOW_EFFECTS = {
  two_meters_low: {
    cascade_risk: 0.3,                  // 30% chance other meters drop
    recovery_time_multiplier: 1.5,      // Takes 50% longer to recover
    crisis_cards_frequent: true
  },
  
  three_meters_low: {
    cascade_risk: 0.6,                  // 60% chance cascade
    recovery_time_multiplier: 2.0,      // Takes double time
    forced_intervention: true,          // Game forces action
    life_direction_reevaluation: true   // May need to change life direction
  },
  
  all_meters_low: {
    // Complete life crisis
    cascade_certain: true,
    emergency_intervention_required: true,
    major_life_change_forced: true,
    phase_transition_triggered: true
  }
};
```

---

## Meter Change Rates

### Passive Change (Per Week)

```javascript
const PASSIVE_METER_CHANGES = {
  physical: {
    base_decay: -0.5,                   // Slowly decays without maintenance
    with_routine: 0,                    // Stable with basic care
    with_exercise: +0.5                 // Improves with regular exercise
  },
  
  mental: {
    base_decay: -0.3,
    with_stress: -1.0,                  // Decays faster under stress
    with_rest: +0.5,
    with_work_life_balance: +0.3
  },
  
  social: {
    base_decay: -0.4,                   // Relationships decay without contact
    with_weekly_social: 0,
    with_regular_connection: +0.3
  },
  
  emotional: {
    base_decay: -0.2,
    with_fulfillment: +0.5,
    with_aspiration_progress: +0.3,
    with_neglect: -0.8
  }
};
```

---

## Meter Recovery Activities

### Physical Meter Recovery

```javascript
const PHYSICAL_RECOVERY = {
  "Rest Day": { recovery: +1, time: "1 day" },
  "Full Weekend Rest": { recovery: +2, time: "2 days" },
  "Sleep 9+ Hours": { recovery: +0.5, time: "1 night" },
  "Gentle Exercise": { recovery: +1, time: "1 hour" },
  "Medical Checkup": { recovery: +1.5, time: "3 hours", cost: 150 },
  "Spa Day": { recovery: +2, time: "4 hours", cost: 200 },
  "Vacation Week": { recovery: +3, time: "1 week", cost: 1000 }
};
```

### Mental Meter Recovery

```javascript
const MENTAL_RECOVERY = {
  "Mental Health Day": { recovery: +1, time: "1 day" },
  "Therapy Session": { recovery: +1.5, time: "1 hour", cost: 150 },
  "Meditation Practice": { recovery: +0.5, time: "30 min" },
  "Nature Walk": { recovery: +1, time: "2 hours" },
  "Digital Detox Weekend": { recovery: +2, time: "2 days" },
  "Sabbatical": { recovery: +4, time: "4 weeks", requires: "savings" }
};
```

### Social Meter Recovery

```javascript
const SOCIAL_RECOVERY = {
  "Coffee with Friend": { recovery: +0.5, time: "1 hour" },
  "Dinner Party": { recovery: +1.5, time: "4 hours", cost: 50 },
  "Weekend Trip with Friends": { recovery: +2.5, time: "2 days", cost: 300 },
  "Join Community Group": { recovery: +2, time: "ongoing" },
  "Reconnect with Old Friend": { recovery: +1, time: "2 hours" }
};
```

### Emotional Meter Recovery

```javascript
const EMOTIONAL_RECOVERY = {
  "Therapy": { recovery: +1.5, time: "1 hour", cost: 150 },
  "Fulfilling Activity": { recovery: +1, time: "varies" },
  "Aspiration Progress": { recovery: +2, time: "varies" },
  "Deep Conversation": { recovery: +1, time: "2 hours" },
  "Creative Expression": { recovery: +1.5, time: "3 hours" },
  "Gratitude Practice": { recovery: +0.5, time: "15 min" }
};
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
- [x] **Dramatic irony mechanics used when knowledge gaps exist (score ≥ 0.6)**
- [x] **Memory resonance factors applied to recall (weights: 0.7-0.95)**
- [x] **Novel-quality thresholds met (≥ 0.7 overall; authenticity ≥ 0.7; tension ≥ 0.6; hooks ≥ 0.6)**
- [x] This doc cites **Truths v1.2** at the top

**Master Truths v1.2 Enhancements Implemented:**
- ✅ Emotional Capacity system with calculation formulas (Section 16)
- ✅ Circumstance stacking penalties on capacity
- ✅ Capacity thresholds and support availability checks (capacity ≥ need + 2 rule)
- ✅ Capacity recovery mechanics
- ✅ Support quality ratings based on capacity buffer

**References:**
- See `12-success-probability-formulas.md` for exact meter modifier calculations
- See `14-emotional-state-mechanics.md` for meter-triggered emotional states and circumstance stacking
- See `71-daily-turn-flow-detailed.md` for when meters are checked
- See `33-dialogue-generation-templates.md` for capacity-gated dialogue responses
- See `7.schema/04-gameplay-mechanics.md` for MeterState TypeScript interface

---

**This specification enables developers to implement complete meter threshold effects with exact modifiers, emotional capacity constraints, and recovery mechanics from Master Truths v1.2.**

