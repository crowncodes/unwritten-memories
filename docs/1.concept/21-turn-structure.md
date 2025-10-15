# Unwritten: Turn Structure & Gameplay Loops

## Overview

Unwritten operates on **nested time scales**, from individual card plays (30 seconds) to complete lifetimes (3000+ weeks). This document details the MICRO, MESO, and MACRO gameplay loops that create Unwritten's unique rhythm.

---

## Multi-Scale Time Architecture

```
MICRO (30sec-2min):    Individual card plays
         ↓
MESO (10-15min):       Day structure (morning/afternoon/evening)
         ↓
MACRO (45-60min):      Weekly cycles
         ↓
MEGA (8-12 hours):     Seasons (12/24/36 weeks - see 15-progression-phases.md)
         ↓
ULTRA (Multi-Season):  Character lifecycle (8-10 seasons per character)
```

---

## MICRO SCALE: Individual Turn (30 seconds - 2 minutes)

### The Basic Turn Loop

```
PLAYER'S TURN STRUCTURE:
┌────────────────────────────────────────┐
│ MONDAY, WEEK 3, 9:00 AM                │
│ Energy: 5/8 | Money: $1,847            │
│ 🔵 FEEL: MOTIVATED | 🟡 CURIOUS        │
├────────────────────────────────────────┤
│                                        │
│ YOUR HAND (6 cards drawn):             │
│                                        │
│ 1. ☕ Coffee at Café Luna              │
│    → 30 min, 1 energy, $6              │
│    → Social +1, chance to see Sarah    │
│                                        │
│ 2. 💼 Team Meeting (Obligation)        │
│    → 2 hours, 1 energy, $0             │
│    → Mental +1, career progress        │
│                                        │
│ 3. 🎨 Work on Portfolio Piece          │
│    → 3 hours, 2 energy, $0             │
│    → ASPIRATION PROGRESS: 3/12 pieces  │
│    → Motivated: -1 energy cost!        │
│                                        │
│ 4. 📞 Marcus: "Lunch today?"           │
│    → 1 hour, 1 energy, $15             │
│    → Social +2, strengthen friendship  │
│                                        │
│ 5. 🏃 Quick Gym Session                │
│    → 1 hour, 2 energy, $0              │
│    → Physical +2, Mental +1            │
│                                        │
│ 6. 💤 Take a Break                     │
│    → 1 hour, +1 energy (restore), $0   │
│    → Mental +1, stress relief          │
│                                        │
│ [Choose cards to play] →               │
│ [Or skip to next interesting moment] → │
└────────────────────────────────────────┘
```

### Card Selection & Resolution

```javascript
// TURN FLOW
1. Display current state
   ↓
2. Draw 6-8 cards (filtered by emotional state, time of day, obligations)
   ↓
3. Player selects card(s) to play
   ↓
4. Card resolution
   ↓
5. Update resources (energy, time, money)
   ↓
6. Update meters (physical, mental, social, emotional)
   ↓
7. Check for events/unlocks
   ↓
8. Redraw hand (if time/energy remaining)
   ↓
9. Repeat or advance to next phase
```

### Hand Composition Algorithm

```javascript
function drawHand(gameState) {
  const hand = [];
  const { emotional_states, time_of_day, energy, active_aspirations, obligations } = gameState;
  
  // 1. OBLIGATIONS (must appear if applicable)
  const obligationCards = getObligationCards(time_of_day);
  hand.push(...obligationCards);
  
  // 2. ASPIRATION-RELATED (1-2 cards)
  const aspirationCards = getAspirationCards(active_aspirations, emotional_states);
  hand.push(...aspirationCards.slice(0, 2));
  
  // 3. EMOTIONAL STATE FILTERED (2-3 cards)
  const emotionalCards = getEmotionallyFilteredCards(emotional_states, energy);
  hand.push(...emotionalCards.slice(0, 3));
  
  // 4. RANDOM OPPORTUNITIES (1-2 cards)
  const opportunityCards = getRandomCards(gameState);
  hand.push(...opportunityCards.slice(0, 2));
  
  // 5. RECOVERY OPTIONS (always available if low energy)
  if (energy < 3) {
    hand.push(getRestCards());
  }
  
  // Cap at 6-8 cards
  return hand.slice(0, 8);
}
```

### Emotional State Influence on Hand

From `19-emotional-state-system.md`, emotional states dynamically filter cards:

```javascript
const EMOTIONAL_FILTERS = {
  MOTIVATED: {
    boost_cards: ["aspiration_work", "skill_development", "challenging_tasks"],
    reduce_cards: ["relaxation", "escapism"],
    cost_modifier: {
      aspiration_related: -1 // energy
    }
  },
  
  OVERWHELMED: {
    boost_cards: ["rest", "simple_tasks", "comfort_activities"],
    reduce_cards: ["social_events", "challenging_tasks", "new_experiences"],
    cost_modifier: {
      social_high_energy: +1,
      work_tasks: +1
    }
  },
  
  ANXIOUS: {
    boost_cards: ["safe_routines", "familiar_activities", "solo_options"],
    reduce_cards: ["risky_choices", "social_performance", "new_people"],
    success_chance_modifier: {
      social_risky: -10, // percentage
      safe_routine: +5
    }
  },
  
  INSPIRED: {
    boost_cards: ["creative_activities", "new_experiences", "expression"],
    reduce_cards: ["routine_tasks", "mundane_work"],
    benefits: {
      creative_skill_gain: "+50%",
      unique_fusion_chance: "+20%"
    }
  },
  
  EXHAUSTED: {
    boost_cards: ["sleep", "rest", "low_energy_activities"],
    reduce_cards: ["high_energy_activities", "social_events"],
    cost_modifier: {
      all_activities: +1 // everything costs more
    }
  }
};
```

### Card Resolution Example

```javascript
async function resolveCard(card, gameState) {
  const resolution = {
    narrative: "",
    effects: {},
    unlocks: [],
    fusion_results: null
  };
  
  // 1. GENERATE NARRATIVE
  resolution.narrative = await AI.generateMicroNarrative({
    card: card,
    context: gameState,
    emotional_state: gameState.emotional_states,
    recent_history: gameState.recent_cards,
    relationships: gameState.relationships
  });
  
  // Example output:
  // "You sit at your usual spot by the window. Sarah brings your coffee 
  //  without asking—she remembers. 'You look tired,' she says. 'Long week?'"
  
  // 2. APPLY COSTS
  gameState.energy -= card.costs.energy;
  gameState.time += card.costs.time_minutes;
  gameState.money -= card.costs.money;
  
  // 3. APPLY EFFECTS
  Object.keys(card.effects).forEach(effect => {
    if (effect.type === "meter") {
      gameState.meters[effect.meter] += effect.delta;
    }
    if (effect.type === "relationship") {
      gameState.relationships[effect.target].bond += effect.delta;
    }
    if (effect.type === "skill") {
      gameState.skills[effect.skill] += effect.xp;
    }
  });
  
  // 4. CHECK FOR COMBINATIONS/FUSIONS
  if (card.combinable_with && gameState.active_cards.length > 0) {
    resolution.fusion_results = checkFusions(card, gameState.active_cards);
  }
  
  // 5. CHECK FOR EVENTS
  resolution.events = checkForTriggeredEvents(gameState);
  
  // 6. UPDATE EMOTIONAL STATE
  gameState.emotional_states = updateEmotionalState(
    gameState.emotional_states,
    card,
    resolution.effects
  );
  
  // 7. TRACK FOR NOVEL GENERATION
  trackGameplayEvent({
    week: gameState.week,
    day: gameState.day,
    time: gameState.time_of_day,
    card_played: card,
    narrative: resolution.narrative,
    effects: resolution.effects,
    emotional_state: gameState.emotional_states,
    meters: gameState.meters
  });
  
  return resolution;
}
```

### Turn Pacing: Adaptive Speed

```javascript
const PACING_MODES = {
  granular: {
    description: "Every card played individually",
    when: "Important days, decisive moments, crisis events",
    time_per_turn: "30-60 seconds"
  },
  
  batched: {
    description: "Group routine cards together",
    when: "Established routines, normal weekdays",
    time_per_turn: "10-15 seconds",
    example: "'Your morning routine takes you to 12pm. Energy: 5/8'"
  },
  
  summary: {
    description: "Skip unimportant time",
    when: "Nothing interesting happening",
    time_per_turn: "5 seconds",
    example: "'The week passes normally. Friday evening arrives.'"
  }
};
```

Player can choose pacing preference, but game suggests appropriate mode based on context.

---

## MESO SCALE: Day Structure (10-15 minutes gameplay)

### The Three-Part Day

```
DAY STRUCTURE (18 hours: 6am - 12am):
┌────────────────────────────────────────┐
│ MORNING (6am-12pm) - "THE PRODUCTIVE HOURS" │
├────────────────────────────────────────┤
│ Energy: HIGH (6-8)                     │
│ Hand Size: 6-8 cards                   │
│                                        │
│ Card Types Available:                  │
│ • Obligation cards (work, errands)     │
│ • Challenging tasks                    │
│ • Aspiration work                      │
│ • Exercise (peak efficiency)           │
│ • Planning/strategy activities         │
│                                        │
│ Emotional States More Common:          │
│ • MOTIVATED, FOCUSED, ENERGIZED        │
│                                        │
│ Best For:                              │
│ • Important decisions                  │
│ • High-energy activities               │
│ • Skill development                    │
│ • Career advancement                   │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ AFTERNOON (12pm-6pm) - "THE SOCIAL WINDOW" │
├────────────────────────────────────────┤
│ Energy: MODERATE (4-6)                 │
│ Hand Size: 6-8 cards                   │
│                                        │
│ Card Types Available:                  │
│ • Social activities                    │
│ • Errands and logistics                │
│ • Moderate work tasks                  │
│ • Aspiration progress                  │
│ • Hobby activities                     │
│                                        │
│ Emotional States More Common:          │
│ • BALANCED, SOCIAL, ENGAGED            │
│                                        │
│ Best For:                              │
│ • Meeting people                       │
│ • Collaborative work                   │
│ • Balanced activities                  │
│ • Exploring new options                │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ EVENING (6pm-12am) - "THE WIND DOWN"  │
├────────────────────────────────────────┤
│ Energy: LOW (2-4)                      │
│ Hand Size: 4-6 cards                   │
│                                        │
│ Card Types Available:                  │
│ • Relaxation activities                │
│ • Low-energy social (dates, hangouts) │
│ • Creative expression                  │
│ • Reflection/journaling                │
│ • Entertainment/escapism               │
│ • Sleep preparation                    │
│                                        │
│ Emotional States More Common:          │
│ • REFLECTIVE, PEACEFUL, CONTENT, TIRED │
│                                        │
│ Best For:                              │
│ • Relationship deepening               │
│ • Creative work (if inspired)          │
│ • Processing day's events              │
│ • Recovery and rest                    │
└────────────────────────────────────────┘

END OF DAY:
• Energy resets next morning
• Meters process overnight
• Day tracked for novel generation
• Preview tomorrow's obligations
```

### Adaptive Day Pacing

```javascript
function determineDayPacing(gameState) {
  const { player_preferences, active_arcs, emotional_state } = gameState;
  
  // ROUTINE-HEAVY PLAYERS: Batch morning/afternoon
  if (player_preferences.pacing === "fast" && !hasImportantEvents(gameState)) {
    return {
      mode: "batched",
      structure: [
        "Your routine took you to 6pm. What now?",
        "→ Show evening cards"
      ]
    };
  }
  
  // FREEFORM PLAYERS: Granular card-by-card
  if (player_preferences.pacing === "detailed") {
    return {
      mode: "granular",
      structure: [
        "Show each time period separately",
        "→ Player makes each card choice"
      ]
    };
  }
  
  // CRISIS/DECISION DAYS: Single major event dominates
  if (hasCrisisEvent(gameState) || hasDecisiveMoment(gameState)) {
    return {
      mode: "focused",
      structure: [
        "Your father is in the hospital.",
        "Nothing else matters today.",
        "→ Show only crisis-related cards"
      ]
    };
  }
  
  // ADAPTIVE (default): Mix based on content
  return {
    mode: "adaptive",
    structure: [
      "Routine morning → batch",
      "Important afternoon event → granular",
      "Free evening → player choice"
    ]
  };
}
```

### Day Types

```javascript
const DAY_TYPES = {
  routine_day: {
    frequency: "60% of days",
    structure: "Obligations + normal activities",
    pacing: "Can be batched",
    novel_generation: "Compressed into brief summary"
  },
  
  event_day: {
    frequency: "25% of days",
    structure: "Special event or opportunity",
    pacing: "Granular during event",
    novel_generation: "Full scene detail"
  },
  
  crisis_day: {
    frequency: "10% of days",
    structure: "Major problem or challenge",
    pacing: "Focused, minimal other activities",
    novel_generation: "Full chapter potential"
  },
  
  decisive_day: {
    frequency: "5% of days",
    structure: "Life-changing decision",
    pacing: "Very granular, time slows",
    novel_generation: "Key chapter, high emotional weight"
  }
};
```

### Day-End Processing

```javascript
function processDayEnd(gameState) {
  // 1. METER UPDATES
  gameState.meters = calculateOvernightMeterChanges(gameState.meters);
  
  // 2. ENERGY RESET
  gameState.energy = gameState.max_energy;
  
  // 3. OBLIGATIONS REFRESH
  gameState.obligations = getNextDayObligations(gameState);
  
  // 4. EMOTIONAL STATE EVOLUTION
  gameState.emotional_states = evolveEmotionalState(
    gameState.emotional_states,
    gameState.day_events
  );
  
  // 5. TRACK FOR CONTINUITY
  gameState.history.days.push({
    day: gameState.current_day,
    week: gameState.current_week,
    cards_played: gameState.today_cards,
    major_events: gameState.today_major_events,
    meter_changes: gameState.today_meter_changes,
    emotional_journey: gameState.today_emotional_arc
  });
  
  // 6. NOVEL GENERATION DATA
  if (gameState.today_major_events.length > 0) {
    createChapterDataPoint({
      type: "significant_day",
      day: gameState.current_day,
      week: gameState.current_week,
      events: gameState.today_major_events,
      emotional_weight: calculateEmotionalWeight(gameState.today_events),
      narrative_beats: extractNarrativeBeats(gameState.today_cards),
      character_state: snapshotCharacterState(gameState)
    });
  }
  
  // 7. CHECK FOR WARNINGS
  if (hasExtremeMeters(gameState.meters)) {
    queueWarningEvent(gameState);
  }
  
  return gameState;
}
```

---

## MACRO SCALE: Weekly Cycle (45-60 minutes gameplay)

### Week Structure

```
WEEK STRUCTURE:
┌────────────────────────────────────────┐
│ MONDAY-THURSDAY (ROUTINE DAYS)         │
│ 4 days, ~25-35 minutes gameplay        │
├────────────────────────────────────────┤
│ Pattern:                               │
│ • Obligation cards (work, bills, etc.) │
│ • Routine activity cards               │
│ • Quest chain progress cards           │
│ • Occasional NPC spontaneous events    │
│                                        │
│ Typical Flow:                          │
│ Mon-Wed: Routine + aspiration work     │
│ Thursday: Buildup to weekend           │
│                                        │
│ Player Experience:                     │
│ • Establishing rhythm                  │
│ • Making incremental progress          │
│ • Building toward weekend freedom      │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ FRIDAY (TRANSITION DAY)                │
│ 1 day, ~8-10 minutes gameplay          │
├────────────────────────────────────────┤
│ Pattern:                               │
│ • Morning: Last obligations            │
│ • Afternoon: Week wrapping up          │
│ • Evening: Social options ↑↑           │
│                                        │
│ Special:                               │
│ • Weekend invitations appear           │
│ • NPCs reach out with plans            │
│ • Preview weekend opportunities        │
│                                        │
│ Player Experience:                     │
│ • Relief (work week done)              │
│ • Anticipation (weekend ahead)         │
│ • Freedom approaching                  │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ SATURDAY-SUNDAY (EVENT DAYS)           │
│ 2 days, ~15-20 minutes gameplay        │
├────────────────────────────────────────┤
│ Pattern:                               │
│ • 2-4x more activity cards available   │
│ • Major NPC events (parties, trips)    │
│ • Special location unlocks             │
│ • Scheduled events (if any)            │
│ • Exploration opportunities            │
│ • High choice density                  │
│                                        │
│ Player Experience:                     │
│ • "What kind of weekend will this be?" │
│ • Major relationship moments           │
│ • Big aspiration pushes                │
│ • Or recovery/rest (player choice)     │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ END OF WEEK PROCESSING (2 minutes)     │
├────────────────────────────────────────┤
│ • Aspiration milestone check           │
│ • Meter review (warnings if extreme)   │
│ • Relationship updates                 │
│ • Financial summary (rent, income)     │
│ • Neglect tracking updates             │
│ • Skill progression display            │
│                                        │
│ → PREVIEW NEXT WEEK                    │
│ "Sarah invited you to dinner Friday"   │
│ "Work: Big presentation Thursday"      │
│ "Rent due: $1,200"                     │
└────────────────────────────────────────┘
```

### End-of-Week Processing

```javascript
function processWeekEnd(gameState) {
  const weekSummary = {
    week: gameState.current_week,
    season: gameState.current_season,
    summary: {}
  };
  
  // 1. ASPIRATION PROGRESS
  weekSummary.aspirations = gameState.active_aspirations.map(asp => {
    const progress = calculateProgress(asp, gameState.week_actions);
    return {
      name: asp.name,
      progress_pct: progress,
      on_track: progress >= asp.expected_progress_by_week[gameState.current_week],
      major_steps_completed: asp.milestones.filter(m => m.completed_this_week)
    };
  });
  
  // 2. METER REVIEW
  weekSummary.meters = {
    current: gameState.meters,
    trends: calculateMeterTrends(gameState.meters, gameState.history.last_4_weeks),
    warnings: []
  };
  
  if (gameState.meters.physical < 3) {
    weekSummary.meters.warnings.push({
      type: "physical_critical",
      message: "Your body is suffering. Rest or crisis imminent.",
      recommended_actions: ["Rest activities", "Reduce obligations", "Health focus"]
    });
  }
  
  if (gameState.meters.mental < 3) {
    weekSummary.meters.warnings.push({
      type: "mental_critical",
      message: "Burnout approaching. Your stress is unsustainable.",
      recommended_actions: ["Reduce workload", "Therapy", "Boundaries"]
    });
  }
  
  // 3. RELATIONSHIP UPDATES
  weekSummary.relationships = Object.entries(gameState.relationships).map(([npc, data]) => {
    const weekInteractions = countWeekInteractions(npc, gameState.week_cards);
    const bondChange = data.bond - data.bond_last_week;
    
    return {
      npc: npc,
      level: data.level,
      bond: data.bond,
      bond_change: bondChange,
      interactions_this_week: weekInteractions,
      status: weekInteractions === 0 ? "neglected" : bondChange > 0 ? "growing" : "stable",
      unlocks: data.new_unlocks_this_week
    };
  }).filter(r => r.interactions_this_week > 0 || r.bond_change !== 0);
  
  // 4. FINANCIAL SUMMARY
  weekSummary.financial = {
    starting_money: gameState.money_week_start,
    ending_money: gameState.money,
    income: gameState.week_income,
    expenses: gameState.week_expenses,
    major_transactions: gameState.week_major_transactions,
    upcoming_obligations: [
      gameState.rent_due_soon ? { type: "rent", amount: gameState.rent, due: "Week start" } : null,
      ...gameState.upcoming_bills
    ].filter(Boolean)
  };
  
  // 5. SKILL PROGRESSION
  weekSummary.skills = Object.entries(gameState.skills)
    .filter(([skill, data]) => data.xp_gained_this_week > 0)
    .map(([skill, data]) => ({
      skill: skill,
      level: data.level,
      xp_gained: data.xp_gained_this_week,
      leveled_up: data.leveled_up_this_week
    }));
  
  // 6. NEGLECT TRACKING
  weekSummary.neglect = {
    aspirations: gameState.active_aspirations.filter(a => 
      countProgressCards(a, gameState.week_cards) === 0
    ),
    relationships: Object.entries(gameState.relationships)
      .filter(([npc, data]) => 
        countWeekInteractions(npc, gameState.week_cards) === 0 && 
        data.level >= 2
      )
      .map(([npc, data]) => ({
        npc: npc,
        weeks_neglected: data.weeks_since_interaction,
        bond_decay: data.decay_per_week * data.weeks_since_interaction
      })),
    meters: Object.entries(gameState.meters)
      .filter(([meter, value]) => value < 4)
      .map(([meter, value]) => ({ meter, value, warning_level: value < 3 ? "critical" : "low" }))
  };
  
  // 7. PREVIEW NEXT WEEK
  weekSummary.next_week_preview = generateNextWeekPreview(gameState);
  
  // 8. NOVEL GENERATION: WEEK SUMMARY
  createNovelDataPoint({
    type: "week_summary",
    week: gameState.current_week,
    season: gameState.current_season,
    major_events: gameState.week_major_events,
    character_development: calculateCharacterDevelopment(gameState),
    relationship_moments: gameState.week_relationship_moments,
    emotional_arc: gameState.week_emotional_journey,
    narrative_significance: calculateNarrativeWeight(gameState.week_events)
  });
  
  return weekSummary;
}
```

### Next Week Preview

```javascript
function generateNextWeekPreview(gameState) {
  const preview = {
    obligations: [],
    opportunities: [],
    scheduled_events: [],
    warnings: []
  };
  
  // OBLIGATIONS (must do)
  if (gameState.rent_due_next_week) {
    preview.obligations.push({
      type: "financial",
      description: `Rent due: $${gameState.rent}`,
      impact: "Required payment"
    });
  }
  
  if (gameState.work_obligations_next_week.length > 0) {
    preview.obligations.push(...gameState.work_obligations_next_week);
  }
  
  // OPPORTUNITIES (special cards appearing)
  preview.opportunities = gameState.scheduled_opportunities_next_week;
  
  // SCHEDULED EVENTS (NPC invitations, etc.)
  preview.scheduled_events = gameState.npc_invitations.filter(inv => 
    inv.week === gameState.current_week + 1
  );
  
  // WARNINGS (things needing attention)
  if (gameState.aspirations.some(a => a.deadline_approaching)) {
    preview.warnings.push({
      type: "aspiration_deadline",
      message: "Major aspiration deadline approaching"
    });
  }
  
  return preview;
}
```

---

## Integration with Novel Generation

From `novel-generation-data-structure.md`, turn-level gameplay creates the raw material for literary chapters:

### Tracking for Chapter Generation

```javascript
const TURN_TO_NOVEL_MAPPING = {
  // Every card play creates a micro-narrative beat
  card_play: {
    tracked_data: {
      card: "What activity/who",
      context: "When, where, emotional state",
      narrative: "AI-generated micro-narrative (100-200 words)",
      effects: "Meter changes, relationship shifts",
      player_choice: "Why this card (inferred from context)",
      emotional_response: "How player character felt"
    },
    
    novel_use: "Becomes scene beats or compressed summary"
  },
  
  // Days with major events become scenes
  significant_day: {
    tracked_data: {
      major_event: "Crisis, decisive moment, breakthrough",
      full_narrative: "AI-generated scene (500-1000 words)",
      character_states: "Before/after emotional state",
      relationship_impacts: "How connections changed",
      life_impact: "Long-term consequences"
    },
    
    novel_use: "Full scene in chapter"
  },
  
  // Weeks become chapter building blocks
  week_summary: {
    tracked_data: {
      week_arc: "Emotional journey over 7 days",
      major_beats: "3-5 most important moments",
      character_development: "How character evolved",
      relationship_progression: "Key relationship moments",
      aspiration_progress: "Steps toward goals"
    },
    
    novel_use: "Chapter structure or compressed passage"
  },
  
  // Decisive moments become key chapters
  decisive_moment: {
    tracked_data: {
      full_scene_data: "Complete scene structure",
      before_state: "Character state entering moment",
      decision_context: "Options, pressures, stakes",
      decision_made: "What was chosen and why",
      after_state: "Character state after decision",
      consequences: "Immediate and long-term effects",
      symbolic_weight: "What this means for story"
    },
    
    novel_use: "Complete chapter with full dramatic weight"
  }
};
```

### Example: Turn → Novel Scene Mapping

```javascript
// GAMEPLAY: Card Play
const CARD_PLAY = {
  week: 28,
  day: "Tuesday",
  time: "afternoon",
  card: "coffee_meetup",
  characters: ["player", "sarah"],
  location: "cafe_luna",
  emotional_state: {
    player: "CURIOUS",
    sarah: "ANXIOUS"
  },
  
  micro_narrative: `
    You sit at your usual spot by the window. Sarah brings 
    your coffee without asking—she remembers. But something's 
    different today. Her hands tremble slightly as she sets 
    down the mug. She has a notebook with her, worn at the edges.
    
    'Can we talk?' she asks quietly. 'I want to show you something.'
  `,
  
  effects: {
    relationship_sarah: +0.05,
    unlocked_card: "sarah_business_plan_reveal"
  }
};

// NOVEL: Chapter Scene
const NOVEL_SCENE = {
  chapter: 8,
  scene: "cafe_invitation",
  
  prose: `
    The café smells like it always does—fresh coffee and vanilla 
    from the pastries. Your usual table by the window, afternoon 
    light going golden. Sarah brings your coffee without asking. 
    She remembers.
    
    But her hands shake when she sets it down. Just slightly. 
    You notice because you've learned to notice Sarah.
    
    She has a notebook with her. Worn leather, edges soft from 
    handling. You've never seen it before.
    
    'Can we talk?' Her voice is quieter than usual. Like she's 
    confessing something. 'I want to show you something. But you 
    have to promise to be honest.'
    
    The notebook sits between you like a question.
  `,
  
  emotional_weight: 8,
  narrative_function: "setup",
  foreshadowing: ["business_plan_reveal", "sarah_vulnerability", "bookshop_dream"]
};
```

---

## Resource Management Systems

### Energy System

```javascript
const ENERGY_SYSTEM = {
  daily_maximum: {
    base: 8,
    modifiers: [
      { source: "age", effect: "18-30: +0, 31-50: -1, 51+: -2" },
      { source: "health", effect: "excellent: +1, managing: -1, recovering: -2" },
      { source: "physical_meter", effect: "Each point below 5: -0.5" },
      { source: "emotional_exhausted", effect: "EXHAUSTED state: -1" }
    ]
  },
  
  recovery: {
    overnight: "Full restore to max",
    during_day: "Rest cards restore 1-2 energy",
    weekend_bonus: "+1 max energy Saturday/Sunday"
  },
  
  costs: {
    light_activity: 1,
    medium_activity: 2,
    heavy_activity: 3,
    emotional_modifier: "EXHAUSTED: +1 to all costs, ENERGIZED: -1 to physical"
  }
};
```

### Time System

```javascript
const TIME_SYSTEM = {
  day_structure: {
    total_hours: 18, // 6am - 12am
    morning: { hours: 6, high_value: true },
    afternoon: { hours: 6, medium_value: true },
    evening: { hours: 6, low_energy: true }
  },
  
  activity_costs: {
    quick: "30min",
    short: "1-2hrs",
    medium: "3-4hrs",
    long: "6+hrs"
  },
  
  time_pressure: {
    deadlines: "Aspiration deadlines create urgency",
    obligations: "Work/appointments consume time",
    opportunity_cost: "Choosing one activity excludes others"
  }
};
```

### Multi-Resource Card Costs

From `complete-game-flow.md`, cards have complex costs:

```javascript
const CARD_COST_STRUCTURE = {
  energy: "1-3 per activity",
  time: "Minutes/hours consumed",
  money: "Optional spending ($0-$500+)",
  social_capital: "For asking favors or using connections",
  comfort_zone: "Risky activities cost comfort points",
  emotional_cost: "High-stress activities drain emotional meter",
  success_chance: "Not all outcomes guaranteed (10%-95%)",
  
  example_cards: {
    coffee_meetup: {
      energy: 1,
      time: 30,
      money: 6,
      social_capital: 0,
      comfort_zone: 0,
      success_chance: 100
    },
    
    job_interview: {
      energy: 2,
      time: 120,
      money: 0,
      social_capital: 1, // Used connection to get it
      comfort_zone: 2, // Risky, uncomfortable
      success_chance: 45, // Based on skills + personality
      emotional_cost: "ANXIOUS state likely after"
    },
    
    ask_sarah_investment: {
      energy: 2,
      time: 180,
      money: 0,
      social_capital: 3, // Asking huge favor
      comfort_zone: 5, // Extremely uncomfortable
      success_chance: 65, // Based on relationship level
      emotional_cost: "High vulnerability",
      relationship_risk: "Could damage if refused"
    }
  }
};
```

---

## Design Principles

### 1. Nested Loops Create Rhythm
Short turns → Days → Weeks create natural play sessions and stopping points.

### 2. Adaptive Pacing Respects Player Time
Routine can be fast, important moments slow down.

### 3. Every Turn Tracked for Narrative
Even "routine" days contribute to character development story.

### 4. Emotional States Drive Experience
How you feel changes what you see and how hard things are.

### 5. Resources Create Meaningful Choices
Limited energy/time/money forces prioritization.

---

## Summary

Unwritten's turn structure operates on three primary scales:

**MICRO (30sec-2min):** Individual card plays with AI-generated micro-narratives, immediate resource management, and emotional state influence.

**MESO (10-15min):** Day structure with morning/afternoon/evening rhythm, adaptive pacing, and daily narrative tracking.

**MACRO (45-60min):** Weekly cycles with routine days, event days, and end-of-week processing that tracks progress toward goals.

All three scales feed into the novel generation system, with turn-level gameplay creating the raw narrative material that becomes literary fiction in the Archive system.

The system balances **player agency** (every turn is a choice) with **narrative coherence** (everything tracked for story), creating emergent gameplay that feels both playful and meaningful.

