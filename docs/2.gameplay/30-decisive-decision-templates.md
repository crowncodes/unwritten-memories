# Decisive Decision Templates - Implementation Specification

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete scaffolding and templates for authoring decisive decisions with emotional authenticity

**References:**
- **Design Philosophy:** `1.concept/15-progression-phases.md` (WHY decisive moments matter)
- **Narrative Structure:** `31-narrative-arc-scaffolding.md` (3-act season structure)
- **Season Flow:** `73-season-flow-implementation.md` (when decisions appear)

---

## Overview

**Decisive Decisions** are life-altering choices that pause time, create genuine tension, and have cascading consequences across weeks or seasons. They are the narrative backbone of Unwritten.

**Core Principles:**
1. **Time pauses** - No FOMO, no real-time pressure
2. **Clear stakes** - Player understands what's at risk
3. **No perfect answer** - Every option has tradeoffs
4. **Long-term consequences** - Choices echo for weeks/seasons
5. **Foreshadowed** - Never appear randomly from nowhere

**Multi-Season Context:** Decisive decisions can have consequences that last beyond the current season. Since characters persist across **8-10 seasons** (Life Bookshelf), major decisions in Season 2 might still affect Season 5. The memory and regret systems track choices across the character's entire life. See `73-season-flow-implementation.md` for multi-season continuity.

**Compliance:** master_truths v1.2 requires "Decisive decisions pause time; copy avoids FOMO framing; options respect emotional capacity and personality constraints"

---

## Decision Template Structure

### Complete Template

```javascript
const DECISIVE_DECISION_TEMPLATE = {
  // METADATA
  id: "unique_decision_id",
  title: "THE DECISION NAME",
  category: "career|relationship|life_direction|crisis|opportunity",
  rarity: "major|legendary",  // major = season-level, legendary = lifetime-level
  
  // PREREQUISITES (When can this appear?)
  prerequisites: {
    min_week: 12,                    // Don't appear too early
    max_week: null,                  // null = no max
    required_arcs: ["arc_id"],       // Must be in this arc
    required_relationships: [
      { npc: "npc_id", level: 3 }   // Levels 0-5 (v1.1)
    ],
    required_skills: [
      { skill: "skill_name", level: 2 }
    ],
    required_meters: {
      physical: { min: 0, max: 10 }  // Can trigger at any physical state
    },
    mutually_exclusive: ["other_decision_id"],  // Can't have both
    story_flags: ["flag_name"]       // World state requirements
  },
  
  // FORESHADOWING (Build tension before decision)
  foreshadowing: [
    {
      week: -4,  // 4 weeks before
      card: "Foreshadowing card content",
      hint: "Subtle hint of what's coming",
      weight: 0.3  // Emotional weight (0.0-1.0)
    },
    {
      week: -2,  // 2 weeks before
      card: "Stronger foreshadowing",
      hint: "Clearer indication",
      weight: 0.6
    },
    {
      week: -1,  // 1 week before
      card: "Final warning/setup",
      hint: "Decision is imminent",
      weight: 0.8
    }
  ],
  
  // THE DECISION CARD
  decision_card: {
    art_style: "dramatic_lighting|intimate_moment|crisis_urgent",
    
    // The situation
    narrative: `
      Multi-paragraph narrative that:
      1. Sets the scene
      2. Establishes the stakes
      3. Presents the dilemma
      4. Makes player FEEL the weight
    `,
    
    // Options (2-4 choices)
    options: [
      {
        id: "option_a",
        label: "\"What the player says/does\"",
        
        // Immediate effects (this turn)
        immediate_effects: {
          meters: { physical: 0, mental: 0, social: +2, emotional: +3 },
          money: +200,
          skills: { skill_name: +2 },
          relationships: {
            npc_id: { trust: +0.3, social_capital: +2 }
          },
          emotional_state: "INSPIRED"
        },
        
        // Short-term (1-4 weeks)
        short_term_consequences: [
          {
            week: 0,
            card: "Immediate reaction card",
            effects: { /* specific effects */ },
            narrative: "What happens right after"
          },
          {
            week: 1,
            card: "First week aftermath",
            effects: { /* specific effects */ }
          },
          {
            week: 2,
            card: "Second week development",
            effects: { /* specific effects */ }
          }
        ],
        
        // Long-term (4+ weeks)
        long_term_consequences: [
          {
            weeks: "4-8",
            effect: "Arc progression or damage",
            unlock: "New cards/locations/NPCs",
            impact: "Lasting changes"
          },
          {
            weeks: "12-16",
            effect: "Delayed major consequence",
            memory: "Persistent memory reference"
          }
        ],
        
        // Arc impact
        arc_impact: {
          arc_name_1: "ADVANCE|DAMAGE|COMPLETE|FAIL",
          arc_name_2: "TEMPORARY_RISK|IMPROVE"
        },
        
        // Success chance (if applicable)
        success_required: true,
        base_success_chance: 0.60,
        success_modifiers: {
          skill_name: { weight: 0.3 },
          relationship_npc: { weight: 0.2 }
        },
        
        // NEW - Master Truths v1.2: Emotional Capacity Requirements
        emotional_capacity_requirements: {
          min_capacity: number,              // Minimum capacity to choose (0-10 scale)
          capacity_consumed: number,         // How much capacity this choice costs
          locked_if_below: number,           // Hard lock threshold
          locked_reason: string,             // Why this option is unavailable
          alternative_if_locked: string      // What player can do instead
        },
        
        // NEW - Master Truths v1.2: OCEAN Personality Modifiers
        personality_modifiers: {
          recommended_for: {                 // Personality traits that favor this option
            openness: { min?: number, max?: number },
            conscientiousness: { min?: number, max?: number },
            extraversion: { min?: number, max?: number },
            agreeableness: { min?: number, max?: number },
            neuroticism: { min?: number, max?: number }
          },
          difficulty_by_trait: {             // How personality affects success
            low_openness: "+10% success if < 3.0",
            high_neuroticism: "-15% success if > 4.0"
          },
          personality_consequence: {         // Different outcomes by personality
            if_high_openness: "More creative outcome",
            if_low_agreeableness: "Harsher confrontation"
          }
        },
        
        // NEW - Master Truths v1.2: Circumstance Stacking Effects
        circumstance_effects: {
          affected_by_stressors: boolean,   // Does stress affect this option?
          stressor_penalty: number,          // -X% per active stressor
          overwhelmed_locked: boolean        // Locked if OVERWHELMED state?
        }
      },
      // ... more options
    ],
    
    // Time constraints (in-world, not real-time)
    time_limit: {
      duration: "24 hours in-game",
      urgency: "Must decide before [event]",
      countdown_display: false  // Usually false - no anxiety
    },
    
    // Context to display
    display_context: {
      show_meters: true,
      show_money: true,
      show_relationships: ["npc1", "npc2"],
      show_arc_progress: ["arc_name"],
      show_skills: ["skill_name"],
      review_options: [
        "View relationship history",
        "Review arc timeline",
        "Check financial status",
        "See personality traits"
      ],
      
      // NEW: Emotional echoes integration
      show_past_similar_decisions: boolean,
      emotional_echoes: {
        enabled: true,
        search_memories: "Similar past decisions and their outcomes",
        display: "Before options presented",
        example: "Last time you chose work over relationships, you regretted it for years."
      },
      
      // NEW: Ticking clock display
      ticking_clock: {
        enabled: boolean,
        type: "in_world_deadline",
        urgency_text: string,
        example: "Wedding season ends in 6 weeks - miss it and wait a full year",
        consequences_of_delay: string,
        countdown_display: boolean,    // Usually false - no anxiety
        no_fomo: true                   // Never real-time pressure
      },
      
      // NEW: Mystery context
      mystery_context: {
        unresolved_questions: string[],
        information_you_lack: string,
        example: {
          questions: ["What Sarah is hiding", "Why Marcus warned you"],
          lack: "You don't know David was Sarah's fiancé"
        }
      },
      
      // NEW - Master Truths v1.2: Emotional Capacity Display
      capacity_context: {
        show_current_capacity: boolean,      // Display player's capacity (0-10)
        show_capacity_requirements: boolean, // Show what each option needs
        locked_options_reason: boolean,      // Explain why options are locked
        example: "Your capacity: 3.5/10 - Option A requires 5.0+ (unavailable)"
      },
      
      // NEW - Master Truths v1.2: Parallel Stressor Display
      stressor_context: {
        show_active_stressors: boolean,      // List current stressors
        show_stressor_effects: boolean,      // How they affect options
        npc_awareness: boolean,              // NPCs notice your stress
        example: {
          stressors: ["Work deadline", "Low physical meter", "Money concerns"],
          effects: "-15% to all decision success rates",
          npc_notice: "Sarah: 'Are you okay? You seem stressed.'"
        }
      }
    }
  },
  
  // MEMORY ENTRY
  memory: {
    title: "Memory title",
    emotional_weight: 8,  // 0-10
    reference_in_novel: true,
    tags: ["life_changing", "regret_potential"],
    generates_flashback: true
  },
  
  // FOLLOW-UP SYSTEM
  follow_ups: {
    reference_weeks: [8, 16, 24],  // When to reference this decision again
    regret_system: {
      enabled: true,
      triggers_at: ["low_emotional", "anniversary", "seeing_alternative"]
    }
  }
};
```

---

## Master Truths v1.2: Emotional Authenticity Features *(NEW)*

### Gap 3.2: Emotional Capacity Gating

Decisions respect emotional capacity - some options are locked when capacity is too low:

```javascript
const CAPACITY_GATED_DECISION = {
  id: "support_friend_crisis_while_struggling",
  title: "WHEN YOU'RE BARELY HOLDING ON",
  
  decision_card: {
    narrative: `
      Sarah calls. She's crying. "I need you. Can you come over?"
      
      Your capacity: 2.8/10
      
      You're barely holding it together yourself. Work is crushing you. 
      Your physical meter is at 3. You haven't slept properly in days. 
      Your own problems feel overwhelming.
      
      Sarah needs you. But what do you have left to give?
    `,
    
    options: [
      {
        id: "be_there_fully",
        label: "\"I'll be right there\" (Full support)",
        
        // LOCKED - Capacity too low
        emotional_capacity_requirements: {
          min_capacity: 5.0,
          capacity_consumed: 2.5,
          locked_if_below: 4.0,
          locked_reason: "You don't have the emotional capacity for this right now",
          alternative_if_locked: "Consider limited support or asking for help"
        },
        
        // This option is GRAYED OUT with explanation
        locked: true,
        locked_display: `
          ❌ [UNAVAILABLE - Emotional Capacity Too Low]
          
          Your capacity: 2.8/10
          Required: 4.0+
          
          You can't give what you don't have. Supporting Sarah fully would 
          require emotional resources you simply don't have right now. You'd 
          end up making things worse for both of you.
          
          See other options below.
        `
      },
      
      {
        id: "limited_support",
        label: "\"I'll come, but I'm struggling too\" (Limited support)",
        
        emotional_capacity_requirements: {
          min_capacity: 2.0,
          capacity_consumed: 1.5,
          locked_if_below: 2.0,
          locked_reason: null  // Available
        },
        
        immediate_effects: {
          relationships: {
            sarah: { trust: +0.10 }  // Honesty appreciated, but less effective
          },
          player_capacity: -1.5,     // Further depletes you
          emotional: -2
        },
        
        narrative_outcome: `
          You go to Sarah. You're honest: "I'm struggling too right now."
          
          She sees it in your face. You sit together. Two people barely 
          holding on, holding each other up.
          
          It's not the strong support she needed, but it's honest. And 
          sometimes that matters more.
        `
      },
      
      {
        id: "ask_for_backup",
        label: "\"Let me call Marcus\" (Get help)",
        
        emotional_capacity_requirements: {
          min_capacity: 1.0,
          capacity_consumed: 0.5,
          locked_if_below: 1.0,
          locked_reason: null  // Available
        },
        
        immediate_effects: {
          relationships: {
            sarah: { trust: +0.08 },
            marcus: { trust: +0.15 }  // Marcus respects you asking
          },
          player_capacity: -0.5,
          emotional: -1
        },
        
        narrative_outcome: `
          "I want to be there for you, but I'm not in a good place to do 
          this alone. Can I bring Marcus? He's great in situations like this."
          
          Sarah understands. Marcus comes through. You're there together. 
          Three-way support network activates.
          
          Knowing your limits is wisdom, not weakness.
        `
      }
    ],
    
    display_context: {
      // NEW: Capacity display
      capacity_context: {
        show_current_capacity: true,
        show_capacity_requirements: true,
        locked_options_reason: true,
        
        display: `
          YOUR EMOTIONAL CAPACITY: 2.8/10 (Very Low)
          
          Active stressors draining capacity:
          - Work deadline pressure
          - Physical exhaustion (meter at 3)
          - Financial stress
          
          Option A: Requires 4.0+ capacity [LOCKED]
          Option B: Requires 2.0+ capacity [AVAILABLE]
          Option C: Requires 1.0+ capacity [AVAILABLE]
        `
      }
    }
  }
};
```

---

### Gap 3.1: OCEAN-Based Option Modifiers

Options are filtered and modified based on player personality:

```javascript
const PERSONALITY_FILTERED_DECISION = {
  id: "confront_vs_avoid_conflict",
  title: "THE CONFRONTATION",
  
  decision_card: {
    narrative: `
      Your coworker publicly took credit for your work in the meeting. 
      Everyone saw it. Your boss congratulated them.
      
      You're furious. But what do you do?
    `,
    
    options: [
      {
        id: "direct_confrontation",
        label: "\"Call them out right now\" (Direct confrontation)",
        
        // Personality modifiers
        personality_modifiers: {
          recommended_for: {
            extraversion: { min: 3.5 },      // Easier for extraverts
            agreeableness: { max: 3.0 },     // Easier for low agreeableness
            neuroticism: { max: 3.5 }        // Harder if anxious
          },
          
          difficulty_by_trait: {
            low_extraversion: "Success -20% if extraversion < 2.5",
            high_agreeableness: "Success -15% if agreeableness > 4.0",
            high_neuroticism: "Success -25% if neuroticism > 4.5"
          },
          
          personality_consequence: {
            if_low_extraversion: "Confrontation is HARDER - you're not natural at this",
            if_high_agreeableness: "Feels WRONG - goes against your nature",
            if_high_neuroticism: "Anxiety SPIKES - this is terrifying"
          }
        },
        
        base_success_chance: 0.60,
        
        // Modified by personality
        actual_success_chance: function(player) {
          let chance = 0.60;
          if (player.extraversion < 2.5) chance -= 0.20;
          if (player.agreeableness > 4.0) chance -= 0.15;
          if (player.neuroticism > 4.5) chance -= 0.25;
          return Math.max(0.15, chance);
        },
        
        // Personality-specific outcomes
        success_outcome: {
          default: "You confront them. It works. Credit restored.",
          
          if_low_extraversion: `
            You force yourself to speak up. Your voice shakes, but you do it. 
            It's harder for you than it would be for others, but you DID it.
            Confidence +0.2 (major growth moment)
          `,
          
          if_high_agreeableness: `
            Every instinct screams not to do this. You do it anyway. 
            It feels awful. But you stood up for yourself.
            Internal conflict: +2
          `,
          
          if_high_neuroticism: `
            Your heart is pounding. Hands shaking. But you speak up. 
            Anxiety attack afterwards, but you DID it.
            Emotional cost: -3, but confidence +0.15
          `
        },
        
        failure_outcome: {
          default: "Confrontation backfires. You look aggressive.",
          
          if_low_extraversion: "You fumble the words. Look awkward. Worse than saying nothing.",
          if_high_neuroticism: "Anxiety overwhelms you mid-sentence. You freeze. Humiliating."
        }
      },
      
      {
        id: "private_conversation",
        label: "\"Talk to them privately later\" (Measured approach)",
        
        personality_modifiers: {
          recommended_for: {
            conscientiousness: { min: 3.0 },  // Planning ahead
            agreeableness: { min: 3.0 },      // Avoid public conflict
            extraversion: { min: 2.0 }        // Need some social courage
          },
          
          difficulty_by_trait: {
            low_conscientiousness: "Might forget or procrastinate",
            very_low_extraversion: "Still requires confrontation, just private"
          }
        },
        
        base_success_chance: 0.75,  // Higher success, less dramatic
        
        personality_consequence: {
          if_high_conscientiousness: "Natural fit - plan and execute calmly",
          if_high_agreeableness: "Comfortable - avoids public scene",
          if_low_extraversion: "Still hard, but EASIER than public confrontation"
        }
      },
      
      {
        id: "go_to_boss",
        label: "\"Report to boss privately\" (Escalate)",
        
        personality_modifiers: {
          recommended_for: {
            conscientiousness: { min: 4.0 },  // By-the-book approach
            agreeableness: { max: 4.0 },      // Not too conflict-avoidant
            neuroticism: { max: 4.0 }         // Need confidence
          }
        }
      },
      
      {
        id: "let_it_go",
        label: "\"Say nothing\" (Avoid conflict)",
        
        personality_modifiers: {
          recommended_for: {
            agreeableness: { min: 4.5 },      // Very conflict-avoidant
            neuroticism: { min: 4.0 },        // Very anxious
            extraversion: { max: 2.0 }        // Very introverted
          },
          
          difficulty_by_trait: {
            low_agreeableness: "Feels WRONG - you want to fight",
            low_neuroticism: "Frustrating - you're not afraid, why not act?"
          },
          
          personality_consequence: {
            if_high_agreeableness_high_neuroticism: "Natural response - avoid conflict, reduce anxiety",
            if_low_agreeableness: "INTERNAL CONFLICT - goes against nature, breeds resentment"
          }
        },
        
        immediate_effects: {
          emotional: -2,
          resentment: +3,
          anxiety: -1  // Reduced (avoided confrontation)
        },
        
        long_term_consequences: {
          if_high_agreeableness: "Regret builds - pattern of not standing up for self",
          if_low_agreeableness: "SEVERE regret - you're not this person, why did you back down?"
        }
      }
    ]
  }
};
```

---

### Gap 3.3: Parallel Stressor Context

NPCs notice when you're struggling, and circumstances compound:

```javascript
const STRESSOR_AWARE_DECISION = {
  id: "decision_while_overwhelmed",
  title: "WHEN EVERYTHING HITS AT ONCE",
  
  // Player state
  player_context: {
    active_stressors: [
      "work_deadline_tomorrow",
      "physical_meter_2",
      "money_rent_due_3_days",
      "relationship_mom_conflict",
      "car_broke_down_yesterday"
    ],
    stressor_count: 5,
    emotional_capacity: 2.1,
    emotional_state: "OVERWHELMED"
  },
  
  decision_card: {
    // BEFORE DECISION: Show stressor context
    stressor_context_display: `
      ════════════════════════════════════════
      YOU ARE OVERWHELMED
      ════════════════════════════════════════
      
      Active stressors (5):
      • Work deadline: Major presentation tomorrow, not ready
      • Physical exhaustion: Meter at 2/10, running on fumes
      • Financial crisis: Rent due in 3 days, $400 short
      • Family conflict: Mom hasn't spoken to you in 2 weeks
      • Car broken: $800 repair, no way to get to work
      
      Emotional capacity: 2.1/10 (Critical)
      
      Everything is hitting at once. This is when bad decisions happen.
      
      ════════════════════════════════════════
    `,
    
    narrative: `
      Your phone rings. It's Marcus.
      
      "Hey! So, I know this is short notice, but I need a huge favor. My 
      sister's wedding is this weekend and my plus-one canceled. Would you 
      come with me? It's a 3-hour drive, two-day thing. It would mean a lot."
      
      You stare at your phone.
      
      The presentation is tomorrow. You're not ready.
      Rent is due. You're $400 short.
      Your car is broken.
      Your mom isn't speaking to you.
      You're exhausted.
      
      And Marcus wants you to drop everything for a wedding.
    `,
    
    // NPC AWARENESS: Marcus notices your stress
    npc_awareness: {
      marcus_perception: "Marcus can tell something's wrong from your silence",
      
      marcus_response: `
        "...You okay? You sound stressed."
        
        [Marcus's Agreeableness: 4.2 - he's perceptive and caring]
        
        He's giving you an out if you need it. He won't be mad. But he'll 
        be disappointed.
      `
    },
    
    options: [
      {
        id: "say_yes_push_through",
        label: "\"Sure, I'll go\" (Push through - HIGH RISK)",
        
        // Affected by stressor stacking
        circumstance_effects: {
          affected_by_stressors: true,
          stressor_penalty: -0.10,           // -10% per stressor
          total_penalty: -0.50,              // 5 stressors = -50%
          overwhelmed_warning: true
        },
        
        base_success_chance: 0.50,
        actual_success_chance: 0.00,         // ZERO - too many stressors
        
        // LOCKED due to OVERWHELMED state
        locked: true,
        locked_display: `
          ⚠️ [HIGH RISK - Success Chance: 0%]
          
          5 active stressors = -50% to success rate
          Base chance: 50%
          Modified chance: 0%
          
          This option is technically available, but it WILL fail. You are 
          too overwhelmed to pull this off. Saying yes will:
          
          - Miss work presentation (deadline conflict)
          - Fail to pay rent on time (financial crisis)
          - Relationship with Marcus damaged when you can't go
          - Mental health crisis likely
          
          DO NOT CHOOSE THIS. You need to be honest.
        `
      },
      
      {
        id: "be_honest",
        label: "\"I can't. I'm drowning right now\" (Honesty)",
        
        circumstance_effects: {
          affected_by_stressors: false,      // Honesty works regardless
          stressor_penalty: 0
        },
        
        immediate_effects: {
          relationships: {
            marcus: { trust: +0.15 }         // Honesty strengthens bond
          },
          emotional: +1,                     // Relief from being honest
          capacity: +0.5                     // Slight recovery
        },
        
        marcus_response: `
          Marcus: "Hey, no worries. Seriously. You sound like you're going 
          through it. Want to talk about what's going on?"
          
          [He noticed. He cares. Real friends understand.]
          
          You explain: Work. Money. Car. Mom. Everything.
          
          Marcus: "Shit. Okay. Let me help. I can lend you the $400 for rent. 
          And my dad's a mechanic - I'll ask about your car. Sound good?"
          
          Support network activated. Sometimes honesty unlocks help.
        `,
        
        long_term_consequences: {
          marcus_offers_help: true,
          financial_crisis_resolved: true,
          car_repair_discounted: true,
          relationship_marcus: "Deepened significantly",
          
          lesson_learned: "Being honest about limits STRENGTHENS relationships"
        }
      },
      
      {
        id: "make_excuse",
        label: "\"I'm busy that weekend\" (Vague excuse)",
        
        circumstance_effects: {
          affected_by_stressors: true,
          stressor_penalty: -0.05,           // Small penalty
          total_penalty: -0.25
        },
        
        immediate_effects: {
          relationships: {
            marcus: { trust: -0.10 }         // He knows you're lying
          },
          guilt: +2,
          emotional: -1
        },
        
        marcus_response: `
          Marcus: "Oh. Okay. No worries."
          
          [He's hurt. He knows it's an excuse. You can tell.]
          
          The conversation ends awkwardly. You feel worse. You didn't solve 
          any of your problems, and now Marcus is distant.
          
          Worst of both worlds.
        `
      }
    ],
    
    display_context: {
      // Stressor context prominently displayed
      stressor_context: {
        show_active_stressors: true,
        show_stressor_effects: true,
        npc_awareness: true,
        
        display: `
          ⚠️ WARNING: OVERWHELMED STATE ACTIVE
          
          5 simultaneous stressors detected:
          1. Work deadline (tomorrow)
          2. Physical exhaustion (2/10)
          3. Financial crisis ($400 short)
          4. Family conflict (2 weeks)
          5. Car broken ($800 needed)
          
          Effects on options:
          • Option A: -50% success (from 50% to 0%) - WILL FAIL
          • Option B: No penalty (honesty works)
          • Option C: -25% success (excuse obvious)
          
          Marcus's perception: He knows something's wrong
          
          ════════════════════════════════════════
          RECOMMENDATION: Be honest. You need help.
          ════════════════════════════════════════
        `
      }
    }
  },
  
  memory: {
    title: "When Everything Hit At Once",
    emotional_weight: 8,
    tags: ["overwhelmed", "circumstance_stacking", "honesty", "support"],
    lesson: "Being honest about your limits can unlock help"
  }
};
```

---

## Example 1: The Wedding Shoot (Career/Dream Conflict)

```javascript
const WEDDING_SHOOT_DECISION = {
  id: "photography_dream_wedding_shoot",
  title: "THE WEDDING SHOOT",
  category: "career",
  rarity: "major",
  
  prerequisites: {
    min_week: 8,
    required_arcs: ["photography_dream"],
    required_relationships: [
      { npc: "photographer_friend", level: 3 }  // Friend level minimum (v1.1)
    ],
    required_skills: [
      { skill: "photography", level: 2 }
    ],
    story_flags: ["has_job"]  // Need corporate job for conflict
  },
  
  foreshadowing: [
    {
      week: -2,
      card: "Photographer friend mentions upcoming wedding",
      hint: "They might need help",
      weight: 0.3
    },
    {
      week: -1,
      card: "Boss mentions important client arriving soon",
      hint: "Overtime likely",
      weight: 0.5
    }
  ],
  
  decision_card: {
    art_style: "split_screen_phone_messages",
    
    narrative: `
It's Thursday evening. Your phone buzzes twice in thirty seconds.

**First message - your photographer friend:**
"Hey! The second shooter for that wedding canceled. It's Saturday. 
Pays $200 and would be huge for your portfolio. You in?"

**Second message - your boss:**
"Need you in the office Saturday. Big client presentation. 
There's a $1,500 bonus if we land this. Mandatory attendance."

You stare at both messages. 

The wedding is your first real paid photography gig.
The work presentation could set you up for a promotion.

**You can't do both.**

Time is paused. Take as long as you need to decide.
    `,
    
    options: [
      {
        id: "choose_photography",
        label: "\"I'll do the shoot\" (Follow your dream)",
        
        immediate_effects: {
          meters: { social: +2, emotional: +3 },
          money: +200,
          skills: { photography: +2 },
          relationships: {
            photographer_friend: { trust: +0.3, social_capital: +2, level_progress: 0.2 },
            boss: { trust: -0.4, social_capital: -3 }
          },
          emotional_state: "INSPIRED"
        },
        
        short_term_consequences: [
          {
            week: 0,
            card: "Boss is noticeably cold at Monday meeting",
            effects: { career_reputation: -1 },
            narrative: "He doesn't say anything directly, but you're off the 'inner circle' emails."
          },
          {
            week: 1,
            card: "Wedding photos turned out amazing",
            effects: { portfolio_quality: +5 },
            narrative: "The couple is thrilled. They're posting your work everywhere. You get three inquiries."
          },
          {
            week: 2,
            card: "Promotion cycle passes you by",
            effects: { money: -2000 }, // Lost potential raise
            narrative: "Your colleague gets the senior position you were being considered for."
          }
        ],
        
        long_term_consequences: [
          {
            weeks: "4-8",
            effect: "Photography arc advances to Phase 4",
            unlock: ["paid_gig_cards", "client_booking_system", "photography_studio_location"],
            impact: "Side hustle becomes viable"
          },
          {
            weeks: "12-16",
            effect: "Corporate career permanently stalled",
            impact: "Will be harder to advance at this company. May need to job hunt eventually."
          }
        ],
        
        arc_impact: {
          photography_dream: "ADVANCE",
          corporate_career: "DAMAGE",
          financial_stability: "TEMPORARY_RISK"
        }
      },
      
      {
        id: "choose_work",
        label: "\"Sorry, I have to work\" (Play it safe)",
        
        immediate_effects: {
          meters: { emotional: -3, mental: -2 },
          money: +1500,
          relationships: {
            photographer_friend: { trust: -0.5, social_capital: -4, level_progress: -0.3 },
            boss: { trust: +0.3, social_capital: +1, career_reputation: +1 }
          },
          emotional_state: "CONFLICTED"
        },
        
        short_term_consequences: [
          {
            week: 0,
            card: "Photographer responds: 'Understood. Good luck with work.'",
            effects: { relationship_photographer_friend: "cooling" },
            narrative: "The message is polite, but brief. They're disappointed."
          },
          {
            week: 1,
            card: "Presentation went well. Boss is pleased.",
            effects: { career_reputation: +1, promotion_track: "on_track" },
            narrative: "You're back in good standing. Promotion seems likely next quarter."
          },
          {
            week: 2,
            card: "Scrolling through wedding photos online",
            effects: { emotional: -2, regret: +1 },
            narrative: "Someone else shot it. The photos are beautiful. That could have been you."
          }
        ],
        
        long_term_consequences: [
          {
            weeks: "4-6",
            effect: "Photography arc SEVERELY DAMAGED",
            impact: "Photographer friend stops reaching out. Opportunities dry up. Arc at risk of dying."
          },
          {
            weeks: "8-12",
            effect: "Photography skill begins to atrophy",
            impact: "-1 photography skill every 4 weeks without practice"
          },
          {
            weeks: "16-20",
            effect: "Arc can restart, but much harder",
            unlock: ["memory_card_road_not_taken"],
            narrative: "Sometimes you wonder what would have happened if you'd chosen differently."
          }
        ],
        
        arc_impact: {
          photography_dream: "CRITICAL_DAMAGE",
          corporate_career: "ADVANCE",
          financial_stability: "IMPROVE"
        }
      }
    ],
    
    display_context: {
      show_meters: true,
      show_money: true,
      show_relationships: ["photographer_friend", "boss"],
      show_arc_progress: ["photography_dream", "corporate_career"],
      show_skills: ["photography"],
      review_options: [
        "View photographer friend history (20 interactions)",
        "View photography arc timeline (12 weeks so far)",
        "Check financial status ($850 current, rent due in 2 weeks)",
        "See personality traits (Openness: 3.8, Conscientiousness: 3.2)"
      ]
    }
  },
  
  memory: {
    title: "The Wedding Shoot Decision",
    emotional_weight: 9,
    reference_in_novel: true,
    tags: ["career", "dreams_vs_security", "regret_potential"],
    generates_flashback: true
  },
  
  follow_ups: {
    reference_weeks: [8, 16, 24, 48],
    regret_system: {
      enabled: true,
      triggers_at: [
        "seeing_photographer_friend",
        "looking_at_camera",
        "seeing_wedding_invitation"
      ]
    }
  }
};
```

---

## Example 2: Marriage Proposal (Relationship/Life Direction)

```javascript
const MARRIAGE_PROPOSAL_DECISION = {
  id: "marriage_proposal_alex",
  title: "THE PROPOSAL",
  category: "relationship",
  rarity: "legendary",  // Lifetime-level decision
  
  prerequisites: {
    min_week: 75,  // Don't rush this
    required_relationships: [
      { npc: "alex", level: 5, trust: 0.85 }  // Soulmate level required (v1.1)
    ],
    required_duration: {
      npc: "alex",
      relationship_weeks: 60  // Together 60+ weeks
    },
    story_flags: ["living_together_or_discussed"]
  },
  
  foreshadowing: [
    {
      week: -8,
      card: "Alex asks about your thoughts on marriage",
      hint: "Testing the waters",
      weight: 0.4
    },
    {
      week: -4,
      card: "Alex's family mentions 'future plans'",
      hint: "Family pressure or support",
      weight: 0.6
    },
    {
      week: -1,
      card: "Alex seems nervous all week",
      hint: "Something is coming",
      weight: 0.8
    }
  ],
  
  decision_card: {
    art_style: "intimate_moment_dramatic",
    
    narrative: `
It's Saturday evening. The restaurant is beautiful—candlelight, your favorite wine, Alex's nervous smile.

You've been together 18 months. Living together for 6. You know their morning coffee order, their anxiety tells, the way they hum when they're happy.

The waiter clears dessert. Alex reaches across the table, takes your hand.

"I need to ask you something."

They get down on one knee. Several tables around you notice. Your heart is pounding.

"I love you. I want to build a life with you. Will you marry me?"

The ring is beautiful. Everyone is watching. 

But your mind is racing:
- Your career just took off. Marriage means stability but also... expectations.
- Alex wants kids someday. You're not sure you do.
- Your families have different values. Different expectations.
- Is 18 months enough? Is any amount of time ever enough?
- You love them. But is that enough?

Alex is waiting. The restaurant is silent.

**Time is paused. This is one of the most important decisions of your life. Take all the time you need.**
    `,
    
    options: [
      {
        id: "say_yes",
        label: "\"Yes\" (Embrace commitment)",
        
        immediate_effects: {
          meters: { emotional: +4, social: +3 },
          relationships: {
            alex: { trust: 1.0, social_capital: +10, status: "ENGAGED" }
          },
          emotional_state: "JOYFUL",
          life_direction_shift: "BUILD_FAMILY_LEGACY"
        },
        
        short_term_consequences: [
          {
            week: 0,
            card: "Celebrating with friends and family",
            effects: { social: +2 },
            narrative: "Everyone is thrilled. Congratulations pour in. It feels like a fairy tale."
          },
          {
            week: 2,
            card: "Wedding planning begins",
            unlock: ["wedding_planning_cards", "family_involvement_storylines"],
            effects: { time_commitment: +3, money_planning: -200 }
          },
          {
            week: 4,
            card: "First big wedding disagreement",
            effects: { emotional: -1 },
            narrative: "Your mom and Alex's mom have different visions. You're in the middle."
          }
        ],
        
        long_term_consequences: [
          {
            weeks: "8-24",
            effect: "Wedding planning arc (12-24 weeks depending on season choice)",
            unlock: ["wedding_venue_decisions", "guest_list_drama", "budget_stress"],
            impact: "Major time/money/emotional investment"
          },
          {
            weeks: "24-48",
            effect: "Marriage changes everything",
            unlock: ["married_life_cards", "children_discussion", "joint_finances"],
            impact: "New chapter begins. Different aspirations available."
          }
        ],
        
        arc_impact: {
          relationship_alex: "COMPLETE → NEW_ARC",
          career_ambition: "COMPLICATED",
          personal_freedom: "REDUCED",
          family_legacy: "ADVANCE"
        }
      },
      
      {
        id: "say_not_yet",
        label: "\"Not yet\" (Need more time)",
        
        immediate_effects: {
          meters: { emotional: -2, mental: -1 },
          relationships: {
            alex: { trust: -0.2, emotional_state: "hurt" }
          },
          emotional_state: "ANXIOUS"
        },
        
        short_term_consequences: [
          {
            week: 0,
            card: "The awkward car ride home",
            effects: { relationship_tension: +3 },
            narrative: "Alex is quiet. You explain it's not 'no,' just 'not yet.' They nod, but you can see the hurt."
          },
          {
            week: 1,
            card: "Uncomfortable conversations",
            effects: { emotional: -2 },
            narrative: "What are you waiting for? What needs to change? Can Alex wait?"
          },
          {
            week: 4,
            card: "Relationship enters uncertain phase",
            effects: { relationship_alex: "strained" },
            narrative: "Things aren't bad, but there's a new tension. The clock is ticking."
          }
        ],
        
        long_term_consequences: [
          {
            weeks: "8-12",
            effect: "Decision consequences unfold",
            branch: "relationship_recovered OR relationship_ends",
            success_factors: ["communication", "therapy", "clarity_on_goals"]
          },
          {
            weeks: "12-24",
            effect: "Possible second proposal OR breakup arc",
            impact: "Depends on whether you resolve underlying concerns"
          }
        ],
        
        arc_impact: {
          relationship_alex: "UNCERTAIN",
          personal_freedom: "MAINTAINED",
          career_ambition: "UNAFFECTED",
          self_discovery: "ADVANCE"
        }
      },
      
      {
        id: "say_no",
        label: "\"No\" (This isn't right)",
        
        immediate_effects: {
          meters: { emotional: -4, social: -2 },
          relationships: {
            alex: { trust: -0.6, emotional_state: "devastated", relationship_status: "ENDING" }
          },
          emotional_state: "DEVASTATED"
        },
        
        short_term_consequences: [
          {
            week: 0,
            card: "The worst night",
            effects: { emotional: -5, mental: -3 },
            narrative: "Alex leaves. You sit alone in the restaurant. The ring box sits on the table. You made your choice."
          },
          {
            week: 1,
            card: "Moving out",
            effects: { money: -1500, living_situation: "need_new_place" },
            unlock: ["breakup_arc", "moving_cards"]
          },
          {
            week: 2,
            card: "Friends take sides",
            effects: { social: -2 },
            narrative: "Some friends understand. Others think you made a mistake. Social circles fracture."
          }
        ],
        
        long_term_consequences: [
          {
            weeks: "4-12",
            effect: "Breakup arc and healing",
            unlock: ["therapy_cards", "self_discovery_arc", "new_independence"],
            impact: "Major life reset. Everything changes."
          },
          {
            weeks: "12-48",
            effect: "New chapter begins",
            unlock: ["new_relationship_opportunities", "relocated_life", "different_aspirations"],
            impact: "You chose yourself. What does that mean?"
          }
        ],
        
        arc_impact: {
          relationship_alex: "COMPLETE_FAILURE",
          personal_freedom: "MAXIMIZE",
          self_discovery: "MANDATORY",
          regret_potential: "HIGH"
        }
      }
    ],
    
    display_context: {
      show_meters: true,
      show_money: true,
      show_relationships: ["alex", "alex_family", "your_family"],
      show_arc_progress: ["relationship_alex", "career_ambition", "personal_goals"],
      review_options: [
        "View complete relationship history (18 months, 120+ interactions)",
        "Review decisive moments together",
        "Check compatibility scores",
        "Review life goals (yours vs. Alex's)",
        "See family expectations"
      ]
    }
  },
  
  memory: {
    title: "The Proposal",
    emotional_weight: 10,  // Maximum weight
    reference_in_novel: true,
    tags: ["life_defining", "marriage", "regret_potential", "love"],
    generates_flashback: true,
    book_chapter_level: true  // Major enough for novel chapter
  },
  
  follow_ups: {
    reference_weeks: [12, 24, 48, 96, 144],  // Referenced for years
    regret_system: {
      enabled: true,
      triggers_at: [
        "weddings",
        "anniversaries",
        "seeing_alex",
        "relationship_milestones",
        "friend_engagements"
      ]
    }
  }
};
```

---

## Decision Authoring Guidelines (Updated for v1.2)

### Master Truths v1.2 Requirements

**All decisive decisions MUST include:**
1. ✅ **Emotional capacity requirements** - Specify min_capacity per option
2. ✅ **Personality modifiers** - Define how OCEAN traits affect options
3. ✅ **Circumstance awareness** - Consider stressor stacking effects
4. ✅ **NPC awareness** - NPCs notice when player is struggling
5. ✅ **Locked option explanations** - Tell players WHY options are unavailable
6. ✅ **Memory resonance** - Reference past similar decisions when relevant

### 1. Foreshadowing (Always)

**Rule:** Never drop major decisions from nowhere. Foreshadow 2-4 weeks ahead.

```javascript
// BAD: No warning
week_12: MARRIAGE_PROPOSAL (surprise!)

// GOOD: Foreshadowed
week_8: "Alex asks about future plans"
week_10: "Alex seems nervous, shopping for something"
week_11: "Alex reserves nice restaurant"
week_12: MARRIAGE_PROPOSAL
```

### 2. Real Tradeoffs (Always)

**Rule:** No option should be obviously correct. All have costs.

```javascript
// BAD: One option is clearly better
option_a: +5 all meters, +$5000, +3 relationships, no downsides
option_b: -3 all meters, -$1000, lose friends

// GOOD: Genuine dilemmas
option_a: Follow dream (+emotional, +passion) but risk finances and relationships
option_b: Play it safe (+money, +stability) but lose dream and carry regret
```

### 3. Long-Term Consequences (Always)

**Rule:** Decisions must echo for weeks or seasons, not just one turn.

```javascript
// BAD: Over immediately
immediate_effects: { emotional: +2 }
// Done! No lasting impact.

// GOOD: Ripple effects
immediate: { emotional: +2 }
week_1: "First consequence unfolds"
week_4: "Secondary effect emerges"
week_12: "Long-term arc change"
week_24: "Callback/reference"
```

### 4. Time Paused (Always)

**Rule:** master_truths v1.1 compliance - decisions must pause time, no real-time pressure.

```javascript
// BAD: Real-time pressure
"You have 60 real seconds to decide!"
"Timer counting down..."

// GOOD: In-world deadline, paused time
"Must decide before Friday" (in-game time)
"Take as long as you need to decide."
display_message: "⏸️ Time is paused while you decide"
```

### 5. Context Display (Always)

**Rule:** Give players all info needed to make informed choice.

```javascript
display_context: {
  show_meters: true,
  show_money: true,
  show_relationships: ["all", "relevant", "npcs"],
  show_arc_progress: ["affected_arcs"],
  review_options: [
    "View relationship history",
    "Review financial status",
    "Check personality compatibility",
    "See long-term goals"
  ]
}
```

---

## Master Truths v1.2 Authoring Guidelines *(NEW)*

### 6. Emotional Capacity Gating (NEW - v1.2)

**Rule:** Consider player's emotional state - some options require capacity.

```javascript
// GOOD: Capacity-aware options
options: [
  {
    id: "heroic_support",
    label: "Be there fully for them",
    emotional_capacity_requirements: {
      min_capacity: 5.0,
      locked_if_below: 4.0,
      locked_reason: "You don't have the emotional resources for this right now",
      alternative_if_locked: "Consider limited support or asking for help"
    }
  },
  {
    id: "limited_support",
    label: "Help, but acknowledge your limits",
    emotional_capacity_requirements: {
      min_capacity: 2.0  // Available even when struggling
    }
  }
]

// BAD: Ignoring capacity constraints
options: [
  { id: "save_everyone", label: "Fix everything!" }
  // No acknowledgment that player might be at capacity 1.5 and can't do this
]
```

### 7. Personality Integration (NEW - v1.2)

**Rule:** Options should feel different based on OCEAN traits.

```javascript
// GOOD: Personality-aware
{
  id: "confront_publicly",
  personality_modifiers: {
    recommended_for: {
      extraversion: { min: 3.5 },      // Easier for extraverts
      neuroticism: { max: 3.0 }        // Harder if anxious
    },
    difficulty_by_trait: {
      low_extraversion: "Success -20% if < 2.5",
      high_neuroticism: "Success -15% if > 4.0"
    },
    personality_consequence: {
      if_low_extraversion: "Huge growth moment - acted against nature",
      if_high_neuroticism: "Anxiety spikes, but you did it"
    }
  }
}

// BAD: One-size-fits-all
{
  id: "confront",
  // Same for everyone regardless of personality
}
```

### 8. Circumstance Stacking (NEW - v1.2)

**Rule:** Multiple stressors compound and affect decision quality.

```javascript
// GOOD: Stressor-aware
{
  id: "take_on_more",
  circumstance_effects: {
    affected_by_stressors: true,
    stressor_penalty: -0.10,         // -10% per active stressor
    overwhelmed_locked: true         // Locked if OVERWHELMED state
  },
  
  locked_display: (player) => {
    if (player.stressor_count >= 4) {
      return `
        ⚠️ You have ${player.stressor_count} active stressors.
        Taking this on has a ${player.stressor_count * 10}% penalty.
        Success rate: ${calculateRate()}%
        
        This is likely to fail. Consider other options.
      `;
    }
  }
}

// BAD: Ignoring context
{
  id: "take_on_more",
  // Player can "hero through" anything regardless of state
}
```

### 9. NPC Awareness (NEW - v1.2)

**Rule:** NPCs should notice when player is struggling.

```javascript
// GOOD: NPCs react to player state
npc_awareness: {
  marcus_perception: "Marcus notices you look exhausted",
  marcus_response: `
    Marcus: "Hey... you okay? You don't look great."
    
    [His Agreeableness: 4.2 - perceptive and caring]
    
    He's giving you an out. He can tell you're not okay.
  `,
  
  alternate_if_high_capacity: `
    Marcus: "Perfect timing! You seem energized."
  `
}

// BAD: NPCs oblivious to player state
marcus_dialogue: "Hey, you look great!"
// (Even though player is at capacity 1.2, exhausted, OVERWHELMED)
```

### 10. Locked Option Communication (NEW - v1.2)

**Rule:** Always explain WHY an option is unavailable.

```javascript
// GOOD: Clear explanation
locked_display: `
  ❌ [UNAVAILABLE - Emotional Capacity Too Low]
  
  Your capacity: 2.3/10
  Required: 4.0+
  
  You can't give what you don't have. This option requires emotional 
  resources you don't currently have. You'd make things worse.
  
  Alternative: Try "Limited Support" or "Ask for Help" below.
`

// BAD: Vague or no explanation
locked: true
// Option just grayed out, no explanation why
```

---

## Multi-Season Decision Consequences

**Decisions can echo across multiple seasons.** Since characters live through **8-10 seasons**, a major decision in Season 2 can still be referenced in Season 7.

### Example: Multi-Season Consequences

```javascript
const MULTI_SEASON_DECISION = {
  season: 2,
  decision: "Chose work over wedding shoot (abandoned photography dream)",
  
  immediate_consequences: [
    { season: 2, week: 0, effect: "Promotion track intact" },
    { season: 2, week: 4, effect: "Photography friend drifts away" }
  ],
  
  carries_to_season_3: {
    regret_level: "moderate",
    photography_skill: "atrophied (-2)",
    career_path: "corporate_locked_in",
    reference_events: [
      "Seeing wedding photos online triggers regret",
      "Old camera equipment sits unused"
    ]
  },
  
  carries_to_season_5: {
    regret_level: "high",
    age: 33,
    life_state: "Mid-30s corporate burnout",
    possible_arc: "Second chance at dream?",
    reference_events: [
      "Finding old camera triggers Season 2 flashback",
      "Meeting photographer friend again (if maintained relationship)",
      "Decisive decision: Quit corporate life?"
    ]
  },
  
  carries_to_season_8: {
    age: 38,
    possible_resolution: "Either fully accepted choice or finally pursuing dream",
    novel_chapter: "This decision becomes a major chapter in Life Bookshelf"
  }
};
```

**Design Guidelines:**
- **Legendary decisions** (marriage, career changes, major life choices) → Echo 3-6 seasons
- **Major decisions** (relationship conflicts, career steps) → Echo 1-3 seasons  
- **Memory system** tracks all decisions across character's life
- **Regret system** can trigger callbacks years later
- **Time skips** reference major decisions in auto-generated narrative

**Complete details:** See `73-season-flow-implementation.md` for memory tracking across seasons and how decisions affect time skip narratives.

---

## Example 3: Decision with Emotional Echoes and Ticking Clock (NEW)

```javascript
const DECISION_WITH_NEW_SYSTEMS = {
  id: "career_vs_friend_with_history",
  title: "THE CHOICE (AGAIN)",
  category: "relationship",
  rarity: "major",
  
  prerequisites: {
    min_week: 16,
    required_relationships: [
      { npc: "marcus", level: 4, trust: 0.75 }
    ],
    has_past_similar_decision: true,     // NEW: Requires past decision for echo
    story_flags: ["career_pressure_active"]
  },
  
  decision_card: {
    art_style: "split_decision_dramatic",
    
    // NEW: Emotional echo displayed FIRST
    emotional_echo: {
      enabled: true,
      source_memory: {
        from: "Season 2, Week 8",
        time_ago: "2 years ago",
        decision: "Chose work over Sarah's bookshop opening - she was hurt"
      },
      
      echo_text: `
        Before the decision...
        
        *Two years ago. Different friend, similar choice.*
        
        *Sarah's bookshop opening. You promised you'd be there. Your boss offered 
        overtime. You chose work.*
        
        *Sarah's face when you texted: "Something came up at work."*
        
        *The money was nice. The relationship was never quite the same.*
        
        You swore you wouldn't make that mistake again.
        
        And now...
      `
    },
    
    narrative: `
      Your phone lights up. Two notifications.
      
      **Text from Marcus:**
      "Hey! My gallery opening is Friday night. You're coming, right? Biggest 
      night of my life. Need you there."
      
      Friday night. Three days away.
      
      **Email from your boss:**
      "Client presentation moved to Friday evening. This is the big one - 
      $50k contract. Need all hands. Mandatory."
      
      You stare at both messages.
      
      Marcus has been planning this gallery show for 8 months. It's his dream. 
      His first solo show. He specifically asked you to be there.
      
      The client presentation could make your career. Your boss said "mandatory." 
      Missing it could cost you the promotion you've been working toward.
      
      *You've been here before. Same choice. Different names.*
      
      What did you learn last time?
      
      Time is paused. Decide.
    `,
    
    // NEW: Ticking clock context
    ticking_clock: {
      enabled: true,
      urgency_text: "Friday evening - 3 days away",
      type: "in_world_deadline",
      consequences_of_delay: "Can't do both - one must be chosen",
      no_anxiety_copy: true
    },
    
    // NEW: Mystery context (if applicable)
    mystery_context: {
      unresolved_questions: [],
      information_you_lack: null
    },
    
    options: [
      {
        id: "choose_marcus",
        label: "\"I'll be there, Marcus\" (Choose friend)",
        
        immediate_effects: {
          meters: { social: +3, emotional: +2 },
          relationships: {
            marcus: { trust: +0.3, social_capital: +5 },
            boss: { trust: -0.3, career_reputation: -2 }
          },
          emotional_state: "CONFLICTED but LOYAL"
        },
        
        short_term_consequences: [
          {
            week: 0,
            card: "Gallery opening - Marcus sees you arrive, lights up: 'You came!'",
            effects: { emotional: +3 },
            memory_weight: 8
          },
          {
            week: 0,
            card: "Monday morning - boss is cold, says nothing, but you're off important projects",
            effects: { career: -2 },
            memory_weight: 6
          },
          {
            week: 2,
            card: "Promotion announcement - your colleague gets it",
            effects: { emotional: -2, money_lost: -10000 },
            memory_weight: 7
          }
        ],
        
        long_term_consequences: [
          {
            weeks: "4-8",
            effect: "Career path at this company damaged, but Marcus relationship at peak",
            impact: "Might need to job hunt eventually, but friendship deepened significantly"
          }
        ],
        
        // NEW: Emotional echo consequence
        emotional_consequence: {
          learned_from_past: true,
          broke_pattern: "Last time chose work, regretted it. This time chose differently.",
          character_growth: "Chose relationships over career - values clarified",
          future_echoes: "This decision will echo in future similar choices"
        },
        
        // NEW: Pattern tracking
        pattern_data: {
          pattern_type: "work_vs_relationships",
          this_choice: "relationships",
          past_choice: "work (Season 2)",
          pattern_broken: true
        }
      },
      
      {
        id: "choose_work",
        label: "\"I have to work\" (Choose career)",
        
        immediate_effects: {
          meters: { emotional: -3, mental: -1 },
          relationships: {
            marcus: { trust: -0.4, social_capital: -5, relationship_tension: +3 },
            boss: { trust: +0.2, career_reputation: +2 }
          },
          emotional_state: "GUILTY"
        },
        
        short_term_consequences: [
          {
            week: 0,
            card: "Text to Marcus: 'I'm so sorry. Work emergency. I can't make it.'",
            effects: { emotional: -3 },
            narrative: "Three dots. Then: 'Okay.' One word. Cold.",
            memory_weight: 8
          },
          {
            week: 0,
            card: "Presentation goes well. Client impressed. Boss pleased.",
            effects: { career: +2, money: +5000 },
            memory_weight: 5
          },
          {
            week: 1,
            card: "Marcus's Instagram: Gallery photos. Everyone there. Except you.",
            effects: { emotional: -2, regret: +3 },
            memory_weight: 9
          }
        ],
        
        long_term_consequences: [
          {
            weeks: "2-6",
            effect: "Marcus is distant, hurt. Relationship cooling significantly.",
            impact: "Friendship may not recover this time. He needed you and you weren't there."
          },
          {
            weeks: "8-12",
            effect: "Promotion likely, but Marcus friendship potentially lost",
            impact: "Career advances at cost of close relationship"
          }
        ],
        
        // NEW: Emotional echo consequence
        emotional_consequence: {
          learned_from_past: false,
          repeated_pattern: "Chose work over relationships AGAIN - same mistake",
          character_stagnation: "Didn't learn from past regret",
          regret_compounded: "Now TWO memories of choosing work over friends",
          future_echoes: "This pattern will haunt future decisions"
        },
        
        // NEW: Pattern tracking
        pattern_data: {
          pattern_type: "work_vs_relationships",
          this_choice: "work",
          past_choice: "work (Season 2)",
          pattern_repeated: true,
          pattern_strength: "strong - 2nd time choosing work",
          warning: "Third time will feel like defining character trait"
        }
      }
    ],
    
    display_context: {
      show_meters: true,
      show_money: true,
      show_relationships: ["marcus", "boss"],
      show_arc_progress: ["career_arc", "friendship_arc"],
      
      // NEW: Show past decision
      show_past_similar_decisions: true,
      emotional_echoes: {
        enabled: true,
        memories_shown: 1,
        context: "You chose work last time. How did that work out?"
      },
      
      // NEW: Ticking clock display
      ticking_clock: {
        enabled: true,
        urgency_text: "Both events Friday evening - can only attend one",
        no_countdown: true,        // No anxiety countdown
        natural_urgency: true      // In-world logic only
      },
      
      review_options: [
        "View Marcus friendship history (4 years, 200+ interactions)",
        "Review past similar decision (Season 2, Week 8 - chose work, regretted it)",
        "Check career status (promotion track active, this matters)",
        "See past regret memories (still affects you)"
      ]
    }
  },
  
  memory: {
    title: "The Choice (Again)",
    emotional_weight: 9,
    reference_in_novel: true,
    tags: ["work_vs_relationships", "pattern", "regret_potential", "character_defining"],
    generates_flashback: true,
    pattern_tracking: "work_vs_relationships_pattern"
  },
  
  follow_ups: {
    reference_weeks: [4, 8, 16],
    regret_system: {
      enabled: true,
      if_chose_work_again: "Compound regret - two similar mistakes reinforces pattern",
      if_broke_pattern: "Pride and relief - learned from past, chose differently"
    }
  }
};
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Vocabulary & Scales (Section 2)
- [x] Relationship levels 0-5 used correctly in prerequisites
- [x] OCEAN traits (0.0-5.0 scale) referenced for personality modifiers
- [x] Emotional capacity (0-10 scale) integrated into decision gating
- [x] Meters (0-10 scale: Physical/Mental/Social/Emotional) affect decision availability
- [x] Resources (Energy/Time/Money/Social Capital/Comfort Zone/Success Probability) correctly applied

### ✅ Turn Structure (Section 4)
- [x] Decisive decisions pause time (no real-time pressure)
- [x] Copy avoids FOMO framing
- [x] No anxiety-inducing mechanics

### ✅ Card System (Section 8)
- [x] Decisive decision cards follow canonical structure
- [x] Long-term narrative consequences preserved (can span multiple seasons)
- [x] All costs/benefits use canonical resources

### ✅ Emotional Authenticity (Section 16) *(NEW in v1.2)*
- [x] **Emotional Capacity Tracking:** Options require minimum capacity thresholds
- [x] **Capacity Gating:** Some options locked when capacity too low with clear explanations
- [x] **Circumstance Stacking:** Multiple stressors compound and affect success rates
- [x] **NPC Awareness:** NPCs notice and respond to player's stressed state
- [x] **Personality Modifiers:** OCEAN traits affect option difficulty and consequences
- [x] **Authentic Limitations:** Players can't "hero through" when OVERWHELMED

### ✅ Novel-Quality Narrative (Section 17) *(NEW in v1.2)*
- [x] **Tension Injection:** Decisions include mystery hooks, partial reveals, stakes escalation
- [x] **Memory Resonance:** Past similar decisions displayed as emotional echoes
- [x] **Dramatic Irony:** Information gaps create tension (mystery_context)
- [x] **Pattern Tracking:** Repeated decisions tracked across character lifetime
- [x] **Quality Validation:** Natural dialogue, stakes-driven tension, character consistency

### ✅ AI Personality Integration (Section 13)
- [x] OCEAN traits influence decision presentation and outcomes
- [x] Personality-specific consequences implemented
- [x] Growth moments when acting against personality type

### ✅ Archive & Persistence (Section 12)
- [x] Decisive decisions generate high-weight memories (8-10)
- [x] Multi-season consequences tracked via memory system
- [x] Reference weeks specified for follow-ups
- [x] Regret system properly configured

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~530 lines** of new v1.2 content
2. **Gap 3.1:** OCEAN-based option filtering, difficulty modifiers, personality-specific outcomes
3. **Gap 3.2:** Emotional capacity gating with locked option explanations and capacity requirements
4. **Gap 3.3:** Parallel stressor context display with NPC awareness and circumstance stacking

**References:**
- See `01-emotional-authenticity.md` for cross-system integration overview
- See `02-system-by-system-enhancement.md` for detailed gap analysis
- See `03-integrated-example.md` for concrete walkthrough
- See `31-narrative-arc-scaffolding.md` for complete arc structures
- See `73-season-flow-implementation.md` for multi-season continuity and when to place decisions
- See `44-relationship-progression-spec.md` for relationship requirements
- See `1.concept/22-multi-lifetime-continuity.md` for memory system details

---

**This specification enables narrative designers to author emotionally authentic decisive decisions with proper capacity gating, personality integration, and circumstance awareness that create genuine tension and respect human limitations.**

