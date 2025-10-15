# Unwritten: Character Creation System

## Philosophy

Start specific enough to feel real, but open enough to discover who you become. Character creation establishes your **starting point**, not your destination. The 10-minute process creates a foundation that evolves through thousands of choices.

---

## The Five-Stage Creation Flow

### Stage 1: Biographical Basics (2 minutes)

```
┌────────────────────────────────────────┐
│ WHO ARE YOU?                           │
├────────────────────────────────────────┤
│ Name: [Your Name]                      │
│                                        │
│ Starting Age: [18-65]                  │
│ ↳ Affects available options, energy   │
│   levels, cultural references          │
│                                        │
│ Starting Location:                     │
│ ○ Small Town (tight community)         │
│ ○ Suburban Area (balance)              │
│ ○ Major City (endless options)         │
│ ○ Rural Isolation (introspection)      │
│                                        │
│ Starting Financial Status:             │
│ ○ Struggling ($200, debt possible)     │
│ ○ Getting By ($2000, paycheck-to-paycheck)│
│ ○ Comfortable ($10k, some cushion)     │
│ ○ Well-Off ($50k, many options)        │
│                                        │
│ Living Situation:                      │
│ ○ Studio apartment (solo)              │
│ ○ Shared housing (roommates)           │
│ ○ Family home (dependent/supporting)   │
│ ○ Own place (independent)              │
└────────────────────────────────────────┘

Impact: These create your initial card pool,
available NPCs, and financial constraints.
```

#### System Effects

**Starting Age Impact:**
- **18-25:** High energy (8), more exploration cards, educational paths, unstable identity
- **26-35:** Medium energy (8), career establishment, relationship focus, identity forming
- **36-50:** Medium energy (7), peak achievement, complex responsibilities, established identity
- **51-65:** Lower energy (6), wisdom bonuses, mentorship roles, legacy focus

**Location Impact:**
```javascript
const LOCATION_EFFECTS = {
  small_town: {
    npc_pool: "20 base NPCs, tight-knit community",
    activities: "+50% community events, -30% career variety",
    social_pressure: "High visibility, strong expectations",
    cost_of_living: "Low ($800/mo rent)"
  },
  
  suburban: {
    npc_pool: "35 base NPCs, moderate connections",
    activities: "Balanced variety",
    social_pressure: "Moderate, some anonymity",
    cost_of_living: "Medium ($1500/mo rent)"
  },
  
  major_city: {
    npc_pool: "50 base NPCs, anonymous possibility",
    activities: "+80% career variety, +60% cultural options",
    social_pressure: "Low, complete anonymity possible",
    cost_of_living: "High ($2500/mo rent)"
  },
  
  rural: {
    npc_pool: "15 base NPCs, isolated",
    activities: "+70% nature/solo activities, -50% social",
    social_pressure: "Very low, deep solitude",
    cost_of_living: "Very low ($600/mo rent)"
  }
};
```

**Financial Status Impact:**
- Determines starting money
- Affects available housing options
- Gates certain activities (expensive hobbies, travel)
- Creates different stressors (debt vs. wealth management)

---

### Stage 2: Personality Foundation (3 minutes)

Rather than asking players to self-report personality traits, use **scenario-based questions** that reveal OCEAN traits naturally.

```
┌────────────────────────────────────────┐
│ HOW DO YOU APPROACH LIFE?              │
│ (Choose scenarios that feel natural)   │
├────────────────────────────────────────┤
│ Scenario 1: Friday Night              │
│                                        │
│ Your week was exhausting. You have     │
│ no plans. What sounds appealing?       │
│                                        │
│ A) Call friends for spontaneous        │
│    plans (Extraversion ↑)              │
│                                        │
│ B) Solo activity: book, game, art      │
│    (Introversion ↑)                    │
│                                        │
│ C) Something new and unexpected         │
│    (Openness ↑, Comfort risk)          │
│                                        │
│ D) Productive use of time (gym,        │
│    skill-building) (Conscientiousness ↑)│
│                                        │
│ E) Whatever requires least energy       │
│    (Neuroticism ↑, low Energy)         │
└────────────────────────────────────────┘
```

#### The 8 Scenario Questions

**Present 6-8 scenarios across:**

1. **Social Situations** (Extraversion)
   - Friday night plans
   - Party invitation when tired
   - Meeting new people at event

2. **Novel Experiences** (Openness)
   - Trying unfamiliar cuisine
   - Exploring new neighborhood
   - Unconventional art exhibit

3. **Planning vs Spontaneity** (Conscientiousness)
   - Weekend structure approach
   - Project deadline approach
   - Daily routine preference

4. **Conflict Handling** (Agreeableness)
   - Friend disagrees with you
   - Service error at restaurant
   - Group decision disagreement

5. **Stress Response** (Neuroticism)
   - Unexpected work crisis
   - Financial setback
   - Relationship tension

#### Scoring System

```javascript
function calculatePersonality(answers) {
  let traits = {
    openness: 3.0,
    conscientiousness: 3.0,
    extraversion: 3.0,
    agreeableness: 3.0,
    neuroticism: 3.0
  };
  
  answers.forEach(answer => {
    // Each answer adjusts 1-3 traits by ±0.3 to ±0.8
    traits[answer.primary_trait] += answer.adjustment;
    
    // Some answers affect multiple traits
    if (answer.secondary_traits) {
      answer.secondary_traits.forEach(secondary => {
        traits[secondary.trait] += secondary.adjustment;
      });
    }
  });
  
  // Clamp to 1.0-5.0 range
  Object.keys(traits).forEach(trait => {
    traits[trait] = Math.max(1.0, Math.min(5.0, traits[trait]));
  });
  
  return traits;
}
```

#### Result Display

```
┌────────────────────────────────────────┐
│ YOUR PERSONALITY BASELINE              │
├────────────────────────────────────────┤
│ Openness:           ████████░░ 4.2     │
│ Conscientiousness:  ██████░░░░ 3.1     │
│ Extraversion:       ████░░░░░░ 2.0     │
│ Agreeableness:      ███████░░░ 3.8     │
│ Neuroticism:        ██████████ 4.9     │
│                                        │
│ Your Starting Archetype:               │
│ "The Anxious Creative"                 │
│                                        │
│ This affects:                          │
│ • Which cards appear more often        │
│ • Success chances for comfort-zone     │
│   vs outside-comfort actions           │
│ • NPC attraction & compatibility       │
│ • Energy costs for different activities│
│ • Emotional states you experience      │
└────────────────────────────────────────┘
```

**Archetype Names** (generated from trait combination):
- High O + Low C: "The Free Spirit"
- High C + High N: "The Perfectionist"
- Low E + High O: "The Introspective Artist"
- High E + High A: "The Social Connector"
- High O + Low N: "The Confident Adventurer"

---

### Stage 3: Life Direction (3 minutes)

```
┌────────────────────────────────────────┐
│ WHAT MATTERS TO YOU RIGHT NOW?         │
│ (Choose your starting direction)       │
├────────────────────────────────────────┤
│ You don't have to know who you'll      │
│ become. But where do you want to       │
│ start?                                 │
│                                        │
│ 🎨 PURSUE CREATIVE FULFILLMENT         │
│    Express yourself, create art,       │
│    prioritize passion over practicality│
│    → Unlocks: Art, writing, music cards│
│                                        │
│ 💼 ACHIEVE FINANCIAL SECURITY          │
│    Build career, stability, wealth     │
│    Practical path, clear goals         │
│    → Unlocks: Career, investment cards │
│                                        │
│ ❤️  SEEK DEEP RELATIONSHIPS            │
│    Connection matters most             │
│    People over achievements            │
│    → Unlocks: Social, intimacy cards   │
│                                        │
│ 🌍 FIND PERSONAL FREEDOM               │
│    Independence, travel, exploration   │
│    Non-conformity, breaking rules      │
│    → Unlocks: Travel, adventure cards  │
│                                        │
│ 🏠 BUILD FAMILY LEGACY                 │
│    Domestic life, children, home       │
│    Generational impact                 │
│    → Unlocks: Family, home cards       │
│                                        │
│ 🎯 MASTER A CRAFT                      │
│    Obsessive skill development         │
│    Expertise over breadth              │
│    → Unlocks: Skill, training cards    │
│                                        │
│ 🌟 MAKE SOCIAL IMPACT                  │
│    Activism, service, change-making    │
│    Leave world better                  │
│    → Unlocks: Community, activism cards│
│                                        │
│ 🔍 DISCOVER WHO YOU ARE                │
│    Self-exploration, therapy, growth   │
│    Journey inward                      │
│    → Unlocks: Therapy, reflection cards│
│                                        │
│ ⚖️  BALANCE EVERYTHING                 │
│    Jack-of-all-trades                  │
│    No single obsession                 │
│    → Unlocks: Balanced card mix        │
│                                        │
│ NOTE: This is your STARTING direction. │
│ Life will test it. You can change it.  │
└────────────────────────────────────────┘
```

#### Life Direction Effects

```javascript
const LIFE_DIRECTION_EFFECTS = {
  pursue_creative_fulfillment: {
    card_pool_modifier: {
      creative_activities: "+40%",
      work_activities: "-20%",
      financial_activities: "-30%"
    },
    npc_types: [
      "Artists", "Musicians", "Writers", 
      "Gallery owners", "Creative mentors"
    ],
    starting_aspirations: [
      "Complete Your Portfolio",
      "Get Art Director Promotion",
      "Produce a Show",
      "Discover Your Artistic Voice",
      "Transition to Freelance"
    ],
    personality_compatibility: {
      best_fit: "High Openness",
      tension_with: "High Conscientiousness (structure vs freedom)"
    }
  },
  
  achieve_financial_security: {
    card_pool_modifier: {
      work_activities: "+40%",
      financial_activities: "+30%",
      creative_activities: "-20%"
    },
    npc_types: [
      "Colleagues", "Mentors", "Investors",
      "Business owners", "Career coaches"
    ],
    starting_aspirations: [
      "Get Promoted",
      "Save $50k Emergency Fund",
      "Start Side Business",
      "Achieve Financial Independence",
      "Master Industry Skill"
    ],
    personality_compatibility: {
      best_fit: "High Conscientiousness",
      tension_with: "High Openness (routine vs novelty)"
    }
  }
  
  // ... other directions follow same pattern
};
```

**Important:** Life Direction can **evolve** through gameplay:
- Major life events can shift priorities
- Season outcomes can change what matters
- Phase transitions often trigger direction reassessment

---

### Stage 4: Current Life Status (2 minutes)

```
┌────────────────────────────────────────┐
│ WHERE ARE YOU IN LIFE?                 │
├────────────────────────────────────────┤
│ Career Status:                         │
│ ○ Student/Entry-level (learning phase) │
│ ○ Established (steady income, routine) │
│ ○ Transitioning (between jobs/paths)   │
│ ○ Unemployed (seeking, struggling)     │
│ ○ Retired (new chapter, different pace)│
│                                        │
│ Relationship Status:                   │
│ ○ Single (open to possibility)         │
│ ○ Dating (exploring connections)       │
│ ○ Committed Relationship (established) │
│ ○ Married (long-term commitment)       │
│ ○ Complicated (separation, healing)    │
│                                        │
│ Health Status:                         │
│ ○ Excellent (high baseline energy)     │
│ ○ Good (normal energy)                 │
│ ○ Managing Condition (ongoing care)    │
│ ○ Recovering (limited energy)          │
│                                        │
│ Social Network:                        │
│ ○ Rich (many established friends)      │
│ ○ Moderate (a few close friends)       │
│ ○ Limited (building connections)       │
│ ○ Fresh Start (new city/phase)         │
└────────────────────────────────────────┘
```

#### Status Effects on Gameplay

**Career Status:**
```javascript
const CAREER_EFFECTS = {
  student_entry: {
    energy_max: 8,
    income: "$0-1500/mo",
    obligations: "Classes, homework",
    stress_baseline: 5,
    available_time: "High flexibility"
  },
  
  established: {
    energy_max: 7,
    income: "$3000-8000/mo",
    obligations: "40hr work week, meetings",
    stress_baseline: 6,
    available_time: "Structured (weekends free)"
  },
  
  transitioning: {
    energy_max: 6,
    income: "$0-2000/mo",
    obligations: "Job search, interviews",
    stress_baseline: 8,
    available_time: "High but stressful"
  },
  
  unemployed: {
    energy_max: 7,
    income: "$0",
    obligations: "Survival, job search",
    stress_baseline: 9,
    available_time: "High but desperate"
  },
  
  retired: {
    energy_max: 5,
    income: "$2000-4000/mo (fixed)",
    obligations: "Minimal",
    stress_baseline: 3,
    available_time: "Maximum freedom"
  }
};
```

**Health Status:**
```javascript
const HEALTH_EFFECTS = {
  excellent: {
    energy_max_modifier: +1,
    physical_meter_start: 8,
    crisis_chance: 0.02
  },
  
  good: {
    energy_max_modifier: 0,
    physical_meter_start: 7,
    crisis_chance: 0.05
  },
  
  managing_condition: {
    energy_max_modifier: -1,
    physical_meter_start: 5,
    crisis_chance: 0.10,
    new_cards_unlocked: ["Doctor visits", "Medication management", "Health tracking"]
  },
  
  recovering: {
    energy_max_modifier: -2,
    physical_meter_start: 4,
    crisis_chance: 0.15,
    recovery_arc_active: true
  }
};
```

**Social Network:**
```javascript
const SOCIAL_NETWORK_EFFECTS = {
  rich: {
    starting_npcs: 10,
    social_meter_start: 8,
    social_obligation_cards: "High (many people expect time)"
  },
  
  moderate: {
    starting_npcs: 5,
    social_meter_start: 6,
    social_obligation_cards: "Moderate (balanced)"
  },
  
  limited: {
    starting_npcs: 2,
    social_meter_start: 4,
    social_obligation_cards: "Low (more free time)"
  },
  
  fresh_start: {
    starting_npcs: 0,
    social_meter_start: 3,
    social_obligation_cards: "None (total freedom, but lonely)"
  }
};
```

---

### Stage 5: Initial Meters & Final Setup

```
┌────────────────────────────────────────┐
│ YOUR STARTING STATE                    │
├────────────────────────────────────────┤
│ PHYSICAL:   ███████░░░ 7               │
│ (Based on: age, health status)         │
│                                        │
│ MENTAL:     █████░░░░░ 5               │
│ (Based on: career status, neuroticism) │
│                                        │
│ SOCIAL:     ████░░░░░░ 4               │
│ (Based on: network, extraversion)      │
│                                        │
│ EMOTIONAL:  ██████░░░░ 6               │
│ (Based on: relationship status, goals) │
│                                        │
│ STARTING RESOURCES:                    │
│ Energy: 6/8 (refreshes daily)          │
│ Money: $2,000                          │
│ Time: Full week available              │
│                                        │
│ INITIAL DECK:                          │
│ • 20 base activity cards               │
│ • 5 NPCs in your network               │
│ • 3 locations you frequent             │
│ • Career/obligation cards              │
│ • Filtered by Life Direction           │
│                                        │
│ INITIAL EMOTIONAL STATE:               │
│ 🔵 CURIOUS (exploring new life)        │
│ 🟡 UNCERTAIN (don't know path yet)     │
│                                        │
│ [BEGIN YOUR LIFE] →                    │
└────────────────────────────────────────┘
```

#### Meter Calculation Algorithm

```javascript
function calculateInitialMeters(character) {
  const meters = {};
  
  // PHYSICAL
  meters.physical = 7; // Baseline
  if (character.age < 30) meters.physical += 1;
  if (character.age > 50) meters.physical -= 1;
  if (character.health === "excellent") meters.physical += 1;
  if (character.health === "managing" || character.health === "recovering") {
    meters.physical -= 2;
  }
  
  // MENTAL
  meters.mental = 6; // Baseline
  meters.mental -= character.personality.neuroticism / 2; // High neuroticism = lower mental
  if (character.career_status === "unemployed" || character.career_status === "transitioning") {
    meters.mental -= 2;
  }
  if (character.career_status === "retired") meters.mental += 1;
  
  // SOCIAL
  meters.social = 5; // Baseline
  meters.social += (character.personality.extraversion - 3.0); // Extraversion affects baseline
  if (character.social_network === "rich") meters.social += 2;
  if (character.social_network === "fresh_start") meters.social -= 3;
  
  // EMOTIONAL
  meters.emotional = 6; // Baseline
  if (character.relationship_status === "single") meters.emotional -= 1;
  if (character.relationship_status === "married") meters.emotional += 1;
  if (character.relationship_status === "complicated") meters.emotional -= 3;
  meters.emotional -= character.personality.neuroticism / 3;
  
  // Clamp all to 1-10 range
  Object.keys(meters).forEach(meter => {
    meters[meter] = Math.max(1, Math.min(10, Math.round(meters[meter])));
  });
  
  return meters;
}
```

---

## Character Creation Output (JSON)

```javascript
const STARTING_CHARACTER = {
  id: "uuid-12345",
  created_at: "2025-10-13T10:00:00Z",
  
  // STAGE 1: Biographical
  name: "Alex Chen",
  age: 28,
  location: "major_city",
  financial_status: "getting_by",
  living_situation: "studio_apartment",
  
  // STAGE 2: Personality (evolves over time)
  personality: {
    openness: 4.2,
    conscientiousness: 3.1,
    extraversion: 2.0,
    agreeableness: 3.8,
    neuroticism: 4.9
  },
  archetype: "The Anxious Creative",
  
  // STAGE 3: Direction
  life_direction: "pursue_creative_fulfillment",
  direction_confidence: 0.6, // Can decrease with challenges
  
  // STAGE 4: Current Status
  career_status: "established",
  career_type: "graphic_designer",
  relationship_status: "single",
  health_status: "good",
  social_network: "moderate",
  
  // STAGE 5: Initial State
  meters: {
    physical: 7,
    mental: 5,
    social: 4,
    emotional: 6
  },
  
  resources: {
    energy: 6,
    max_energy: 8,
    money: 2000,
    savings: 0
  },
  
  // EMOTIONAL STATE
  emotional_states: {
    primary: "CURIOUS",
    secondary: "UNCERTAIN",
    intensity: 0.6
  },
  
  // STARTING CONTENT
  deck: {
    activities: [
      "coffee_shop", "gym", "work", "design_projects",
      "museum_visit", "art_class", "park_walk", "reading",
      "cooking_experiment", "photography_hobby"
    ],
    npcs: [
      "sarah_barista", "marcus_best_friend", "boss", 
      "neighbor_friendly", "gym_regular"
    ],
    locations: [
      "apartment", "cafe_luna", "office", "park_nearby"
    ],
    skills: {
      design_basics: 3,
      communication: 2,
      cooking: 1
    },
    items: []
  },
  
  // TRACKING
  week: 1,
  season: 1,
  phase: "early_discovery",
  active_arcs: [],
  
  // HISTORY (starts empty, accumulates)
  history: {
    cards_played: [],
    decisions_made: [],
    relationships_formed: [],
    crises_survived: [],
    accomplishments: []
  },
  
  // NOVEL GENERATION CONTEXT (for future book generation)
  narrative_voice: {
    pov_style: "second_person", // Can change based on playstyle
    tone: "introspective_hopeful",
    themes: [], // Emerge through gameplay
    established_facts: [] // Accumulate as canonical truths
  }
};
```

---

## First Week Setup

After character creation, the game presents **Week 1 goals** during the first play session:

```
WEEK 1: YOUR FIRST SEASON BEGINS
┌────────────────────────────────────────┐
│ WELCOME TO YOUR LIFE                   │
├────────────────────────────────────────┤
│ This season lasts 12-20 weeks. You'll  │
│ choose goals that shape your journey.  │
│                                        │
│ Choose 1 MAJOR ASPIRATION:             │
│ (Spans 12+ weeks, defines season)      │
│                                        │
│ Based on your Life Direction           │
│ (Creative Fulfillment), these fit:     │
│                                        │
│ 🎨 COMPLETE YOUR PORTFOLIO             │
│    12 pieces, ready to showcase        │
│    Challenge: Discipline + skill       │
│    Duration: ~15 weeks                 │
│                                        │
│ 💼 GET PROMOTED TO ART DIRECTOR        │
│    Step up at current job              │
│    Challenge: Politics + performance   │
│    Duration: ~20 weeks                 │
│                                        │
│ 🎭 PRODUCE A SHOW (photography exhibit)│
│    Public display of your work         │
│    Challenge: Resources + networking   │
│    Duration: ~18 weeks                 │
│                                        │
│ 🌱 DISCOVER YOUR ARTISTIC VOICE        │
│    Experimentation and growth          │
│    Challenge: Self-doubt + exploration │
│    Duration: ~12 weeks                 │
│                                        │
│ ⚖️  ACHIEVE WORK-LIFE BALANCE          │
│    Stop burnout, find sustainability   │
│    Challenge: Boundaries + priorities  │
│    Duration: ~14 weeks                 │
│                                        │
│ [Choose One] →                         │
└────────────────────────────────────────┘

Then:

┌────────────────────────────────────────┐
│ Choose 1-2 MINOR ASPIRATIONS:          │
│ (4-8 weeks each, smaller scope)        │
│                                        │
│ 🏃 Build exercise habit (4 weeks)      │
│ 📚 Read 5 books (8 weeks)              │
│ 💬 Make 3 new friends (6 weeks)        │
│ 💰 Save $2000 emergency fund (8 weeks) │
│ 🧘 Start meditation practice (4 weeks) │
│ 🍳 Learn to cook 10 meals (6 weeks)    │
│                                        │
│ [Choose 1-2] →                         │
└────────────────────────────────────────┘
```

### Goal Generation Logic

```javascript
function generateInitialGoals(character) {
  const majorAspirations = [];
  const minorAspirations = [];
  
  // MAJOR ASPIRATIONS filtered by:
  // 1. Life Direction (60% weight)
  // 2. Personality fit (20% weight)
  // 3. Current life status (20% weight)
  
  if (character.life_direction === "pursue_creative_fulfillment") {
    majorAspirations.push(
      {
        id: "complete_portfolio",
        title: "Complete Your Portfolio",
        duration_weeks: 15,
        difficulty: "medium",
        personality_fit: checkFit(character, {openness: ">3.5"})
      },
      {
        id: "get_art_director_promotion",
        title: "Get Promoted to Art Director",
        duration_weeks: 20,
        difficulty: "hard",
        personality_fit: checkFit(character, {conscientiousness: ">3.5"})
      },
      {
        id: "produce_show",
        title: "Produce a Show",
        duration_weeks: 18,
        difficulty: "hard",
        personality_fit: checkFit(character, {extraversion: ">3.0"})
      },
      {
        id: "discover_artistic_voice",
        title: "Discover Your Artistic Voice",
        duration_weeks: 12,
        difficulty: "medium",
        personality_fit: checkFit(character, {openness: ">4.0"})
      },
      {
        id: "transition_to_freelance",
        title: "Transition to Freelance",
        duration_weeks: 16,
        difficulty: "hard",
        personality_fit: checkFit(character, {conscientiousness: ">3.0", neuroticism: "<4.0"})
      }
    );
  }
  
  // MINOR ASPIRATIONS available to everyone, but filtered by:
  // - Personality (introverts get fewer social goals)
  // - Status (can't "make new friends" if rich social network)
  // - Health (can't marathon if health status low)
  // - Finance (can't save if struggling)
  
  const minorPool = [
    {
      id: "exercise_habit",
      title: "Build Exercise Habit",
      duration_weeks: 4,
      requires: {physical: ">3", health: "good|excellent"}
    },
    {
      id: "read_5_books",
      title: "Read 5 Books",
      duration_weeks: 8,
      requires: {mental: ">3"}
    },
    {
      id: "make_friends",
      title: "Make 3 New Friends",
      duration_weeks: 6,
      requires: {social: "<7", extraversion: ">2.5"}
    },
    {
      id: "emergency_fund",
      title: "Save $2000 Emergency Fund",
      duration_weeks: 8,
      requires: {money: "<5000", financial_status: "!struggling"}
    },
    {
      id: "meditation",
      title: "Start Meditation Practice",
      duration_weeks: 4,
      requires: {emotional: "<7"}
    },
    {
      id: "learn_cooking",
      title: "Learn to Cook 10 Meals",
      duration_weeks: 6,
      requires: {physical: ">2"}
    }
  ];
  
  return {
    major: majorAspirations
      .filter(asp => asp.personality_fit > 0.5)
      .sort((a, b) => b.personality_fit - a.personality_fit)
      .slice(0, 5),
    
    minor: minorPool
      .filter(asp => meetsRequirements(character, asp.requires))
      .slice(0, 8)
  };
}
```

---

## Integration with Other Systems

**Character Creation feeds into:**

1. **Turn Structure** (`21-turn-structure.md`)
   - Initial energy levels
   - Starting hand composition
   - Available activities

2. **Emotional State System** (`19-emotional-state-system.md`)
   - Starting emotional states
   - Personality influences emotional tendencies
   - Baseline emotional reactivity

3. **AI Personality System** (`13-ai-personality-system.md`)
   - NPC compatibility calculations
   - Attraction and trust base values
   - Communication style matching

4. **Progression System** (`15-progression-phases.md`)
   - Starting phase (always "Early Discovery")
   - Initial season goals
   - Life direction influences

5. **Novel Generation** (`novel-generation-data-structure.md`)
   - Character voice profile established
   - Baseline personality for tracking evolution
   - Initial narrative themes

---

## Design Principles

### 1. Quick but Meaningful
10 minutes of choices creates 100+ hours of personalized gameplay.

### 2. Scenario-Based Not Self-Report
Players reveal personality through choices, not checkboxes.

### 3. Starting Point Not Destination
Everything can evolve. Nothing is locked forever.

### 4. Grounded in Consequences
Every choice has immediate gameplay effects.

### 5. Respect Player Time
No overwhelming detail. Get to gameplay fast.

---

## Technical Notes

### Storage Requirements
```javascript
{
  character_creation_data: "~2KB",
  includes: [
    "All biographical data",
    "Personality scores",
    "Initial state",
    "Starting deck composition"
  ]
}
```

### Performance Targets
```javascript
{
  character_creation_flow: "< 10 minutes",
  data_generation: "< 500ms",
  initial_deck_build: "< 1000ms",
  first_turn_ready: "< 2000ms"
}
```

---

## Summary

Character creation in Unwritten establishes:
- **Who you are** (biographical facts)
- **How you think** (personality baseline)
- **What matters** (life direction)
- **Where you're starting** (current life status)
- **Your initial tools** (deck, resources, meters)

From this foundation, your unique story unfolds through thousands of choices over dozens of seasons, creating a character that is **yours alone**.

The system balances **speed** (10 minutes) with **depth** (every choice matters), creating a personalized starting point for a lifetime of emergent storytelling.

