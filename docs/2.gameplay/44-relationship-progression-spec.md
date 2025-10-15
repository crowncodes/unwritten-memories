# Relationship Progression Specification - Implementation

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete implementation of relationship levels 0-5 with NPC capacity tracking, support mechanics, and dramatic irony opportunities

**References:**
- **Design Philosophy:** `1.concept/13-ai-personality-system.md` (WHY relationships matter)
- **Schema Definition:** `7.schema/03-character-system.md` (RelationshipState interface)
- **Card System:** `20-base-card-catalog.md` (character cards)
- **Social Capital:** `11-turn-economy-implementation.md` (relationship currency)

---

## Overview

**Relationships** progress through **6 discrete levels (0-5)** based on **both interaction count AND trust threshold**. Level 0 ("Not Met") is tracked internally but never displayed to players.

**Core Principle:** Relationships require both quantity (interactions) and quality (trust). High trust alone is insufficient—relationships need time. Many interactions with low trust is insufficient—relationships need genuine connection.

**Compliance:** master_truths v1.1 specifies "Levels: 0–5 (discrete stages; 0 = 'Not Met', tracked internally but never displayed as 'Level 0')" and "Level-Up Requirements: Both interaction count AND minimum trust threshold required."

---

## The 6 Relationship Levels

### Complete Level Structure

```typescript
enum RelationshipLevel {
  NOT_MET = 0,        // Never interacted (internal only)
  STRANGER = 1,       // First meeting through 5 interactions
  ACQUAINTANCE = 2,   // 6-15 interactions
  FRIEND = 3,         // 16-30 interactions
  CLOSE_FRIEND = 4,   // 31-75 interactions
  SOULMATE = 5        // 76+ interactions (or Best Friend)
}

interface RelationshipState {
  level: RelationshipLevel;
  trust: RangedFloat<0.0, 1.0>;
  interaction_count: number;
  
  // Derived
  display_name: string;            // Never "Level 0", show "Not Met"
  level_progress: RangedFloat<0.0, 1.0>;
  next_level_requirements: LevelRequirement;
  
  // History
  first_met: GameTime | null;
  relationship_age_weeks: number;
  major_moments: RelationshipMoment[];
}
```

---

## Level 0: NOT MET

**Display:** "Not Met" (NEVER show "Level 0")

**State:**
```javascript
{
  level: 0,
  trust: null,                       // No trust yet
  interaction_count: 0,
  first_met: null,
  
  gameplay_state: {
    card_in_deck: false,             // NPC card not yet acquired
    can_interact: false,             // Cannot play cards with this NPC
    appears_in_events: false,        // Won't appear in events
    tracked_in_archives: true        // But tracked as "potential NPC"
  },
  
  ui_display: {
    show_as: "Not Met",
    icon: "question_mark",
    tooltip: "You haven't met this person yet"
  }
}
```

**How to Progress to Level 1:**
- Must trigger "first meeting" event
- Usually through: new location unlock, introduction by mutual friend, event attendance, quest trigger
- First meeting is ALWAYS a special interaction (generates unique narrative)

**First Meeting Mechanics:**
```javascript
function triggerFirstMeeting(npc, context) {
  return {
    event_type: "FIRST_MEETING",
    narrative_special: true,          // Always gets custom narrative
    trust_initial: 0.1,               // Start at 10% trust
    interaction_count: 1,             // This counts as interaction #1
    level: 1,                         // Immediately becomes STRANGER
    
    memory_created: {
      type: "first_meeting",
      weight: 0.7,                    // Important memory
      never_forgotten: true           // First meetings always remembered
    },
    
    card_acquired: {
      npc_card: npc.card_id,
      rarity: npc.rarity,
      added_to_deck: true
    }
  };
}
```

---

## Level 1: STRANGER

**Display:** "Stranger" (Level 1)

**Requirements:**
```javascript
{
  min_interactions: 0,               // First meeting = Level 1
  max_interactions: 5,
  min_trust: 0.0,
  max_trust: 0.2,                    // Caps at 20% trust while Stranger
  
  typical_trust_range: "0.05-0.15"
}
```

**Relationship Characteristics:**
```javascript
{
  interaction_type: "surface_level",
  typical_duration: "1-3 weeks",     // Usually progress quickly
  conversation_depth: "small_talk",
  
  available_activities: [
    "coffee_casual",
    "group_event_together",
    "brief_conversation",
    "wave_hello"
  ],
  
  unavailable_activities: [
    "deep_conversation",              // Too soon
    "ask_personal_favor",            // Not close enough
    "share_vulnerability",           // Would be weird
    "hang_out_alone"                 // Need more comfort
  ],
  
  social_capital: {
    max: 2,                          // Can't earn much yet
    asking_favor_cost: 3,            // Very expensive to ask favors
    earning_rate: 0.5                // Slow to build
  }
}
```

**Level-Up to Acquaintance:**
```javascript
{
  required_interactions: 6,          // At least 6 interactions
  required_trust: 0.15,              // At least 15% trust
  
  // BOTH must be met
  formula: "interactions >= 6 AND trust >= 0.15"
}
```

**Typical Progression:**
- Interaction 1-2: Polite small talk, surface info
- Interaction 3-4: Starting to remember details, share basic info
- Interaction 5-6: Enough rapport to move to Acquaintance

---

## Level 2: ACQUAINTANCE

**Display:** "Acquaintance" (Level 2)

**Requirements:**
```javascript
{
  min_interactions: 6,
  max_interactions: 15,
  min_trust: 0.15,                   // Must have at least 15% trust
  max_trust: 0.4,                    // Caps at 40% while Acquaintance
  
  typical_trust_range: "0.20-0.35"
}
```

**Relationship Characteristics:**
```javascript
{
  interaction_type: "friendly_casual",
  typical_duration: "3-6 weeks",
  conversation_depth: "getting_to_know_you",
  
  available_activities: [
    "lunch_together",
    "share_hobby_interest",
    "casual_hangout",
    "text_conversation",
    "attend_event_together"
  ],
  
  still_unavailable: [
    "ask_big_favor",
    "deep_vulnerability",
    "crisis_support",
    "introduce_to_family"
  ],
  
  social_capital: {
    max: 5,
    asking_favor_cost: 2,            // Moderate cost
    earning_rate: 0.8
  },
  
  memory_threshold: 0.5,             // Memories stick better now
  personality_visible: "surface"     // Starting to see personality
}
```

**Level-Up to Friend:**
```javascript
{
  required_interactions: 16,         // At least 16 interactions total
  required_trust: 0.30,              // At least 30% trust
  
  // AND one of:
  special_moments: [
    "shared_vulnerability",
    "helped_in_need",
    "consistent_presence",
    "memorable_experience_together"
  ],
  
  formula: "interactions >= 16 AND trust >= 0.30 AND special_moment_occurred"
}
```

**Typical Progression:**
- Interaction 6-9: Learning about each other's lives
- Interaction 10-13: Starting to rely on each other
- Interaction 14-16: Genuine friendship forming

---

## Level 3: FRIEND

**Display:** "Friend" (Level 3)

**Requirements:**
```javascript
{
  min_interactions: 16,
  max_interactions: 30,
  min_trust: 0.30,
  max_trust: 0.6,                    // Caps at 60% while Friend
  
  typical_trust_range: "0.40-0.55"
}
```

**Relationship Characteristics:**
```javascript
{
  interaction_type: "genuine_friendship",
  typical_duration: "8-15 weeks",
  conversation_depth: "personal_meaningful",
  
  available_activities: [
    "deep_conversation",
    "ask_moderate_favor",
    "hang_out_regularly",
    "share_problems",
    "celebrate_together",
    "introduce_to_other_friends",
    "weekend_activity",
    "mutual_support"
  ],
  
  still_unavailable: [
    "ask_huge_favor",
    "stay_at_their_place_week",
    "borrow_significant_money",
    "make_life_decisions_together"
  ],
  
  social_capital: {
    max: 8,
    asking_favor_cost: 1.5,          // Easier to ask
    earning_rate: 1.0,
    reciprocal_bonus: true           // They help you back
  },
  
  memory_threshold: 0.7,
  personality_visible: "deep",       // Know them well
  
  relationship_resilience: {
    can_survive_neglect: "2-3 weeks",
    trust_decay_rate: 0.01           // Slow decay
  }
}
```

**Level-Up to Close Friend:**
```javascript
{
  required_interactions: 31,         // At least 31 interactions
  required_trust: 0.50,              // At least 50% trust
  
  // AND at least two of:
  special_requirements: [
    "vulnerable_moment_shared",
    "crisis_supported",
    "consistent_presence_3_months",
    "life_milestone_together",
    "conflict_resolved",
    "trust_demonstrated"
  ],
  
  minimum_relationship_age: 12,      // At least 12 weeks minimum
  
  formula: "interactions >= 31 AND trust >= 0.50 AND special_requirements >= 2 AND weeks >= 12"
}
```

**Typical Progression:**
- Interaction 16-20: Deep trust building
- Interaction 21-25: Rely on each other
- Interaction 26-30: Genuine close bond

---

## Level 4: CLOSE FRIEND

**Display:** "Close Friend" (Level 4)

**Requirements:**
```javascript
{
  min_interactions: 31,
  max_interactions: 75,
  min_trust: 0.50,
  max_trust: 0.8,
  
  typical_trust_range: "0.60-0.75"
}
```

**Relationship Characteristics:**
```javascript
{
  interaction_type: "deep_bond",
  typical_duration: "15-30 weeks",
  conversation_depth: "complete_honesty",
  
  available_activities: [
    "ask_big_favor",
    "life_decision_consultation",
    "crisis_support",
    "vulnerable_sharing",
    "travel_together",
    "introduce_to_family",
    "borrow_money",
    "stay_at_place",
    "daily_contact"
  ],
  
  still_unavailable: [
    // Very little is unavailable at this level
    "expect_always_available",       // Still have boundaries
    "make_decisions_for_them"        // Respect autonomy
  ],
  
  social_capital: {
    max: 15,
    asking_favor_cost: 1,            // Very low cost
    earning_rate: 1.5,
    reciprocal_automatic: true       // They offer help unprompted
  },
  
  memory_threshold: 0.9,             // Remember everything
  personality_visible: "complete",
  
  relationship_resilience: {
    can_survive_neglect: "4-6 weeks",
    trust_decay_rate: 0.005,         // Very slow decay
    conflict_recovery: true          // Can recover from conflicts
  },
  
  special_features: {
    appears_in_major_decisions: true, // Included in big choices
    provides_perspective: true,      // Gives advice on life
    mutual_growth: true              // You grow together
  }
}
```

**Level-Up to Soulmate/Best Friend:**
```javascript
{
  required_interactions: 76,         // At least 76 interactions
  required_trust: 0.75,              // At least 75% trust
  
  // AND ALL of:
  special_requirements: [
    "multiple_crises_weathered",
    "consistent_presence_6_months",
    "life_changing_moments_together",
    "complete_trust_demonstrated",
    "mutual_vulnerability",
    "unbreakable_bond_evident"
  ],
  
  minimum_relationship_age: 24,      // At least 24 weeks (6 months)
  
  formula: "interactions >= 76 AND trust >= 0.75 AND all_special_requirements_met AND weeks >= 24"
}
```

**Typical Progression:**
- Interaction 31-45: Deep intimate friendship
- Interaction 46-60: Life intertwined
- Interaction 61-75: Unbreakable bond

---

## Level 5: SOULMATE / BEST FRIEND

**Display:** "Soulmate" or "Best Friend" (Level 5)

**Requirements:**
```javascript
{
  min_interactions: 76,
  max_interactions: Infinity,        // No upper limit
  min_trust: 0.75,
  max_trust: 1.0,
  
  typical_trust_range: "0.85-0.98"   // Rarely perfect 1.0
}
```

**Relationship Characteristics:**
```javascript
{
  interaction_type: "soul_connection",
  typical_duration: "indefinite",    // Lifelong
  conversation_depth: "complete_understanding",
  
  available_activities: [
    // EVERYTHING
    "anything",
    "life_partnership_decisions",
    "complete_vulnerability",
    "unconditional_support",
    "shared_life_journey",
    "family_level_bond"
  ],
  
  social_capital: {
    max: 25,
    asking_favor_cost: 0.5,          // Almost free
    earning_rate: 2.0,
    infinite_reciprocity: true,      // They'd do anything
    no_tracking_needed: true         // Beyond accounting
  },
  
  memory_threshold: 1.0,             // Never forget anything
  personality_visible: "soul_deep",  // Know them better than they know themselves
  
  relationship_resilience: {
    can_survive_neglect: "indefinite",
    trust_decay_rate: 0.0,           // Doesn't decay
    conflict_makes_stronger: true,   // Conflicts deepen bond
    unbreakable: true
  },
  
  special_features: {
    central_to_life_story: true,
    major_character_in_novel: true,
    life_changing_influence: true,
    mutual_transformation: true,
    legacy_relationship: true        // Remembered forever
  },
  
  rare_achievement: true,            // Hard to achieve
  max_count_recommended: 2-3         // Can't have 10 soulmates
}
```

**Maintenance:**
- Trust at this level is nearly unbreakable
- Even with neglect, drops slowly to Level 4 at worst
- Major betrayal could damage, but hard to destroy completely
- Often becomes lifelong relationship

**Special Statuses Possible:**
```javascript
const LEVEL_5_STATUSES = {
  "Life Partnership": "Married or equivalent committed partnership",
  "Best Friend Forever": "Platonic soulmate",
  "Found Family": "Chosen family member",
  "Ride or Die": "Unbreakable loyalty",
  "Kindred Spirit": "Deep spiritual/intellectual connection"
};
```

---

## Level-Up Mechanics

### Interaction Counting

**What Counts as an Interaction:**
```javascript
const INTERACTION_TYPES = {
  full_interaction: 1.0,             // Normal interaction
  brief_interaction: 0.5,            // Quick chat, text
  group_interaction: 0.7,            // With others present
  deep_interaction: 1.5,             // Deep conversation, vulnerable moment
  crisis_interaction: 2.0,           // Supporting in crisis
  
  // Special
  first_meeting: 1.0,                // First meeting always counts as 1
  life_milestone: 2.0,               // Wedding, funeral, birth, etc.
  conflict: -0.5                     // Arguments subtract (but can strengthen later)
};
```

**Interaction Frequency Effects:**
```javascript
function calculateInteractionQuality(frequency, consistency) {
  // Regular interactions build trust faster
  if (frequency === "daily" && consistency > 0.8) {
    return { trust_gain_multiplier: 1.5 };
  }
  if (frequency === "weekly" && consistency > 0.7) {
    return { trust_gain_multiplier: 1.2 };
  }
  if (frequency === "sporadic") {
    return { trust_gain_multiplier: 0.8 };
  }
}
```

---

### Trust Building

**Trust Gains by Activity Type:**
```javascript
const TRUST_GAINS = {
  small_talk: 0.01,                  // +1% trust
  meaningful_conversation: 0.03,
  shared_activity: 0.02,
  vulnerable_sharing: 0.05,
  helped_in_need: 0.08,
  crisis_support: 0.12,
  kept_promise: 0.04,
  showed_up_when_mattered: 0.10,
  
  // Negative
  broke_promise: -0.08,
  betrayed_confidence: -0.15,
  major_betrayal: -0.30
};
```

**Trust Requirements by Level:**
```javascript
const TRUST_GATES = {
  level_1_to_2: 0.15,                // Need 15% trust minimum
  level_2_to_3: 0.30,                // Need 30% trust minimum
  level_3_to_4: 0.50,                // Need 50% trust minimum
  level_4_to_5: 0.75                 // Need 75% trust minimum
};
```

---

### Level-Up Formula (Complete)

```javascript
function checkLevelUp(relationship) {
  const current_level = relationship.level;
  const next_level = current_level + 1;
  
  if (next_level > 5) return null;   // Max level reached
  
  // Get requirements for next level
  const requirements = LEVEL_REQUIREMENTS[next_level];
  
  // Check interaction count
  const interactions_met = relationship.interaction_count >= requirements.min_interactions;
  
  // Check trust threshold
  const trust_met = relationship.trust >= requirements.min_trust;
  
  // Check special requirements (for some levels)
  const special_met = requirements.special_requirements 
    ? checkSpecialRequirements(relationship, requirements.special_requirements)
    : true;
  
  // Check minimum relationship age (for some levels)
  const age_met = requirements.minimum_relationship_age
    ? relationship.relationship_age_weeks >= requirements.minimum_relationship_age
    : true;
  
  // ALL must be true
  if (interactions_met && trust_met && special_met && age_met) {
    return {
      can_level_up: true,
      new_level: next_level,
      trigger_special_event: true,   // Level-up is special moment
      narrative: generateLevelUpNarrative(relationship, next_level)
    };
  }
  
  // Return progress toward next level
  return {
    can_level_up: false,
    progress: {
      interactions: `${relationship.interaction_count}/${requirements.min_interactions}`,
      trust: `${(relationship.trust * 100).toFixed(0)}%/${(requirements.min_trust * 100).toFixed(0)}%`,
      blockers: getBlockers(interactions_met, trust_met, special_met, age_met)
    }
  };
}
```

---

## Display Format

### UI Display Rules

**master_truths v1.1:** "Display: 'Level 3 (Trust 0.62)' — never '10/10', 'Level 6', or 'Level 0' (show 'Not Met' instead)."

```javascript
function formatRelationshipDisplay(relationship) {
  // Never show "Level 0"
  if (relationship.level === 0) {
    return {
      primary: "Not Met",
      secondary: null,
      icon: "question_mark",
      color: "gray"
    };
  }
  
  // Standard display
  return {
    primary: `${LEVEL_NAMES[relationship.level]} (Level ${relationship.level})`,
    secondary: `Trust ${(relationship.trust * 100).toFixed(0)}%`,
    
    // Alternative formats
    format_A: `Level ${relationship.level}: ${LEVEL_NAMES[relationship.level]}`,
    format_B: `${LEVEL_NAMES[relationship.level]} (Trust ${(relationship.trust * 100).toFixed(0)}%)`,
    format_C: `${LEVEL_NAMES[relationship.level]} • ${relationship.interaction_count} interactions`,
    
    // NEVER use these formats
    never_use: [
      "Level 0",                     // Use "Not Met"
      "10/10",                       // Not a rating
      "Level 6",                     // Max is 5
      "100% trust"                   // Use decimal format
    ]
  };
}
```

---

## Master Truths v1.2: NPC Capacity Tracking *(NEW)*

### NPCs Have Emotional Capacity Too

**Core Principle:** NPCs aren't infinite support machines. They have their own emotional capacity (0-10 scale) that fluctuates based on their circumstances, just like the player.

```javascript
const NPC_CAPACITY_SYSTEM = {
  principle: "NPCs can only provide support equal to their current capacity. A friend at capacity 3 cannot provide high-level emotional support.",
  
  capacity_scale: {
    range: "0-10 (same as player)",
    typical_baseline: 6-7,  // Most NPCs in stable state
    
    meaning: {
      0-2: "Crisis state - needs support, cannot give support",
      3-5: "Struggling - limited capacity to help",
      6-8: "Normal - can provide typical support",
      9-10: "Thriving - can provide extraordinary support"
    }
  },
  
  capacity_tracking: {
    every_npc_has: {
      current_capacity: "0-10 continuous",
      baseline_capacity: "6-8 typical (varies by personality)",
      active_stressors: "Array of current life challenges",
      capacity_trend: "Increasing / Stable / Decreasing"
    },
    
    updated_when: [
      "NPC-specific life events occur",
      "Time passes (gradual recovery or decline)",
      "Player interactions affect NPC state",
      "Season transitions"
    ]
  }
};
```

**Example NPC Capacity States:**

```javascript
const SARAH_CAPACITY_EXAMPLES = {
  baseline_state: {
    capacity: 7,
    life_status: "Bookshop running smoothly, no major stressors",
    relationships: "Good - Marcus, Player, other friends",
    can_provide_support: "High - can be there for friend in crisis",
    
    narrative_signals: [
      "Sarah seems happy lately",
      "She's been checking in on you regularly",
      "Offers to help without being asked"
    ]
  },
  
  moderate_stress: {
    capacity: 5,
    life_status: "Bookshop slow sales, mild financial worry",
    active_stressors: ["financial_concern"],
    can_provide_support: "Moderate - can listen, but distracted",
    
    narrative_signals: [
      "Sarah seems preoccupied when you talk",
      "Takes longer to respond to texts",
      "Still supportive but less energy"
    ],
    
    support_availability: {
      emotional_venting: "Available - can listen",
      crisis_support: "Limited - she's got her own worries",
      practical_help: "Available but strained"
    }
  },
  
  crisis_state: {
    capacity: 2,
    life_status: "Bookshop facing closure, may lose life's work",
    active_stressors: ["financial_crisis", "identity_threat", "future_uncertainty"],
    can_provide_support: "Minimal - needs support herself",
    
    narrative_signals: [
      "Sarah's texts are short, stressed",
      "She's not initiating conversations",
      "Looks exhausted when you see her",
      "Marcus: 'Sarah's really struggling right now'"
    ],
    
    support_availability: {
      emotional_venting: "❌ UNAVAILABLE - She's overwhelmed",
      crisis_support: "❌ UNAVAILABLE - She can't handle more",
      practical_help: "❌ UNAVAILABLE - She needs help, not giving it",
      
      role_reversal: "Player should be supporting HER, not asking for support"
    },
    
    if_player_asks_for_support_anyway: {
      sarah_tries: true,
      but_cant: "She tries to be there but breaks down crying",
      emotional_impact: "Sarah feels guilty she can't help, player feels guilty for asking",
      relationship_damage: -0.1,
      
      narrative: `
        "I'm sorry," Sarah says, voice cracking. "I want to be there for you, 
        I do. But I... I can't right now. I just... I can't."
        
        You see tears in her eyes. She's not okay.
        
        You realize: You asked too much. She's drowning and you asked her to 
        save you too.
      `
    }
  },
  
  npc_in_crisis_needs_player: {
    capacity: 1,
    life_status: "CRISIS - Bookshop closed, life's work lost",
    emotional_state: "DEVASTATED",
    
    narrative_moment: {
      title: "When Your Friend Needs You",
      content: `
        Sarah's calling. 2 AM.
        
        "It's over," she says. Voice hollow. "I signed the papers. 
        The bookshop... it's gone."
        
        She's crying. That deep, shaking crying that comes from somewhere 
        fundamental breaking.
        
        "Can you come over? I don't... I don't want to be alone right now."
        
        This is when friendship matters. When they need you.
      `,
      
      player_choice: {
        go_to_sarah: {
          description: "Drop everything, go be with her",
          cost: { time: 3, energy: 2, sleep: "sacrifice" },
          relationship_impact: +0.3,
          trust_impact: +0.2,
          memory_weight: 10,
          
          sarah_remembers: "You were there when everything fell apart. Forever remembered.",
          
          long_term: "When player has crisis, Sarah will move heaven and earth to help"
        },
        
        say_cant_come: {
          description: "Too tired, have important thing tomorrow",
          relationship_damage: -0.8,
          trust_shattered: "She called for help and you said no",
          
          sarah_feels: "Abandoned in worst moment",
          
          may_never_recover: "Some wounds don't heal. This might be one.",
          
          long_term: "Sarah becomes distant. Trust broken at critical moment. May never reach Level 4-5."
        }
      }
    }
  }
};
```

---

## Master Truths v1.2: Support Mechanics *(NEW)*

### The Capacity + 2 Rule

**Core Principle:** An NPC can provide support up to their current capacity + 2. A friend at capacity 5 can support you up to level 7 problems, but not level 9 crises.

```javascript
const SUPPORT_CAPACITY_RULE = {
  formula: "max_support_level = npc_capacity + 2",
  
  explanation: "People can stretch beyond their own capacity to help loved ones, but only by ~2 points",
  
  examples: [
    {
      npc_capacity: 8,
      max_support: 10,
      meaning: "Can support ANY problem - they're thriving and can handle anything"
    },
    {
      npc_capacity: 6,
      max_support: 8,
      meaning: "Can support most problems - typical friend in stable state"
    },
    {
      npc_capacity: 4,
      max_support: 6,
      meaning: "Can support moderate issues - but not major crises"
    },
    {
      npc_capacity: 2,
      max_support: 4,
      meaning: "Can barely help - they're struggling themselves"
    }
  ],
  
  gameplay_implementation: {
    when_player_seeks_support: {
      player_crisis_level: 8,  // Major crisis (job loss, breakup, etc)
      
      check_npc_capacity: {
        marcus_capacity: 7,
        marcus_max_support: 9,  // 7 + 2
        
        result: "✅ Marcus CAN support - crisis level 8 < max support 9",
        
        narrative: `
          Marcus listens. Really listens.
          
          "Hey," he says. "We'll figure this out. You're not alone."
          
          And you believe him. Because he has the capacity to be there.
        `
      },
      
      sarah_capacity: 3,
      sarah_max_support: 5,  // 3 + 2
      
      result: "❌ Sarah CANNOT fully support - crisis level 8 > max support 5",
      
      narrative: `
        Sarah tries. You can see her trying.
        
        But she's overwhelmed. By your crisis, by her own problems.
        
        "I'm sorry," she says. "I wish I could... I just..."
        
        She can't. And that's okay. She's got her own stuff.
      `
    }
  }
};
```

**Support Availability by Capacity:**

```javascript
const SUPPORT_MATRIX = {
  npc_capacity_10: {
    max_support_level: 12,  // Can handle anything
    support_types: {
      emotional_venting: "✅ UNLIMITED",
      crisis_support: "✅ Can handle extreme crisis",
      practical_help: "✅ Will drop everything",
      daily_check_ins: "✅ Proactive support",
      long_term_support: "✅ Sustained over months"
    },
    narrative_quality: "Rock. Unshakeable. You can lean on them completely."
  },
  
  npc_capacity_8: {
    max_support_level: 10,
    support_types: {
      emotional_venting: "✅ Available",
      crisis_support: "✅ Can handle major crisis",
      practical_help: "✅ Available",
      daily_check_ins: "✅ Available",
      long_term_support: "✅ Can sustain"
    },
    narrative_quality: "Solid friend. Can be there when you need them."
  },
  
  npc_capacity_6: {
    max_support_level: 8,
    support_types: {
      emotional_venting: "✅ Available",
      crisis_support: "✅ Can handle moderate crisis",
      practical_help: "⚠️ Available but may be strained",
      daily_check_ins: "⚠️ Occasional, not constant",
      long_term_support: "⚠️ Limited bandwidth"
    },
    narrative_quality: "Good friend, but has limits. Can help most of the time."
  },
  
  npc_capacity_4: {
    max_support_level: 6,
    support_types: {
      emotional_venting: "⚠️ Available for brief sessions",
      crisis_support: "❌ Cannot handle major crisis",
      practical_help: "⚠️ Limited - they're struggling too",
      daily_check_ins: "❌ Not available",
      long_term_support: "❌ Can't sustain"
    },
    narrative_quality: "Wants to help but doesn't have bandwidth. They're dealing with their own stuff."
  },
  
  npc_capacity_2: {
    max_support_level: 4,
    support_types: {
      emotional_venting: "❌ Cannot handle",
      crisis_support: "❌ Will make it worse",
      practical_help: "❌ None available",
      daily_check_ins: "❌ They're not checking on you",
      long_term_support: "❌ Impossible"
    },
    role_reversal: "They need YOUR support, not other way around",
    narrative_quality: "Drowning. Can't throw you a life preserver when they're underwater."
  }
};
```

---

## Master Truths v1.2: NPC Capacity Fluctuation *(NEW)*

### Life Events Change NPC Capacity

**Core Principle:** NPC capacity changes based on their life circumstances, just like the player's capacity changes based on player circumstances.

```javascript
const NPC_CAPACITY_FLUCTUATION = {
  typical_changes: {
    positive_events: {
      job_promotion: +1,
      relationship_milestone: +1,
      aspiration_achieved: +2,
      crisis_resolved: +2,
      therapy_breakthrough: +1,
      
      examples: {
        marcus_gets_promotion: {
          baseline_capacity: 7,
          new_capacity: 8,
          duration: "4-8 weeks",
          
          narrative: "Marcus has been in a great mood lately. Work's going well.",
          support_availability: "Increased - he's got bandwidth to help more"
        }
      }
    },
    
    negative_events: {
      job_loss: -3,
      breakup: -4,
      family_emergency: -2,
      health_crisis: -5,
      financial_crisis: -3,
      major_loss: -5,
      
      examples: {
        sarah_business_failing: {
          baseline_capacity: 7,
          active_stressors: ["financial_crisis", "identity_threat"],
          new_capacity: 3,
          duration: "Until resolved or 12+ weeks",
          
          narrative: "Sarah's been distant. The bookshop is struggling and she's terrified.",
          support_availability: "Minimal - she's barely holding it together"
        },
        
        marcus_breakup: {
          baseline_capacity: 7,
          event: "Girlfriend of 2 years broke up with him",
          new_capacity: 4,
          duration: "6-10 weeks recovery",
          
          narrative: "Marcus is hurting. You can see it even when he tries to hide it.",
          support_availability: "Reduced - he's processing his own grief",
          
          week_1: { capacity: 2, support: "None - he's devastated" },
          week_4: { capacity: 4, support: "Limited - starting to recover" },
          week_8: { capacity: 6, support: "Mostly back - healing" }
        }
      }
    },
    
    gradual_recovery: {
      principle: "Capacity recovers slowly over time if stressors resolve",
      rate: "+0.5 per week" + " if circumstances stable",
      
      example: {
        sarah_after_crisis: {
          week_0: 2,  // Crisis peak
          week_2: 3,  // Starting to process
          week_4: 4,  // Accepting reality
          week_8: 5,  // Rebuilding
          week_12: 6, // Back to stable
          week_16: 7  // Returned to baseline
        }
      }
    },
    
    circumstance_stacking: {
      multiple_stressors_compound: true,
      
      example: {
        marcus_stacked_crises: {
          baseline_capacity: 7,
          
          stressor_1: "Breakup (-4)",
          capacity_after: 3,
          
          stressor_2: "Father hospitalized (-2)",
          capacity_after: 1,  // Compounding effect
          
          stressor_3: "Job performance suffering (-1)",
          capacity_after: 0,  // Breaking point
          
          result: "Marcus is in complete crisis. Cannot function, needs intervention.",
          
          narrative: `
            Marcus doesn't answer your texts for three days.
            
            When you finally see him, he looks... broken.
            
            The breakup. His dad in the hospital. Work falling apart.
            
            "I can't..." he starts, then stops. Just shakes his head.
            
            He needs help. Serious help.
          `,
          
          player_choice: {
            be_there: "Drop everything, full support for friend in crisis",
            limited_help: "Check in but can't provide intensive support",
            miss_it: "Too wrapped up in own stuff to notice Marcus drowning"
          }
        }
      }
    }
  }
};
```

---

## Master Truths v1.2: Dramatic Irony at Level 3+ *(NEW)*

### Knowledge Gaps Create Tension in Deep Friendships

**Core Principle:** At Level 3+, player sees enough of NPC's life to notice things the NPC might not see about themselves - or see that NPC is hiding something.

```javascript
const DRAMATIC_IRONY_OPPORTUNITIES = {
  level_3_friend: {
    knowledge_access: "Player sees NPC's patterns, can notice changes",
    
    irony_types: {
      player_knows_npc_struggling: {
        scenario: "Sarah insists she's fine, but player sees signs",
        
        player_sees: [
          "Sarah's bookshop has been empty last 3 visits",
          "She's lost weight, looks tired",
          "Her texts are shorter, more stressed",
          "She declined lunch twice - 'too busy' (unusual for her)"
        ],
        
        sarah_says: "I'm fine! Just busy with inventory.",
        
        player_knows: "She's not fine. Something's wrong.",
        
        tension: "Do you confront her? Or respect her privacy?",
        
        decision_point: {
          confront: "Sarah, I can see you're struggling. Talk to me?",
          respect_privacy: "Don't push - wait for her to open up",
          offer_help: "Let me help with the bookshop this week"
        }
      },
      
      npc_blind_to_own_pattern: {
        scenario: "Marcus doesn't see he's burning out",
        
        player_notices: [
          "Marcus working 70 hour weeks",
          "Skipped last 2 friend hangouts",
          "Defensive when you ask about work",
          "Third coffee by 10 AM every day"
        ],
        
        marcus_says: "I'm fine! Just a busy period. I've got this.",
        
        player_thinks: "You're heading for collapse. I've seen this before.",
        
        dramatic_irony: "Player knows Marcus is repeating player's own burnout pattern",
        
        tension: "Warn him? He won't listen. But you can't watch him crash.",
        
        parallel_to_player_experience: {
          if_player_burned_out_before: "Emotional weight 2x - 'Don't do what I did'",
          player_agency: "Intervention possible but difficult"
        }
      },
      
      npc_hiding_something: {
        scenario: "Sarah is lying about relationship status",
        
        evidence_player_sees: [
          "Week 1: Sarah mentions 'a friend' multiple times",
          "Week 2: Sees Sarah at coffee shop with same person twice",
          "Week 3: Sarah's phone buzzes, she smiles and hides screen",
          "Week 4: Mutual friend: 'Sarah seeing someone?'"
        ],
        
        sarah_says: "No, I'm not dating anyone. Why do you ask?",
        
        player_knows: "You're definitely seeing someone and not telling me.",
        
        tension: "Why is she hiding it? Is she worried I'll judge?",
        
        resolution_options: [
          "Call her out directly",
          "Wait for her to tell you",
          "Ask mutual friends what they know",
          "Feel hurt she's not sharing"
        ]
      }
    }
  },
  
  level_4_close_friend: {
    knowledge_access: "Player knows NPC deeply - can spot lies, changes, secrets",
    
    irony_types: {
      player_sees_npc_self_destructing: {
        scenario: "Sarah spiraling into depression, denying it",
        
        player_knows_sarah_deeply: [
          "This is how she acted after David died",
          "The isolation, the 'I'm fine', the forced smiles",
          "She's lying to herself, not just to you"
        ],
        
        dramatic_weight: 9,  // Very high - watching friend repeat trauma pattern
        
        player_choice: {
          intervention: "Force the conversation, risk pushing her away",
          gentle_approach: "Be present, wait for opening",
          involve_others: "Talk to Marcus, coordinate support",
          
          all_options_risky: "No perfect answer. Friend in crisis.",
          
          tension: "You see her drowning. She won't grab the life preserver."
        }
      },
      
      player_knows_secret_that_affects_npc: {
        scenario: "Player knows Marcus's girlfriend is cheating (saw her with someone else)",
        
        knowledge_gap: "Player knows / Marcus doesn't know",
        
        emotional_weight: 10,  // Maximum tension
        
        player_dilemma: {
          tell_marcus: {
            pro: "He deserves to know",
            con: "Destroys his relationship, he might shoot the messenger",
            risk: "What if I'm wrong? What if there's an explanation?"
          },
          
          dont_tell: {
            pro: "Not your place, maybe you're wrong",
            con: "Watch him be lied to, complicit in deception",
            guilt: "Every time he talks about her, you're keeping this secret"
          },
          
          investigate: {
            pro: "Make sure before destroying his life",
            con: "Invasion of privacy, playing detective",
            time_pressure: "The longer you wait, the worse it gets"
          }
        },
        
        tension: "Classic dramatic irony - you know, he doesn't, and knowing is torture.",
        
        relationship_stakes: "How you handle this will define your friendship forever."
      }
    }
  },
  
  level_5_soulmate: {
    knowledge_access: "Complete - you know them better than they know themselves",
    
    irony_potential: "Maximum - can see their blind spots, future mistakes, self-deception",
    
    bittersweet_knowledge: "Sometimes loving someone means watching them make mistakes you can see coming"
  }
};
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Relationship System (v1.1 Foundation)
- [x] Relationship Levels: 0–5 (six discrete stages)
- [x] Level 0 = "Not Met" (tracked internally, never displayed as "Level 0")
- [x] Level-up requires BOTH interaction count AND trust threshold
- [x] Trust: 0.0–1.0 continuous meter under the hood
- [x] Display: "Level 3 (Trust 0.62)" format
- [x] Statuses (Life Partnership, Estranged) are post-level, not new levels
- [x] Interaction counting and trust building mechanics
- [x] Level-specific activities and social capital costs
- [x] Relationship resilience and decay rates per level

### ✅ Master Truths v1.2: NPC Capacity System *(NEW)*
- [x] **NPC Capacity Tracking (0-10 scale)**
  - Every NPC has current_capacity (0-10 continuous)
  - Baseline capacity (6-8 typical, varies by personality)
  - Active stressors array tracking life challenges
  - Capacity trend (increasing/stable/decreasing)
- [x] **Support Availability by Capacity**
  - Capacity 0-2: Crisis state - needs support, cannot give
  - Capacity 3-5: Struggling - limited capacity to help
  - Capacity 6-8: Normal - can provide typical support
  - Capacity 9-10: Thriving - extraordinary support available
- [x] **Capacity + 2 Rule**
  - Formula: max_support_level = npc_capacity + 2
  - NPC at capacity 6 can support up to level 8 problems
  - NPC at capacity 3 can only support up to level 5 problems
  - NPCs cannot provide support beyond their capacity range
- [x] **Support Matrix by Capacity**
  - Emotional venting availability
  - Crisis support capability
  - Practical help availability
  - Daily check-ins feasibility
  - Long-term support sustainability

### ✅ Master Truths v1.2: NPC Capacity Fluctuation *(NEW)*
- [x] **Life Events Change NPC Capacity**
  - Positive events: job promotion (+1), aspiration achieved (+2), crisis resolved (+2)
  - Negative events: job loss (-3), breakup (-4), health crisis (-5)
  - Gradual recovery: +0.5 per week if circumstances stable
- [x] **Circumstance Stacking for NPCs**
  - Multiple stressors compound (just like player)
  - Example: Breakup (-4) + family emergency (-2) + job stress (-1) = capacity 0 (breaking point)
  - NPCs can reach crisis state requiring player support
- [x] **Narrative Signals of NPC Capacity**
  - High capacity: "Sarah seems happy, offers help unprompted"
  - Moderate: "Sarah preoccupied, takes longer to respond"
  - Low capacity: "Sarah's texts are short, stressed, not initiating"
  - Crisis: "Marcus doesn't answer for days, looks broken"
- [x] **Role Reversal Mechanics**
  - When NPC at capacity ≤2, player should support THEM
  - Asking for support from struggling friend = relationship damage
  - Narrative example: Sarah tries to help but breaks down crying

### ✅ Master Truths v1.2: Dramatic Irony (Level 3+) *(NEW)*
- [x] **Level 3 (Friend) Irony Opportunities**
  - Player sees NPC patterns, can notice changes
  - Player knows NPC struggling (Sarah insists she's fine, player sees signs)
  - NPC blind to own pattern (Marcus burning out, doesn't see it)
  - NPC hiding something (Sarah dating someone, not telling player)
- [x] **Level 4 (Close Friend) Irony**
  - Player knows NPC deeply - can spot lies, changes, secrets
  - Player sees NPC self-destructing (Sarah spiraling like after David's death)
  - Player knows secret that affects NPC (Marcus's girlfriend cheating)
  - Maximum tension: "You know, he doesn't, and knowing is torture"
- [x] **Level 5 (Soulmate) Irony**
  - Complete knowledge: "Know them better than they know themselves"
  - Can see blind spots, future mistakes, self-deception
  - Bittersweet: "Watching them make mistakes you can see coming"

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~590 lines** of new v1.2 relationship mechanics
2. **NPC capacity tracking system** - NPCs have 0-10 capacity that fluctuates
3. **Capacity + 2 support rule** - NPCs can only provide support within their capacity range
4. **NPC capacity fluctuation** - life events change NPC availability
5. **Support matrix** - detailed support availability by NPC capacity level
6. **Role reversal** - when NPC in crisis, player should support them
7. **Dramatic irony at L3+** - knowledge gaps create tension in deep friendships

**NPC Capacity Examples:**
- Sarah at capacity 7: "Happy, offers help unprompted, can handle your crises"
- Sarah at capacity 5: "Preoccupied, still supportive but distracted, limited bandwidth"
- Sarah at capacity 2: "Crisis state - she needs YOU, can't provide support"
- Sarah at capacity 1 calls 2 AM: "Bookshop closed. 'Can you come over? I don't want to be alone.'"

**Support Rule Examples:**
- Marcus at capacity 7 → max support 9: Can handle your major crisis (level 8)
- Sarah at capacity 3 → max support 5: Cannot handle your major crisis (level 8), she's overwhelmed

**Dramatic Irony Examples:**
- Level 3: "Sarah says she's fine. Player sees bookshop empty, she's lost weight, stressed texts."
- Level 4: "Player knows Marcus's girlfriend is cheating. Tell him? Don't tell? Investigation? Torture."
- Level 5: "You know them better than they know themselves. See mistakes coming."

**Design Principles:**
- NPCs have emotional limits - not infinite support machines
- Friends at capacity 2 cannot provide crisis support
- Multiple NPC stressors compound (same as player)
- Deep friendships create dramatic irony opportunities
- Role reversal: sometimes you support them, not other way around
- Support availability = f(NPC capacity, player crisis level, relationship level)

**References:**
- See `01-emotional-authenticity.md` for cross-system capacity integration
- See `14-emotional-state-mechanics.md` for player capacity calculation (same rules apply to NPCs)
- See `11-turn-economy-implementation.md` for Social Capital mechanics
- See `12-success-probability-formulas.md` for relationship success modifiers
- See `37-dramatic-irony-system.md` for detailed dramatic irony mechanics and knowledge gap scoring
- See `1.concept/13-ai-personality-system.md` for AI personality and memory
- See `7.schema/03-character-system.md` for RelationshipState interface

---

**This specification enables developers to implement the complete relationship progression system with Master Truths v1.2 enhancements: NPC capacity tracking (0-10 scale) with the capacity+2 support rule, NPC capacity fluctuation based on life circumstances, support availability matrices showing when NPCs can/cannot help, role reversal mechanics where player supports struggling friends, and dramatic irony opportunities at Level 3+ where knowledge gaps create emotional tension - creating relationships that feel authentic, with friends who have their own limits and struggles, not infinite support machines.**

