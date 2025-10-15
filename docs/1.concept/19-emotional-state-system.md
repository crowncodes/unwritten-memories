# Unwritten: Emotional State & Turn Driver System

## Philosophy

Your character's emotional state isn't just a number—it's a **lens through which you experience life**. During each turn, your current emotional state automatically influences which cards appear, which choices feel appealing, and how activities unfold.

---

## How Emotional States Work

### Automatic State Detection

Every turn, the system analyzes your character's state and assigns 1-2 **Active Emotional States** that color your current experience:

```
TURN START ANALYSIS:
┌────────────────────────────────────────┐
│ MONDAY MORNING, WEEK 5                 │
├────────────────────────────────────────┤
│ Analyzing your current state...        │
│                                        │
│ Physical: 6/10 (Moderate)              │
│ Mental: 3/10 (Exhausted)               │
│ Social: 7/10 (Connected)               │
│ Emotional: 5/10 (Neutral)              │
│                                        │
│ Recent Events:                         │
│ • Worked late 3 nights this week       │
│ • Deadline pressure high               │
│ • Weekend plans cancelled              │
│                                        │
│ Personality Factors:                   │
│ • Neuroticism: 4.9 (High)              │
│ • Conscientiousness: 3.1 (Moderate)    │
│                                        │
│ ACTIVE EMOTIONAL STATES:               │
│ 🔵 OVERWHELMED (Primary)               │
│ 🟡 RESTLESS (Secondary)                │
│                                        │
│ These will influence your hand...      │
└────────────────────────────────────────┘
```

---

## Emotional State Categories

### The 20 Emotional States

**ENERGIZING STATES (Positive High-Energy)**
```
⚡ MOTIVATED
- Increases: Goal-oriented activities, productive tasks
- Decreases: Leisure activities, procrastination options
- Modifiers: +20% aspiration progress, -1 energy cost for work

✨ INSPIRED
- Increases: Creative activities, artistic pursuits
- Decreases: Routine obligations, administrative tasks
- Modifiers: +30% creative output, unlock spontaneous ideas

🎉 EXCITED
- Increases: Social events, new experiences, adventures
- Decreases: Solo activities, planning, reflection
- Modifiers: +2 Social from activities, risk tolerance +20%

🔥 CONFIDENT
- Increases: Challenging tasks, confrontations, bold choices
- Decreases: Safe options, avoidance behaviors
- Modifiers: +15% success chance, -anxiety from risks
```

**CALM STATES (Positive Low-Energy)**
```
😌 CONTENT
- Increases: Relaxation, maintenance, routine
- Decreases: Ambitious pursuits, dramatic changes
- Modifiers: Energy recovery +1, stress resistance +10%

🧘 PEACEFUL
- Increases: Meditation, nature, solitude
- Decreases: Intense activities, social pressure
- Modifiers: Mental +1 passive, clarity for decisions

💝 GRATEFUL
- Increases: Relationship deepening, giving back, reflection
- Decreases: Complaint, acquisition, self-focus
- Modifiers: +0.1 to all relationships, appreciation moments

🌱 REFLECTIVE
- Increases: Introspection, learning, therapy, journaling
- Decreases: Action-oriented, external focus
- Modifiers: Self-awareness +1, unlock insight cards
```

**ENERGIZING STATES (Negative High-Energy)**
```
😠 FRUSTRATED
- Increases: Venting, confrontation, change-seeking
- Decreases: Patience, diplomatic options
- Modifiers: Conflict chance +30%, dramatic choices appear

😰 ANXIOUS
- Increases: Preparation, overthinking, seeking reassurance
- Decreases: Risk-taking, spontaneity, new experiences
- Modifiers: -10% success on unfamiliar, +comfort-seeking

😤 RESTLESS
- Increases: Activity, exploration, novelty-seeking
- Decreases: Stillness, routine, patience
- Modifiers: Boredom resistance, +movement activities

🔥 PASSIONATE
- Increases: Intensity, commitment, all-in behaviors
- Decreases: Moderation, balance, careful consideration
- Modifiers: +2 to chosen focus, -1 to everything else
```

**WITHDRAWING STATES (Negative Low-Energy)**
```
😔 MELANCHOLY
- Increases: Solitude, contemplation, nostalgia
- Decreases: Social energy, optimism, new ventures
- Modifiers: -1 Social from activities, +depth in reflection

😞 DISCOURAGED
- Increases: Doubt, hesitation, safety-seeking
- Decreases: Ambition, risk-taking, confidence
- Modifiers: -15% success perception, comfort options appear

😐 NUMB
- Increases: Routine, autopilot, avoidance
- Decreases: Emotional engagement, meaningful choice
- Modifiers: -1 Emotional from all, +detachment

🥱 EXHAUSTED
- Increases: Rest, delegation, saying no
- Decreases: Energy-intensive options, obligations
- Modifiers: All activities +1 energy cost, recovery prioritized
```

**NEUTRAL STATES**
```
😊 CURIOUS
- Increases: Exploration, learning, questions
- Decreases: Assumptions, routines
- Modifiers: +unlock new options, +discovery bonuses

🎯 FOCUSED
- Increases: Concentration, goal pursuit, discipline
- Decreases: Distractions, social pulls
- Modifiers: +20% task efficiency, -interruptions

⚖️ BALANCED
- Increases: All options appear equally
- Decreases: Nothing specifically
- Modifiers: Neutral baseline (rare state)

🤔 UNCERTAIN
- Increases: Information-seeking, advice, exploration
- Decreases: Decisive action, commitment
- Modifiers: Decision cards more common, consequences visible
```

---

## State Determination Algorithm

```javascript
function determineEmotionalStates(character, recentEvents, currentContext) {
  let primaryState = null;
  let secondaryState = null;
  
  // STEP 1: Check meter thresholds (Crisis states)
  if (character.meters.mental < 3) {
    primaryState = "EXHAUSTED";
  } else if (character.meters.emotional < 3) {
    primaryState = "DISCOURAGED";
  } else if (character.meters.physical < 3) {
    primaryState = "DRAINED";
  }
  
  // STEP 2: Check recent events (Reactive states)
  if (!primaryState) {
    const recentPositive = recentEvents.filter(e => e.valence > 0.7);
    const recentNegative = recentEvents.filter(e => e.valence < -0.7);
    const recentStress = recentEvents.filter(e => e.stress_impact > 0.5);
    
    if (recentPositive.length >= 3) {
      primaryState = weightedChoice(["EXCITED", "CONFIDENT", "GRATEFUL"]);
    } else if (recentNegative.length >= 3) {
      primaryState = weightedChoice(["DISCOURAGED", "MELANCHOLY", "FRUSTRATED"]);
    } else if (recentStress.length >= 2) {
      primaryState = "OVERWHELMED";
    }
  }
  
  // STEP 3: Check aspiration progress (Goal-related states)
  if (!primaryState) {
    const aspirationProgress = character.current_aspiration.progress;
    const deadline = character.current_aspiration.deadline_proximity;
    
    if (aspirationProgress > 0.7 && deadline < 3) {
      primaryState = "MOTIVATED";
    } else if (aspirationProgress < 0.3 && deadline < 5) {
      primaryState = "ANXIOUS";
    } else if (aspirationProgress > 0.5) {
      primaryState = "CONFIDENT";
    }
  }
  
  // STEP 4: Personality-influenced baseline
  if (!primaryState) {
    if (character.personality.neuroticism > 4.0) {
      primaryState = weightedChoice(["ANXIOUS", "OVERWHELMED", "RESTLESS"]);
    } else if (character.personality.openness > 4.0) {
      primaryState = weightedChoice(["CURIOUS", "INSPIRED", "EXCITED"]);
    } else if (character.personality.conscientiousness > 4.0) {
      primaryState = weightedChoice(["MOTIVATED", "FOCUSED", "DISCIPLINED"]);
    } else {
      primaryState = "BALANCED";
    }
  }
  
  // STEP 5: Determine secondary state (complementary or contrasting)
  secondaryState = determineSecondaryState(primaryState, character);
  
  return {
    primary: primaryState,
    secondary: secondaryState,
    intensity: calculateIntensity(character.meters, recentEvents)
  };
}
```

---

## Turn Structure with Emotional States

### Enhanced Turn Flow

```
MONDAY MORNING, WEEK 5
┌────────────────────────────────────────┐
│ 🔵 YOU FEEL: OVERWHELMED              │
│ 🟡 AND ALSO: RESTLESS                 │
├────────────────────────────────────────┤
│ The weight of everything sits on your │
│ chest. Too much to do, not enough     │
│ time. You need to move, to DO         │
│ something, but everything feels like  │
│ too much.                              │
└────────────────────────────────────────┘

↓ EMOTIONAL STATES FILTER YOUR HAND ↓

HAND (6 cards drawn, filtered by states):
┌────────────────────────────────────────┐
│ 1. 💼 Team Meeting (Obligation)        │
│    [OVERWHELMED: This feels daunting]  │
│    → 2 hours, 2 energy (usually 1)    │
│    → Mental +1, but anxiety spike      │
│    Success chance: 60% (usually 85%)   │
│                                        │
│ 2. 🏃 Quick Run                        │
│    [RESTLESS: This calls to you]       │
│    → 30 min, 1 energy                 │
│    → Physical +2, clear your head      │
│    → Reduces OVERWHELMED intensity     │
│                                        │
│ 3. ☕ Coffee with Marcus                │
│    [OVERWHELMED: Could use support]    │
│    → 1 hour, 1 energy                 │
│    → Social +2, vent frustration       │
│    → May reduce stress if you open up  │
│                                        │
│ 4. 🎨 Work on Portfolio (Aspiration)   │
│    [OVERWHELMED: Too much pressure]    │
│    → 3 hours, 3 energy (usually 2)    │
│    → Creative progress, but draining   │
│    → Low completion quality likely     │
│                                        │
│ 5. 💤 Take Mental Health Break         │
│    [OVERWHELMED: This is what you need]│
│    → 2 hours, -1 energy (restore)     │
│    → Mental +2, reduce emotional states│
│    → May disappoint boss if skip work  │
│                                        │
│ 6. 📱 Scroll Phone Mindlessly          │
│    [RESTLESS: Easy distraction]        │
│    → 1 hour, 0 energy                 │
│    → Nothing gained, time lost         │
│    → Avoidance behavior                │
│                                        │
│ [Choose your cards] →                  │
└────────────────────────────────────────┘

EMOTIONAL STATE GUIDANCE:
┌────────────────────────────────────────┐
│ When OVERWHELMED:                      │
│ • High-demand activities cost more     │
│ • Success chances reduced              │
│ • Rest/support options emphasized      │
│ • Obligations feel harder              │
│                                        │
│ When RESTLESS:                         │
│ • Movement activities appealing        │
│ • Stillness options de-emphasized      │
│ • Change-seeking cards appear          │
│ • Avoidance temptations present        │
│                                        │
│ Managing Your State:                   │
│ → Choose cards that shift your state   │
│ → Or lean into the state productively  │
│ → States evolve based on your choices  │
└────────────────────────────────────────┘
```

---

## Card Filtering System

### How States Affect Your Hand

**Hand Composition Algorithm:**

```javascript
function drawHand(character, emotionalStates, availableCards) {
  const hand = [];
  const {primary, secondary} = emotionalStates;
  
  // OBLIGATIONS (Always appear, but modified)
  const obligations = getObligations(character.current_week);
  obligations.forEach(card => {
    card.emotional_modifier = applyStateModifiers(card, primary, secondary);
    hand.push(card);
  });
  
  // DRAW POOL ADJUSTMENT (based on emotional states)
  const drawPool = availableCards.filter(card => {
    const appealScore = calculateAppeal(card, primary, secondary, character);
    return appealScore > 0.3; // Only cards with some appeal
  });
  
  // Sort by appeal (high appeal cards more likely)
  const weightedPool = drawPool.map(card => ({
    card: card,
    weight: calculateAppeal(card, primary, secondary, character),
    emotional_context: getEmotionalContext(card, primary, secondary)
  }));
  
  // Draw remaining cards (weighted random)
  const remainingSlots = 6 - hand.length;
  for (let i = 0; i < remainingSlots; i++) {
    const drawn = weightedRandomDraw(weightedPool);
    drawn.emotional_context = formatContext(drawn);
    hand.push(drawn);
  }
  
  return hand;
}

function calculateAppeal(card, primaryState, secondaryState, character) {
  let appeal = 1.0; // Baseline
  
  // Primary state strongly influences appeal
  const primaryModifier = STATE_APPEAL_TABLE[primaryState][card.category];
  appeal *= primaryModifier; // 0.3 to 2.5 multiplier
  
  // Secondary state moderately influences
  if (secondaryState) {
    const secondaryModifier = STATE_APPEAL_TABLE[secondaryState][card.category];
    appeal *= (1.0 + (secondaryModifier - 1.0) * 0.5); // Half-strength
  }
  
  // Personality creates baseline preferences
  appeal *= getPersonalityAppeal(card, character.personality);
  
  // Recent choices influence (variety seeking)
  appeal *= getVarietyModifier(card, character.recent_cards);
  
  return Math.max(0.1, Math.min(3.0, appeal)); // Clamp between 0.1-3.0
}
```

---

## State Appeal Table

```javascript
const STATE_APPEAL_TABLE = {
  
  MOTIVATED: {
    work_tasks: 2.0,           // Very appealing
    aspiration_progress: 2.5,  // Highly appealing
    productive_activities: 1.8,
    social_casual: 0.7,        // Less appealing
    rest_activities: 0.3,      // Unappealing
    avoidance: 0.2             // Very unappealing
  },
  
  OVERWHELMED: {
    work_tasks: 0.4,           // Unappealing (but may be obligation)
    aspiration_progress: 0.3,  // Very unappealing
    high_demand: 0.2,          // Very unappealing
    support_seeking: 2.0,      // Very appealing
    rest_activities: 2.5,      // Highly appealing
    avoidance: 1.5,            // Moderately appealing (tempting)
    easy_social: 1.3           // Somewhat appealing (comfort)
  },
  
  ANXIOUS: {
    preparation: 2.0,          // Very appealing
    information_seeking: 1.8,  // Appealing
    reassurance: 1.7,          // Appealing
    risky_activities: 0.3,     // Very unappealing
    new_experiences: 0.5,      // Unappealing
    comfortable_routine: 1.6   // Appealing
  },
  
  INSPIRED: {
    creative_activities: 2.5,  // Highly appealing
    artistic_pursuits: 2.3,    // Very appealing
    novel_experiences: 1.7,    // Appealing
    routine_tasks: 0.4,        // Unappealing
    administrative: 0.3,       // Very unappealing
    spontaneous: 1.6           // Appealing
  },
  
  EXHAUSTED: {
    rest_activities: 2.8,      // Extremely appealing
    low_energy: 1.8,           // Appealing
    delegation: 1.6,           // Appealing
    high_energy: 0.2,          // Very unappealing
    demanding_social: 0.3,     // Very unappealing
    obligations: 0.4           // Unappealing (but may be required)
  },
  
  EXCITED: {
    social_events: 2.3,        // Very appealing
    new_experiences: 2.5,      // Highly appealing
    adventures: 2.2,           // Very appealing
    routine_tasks: 0.5,        // Unappealing
    solo_activities: 0.7,      // Less appealing
    planning: 0.6              // Less appealing
  },
  
  CURIOUS: {
    exploration: 2.2,          // Very appealing
    learning: 2.0,             // Very appealing
    questions: 1.8,            // Appealing
    new_npcs: 1.7,             // Appealing
    routine: 0.7,              // Less appealing
    familiar: 0.8              // Less appealing
  },
  
  RESTLESS: {
    movement: 2.0,             // Very appealing
    change: 1.8,               // Appealing
    activity: 1.7,             // Appealing
    novelty: 1.6,              // Appealing
    stillness: 0.3,            // Very unappealing
    routine: 0.4,              // Unappealing
    patience: 0.5              // Unappealing
  },
  
  DISCOURAGED: {
    comfort_seeking: 1.8,      // Appealing
    low_stakes: 1.6,           // Appealing
    support: 1.7,              // Appealing
    challenging: 0.4,          // Unappealing
    ambitious: 0.3,            // Very unappealing
    new_risks: 0.2             // Very unappealing
  },
  
  CONTENT: {
    maintenance: 1.8,          // Appealing
    routine: 1.6,              // Appealing
    relaxation: 1.7,           // Appealing
    appreciation: 1.5,         // Moderately appealing
    dramatic_change: 0.6,      // Less appealing
    ambitious_push: 0.7        // Less appealing
  }
  
  // ... (all 20 states have full tables)
};
```

---

## Emotional State Evolution

### States Change Based on Actions

```javascript
function updateEmotionalStates(currentStates, cardPlayed, outcome) {
  const {primary, secondary, intensity} = currentStates;
  
  // IMMEDIATE SHIFTS
  const immediateEffects = CARD_EMOTIONAL_EFFECTS[cardPlayed.id];
  
  // Example: Playing "Quick Run" while OVERWHELMED
  if (primary === "OVERWHELMED" && cardPlayed.category === "physical_activity") {
    return {
      primary: "RESTLESS", // Shift primary
      secondary: "MOTIVATED", // Energy channeled
      intensity: intensity * 0.7, // Reduce intensity
      reason: "Physical activity helped clear your head"
    };
  }
  
  // Example: Ignoring obligations while OVERWHELMED
  if (primary === "OVERWHELMED" && cardPlayed.category === "avoidance") {
    return {
      primary: "OVERWHELMED", // Persists
      secondary: "GUILTY", // New secondary emerges
      intensity: intensity * 1.2, // Intensifies
      reason: "Avoidance provided temporary relief but guilt builds"
    };
  }
  
  // GRADUAL DECAY
  // If you don't address a state, it may naturally fade or worsen
  if (cardsPlayedThisTurn === 0) {
    intensity *= 0.95; // Slight natural decay
  }
  
  // METER-DRIVEN SHIFTS
  // If meters change significantly, states may shift
  if (outcome.meters.mental < 2) {
    return {
      primary: "EXHAUSTED",
      secondary: primary, // Old state becomes secondary
      intensity: 0.9,
      reason: "Mental exhaustion overwhelming other feelings"
    };
  }
  
  return updatedStates;
}
```

---

## Example: Full Turn with Emotional States

```
═══════════════════════════════════════════
TUESDAY EVENING, WEEK 5, 7:00 PM
═══════════════════════════════════════════

YOUR CURRENT STATE:
┌────────────────────────────────────────┐
│ Physical: 6/10                         │
│ Mental: 4/10 (Stressed)                │
│ Social: 7/10                           │
│ Emotional: 5/10                        │
│                                        │
│ Active Aspiration:                     │
│ Complete Portfolio (7/12 pieces done)  │
│ Deadline: 5 weeks remaining            │
│                                        │
│ Recent Events:                         │
│ • This morning: Tense meeting with boss│
│ • Lunch: Supportive chat with Marcus   │
│ • Afternoon: Made progress on piece    │
└────────────────────────────────────────┘

↓ EMOTIONAL STATE ANALYSIS ↓

┌────────────────────────────────────────┐
│ 🔵 YOU FEEL: MOTIVATED (Primary)       │
│ 🟡 AND ALSO: ANXIOUS (Secondary)       │
├────────────────────────────────────────┤
│ You have momentum. That piece came     │
│ together today and you can feel the    │
│ portfolio taking shape. But there's    │
│ an edge of worry—the deadline isn't    │
│ far. You want to push forward, but     │
│ you're aware of the stakes.            │
└────────────────────────────────────────┘

YOUR HAND (6 cards, filtered by states):
┌────────────────────────────────────────┐
│ 1. 🎨 Work on Portfolio Piece #8       │
│    [MOTIVATED: You're in the zone]     │
│    → 3 hours, 2 energy                │
│    → Progress: +8% (higher than usual) │
│    → Quality boosted by motivation     │
│    → But may increase anxiety if stuck │
│                                        │
│ 2. 📞 Sarah: "Coffee tomorrow?"        │
│    [ANXIOUS: Should you take time off?]│
│    → Commit 1 hour tomorrow morning   │
│    → Social +2, relationship +0.1      │
│    → Guilt if you say yes? Or support? │
│                                        │
│ 3. 📚 Research: Study Other Portfolios │
│    [ANXIOUS: Prepare, reduce risk]     │
│    → 2 hours, 1 energy                │
│    → Confidence +1, reduce anxiety     │
│    → Learn best practices              │
│                                        │
│ 4. 💪 Quick Workout                    │
│    [MOTIVATED: Channel energy]         │
│    → 45 min, 1 energy                 │
│    → Physical +2, Mental +1           │
│    → Clear head for work later         │
│                                        │
│ 5. 📱 Scroll Social Media              │
│    [ANXIOUS: Procrastination tempting] │
│    → 1 hour, 0 energy                 │
│    → Temporary anxiety relief          │
│    → But time wasted, guilt follows    │
│                                        │
│ 6. 💤 Call It a Night Early            │
│    [ANXIOUS: Afraid of burnout]        │
│    → End turn, restore 2 energy       │
│    → Mental recovery                   │
│    → But less portfolio progress       │
│                                        │
│ [What do you do?] →                    │
└────────────────────────────────────────┘

PLAYER CHOICE: #1 (Work on Portfolio) + #4 (Quick Workout)

↓ RESOLUTION ↓

You choose to work out first:
┌────────────────────────────────────────┐
│ 💪 QUICK WORKOUT                       │
├────────────────────────────────────────┤
│ Thirty minutes into the run, the       │
│ tension in your shoulders starts to    │
│ release. By the end, your mind is      │
│ clearer. The anxiety about the         │
│ deadline is still there, but it feels  │
│ manageable now.                        │
│                                        │
│ Physical: 6 → 8                        │
│ Mental: 4 → 5                          │
│ Energy: 6 → 5                          │
│                                        │
│ EMOTIONAL STATE SHIFT:                 │
│ MOTIVATED → FOCUSED (Primary)          │
│ ANXIOUS → (Reduced, no longer secondary)│
└────────────────────────────────────────┘

Then portfolio work:
┌────────────────────────────────────────┐
│ 🎨 WORK ON PORTFOLIO PIECE #8          │
├────────────────────────────────────────┤
│ [FOCUSED + MOTIVATED: Optimal state]   │
│                                        │
│ You sit down and it flows. Three hours │
│ disappear. When you look up, piece #8  │
│ is complete. Actually complete. And    │
│ it's good. Better than good.           │
│                                        │
│ Portfolio Progress: 7/12 → 8/12        │
│ Mental: 5 → 4 (tired but satisfied)    │
│ Emotional: 5 → 7 (proud)               │
│ Energy: 5 → 3                          │
│                                        │
│ EMOTIONAL STATE SHIFT:                 │
│ FOCUSED → CONFIDENT (Primary)          │
│ (No secondary - clear emotional state) │
│                                        │
│ Fusion Card Unlocked:                  │
│ "In The Zone" - Can recreate this flow│
└────────────────────────────────────────┘

TURN END:
┌────────────────────────────────────────┐
│ 10:30 PM - You're tired but satisfied │
│                                        │
│ 🔵 YOU FEEL: CONFIDENT                 │
│ 💭 "I can do this. Five weeks. I got   │
│     this."                             │
│                                        │
│ Tomorrow morning starts with different │
│ emotional state and new possibilities. │
└────────────────────────────────────────┘
```

---

## Design Principles

### 1. Emotions Guide, Don't Force
Players always have choice, but emotions make some choices feel more natural.

### 2. States Are Dynamic
Your emotional state evolves throughout the day based on what you do.

### 3. Personality Influences States
High neuroticism = more negative states. High openness = more curious/inspired states.

### 4. States Create Authentic Challenge
Sometimes the "optimal" choice doesn't feel appealing because you're in the wrong emotional state.

### 5. Managing Emotions Is Part of Gameplay
Learning when to lean into a state vs. when to shift it is a skill.

---

## Technical Implementation

### Emotional State JSON

```json
{
  "turn_id": "week5_monday_morning",
  "emotional_states": {
    "primary": {
      "state": "OVERWHELMED",
      "intensity": 0.85,
      "duration_turns": 3,
      "triggers": [
        "mental_meter_low",
        "recent_stress_events",
        "deadline_pressure"
      ]
    },
    "secondary": {
      "state": "RESTLESS",
      "intensity": 0.6,
      "duration_turns": 2,
      "triggers": [
        "high_neuroticism",
        "lack_of_movement",
        "cabin_fever"
      ]
    }
  },
  
  "hand_modifications": {
    "obligations_modified": true,
    "draw_pool_filtered": true,
    "appeal_scores_applied": true,
    "emotional_context_added": true
  },
  
  "player_guidance": {
    "state_explanation": "The weight of everything sits on your chest...",
    "management_suggestions": [
      "Choose cards that shift your state",
      "Or lean into the state productively",
      "States evolve based on your choices"
    ]
  }
}
```

---

## Integration with Other Systems

### With Personality System
- Personality determines baseline emotional states
- High neuroticism → More negative states
- High openness → More curious/inspired states
- Conscientiousness → More motivated/focused states

### With Meter System
- Low meters trigger crisis emotional states
- High meters enable positive emotional states
- Meter extremes override other factors

### With Aspiration System
- Progress toward goals creates motivation
- Deadlines create anxiety
- Success creates confidence
- Failure creates discouragement

### With Relationship System
- Strong relationships provide emotional support
- Conflicts create negative emotional states
- Loneliness creates melancholy states
- New connections create excitement

---

## Player Experience Goals

**Players should:**
- Feel their character's emotional life is authentic
- Understand why certain cards appeal more
- Learn to manage emotional states strategically
- Experience the challenge of "not feeling like it"
- Appreciate when emotional states align with goals

**Players should feel:**
- Their character is alive, not just stats
- Emotional authenticity in decisions
- Challenge in self-management
- Reward for emotional intelligence
- Connection to character's inner life

