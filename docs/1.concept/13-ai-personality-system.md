# Unwritten: AI Personality & Memory System

## Overview

NPCs in Unwritten feel real because they have:
- **Dynamic personalities** that evolve over time
- **Three-tier memory systems** that remember what matters
- **Authentic behavioral generation** driven by personality + context
- **Relationship dynamics** that respond to player actions

**See also:** `20-character-creation.md` for how the player character's personality is established through scenario-based questions, and `22-multi-lifetime-continuity.md` for how both player and NPC personalities evolve across decades.

---

## OCEAN Personality Model

### The Five-Factor Model (Big Five)

Every character (player and NPCs) in Unwritten has a personality defined by five core traits, each scored 1.0-5.0:

---

### **O**penness to Experience (1.0-5.0)

Measures creativity, curiosity, and appreciation for new experiences.

**Low Openness (1.0-2.5):**
- Prefers routine and familiarity
- Practical and conventional
- Uncomfortable with abstract ideas
- Resistant to change

**High Openness (3.5-5.0):**
- Curious and imaginative
- Appreciates art and culture
- Open to new experiences
- Creative thinking

**Example NPC:**
```
Sarah Anderson
Openness: 4.3

Behaviors:
• Suggests trying new cafés
• Reads experimental literature
• Excited by abstract art
• Dreams of unconventional career path
```

---

### **C**onscientiousness (1.0-5.0)

Measures organization, reliability, and goal-orientation.

**Low Conscientiousness (1.0-2.5):**
- Spontaneous and flexible
- Disorganized
- Procrastinates
- Struggles with long-term planning

**High Conscientiousness (3.5-5.0):**
- Organized and responsible
- Goal-driven
- Reliable and punctual
- Plans ahead

**Example NPC:**
```
Marcus Rivera
Conscientiousness: 4.6

Behaviors:
• Always on time
• Has detailed life plans
• Follows through on commitments
• Keeps organized schedules
```

---

### **E**xtraversion (1.0-5.0)

Measures energy levels, sociability, and assertiveness.

**Low Extraversion / High Introversion (1.0-2.5):**
- Prefers solitude or small groups
- Thoughtful and reserved
- Recharges alone
- Selective with socializing

**High Extraversion (3.5-5.0):**
- Energized by social interaction
- Outgoing and talkative
- Seeks excitement
- Large friend circles

**Example NPC:**
```
Jenna Park
Extraversion: 4.8

Behaviors:
• Suggests group activities
• Comfortable with strangers
• Life of the party
• Initiates social events
```

---

### **A**greeableness (1.0-5.0)

Measures compassion, cooperation, and trust.

**Low Agreeableness (1.0-2.5):**
- Direct and blunt
- Competitive
- Skeptical of others
- Prioritizes truth over feelings

**High Agreeableness (3.5-5.0):**
- Empathetic and kind
- Cooperative
- Trusting
- Avoids conflict

**Example NPC:**
```
Sarah Anderson
Agreeableness: 4.6

Behaviors:
• Goes out of way to help
• Listens without judgment
• Avoids confrontation
• Assumes good intentions
```

---

### **N**euroticism (1.0-5.0)

Measures emotional stability and anxiety levels.

**Low Neuroticism / High Stability (1.0-2.5):**
- Calm under pressure
- Emotionally stable
- Resilient
- Rarely worried

**High Neuroticism (3.5-5.0):**
- Anxious and worried
- Emotional sensitivity
- Stress-prone
- Mood fluctuations

**Example NPC:**
```
David Chen
Neuroticism: 3.8

Behaviors:
• Worries about decisions
• Seeks reassurance
• Stress affects mood
• Emotional in conflicts
```

---

## Personality Evolution

### How Traits Change Over Time

**Single Interaction Impact:**
- Typical shift: 0.1-0.3 points
- Must make psychological sense
- Cumulative over multiple interactions

**Major Life Event Impact:**
- Crisis overcome: -0.5 Neuroticism
- Success achieved: +0.3 Conscientiousness  
- Betrayal experienced: -0.4 Agreeableness
- New experience embraced: +0.2 Openness

**Realistic Constraints:**
- Traits can't flip overnight
- Core personality remains recognizable
- Growth is gradual but noticeable
- Regression is possible with trauma

---

### Example: Sarah's Evolution

**Week 1 (Base):**
```
Openness: 3.5
Conscientiousness: 4.0
Extraversion: 2.8
Agreeableness: 3.9
Neuroticism: 3.8
```

**Week 12 (After 10+ supportive interactions):**
```
Openness: 3.8 (+0.3) - More willing to try new things
Conscientiousness: 4.2 (+0.2) - More organized with plans
Extraversion: 3.0 (+0.2) - Slightly more outgoing
Agreeableness: 4.1 (+0.2) - Trusts you more
Neuroticism: 3.5 (-0.3) - Less anxious around you
```

**Week 40 (After major achievements together):**
```
Openness: 4.3 (+0.8 total) - Embraced risky dream
Conscientiousness: 4.5 (+0.5 total) - Running business
Extraversion: 3.4 (+0.6 total) - More confident
Agreeableness: 4.6 (+0.7 total) - Deep trust
Neuroticism: 2.9 (-0.9 total) - Found confidence
```

---

## Memory Architecture

### Three-Tier Memory System

```
┌─────────────────────────────────────┐
│     SHORT-TERM MEMORY (24 hours)    │
├─────────────────────────────────────┤
│ • Recent conversations              │
│ • Emotional reactions               │
│ • Activity observations             │
│ • Temporary mood states             │
│                                     │
│ Stored: Last 5-10 interactions      │
│ Weight: 0.3-0.5                     │
└─────────────────────────────────────┘
           ↓ (Consolidation)
┌─────────────────────────────────────┐
│   MEDIUM-TERM MEMORY (1-4 weeks)    │
├─────────────────────────────────────┤
│ • Relationship patterns             │
│ • Preference learning               │
│ • Significant events                │
│ • Recurring themes                  │
│                                     │
│ Stored: 15-30 key moments           │
│ Weight: 0.6-0.8                     │
└─────────────────────────────────────┘
           ↓ (Integration)
┌─────────────────────────────────────┐
│   LONG-TERM MEMORY (Permanent)      │
├─────────────────────────────────────┤
│ • Core personality traits           │
│ • Major life events                 │
│ • Deep relationship history         │
│ • Defining moments                  │
│                                     │
│ Stored: Unlimited pivotal memories  │
│ Weight: 0.85-1.0                    │
└─────────────────────────────────────┘
```

---

### Memory Structure

**Each Memory Contains:**
```json
{
  "id": "mem_12847",
  "timestamp": "Week 12, Day 3",
  "event": "coffee_deep_conversation",
  "location": "cafe_luna",
  "participants": ["player", "sarah_anderson"],
  "description": "Late night at Café Luna. Sarah's hands wrapped around a cold mug, speaking quietly about fear of failure...",
  "emotion": "vulnerable_solidarity",
  "weight": 0.85,
  "tags": ["vulnerability", "shared_fears", "trust_building"],
  "personality_impact": {
    "neuroticism": -0.2,
    "agreeableness": +0.15
  },
  "unlocks": ["business_planning", "grandmother_grave"]
}
```

---

### Memory Weight System

**Weight determines influence on behavior:**

**0.1-0.3 (Trivial):**
- Casual interactions
- Brief encounters
- Small talk
- Forgotten quickly

**0.4-0.6 (Noticeable):**
- Meaningful conversations
- Fun activities together
- Helpful moments
- Shape preferences

**0.7-0.8 (Significant):**
- Deep conversations
- Crisis support
- Major activities
- Build relationship

**0.85-0.95 (Defining):**
- Life-changing events
- Vulnerable moments
- Major decisions together
- Core memories

**1.0 (Legendary):**
- Climax of relationship arc
- Irreplaceable experiences
- Story-defining moments
- Never forgotten

---

## Behavioral Generation

### How NPCs React

**AI considers all three factors:**
1. Current personality traits (OCEAN)
2. Memory history with player
3. Current context and emotional state

**Example Decision:**
```
Scenario: Player asks Sarah to quit job and start bookshop NOW

AI Analysis:
• Openness: 4.3 (high) → Attracted to risky idea
• Neuroticism: 2.9 (lowered) → Less afraid than before
• Memory: 47 positive interactions, trust=0.92
• Recent memory: "You believed in me" (weight 0.9)

Result: Sarah says YES
"I've been waiting for someone to believe in me.
Let's do it."

Alternative scenario (different history):
• Openness: 3.5 (medium)
• Neuroticism: 3.8 (higher)
• Memory: Only 12 interactions, trust=0.45
• No deep vulnerability shared

Result: Sarah hesitates
"That's... a big step. Can we talk about this more?
I need time to think."
```

---

## Dialogue Generation

### Context-Aware Conversations

**AI generates dialogue considering:**

**1. Personality Traits:**
```
High Openness + High Extraversion:
"Oh! I just thought of the wildest idea—what if we..."

High Conscientiousness + Low Extraversion:
"I've been thinking carefully about this, and..."

Low Agreeableness + High Neuroticism:
"Look, I'm just being realistic here..."
```

**2. Relationship Level:**
```
Level 1 (Stranger):
"Hi. Nice weather today."

Level 3 (Friend):
"Hey! I was just thinking about you. Remember when..."

Level 5 (Soulmate):
"You know what I was going to say, don't you?
We've been through too much together for me to hide this."
```

**3. Recent Memories:**
```
If player helped during crisis last week:
"I'm still thinking about what you did for me.
I don't know if I said it enough, but... thank you."

If player was absent during important moment:
"You weren't there when I needed you. I get that
you were busy, but..."
```

**4. Emotional State:**
```
Happy + Excited:
"This is incredible! Do you realize what this means?"

Anxious + Stressed:
"I don't know... what if everything goes wrong?"

Melancholy + Reflective:
"Sometimes I wonder what my grandmother would think..."
```

---

## Relationship Dynamics

### Relationship Level System (0-5)

**Level Progression:**
```
Level 0: NOT MET
├─ Never interacted with this NPC
├─ Card not yet in deck
└─ First meeting will trigger → Level 1

Level 1: STRANGER (0-5 interactions)
├─ Trust: 0.0-0.2
├─ Polite but distant
├─ Small talk only
└─ Learning basic info

Level 2: ACQUAINTANCE (6-15 interactions)
├─ Trust: 0.2-0.4
├─ Friendly, recognizable
├─ Surface conversations
└─ Some personal sharing

Level 3: FRIEND (16-30 interactions)
├─ Trust: 0.4-0.6
├─ Genuine connection
├─ Deep conversations possible
└─ Help with problems

Level 4: CLOSE FRIEND (31-75 interactions)
├─ Trust: 0.6-0.8
├─ Strong bond
├─ Vulnerable moments
└─ Life-changing decisions together

Level 5: SOULMATE/BEST FRIEND (76+ interactions)
├─ Trust: 0.8-1.0
├─ Unbreakable connection
├─ Complete understanding
└─ Forever bonds
```

**Display Format:**
- UI shows: "Level 3 (Trust 0.52)"
- Never show "Level 0" (show "Not Met" instead)
- Archives track Level 0 internally for "never met" NPCs

---

### Trust System (0.0-1.0)

**Trust is continuous under relationship levels:**

**How Trust Builds:**
- Consistent interactions: +0.02/interaction
- Keeping promises: +0.05
- Being there in crisis: +0.1-0.2
- Vulnerability sharing: +0.08
- Time together: +0.01/week

**How Trust Breaks:**
- Breaking promises: -0.1
- Absence in crisis: -0.15
- Betrayal: -0.3 to -0.6
- Neglect over time: -0.02/week

**Level-Up Requirements:**
```
0→1: First meeting (automatic)
1→2: 6+ interactions AND trust >= 0.2
2→3: 16+ interactions AND trust >= 0.4
3→4: 31+ interactions AND trust >= 0.6
4→5: 76+ interactions AND trust >= 0.8
```

**Important:** You need BOTH sufficient interactions AND trust to level up. High trust with few interactions won't trigger evolution (relationship needs time). Many interactions with low trust keeps you stuck (relationship needs quality)

---

### Attraction System (0.0-1.0)

**Separate from Trust:**
- Attraction = romantic/deep connection interest
- Trust = reliability and safety

**Factors:**
- Personality compatibility: Base multiplier
- Shared interests: +0.05 per aligned activity
- Physical chemistry: Random 0.3-0.7 base
- Emotional intimacy: +0.1 per vulnerable moment
- Timing: Right life phase: +0.2

**Attraction doesn't guarantee relationship:**
- High attraction + low trust = tension
- High trust + low attraction = deep friendship
- Both high = romantic potential

---

### Compatibility Scoring

**AI calculates compatibility:**

```javascript
function calculateCompatibility(npc, player) {
  // Trait alignment
  const opennessDiff = Math.abs(npc.openness - player.openness);
  const compatScore = 5 - opennessDiff; // Higher = better
  
  // Complementary traits
  if (npc.extraversion > 3.5 && player.extraversion < 2.5) {
    compatScore -= 0.5; // Might clash
  }
  
  // Shared values
  if (bothValueCreativity && bothValueDepth) {
    compatScore += 1.0;
  }
  
  // Life stage alignment
  if (similarAgeAndGoals) {
    compatScore += 0.5;
  }
  
  return compatScore; // 0.0-5.0 scale
}
```

**Result affects:**
- How quickly relationship deepens
- Natural conversation flow
- Conflict frequency/resolution
- Long-term relationship viability

---

## Emotional Intelligence

### NPCs Notice Player Patterns

**AI tracks player's:**

**Conversation Style:**
- Always supportive → NPC feels safe sharing
- Often challenging → NPC expects debate
- Frequently distracted → NPC feels unvalued
- Deep listener → NPC opens up more

**Activity Preferences:**
- Cultural activities → NPC suggests museums
- Physical activities → NPC invites to sports
- Intellectual pursuits → NPC shares ideas
- Social gatherings → NPC includes in groups

**Relationship Pace:**
- Fast-moving → NPC might feel rushed or excited
- Slow-burn → NPC respects boundaries
- Inconsistent → NPC feels confused
- Steady → NPC feels secure

**Emotional Availability:**
- Always there → NPC relies on you
- Sometimes distant → NPC learns independence
- Unpredictable → NPC feels insecure
- Balanced → NPC appreciates space

---

### NPCs Have Agency

**They make their own choices:**

**Initiate Activities:**
```
"Hey, I found this great bookstore. Want to check
it out this weekend? I think you'd love it."
```

**Share Life Updates:**
```
"So... I applied for that grant I was telling you
about. I'm terrified but also... excited?"
```

**Express Needs:**
```
"I feel like we haven't really talked in a while.
Can we grab coffee? Just the two of us?"
```

**Set Boundaries:**
```
"I appreciate you wanting to help, but I need to
figure this out on my own first."
```

**Have Bad Days:**
```
"I'm sorry, I'm just not in the mood for this
today. Can we reschedule?"
```

---

## Advanced AI Features

### Contextual Awareness

**NPCs remember and reference:**
- Current player stress level
- Recent major life events
- Other relationships in your life
- Your career situation
- Time since last interaction

**Example:**
```
If player is stressed from work:
"You look exhausted. Want to just watch something
mindless and not talk about it?"

If player just had breakthrough:
"I heard about your promotion! See? I told you
you'd get it. We should celebrate!"

If you've been neglecting them:
"It's been what, three weeks? I was starting to
think you forgot about me."
```

---

### Predictive Modeling

**AI anticipates needs:**

**Early in relationship:**
- Suggests activities matching your interests
- Shares information at comfortable pace
- Respects boundaries

**Deep relationship:**
- Knows when you need space vs. company
- Brings up topics you'd want to discuss
- Surprises you with thoughtful gestures
- Completes your sentences

**Example:**
```
Marcus (Level 5, knows you well):
"Before you say anything—yes, I brought coffee.
And yes, it's that ridiculously specific order
you always get. Don't look at me like that."
```

---

## Technical Implementation

### Personality State Management

```javascript
class NPCPersonality {
  constructor(base) {
    this.ocean = { ...base.ocean };
    this.memories = [];
    this.trust = 0.0;
    this.attraction = Math.random() * 0.4 + 0.3;
    this.relationshipLevel = 1;
  }
  
  evolve(interaction) {
    // Update traits
    this.ocean.openness += interaction.traits.openness || 0;
    
    // Add memory
    this.memories.push({
      ...interaction,
      weight: this.calculateWeight(interaction)
    });
    
    // Update trust
    this.trust = Math.min(1.0, this.trust + interaction.trust_delta);
    
    // Check for level up
    if (this.shouldLevelUp()) {
      this.relationshipLevel++;
    }
  }
  
  generateResponse(context) {
    const relevantMemories = this.getRelevantMemories(context);
    const emotionalState = this.getCurrentEmotionalState();
    
    return AI.generate({
      personality: this.ocean,
      memories: relevantMemories,
      trust: this.trust,
      emotion: emotionalState,
      context: context
    });
  }
}
```

---

## Design Principles

### 1. Psychological Realism
NPCs behave like real people with consistent personalities.

### 2. Growth Through Interaction
Relationships change you and change them.

### 3. Memory Matters
Past interactions inform present behavior.

### 4. Imperfect Understanding
NPCs can misunderstand, have bad days, make mistakes.

### 5. Agency and Boundaries
NPCs have their own lives and limits.

### 6. Character Depth Through Contradiction (NEW)
NPCs occasionally act against established patterns, revealing hidden complexity.

### 7. Hidden Motivations (NEW)
NPCs think and plan beyond what they reveal to the player.

---

## NEW: Character Contradiction System

### Purpose

**Goal:** Make NPCs feel less predictable and more human by having them occasionally act against established patterns, revealing hidden depths.

**Frequency:** 1-2 contradiction moments per major NPC per season

**Philosophy:** Real people aren't consistent. They surprise us. A cautious friend takes a big risk. A supportive friend confronts you. These moments make characters memorable and three-dimensional.

---

### Contradiction Types

```javascript
const CHARACTER_CONTRADICTION_SYSTEM = {
  frequency: "1-2 times per season per major NPC (Level 3+)",
  
  timing: "Mid-Act II or before major narrative beats",
  
  purpose: [
    "Reveal hidden depth",
    "Make NPC less predictable", 
    "Create memorable character moment",
    "Challenge player assumptions"
  ],
  
  types: {
    cautious_becomes_bold: {
      description: "Reserved/careful NPC takes unexpected risk",
      
      examples: [
        {
          npc: "Sarah",
          established_pattern: {
            openness: 2.5,                   // Low openness
            conscientiousness: 4.2,          // High conscientiousness
            behavior: "Careful, plans everything, risk-averse, takes months to make decisions"
          },
          
          contradiction_moment: {
            week: 16,
            trigger: "Breaking through fear after therapy/growth",
            action: "Quits stable job to open bookshop within 1 month",
            narrative: `
              Sarah texts: "I did something crazy. Quit my job. Opening the bookshop next month. 
              I know it's reckless but... I'm tired of being scared."
              
              You stare at your phone. This is Sarah. Careful Sarah. Sarah who took 3 months 
              to decide on a haircut.
              
              But maybe she's been changing. Maybe you didn't notice.
            `
          },
          
          reveals: "Sarah has been fighting fear since David died. This is breakthrough moment.",
          
          affects: {
            player_perception: "Realize you may have underestimated Sarah",
            relationship: "Respect increases, dynamic shifts",
            future_interactions: "Sarah more confident in subsequent scenes"
          },
          
          believable_because: "Foreshadowed through therapy mentions, David backstory, gradual confidence build"
        }
      ]
    },
    
    supportive_becomes_confrontational: {
      description: "Always-supportive NPC confronts/challenges player",
      
      examples: [
        {
          npc: "Marcus",
          established_pattern: {
            agreeableness: 4.5,              // High agreeableness
            extraversion: 3.8,               // Warm and social
            behavior: "Supportive, encouraging, positive, always has your back"
          },
          
          contradiction_moment: {
            week: 18,
            trigger: "Player physical meter < 3 for 4+ weeks, Marcus increasingly worried",
            action: "Direct confrontation expressing disappointment",
            narrative: `
              Marcus: "I think you're making a mistake. I think you're sacrificing too much 
              for this. And I think you don't want to hear it, but I'm going to say it anyway."
              
              You've never heard him like this. Sharp. Frustrated. Disappointed.
              
              Marcus: "I support you. Always will. But I'm not going to pretend this is 
              healthy anymore."
              
              He's your friend. That's why he's saying it. You know that.
              
              But it still hurts.
            `
          },
          
          reveals: "Marcus's support has boundaries. He values honesty over comfort. His caring includes being willing to risk friendship to speak truth.",
          
          affects: {
            player_perception: "Marcus isn't just cheerleader - he's real friend with real concerns",
            relationship: {
              immediate: "Stings, might lower trust slightly (-0.05)",
              long_term: "If player responds well, trust increases significantly (+0.2)",
              dynamic: "Relationship deepens - can handle difficult conversations"
            }
          },
          
          believable_because: "Preceded by weeks of subtle concern, building worry, failed gentle hints"
        }
      ]
    },
    
    reserved_becomes_vulnerable: {
      description: "Emotionally guarded NPC opens up unexpectedly",
      
      examples: [
        {
          npc: "Sarah",
          established_pattern: {
            neuroticism: 3.8,                // Higher anxiety
            behavior: "Emotionally distant, doesn't share feelings, deflects personal questions"
          },
          
          contradiction_moment: {
            week: 22,
            trigger: "Trust threshold reached (0.85+) + anniversary of David's death",
            action: "Fully opens up about past trauma",
            narrative: `
              Sarah's been quiet all evening. Then:
              
              "David died five years ago today. Car accident. Week before our wedding."
              
              She's crying. You've never seen her cry. Not once in all these months.
              
              "I was terrified of telling you. Terrified you'd see me as broken. But... 
              I think you deserve to know why I am the way I am."
            `
          },
          
          reveals: "All her behavior - distance, fear of commitment, emotional walls - makes sense now",
          
          affects: {
            player_understanding: "Entire relationship recontextualizes",
            relationship: {
              trust: +0.3,
              level_up_possible: true,
              intimacy: "Major breakthrough",
              future_behavior: "Sarah gradually more open after this"
            }
          },
          
          believable_because: "Built up through mystery thread, earned through consistent support, timing is meaningful (anniversary)"
        }
      ]
    },
    
    optimistic_shows_darkness: {
      description: "Usually positive NPC reveals struggle/shadow side",
      
      examples: [
        {
          npc: "Marcus",
          contradiction_moment: {
            week: 20,
            narrative: `
              Marcus, always cheerful Marcus, sits with beer untouched.
              
              "Can I tell you something? I'm... not okay. Haven't been for a while. 
              I just... put on the smile because that's what I do. But I'm exhausted."
              
              This is new. This is real. This is Marcus without the mask.
            `
          },
          
          reveals: "Even the 'together' friend struggles. His support of you is also him avoiding his own problems."
        }
      ]
    }
  },
  
  implementation_rules: {
    must_be_earned: "Contradiction moments require sufficient relationship level (3+) and trust (0.6+)",
    must_be_foreshadowed: "Subtle hints in prior weeks that complexity exists",
    must_be_believable: "Contradiction reveals hidden truth, doesn't break character",
    affects_future: "NPC behavior adjusts after contradiction moment",
    permanent_impact: "These moments become high-weight memories"
  }
};
```

---

## NEW: Hidden Motivations System

### NPCs Think Beyond What They Say

**Purpose:** Create depth through dramatic irony - NPCs have internal lives, thoughts, and plans player doesn't see (until they do).

```javascript
const HIDDEN_MOTIVATION_SYSTEM = {
  principle: "NPCs have thoughts, feelings, and plans that player doesn't know about",
  
  revelation_method: [
    "Dramatic irony cards (show NPC perspective)",
    "Overheard conversations",
    "Third-party reveals",
    "NPC finally tells player directly"
  ],
  
  examples: {
    sarah_grief_david: {
      hidden_motivation: "Sarah is emotionally distant because she's terrified of losing someone again after David's death",
      
      player_sees: "Sarah is warm but keeps distance, doesn't want to get too close",
      
      sarah_actually_thinking: `
        "I like [Player Name]. A lot. Maybe too much. What if something happens 
        to them too? What if I can't handle losing someone again?"
      `,
      
      revelation_path: [
        "Week 5: Mentions David, changes subject (mystery planted)",
        "Week 10: Dramatic irony card shows Sarah's POV thinking about David",
        "Week 15: Friend mentions Sarah was engaged once",
        "Week 22: Sarah finally tells full story"
      ],
      
      payoff: "Player understands ALL of Sarah's behavior retroactively. 'Oh. That's why.'"
    },
    
    marcus_health_concern: {
      hidden_motivation: "Marcus has been discussing intervention with Sarah for weeks, worried about player's health",
      
      player_sees: "Marcus seems concerned sometimes, asks if you're okay",
      
      marcus_actually_thinking: `
        "They look terrible. When's the last time they slept properly? Sarah and I 
        have been talking about it. We need to say something. But I don't want to 
        seem like I'm nagging..."
      `,
      
      revelation_path: [
        "Week 10: Dramatic irony card from Marcus's POV watching player with concern",
        "Week 12: Overhear Marcus on phone: 'I'm worried about them...'",
        "Week 14: Marcus confronts player directly about health"
      ],
      
      payoff: "Player realizes friends have been worried for weeks. Wake-up call."
    },
    
    mentor_secret_pride: {
      hidden_motivation: "Mentor is secretly proud of player but struggles to show it (own father was critical)",
      
      player_sees: "Mentor is demanding, rarely gives praise, hard to please",
      
      mentor_actually_thinking: `
        "They're doing so well. Better than I was at their age. I should tell them. 
        But... I don't know how. Dad never praised me. Don't know how to do it."
      `,
      
      revelation: "Week 20: Mentor breaks down and admits pride + explains own father issues",
      
      payoff: "Harsh criticism was love language all along"
    },
    
    boss_protecting_player: {
      hidden_motivation: "Boss has been shielding player from upper management criticism",
      
      player_sees: "Boss seems distant, formal, maybe disappointed",
      
      boss_actually_thinking: `
        "Upper management wanted to put [Player Name] on performance plan. I fought 
        for them. Convinced them to give more time. But I can't tell them that..."
      `,
      
      revelation: "Week 16: Overhear boss defending player in closed meeting",
      
      payoff: "Boss isn't enemy - they're secret ally"
    }
  },
  
  implementation: {
    track_internally: "System tracks NPC internal state even when player doesn't see it",
    reveal_strategically: "Dramatic irony cards or key conversations reveal truth",
    creates_depth: "NPCs feel like real people with inner lives",
    affects_decisions: "Player makes different choices once they understand motivations"
  },
  
  integration_with_mysteries: {
    hidden_motivations_are_mysteries: true,
    use_mystery_thread_system: "Plant clues, escalate, reveal",
    emotional_payoff: "Understanding character motivation deepens relationship"
  }
};
```

---

## Player Impact

**Players should notice:**
- NPCs remember what they say
- Personality shifts feel earned
- Relationships require maintenance
- Different approaches yield different results
- Each NPC feels like an individual

**Players should never feel:**
- NPCs are robots following scripts
- All NPCs are the same
- Choices don't matter
- Relationships are guaranteed
- Personality changes are random

---

## Long-Term NPC Evolution

### NPCs Across Lifetimes

For details on how NPCs live parallel lives across 3000+ weeks, see **`22-multi-lifetime-continuity.md`**:

**Key Systems:**
- **Parallel Aging:** NPCs age at same rate as player (28 → 38 over 520 weeks)
- **Background Life Events:** NPCs have careers, relationships, achievements happening off-screen
- **Departure & Return:** NPCs can move away, return years later, or leave permanently
- **Personality Drift:** OCEAN traits evolve based on their life experiences
- **Memory Persistence:** NPCs remember your shared history, even after years apart

**Example Evolution:**
```
Sarah, Week 1:
  Age: 28, Barista
  Personality: [3.5, 4.0, 2.8, 3.9, 3.8]
  Relationship: Stranger
  
Sarah, Week 150:
  Age: 31, Bookshop Owner
  Personality: [4.3, 4.5, 3.4, 4.6, 2.9]
  Relationship: Business Partner (Bond: 0.95)
  Evolution: +0.8 Openness (took risks), +0.6 Extraversion (business owner), -0.9 Neuroticism (confidence)
  
Sarah, Week 520:
  Age: 38, Established Business Owner
  Personality: [4.6, 4.7, 3.8, 4.8, 2.5]
  Relationship: Deep Partnership (potentially romantic)
  Life Events: Bookshop expanded, won local award, became mentor to young entrepreneurs
```

**Canonical Consistency:**
- Core identity facts never contradict (see `22-multi-lifetime-continuity.md` → Canonical Facts System)
- Past conversations remembered through multi-tier memory system
- Relationship history preserved even after periods of no contact
- NPCs reference shared history authentically in dialogue

---

## Integration with Other Systems

**Character Creation (`20-character-creation.md`):**
- Player personality established through scenario-based questions
- Starting compatibility calculated with NPCs
- Personality influences starting hand composition

**Turn Structure (`21-turn-structure.md`):**
- NPC availability cards filtered by time of day, relationship level
- Conversations generate micro-narratives based on personality + memories
- Relationship changes tracked per interaction

**Emotional States (`19-emotional-state-system.md`):**
- NPCs have their own emotional states that affect interactions
- Player's emotional state influences success of social cards
- Emotional compatibility creates dynamic relationship chemistry

**Novel Generation (`novel-generation-data-structure.md`):**
- Full character state snapshots feed chapter generation
- Voice profiles ensure NPCs sound consistent across chapters
- Memory fragments surface in dialogue naturally

