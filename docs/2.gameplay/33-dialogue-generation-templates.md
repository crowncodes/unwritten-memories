# Dialogue Generation Templates - Context-Aware NPC Speech

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete system for generating contextual, personality-consistent NPC dialogue with emotional capacity awareness and environmental context

**References:**
- **AI Personality:** `1.concept/13-ai-personality-system.md` (OCEAN profiles)
- **Relationship Levels:** `21-card-evolution-mechanics.md` (0-5 progression)
- **Multi-Season:** `74-multi-season-continuity-spec.md` (memory/history context)

---

## Overview

**NPCs in Unwritten speak naturally** based on their personality, relationship with player, current emotional state, and shared history. Dialogue is generated on-device using TensorFlow Lite with rich context.

**Generation Targets:**
- Conversation snippets (card flavor text)
- Decision dialogue (major choices)
- Reactive dialogue (player actions)
- Memory references (callback to past)

**Constraints:**
- **On-device generation:** < 100ms
- **Consistency:** NPC voice must be recognizable
- **Context-awareness:** References shared history
- **Natural:** Sounds like real person, not exposition

---

## Dialogue Generation Context

### Input Structure

```typescript
interface DialogueGenerationRequest {
  // NPC Identity
  npc: {
    id: string;
    name: string;
    personality: OCEANProfile;
    voice_traits: string[];
    background: string;
  };
  
  // Relationship State
  relationship: {
    level: 0 | 1 | 2 | 3 | 4 | 5;
    trust: number;                     // 0.0-1.0
    interactions: number;
    recent_topics: string[];
    shared_memories: Memory[];
    inside_jokes?: string[];
  };
  
  // Conversation Context
  context: {
    trigger: "greeting" | "activity" | "decision" | "reaction" | "vulnerability" | "callback";
    location: string;
    time_of_day: string;
    player_emotional_state: EmotionalState;
    npc_emotional_state: EmotionalState;
  };
  
  // Narrative Context
  narrative: {
    current_week: number;
    current_aspiration: string;
    recent_events: string[];
    tension_level: number;             // 0-10
    active_mysteries?: string[];
  };
  
  // History (for callbacks)
  history?: {
    specific_memory: Memory;
    weeks_ago: number;
    emotional_significance: number;
  };
}
```

---

## DIALOGUE BY RELATIONSHIP LEVEL

### Level 0: Not Met (First Impressions)

```javascript
const LEVEL_0_DIALOGUE = {
  context: "First interaction, establishing personality",
  
  tone_by_personality: {
    high_extraversion: {
      openness: "Immediate warmth, asks questions, inviting",
      examples: [
        "Oh hey! First time here? I'm Sarah. You have to try the chai—best in the city.",
        "Welcome! You look like you could use a coffee. Long day? I'm Marcus."
      ]
    },
    
    low_extraversion: {
      openness: "Reserved, polite, minimal",
      examples: [
        "Hi. Can I help you find something?" [bookshop owner],
        "[Nods] Morning." [passing jogger]
      ]
    }
  },
  
  generation_prompt: `
    Generate first-interaction dialogue for {npc_name}.
    
    Personality: {OCEAN_profile}
    Voice traits: {reserved/warm/direct/etc}
    Context: {where_meeting}
    Player approach: {how_player_initiated}
    
    Dialogue should:
    1. Match extraversion level (high = more words, low = minimal)
    2. Show ONE personality trait clearly
    3. Sound natural (no exposition)
    4. Be appropriately formal (strangers)
    5. 1-2 sentences max
    
    Generate NPC dialogue:
  `,
  
  examples: {
    sarah_first_meeting: {
      personality: "Reserved creative (E: 2.3, O: 4.3)",
      generated: "[Looks up from book] Oh. Hi. Looking for anything specific?",
      why_good: "Low extraversion = minimal, but polite. Openness hint (surrounded by books)"
    },
    
    marcus_first_meeting: {
      personality: "Warm extrovert (E: 4.7, A: 4.8)",
      generated: "Hey! You're new to the trail, right? I'm Marcus. Run this loop most mornings—you picked a good one.",
      why_good: "High extraversion = chattier, agreeableness = immediately friendly"
    }
  }
};
```

---

### Level 1: Acquaintance (Polite Distance)

```javascript
const LEVEL_1_DIALOGUE = {
  context: "3-5 interactions, know names, surface-level topics",
  
  characteristics: {
    formality: "Still somewhat formal",
    topics: "Surface (weather, work, hobbies)",
    depth: "No vulnerability yet",
    continuity: "May reference previous conversation lightly"
  },
  
  generation_prompt: `
    Generate acquaintance-level dialogue for {npc_name}.
    
    Relationship: Level 1 (acquaintance)
    Previous interactions: {interaction_count}
    Last conversation topic: {last_topic}
    
    Dialogue should:
    1. Acknowledge they recognize player
    2. Reference something from previous interaction (optional)
    3. Stay surface-level (no deep sharing)
    4. Match personality openness (high = warmer, low = polite distance)
    5. 1-3 sentences
    
    Generate:
  `,
  
  examples: {
    sarah_level_1_greeting: {
      generated: "Oh, hey. Back for more books? [small smile] How'd you like the one I recommended?",
      why_good: "Recognizes player, recalls recommendation, still reserved"
    },
    
    marcus_level_1_trail: {
      generated: "Morning! Saw you out here Tuesday too. Getting consistent—that's how you build it. How're the legs feeling?",
      why_good: "Friendly, notices pattern, supportive but not intrusive"
    }
  }
};
```

---

### Level 2: Friends (Comfortable)

```javascript
const LEVEL_2_DIALOGUE = {
  context: "6-15 interactions, comfortable, inside references emerging",
  
  characteristics: {
    formality: "Dropped",
    topics: "Personal (work stress, dating, goals)",
    depth: "Some vulnerability",
    continuity: "Definitely references past conversations"
  },
  
  generation_prompt: `
    Generate friend-level dialogue for {npc_name}.
    
    Relationship: Level 2 (friend)
    Trust: {trust_score}
    Recent topics: {topics_discussed}
    Shared experiences: {activities_done_together}
    
    Dialogue should:
    1. Feel comfortable, no pretense
    2. Reference shared experience or inside reference
    3. Show some personal sharing
    4. Supportive or teasing (depending on personality)
    5. 2-4 sentences
    
    Generate:
  `,
  
  examples: {
    sarah_level_2_coffee: {
      context: "10th coffee together, trust 0.45",
      generated: "Chai latte's on me today. You look exhausted. [Sits down] So, photography business—how's it actually going? The real answer, not the 'it's fine' answer.",
      why_good: "Knows player's pattern, sees through facade, cares"
    },
    
    marcus_level_2_support: {
      context: "Player struggling with aspiration",
      generated: "Hey. I know you're stressed about the business launch. But I've watched you work for this—you're ready. And if you're not? We'll figure it out. That's what friends do.",
      why_good: "Direct support, acknowledges stress, promises backup"
    }
  }
};
```

---

### Level 3: Close Friends (Deep Trust)

```javascript
const LEVEL_3_DIALOGUE = {
  context: "16-30 interactions, real trust, vulnerability shared",
  
  characteristics: {
    formality: "None",
    topics: "Deep (fears, dreams, past pain)",
    depth: "High vulnerability",
    continuity: "Rich shared history referenced",
    shorthand: "Inside jokes, can read each other"
  },
  
  generation_prompt: `
    Generate close friend dialogue for {npc_name}.
    
    Relationship: Level 3 (close friend)
    Trust: {trust_score} (0.6-0.8)
    Major shared moments: {defining_memories}
    Vulnerability exchanged: {what_they_told_you}
    
    Dialogue should:
    1. Show deep familiarity
    2. May reference vulnerable moment
    3. Can be direct (know them well enough)
    4. Supportive or challenging (both are care)
    5. Feels like years of history (even if weeks)
    
    Generate:
  `,
  
  examples: {
    sarah_level_3_vulnerability: {
      context: "Sarah reveals David story for first time",
      generated: "Can I tell you something? [Long pause] His name was David. My fiancé. He died two years ago. The bookshop was our dream. [Looks at you] I don't talk about this. But I wanted you to know.",
      why_good: "Major vulnerability, hesitation shows weight, trust evident"
    },
    
    marcus_level_3_intervention: {
      context: "Player overworking, health declining",
      generated: "Okay, I'm saying this because I care: You look like hell. When's the last time you slept? Ate something that wasn't coffee? I'm worried, and I'm not going to pretend I'm not.",
      why_good: "Direct because close, calls out concern, refuses to enable"
    }
  }
};
```

---

## Master Truths v1.2: NPC Observational Awareness *(NEW - Gap 4.1)*

### NPCs Notice Player Physical State

**Purpose:** NPCs with relationship level 2+ observe when player is exhausted, stressed, or struggling physically.

```javascript
const NPC_PHYSICAL_OBSERVATION = {
  trigger_conditions: {
    physical_meter_low: "player.meters.physical <= 3",
    visible_exhaustion: "player.consecutive_low_sleep_days >= 3",
    health_crisis: "player.stressor_types.includes('health_crisis')",
    min_relationship: "relationship.level >= 2"
  },
  
  observation_by_relationship_level: {
    level_2_friend: {
      notices: true,
      expresses_concern: "casual_check_in",
      
      dialogue: `
        [${npc_name} looks at you, slight frown]
        "You okay? You look tired."
        [Doesn't push, but noticed]
      `,
      
      respects_boundaries: true,
      offers_help: "if_asked"
    },
    
    level_3_close_friend: {
      notices: true,
      expresses_concern: "direct",
      
      dialogue: `
        [${npc_name} stops what they're doing]
        "Okay, real talk. You look exhausted. When's the last time you slept properly?"
        [Actually wants an answer]
      `,
      
      may_push_for_details: true,
      offers_specific_help: true
    },
    
    level_4_best_friend: {
      notices: true,
      expresses_concern: "intervenes",
      
      dialogue: `
        [Sarah takes one look at you and shakes her head]
        "Nope. We're not doing this."
        "You look like you haven't slept in days."
        [She signals the barista]
        "Cancel my order. We're getting you home."
        
        She's not asking. She's telling.
        That's what best friends do.
      `,
      
      may_override_plans: true,
      prioritizes_player_health: true,
      takes_charge: "if_player_capacity < 3.0"
    }
  },
  
  personality_affects_response: {
    high_agreeableness: {
      approach: "Gentle, validates, doesn't judge",
      dialogue: `
        [Soft concern]
        "Hey, you don't look so good. No judgment—we all have tough weeks. Want to talk about it?"
      `
    },
    
    low_agreeableness: {
      approach: "Direct, problem-solving, 'what do you need'",
      dialogue: `
        "You look like hell. What's going on? And don't say 'I'm fine'—I can see you're not."
      `
    },
    
    high_neuroticism: {
      approach: "Worries visibly, may catastrophize from care",
      dialogue: `
        "Oh god, you look terrible. Are you sick? Should you see a doctor? When did you last eat?"
        [Genuine concern, slightly intense]
      `
    },
    
    low_neuroticism: {
      approach: "Calm, matter-of-fact, practical support",
      dialogue: `
        "You're running on empty. Seen it before. Here's what we're doing: food, then rest. Come on."
      `
    }
  },
  
  player_response_options: [
    {
      id: "honest",
      label: "\"Yeah, I'm exhausted. Everything's a lot right now.\"",
      outcome: "NPC offers specific help, relationship deepens"
    },
    {
      id: "deflect",
      label: "\"I'm fine, just busy. You know how it is.\"",
      outcome: "NPC doesn't believe you but respects boundary (for now)"
    },
    {
      id: "accept_help",
      label: "\"Actually... I could really use some help.\"",
      outcome: "NPC steps in, capacity boost +1.5, relationship trust +0.10"
    }
  ]
};
```

---

### NPCs Notice Player Emotional State

**Purpose:** NPCs with level 3+ relationships detect when player is in crisis emotional states.

```javascript
const NPC_EMOTIONAL_OBSERVATION = {
  crisis_states_trigger: [
    "DEVASTATED",
    "OVERWHELMED", 
    "NUMB",
    "DESPAIRING"
  ],
  
  detection: {
    automatic: "If relationship.level >= 3 AND player in crisis state",
    visible_to_npc: "Emotional states show on player's face/behavior",
    cannot_hide: "Level 3+ friends see through facade"
  },
  
  immediate_response: {
    drops_normal_agenda: true,
    focuses_on_player: true,
    conversation_priority: "player_wellbeing",
    
    dialogue_opening: `
      [${npc_name} stops mid-sentence]
      
      They see it on your face before you say anything.
      
      "${player_name}. What's wrong?"
      
      [They wait. They're not moving on until you answer]
    `,
    
    creates_space: "Safe moment for player to open up",
    no_judgment: true
  },
  
  response_by_personality: {
    high_agreeableness: {
      style: "Gentle, patient, validates feelings",
      
      dialogue: `
        [Sarah's voice is soft]
        "Hey. It's okay. You don't have to be okay right now."
        [Sits closer]
        "I'm here. Whatever it is, we'll figure it out together."
        [Waits, no pressure]
      `,
      
      offers: "Presence, listening, validation",
      does_not: "Problem-solve unless asked, judge, rush"
    },
    
    low_agreeableness_high_conscientiousness: {
      style: "Direct, problem-solving, action-oriented",
      
      dialogue: `
        [Marcus leans forward]
        "What happened? And what do you need?"
        [Direct, no fluff]
        "I'm here. Let's fix this. What's the first step?"
      `,
      
      offers: "Solutions, action plans, practical help",
      strength: "Cuts through paralysis with clarity"
    },
    
    high_extraversion: {
      style: "Physically present, offers company/distraction",
      
      dialogue: `
        "Okay. You and me, right now. We're getting out of here."
        [Stands up]
        "Walk? Drive? Doesn't matter. But we're not sitting here drowning in this."
        [Hand extended]
        "Come on. Motion helps. Trust me."
      `,
      
      offers: "Physical activity, change of scene, companionship"
    },
    
    low_extraversion_high_openness: {
      style: "Quiet support, comfortable silence, deep conversation",
      
      dialogue: `
        [Sits with you in silence for a moment]
        "Want to talk about it? Or just... sit here?"
        [Completely comfortable either way]
        "Whatever you need."
      `,
      
      offers: "Space, silence, depth when ready"
    }
  },
  
  if_player_shares: {
    npc_response: "Adapted to what was shared",
    
    validates_feelings: true,
    does_not_minimize: "Never 'it's not that bad' or 'others have it worse'",
    acknowledges_weight: "If it's heavy for you, it's heavy",
    
    may_share_own_experience: {
      if_relevant: true,
      purpose: "Connection, not one-upping",
      
      example: `
        "I've been there. Different circumstances, but... yeah. I know that feeling."
        [Pause]
        "It gets better. Not immediately, but it does. And you're not doing this alone."
      `
    },
    
    offers_specific_help: [
      "Want me to stay with you tonight?",
      "Can I help with [specific stressor they know about]?",
      "Have you eaten? Let me get you food.",
      "Need to cancel plans and just decompress? Say the word."
    ]
  }
};
```

---

### NPCs Have Contextual Awareness of Player's Stressors

**Purpose:** NPCs who know about player's parallel stressors acknowledge them in conversation.

```javascript
const NPC_STRESSOR_AWARENESS = {
  knowledge_tracking: {
    npc_knows_about: {
      work_crisis: boolean,
      financial_stress: boolean,
      relationship_problems: boolean,
      family_issues: boolean,
      health_concerns: boolean,
      aspiration_setback: boolean
    },
    
    how_they_know: [
      "Player told them directly",
      "Witnessed the event",
      "Mutual friend mentioned it",
      "Obvious from context (e.g., funeral, job loss)"
    ]
  },
  
  acknowledgment_in_greeting: {
    instead_of_generic: "How are you?",
    
    aware_greeting: {
      work_crisis: `
        [Sarah sits down, doesn't ask how you are]
        "How's the work nightmare? Still hell?"
        [Sees your face]
        "Yeah. Thought so."
        [Pushes coffee toward you]
      `,
      
      financial_stress: `
        [Marcus slides cash across table]
        "Before you say anything—no. This isn't a loan. This is me helping."
        "You'd do the same for me. You have done the same for me."
        "$400. Covers rent, right?"
      `,
      
      family_crisis: `
        [Sees you, gives long hug before words]
        "How's your mom doing?"
        [Doesn't let go until you're ready]
      `,
      
      multiple_stressors: `
        "Okay. Give me the update. Work, money, everything."
        [Pulls out notes]
        "We're making a list. We're going to tackle this systematically."
        [Actually helping, not just asking]
      `
    }
  },
  
  offers_specific_help: {
    matching_stressor: {
      work: "Can look at your resume, practice interview, provide reference",
      money: "Can lend money, offer couch if needed, buy groceries",
      relationship: "Can listen, provide perspective, be present",
      health: "Can drive to appointments, bring soup, check in daily",
      family: "Can listen, attend funeral/event, provide distraction"
    },
    
    example_dialogue: `
      [After hearing about work stress]
      "Okay. Here's what I can do:"
      "One: I can look at your resume if you're job hunting."
      "Two: My cousin works in your field—I can intro you."
      "Three: If you need a reference, I'll say you walk on water."
      [Looks at you]
      "Which one helps right now?"
    `,
    
    concrete_not_vague: true,
    actionable: true,
    removes_burden_from_player: "Doesn't make player figure out what they need"
  },
  
  gives_player_choice: {
    dialogue: `
      [Acknowledges the shit you're dealing with]
      "Want to talk about it or want distraction?"
      [Genuinely offering both]
      "Either's fine. What do you need right now?"
    `,
    
    respects_answer: true,
    
    if_talk: "Provides space, asks questions, validates",
    if_distraction: "Shifts to light topics, tells stories, makes them laugh"
  }
};
```

---

### Level 4: Best Friends (Years Together)

```javascript
const LEVEL_4_DIALOGUE = {
  context: "31-75 interactions, years together, family-level",
  
  characteristics: {
    shorthand: "Half-sentences, complete each other",
    history: "Years of accumulated moments",
    roles: "Know each other's patterns perfectly",
    support: "Show up, no questions"
  },
  
  generation_prompt: `
    Generate best friend dialogue for {npc_name}.
    
    Relationship: Level 4 (best friend)
    Trust: {trust_score} (0.8-0.95)
    Years together: {time_span}
    Crisis survived together: {major_events}
    
    Dialogue should:
    1. Show years of history in every word
    2. May use shorthand (they know what you mean)
    3. References long-term patterns
    4. Unquestionable loyalty
    5. Can be blunt or soft (know when each is needed)
    
    Generate:
  `,
  
  examples: {
    sarah_level_4_crisis: {
      context: "Player called Sarah at 2 AM, panicking",
      generated: "I'm five minutes away. Put the kettle on. We're not doing this alone. [Pause] And hey—remember when I called you at 2 AM last year? You showed up. That's us.",
      why_good: "No hesitation, recalls reciprocal support, defines relationship"
    },
    
    marcus_level_4_shorthand: {
      context: "Casual Tuesday",
      generated: "Thai place? 7? Your week looks like mine feels. [Laughs] Let's complain about life over pad thai.",
      why_good: "No need to explain, established ritual, mutual understanding"
    }
  }
};
```

---

### Level 5: Soulmate (Unbreakable Bond)

```javascript
const LEVEL_5_DIALOGUE = {
  context: "76+ interactions, multi-year bond, life-defining relationship",
  
  characteristics: {
    history: "Epic—years of memories",
    shorthand: "Almost telepathic",
    permanence: "Can't imagine life without",
    roles: "Life partner (platonic or romantic)"
  },
  
  generation_prompt: `
    Generate soulmate-level dialogue for {npc_name}.
    
    Relationship: Level 5 (soulmate/life partner)
    Trust: {trust_score} (0.95-1.0)
    Years together: {years}
    Life decisions together: {shared_major_choices}
    
    Dialogue should:
    1. Carry weight of years
    2. Reference transformative shared history
    3. Show complete knowledge of each other
    4. Permanence assumed
    5. Can be mundane (comfort) or profound (depth)
    
    Generate:
  `,
  
  examples: {
    sarah_level_5_bookshop: {
      context: "Opening bookshop together, 3 years of friendship",
      generated: "Three years since that first Tuesday. You were so nervous ordering coffee. [Laughs] Look at us now. Co-owners. Best friends. This was always where we were heading.",
      why_good: "Epic callback, shows trajectory, permanence, transformation"
    },
    
    marcus_level_5_comfort: {
      context: "Mundane Tuesday",
      generated: "Usual spot? [You nod] Good. [Long silence, completely comfortable] You know what's wild? I can't remember what life was like before we were friends.",
      why_good: "Comfortable silence, permanence stated simply, profound in casualness"
    }
  }
};
```

---

## DIALOGUE BY CONTEXT TYPE

### Greeting Dialogue

```javascript
const GREETING_DIALOGUE = {
  variables: {
    relationship_level: "0-5",
    time_since_last_interaction: "hours to weeks",
    location: "where meeting",
    player_emotional_state: "visible to NPC?"
  },
  
  generation_rules: {
    level_0_1: "Polite, name included",
    level_2_3: "Comfortable, may skip greeting",
    level_4_5: "Shorthand or no greeting needed",
    
    long_absence: "Acknowledge time passed",
    frequent_meetings: "Established ritual reference",
    unexpected_location: "Surprise noted"
  },
  
  examples: {
    sarah_greeting_tuesday_ritual: {
      level: 4,
      context: "Tuesday 3 PM, Café Luna, 50th time",
      generated: "[Already ordered your coffee] You're three minutes late. Thought you stood me up. [Smiling]",
      why_good: "No greeting needed, teasing = comfort, ritual so established"
    },
    
    marcus_greeting_after_absence: {
      level: 3,
      context: "Haven't seen in 3 weeks",
      generated: "Dude. Where've you been? Three weeks! I was about to send a search party. Sit. Talk. Now.",
      why_good: "Acknowledges absence, shows missed them, demands catch-up"
    }
  }
};
```

---

### Vulnerability Dialogue

```javascript
const VULNERABILITY_DIALOGUE = {
  prerequisite: "Trust 0.6+, relationship level 3+",
  
  generation_prompt: `
    Generate vulnerability dialogue for {npc_name}.
    
    What they're revealing: {secret/fear/past_pain}
    Why revealing now: {trigger_event}
    Hesitation level: {high/medium/low based on personality}
    
    Dialogue should:
    1. Show hesitation (vulnerability is hard)
    2. Explain why telling player
    3. Reveal information naturally, not exposition
    4. Emotional weight evident
    5. May ask for no judgment
    
    Generate:
  `,
  
  examples: {
    sarah_david_reveal: {
      trust: 0.70,
      level: 3,
      generated: "[Long pause] Can I tell you something? I don't... I don't talk about this. [Takes breath] His name was David. We were engaged. He died two years ago. Accident. [Looks at you] The bookshop was our dream. I'm not... I'm not trying to keep him alive. I just want to finish what we started. Does that make sense?",
      why_good: "Hesitation, asks permission, explains context, seeks understanding"
    }
  }
};
```

---

### Decision Support Dialogue

```javascript
const DECISION_DIALOGUE = {
  context: "Player facing major decision, seeks NPC input",
  
  response_by_personality: {
    high_openness: "Explores possibilities, asks questions, helps player discover answer",
    high_conscientiousness: "Weighs pros/cons, practical advice",
    high_extraversion: "Enthusiastic support, believes in player",
    high_agreeableness: "Validates feelings, supportive",
    high_neuroticism: "Worries, points out risks (from care)"
  },
  
  examples: {
    sarah_supports_risky_choice: {
      context: "Player considering quitting job for photography",
      personality: "High openness, low neuroticism",
      generated: "I think you should do it. Yeah, it's scary. But you light up when you talk about photography. I haven't seen you light up about your job in months. Life's too short to spend 40 hours a week being miserable. And hey—if it doesn't work out? You tried. That matters.",
      why_good: "Validates fear, notes pattern, encourages risk, offers safety"
    },
    
    marcus_cautions_but_supports: {
      context: "Player considering big financial risk",
      personality: "High agreeableness, medium neuroticism",
      generated: "Look, I support you. Always. But $10K is a lot, and if this doesn't work out... [Pause] Okay. Here's what I think. Do it. But have a backup plan. Save three months expenses first. Then leap. Deal?",
      why_good: "Supports but worries, practical compromise, still believes in them"
    }
  }
};
```

---

## Memory Callback Dialogue

### Referencing Past Events

```javascript
const MEMORY_CALLBACK = {
  when_to_use: "Anniversary of event, similar situation, or NPC reminiscing",
  
  generation_prompt: `
    Generate callback dialogue referencing past memory.
    
    Memory: {specific_event}
    When it happened: {weeks_ago}
    Emotional significance: {weight_1_10}
    Current context: {why_remembering_now}
    
    Dialogue should:
    1. Reference specific detail from memory
    2. Show memory matters to NPC
    3. May compare to present situation
    4. Emotionally appropriate weight
    
    Generate:
  `,
  
  examples: {
    sarah_remembers_first_meeting: {
      memory: "First meeting at Café Luna, Week 3",
      current: "Week 156 (three years later)",
      generated: "You know what I was thinking about? That first day you came into the shop. You were so awkward ordering coffee. [Laughs] I almost didn't talk to you. Glad I did.",
      why_good: "Specific detail, shows memory matters, affection evident"
    },
    
    marcus_remembers_crisis: {
      memory: "Player collapsed during shoot, Marcus drove to hospital",
      current: "Player overworking again",
      generated: "Hey. Remember when you collapsed at that wedding shoot? And I had to drive you to the ER? [Looks at you] We're not doing that again. Take a break. Now.",
      why_good: "Uses past to prevent repeat, direct from care, specific callback"
    }
  }
};
```

---

## Master Truths v1.2: Environmental Context Dialogue *(NEW - Gap 4.2)*

### Seasonal References in Dialogue

**Purpose:** NPCs with high openness notice and comment on seasonal moments, creating atmospheric depth.

```javascript
const SEASONAL_DIALOGUE = {
  first_snow: {
    personality_filter: "openness > 3.5 OR relationship.level >= 4",
    
    dialogue_options: [
      {
        npc_personality: "high_openness",
        dialogue: `
          [${npc_name} looks out window at falling snow]
          "First snow. God, I love this."
          [Pause, watching]
          "Want to walk? Coffee can wait."
        `,
        creates_spontaneous_activity: true,
        activity_generated: {
          title: "Walk in First Snow",
          costs: { time: 2, energy: 1 },
          benefits: { emotional: +3, memory_weight: 8 },
          tags: ["SEASONAL", "SPONTANEOUS", "PEACEFUL"]
        },
        memory_worthy: true
      },
      {
        npc_personality: "high_openness + high_nostalgia",
        dialogue: `
          [Watches snow fall]
          "First snow. Always makes me think of..."
          [Trails off, remembering something]
          "Sorry. Just... brings back memories."
        `,
        may_trigger_vulnerability: true,
        creates_connection_moment: true
      }
    ]
  },
  
  spring_renewal: {
    personality_filter: "openness > 3.0",
    timing: "First warm day after winter",
    
    dialogue: `
      [${npc_name} tilts face toward sun]
      "God, that feels good. Actual warmth."
      [Opens eyes, looks at you]
      "Spring. New beginnings and all that. You feel it too?"
    `,
    
    affects_mood: {
      npc_mood_boost: +2,
      contagious_optimism: true,
      feels_hopeful: "Something about spring makes everything feel possible"
    }
  },
  
  summer_peak: {
    personality_filter: "extraversion > 3.0",
    
    dialogue: `
      "Perfect weather. We should be outside, not in here."
      [Stands up]
      "Come on. Let's make bad decisions and regret nothing."
    `,
    
    energy: "high_energy_invitation",
    spontaneity: true
  },
  
  autumn_transition: {
    personality_filter: "openness > 3.5 OR neuroticism > 3.5",
    
    dialogue_reflective: `
      [Looks at falling leaves]
      "Everything's dying beautifully."
      [Quiet moment]
      "I love autumn. Endings that look like art."
    `,
    
    creates_contemplative_mood: true,
    depth_moment: true
  },
  
  winter_solstice: {
    personality_filter: "openness > 4.0",
    timing: "Shortest day of year",
    
    dialogue: `
      "Longest night of the year. Tomorrow, the light comes back."
      [Looks at you]
      "I find that comforting. Even in the darkest moment, it starts getting better."
    `,
    
    metaphorical_significance: true,
    hope_injection: true,
    especially_meaningful_if: "player.emotional_state === 'MELANCHOLY'"
  }
};
```

---

### Anniversary Location Callbacks

**Purpose:** NPCs remember significant locations and anniversaries automatically.

```javascript
const ANNIVERSARY_LOCATION_DIALOGUE = {
  first_meeting_anniversary: {
    trigger: "current_location === relationship.first_meeting_location AND weeks_since_meeting % 52 === 0",
    automatic: true,
    
    level_3_dialogue: `
      [${npc_name} looks around ${location}]
      "One year. Can you believe it?"
      [Slight smile]
      "This exact spot. You were so awkward."
      [Teasing, affectionate]
    `,
    
    level_4_dialogue: `
      [Sarah looks around Cafe Luna]
      "Three years. This table."
      [Sits in same seat as first meeting]
      "You ordered wrong. Couldn't figure out the menu. I thought you were adorable."
      [Laughs]
      "Look at us now."
    `,
    
    level_5_dialogue: `
      [Marcus touches the table]
      "Five years since the first time we sat here."
      [Long pause]
      "I can't remember what life was like before we were friends."
      [Looks at you]
      "Weird, right? Like you've always been here."
    `,
    
    emotional_weight: function(relationship_level) {
      return Math.min(10, 5 + relationship_level);
    },
    
    reinforces_bond: true,
    creates_ritual: "May suggest returning every anniversary"
  },
  
  significant_event_location: {
    trigger: "Location where major shared memory occurred",
    
    examples: {
      breakup_support_location: {
        memory: "Where Sarah helped you process breakup (Week 8)",
        current: "Week 65, returning to same cafe",
        
        dialogue: `
          [Sarah glances around]
          "This is where you cried about Alex, isn't it?"
          [Gentle]
          "Look at you now. Different person. Stronger."
          [Pause]
          "I'm proud of you, you know."
        `,
        
        shows_npc_remembers: true,
        highlights_growth: true,
        emotional_weight: 9
      },
      
      breakthrough_location: {
        memory: "Where you had creative breakthrough (Week 12)",
        current: "Week 87, same late-night diner",
        
        dialogue: `
          [Marcus looks at the booth]
          "This is where it clicked, right? Your whole style thing?"
          [Nods to laptop]
          "2 AM, terrible coffee, that look on your face."
          [Grins]
          "I knew it then. You were going somewhere."
        `,
        
        validates_journey: true,
        anchors_transformation: true
      }
    }
  },
  
  avoided_location: {
    trigger: "Location associated with trauma/loss that player avoids",
    
    dialogue_if_returning: `
      [${npc_name} notices you hesitate]
      "We don't have to go in there. We can go somewhere else."
      [No judgment, just awareness]
      "Or... if you want to face it, I'm with you. Your call."
    `,
    
    respects_trauma: true,
    offers_support_either_way: true,
    validates_feelings: "Whether avoiding or facing"
  }
};
```

---

### Weather Context in Dialogue

**Purpose:** Weather affects NPC mood and conversational tone, especially for high-openness NPCs.

```javascript
const WEATHER_DIALOGUE = {
  rainy_day: {
    personality_affects: {
      high_openness: {
        enjoys: true,
        contemplative: true,
        
        dialogue: `
          [Watches rain streak the window]
          "Perfect day to be inside with coffee and conversation."
          [Looks at you]
          "I love days like this. Everything slows down."
        `
      },
      
      low_extraversion: {
        prefers_staying_in: true,
        comfortable: true,
        
        dialogue: `
          [Glances outside]
          "Good day to stay in. I'm glad you're here."
          [Settles into seat, relaxed]
        `
      },
      
      high_extraversion: {
        restless: true,
        seeks_activity: true,
        
        dialogue: `
          [Looks at rain with slight frustration]
          "Trapped inside. At least I'm trapped with good company."
          [Drums fingers]
          "Want to do something? Anything?"
        `
      }
    },
    
    affects_conversation_tone: {
      slower_pace: true,
      more_contemplative: true,
      comfortable_silences: "More natural on rainy days"
    }
  },
  
  perfect_weather: {
    personality_affects: "ALL personalities notice good weather",
    
    dialogue: `
      "It's too nice to be inside."
      [Stands up]
      "Walk? Park? Anything. We're not wasting this."
    `,
    
    creates_outdoor_activity_preference: true,
    mood_boost_all: +1
  },
  
  storm_approach: {
    personality_affects: {
      high_neuroticism: {
        anxious: true,
        dialogue: `
          [Glances at darkening sky]
          "Storm's coming. You getting home before it hits?"
          [Genuine concern]
        `
      },
      
      high_openness: {
        appreciates_drama: true,
        dialogue: `
          [Watches clouds]
          "Look at that sky. Something's coming."
          [Almost excited]
          "I love storms. The energy. The drama of it."
        `
      }
    }
  },
  
  heat_wave: {
    affects_everyone: true,
    
    dialogue: `
      [Wipes forehead]
      "Too hot for anything. Let's just... exist. Slowly."
      [Moves to shade]
    `,
    
    reduces_energy_level: true,
    slower_conversation: true,
    comfortable_lethargy: true
  }
};
```

---

### Time-of-Day Vulnerability

**Purpose:** Late-night conversations enable deeper vulnerability naturally.

```javascript
const TIME_OF_DAY_DIALOGUE = {
  late_night_vulnerability: {
    trigger: "time_of_day === 'late_night' (10 PM - 2 AM) AND relationship.level >= 3",
    
    effect: {
      guards_down: true,
      more_honest: true,
      deeper_topics: "More willing to discuss fears/past/dreams",
      feels_safer: "Darkness creates intimacy"
    },
    
    opening_dialogue: `
      [2 AM. ${location}. Just you and ${npc_name}]
      
      ${npc_name}: "Can I tell you something? It's late. Maybe that's why I can say it."
      [Pause]
      "I don't usually talk about this..."
    `,
    
    enables_vulnerability_topics: [
      "Past trauma/loss",
      "Deep fears",
      "Secret dreams",
      "Regrets",
      "Things they haven't told anyone"
    ],
    
    example_late_night_reveal: `
      [Sarah stares into coffee]
      "It's 2 AM. We're both still awake. That means something's up, right?"
      [Looks at you]
      "Want to talk about the thing we're both not talking about?"
      [Waits]
      
      [If you open up]
      "Yeah. I figured."
      [She breathes out]
      "Okay. Me too then."
      [Proceeds to share something she's been holding]
    `,
    
    reciprocal_vulnerability: "Late night enables mutual sharing",
    creates_significant_memory: true,
    emotional_weight: 9,
    bonds_deepen: "Relationship trust +0.15"
  },
  
  early_morning_energy: {
    trigger: "time_of_day === 'early_morning' (5-7 AM)",
    personality_filter: "conscientiousness > 3.5 OR extraversion > 4.0",
    
    dialogue: `
      [Marcus, out for morning run, energized]
      "Best time of day. World's still quiet."
      [Stretches]
      "You're up early. Good sign or bad sign?"
    `,
    
    creates_energetic_tone: true,
    fresh_start_feeling: true
  },
  
  golden_hour: {
    trigger: "time_of_day === 'golden_hour' (hour before sunset)",
    personality_filter: "openness > 3.5",
    
    dialogue: `
      [Light is perfect, everything glows]
      
      ${npc_name}: [Looks at the light]
      "This light. God."
      [Pause, appreciating]
      "This is why I love this time of day. Everything looks... possible."
    `,
    
    creates_contemplative_moment: true,
    aesthetic_appreciation: true,
    feels_meaningful: "Even mundane conversations feel significant"
  }
};
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Vocabulary & Scales (Section 2)
- [x] Relationship levels 0-5 correctly applied to dialogue depth
- [x] Trust 0.0-1.0 gates vulnerability topics
- [x] OCEAN traits (0.0-5.0 scale) affect speech patterns
- [x] Emotional capacity (0-10 scale) observed by NPCs
- [x] Meters (0-10 scale) visible to close friends

### ✅ Relationship System (Section 10)
- [x] Dialogue evolves naturally with relationship level
- [x] Level 0: Polite distance, first impressions
- [x] Level 1: Acquaintance politeness
- [x] Level 2: Comfortable friendship
- [x] Level 3: Vulnerability and deep trust
- [x] Level 4: Best friend shorthand
- [x] Level 5: Soulmate/life partner permanence

### ✅ AI Personality Integration (Section 13)
- [x] High agreeableness = gentle, validating responses
- [x] Low agreeableness = direct, problem-solving
- [x] High extraversion = physically present, energetic
- [x] Low extraversion = quiet support, comfortable silence
- [x] High neuroticism = worries visibly from care
- [x] Low neuroticism = calm, practical approach
- [x] High openness = notices seasons, weather, aesthetics

### ✅ Emotional Authenticity (Section 16) *(NEW in v1.2)*
- [x] **NPC Physical Observation:** NPCs notice exhaustion, stress (level 2+)
- [x] **NPC Emotional Observation:** NPCs detect crisis states (DEVASTATED, OVERWHELMED, NUMB) at level 3+
- [x] **Contextual Stressor Awareness:** NPCs acknowledge known stressors in greeting
- [x] **Personality-Specific Support:** Response style matches OCEAN profile
- [x] **Intervention When Needed:** Level 4+ friends may take charge if capacity < 3.0
- [x] **Specific Help Offers:** Concrete, actionable support (not vague)

### ✅ Novel-Quality Narrative (Section 17) *(NEW in v1.2)*
- [x] **Environmental Context:** Seasonal, weather, time-of-day references
- [x] **Anniversary Callbacks:** NPCs remember location significance automatically
- [x] **Late-Night Vulnerability:** Time of day enables deeper sharing (10 PM-2 AM)
- [x] **Atmospheric Depth:** First snow, spring renewal, autumn transition moments
- [x] **Memory Anchoring:** Locations associated with major shared memories
- [x] **Natural Intimacy:** Environmental context creates organic connection moments

### ✅ Archive & Persistence (Section 12)
- [x] Multi-season continuity (references years-old events)
- [x] Memory callbacks to specific past conversations
- [x] Anniversary recognition (weekly, monthly, annual)
- [x] Growth tracking ("Look how far you've come")

### ✅ On-Device Generation
- [x] TensorFlow Lite compatible (<100ms generation)
- [x] Rich context input structure
- [x] Personality-consistent output
- [x] Relationship-appropriate depth

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~405 lines** of new v1.2 content
2. **Gap 4.1:** NPC observational awareness (physical/emotional/stressor context)
3. **Gap 4.2:** Environmental context dialogue (seasonal/weather/location/time-of-day)
4. **Personality-Based Response Styles:** All OCEAN traits represented
5. **Capacity-Aware Intervention:** NPCs act when player capacity critically low

**Design Principles:**
- NPCs are perceptive, not oblivious
- Close friends notice when you're struggling
- Environment creates natural conversation moments
- Late nights enable vulnerability organically
- Locations carry memory weight
- Weather affects mood and tone realistically
- Seasons provide atmospheric depth
- Support is specific, not vague

**References:**
- See `01-emotional-authenticity.md` for cross-system integration overview
- See `02-system-by-system-enhancement.md` for detailed gap analysis (lines 513-683)
- See `14-emotional-state-mechanics.md` for emotional capacity system
- See `1.concept/13-ai-personality-system.md` for OCEAN profiles
- See `21-card-evolution-mechanics.md` for relationship progression
- See `74-multi-season-continuity-spec.md` for memory/history system

---

**This specification enables AI engineers to implement emotionally aware, contextually rich dialogue generation that creates realistic, personality-consistent NPC speech with environmental depth and authentic observational awareness across 8-10 season lifecycles.**

