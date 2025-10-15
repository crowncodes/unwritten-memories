# Success Probability Formulas - Implementation Specification

**Compliance:** `master_truths_canonical_spec_v_1_2.md` (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Exact mathematical formulas for success probability calculations

**References:**
- **Design Philosophy:** `1.concept/12-card-evolution.md` (WHY success/failure matters)
- **Resource Economy:** `11-turn-economy-implementation.md` (resource costs)
- **Emotional States:** `14-emotional-state-mechanics.md` (state modifiers)

---

## Overview

Success probability determines whether card plays succeed, partially succeed, or fail. This creates **risk/reward tension** and makes **player choices, personality, and skills mechanically meaningful**.

**Core Principle:** Success is NEVER guaranteed (min 5%) and NEVER impossible (max 95%). This maintains drama and unpredictability.

---

## Base Success Calculation

### Formula

```javascript
function calculateSuccessChance(activity, player) {
  // 1. Start with activity's base rate
  let successChance = activity.baseSuccessRate || 0.70; // 70% default
  
  // 2. Apply personality alignment
  const personalityMod = calculatePersonalityModifier(activity, player.personality);
  successChance += personalityMod; // Range: -0.25 to +0.25
  
  // 3. Apply skill bonus
  const skillMod = calculateSkillModifier(activity, player.skills);
  successChance += skillMod; // Range: 0 to +0.50
  
  // 4. Apply meter effects
  const meterMod = calculateMeterModifier(activity, player.meters);
  successChance += meterMod; // Range: -0.30 to +0.15
  
  // 5. Apply emotional state
  const emotionMod = calculateEmotionalModifier(player.emotionalState, activity);
  successChance += emotionMod; // Range: -0.20 to +0.20
  
  // 6. Apply relationship bonus (if relevant)
  const relationshipMod = calculateRelationshipModifier(activity, player);
  successChance += relationshipMod; // Range: 0 to +0.30
  
  // 7. Apply environmental factors
  const environmentMod = calculateEnvironmentModifier(activity, player);
  successChance += environmentMod; // Range: -0.15 to +0.15
  
  // 8. Apply memory resonance (NEW - Master Truths v1.2)
  const memoryMod = calculateMemoryResonanceModifier(activity, player);
  successChance += memoryMod; // Range: -0.20 to +0.15
  
  // 9. Apply emotional capacity effects (NEW - Master Truths v1.2)
  const capacityMod = calculateCapacityModifier(player);
  successChance += capacityMod; // Range: -0.15 to +0.05
  
  // 10. Apply circumstance stacking penalty (NEW - Master Truths v1.2)
  const stackingPenalty = calculateStackingPenalty(player.activeStressors);
  successChance -= stackingPenalty; // Range: 0 to -0.25
  
  // 11. Clamp to valid range
  return Math.max(0.05, Math.min(0.95, successChance));
}
```

---

## Component Calculations

### 1. Personality Alignment Modifier

**Purpose:** Make personality mechanically meaningful - activities aligned with personality are easier.

```javascript
function calculatePersonalityModifier(activity, personality) {
  let modifier = 0;
  
  // OPENNESS (affects new/novel activities)
  if (activity.tags.includes('new') || activity.tags.includes('unfamiliar')) {
    const opennessAlign = (personality.openness - 3.0) / 10; // -0.20 to +0.20
    modifier += opennessAlign;
  }
  
  // CONSCIENTIOUSNESS (affects planning/organization activities)
  if (activity.tags.includes('planning') || activity.tags.includes('detailed')) {
    const conscientiousnessAlign = (personality.conscientiousness - 3.0) / 10;
    modifier += conscientiousnessAlign;
  }
  
  // EXTRAVERSION (affects social activities)
  if (activity.socialLevel === 'high' || activity.tags.includes('social')) {
    const extraversionAlign = (personality.extraversion - 3.0) / 10;
    modifier += extraversionAlign;
  }
  
  // AGREEABLENESS (affects cooperation/teamwork)
  if (activity.tags.includes('cooperation') || activity.tags.includes('teamwork')) {
    const agreeablenessAlign = (personality.agreeableness - 3.0) / 10;
    modifier += agreeablenessAlign;
  }
  
  // NEUROTICISM (INVERSE for high-stress activities)
  if (activity.stressLevel === 'high' || activity.tags.includes('pressure')) {
    const neuroticismPenalty = (personality.neuroticism - 3.0) / 10;
    modifier -= neuroticismPenalty; // High neuroticism = penalty
  }
  
  // Clamp personality modifier to ±0.25
  return Math.max(-0.25, Math.min(0.25, modifier));
}
```

**Examples:**
```javascript
// Low openness (2.0) doing new activity
personality.openness = 2.0;
activity.tags = ['new'];
// Modifier: (2.0 - 3.0) / 10 = -0.10 (10% penalty)

// High extraversion (4.5) at party
personality.extraversion = 4.5;
activity.socialLevel = 'high';
// Modifier: (4.5 - 3.0) / 10 = +0.15 (15% bonus)

// High neuroticism (4.2) under pressure
personality.neuroticism = 4.2;
activity.stressLevel = 'high';
// Modifier: -((4.2 - 3.0) / 10) = -0.12 (12% penalty)
```

---

### 2. Skill Modifier

**Purpose:** Make skill progression mechanically rewarding - higher skills = better success.

```javascript
function calculateSkillModifier(activity, skills) {
  if (!activity.relatedSkill) return 0;
  
  const skillLevel = skills[activity.relatedSkill] || 0; // 0-10
  
  // Each skill level = +5% success
  const skillBonus = skillLevel * 0.05;
  
  // Max bonus: +50% at Level 10
  return Math.min(0.50, skillBonus);
}
```

**Skill Progression Table:**
```
Skill Level  | Bonus | Example Success Rate (70% base)
-------------|-------|--------------------------------
0 (Novice)   | +0%   | 70%
1-2 (Beginner)| +5-10%| 75-80%
3-4 (Competent)| +15-20%| 85-90%
5-6 (Proficient)| +25-30%| 95% (capped)
7-8 (Expert) | +35-40%| 95% (capped)
9-10 (Master)| +45-50%| 95% (capped)
```

**Note:** Skill bonus is most impactful for difficult tasks (low base rate).

---

### 3. Meter Effects Modifier

**Purpose:** Physical/mental/social/emotional state affects performance.

```javascript
function calculateMeterModifier(activity, meters) {
  let modifier = 0;
  
  // PHYSICAL METER (affects physical activities)
  if (activity.physicalDemand === 'high') {
    if (meters.physical <= 2) {
      modifier -= 0.20; // Exhausted: -20%
    } else if (meters.physical <= 4) {
      modifier -= 0.10; // Tired: -10%
    } else if (meters.physical >= 8) {
      modifier += 0.10; // Energized: +10%
    }
  }
  
  // MENTAL METER (affects cognitive activities)
  if (activity.mentalDemand === 'high') {
    if (meters.mental <= 2) {
      modifier -= 0.20; // Burned out: -20%
    } else if (meters.mental <= 4) {
      modifier -= 0.10; // Foggy: -10%
    } else if (meters.mental >= 8) {
      modifier += 0.10; // Sharp: +10%
    }
  }
  
  // SOCIAL METER (affects social activities)
  if (activity.socialLevel === 'high') {
    if (meters.social <= 2) {
      modifier -= 0.15; // Isolated: -15%
    } else if (meters.social >= 8) {
      modifier += 0.10; // Connected: +10%
    }
  }
  
  // EMOTIONAL METER (affects all activities when extreme)
  if (meters.emotional <= 2) {
    modifier -= 0.15; // Distressed: -15% to everything
  } else if (meters.emotional >= 8) {
    modifier += 0.05; // Content: +5% to everything
  }
  
  // Clamp total meter modifier
  return Math.max(-0.30, Math.min(0.15, modifier));
}
```

**Meter Threshold Effects:**
```
Physical Meter:
0-2: EXHAUSTED    (-20% physical activities)
3-4: TIRED        (-10% physical activities)
5-7: NORMAL       (no modifier)
8-10: ENERGIZED   (+10% physical activities)

Mental Meter:
0-2: BURNED OUT   (-20% cognitive activities)
3-4: FOGGY        (-10% cognitive activities)
5-7: NORMAL       (no modifier)
8-10: SHARP       (+10% cognitive activities)

Social Meter:
0-2: ISOLATED     (-15% social activities)
3-4: LONELY       (-5% social activities)
5-7: NORMAL       (no modifier)
8-10: CONNECTED   (+10% social activities)

Emotional Meter:
0-2: DISTRESSED   (-15% ALL activities)
3-4: STRUGGLING   (-5% ALL activities)
5-7: NORMAL       (no modifier)
8-10: CONTENT     (+5% ALL activities)
```

---

### 4. Emotional State Modifier

**Purpose:** Current emotional state affects specific activity types.

```javascript
function calculateEmotionalModifier(emotionalState, activity) {
  if (!emotionalState) return 0;
  
  // Emotional state effect tables
  const EMOTIONAL_EFFECTS = {
    // Positive states
    CONFIDENT: {
      social: +0.15,
      challenging: +0.10,
      default: +0.05
    },
    INSPIRED: {
      creative: +0.20,
      learning: +0.10,
      default: +0.05
    },
    ENERGIZED: {
      physical: +0.15,
      active: +0.10,
      default: +0.05
    },
    FOCUSED: {
      cognitive: +0.20,
      detailed: +0.15,
      default: +0.05
    },
    
    // Negative states
    ANXIOUS: {
      social: -0.15,
      challenging: -0.10,
      routine: -0.05
    },
    EXHAUSTED: {
      physical: -0.20,
      cognitive: -0.15,
      default: -0.10
    },
    OVERWHELMED: {
      complex: -0.20,
      multi_step: -0.15,
      default: -0.10
    },
    DISCOURAGED: {
      challenging: -0.15,
      new: -0.10,
      default: -0.05
    },
    MELANCHOLY: {
      social: -0.10,
      upbeat: -0.15,
      default: -0.05
    }
  };
  
  const stateEffects = EMOTIONAL_EFFECTS[emotionalState];
  if (!stateEffects) return 0;
  
  // Check activity tags for matching effect
  for (const [tag, modifier] of Object.entries(stateEffects)) {
    if (tag === 'default') continue;
    if (activity.tags.includes(tag) || activity[tag] === true) {
      return modifier;
    }
  }
  
  // Default effect
  return stateEffects.default || 0;
}
```

**Examples:**
```javascript
// CONFIDENT state doing social activity
emotionalState = 'CONFIDENT';
activity.tags = ['social'];
// Modifier: +0.15 (15% bonus)

// ANXIOUS state doing challenging activity
emotionalState = 'ANXIOUS';
activity.tags = ['challenging'];
// Modifier: -0.10 (10% penalty)

// INSPIRED state doing creative work
emotionalState = 'INSPIRED';
activity.tags = ['creative'];
// Modifier: +0.20 (20% bonus!)
```

---

### 5. Relationship Modifier

**Purpose:** Doing activities WITH friends/partners increases success.

```javascript
function calculateRelationshipModifier(activity, player) {
  if (!activity.involvesTags) return 0;
  
  let modifier = 0;
  
  // Check if activity involves NPCs
  for (const npcId of activity.involvesTags) {
    const relationship = player.relationships[npcId];
    if (!relationship) continue;
    
    // Relationship level bonus
    const levelBonus = relationship.level * 0.03; // +3% per level
    
    // Trust bonus (only if Level 3+)
    const trustBonus = relationship.level >= 3
      ? relationship.trust * 0.10
      : 0;
    
    // Social capital bonus (positive balance helps)
    const socialCapitalBonus = relationship.socialCapital > 0
      ? Math.min(relationship.socialCapital * 0.02, 0.05)
      : 0;
    
    modifier += levelBonus + trustBonus + socialCapitalBonus;
  }
  
  // Max +30% total from relationships
  return Math.min(0.30, modifier);
}
```

**Relationship Bonus Table:**
```
Level 0 (Not Met):      +0%
Level 1 (Stranger):     +3%
Level 2 (Acquaintance): +6%
Level 3 (Friend):       +9% + trust bonus (up to +10%)
Level 4 (Close Friend): +12% + trust bonus (up to +10%)
Level 5 (Soulmate):     +15% + trust bonus (up to +10%)

Max possible relationship bonus: +30%
(Level 5 + max trust + positive social capital)
```

---

### 6. Environment Modifier

**Purpose:** Time of day, weather, location affect success.

```javascript
function calculateEnvironmentModifier(activity, player) {
  let modifier = 0;
  
  // TIME OF DAY
  if (activity.preferredTime) {
    const currentPhase = player.currentPhase; // 'morning', 'afternoon', 'evening'
    if (currentPhase === activity.preferredTime) {
      modifier += 0.10; // Right time: +10%
    } else if (activity.preferredTime === 'morning' && currentPhase === 'evening') {
      modifier -= 0.10; // Wrong time: -10%
    }
  }
  
  // LOCATION MATCH
  if (activity.preferredLocation) {
    const currentLocation = player.currentLocation;
    if (currentLocation === activity.preferredLocation) {
      modifier += 0.10; // Right place: +10%
    } else if (activity.requiresLocation === activity.preferredLocation) {
      modifier -= 0.15; // Wrong place for required location: -15%
    }
  }
  
  // WEATHER (if activity is outdoors)
  if (activity.tags.includes('outdoor')) {
    const weather = player.currentWeather;
    if (weather === 'rain' || weather === 'storm') {
      modifier -= 0.10; // Bad weather: -10%
    } else if (weather === 'clear' || weather === 'sunny') {
      modifier += 0.05; // Good weather: +5%
    }
  }
  
  // Clamp environment modifier
  return Math.max(-0.15, Math.min(0.15, modifier));
}
```

---

### 7. Memory Resonance Modifier *(NEW - Master Truths v1.2)*

**Purpose:** Past experiences with similar activities affect success through memory resonance.

**Master Truths v1.2, Section 17:**
> "Memory Resonance Factors: 0.7-0.95 weights based on emotional impact and context relevance"

```javascript
function calculateMemoryResonanceModifier(activity, player) {
  // Search for memories related to this activity type
  const relevantMemories = player.memoryArchive.filter(memory => 
    memory.tags.some(tag => activity.tags.includes(tag)) ||
    memory.category === activity.category
  );
  
  if (relevantMemories.length === 0) return 0;
  
  let modifier = 0;
  
  // Process up to 3 most relevant memories
  const topMemories = relevantMemories
    .sort((a, b) => b.emotional_weight - a.emotional_weight)
    .slice(0, 3);
  
  topMemories.forEach(memory => {
    // Calculate resonance weight (0.7-0.95 based on relevance)
    const resonanceWeight = calculateResonanceWeight(memory, activity);
    
    // Apply memory effect based on outcome
    if (memory.outcome === 'success' || memory.outcome === 'breakthrough') {
      // Positive memory: confidence boost
      const boost = memory.emotional_weight * resonanceWeight * 0.10;
      modifier += boost;  // Max +0.15 from strong positive memory
    } else if (memory.outcome === 'failure' || memory.outcome === 'trauma') {
      // Negative memory: anxiety/doubt
      const penalty = memory.emotional_weight * resonanceWeight * 0.12;
      modifier -= penalty;  // Max -0.20 from traumatic memory
    }
  });
  
  // Clamp total memory modifier
  return Math.max(-0.20, Math.min(0.15, modifier));
}

function calculateResonanceWeight(memory, activity) {
  let weight = 0.70;  // Base resonance
  
  // EXACT MATCH: Same activity
  if (memory.activity_id === activity.id) {
    weight = 0.95;  // Highest resonance
  }
  // CATEGORY MATCH: Similar activity type
  else if (memory.category === activity.category) {
    weight = 0.85;
  }
  // TAG OVERLAP: Some shared elements
  else {
    const tagOverlap = memory.tags.filter(tag => 
      activity.tags.includes(tag)
    ).length;
    weight = 0.70 + (tagOverlap * 0.03);  // +3% per shared tag
  }
  
  // RECENCY BONUS: Recent memories more impactful
  const weeksSince = getWeeksSince(memory.date, currentDate);
  if (weeksSince < 4) {
    weight += 0.05;  // Recent memory
  } else if (weeksSince > 26) {
    weight -= 0.05;  // Old memory fading
  }
  
  // Clamp to 0.70-0.95 range (Master Truths v1.2 requirement)
  return Math.max(0.70, Math.min(0.95, weight));
}
```

**Examples:**

```javascript
// SCENARIO 1: Previous Success Memory
const memory = {
  activity_id: "public_speaking_presentation",
  category: "public_speaking",
  tags: ["professional", "high_stakes"],
  outcome: "success",
  emotional_weight: 0.85,
  date: "4 weeks ago"
};

const currentActivity = {
  id: "public_speaking_workshop",
  category: "public_speaking",
  tags: ["professional", "learning"]
};

// Calculate resonance
const resonanceWeight = 0.85;  // Category match + recency
const modifier = 0.85 * 0.85 * 0.10 = +0.072 (+7.2% boost)
// Memory: "Last time you spoke publicly, it went great. You can do this."

// SCENARIO 2: Traumatic Failure Memory
const traumaMemory = {
  activity_id: "audition_theater",
  category: "performance",
  tags: ["public", "vulnerable", "creative"],
  outcome: "trauma",
  emotional_weight: 0.92,
  date: "8 weeks ago"
};

const auditionActivity = {
  id: "audition_film",
  category: "performance",
  tags: ["public", "vulnerable"]
};

// Calculate resonance
const resonanceWeight = 0.88;  // Category match + tag overlap
const modifier = -(0.92 * 0.88 * 0.12) = -0.097 (-9.7% penalty)
// Memory: "The audition. That memory still stings. What if it happens again?"
```

---

### 8. Emotional Capacity Modifier *(NEW - Master Truths v1.2)*

**Purpose:** Character's emotional capacity affects performance on emotionally demanding activities.

```javascript
function calculateCapacityModifier(player) {
  // Calculate current emotional capacity (see 13-meter-effects-tables.md)
  const capacity = calculateEmotionalCapacity(
    player.meters,
    player.activeStressors
  );
  
  let modifier = 0;
  
  // LOW CAPACITY (0-4.0): Struggling affects performance
  if (capacity <= 2.0) {
    modifier = -0.15;  // Depleted: -15%
  } else if (capacity <= 4.0) {
    modifier = -0.08;  // Low: -8%
  }
  // MODERATE CAPACITY (4.1-6.0): No effect
  else if (capacity <= 6.0) {
    modifier = 0;      // Normal: no change
  }
  // HIGH CAPACITY (6.1+): Extra bandwidth helps
  else if (capacity <= 8.0) {
    modifier = +0.03;  // High: +3%
  } else {
    modifier = +0.05;  // Peak: +5%
  }
  
  return modifier;
}
```

**Capacity Impact on Activities:**

```javascript
const CAPACITY_SENSITIVE_ACTIVITIES = {
  emotionally_demanding: {
    // Activities that require emotional bandwidth
    examples: [
      "deep_conversation",
      "provide_support",
      "confront_conflict",
      "express_vulnerability",
      "process_grief"
    ],
    capacity_effect: "double",  // 2x the capacity modifier
    narrative: "This requires emotional energy you might not have right now."
  },
  
  emotionally_neutral: {
    // Activities not affected by capacity
    examples: [
      "exercise",
      "technical_work",
      "routine_tasks",
      "hobbies"
    ],
    capacity_effect: "none",
    narrative: "This doesn't require much emotional bandwidth."
  }
};

function applyCapacityToActivity(baseModifier, activity) {
  if (activity.emotionally_demanding) {
    return baseModifier * 2.0;  // Double effect for emotional activities
  }
  return baseModifier;
}
```

---

### 9. Circumstance Stacking Penalty *(NEW - Master Truths v1.2)*

**Purpose:** Multiple simultaneous stressors compound to reduce success rates.

**Master Truths v1.2, Section 16:**
> "Circumstance Stacking: When multiple life stressors occur simultaneously, effects compound rather than add linearly."

```javascript
function calculateStackingPenalty(activeStressors) {
  const stressorCount = countActiveStressors(activeStressors);
  
  // Progressive penalty based on stressor count
  const STACKING_PENALTIES = {
    0: 0.00,    // No stressors
    1: 0.00,    // Single stressor (manageable)
    2: 0.05,    // -5% (starting to feel it)
    3: 0.12,    // -12% (juggling multiple issues)
    4: 0.20,    // -20% (seriously struggling)
    5: 0.25     // -25% (overwhelmed - capped)
  };
  
  return STACKING_PENALTIES[Math.min(5, stressorCount)];
}

// Count active stressors
function countActiveStressors(stressors) {
  let count = 0;
  
  if (stressors.workPressure > 7) count++;
  if (stressors.moneyStress && player.money < 500) count++;
  if (stressors.relationshipTension.length >= 2) count++;
  if (stressors.healthIssues && player.meters.physical < 4) count++;
  if (stressors.familyCrisis) count++;
  if (stressors.housingIssues) count++;
  if (stressors.aspirationDeadline && stressors.aspirationProgress < 0.5) count++;
  
  return count;
}
```

**Stacking Impact Examples:**

```javascript
// SCENARIO A: Single Stressor (Manageable)
const singleStressor = {
  workPressure: 8,  // High work stress
  // Everything else fine
};
// Penalty: 0% (single issues are manageable)

// SCENARIO B: Three Stressors (Compounding)
const tripleStressor = {
  workPressure: 8,          // Work deadline
  moneyStress: true,        // Rent due, low funds
  relationshipTension: [    // Two relationships strained
    "sarah_tension",
    "marcus_tension"
  ]
};
// Penalty: -12% (everything at once is harder)
// Narrative: "You're juggling too much. Work. Money. Relationships. Each thing alone would be manageable, but all together..."

// SCENARIO C: Five Stressors (Overwhelmed)
const overwhelmed = {
  workPressure: 9,
  moneyStress: true,
  relationshipTension: ["sarah_tension", "elena_tension"],
  healthIssues: true,
  familyCrisis: true,
  aspirationDeadline: true,
  aspirationProgress: 0.3
};
// Penalty: -25% (maximum - capped)
// Narrative: "Everything is falling apart at once. When it rains, it pours."
```

---

### 10. Personality-Based Tension Perception *(NEW - Master Truths v1.2)*

**Purpose:** Personality affects how characters perceive and handle tension/risk.

```javascript
function calculateTensionPerceptionModifier(activity, personality) {
  if (!activity.tension_level) return 0;
  
  let modifier = 0;
  
  // HIGH NEUROTICISM: Tension feels worse
  if (personality.neuroticism > 3.5 && activity.tension_level >= 0.6) {
    const neuroticismEffect = (personality.neuroticism - 3.5) * 0.04;
    modifier -= neuroticismEffect;  // Up to -10% for neuroticism 6.0
  }
  
  // LOW NEUROTICISM: Handles tension better
  if (personality.neuroticism < 2.5 && activity.tension_level >= 0.6) {
    const stabilityBonus = (2.5 - personality.neuroticism) * 0.03;
    modifier += stabilityBonus;  // Up to +7.5% for neuroticism 0
  }
  
  // HIGH OPENNESS: Comfortable with uncertainty
  if (personality.openness > 4.0 && activity.tags.includes('uncertain')) {
    modifier += 0.05;  // +5% for high openness
  }
  
  return Math.max(-0.10, Math.min(0.08, modifier));
}
```

---

## Risk Modifiers (Player Choice)

Players can choose risk level when playing cards:

```javascript
const RISK_OPTIONS = {
  play_it_safe: {
    successModifier: +0.15,      // +15% success
    rewardMultiplier: 0.60,      // 60% rewards
    timeMultiplier: 1.20,        // 20% longer
    energyCostMultiplier: 0.80,  // 20% less energy
    description: "Cautious approach - lower risk, lower reward"
  },
  
  standard: {
    successModifier: 0,
    rewardMultiplier: 1.0,
    timeMultiplier: 1.0,
    energyCostMultiplier: 1.0,
    description: "Normal approach - balanced risk and reward"
  },
  
  go_for_it: {
    successModifier: -0.15,      // -15% success
    rewardMultiplier: 1.50,      // 150% rewards (+50%)
    timeMultiplier: 0.90,        // 10% faster
    energyCostMultiplier: 1.20,  // 20% more energy
    description: "Ambitious approach - higher risk, higher reward"
  }
};
```

**When to Use:**
- **Play It Safe:** When you can't afford failure (low savings, crisis situation)
- **Standard:** Default balanced approach
- **Go For It:** When rewards matter more than risk (trying to impress, need breakthrough)

---

## Success Resolution Tiers

After calculating final success chance, roll determines outcome:

```javascript
function resolveSuccess(successChance) {
  const roll = Math.random(); // 0.0 to 1.0
  
  if (roll < successChance) {
    // SUCCESS (within success range)
    return {
      result: "success",
      quality: getSuccessQuality(roll, successChance),
      narrative: "success_narrative",
      applyRewards: "full"
    };
  } else if (roll < successChance + 0.15) {
    // PARTIAL SUCCESS (within 15% margin)
    return {
      result: "partial",
      quality: "mixed",
      narrative: "partial_narrative",
      applyRewards: "reduced",  // 50% rewards
      applyPenalties: "minor"   // Minor penalties
    };
  } else {
    // FAILURE (beyond partial range)
    return {
      result: "failure",
      quality: getFailureQuality(roll, successChance),
      narrative: "failure_narrative",
      applyPenalties: "full"
    };
  }
}

function getSuccessQuality(roll, successChance) {
  const margin = successChance - roll;
  if (margin > 0.30) return "exceptional"; // Way above needed
  if (margin > 0.15) return "strong";      // Comfortably above
  return "close";                          // Barely made it
}

function getFailureQuality(roll, successChance) {
  const margin = roll - (successChance + 0.15);
  if (margin > 0.30) return "catastrophic"; // Badly failed
  if (margin > 0.15) return "significant";  // Clear failure
  return "narrow";                          // Just missed
}
```

**Outcome Distribution Example (70% base success):**
```
0-70%:    SUCCESS (70% chance)
70-85%:   PARTIAL SUCCESS (15% chance)
85-100%:  FAILURE (15% chance)
```

---

## Complete Example Calculation

**Scenario:** Hot Yoga Class (First Time)

```javascript
const ACTIVITY = {
  id: "hot_yoga_first_class",
  baseSuccessRate: 0.40,  // Challenging!
  tags: ['physical', 'new', 'challenging'],
  physicalDemand: 'high',
  relatedSkill: 'flexibility',
  preferredTime: 'morning'
};

const PLAYER = {
  personality: {
    openness: 2.1,         // Low! Uncomfortable with new
    neuroticism: 3.8       // Slightly high
  },
  skills: {
    flexibility: 0         // Never done this
  },
  meters: {
    physical: 7,           // Decent shape
    mental: 5,
    emotional: 6
  },
  emotionalState: 'ANXIOUS',
  currentPhase: 'morning'
};

// CALCULATION:
let successChance = 0.40; // Base 40%

// 1. Personality modifier
// - Low openness (2.1) doing new activity: (2.1 - 3.0)/10 = -0.09
// - High neuroticism (3.8) in challenging: -((3.8 - 3.0)/10) = -0.08
// Total personality: -0.17 (-17%)
successChance += -0.17; // Now 23%

// 2. Skill modifier
// - Flexibility skill 0: +0%
successChance += 0; // Still 23%

// 3. Meter modifier
// - Physical 7 in high-demand: no modifier
successChance += 0; // Still 23%

// 4. Emotional modifier
// - ANXIOUS doing challenging: -0.10 (-10%)
successChance += -0.10; // Now 13%

// 5. Relationship modifier
// - No NPCs involved: +0%
successChance += 0; // Still 13%

// 6. Environment modifier
// - Morning activity in morning phase: +0.10 (+10%)
successChance += 0.10; // Now 23%

// 7. Clamp to 5-95%
successChance = Math.max(0.05, Math.min(0.95, 0.23)); // 23%

// FINAL SUCCESS CHANCE: 23%
```

**Player Options:**
```
PLAY IT SAFE (+15%):  38% success, 60% rewards
STANDARD:             23% success, 100% rewards
GO FOR IT (-15%):     8% success (clamped to 5%), 150% rewards
```

**Recommendation:** This is genuinely risky! Player should either:
1. Play it safe (38% still tough but fair)
2. Bring a friend (can add +20% modifier)
3. Try beginner class instead (easier base rate)

---

## Worked Examples by Activity Type

### Social Activity (Party)

```javascript
baseSuccess: 0.70
personality: extraversion 4.2 → +0.12
skill: social_skills 4 → +0.20
meters: social 8 → +0.10
emotional: CONFIDENT → +0.15
relationship: host Level 4, trust 0.75 → +0.19
environment: evening (preferred) → +0.10

FINAL: 70% + 86% modifiers = 95% (capped) ✓ Easy win
```

### Cognitive Activity (Programming)

```javascript
baseSuccess: 0.60
personality: conscientiousness 3.8 → +0.08
skill: programming 6 → +0.30
meters: mental 3 → -0.10
emotional: FOCUSED → +0.20
environment: morning (preferred) → +0.10

FINAL: 60% + 58% modifiers = 95% (capped) ✓ Skilled success
```

### Physical Challenge (Marathon)

```javascript
baseSuccess: 0.30  // Very hard!
personality: conscientiousness 4.5 → +0.15
skill: running 8 → +0.40
meters: physical 2 → -0.20
emotional: EXHAUSTED → -0.20
environment: weather rain → -0.10

FINAL: 30% + 5% modifiers = 35% ⚠️ Tough but possible
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
- ✅ Memory resonance modifiers (0.7-0.95 weight range, Section 17)
- ✅ Emotional capacity effects on success rates
- ✅ Circumstance stacking penalties (0% to -25%)
- ✅ Personality-based tension perception modifiers
- ✅ Capacity-sensitive activity differentiation

**References:**
- See `13-meter-effects-tables.md` for emotional capacity calculations
- See `14-emotional-state-mechanics.md` for all emotional state modifiers and circumstance stacking
- See `38-emotional-memory-tracking.md` for memory resonance weights
- See `44-relationship-progression-spec.md` for relationship bonuses

---

**This specification enables developers to implement the complete success probability system with exact formulas including Master Truths v1.2 emotional authenticity mechanics.**

