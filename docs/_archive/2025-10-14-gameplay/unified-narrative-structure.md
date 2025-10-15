# Unified Narrative Structure System

## Overview

Unwritten's narrative structure integrates three interconnected systems to create compelling, personalized life stories:
1. **Three-Act Narrative Arcs** - Multi-phase story threads with decisive decisions
2. **Archive & Persistence** - Season-based progression with memory preservation
3. **AI Personality & Memory** - Dynamic NPCs that evolve through interactions

**Core Philosophy:** Every playthrough generates a unique, dramatic story with genuine tension, meaningful choices, and emotional payoff—a story worth reading as a novel.

---

## I. Season-Based Narrative Structure

### The Season Model

```
SEASON = One complete story arc (12-100 weeks)
├─ Act I: Discovery & Possibility (Weeks 1-20)
│  • Meet characters, explore options
│  • Establish dreams and desires
│  • Plant seeds of future arcs
│  • Low stakes, high variety
├─ Act II: Pursuit & Friction (Weeks 21-60)
│  • Commit to paths
│  • Face meaningful obstacles
│  • Make hard choices with real consequences
│  • Moderate-to-high stakes
└─ Act III: Crisis & Resolution (Weeks 61-End)
   • Major decisions with lasting impact
   • Convergence of multiple arc threads
   • Sacrifices and triumphs
   • Highest stakes
```

### Lifetime Structure

```
LIFETIME = Character's full story (potentially 3000+ weeks, 20-40 seasons)
├─ Season 1: "Finding My Footing"
├─ Season 2: "The Photography Dream"
├─ Season 3: "Sarah's Bookshop"
├─ Season 4-7: Continued character development
└─ Final Season: Player-chosen ending
→ Generates complete collection (novel or series)
```

**Key Principles:**
- Each season is a complete, satisfying story arc that can stand alone
- Seasons build on each other—consequences persist, relationships evolve
- Players can end after any season OR continue indefinitely
- No forced endings—players choose when the story is complete

---

## II. Story Arc Architecture

### Multi-Phase Arc Template

Story arcs span 8-30+ weeks, creating sustained dramatic tension through progressive escalation, decisive decisions, and lasting consequences.

**Example: Photography Dream Arc**

```javascript
const STORY_ARC = {
  id: "photography-dream",
  title: "The Photography Dream",
  category: "Career/Passion",
  
  phases: [
    {
      phase: 1,
      title: "The Spark",
      weeks: [2, 4],
      trigger: "Discover camera or meet photographer NPC",
      goals: ["Take 10 photos", "Share work with someone"],
      cards_unlocked: ["Photography Basics", "Camera Shop Visit"],
      tension: "Curiosity vs. practicality"
    },
    {
      phase: 2,
      title: "Serious Interest",
      weeks: [4, 8],
      trigger: "Complete Phase 1 + meet mentor",
      goals: ["Take online course", "Buy better equipment"],
      cards_unlocked: ["Weekend Photography", "Portfolio Building"],
      tension: "Time commitment + financial investment"
    },
    {
      phase: 3,
      title: "The Opportunity",
      weeks: [8, 12],
      decisive_decision: {
        card: "WEDDING SHOOT INVITATION",
        description: "Friend invites you to assist on paid wedding shoot",
        same_day_conflict: "WORK OVERTIME REQUEST",
        stakes: {
          choose_shoot: {
            positive: ["Progress arc", "+2 Photography skill", "$200"],
            negative: ["Miss $1500 bonus", "-1 Career reputation"]
          },
          choose_work: {
            positive: ["$1500 bonus", "+1 Career reputation"],
            negative: ["Kill photography arc", "Lose friendship"]
          }
        }
      },
      tension: "Dream vs. security"
    },
    {
      phase: 4,
      title: "Building Momentum",
      weeks: [12, 20],
      trigger: "Chose shoot in Phase 3",
      goals: ["Get 3 paid gigs", "Build client base"],
      crisis_risk: "Financial strain",
      tension: "Sustainable vs. pipe dream"
    },
    {
      phase: 5,
      title: "The Crossroads",
      weeks: [20, 24],
      decisive_decision: {
        card: "FULL-TIME PHOTOGRAPHY OFFER",
        description: "Studio offers full-time position, 40% less salary",
        stakes: {
          go_full_time: {
            positive: ["Living your dream", "Creative fulfillment"],
            negative: ["Financial stress", "Risk of failure"]
          },
          stay_corporate: {
            positive: ["Financial security", "Keep benefits"],
            negative: ["Dream deferred", "Regret", "What if?"]
          }
        }
      },
      tension: "Ultimate commitment"
    }
  ],
  
  failure_conditions: [
    {
      condition: "Choose work over shoot in Phase 3",
      result: "Arc ends, but memory persists as 'The Road Not Taken'"
    },
    {
      condition: "Neglect arc for 8+ weeks during phases 2-4",
      result: "Arc atrophies, skill degrades, opportunities close"
    }
  ],
  
  success_variations: [
    {
      path: "Full-time photographer",
      fusion_card: "Professional Photographer You",
      ending_impact: "Career fulfilled, financial moderate"
    },
    {
      path: "Hybrid (corporate + side gig)",
      fusion_card: "Balanced Creative You",
      ending_impact: "Career stable, creativity outlet"
    }
  ]
};
```

### Arc Integration with Seasons

**Within a Season:**
- 2-4 story arcs run concurrently
- Arcs interact and create conflicts
- Season climax typically resolves primary arc
- Secondary arcs may continue into next season

**Across Seasons:**
- Failed arcs from Season 1 can restart in Season 2
- Success in one arc unlocks new arcs
- Long-term consequences persist (relationships, career, skills)
- Themes and callbacks create continuity

---

## III. Decisive Decision Points

### Structure of Major Decisions

Every decisive decision follows this pattern:

**1. Foreshadowing (1-2 weeks before)**
```
Week -2: "Your friend mentions a big wedding coming up"
Week -1: "Boss mentions important client arriving soon"
```

**2. The Decisive Card**
```
Title: "THE WEDDING SHOOT"
Type: DECISIVE_DECISION
Rarity: Legendary

Narrative:
"It's Thursday evening. Your phone buzzes twice.
 
First: Your photographer friend offers $200 wedding gig Saturday
Second: Your boss demands mandatory overtime, $1500 bonus
 
You can't do both."

Options:
• "I'll do the shoot" → Photography arc advances, career damaged
• "Sorry, I have to work" → Career advances, dream deferred

Time Limit: 24 hours in-game
Context Display: Shows current meters, savings, relationships
```

**3. Immediate Consequences (Week 0-2)**
```
Week 0: Boss is noticeably cold at Monday meeting
Week 1: Wedding photos turned out amazing, referrals start
Week 2: Missed promotion cycle, no raise this quarter
```

**4. Long-Term Consequences (Weeks 4-16)**
```
Weeks 4-8: Photography arc progresses to Phase 4
Weeks 12-16: Corporate career permanently limited
```

**5. Memory Entry**
```
Title: "The Wedding Shoot Decision"
Emotional Weight: 9/10
Reference in Novel: Yes
Quote: Player choice-dependent
Regret Potential: High if wrong choice for character
```

### Decision-NPC Integration

NPCs remember your decisions and react accordingly:

**If you chose photography over work:**
```
Photographer Friend (trust +0.3):
"I can't thank you enough for showing up. You were incredible."

Boss (trust -0.4):
"Where were you Saturday? We needed you."

Sarah (observing):
"I saw you make that choice. It was brave."
```

**If you chose work over photography:**
```
Photographer Friend (trust -0.5, attraction -0.2):
"Understood. Good luck with work." [disappointment evident]

Boss (trust +0.3):
"Good to see you have your priorities straight."

Sarah (observing):
"I get it. Bills don't pay themselves."
```

---

## IV. Crisis Events System

### Crisis Trigger Mechanics

Crises emerge from player behavior patterns tracked across multiple dimensions:

**Health Crisis**
```
Trigger: Physical meter ≤ 2 for 8+ weeks OR 60+ hour work weeks
Timing: When pursuing major arc (worst possible moment)

Crisis Card: "YOUR BODY IS BREAKING DOWN"
Narrative: Can't get out of bed, vision swimming, heart racing
Options:
• Go to hospital → Miss all commitments, mandatory rest
• Push through → Risk major breakdown
• Call in sick → Partial recovery if habits change

Aftermath:
• Forced lifestyle audit
• NPCs express concern
• New healthy habit cards appear
• Boss questions commitment
```

**Relationship Crisis**
```
Trigger: Haven't played [NPC] card in 6+ weeks
         Declined 5+ social invitations
         Social meter < 3 extended period

Crisis Card: "THE CONFRONTATION"
Narrative: Sarah shows up at your door
"I need to say this. You've disappeared. I know you're busy,
but... I feel like I don't matter to you anymore."

Options:
• Promise to change (must follow through next 4 weeks)
• Make excuses → Relationship severely damaged
```

**Financial Crisis**
```
Trigger: Savings < rent + $200 while pursuing passion arc
Timing: When committed to risky career change

Crisis Card: "RENT IS DUE IN 3 DAYS"
Bank: $847 | Rent: $1,800

Options:
• Call old job and beg for position back
• Borrow from Sarah/parents (affects relationships)
• Desperate gig hustle (40% success, depletes energy)
• Risk eviction (25% success for extension)
```

**Parent Illness Crisis**
```
Trigger: Arc at critical phase + 5% chance per week after week 30
Timing: Absolutely worst possible moment

Crisis Card: "YOUR PARENT IS SICK"
2 AM call: "Dad's in the hospital. Heart attack. Can you come?"

Your calendar:
• Tomorrow: Final photography client meeting
• This week: Critical work presentation
• Saturday: Sarah's bookshop grand opening

Options:
• Drop everything and go → All arcs pause/damage, family deepens
• Handle commitments then go Friday → Guilt, family resentment
• Send money, stay here → Financial help, devastating relationship damage
```

### Crisis Memory Weight

All crises create high-weight memories (0.85-1.0) that:
- Influence future NPC behavior
- Unlock reflective dialogue
- Shape character personality evolution
- Become key moments in generated novel

---

## V. NPC Personality & Memory System

### OCEAN Personality Model

Every NPC has five core traits (1.0-5.0 scale):

**Openness to Experience**
- High (4.0-5.0): Creative, curious, embraces new experiences
- Low (1.0-2.5): Practical, conventional, prefers routine

**Conscientiousness**
- High: Organized, reliable, goal-driven
- Low: Spontaneous, flexible, procrastinates

**Extraversion**
- High: Energized by social interaction, outgoing
- Low: Prefers solitude, reserved, introspective

**Agreeableness**
- High: Empathetic, cooperative, avoids conflict
- Low: Direct, competitive, skeptical

**Neuroticism**
- High: Anxious, emotional sensitivity, stress-prone
- Low: Calm, emotionally stable, resilient

### Personality Evolution Through Story

**Example: Sarah's Evolution Across Season**

```
Week 1 (First Meeting):
Openness: 3.5 | Conscientiousness: 4.0 | Extraversion: 2.8
Agreeableness: 3.9 | Neuroticism: 3.8

Behavior: Quiet barista, dreams hidden, anxious about sharing

Week 12 (After supportive interactions):
Openness: 3.8 (+0.3) | Neuroticism: 3.5 (-0.3)

Behavior: More willing to share dreams, less anxious around you

Week 40 (After opening bookshop together):
Openness: 4.3 (+0.8) | Conscientiousness: 4.5 (+0.5)
Extraversion: 3.4 (+0.6) | Neuroticism: 2.9 (-0.9)

Behavior: Confident business owner, embraced risky dream
```

**Evolution Triggers:**
- Single interaction: 0.1-0.3 point shift
- Major life event: 0.3-0.5 point shift
- Crisis overcome: Reduces neuroticism
- Success achieved: Increases conscientiousness
- Betrayal: Reduces agreeableness
- New experience: Increases openness

### Three-Tier Memory System

```
┌─────────────────────────────────────┐
│  SHORT-TERM MEMORY (24 hours)       │
│  • Recent conversations              │
│  • Emotional reactions               │
│  • Last 5-10 interactions            │
│  Weight: 0.3-0.5                     │
└─────────────────────────────────────┘
           ↓ Consolidation
┌─────────────────────────────────────┐
│  MEDIUM-TERM MEMORY (1-4 weeks)     │
│  • Relationship patterns             │
│  • Significant events                │
│  • 15-30 key moments                 │
│  Weight: 0.6-0.8                     │
└─────────────────────────────────────┘
           ↓ Integration
┌─────────────────────────────────────┐
│  LONG-TERM MEMORY (Permanent)       │
│  • Major life events                 │
│  • Deep relationship history         │
│  • Defining moments                  │
│  Weight: 0.85-1.0                    │
└─────────────────────────────────────┘
```

**Memory Structure Example:**
```json
{
  "id": "mem_12847",
  "timestamp": "Week 12, Day 3",
  "event": "coffee_deep_conversation",
  "location": "cafe_luna",
  "participants": ["player", "sarah_anderson"],
  "description": "Late night at Café Luna. Sarah's hands wrapped around cold mug, speaking quietly about fear of failure...",
  "emotion": "vulnerable_solidarity",
  "weight": 0.85,
  "tags": ["vulnerability", "shared_fears", "trust_building"],
  "personality_impact": {
    "neuroticism": -0.2,
    "agreeableness": +0.15
  },
  "unlocks": ["business_planning", "grandmother_grave"]
}
```

### Trust & Attraction Systems

**Trust (0.0-1.0 scale):**
- Builds through: Consistent interaction, keeping promises, crisis support
- Breaks through: Broken promises, absence in crisis, betrayal
- Thresholds:
  - 0.0-0.2: Stranger, guarded
  - 0.4-0.6: Friend, shares personal info
  - 0.8-0.95: Best friend, complete trust
  - 0.95-1.0: Soulmate-level connection

**Attraction (0.0-1.0 scale):**
- Separate from trust (romantic vs. reliable)
- Factors: Personality compatibility, shared interests, emotional intimacy, timing
- Outcomes:
  - High attraction + low trust = tension
  - High trust + low attraction = deep friendship
  - Both high = romantic potential

### NPC Agency & Behavior

**NPCs actively initiate:**
```
"Hey, I found this great bookstore. Want to check it out?"
[Suggests activities matching your interests]

"So... I applied for that grant. I'm terrified but excited."
[Shares life updates proactively]

"I feel like we haven't really talked in a while. Coffee?"
[Expresses needs for connection]

"I appreciate your help, but I need to figure this out alone."
[Sets boundaries]

"I'm sorry, I'm just not in the mood today. Reschedule?"
[Has bad days]
```

**Contextual Awareness:**
NPCs notice and respond to:
- Your current stress level
- Recent major life events
- Time since last interaction
- Your career situation
- Other relationships in your life

**Example:**
```
If player stressed from work:
"You look exhausted. Want to just watch something mindless?"

If player just had breakthrough:
"I heard about your promotion! We should celebrate!"

If you've been neglecting them:
"It's been three weeks. Was starting to think you forgot about me."
```

---

## VI. Archive & Persistence System

### Season Archives

**When Season Ends:**
```
SEASON 3 COMPLETE: "SARAH'S BOOKSHOP"
┌────────────────────────────────────┐
│ Duration: 45 weeks                 │
│ Outcome: SUCCESS                   │
│ Opened bookshop with Sarah         │
│                                    │
│ [📖 Generate Season Book]          │
│ [👁️ Review Season Archive]        │
│ [➡️ Start New Season]              │
│ [🔚 End This Lifetime]             │
└────────────────────────────────────┘
```

**Season Archive Contains:**
- All cards evolved during season
- Week-by-week story log with decisive decisions
- Relationship evolution (trust/attraction changes)
- NPC personality changes
- Statistics (money, career, skills)
- Generated free book (3-5k words)
- Premium novella option (12-15k words)

### Lifetime Archives

**Character Organization:**
```
CHARACTER 1: ALEX CHEN
Age: 28 → 47 (19 years lived)
Status: ACTIVE (Season 8 in progress)

📚 SEASON ARCHIVES (7 complete)
  S1: "Finding My Footing" (18 weeks)
  S2: "The Photography Spark" (22 weeks)
  S3: "Sarah's Bookshop" (45 weeks)
  S4: "The Expansion" (38 weeks)
  S5: "Sarah's Departure" (28 weeks)
  S6: "Rebuilding Solo" (31 weeks)
  S7: "New Beginnings" (42 weeks)

🎮 CURRENTLY PLAYING:
  Season 8: "Teaching & Mentoring" (Week 15/30)
```

### What Carries Forward

**Between Seasons (Same Character):**
✅ Personality (evolved state)
✅ Skills (current levels)
✅ NPC Relationships (trust, attraction, memories)
✅ Money (current balance)
✅ Career (current position)
✅ Location (where you are)
✅ All consequences

**Example:**
```
END Season 3:
├─ Money: $8,000 (spent savings on shop)
├─ Sarah: Trust 1.0, Partner
├─ Career: Bookshop co-owner
└─ Age: 31

START Season 4:
├─ Money: Still $8,000 (you're broke!)
├─ Sarah: Still your partner (but watch for tension)
├─ Career: Still bookshop co-owner
└─ New challenges based on Season 3 outcome
```

**Between Characters (Different Lifetimes):**
- Account-wide mastery bonuses only
- No direct skill/money/relationship transfers
- "Character echoes" for familiar NPCs
- Déjà vu moments in dialogue

### Book Generation Tiers

**Per-Season:**
```
TIER 1: FREE SUMMARY (3-5k words)
├─ Auto-generated at season end
├─ Covers major moments
├─ Single POV (player)
└─ Embedded card images

TIER 2: PREMIUM NOVELLA ($2.99, 12-15k words)
├─ Enhanced narrative
├─ Multi-POV chapters (NPCs)
├─ Professional formatting
├─ Character development deep-dives
└─ Internal monologues
```

**Multi-Season Collections:**
```
FREE: Individual season books (read separately)

PREMIUM: Compiled Collection ($7.99)
├─ All seasons revised with continuity edits
├─ Themes and callbacks highlighted
├─ Character development across seasons
├─ Bridging text between seasons
└─ 45,000+ words total
```

**Full Lifetime Novel (When character ends):**
```
FREE: LIFETIME SUMMARY (10-15k words)
├─ Key moments from all seasons
├─ Major relationships and arcs
└─ Final reflection

PREMIUM: COMPLETE NOVEL ($9.99, 80-150k words)
├─ Full narrative across all seasons
├─ Multi-volume format (trilogy structure)
├─ Deep character development
├─ Thematic through-lines
└─ Export to PDF/ePub
```

---

## VII. Comprehensive History Tracking

### Master JSON Structure

Everything tracked for novel generation:

```javascript
const RUN_HISTORY = {
  run_id: "uuid",
  character_name: "Alex Chen",
  start_date: "2025-10-13",
  end_date: "2026-02-15",
  total_weeks: 78,
  total_seasons: 3,
  ending_type: "Started bookshop with Sarah",
  
  // ACT STRUCTURE PER SEASON
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
      key_moments: [...]
    },
    // Act 2 & 3...
  ],
  
  // STORY ARCS (Detailed)
  story_arcs: [
    {
      arc_id: "photography_dream",
      title: "The Photography Dream",
      status: "TRANSFORMED_INTO_SIDE_PASSION",
      phases_completed: [...],
      decisive_decisions: [...],
      final_state: {
        outcome: "Hybrid path—serious hobby + bookshop",
        fusion_card: "Creative Soul",
        emotional_impact: "Fulfilled without pressure"
      },
      memorable_moments: [
        {
          week: 32,
          moment: "First wedding shoot",
          narrative: "Camera felt right. Like coming home.",
          emotional_weight: 9
        }
      ]
    },
    {
      arc_id: "sarah_relationship",
      title: "Sarah's Journey",
      status: "SUCCESS_DEEP_BOND",
      relationship_timeline: [
        {week: 8, event: "First conversation", level: 0.2},
        {week: 28, event: "She shared bookshop dream", level: 0.6},
        {week: 72, event: "She asked you to be co-owner", level: 1.0}
      ],
      decisive_moments: [...],
      shared_memories: [...],
      
      // SARAH'S PERSPECTIVE (for multi-POV novel)
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
          }
        ],
        end: "Confident bookshop co-owner",
        
        perspective_moments: [
          {
            week: 8,
            her_pov: "I wasn't going to say anything. I never talk to customers. But you were reading Murakami, and I just... spoke."
          },
          {
            week: 72,
            her_pov: "I practiced this fifty times. But every version sounded insane. Until I just... asked."
          }
        ]
      }
    }
  ],
  
  // CRISES & MAJOR EVENTS
  crises: [
    {
      week: 38,
      type: "health_breakdown",
      cause: "Worked 65+ hours/week for 10 weeks",
      severity: 8,
      resolution: "Hospitalized 5 days, lifestyle change",
      lasting_impact: "Learned to set boundaries"
    }
  ],
  
  // DECISIVE DECISIONS (All major choices)
  decisive_decisions: [
    {
      week: 32,
      decision_id: "wedding_shoot_vs_overtime",
      choice_made: "wedding_shoot",
      alternative_not_taken: "work_overtime",
      immediate_consequences: {...},
      long_term_impact: "Photography viable, corporate limited",
      regret_level: 1,
      satisfaction_level: 9
    }
  ],
  
  // CHARACTER RELATIONSHIPS (Detailed)
  npcs: [
    {
      npc_id: "sarah-anderson",
      name: "Sarah Anderson",
      relationship_final: 1.0,
      first_met: {week: 8, context: "Café Luna, Murakami book"},
      major_moments: [...],
      personality_evolution: {
        start: {
          openness: 3.5, 
          extraversion: 2.8, 
          neuroticism: 3.8
        },
        end: {
          openness: 4.8, 
          extraversion: 4.7, 
          neuroticism: 2.1
        }
      },
      memorable_quotes: [
        {week: 8, quote: "Kafka on the Shore? That's a good one."},
        {week: 78, quote: "We did it.", context: "Opening day"}
      ],
      arc: "Barista with hidden dreams → Confident bookshop owner",
      role_in_story: "Catalyst and co-protagonist"
    }
  ],
  
  // METERS OVER TIME (For novel pacing)
  meter_history: {
    physical: {
      average: 5.2,
      lowest: {week: 38, value: 1, event: "Health crisis"},
      trend: "Crashed mid-story, recovered"
    },
    emotional: {
      average: 6.8,
      highest: {week: 78, value: 10, event: "Opening day"}
    }
  },
  
  // SKILLS DEVELOPED
  skills: {
    photography: {
      start: 0, 
      end: 7, 
      pivotal_moments: ["First shoot", "Gallery showing"]
    }
  },
  
  // ITEMS & SYMBOLS
  significant_items: [
    {
      item: "Camera",
      acquired: {week: 18},
      significance: "Symbol of creative awakening"
    },
    {
      item: "Sarah's blue scarf",
      first_noticed: {week: 8},
      significance: "Visual anchor of Sarah's character"
    }
  ],
  
  // ENDING DATA
  ending: {
    type: "new_beginning",
    title: "The Bookshop Dream",
    outcome: "Co-founded bookshop with Sarah",
    final_state: {...},
    legacy: {
      what_you_built: "A community bookshop",
      who_you_became: "Someone brave enough to choose meaning over money"
    },
    final_reflection: "You stand in the bookshop on a quiet Tuesday afternoon..."
  },
  
  // NOVEL GENERATION METADATA
  narrative_metadata: {
    tone: "Hopeful, introspective, emotionally authentic",
    themes: ["Courage to pursue dreams", "Relationships as catalyst"],
    emotional_arc: "Searching → Discovering → Struggling → Choosing → Becoming",
    pov_chapters: [
      {character: "Sarah", week: 28, title: "The Dream She'd Never Told"},
      {character: "Sarah", week: 58, title: "The Day She Signed"}
    ],
    must_include_scenes: [
      "Week 8: First conversation",
      "Week 32: Wedding shoot decision",
      "Week 38: Health breakdown",
      "Week 78: Grand opening"
    ]
  }
};
```

---

## VIII. Neglect & Consequence Tracking

### The Neglect System

The game tracks what you're ignoring and punishes neglect with escalating consequences:

**Tracked Categories:**
- Physical health
- Mental health
- Relationships
- Career
- Finances
- Creativity
- Personal growth

**Escalation Pattern:**

```
Week 4: Early Warning
Card: "Feeling Sluggish"
"You notice you're tired all the time."

Week 8: Clear Warning
Card: "The Warning Signs"
"You catch your reflection. When did you start looking this run down?"

Week 12: Crisis Point
Card: "HEALTH BREAKDOWN CRISIS"
Forced choice with major consequences

Permanent Effects if Ignored:
Chronic issues, permanently lower physical ceiling
```

**Relationship Neglect Example:**
```
Week 3: Sarah texts: "Hey stranger, you okay?"
Week 6: Photographer friend stops inviting you
Week 10: THE CONFRONTATION
Sarah: "I need to say this. You've disappeared. I know you're 
busy, but... I feel like I don't matter to you anymore."

Options:
• Promise to change (must prove it next 4 weeks)
• Make excuses → Relationship may be irreparable
```

### Balance Tracking

```
Ideal State: All meters 4-7, no category neglected > 4 weeks

Imbalance Warnings:
• One meter 9+, another 2- → "Something's off"
• Three areas neglected → "Everything's falling apart"

Burnout Formula:
(high_meter - low_meter) + neglect_weeks
If > 15 → BURNOUT CRISIS CARD
```

---

## IX. Integration: How Systems Work Together

### Card Generation Priority System

```javascript
function generateDailyCards(player) {
  const baseCards = generateBaseCards(player.phase, player.meters);
  const arcCards = generateArcCards(player.active_arcs, player.week);
  const crisisCards = checkForCrisis(player.neglect_tracking);
  const decisiveCards = checkForDecisiveDecision(player.active_arcs);
  
  // PRIORITY HIERARCHY
  if (decisiveCards.length > 0) {
    // Decisive decision takes over the day
    return decisiveCards[0];
  }
  
  if (crisisCards.length > 0) {
    // Crisis interrupts normal flow
    return [crisisCards[0], ...baseCards.slice(0, 2)];
  }
  
  // Normal day: Mix base + arc progression
  return [
    ...arcCards.filter(c => c.priority === 'high').slice(0, 2),
    ...baseCards.slice(0, 4),
    ...arcCards.filter(c => c.priority === 'medium').slice(0, 2)
  ];
}
```

### Complete Interaction Flow

```
1. PLAYER PLAYS CARD
   ├─ Update meters (emotional state system)
   ├─ Apply immediate effects
   └─ Log to history

2. UPDATE NPC MEMORY
   ├─ Create memory entry with weight
   ├─ Update NPC personality (OCEAN evolution)
   ├─ Adjust trust/attraction levels
   └─ Check for relationship level-up

3. UPDATE ARC PROGRESS
   ├─ Advance arc phase if conditions met
   ├─ Check for decisive decision trigger
   └─ Update neglect tracking

4. CHECK CONSEQUENCES
   ├─ Short-term: Immediate reactions (same week)
   ├─ Medium-term: Follow-up cards (1-4 weeks)
   └─ Long-term: Persistent state changes

5. RECORD FOR ARCHIVE
   ├─ Add to season history
   ├─ Update relationship timeline
   ├─ Mark significant moments
   └─ Prepare for novel generation
```

### Example: Complete Decision Flow

**Week 32: Wedding Shoot Decision**

```
1. FORESHADOWING CARDS (Weeks 30-31)
   • Photographer friend mentions big wedding
   • Boss hints at important client weekend

2. DECISIVE CARD APPEARS (Week 32)
   • Phone buzzes twice
   • Must choose: Photography vs. Work
   • Time limit: 24 hours
   • Shows context: meters, money, relationships

3. PLAYER CHOOSES PHOTOGRAPHY

4. IMMEDIATE UPDATES
   Meters:
   • Social +2, Emotional +3
   • Money +$200
   
   Skills:
   • Photography +2
   
   NPCs:
   • Photographer friend: Trust +0.3, creates HIGH-WEIGHT memory
   • Boss: Trust -0.4, creates NEGATIVE memory
   • Sarah: Observing, creates memory about your courage

5. ARC PROGRESSION
   • Photography arc: Phase 3 → Phase 4
   • Corporate arc: Permanently limited
   • New cards unlock: "Client Bookings", "Equipment Upgrade"

6. CONSEQUENCE CARDS (Following weeks)
   Week 33: "Boss is cold at Monday meeting"
   Week 34: "Wedding photos turned out amazing"
   Week 35: "Missed the promotion cycle"

7. NPC PERSONALITY EVOLUTION
   Photographer Friend:
   • Conscientiousness +0.1 (respects reliability)
   • Friendship deepens → initiates more opportunities
   
   Boss:
   • Agreeableness toward you -0.2
   • Trust -0.4
   • Future interactions colored by disappointment
   
   Sarah:
   • Openness +0.1 (inspired by your courage)
   • Attraction +0.15 (respects following dreams)
   • New dialogue unlocked about her own dreams

8. ARCHIVE ENTRY
   {
     week: 32,
     decision: "wedding_shoot_vs_overtime",
     choice: "wedding_shoot",
     emotional_weight: 9,
     consequences_logged: true,
     npc_reactions: {
       photographer_friend: "grateful",
       boss: "disappointed",
       sarah: "inspired"
     },
     novel_chapter_marker: true
   }

9. LONG-TERM IMPACT
   • Photography becomes viable career path
   • Corporate ladder permanently harder
   • Created "Road Taken" memory (high emotional weight)
   • Influences Sarah's arc (she sees your courage)
   • Unlocks future decisive decision in Phase 5
```

---

## X. Novel Generation Process

### From Gameplay to Narrative

**Step 1: Data Collection (During Play)**
- Every card played logged
- Every decision recorded with context
- NPC memories and personality changes tracked
- Meter fluctuations recorded
- Emotional moments tagged

**Step 2: Narrative Extraction**
```javascript
const narrativeData = {
  character_arc: extractCharacterJourney(history),
  key_relationships: extractRelationshipStories(npcs),
  decisive_moments: extractDecisiveMoments(decisions),
  emotional_peaks: extractEmotionalPeaks(meter_history),
  thematic_threads: identifyThemes(story_arcs),
  npc_perspectives: extractNPCPerspectives(npc_memories)
};
```

**Step 3: Structure Generation**
```
ACT I (Weeks 1-20):
├─ Opening scene: First meeting with Sarah
├─ Introduction of photography passion
├─ Establishment of corporate life
└─ Seeds planted for future conflicts

ACT II (Weeks 21-60):
├─ Wedding shoot decision (climax of first half)
├─ Health breakdown crisis
├─ Sarah shares bookshop dream
├─ Building momentum toward major change
└─ Multiple threads escalating

ACT III (Weeks 61-78):
├─ Investment decision (giving up savings)
├─ Quitting corporate job
├─ Building bookshop together
├─ Grand opening
└─ Resolution: New beginning
```

**Step 4: Multi-POV Integration (Premium)**
```
Player POV (Majority of narrative):
First-person or close third-person
"You stand in the bookshop..."

Sarah POV (Key chapters):
Third-person, her internal thoughts
"She'd practiced this conversation fifty times..."

Marcus POV (1-2 chapters):
Third-person, observing player's journey
"He watched his friend work himself to exhaustion..."
```

**Step 5: Literary Enhancement**
- Sensory details added to key scenes
- Internal monologues for emotional depth
- Thematic symbolism (camera, blue scarf, bookshop lease)
- Dialogue polishing while preserving key quotes
- Pacing adjusted for dramatic tension
- Callbacks and foreshadowing woven in

**Step 6: Output Formatting**
```
FREE VERSION (3-5k words):
- Chapter structure (8-10 chapters)
- Major scenes only
- Single POV
- Basic formatting

PREMIUM VERSION (12-15k words per season):
- Expanded chapter structure (15-20 chapters)
- All significant scenes
- Multi-POV chapters
- Rich sensory details
- Professional formatting
- Export to PDF/ePub
```

---

## XI. Design Principles

### 1. Dramatic Structure First
Every season follows three-act structure with clear setup, conflict, and resolution. This ensures generated novels have proper pacing.

### 2. Consequences Matter
Decisions have short-term and long-term consequences that persist across seasons. This creates narrative continuity and weight.

### 3. Characters Are Real People
NPCs have consistent personalities that evolve believably. They remember, react, and have agency. This makes relationships feel authentic.

### 4. Memory Creates Meaning
High-weight memories become the emotional core of the story. These moments are what players and readers remember.

### 5. Player Agency Within Structure
Players have freedom within a structured framework. Arcs have multiple paths and outcomes, but all lead to compelling stories.

### 6. Neglect Has Consequences
Ignoring aspects of life creates drama. The game tracks what you're neglecting and makes you face it.

### 7. Stories Scale Naturally
One season = short story. Multiple seasons = novel. Full lifetime = series. Book generation scales with content.

### 8. No Forced Endings
Players choose when their character's story is complete. Each season can be an ending or a new beginning.

---

## XII. Player Experience Goals

**Players Should Feel:**
✅ Their choices genuinely matter
✅ NPCs are real, evolving individuals
✅ The story has dramatic structure and pacing
✅ Crises emerge naturally from their behavior
✅ Each season is a complete, satisfying arc
✅ Relationships require maintenance and effort
✅ The generated novel captures their unique story
✅ Emotional moments have weight and consequence
✅ They're creating a story worth reading

**Players Should Never Feel:**
✅ Choices are meaningless or cosmetic
✅ NPCs are robots following scripts
✅ Story is random or incoherent
✅ Crises are arbitrary or unfair
✅ Seasons end abruptly without resolution
✅ Relationships are guaranteed or automatic
✅ Generated books don't reflect their choices
✅ Emotional moments are forgotten
✅ It's just a pleasant life sim without stakes

---

## XIII. Summary

Unwritten's unified narrative structure creates **dramatic, personalized life stories** through:

**Season-Based Structure:**
- Each season = complete 3-act story (12-100 weeks)
- Multiple seasons = character's ongoing life
- Players choose when to end
- Natural book generation at each level

**Story Arcs:**
- Multi-phase arcs (8-30+ weeks)
- Decisive decision points with lasting consequences
- Crisis events emerging from player behavior
- Arcs interact and create conflicts

**Dynamic NPCs:**
- OCEAN personality model with believable evolution
- Three-tier memory system
- Trust and attraction systems
- Agency and contextual awareness

**Archive System:**
- Season archives preserve each chapter
- Lifetime archives compile full character story
- Everything carries forward between seasons
- Book generation scales from short story to novel

**Comprehensive Tracking:**
- Every decision logged for novel generation
- NPC perspectives captured for multi-POV
- Meter history tracks emotional journey
- Neglect system creates natural drama

**Result:** Every playthrough generates a unique, compelling story with genuine tension, meaningful relationships, and emotional payoff—a story worth reading as a novel.

The free book will be good. The premium novel will be **compelling** because the life was compelling.