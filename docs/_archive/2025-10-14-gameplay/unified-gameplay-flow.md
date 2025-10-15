# Unwritten: Unified Gameplay Flow & Turn System

## Table of Contents
1. [Gameplay Philosophy](#gameplay-philosophy)
2. [Resource Management System](#resource-management-system)
3. [Turn Structure](#turn-structure)
4. [Emotional State-Driven Gameplay](#emotional-state-driven-gameplay)
5. [Season & Progression System](#season-progression-system)
6. [Time Management & Pacing](#time-management-pacing)
7. [Decision Weight System](#decision-weight-system)
8. [Flow Optimization](#flow-optimization)

---

## Gameplay Philosophy

### Core Principles

**Life Simulation, Not Optimization Puzzle**
- Emotional authenticity over mechanical efficiency
- Sometimes the "right" choice doesn't feel appealing
- Managing your emotional state IS gameplay
- Balance creates breakthrough, imbalance creates crisis

**Respect Both Playstyles**
- **Routine-builders:** Batch processing, automation, efficiency
- **Explorers:** Granular choices, variety, discovery
- Both are valid, both feel good

**Meaningful Scarcity**
- Limited time, energy, and emotional bandwidth
- Tradeoffs create interesting decisions
- You can't do everything—what matters most?

**Dynamic Difficulty Through State**
- Your emotional state affects what's appealing and possible
- Some days everything feels easy (MOTIVATED state)
- Other days everything feels hard (OVERWHELMED state)
- This mimics real life authentically

---

## Resource Management System

### The Six Resource Types

Every card and activity costs some combination of these resources:

#### 1. ⚡ ENERGY (Daily Pool)

**Regeneration Pattern:**
```
MORNING (6am-12pm):   3 Energy available
AFTERNOON (12pm-6pm): 3 Energy available
EVENING (6pm-12am):   2 Energy available
NIGHT (12am-6am):     0 Energy (sleep time)

WEEKEND BONUS:
Saturday/Sunday:      +1 Energy per phase
```

**Energy Costs:**
- **Low (1 Energy):** Coffee, reading, casual social, browsing
- **Medium (2-3 Energy):** Work projects, exercise, cooking, meaningful social
- **High (4+ Energy):** Intense work, crisis response, challenging social, risky activities

**Emotional State Modifiers:**
```javascript
if (state === "EXHAUSTED") {
  allEnergyCosts += 1; // Everything costs more
  maxEnergy *= 0.7;    // Less total available
}
if (state === "MOTIVATED") {
  workActivities.energyCost -= 1; // Work feels easier
}
if (state === "ANXIOUS") {
  socialActivities.energyCost += 1; // Social feels draining
}
```

**Zero Energy Consequences:**
- Can only play obligation cards (must do)
- Quality of work suffers (-20% success rates)
- Higher chance of mistakes/conflicts
- Emotional stat drops (-1 per turn at zero energy)
- May trigger EXHAUSTED emotional state

---

#### 2. ⏰ TIME (Weekly Budget)

**Time Allocation:**
```
TOTAL: 168 hours/week

FIXED OBLIGATIONS:
- Sleep: 56 hours (8hr/night)
- Work: 40-50 hours
- Essential tasks: 14 hours (meals, hygiene, commute)
SUBTOTAL: 110-120 hours

DISCRETIONARY TIME: 48-58 hours/week
This is YOUR time to allocate
```

**Time Costs:**
- **Micro (15-30 min):** Quick coffee, phone call, snack
- **Short (1-2 hours):** Meal, gym session, social meetup, hobby
- **Medium (3-4 hours):** Work project, event, activity cluster
- **Long (5+ hours):** Major event, day trip, intensive project

**Weekend Concentration:**
- ~32 of your 48 flexible hours are weekend
- Weekdays = mostly evenings (2-3 hours available)
- Weekends = full days (8-12 hours available per day)

**Parallel Activities:**
- Some activities can combine (podcast while commuting)
- Some must be exclusive (can't work and party simultaneously)
- Routines optimize time (batch similar activities)

---

#### 3. 💰 MONEY (Monthly Budget)

**Income Sources:**
```
CAREER DEPENDENT:
- Entry Level: $3,000-4,500/month
- Mid Career: $5,000-8,000/month
- Senior Level: $8,000-15,000/month
- Business Owner: $0-20,000/month (variable)

SIDE INCOME:
- Skills/freelance: $200-2,000/month
- Passive: $0-500/month
```

**Fixed Expenses (Auto-Deduct):**
```
MONTHLY BILLS:
- Rent/Mortgage: $1,200-2,500
- Utilities: $150-250
- Insurance: $200-400
- Debt Payments: $0-800
- Transportation: $150-400
- Food (base): $300-500
TOTAL: $2,000-4,850/month

DISCRETIONARY: Remaining after bills
```

**Activity Costs:**
- **Free:** Park, home activities, some social
- **Low ($5-20):** Coffee, fast food, movies, basic entertainment
- **Medium ($20-100):** Dinner out, event tickets, hobby supplies
- **High ($100-500):** Weekend trip, major purchase, luxury experience
- **Major ($500+):** Vacation, business investment, life changes

**Financial Crisis Triggers:**
- Savings < Rent cost = Crisis card imminent
- Missing bill payment = Credit impact, stress
- Debt > 40% income = Limited options appear
- Bankruptcy possible if mismanaged

---

#### 4. 🤝 SOCIAL CAPITAL (Relationship Currency)

**What It Represents:**
- Your ability to ask favors
- Goodwill in relationships
- Reciprocity balance
- Trust reservoir

**Earning Social Capital:**
```
ACTIONS THAT BUILD:
- Help friend move: +2 with that person
- Remember birthday: +0.5
- Show up when needed: +3
- Introduce friends: +1 each
- Support during crisis: +5

NATURAL REGENERATION:
+0.1 per week in established relationships
(Friendship maintenance through existence)
```

**Spending Social Capital:**
```
COSTS:
- Ask help moving: -2
- Borrow money: -4
- Cancel plans last minute: -3
- Need emotional support: -1
- Introduce to your friends: -1
- Ask professional favor: -3
```

**Zero Social Capital:**
- NPCs decline requests
- "Sorry, I'm busy" responses
- Relationship strain appears
- Must rebuild through giving first

**Negative Social Capital:**
- Relationship at risk
- Confrontation cards appear
- May lose friendship if not repaired
- "We need to talk" events trigger

---

#### 5. 😰 COMFORT ZONE (Personality Stretch)

**What It Represents:**
- Emotional cost of going against personality
- Growth happens here, but it's draining
- Higher cost = more anxiety/discomfort

**Calculating Comfort Risk:**
```javascript
function calculateComfortRisk(card, personality) {
  let risk = 0;
  
  // OPENNESS CHECK
  if (card.category === "novel_experience") {
    if (personality.openness < 3.0) {
      risk += 2; // High discomfort
    }
  }
  
  // EXTRAVERSION CHECK
  if (card.category === "social_performance") {
    if (personality.extraversion < 3.0) {
      risk += 2; // High discomfort
    }
  }
  
  // NEUROTICISM CHECK
  if (card.category === "risky_uncertainty") {
    if (personality.neuroticism > 4.0) {
      risk += 3; // Extreme discomfort
    }
  }
  
  return risk; // 0-5 scale
}
```

**Comfort Risk Effects:**
```
RISK 0: No discomfort, natural fit
RISK 1: Slight stretch, manageable
RISK 2: Moderate discomfort, Energy +1
RISK 3: High discomfort, Energy +2, Emotional -1
RISK 4: Extreme discomfort, Energy +3, Emotional -2
RISK 5: Near-impossible, may fail even if attempted
```

**Growth Reward:**
- Successfully completing high comfort risk cards
- Personality shift toward that trait
- Example: Introvert does public speaking (Risk 4)
  - If success: Extraversion +0.3
  - Unlock: More confidence in similar situations
  - Memory: "I did the scary thing"

---

#### 6. 🎲 SUCCESS CHANCE (Probability-Based)

**Success Influenced By:**
1. **Personality Fit** (30% weight)
2. **Skill Level** (25% weight)
3. **Emotional State** (20% weight)
4. **Preparation** (15% weight)
5. **Random Chance** (10% weight)

**Success Formula:**
```javascript
function calculateSuccessChance(card, player) {
  let baseChance = card.base_difficulty; // 0.5 typical
  
  // PERSONALITY FIT
  const personalityMatch = getPersonalityMatch(card, player.personality);
  baseChance += personalityMatch * 0.3; // -0.3 to +0.3
  
  // SKILL LEVEL
  if (card.required_skill) {
    const skillLevel = player.skills[card.required_skill];
    baseChance += (skillLevel / 10) * 0.25; // 0 to +0.25
  }
  
  // EMOTIONAL STATE
  const stateModifier = getStateModifier(card, player.emotional_state);
  baseChance += stateModifier; // -0.2 to +0.2
  
  // PREPARATION
  if (card.preparation_cards_completed) {
    baseChance += 0.15; // Prepared = better odds
  }
  
  // CLAMP
  return Math.max(0.05, Math.min(0.95, baseChance));
}
```

**Outcome Distribution:**
```
SUCCESS (60%+): Good outcome, rewards as expected
PARTIAL SUCCESS (20-60%): Mixed results, some progress
FAILURE (5-20%): Setback, loss of resources
CRITICAL FAILURE (<5%): Disaster, major consequences
```

**Player Can Modify:**
- Preparation cards: +10-20% success
- Bring friend: +10-15% success
- Optimal emotional state: +10-20% success
- Skill training: +5% per level
- Choose easier variant: Guaranteed success but lower rewards

---

## Turn Structure

### Daily Turn Pattern

**Each Day = 3 Turns (Phases)**

```
═══════════════════════════════════════════
MONDAY, WEEK 5
═══════════════════════════════════════════

┌─ MORNING TURN (6am-12pm) ─────────────┐
│ Energy: ⚡⚡⚡ (3 available)            │
│ Time: 6 hours                          │
│                                        │
│ EMOTIONAL STATE ANALYSIS:              │
│ 🔵 OVERWHELMED (Primary)               │
│ 🟡 RESTLESS (Secondary)                │
│                                        │
│ HAND DRAWN (8 cards):                  │
│ 1. 💼 Team Meeting [OBLIGATION]        │
│ 2. 🏃 Quick Run [Appealing: RESTLESS]  │
│ 3. ☕ Coffee Routine [Comfort: ANXIOUS] │
│ 4. 💼 Work Project [Low Appeal: TIRED]  │
│ 5. 📞 Marcus Texts [Support: NEEDED]   │
│ 6. 🎨 Portfolio Work [Too Much: SKIP]  │
│ 7. 💤 Take Break [High Appeal: NEED]   │
│ 8. 📱 Scroll Phone [Avoidance: TEMPT]  │
│                                        │
│ Player chooses:                        │
│ • Coffee Routine (auto, 20min, 0 energy)│
│ • Team Meeting (required, 2hr, 2 energy)│
│ • Quick Run (chosen, 45min, 1 energy)  │
│                                        │
│ Resolution:                            │
│ • Physical +1, Mental +1               │
│ • State shifts: OVERWHELMED→RESTLESS   │
│ • Energy remaining: 0                  │
└────────────────────────────────────────┘

┌─ AFTERNOON TURN (12pm-6pm) ───────────┐
│ Energy: ⚡⚡⚡ (3 regenerated)          │
│ Time: 6 hours                          │
│                                        │
│ EMOTIONAL STATE UPDATED:               │
│ 🟢 RESTLESS (Primary - from morning)   │
│ 🟡 MOTIVATED (Secondary - run helped)  │
│                                        │
│ HAND DRAWN (8 cards):                  │
│ [New cards based on updated state]     │
│ More active/productive options appear  │
│                                        │
│ Player chooses afternoon activities... │
└────────────────────────────────────────┘

┌─ EVENING TURN (6pm-12am) ─────────────┐
│ Energy: ⚡⚡ (2 available, end of day)  │
│ Time: 6 hours                          │
│                                        │
│ EMOTIONAL STATE UPDATED:               │
│ 😊 CONTENT (Productive day complete)   │
│                                        │
│ HAND DRAWN (6 cards):                  │
│ [Evening-appropriate cards]            │
│ More social, leisure, rest options     │
│                                        │
│ Player chooses evening activities...   │
└────────────────────────────────────────┘

END OF DAY SUMMARY:
├─ Meters: Physical 7, Mental 5, Social 6, Emotional 6
├─ Energy spent: 8/8
├─ Time used: 14/18 hours
├─ Money spent: $32
├─ Tomorrow starts with: CONTENT state (likely)
└─ Aspiration progress: +5%
```

---

### Weekly Structure

**Week = 7 Days × 3 Turns = 21 Turn Opportunities**

```
WEEKDAY PATTERN (Monday-Friday):
├─ Morning: Routine-heavy (work obligations)
├─ Afternoon: Mix of work & discretionary
└─ Evening: Free time (2-3 hours available)

WEEKEND PATTERN (Saturday-Sunday):
├─ Morning: Full discretionary (4 energy)
├─ Afternoon: Full discretionary (4 energy)
└─ Evening: Social prime time (3 energy)
```

**Weekly Pacing:**
```
WEEK PHASES:

DAYS 1-2 (Mon-Tue): ROUTINE
• Establish rhythm
• Mostly obligations
• Build momentum
• 60% routine, 40% choice

DAYS 3-4 (Wed-Thu): PROGRESSION
• Aspiration focus
• Quest cards appear
• Mid-week choices
• 40% routine, 60% choice

DAY 5 (Friday): TRANSITION
• Week wrapping up
• Social invitations increase
• Weekend planning
• 30% routine, 70% choice

DAYS 6-7 (Sat-Sun): EVENT FOCUS
• Special events peak
• Long-form activities
• Relationship building
• 10% routine, 90% choice
• Most memorable moments
```

---

### Seasonal Structure (12-Week Arc)

**Season = Major Life Chapter**

```
═══════════════════════════════════════════
SEASON 3: "SARAH'S BOOKSHOP"
Weeks 1-12 (45 weeks actual)
═══════════════════════════════════════════

┌─ WEEK 1: SEASON INITIATION ───────────┐
│ Player chooses Major Aspiration:       │
│ "Open Bookshop with Sarah"             │
│                                        │
│ This decision affects:                 │
│ • Deck composition (business cards ↑)  │
│ • NPC interactions (Sarah featured)    │
│ • Quest chain generation (begins)      │
│ • Resource allocation (save money)     │
│                                        │
│ Starting state:                        │
│ • Money: $32,000 (need $50k total)     │
│ • Sarah relationship: 0.8              │
│ • Career: Corporate job (will quit)    │
│ • Emotional: Excited + Anxious mix     │
└────────────────────────────────────────┘

┌─ WEEKS 2-11: PROGRESSION PHASE ───────┐
│ QUEST CHAIN CARDS APPEAR:              │
│                                        │
│ Week 2-4: Planning & Research          │
│ • Business plan cards                  │
│ • Financial planning                   │
│ • Location scouting                    │
│                                        │
│ Week 5-7: Saving & Preparation         │
│ • Side income opportunities            │
│ • Expense cutting                      │
│ • Sarah deepening bond                 │
│                                        │
│ Week 8-9: DECISION POINT (Crisis)      │
│ • "Invest Life Savings?" card          │
│ • Major decision with consequences     │
│ • Emotional state: ANXIOUS peak        │
│                                        │
│ Week 10-11: Final Push                 │
│ • Quit job (if committed)              │
│ • Sign lease                           │
│ • Renovation work                      │
│ • Emotional: MOTIVATED + STRESSED      │
└────────────────────────────────────────┘

┌─ WEEK 12: SEASON CLIMAX ──────────────┐
│ MILESTONE CARD: "Opening Day"          │
│                                        │
│ This is the culmination of entire arc │
│                                        │
│ SUCCESS CHANCE: 75%                    │
│ (Based on 11 weeks of preparation)     │
│                                        │
│ OUTCOMES:                              │
│                                        │
│ SUCCESS (75%):                         │
│ • Bookshop opens successfully          │
│ • Sarah bond → MAX (1.0)               │
│ • Career identity: Entrepreneur        │
│ • Money: $8,000 left (depleted)        │
│ • FUSION: "The Bookshop Dream"         │
│ • Archive Memory: LEGENDARY            │
│ • Book Chapter: Triumphant ending      │
│                                        │
│ PARTIAL SUCCESS (20%):                 │
│ • Opens but struggles                  │
│ • Financial strain ongoing             │
│ • Relationship tested                  │
│ • Next season: "Survival Mode"         │
│                                        │
│ FAILURE (5%):                          │
│ • Deal falls through                   │
│ • Lost investment                      │
│ • Relationship damage with Sarah       │
│ • Crisis card triggers                 │
│ • Phase Transition forced              │
└────────────────────────────────────────┘

SEASON COMPLETE
↓
ARCHIVE GENERATED
↓
BOOK OFFER (3-5k free / 12-15k premium)
↓
CHOICE: Start Season 4 or End Lifetime
```

---

## Emotional State-Driven Gameplay

### State Detection System

**Every Turn Begins With State Analysis:**

```javascript
function determineEmotionalState(player, context) {
  // STEP 1: CRISIS OVERRIDE
  if (player.meters.mental < 3) return "EXHAUSTED";
  if (player.meters.emotional < 3) return "DISCOURAGED";
  if (player.meters.physical < 3) return "DRAINED";
  
  // STEP 2: RECENT EVENTS
  const recentPositive = context.recentEvents.filter(e => e.valence > 0.7);
  const recentNegative = context.recentEvents.filter(e => e.valence < -0.7);
  const recentStress = context.recentEvents.filter(e => e.stress > 0.5);
  
  if (recentPositive.length >= 3) return weightedChoice(["EXCITED", "CONFIDENT", "GRATEFUL"]);
  if (recentNegative.length >= 3) return weightedChoice(["DISCOURAGED", "MELANCHOLY", "FRUSTRATED"]);
  if (recentStress.length >= 2) return "OVERWHELMED";
  
  // STEP 3: ASPIRATION PROGRESS
  if (player.aspiration.progress > 0.7 && player.aspiration.deadline < 3) {
    return "MOTIVATED";
  }
  if (player.aspiration.progress < 0.3 && player.aspiration.deadline < 5) {
    return "ANXIOUS";
  }
  
  // STEP 4: PERSONALITY BASELINE
  if (player.personality.neuroticism > 4.0) {
    return weightedChoice(["ANXIOUS", "OVERWHELMED", "RESTLESS"]);
  }
  if (player.personality.openness > 4.0) {
    return weightedChoice(["CURIOUS", "INSPIRED", "EXCITED"]);
  }
  
  // STEP 5: DEFAULT
  return "CONTENT";
}
```

---

### The 20 Emotional States

**ENERGIZING POSITIVE:**
- ⚡ **MOTIVATED:** Goal-driven, productive, aspiration cards +200% appeal
- ✨ **INSPIRED:** Creative surge, artistic activities +250% appeal
- 🎉 **EXCITED:** Social energy peak, events +230% appeal
- 🔥 **CONFIDENT:** Challenge-ready, risk activities +180% appeal

**CALM POSITIVE:**
- 😌 **CONTENT:** Balanced state, routine comfortable, maintenance appeal
- 🧘 **PEACEFUL:** Meditative, solo activities +200% appeal, low stimulation preferred
- 💝 **GRATEFUL:** Relationship focus, giving back +180% appeal
- 🌱 **REFLECTIVE:** Introspection, learning +170% appeal, therapy/journaling

**ENERGIZING NEGATIVE:**
- 😠 **FRUSTRATED:** Venting needed, confrontation +150% appeal, change-seeking
- 😰 **ANXIOUS:** Preparation overdrive, risk activities -50% appeal, comfort +180%
- 😤 **RESTLESS:** Movement craving, novelty +160% appeal, stillness -70%
- 🔥 **PASSIONATE:** Intensity, all-in on focus area +200%, balance -50%

**WITHDRAWING NEGATIVE:**
- 😔 **MELANCHOLY:** Solitude preferred, social -50% appeal, contemplation +150%
- 😞 **DISCOURAGED:** Low confidence, challenges -60% appeal, comfort +170%
- 😐 **NUMB:** Autopilot mode, all activities -30% appeal, avoidance tempting
- 🥱 **EXHAUSTED:** Rest priority +280% appeal, demanding activities near-impossible

**NEUTRAL STATES:**
- 😊 **CURIOUS:** Exploration +220% appeal, routine -40% appeal
- 🎯 **FOCUSED:** Concentration peak, goal activities +200%, distractions -80%
- ⚖️ **BALANCED:** Rare optimal state, all cards equal appeal
- 🤔 **UNCERTAIN:** Decision paralysis, information-seeking +180%, commitment -40%

---

### State Affects Everything

**HAND COMPOSITION:**
```javascript
// OVERWHELMED Example
const hand_overwhelmed = {
  work_tasks: 0.4,        // Appear less (too much)
  rest_activities: 2.5,   // Appear much more (needed)
  support_seeking: 2.0,   // Social support cards increased
  avoidance: 1.5,         // Temptation cards (scrolling, etc)
  aspirations: 0.3        // Goal cards disappear (can't handle)
};

// MOTIVATED Example
const hand_motivated = {
  work_tasks: 2.0,        // Appear more (feel capable)
  aspirations: 2.5,       // Goal cards prominent
  rest_activities: 0.3,   // Rest cards disappear (don't need)
  social_casual: 0.7,     // Less social (focused on goals)
  challenges: 1.8         // Willing to take on more
};
```

**ENERGY COSTS:**
```javascript
if (state === "EXHAUSTED") {
  allActivities.energyCost += 1;
  maxEnergyPool *= 0.7;
}

if (state === "MOTIVATED") {
  aspirationActivities.energyCost -= 1;
  workActivities.energyCost -= 1;
}

if (state === "ANXIOUS") {
  socialActivities.energyCost += 1;
  riskActivities.energyCost += 2;
}
```

**SUCCESS CHANCES:**
```javascript
const stateModifiers = {
  CONFIDENT: { challenges: +0.15, performance: +0.20, risk: +0.10 },
  ANXIOUS: { challenges: -0.10, social: -0.05, risk: -0.20 },
  INSPIRED: { creative: +0.30, artistic: +0.25, novel: +0.15 },
  EXHAUSTED: { everything: -0.20, demanding: -0.40 },
  OVERWHELMED: { complex: -0.25, work: -0.15, decisions: -0.10 }
};
```

---

### State Transitions

**States Change Based on Actions:**

```javascript
// EXAMPLE: Morning Run While OVERWHELMED

BEFORE:
State: OVERWHELMED (Primary)
Meters: Mental 3, Physical 6, Emotional 4

ACTION: Quick Run
- Time: 45 minutes
- Energy: -2
- Physical: +1
- Mental: +1 (stress relief)
- Emotional: +1 (endorphins)

AFTER:
State: RESTLESS → MOTIVATED (Transition)
Meters: Mental 4, Physical 7, Emotional 5
Reasoning: "Physical activity channeled anxiety into productive energy"

GAMEPLAY EFFECT:
- Afternoon hand draws different cards
- More goal-oriented options appear
- Aspiration activities feel appealing again
- Player "turned the day around"
```

**State Persistence:**
```
TEMPORARY STATES (1-3 turns):
- Excited (after good news)
- Frustrated (after setback)
- Inspired (creative breakthrough)

PERSISTENT STATES (3-10 turns):
- Anxious (ongoing stress)
- Motivated (goal progress)
- Content (sustained balance)

CHRONIC STATES (10+ turns):
- Exhausted (burnout)
- Discouraged (repeated failure)
- Balanced (mastery achieved)
```

---

## Season & Progression System

### Life Phases (Multi-Season Framework)

```
═══════════════════════════════════════════
LIFETIME ARC: Alex Chen's Story
Age 28 → 47 (19 years)
═══════════════════════════════════════════

PHASE 1: EXPLORATION (Age 28-32)
Season 1-3 (52 weeks)
├─ "Finding My Footing" (18 weeks)
├─ "The Photography Spark" (22 weeks)
└─ "Sarah's Bookshop" (45 weeks)
Theme: Discovery, experimentation, taking risks
Life Direction: Shifting from security to fulfillment

PHASE 2: ESTABLISHMENT (Age 33-38)
Season 4-5 (66 weeks)
├─ "The Expansion" (38 weeks)
└─ "Sarah's Departure" (28 weeks)
Theme: Building, then rebuilding
Life Direction: Entrepreneurship, resilience

PHASE 3: MASTERY (Age 39-44)
Season 6-7 (73 weeks)
├─ "Rebuilding Solo" (31 weeks)
└─ "New Beginnings" (42 weeks)
Theme: Confidence, expertise, mentoring
Life Direction: Legacy building

PHASE 4: WISDOM (Age 45-47)
Season 8 (33 weeks, ongoing)
└─ "Teaching & Mentoring"
Theme: Giving back, reflection
Life Direction: Purpose beyond self
```

---

### Season Pacing Arc

**Every Season Follows 3-Act Structure:**

```
ACT I: SETUP (Weeks 1-4, 33%)
├─ Choose aspiration
├─ Meet/deepen characters
├─ Establish routine
├─ Plant seeds for conflict
└─ Low stakes, exploration

ACT II: CONFLICT (Weeks 5-9, 50%)
├─ Obstacles emerge
├─ Hard decisions required
├─ Relationships tested
├─ Resource scarcity
├─ Crisis cards possible
└─ High stakes, struggle

ACT III: RESOLUTION (Weeks 10-12, 17%)
├─ Climax event
├─ Major decision point
├─ Success or failure
├─ Consequences realized
├─ New equilibrium
└─ Highest stakes, catharsis
```

---

### Progression Metrics

**Per-Season Tracking:**
```json
{
  "season_3": {
    "weeks_played": 45,
    "turns_taken": 945,
    "cards_played": 3,234,
    "cards_evolved": 347,
    "fusions_created": 23,
    "relationships_changed": 8,
    "major_decisions": 12,
    "crisis_events": 2,
    "breakthrough_events": 1,
    
    "resource_tracking": {
      "total_money_earned": 156000,
      "total_money_spent": 148000,
      "net_worth_change": -24000,
      "total_energy_spent": 2834,
      "total_time_invested": 7560
    },
    
    "emotional_journey": {
      "dominant_states": ["MOTIVATED", "ANXIOUS", "EXCITED"],
      "crisis_states": ["OVERWHELMED", "EXHAUSTED"],
      "peak_moments": 8,
      "low_moments": 4,
      "overall_tone": "hopeful_struggle"
    },
    
    "outcome": {
      "aspiration_success": true,
      "climax_rating": 0.87,
      "satisfaction_score": 9.2,
      "would_replay": false,
      "archive_quality": "legendary"
    }
  }
}
```

---

## Time Management & Pacing

### Adaptive Flow System

The game respects different player preferences for pacing:

#### ROUTINE-HEAVY FLOW (High Conscientiousness)

```
MONDAY MORNING:
┌────────────────────────────────────────┐
│ YOUR ESTABLISHED ROUTINE               │
│                                        │
│ ☕ Coffee at Maya's (20min, auto)      │
│ 🚗 Commute (30min, auto)               │
│ 💼 Team Meeting (2hr, required)        │
│                                        │
│ Total: 2.8 hours, 2 energy             │
│                                        │
│ [✓ AUTO-RESOLVE ROUTINE]               │
│ [📋 Review Details If Desired]         │
│                                        │
│ → Fast-forward to 12pm                 │
│ → 3 Energy regenerated                 │
│ → Draw afternoon cards (interesting)   │
└────────────────────────────────────────┘

GAMEPLAY TIME: ~1 minute
STORY TIME: 6 hours

TUESDAY - THURSDAY:
┌────────────────────────────────────────┐
│ BATCH PROCESS WORK WEEK                │
│                                        │
│ Same routine × 3 days                  │
│ Any modifications desired?             │
│                                        │
│ [✓ Continue as planned]                │
│ [⚙️ Modify specific day]               │
│                                        │
│ → Fast-forward to Friday               │
└────────────────────────────────────────┘

GAMEPLAY TIME: ~30 seconds
STORY TIME: 3 days

RESULT:
- Entire work week: 3-5 minutes gameplay
- Skip to interesting decisions (weekend)
- Efficiency respected
- Routine = progress toward goals
```

---

#### FREEFORM FLOW (High Openness)

```
MONDAY MORNING:
┌────────────────────────────────────────┐
│ WHAT DO YOU FEEL LIKE DOING?           │
│                                        │
│ 10 CARDS DRAWN:                        │
│ 1. 🎨 Spontaneous Art Class ($45)      │
│ 2. ☕ Try New Coffee Shop              │
│ 3. 🏃 Impromptu Run in Park            │
│ 4. 💼 Work (flexible hours today)      │
│ 5. 📚 Start Interesting Book           │
│ 6. 🎵 Check Out That Band              │
│ 7. 🍳 Experiment with Cooking          │
│ 8. 👥 Text Random Friend               │
│ 9. 🧘 Try Meditation                   │
│ 10. 💤 Or Just Sleep In                │
│                                        │
│ Choose 2-3 for morning:                │
└────────────────────────────────────────┘

Player: "Art class + new coffee shop"
System: "That's 3.5 hours, you'll start work late"
Player: "Worth it"

GAMEPLAY TIME: ~2 minutes (choice rich)
STORY TIME: 3.5 hours

EVERY TURN: New choices
NO BATCH PROCESSING: Fresh decisions always
MORE GAMEPLAY: But more variety and discovery

PACING AID: "Focus Mode" Toggle
┌────────────────────────────────────────┐
│ [ALL] [INTERESTING ONLY]               │
│                                        │
│ "Interesting Only" Mode:               │
│ • Hides sleep, commute, meals          │
│ • Auto-resolves necessities            │
│ • Shows only: social, events, goals    │
│ • Speeds freeform by 40%               │
│                                        │
│ • You can toggle anytime               │
└────────────────────────────────────────┘
```

---

### Time Skip System

**Between Interesting Moments:**

```
┌────────────────────────────────────────┐
│ NOTHING SIGNIFICANT RIGHT NOW          │
│                                        │
│ Next meaningful moment in:             │
│                                        │
│ [⏩ 2 hours - Sarah texts]             │
│ [⏩⏩ 3 days - Weekend plans]           │
│ [⏩⏩⏩ 1 week - Aspiration milestone]   │
│                                        │
│ Auto-resolve routine in between:       │
│ • Work continues normally              │
│ • Meters adjust predictably            │
│ • Resources spent/earned               │
│ • No significant events missed         │
│                                        │
│ [⏩ SKIP TO NEXT MOMENT]               │
└────────────────────────────────────────┘

PLAYER CONTROL:
Always has agency to stop skip
Can review what was auto-resolved
No forced waiting
```

---

## Decision Weight System

### Four Decision Tiers

#### TIER 1: AUTO-RESOLVE (Trivial)
```
"Coffee at usual spot?"
"Go to work today?"
"Sleep tonight?"

ONE-CLICK: [Yes] [No]
DEFAULT: Yes (automatic if not changed)
TIME: 0-2 seconds
```

#### TIER 2: QUICK CHOICE (Minor)
```
"Sarah texts: Want to grab lunch?"

OPTIONS:
↑ Yes - Accept invitation
→ No - Decline politely
↓ Maybe later - Defer

TIME: 3-5 seconds
IMPACTS: Small, reversible
```

#### TIER 3: CONSIDERED CHOICE (Significant)
```
"Take this job offer?"
"Move in with partner?"
"Invest in friend's business?"

OPTIONS: 3-5 choices
IMPACTS: Medium-term consequences
TIME: 30-60 seconds
INFORMATION: Full context provided
```

#### TIER 4: LIFE-DEFINING (Major)
```
┌────────────────────────────────────────┐
│ 💍 MARRIAGE PROPOSAL                   │
│ Life-Defining Decision                 │
├────────────────────────────────────────┤
│ Alex proposed last night. You weren't  │
│ expecting this. Your mind races.       │
│                                        │
│ TIME PAUSES. No rush. Consider:       │
│                                        │
│ [📊 View Relationship History]         │
│ [💭 Review Life Goals]                 │
│ [💰 Check Financial State]             │
│ [⚖️ See Compatibility Analysis]        │
│                                        │
│ This affects next 52+ weeks            │
│ Changes Life Direction                 │
│ Creates new season arc                 │
│                                        │
│ [Take Time] [See More Info]            │
└────────────────────────────────────────┘

TIME: As long as needed
NO PRESSURE: Game waits for player
FULL INFORMATION: Everything accessible
CONSEQUENCES: Clearly explained
```

---

## Flow Optimization

### Preventing Slow Pace

**PROBLEM 1: Too Many Mundane Decisions**

SOLUTION: Smart Defaults + Batch Processing
```javascript
// Automatic decisions for established patterns
if (card.isRoutine && player.preferredChoice) {
  autoResolve(card, player.preferredChoice);
  return "Auto-resolved: Coffee at Maya's (+1 Energy, 20min, $6.50)";
}

// Batch similar cards
if (weekdayRoutine.established && player.confirmBatch) {
  batchResolve(weekdayRoutine, 5); // M-F
  return "Resolved: Standard work week → Friday afternoon";
}
```

**PROBLEM 2: Repetitive Goal Actions**

SOLUTION: Progress Bars + Automation
```
┌────────────────────────────────────────┐
│ MARATHON TRAINING (Week 5/12)          │
│                                        │
│ ROUTINE ESTABLISHED:                   │
│ • Training runs 4x/week                │
│ • Rest days 2x/week                    │
│ • Long run Saturday                    │
│                                        │
│ [✓ AUTO-CONTINUE THIS SCHEDULE]        │
│ [⚙️ MODIFY WEEK]                       │
│ [⏸️ PAUSE TRAINING]                    │
│                                        │
│ Auto-continues unless conflict arises: │
│ "Skip Saturday run? Marcus needs help" │
│ → Player chooses priority              │
└────────────────────────────────────────┘
```

**PROBLEM 3: Analysis Paralysis**

SOLUTION: Timer + Visual Simplification
```
MINOR DECISIONS: 10-second soft timer
- Not enforced, but creates gentle urgency
- "Trust your gut" moment
- Auto-default if timer expires (safe choice)

MAJOR DECISIONS: No timer
- Life-changing deserves reflection
- Full information available
- Visual impact preview
```

**PROBLEM 4: Too Much Text**

SOLUTION: Progressive Disclosure
```
CARD PRESENTATION:

GLANCE VIEW (Always visible):
┌────────────────────────────┐
│ 🎨 Gallery Opening          │
│ ⏰ 2hr | ⚡2 | 💰Free        │
│ Meet 2-4 artists            │
│ [DETAILS] [PLAY]            │
└────────────────────────────┘

EXPANDED VIEW (On click):
Full narrative, options, consequences

DETAIL VIEW (On deep dive):
Emotional state impact, success chances, relationships
```

---

## Summary

The Unified Gameplay Flow creates **authentic life simulation** through:

1. **Six Resource Types** creating meaningful scarcity and tradeoffs
2. **Three-Turn Daily Structure** respecting real-life rhythm
3. **Emotional State-Driven Gameplay** mimicking authentic decision-making
4. **12-Week Season Arcs** providing narrative structure and progression
5. **Adaptive Pacing** respecting both routine-builders and explorers
6. **Tiered Decision Weight** focusing attention on what matters
7. **Smart Automation** removing tedium without removing agency
8. **Time Management** that feels authentic not mechanical

**Result:** A game that feels like **living a life** rather than **playing a game**, where:
- Some days everything clicks (MOTIVATED state, high energy)
- Other days everything is hard (EXHAUSTED state, crisis mode)
- Your personality shapes what appeals to you
- Emotional states evolve based on your choices
- Balance creates breakthrough, imbalance creates crisis
- Every season tells a complete, emotionally resonant story

The system creates space for both **efficiency** (routine players) and **exploration** (variety seekers) while maintaining **emotional authenticity** through state-driven gameplay that mirrors real human experience.

