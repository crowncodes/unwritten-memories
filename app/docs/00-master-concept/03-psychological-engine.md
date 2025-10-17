# Psychological Engine

**Document Status**: V2 Canonical Reference  
**Last Updated**: October 16, 2025  
**Authority Level**: Master Truth

---

## 1. Core Philosophy: Simulate the Inner World

The psychological engine is what makes Unwritten feel **authentic** rather than gamified. It simulates not just what a character does, but **how they experience their life**.

**The Key Insight:**
> Reality is objective. Experience is subjective. Unwritten simulates both.

Two characters facing the same event will perceive, process, and respond differently based on their personality and current mental state. This is the heart of emergent narrative.

---

## 2. The Dual Resource System

### Energy: The Fast-Moving Resource

**What It Represents:**
- Daily physical and mental stamina
- Immediate capacity to act

**Mechanical Properties:**
- **Starting value**: 10 points per day (base)
- **Restores**: Full reset every midnight
- **Modified by**: Perks (`morning_person` +2), State Cards (`DRAINED` -3)
- **Costs**: Individual activities consume 1-4 Energy

**The Energy Debt System:**

**Entering Debt (Negative Energy):**
- Player can play cards even at 0 Energy
- Each action beyond 0 pushes character into negative values
- **This is not a hard stop—it's a dangerous choice**

**Consequences of Debt:**
```
Energy: -1 → Apply STATE_TIRED
  - +1 Energy cost to all actions
  - -10% success rate
  
Energy: -2 → Apply STATE_EXHAUSTED  
  - +2 Energy cost to all actions
  - -20% success rate
  - Cannot perform Challenge activities
  
Energy: -3 → TRIGGER EVENT: Collapse
  - Forced narrative event
  - Location-specific consequences
  - Potential NPC reactions
```

**Why This Matters:**
- Players can push themselves in emergencies (authentic)
- But there are real, escalating consequences (authentic)
- The collapse is a narrative moment, not a game over screen (emergent storytelling)

---

### Emotional Capacity: The Slow-Moving Resource

**What It Represents:**
- Long-term psychological resilience
- Ability to handle stress, support others, and engage emotionally

**Mechanical Properties:**
- **Range**: 0.0 - 10.0 (float, precise tracking)
- **Starting value**: 7.0 (healthy baseline)
- **Decay rate**: Very slow (~0.1 per major crisis)
- **Recovery rate**: Very slow (~0.2 per major positive milestone)

**Critical Distinction from Energy:**
> A character can wake up with full Energy (10) but have critically low Capacity (2.0).

**This represents:**
- "I can physically go to work today"
- "But I'm one bad email away from a breakdown"

**The Capacity Zones:**

```
10.0 - 8.0: THRIVING
  - Full perception abilities
  - Can support others effectively
  - Bonus to growth activities
  
7.9 - 5.0: STABLE
  - Normal functioning
  - Standard perception
  - Can give and receive support
  
4.9 - 3.0: VULNERABLE
  - Reduced perception (miss subtle cues)
  - Limited ability to help others
  - Increased cost for emotional activities
  
2.9 - 1.0: FRAGILE
  - Major perception penalties
  - Cannot effectively support others
  - Most empathetic options locked
  - High risk of breakdown
  
0.9 - 0.0: BREAKDOWN
  - Automatic crisis event triggered
  - Intervention required
  - All non-essential activities locked
```

---

## 3. Personality as Perceptual Filter

### The OCEAN Model Integration

Unwritten uses the **Big Five (OCEAN)** personality model:
- **O**penness to Experience
- **C**onscientiousness  
- **E**xtraversion
- **A**greeableness
- **N**euroticism

**Each trait is a 0.0 - 1.0 float value**

### How Personality Shapes Perception

**Same Objective Event, Different Subjective Experience:**

#### Example: Upcoming Work Presentation

**Objective Tension Level**: `PRESSURE` (medium stakes)

**High Neuroticism Character (0.8):**
- **Perceives as**: `URGENT` or `CRITICAL`
- **Narrative text**: "Your heart races. This could ruin everything. What if you freeze up? What if they hate it?"
- **Available options**: "Overprepare until 2 AM," "Cancel and call in sick," "Ask mentor for emergency help"

**Low Neuroticism Character (0.2):**
- **Perceives as**: `CONCERN` (mild)
- **Narrative text**: "You've got a presentation tomorrow. It should go fine if you prep tonight."
- **Available options**: "Practice for an hour," "Review notes," "Get a good night's sleep"

**The Mechanical Implementation:**

```
objective_tension_level = calculate_stakes(situation)

if character.neuroticism >= 0.7:
    perceived_tension = objective_tension_level + 2
elif character.neuroticism <= 0.3:
    perceived_tension = objective_tension_level - 1
else:
    perceived_tension = objective_tension_level

narrative_tone = get_tone_for_tension(perceived_tension)
available_actions = filter_by_perception(all_actions, perceived_tension)
```

**Why This Is Revolutionary:**
- The game world doesn't change—**your experience of it does**
- Personality is not a stat bonus—**it's a lens**
- High Neuroticism is not a penalty—**it's a different reality**

---

## 4. Capacity-Limited Perception

### The Empathy Gate

**Core Rule:**
> **You can only perceive and respond to what you have the Capacity to hold.**

When Emotional Capacity drops below certain thresholds, the character **cannot see** social cues, emotional subtext, or opportunities to help others.

#### Example: A Friend in Crisis

**Setup:**
- Your friend Sarah is struggling after losing her job
- She reaches out: "Hey, want to grab coffee?"

**High Capacity Character (7.0+):**
- **Perceives**: "She sounds off. Something's wrong."
- **Available responses**:
  - "Of course. Want to talk about what's going on?" (empathetic)
  - "Sure, I've been meaning to catch up." (supportive)
  - "I'm pretty busy, but I can make time." (honest but present)

**Low Capacity Character (2.5):**
- **Perceives**: "Sarah wants coffee."
- **Available responses**:
  - "Sure, but I can only do 30 minutes." (oblivious)
  - "I'm swamped, can we do next week?" (dismissive)
  - ~~"Of course. Want to talk about what's going on?"~~ (LOCKED)

**Note on Narrative Priming:** 
Even with high Narrative Priming (VolatilityIndex), locked options remain locked. Priming modifies outcome probabilities WITHIN available choices, not available choices themselves. Capacity gates are non-negotiable boundaries that Priming respects.

**UI Treatment of Locked Options:**

```
[ ] "Of course. Want to talk about what's going on?"
    🔒 CAPACITY TOO LOW
    "You're too overwhelmed by your own problems to have 
     the emotional bandwidth for this conversation."
```

**The Narrative Consequence:**
- Player is forced to choose a tone-deaf response
- Sarah feels dismissed
- Relationship takes damage
- **This is not a "wrong choice"—it's an authentic limitation**

**The Meta-Experience:**
- Player understands: "I couldn't help her because I'm not okay"
- This creates empathy for real-world situations
- Reinforces the need for self-care before supporting others

---

## 5. The "Capacity + 2" Rule for NPC Support

### NPCs Have Limits Too

**Core Mechanic:**
> **An NPC can only effectively support a crisis if (NPC Capacity + 2) > Crisis Level**

#### Example: Seeking Support After Job Loss

**Your Crisis:**
- `evt_job_loss` (Crisis Level: 5)
- Your Capacity drops to 3.0
- You need support

**Sarah's Current State:**
- Sarah's Capacity: 6.5
- Can she help? `6.5 + 2 = 8.5 > 5` ✅ **YES**

**Sarah's Response:**
- She has the bandwidth
- Provides effective support
- Your Capacity recovers +0.5
- Relationship deepens (vulnerability shared)

---

**Alternative Scenario:**

**Sarah's Current State:**
- Sarah's Capacity: 2.8 (she's also struggling)
- Can she help? `2.8 + 2 = 4.8 < 5` ❌ **NO**

**Sarah's Response:**
- "I'm so sorry... I wish I could be there for you right now."
- "I'm barely holding it together myself."
- Shared moment of vulnerability
- No Capacity recovery for you
- Relationship can deepen or strain depending on player response

**The Beautiful Tension:**
- Support is not guaranteed
- NPCs are not vending machines
- This creates authentic, complex relationships
- Sometimes nobody can help, and that's the story

---

## 6. Personality Modifiers on Actions

### How OCEAN Traits Affect Gameplay

Every Action Card is modified by relevant personality traits. This is not just "+10% success"—it's **fundamental changes to cost and experience**.

#### Example: `act_networking_event`

**Base Costs:**
- Time: 3 hours
- Energy: 2
- Money: $20
- Emotional Capacity: 0.5

**High Extraversion (0.8) Modifier:**
- Energy cost: **-1** (energizing, not draining)
- Success rate: **+30%**
- Narrative tone: "You're in your element. Meeting new people excites you."

**Low Extraversion (0.2) Modifier:**
- Energy cost: **+2** (exhausting)
- Capacity cost: **+0.3** (emotionally draining)
- Success rate: **-10%**
- Narrative tone: "Small talk feels like wading through mud. You count the minutes until you can leave."

**The Result:**
- Extraverts are encouraged to network (it's energizing!)
- Introverts can still network but pay a real price
- Neither is "wrong"—both are authentic to personality

---

#### Example: `asp_write_novel` (Long-term Aspiration)

**Base Difficulty:** High (multi-month commitment)

**High Openness (0.8) + High Conscientiousness (0.8):**
- **Ideal personality combination**
- Progress rate: **+40%**
- Narrative: "The words flow. You've found your rhythm."

**High Openness (0.8) + Low Conscientiousness (0.2):**
- **Creative but undisciplined**
- Progress rate: **-20%**
- Special mechanics: "Inspiration Bursts" (rapid progress) followed by "Motivation Droughts" (stalls)
- Narrative: "You write 5,000 words in a frenzy, then don't touch it for two weeks."

**Low Openness (0.3) + High Conscientiousness (0.8):**
- **Disciplined but uninspired**
- Progress rate: **-30%**
- Different failure mode: "Technically competent but lifeless prose"
- Narrative: "You hit your daily word count, but reading it back feels like chewing cardboard."

**The Design Lesson:**
- Personality doesn't just modify difficulty
- It changes **how** you experience the challenge
- It creates different failure modes and success paths
- Some goals are just harder for some personalities (authentic)

---

## 7. State Cards: Persistent Conditions

### What Are State Cards?

**State Cards are not played—they are applied.**

They represent ongoing conditions that affect the character until resolved.

### The State Card Panel (UI)

**Dedicated UI space showing:**
- Active State Cards
- Duration (if time-limited)
- Current effects (hover for details)

**Example Display:**
```
┌─ ACTIVE CONDITIONS ─────────────┐
│ 😰 OVERWHELMED                  │
│    - +50% Energy costs          │
│    - -20% success rates         │
│    - Filters toward rest        │
│                                  │
│ 💔 GRIEVING (8 days remaining)  │
│    - -2 Capacity                │
│    - Filters out parties        │
│    - Unlocks memorial actions   │
│                                  │
│ 💪 INSPIRED (3 days remaining)  │
│    - +30% creative success      │
│    - -1 Energy for art actions  │
└──────────────────────────────────┘
```

### How State Cards Are Applied

**By Events:**
- `evt_relationship_breakup` → applies `STATE_GRIEVING`
- `evt_health_crisis` → applies `STATE_INJURED`
- `evt_creative_breakthrough` → applies `STATE_INSPIRED`

**By Threshold Triggers:**
- Capacity drops below 3.0 → applies `STATE_VULNERABLE`
- Energy hits -2 → applies `STATE_EXHAUSTED`
- Work stress accumulates → applies `STATE_BURNOUT`

**By NPC Actions:**
- Mentor gives encouragement → applies `STATE_MOTIVATED`
- Friend betrays trust → applies `STATE_DISTRUSTFUL`

### State Card Stacking

**Multiple State Cards interact multiplicatively:**

```
Base action: act_difficult_work_project
  - Energy cost: 3
  - Success rate: 60%

Active states:
  - STATE_OVERWHELMED: +50% costs, -20% success
  - STATE_EXHAUSTED: +67% costs, -20% success
  
Final calculation:
  - Energy cost: 3 × 1.5 × 1.67 = 7.5 (rounds to 8)
  - Success rate: 60% × 0.8 × 0.8 = 38.4%
  
Narrative outcome:
  "This task feels insurmountable. In your current state,
   attempting this is nearly futile."
```

**The Design Intent:**
- Circumstance stacking is mechanized
- "When it rains, it pours" is systemic, not narrative fluff
- Players must prioritize resolving conditions, not pushing through

---

## 8. The Perception → Action → Consequence Loop

### How It All Connects

```
1. OBJECTIVE SITUATION
   └─> Modified by Personality (Neuroticism)
       └─> SUBJECTIVE PERCEPTION
           └─> Filtered by Capacity
               └─> AVAILABLE ACTIONS
                   └─> Modified by State Cards & Personality
                       └─> CHOSEN ACTION
                           └─> OUTCOME
                               └─> Updates Capacity & State
                                   └─> LOOP CONTINUES
```

### Example: Full Loop

**Setup:**
- Character has Low Capacity (3.2) and High Neuroticism (0.7)
- Objective event: Boss requests meeting

**1. Objective Situation:**
- Meeting request (neutral event)

**2. Personality Filter (High Neuroticism):**
- Amplifies perceived threat
- "What did I do wrong? Am I getting fired?"

**3. Capacity Filter (Low Capacity):**
- Locks calm, rational responses
- Only anxious, defensive options available

**4. Available Actions:**
- "Panic and overprepare for every possible bad scenario"
- "Avoid by calling in sick"
- ~~"Ask directly what the meeting is about"~~ (LOCKED - requires 5.0+ Capacity)

**5. Player Chooses:** "Panic and overprepare"
- Costs: 4 Energy, 0.3 Capacity (exhausting, stressful)

**6. Outcome:**
- Meeting was about a promotion
- Boss notices character seems stressed
- Mixed result: Good news, but character's anxiety is now visible to authority figure

**7. Capacity Update:**
- Good news: +0.4 Capacity (relief)
- But boss concern: -0.1 Capacity (embarrassment)
- Net: +0.3 Capacity (now 3.5)

**8. New State:**
- If this pattern repeats, may apply `STATE_ANXIOUS_REPUTATION`
- This affects future workplace interactions

**The Meta-Lesson:**
- Personality shapes perception
- Capacity limits responses
- Choices have layered consequences
- Character behavior becomes reputation
- **The loop is the story**

---

## 9. Critical Design Rules

### Rule 1: Perception Is Reality
- Never tell the player "you're wrong to feel this way"
- If Neuroticism says it's urgent, **it IS urgent for that character**
- Validate subjective experience

### Rule 2: Limitations Create Stories
- Locked dialogue options are not failures
- Being "too tired to help" is a narrative beat, not a bug
- Breakdowns are story turning points

### Rule 3: NPCs Have Inner Worlds
- Every NPC has Capacity
- Every NPC has personality
- NPCs are not quest givers—they're characters

### Rule 4: Recovery Is Slow and Earned
- Capacity doesn't rebound from one nap
- Major recovery requires resolution (completing Aspiration, resolving crisis, therapy)
- Respect the weight of psychological damage

### Rule 5: The System Serves the Story
- All mechanics exist to create authentic narrative
- If a calculation feels wrong, trust the narrative intent
- Mathematics serve emotion, not the reverse

---

## 10. The Psychological Engine's Promise

**What This System Creates:**

✅ **Characters feel psychologically authentic**
- You understand why they made that choice
- Their limitations make sense
- Their growth feels earned

✅ **Stories feel emotionally real**
- Consequences reflect actual human experience
- Relationships have natural complexity
- Crises have lasting impact

✅ **Replayability through personality**
- Same events, completely different experience
- High Neuroticism playthrough ≠ Low Neuroticism playthrough
- Each personality is a new lens on life

✅ **Player empathy and insight**
- "Oh, this is what anxiety feels like systemically"
- "I couldn't help because I wasn't okay first"
- "Personality isn't good or bad—it's just different"

**The Ultimate Goal:**

> When a player finishes a life in Unwritten, they shouldn't just remember what happened. They should understand **why** it happened, **what it felt like**, and **who their character truly was**.

The psychological engine makes that possible.

