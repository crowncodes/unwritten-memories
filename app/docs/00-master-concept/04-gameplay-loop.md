# Gameplay Loop

**Document Status**: V3 Canonical Reference  
**Last Updated**: October 17, 2025  
**Authority Level**: Master Truth  
**Compliance**: Master Truths v3.0 (Predictive Pre-Fetching, CFP system)

---

## 1. Core Philosophy: Fluid Time, Real Choices

**The V1 Problem:**
- Rigid "Morning/Afternoon/Evening" phases
- Every day felt identical in structure
- Time felt gamified, not authentic

**The V2 Solution:**
- **Fluid time progression** based on actual activity duration
- **Flexible energy system** with debt mechanics
- **Adaptive granularity** where the AI decides what to zoom in on

**The Result:**
> Days feel like days. Long activities consume more time. Players manage a day, not fill three slots.

---

## 2. Time: The Continuous Timeline

### How Time Works

**Each day is a continuous 24-hour timeline:**
- Starts at character's wake time (typically 7:00 AM)
- Advances based on `time_cost` of played Action Cards
- Ends when character goes to sleep or reaches exhaustion

**Time Cost Examples:**
```
act_quick_coffee:        0.5 hours
act_gym_workout:         1.5 hours
act_social_dinner:       3.0 hours
act_weekend_trip:        48.0 hours (multi-day)
```

### The Daily Flow

**Example Day:**
```
07:00 - Wake up (Energy: 10)
07:30 - Play: act_morning_routine (0.5hr, -1 Energy)
08:00 - Play: act_commute_to_work (1hr, -1 Energy)
09:00 - Play: act_difficult_work_project (4hr, -3 Energy)
13:00 - Play: act_lunch_with_colleague (1hr, -1 Energy)
14:00 - Play: act_another_work_task (3hr, -2 Energy)
17:00 - Play: act_gym_workout (1.5hr, -2 Energy)
18:30 - Energy: 0
18:30 - Play: act_dinner_with_friend (2hr, -2 Energy)
20:30 - Energy: -2 (EXHAUSTED state applied)
20:30 - End day (collapse triggered)
```

**Key Properties:**
- Number of activities varies by duration chosen
- Player can fit 3 long activities or 10 short ones
- Energy constrains choices as day progresses
- Going into debt is possible but dangerous

---

## 3. Contextual Time-of-Day Filtering

### No More Rigid Phases

**Instead of:**
- Morning (3 slots)
- Afternoon (3 slots)
- Evening (3 slots)

**We have:**
- Contextual time categories as **tags**
- Cards are **suggested, not locked** by time
- AI filters card pool based on current time

### Time-of-Day Tags

**Each Action Card has preferred time tags:**

```json
{
  "card_id": "act_networking_event",
  "preferred_times": ["evening", "night"],
  "discouraged_times": ["early_morning", "late_night"]
}

{
  "card_id": "act_morning_run",
  "preferred_times": ["early_morning", "morning"],
  "discouraged_times": ["night", "late_night"]
}

{
  "card_id": "act_midnight_writing_session",
  "preferred_times": ["late_night"],
  "discouraged_times": ["morning", "afternoon"]
}
```

**Time Categories:**
- `early_morning`: 5:00 - 7:00
- `morning`: 7:00 - 12:00
- `afternoon`: 12:00 - 17:00
- `evening`: 17:00 - 21:00
- `night`: 21:00 - 23:00
- `late_night`: 23:00 - 5:00

**Filter Behavior:**
- Cards with matching `preferred_times`: **+50% draw chance**
- Cards with matching `discouraged_times`: **-80% draw chance**
- Cards with no time preference: **neutral chance**

**But not hard locks:**
- A player CAN go to the gym at 2 AM if they want
- A player CAN work late into the night
- The system suggests, doesn't dictate

---

## 4. Energy System: The Daily Budget

### Starting Energy

**Base daily energy:**
- Default: **10 points**
- Modified by perks and traits

**Modifiers:**
```
perk_morning_person:      +2 starting energy
perk_night_owl:           +0 but no late-night penalties
STATE_WELL_RESTED:        +3 starting energy
STATE_SLEEP_DEPRIVED:     -3 starting energy
```

### Energy Costs by Activity Type

**Energy costs can be fractional (0.5 increments) for fine-grained balance.**

**Low Energy (0.5-1.5 points):**
- Passive social (coffee, casual chat): 0.5-1 Energy
- Light entertainment (reading, casual gaming): 0.5-1 Energy
- Routine maintenance (meal prep, errands): 1-1.5 Energy
- Example: `act_morning_meditation` costs 0.5 Energy

**Medium Energy (2-2.5 points):**
- Active social (dinner party, group activity): 2 Energy
- Standard work tasks: 2 Energy
- Light exercise (yoga, walking): 1.5-2 Energy

**High Energy (3-4 points):**
- Intense work (difficult projects, deadlines): 3-4 Energy
- Vigorous exercise (running, gym): 2.5-3 Energy
- High-stakes social (first dates, networking events): 3 Energy
- Creative deep work: 3-4 Energy

**Personality Modifiers (can create fractional costs):**
```
act_networking_event (base: 2 Energy)
  + High Extraversion: -1 Energy (1 total)
  + Low Extraversion: +2 Energy (4 total)

act_coffee_with_friend (base: 1 Energy)
  + High Extraversion: -0.5 Energy (0.5 total)
  + Low Extraversion: +1 Energy (2 total)
```

---

## 5. The Energy Debt System

### Going Negative: A Dangerous Choice

**When Energy reaches 0:**
- Player is **not forced to end the day**
- Player can **continue playing cards**
- Each card pushes them into **negative Energy**
- Negative Energy applies **State Cards** with escalating penalties

**Why Allow This?**
> Authentic choice. Sometimes you MUST push through exhaustion (deadline, crisis, important event).

### The Debt Spiral

**Tier 1: Energy -1**
```
Apply: STATE_TIRED
Effects:
  - All actions: +1 Energy cost
  - All actions: -10% success rate
  - Narrative tone: "You're dragging. Everything feels harder."
```

**Tier 2: Energy -2**
```
Apply: STATE_EXHAUSTED
Effects:
  - All actions: +2 Energy cost
  - All actions: -20% success rate
  - Challenge activities locked
  - Narrative tone: "Your body is screaming for rest. Mistakes are inevitable."
```

**Tier 3: Energy -3 (Collapse Threshold)**
```
TRIGGER: Automatic "Collapse" Event
The character physically cannot continue.
```

### The Collapse Event

**What Happens:**
- Day immediately ends
- Location-specific narrative event generated
- Potential consequences based on context

**Context-Aware Outcomes:**

**If at work:**
- Boss notices you collapse at desk
- Option 1: Concerned conversation (+ relationship, but now they're watching)
- Option 2: Sent home (lose rest of day's productivity)
- Option 3: Embarrassment (- confidence, - professional reputation)

**If on a date:**
- Date is clearly ruined
- Relationship takes -2 damage
- NPC may be concerned OR turned off depending on personality

**If at home:**
- Wake up 12 hours later
- Miss important commitments (potential crisis events)
- Recover to Energy 5 (not fully rested)

**If at gym:**
- Risk of injury (apply STATE_INJURED)
- Stranger may help (random NPC meet-cute opportunity)

**The Design Intent:**
- Collapse is not "game over"
- It's a **narrative consequence** with real stakes
- It can be positive, negative, or mixed
- It's memorable

---

## 6. Adaptive Granularity: Zoom In or Montage

### The Pacing Problem

**Challenge:**
- Some activities are short and simple (coffee: 30 min)
- Some activities are long and complex (weekend trip: 48 hours)
- How do we handle both without breaking flow?

**The V2 Solution: Let the AI decide**

When a long-duration activity is played, the **Story Weaver assesses narrative significance** and presents pacing options to the player.

---

### Option 1: Narrative Summary (The Montage)

**When Used:**
- Low-stakes, routine activities
- Character is stable (Capacity healthy)
- No major relationship tests in progress
- Pacing Specialist says: "Safe to compress"

**Example: Weekend Camping Trip (Low Stakes)**

**AI Analysis:**
```
Context:
  - Relationship with friend: Solid (8/10)
  - No active crises
  - Capacity: 7.5 (healthy)
  - Recent pacing: Steady, could use light moment
  
Recommendation: NARRATIVE_SUMMARY
```

**Player Sees:**
```
┌─ WEEKEND CAMPING TRIP ──────────────────┐
│                                          │
│ This is a 48-hour activity.              │
│                                          │
│ The Story Weaver recommends:             │
│ 📖 NARRATIVE SUMMARY (quick)             │
│                                          │
│ "Play through the whole weekend as a     │
│  single scene with a summary."           │
│                                          │
│ [ Accept Summary ] [ Play It Out ]      │
└──────────────────────────────────────────┘
```

**If player accepts:**
```
You and Alex spend the weekend in the mountains.
The hike is challenging but rewarding. Around the
campfire, you share stories about your childhoods.
There's something peaceful about being away from
the city's noise.

When you return Sunday evening, you feel refreshed.

Outcomes:
  + Capacity: +0.8 (restful weekend)
  + Energy: Restored to 10
  + Relationship with Alex: +0.5 (quality time)
  + STATE_REFRESHED applied (3 days)
```

---

### Option 2: Granular Play (The Scene)

**When Used:**
- High-stakes situation
- Relationship test in progress
- Character is vulnerable (low Capacity)
- Pacing Specialist says: "This matters, zoom in"

**Example: Weekend Camping Trip (High Stakes)**

**AI Analysis:**
```
Context:
  - Relationship with Alex: Strained (4/10)
  - Recent fight unresolved
  - Capacity: 3.2 (vulnerable)
  - This trip was planned to "fix things"
  
Recommendation: GRANULAR_PLAY
```

**Player Sees:**
```
┌─ WEEKEND CAMPING TRIP ──────────────────┐
│                                          │
│ This is a 48-hour activity.              │
│                                          │
│ The Story Weaver recommends:             │
│ 🎬 GRANULAR PLAY (detailed)              │
│                                          │
│ "This weekend could define your          │
│  relationship. Play out the key moments."│
│                                          │
│ [ Accept Recommendation ] [ Skip It ]   │
└──────────────────────────────────────────┘
```

**If player accepts:**
- Game zooms in to **key scenes**
- Friday night: Setting up camp (initial tension)
- Saturday morning: The difficult conversation by the lake (decisive moment)
- Saturday night: Choice to share vulnerability or stay guarded
- Sunday morning: Resolution or lingering hurt

**Each scene presents choices**
**Relationship can be saved OR destroyed**
**Player feels in control of the outcome**

---

### Player Always Has Choice

**Important:**
- AI **recommends**, never forces
- Player can override: "I want to skip this" or "I want to play this out"
- System respects player preference for future similar events

---

## 7. The Day-to-Day Gameplay Rhythm

### The Core Loop (One Day)

```
1. WAKE UP
   └─> Energy restored (base 10)
   └─> Check State Cards (any persistent effects?)
   └─> Draw 7-card hand (contextually filtered)

2. MORNING DECISIONS
   └─> Play Action Cards
   └─> Time advances, Energy depletes
   └─> Hand refills after discard

3. MIDDAY EVENTS
   └─> Story Weaver may trigger Situation Card
   └─> Player makes choice
   └─> Consequences update state

4. AFTERNOON GRIND
   └─> Continue playing cards
   └─> Energy management becomes critical
   └─> Decisions about pushing limits

5. EVENING CHOICES
   └─> Low Energy: Safe activities or risk debt?
   └─> Social obligations vs. rest needs
   └─> Capacity considerations (can I support someone?)

6. END OF DAY
   └─> Option: "End Day Early" (go to sleep)
   └─> OR: Push into negative Energy
   └─> If collapse threshold: Automatic event

7. SLEEP
   └─> Day summary generated
   └─> Archive updated with today's events
   └─> Memory Facets generated for significant moments
       - Primary visible in day recap
       - Sensory/Observational stored for EWR analysis
   └─> Aspiration progress calculated
   └─> Tomorrow's context prepared
```

---

## 8. The Week-to-Week Rhythm

### The Routine Layer

**Weekly Routines auto-execute:**
- `rout_family_call_weekly` (every Sunday evening)
- `rout_meal_prep_sunday` (every Sunday morning)
- `rout_gym_three_times_week` (Monday/Wednesday/Friday)

**These create:**
- Predictable rhythm (like real life)
- Opportunities for disruption (missed routine = narrative hook)
- Background character development

**End of Week: EWR Narrative Analysis**
- Reviews all Memory Facets from week
- Detects patterns in Observational Facets
- Generates event seeds for next week
- See 09-turn-structure.md Section 6 for full process

**Routine Breach Events:**

**Example: Missing Family Call**
```
You meant to call your parents Sunday, but you
were too exhausted (collapsed at -3 Energy).

Monday morning:
[Situation Card Generated]

EVENT: Concerned Mother

"Your mom calls. 'You always call Sundays. Is
everything okay? You sound stressed lately...'"

Choices:
  [ ] Reassure her (requires 5.0+ Capacity)
  [ ] Dodge the conversation (-1 relationship)
  [ ] Open up about struggles (vulnerability moment)
```

---

## 9. The Season-to-Season Rhythm

### What Is a Season?

**Duration:** 12-16 in-game weeks (84-112 days)

**Structure:**
- Follows a 3-act narrative arc
- Driven by 3-5 active Aspirations
- Contains 8-12 major narrative events
- Ends with resolutions (success/failure/partial)

### The Season Arc

**Act 1: Setup (Weeks 1-4)**
- Choose Aspirations for season
- Establish routines
- Meet key NPCs
- Narrative Arc Specialist: "Introduce complications"

**Act 2: Complications (Weeks 5-10)**
- Aspirations encounter obstacles
- Situation Cards create tests
- Relationships evolve or strain
- Capacity likely drops (pressure builds)
- Narrative Arc Specialist: "Escalate stakes"

**Act 3: Resolution (Weeks 11-16)**
- Decisive moments for each Aspiration
- Major relationship turning points
- Capacity recovery or breakdown
- Narrative Arc Specialist: "Trigger climax and resolution"

### Inter-Season Transition

**Between seasons:**
1. **Season Recap** (AI-generated narrative summary)
2. **Archive Reflection** (review key moments)
3. **Character Growth** (new perks, evolved cards)
4. **New Aspirations** (choose next season's goals)
5. **Life Phase Check** (are you ready for new life stage?)

---

## 10. Long-Duration Activities

### Multi-Day Events

**Activities that span days:**
- Weekend trips (48 hours)
- Vacations (168+ hours)
- Intensive courses (80 hours over 2 weeks)
- Illness recovery (variable)

**How They Work:**

**Option A: Narrative Summary**
- Entire activity compressed into one scene
- Outcomes calculated
- Time advances in one jump

**Option B: Check-In Points**
- AI identifies key decision moments within the activity
- Player plays 3-5 "beats" across the duration
- Time advances between beats

**Example: One-Week Vacation**

**Granular Play Mode:**
```
Beat 1: Day 1 - Arrival (set tone)
  └─> Skip Days 2-3 (summary: "You spent two days relaxing")
Beat 2: Day 4 - Midpoint Event (complication)
  └─> Skip Day 5 (summary: "You processed what happened")
Beat 3: Day 6 - Resolution moment
Beat 4: Day 7 - Return home (reflection)
```

**Player plays 4 scenes across 7 days**
**Feels complete but not tedious**

---

## 11. The Hand Management System

### The 7-Card Hand

**Rules:**
- Always maintain **7 cards**
- Drawn from **contextually filtered pool**
- **Discard unused cards** at end of turn
- **No card hoarding** (can't save cards for later)

**Why 7?**
- Large enough for meaningful choice
- Small enough to not overwhelm
- Forces prioritization

### Refilling the Hand: Predictive Pre-Fetching

**⚠️ V3 SYSTEM: Not Simple 1-for-1 Replacement**

**When cards are played:**
1. Card is discarded from hand (hand size decreases)
2. If hand drops to **4 cards remaining** → **Trigger Pre-Fetch**
3. Pre-fetch generates 3-4 cards in parallel and holds in buffer
4. Next card played → Instantly replenished from buffer (0ms perceived latency)

**Pre-Fetch System Details:**
- **Trigger Point**: Hand size drops to 4 cards
- **Buffer Size**: 3-4 cards ready
- **Generation**: Batch process (Tier 1 instant, Tier 2 batched EWR call)
- **Target Hit Rate**: >95% (buffer ready when needed)
- **Player Experience**: Seamless, instant replenishment
- **Fallback**: If buffer empty (rare <5%), use Tier 1 instant generation

**Technical Flow:**
```
Hand: 7 → Play card → 6 cards (no action)
Hand: 6 → Play card → 5 cards (no action)
Hand: 5 → Play card → 4 cards (TRIGGER PRE-FETCH IN BACKGROUND)
  └─> Server: CFP update + weighted draw + batch generate 3-4 cards
  └─> Buffer: 3-4 cards ready in 1-3 seconds
Hand: 4 → Play card → Add from buffer → 4 cards (instant from buffer)
Hand: 4 → Play card → Add from buffer → 4 cards (instant from buffer)
```

**Why This System?**
- Masks Tier 2 cloud generation latency (1-3 seconds)
- Player decision time (5-15 seconds) allows pre-fetch to complete
- Batch generation reduces cost (~50% token savings)
- Seamless experience (feels instant)

**See:** `09-turn-structure.md` Section 4 for complete technical specification

**At end of day:**
1. Discard all remaining cards
2. Clear pre-fetch buffer
3. Draw fresh 7-card hand next morning
4. Filtering recalculated based on new context

**Why No Card Saving?**
- Prevents hoarding "best" cards
- Forces engagement with current options
- Mimics real life (you can't save "having coffee" for later)

---

## 12. Critical Design Rules

### Rule 1: Time Is Continuous, Not Discrete
- No "turns" or "rounds"
- Time advances smoothly based on actions
- Days vary in length (5 activities vs. 15 activities)

### Rule 2: Energy Is Resource, Not Timer
- Energy gates actions but doesn't end the day
- Debt is possible and sometimes necessary
- Collapse is narrative, not failure

### Rule 3: AI Curates, Player Decides
- AI recommends summary vs. granular
- Player can always override
- System learns player preferences

### Rule 4: Routine Creates Rhythm
- Auto-executing routines provide structure
- Disrupted routines create narrative opportunities
- Routines can evolve into cherished rituals

### Rule 5: Every Day Should Feel Different
- Card filtering creates variety
- State Cards change available options
- NPC availability is dynamic
- Story Weaver injects surprise

---

## 13. Example: Full Day Walkthrough

**Character:** Maya (Age 24, High Neuroticism, Low Extraversion)
**Current State:** Capacity 4.5 (Vulnerable), Energy 10, No State Cards
**Active Aspiration:** "Get Promoted to Senior Designer"
**Season:** Act 2 (Week 7, complications phase)

---

**07:00 - Wake Up**
```
Energy: 10
Hand drawn (filtered by: morning, introspective preference, work pressure)

Your Hand:
1. act_morning_meditation (0.5hr, -0.5 Energy) [TIME MATCH]
2. act_prepare_presentation (2hr, -2 Energy)
3. act_commute_to_work (1hr, -1 Energy) [TIME MATCH]
4. act_coffee_with_sarah (1.5hr, -1 Energy)
5. act_procrastinate_online (1hr, -0.5 Energy)
6. act_call_mentor_for_advice (0.75hr, -1 Energy, -0.3 Capacity)
7. act_go_back_to_sleep (2hr, +2 Energy) [DISCOURAGED]
```

**Maya's player chooses:** `act_morning_meditation`
- Time: 07:30
- Energy: 9.5
- Capacity: 4.7 (+0.2 from meditation)

---

**07:30 - Morning Continues**
```
New card drawn (replaces meditation)

Your Hand:
1. act_prepare_presentation (2hr, -2 Energy)
2. act_commute_to_work (1hr, -1 Energy) [TIME MATCH]
3. act_coffee_with_sarah (1.5hr, -1 Energy)
4. act_procrastinate_online (1hr, -0.5 Energy)
5. act_call_mentor_for_advice (0.75hr, -1 Energy, -0.3 Capacity)
6. act_go_back_to_sleep (2hr, +2 Energy) [DISCOURAGED]
7. act_nervous_pacing (0.5hr, -1 Energy) [NEW]
```

**Maya's player chooses:** `act_commute_to_work`
- Time: 08:30
- Energy: 8.5

---

**08:30 - At Work**
```
[SITUATION CARD TRIGGERED BY STORY WEAVER]

EVENT: Last-Minute Meeting Announcement

Your boss just sent an email: "Team meeting at 2 PM
to review everyone's progress on the redesign project.
Be ready to present your work."

Your presentation is half-finished. You have 5.5 hours.

High Neuroticism perception: This feels CRITICAL.

Choices:
[ ] Panic-work on presentation (5hr, -4 Energy, -0.4 Capacity)
[ ] Ask boss if you can present next week (requires 5.5+ Capacity) [LOCKED]
[ ] Work on it, accept it won't be perfect (3hr, -2 Energy)
[ ] Fake being sick and go home (avoid, -2 Capacity guilt)
```

**Maya's player chooses:** Panic-work (High Neuroticism amplified fear)
- Time: 13:30
- Energy: 4.5
- Capacity: 4.3

---

**13:30 - Pre-Meeting**
```
Your presentation is done, but you're exhausted.

[SMALL SITUATION CARD]

Sarah (coworker) stops by: "Hey, want to grab lunch
before the meeting? You look stressed."

Capacity check: 4.3 (Vulnerable range)
Sarah's Capacity: 7.2
Can she support you? 7.2 + 2 = 9.2 > your stress (3)
✅ Sarah can help

Choices:
[ ] Yes, talk to Sarah about your stress (1hr, -1 Energy, +0.5 Capacity)
[ ] No, stay at desk and review notes (0.5hr, -0.5 Energy)
```

**Maya's player chooses:** Talk to Sarah
- Time: 14:30
- Energy: 3.5
- Capacity: 4.8 (Sarah helped!)
- Relationship with Sarah: +0.3 (vulnerability shared)

---

**14:30 - The Meeting**
```
[ASPIRATION MILESTONE EVENT]

The presentation goes... okay.

Your boss: "Good start, Maya. But I expected more
depth here. Can you revise and present again Friday?"

Result: Partial success
  - Not a disaster
  - But not the breakthrough you needed
  - More work required

Aspiration Progress: +15% (milestone hit, but not cleanly)

Maya's Neuroticism: "You failed. Everyone thinks you're incompetent."

Capacity: 4.8 → 4.0 (perceived failure, even though objective was "okay")
```

---

**16:00 - Late Afternoon**
```
Energy: 3.5 (getting low)
Capacity: 4.0 (vulnerable)

Hand refreshed:

Your Hand:
1. act_stay_late_revise_presentation (3hr, -3 Energy) [RISKY - would hit 0.5]
2. act_comfort_food_binge (1hr, -0.5 Energy, -0.3 Capacity)
3. act_call_best_friend (1hr, -1 Energy, requires 4.5 Capacity) [LOCKED]
4. act_go_to_gym (1.5hr, -2 Energy) [DISCOURAGED - tired]
5. act_go_home_early (0.5hr, -0.5 Energy, +1 Capacity rest at home)
6. act_scroll_phone_numbly (0.5hr, -0.5 Energy)
7. act_cry_in_bathroom (0.25hr, -0.5 Energy, +0.2 Capacity release)

STORY WEAVER NOTE:
"Character is vulnerable. Consider rest or support seeking.
 Pushing further risks breakdown."
```

**Maya's player chooses:** Go home early
- Time: 17:00
- Energy: 3.0
- Capacity: 5.0 (rest helped)

---

**17:00 - Home**
```
Energy: 3.0 (enough for a couple more activities)

Your Hand (filtered: evening, home, restorative preference):
1. act_cook_comfort_meal (1hr, -1 Energy, +0.3 Capacity)
2. act_watch_mindless_tv (2hr, -0.5 Energy, +0.2 Capacity)
3. act_journal_about_feelings (1hr, -1 Energy, +0.4 Capacity)
4. act_text_sarah_thanks (0.25hr, -0.5 Energy)
5. act_work_on_presentation_at_home (2hr, -2 Energy, -0.5 Capacity)
6. act_early_bedtime (4hr, -0 Energy, +1 Capacity tomorrow)
7. act_online_shopping_therapy (1hr, -1 Energy, -$50)
```

**Maya's player chooses:** Cook comfort meal + Journal
- Time: 19:00
- Energy: 1.0
- Capacity: 5.7

---

**19:00 - Evening**
```
Energy: 1.0 (very low)

Maya could:
  - Push into negative Energy (risky)
  - End day early (safe)

Player chooses: End Day Early

[DAY SUMMARY GENERATED]

Today was challenging. The meeting didn't go
as you hoped, and your confidence took a hit.
But Sarah's support reminded you that you're
not alone in this. Tomorrow, you'll try again.

Progress:
  - Aspiration "Get Promoted": 52% → 67%
  - Relationship with Sarah: 6.5 → 6.8
  - Capacity: 5.7 (recovering)

Archive updated with 8 new memories.

[SLEEP]
```

---

**The Day's Narrative Arc:**
1. Started vulnerable but stable
2. Crisis injected (surprise meeting)
3. Character's personality shaped response (panic-work)
4. Support from NPC helped (Sarah)
5. Mixed outcome (okay but not great)
6. Character chose rest over pushing
7. Day ended with reflection

**Authentic experience of anxiety, work pressure, and friendship.**

---

## Conclusion

The gameplay loop is designed to feel like **living a life**, not playing a game:

✅ **Time flows naturally** (not in rigid phases)  
✅ **Energy constraints are realistic** (you can push, but you pay)  
✅ **The AI zooms in on what matters** (not every moment is equal)  
✅ **Routines create rhythm** (structure that can be disrupted)  
✅ **Every day feels different** (contextual filtering prevents repetition)  

The result: **A life simulation that feels authentic, reactive, and deeply personal.**

