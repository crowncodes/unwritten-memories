# Weekly Cycle Implementation - Complete Specification

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete week-level gameplay flow with capacity fluctuation tracking, tension hook progression, NPC capacity monitoring, and quality validation

**References:**
- **Design Philosophy:** `1.concept/21-turn-structure.md` (WHY weekly cycles)
- **Daily Turn Flow:** `71-daily-turn-flow-detailed.md` (turn-by-turn gameplay)
- **Resource Economy:** `11-turn-economy-implementation.md` (weekly budgets)
- **Narrative Arc:** `31-narrative-arc-scaffolding.md` (week-level beats)

---

## Overview

Each week consists of **7 days × 3 turns/day = 21 turns** with distinct weekday/weekend rhythms. The system manages weekly resource budgets, processes routine batching, triggers weekly events, and updates long-term progression.

**Core Principle:** Weeks are the strategic planning unit. Days are tactical execution. Turns are immediate decisions.

**Compliance:** master_truths v1.1 specifies "7 days per week" with turn economy designed around weekly cycles.

---

## Week Structure

### Complete Weekly Template

```typescript
interface WeekState {
  week_number: number;               // Season-relative (1-12, 1-24, or 1-36)
  season: SeasonState;
  days: DayState[];                  // 7 days
  
  // Weekly budgets
  budgets: {
    time_hours: 168,
    time_flexible: 53,               // After fixed obligations
    time_spent: number,
    money_income: number,            // Weekly paycheck
    money_expenses: number,          // Weekly bills
    energy_total: 58                 // 8×5 weekdays + 11×2 weekend
  };
  
  // Weekly goals
  aspiration_progress_target: number;
  relationship_maintenance_needed: NPC[];
  routine_schedule: RoutineTemplate;
  
  // Events
  scheduled_events: Event[];
  triggered_events: Event[];
  
  // Narrative
  narrative_beat: NarrativeBeat | null;
  complications: Complication[];
  decisive_decision: DecisiveDecision | null;
}
```

---

## Week Start Processing

### Monday Morning Initialization

```javascript
async function startWeek(gameState) {
  const weekState = {
    week_number: gameState.season.current_week,
    season: gameState.season,
    start_date: getCurrentDate(gameState)
  };
  
  // 1. RESET WEEKLY RESOURCES
  weekState.resources = resetWeeklyResources(gameState.player);
  
  // 2. PROCESS INCOME/EXPENSES
  weekState.finances = processWeeklyFinances(gameState.player);
  
  // 3. CHECK NARRATIVE BEATS
  weekState.narrative_beat = getNarrativeBeatForWeek(
    gameState.season.arc,
    weekState.week_number
  );
  
  // 4. GENERATE WEEKLY EVENTS
  weekState.scheduled_events = generateWeeklyEvents(
    gameState,
    weekState.narrative_beat
  );
  
  // 5. CHECK RELATIONSHIP MAINTENANCE
  weekState.relationship_needs = checkRelationshipMaintenance(
    gameState.player.relationships
  );
  
  // 6. OFFER ROUTINE BATCHING (if applicable)
  if (gameState.player.settings.routine_batching_enabled) {
    weekState.routine_proposal = proposeRoutineBatching(
      gameState.player,
      weekState
    );
  }
  
  // 7. DISPLAY WEEK PREVIEW
  displayWeekPreview(weekState);
  
  return weekState;
}
```

**Week Preview UI:**
```
┌────────────────────────────────────────┐
│ WEEK 5 BEGINS - SEASON: THE PORTFOLIO │
├────────────────────────────────────────┤
│ Monday, March 1st                      │
│                                        │
│ THIS WEEK'S FOCUS:                     │
│ 🎨 Complete 3 portfolio pieces        │
│ 📈 Aspiration: 68% → 80% (target)    │
│                                        │
│ WEEKLY BUDGET:                         │
│ ⏰ Time: 53 flexible hours             │
│ 💰 Money: +$900 (paycheck Friday)     │
│    Bills: -$125 (utilities Wed)       │
│                                        │
│ SCHEDULED EVENTS:                      │
│ Wed Evening: Sarah's Birthday Party    │
│ Fri Afternoon: 1-on-1 with Boss       │
│                                        │
│ RELATIONSHIP MAINTENANCE:              │
│ ⚠️ Marcus (2 weeks since contact)     │
│ ⚠️ Elena (3 weeks since contact)      │
│                                        │
│ ROUTINE BATCHING AVAILABLE:            │
│ ✓ Batch Mon-Thu work routine?         │
│   (Saves time, auto-processes days)    │
│                                        │
│ [Begin Week] [Review Season] [?] Help  │
└────────────────────────────────────────┘
```

---

## Weekly Resource Management

### Time Budget (168 Hours)

```javascript
const WEEKLY_TIME_BUDGET = {
  total_hours: 168,
  
  fixed_obligations: {
    sleep: 56,                       // 8 hours × 7 days
    work: 45,                        // 9 hours × 5 days (if employed)
    basic_needs: 14,                 // 2 hours/day (meals, hygiene, etc.)
    total: 115
  },
  
  flexible_hours: 53,                // What player controls
  
  // Breakdown by day type
  weekday: {
    total: 24,
    fixed: 19,                       // Sleep 8 + Work 9 + Needs 2
    flexible: 5                      // 5 hours/weekday to allocate
  },
  
  weekend: {
    total: 48,                       // 24 × 2 days
    fixed: 20,                       // Sleep 16 + Needs 4
    flexible: 28                     // 28 hours/weekend to allocate
  }
};
```

**Time Tracking:**
```javascript
function trackWeeklyTime(activities, weekState) {
  let timeSpent = 0;
  
  activities.forEach(activity => {
    if (activity.time_cost) {
      timeSpent += activity.time_cost;
    }
  });
  
  weekState.budgets.time_spent = timeSpent;
  weekState.budgets.time_remaining = 53 - timeSpent;
  
  // Check for over-scheduling
  if (timeSpent > 53) {
    return {
      over_scheduled: true,
      excess_hours: timeSpent - 53,
      warning: "You're trying to do more than time allows this week"
    };
  }
  
  return {
    on_track: true,
    remaining: 53 - timeSpent
  };
}
```

---

### Money Budget (Weekly Income/Expenses)

```javascript
function processWeeklyFinances(player) {
  const finances = {
    // Income (usually Friday)
    income: {
      paycheck: player.career ? player.career.weekly_salary : 0,
      side_income: calculateSideIncome(player),
      total: 0
    },
    
    // Expenses (various days)
    expenses: {
      rent: player.living.rent / 4,  // Weekly portion of monthly rent
      utilities: player.living.utilities / 4,
      groceries: 80,                 // ~$80/week average
      transport: 30,                 // Gas, transit, etc.
      subscriptions: calculateWeeklySubscriptions(player),
      discretionary: 0,              // Variable spending
      total: 0
    },
    
    // Net
    net_weekly: 0,
    projected_balance_end_of_week: player.money.current + net_weekly
  };
  
  finances.income.total = finances.income.paycheck + finances.income.side_income;
  finances.expenses.total = Object.values(finances.expenses)
    .filter(v => typeof v === 'number')
    .reduce((sum, v) => sum + v, 0);
  finances.net_weekly = finances.income.total - finances.expenses.total;
  finances.projected_balance_end_of_week = player.money.current + finances.net_weekly;
  
  return finances;
}
```

**Financial Events During Week:**
```javascript
const FINANCIAL_EVENTS = [
  {
    day: "monday",
    type: "expense",
    category: "groceries",
    amount: 80,
    narrative: "Weekly grocery shopping"
  },
  {
    day: "wednesday",
    type: "expense",
    category: "utilities",
    amount: 125,
    narrative: "Utilities bill auto-paid"
  },
  {
    day: "friday",
    type: "income",
    category: "paycheck",
    amount: 900,
    narrative: "Paycheck deposited"
  }
];
```

---

## Day-by-Day Flow

### Weekday vs Weekend Rhythm

```javascript
const DAY_RHYTHMS = {
  weekday: {
    day_type: "weekday",
    energy_budget: 8,                // Lower energy
    time_flexible: 5,                // Limited time
    
    typical_structure: {
      morning: {
        energy: 3,
        typical_cards: ["morning_routine", "commute", "work_start"],
        player_choice_limited: true  // Mostly obligations
      },
      afternoon: {
        energy: 3,
        typical_cards: ["work", "lunch_break"],
        player_choice_limited: true
      },
      evening: {
        energy: 2,
        typical_cards: ["commute_home", "dinner", "aspiration_work", "relax", "social"],
        player_choice_high: true     // This is "free time"
      }
    },
    
    batching_eligible: true          // Can batch weekdays
  },
  
  weekend: {
    day_type: "weekend",
    energy_budget: 11,               // Higher energy
    time_flexible: 14,               // Lots of time per day
    
    typical_structure: {
      morning: {
        energy: 4,
        typical_cards: ["sleep_in", "breakfast", "errands", "hobbies", "social"],
        player_choice_high: true
      },
      afternoon: {
        energy: 4,
        typical_cards: ["activities", "social", "aspiration_work", "errands"],
        player_choice_high: true
      },
      evening: {
        energy: 3,
        typical_cards: ["social", "date", "hobbies", "prep_for_week"],
        player_choice_high: true
      }
    },
    
    batching_eligible: false         // Never batch weekends - too unique
  }
};
```

---

## Routine Batching System

### Batch 2-4 Days of Routine

```javascript
async function proposeRoutineBatching(player, weekState) {
  // Analyze player's recent patterns
  const routine = detectRoutine(player.history, 3); // Last 3 weeks
  
  if (!routine || routine.consistency < 0.7) {
    return null; // No consistent routine to batch
  }
  
  // Propose batching
  const proposal = {
    days_to_batch: ["monday", "tuesday", "wednesday", "thursday"],
    routine_detected: routine,
    
    // Show what will happen
    preview: {
      turns_batched: 12,             // 4 days × 3 turns
      time_saved_real: "~15 minutes gameplay",
      
      // Predicted outcomes
      resources: {
        energy_spent: 32,            // 8/day × 4 days
        time_spent: 40,              // ~10 hours/day
        money_net: -45,              // Small expenses
      },
      
      meters_change: {
        physical: 0,                 // Stable
        mental: -1,                  // Work stress
        social: 0,
        emotional: 0
      },
      
      aspiration_progress: "+8%",    // Steady progress
      
      narrative: `Monday through Thursday pass in a familiar rhythm.
                  You work, make progress on your portfolio, and 
                  maintain your routine. By Friday morning, you're 
                  on track and ready for the weekend.`
    },
    
    can_adjust: true,                // Player can tweak
    can_decline: true                // Or play day-by-day
  };
  
  return proposal;
}
```

**Batching UI:**
```
┌────────────────────────────────────────┐
│ ROUTINE BATCHING AVAILABLE             │
├────────────────────────────────────────┤
│ Detected routine (87% consistent):     │
│                                        │
│ MON-THU: Work → Portfolio → Rest       │
│                                        │
│ BATCH THESE 4 DAYS?                    │
│ ⏩ Saves ~15 minutes gameplay          │
│ ⏰ Spends 40 hours (of 53 total)      │
│ 🎨 Aspiration: +8% progress           │
│ 📊 Meters: Mental -1 (work stress)    │
│                                        │
│ Friday/Weekend: You'll play normally   │
│                                        │
│ [✓ Batch Mon-Thu] [✗ Play Day-by-Day] │
│ [Adjust Routine...] [?] More Info      │
└────────────────────────────────────────┘
```

---

## Weekly Event Generation

### Event Frequency by Week Position

```javascript
function generateWeeklyEvents(gameState, narrative_beat) {
  const events = [];
  const { week_number, season } = gameState;
  
  // Base event frequency
  let event_probability = {
    social: 0.6,                     // 60% chance of social event
    aspiration: 0.5,                 // 50% chance of aspiration event
    career: 0.3,                     // 30% chance of work event
    crisis: 0.1,                     // 10% chance of crisis
    opportunity: 0.2                 // 20% chance of opportunity
  };
  
  // Modify based on narrative beat
  if (narrative_beat) {
    switch (narrative_beat.beat_type) {
      case "COMPLICATION":
        event_probability.crisis = 0.4;        // Higher crisis chance
        event_probability.opportunity = 0.1;   // Lower opportunity
        break;
      case "DECISIVE_DECISION":
        // Decisive decision is the event (no other major events)
        return [{
          type: "decisive_decision",
          decision: narrative_beat.content,
          day: calculateDecisionDay(week_number),
          phase: "evening",
          pauses_time: true
        }];
      case "RESOLUTION":
        event_probability.opportunity = 0.5;   // More opportunities
        event_probability.crisis = 0.05;       // Fewer crises
        break;
    }
  }
  
  // Generate events
  Object.entries(event_probability).forEach(([type, prob]) => {
    if (Math.random() < prob) {
      const event = generateEvent(type, gameState, week_number);
      if (event) {
        events.push(event);
      }
    }
  });
  
  // Place events on specific days
  events.forEach(event => {
    event.day = selectDayForEvent(event, week_number);
    event.phase = selectPhaseForEvent(event);
  });
  
  return events;
}
```

**Event Placement Strategy:**
```javascript
function selectDayForEvent(event, week_number) {
  // Strategic placement
  const placement_rules = {
    social_event: ["wednesday", "friday", "saturday"], // Mid-week or weekend
    work_event: ["monday", "tuesday", "thursday", "friday"], // Weekdays
    crisis: ["monday", "tuesday"],     // Early week (more time to deal)
    opportunity: ["monday", "wednesday"], // Early-mid week (time to capitalize)
    relationship_event: ["wednesday", "weekend"] // Mid-week or weekend
  };
  
  const eligible_days = placement_rules[event.category] || ["any"];
  return selectRandom(eligible_days);
}
```

---

## Week End Processing

### Sunday Evening Wrap-Up

```javascript
async function endWeek(weekState, player) {
  // 1. CALCULATE WEEK SUMMARY
  const summary = calculateWeekSummary(weekState);
  
  // 2. PROCESS PASSIVE CHANGES
  applyPassiveWeeklyChanges(player);
  
  // 3. CHECK RELATIONSHIP DECAY
  processRelationshipDecay(player.relationships, weekState);
  
  // 4. UPDATE ASPIRATION PROGRESS
  if (player.aspiration) {
    updateWeeklyAspirationProgress(player.aspiration, weekState);
  }
  
  // 5. PROCESS NARRATIVE ARC
  updateNarrativeArc(player.season.arc, weekState);
  
  // 6. CHECK FOR MILESTONES
  const milestones = checkWeeklyMilestones(player, weekState);
  
  // 7. GENERATE WEEK REFLECTION
  const reflection = generateWeekReflection(summary, player);
  
  // 8. SAVE WEEK HISTORY
  saveWeekToArchive(weekState, summary);
  
  // 9. PREPARE NEXT WEEK
  const nextWeek = prepareNextWeek(player, weekState);
  
  // Display summary
  displayWeekSummary(summary, reflection, milestones);
  
  return {
    week_complete: true,
    summary,
    next_week: nextWeek
  };
}
```

**Week Summary Display:**
```
┌────────────────────────────────────────┐
│ WEEK 5 COMPLETE                        │
├────────────────────────────────────────┤
│ 🎨 THE PORTFOLIO - Season 1            │
│                                        │
│ THIS WEEK'S STORY:                     │
│ You pushed hard on portfolio work,     │
│ celebrated Sarah's birthday, and had   │
│ a tough but productive 1-on-1 with     │
│ your boss. Progress is visible.        │
│                                        │
│ ASPIRATION PROGRESS:                   │
│ 68% → 79% (+11%)                       │
│ ✓ Completed 4 portfolio pieces         │
│ ⏳ 4 weeks remaining                   │
│                                        │
│ METERS:                                │
│ Physical: 6 (↔)                        │
│ Mental: 5 (↓1) - Work stress           │
│ Social: 8 (↑1) - Great connections     │
│ Emotional: 7 (↑1) - Feeling good       │
│                                        │
│ RELATIONSHIPS:                         │
│ Sarah: Level 3 → Level 4! 🎉          │
│   (Close Friend now - 32 interactions) │
│ Marcus: Level 2 (no change)            │
│ Elena: Level 2 (⚠️ 3 weeks neglect)   │
│                                        │
│ FINANCES:                              │
│ Starting: $1,250                       │
│ Income: +$900                          │
│ Expenses: -$285                        │
│ Ending: $1,865                         │
│                                        │
│ NEXT WEEK PREVIEW:                     │
│ Week 6 will bring a major complication │
│ related to work-life balance...        │
│                                        │
│ [Continue to Week 6] →                 │
└────────────────────────────────────────┘
```

---

## Master Truths v1.2: Capacity Fluctuation Tracking *(NEW)*

### Track Capacity Patterns Across Week

**Core Principle:** Weekly capacity patterns reveal burnout risk and inform intervention recommendations.

```javascript
function trackWeeklyCapacity(weekState, player) {
  const capacityTracking = {
    week_number: weekState.week_number,
    
    // Daily snapshots
    daily_capacity: [],
    
    // Weekly statistics
    average_capacity: 0,
    lowest_capacity: 10,
    highest_capacity: 0,
    
    // Pattern detection
    declining_trend: false,
    burnout_risk: false,
    recovery_needed: false,
    
    // Stressor analysis
    persistent_stressors: [],
    stressor_count_by_day: []
  };
  
  // Collect daily capacity values
  weekState.days.forEach((day, index) => {
    day.turns.forEach(turn => {
      if (turn.capacity_snapshot) {
        capacityTracking.daily_capacity.push({
          day: day.day_name,
          turn: turn.phase,
          capacity: turn.capacity_snapshot.value,
          stressors: turn.capacity_snapshot.active_stressors
        });
        
        // Update stats
        if (turn.capacity_snapshot.value < capacityTracking.lowest_capacity) {
          capacityTracking.lowest_capacity = turn.capacity_snapshot.value;
        }
        if (turn.capacity_snapshot.value > capacityTracking.highest_capacity) {
          capacityTracking.highest_capacity = turn.capacity_snapshot.value;
        }
      }
    });
  });
  
  // Calculate average
  const totalCapacity = capacityTracking.daily_capacity.reduce((sum, c) => sum + c.capacity, 0);
  capacityTracking.average_capacity = totalCapacity / capacityTracking.daily_capacity.length;
  
  // Detect declining trend
  const firstHalf = capacityTracking.daily_capacity.slice(0, 10).reduce((sum, c) => sum + c.capacity, 0) / 10;
  const secondHalf = capacityTracking.daily_capacity.slice(10).reduce((sum, c) => sum + c.capacity, 0) / 11;
  capacityTracking.declining_trend = (secondHalf < firstHalf - 1.0);
  
  // Check burnout risk
  const daysUnder4 = capacityTracking.daily_capacity.filter(c => c.capacity < 4.0).length;
  capacityTracking.burnout_risk = daysUnder4 >= 10 || capacityTracking.lowest_capacity <= 2.0;
  
  // Identify persistent stressors
  const stressorFrequency = {};
  capacityTracking.daily_capacity.forEach(snapshot => {
    snapshot.stressors.forEach(stressor => {
      stressorFrequency[stressor.type] = (stressorFrequency[stressor.type] || 0) + 1;
    });
  });
  
  capacityTracking.persistent_stressors = Object.entries(stressorFrequency)
    .filter(([type, count]) => count >= 10)  // Present in 10+ turns
    .map(([type, count]) => ({ type, frequency: count }));
  
  // Recommendations
  if (capacityTracking.burnout_risk) {
    capacityTracking.warning = {
      level: "HIGH",
      message: "Burnout risk detected. Capacity averaged " + capacityTracking.average_capacity.toFixed(1) + " this week.",
      recommendations: [
        "Reduce workload next week",
        "Schedule recovery activities",
        "Address persistent stressors: " + capacityTracking.persistent_stressors.map(s => s.type).join(", "),
        "Consider therapy/support options"
      ]
    };
  } else if (capacityTracking.declining_trend) {
    capacityTracking.warning = {
      level: "MODERATE",
      message: "Capacity declining. Started " + firstHalf.toFixed(1) + ", ended " + secondHalf.toFixed(1) + ".",
      recommendations: [
        "Monitor next week",
        "Plan weekend recovery",
        "Address emerging stressors early"
      ]
    };
  }
  
  return capacityTracking;
}
```

### Capacity Warning Display (Week End)

```
┌────────────────────────────────────────┐
│ ⚠️ CAPACITY WARNING                    │
├────────────────────────────────────────┤
│ This week's emotional capacity:        │
│                                        │
│ Average: 4.2 / 10 (LOW)                │
│ Lowest: 2.5 (VERY LOW - Tuesday AM)   │
│ Highest: 6.0 (Thursday Eve)            │
│                                        │
│ 📉 DECLINING TREND DETECTED            │
│ Started: 5.5 → Ended: 3.0              │
│                                        │
│ PERSISTENT STRESSORS (all week):       │
│ • Work overload (16/21 turns)          │
│ • Financial pressure (13/21 turns)     │
│                                        │
│ ⚠️ BURNOUT RISK: HIGH                  │
│                                        │
│ RECOMMENDATIONS FOR NEXT WEEK:         │
│ 1. Reduce work hours (batch less)     │
│ 2. Schedule 3+ recovery activities     │
│ 3. Address financial stress (priority) │
│ 4. Seek support from Sarah or Marcus   │
│                                        │
│ [Acknowledge] [Plan Recovery Week]     │
└────────────────────────────────────────┘
```

---

## Master Truths v1.2: Tension Hook Progression *(NEW)*

### Track Hook Payoff Timeline

**Core Principle:** Hooks planted at turn-level must pay off at appropriate intervals. Week-end validates all active hooks.

```javascript
function trackTensionHooks(weekState, activeHooks) {
  const hookTracking = {
    week_number: weekState.week_number,
    
    hooks_active_start: activeHooks.filter(h => h.status === "planted").length,
    hooks_paid_off: [],
    hooks_now_overdue: [],
    hooks_still_building: [],
    
    validation: {
      all_hooks_tracked: true,
      no_abandoned_hooks: true,
      payoff_quality_acceptable: true
    }
  };
  
  activeHooks.forEach(hook => {
    const weeksActive = weekState.week_number - hook.season_planted;
    
    if (hook.status === "resolved" && hook.payoff_week === weekState.week_number) {
      // PAID OFF THIS WEEK
      hookTracking.hooks_paid_off.push({
        hook_id: hook.hook_id,
        hook_type: hook.hook_type,
        weeks_active: weeksActive,
        payoff_quality: hook.payoff_quality_score,
        tension_created: hook.tension_score,
        player_satisfaction: hook.player_satisfaction || "unknown"
      });
    } else if (hook.status === "planted") {
      // STILL ACTIVE
      const expectedPayoffWeeks = hook.expected_payoff === "2-4 weeks" ? 4 : 8;
      const isOverdue = weeksActive > expectedPayoffWeeks;
      
      if (isOverdue) {
        hookTracking.hooks_now_overdue.push({
          hook_id: hook.hook_id,
          hook_type: hook.hook_type,
          weeks_active: weeksActive,
          expected_payoff: hook.expected_payoff,
          action_required: "MUST pay off next week or abandon"
        });
        
        // Mark hook as overdue
        hook.status = "overdue";
        hook.overdue_since_week = weekState.week_number;
      } else {
        hookTracking.hooks_still_building.push({
          hook_id: hook.hook_id,
          weeks_active: weeksActive,
          building_properly: true
        });
      }
    }
  });
  
  // Validation
  if (hookTracking.hooks_now_overdue.length > 0) {
    hookTracking.validation.no_abandoned_hooks = false;
    hookTracking.warning = {
      level: "MODERATE",
      message: `${hookTracking.hooks_now_overdue.length} tension hook(s) now overdue`,
      hooks: hookTracking.hooks_now_overdue.map(h => h.hook_id)
    };
  }
  
  const lowQualityPayoffs = hookTracking.hooks_paid_off.filter(h => h.payoff_quality < 0.7);
  if (lowQualityPayoffs.length > 0) {
    hookTracking.validation.payoff_quality_acceptable = false;
    hookTracking.quality_warning = {
      level: "LOW",
      message: "Some hook payoffs below quality threshold (0.7)",
      hooks: lowQualityPayoffs.map(h => h.hook_id)
    };
  }
  
  return hookTracking;
}
```

---

## Master Truths v1.2: NPC Capacity Tracking *(NEW)*

### Monitor NPC Availability Per Week

**Core Principle:** NPCs have fluctuating capacity. Week-end reports which NPCs are available for support vs. need support.

```javascript
function trackNPCCapacity(weekState, player) {
  const npcTracking = {
    week_number: weekState.week_number,
    npcs: []
  };
  
  player.relationships.forEach(rel => {
    const npc = rel.npc;
    
    // Calculate NPC's capacity trajectory this week
    const capacitySnapshots = weekState.days.flatMap(day => 
      day.turns
        .filter(t => t.interactions && t.interactions.some(i => i.npc_id === npc.id))
        .map(t => ({
          day: day.day_name,
          turn: t.phase,
          npc_capacity: t.npc_capacity_values && t.npc_capacity_values[npc.id]
        }))
    ).filter(s => s.npc_capacity);
    
    if (capacitySnapshots.length > 0) {
      const avgCapacity = capacitySnapshots.reduce((sum, s) => sum + s.npc_capacity, 0) / capacitySnapshots.length;
      const lowestCapacity = Math.min(...capacitySnapshots.map(s => s.npc_capacity));
      
      npcTracking.npcs.push({
        npc_id: npc.id,
        npc_name: npc.name,
        
        average_capacity: avgCapacity,
        lowest_capacity: lowestCapacity,
        
        // Support availability (capacity + 2 rule)
        can_support_level: avgCapacity + 2,
        
        // Status
        available_for_support: avgCapacity >= 6.0,
        needs_support_themselves: avgCapacity <= 4.0,
        struggling: lowestCapacity <= 3.0,
        
        // Recommendation
        interaction_advice: generateNPCInteractionAdvice(avgCapacity, rel.relationship_level)
      });
    }
  });
  
  return npcTracking;
}

function generateNPCInteractionAdvice(npcCapacity, relationshipLevel) {
  if (npcCapacity >= 7.0) {
    return {
      status: "HIGH_CAPACITY",
      advice: "Great time to seek support or deepen connection",
      can_handle: "Complex emotional conversations, crisis support"
    };
  } else if (npcCapacity >= 5.0 && npcCapacity < 7.0) {
    return {
      status: "MODERATE_CAPACITY",
      advice: "Available for moderate support, avoid heavy topics",
      can_handle: "Light conversations, routine social time"
    };
  } else if (npcCapacity >= 3.0 && npcCapacity < 5.0) {
    return {
      status: "LOW_CAPACITY",
      advice: "Limited availability, may need YOUR support instead",
      can_handle: "Brief check-ins only, be prepared to support them"
    };
  } else {
    return {
      status: "CRISIS_CAPACITY",
      advice: "Do NOT ask for support. They need help.",
      can_handle: "Nothing - offer support TO them if close enough"
    };
  }
}
```

### NPC Capacity Report (Week End)

```
┌────────────────────────────────────────┐
│ NPC CAPACITY REPORT - WEEK 5          │
├────────────────────────────────────────┤
│ 🟢 SARAH (HIGH CAPACITY 7.5/10)       │
│    ✓ Available for support             │
│    ✓ Can handle complex conversations  │
│    Great time to deepen friendship     │
│                                        │
│ 🟡 MARCUS (MODERATE 5.5/10)           │
│    ~ Limited availability              │
│    ~ Best for light social time        │
│    Avoid heavy emotional topics        │
│                                        │
│ 🔴 ELENA (LOW 3.0/10)                 │
│    ✗ Do NOT ask for support            │
│    ✗ She's struggling herself          │
│    Consider offering support TO her    │
│    (if relationship level permits)     │
│                                        │
│ NEXT WEEK PLANNING:                    │
│ • Lean on Sarah if you need support   │
│ • Keep things light with Marcus       │
│ • Check in on Elena (she may need you)│
└────────────────────────────────────────┘
```

---

## Master Truths v1.2: Weekly Quality Validation *(NEW)*

### Validate Week Met v1.2 Standards

**Core Principle:** Each week must pass quality thresholds for emotional authenticity, tension, and numerical grounding.

```javascript
function validateWeekQuality(weekState, player) {
  const validation = {
    week_number: weekState.week_number,
    
    scores: {
      emotional_authenticity: 0,
      tension_maintenance: 0,
      numerical_grounding: 0,
      
      overall_quality: 0
    },
    
    thresholds: {
      emotional_authenticity: 0.75,  // Week-level threshold
      tension_maintenance: 0.65,
      numerical_grounding: 1.0,       // REQUIRED
      
      overall_minimum: 0.70
    },
    
    passes: false,
    warnings: []
  };
  
  // SCORE 1: Emotional Authenticity
  const authenticityChecks = {
    capacity_constraints_respected: checkCapacityConstraints(weekState),
    npc_limitations_shown: checkNPCLimitations(weekState),
    circumstance_stacking_handled: checkCircumstanceStacking(weekState),
    ocean_consistent_behaviors: checkOCEANConsistency(weekState)
  };
  
  const authenticityScore = Object.values(authenticityChecks).filter(v => v === true).length / 4;
  validation.scores.emotional_authenticity = authenticityScore;
  
  // SCORE 2: Tension Maintenance
  const tensionChecks = {
    hooks_progressed: weekState.tension_hooks_progressed > 0,
    no_abandoned_hooks: weekState.tension_hooks_overdue === 0,
    new_hooks_planted: weekState.tension_hooks_planted > 0,
    mystery_maintained: weekState.information_debt_active > 0
  };
  
  const tensionScore = Object.values(tensionChecks).filter(v => v === true).length / 4;
  validation.scores.tension_maintenance = tensionScore;
  
  // SCORE 3: Numerical Grounding
  const groundingChecks = {
    all_trust_impacts_calculated: checkTrustCalculations(weekState),
    all_capacity_values_derived: checkCapacityDerivations(weekState),
    qualitative_anchors_referenced: checkQualitativeAnchors(weekState)
  };
  
  const groundingScore = Object.values(groundingChecks).filter(v => v === true).length / 3;
  validation.scores.numerical_grounding = groundingScore;
  
  // OVERALL SCORE
  validation.scores.overall_quality = 
    (validation.scores.emotional_authenticity * 0.40) +
    (validation.scores.tension_maintenance * 0.30) +
    (validation.scores.numerical_grounding * 0.30);
  
  // VALIDATION
  validation.passes = 
    validation.scores.emotional_authenticity >= validation.thresholds.emotional_authenticity &&
    validation.scores.tension_maintenance >= validation.thresholds.tension_maintenance &&
    validation.scores.numerical_grounding >= validation.thresholds.numerical_grounding &&
    validation.scores.overall_quality >= validation.thresholds.overall_minimum;
  
  if (!validation.passes) {
    if (validation.scores.emotional_authenticity < validation.thresholds.emotional_authenticity) {
      validation.warnings.push({
        category: "emotional_authenticity",
        score: validation.scores.emotional_authenticity,
        threshold: validation.thresholds.emotional_authenticity,
        issue: "NPCs not respecting capacity limits or OCEAN traits inconsistent"
      });
    }
    
    if (validation.scores.numerical_grounding < 1.0) {
      validation.warnings.push({
        category: "numerical_grounding",
        score: validation.scores.numerical_grounding,
        threshold: 1.0,
        issue: "CRITICAL: Missing formulas or qualitative anchors"
      });
    }
  }
  
  return validation;
}
```

---

## Week-Level Progression Tracking

### Aspiration Progress

```javascript
function updateWeeklyAspirationProgress(aspiration, weekState) {
  // Calculate progress based on activities
  let progress_this_week = 0;
  
  weekState.activities_completed.forEach(activity => {
    if (activity.contributes_to_aspiration) {
      progress_this_week += activity.progress_contribution;
    }
  });
  
  // Update aspiration
  aspiration.current_progress += progress_this_week;
  aspiration.weeks_active++;
  
  // Check milestones
  aspiration.milestones.forEach(milestone => {
    if (!milestone.completed && aspiration.current_progress >= milestone.threshold) {
      milestone.completed = true;
      milestone.completed_week = weekState.week_number;
      triggerMilestoneEvent(milestone, aspiration);
    }
  });
  
  // Check for completion
  if (aspiration.current_progress >= 100) {
    aspiration.status = "COMPLETED";
    aspiration.completed_week = weekState.week_number;
    triggerAspirationCompletion(aspiration);
  }
  
  return {
    progress_gained: progress_this_week,
    total_progress: aspiration.current_progress,
    milestones_reached: aspiration.milestones.filter(m => m.completed_week === weekState.week_number)
  };
}
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Weekly Mechanics (v1.1 Foundation)
- [x] 7 days per week
- [x] 21 turns per week (7 days × 3 turns)
- [x] Weekly time budget: 168 hours (53 flexible)
- [x] Routine batching available (player choice)
- [x] Weekday/weekend rhythm distinction
- [x] Weekly events appropriately paced
- [x] Relationship maintenance tracked weekly

### ✅ Master Truths v1.2: Capacity Fluctuation Tracking
- [x] **Weekly Capacity Tracking** (~90 lines)
  - Daily capacity snapshots collected per turn
  - Average, lowest, highest capacity calculated
  - Declining trend detection (first half vs. second half)
  - Burnout risk identification (10+ turns < 4.0 capacity)
  - Persistent stressor analysis (frequency tracking)
- [x] **Capacity Warning Display** at week end
- [x] **Intervention Recommendations** based on patterns
- [x] **Recovery Week Planning** when burnout risk high

### ✅ Master Truths v1.2: Tension Hook Progression
- [x] **Hook Tracking System** (~75 lines)
  - Track hooks planted, paid off, overdue
  - Validate payoff timelines (2-4 weeks, 5-8 weeks)
  - Mark hooks overdue if past expected payoff
  - Quality validation (payoff quality ≥ 0.7)
- [x] **Hook Status Monitoring** per week
- [x] **Payoff Quality Scoring** with warnings
- [x] **Abandoned Hook Detection** and warnings

### ✅ Master Truths v1.2: NPC Capacity Tracking
- [x] **NPC Capacity Monitoring** (~75 lines)
  - Track NPC capacity snapshots per interaction
  - Calculate average and lowest capacity per NPC
  - Support availability calculation (capacity + 2 rule)
  - Status classification (HIGH, MODERATE, LOW, CRISIS)
- [x] **Interaction Advice Generation** per NPC
- [x] **NPC Capacity Report Display** at week end
- [x] **Next Week Planning Recommendations** based on NPC states

### ✅ Master Truths v1.2: Weekly Quality Validation
- [x] **Quality Scoring System** (~90 lines)
  - Emotional Authenticity Score (threshold 0.75)
  - Tension Maintenance Score (threshold 0.65)
  - Numerical Grounding Score (threshold 1.0 - REQUIRED)
  - Overall Quality Score (threshold 0.70)
- [x] **Authenticity Validation** (capacity constraints, NPC limitations, OCEAN consistency)
- [x] **Tension Validation** (hooks progressed, no abandoned hooks, mystery maintained)
- [x] **Grounding Validation** (formulas exist, anchors referenced)
- [x] **Warning System** for failed checks

### ✅ Cross-References
- [x] Links to `71-daily-turn-flow-detailed.md` (turn-level capacity, hooks, dramatic irony)
- [x] Links to `74-multi-season-continuity-spec.md` (memory resonance, hook tracking)
- [x] Links to `11-turn-economy-implementation.md` (resource budgets)
- [x] Links to `master_truths_canonical_spec_v_1_2.md` Sections 16 & 17
- [x] This doc cites **Truths v1.2** at the top

**Total v1.2 Enhancements:** ~330 lines of weekly-level v1.2 mechanics

**References:**
- See `71-daily-turn-flow-detailed.md` for turn-by-turn gameplay with v1.2 mechanics
- See `11-turn-economy-implementation.md` for weekly resource budgets
- See `31-narrative-arc-scaffolding.md` for weekly narrative beats
- See `73-season-flow-implementation.md` for season-level flow
- See `74-multi-season-continuity-spec.md` for hook persistence and memory resonance
- See `master_truths_canonical_spec_v_1_2.md` Section 16 (Emotional Authenticity)
- See `master_truths_canonical_spec_v_1_2.md` Section 17 (Novel-Quality Narratives)

---

**This specification enables developers to implement the complete weekly gameplay cycle with capacity fluctuation tracking, tension hook progression monitoring, NPC capacity reporting, quality validation, resource management, event generation, routine batching, and progression tracking that meets Master Truths v1.2 standards.**

