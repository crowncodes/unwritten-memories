# Unwritten: Multi-Lifetime Continuity Systems

## The Challenge

A playthrough spanning 8-10 seasons (potentially 200-360 weeks / 4-7 years per character) requires sophisticated systems to maintain:
- **Context Management** (can't keep everything in active memory)
- **Consistency Tracking** (avoid contradictions across decades)
- **Identity Evolution** (character changes meaningfully over time)
- **Narrative Coherence** (life story makes sense as a whole)
- **NPC Lifecycle** (characters live their own lives in parallel)

---

## Hierarchical Context System

### The Four-Tier Architecture

```
┌─────────────────────────────────────────────────────────┐
│ TIER 1: CURRENT ACTIVE CONTEXT (Always in Memory)      │
│ Last 12 weeks in FULL detail                           │
│ Size: ~2MB | Generation Use: Full detail for AI        │
├─────────────────────────────────────────────────────────┤
│         TIER 2: RECENT MEMORY (Rolling Window)          │
│         Last 50 weeks summarized                        │
│         Size: ~5MB | Generation Use: Reference context  │
├─────────────────────────────────────────────────────────┤
│           TIER 3: LIFE STORY (Compressed)               │
│           All previous seasons compressed 50:1          │
│           Size: ~5-10MB for 8-10 seasons (200-360 weeks)│
│           Generation Use: Foundational truths           │
├─────────────────────────────────────────────────────────┤
│        TIER 4: CHARACTER STATE (Current Snapshot)       │
│        Who you are NOW (not history)                    │
│        Size: ~1MB | Generation Use: Present identity    │
└─────────────────────────────────────────────────────────┘
```

### Tier 1: Current Active Context

```javascript
const TIER_1_ACTIVE = {
  scope: "Last 12 weeks",
  detail_level: "Complete - every card play, every conversation",
  
  contains: {
    current_season: {
      season_number: 8,
      season_title: "The Bookshop Opening",
      season_length_selected: 36, // Player chose Epic (12/24/36 options)
      weeks_in_season: 36,
      current_week: 28,
      aspiration: "Open bookshop with Sarah",
      act: 2 // Act II of three-act structure
    },
    
    active_arcs: [
      {
        arc_id: "bookshop_business",
        phase: "preparation",
        key_moments: ["Signed lease", "Renovation started", "Inventory ordered"],
        current_tension: "Deadline approaching, budget tight"
      },
      {
        arc_id: "sarah_relationship",
        phase: "deep_partnership",
        recent_developments: ["Business partners now", "Trust at 0.95"],
        current_tension: "Stress testing friendship"
      }
    ],
    
    recent_cards: [
      /* Every single card played in last 12 weeks */
    ],
    
    current_relationships: {
      /* Full relationship objects for all active NPCs */
      sarah: {
        level: 5,
        bond: 0.95,
        trust: 0.92,
        last_interaction: "2 days ago",
        recent_memories: [/* Last 10 memories */],
        current_feelings: "Excited but terrified about opening"
      }
      // ... all active NPCs
    },
    
    current_meters: {
      physical: 6,
      mental: 4,
      social: 8,
      emotional: 7
    },
    
    current_resources: {
      energy: 5,
      max_energy: 7,
      money: 850, // Spent most on business
      savings: 0
    },
    
    obligations: [
      "Work 3 days/week at old job",
      "Bookshop renovation supervision",
      "Weekly check-ins with Sarah"
    ],
    
    pending_decisions: [
      {
        decision: "Hire employee or do it alone",
        deadline: "Week 10",
        implications: "Money vs workload"
      }
    ],
    
    emotional_states_history: [
      /* Last 12 weeks of emotional states */
    ]
  },
  
  memory_impact: "~2MB",
  generation_use: "Full detail - AI can reference anything recent"
};
```

### Tier 2: Recent Memory (Rolling Window)

```javascript
const TIER_2_RECENT = {
  scope: "Weeks 1-50 (last ~1 year)",
  detail_level: "Summarized - major events and patterns",
  
  contains: {
    completed_seasons: [
      {
        season: 7,
        title: "Building Momentum",
        weeks: [85, 107],
        aspiration: "Establish Photography Side Business",
        result: "SUCCESS",
        key_events: [
          "First paid gig",
          "Financial crisis (borrowed from Marcus)",
          "Portfolio recognition"
        ],
        character_development: {
          confidence: "+0.5",
          photography_skill: "4 → 7",
          openness: "+0.3"
        },
        major_relationships: {
          marcus: "Deepened through crisis support",
          sarah: "Grew through shared creative passion"
        }
      },
      {
        season: 6,
        title: "The Crossroads",
        weeks: [60, 84],
        aspiration: "Decide Career Path",
        result: "SUCCESS - Chose hybrid photographer + day job",
        key_events: [
          "Career crisis",
          "Negotiated part-time arrangement",
          "First exhibition"
        ]
      }
      // ... last 3-4 completed seasons
    ],
    
    major_decisions: [
      {
        week: 67,
        decision: "Invested $25k in Sarah's bookshop",
        reasoning: "Believed in her dream + financial opportunity",
        consequences: ["Business partner", "Savings depleted", "Relationship deepened"],
        regrets: "None yet, but risky"
      },
      {
        week: 58,
        decision: "Chose wedding shoot over work presentation",
        reasoning: "Photography passion over corporate advancement",
        consequences: ["Career path limited", "Photography viable", "Boss relationship damaged"],
        regrets: "Sometimes wonders about corporate path"
      }
      // ... all major decisions in window
    ],
    
    key_crises: [
      {
        week: 78,
        crisis: "Financial emergency - rent + business costs",
        resolution: "Borrowed from Marcus",
        lasting_impact: "Debt resolved, but financial anxiety increased"
      },
      {
        week: 91,
        crisis: "Health scare (exhaustion)",
        resolution: "Forced rest, delegated work",
        lasting_impact: "Better work-life boundaries"
      }
    ],
    
    relationship_milestones: {
      sarah: [
        {week: 67, event: "Business partnership formed"},
        {week: 78, event: "Supported through doubt crisis"},
        {week: 95, event: "Celebrated lease signing together"}
      ],
      marcus: [
        {week: 78, event: "Asked for loan (deepened trust)"},
        {week: 85, event: "Paid back loan (honored commitment)"}
      ]
    },
    
    significant_achievements: [
      {week: 72, achievement: "First profitable photography quarter"},
      {week: 88, achievement: "Quit corporate job for creative life"},
      {week: 95, achievement: "Signed bookshop lease"}
    ],
    
    identity_shifts: [
      {week: 60, from: "Corporate Designer", to: "Hybrid Creative"},
      {week: 88, from: "Hybrid Creative", to: "Full-time Creative Entrepreneur"}
    ]
  },
  
  memory_impact: "~5MB",
  generation_use: "Reference for callbacks - 'Remember when...', consistency checks"
};
```

### Tier 3: Life Story (Compressed)

```javascript
const TIER_3_COMPRESSED = {
  scope: "All previous seasons (8-10 seasons, 200-360 weeks typical)",
  detail_level: "Heavily compressed - 50:1 ratio",
  compression_strategy: "Keep defining moments, discard routine",
  
  contains: {
    phase_transitions: [
      {
        week: 1,
        phase: "Early Discovery",
        identity: "Anxious Creative starting out",
        key_baseline: {
          personality: [4.2, 3.1, 2.0, 3.8, 4.9],
          life_direction: "Pursue Creative Fulfillment",
          starting_state: "28 years old, graphic designer, single, moderate network"
        }
      },
      {
        week: 60,
        phase: "Establishment",
        identity: "Emerging Photographer finding voice",
        trigger: "Career crossroads - chose creativity",
        major_change: "Stopped apologizing for dreams"
      },
      {
        week: 150,
        phase: "Peak Life",
        identity: "Creative Entrepreneur & Partner",
        trigger: "Business partnership with Sarah",
        major_change: "From solo dreamer to collaborative builder"
      }
    ],
    
    defining_moments: [
      {
        week: 8,
        moment: "Chose wedding shoot over work promotion",
        why_defining: "First time prioritized passion over security",
        quote: "'I want to create, not just execute.'",
        lasting_impact: "Set pattern of choosing authenticity"
      },
      {
        week: 28,
        moment: "Sarah showed you her business plan",
        why_defining: "First person she trusted with her dream",
        quote: "'Then we'll both be brave failures together.'",
        lasting_impact: "Became her believer, changed her life path"
      },
      {
        week: 67,
        moment: "Invested life savings in bookshop",
        why_defining: "Bet everything on partnership and belief",
        quote: "'I believe in you. And this.'",
        lasting_impact: "Point of no return - fully committed"
      }
      // ... only the MOST defining moments (maybe 30-50 total)
    ],
    
    major_relationships_summary: {
      sarah: {
        met: "Week 8",
        relationship_journey: "Stranger → Friend → Close Friend → Business Partner → [current]",
        key_beats: [
          "Week 8: First conversation (Murakami)",
          "Week 28: Business plan reveal",
          "Week 67: Investment & partnership",
          "Week 95: Lease signing celebration"
        ],
        defining_quote: "'You believed in me when I couldn't believe in myself.'",
        current_state: "Business partner, trust 0.95, potentially deeper feelings emerging"
      },
      
      marcus: {
        met: "Week 1",
        relationship_journey: "Best friend → Crisis support → Trusted confidant",
        key_beats: [
          "Week 1: Starting friend",
          "Week 78: Lent money during crisis",
          "Week 85: Debt repaid (trust proven)"
        ],
        defining_quote: "'I've got you. Always.'",
        current_state: "Best friend, trust 0.88, steady presence"
      }
      // ... other major NPCs (5-10 max at any time)
    },
    
    identity_evolution_timeline: [
      {week: 1, identity: "The Anxious Creative", traits_snapshot: [4.2, 3.1, 2.0, 3.8, 4.9]},
      {week: 30, identity: "Emerging Photographer", traits_snapshot: [4.5, 3.3, 2.4, 3.9, 4.5]},
      {week: 90, identity: "Confident Creative", traits_snapshot: [4.7, 3.8, 3.2, 4.0, 3.8]},
      {week: 150, identity: "Creative Entrepreneur & Partner", traits_snapshot: [4.8, 4.2, 3.8, 4.3, 3.2]}
    ],
    
    critical_decisions_compressed: [
      /* Only life-changing decisions, compressed to essence */
      "Week 8: Photography over promotion → Creative path",
      "Week 67: $25k investment → Business partnership",
      "Week 88: Quit corporate → Full creative commitment"
    ],
    
    life_direction_evolution: [
      {week: 1, direction: "Pursue Creative Fulfillment", confidence: 0.6},
      {week: 60, direction: "Pursue Creative Fulfillment", confidence: 0.85, note: "Tested and confirmed"},
      {week: 150, direction: "Build Legacy + Creative Fulfillment", confidence: 0.95, note: "Expanded to partnership/impact"}
    ]
  },
  
  memory_impact: "~5-10MB for 8-10 seasons (200-360 weeks)",
  compression_ratio: "50:1 (300 weeks of detail → compressed to 6 weeks worth of data)",
  generation_use: "Foundational truth - 'Who has this person been across their life?'"
};
```

### Tier 4: Character State (Current Snapshot)

```javascript
const TIER_4_CURRENT = {
  scope: "Present moment only",
  detail_level: "Complete snapshot of WHO YOU ARE NOW",
  
  contains: {
    current_identity: {
      primary: "Creative Entrepreneur",
      secondary: "Business Partner",
      emerging: "Mentor/Teacher (starting to unlock)",
      self_narrative: "I'm the person who took the risk. Who believed in someone's dream and made it real.",
      confidence_level: 0.92
    },
    
    current_personality: {
      openness: 4.8, // Evolved from 4.2
      conscientiousness: 4.2, // Evolved from 3.1
      extraversion: 3.8, // Evolved from 2.0
      agreeableness: 4.3, // Evolved from 3.8
      neuroticism: 3.2, // Evolved from 4.9
      
      evolution_notes: [
        "Openness +0.6: Embraced risky creative path",
        "Conscientiousness +1.1: Running business requires discipline",
        "Extraversion +1.8: Partnership and community building",
        "Neuroticism -1.7: Confidence from proven success"
      ]
    },
    
    all_skills_current: {
      photography: 9,
      business: 7,
      leadership: 4,
      design: 6,
      communication: 7,
      // ... all skills at current levels
    },
    
    all_relationships_current: {
      /* Every NPC ever met, with current state */
      sarah: {
        level: 5,
        bond: 0.95,
        trust: 0.92,
        current_arc: "Business partnership, feelings emerging",
        last_interaction: "2 days ago",
        weeks_known: 142
      },
      
      boss_former: {
        level: 1,
        bond: 0.1,
        trust: 0.2,
        current_arc: "Relationship ended when quit",
        last_interaction: "50 weeks ago",
        weeks_known: 88,
        status: "inactive"
      }
      // ... ALL NPCs
    },
    
    identity_tags_accumulated: [
      "Anxious Creative (Week 1)",
      "Emerging Photographer (Week 30)",
      "Confident Creative (Week 90)",
      "Creative Entrepreneur (Week 150)",
      "Business Partner (Week 95)",
      "Risk-Taker (Week 67)",
      "Believer in Others (Week 28)"
    ],
    
    current_phase_and_age: {
      phase: "Peak Life",
      age: 31, // Started at 28, 150 weeks later
      weeks_lived: 150,
      life_stage: "Building achievement"
    },
    
    current_resources: {
      money: 850,
      savings: 0,
      assets: ["Bookshop partnership share (50%)"],
      debts: []
    },
    
    permanent_consequences: [
      "Corporate career path closed (chose creative)",
      "Business partnership with Sarah (ongoing commitment)",
      "Reputation in creative community (established)",
      "Financial risk taken (all savings invested)"
    ],
    
    active_emotional_baseline: {
      typical_states: ["MOTIVATED", "CONFIDENT", "PASSIONATE"],
      rare_states: ["ANXIOUS", "DISCOURAGED"],
      triggers: {
        motivated: "Business progress, creative success",
        anxious: "Financial pressure, high stakes moments",
        confident: "Default state now (evolved from anxious)"
      }
    }
  },
  
  memory_impact: "~1MB",
  generation_use: "WHO YOU ARE NOW - present tense identity"
};
```

---

## Canonical Facts System

### Preventing Contradictions

```javascript
const CANONICAL_FACTS = {
  philosophy: "Establish immutable truths on first occurrence, never contradict",
  
  // IDENTITY (immutable once set)
  identity: {
    name: "Alex Chen",
    starting_age: 28,
    birth_year: 1997,
    starting_location: "Major City",
    never_changes: true
  },
  
  // CAREER HISTORY (permanent record)
  career_history: [
    {
      weeks: [1, 102],
      job: "Graphic Designer at XYZ Corp",
      salary: "$65k/year",
      status: "Left voluntarily"
    },
    {
      weeks: [103, "current"],
      job: "Creative Entrepreneur / Photographer",
      income: "Variable ($30k-80k projected)",
      status: "Active"
    }
  ],
  
  // MAJOR DECISIONS (permanent record)
  decisive_decisions: [
    {
      week: 8,
      decision: "Chose wedding shoot photography over work promotion opportunity",
      context: "Boss requested overtime for presentation, friend asked for wedding photographer",
      choice: "Wedding shoot",
      stated_reason: "'I want to create, not just execute.'",
      consequences: [
        "Boss relationship damaged (-0.3 trust)",
        "Photography path opened",
        "Promotion track closed"
      ],
      irreversible: true
    },
    {
      week: 28,
      decision: "Promised Sarah honest opinion on business plan",
      context: "Sarah revealed bookshop dream, asked for honesty",
      choice: "Gave genuine, supportive feedback",
      stated_reason: "'This is real. You're prepared. The numbers work.'",
      consequences: [
        "Sarah's confidence boosted",
        "Became her 'believer'",
        "Partnership path opened"
      ],
      irreversible: true
    },
    {
      week: 67,
      decision: "Invested $25,000 life savings in Sarah's bookshop",
      context: "Sarah needed capital, player had savings, high trust",
      choice: "Full investment for 50% partnership",
      stated_reason: "'I believe in you. And this.'",
      consequences: [
        "Became business partner",
        "Savings depleted",
        "Financial risk taken",
        "Relationship fundamentally changed"
      ],
      irreversible: true
    },
    {
      week: 88,
      decision: "Quit corporate job to focus on photography + bookshop",
      context: "Business taking off, corporate job feeling meaningless",
      choice: "Resignation",
      stated_reason: "'I'm not playing it safe anymore.'",
      consequences: [
        "Steady income lost",
        "Full creative commitment",
        "Identity shift to entrepreneur"
      ],
      irreversible: true
    }
  ],
  
  // NPC FACTS (locked on first appearance, evolves but core identity stable)
  npcs: {
    sarah_anderson: {
      identity_lock: {
        name: "Sarah Anderson",
        age: 28, // Ages in parallel with player
        appearance: "Light brown wavy hair, brown eyes, light freckles, petite",
        core_traits: "Reserved, conscientious, loves books obsessively",
        family: "Grandmother died 2 years before Week 1, raised by grandmother",
        never_changes: true
      },
      
      canonical_facts: [
        "Works at Café Luna as barista (Weeks 1-95)",
        "Owns bookshop (Week 95-present)",
        "Grandmother left her $15k for 'something brave'",
        "Birthday: June 15",
        "Favorite author: Haruki Murakami",
        "Has cerulean blue scarf (grandmother's)",
        "Been saving for bookshop for 4 years before revealing",
        "Nervous habit: traces coffee cup rim",
        "Says 'I'm sorry' reflexively when vulnerable"
      ],
      
      life_events: [
        {week: 95, event: "Opened bookshop (The Book Nook)"},
        {week: 67, event: "Formed business partnership with player"},
        {week: 28, event: "Revealed bookshop dream to player"}
      ],
      
      personality_evolution: {
        week_1: [3.5, 4.0, 2.8, 3.9, 3.8],
        week_150: [4.3, 4.5, 3.4, 4.6, 2.9],
        evolution: "Openness +0.8 (took risks), Extraversion +0.6 (business owner), Neuroticism -0.9 (confidence from success)"
      }
    },
    
    marcus_rivera: {
      identity_lock: {
        name: "Marcus Rivera",
        age: 29,
        appearance: "Tall, athletic build, warm brown eyes, easy smile",
        core_traits: "Loyal, conscientious, pragmatic but supportive",
        family: "Close with parents, youngest of three",
        never_changes: true
      },
      
      canonical_facts: [
        "Best friend since Week 1 (pre-existing relationship)",
        "Works in software engineering",
        "Lent player $1,800 during crisis (Week 78)",
        "Player repaid debt (Week 85)",
        "Birthday: March 3",
        "Loves basketball, follows Lakers",
        "Has girlfriend Jessica (met Week 45)"
      ]
    }
  },
  
  // WORLD FACTS (persistent world state)
  world: {
    locations: {
      cafe_luna: {
        exists: "Weeks 1-present",
        type: "Coffee shop",
        significance: "Where player met Sarah, site of many key moments",
        canonical_details: [
          "Window seat is player's spot",
          "Barista knows player's order",
          "Has warm wooden tables, plants by windows",
          "Smells like coffee and vanilla pastries"
        ],
        never_closed: true // Still exists
      },
      
      the_book_nook: {
        exists: "Week 95-present",
        type: "Bookshop",
        owners: ["Player (50%)", "Sarah (50%)"],
        location: "Downtown, near Café Luna",
        canonical_details: [
          "Has vintage books section (Sarah's passion)",
          "Large front windows",
          "Opened Week 95",
          "Named by Sarah"
        ]
      },
      
      xyz_corp_office: {
        exists: "Weeks 1-102 (player access)",
        type: "Corporate office",
        relationship: "Former employer",
        access: "Lost when quit Week 88"
      }
    },
    
    global_events: [] // Major world events timestamped if applicable
  },
  
  // ESTABLISHED PATTERNS (consistent behaviors)
  patterns: {
    player_patterns: [
      "Always chooses authenticity over safety",
      "Believes in others' dreams strongly",
      "Financial risk-taker when emotionally invested",
      "Observant of small details (notices Sarah's tells)",
      "Doesn't regret bold choices, even when hard"
    ],
    
    relationship_patterns: {
      sarah: [
        "Coffee meetups are Tuesday ritual",
        "Player notices when Sarah touches grandmother's bracelet (nervous tell)",
        "Sarah asks player's opinion before major decisions",
        "They finish each other's sentences now"
      ]
    }
  }
};
```

### Contradiction Prevention System

```javascript
const CONTRADICTION_PREVENTION = {
  
  pre_generation_checks: async function(content_to_generate) {
    const checks = [];
    
    // CHECK 1: Has player ever worked at X?
    if (content_to_generate.mentions_job) {
      const query = await checkCareerHistory(content_to_generate.job_name);
      checks.push({
        type: "career",
        valid: query.found && query.timeline_matches,
        details: query
      });
    }
    
    // CHECK 2: What is character's relationship to NPC?
    if (content_to_generate.mentions_npc) {
      const query = await checkRelationshipState(content_to_generate.npc_id);
      checks.push({
        type: "relationship",
        valid: query.relationship_exists,
        current_state: query.current_state,
        details: query
      });
    }
    
    // CHECK 3: Does character have skill/knowledge?
    if (content_to_generate.assumes_skill) {
      const query = await checkSkillState(content_to_generate.skill);
      checks.push({
        type: "skill",
        valid: query.has_skill && query.level >= content_to_generate.required_level,
        details: query
      });
    }
    
    // CHECK 4: Timeline coherence
    if (content_to_generate.references_past_event) {
      const query = await checkTimelineEvent(content_to_generate.event_id);
      checks.push({
        type: "timeline",
        valid: query.event_occurred && query.week <= content_to_generate.current_week,
        details: query
      });
    }
    
    // CHECK 5: Location accessibility
    if (content_to_generate.uses_location) {
      const query = await checkLocationAccess(content_to_generate.location_id, content_to_generate.current_week);
      checks.push({
        type: "location",
        valid: query.accessible,
        details: query
      });
    }
    
    return {
      all_valid: checks.every(c => c.valid),
      checks: checks,
      blocks_generation: checks.some(c => !c.valid && c.critical)
    };
  },
  
  consistency_rules: [
    "NPCs remember what they know about player",
    "NPCs DON'T know what they haven't been told",
    "Skills don't disappear (may atrophy slowly, -1 per 100 weeks inactive)",
    "Past decisions can't be undone",
    "Consequences persist unless actively resolved",
    "Locations you've visited remain accessible (unless narrative close)",
    "People you've met remain in world (unless death/move narratively justified)",
    "Money spent is gone (unless loan repaid)",
    "Time moves forward only (no retcons)"
  ],
  
  auto_resolution: {
    when_conflict_detected: [
      "1. Check canonical facts database",
      "2. Prioritize: explicit recent facts > older assumptions",
      "3. If unresolvable, flag for human review",
      "4. Default: Use most recently established fact",
      "5. Never generate content that contradicts Tier 1 (current) data"
    ]
  }
};
```

---

## NPC Lifecycle System

### Parallel Lives

NPCs don't freeze when not interacting with player. They live parallel lives:

```javascript
const NPC_LIFECYCLE = {
  
  // NPCs AGE IN PARALLEL
  aging: {
    rule: "All NPCs age at same rate as player",
    effects: {
      every_decade: [
        "Appearance descriptions update",
        "Life stage appropriate changes",
        "Energy/capability shifts",
        "New life-stage appropriate cards"
      ]
    },
    
    example: {
      sarah: {
        week_1: {
          age: 28,
          description: "Young woman, energetic but uncertain",
          life_stage: "Early establishment"
        },
        week_520: {
          age: 38,
          description: "Mature woman, confident business owner",
          life_stage: "Peak achievement",
          changes: [
            "More confident posture",
            "Laugh lines around eyes",
            "Voice has more authority"
          ]
        }
      }
    }
  },
  
  // NPCs HAVE LIFE EVENTS IN BACKGROUND
  background_life_events: {
    process: "AI generates life events for NPCs based on their personality, goals, and time passed",
    
    notification_system: {
      if_close_relationship: "Player gets notified directly",
      if_distant_relationship: "Player hears through others or discovers later",
      if_no_contact: "Event happens, player may never know"
    },
    
    examples: [
      {
        npc: "Marcus",
        week: 120,
        event: "Got engaged to Jessica",
        player_notification: "Marcus texts: 'Big news! I proposed. She said yes!'",
        relationship_impact: "If player responds supportively, +0.1 bond",
        life_impact: "Marcus now planning wedding, different availability"
      },
      {
        npc: "Sarah",
        week: 200,
        event: "Bookshop won local business award",
        player_notification: "You see it in local paper (if didn't interact recently) OR Sarah tells you directly (if did)",
        context_dependent: true
      },
      {
        npc: "Former_coworker",
        week: 180,
        event: "Got promoted to your old boss's role",
        player_notification: "You hear through LinkedIn or mutual connection",
        feeling: "Complicated mix of validation and 'what if'"
      }
    ]
  },
  
  // NPCs CAN LEAVE
  departure: {
    reasons: [
      "Move away (job, relationship, family)",
      "Relationship ends (player neglect, conflict, natural drift)",
      "Death (if elderly, if health crisis, if accident)",
      "Life paths diverge (no longer compatible)"
    ],
    
    permanence: "Departures are permanent unless narrative reason to return",
    
    notification: {
      close_relationship: "Farewell scene, emotional weight",
      moderate_relationship: "They tell you they're leaving",
      distant_relationship: "You find out they've left"
    },
    
    examples: [
      {
        npc: "Marcus",
        week: 300,
        reason: "Job opportunity in another city",
        player_choice: {
          options: [
            "Convince him to stay (high social capital cost)",
            "Support his decision (lose regular contact)",
            "Offer business partnership (keep him close)"
          ]
        },
        if_leaves: {
          status: "Moved away, relationship persists remotely",
          future_interactions: "Rare, special occasions",
          nostalgia_weight: "High - best friend who left"
        }
      }
    ]
  },
  
  // NPCS CAN RETURN
  reconnection: {
    trigger_chance: "If NPC left but relationship was significant",
    
    conditions: [
      "Random encounter cards (low probability)",
      "Narrative-appropriate moments",
      "Player seeks them out",
      "NPC reaches out"
    ],
    
    reunion_rules: {
      time_remembered: "NPCs remember time apart",
      relationship_picks_up: "Where it left off, but time acknowledged",
      they_evolved_too: "NPC has changed during absence",
      nostalgia_heavy: "Emotional weight of reunion"
    },
    
    example: {
      npc: "Photographer_mentor",
      left: "Week 100 (moved to NYC)",
      reconnection: "Week 300 (visiting hometown)",
      reunion_card: {
        title: "Unexpected Reunion",
        description: "You see them at gallery opening. It's been... what, four years?",
        dialogue: "'You did it. You actually did it. I'm so proud of you.'",
        current_state: "They're successful wedding photographer now",
        relationship: "Picks up warmly, but different - time passed",
        nostalgia: "Remember when they first taught you about light and composition"
      }
    }
  }
};
```

---

## Identity Evolution Tracking

### Character Transformation Over Decades

```javascript
const IDENTITY_EVOLUTION = {
  
  // TRACKING IDENTITY SHIFTS
  identity_timeline: [
    {
      week: 1,
      primary_identity: "Anxious Creative",
      personality: [4.2, 3.1, 2.0, 3.8, 4.9],
      self_narrative: "I'm the person who plays it safe and hates myself for it.",
      confidence: 0.4,
      fears: ["Failure", "Judgment", "Taking up space"],
      desires: ["Creative expression", "Meaningful work", "Courage"]
    },
    
    {
      week: 50,
      primary_identity: "Emerging Photographer",
      personality: [4.5, 3.4, 2.6, 3.9, 4.3],
      self_narrative: "I'm beginning to believe I might be able to do this.",
      confidence: 0.65,
      fears: ["Not being good enough", "Financial instability"],
      desires: ["Artistic recognition", "Sustainable creative life"],
      major_shift: "Took first big risk (wedding shoot over promotion)"
    },
    
    {
      week: 100,
      primary_identity: "Confident Creative",
      personality: [4.7, 3.9, 3.4, 4.1, 3.6],
      self_narrative: "I chose this path and I'm making it work.",
      confidence: 0.85,
      fears: ["Letting down people who believe in me"],
      desires: ["Building something lasting", "Partnership"],
      major_shift: "Quit corporate job, fully committed to creative path"
    },
    
    {
      week: 150,
      primary_identity: "Creative Entrepreneur & Partner",
      personality: [4.8, 4.2, 3.8, 4.3, 3.2],
      self_narrative: "I'm the person who takes risks and believes in people's dreams.",
      confidence: 0.92,
      fears: ["Business failure affecting Sarah"],
      desires: ["Making the bookshop a success", "Deeper partnership with Sarah"],
      major_shift: "Business partnership, identity now intertwined with another person"
    }
  ],
  
  // PERSONALITY DRIFT
  personality_evolution_rules: {
    openness: {
      increases_with: ["New experiences", "Risk-taking", "Creative success"],
      decreases_with: ["Routine dominance", "Fear responses"],
      typical_range: "±0.5 per 100 weeks if actively evolving"
    },
    
    conscientiousness: {
      increases_with: ["Responsibility", "Business ownership", "Commitments"],
      decreases_with: ["Burnout", "Rejection of structure"],
      typical_range: "±0.3 per 100 weeks"
    },
    
    extraversion: {
      increases_with: ["Positive social experiences", "Confidence", "Public roles"],
      decreases_with: ["Social trauma", "Preference for solitude"],
      typical_range: "±0.5 per 100 weeks if significant social change"
    },
    
    agreeableness: {
      increases_with: ["Successful collaborations", "Empathy development"],
      decreases_with: ["Betrayal", "Competitive pressure"],
      typical_range: "±0.2 per 100 weeks"
    },
    
    neuroticism: {
      decreases_with: ["Therapy", "Success", "Confidence", "Age/wisdom"],
      increases_with: ["Trauma", "Chronic stress", "Crises"],
      typical_range: "±0.5 per 100 weeks (often decreases with maturity)"
    }
  },
  
  // MAJOR TRANSFORMATION TRIGGERS
  transformation_triggers: [
    "Phase transitions (Early → Establishment → Peak)",
    "Major crises survived",
    "Significant achievements",
    "Deep relationships formed",
    "Therapy/self-work arcs",
    "Identity-questioning seasons",
    "Near-death experiences",
    "Becoming a mentor/parent"
  ],
  
  // REFLECTION MOMENTS
  reflection_system: {
    trigger: "Every 50-100 weeks, offer reflection card",
    
    card_example: {
      title: "Looking Back",
      description: "You're cleaning out old things and find a journal from 3 years ago. You barely recognize the person who wrote it.",
      
      reflection_prompts: [
        "What would you tell your past self?",
        "What are you proud of changing?",
        "What do you miss about who you were?",
        "What stayed the same (core values)?"
      ],
      
      mechanical_effect: {
        updates_self_narrative: true,
        creates_memory_with_high_weight: true,
        generates_novel_moment: "Chapter-worthy introspection"
      }
    }
  }
};
```

---

## Memory Compression Strategy

### What to Keep, Summarize, Discard

```javascript
const COMPRESSION_STRATEGY = {
  
  when_to_compress: "After each season ends, compress seasons older than 50 weeks",
  
  // ALWAYS KEEP (Full Detail)
  always_keep: [
    "Decisive decisions (every detail preserved)",
    "Crisis events (full narrative)",
    "Major relationship milestones (full scenes)",
    "Identity shifts (complete context)",
    "Significant achievements (full story)",
    "Defining moments (everything)",
    "Quotes that reveal character"
  ],
  
  // SUMMARIZE (Condense)
  summarize: [
    "Routine weeks → single line ('Weeks 45-48: Normal work routine, steady progress')",
    "Minor activities → aggregate stats ('Went to gym 12 times, cooked 8 meals')",
    "Unsuccessful attempts → outcome only ('Tried speed dating, didn't connect with anyone')",
    "NPCs not currently relevant → summary state ('Marcus: Still friends, works in tech, engaged')"
  ],
  
  // DISCARD (Delete)
  discard: [
    "Individual routine card plays (keep stats only)",
    "Micro meter fluctuations (keep major changes)",
    "Failed minor aspirations (keep only if led to something)",
    "Irrelevant NPCs never developed beyond level 1",
    "Locations visited once and never returned",
    "Activities tried once with no significance"
  ],
  
  // EXAMPLE COMPRESSION
  compression_examples: {
    before_compression: {
      week_142: {
        days: 7,
        cards_played: 49,
        detailed_narrative: "5000 words of day-by-day description",
        every_conversation: "Full dialogue for 15 interactions",
        meter_tracking: "Daily meter changes recorded"
      }
    },
    
    after_compression: {
      week_142: {
        summary: "Routine work week. Photography side gig. Fitness maintenance. Nothing notable.",
        word_count: "15 words",
        compression_ratio: "333:1"
      }
    },
    
    vs_significant_week: {
      week_156: {
        summary: "DECISIVE DECISION - Chose to invest $25k in Sarah's bookshop over keeping safety net. Changed life trajectory. Sarah cried. Partnership formed. Point of no return.",
        preserved_detail: "Full scene of the decision moment, dialogue, emotional context, consequences",
        word_count: "2000 words preserved",
        compression_ratio: "No compression - too important"
      }
    }
  },
  
  // COMPRESSION RATIOS BY CONTENT TYPE
  typical_ratios: {
    routine_weeks: "40 weeks → 200 words (200:1 ratio)",
    event_weeks: "1 week → 500 words (10:1 ratio)",
    decisive_weeks: "1 week → 2000 words (no compression)",
    entire_season: {
      if_routine: "12 weeks → 3000 words (40:1)",
      if_dramatic: "12 weeks → 15000 words (8:1)"
    }
  }
};
```

---

## Integration with Novel Generation

From `novel-generation-data-structure.md`, the continuity system feeds chapter generation:

```javascript
const CONTINUITY_TO_NOVEL = {
  
  // TIER 1 (Current) → Chapter Detail
  current_context: {
    use: "Full scene detail for current season chapters",
    detail_level: "Every conversation, emotional beat, decision",
    example: "Chapter about bookshop opening pulls from last 12 weeks detailed data"
  },
  
  // TIER 2 (Recent) → Callbacks & References
  recent_memory: {
    use: "Callback moments, character remembering recent past",
    detail_level: "Summary with key emotional beats",
    example: "'You remember the financial crisis three months ago, when Marcus lent you money...'"
  },
  
  // TIER 3 (Compressed) → Deep Backstory
  life_story: {
    use: "Foundational character truth, long-term consistency",
    detail_level: "Defining moments only",
    example: "'You've been building toward this since that day you chose the wedding shoot over promotion, two years ago.'"
  },
  
  // TIER 4 (Current State) → Character Voice
  character_state: {
    use: "POV voice, personality in narration, current identity",
    detail_level: "Complete present-tense snapshot",
    example: "Narration reflects current confidence (0.92) vs starting anxiety"
  },
  
  // CANONICAL FACTS → Continuity Anchors
  canonical_facts: {
    use: "Prevent contradictions in novel generation",
    detail_level: "Immutable truths",
    example: "Chapter generation checks: Has Sarah always worked at Café Luna weeks 1-95? Yes."
  }
};
```

---

## Technical Performance

### Memory Management

```javascript
const MEMORY_PERFORMANCE = {
  total_size_8_10_seasons: {
    tier_1_current: "2MB (12 weeks)",
    tier_2_recent: "5MB (50 weeks)",
    tier_3_compressed: "5-10MB (8-10 seasons compressed 50:1)",
    tier_4_state: "1MB (current snapshot)",
    canonical_facts: "2MB (all immutable truths)",
    total: "~15-20MB for complete 8-10 season character"
  },
  
  query_performance: {
    tier_1_lookup: "< 10ms (in-memory)",
    tier_2_lookup: "< 50ms (indexed)",
    tier_3_lookup: "< 200ms (compressed search)",
    canonical_fact_check: "< 5ms (indexed)"
  },
  
  compression_performance: {
    compress_season: "< 2 seconds per season",
    triggered: "After season ends, async background process",
    player_impact: "None - happens during interseason"
  }
};
```

---

## Summary

Multi-season continuity in Unwritten maintains consistency across 8-10 seasons (200-360 weeks) through:

1. **Four-Tier Context System** - Balances detail (recent) with scope (entire life)
2. **Canonical Facts Database** - Prevents contradictions through immutable truth tracking
3. **NPC Lifecycle** - Characters live parallel lives, age, leave, return
4. **Identity Evolution** - Personality and self-concept evolve meaningfully over decades
5. **Smart Compression** - Preserves defining moments, compresses routine 50:1
6. **Consistency Checks** - Pre-generation validation prevents impossible content

The system ensures that a character's story remains **coherent** across 8-10 seasons while tracking **meaningful evolution**, creating a life story that feels both **authentic** and **narratively satisfying** when compiled into Life Bookshelf novels.

Every turn, day, and season contributes to a larger story (up to 150k words across 10 seasons) that never contradicts itself, honors its past, and allows genuine transformation. When a character reaches the season limit or player chooses to retire them, their complete Life Bookshelf becomes a permanent archive—a full novel trilogy of their journey.

