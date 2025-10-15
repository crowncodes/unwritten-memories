# Progressive Disclosure UI System - Natural Information Architecture

## Core Principle: **"Show Glanceables, Reveal Depth"**

The UI should be **clean and breathable by default**, but any element can be **tapped once to expand into rich context**. Think of each cluster as a "book spine" that opens to reveal pages of detail.

---

## The 6 Core Clusters (Collapsed → Expanded)

### **Cluster 1: Character State** 
*"How am I doing right now?"*

#### Collapsed View (Always Visible)
```
┌─────────────────────┐
│  [Avatar]           │
│  MOTIVATED          │
│  Capacity: 7.2/10   │
└─────────────────────┘
```

#### Expanded View (Single Tap)
```
┌────────────────────────────────────────────────────┐
│  CHARACTER STATE                                   │
├────────────────────────────────────────────────────┤
│  [Avatar - larger]                                 │
│                                                    │
│  Primary: MOTIVATED (intensity: 0.75)              │
│  Secondary: ANXIOUS (intensity: 0.40)              │
│                                                    │
│  Emotional Capacity: 7.2/10 (HIGH)                 │
│  ├─ Base from meters: 7.8                          │
│  ├─ Stressor penalty: -0.6 (1 active)              │
│  └─ You can handle emotional demands right now     │
│                                                    │
│  Active Stressors (1):                             │
│  • Work deadline approaching (reduces -0.6)        │
│                                                    │
│  Burnout Level: 15/100 (Healthy)                   │
│  Recovery Rate: +0.5/week with current rest        │
│                                                    │
│  Recent Shifts:                                    │
│  • 3 days ago: DISCOURAGED → MOTIVATED             │
│    (after client approved portfolio)               │
│                                                    │
│  Memory Echo:                                      │
│  • This motivation reminds you of Week 4,          │
│    when Sarah first believed in your work          │
│                                                    │
│  💡 Maintain capacity by balancing work/rest       │
└────────────────────────────────────────────────────┘
```

---

### **Cluster 2: Life Meters**
*"How healthy are my core needs?"*

#### Collapsed View
```
┌──────────────┐
│ Physical: 7  │
│ Mental:   6  │
│ Social:   8  │
│ Emotional: 7 │
└──────────────┘
```

#### Expanded View
```
┌────────────────────────────────────────────────────┐
│  LIFE METERS                                       │
├────────────────────────────────────────────────────┤
│  Physical: ●●●●●●●○○○ 7/10 (Energized)             │
│  ├─ Regular exercise helping                       │
│  ├─ Passive decay: -0.5/week                       │
│  └─ ✓ Safe - will stay green for 8+ turns          │
│                                                    │
│  Mental: ●●●●●●○○○○ 6/10 (Stable)                   │
│  ├─ Work stress building                           │
│  ├─ Passive decay: -0.3/week                       │
│  └─ ⚠️ Warning at 2 if keep working hard            │
│     → Consider rest day or therapy                 │
│                                                    │
│  Social: ●●●●●●●●○○ 8/10 (Thriving)                 │
│  ├─ Regular connection with friends                │
│  ├─ Passive decay: -0.4/week                       │
│  └─ ✓ Excellent - can skip social for 2-3 weeks    │
│                                                    │
│  Emotional: ●●●●●●●○○○ 7/10 (Fulfilled)             │
│  ├─ Aspiration progress boosting                   │
│  ├─ Passive decay: -0.2/week                       │
│  └─ ✓ Strong - resilient to setbacks               │
│                                                    │
│  Restore Options:                                  │
│  • Rest Day → Physical +1, Mental +1               │
│  • Coffee with Sarah → Social +1, Emotional +1     │
│  • Therapy Session → Mental +2, Emotional +1.5     │
│                                                    │
│  🎯 Priority: Keep Mental above 5 this week         │
└────────────────────────────────────────────────────┘
```

---

### **Cluster 3: Progress & Story**
*"What am I working toward and what's happening?"*

#### Collapsed View
```
┌──────────────────────┐
│ 📸 Photography: 15%  │
│ 🎯 2 Active Hooks    │
│ Act I - Week 1       │
└──────────────────────┘
```

#### Expanded View
```
┌────────────────────────────────────────────────────┐
│  PROGRESS & STORY                                  │
├────────────────────────────────────────────────────┤
│  Current Aspiration:                               │
│  📸 Launch Photography Business                    │
│  Progress: ▓▓▓░░░░░░░ 15%                          │
│                                                    │
│  Recent Progress:                                  │
│  • Week 1: Portfolio reviewed (+5%)                │
│  • Week 1: Client approved work (+10%)             │
│                                                    │
│  Next Milestones:                                  │
│  • 25%: First paid gig completed                   │
│  • 50%: 5 regular clients established              │
│  • 100%: Sustainable monthly income                │
│                                                    │
│  Active Hooks (2):                                 │
│  1. ❓ Why has Sarah been distant? (5 weeks)       │
│     └─ Tension: Medium | Resolve: Week 8-10        │
│  2. 🎯 Gallery contact intro promised (2 weeks)    │
│     └─ Tension: Low | Resolve: Week 3              │
│                                                    │
│  Season Arc: Act I - Setup                         │
│  ▓▓▓░░░░░░ Week 1/3                                │
│  Next: Complication #1 emerging (Week 4)           │
│                                                    │
│  Upcoming Events:                                  │
│  • Week 2: Client meeting scheduled                │
│  • Week 3: Marcus introducing gallery contact      │
│                                                    │
│  Decisive Decisions Coming:                        │
│  • Week 6: Major choice approaching                │
│                                                    │
│  💡 Focus on building portfolio quality this week   │
└────────────────────────────────────────────────────┘
```

---

### **Cluster 4: Resources**
*"What do I have to work with?"*

#### Collapsed View
```
┌──────────────┐
│ ⚡ 8/10       │
│ ⏱️ 1.0h       │
│ 💰 $100       │
└──────────────┘
```

#### Expanded View
```
┌────────────────────────────────────────────────────┐
│  RESOURCES                                         │
├────────────────────────────────────────────────────┤
│  Energy: ⚡⚡⚡⚡⚡⚡⚡⚡ 8/10                           │
│  ├─ Max: 10 (Physical 7 = normal max)              │
│  ├─ Regeneration: +8 per day (after sleep)         │
│  └─ Today's usage: -2 (work activity)              │
│                                                    │
│  Time Remaining: ⏱️ 1.0 hours (this phase)          │
│  ├─ Morning phase total: 4 hours                   │
│  ├─ Used: 3 hours (work meeting, coffee)           │
│  └─ Afternoon phase: 4 hours available             │
│                                                    │
│  Money: 💰 $100                                     │
│  ├─ Rent due: Week 3 ($1,200)                      │
│  ├─ Weekly income: $400 (corporate job)            │
│  ├─ Savings goal: $5,000 (business fund)           │
│  └─ ⚠️ Need $1,100 more before rent                 │
│                                                    │
│  Weekly Budget:                                    │
│  Income:  +$400                                    │
│  Expenses: -$300 (food, transport, etc.)           │
│  Net: +$100/week                                   │
│                                                    │
│  Social Capital:                                   │
│  • Sarah: 12 (high - can ask favors)               │
│  • Marcus: 8 (good - occasional help)              │
│  • Boss: 4 (low - careful asking)                  │
│                                                    │
│  💡 Pick up freelance gig to boost rent fund        │
└────────────────────────────────────────────────────┘
```

---

### **Cluster 5: Relationships**
*"Who matters in my life?"*

#### Collapsed View
```
┌─────────────────┐
│ [S] [M] [A]     │
│  4   3   5      │
└─────────────────┘
```
*(S=Sarah, M=Marcus, A=Alex with tiny trust dots)*

#### Expanded View
```
┌────────────────────────────────────────────────────┐
│  KEY RELATIONSHIPS                                 │
├────────────────────────────────────────────────────┤
│  Sarah Chen - Best Friend (Level 4)                │
│  Trust: ●●●●○ 0.75                                 │
│  Social Capital: 12                                │
│  ├─ Last interaction: 2 days ago (coffee)          │
│  ├─ Relationship status: Strong, slight distance   │
│  ├─ Unresolved: Who is David? (mystery)            │
│  └─ Next: Check in about her quietness             │
│                                                    │
│  Marcus Webb - Close Friend (Level 3)              │
│  Trust: ●●●○○ 0.60                                 │
│  Social Capital: 8                                 │
│  ├─ Last interaction: 5 days ago (gym)             │
│  ├─ Promised: Gallery contact intro (this week)    │
│  ├─ Personality: Supportive, encouraging (E:4.7)   │
│  └─ Next: Follow up on gallery intro               │
│                                                    │
│  Alex Rivera - Romantic Interest (Level 5)         │
│  Trust: ●●●●● 0.90                                 │
│  Social Capital: 15                                │
│  ├─ Last interaction: Yesterday (dinner)           │
│  ├─ Relationship status: Soulmate level            │
│  ├─ Recent: Mentioned future plans together        │
│  └─ Next: Regular date planned (this week)         │
│                                                    │
│  ⚠️ At Risk:                                        │
│  • Sarah: 3+ weeks without deep conversation       │
│                                                    │
│  Recent Changes:                                   │
│  • Marcus: Trust +0.05 (supported your work)       │
│  • Alex: Level 4→5 (vulnerable conversation)       │
│                                                    │
│  Memory Spotlight:                                 │
│  • 3 weeks ago: Sarah said "These photos are       │
│    beautiful. You could really do this."           │
│    - That belief matters. Don't forget it.         │
│                                                    │
│  💡 Spend quality time with Sarah this week         │
└────────────────────────────────────────────────────┘
```

---

### **Cluster 6: Timeline & Context**
*"Where am I in the bigger picture?"*

#### Collapsed View
```
┌──────────────┐
│ Week 1, Day 1│
│ Monday       │
│ Act I: ●●○   │
└──────────────┘
```

#### Expanded View
```
┌────────────────────────────────────────────────────┐
│  SEASON TIMELINE                                   │
├────────────────────────────────────────────────────┤
│  Current: Week 1, Day 1, Monday - Morning          │
│  Season Length: 24 weeks (Extended)                │
│  Season Theme: Launch Photography Business         │
│                                                    │
│  Act Structure:                                    │
│  Act I: Setup (Weeks 1-6)                          │
│  ▓░░░░░ Currently here                             │
│  └─ Goals: Establish aspiration, build portfolio   │
│                                                    │
│  Act II: Complications (Weeks 7-18)                │
│  ░░░░░░░░░░░░                                      │
│  └─ Expected: 4-6 complications, 2-4 decisions     │
│                                                    │
│  Act III: Resolution (Weeks 19-24)                 │
│  ░░░░░░                                            │
│  └─ Expected: Climax decision, arc resolution      │
│                                                    │
│  This Week (Week 1):                               │
│  • Day 1: ← You are here                           │
│  • Day 3: Client meeting scheduled                 │
│  • Day 5: Sarah coffee date                        │
│  • Day 7: Week recap & reflection                  │
│                                                    │
│  Last Week Summary:                                │
│  • Season just started - fresh beginning           │
│                                                    │
│  Next Week Preview:                                │
│  • Week 2: Portfolio submission deadline           │
│  • Week 2: Marcus gallery intro                    │
│                                                    │
│  Tension Level: ▓▓░░░░░░░░ 3/10 (Low)              │
│  └─ Act I baseline - gentle hooks establishing     │
│                                                    │
│  Capacity Forecast:                                │
│  Current: 7.2 (High) ✓                             │
│  Projected Week 6: 6.0 (Moderate)                  │
│  └─ Should remain healthy through Act I            │
│                                                    │
│  💡 This week: Focus on building momentum           │
└────────────────────────────────────────────────────┘
```

---

## UI Implementation Strategy

### Visual Behavior
```typescript
interface Cluster {
  id: string;
  collapsedView: ReactNode;
  expandedView: ReactNode;
  position: Position;
  
  // Interaction
  isExpanded: boolean;
  onClick: () => toggleExpanded();
  
  // Animation
  expandAnimation: "slide-down" | "fade-in" | "modal";
  expandDuration: "200ms";
  
  // Priority
  collapseOthersOnExpand: boolean; // If true, only 1 cluster open at a time
}
```

### Layout Positions
```
Collapsed Layout:
┌────────────────────────────────────────────────────┐
│ [Character State]            [Life Meters]         │
│                              [Resources]           │
│                                                    │
│                                                    │
│            [SCENE BACKGROUND]                      │
│                                                    │
│                                                    │
│ [Progress/Story]             [Relationships]       │
│ [Timeline]                                         │
│                                                    │
│              [CARD HAND - FANNED]                  │
└────────────────────────────────────────────────────┘

Expanded Example (Character State):
┌────────────────────────────────────────────────────┐
│ ┌───────────────────────────┐    [Life Meters]    │
│ │ CHARACTER STATE           │    [Resources]       │
│ │ [Expanded details...]     │                      │
│ │ [Avatar, capacity...]     │                      │
│ │ [Stressors, burnout...]   │                      │
│ │ [Memory echoes...]        │                      │
│ │ [Suggestions...]          │                      │
│ └───────────────────────────┘                      │
│                                                    │
│            [SCENE BACKGROUND]                      │
│                                                    │
│ [Progress/Story]             [Relationships]       │
│ [Timeline]                                         │
│                                                    │
│              [CARD HAND - FANNED]                  │
└────────────────────────────────────────────────────┘
```

---

## Design Principles

### ✅ DO
- **Show glanceables by default** (just enough to monitor)
- **One tap to reveal depth** (all context available)
- **Provide actionable insights** (not just data dumps)
- **Include suggestions** ("💡 Try this...")
- **Reference memories** (connect to past)
- **Show cause-and-effect** ("Work stress → Mental -0.3")
- **Predict futures** ("Will hit critical in 3 turns if...")
- **Use progressive disclosure** (collapsed → expanded)

### ❌ DON'T
- Show all information at once (overwhelming)
- Require multiple clicks to access info (friction)
- Present raw numbers without context (confusing)
- Leave players wondering "why?" (always explain)
- Hide critical warnings (always visible)
- Make UI feel crowded (breathable space)

---

## Key Insight

**Every cluster is a "book" that opens:**
- **Spine (collapsed):** Title and status at a glance
- **Pages (expanded):** Full story with context, history, and guidance

This matches the "Life Bookshelf" metaphor perfectly - your life's details are always available, just a tap away, but never overwhelming.
