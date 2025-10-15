# Stakes Escalation & Consequence Chain System - Implementation

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete system for escalating stakes with personal meaning, relationship depth, and capacity-aware perception

**References:**
- **Arc Structure:** `31-narrative-arc-scaffolding.md` (complication types, consequence chains)
- **Tension System:** `35-tension-maintenance-system.md` (hook escalation)
- **Meter Effects:** `13-meter-effects-tables.md` (meter-driven consequences)

---

## Overview

**Stakes** are what the player has to lose. **Escalation** is making those stakes progressively higher. The system creates dramatic, interconnected consequences where neglecting one area causes crises in others.

**Core Principle:** Consequences should feel dramatic and story-worthy, not just stat penalties. "You collapse during the wedding shoot" is more impactful than "Physical -2".

**Compliance:** master_truths v1.1 requires consequences to feel meaningful while avoiding anxiety mechanics - stakes create drama, not stress.

---

## Consequence Chain Types

### Health Neglect → Multi-Area Collapse

```javascript
const HEALTH_NEGLECT_CHAIN = {
  trigger: {
    condition: "Physical meter < 3 for 3+ consecutive weeks",
    player_warning: "You've been ignoring your body for weeks..."
  },
  
  progression: [
    {
      week: 0,
      stage: "warning_signs",
      symptoms: [
        "Constant fatigue despite sleep",
        "Coffee isn't helping anymore",
        "Small tasks feel overwhelming"
      ],
      gameplay_effects: {
        energy_regen: -1,              // Less energy per day
        success_chance_penalty: -0.10,  // 10% penalty to all actions
        aspiration_progress_rate: 0.85  // 15% slower
      },
      narrative_moments: [
        "Mirror reflection: You look... tired. Really tired.",
        "Third coffee by noon. Still foggy.",
        "Friends: 'Are you okay? You look exhausted.'"
      ]
    },
    
    {
      week: 2,
      stage: "visible_deterioration",
      symptoms: [
        "Visible exhaustion others comment on",
        "Hands shake during precision tasks",
        "Forgetting things mid-conversation"
      ],
      gameplay_effects: {
        energy_regen: -2,
        success_chance_penalty: -0.20,
        social_interactions_affected: true,
        relationship_concern_triggered: ["close_friends", "family"]
      },
      narrative_moments: [
        "Marcus: 'I'm worried about you. When's the last time you slept?'",
        "Hands shake slightly during photo shoot. Client notices.",
        "Sarah and Marcus text each other (player sees): 'We need to talk about [Player Name].'"
      ],
      escalation_warning: {
        card_text: "Your body is sending clear signals. Something has to give. Soon.",
        dramatic_weight: 0.7,
        skippable: false
      }
    },
    
    {
      week: 3,
      stage: "crisis_event",
      crisis_type: "public_collapse",
      
      dramatic_moment: {
        title: "THE COLLAPSE",
        setting: "During critical moment (wedding shoot / work presentation / important date)",
        
        narrative: `
          You're shooting the ceremony. Bride walking down the aisle. 
          This is the shot. This is what they're paying you for.
          
          The camera feels heavy. The room tilts slightly.
          
          You blink. Once. Twice. The floor is suddenly very interesting.
          
          You don't remember falling.
          
          You wake up to Marcus and Sarah's faces above you. Paramedics.
          The bride's mother looking horrified. Your camera on the ground.
          
          "You collapsed," Sarah says, voice shaking. "Right in the middle of—"
          
          You know. You remember the moment before. The moment everything went dark.
        `,
        
        immediate_consequences: {
          physical: "Hospitalized, forced rest for 1 week",
          aspiration: {
            photography_business: [
              "Wedding shoot incomplete - NO PAY ($500 lost)",
              "Must refund deposit ($200 lost)",
              "Negative review posted online",
              "Reputation damage: -3",
              "Future bookings: 2 clients cancel"
            ]
          },
          career: {
            if_corporate_job: [
              "Missed critical presentation",
              "Reputation damaged",
              "Boss questions reliability",
              "Promotion track: stalled"
            ]
          },
          relationships: {
            marcus: {
              reaction: "Terrified, then angry: 'I TOLD you to slow down!'",
              trust: +0.2,                    // Paradox: crisis deepens bond
              interaction_type: "confrontation_then_support",
              new_dynamic: "Marcus becomes health watchdog"
            },
            sarah: {
              reaction: "Quiet concern, brings food to hospital",
              trust: +0.1,
              reveals: "Sarah understands burnout (relates to David trauma)",
              new_dynamic: "Sarah shares her own story of collapse after David's death"
            },
            client: {
              trust: -0.8,
              relationship_status: "SEVERED",
              permanent_damage: true
            }
          },
          financial: {
            immediate_loss: -700,              // Lost pay + refund
            medical_bills: -400,
            total_impact: -1100,
            creates_new_crisis: "Money suddenly tight"
          },
          emotional: {
            state: "DEVASTATED → REFLECTIVE",
            arc_impact: "Forced reckoning with priorities"
          }
        },
        
        long_term_ripples: [
          {
            weeks: "4-6",
            effect: "Recovery period, can't take on intense projects",
            aspiration_delay: "2-4 weeks lost progress"
          },
          {
            weeks: "8-12",
            effect: "Reputation slowly rebuilding, or career pivot forced",
            arc_options: ["Double down with caution", "Abandon aspiration", "Shift to part-time"]
          },
          {
            weeks: "16+",
            memory: "The collapse becomes defining moment",
            reference_points: [
              "Friends: 'Remember when you collapsed? Don't do that again.'",
              "Self-reflection: 'I almost destroyed everything.'",
              "Turning point: 'That's when I learned balance matters.'"
            ]
          }
        ],
        
        novel_worthy: true,
        chapter_title_suggestion: "The Day Everything Fell Apart"
      }
    }
  ],
  
  prevention_opportunities: [
    { week: 0, card: "Take a rest day? (Skip aspiration work, restore Physical)" },
    { week: 1, card: "Marcus offers to cover for you. Accept help?" },
    { week: 2, card: "Doctor visit available. Go? ($100 cost)" }
  ],
  
  player_agency: "Can prevent through rest, or ignore warnings and face crisis"
};
```

---

### Relationship Neglect → Permanent Loss

```javascript
const RELATIONSHIP_NEGLECT_CHAIN = {
  trigger: {
    condition: "Major NPC (Level 3+) not interacted with for 4+ weeks",
    applies_to: "NPCs player has invested in (Level 3-5)"
  },
  
  progression: [
    {
      week: 0,
      stage: "cooling_off",
      npc_behavior: [
        "Stops reaching out first",
        "Texts are brief, polite but distant",
        "Stops sharing personal updates"
      ],
      gameplay_effects: {
        social_capital_with_npc: -1,
        trust: -0.05,
        interaction_opportunities: "reduced"
      },
      narrative_signals: [
        "[NPC]: 'Hey, I haven't heard from you in a while. Everything okay?'",
        "You see [NPC] posted photos from weekend hangout. You weren't invited.",
        "[NPC]'s texts take longer to respond. Hours instead of minutes."
      ],
      reversible: true,
      recovery_action: "Reach out, acknowledge absence, rebuild"
    },
    
    {
      week: 2,
      stage: "active_drifting",
      npc_behavior: [
        "Makes plans without you",
        "Life continues without your involvement",
        "Friendship circle shifts"
      ],
      gameplay_effects: {
        social_capital_with_npc: -2,
        trust: -0.10,
        relationship_level: "at risk of downgrade"
      },
      narrative_moments: [
        {
          card_title: "The Photos",
          content: `
            Instagram notification: Sarah tagged in photos.
            
            It's her birthday party. Last night. A dozen people you vaguely know. 
            Marcus is there. Other friends. Everyone smiling.
            
            You didn't know she was having a party.
            
            You check your messages. Nothing from Sarah about it.
            You realize: she stopped inviting you weeks ago.
          `,
          emotional_impact: "Hurt, regret, realization",
          dramatic_weight: 0.7
        }
      ],
      reversible: true,
      recovery_action: "Confrontation + honest conversation + consistent follow-through",
      difficulty: "harder than week 0"
    },
    
    {
      week: 4,
      stage: "major_life_event_without_you",
      npc_makes_decision: true,
      
      dramatic_moment: {
        title: "WHAT YOU LOST",
        
        scenario_options: [
          {
            event: "sarah_moves_away",
            narrative: `
              You finally text Sarah after another week of silence.
              
              Sarah: "Hey! Sorry for the slow response. I've been swamped 
              with packing."
              
              Packing?
              
              Sarah: "Oh. I thought Marcus told you. I'm moving to Portland. 
              Got a job offer I couldn't refuse. I leave next week."
              
              Next week. Your best friend of two years is moving across the 
              country next week, and you're finding out via text.
            `,
            
            permanent_consequences: {
              relationship_status: "long_distance",
              interaction_frequency: "quarterly instead of weekly",
              trust: -0.30,
              relationship_level: "3 → 2 (downgrade)",
              aspirations_affected: [
                "If Sarah was connected to aspiration (bookshop collab, etc), that path closes"
              ],
              emotional_cost: "Regret, loss, 'what if I had stayed in touch?'",
              novel_chapter: "The Friend I Let Slip Away"
            }
          },
          
          {
            event: "marcus_gets_engaged_you_find_out_last",
            narrative: `
              You're scrolling social media. Photo from Marcus. 
              Him and Jess. She's holding up her hand. Ring.
              
              "She said yes! Engaged to my best friend!"
              
              34 likes. 12 comments. All your mutual friends congratulating him.
              
              You check your messages. Nothing from Marcus directly.
              You weren't there when he proposed. You didn't even know 
              he was planning to.
              
              You used to be the first person he told everything.
            `,
            
            permanent_consequences: {
              relationship_status: "still friends, but not BEST friend anymore",
              trust: -0.20,
              role_in_life: "outer circle instead of inner circle",
              wedding: "invited but not in wedding party",
              emotional_cost: "Realization you missed the moment your friendship changed",
              can_rebuild: true,
              difficulty: "very hard, requires season-long effort"
            }
          }
        ]
      },
      
      reversible: "partially",
      recovery_path: "Acknowledge the loss, apologize, slowly rebuild",
      will_never_be_same: true
    }
  ],
  
  prevention_system: {
    week_1_warning: "You haven't talked to [NPC] in a while. Reach out?",
    week_2_warning: "[NPC] seems distant. Have a conversation?",
    week_3_urgent: "[NPC] is drifting away. Fix this now or lose them.",
    
    easy_prevention: "One meaningful interaction per 2-3 weeks maintains relationship"
  }
};
```

---

## Dramatic Consequence Design Principles

### Story Moments > Stat Penalties

```javascript
const CONSEQUENCE_DESIGN = {
  bad_example: {
    consequence: "Physical meter -2",
    why_weak: [
      "Just a number",
      "No narrative context",
      "Not memorable",
      "Doesn't affect story"
    ]
  },
  
  good_example: {
    consequence: "You collapse during the wedding ceremony you're photographing",
    why_strong: [
      "Specific, visualizable moment",
      "Affects multiple life areas (career, money, relationships)",
      "Creates memorable story beat",
      "Has long-term ripple effects",
      "Could be a novel chapter"
    ],
    implementation: {
      stat_changes: "Physical = 0, Money -$700, Reputation -3",
      but_more_importantly: "Creates dramatic narrative moment with emotional weight"
    }
  },
  
  design_checklist: {
    is_it_visualizable: "Can player imagine the scene?",
    does_it_ripple: "Does it affect multiple life areas?",
    is_it_memorable: "Will player remember this in 10 weeks?",
    is_it_novel_worthy: "Could this be a chapter in generated novel?",
    does_it_feel_earned: "Was player warned this could happen?",
    
    if_all_yes: "Good dramatic consequence"
  }
};
```

---

## Interconnected Stakes System

### Cascading Failures

```javascript
const CASCADE_SYSTEM = {
  principle: "One failure creates problems in other areas",
  
  example_cascade: {
    initial_problem: "Choose aspiration work over rest (Physical neglect)",
    
    week_1: {
      effect: "Exhaustion reduces work performance",
      cascade_to: "career"
    },
    
    week_2: {
      effect: "Boss notices poor performance, assigns less important work",
      cascade_to: "financial (smaller bonus) + emotional (feel undervalued)"
    },
    
    week_3: {
      effect: "Frustration at work + exhaustion → snap at friend",
      cascade_to: "relationships (Sarah hurt)"
    },
    
    week_4: {
      effect: "Sarah distant + work stress + exhaustion → miss aspiration deadline",
      cascade_to: "aspiration failure"
    },
    
    final_state: {
      physical: "Still exhausted",
      career: "Reputation damaged",
      relationships: "Sarah cooling off",
      aspiration: "Behind schedule",
      emotional: "DISCOURAGED",
      
      narrative_realization: `
        You collapse on the couch Thursday night.
        
        Work is a mess. You haven't talked to Sarah in a week. 
        The photography project you were so excited about? Abandoned.
        
        You were trying to do everything. 
        Now you're failing at all of it.
      `
    }
  }
};
```

---

## Escalation Timing & Pacing

### When to Escalate Stakes

```javascript
const ESCALATION_TIMING = {
  act_1_setup: {
    weeks: "1-3",
    escalation_level: "low",
    principle: "Establish stakes, don't overwhelm",
    examples: [
      "Hint at potential problems",
      "Set up future consequences",
      "Give player time to understand systems"
    ]
  },
  
  act_2_early: {
    weeks: "4-6",
    escalation_level: "moderate",
    principle: "First real consequences",
    examples: [
      "First complication hits",
      "Player faces first real choice with costs",
      "Stakes become clear"
    ]
  },
  
  act_2_midpoint: {
    weeks: "7-9",
    escalation_level: "high",
    principle: "Major decisive decision, stakes peak",
    examples: [
      "Decisive decision with permanent consequences",
      "Multiple areas at risk simultaneously",
      "Player must choose what to sacrifice"
    ]
  },
  
  act_2_late: {
    weeks: "10-15 (24w season)",
    escalation_level: "very high",
    principle: "Cascading consequences, everything interconnected",
    examples: [
      "Previous decisions creating new problems",
      "Multiple concurrent crises possible",
      "Player feels pressure (in-world, not real-time)"
    ]
  },
  
  act_3_climax: {
    weeks: "Final push to resolution",
    escalation_level: "maximum",
    principle: "Everything comes to a head",
    examples: [
      "Final decisive decision determines outcome",
      "All stakes at maximum",
      "Success or failure of entire season arc"
    ]
  },
  
  act_3_resolution: {
    weeks: "Final 1-2 weeks",
    escalation_level: "release",
    principle: "Consequences resolve, breathing room",
    examples: [
      "See outcomes of choices",
      "Relationships heal or end",
      "Reflection on journey"
    ]
  }
};
```

---

## Player Agency in Stakes

### Meaningful Choices

```javascript
const AGENCY_SYSTEM = {
  principle: "Player should feel consequences are result of their choices, not arbitrary punishment",
  
  good_agency_example: {
    setup: "You've been choosing aspiration work over sleep for 3 weeks",
    warning: "Mirror card: 'You look exhausted.' (week 2)",
    warning_2: "Friends express concern (week 3)",
    choice_point: "Rest today or push for deadline?",
    consequence_if_push: "Collapse during critical moment",
    
    why_good: [
      "Player made explicit choices",
      "Was warned consequences were coming",
      "Had opportunity to prevent",
      "Consequence feels earned, not arbitrary"
    ]
  },
  
  bad_agency_example: {
    setup: "Player working normally",
    no_warning: true,
    sudden_event: "You collapse randomly!",
    consequence: "Aspiration fails",
    
    why_bad: [
      "No player choice involved",
      "No warning",
      "Feels arbitrary and unfair",
      "Player can't learn or improve"
    ]
  },
  
  prevention_opportunities: {
    always_provide: [
      "Warning cards 1-3 weeks before crisis",
      "Explicit choice to prevent (even if costly)",
      "Visual/narrative signals that danger is building",
      "NPC concern/advice"
    ],
    
    example_prevention_cards: [
      "Marcus: 'Take a day off. Seriously.' [Skip aspiration work, restore Physical]",
      "You feel yourself burning out. Rest now? (Costs progress but prevents crisis)",
      "Doctor appointment available. $100. Go? (Identify health issue early)"
    ]
  }
};
```

---

## Master Truths v1.2: Personal Meaning Integration *(NEW)*

### Stakes Are Personal, Not Universal

**Core Principle:** What matters to one player may not matter to another. Stakes should reflect player's values, relationships, and aspirations - not just generic "lose money" or "fail quest."

```javascript
const PERSONAL_MEANING_SYSTEM = {
  principle: "Stakes carry weight because they threaten what player specifically cares about",
  
  generic_vs_personal: {
    generic_stake: {
      consequence: "Lose $500",
      why_weak: "Money is abstract, player may not care",
      emotional_impact: "Low - just a number"
    },
    
    personal_stake: {
      consequence: "Can't afford to keep apartment where Sarah and you have coffee every Tuesday",
      why_strong: "Threatens ritual that matters to relationship player has invested in",
      emotional_impact: "High - threatens meaningful routine and connection"
    }
  },
  
  examples: [
    {
      aspiration: "Photography business",
      player_cares_about: "Creative expression, financial independence, proving critics wrong",
      
      personal_stakes: {
        creative: {
          threat: "Gallery owner: 'Your work is technically good but lacks soul'",
          why_hurts: "Challenges core identity as artist",
          player_feels: "Devastated - this is about WHO they are, not just success"
        },
        
        financial: {
          threat: "Can't afford equipment repair, might miss once-in-lifetime shoot",
          why_hurts: "Opportunity to prove themselves slipping away",
          player_feels: "Desperate - this was THE chance"
        },
        
        validation: {
          threat: "Father: 'I knew you'd fail. You should have listened to me.'",
          why_hurts: "If player has contentious relationship with father who doubted them",
          player_feels: "Crushing - he was right, I was wrong"
        }
      }
    }
  ]
};
```

**Implementation:**

```javascript
function personalizeStakes(genericConsequence, playerProfile) {
  return {
    generic: genericConsequence,
    
    personalized: {
      threatens: identifyWhatPlayerCaresAbout(playerProfile),
      emotional_core: extractEmotionalMeaning(playerProfile),
      narrative: generatePersonalizedNarrative(genericConsequence, playerProfile),
      
      examples: {
        player_values_independence: {
          generic: "Lose job",
          personal: "Have to move back in with parents who said you'd never make it"
        },
        
        player_values_creativity: {
          generic: "Business fails",
          personal: "Admit that safe corporate job was right path after all"
        },
        
        player_values_relationships: {
          generic: "Time constraints",
          personal: "Miss Sarah's wedding because you're working - she'll never forgive you"
        }
      }
    }
  };
}
```

---

## Master Truths v1.2: Relationship Stakes (Level 4-5) *(NEW)*

### Deep Bonds Create Maximum Stakes

**Core Principle:** Level 4-5 relationships (Best Friend, Soulmate) have unique, irreplaceable stakes. Losing them isn't just sad - it's devastating.

```javascript
const DEEP_RELATIONSHIP_STAKES = {
  level_4_best_friend: {
    relationship_quality: "Person who truly knows you, irreplaceable connection",
    
    stakes_unique_to_level_4: {
      losing_them: {
        consequence: "Not just losing a friend - losing the person who SAW you",
        emotional_weight: 9,
        
        narrative_example: `
          Sarah isn't just your friend. She's the person who believed in you 
          when you didn't believe in yourself.
          
          She's the one who knows about the panic attacks you hide from everyone else.
          She's the one you call at 2 AM when everything is falling apart.
          She's the one who remembers your dad's birthday when you forget.
          
          Losing her isn't losing "a friend." It's losing the person who knows 
          all of you - the good, the bad, the scared - and stayed anyway.
          
          That kind of friendship? You don't get many of those in a lifetime.
        `
      },
      
      betraying_trust: {
        consequence: "Breaking bond with person who trusted you completely",
        emotional_weight: 10,
        
        narrative_example: `
          Sarah told you about David. She doesn't tell people about David.
          
          And you told Marcus. At a party. After too many drinks. 
          Like it was just gossip.
          
          Sarah's face when she found out. That look. You'll carry that forever.
          
          She trusted you with her grief. Her trauma. Her heart.
          
          And you broke it.
          
          Some things can't be taken back.
        `,
        
        permanent_damage: true,
        relationship_may_end: "High probability",
        trust_shattered: "May never fully recover"
      },
      
      choosing_against_them: {
        consequence: "Proving their fears right, becoming like everyone who hurt them before",
        emotional_weight: 9,
        
        scenario: `
          DECISION: Sarah's bookshop is failing. She needs $5,000 to avoid closure.
          You have $5,000 saved. For your photography business launch.
          
          Option 1: Give Sarah the money
          - Your business launch delayed 6 months
          - Sarah's bookshop survives
          - She knows you chose her
          
          Option 2: Keep the money, launch business
          - Your dream moves forward
          - Sarah loses bookshop
          - She asked for help and you said no
          
          Stakes: This isn't just about money.
          
          This is: "When I needed you most, were you there?"
          
          Sarah has been abandoned before. By death (David). By friends who 
          couldn't handle her grief. By a father who said she'd never succeed.
          
          If you choose your business over her... you're another person who 
          left when it mattered.
        `,
        
        consequences_if_choose_business: {
          relationship_damage: -0.8,
          sarah_becomes_distant: "Permanently",
          trust_broken: "Feels like another abandonment",
          sarah_closes_off: "Won't be vulnerable again",
          
          long_term: "Relationship may never recover to Level 4. Some wounds don't heal."
        }
      }
    }
  },
  
  level_5_soulmate: {
    relationship_quality: "Life partner potential, deepest possible bond",
    
    stakes_unique_to_level_5: {
      losing_them: {
        consequence: "Losing person you planned future with - life trajectory changes",
        emotional_weight: 10,
        
        narrative_example: `
          You weren't just losing Alex. You were losing:
          
          - The apartment you were saving for together
          - The future where you'd travel Europe next summer
          - The person you'd imagined growing old with
          - The version of yourself that existed with them
          
          When a Level 5 relationship ends, you don't just lose them.
          You lose the future you'd built in your mind.
          You lose the person you were becoming with them.
          
          That's why it's called a soulmate.
        `
      },
      
      betrayal_at_this_level: {
        consequence: "Trauma that affects future relationships, trust capacity diminished",
        emotional_weight: 10,
        permanent_scar: true,
        
        affects_future_seasons: "Trust issues carry into new relationships"
      },
      
      choosing_career_over_relationship: {
        scenario: `
          DECISIVE DECISION: 
          
          Dream job offer. Different city. Career-defining opportunity.
          
          Alex: "I can't move. My family is here. My job is here. My life is here."
          
          You: "This is everything I've worked for."
          
          Alex: "And I'm not?"
          
          You: "That's not fair."
          
          Alex: "Isn't it? Five years together. We've talked about forever. 
          And the second your career calls, you're ready to leave?"
          
          You: "It's not that simple."
          
          Alex: "It is, though. It's me or the job. And we both know which 
          you're going to choose."
          
          They're right. You do know.
          
          But knowing doesn't make it easier.
        `,
        
        consequences_if_choose_career: {
          relationship_ends: true,
          alex_devastated: "Feels abandoned, trust destroyed",
          player_grief: "Months of processing, questioning decision",
          
          long_term_effects: [
            "Season-long emotional recovery period",
            "Difficulty trusting new partners (fear of abandonment/being abandoned)",
            "Success feels hollow without them",
            "Years later, still wonder 'what if?'"
          ],
          
          future_season_callbacks: "May run into Alex years later, see what could have been"
        }
      }
    }
  },
  
  design_principle: "Level 4-5 stakes are about identity, future, and irreplaceable connections"
};
```

---

## Master Truths v1.2: Capacity-Limited Stakes Perception *(NEW)*

### Low Capacity Changes How Stakes Feel

**Core Principle:** When emotional capacity is low, stakes perception changes. Things that normally wouldn't break you become overwhelming. Small problems feel catastrophic.

```javascript
const CAPACITY_LIMITED_STAKES = {
  principle: "Same stake feels different at capacity 8 vs capacity 2",
  
  example_stake: "Client cancels photography gig ($500 loss)",
  
  perception_at_high_capacity: {
    capacity: 8,
    physical: 8,
    emotional: 8,
    stress_load: 2,
    
    player_perception: `
      [Email: "Sorry, we need to cancel the shoot."]
      
      You read it. Sigh. Annoying, but okay.
      
      $500 loss hurts, but you'll find another client.
      You have savings. You'll be fine.
      
      Internal response: Disappointment, minor frustration.
      Action: Email back professionally, move on, book another gig.
      
      Stakes feel: 4/10 - Setback, not crisis
    `,
    
    narrative_tone: "Calm, proportional, solution-focused",
    available_responses: "All options available, including healthy coping"
  },
  
  perception_at_moderate_capacity: {
    capacity: 5,
    physical: 5,
    emotional: 5,
    stress_load: 5,
    
    player_perception: `
      [Email: "Sorry, we need to cancel the shoot."]
      
      You read it. Your stomach drops.
      
      $500. That's... that's a lot right now. You were counting on that.
      Rent is due in two weeks. You're already cutting it close.
      
      Internal response: Anxiety spike, worry, "What now?"
      Action: Panic briefly, then scramble to find replacement gig.
      
      Stakes feel: 6/10 - Concerning, need to fix this
    `,
    
    narrative_tone: "Anxious, stressed, but still functional",
    available_responses: "Most options available, some emotional reactions"
  },
  
  perception_at_critical_capacity: {
    capacity: 2,
    physical: 3,
    emotional: 2,
    stress_load: 9,
    active_stressors: [
      "Overworked for weeks",
      "Haven't slept well",
      "Relationship tension with Sarah",
      "Family emergency last week",
      "Already behind on rent"
    ],
    
    player_perception: `
      [Email: "Sorry, we need to cancel the shoot."]
      
      You read it. Everything stops.
      
      $500. Gone.
      
      You were $300 short on rent already. Now you're $800 short.
      Two weeks. How do you make up $800 in two weeks?
      
      Your hands are shaking. You can't breathe right.
      
      This isn't just about the money. This is:
      - Evidence you're failing
      - Proof you can't make this work
      - The moment everything falls apart
      
      You stare at the screen. The room feels smaller.
      
      Everything feels impossible.
      
      You don't email back. You just sit there.
      
      Internal response: Catastrophizing, paralysis, despair
      Stakes feel: 10/10 - This is the end
    `,
    
    narrative_tone: "Desperate, catastrophizing, paralyzed",
    
    available_responses: {
      locked_healthy_options: [
        "❌ LOCKED: Calmly find another client (Requires Capacity >= 5)",
        "❌ LOCKED: Ask Marcus for help professionally (Requires Emotional >= 5)",
        "❌ LOCKED: Make backup plan (Requires Mental >= 4)"
      ],
      
      available_crisis_options: [
        "✅ Panic. Just... panic.",
        "✅ Avoid thinking about it (scroll social media for hours)",
        "✅ Desperate message to client begging them to reconsider",
        "✅ Break down crying",
        "✅ Call Sarah in crisis (if relationship good enough)"
      ]
    },
    
    why_stakes_feel_catastrophic: [
      "Capacity too low to process rationally",
      "Multiple stressors compounding",
      "No emotional buffer to absorb setback",
      "Everything feels like 'last straw'",
      "Can't access problem-solving skills when capacity exhausted"
    ]
  },
  
  design_principle: "Low capacity makes all stakes feel worse. Same problem, different capacity, completely different experience."
};
```

**Gameplay Implementation:**

```javascript
function calculatePerceivedStakes(objectiveStakes, playerCapacity) {
  const baseStakes = objectiveStakes;  // 0-10 scale
  
  let perceivedStakes = baseStakes;
  
  // Capacity modifier
  if (playerCapacity <= 3) {
    perceivedStakes *= 1.5;  // Everything feels 50% worse
  } else if (playerCapacity <= 5) {
    perceivedStakes *= 1.2;  // Everything feels 20% worse
  } else if (playerCapacity >= 8) {
    perceivedStakes *= 0.8;  // Better equipped to handle
  }
  
  // Multiple stressor amplification
  const activeStressors = countActiveStressors(player);
  if (activeStressors >= 3 && playerCapacity <= 5) {
    perceivedStakes *= 1.3;  // "When it rains it pours" effect
  }
  
  return Math.min(10, perceivedStakes);
}
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Stakes System (v1.1 Foundation)
- [x] Consequences create drama, not anxiety (all in-world, no FOMO)
- [x] Player agency maintained (warned, given prevention opportunities)
- [x] Stakes feel meaningful and story-worthy
- [x] Interconnected systems create realistic cascades
- [x] All consequences use canonical resources/relationships
- [x] Dramatic moments are novel-worthy (support book generation)
- [x] Story moments > stat penalties principle
- [x] Cascading failures across multiple life areas
- [x] Prevention opportunities provided (1-3 weeks warning)

### ✅ Master Truths v1.2: Stakes Enhancements *(NEW)*
- [x] **Personal Meaning Integration**
  - Stakes reflect player's specific values/relationships/aspirations
  - Generic consequences personalized to what player cares about
  - Threatens identity, not just resources
- [x] **Level 4-5 Relationship Stakes**
  - Best Friend (Level 4): Irreplaceable connections, person who "sees" you
  - Soulmate (Level 5): Life trajectory stakes, future together threatened
  - Betrayal/loss at these levels = maximum emotional weight (9-10)
  - Permanent consequences possible (trust shattered, relationship may never recover)
- [x] **Capacity-Limited Stakes Perception**
  - Same stake feels different at capacity 8 vs capacity 2
  - Low capacity (≤3): Stakes feel 50% worse, catastrophizing
  - Moderate capacity (4-6): Stakes feel 20% worse, anxious but functional
  - High capacity (≥8): Stakes feel 20% better, solution-focused
  - Multiple stressors compound perception (1.3x when ≥3 stressors + low capacity)

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~430 lines** of new v1.2 stakes mechanics
2. **Personal meaning system** - stakes threaten what player specifically cares about
3. **Deep relationship stakes (L4-5)** - losing irreplaceable bonds, maximum emotional weight
4. **Capacity-limited perception** - low capacity makes everything feel catastrophic
5. **Perceived vs objective stakes** - same problem, different experience based on capacity
6. **Locked options when capacity critical** - healthy coping unavailable when exhausted

**Personal Meaning Examples:**
- Player values independence → stake: "Move back with parents who doubted you"
- Player values creativity → stake: "Admit corporate job was right path after all"
- Player values relationships → stake: "Miss Sarah's wedding - she'll never forgive you"

**Level 4-5 Stakes:**
- Level 4 betrayal: "She trusted you with her grief. You broke it. Some things can't be taken back."
- Level 5 loss: "You lose the future you'd built in your mind. The person you were becoming with them."

**Capacity Effects:**
- Capacity 8 + $500 loss: "4/10 - Annoying but fine, will find another client"
- Capacity 2 + $500 loss: "10/10 - Evidence I'm failing, everything's falling apart, I can't breathe"

**Design Principles:**
- Stakes are personal, not universal
- Deep bonds create irreplaceable stakes
- Low capacity makes all problems feel catastrophic
- Perception matters more than objective reality
- Level 4-5 relationship loss = life-changing event

**References:**
- See `01-emotional-authenticity.md` for cross-system integration
- See `14-emotional-state-mechanics.md` for capacity calculation and circumstance stacking
- See `31-narrative-arc-scaffolding.md` for consequence chains in 3-act structure
- See `35-tension-maintenance-system.md` for how stakes create tension and personality-based perception
- See `13-meter-effects-tables.md` for meter-driven consequence triggers
- See `30-decisive-decision-templates.md` for high-stakes decision moments with capacity gating

---

**This specification enables developers to implement the complete stakes escalation system with Master Truths v1.2 enhancements: personalized stakes that threaten what player specifically cares about, maximum-weight Level 4-5 relationship stakes with irreplaceable consequences, and capacity-limited perception where low emotional capacity makes all problems feel catastrophic - creating stakes that feel authentic, personal, and emotionally devastating when appropriate.**
