# Dramatic Irony & NPC Depth System - Implementation

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete system with Master Truths v1.2 dramatic irony mechanics, knowledge gap scoring, and capacity-limited perception

**References:**
- **Arc Structure:** `31-narrative-arc-scaffolding.md` (dramatic irony beats)
- **Relationship System:** `44-relationship-progression-spec.md` (relationship levels)
- **Tension System:** `35-tension-maintenance-system.md` (mysteries and reveals)
- **Personality System:** `13-ai-personality-system.md` (OCEAN trait implementation)
- **Emotional System:** `19-emotional-state-system.md` (emotional state mechanics)

---

## Overview

**Dramatic Irony** occurs when the player knows something the character doesn't (or vice versa), creating anticipation, empathy, or understanding. The system uses NPC perspective cards, secret reveals, and character contradiction moments to deepen relationships without breaking immersion.

**Core Principle:** Show NPCs as full people with inner lives, not just supporting characters. Their thoughts, fears, and secrets exist independently of the player character.

**Enhanced Mechanics:**
- **Character Obliviousness:** Dialogue options reveal character's ignorance, creating "yelling at the TV screen" tension
- **Memory Callbacks:** Remembering dramatic irony moments enables meaningful actions in the future (e.g., remembering David's birthday one year later)
- **Trait-Driven Consequences:** OCEAN personality determines whether discovery helps or harms (jealousy, anxiety, toxic responses)
- **Real Emotional Complexity:** Current emotional state, relationship history, and personality traits all affect how character responds to secrets
- **Persistent Consequences:** Bad choices aren't forgotten—relationships remember and change accordingly

**Compliance:** master_truths v1.1 requires meaningful relationships with depth - dramatic irony serves character development, not manipulation. **All interactions must feel real, with real emotions, real behavior, and real consequences based on personality and context.**

---

## NPC Perspective Cards

### Structure & Format

```typescript
interface NPCPerspectiveCard {
  id: string;
  npc_id: string;
  title: string;                     // "What Sarah Is Really Thinking"
  
  timing: {
    week: number,
    act: 1 | 2 | 3,
    placement_reason: string          // Why now?
  };
  
  pov_narrative: string;              // Full NPC POV scene
  
  reveals: {
    player_knows_before: string,      // What player already knew
    now_revealed: string,              // What this reveals
    emotional_impact: string,          // How this should make player feel
    affects_future: string             // How this changes interactions
  };
  
  format: "internal_monologue" | "pov_scene" | "overheard_conversation";
  
  integration: {
    references_past_events: string[],
    foreshadows_future: string[],
    deepens_relationship: boolean,
    creates_empathy: boolean
  };
}
```

---

## Types of Dramatic Irony

### 1. NPC POV Scenes (Player Sees NPC's Thoughts)

```javascript
const NPC_POV_EXAMPLES = {
  sarah_grief_reveal: {
    week: 14,
    npc: "Sarah",
    title: "What Sarah Is Really Thinking",
    format: "internal_monologue",
    
    trigger: {
      condition: "Sarah has been distant for 4+ weeks",
      player_state: "Confused why Sarah is pulling away",
      mystery_active: "Who is David?"
    },
    
    narrative: `
      [Sarah's POV]
      
      You're sitting across from [Player Name] at the coffee shop. They're 
      excited about the photography gig this weekend. You smile and nod 
      at the right moments.
      
      But today is August 14th.
      
      David would be 31 today. Would have been. Is? Grammar is hard when 
      someone's dead.
      
      [Player Name] doesn't know about David. You haven't told them. How 
      do you explain: "My fiancé died two years ago and every August 14 
      I turn into a ghost of myself"?
      
      They're still talking. Something about aperture settings. You missed 
      the question.
      
      [Player Name]: "Sarah? You okay? You seem a million miles away."
      
      You: "I'm fine. Just tired."
      
      You're not fine. But you're trying. That counts for something.
      
      [Player Name] reaches across the table, squeezes your hand. They 
      don't know why you need it today, but they know you need it.
      
      Maybe someday you'll tell them.
      
      Maybe today.
    `,
    
    reveals: {
      player_knows_before: "Sarah is distant, something is wrong",
      now_revealed: "David died, today is his birthday, Sarah is grieving",
      emotional_impact: "Empathy, understanding, patience, protective",
      affects_future: [
        "Player now understands Sarah's behavior",
        "Can offer appropriate support",
        "Mystery of 'Who is David' partially answered",
        "Relationship deepens through understanding"
      ]
    },
    
    gameplay_effects: {
      mystery_progress: "+40% toward David mystery resolution",
      relationship_trust: "+0.2 (player now trusted with painful truth)",
      new_dialogue_options: [
        "Ask Sarah about David gently",
        "Offer support without pushing",
        "Be patient with her distance"
      ],
      future_event_trigger: "Sarah opens up fully about David (week 18-24)"
    },
    
    design_notes: {
      why_effective: [
        "Recontextualizes all of Sarah's behavior",
        "Creates empathy (player was frustrated, now understanding)",
        "Deepens character (Sarah is more than 'reserved friend')",
        "Advances mystery without explicit reveal",
        "Shows Sarah's internal struggle"
      ],
      frequency: "1 per major NPC per season maximum"
    }
  },
  
  marcus_intervention_planning: {
    week: 15,
    npc: "Marcus",
    title: "What Marcus Sees",
    format: "internal_monologue",
    
    trigger: {
      condition: "Player Physical meter < 3 for 3+ weeks",
      player_state: "Pushing hard for aspiration, ignoring health",
      marcus_has_noticed: true
    },
    
    narrative: `
      [Marcus's POV]
      
      You watch [Player Name] across the table at lunch. They're on their 
      third coffee. It's 1 PM.
      
      They're talking fast about the upcoming project, the deadline, how 
      close they are to the goal. "Just need to push a bit harder."
      
      You notice what they don't:
      - The dark circles that concealer can't quite hide
      - The way their hand shakes slightly reaching for the coffee
      - The fact they ordered coffee, not food
      - They've said "just push a bit harder" for three weeks now
      
      You've been talking to Sarah about it. Both worried. Neither knows 
      how to bring it up without sounding like nagging parents.
      
      Sarah thinks you should say something. You think she should.
      
      [Player Name]: "You're quiet today. Everything okay?"
      
      The irony isn't lost on you.
      
      You: "Yeah. Just... don't burn out, okay? It's not worth it."
      
      They wave it off. "I'm fine. Really."
      
      You don't think they are. And you're afraid of what comes next.
      
      You text Sarah under the table: "We need to have that conversation 
      with them. Soon."
    `,
    
    reveals: {
      player_knows_before: "Marcus seems concerned sometimes",
      now_revealed: "Marcus and Sarah discussing intervention, genuinely worried",
      emotional_impact: "Realization friends care deeply, possible wake-up call",
      affects_future: [
        "Player aware friends are watching",
        "Foreshadows intervention conversation (week 17-18)",
        "Creates tension (will they listen or push harder?)"
      ]
    },
    
    gameplay_effects: {
      foreshadows_event: "Marcus/Sarah intervention conversation (week 17)",
      tension_increase: +0.2,
      player_choice_upcoming: "Listen to friends or push harder?",
      stakes_clarified: "Friends will intervene if player doesn't change course"
    }
  }
};
```

---

### 2. Player Overhears/Discovers Secret

```javascript
const SECRET_REVEAL_EXAMPLES = {
  overhear_boss_evaluation: {
    week: 11,
    title: "What You Weren't Supposed to Hear",
    format: "overheard_conversation",
    
    setup: {
      player_location: "Break room, getting coffee",
      npc_location: "Boss's office, door slightly ajar",
      boss_thinks: "Conversation is private"
    },
    
    narrative: `
      You're in the break room, early morning coffee run. The office is quiet.
      
      Your boss's door is cracked open. Phone call. You don't mean to listen, 
      but her voice carries.
      
      Boss: "...yes, I think [Player Name] has potential, but they've been 
      distracted lately with that photography thing. Performance has slipped."
      
      You freeze, coffee pot in hand.
      
      Boss: "If they don't refocus by end of quarter... well, we have other 
      candidates for the senior position. Someone who's actually committed 
      to being here."
      
      Pause.
      
      Boss: "I'll give them until mid-November. Six weeks. Then we'll make 
      a decision."
      
      You very carefully finish pouring coffee. Very carefully walk back 
      to your desk.
      
      Six weeks. You have six weeks to prove you're "committed to being here."
      
      Or your boss will decide you're not.
    `,
    
    dramatic_irony_created: {
      player_knows: "Boss is evaluating, has 6-week deadline, job at risk",
      boss_knows: "Thinks evaluation is private, player unaware",
      creates_tension: [
        "Player has secret knowledge",
        "Can act on it or pretend ignorance",
        "Ticking clock created (6 weeks)",
        "Choice: Focus on career or continue aspiration?"
      ]
    },
    
    gameplay_effects: {
      new_hook_created: "Job performance evaluation (threat, 6 weeks)",
      tension_spike: +0.4,
      player_options: [
        {
          action: "Refocus on career",
          consequence: "Aspiration progress slows, job secure"
        },
        {
          action: "Continue aspiration focus",
          consequence: "Risk job, but pursue dream"
        },
        {
          action: "Try to balance both",
          consequence: "Difficult, requires high success rates"
        }
      ],
      decisive_decision_triggered: "Week 14-15: Career vs aspiration"
    }
  },
  
  see_npc_text_not_meant_for_you: {
    week: 8,
    title: "The Text You Weren't Supposed to See",
    format: "accidental_revelation",
    
    scenario: `
      You're at Sarah's apartment. She's in the kitchen making tea.
      Her phone is on the couch next to you.
      
      It lights up. Text from Marcus.
      
      You're not trying to read it. But it's right there:
      
      Marcus: "Did you talk to them yet? About the thing?"
      
      Sarah: "Not yet. I don't know how to bring it up. They seem so happy 
      about the photography stuff, I don't want to... you know."
      
      Marcus: "I know. But they should know what people are saying. That 
      the gallery owner mentioned them specifically."
      
      Sarah: "Tomorrow. I'll tell them tomorrow. Promise."
      
      The screen goes dark.
      
      Sarah comes back with tea, smiling.
      
      You don't mention the text. But you're very aware there's something 
      Sarah's been afraid to tell you. Something about a gallery owner.
      
      Something good? Or something bad she doesn't want to ruin your excitement?
    `,
    
    dramatic_irony_created: {
      player_knows: "Sarah has important information, has been avoiding telling you",
      sarah_knows: "She needs to tell you but is scared",
      marcus_knows: "About the thing, encouraging Sarah to speak",
      none_know_player_saw_text: true,
      
      creates_tension: [
        "Player has forbidden knowledge",
        "Wait for Sarah to tell them naturally?",
        "Or bring it up first?",
        "What is 'the thing'?"
      ]
    },
    
    player_agency: {
      option_1: {
        action: "Wait for Sarah to tell you",
        result: "Sarah brings it up week 9, respects her process"
      },
      option_2: {
        action: "Ask Sarah directly about it",
        result: "Sarah surprised, slightly hurt you saw her text, but relieved"
      },
      option_3: {
        action: "Ask Marcus what he meant",
        result: "Marcus uncomfortable being in middle, deflects to Sarah"
      }
    }
  }
};
```

---

### 3. Character Contradiction Moments

```javascript
const CHARACTER_CONTRADICTION_EXAMPLES = {
  cautious_sarah_takes_huge_risk: {
    week: 16,
    npc: "Sarah",
    title: "Sarah's Unexpected Risk",
    
    established_pattern: {
      trait: "Cautious, risk-averse, careful",
      evidence: [
        "Took 3 months to decide on haircut",
        "Still in corporate job she hates",
        "Won't try new restaurants without reviews",
        "Avoids confrontation"
      ]
    },
    
    contradiction_moment: {
      week: 16,
      event: "Sarah texts: 'I did something crazy'",
      
      narrative: `
        Your phone buzzes. Sarah.
        
        Sarah: "I did something crazy. Can we talk?"
        
        Crazy? Sarah, who color-codes her grocery lists?
        
        You meet her at the coffee shop. She's jittery. Excited. Scared.
        
        Sarah: "I quit my job."
        
        You: "...what?"
        
        Sarah: "Today. I walked into my boss's office and quit. No backup 
        plan. No safety net. I just... I'm tired of being scared."
        
        This is the woman who researches coffee shops on Yelp before 
        visiting. She quit her job. Without a plan.
        
        Sarah: "I'm opening the bookshop. David and I always talked about 
        it. I've been saving. I have enough for six months of rent on a 
        small space. And I'm just... doing it."
        
        She's crying. Smiling. Terrified.
        
        Sarah: "Tell me I'm not insane."
        
        You realize: You don't know Sarah as well as you thought you did.
        
        Or maybe grief changed her. Or maybe she was always braver than 
        she let herself be.
      `
    },
    
    reveals: {
      sarah_is_deeper_than: "Just 'the cautious friend'",
      trauma_has_changed_her: "David's death made her reevaluate everything",
      courage_was_always_there: "Fear held it back, grief released it",
      
      recontextualizes: [
        "All her caution was protection after losing David",
        "Risk aversion was survival mechanism",
        "This is the Sarah David knew - before grief"
      ]
    },
    
    gameplay_effects: {
      relationship_deepens: "Sarah trust +0.3",
      new_understanding: "Sarah as complex, evolving person",
      arc_opens: "Support Sarah's bookshop arc",
      inspiration: "Player inspired by Sarah's courage",
      
      future_references: [
        "Sarah becomes braver in future interactions",
        "Her success/failure affects player's choices",
        "Bookshop becomes location for future events"
      ]
    },
    
    design_principle: "Characters who surprise us feel real"
  },
  
  supportive_marcus_confronts: {
    week: 18,
    npc: "Marcus",
    title: "The Fight",
    
    established_pattern: {
      trait: "Supportive, encouraging, positive, 'biggest cheerleader'",
      evidence: [
        "Always says 'you can do this'",
        "Never critical, always constructive",
        "Shows up when you need him",
        "Makes you laugh when things are hard"
      ]
    },
    
    contradiction_moment: {
      week: 18,
      event: "Marcus confronts you about burnout",
      
      narrative: `
        Marcus: "We need to talk."
        
        His voice is different. Flat. Not the usual warm tone.
        
        You: "What's up?"
        
        Marcus: "I think you're making a mistake."
        
        You've never heard Marcus say this. About anything. To anyone.
        
        Marcus: "I think you're sacrificing too much. Your health. Your 
        friendships. Maybe even your job. And I think you don't want to 
        hear it, but I'm going to say it anyway."
        
        You: "Marcus—"
        
        Marcus: "No. Let me finish. I support you. You know that. I've 
        been in your corner since day one. But supporting you doesn't 
        mean I have to watch you destroy yourself and say nothing."
        
        He's not yelling. He's disappointed. Which somehow feels worse.
        
        Marcus: "Sarah and I have been watching you run yourself into 
        the ground for weeks. We've tried gentle hints. We've tried 
        concerned questions. You brush us off every time."
        
        You: "I'm fine—"
        
        Marcus: "You collapsed last week."
        
        Silence.
        
        Marcus: "I will always support your dreams. But I'm not going 
        to pretend this is healthy anymore. I love you too much to 
        watch this and say nothing."
        
        He stands up.
        
        Marcus: "When you're ready to hear us, we're here. But I'm 
        done pretending everything is fine."
        
        He leaves. You sit alone with your coffee.
        
        Marcus has never walked out on you before.
      `
    },
    
    reveals: {
      marcus_has_limits: "Support has boundaries",
      love_includes_honesty: "Real friends tell hard truths",
      marcus_depth: "Not just cheerleader, but person with values",
      
      recontextualizes: [
        "His support was never unconditional approval",
        "He's been suffering watching you struggle",
        "This confrontation is act of love, not betrayal"
      ]
    },
    
    gameplay_effects: {
      relationship_at_crossroads: true,
      player_choice_critical: {
        option_1: {
          action: "Dismiss Marcus's concern, double down",
          consequence: "Relationship damaged, Marcus distances himself"
        },
        option_2: {
          action: "Hear Marcus, make changes",
          consequence: "Relationship deepens, Marcus's respect increases"
        },
        option_3: {
          action: "Defensive, but privately consider",
          consequence: "Relationship strained but recoverable"
        }
      },
      
      future_impact: [
        "Marcus's role in life depends on player response",
        "Can strengthen or permanently damage relationship",
        "Test of whether player values honesty or comfort",
        "Defines what kind of friend player is"
      ]
    },
    
    design_principle: "Characters who challenge us feel real"
  }
};
```

---

## Placement & Timing Rules

### When to Use Dramatic Irony

```javascript
const PLACEMENT_RULES = {
  frequency: {
    npc_pov_cards: "1-2 per major NPC per season maximum",
    overheard_secrets: "1-2 per season across all NPCs",
    contradiction_moments: "1 per major NPC per season",
    
    rationale: "Overuse dilutes impact, becomes gimmick"
  },
  
  timing: {
    optimal_placement: "Mid Act II (weeks 10-18 in 24w season)",
    why: [
      "After player has spent time with NPC (investment built)",
      "Before major reveals or decisions (creates anticipation)",
      "During complications (adds depth to conflict)",
      "When tension is high (provides emotional context)"
    ],
    
    avoid: [
      "Too early (player hasn't invested in NPC yet)",
      "Too late (no time for impact to matter)",
      "During Act III climax (distracts from resolution)",
      "Back-to-back dramatic irony beats (exhausting)"
    ]
  },
  
  prerequisites: {
    relationship_level: "Minimum Level 3 (Friend)",
    weeks_knowing_npc: "Minimum 8 weeks",
    player_investment: "Player must have reason to care",
    narrative_setup: "Must have established patterns to contradict/reveal"
  }
};
```

---

## Character Obliviousness & Tension

### Dialogue Options That Showcase Ignorance

**Core Principle:** When player knows something the character doesn't, dialogue options must reflect character's realistic ignorance, creating "yelling at the screen" tension.

```typescript
interface ObliviousDialogueSet {
  context: string;                          // What player knows
  character_knows: string;                  // What character knows (limited)
  
  dialogue_options: {
    text: string,
    reveals_ignorance: boolean,             // Shows character is clueless
    player_internal_reaction: string,       // "You know this is wrong, but..."
    npc_reaction: string,                   // NPC responds to character's ignorance
    tension_increase: number
  }[];
  
  player_choice_overlay?: string;           // "(You know Sarah is grieving David...)"
}
```

#### Example: Sarah's Birthday Mystery (Player Knows About David)

```javascript
const OBLIVIOUS_DIALOGUE_EXAMPLE = {
  context: {
    player_knows: "Today is David's birthday. Sarah is grieving her dead fiancé.",
    character_knows: "Sarah seems distant and sad today. Not sure why.",
    week: 14
  },
  
  scene: `
    [Coffee shop. Sarah is quiet, barely touched her latte]
    
    Sarah: "Sorry, I'm just... not great company today."
    
    (You know exactly why. It's August 14th. David's birthday.)
  `,
  
  dialogue_options: [
    {
      text: "Want to go do something fun? Get your mind off things?",
      reveals_ignorance: true,
      
      player_overlay: "(You know this is tone-deaf, but your character doesn't...)",
      
      character_internal: "That would cheer her up, right?",
      
      npc_reaction: `
        Sarah looks at you. There's something in her expression—pain? 
        Frustration? She takes a breath.
        
        Sarah: "I just... I need to sit with this today. But thank you."
        
        You notice she didn't explain what "this" is. You've never seen her 
        so closed off.
      `,
      
      relationship_impact: -0.05,
      tension_increase: +0.2,
      
      player_feeling: "Helpless frustration (you know how to help, but character doesn't)"
    },
    
    {
      text: "You've been distant for weeks. Are you okay? Really?",
      reveals_ignorance: true,
      
      player_overlay: "(Pushing when she's grieving... but your character is worried)",
      
      character_internal: "Something is really wrong. Maybe if I push...",
      
      npc_reaction: `
        Sarah's eyes water slightly. She looks away.
        
        Sarah: "I'm dealing with something. I'll tell you when I'm ready. 
        Please don't push."
        
        The please sounds desperate. You've made it worse.
      `,
      
      relationship_impact: -0.1,
      tension_increase: +0.3,
      mystery_progress: -10,  // Set back "David mystery" by pushing too hard
      
      player_feeling: "Guilt (you pushed when you knew better)"
    },
    
    {
      text: "I'm here if you need anything. No questions.",
      reveals_ignorance: false,  // Character somehow got it right
      
      player_overlay: "(Perfect. This is what she needs.)",
      
      character_internal: "Sometimes people just need space.",
      
      npc_reaction: `
        Sarah looks at you. Really looks at you. Her eyes are wet.
        
        Sarah: "Thank you. That means more than you know."
        
        She reaches across the table and squeezes your hand.
        
        Sarah: "Today is... a hard day. But you being here helps."
      `,
      
      relationship_impact: +0.15,
      tension_release: -0.1,
      trust_increase: +0.2,
      
      player_feeling: "Relief (character got it right despite not knowing)"
    },
    
    {
      text: "Is this about David?",
      reveals_ignorance: true,  // Character SHOULDN'T know this yet
      
      immersion_break: true,  // This breaks realism
      locked_reason: "Character has no way of knowing about David yet",
      
      note: "Only unlocked if player has discovered clues in-world that would 
             give character this knowledge"
    }
  ]
};
```

---

## Memory-Based Callback System

### Remembering Key Dates & Acting On Them

**Core Mechanic:** Player can remember dramatic irony moments and choose to act on that knowledge in future weeks.

```typescript
interface MemoryCallback {
  memory_id: string;
  learned_week: number;              // When player learned the truth
  key_date?: string;                 // "August 14" (David's birthday)
  
  callback_opportunity: {
    week: number,                    // One year later, or next occurrence
    reminder: string,                // "It's August 14th again..."
    
    action_options: {
      text: string,
      requires_memory: boolean,      // Did player remember?
      trait_influenced: boolean,     // Does personality affect this choice?
      consequence: string
    }[]
  };
}
```

#### Example: Remembering David's Birthday (One Year Later)

```javascript
const MEMORY_CALLBACK_EXAMPLE = {
  learned_week: 14,  // Season 1, Week 14
  learned_date: "August 14, 2024",
  memory_content: "David's birthday. Sarah's dead fiancé.",
  
  callback_week: 66,  // Season 2, Week 14 (one year later)
  callback_date: "August 14, 2025",
  
  morning_reminder: `
    [Morning of August 14, 2025]
    
    You check your calendar. August 14th.
    
    Something tugs at your memory. Last year... 
    
    Sarah. She was so sad this day last year. Something about David.
    
    (Do you remember? Do you act on it?)
  `,
  
  action_options: [
    {
      text: "Send Sarah a message: 'Thinking of you today ❤️'",
      requires_memory: true,
      
      prerequisite: {
        openness: ">= 0.5",  // Willing to be vulnerable
        conscientiousness: ">= 0.4",  // Remembers details
      },
      
      consequence: `
        Sarah's response comes quickly:
        
        Sarah: "You remembered."
        
        Sarah: "I can't believe you remembered."
        
        Sarah: "Thank you. This year is easier. But that means everything."
        
        [Three dots appear, disappear, appear again]
        
        Sarah: "David would have liked you."
      `,
      
      relationship_impact: +0.3,
      trust_spike: +0.4,
      
      emotional_weight: "Major positive moment. Sarah feels truly seen.",
      
      player_feeling: "Deep satisfaction (you remembered when it mattered)"
    },
    
    {
      text: "Forget about it / Don't act",
      requires_memory: false,
      
      consequence: `
        The day passes normally. You don't think about it again.
        
        Later that week, Marcus mentions Sarah had a hard day on the 14th.
        
        You realize: You could have been there. You knew. But you forgot.
      `,
      
      relationship_impact: 0,
      player_feeling: "Quiet regret (missed opportunity)",
      
      note: "No punishment, but player feels natural consequence of forgetting"
    },
    
    {
      text: "Plan something: Take Sarah to David's favorite place",
      requires_memory: true,
      
      prerequisite: {
        conscientiousness: ">= 0.6",  // Plans ahead
        openness: ">= 0.5",
        emotional_intelligence: ">= 0.6"
      },
      
      consequence: `
        You suggest coffee at the waterfront café. You don't say why.
        
        Sarah arrives. Sees the location. Stops.
        
        Sarah: "This was David's favorite spot."
        
        You: "I know. I thought... maybe it would be nice to remember him 
        somewhere he loved."
        
        Sarah doesn't speak for a moment. Then:
        
        Sarah: "I've been avoiding this place for three years. I thought it 
        would hurt too much."
        
        She looks at the water.
        
        Sarah: "It does hurt. But it's also beautiful. Thank you for 
        reminding me."
        
        You spend the afternoon there. She tells you stories about David. 
        She laughs. She cries. She's healing.
      `,
      
      relationship_impact: +0.5,
      trust_spike: +0.6,
      emotional_milestone: "Sarah begins to heal from David's death",
      
      arc_progression: "Sarah's grief arc reaches resolution phase",
      
      player_feeling: "Profound emotional impact (you helped her heal)"
    }
  ]
};
```

---

## Trait-Based Discovery Consequences

### When Finding Out Makes Things Worse

**Core Principle:** Character's OCEAN traits determine how they handle discovered truths. Some personalities should NOT pursue certain knowledge.

```typescript
interface TraitDrivenConsequence {
  discovery_scenario: string;
  
  personality_risk_factors: {
    trait: string,              // "Neuroticism", "Agreeableness"
    threshold: number,          // 0.7 = high risk
    negative_outcome: string
  }[];
  
  outcomes: {
    healthy_response: string,   // Trait profile for good outcome
    toxic_response: string      // Trait profile for bad outcome
  };
}
```

#### Example: Discovering Sarah's Late Fiancé (Jealousy Risk)

```javascript
const TOXIC_DISCOVERY_EXAMPLE = {
  scenario: "Player discovers Sarah was engaged to David, deeply loved him",
  
  week: 16,
  discovery_method: "POV card reveals Sarah still loves David deeply",
  
  player_reaction_based_on_traits: {
    
    // LOW NEUROTICISM + HIGH AGREEABLENESS = Healthy Response
    healthy_profile: {
      neuroticism: "< 0.4",
      agreeableness: ">= 0.6",
      openness: ">= 0.5",
      
      internal_reaction: `
        You learn Sarah loved David deeply. Still does, in a way.
        
        You feel: Understanding. Empathy. Sadness for her loss.
        
        You think: "She's been carrying this alone. No wonder she's been distant."
      `,
      
      dialogue_options: [
        {
          text: "I'm glad David was in your life. He must have been special.",
          outcome: "Sarah feels accepted, understood, safe to grieve",
          relationship: +0.3
        },
        {
          text: "You don't have to hide your grief from me.",
          outcome: "Trust deepens, Sarah opens up more",
          relationship: +0.4
        }
      ]
    },
    
    // HIGH NEUROTICISM + LOW AGREEABLENESS = Toxic Response
    toxic_profile: {
      neuroticism: ">= 0.7",  // High anxiety, insecurity
      agreeableness: "< 0.4",  // Low empathy, competitive
      openness: "< 0.3",  // Rigid thinking
      
      internal_reaction: `
        You learn Sarah loved David deeply. Still does.
        
        You feel: Threatened. Jealous. Inadequate.
        
        You think: "How can I compete with a dead man? She'll never love 
        anyone the way she loved him."
        
        You think: "Is that why she keeps me at distance? Because I'm not him?"
      `,
      
      dialogue_options: [
        {
          text: "Do you still love him more than anyone else?",
          reveals_insecurity: true,
          
          sarah_reaction: `
            Sarah: "What? That's... that's not a fair question."
            
            You: "It's a simple question."
            
            Sarah: "He's DEAD. Why are you—"
            
            You: "And you're still in love with him."
            
            Sarah: "I think you should leave."
          `,
          
          consequence: "Relationship damage: -0.4",
          trust_broken: -0.6,
          
          future_impact: "Sarah becomes guarded, doubts your emotional maturity",
          
          player_feeling: "Immediate regret, but trait-driven impulse won"
        },
        
        {
          text: "I need to know where I stand compared to him.",
          reveals_insecurity: true,
          
          sarah_reaction: `
            Sarah looks at you like she doesn't recognize you.
            
            Sarah: "You're making this about YOU? Today? On his BIRTHDAY?"
            
            You: "I just—"
            
            Sarah: "You know what? I thought you understood. I thought you 
            were different. But you're just like everyone else who can't 
            handle that I had a life before them."
            
            She grabs her bag.
            
            Sarah: "I need space. A lot of space."
          `,
          
          consequence: "Relationship damage: -0.6",
          trust_broken: -0.8,
          
          potential_relationship_end: true,
          
          future_impact: "Sarah may end friendship if pattern continues",
          
          player_feeling: "Shame, self-awareness that you hurt her"
        },
        
        {
          text: "[Stay silent but let jealousy fester]",
          reveals_insecurity: false,  // Hidden from Sarah
          
          consequence: `
            You say nothing. But the jealousy sits in your chest.
            
            Over the next weeks, you notice things:
            - Sarah mentions David sometimes
            - She wears a ring on a chain (engagement ring?)
            - She keeps a photo of him
            
            Each thing feels like a small betrayal. You know it's irrational. 
            You can't help it.
            
            Your interactions with Sarah become strained. You're distant. 
            Cold sometimes.
            
            Sarah notices but doesn't understand why.
          `,
          
          slow_relationship_decay: -0.05 per week,
          
          future_event: "Week 22: Sarah confronts you about changed behavior",
          
          player_feeling: "Internal conflict (know it's wrong, can't stop feeling it)"
        },
        
        {
          text: "[Recognize jealousy, choose not to act on it]",
          requires_self_awareness: true,
          
          prerequisite: {
            conscientiousness: ">= 0.5",  // Self-control
            openness: ">= 0.4"  // Emotional flexibility
          },
          
          consequence: `
            You feel the jealousy. The insecurity. The inadequacy.
            
            But you recognize it for what it is: Your issue. Not hers.
            
            You take a breath. You choose compassion over insecurity.
            
            You: "I'm sorry you went through that loss. I'm here if you 
            need to talk about him."
            
            Sarah: "Thank you. That means a lot."
            
            The jealousy doesn't disappear. But you don't let it control you.
          `,
          
          relationship_impact: +0.2,
          personal_growth: +0.1,
          
          internal_note: "Character growth moment - overcame negative trait impulse",
          
          player_feeling: "Proud of choosing better path despite difficulty"
        }
      ]
    },
    
    // HIGH NEUROTICISM + HIGH CONSCIENTIOUSNESS = Anxious but Controlled
    anxious_controlled_profile: {
      neuroticism: ">= 0.6",
      conscientiousness: ">= 0.6",
      
      internal_reaction: `
        You feel the jealousy spike. The anxiety. The comparison.
        
        But you also recognize: This is your anxiety talking. This is 
        not rational. This is not fair to Sarah.
        
        You're scared. But you're not going to act on it.
      `,
      
      outcome: "Player struggles internally but makes healthy choices",
      growth_opportunity: true
    }
  },
  
  design_principle: "Personality determines whether knowledge helps or hurts"
};
```

#### Example: Discovering Partner's Secret (Trust vs. Jealousy)

```javascript
const TRUST_VS_JEALOUSY_EXAMPLE = {
  scenario: "Player overhears partner planning secret meeting",
  
  week: 12,
  
  overheard_text: `
    You're at Alex's apartment. They're in the kitchen.
    
    Their phone is on the couch. It buzzes.
    
    Message from "Jamie": "Still on for Wednesday? 7pm? Don't forget the thing."
    
    Alex: "Yep! It's all planned. Don't tell anyone."
    
    Jamie: "Your secret is safe with me 😊"
    
    You freeze. Secret? Wednesday? Jamie?
    
    Alex comes back, smiling. "Ready to watch the movie?"
    
    You don't mention the text. But your mind is racing.
  `,
  
  personality_responses: {
    
    high_trust_profile: {
      agreeableness: ">= 0.6",
      neuroticism: "< 0.4",
      
      internal_thought: "Probably a surprise for me? Or work thing? I trust Alex.",
      
      action: "Wait and see what Wednesday brings",
      
      result: `
        [Wednesday, 7:30pm]
        
        Alex: "Can you come to the park? Like, right now?"
        
        You arrive. There's a picnic setup. Fairy lights. Your favorite foods.
        Jamie is there with a camera.
        
        Alex: "Remember you said you wished someone had filmed your thesis 
        presentation for your parents? Jamie's a videographer. We recreated 
        it. Surprise!"
        
        You realize: The secret was for YOU. And you trusted them.
      `,
      
      relationship_impact: +0.4,
      
      player_feeling: "Warmth, validation that trust was correct"
    },
    
    high_anxiety_profile: {
      neuroticism: ">= 0.7",
      agreeableness: "< 0.5",
      
      internal_thought: "Who is Jamie? Why is it secret? Are they cheating?",
      
      action_options: [
        {
          text: "Ask Alex directly about Jamie",
          
          outcome: `
            You: "Who's Jamie?"
            
            Alex: "Jamie? From work. Why?"
            
            You: "Just... saw the name on your phone. What are you doing 
            Wednesday?"
            
            Alex: "I... it's a surprise. Can you trust me?"
            
            You: "Are you seeing someone else?"
            
            Alex stops. Looks hurt.
            
            Alex: "Are you serious right now? I'm planning something NICE 
            for you and you think I'm CHEATING?"
            
            The surprise is ruined. The trust is damaged.
          `,
          
          consequence: "Relationship damage: -0.3, surprise ruined",
          
          player_feeling: "Regret mixed with residual anxiety"
        },
        
        {
          text: "Follow Alex on Wednesday (stalking)",
          
          outcome: `
            You follow Alex to the park. Stay hidden.
            
            You see: Picnic setup. Fairy lights. Jamie with camera equipment.
            
            Alex checks their phone: "Where are you? Everything's ready!"
            
            You realize: You just stalked your partner. Who was planning 
            something nice for you.
            
            You text back: "Sorry, running late."
            
            You arrive. Pretend to be surprised. Pretend you didn't just 
            follow them because you didn't trust them.
            
            You enjoy the surprise. But you feel sick with guilt.
          `,
          
          consequence: "Relationship unchanged externally, -0.2 internal guilt",
          secret_kept: "Player knows they crossed line, Alex doesn't know",
          
          future_impact: "Player carries guilt, may affect future interactions",
          
          player_feeling: "Shame (you violated trust based on insecurity)"
        },
        
        {
          text: "Struggle with anxiety, choose to trust",
          
          prerequisite: {
            conscientiousness: ">= 0.5"
          },
          
          outcome: `
            The anxiety eats at you. Wednesday. Jamie. Secret.
            
            But you choose: I will trust Alex. Even though it's hard.
            
            Wednesday arrives. The surprise. It was for you.
            
            Later, Alex: "You okay? You seem relieved."
            
            You could tell the truth. Or not.
          `,
          
          followup_choice: "Admit you struggled with trust, or keep it hidden?",
          
          growth_opportunity: true
        }
      ]
    }
  },
  
  design_principle: "Same information, different personalities, different outcomes"
};
```

---

## OCEAN Trait Integration Matrix

### How Personality Affects Dramatic Irony Response

```javascript
const TRAIT_RESPONSE_MATRIX = {
  openness: {
    high: {
      response_to_secrets: "Curious, understanding, flexible interpretation",
      example: "Wonders about context, considers multiple explanations"
    },
    low: {
      response_to_secrets: "Rigid thinking, jumps to conclusions",
      example: "Sees things in black/white, struggles with ambiguity"
    }
  },
  
  conscientiousness: {
    high: {
      response_to_secrets: "Remembers details, plans actions, self-controlled",
      example: "Remembers David's birthday a year later, plans thoughtful gesture"
    },
    low: {
      response_to_secrets: "Forgets details, acts impulsively",
      example: "Knows Sarah is grieving, blurts out insensitive comment anyway"
    }
  },
  
  extraversion: {
    high: {
      response_to_secrets: "Wants to talk about it, seeks external processing",
      example: "Struggles to keep secret, wants to discuss with friends"
    },
    low: {
      response_to_secrets: "Processes internally, comfortable with secrets",
      example: "Sits with knowledge quietly, doesn't need to share"
    }
  },
  
  agreeableness: {
    high: {
      response_to_secrets: "Empathetic, assumes best intentions",
      example: "Partner has secret meeting → 'Probably planning something nice'"
    },
    low: {
      response_to_secrets: "Suspicious, competitive, assumes worst",
      example: "Partner has secret meeting → 'Probably cheating'"
    }
  },
  
  neuroticism: {
    high: {
      response_to_secrets: "Anxious, worst-case scenarios, emotional volatility",
      example: "Can't stop thinking about it, obsesses, acts on fear"
    },
    low: {
      response_to_secrets: "Calm, stable response, trusts process",
      example: "Notes the information, waits to see how it unfolds"
    }
  }
};
```

---

## Emotional State Modifiers

### Current Mood Affects Response to Dramatic Irony

```javascript
const EMOTIONAL_STATE_MODIFIERS = {
  example: "Player discovers Sarah is grieving David",
  
  player_in_good_emotional_state: {
    physical: ">= 7",
    emotional: ">= 7",
    stress: "< 4",
    
    response: "More patient, empathetic, controlled responses available",
    
    dialogue_quality: "Higher EQ options unlocked"
  },
  
  player_in_poor_emotional_state: {
    physical: "< 4",
    emotional: "< 4",
    stress: ">= 7",
    
    response: "Irritable, self-centered, reactive responses more likely",
    
    dialogue_quality: "EQ options locked, more selfish options appear",
    
    example: `
      [Player is burned out, stressed, exhausted]
      
      Sarah: "I'm having a hard day."
      
      Player options:
      
      ❌ LOCKED: "I'm here if you need anything" 
         (Requires Emotional >= 6)
      
      ✅ AVAILABLE: "Me too. Everything is terrible."
         (Self-centered, but honest given state)
      
      ✅ AVAILABLE: "Can we talk about this later? I'm barely holding it together."
         (Honest boundary-setting, but not supportive)
    `
  },
  
  design_principle: "Player's current state affects ability to respond well to others' pain"
};
```

---

## Integration with Mystery System

### Dramatic Irony as Clue Delivery

```javascript
const MYSTERY_INTEGRATION = {
  example: "David Mystery",
  
  clue_progression: [
    {
      week: 4,
      type: "mention",
      method: "dialogue",
      clue: "Sarah mentions David in passing"
    },
    {
      week: 9,
      type: "photograph",
      method: "environmental",
      clue: "Photo of David seen in Sarah's apartment"
    },
    {
      week: 14,
      type: "POV_REVEAL",
      method: "dramatic_irony",
      clue: "Sarah POV card reveals David died, today is birthday, still grieving",
      
      why_effective: [
        "Player learns truth without Sarah explicitly telling character",
        "Creates anticipation (when will character learn?)",
        "Builds empathy (player understands before character)",
        "Makes eventual reveal more emotional (player has been waiting)"
      ]
    },
    {
      week: 20,
      type: "full_reveal",
      method: "sarah_finally_tells_character",
      emotional_weight: "Maximum (player knew, finally character knows)",
      
      narrative_power: "Player feels relief character finally knows what they've known"
    }
  ],
  
  design_principle: "Dramatic irony can advance mysteries without explicit exposition"
};
```

---

## Master Truths v1.2: Knowledge Gap Scoring *(NEW)*

### Quantifying Dramatic Irony Effectiveness

**Core Principle:** Dramatic irony should meet minimum threshold (≥ 0.6) for maximum emotional impact.

```javascript
const KNOWLEDGE_GAP_SCORING = {
  purpose: "Measure effectiveness of dramatic irony moment",
  threshold: 0.6,  // Master Truths v1.2 Section 17
  
  scoring_formula: function(ironyMoment) {
    const factors = {
      knowledge_clarity: scoreKnowledgeClarity(ironyMoment),
      tension_created: scoreTensionLevel(ironyMoment),
      emotional_weight: scoreEmotionalImpact(ironyMoment),
      player_investment: scorePlayerInvestment(ironyMoment),
      timing_quality: scoreTimingQuality(ironyMoment)
    };
    
    // Weighted average
    const score = 
      (factors.knowledge_clarity * 0.25) +
      (factors.tension_created * 0.25) +
      (factors.emotional_weight * 0.25) +
      (factors.player_investment * 0.15) +
      (factors.timing_quality * 0.10);
    
    return score;  // 0.0-1.0
  },
  
  components: {
    knowledge_clarity: {
      description: "How clear is the knowledge gap?",
      
      scoring: {
        high: {
          score: 0.9,
          example: "Player knows Sarah's fiancé died. Character has no idea."
        },
        moderate: {
          score: 0.6,
          example: "Player suspects something about David. Character oblivious."
        },
        low: {
          score: 0.3,
          example: "Both player and character vaguely aware something's off."
        }
      }
    },
    
    tension_created: {
      description: "How much anticipation/dread does gap create?",
      
      scoring: {
        high: {
          score: 0.9,
          example: "Character about to make terrible mistake player can see coming"
        },
        moderate: {
          score: 0.6,
          example: "Character missing obvious social cue player notices"
        },
        low: {
          score: 0.3,
          example: "Minor misunderstanding with low stakes"
        }
      }
    },
    
    emotional_weight: {
      description: "How emotionally impactful is the gap?",
      
      scoring: {
        high: {
          score: 0.9,
          example: "Sarah grieving dead fiancé while character suggests fun outing"
        },
        moderate: {
          score: 0.6,
          example: "Character misreading NPC's mood, offering wrong support"
        },
        low: {
          score: 0.3,
          example: "Character unaware NPC prefers tea over coffee"
        }
      }
    },
    
    player_investment: {
      description: "How much does player care about outcome?",
      
      scoring: {
        high: {
          score: 0.9,
          prerequisite: "Level 4-5 relationship, or player aspiration at stake"
        },
        moderate: {
          score: 0.6,
          prerequisite: "Level 2-3 relationship, or secondary concern"
        },
        low: {
          score: 0.3,
          prerequisite: "Low-stakes NPC or minor situation"
        }
      }
    },
    
    timing_quality: {
      description: "Is this the right moment for this irony?",
      
      scoring: {
        optimal: {
          score: 0.9,
          example: "Mid Act II after player invested, before resolution"
        },
        adequate: {
          score: 0.6,
          example: "Early Act II or late Act II"
        },
        poor: {
          score: 0.3,
          example: "Too early (player not invested) or too late (no time for impact)"
        }
      }
    }
  }
};
```

**Example Calculation:**

```javascript
const SARAH_DAVID_IRONY_SCORED = {
  moment: "Sarah grieving David's birthday, character offers to 'cheer her up'",
  
  scoring: {
    knowledge_clarity: 0.95,  // Player knows exactly why Sarah is sad
    tension_created: 0.85,    // Player dreading character's tone-deaf response
    emotional_weight: 0.90,   // High emotional stakes (grief)
    player_investment: 0.80,  // Level 3 relationship, player cares
    timing_quality: 0.75,     // Mid Act II, good placement
    
    calculated_score: (0.95 * 0.25) + (0.85 * 0.25) + (0.90 * 0.25) + (0.80 * 0.15) + (0.75 * 0.10),
    
    final_score: 0.87  // ✅ PASSES v1.2 threshold (≥ 0.6)
  },
  
  why_effective: [
    "Crystal clear knowledge gap",
    "High tension (player watching trainwreck)",
    "Emotionally weighty (grief)",
    "Player invested in Sarah",
    "Well-timed in narrative"
  ]
};
```

---

## Master Truths v1.2: Capacity-Limited Irony Perception *(NEW)*

### Low Capacity Reduces Ability to Perceive Others

**Core Principle:** When player's capacity is low, character can't recognize or respond appropriately to dramatic irony moments.

```javascript
const CAPACITY_LIMITED_IRONY = {
  principle: "Exhausted people can't read social cues well",
  
  example: "Sarah is visibly grieving, character should notice",
  
  perception_at_high_capacity: {
    capacity: 8,
    physical: 8,
    emotional: 8,
    
    character_perceives: `
      Sarah is off today. Really off.
      
      She's barely touched her coffee. Eyes red, like she's been crying.
      Keeps checking her phone. Distracted.
      
      Something is wrong. You ask: "You okay? You seem... not okay."
    `,
    
    dialogue_options: [
      "You okay? You seem upset.",  // Observant, appropriate
      "Want to talk about it?",  // Offering support
      "I'm here if you need anything."  // Good friend response
    ],
    
    player_feeling: "Character is perceptive, caring, present"
  },
  
  perception_at_moderate_capacity: {
    capacity: 5,
    physical: 5,
    emotional: 5,
    
    character_perceives: `
      Sarah seems quiet today.
      
      You notice, but you're also tired. A lot on your mind.
      Work stress. Money worries. Haven't slept great.
      
      Sarah: [silent, looking at phone]
      
      You: "Everything okay?"
      
      You're trying. But you're not... fully present.
    `,
    
    dialogue_options: [
      "You okay?",  // Basic check-in, not deeply perceptive
      "You've been quiet.",  // Observation but no empathy
      "[Say nothing, assume she's fine]"  // Missing cues due to own state
    ],
    
    player_feeling: "Character is trying but not fully attentive"
  },
  
  perception_at_critical_capacity: {
    capacity: 2,
    physical: 3,
    emotional: 2,
    stress_load: 9,
    
    character_perceives: `
      You're at coffee with Sarah. You think. Hard to focus.
      
      Work crisis. Money problems. Exhausted. Overwhelmed.
      
      Sarah is saying something. You missed it.
      
      Sarah: "...anyway."
      
      You: "Sorry, what?"
      
      You don't notice she's upset. You're too deep in your own crisis.
      You don't see her red eyes. Your own are worse.
      You don't notice her distraction. You're more distracted.
      
      Your capacity is too low to perceive anyone else's pain.
    `,
    
    dialogue_options: {
      locked_empathetic: [
        "❌ LOCKED: 'You seem upset. What's wrong?' (Requires Emotional >= 5)",
        "❌ LOCKED: 'I'm here for you' (Requires Capacity >= 4)"
      ],
      
      available_self_focused: [
        "✅ 'Sorry, I'm so distracted today. Work is insane.'",
        "✅ [Zone out, barely listening]",
        "✅ 'Can we cut this short? I have so much to do.'"
      ]
    },
    
    dramatic_irony_failure: {
      player_knows: "Sarah is grieving David's birthday",
      character_misses: "Completely misses all signals due to own exhaustion",
      
      consequence: "Sarah feels alone, unseen, abandoned during painful moment",
      relationship_impact: -0.15,
      
      narrative: `
        Sarah needed you today. Needed you to SEE her.
        
        But you were too exhausted to see anything but your own problems.
        
        Later that week, Marcus mentions: "Sarah had a really hard day Thursday. 
        She said you met for coffee but you seemed... elsewhere."
        
        Thursday. David's birthday. She was reaching out.
        
        And you missed it completely.
      `
    },
    
    player_feeling: "Guilt (realized you failed someone who needed you)"
  },
  
  design_principle: "Low capacity = can't perceive or respond to others' needs appropriately"
};
```

---

## Master Truths v1.2: Three Response Types *(NEW)*

### Categorizing Character Responses to Dramatic Irony

**Core Principle:** There are three main response types when character doesn't know what player knows: tone-deaf, misguided, growth.

```javascript
const THREE_RESPONSE_TYPES = {
  
  type_1_tone_deaf: {
    description: "Character response is clearly inappropriate (player cringes)",
    
    causes: [
      "Character completely oblivious to situation",
      "Low emotional intelligence",
      "Too focused on own agenda",
      "Low capacity (can't read cues)"
    ],
    
    example: {
      context: "Player knows Sarah is grieving David (dead fiancé)",
      
      tone_deaf_response: `
        Character: "You've been so down lately! Let's go out and have FUN! 
        Maybe we can find you a date!"
      `,
      
      sarah_reaction: `
        Sarah's face. You'll remember that look forever.
        
        Sarah: "I... I need to go."
        
        She leaves. You don't understand why.
      `,
      
      player_experience: "Cringe, 'No, don't say that!', helpless watching mistake",
      
      consequence: "Relationship damage, Sarah feels misunderstood",
      
      why_tone_deaf: [
        "Completely misreads emotional state",
        "Suggests romance when she's grieving dead fiancé",
        "Focus on fun when she needs space for grief",
        "Total empathy failure"
      ]
    },
    
    gameplay_purpose: "Create 'yelling at screen' tension, show cost of obliviousness"
  },
  
  type_2_misguided: {
    description: "Character tries to help but wrong approach (player sympathizes)",
    
    causes: [
      "Character notices something wrong",
      "Wants to help but doesn't have full context",
      "Good intentions, wrong execution",
      "Trying their best with incomplete information"
    ],
    
    example: {
      context: "Player knows Sarah is grieving David, character knows something's wrong",
      
      misguided_response: `
        Character: "Hey, I can tell something's been bothering you. 
        Want to talk about it? I'm here."
      `,
      
      sarah_reaction: `
        Sarah: "I... not today. But thank you. Really."
        
        She squeezes your hand. You didn't fix it, but you tried.
        She noticed you trying.
      `,
      
      player_experience: "Warm feeling - character got it partly right despite not knowing",
      
      consequence: "Neutral to slight positive, Sarah appreciates attempt",
      
      why_misguided_not_tone_deaf: [
        "Character recognized something wrong",
        "Offered support, didn't push agenda",
        "Gave Sarah space to decline",
        "Genuine empathy attempt"
      ]
    },
    
    gameplay_purpose: "Show character trying despite knowledge gap, create sympathy"
  },
  
  type_3_growth: {
    description: "Character somehow gets it right (player relieved/proud)",
    
    causes: [
      "High emotional intelligence",
      "Learned from past mistakes",
      "Personality traits align (high agreeableness, low neuroticism)",
      "Good capacity + empathy",
      "Lucky instinct"
    ],
    
    example: {
      context: "Player knows Sarah is grieving, character doesn't know details",
      
      growth_response: `
        Character: "I don't know what's going on today. But I'm here 
        if you need anything. No questions. Just... here."
      `,
      
      sarah_reaction: `
        Sarah's eyes water. She squeezes your hand.
        
        Sarah: "Thank you. That means more than you know."
        
        Later, weeks later, she'll tell you: "That day you didn't push. 
        That day you just... were there. I needed that."
      `,
      
      player_experience: "Relief, pride, 'Thank god character got it right'",
      
      consequence: "Significant positive impact, trust increase +0.20",
      
      why_this_worked: [
        "Recognized pain without needing details",
        "Offered support without demanding vulnerability",
        "Respected Sarah's boundaries",
        "Sometimes not knowing is okay if you're present"
      ]
    },
    
    gameplay_purpose: "Reward good character development, show growth, create satisfaction"
  },
  
  distribution: {
    low_EQ_player: "70% tone-deaf, 25% misguided, 5% growth",
    moderate_EQ_player: "30% tone-deaf, 50% misguided, 20% growth",
    high_EQ_player: "10% tone-deaf, 40% misguided, 50% growth",
    
    capacity_affects: "Low capacity shifts toward tone-deaf even for high-EQ players"
  }
};
```

**Implementation Example:**

```javascript
function determineResponseType(player, situation, dramaticIrony) {
  let responseType;
  
  // Factor 1: Emotional Intelligence
  const EQ = calculateEQ(player.personality);
  
  // Factor 2: Current Capacity
  const capacity = player.emotional_capacity;
  
  // Factor 3: Relationship Level
  const relationship = situation.relationship_level;
  
  // Calculate probabilities
  let tone_deaf_prob = 0.3;
  let misguided_prob = 0.5;
  let growth_prob = 0.2;
  
  // Adjust for EQ
  if (EQ < 0.4) {
    tone_deaf_prob += 0.3;
    growth_prob -= 0.2;
  } else if (EQ > 0.7) {
    tone_deaf_prob -= 0.2;
    growth_prob += 0.3;
  }
  
  // Adjust for capacity
  if (capacity <= 3) {
    tone_deaf_prob += 0.4;  // Exhausted = oblivious
    growth_prob = 0;  // No growth responses when exhausted
  } else if (capacity >= 8) {
    tone_deaf_prob -= 0.2;
    growth_prob += 0.2;
  }
  
  // Adjust for relationship
  if (relationship >= 4) {
    growth_prob += 0.15;  // Know them well enough to intuit
  }
  
  // Normalize probabilities
  const total = tone_deaf_prob + misguided_prob + growth_prob;
  tone_deaf_prob /= total;
  misguided_prob /= total;
  growth_prob /= total;
  
  // Select response type
  const roll = Math.random();
  if (roll < tone_deaf_prob) {
    responseType = "tone_deaf";
  } else if (roll < tone_deaf_prob + misguided_prob) {
    responseType = "misguided";
  } else {
    responseType = "growth";
  }
  
  return {
    type: responseType,
    probabilities: { tone_deaf_prob, misguided_prob, growth_prob }
  };
}
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Dramatic Irony System (v1.1 Foundation)
- [x] Dramatic irony serves character depth, not manipulation
- [x] NPCs have inner lives independent of player
- [x] No fourth-wall breaks (everything stays in-world)
- [x] Relationship levels respected (min Level 3 for POV cards)
- [x] Player agency maintained (can act on knowledge or not)
- [x] Creates empathy and understanding, not anxiety
- [x] Character obliviousness creates authentic tension
- [x] Memory callbacks reward player attention
- [x] OCEAN traits determine healthy vs. toxic responses
- [x] Discovery can have negative consequences
- [x] Emotional state affects dialogue quality
- [x] Real consequences based on personality

### ✅ Master Truths v1.2: Dramatic Irony Enhancements *(NEW)*
- [x] **Knowledge Gap Scoring System (≥ 0.6 threshold)**
  - 5 scoring components: Clarity, Tension, Weight, Investment, Timing
  - Weighted formula: 25% + 25% + 25% + 15% + 10% = 1.0
  - Example: Sarah/David scenario scores 0.87 (passes threshold)
- [x] **Capacity-Limited Irony Perception**
  - High capacity (≥8): Character perceptive, caring, present
  - Moderate capacity (5-7): Character trying but not fully attentive
  - Critical capacity (≤3): Character misses all signals, self-focused only
  - Empathetic options locked when capacity too low
- [x] **Three Response Types**
  - Tone-Deaf: Inappropriate, player cringes, relationship damage
  - Misguided: Good intentions, wrong approach, player sympathizes
  - Growth: Gets it right, player relieved/proud, trust increase
  - Distribution based on EQ + capacity + relationship level

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~500 lines** of new v1.2 dramatic irony mechanics
2. **Knowledge gap scoring** - quantify effectiveness with 5-component weighted system
3. **Capacity-limited perception** - exhausted characters can't read social cues
4. **Three response types** - tone-deaf, misguided, growth with probability distributions
5. **Failed irony moments** - low capacity = missed Sarah's grief, guilt later
6. **EQ + capacity response calculation** - determines which type character exhibits

**Knowledge Gap Scoring Components:**
- Knowledge Clarity (25%): How clear is the gap? (0.3-0.9)
- Tension Created (25%): How much anticipation? (0.3-0.9)
- Emotional Weight (25%): How impactful? (0.3-0.9)
- Player Investment (15%): How much do they care? (0.3-0.9)
- Timing Quality (10%): Right moment? (0.3-0.9)

**Capacity Effects on Irony:**
- Capacity 8: "Sarah is off today. Really off. You ask: 'You okay?'" (perceptive)
- Capacity 5: "Sarah seems quiet. You're trying. Not fully present." (partial)
- Capacity 2: "You don't notice she's upset. Too deep in own crisis." (failure)

**Three Response Type Distribution:**
- Low EQ: 70% tone-deaf, 25% misguided, 5% growth
- Moderate EQ: 30% tone-deaf, 50% misguided, 20% growth
- High EQ: 10% tone-deaf, 40% misguided, 50% growth
- Low capacity shifts ALL toward tone-deaf (even high-EQ players)

**Design Principles:**
- Dramatic irony effectiveness is measurable (≥ 0.6)
- Low capacity = can't perceive or respond appropriately
- Three response types create varied emotional experiences
- Growth responses reward high EQ + good capacity + deep relationships
- Tone-deaf responses show cost of obliviousness or exhaustion

**References:**
- See `01-emotional-authenticity.md` for cross-system integration
- See `14-emotional-state-mechanics.md` for capacity calculation
- See `31-narrative-arc-scaffolding.md` for dramatic irony beat placement
- See `35-tension-maintenance-system.md` for mystery system integration
- See `36-stakes-escalation-mechanics.md` for consequence moments and capacity-limited perception
- See `44-relationship-progression-spec.md` for relationship level requirements
- See `13-ai-personality-system.md` for OCEAN trait implementation
- See `19-emotional-state-system.md` for emotional state mechanics

---

## Implementation Checklist

### For Dialogue Writers
- [ ] Create oblivious dialogue options that reveal character's ignorance
- [ ] Add player overlays: "(You know this is wrong, but...)"
- [ ] Write trait-specific internal reactions to dramatic irony
- [ ] Design both healthy and toxic response paths
- [ ] Include emotional state prerequisites for empathetic options

### For Systems Designers
- [ ] Implement memory callback triggers (key dates, anniversaries)
- [ ] Create trait-based dialogue filtering (lock/unlock based on OCEAN)
- [ ] Build emotional state modifiers for dialogue availability
- [ ] Design consequence tracking for jealousy, trust violations
- [ ] Implement slow relationship decay for festering resentment

### For Narrative Designers
- [ ] Identify dramatic irony moments in each major NPC arc
- [ ] Plan POV card placement (1-2 per NPC per season max)
- [ ] Design memory callback opportunities (one year later scenarios)
- [ ] Map trait profiles to discovery outcomes
- [ ] Balance positive and negative consequence paths

### For QA/Testing
- [ ] Test all OCEAN trait combinations with dramatic irony moments
- [ ] Verify emotional state correctly locks/unlocks options
- [ ] Confirm memory callbacks trigger at correct times
- [ ] Test toxic path consequences (relationship damage, decay)
- [ ] Ensure player overlays display correctly

---

**This specification enables narrative designers to implement the complete dramatic irony system with:**
- **NPC perspective reveals** that show characters as full, complex people
- **Secret discoveries** that create tension and player anticipation
- **Character contradiction moments** that deepen and surprise
- **Oblivious dialogue options** that create "yelling at screen" tension
- **Memory-based callbacks** that reward player attention
- **Trait-driven consequences** where personality determines outcomes (healthy vs. toxic)
- **Real emotional complexity** grounded in OCEAN traits, history, and current state

**All serving the core goal: Relationships that feel real, with real stakes, real emotions, and real consequences.**

---

## Quick Reference: Key Design Principles

### 1. **Tension Through Obliviousness**
```
Player knows → Character doesn't → Dialogue reveals ignorance → Player feels tension
```
**Example:** Player knows Sarah is grieving David. Character offers to "cheer her up." Player watches it backfire.

### 2. **Memory Rewards Attention**
```
Dramatic irony moment → Player remembers → Future callback opportunity → Meaningful action
```
**Example:** Learn David's birthday (Week 14) → Remember one year later (Week 66) → Send thoughtful message → Deep emotional impact

### 3. **Personality Determines Outcome**
```
Same secret + Different OCEAN traits = Completely different consequences
```
**High Agreeableness:** "They're planning something nice for me" → Trust rewarded
**High Neuroticism:** "They're cheating on me" → Ruins surprise, damages relationship

### 4. **Discovery Can Harm**
```
Knowledge ≠ Always good
Some personalities + Some secrets = Toxic outcomes
```
**Example:** High neuroticism character learns partner loved someone deeply before → Jealousy spiral → Relationship damage

### 5. **Emotional State Gates Empathy**
```
Poor emotional state → Locked empathetic options → Only selfish choices available
```
**Exhausted player** can't choose "I'm here for you" → Only "I'm barely holding it together" available

### 6. **Real Consequences Persist**
```
Bad choice → Not forgotten → Relationships remember → Future interactions affected
```
**Jealous outburst** → Trust broken → NPC guarded for weeks/months → May end relationship

### 7. **Growth Through Struggle**
```
Negative trait impulse → Self-awareness → Choose better path → Character growth
```
**Feel jealousy** → Recognize it's unfair → Choose compassion anyway → Personal growth moment

---

## Testing Scenarios

### Scenario 1: High Conscientiousness Player
- **Week 14:** Learns David's birthday through POV card
- **Week 66:** Gets reminder, remembers immediately
- **Action:** Plans thoughtful gesture
- **Result:** +0.5 relationship, major emotional moment

### Scenario 2: Low Conscientiousness Player
- **Week 14:** Learns David's birthday through POV card
- **Week 66:** Gets reminder, vaguely remembers but doesn't act
- **Result:** Natural regret, no punishment, missed opportunity

### Scenario 3: High Neuroticism, Low Agreeableness
- **Discovery:** Partner has secret meeting
- **Response:** Assumes cheating, confronts or stalks
- **Result:** Surprise ruined, relationship damaged, carries guilt

### Scenario 4: High Neuroticism, High Conscientiousness
- **Discovery:** Partner has secret meeting
- **Response:** Feels anxiety, recognizes it's unfair, chooses trust
- **Result:** Surprise succeeds, internal growth, can choose to admit struggle

### Scenario 5: Emotionally Exhausted Player
- **Situation:** Friend reveals pain
- **Available Options:** Only self-centered responses (empathetic options locked)
- **Result:** Natural consequence of being too drained to support others

---

**End of Specification**
