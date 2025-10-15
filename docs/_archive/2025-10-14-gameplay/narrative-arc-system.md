# Narrative Arc & Decisive Decision System

## Philosophy

**For a novel to be compelling, the LIFE must be compelling.** The game needs dramatic structure with meaningful choices, consequences, and hard decisions that create genuine tension. This system transforms gameplay from "pleasant life simulation" into "dramatic story worth reading about."

---

## Core Principles

### 1. **Every Run Follows a Three-Act Structure**

```
ACT I: DISCOVERY & POSSIBILITY (Weeks 1-20)
- Meet characters, explore options
- Establish dreams and desires
- Plant seeds of future arcs
- Low stakes, high variety

ACT II: PURSUIT & FRICTION (Weeks 21-60)
- Commit to paths
- Face meaningful obstacles
- Make hard choices with real consequences
- Moderate-to-high stakes

ACT III: CRISIS & RESOLUTION (Weeks 61-End)
- Major decisions with lasting impact
- Convergence of multiple arc threads
- Sacrifices and triumphs
- Highest stakes
```

### 2. **Story Arcs Create Long-Form Tension**

Story arcs are multi-phase narrative threads that span 8-30+ weeks, creating sustained dramatic tension through:
- **Progressive escalation** of stakes
- **Decisive decision points** that change the trajectory
- **Consequences** that ripple through the rest of the story
- **Competing priorities** that force hard choices

### 3. **Neglect and Imbalance Have Consequences**

The game tracks what you're ignoring, and it *punishes* neglect:
- Ignore health → Crisis card: "Your body is breaking down"
- Ignore relationships → NPCs drift away or confront you
- Ignore career → Financial crisis or termination
- Ignore mental health → Burnout, depression, panic attacks

---

## Story Arc Architecture

### Arc Structure Template

```javascript
const STORY_ARC = {
  id: "photography-dream",
  title: "The Photography Dream",
  category: "Career/Passion",
  
  // PHASES (Each arc has 3-5 phases)
  phases: [
    {
      phase: 1,
      title: "The Spark",
      weeks: 2-4,
      trigger: "Discover camera or meet photographer NPC",
      goals: ["Take 10 photos", "Share work with someone"],
      cards_unlocked: ["Photography Basics", "Camera Shop Visit"],
      tension: "Curiosity vs. practicality"
    },
    {
      phase: 2,
      title: "Serious Interest",
      weeks: 4-8,
      trigger: "Complete Phase 1 + meet mentor or get positive feedback",
      goals: ["Take online course", "Buy better equipment", "Join photo group"],
      cards_unlocked: ["Weekend Photography", "Portfolio Building"],
      tension: "Time commitment + financial investment"
    },
    {
      phase: 3,
      title: "The Opportunity",
      weeks: 8-12,
      trigger: "Skill level 3 + relationship with photographer friend",
      decisive_decision: {
        card: "WEDDING SHOOT INVITATION",
        description: "Your friend invites you to assist on a paid wedding shoot",
        same_day_conflict: "WORK OVERTIME REQUEST",
        stakes: {
          choose_shoot: {
            positive: ["Progress arc", "+2 Photography skill", "Build portfolio", "$200", "Deepen friendship"],
            negative: ["Miss $1500 bonus", "Disappoint boss", "-1 Career reputation"]
          },
          choose_work: {
            positive: ["$1500 bonus", "+1 Career reputation", "Boss trust"],
            negative: ["Kill photography arc", "Lose photographer friend", "Regret lingers"]
          }
        }
      },
      tension: "Dream vs. security"
    },
    {
      phase: 4,
      title: "Building Momentum",
      weeks: 12-20,
      trigger: "Chose shoot in Phase 3",
      goals: ["Get 3 paid gigs", "Build client base", "Create website"],
      cards_unlocked: ["Client Bookings", "Equipment Upgrade", "Side Hustle"],
      crisis_risk: "Financial strain (equipment costs + reduced work hours)",
      tension: "Sustainable vs. pipe dream"
    },
    {
      phase: 5,
      title: "The Crossroads",
      weeks: 20-24,
      decisive_decision: {
        card: "FULL-TIME PHOTOGRAPHY OFFER",
        description: "A studio offers you a full-time position, but salary is 40% less than corporate job",
        context: {
          rent_due: true,
          savings: "player_dependent",
          relationship_status: "varies",
          parent_health: "potential_factor"
        },
        stakes: {
          go_full_time: {
            positive: ["Arc success", "Living your dream", "Creative fulfillment", "Freedom"],
            negative: ["Financial stress", "Lost stability", "Risk of failure", "Can't help family financially"]
          },
          stay_corporate: {
            positive: ["Financial security", "Keep benefits", "Can help family", "Photography stays hobby"],
            negative: ["Arc failure", "Dream deferred", "Regret", "What if?"]
          }
        }
      },
      tension: "Ultimate commitment"
    }
  ],
  
  // FAILURE PATHS
  failure_conditions: [
    {
      condition: "Choose work over shoot in Phase 3",
      result: "Arc ends, but memory persists as 'The Road Not Taken'"
    },
    {
      condition: "Neglect arc for 8+ weeks during phases 2-4",
      result: "Arc atrophies, skill degrades, opportunities close"
    },
    {
      condition: "Physical meter hits zero during critical phase",
      result: "Forced pause, potentially miss key opportunity"
    }
  ],
  
  // SUCCESS OUTCOMES
  success_variations: [
    {
      path: "Full-time photographer",
      fusion_card: "Professional Photographer You",
      ending_impact: "Career fulfilled, financial moderate, creative high"
    },
    {
      path: "Hybrid (corporate + side gig)",
      fusion_card: "Balanced Creative You",
      ending_impact: "Career stable, creativity outlet, less regret"
    }
  ]
};
```

---

## Decisive Decision Points

### Structure of a Decisive Decision

Every major decision follows this template:

```javascript
const DECISIVE_DECISION = {
  trigger: {
    arc_phase: "photography-dream-phase-3",
    week_range: [8, 12],
    preconditions: [
      "photography_skill >= 3",
      "relationship.photographer_friend >= 0.6",
      "energy >= 2"
    ]
  },
  
  setup: {
    // Build tension BEFORE presenting choice
    foreshadowing_cards: [
      {
        week: -2,
        card: "Your friend mentions a big wedding coming up",
        hint: "They might need help"
      },
      {
        week: -1,
        card: "Boss mentions important client arriving soon",
        hint: "Overtime likely"
      }
    ]
  },
  
  decision_card: {
    title: "THE WEDDING SHOOT",
    type: "DECISIVE_DECISION",
    rarity: "legendary",
    art_style: "dramatic_lighting",
    
    // The situation
    narrative: `
      It's Thursday evening. Your phone buzzes twice in thirty seconds.
      
      First message - your photographer friend:
      "Hey! The second shooter for that wedding canceled. It's Saturday. 
      Pays $200 and would be huge for your portfolio. You in?"
      
      Second message - your boss:
      "Need you in the office Saturday. Big client presentation. 
      There's a $1,500 bonus if we land this. Mandatory attendance."
      
      You stare at both messages. 
      
      The wedding is your first real paid photography gig.
      The work presentation could set you up for a promotion.
      
      You can't do both.
    `,
    
    // Present the choice
    options: [
      {
        id: "choose_photography",
        label: "\"I'll do the shoot\"",
        immediate_effects: {
          meters: {social: +2, emotional: +3},
          money: +200,
          skill_photography: +2,
          relationship_photographer_friend: +0.3,
          relationship_boss: -0.4
        },
        short_term_consequences: [
          {
            week: 0,
            card: "Boss is noticeably cold at Monday meeting",
            effect: "Career reputation -1"
          },
          {
            week: 1,
            card: "Wedding photos turned out amazing",
            effect: "Portfolio +5 quality, Client referrals start"
          },
          {
            week: 2,
            card: "Missed the promotion cycle",
            effect: "No raise this quarter"
          }
        ],
        long_term_consequences: [
          {
            weeks: 4-8,
            effect: "Photography arc progresses to Phase 4",
            unlock: "More paid gig opportunities"
          },
          {
            weeks: 12-16,
            effect: "Corporate career stalls",
            impact: "Harder to get promoted later"
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
        label: "\"Sorry, I have to work\"",
        immediate_effects: {
          meters: {emotional: -3, mental: -2},
          money: +1500,
          relationship_photographer_friend: -0.5,
          relationship_boss: +0.3,
          career_reputation: +1
        },
        short_term_consequences: [
          {
            week: 0,
            card: "Photographer friend responds: 'Understood. Good luck with work.'",
            effect: "Friendship cooling",
            subtext: "They're disappointed"
          },
          {
            week: 1,
            card: "Presentation went well. Boss pleased.",
            effect: "On track for promotion"
          },
          {
            week: 2,
            card: "You scroll through wedding photos online",
            narrative: "Someone else shot it. The photos are beautiful. That could have been you.",
            effect: "Emotional -2, persistent regret"
          }
        ],
        long_term_consequences: [
          {
            weeks: 4-6,
            effect: "Photography arc SEVERELY DAMAGED",
            impact: "Opportunities dry up, friend drifts away"
          },
          {
            weeks: 8-12,
            effect: "Photography skill begins to atrophy",
            impact: "-1 skill every 4 weeks of neglect"
          },
          {
            weeks: 16-20,
            effect: "Arc can potentially restart, but much harder",
            card: "Memory Card: The Road Not Taken",
            narrative: "Sometimes you wonder what would have happened if you'd taken the shoot."
          }
        ],
        arc_impact: {
          photography_dream: "CRITICAL_DAMAGE",
          corporate_career: "ADVANCE",
          financial_stability: "IMPROVE"
        }
      }
    ],
    
    // Time pressure
    time_limit: {
      duration: "24 hours in-game time",
      urgency: "Must decide before Friday evening"
    },
    
    // Context display
    current_state: {
      show_meters: true,
      show_savings: true,
      show_rent_status: true,
      show_relationship_levels: ["boss", "photographer_friend"],
      show_arc_progress: ["photography_dream", "corporate_career"]
    }
  },
  
  // MEMORY ENTRY
  memory_created: {
    title: "The Wedding Shoot Decision",
    emotional_weight: 9,
    reference_in_novel: true,
    quote: "player_choice_dependent",
    regret_potential: true
  }
};
```

---

## Crisis Events: When Choices Collide

### Crisis Trigger System

```javascript
const CRISIS_TRIGGERS = {
  
  // HEALTH CRISIS (Neglect Physical meter)
  health_breakdown: {
    trigger: {
      condition: "physical_meter <= 2 for 8+ weeks",
      alternative: "working_60+_hours for 12+ weeks"
    },
    crisis_card: {
      title: "YOUR BODY IS BREAKING DOWN",
      narrative: `
        You wake up and can't get out of bed. Not "don't want to"—
        physically can't. Your vision swims. Heart racing. Hands shaking.
        
        The mirror shows someone you don't recognize: hollow eyes, 
        weight loss, pale skin. When did this happen?
        
        You've been running on coffee and adrenaline for months.
        You skipped meals. Ignored sleep. Canceled gym. "Too busy."
        
        Your phone buzzes with messages you can't handle right now:
        - Boss: "Where are you? Client meeting in 30 min"
        - Sarah: "Are you okay? Haven't heard from you"
        - Photographer friend: "That gallery opening is tonight"
        
        You need to make a choice. Now.
      `,
      options: [
        {
          id: "hospital",
          label: "Go to urgent care / hospital",
          cost: {money: -400, time: "full day"},
          effects: {
            immediate: "Miss all commitments today",
            short_term: "Mandatory rest (3-7 days)",
            long_term: "Wake-up call, but recovery takes time"
          },
          consequences: [
            "Miss client meeting → Career damage",
            "Miss gallery opening → Photography setback",
            "Sarah worried → Relationship affected",
            "Physical meter forced to minimum 5 for 4 weeks"
          ]
        },
        {
          id: "push_through",
          label: "Take some pills and push through",
          effects: {
            immediate: "Make it to commitments (barely)",
            short_term: "Condition worsens",
            long_term: "Risk of major breakdown or hospitalization"
          },
          consequences: [
            "Physical -2 immediately",
            "20% chance of hospitalization next week (worse outcome)",
            "If hospitalized: out of commission 2+ weeks, permanent consequences"
          ],
          risk: "Very high"
        },
        {
          id: "call_in_sick",
          label: "Call in sick, rest at home today",
          effects: {
            immediate: "Relief, but guilt",
            short_term: "Partial recovery",
            long_term: "Manageable if you change habits"
          },
          consequences: [
            "Miss commitments → moderate damage to arcs",
            "Physical +3 over next week if you actually rest",
            "Must make lifestyle changes or crisis returns"
          ]
        }
      ],
      aftermath: {
        forced_cards: [
          "LIFESTYLE AUDIT",
          "Relationship check-ins (NPCs concerned)",
          "Career conversation (boss questions commitment)",
          "New routine cards appear (healthy habits)"
        ]
      }
    }
  },
  
  // PARENT ILLNESS (Competing priorities)
  parent_crisis: {
    trigger: {
      condition: "Arc at critical phase + random(5% chance per week after week 30)",
      timing: "Worst possible moment"
    },
    crisis_card: {
      title: "YOUR PARENT IS SICK",
      narrative: `
        Your phone rings at 2 AM. It's your sibling.
        
        "Dad's in the hospital. Heart attack. He's stable, but...
        can you come? I don't know how long... the doctors say 
        we should be here."
        
        You hang up and stare at your calendar:
        
        - Tomorrow: Final photography client meeting (could make or break your business)
        - This week: Critical work presentation (promotion decision)
        - Saturday: Sarah's bookshop grand opening (you promised to be there)
        
        Your dad is 800 miles away.
        
        What do you do?
      `,
      options: [
        {
          id: "go_immediately",
          label: "Drop everything and go",
          immediate_effects: {
            emotional: +5,  // Right choice for family
            all_active_arcs: "PAUSE or DAMAGE"
          },
          consequences: [
            "Miss all commitments this week",
            "Photography client: Lost opportunity",
            "Work presentation: Someone else gets promotion",
            "Sarah's opening: She's hurt but understands",
            "Family relationship: Deepened",
            "New arc: Caregiving, family dynamics"
          ],
          time_cost: "1-4 weeks depending on father's recovery"
        },
        {
          id: "attend_commitments_then_go",
          label: "Handle commitments, then travel Friday",
          immediate_effects: {
            mental: -4,  // Guilt and stress
            emotional: -3
          },
          consequences: [
            "Father: 'Where were you?'",
            "Sibling: Resentment for not coming immediately",
            "Keep professional commitments",
            "Personal cost: Guilt, damaged family relationships",
            "NPCs notice you're distracted"
          ],
          moral_weight: "Heavy"
        },
        {
          id: "send_money_stay_here",
          label: "Send money for hospital bills, stay here",
          requirements: {
            savings: ">= $5000"
          },
          immediate_effects: {
            money: -3000,
            emotional: -6,
            mental: -5
          },
          consequences: [
            "Family: Deep disappointment",
            "Father: 'I didn't need money, I needed you'",
            "Sibling: Lasting resentment",
            "Keep all professional opportunities",
            "Permanent relationship damage with family",
            "Regret arc: 'The Choice I Can't Take Back'"
          ],
          moral_weight: "Devastating"
        }
      ],
      followup_weeks: [
        {
          week: 1,
          cards: ["Family update", "Work/career fallout", "NPC reactions"],
          new_decisions: "How much time do you spend visiting? How to balance?"
        },
        {
          week: 4,
          cards: ["Father's recovery status", "Sibling conversation", "Life rebalancing"],
          arc_restart: "Can you rebuild what you paused?"
        }
      ]
    }
  },
  
  // FINANCIAL CRISIS (Multiple factors converge)
  financial_crisis: {
    trigger: {
      conditions_any: [
        "savings < rent_cost + 200",
        "unemployed + weeks > 4",
        "major_expense (car, medical) + low_savings"
      ],
      timing: "When pursuing passion arc (photography) or major life change"
    },
    crisis_card: {
      title: "RENT IS DUE IN 3 DAYS",
      narrative: `
        Bank account: $847
        Rent due: $1,800
        
        You've been chasing the photography dream. The gigs are coming,
        but not fast enough. You've been eating ramen. Walking instead
        of ubering. Skipping coffee with Sarah to save $4.
        
        Three options, all bad:
        
        1. Call your old corporate job and beg for your position back
        2. Borrow from someone (but who?)
        3. Risk eviction and hope a big gig comes through
        
        Your phone buzzes: "Final reminder: Rent due Friday"
        
        This is real now.
      `,
      options: [
        {
          id: "call_old_job",
          label: "Swallow pride, call your old boss",
          effects: {
            emotional: -5,
            pride: -3,
            photography_arc: "ENDS or SEVERELY DAMAGED"
          },
          success_chance: 0.60,
          outcomes: {
            success: "They'll take you back, but at lower position and salary",
            failure: "They already filled your role. Now what?"
          }
        },
        {
          id: "borrow_from_sarah",
          label: "Ask Sarah for a loan",
          requirements: "relationship >= 0.7",
          effects: {
            relationship_sarah: -0.3,
            emotional: -4,
            money: +1800
          },
          consequences: [
            "She lends you the money",
            "But something shifts between you",
            "Debt creates tension",
            "New cards: 'Paying Sarah Back', 'Awkward Interactions'"
          ]
        },
        {
          id: "borrow_from_parent",
          label: "Call your parents",
          requirements: "family_relationship >= 0.5",
          effects: {
            money: +1800,
            pride: -4,
            family_relationship: "COMPLICATED"
          },
          consequences: [
            "'I knew this photography thing wouldn't work out'",
            "They help, but lectures come with it",
            "Your parent's disappointment lingers"
          ]
        },
        {
          id: "gig_hustle",
          label: "Desperate gig hunt (3 days)",
          effects: {
            time: "ALL available time",
            energy: "Depleted",
            physical: -3,
            mental: -4
          },
          success_chance: 0.40,
          outcomes: {
            success: "You cobble together $1,850 from random gigs, exhausted",
            failure: "You make $600. Not enough. Face other consequences."
          }
        },
        {
          id: "risk_eviction",
          label: "Talk to landlord, beg for extension",
          success_chance: 0.25,
          effects: {
            stress: "Maximum",
            emotional: -6
          },
          outcomes: {
            success: "2-week extension, but they're watching you",
            failure: "Eviction proceedings begin. 30 days to move out."
          }
        }
      ]
    }
  }
};
```

---

## Neglect & Consequence Tracking

### The Neglect Accumulator

```javascript
const NEGLECT_SYSTEM = {
  
  tracked_categories: [
    "physical_health",
    "mental_health",
    "relationships",
    "career",
    "finances",
    "creativity",
    "personal_growth"
  ],
  
  neglect_tracking: {
    physical_health: {
      signals: [
        "No exercise cards played in 4+ weeks",
        "Fast food cards > 50% of meals",
        "Sleep <6 hours regularly",
        "Physical meter consistently below 4"
      ],
      early_warnings: [
        {
          week: 4,
          card: "Feeling Sluggish",
          narrative: "You notice you're tired all the time. Coffee doesn't help like it used to."
        },
        {
          week: 8,
          card: "The Warning Signs",
          narrative: "You catch your reflection. When did you start looking this run down?"
        }
      ],
      crisis_point: {
        week: 12,
        card: "HEALTH_BREAKDOWN_CRISIS" // Full crisis card from earlier
      },
      permanent_effects: {
        if_ignored: "Chronic health issues, permanently lower physical ceiling"
      }
    },
    
    relationships: {
      signals: [
        "Haven't played [NPC] card in 6+ weeks",
        "Declined 5+ social invitations in a row",
        "Social meter < 3 for extended period"
      ],
      early_warnings: [
        {
          week: 3,
          card: "Sarah texts: 'Hey stranger, you okay?'",
          narrative: "You realize it's been weeks since you've seen her."
        },
        {
          week: 6,
          card: "Photographer friend stops inviting you",
          narrative: "You've canceled on them three times. They got the message."
        }
      ],
      crisis_point: {
        week: 10,
        card: "THE CONFRONTATION",
        narrative: `
          Sarah shows up at your door.
          
          "I need to say this. You've disappeared. I know you're 
          busy, but... I feel like I don't matter to you anymore."
          
          You start to explain—work, photography, everything—
          but she shakes her head.
          
          "I've heard the explanations. What I haven't seen is you."
          
          This is a breaking point.
        `,
        options: [
          {
            label: "Promise to change and actually commit time",
            requires: "Actually change behavior next 4 weeks"
          },
          {
            label: "Make excuses, ask for more time",
            result: "Relationship severely damaged, may be irreparable"
          }
        ]
      }
    },
    
    career: {
      signals: [
        "Working <30 hours/week without plan",
        "Declining important projects",
        "Missing skill development opportunities",
        "Ignoring boss communications"
      ],
      crisis_point: {
        week: 8-12,
        card: "PERFORMANCE REVIEW",
        narrative: `
          Your boss calls you into their office.
          
          "Let's talk about your performance. You used to be 
          our strongest contributor. Now... you're barely here.
          
          I need to know: Are you committed to this role? 
          Because if not, I need to make some changes."
          
          They slide a document across the desk.
          Performance Improvement Plan.
          
          You have 60 days to turn this around or you're out.
        `
      }
    }
  },
  
  // THE BALANCING ACT
  balance_tracking: {
    ideal_state: "All meters 4-7, no category neglected >4 weeks",
    
    imbalance_warnings: [
      {
        trigger: "One meter 9+, another meter 2-",
        card: "SOMETHING'S OFF",
        narrative: "You're crushing it at work, but you can't remember the last time you felt happy."
      },
      {
        trigger: "Three areas neglected simultaneously",
        card: "EVERYTHING'S FALLING APART",
        narrative: "Work is suffering. Friends are drifting. You're exhausted. How did it get this bad?"
      }
    ],
    
    burnout_formula: {
      calculate: "(high_meter - low_meter) + neglect_weeks",
      threshold: 15,
      result: "BURNOUT_CRISIS_CARD"
    }
  }
};
```

---

## Comprehensive History Tracking

### The Master JSON Structure

Everything that happens gets logged for novel generation:

```javascript
const RUN_HISTORY = {
  run_id: "uuid",
  player_name: "Player",
  start_date: "2025-10-13",
  end_date: "2026-02-15",
  total_weeks: 78,
  ending_type: "Started bookshop with Sarah, left corporate career",
  
  // ACT STRUCTURE
  acts: [
    {
      act: 1,
      title: "Discovery & Possibility",
      weeks: [1, 20],
      arc_threads_introduced: [
        "photography_dream",
        "sarah_relationship",
        "corporate_career"
      ],
      key_moments: [
        {
          week: 8,
          title: "First Coffee with Sarah",
          emotional_weight: 7,
          decision_made: null,
          outcome: "Relationship began",
          quote: "She noticed you were reading Murakami"
        }
      ]
    },
    {
      act: 2,
      title: "Pursuit & Friction",
      weeks: [21, 60],
      decisive_decisions: [
        {
          week: 32,
          decision: "wedding_shoot_vs_work_overtime",
          choice_made: "wedding_shoot",
          consequences: "Photography arc advanced, career arc damaged"
        },
        {
          week: 45,
          decision: "parent_illness_crisis",
          choice_made: "drop_everything_go_to_hospital",
          consequences: "Missed promotion, but family relationship deepened"
        }
      ],
      crises: [
        {
          week: 38,
          type: "health_breakdown",
          trigger: "Physical meter = 1 for 6 weeks",
          resolution: "Hospitalized 5 days, mandatory rest"
        }
      ]
    },
    {
      act: 3,
      title: "Crisis & Resolution",
      weeks: [61, 78],
      climax: {
        week: 72,
        event: "Sarah asks you to co-own bookshop",
        decision: "Leave corporate job, invest savings",
        outcome: "New chapter begins"
      }
    }
  ],
  
  // STORY ARCS (Detailed tracking)
  story_arcs: [
    {
      arc_id: "photography_dream",
      title: "The Photography Dream",
      status: "TRANSFORMED_INTO_SIDE_PASSION",
      
      phases_completed: [
        {
          phase: 1,
          weeks: [12, 16],
          outcome: "Discovered passion"
        },
        {
          phase: 2,
          weeks: [17, 24],
          outcome: "Took course, bought equipment"
        },
        {
          phase: 3,
          weeks: [25, 32],
          decisive_decision: {
            week: 32,
            choice: "wedding_shoot",
            impact: "Arc advanced"
          }
        },
        {
          phase: 4,
          weeks: [33, 48],
          outcome: "Built portfolio, got clients",
          crisis: {
            week: 45,
            type: "parent_illness",
            impact: "Paused arc for 3 weeks"
          }
        }
      ],
      
      final_state: {
        outcome: "Hybrid path—kept as serious hobby while pursuing bookshop",
        fusion_card: "Creative Soul (Photography + Sarah's Dreams)",
        emotional_impact: "Fulfilled without pressure of full-time career"
      },
      
      key_relationships: ["photographer_friend", "sarah"],
      skills_gained: {photography: 7, business: 3},
      
      memorable_moments: [
        {
          week: 32,
          moment: "First wedding shoot",
          narrative: "The camera felt right in your hands. Like coming home.",
          emotional_weight: 9
        },
        {
          week: 41,
          moment: "Gallery showing of your work",
          narrative: "Sarah stood beside you, looking at your photo on the wall. 'You did this,' she whispered.",
          emotional_weight: 8
        }
      ]
    },
    
    {
      arc_id: "sarah_relationship",
      title: "Sarah's Journey",
      status: "SUCCESS_DEEP_BOND",
      
      relationship_timeline: [
        {week: 8, event: "First conversation", level: 0.2},
        {week: 15, event: "Coffee became routine", level: 0.4},
        {week: 28, event: "She shared her bookshop dream", level: 0.6},
        {week: 42, event: "You encouraged her to take the leap", level: 0.8},
        {week: 58, event: "She signed the lease", level: 0.9},
        {week: 67, event: "You offered to help financially", level: 1.0},
        {week: 72, event: "She asked you to be co-owner", level: 1.0}
      ],
      
      decisive_moments: [
        {
          week: 42,
          decision: "Encouraged her to pursue bookshop despite risks",
          impact: "Changed her life trajectory"
        },
        {
          week: 67,
          decision: "Invested $25k of savings into her dream",
          impact: "Showed ultimate commitment"
        }
      ],
      
      shared_memories: [
        {
          week: 28,
          memory: "Late night planning session",
          narrative: "You stayed up until 3am helping her sketch out the floor plan. She cried happy tears.",
          emotional_weight: 9
        },
        {
          week: 74,
          memory: "Building the shelves",
          narrative: "Sawdust and possibility. Her hands stained with wood stain. 'It's real,' she whispered.",
          emotional_weight: 10
        },
        {
          week: 78,
          memory: "Grand opening day",
          narrative: "She looked at you across the bookshop filled with customers. Mouthed: 'We did it.'",
          emotional_weight: 10
        }
      ],
      
      // SARAH'S PERSPECTIVE (for novel)
      sarah_evolution: {
        start: "Quiet barista with hidden dreams",
        key_transformations: [
          {
            week: 28,
            change: "First shared her dream aloud",
            internal: "She'd never told anyone before. You were the first person who didn't laugh."
          },
          {
            week: 42,
            change: "Decided to actually pursue it",
            internal: "Your belief in her gave her permission to believe in herself"
          },
          {
            week: 58,
            change: "Signed the lease despite terror",
            internal: "She almost backed out three times that day. But you were there."
          }
        ],
        end: "Bookshop co-owner, confident, brave",
        
        // What she thought during key moments
        perspective_moments: [
          {
            week: 8,
            her_pov: "I wasn't going to say anything. I never talk to customers. But you were reading Murakami, and I just... spoke."
          },
          {
            week: 28,
            her_pov: "Why am I telling you this? I've never told anyone about the bookshop. But somehow I knew you'd understand."
          },
          {
            week: 72,
            her_pov: "I practiced this conversation fifty times. 'Want to go into business together?' But every version sounded insane. Until I just... asked."
          }
        ]
      }
    },
    
    {
      arc_id: "corporate_career",
      title: "The Corporate Path",
      status: "ABANDONED_FOR_PASSION",
      
      career_progression: [
        {week: 1, position: "Junior Analyst", salary: 55000},
        {week: 20, position: "Analyst", salary: 65000},
        {week: 45, event: "Missed promotion due to parent crisis", salary: 65000},
        {week: 52, event: "Passed over again (photography distraction)", salary: 65000},
        {week: 72, decision: "Resigned to join bookshop", final_salary: 65000}
      ],
      
      why_abandoned: "Realized fulfillment > money. Sarah's dream became shared dream.",
      
      final_reflection: {
        regret_level: 2,  // Out of 10
        peace_level: 9,
        quote: "I traded a cubicle for a bookshop. Best decision I ever made."
      }
    }
  ],
  
  // CRISES & MAJOR EVENTS
  crises: [
    {
      week: 38,
      type: "health_breakdown",
      cause: "Worked 65+ hours/week for 10 weeks, neglected physical health",
      severity: 8,
      resolution: "Hospitalized 5 days, mandatory lifestyle change",
      lasting_impact: "Learned to set boundaries, prioritized health"
    },
    {
      week: 45,
      type: "parent_illness",
      severity: 9,
      decision: "Dropped everything, went to hospital",
      consequences: [
        "Missed work promotion",
        "Photography arc paused",
        "Sarah understood",
        "Family relationship deepened"
      ],
      lasting_impact: "Perspective shift—family > career advancement"
    },
    {
      week: 63,
      type: "financial_strain",
      cause: "Saving for bookshop investment while maintaining apartment",
      severity: 6,
      resolution: "Moved to cheaper place, cut expenses",
      lasting_impact: "Learned to live with less, gained financial discipline"
    }
  ],
  
  // DECISIVE DECISIONS (All major choices)
  decisive_decisions: [
    {
      week: 32,
      decision_id: "wedding_shoot_vs_overtime",
      choice_made: "wedding_shoot",
      alternative_not_taken: "work_overtime",
      immediate_consequences: {
        gained: ["Photography portfolio", "$200", "Photographer friendship +0.3"],
        lost: ["$1500 bonus", "Boss trust", "Promotion track delayed"]
      },
      long_term_impact: "Photography became viable path, but corporate career permanently limited",
      regret_level: 1,  // Very low
      satisfaction_level: 9
    },
    {
      week: 45,
      decision_id: "parent_illness_response",
      choice_made: "drop_everything",
      alternative_not_taken: "handle_commitments_first",
      emotional_weight: 10,
      consequences: "Career impact significant, but no guilt. Family bond strengthened.",
      long_term_impact: "Shifted priorities permanently. Career became means, not end.",
      regret_level: 0
    },
    {
      week: 67,
      decision_id: "invest_in_sarahs_bookshop",
      choice_made: "invest_25k_savings",
      alternative_not_taken: "keep_savings_as_safety_net",
      stakes: "Life savings",
      courage_required: 9,
      outcome: "Became co-owner, changed life trajectory",
      regret_level: 0,
      satisfaction_level: 10
    }
  ],
  
  // CHARACTER RELATIONSHIPS (Detailed)
  npcs: [
    {
      npc_id: "sarah-anderson",
      name: "Sarah Anderson",
      relationship_final: 1.0,
      
      first_met: {week: 8, context: "Café Luna, Murakami book conversation"},
      
      major_moments: [
        {week: 8, event: "First conversation", impact: "Clicked immediately"},
        {week: 28, event: "Shared bookshop dream", impact: "Trust deepened"},
        {week: 42, event: "You encouraged the leap", impact: "Changed her life"},
        {week: 58, event: "She signed lease", impact: "Dream became real"},
        {week: 74, event: "Built shelves together", impact: "Partnership solidified"},
        {week: 78, event: "Grand opening", impact: "Shared triumph"}
      ],
      
      personality_evolution: {
        start: {openness: 4.3, extraversion: 3.4, agreeableness: 4.6, conscientiousness: 4.8, neuroticism: 3.9},
        end: {openness: 4.8, extraversion: 4.7, agreeableness: 4.7, conscientiousness: 4.9, neuroticism: 2.1}
      },
      
      memorable_quotes: [
        {week: 8, quote: "Kafka on the Shore? That's a good one.", context: "First words to you"},
        {week: 28, quote: "I've never told anyone this before.", context: "Sharing bookshop dream"},
        {week: 72, quote: "Want to be my business partner?", context: "The ask"},
        {week: 78, quote: "We did it.", context: "Opening day"}
      ],
      
      // FOR NOVEL GENERATION
      arc: "Barista with hidden dreams → Confident bookshop owner",
      role_in_story: "Catalyst and co-protagonist",
      emotional_core: "Belief enabled transformation"
    },
    {
      npc_id: "marcus-chen",
      name: "Marcus Chen",
      relationship_final: 0.7,
      role: "Best friend, voice of reason",
      
      key_moments: [
        {week: 20, event: "Warned you about burning out", impact: "You ignored him"},
        {week: 38, event: "Visited you in hospital", impact: "'I told you so' but with love"},
        {week: 45, event: "Covered for you at work during parent crisis", impact: "True friend"},
        {week: 72, event: "Celebrated your resignation", impact: "'About time you followed your heart'"}
      ]
    }
  ],
  
  // METERS OVER TIME (For novel pacing)
  meter_history: {
    physical: {
      average: 5.2,
      lowest: {week: 38, value: 1, event: "Health crisis"},
      highest: {week: 70, value: 8, event: "Healthy lifestyle established"},
      trend: "Started high, crashed mid-story, recovered and stabilized"
    },
    mental: {
      average: 5.8,
      critical_lows: [
        {week: 32, value: 2, event: "Stress of decision"},
        {week: 45, value: 1, event: "Parent crisis + work pressure"}
      ],
      trend: "Volatile, multiple crisis points, eventual peace"
    },
    social: {
      average: 7.1,
      trend: "Consistently high, maintained relationships despite chaos"
    },
    emotional: {
      average: 6.8,
      highest: {week: 78, value: 10, event: "Opening day"},
      trend: "Journey from searching to fulfilled"
    }
  },
  
  // SKILLS DEVELOPED
  skills: {
    photography: {start: 0, end: 7, pivotal_moments: ["First shoot", "Gallery showing"]},
    business: {start: 0, end: 6, learned_through: "Helping Sarah plan bookshop"},
    emotional_intelligence: {start: 4, end: 8, growth_driver: "Deep relationships"},
    work_life_balance: {start: 2, end: 7, learned_through: "Health crisis"}
  },
  
  // ITEMS & SYMBOLS
  significant_items: [
    {
      item: "Camera",
      acquired: {week: 18},
      significance: "Symbol of creative awakening",
      appeared_in_moments: [32, 41, 56]
    },
    {
      item: "Sarah's blue scarf",
      first_noticed: {week: 8},
      significance: "Visual anchor of Sarah's character",
      described_as: "Cerulean blue, always worn"
    },
    {
      item: "Bookshop lease",
      week: 58,
      significance: "Physical proof of dreams made real"
    }
  ],
  
  // ENDING DATA
  ending: {
    type: "new_beginning",
    title: "The Bookshop Dream",
    outcome: "Left corporate career, co-founded bookshop with Sarah",
    
    final_state: {
      career: "Bookshop co-owner",
      location: "Same city, different neighborhood",
      relationships: {
        sarah: "Business partner & close friend",
        photographer_friend: "Still friends, collaborate occasionally",
        marcus: "Still best friend",
        family: "Closer after parent crisis"
      },
      financial: "Lower income, higher satisfaction",
      fulfillment: 9.5
    },
    
    legacy: {
      what_you_built: "A community bookshop",
      who_you_became: "Someone brave enough to choose meaning over money",
      what_you_learned: "Fulfillment > security, relationships > career, courage is choosing despite fear"
    },
    
    final_reflection: `
      You stand in the bookshop on a quiet Tuesday afternoon. 
      Sarah is helping a kid find a book. The coffee machine hisses. 
      Someone laughs in the reading nook.
      
      Two years ago, you were in a cubicle, pretending to care about 
      quarterly reports. Now you smell old books and fresh coffee. 
      Now you built something that matters.
      
      Was it worth it? The pay cut, the risk, the fear?
      
      You look at Sarah. She catches your eye and smiles.
      
      Yes. A thousand times yes.
    `
  },
  
  // NOVEL GENERATION DATA
  narrative_metadata: {
    tone: "Hopeful, introspective, emotionally authentic",
    themes: ["Courage to pursue dreams", "Relationships as catalyst", "Meaning over money"],
    emotional_arc: "Searching → Discovering → Struggling → Choosing → Becoming",
    
    chapter_structure: [
      {act: 1, chapters: 8, focus: "Discovery and possibility"},
      {act: 2, chapters: 12, focus: "Pursuit and friction (most dramatic)"},
      {act: 3, chapters: 6, focus: "Crisis and resolution"}
    ],
    
    pov_chapters: [
      {character: "Sarah", week: 28, title: "The Dream She'd Never Told"},
      {character: "Sarah", week: 58, title: "The Day She Signed"},
      {character: "Marcus", week: 38, title: "Hospital Visit"},
      {character: "Parent", week: 45, title: "What They Didn't Say"}
    ],
    
    must_include_scenes: [
      "Week 8: First conversation",
      "Week 32: The wedding shoot decision",
      "Week 38: Health breakdown",
      "Week 45: Parent crisis",
      "Week 67: Investment decision",
      "Week 74: Building shelves together",
      "Week 78: Grand opening"
    ]
  }
};
```

---

## Integration with Existing Systems

### How This Layers onto Card System

```javascript
// CARD GENERATION NOW CONSIDERS ARCS
function generateDailyCards(player) {
  const baseCards = generateBaseCards(player.phase, player.meters);
  const arcCards = generateArcCards(player.active_arcs, player.week);
  const crisisCards = checkForCrisis(player.neglect_tracking, player.meters);
  const decisiveCards = checkForDecisiveDecision(player.active_arcs, player.week);
  
  // PRIORITY SYSTEM
  if (decisiveCards.length > 0) {
    // Decisive decision takes over the day
    return decisiveCards[0]; // Only show this card
  }
  
  if (crisisCards.length > 0) {
    // Crisis interrupts normal flow
    return [crisisCards[0], ...baseCards.slice(0, 2)];
  }
  
  // Normal day: Mix base cards with arc progression cards
  return [
    ...arcCards.filter(c => c.priority === 'high').slice(0, 2),
    ...baseCards.slice(0, 4),
    ...arcCards.filter(c => c.priority === 'medium').slice(0, 2)
  ];
}

// TRACK EVERYTHING
function onCardPlayed(card, choice) {
  // Update meters (existing system)
  updateMeters(card.effects);
  
  // NEW: Track for history
  runHistory.card_plays.push({
    week: currentWeek,
    card_id: card.id,
    choice: choice.id,
    outcome: choice.outcome
  });
  
  // NEW: Update arc progress
  if (card.arc_id) {
    updateArcProgress(card.arc_id, choice);
  }
  
  // NEW: Track neglect
  updateNeglectTracking(card.category);
  
  // NEW: Check for consequences
  checkConsequences(currentWeek);
}
```

---

## Summary

This system transforms Unwritten from a pleasant life sim into a **dramatic story generator**:

✅ **Multi-phase story arcs** create sustained tension (8-30 weeks)  
✅ **Decisive decision points** force hard choices with real consequences  
✅ **Crisis events** emerge from player behavior (neglect, imbalance, timing)  
✅ **Consequence tracking** makes choices matter long-term  
✅ **Comprehensive history JSON** captures everything for novel generation  
✅ **Integrates seamlessly** with existing card/meter/phase systems  

**The result:** Every playthrough generates a unique, dramatic story with genuine tension, meaningful choices, and emotional payoff—a story worth reading as a novel.

The free book will be good. The premium novel will be **compelling** because the life was compelling.