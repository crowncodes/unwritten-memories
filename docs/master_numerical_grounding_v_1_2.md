# Numerical Grounding & Calibration Guide

**Compliance:** `master_truths_canonical_spec_v_1_2.md` (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Establish qualitative anchors for all quantitative scales to enable consistent numerical assignments

---

## The Problem

Throughout the documentation, you'll see numbers like:
- Trust impact: `-0.2` vs `-1.8`
- Emotional capacity: `2.5/10` vs `6.85/10`
- Meter recovery: `+1` vs `+3`
- Quality scores: `0.7` vs `0.9`

**Question:** How do you determine which number to use?

**Answer:** You need **qualitative anchors** - descriptions of what each number *means* experientially.

---

## Core Principle: Anchor → Calculate → Validate

### The Three-Step Process

```
1. ANCHOR: Start with qualitative description of the situation
   "This is a minor disappointment" → suggests small negative impact
   
2. CALCULATE: Apply formulas to determine magnitude
   base_response × urgency × trust × capacity
   
3. VALIDATE: Check if result matches narrative
   Does -0.3 trust feel right for "minor disappointment"?
   If not, adjust anchors or formula
```

---

## Scale 1: Trust Impact (-3.0 to +1.0)

### Qualitative Anchors

**-3.0 (Maximum Negative): RELATIONSHIP SHATTERING**
```
Narrative Markers:
- "I don't know if I can trust you anymore"
- "This changes everything between us"
- "I need time. A lot of time."
- May never fully recover

Examples:
- Betrayal of deep secret (Level 4-5 relationship)
- Abandonment during genuine crisis (5x urgency)
- Lie that causes major harm to NPC
- Breaking sacred promise

Typical Formula:
base: -0.8 to -1.0 (major betrayal)
× 5 (crisis urgency)
× 0.5-0.8 (existing trust softens slightly)
= -2.0 to -3.0
```

**-1.5 to -2.0: MAJOR HARM**
```
Narrative Markers:
- "You really hurt me"
- "I don't know what to say"
- "I need space right now"
- Weeks to recover

Examples:
- Canceling on important event (wedding, funeral)
- Harsh criticism during vulnerability
- Choosing someone else over them (crisis context)
- Breaking significant promise

Typical Formula:
base: -0.5 to -0.7
× 3-4 (urgent/crisis)
× 0.7-1.0 (moderate trust)
= -1.5 to -2.0
```

**-0.8 to -1.2: MODERATE HARM**
```
Narrative Markers:
- "That stung"
- "I'm disappointed"
- "I expected better from you"
- Days to recover

Examples:
- Forgetting birthday
- Declining help when they really hoped you'd say yes
- Minor lie or omission
- Insensitive comment

Typical Formula:
base: -0.4 to -0.6
× 2 (important context)
× 1.0-1.2 (moderate to high trust)
= -0.8 to -1.2
```

**-0.3 to -0.5: MINOR HARM**
```
Narrative Markers:
- "A little disappointed, but I get it"
- "No worries, really"
- "Maybe next time"
- Hours to recover

Examples:
- Declining routine favor
- Being slightly late
- Forgetting small detail
- Mild disagreement

Typical Formula:
base: -0.3 to -0.5
× 1 (routine context)
× 1.2-1.5 (high trust cushions)
= -0.3 to -0.5
```

**-0.1 to -0.2: NEGLIGIBLE HARM**
```
Narrative Markers:
- "All good!"
- "Don't even think about it"
- No visible impact
- Immediate recovery

Examples:
- Declining trivial request
- Minor scheduling conflict
- Forgetting very small thing
- Different preference on low-stakes choice

Typical Formula:
base: -0.2 to -0.3
× 1 (routine)
× 1.5+ (very high trust)
× high capacity softens further
= -0.1 to -0.2
```

**0.0: NEUTRAL**
```
Narrative Markers:
- No relationship change
- Transactional interaction
- Expected behavior

Examples:
- Normal conversation
- Meeting basic expectations
- Neutral exchange
```

**+0.1 to +0.3: MINOR POSITIVE**
```
Narrative Markers:
- "Thanks, that was nice"
- "I appreciate it"
- Small warmth increase

Examples:
- Small kindness
- Thoughtful gesture
- Following through on small promise
- Quality time (routine)

Note: Positive gains are smaller than negative losses (negativity bias)
```

**+0.5 to +0.8: SIGNIFICANT POSITIVE**
```
Narrative Markers:
- "You really came through for me"
- "Thank you so much"
- Visible gratitude

Examples:
- Helping during important (not crisis) moment
- Meaningful gift or gesture
- Going out of your way for them
- Emotional support when capacity allows
```

**+1.0 (Maximum Positive): DEEPLY MEANINGFUL**
```
Narrative Markers:
- "I'll never forget this"
- "You really showed up for me"
- Relationship-defining moment

Examples:
- Being there during genuine crisis
- Major sacrifice to help them
- Saving them from serious harm
- Proving yourself after trust breach

Note: Trust is harder to build than destroy
Positive actions rarely exceed +1.0
```

---

## Scale 2: Emotional Capacity (0.0-10.0)

### Qualitative Anchors

**0.0-1.0: DEPLETED (Cannot function)**
```
Narrative Markers:
- "I can't do this"
- "Everything is too much"
- "I need to shut down"
- Withdraws completely

Behavioral Signs:
- Cannot maintain conversation
- Avoids all demands
- May not respond to messages
- Survival mode only

Support Capacity: 0
Can provide: Nothing (and that's valid)
Cannot provide: Any emotional labor

Examples:
- After multiple major crises compounding
- Severe depression/anxiety episode
- Complete burnout
- Grief crisis

What it looks like:
"Sarah stares at her phone. Three unread messages from you. She knows she 
should respond. She can't. She doesn't have it in her. Not today. Maybe not 
this week."
```

**2.0-4.0: LOW (Struggling)**
```
Narrative Markers:
- "I'm barely holding it together"
- "I want to help but I can't"
- "I'm so tired"
- Present but limited

Behavioral Signs:
- Short responses
- Apologizes for not being "enough"
- Offers practical help only
- Sets clear boundaries

Support Capacity: 2-4 (need + 2 rule: can support needs ≤ 0-2)
Can provide: Acknowledgment, physical presence, promise to help later
Cannot provide: Emotional processing, advice, long conversations

Examples:
- Multiple stressors active
- One major stressor + exhaustion
- Recent trauma still processing
- Meters mostly in yellow/red

What it looks like:
"Sarah meets you for coffee. She's there, physically. But you can see the 
fatigue in her eyes. When you start to talk about your problem, she nods,
but you can tell she's drowning too. 'I hear you. I really do. But I'm... 
I'm not in a place where I can help the way you need. I'm sorry.'"
```

**5.0-7.0: MODERATE (Stable)**
```
Narrative Markers:
- "I'm doing okay"
- "I've got some bandwidth"
- "Let's talk, I have time"
- Engaged but not unlimited

Behavioral Signs:
- Present and attentive
- Can listen for an hour
- Offers basic advice
- Maintains boundaries

Support Capacity: 5-7 (can support needs ≤ 3-5)
Can provide: Listening (30-60 min), basic advice, encouragement, practical help
Cannot provide: Hours of processing, crisis intervention, deep analysis

Examples:
- Normal life challenges
- Balanced meter states
- 1-2 minor stressors
- Typical baseline state

What it looks like:
"Sarah suggests meeting for coffee. She's present, asks good questions, 
really listens. After an hour she mentions she has some errands, but 
suggests continuing the conversation this weekend if you need more time."
```

**8.0-10.0: HIGH (Thriving)**
```
Narrative Markers:
- "I'm here for you"
- "I've got all the time you need"
- "Tell me everything"
- Fully available

Behavioral Signs:
- Deep presence
- Patient listening
- Insightful advice
- No rush or time pressure

Support Capacity: 8-10 (can support needs ≤ 6-8)
Can provide: Deep processing, crisis support, hours of conversation, nuanced advice
Can provide: Everything needed

Examples:
- All meters green/high
- No active stressors
- Recent wins/good news
- Life feeling balanced

What it looks like:
"Sarah picks up on the second ring. 'Hey, are you okay? You sound... off.' 
You hadn't even started talking yet. She just knew. 'Come over. Now. I'll 
make tea. We'll figure this out together.' And you know she means it. She's 
got the bandwidth. She's solid right now."
```

### Capacity Calculation Example

```javascript
// SARAH'S STATE
const meters = {
  emotional: 6,  // Decent
  mental: 5,     // Okay
  physical: 7,   // Good
  social: 6      // Decent
};

const stressors = {
  workPressure: 8,        // HIGH (counts as stressor)
  moneyStress: true,      // (counts as stressor)
  relationshipTension: [] // None
};

// CALCULATE CAPACITY
let capacity = 
  (6 * 0.50) +  // Emotional (primary): 3.0
  (5 * 0.30) +  // Mental (secondary): 1.5
  (7 * 0.15) +  // Physical (tertiary): 1.05
  (6 * 0.05);   // Social (minor): 0.3
  // = 5.85 base

// COUNT STRESSORS
// workPressure > 7: YES
// moneyStress: YES
// Total: 2 stressors

// APPLY STACKING PENALTY
// 2 stressors = -1.0 capacity
capacity = 5.85 - 1.0 = 4.85

// CLAMP
capacity = Math.max(0, Math.min(10, 4.85)) = 4.85

// RESULT: Sarah is at 4.85/10 capacity (LOW/MODERATE border)
// She can support needs up to: 4.85 - 2 = 2.85
```

**What this MEANS narratively:**

"Sarah is doing *okay* on paper - her meters aren't terrible. But she's 
dealing with a demanding work deadline AND money stress, and those two 
things are grinding her down. She's not in crisis, but she's definitely 
not thriving. If you come to her with a small problem (need level 2), 
she can help. But if you're in crisis (need level 6), she just doesn't 
have it right now. She'll want to help, but she can't."

---

## Scale 3: Meter Values (0-10)

### Physical Meter Anchors

**0-1: CRISIS - "Body broken"**
```
You can barely move. Everything hurts. You've pushed too far.
Activities: Only rest. Medical intervention may be needed.
Recovery: 1-2 weeks minimum
```

**2-3: LOW - "Exhausted"**
```
Your body is tired. Stairs are hard. You need rest soon.
Activities: Reduced energy, physical activities harder
Recovery: 2-3 days of rest
```

**4-6: NORMAL - "Functioning"**
```
You feel fine. Normal energy. Can handle daily activities.
Activities: No modifiers
Maintenance: Occasional exercise, decent sleep
```

**7-8: HIGH - "Energized"**
```
You feel strong. Physical activities are enjoyable. Energy to spare.
Activities: Bonus to physical, +1 energy
Achievement: Regular exercise paying off
```

**9-10: PEAK - "Optimal condition"**
```
You feel amazing. Body is a well-tuned machine.
Activities: Major bonuses, +2 energy, unlocks elite activities
Achievement: Athlete lifestyle
```

### Mental Meter Anchors

**0-1: CRISIS - "Burnout/Breakdown"**
```
You can't think. Everything is fog. Brain is offline.
Work: Impossible. Requires medical leave.
Recovery: 2-4 weeks, therapy recommended
```

**2-3: LOW - "Foggy/Drained"**
```
Thinking is hard. Focus is fleeting. Everything takes longer.
Work: Difficult, reduced productivity
Recovery: 1 week of reduced obligations
```

**4-6: NORMAL - "Stable"**
```
You can think clearly. Focus is normal. Work gets done.
Work: No modifiers
Maintenance: Good sleep, regular breaks
```

**7-8: HIGH - "Sharp/Clear"**
```
Your mind is sharp. Focus comes easily. Ideas flow.
Work: Bonus to cognitive tasks, deep work possible
Achievement: Good mental health practices
```

**9-10: PEAK - "Flow state"**
```
Crystal clarity. Peak mental performance. Breakthroughs possible.
Work: Major bonuses, innovation unlocked
Achievement: Optimal cognitive health
```

### Social Meter Anchors

**0-1: CRISIS - "Completely isolated"**
```
You're alone. Completely. Everyone has stopped reaching out.
Relationships: Decay -0.05/week. Can't form new bonds.
Recovery: 3-4 weeks of deliberate reconnection
```

**2-3: LOW - "Lonely"**
```
You miss people. It's been too long since real connection.
Relationships: Decay -0.02/week
Recovery: 2-3 meaningful interactions
```

**4-6: NORMAL - "Connected"**
```
You have people. Regular contact. Feel part of things.
Relationships: Stable
Maintenance: Weekly social interaction
```

**7-8: HIGH - "Thriving socially"**
```
Rich social life. Multiple active friendships. Feel connected.
Relationships: Bonus to social activities, easier to form bonds
Achievement: Active social engagement
```

**9-10: PEAK - "Social catalyst"**
```
Center of social circles. Magnetic. Can introduce people.
Relationships: Major bonuses, leadership opportunities
Achievement: Community leader
```

### Emotional Meter Anchors

**0-1: CRISIS - "Despair"**
```
Nothing matters. Nothing brings joy. The weight is unbearable.
Life: -20% success on everything. Therapy critical.
Recovery: 4-8 weeks, professional help required
```

**2-3: LOW - "Struggling"**
```
You're having a hard time. Everything feels heavier.
Life: -10% success. Hard to enjoy things.
Recovery: 2-3 weeks, support helpful
```

**4-6: NORMAL - "Stable"**
```
You're okay. Some good days, some bad. Life is livable.
Life: No modifiers
Maintenance: Balance, occasional joy
```

**7-8: HIGH - "Fulfilled"**
```
You feel good. Satisfied. Life has meaning.
Life: +10% success on everything. Resilient.
Achievement: Progress on aspirations, healthy relationships
```

**9-10: PEAK - "Joyful"**
```
Deep fulfillment. Everything feels aligned. You're thriving.
Life: +15% success, spreads positivity to others
Achievement: Rare, special state
```

---

## Scale 4: Quality Scores (0.0-1.0)

### Authenticity Score Anchors

**0.0-0.3: INAUTHENTIC**
```
Narrative Markers:
- Lies or avoids truth
- Says what they think you want to hear
- Defensive or aggressive
- Doesn't acknowledge limitations

Examples:
- "I'm fine!" (when clearly not)
- "Yeah, I can totally help!" (capacity 2/10)
- "Whatever, I don't care" (when they do)
- Complete avoidance

What it looks like:
Capacity 2.5/10, but responds: "Of course I can help! No problem at all!"
→ Score: 0.2 (lying about capacity)
```

**0.4-0.6: STRUGGLING/MIXED**
```
Narrative Markers:
- Wants to be honest but can't quite
- Overcommits with awareness of struggle
- Excessive apologizing
- Half-truths

Examples:
- "I can try... I'm just... I'm sorry"
- "I want to help but I'm really overwhelmed"
- "I'll figure it out" (not confident)

What it looks like:
Capacity 3.5/10, responds: "I... I can try. I'm not sure I'll be much help 
right now, but I'll do my best. Sorry I'm not more..."
→ Score: 0.55 (trying but struggling to set boundary)
```

**0.7-0.8: AUTHENTIC (Target minimum)**
```
Narrative Markers:
- Honest about limitations
- Clear boundaries (with some fumbling)
- Acknowledges reality
- Shows guilt but follows through

Examples:
- "I want to help, but I'm barely keeping it together myself"
- "I can listen for an hour, but then I need to rest"
- "I'm at a 3 out of 10 right now. Can I help you this weekend instead?"

What it looks like:
Capacity 4.0/10, responds: "I can see this is really hard for you. I'm 
honestly not in a place where I can help the way you need right now—I'm 
barely keeping it together myself. Can I check in tomorrow when I'm more 
present?"
→ Score: 0.75 (honest, acknowledges limitations, offers alternative)
```

**0.9-1.0: HIGHLY AUTHENTIC**
```
Narrative Markers:
- Crystal clear boundaries
- Kind but firm
- No excessive guilt
- Offers what they CAN provide

Examples:
- "I'm at capacity right now. I can't take this on. But I care about you."
- "I have an hour. Let's use it well. What's most important?"
- "I'm here. Tell me everything. I've got the bandwidth."

What it looks like:
Capacity 8.5/10, responds: "I can tell something's wrong. Come over. I'll 
make tea. Take your time. I'm not going anywhere. I've got you."
→ Score: 0.95 (fully present, no false promises, authentic availability)
```

### Tension Score Anchors

**0.0-0.3: NO TENSION**
```
Flat narrative. No hooks. No mysteries. Everything explained.
Reader: Bored. No reason to continue.
```

**0.4-0.6: MILD TENSION**
```
Some interesting elements but not compelling.
Reader: Might continue, might not care.
```

**0.7-0.8: GOOD TENSION (Target minimum)**
```
Clear hooks. Unanswered questions. Want to know more.
Reader: Engaged. "One more turn."
```

**0.9-1.0: EXCELLENT TENSION**
```
Multiple hooks. Dramatic irony. Stakes clear. Can't stop reading.
Reader: Must know what happens. "One more week."
```

---

## Scale 5: OCEAN Personality Traits (0.0-1.0)

### How OCEAN Values Affect Base Responses

**Agreeableness: 0.1 (Very Low)**
```
Base response to rejection: -0.7 to -1.0 trust
Interpretation: "Typical. People always let me down."
Forgiveness: Low. Holds grudges. Takes offense easily.

Example:
Player declines routine favor:
- Base: -0.5
- Low agreeableness amplifies: × 1.4
- Result: -0.7 trust for routine rejection
```

**Agreeableness: 0.9 (Very High)**
```
Base response to rejection: -0.1 to -0.3 trust
Interpretation: "They must have a good reason. It's okay."
Forgiveness: High. Gives benefit of doubt. Cushions impact.

Example:
Player declines routine favor:
- Base: -0.5
- High agreeableness softens: × 0.3
- Result: -0.15 trust for routine rejection
```

**Neuroticism: 0.1 (Very Low - Stable)**
```
Emotional regulation: Excellent
Crisis response: Calm, solution-focused
Capacity impact: Minimal (-0.5 max)

Example at capacity 5/10:
"I'm tired, but I can handle this. Let's figure it out."
```

**Neuroticism: 0.9 (Very High - Anxious)**
```
Emotional regulation: Poor
Crisis response: Overwhelmed, catastrophizing
Capacity impact: Severe (-2.0 or more)

Example at capacity 5/10:
"Everything is falling apart. I can't do this. It's too much."
(Acts like capacity 3/10 due to anxiety amplification)
```

---

## Worked Example: Full Calculation with Narrative

### Scenario Setup

```javascript
const SCENARIO = {
  player_action: "Declines to help NPC move apartments",
  
  npc_sarah: {
    personality: {
      openness: 0.7,
      conscientiousness: 0.6,
      extraversion: 0.5,
      agreeableness: 0.8,      // HIGH - forgiving, kind
      neuroticism: 0.6          // MODERATE-HIGH - can get anxious
    },
    
    current_state: {
      emotional_meter: 4,        // Low
      mental_meter: 5,           // Okay
      physical_meter: 7,         // Good
      social_meter: 6,           // Decent
      
      active_stressors: {
        moving_apartment: true,  // YES
        job_transition: true,    // YES
        total_count: 2
      }
    },
    
    relationship_with_player: {
      level: 3,                  // Friend
      trust: 0.65,               // Moderate-high
      weeks_since_interaction: 1
    },
    
    situation_urgency: "crisis" // CRISIS - moving this weekend, stressed
  }
};
```

### Step 1: Calculate Emotional Capacity

```javascript
// Base capacity from meters
const baseCapacity = 
  (4 * 0.50) +   // Emotional (primary): 2.0
  (5 * 0.30) +   // Mental (secondary): 1.5
  (7 * 0.15) +   // Physical (tertiary): 1.05
  (6 * 0.05);    // Social (minor): 0.3
  // = 4.85

// Stacking penalty (2 stressors)
const stackingPenalty = 1.0;

// Final capacity
const capacity = 4.85 - 1.0 = 3.85

// QUALITATIVE INTERPRETATION:
// Sarah is at 3.85/10 capacity (LOW)
// She's in the "struggling" range
// Can support needs up to: 3.85 - 2 = 1.85
```

**What this means narratically:**

"Sarah's meters aren't terrible, but she's dealing with moving AND a job 
transition. Both are major stressors. She's holding it together, but barely. 
She was HOPING you'd say yes to helping her move. She really needed this."

### Step 2: Calculate Base Personality Response

```javascript
// High agreeableness (0.8) baseline
// For "declining favor": base = -0.5 (standard rejection)
// But high agreeableness softens initial reaction

const baseResponse = -0.5;  // Standard rejection base

// Agreeableness modifier
// High agreeableness (0.8) typically softens by 0.6-0.8x
// BUT capacity is LOW (3.85), which affects judgment quality
// Low capacity → less able to be generous/forgiving

const agreablenessModifier = 0.7;  // Softened slightly, but capacity limits it
const personalityAdjustedBase = baseResponse * agreablenessModifier;
// = -0.35
```

**What this means narratively:**

"Normally, Sarah would be really understanding. 'No worries, I get it!' 
But right now? She's stressed, overwhelmed, and was really counting on you."

### Step 3: Apply Situational Urgency Multiplier

```javascript
// Situation: CRISIS
// Moving this weekend, stressed, really needed help
const urgencyMultiplier = 5.0;  // Maximum crisis multiplier

const afterUrgency = -0.35 * 5.0 = -1.75;
```

**What this means narratively:**

"This wasn't a casual 'help me move a box' request. This was 'I'm moving 
in 2 days, I'm overwhelmed, and I really need you.' The urgency amplifies 
the impact SIGNIFICANTLY."

### Step 4: Apply Relationship Trust Modifier

```javascript
// Trust: 0.65 (moderate-high)
// Trust typically provides 0.5x-2x modifier
// Higher trust = cushions negative impacts slightly

const trustModifier = 1.2;  // Moderate cushioning

const afterTrust = -1.75 * 1.2 = -2.1;
```

**What this means narratively:**

"You have decent trust built up. She knows you're generally reliable. 
This actually makes it WORSE - she expected you to come through because 
you usually do."

### Step 5: Apply Capacity Constraint

```javascript
// Sarah's capacity: 3.85 (LOW)
// Low capacity = worse judgment, can't process nuance, black/white thinking

// Capacity effect on judgment:
// - High capacity (8+): Can soften impact, see complexity
// - Moderate capacity (5-7): Normal processing
// - Low capacity (<5): Hardens impact, catastrophizing

const capacityJudgmentFactor = 0.9;  // Slightly hardens (low capacity)

const finalImpact = -2.1 * 0.9 = -1.89;
// Round to: -1.9 trust
```

**What this means narratively:**

"If Sarah were at capacity 8, she might think 'They must have a good reason. 
I'll figure something out.' But at capacity 3.85, she can't see past her 
own stress. It feels like abandonment."

### Step 6: Check for Memory Resonance

```javascript
// Check: Does this resonate with past memories?
// Example: If player has pattern of canceling on Sarah...

const memoryCheck = checkPastPatterns(player, sarah);

if (memoryCheck.pattern === "multiple_cancellations") {
  // Past trauma trigger (0.95 weight)
  finalImpact *= 1.3;  // Amplify by pattern
  // = -2.47 → clamp to -2.5
}

// Let's say no significant pattern exists
// Final impact: -1.9 trust
```

### Final Result: -1.9 Trust Impact

**Clamp to range:** -3.0 to +1.0 ✓

**Qualitative Check:**

Does -1.9 trust match the narrative?

```
Expected narrative for -1.9:
- "This really hurt"
- "I feel let down"
- "I needed you and you weren't there"
- Will take weeks to repair
- Not relationship-ending, but significant damage
```

### The Generated Dialogue

```javascript
{
  "player_action": "Declines to help Sarah move",
  
  "sarah_internal_thought": 
    "I can't believe this. I really needed them. I've been so stressed 
    about this move, and I thought... I thought they'd be there for me. 
    Maybe I was wrong about us.",
  
  "sarah_response": 
    "Oh. Okay. I... I understand. I'll figure something out. 
    [pause] I really needed your help with this, you know? It's... 
    it's fine. I'll manage.",
  
  "sarah_emotional_state": "hurt_and_overwhelmed",
  
  "relationship_impact": -1.9,
  
  "authenticity_score": 0.65,
  // (Trying to be understanding but hurt shows through)
  
  "capacity_constrained": true,
  // (Cannot process nuance - "they must have a reason")
  
  "recovery_time": "2-3 weeks",
  
  "next_interaction_affected": true
  // (Will be more distant in next interaction)
}
```

**Validation Question:** Does this feel right?

- ✅ High urgency (5x multiplier) makes moderate rejection feel major
- ✅ Low capacity (3.85) prevents generous interpretation
- ✅ Moderate-high trust (0.65) means expectations were higher
- ✅ -1.9 trust = "major harm" tier = weeks to recover
- ✅ Dialogue shows hurt without being melodramatic
- ✅ Authenticity score 0.65 (struggling to be understanding)

**YES - this calibration is correct.**

---

## Training Data Requirements

### For Every Numerical Assignment, Include:

1. **The Number Itself**
   ```json
   "relationship_impact": -1.9
   ```

2. **The Formula Used**
   ```json
   "impact_calculation": {
     "base": -0.5,
     "personality_modifier": 0.7,
     "urgency_multiplier": 5.0,
     "trust_modifier": 1.2,
     "capacity_factor": 0.9,
     "result": -1.89,
     "rounded": -1.9
   }
   ```

3. **The Qualitative Anchor**
   ```json
   "impact_tier": "MAJOR HARM",
   "narrative_markers": [
     "This really hurt",
     "I feel let down",
     "I needed you"
   ],
   "recovery_time": "2-3 weeks"
   ```

4. **The Validation Check**
   ```json
   "validation": {
     "does_dialogue_match_score": true,
     "reasoning": "Response shows hurt without melodrama, matches -1.9 tier"
   }
   ```

### Example Training Data Entry

```json
{
  "scenario_id": "decline_help_moving_001",
  
  "context": {
    "player_action": "Declines to help NPC move apartments",
    "npc_personality": {
      "agreeableness": 0.8,
      "neuroticism": 0.6
    },
    "npc_capacity": 3.85,
    "capacity_tier": "LOW - struggling",
    "urgency": "crisis",
    "urgency_multiplier": 5.0,
    "relationship_trust": 0.65
  },
  
  "calculation": {
    "base_response": -0.5,
    "personality_adjusted": -0.35,
    "after_urgency": -1.75,
    "after_trust": -2.1,
    "after_capacity": -1.89,
    "final": -1.9,
    
    "formula_breakdown": "base × personality × urgency × trust × capacity",
    "formula_values": "(-0.5 × 0.7 × 5.0 × 1.2 × 0.9) = -1.89 → -1.9"
  },
  
  "qualitative_anchor": {
    "tier": "MAJOR HARM (-1.5 to -2.0)",
    "expected_narrative": "This really hurt / I feel let down / Weeks to recover",
    "expected_behavior": "Will be distant in next interaction, needs repair"
  },
  
  "generated_content": {
    "internal_thought": "I can't believe this. I really needed them...",
    "dialogue": "Oh. Okay. I... I understand. I'll figure something out...",
    "emotional_state": "hurt_and_overwhelmed"
  },
  
  "quality_scores": {
    "authenticity": 0.65,
    "authenticity_reasoning": "Trying to be understanding but hurt shows through - capacity too low for full generosity",
    
    "tension": 0.75,
    "tension_reasoning": "Creates relationship tension, player will wonder if they damaged friendship",
    
    "alignment_with_capacity": 0.95,
    "capacity_reasoning": "Low capacity (3.85) correctly prevents generous/nuanced response"
  },
  
  "validation": {
    "does_impact_match_narrative": true,
    "does_dialogue_match_capacity": true,
    "does_score_match_tier": true,
    "overall_quality": 0.78
  }
}
```

---

## Common Calibration Errors

### Error 1: Arbitrary Numbers Without Justification

❌ **WRONG:**
```json
{
  "relationship_impact": -1.3,
  "dialogue": "Whatever, I don't care."
}
```

**Problem:** 
- No formula shown
- Dialogue suggests much smaller impact (~-0.3 to -0.5)
- Number doesn't match tier

✅ **CORRECT:**
```json
{
  "relationship_impact": -1.3,
  
  "calculation": {
    "base": -0.6,
    "personality": 0.8,
    "urgency": 3.0,
    "trust": 1.0,
    "formula": "(-0.6 × 0.8 × 3.0 × 1.0) = -1.44 → -1.3"
  },
  
  "qualitative_tier": "MODERATE HARM (-0.8 to -1.2)",
  
  "dialogue": "That stung. I really hoped you'd say yes. I'm disappointed.",
  
  "validation": "Dialogue matches tier - shows hurt but not devastation"
}
```

### Error 2: Dialogue/Score Mismatch

❌ **WRONG:**
```json
{
  "relationship_impact": -2.5,
  "dialogue": "No worries! All good!",
  "authenticity_score": 0.9
}
```

**Problem:**
- -2.5 = "major harm/relationship shattering"
- Dialogue suggests minimal impact
- High authenticity score for clearly inauthentic response

✅ **CORRECT:**
```json
{
  "relationship_impact": -2.5,
  
  "calculation": {
    "base": -0.8,
    "urgency": 5.0,
    "trust": 0.7,
    "capacity": 0.9,
    "formula": "(-0.8 × 5.0 × 0.7 × 0.9) = -2.52 → -2.5"
  },
  
  "qualitative_tier": "MAJOR HARM (-1.5 to -2.0+)",
  
  "dialogue": "I... I don't know what to say. I really needed you. 
  This... this changes things. I need some space.",
  
  "authenticity_score": 0.75,
  "authenticity_reasoning": "Honest about hurt, sets boundary, but struggling to articulate full impact",
  
  "validation": "Dialogue matches -2.5 impact - relationship significantly damaged"
}
```

### Error 3: Ignoring Capacity Constraints

❌ **WRONG:**
```json
{
  "npc_capacity": 2.5,
  "player_emotional_need": 7.0,
  
  "dialogue": "Of course! Tell me everything. I'm here for you. 
  Let's process this together. What's going on?",
  
  "authenticity_score": 0.95
}
```

**Problem:**
- Capacity 2.5 can support needs up to 0.5 (capacity - 2)
- Player needs 7.0 support
- NPC is providing 7.0+ support level
- Violates core capacity constraint rule

✅ **CORRECT:**
```json
{
  "npc_capacity": 2.5,
  "player_emotional_need": 7.0,
  "required_capacity": 9.0,  // need + 2
  "shortfall": 6.5,
  
  "dialogue": "I can see you're really struggling. I want to help, 
  I really do. But I'm barely keeping it together myself right now. 
  I can't... I can't hold space for this. I'm sorry. Maybe try 
  calling Marcus? He's in a better place than I am.",
  
  "authenticity_score": 0.85,
  "authenticity_reasoning": "Honest about limitations, acknowledges desire to help, suggests alternative",
  
  "support_provided": 0.0,
  "validation": "Correctly respects capacity constraint - NPC cannot provide needed support"
}
```

### Error 4: Inconsistent Tier Mapping

❌ **WRONG:**
```json
{
  "impact_A": -0.3,
  "narrative_A": "You absolutely shattered my trust. I'll never forgive you.",
  
  "impact_B": -2.8,
  "narrative_B": "I'm a little disappointed, but it's fine."
}
```

**Problem:**
- -0.3 = "minor harm" but narrative suggests -3.0 level
- -2.8 = "relationship shattering" but narrative suggests -0.3 level
- Complete tier inversion

✅ **CORRECT:**
```json
{
  "impact_A": -0.3,
  "tier_A": "MINOR HARM (-0.3 to -0.5)",
  "narrative_A": "I'm a little disappointed, but I get it. Maybe next time.",
  
  "impact_B": -2.8,
  "tier_B": "RELATIONSHIP SHATTERING (-2.5 to -3.0)",
  "narrative_B": "I can't believe you did that. You knew how much this mattered. 
  I don't... I don't know if I can trust you anymore. I need space.",
  
  "validation": "Both impacts correctly match their narrative tiers"
}
```

---

## Calibration Checklist

When assigning any numerical value, verify:

### For Trust Impact:
- [ ] Formula shown with all factors
- [ ] Base response justified by personality
- [ ] Urgency multiplier (1-5x) applied
- [ ] Trust modifier (0.5-2x) applied
- [ ] Capacity factor affects judgment
- [ ] Memory resonance checked
- [ ] Final number clamped to -3.0 to +1.0
- [ ] Qualitative tier identified
- [ ] Dialogue matches tier
- [ ] Recovery time estimated

### For Emotional Capacity:
- [ ] Meter values listed
- [ ] Weighted sum calculated (50% emo, 30% mental, 15% phys, 5% social)
- [ ] Active stressors counted
- [ ] Stacking penalty applied
- [ ] Final capacity clamped to 0-10
- [ ] Qualitative tier identified (depleted/low/moderate/high)
- [ ] Support limit calculated (capacity - 2)
- [ ] Behavioral description matches tier
- [ ] Dialogue reflects capacity level

### For Quality Scores:
- [ ] Authenticity score matches capacity constraint
- [ ] Tension score justified with hooks/stakes
- [ ] Dramatic irony score reflects knowledge gaps
- [ ] Overall quality ≥ 0.7 threshold
- [ ] Reasoning provided for each score

### For Meter Values:
- [ ] Current meter level specified (0-10)
- [ ] Qualitative tier identified
- [ ] Behavioral effects listed
- [ ] Recovery activities specified
- [ ] Time to recover estimated

---

## Summary: The Grounding System

```
SCALE → ANCHORS → FORMULA → VALIDATION → NARRATIVE

1. Identify the scale (trust, capacity, meter, quality)
2. Find qualitative anchor for approximate range
3. Apply formula with explicit factors
4. Validate: Does number match narrative?
5. Generate narrative that reflects the number

NOT:
"This feels like a -1.3" ❌

BUT:
"Base -0.6 × personality 0.8 × urgency 3x = -1.44 → -1.3
This is MODERATE HARM tier → weeks to recover → dialogue shows hurt" ✅
```

Every number must have:
1. **Derivation** (formula/calculation)
2. **Anchor** (qualitative tier)
3. **Validation** (does narrative match?)

---

## Compliance Checklist (Master Truths v1.2)

- [x] Uses canonical vocab & scales (Levels 0–5; Trust 0.0–1.0; Capacity 0.0-10.0)
- [x] Establishes qualitative anchors for all quantitative scales
- [x] Provides worked examples with full calculations
- [x] Links numbers to narrative descriptions
- [x] Enables consistent numerical assignments
- [x] Supports LLM training data generation
- [x] Validates alignment between numbers and narrative
- [x] This doc cites **Truths v1.2** at the top

---

**This guide provides the missing layer between formulas and narrative - enabling both humans and LLMs to determine what numbers actually mean and when to use them.**

