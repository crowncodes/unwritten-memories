# Daily Turn Flow - Detailed Implementation

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete moment-to-moment turn flow with emotional capacity, tension hooks, memory resonance, and dramatic irony integration

**References:**
- **Design Philosophy:** `1.concept/21-turn-structure.md` (WHY 3 turns/day)
- **Resource Economy:** `10-resource-economy-spec.md` + `11-turn-economy-implementation.md`
- **Emotional States:** `14-emotional-state-mechanics.md` (state determination)
- **Success Formulas:** `12-success-probability-formulas.md` (card resolution)

---

## Overview

Each day has **3 turns** (Morning/Afternoon/Evening) with **7-10 cards drawn per turn**. Players select cards to play based on available resources, then the system resolves outcomes and updates game state.

**Core Principle:** Turns should feel **meaningful but not overwhelming**. 30-120 seconds per turn, 3-8 minutes per day.

**Compliance:** master_truths v1.1 specifies "Turn: Three per day (Morning / Afternoon / Evening). 7 days per week."

---

## Turn Structure (High-Level)

```
TURN START
├─ 1. Context Update (state assessment)
├─ 2. Emotional State Determination
├─ 3. Hand Generation (draw 7-10 cards)
├─ 4. Player Action Phase (select & play cards)
├─ 5. Resolution Phase (process outcomes)
├─ 6. State Update (meters, resources, relationships)
└─ TURN END → Next Turn or Day End
```

**Average Time:** 30-120 seconds per turn

---

## Phase 1: Turn Start - Context Update

### System Assessment

```javascript
async function turnStart(gameState) {
  const turnContext = {
    // Basic info
    current_week: gameState.weekNumber,
    current_day: gameState.currentDay,           // "monday", "tuesday", etc.
    current_phase: gameState.currentPhase,       // "morning", "afternoon", "evening"
    turn_number: gameState.totalTurnCount,
    
    // Player state
    player: {
      meters: gameState.player.meters,           // Physical/Mental/Social/Emotional
      resources: gameState.player.resources,     // Energy/Time/Money/etc.
      location: gameState.player.currentLocation,
      aspiration: gameState.currentAspiration,
      active_arcs: gameState.activeNarrativeArcs
    },
    
    // Recent history
    recent_events: getRecentEvents(gameState, 7), // Last 7 turns
    yesterday_summary: getYesterday(gameState),
    week_progress: getWeekProgress(gameState)
  };
  
  return turnContext;
}
```

**Output:** Complete context object for state determination

---

## Phase 1b: Emotional Capacity Calculation *(NEW - Master Truths v1.2)*

### Calculate Emotional Capacity (0-10 scale)

**Core Principle:** Capacity determines ability to handle emotional complexity and provide/receive support.

```javascript
function calculateEmotionalCapacity(player, turnContext) {
  const { meters } = player;
  
  // BASE FORMULA: Weighted sum of 4 meters
  // Emotional (50%) + Mental (30%) + Physical (15%) + Social (5%)
  const baseCapacity = 
    (meters.emotional * 0.50) +
    (meters.mental * 0.30) +
    (meters.physical * 0.15) +
    (meters.social * 0.05);
  
  // CIRCUMSTANCE STACKING: Detect parallel stressors
  const activeStressors = detectActiveStressors(player, turnContext);
  const stackingPenalty = calculateStackingPenalty(activeStressors);
  
  // FINAL CAPACITY
  const finalCapacity = Math.max(0, baseCapacity - stackingPenalty);
  
  return {
    value: finalCapacity,
    tier: getCapacityTier(finalCapacity),
    base_capacity: baseCapacity,
    stacking_penalty: stackingPenalty,
    active_stressors: activeStressors,
    
    // Functional limits
    can_support_up_to: Math.max(0, finalCapacity - 2),  // Capacity - 2 rule
    can_handle_complexity: finalCapacity >= 5.0,
    needs_support: finalCapacity <= 4.0,
    crisis_state: finalCapacity <= 2.0
  };
}

function detectActiveStressors(player, turnContext) {
  const stressors = [];
  
  // WORK PRESSURE
  if (player.aspiratio && player.aspiration.stress_level > 6) {
    stressors.push({
      type: "work_overload",
      severity: player.aspiration.stress_level,
      penalty: 0.5
    });
  }
  
  // RELATIONSHIP CONFLICT
  const conflicted = player.relationships.filter(r => r.recent_conflict === true);
  if (conflicted.length > 0) {
    stressors.push({
      type: "relationship_tension",
      severity: conflicted.length,
      penalty: 0.3 * conflicted.length
    });
  }
  
  // FINANCIAL STRESS
  if (player.resources.money.current < 0 || player.resources.debt > 3000) {
    stressors.push({
      type: "financial_pressure",
      severity: Math.abs(player.resources.money.current) + player.resources.debt,
      penalty: 0.4
    });
  }
  
  // HEALTH CONCERNS
  if (player.meters.physical <= 3) {
    stressors.push({
      type: "physical_exhaustion",
      severity: 10 - player.meters.physical,
      penalty: 0.6
    });
  }
  
  // DEADLINE PRESSURE
  const upcomingDeadlines = countImminentDeadlines(player, turnContext);
  if (upcomingDeadlines >= 2) {
    stressors.push({
      type: "deadline_pressure",
      severity: upcomingDeadlines,
      penalty: 0.3 * Math.min(upcomingDeadlines, 3)
    });
  }
  
  return stressors;
}

function calculateStackingPenalty(stressors) {
  if (stressors.length === 0) return 0;
  if (stressors.length === 1) return stressors[0].penalty;
  
  // Multiple stressors compound
  // 2 stressors: sum penalties
  // 3+ stressors: sum + 10% amplification per additional stressor
  let totalPenalty = stressors.reduce((sum, s) => sum + s.penalty, 0);
  
  if (stressors.length >= 3) {
    const amplification = (stressors.length - 2) * 0.1;
    totalPenalty *= (1 + amplification);
  }
  
  // Cap at -3.0 (prevents going below 0 capacity in most cases)
  return Math.min(3.0, totalPenalty);
}

function getCapacityTier(capacity) {
  if (capacity >= 8.0) return "HIGH";
  if (capacity >= 6.0) return "MODERATE";
  if (capacity >= 4.0) return "LOW";
  if (capacity >= 2.0) return "VERY_LOW";
  return "CRISIS";
}
```

### Capacity Display in Turn Start

```
┌────────────────────────────────────────┐
│ MONDAY MORNING, WEEK 5                 │
├────────────────────────────────────────┤
│ Emotional Capacity: 4.85 / 10         │
│ [████████░░] LOW (declining)           │
│                                        │
│ ⚠️ Active Stressors (2):               │
│   • Work overload (high pressure)      │
│   • Financial pressure                 │
│                                        │
│ You can handle:                        │
│   ✓ Basic interactions                │
│   ✓ Simple decisions                   │
│   ✗ Complex emotional situations       │
│   ✗ Providing deep support to others   │
└────────────────────────────────────────┘
```

---

## Phase 2: Emotional State Determination

### Calculate Current Emotional State

```javascript
function determineEmotionalStates(turnContext) {
  const { player, recent_events } = turnContext;
  
  // 5-step priority system (from 14-emotional-state-mechanics.md)
  let primary = null;
  let secondary = null;
  
  // STEP 1: Crisis states (meter-driven)
  if (player.meters.mental <= 2 || player.meters.physical <= 2) {
    primary = "EXHAUSTED";
    intensity = 0.9;
  } else if (player.meters.emotional <= 2) {
    primary = "DISCOURAGED";
    intensity = 0.9;
  } else if (player.meters.mental <= 3 && countObligations(turnContext) > 5) {
    primary = "OVERWHELMED";
    intensity = 0.85;
  }
  
  // STEP 2-5: Reactive, aspiration-driven, personality baseline
  // (See 14-emotional-state-mechanics.md for complete algorithm)
  
  if (!primary) {
    primary = calculateBaselineEmotionalState(player, recent_events);
    intensity = 0.7;
  }
  
  secondary = determineSecondaryState(primary, player, intensity);
  
  return {
    primary,
    secondary,
    intensity,
    narrative: generateStateNarrative(primary, secondary, intensity),
    triggers: getStateTriggers(primary, player, recent_events)
  };
}
```

**Output:** Primary + secondary emotional states with narrative

**Display:**
```
┌────────────────────────────────────────┐
│ MONDAY MORNING, WEEK 5                 │
├────────────────────────────────────────┤
│ 🔵 YOU FEEL: OVERWHELMED              │
│ 🟡 AND ALSO: RESTLESS                 │
├────────────────────────────────────────┤
│ The weight of everything sits on your │
│ chest. Too much to do, not enough     │
│ time. You need to move, to DO         │
│ something, but everything feels like  │
│ too much.                              │
└────────────────────────────────────────┘
```

---

## Phase 3: Hand Generation

### Draw Cards for Current Turn

```javascript
function generateHand(turnContext, emotionalStates) {
  const hand = [];
  const { player, current_phase, current_day } = turnContext;
  const { primary, secondary } = emotionalStates;
  
  // 1. OBLIGATIONS (always appear if applicable)
  const obligations = getObligations(player, current_day, current_phase);
  obligations.forEach(card => {
    card.emotional_modifier = applyStateModifiers(card, primary, secondary);
    card.emotional_context = generateEmotionalContext(card, primary, secondary);
    hand.push(card);
  });
  
  // 2. ASPIRATION CARDS (if actively working on aspiration)
  if (player.aspiration && player.aspiration.active) {
    const aspirationCards = getAspirationCards(player.aspiration, current_phase);
    aspirationCards.forEach(card => {
      card.emotional_context = generateEmotionalContext(card, primary, secondary);
      hand.push(card);
    });
  }
  
  // 3. RELATIONSHIP CARDS (NPCs want to interact)
  const relationshipCards = getActiveNPCCards(player.relationships, current_phase);
  relationshipCards.forEach(card => {
    card.emotional_context = generateEmotionalContext(card, primary, secondary);
    hand.push(card);
  });
  
  // 4. FILL WITH FILTERED ACTIVITIES
  const availableCards = getAllAvailableCards(player);
  const filteredCards = filterByEmotionalAppeal(availableCards, primary, secondary, player);
  
  // Sort by appeal
  filteredCards.sort((a, b) => b.appeal - a.appeal);
  
  // Draw remaining slots (target 8-10 total)
  const remainingSlots = Math.max(0, 10 - hand.length);
  for (let i = 0; i < remainingSlots && i < filteredCards.length; i++) {
    const card = filteredCards[i];
    card.emotional_context = generateEmotionalContext(card, primary, secondary);
    hand.push(card);
  }
  
  // 5. SORT HAND (obligations first, then by priority)
  hand.sort((a, b) => {
    if (a.is_obligation && !b.is_obligation) return -1;
    if (!a.is_obligation && b.is_obligation) return 1;
    return b.priority - a.priority;
  });
  
  return hand;
}
```

**Hand Composition:**
```
Typical Morning Hand (8-10 cards):
├─ 2-3 Obligations ("Go to Work", "Morning Routine")
├─ 1-2 Aspiration cards ("Work on Portfolio")
├─ 2-3 Social cards ("Coffee with Sarah", "Text Marcus")
├─ 2-3 Activity cards ("Gym", "Read Book", "Errands")
└─ 0-1 Event cards ("Boss wants meeting", "New opportunity")
```

---

## Phase 3b: Capacity-Aware Hand Generation *(NEW - Master Truths v1.2)*

### Reduce Complexity When Capacity Low

**Core Principle:** When capacity < 4.0, limit hand size and complexity to prevent overwhelming player.

```javascript
function capacityAwareHandGeneration(baseHand, capacity, turnContext) {
  // CHECK CAPACITY TIER
  if (capacity.value >= 6.0) {
    // MODERATE/HIGH CAPACITY: Full hand, all options
    return {
      hand: baseHand,
      hand_size: baseHand.length,
      complexity_allowed: "full",
      note: null
    };
  }
  
  if (capacity.value >= 4.0 && capacity.value < 6.0) {
    // LOW CAPACITY: Slightly reduced complexity
    // Filter out "demanding" cards (high energy cost, complex decisions)
    const filtered = baseHand.filter(card => {
      if (card.is_obligation) return true;  // Always show obligations
      if (card.complexity_level > 7) return false;  // No high-complexity cards
      if (card.costs.energy > 2) return false;  // No high-energy cards
      return true;
    });
    
    // Limit hand size to 7-8 cards
    const limited = filtered.slice(0, 8);
    
    return {
      hand: limited,
      hand_size: limited.length,
      complexity_allowed: "reduced",
      note: "⚠️ Your low capacity limits available options today."
    };
  }
  
  if (capacity.value < 4.0) {
    // VERY LOW / CRISIS CAPACITY: Minimal hand
    // Only obligations + 1-2 simple recovery options
    const obligations = baseHand.filter(c => c.is_obligation);
    const recovery = baseHand.filter(c => 
      c.tags && c.tags.includes("recovery") && 
      c.complexity_level <= 3
    ).slice(0, 2);
    
    const minimal = [...obligations, ...recovery];
    
    return {
      hand: minimal,
      hand_size: minimal.length,
      complexity_allowed: "minimal",
      note: "⚠️ CAPACITY CRISIS: Only essential actions and recovery options available."
    };
  }
}
```

### Example: Capacity 4.85 (LOW) Hand Reduction

```
BEFORE capacity filtering (10 cards):
├─ [OBLIGATION] Go to Work (0 energy, 9h)
├─ Coffee with Sarah (1 energy, 1h)
├─ Work on Portfolio (3 energy, 3h) ← FILTERED (too demanding)
├─ Complex Client Meeting (2 energy, complexity 8) ← FILTERED (too complex)
├─ Quick Run (1 energy, 30min)
├─ Read Book (1 energy, 1h)
├─ Text Marcus (0 energy, 10min)
├─ Difficult Decision: Career Choice ← FILTERED (too complex)
├─ Gym Session (2 energy, 2h) ← FILTERED (too demanding)
└─ Meditation (1 energy, 20min)

AFTER capacity filtering (7 cards):
├─ [OBLIGATION] Go to Work (0 energy, 9h)
├─ Coffee with Sarah (1 energy, 1h)
├─ Quick Run (1 energy, 30min)
├─ Read Book (1 energy, 1h)
├─ Text Marcus (0 energy, 10min)
├─ Meditation (1 energy, 20min)
└─ [RECOVERY] Rest (1 energy, 2h)

⚠️ Your low capacity limits available options today.
   Focus on essentials and recovery.
```

---

## Phase 3c: Tension Hook Integration *(NEW - Master Truths v1.2)*

### Surface Tension Hooks in Relevant Moments

**Core Principle:** If a planted tension hook is relevant to current context, surface it via card dialogue/event.

```javascript
function integrateTensionHooks(hand, turnContext, activeHooks) {
  // Check for hooks that should surface this turn
  const relevantHooks = activeHooks.filter(hook => 
    isHookRelevant(hook, turnContext) &&
    hook.status === "planted" &&
    hook.next_surface_turn <= turnContext.turn_number
  );
  
  if (relevantHooks.length === 0) return hand;
  
  // INTEGRATE HOOKS INTO EXISTING CARDS
  hand.forEach(card => {
    relevantHooks.forEach(hook => {
      if (hookMatchesCard(hook, card)) {
        // Add hook narrative to card
        card.tension_hook = {
          hook_id: hook.hook_id,
          hook_type: hook.hook_type,
          narrative_hint: generateHookHint(hook, turnContext),
          tension_score: hook.tension_score,
          information_debt: hook.information_gaps
        };
        
        // Modify card dialogue to reference hook
        card.dialogue = enhanceDialogueWithHook(card.dialogue, hook);
        
        // Mark hook as surfaced
        hook.last_surface_turn = turnContext.turn_number;
        hook.surface_count++;
      }
    });
  });
  
  // OPTIONALLY: Create dedicated event card for hook
  const urgentHooks = relevantHooks.filter(h => h.weeks_active > 4);
  if (urgentHooks.length > 0) {
    urgentHooks.forEach(hook => {
      const eventCard = createHookEventCard(hook, turnContext);
      hand.unshift(eventCard);  // Add to beginning of hand
    });
  }
  
  return hand;
}

function generateHookHint(hook, turnContext) {
  // Example: "Sarah mentioned 'David' again, voice catching..."
  return {
    type: hook.hook_type,
    hint: hook.current_information_state,
    builds_tension: true,
    player_curious: true
  };
}
```

### Example: Sarah/David Mystery Hook Surfaces

```
CARD: Coffee with Sarah

WITHOUT HOOK:
┌────────────────────────────────────────┐
│ ☕ Coffee with Sarah                   │
│ ⚡ 1 Energy │ ⏰ 1 hour │ 💰 $8        │
│                                        │
│ You meet Sarah at Café Luna for       │
│ coffee. A chance to catch up and      │
│ connect.                               │
│                                        │
│ Social +2, Emotional +1                │
└────────────────────────────────────────┘

WITH HOOK (Week 3 of planting):
┌────────────────────────────────────────┐
│ ☕ Coffee with Sarah                   │
│ ⚡ 1 Energy │ ⏰ 1 hour │ 💰 $8        │
│                                        │
│ 🔍 MYSTERY: Sarah seems distracted    │
│                                        │
│ You meet Sarah at Café Luna. She's    │
│ quieter than usual, lost in thought.  │
│                                        │
│ At one point, she mentions "David"    │
│ again—just his name, then quickly     │
│ changes the subject. Her hands shake  │
│ slightly as she sips her coffee.      │
│                                        │
│ Who is David? Why does she get        │
│ emotional whenever his name comes up? │
│                                        │
│ Maybe this time you can ask...        │
│                                        │
│ Social +2, Emotional +1                │
│ May advance Sarah's relationship story │
└────────────────────────────────────────┘
```

---

## Phase 3d: Memory Resonance in Card Selection *(NEW - Master Truths v1.2)*

### Surface Relevant Memories During Hand Display

**Core Principle:** If current context triggers memory resonance (score ≥ 6.0), display memory echo alongside relevant card.

```javascript
function integrateMemoryResonance(hand, turnContext, memoryDatabase) {
  const { player, recent_events } = turnContext;
  
  // CHECK EACH CARD FOR MEMORY TRIGGERS
  hand.forEach(card => {
    // Get memories related to card context
    const relatedMemories = memoryDatabase.filter(m => 
      isMemoryRelatedToCard(m, card)
    );
    
    if (relatedMemories.length === 0) return;
    
    // Calculate resonance for each memory
    const resonanceScores = relatedMemories.map(memory => 
      calculateMemoryResonance(memory, turnContext, player)
    );
    
    // Find highest scoring memory
    const highestScore = Math.max(...resonanceScores.map(r => r.final_score));
    
    if (highestScore >= 6.0) {
      // MEMORY SURFACES
      const memory = relatedMemories[resonanceScores.findIndex(r => r.final_score === highestScore)];
      const resonance = resonanceScores.find(r => r.final_score === highestScore);
      
      card.memory_echo = {
        memory_id: memory.id,
        memory_content: memory.content,
        season_from: memory.season,
        emotional_weight: memory.emotional_weight,
        resonance_score: resonance.final_score,
        resonance_types: resonance.resonance_factors,
        narrative_integration: generateMemoryEcho(memory, card, resonance)
      };
    }
  });
  
  return hand;
}
```

### Example: Exhaustion Triggers S2 Collapse Memory

```
CARD: Work on Portfolio

CONTEXT:
- Physical meter: 3
- Mental meter: 3
- Capacity: 4.85 (LOW)
- Recent: 70-hour work week

MEMORY TRIGGERED:
- S2W14: Collapsed during wedding shoot
- Emotional weight: 10
- Resonance type: Past trauma trigger (0.95)
- Final score: 6.65 (SURFACES)

┌────────────────────────────────────────┐
│ 🎨 Work on Portfolio                   │
│ ⚡ 3 Energy │ ⏰ 3 hours               │
│                                        │
│ 💭 MEMORY ECHO (Season 2, Week 14):   │
│                                        │
│ Your hands ache. Your head pounds.    │
│ You've been pushing too hard.          │
│                                        │
│ A flash: fluorescent hospital lights. │
│ Marcus's face, pale with fear. "You   │
│ collapsed," he said. "You just...     │
│ fell."                                 │
│                                        │
│ That was six years ago. But your body │
│ remembers. Your hands shake slightly. │
│                                        │
│ Not again. You won't do that to       │
│ yourself again.                        │
│                                        │
│ ───────────────────────────────────── │
│                                        │
│ Push through and work on portfolio?   │
│ Or listen to your body this time?     │
│                                        │
│ Success: 35% (very low - exhausted)   │
│                                        │
│ [Play Card] [Skip] [Ask for Help]     │
└────────────────────────────────────────┘

PLAYER IMPACT:
- Memory echo influences decision
- "Ask for Help" option added (growth choice)
- Player more likely to prioritize recovery
```

---

## Phase 4: Player Action Phase

### Player Selects Cards to Play

```javascript
async function playerActionPhase(hand, player, turnContext) {
  let cardsSelected = [];
  let energyRemaining = player.resources.energy.current;
  let actionComplete = false;
  
  // Display hand to player
  displayHand(hand, emotionalStates);
  
  // Player selection loop
  while (!actionComplete) {
    const selection = await waitForPlayerInput();
    
    if (selection.type === "play_card") {
      const card = hand[selection.card_index];
      
      // Check if playable
      const canPlay = checkPlayability(card, player);
      
      if (!canPlay.playable) {
        showError(canPlay.blockers);
        continue;
      }
      
      // Preview outcomes
      if (selection.preview_requested) {
        showCardPreview(card, player);
        continue;
      }
      
      // Confirm costs
      const costConfirmation = await confirmCosts(card, player);
      if (!costConfirmation.confirmed) continue;
      
      // Add to selected
      cardsSelected.push(card);
      energyRemaining -= card.costs.energy;
      
      // Update hand state
      updateHandAfterSelection(hand, card, energyRemaining);
    }
    
    if (selection.type === "end_turn") {
      // Confirm end turn
      const confirmation = await confirmEndTurn(cardsSelected, energyRemaining);
      if (confirmation) actionComplete = true;
    }
    
    if (selection.type === "review_card") {
      // Show detailed card info
      showCardDetails(hand[selection.card_index], player);
    }
  }
  
  return cardsSelected;
}
```

**UI Flow:**
```
MORNING TURN - MONDAY, WEEK 5
┌────────────────────────────────────────┐
│ Energy: ⚡⚡⚡ (3/3)                    │
│ Time Left This Week: 28 hours          │
│ Money: $1,250                          │
└────────────────────────────────────────┘

YOUR HAND (8 cards):

1. [OBLIGATION] 💼 Go to Work
   ⚡ 0 Energy (auto-batched)
   ⏰ 9 hours
   [OVERWHELMING: This feels daunting today]
   
2. ☕ Coffee with Sarah
   ⚡ 1 Energy
   ⏰ 1 hour
   💰 $8
   [OVERWHELMED: Could use support]
   → Sarah (Level 3, Trust 0.62)
   
3. 🏃 Quick Run
   ⚡ 1 Energy
   ⏰ 30 min
   [RESTLESS: This calls to you]
   → May reduce OVERWHELMED
   
4. 🎨 Work on Portfolio
   ⚡ 3 Energy
   ⏰ 3 hours
   [OVERWHELMED: Too much pressure]
   → Success: 45% (low due to state)

[Select cards to play] [End Turn] [?] Help
```

---

## Phase 5: Resolution Phase

### Process Card Outcomes

```javascript
async function resolveCards(cardsSelected, player, turnContext) {
  const outcomes = [];
  
  for (const card of cardsSelected) {
    // 1. Deduct costs
    const costs = deductCosts(card, player);
    
    // 2. Calculate success (if applicable)
    let outcome;
    if (card.has_success_check) {
      const successChance = calculateSuccessChance(card, player);
      outcome = resolveSuccessCheck(successChance);
    } else {
      outcome = { result: "success" }; // Automatic success
    }
    
    // 3. Apply effects
    const effects = applyCardEffects(card, outcome, player);
    
    // 4. Generate narrative
    const narrative = generateNarrative(card, outcome, player, turnContext);
    
    // 5. Track event
    trackEvent({
      turn: turnContext.turn_number,
      card: card,
      outcome: outcome,
      effects: effects,
      emotional_weight: calculateEmotionalWeight(outcome, player)
    });
    
    // 6. Update relationships (if applicable)
    if (card.involves_npcs) {
      updateRelationships(card, outcome, player);
    }
    
    outcomes.push({
      card,
      outcome,
      effects,
      narrative
    });
  }
  
  return outcomes;
}
```

---

## Phase 5b: NPC Response Framework *(NEW - Master Truths v1.2)*

### Capacity-Constrained NPC Responses with OCEAN-Modified Failures

**Core Principle:** NPCs have capacity limits (capacity + 2 max support). HOW they handle those limits depends on their OCEAN personality. Some acknowledge limits authentically, others push beyond capacity and fail/become resentful/snap.

```javascript
function generateNPCResponse(card, player, npc, turnContext) {
  // 1. Calculate NPC's current capacity
  const npcCapacity = calculateNPCCapacity(npc, turnContext);
  
  // 2. Determine player's support need level
  const playerNeedLevel = determinePlayerNeedLevel(player, card);
  
  // 3. Check if NPC can meet need
  const npcCanSupport = npcCapacity.value + 2;  // Capacity - 2 rule
  const capacityMatch = npcCanSupport >= playerNeedLevel;
  
  // 4. Determine HOW NPC handles capacity mismatch (OCEAN-modified)
  if (capacityMatch) {
    // NPC CAN support
    return generateFullSupportResponse(npc, player, card, npcCapacity);
  } else {
    // NPC CANNOT fully support - personality determines response
    return generateCapacityMismatchResponse(npc, player, card, npcCapacity, playerNeedLevel);
  }
}

function generateCapacityMismatchResponse(npc, player, card, npcCapacity, playerNeedLevel) {
  const gap = playerNeedLevel - (npcCapacity.value + 2);
  
  // DECISION: Does NPC recognize their limitation?
  const recognizesLimit = checkSelfAwareness(npc, npcCapacity);
  
  if (recognizesLimit) {
    // AUTHENTIC LIMITATION RESPONSE (High Openness/Emotional Intelligence)
    return {
      response_type: "authentic_limitation",
      dialogue: generateAuthenticLimitationDialogue(npc, player, npcCapacity),
      effects: {
        player_emotional_meter: +1,  // Partial help
        player_capacity: +0.2,
        relationship_trust: -0.05,  // Minor strain (need unmet but honest)
        npc_capacity: npcCapacity.value - 0.4
      },
      limitation_acknowledged: true
    };
  } else {
    // NPC DOESN'T RECOGNIZE LIMIT - personality-driven failure
    return determineFailureResponse(npc, player, card, npcCapacity, gap);
  }
}

function determineFailureResponse(npc, player, card, npcCapacity, gap) {
  const { conscientiousness, agreeableness, neuroticism } = npc.ocean;
  
  // HIGH AGREEABLENESS: Tries to help anyway, becomes resentful/exhausted
  if (agreeableness >= 0.7 && conscientiousness >= 0.6) {
    return {
      response_type: "overextension_burnout",
      
      dialogue: `
        ${npc.name} tries to help. Really tries. But you can see the 
        strain in their face. They're pushing themselves beyond what 
        they can handle.
        
        Halfway through, they snap.
        
        "I'm sorry," they say, voice tight. "I can't. I just... I 
        can't do this right now. I need to go."
        
        They leave abruptly. You're left feeling worse than before.
      `,
      
      effects: {
        player_emotional_meter: -1,  // WORSE than before
        player_capacity: -0.3,  // Rejection hurts
        relationship_trust: -0.15,  // MODERATE HARM
        npc_capacity: npcCapacity.value - 1.5,  // SEVERE drain from failed attempt
        npc_resentment: +0.2  // NEW: Resentment builds
      },
      
      consequences: {
        immediate: "Player feels rejected, confused, hurt",
        npc_state: `${npc.name} feels guilty and resentful - tried to help, couldn't, now feels inadequate`,
        relationship_damage: "Tension for 1-2 weeks until addressed",
        recovery_required: true
      }
    };
  }
  
  // LOW AGREEABLENESS + LOW CAPACITY: Blunt/dismissive
  if (agreeableness <= 0.4 && npcCapacity.value <= 4.0) {
    return {
      response_type: "blunt_rejection",
      
      dialogue: `
        ${npc.name} cuts you off mid-sentence.
        
        "Look, I've got my own shit to deal with. I can't handle 
        your problems on top of mine right now."
        
        It's not malicious. Just... blunt. Too blunt. The words sting.
      `,
      
      effects: {
        player_emotional_meter: -2,  // Rejection hurts
        player_capacity: -0.5,  // Significant impact
        relationship_trust: -0.25,  // MAJOR HARM
        npc_capacity: npcCapacity.value - 0.2  // Minimal drain (didn't try)
      },
      
      consequences: {
        immediate: "Player feels dismissed, unimportant",
        npc_state: `${npc.name} prioritized self-preservation (correct choice) but delivered poorly`,
        relationship_damage: "Significant tension, may need formal apology",
        recovery_required: true,
        personality_consistent: true  // Low agreeableness = direct communication
      }
    };
  }
  
  // HIGH NEUROTICISM + LOW CAPACITY: Spirals, makes it about themselves
  if (neuroticism >= 0.7 && npcCapacity.value <= 4.5) {
    return {
      response_type: "anxious_spiral",
      
      dialogue: `
        ${npc.name} listens, but their breathing gets shallow.
        
        "God, I'm such a terrible friend," they say suddenly. "You're 
        going through this and I can't even... I'm barely keeping it 
        together myself and now you need me and I can't—"
        
        They're spiraling. You end up comforting THEM instead.
      `,
      
      effects: {
        player_emotional_meter: -1,  // No support received
        player_capacity: -0.4,  // Had to provide support instead
        relationship_trust: -0.12,  // Moderate strain
        npc_capacity: npcCapacity.value - 0.8,  // Spiral drains them more
        role_reversal: true  // Player ended up supporting NPC
      },
      
      consequences: {
        immediate: "Player didn't get support, provided it instead",
        npc_state: `${npc.name} feels guilty and inadequate`,
        relationship_pattern: "Establishes pattern where player can't rely on NPC in crisis",
        long_term_risk: "If repeated, player learns not to ask for help"
      }
    };
  }
  
  // DEFAULT: Tries to help, does poorly, both feel bad
  return {
    response_type: "inadequate_support",
    
    dialogue: `
      ${npc.name} tries to help. They listen, nod, say the right things.
      
      But something's off. They're distracted. Not fully present. 
      Their advice feels... generic. Disconnected.
      
      You both know this isn't working. But neither of you says it.
    `,
    
    effects: {
      player_emotional_meter: +0,  // No real help
      player_capacity: -0.1,  // Slight negative (effort wasted)
      relationship_trust: -0.08,  // Minor harm
      npc_capacity: npcCapacity.value - 0.6
    },
    
    consequences: {
      immediate: "Awkward, unsatisfying interaction",
      both_feel_bad: true,
      missed_opportunity: "Honest limitation would have been better"
    }
  };
}

function checkSelfAwareness(npc, capacity) {
  // HIGH OPENNESS + MODERATE EMOTIONAL INTELLIGENCE = Recognizes limits
  const { openness, neuroticism } = npc.ocean;
  const emotionalIntelligence = npc.emotional_intelligence || 0.5;
  
  // More likely to recognize limits if:
  // - High openness (self-reflective)
  // - Low neuroticism (not anxious, can assess clearly)
  // - High emotional intelligence
  // - Not at crisis capacity (< 2.0 = can't think clearly)
  
  if (capacity.value < 2.0) return false;  // Crisis = no self-awareness
  
  const awarenessScore = 
    (openness * 0.4) +
    ((1.0 - neuroticism) * 0.3) +
    (emotionalIntelligence * 0.3);
  
  return awarenessScore >= 0.6;
}

function generateLimitedSupportDialogue(npc, player, npcCapacity, playerNeedLevel) {
  // Example: Sarah at capacity 4.5, player needs 6.0 support
  return {
    internal_state: `${npc.name} wants to help but is struggling themselves (capacity ${npcCapacity.value})`,
    
    dialogue: `
      Sarah listens as you talk. You can see her trying to be present, 
      but there's something distant in her eyes.
      
      "I want to help," she says, and you can tell she means it. "But 
      I'm barely keeping it together myself right now. I'm sorry. I 
      wish I could give you more."
      
      She reaches for your hand. "I'm here. But I'm... I'm not at my 
      best. I hope that's okay."
    `,
    
    player_experience: "She tried. But you needed more than she could give right now. It's not her fault.",
    
    relationship_impact: {
      trust: -0.1,  // Minor strain
      reason: "Need unmet, but limitation acknowledged authentically",
      recovery: "Will recover when Sarah's capacity improves"
    }
  };
}
```

### Example: Full Support vs. OCEAN-Modified Failures

```
SCENARIO: Player at capacity 3.5 (VERY LOW), needs 6.0 level support

═══════════════════════════════════════════════════════════════

SARAH AT CAPACITY 7.5 (HIGH) - FULL SUPPORT:
┌────────────────────────────────────────┐
│ ☕ Coffee with Sarah                   │
├────────────────────────────────────────┤
│ Sarah notices your exhaustion          │
│ immediately.                           │
│                                        │
│ "Sit down," she says gently. "Tell me │
│ everything."                           │
│                                        │
│ For the next hour, she gives you her  │
│ full attention. No distractions. No    │
│ judgment. Just presence.               │
│                                        │
│ By the time you leave, you feel like  │
│ you can breathe again.                 │
│                                        │
│ Effects:                               │
│ 😊 Emotional: 3 → 5 (+2)              │
│ 💝 Trust (Sarah): +0.08                │
│ 🔋 Capacity: 3.5 → 4.0 (+0.5)         │
│ 🟢 SUCCESS - Need met                 │
└────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════

SARAH AT CAPACITY 4.5 (LOW) - RECOGNIZES LIMITATION:
(High Openness 0.75 + High EI 0.80 = Self-aware)

┌────────────────────────────────────────┐
│ ☕ Coffee with Sarah                   │
├────────────────────────────────────────┤
│ ⚠️ Sarah recognizes her limits (4.5)  │
│                                        │
│ "I want to help," she says honestly.  │
│ "But I'm barely keeping it together   │
│ myself right now. I'm sorry. I wish I │
│ could give you more."                  │
│                                        │
│ She reaches for your hand. "I'm here. │
│ But I'm... not at my best."           │
│                                        │
│ It's not what you needed. But at least│
│ she was honest.                        │
│                                        │
│ Effects:                               │
│ 😊 Emotional: 3 → 4 (+1, partial)     │
│ 💝 Trust: -0.05 (minor, but honest)   │
│ 🔋 Capacity: 3.5 → 3.7 (+0.2)         │
│ 🟡 LIMITATION ACKNOWLEDGED             │
└────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════

SARAH AT CAPACITY 4.5 (LOW) - OVEREXTENSION BURNOUT:
(High Agreeableness 0.80 + High Conscientiousness 0.75 = Tries anyway)

┌────────────────────────────────────────┐
│ ☕ Coffee with Sarah                   │
├────────────────────────────────────────┤
│ ⚠️ Sarah doesn't recognize her limits  │
│                                        │
│ Sarah tries to help. Really tries. But│
│ you can see the strain in her face.   │
│ She's pushing herself beyond what she │
│ can handle.                            │
│                                        │
│ Halfway through, she snaps.            │
│                                        │
│ "I'm sorry," she says, voice tight.   │
│ "I can't. I just... I can't do this   │
│ right now. I need to go."              │
│                                        │
│ She leaves abruptly. You're left      │
│ feeling worse than before.             │
│                                        │
│ Effects:                               │
│ 😞 Emotional: 3 → 2 (-1, WORSE)       │
│ 💔 Trust: -0.15 (MODERATE HARM)       │
│ 🔋 Capacity: 3.5 → 3.2 (-0.3)         │
│ 🔴 FAILURE - Both hurt                │
│                                        │
│ Sarah's resentment: +0.2               │
│ Recovery required: 1-2 weeks           │
└────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════

MARCUS AT CAPACITY 3.5 (VERY LOW) - BLUNT REJECTION:
(Low Agreeableness 0.35 = Direct/blunt when stressed)

┌────────────────────────────────────────┐
│ 💼 Talk to Marcus                      │
├────────────────────────────────────────┤
│ ⚠️ Marcus at capacity 3.5/10           │
│                                        │
│ Marcus cuts you off mid-sentence.      │
│                                        │
│ "Look, I've got my own shit to deal   │
│ with. I can't handle your problems on │
│ top of mine right now."                │
│                                        │
│ It's not malicious. Just... blunt. Too│
│ blunt. The words sting.                │
│                                        │
│ He's right to set a boundary. But it  │
│ hurts how he said it.                  │
│                                        │
│ Effects:                               │
│ 😞 Emotional: 3 → 1 (-2)              │
│ 💔 Trust: -0.25 (MAJOR HARM)          │
│ 🔋 Capacity: 3.5 → 3.0 (-0.5)         │
│ 🔴 CORRECT BOUNDARY, POOR DELIVERY    │
│                                        │
│ Relationship damage significant        │
│ Formal apology may be needed           │
│ (Personality consistent - low agree)   │
└────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════

TAYLOR AT CAPACITY 4.0 (LOW) - ANXIOUS SPIRAL:
(High Neuroticism 0.80 = Spirals when stressed)

┌────────────────────────────────────────┐
│ 📱 Call Taylor for Support             │
├────────────────────────────────────────┤
│ ⚠️ Taylor at capacity 4.0/10           │
│                                        │
│ Taylor listens, but their breathing   │
│ gets shallow.                          │
│                                        │
│ "God, I'm such a terrible friend,"    │
│ they say suddenly. "You're going      │
│ through this and I can't even... I'm  │
│ barely keeping it together myself and │
│ now you need me and I can't—"         │
│                                        │
│ They're spiraling. You end up         │
│ comforting THEM instead.               │
│                                        │
│ Effects:                               │
│ 😞 Emotional: 3 → 2 (-1)              │
│ 💔 Trust: -0.12 (moderate strain)     │
│ 🔋 Capacity: 3.5 → 3.1 (-0.4)         │
│ 🔴 ROLE REVERSAL - You support them   │
│                                        │
│ Pattern established: Can't rely on    │
│ Taylor in crisis (if repeated)         │
└────────────────────────────────────────┘
```

**Key Insight:** The SAME situation (low capacity NPC + high need player) produces DIFFERENT outcomes based on OCEAN traits. Some NPCs handle limits healthily, others don't - and that creates realistic relationship complexity.

---

## Phase 5c: Dramatic Irony Detection *(NEW - Master Truths v1.2)*

### Player Overlay System for Knowledge Gaps

**Core Principle:** When player knows information character doesn't, show overlay explaining dramatic irony.

```javascript
function detectDramaticIrony(card, player, turnContext, knowledgeBase) {
  if (!card.involves_npcs) return null;
  
  // Check for knowledge gaps
  const gaps = detectKnowledgeGaps(
    knowledgeBase.player_knowledge,
    knowledgeBase.character_knowledge,
    turnContext
  );
  
  if (gaps.length === 0) return null;
  
  // Find gaps relevant to this card/NPC
  const relevantGaps = gaps.filter(gap => 
    gap.affects_npcs.includes(card.npc_id) &&
    gap.irony_score >= 0.6  // Master Truths v1.2 threshold
  );
  
  if (relevantGaps.length === 0) return null;
  
  // DRAMATIC IRONY PRESENT
  const primaryGap = relevantGaps[0];  // Highest scored gap
  
  return {
    has_irony: true,
    gap: primaryGap,
    irony_score: primaryGap.irony_score,
    
    // Player overlay
    show_overlay: true,
    overlay_type: determineOverlayType(primaryGap, card),
    overlay_text: generateOverlayText(primaryGap, card, player),
    
    // Response options modification
    add_growth_option: true,
    add_tone_deaf_warning: true
  };
}

function generateOverlayText(gap, card, player) {
  return {
    player_knowledge: gap.content,
    character_knowledge: "Character does NOT know this",
    tension_created: gap.irony_score,
    
    warning: `
      💭 YOU KNOW: ${gap.content}
      
      But your character doesn't know this yet. How you respond 
      will affect ${card.npc_name}'s willingness to share.
      
      Choose carefully.
    `
  };
}
```

### Example: Marcus Job Loss Dramatic Irony

```
CARD: Ask Marcus for Financial Advice

KNOWLEDGE GAP DETECTED:
- Player knows: Marcus lost job 2 weeks ago
- Character knows: Nothing (thinks Marcus is employed)
- Irony score: 0.825 (HIGH - above 0.6 threshold)

┌────────────────────────────────────────┐
│ 💭 DRAMATIC IRONY ACTIVE               │
├────────────────────────────────────────┤
│ YOU (the player) know:                 │
│ Marcus lost his job 2 weeks ago.       │
│ He's been hiding it from everyone.     │
│                                        │
│ YOUR CHARACTER doesn't know this.      │
│ They think Marcus is employed and      │
│ financially stable.                    │
│                                        │
│ How you respond will affect Marcus's   │
│ willingness to open up.                │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ 💼 Ask Marcus for Financial Advice     │
│ ⚡ 1 Energy │ ⏰ 30 min                │
│                                        │
│ Marcus looks tired. But you don't     │
│ notice—you're too focused on your own │
│ bookshop financial stress.             │
│                                        │
│ RESPONSE OPTIONS:                      │
│                                        │
│ 1. [TONE-DEAF] "Marcus, I need your   │
│    advice on managing money. You're   │
│    always so good with finances!"     │
│    ⚠️ Will hurt Marcus (asking broke  │
│    person for financial advice)       │
│    Trust: -0.05                        │
│                                        │
│ 2. [MISGUIDED] "You seem stressed.    │
│    Everything okay?"                   │
│    Gentle probe, respects boundaries  │
│    Trust: -0.02                        │
│    May open door for future reveal    │
│                                        │
│ 3. [GROWTH] "Marcus. I know something │
│    is wrong. You don't have to tell   │
│    me if you're not ready. But I'm    │
│    here when you are."                │
│    ✓ Creates safe space                │
│    Trust: +0.08 (if he shares)        │
│    May lead to job loss reveal        │
│                                        │
│ [Make Choice] →                        │
└────────────────────────────────────────┘
```

---

**Example Resolution:**
```
RESOLVING: Coffee with Sarah

Costs Deducted:
⚡ Energy: 3 → 2
⏰ Time: 28h → 27h
💰 Money: $1,250 → $1,242

Outcome: AUTOMATIC SUCCESS (social activities don't fail)

Effects:
📊 Social Meter: 7 → 9 (+2)
😊 Emotional Meter: 5 → 6 (+1)
🤝 Social Capital (Sarah): +2
💝 Trust (Sarah): 0.62 → 0.65 (+0.03)

Narrative:
────────────────────────────────────────
You meet Sarah at Café Luna. The familiar 
warmth of her smile immediately eases the 
knot in your chest. 

"Rough morning?" she asks, reading you 
instantly.

You nod, and she listens. Really listens. 
By the end of the hour, the overwhelm 
hasn't disappeared, but it feels 
manageable now. You're not alone.

"Thanks," you say. "I needed this."

"Anytime," she replies. And you know she 
means it.
────────────────────────────────────────

State Change:
🔵 OVERWHELMED (0.85) → OVERWHELMED (0.70)
   Intensity reduced through support

[Continue] →
```

---

## Phase 6: State Update

### Update All Game State

```javascript
function updateGameState(outcomes, player, turnContext) {
  // 1. Update player meters (check for thresholds)
  updateMeters(player, outcomes);
  checkMeterThresholds(player);
  
  // 2. Update resources
  // (Already deducted during resolution, but check for regeneration)
  
  // 3. Update relationships
  updateAllRelationships(player, outcomes);
  checkRelationshipLevelUps(player);
  
  // 4. Update aspiration progress
  if (player.aspiration) {
    updateAspirationProgress(player.aspiration, outcomes);
    checkAspirationMilestones(player.aspiration);
  }
  
  // 5. Update narrative arcs
  updateNarrativeArcs(player.activeArcs, outcomes, turnContext);
  
  // 6. Check for triggered events
  const triggeredEvents = checkEventTriggers(player, turnContext, outcomes);
  queueEvents(triggeredEvents);
  
  // 7. Update emotional state (may have changed)
  const newEmotionalState = recalculateEmotionalState(player);
  if (newEmotionalState.primary !== turnContext.emotionalStates.primary) {
    notifyStateChange(newEmotionalState);
  }
  
  // 8. Save turn history
  saveTurnHistory(turnContext, outcomes, player);
  
  return {
    meters_updated: true,
    relationships_updated: true,
    arcs_updated: true,
    state_saved: true
  };
}
```

---

## Turn End

### Transition to Next Turn or Day End

```javascript
function endTurn(player, turnContext) {
  const { current_phase } = turnContext;
  
  // Determine next phase
  const phaseOrder = ["morning", "afternoon", "evening"];
  const currentIndex = phaseOrder.indexOf(current_phase);
  
  if (currentIndex < phaseOrder.length - 1) {
    // More turns today
    const nextPhase = phaseOrder[currentIndex + 1];
    
    // Regenerate energy for next phase
    regenerateEnergy(player, nextPhase);
    
    return {
      continue_day: true,
      next_phase: nextPhase,
      transition_type: "next_turn"
    };
  } else {
    // Day is complete
    return {
      continue_day: false,
      end_of_day: true,
      transition_type: "day_end"
    };
  }
}
```

**Turn Transition:**
```
┌────────────────────────────────────────┐
│ MORNING TURN COMPLETE                  │
├────────────────────────────────────────┤
│ You spent the morning connecting       │
│ with Sarah. The work day awaits.       │
│                                        │
│ It's now 12:00 PM                      │
│ ⚡ Energy Regenerated: 3/3             │
│ ⏰ Time Remaining: 27 hours            │
│                                        │
│ [Begin Afternoon Turn] →               │
└────────────────────────────────────────┘
```

---

## Day End Processing

### When All 3 Turns Complete

```javascript
function endDay(player, dayContext) {
  // 1. Day summary
  const summary = generateDaySummary(dayContext);
  
  // 2. Passive meter changes
  applyPassiveMeterChanges(player);
  
  // 3. Relationship maintenance
  checkRelationshipNeglect(player);
  
  // 4. Check for day-end events
  const dayEndEvents = checkDayEndTriggers(player, dayContext);
  
  // 5. Aspiration daily progress
  if (player.aspiration) {
    updateDailyProgress(player.aspiration, dayContext);
  }
  
  // 6. Prepare for tomorrow
  const tomorrow = {
    day: getNextDay(dayContext.current_day),
    week: dayContext.current_week,
    obligations: generateTomorrowObligations(player),
    events: queuedEvents
  };
  
  // 7. Save day
  saveDayHistory(dayContext, summary);
  
  // Check if week end
  if (tomorrow.day === "saturday" && player.settings.routine_batching) {
    return {
      prompt_weekend_planning: true
    };
  }
  
  if (tomorrow.day === "monday") {
    return {
      week_end: true,
      process_week_end: true
    };
  }
  
  return {
    day_complete: true,
    tomorrow: tomorrow
  };
}
```

**Day Summary:**
```
┌────────────────────────────────────────┐
│ MONDAY COMPLETE                        │
├────────────────────────────────────────┤
│ How the day went:                      │
│                                        │
│ Morning: Connected with Sarah ☕       │
│ Afternoon: Worked (auto-batched) 💼   │
│ Evening: Portfolio work 🎨             │
│                                        │
│ Meters:                                │
│ Physical: 6 (↔)                        │
│ Mental: 4 (↓1)                         │
│ Social: 9 (↑2)                         │
│ Emotional: 6 (↑1)                      │
│                                        │
│ Aspiration Progress: 68% (↑5%)        │
│                                        │
│ [Continue to Tuesday] →                │
└────────────────────────────────────────┘
```

---

## Special Turn Types

### Batched Routine Turns

```javascript
function handleBatchedRoutine(routine, duration) {
  // Skip individual turn display for repeated routines
  return {
    type: "batched_routine",
    routine: routine,
    days_batched: duration,
    
    // Auto-calculate outcomes
    resources_spent: calculateBatchedCosts(routine, duration),
    meters_change: calculateBatchedMeterChanges(routine, duration),
    
    // Fast-forward narrative
    narrative: `${duration} days of familiar routine pass quickly.
                Your ${routine.type} continues as usual.`,
    
    // Player can review details if desired
    detailed_breakdown: generateBatchedBreakdown(routine, duration)
  };
}
```

**Example:**
```
┌────────────────────────────────────────┐
│ ROUTINE BATCHING                       │
├────────────────────────────────────────┤
│ Tuesday - Thursday                     │
│ Your work week routine:                │
│                                        │
│ Morning: Coffee → Work                 │
│ Afternoon: Work                        │
│ Evening: Portfolio work                │
│                                        │
│ Resources Spent (3 days):              │
│ ⚡ Energy: 24 (8/day)                  │
│ ⏰ Time: 30 hours                      │
│ 💰 Money: +$900 (income) -$45 (meals) │
│                                        │
│ Aspiration Progress: +12%              │
│                                        │
│ [Fast Forward →] [Review Details]      │
└────────────────────────────────────────┘
```

---

### Decisive Decision Turns

```javascript
function handleDecisiveDecision(decision, player, turnContext) {
  return {
    type: "decisive_decision",
    time_paused: true,              // master_truths v1.1 compliance
    
    // Full decision display
    decision: decision,
    
    // Context for decision
    display_context: {
      show_meters: true,
      show_money: true,
      show_relationships: decision.relevant_npcs,
      show_arc_progress: decision.relevant_arcs,
      review_options: [
        "View relationship history",
        "Review arc timeline",
        "Check financial status"
      ]
    },
    
    // Player can take unlimited time
    no_time_pressure: true,
    can_review_history: true,
    
    // Resolution handled separately
    requires_explicit_choice: true
  };
}
```

---

## Performance Optimization

### Turn Processing Speed

```javascript
const PERFORMANCE_TARGETS = {
  turn_start_processing: "< 100ms",
  emotional_state_calculation: "< 50ms",
  hand_generation: "< 200ms",
  player_action_phase: "player_controlled",
  resolution_per_card: "< 100ms",
  state_update: "< 150ms",
  
  total_system_time: "< 600ms",
  target_player_time: "30-120 seconds",
  
  // Batching optimization
  batched_routine: "< 500ms for 3 days"
};
```

---

## Phase 5d: Numerical Grounding Examples *(NEW - Master Truths v1.2)*

### Trust Impact Calculation in Turn Resolution

**Core Principle:** Every relationship change must be calculated with formula and validated against qualitative anchor.

```javascript
function calculateTrustImpact(card, outcome, npc, player) {
  // EXAMPLE: Sarah provides limited support due to low capacity
  
  const scenario = {
    action: "Sought emotional support from Sarah",
    player_capacity: 3.5,  // VERY LOW
    player_need: 6.0,      // HIGH need
    sarah_capacity: 4.5,   // LOW
    sarah_can_support: 4.5 + 2 = 6.5  // Capacity + 2 rule
  };
  
  // Sarah CAN support (6.5 >= 6.0) but it drains her
  // Calculate trust impact
  
  const trustImpact = {
    base: +0.05,  // Small positive (she tried to help)
    personality_modifier: player.openness * 0.2,  // High openness = appreciate effort
    capacity_strain: -0.15,  // Sarah struggled, player noticed
    
    formula: "+0.05 + (0.8 openness × 0.2) - 0.15 = -0.08",
    
    final_value: -0.08,
    
    qualitative_anchor: {
      tier: "VERY MINOR HARM (-0.1 to 0)",
      narrative_markers: [
        "Slight disappointment",
        "Needed more than given",
        "But appreciate the effort"
      ],
      expected_dialogue: "She tried. It's not her fault she couldn't give more.",
      recovery_time: "1-2 weeks"
    },
    
    validation: {
      does_narrative_match: true,
      reasoning: "-0.08 is VERY MINOR HARM. Player disappointed but understanding. Matches tier."
    }
  };
  
  return trustImpact;
}
```

### Capacity Calculation Example

```javascript
const CAPACITY_EXAMPLE = {
  turn: "Monday Morning, Week 5",
  
  meters: {
    emotional: 6,
    mental: 5,
    physical: 7,
    social: 6
  },
  
  calculation: {
    emotional_weighted: 6 × 0.50 = 3.0,
    mental_weighted: 5 × 0.30 = 1.5,
    physical_weighted: 7 × 0.15 = 1.05,
    social_weighted: 6 × 0.05 = 0.3,
    
    base_sum: 5.85,
    
    stressors: [
      { type: "work_overload", penalty: 0.5 },
      { type: "financial_pressure", penalty: 0.4 }
    ],
    stacking_penalty: 0.5 + 0.4 = 0.9,
    
    final_capacity: 5.85 - 0.9 = 4.95
  },
  
  qualitative_anchor: {
    tier: "LOW (4-6 range)",
    functional_state: "Can handle basics, struggles with complexity",
    support_capacity: 4.95 - 2 = 2.95,  // Can support up to 2.95 need level
    behavioral_signs: [
      "Present but limited",
      "Short attention span",
      "Apologizes for not being enough"
    ]
  },
  
  validation: {
    matches_tier: true,
    reasoning: "4.95 is LOW tier. Player can function but is strained. Matches expected behavior."
  }
};
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Turn Mechanics (v1.1 Foundation)
- [x] 3 turns per day (Morning/Afternoon/Evening)
- [x] 7 days per week
- [x] Decisive decisions pause time (no real-time pressure)
- [x] Batching available to reduce friction
- [x] Resources tracked per specification
- [x] Emotional states influence card draw
- [x] Success determined by formulas, not RNG gacha

### ✅ Master Truths v1.2: Emotional Capacity System
- [x] **Capacity Calculation** (Phase 1b) - ~110 lines
  - Weighted formula: (Emo×0.5) + (Mental×0.3) + (Phys×0.15) + (Social×0.05)
  - Circumstance stacking detection (5 stressor types)
  - Penalty calculation with amplification (3+ stressors)
  - Tier classification (CRISIS → VERY_LOW → LOW → MODERATE → HIGH)
  - Functional limits (can_support_up_to = capacity - 2)
- [x] **Capacity Display** in turn start with visual bar and warnings
- [x] **Active Stressor Tracking** (work, relationship, financial, health, deadlines)

### ✅ Master Truths v1.2: Capacity-Aware Hand Generation
- [x] **Hand Reduction Logic** (Phase 3b) - ~55 lines
  - Capacity ≥ 6.0: Full hand (8-10 cards), all complexity allowed
  - Capacity 4.0-6.0: Reduced hand (7-8 cards), filter high-complexity/high-energy
  - Capacity < 4.0: Minimal hand (obligations + 2 recovery), crisis mode
- [x] **Complexity Filtering** based on capacity tier
- [x] **Recovery Options** prioritized when capacity low
- [x] **Warning Messages** explain capacity limitations

### ✅ Master Truths v1.2: Tension Hook Integration
- [x] **Hook Detection** (Phase 3c) - ~50 lines
  - Filter relevant hooks for current context
  - Check hook status (planted, weeks active, surface timing)
  - Surface hooks in cards when appropriate
- [x] **Hook Enhancement** of card dialogue and narrative
- [x] **Urgent Hook Events** created when hooks overdue (4+ weeks)
- [x] **Information Debt Display** shows mystery/questions to player

### ✅ Master Truths v1.2: Memory Resonance Integration
- [x] **Memory Surfacing** (Phase 3d) - ~95 lines
  - Calculate resonance scores for related memories
  - Surface memories with score ≥ 6.0
  - Display memory echoes alongside relevant cards
  - Show season/week of memory origin
- [x] **Memory Echo Narrative** integrated into card display
- [x] **Player Decision Influence** - memories affect choices
- [x] **Growth Option Addition** based on memory triggers

### ✅ Master Truths v1.2: NPC Response Framework
- [x] **Capacity-Constrained Responses** (Phase 5b) - ~75 lines
  - Calculate NPC capacity per turn
  - Determine player need level (0-10 scale)
  - Check capacity match (NPC capacity + 2 rule)
  - Generate full_support vs. limited_support responses
- [x] **Authentic Limitation Dialogue** when NPC can't fully help
- [x] **Relationship Impact** varies by capacity match
- [x] **NPC Capacity Drain** tracked per interaction

### ✅ Master Truths v1.2: Dramatic Irony System
- [x] **Knowledge Gap Detection** (Phase 5c) - ~115 lines
  - Detect gaps between player/character knowledge
  - Calculate irony score (≥ 0.6 threshold)
  - Filter relevant gaps per card/NPC
- [x] **Player Overlay Display** explains dramatic irony
- [x] **Three Response Types** (tone-deaf, misguided, growth)
- [x] **Warning System** shows trust impacts per option
- [x] **Growth Choice Emphasis** creates safe space for NPCs

### ✅ Master Truths v1.2: Numerical Grounding
- [x] **Trust Impact Formulas** with full derivation
- [x] **Capacity Calculations** with step-by-step breakdown
- [x] **Qualitative Anchor** integration for all numbers
- [x] **Validation System** confirms narrative matches values
- [x] **Tier Classification** linked to behavioral markers

### ✅ Cross-References
- [x] Links to `74-multi-season-continuity-spec.md` (memory resonance, hooks, dramatic irony)
- [x] Links to `14-emotional-state-mechanics.md` (state determination)
- [x] Links to `11-turn-economy-implementation.md` (resource tracking)
- [x] Links to `12-success-probability-formulas.md` (capacity-modified success)
- [x] Links to `master_truths_canonical_spec_v_1_2.md` Sections 16 & 17
- [x] This doc cites **Truths v1.2** at the top

**Total v1.2 Enhancements:** ~615 lines of new turn-level mechanics

**References:**
- See `10-resource-economy-spec.md` for resource tracking
- See `14-emotional-state-mechanics.md` for state determination
- See `12-success-probability-formulas.md` for card resolution
- See `72-weekly-cycle-implementation.md` for week-level flow
- See `74-multi-season-continuity-spec.md` for memory resonance, hooks, dramatic irony systems
- See `master_truths_canonical_spec_v_1_2.md` Section 16 (Emotional Authenticity)
- See `master_truths_canonical_spec_v_1_2.md` Section 17 (Novel-Quality Narratives)
- See `NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md` for qualitative anchors

---

**This specification enables developers to implement the complete turn-by-turn gameplay loop with emotional capacity tracking, tension hook surfacing, memory resonance, dramatic irony detection, capacity-constrained NPC responses, and full numerical grounding - creating authentic, novel-quality moment-to-moment gameplay.**

