# Unwritten: Card Evolution System

## Evolution Philosophy

Cards don't just level up—they **remember**. Each evolution captures a specific moment from YOUR playthrough, creating a personalized narrative that belongs only to you.

**Integration:** Evolution happens naturally during gameplay as you play cards in your daily turns (see `21-turn-structure.md`). Each meaningful interaction can trigger evolution, tracked through the multi-lifetime continuity system (`22-multi-lifetime-continuity.md`).

---

## How Evolution Works

### The Basic Process

```
PLAYER ACTION
    ↓
CONTEXT ANALYSIS
(What happened? Who was involved? What choices were made?)
    ↓
AI GENERATION
(Create personalized memory, update personality, add details)
    ↓
CARD UPDATE
(New portrait, description, memories, unlocks)
    ↓
VISUAL RENDERING
(Show evolution with animation)
```

---

## Evolution Triggers

### 1. Character + Activity Combination

**Example:**
```
[SARAH ANDERSON] + [COFFEE MEETUP]
         ↓
AI analyzes the interaction
         ↓
Generates evolved version
```

**Before:**
```
SARAH ANDERSON
Level 1 • Stranger

[Generic portrait]

"Works at the coffee shop. Seems nice."

Memories: [Empty]
```

**After:**
```
SARAH ANDERSON  
Level 2 • Acquaintance

[Portrait now shows blue scarf she mentioned]

"Sarah opened up about her passion for vintage
book collecting. She has this infectious laugh
when talking about rare finds."

Memories:
☕ "That coffee where she shared her dream
    of opening a bookshop someday"

Unlocked:
• Bookstore visits
• Literature discussions
```

**What Changed:**
- Portrait updated with specific detail
- Generic description → Unique personality
- Memory created with emotional context
- New activities unlocked
- Relationship level increased

---

### 2. Triple Combination: Character + Activity + Emotion

More complex combinations create deeper evolution.

**Example:**
```
[SARAH] + [BOOKSTORE VISIT] + [EXCITEMENT]
                ↓
        AI GENERATES NEW FUSION:
        
"THE BOOKSHOP DREAM"
Unique Quest Card

"After months of talks, Sarah shared her actual
business plan. She wants YOU to be part of it."

Choices:
→ Invest savings (High risk, new career path)
→ Offer part-time help (Medium commitment)  
→ Encourage but stay out (Safe, less bond)

This decision permanently alters your relationship path.
```

---

### 3. Multi-Card Fusion

**Resource + Character + Event:**
```
[YOUR APARTMENT] + [SARAH] + [CRISIS EVENT]
                ↓
        TEMPORARY ROOMMATE CARD

"Sarah's lease fell through. She's staying on your
couch while she figures things out."

Duration: 2-4 weeks

Effects:
• +5 Sarah bond per week
• -1 Privacy
• New daily activities unlocked
• May evolve into permanent roommate

Your APARTMENT card is now different:

SHARED SPACE
[Art now shows two coffee mugs, her books scattered]
"It's not just YOUR place anymore."
```

---

## Character Evolution Levels

### Level 1 → 2: Stranger → Acquaintance (5-10 interactions)

**Triggers:**
- Regular interactions (coffee, chitchat)
- First real conversation
- Learning basic info

**Changes:**
- Generic traits → Specific personality emerges
- "Seems nice" → "Has dry humor that catches you off-guard"
- Basic portrait → One identifying feature added
- Unlock: Casual hangout activities

---

### Level 2 → 3: Acquaintance → Friend (15-25 interactions)

**Triggers:**
- Deep conversation
- Helping with something
- Spending significant time together
- Sharing vulnerabilities

**Changes:**
- Surface details → Deep backstory revealed
- "Works at café" → "Saving to open bookshop, talks about late grandmother"
- Multiple memories accumulated
- Unlock: Help with problems, introduce to other friends

---

### Level 3 → 4: Friend → Close Friend (30-50 interactions)

**Triggers:**
- Crisis support
- Major life event together
- Consistent presence
- Trust demonstrations

**Changes:**
- Known history → Shared experiences
- Past memories → Inside jokes and references
- Portrait reflects shared aesthetic
- Unlock: Crisis support, life-changing decisions together

---

### Level 4 → 5: Close Friend → Soulmate/Found Family (75+ interactions)

**Triggers:**
- Defining moments together
- Years of story accumulated
- Major accomplishments as a unit
- Deep emotional bonds

**Changes:**
- Individual → Part of your life story
- Generic portrait → Portrait reflects YOUR shared journey
- Unique fusion cards available
- Unlock: Life-changing combination cards (move together, start business, family bonds)

---

## Activity Evolution

Activities don't just level up—they become rituals specific to your relationships.

**Base Activity:**
```
COFFEE MEETUP
"Standard coffee date"
Effects: +1 Social, -1 Energy
```

**After 5 uses with Sarah:**
```
"OUR" COFFEE RITUAL
Evolved Activity

[Illustration: Specific café corner you always sit]

"Your Tuesday morning tradition at Café Luna.
Sarah saves the window seat. You bring the
crossword. She brings terrible puns."

Special Effects:
• +3 Social (was +1)
• +0.5 Sarah bond
• Restore 1 stress
• Trigger random memory flashback

This card is unique to your relationship with Sarah.
It cannot exist with other NPCs.
```

---

## Location Evolution

Places gain meaning through memories made there.

**Base Location:**
```
LOCAL CAFÉ
"A coffee shop. Nothing special."
```

**After 47 memories there:**
```
CAFÉ LUNA
"Your Third Place"

[Now shows YOUR corner, the art you noticed, plant by window]

"Where you met Sarah. Where Marcus told you about
his diagnosis. Where you decided to quit your job.
This place holds your story."

Memories Tied Here: 47

Special: When played alone, may trigger nostalgic
event card featuring past characters.
```

---

## AI Evolution Pipeline

### Step 1: Context Gathering

```javascript
const evolutionContext = {
  // What just happened
  immediateEvent: "Player had deep conversation with Sarah about fears",
  
  // Relationship history
  relationshipLevel: 3.7,
  previousInteractions: [
    "Coffee dates (12x)",
    "Bookstore visits (5x)",
    "Helped her move (1x)",
    "Shared vulnerability (2x)"
  ],
  
  // Player's style (learned over time)
  playerTendencies: {
    conversationStyle: "supportive, curious, not pushy",
    activityPreferences: ["cultural", "quiet", "intellectual"],
    relationshipPace: "slow-burn, values depth"
  },
  
  // Current life context
  playerCareer: "Software Developer",
  playerStressLevel: 6.5,
  recentLifeEvents: ["Promotion", "Moved apartments"]
};
```

---

### Step 2: AI Prompt Construction

```
Given this context, generate an evolved version of Sarah's card:

1. MEMORY: Create a specific memory of this interaction
   - Include sensory details (setting?)
   - Emotional beats (turning point?)
   - Small detail that makes it real (hands, gesture?)
   - One line of dialogue that captures the moment

2. PERSONALITY SHIFT: Adjust traits slightly
   - Which OCEAN traits shift from this interaction?
   - By how much? (0.1-0.3 points)
   - Why does this make psychological sense?

3. NEW DETAIL: Reveal something new about her
   - Something she hasn't shared before
   - Related to conversation topic
   - Adds depth without being random
   - Creates new story threads

4. UNLOCK: What new combinations does this enable?
   - What can you now do together?
   - What locations/activities are meaningful?
   - What future story beats does this set up?

5. PORTRAIT UPDATE: Describe one visual change
   - Detail that reflects this memory
   - Something player would notice
   - Consistent with previous description

Make this feel earned, specific, and emotionally resonant.
```

---

### Step 3: AI Generated Output

```json
{
  "memory": {
    "description": "Late night at Café Luna. Sarah's hands wrapped around a cold mug, speaking quietly about the fear of trying and failing. 'What if I open the shop and no one comes?' she said. You told her about your own fear of the promotion. She smiled and said, 'Then we'll both be brave failures together.'",
    "emotion": "vulnerable_solidarity",
    "weight": 0.85,
    "setting": "Café Luna, after closing, dim lights"
  },
  
  "personality_shifts": {
    "neuroticism": -0.2,
    "agreeableness": +0.15,
    "openness": +0.1
  },
  
  "new_detail": {
    "revelation": "Her grandmother left her $15,000 specifically for 'something brave.' Sarah's been too scared to use it. Until maybe now.",
    "impact": "Adds stakes - money is sacred, tied to grandmother's memory"
  },
  
  "unlocked_combinations": [
    {
      "name": "Business Planning Session",
      "cards": ["Sarah", "Café", "Notebook Item"],
      "description": "Help Sarah actually plan the bookshop"
    },
    {
      "name": "Visit Grandmother's Grave",
      "cards": ["Sarah", "Cemetery Location", "Flowers Item"],
      "description": "She wants to tell grandmother about plan"
    }
  ],
  
  "portrait_update": {
    "add": "Small notebook visible in her bag - her business plan",
    "expression": "More determined, less uncertain"
  }
}
```

---

### Step 4: Card Rendering

The game takes AI output and creates the updated card:

```
┌─────────────────────────┐
│ SARAH ANDERSON          │
│ Level 3 • Close Friend  │
├─────────────────────────┤
│ [Updated portrait:      │
│  Determined expression, │
│  notebook in bag]       │
│                         │
│ OCEAN:                  │
│ Openness: 3.8 ↑        │
│ Agreeableness: 4.1 ↑    │
│ Neuroticism: 3.0 ↓      │
│                         │
│ "Sarah trusted you with │
│ her deepest fear—and    │
│ her grandmother's gift. │
│ She's been carrying     │
│ $15k meant for          │
│ 'something brave.'"     │
│                         │
│ Recent Memory:          │
│ 💙 "Late night at Luna. │
│    'Then we'll both be  │
│    brave failures       │
│    together.' Shared    │
│    vulnerability."      │
│                         │
│ New Opportunities:      │
│ • Business Planning     │
│ • Grandmother's Grave   │
│ • Fear & courage talks  │
└─────────────────────────┘
```

---

## Visual Evolution System

### Portrait Changes

**Level 1 (Base):**
- Generic stock illustration
- No specific details
- Neutral expression
- Simple clothing

**Level 2-3 (Personalized):**
- One signature item appears (scarf, necklace)
- More specific facial features
- Subtle personality in expression
- Context-appropriate clothing

**Level 4-5 (Your Version):**
- Items YOU gave them
- Expression reflects YOUR relationship
- Background hints at shared locations
- Details from YOUR story

**Legendary (Max Evolution):**
- Custom illustration of defining moment
- Shows both you and them (if applicable)
- Rich with specific memory details
- Golden border, particle effects

---

### Border Evolution

**Gray** → Stranger/Base
**Green** → Acquaintance/Friend (Level 1-2)
**Blue** → Friend/Close Friend (Level 3)
**Purple** → Close Friend/Best Friend (Level 4)
**Gold** → Soulmate/Legendary (Level 5)
**Rainbow** → Ultra-rare fusion results

---

### Effects Evolution

**Base:** Static image
**Uncommon:** Subtle glow
**Rare:** Pulsing border
**Epic:** Particle shimmer
**Legendary:** Full animation loop

---

## Memory System

### Memory Types

**First Impressions:**
- Very first interaction
- Low detail, vague
- "Seems nice" level

**Significant Moments:**
- Deep conversations
- Helping/being helped
- Shared activities
- Weight: 0.6-0.8

**Defining Moments:**
- Life-changing events
- Major decisions together
- Crisis support
- Weight: 0.85-0.95

**Legendary Moments:**
- Climax of relationship arc
- Ultimate achievements together
- Irreplaceable experiences
- Weight: 1.0

---

### Memory Display

**On Card:**
```
Memories:
☕ Week 2: "First real conversation about books"
📚 Week 5: "She showed you her secret wish list"
💙 Week 12: "Shared fear of failing at dreams"
🏪 Week 28: "Signed bookshop lease together"
👵 Week 31: "Visited grandmother's grave"
🎉 Week 40: "Opening day - both cried"
```

**In Archive:**
Full timeline view with:
- Date of memory
- Location where it happened
- Who else was present
- Full description
- Screenshot of card at that moment

---

## Evolution Constraints

### Psychological Realism

**Personality changes are gradual:**
- Single interaction: 0.1-0.3 point shift
- Major event: 0.3-0.5 point shift
- Multiple events over time: 0.5-1.0 cumulative

**Traits don't contradict:**
- Can't go from high neuroticism to low in one event
- Growth is believable and earned
- Regression is possible but requires reason

**Memories are consistent:**
- AI references previous memories
- New details don't contradict old ones
- Character voice stays consistent

---

### Narrative Pacing

**Early Game (Days 1-30):**
- Slow evolution
- Surface-level changes
- Building foundation

**Mid Game (Days 31-180):**
- Rapid evolution
- Deep relationship growth
- Major fusion cards appear

**Late Game (Days 181+):**
- Refinement and depth
- Legendary cards possible
- Story climax moments

---

## Evolution Failure States

### What Prevents Evolution

**Insufficient Context:**
- Not enough previous interactions
- Incompatible personality match
- Requirements not met

**Player Choice:**
- Selecting "keep distance" options
- Avoiding deep conversations
- Not following up on hints

**Timing:**
- Too soon after previous evolution
- Wrong life phase
- Conflicting goals

---

## Technical Performance

### Caching Strategy

**Common evolutions pre-generated:**
```
sarah_lvl2_coffee_supportive → Cached
sarah_lvl2_bookstore_curious → Cached
sarah_lvl3_crisis_comforting → Cached
```

**Unique evolutions generated on-demand:**
```
sarah_lvl4_business_partner_YOUR_specific_story → Generated fresh
```

**Result:**
- 80% of evolutions use cached templates (200ms)
- 20% fully custom AI generation (750ms local, 2s cloud)
- Seamless player experience

---

## Design Goals

### Emotional Investment

**Players should:**
- Feel attached to evolved versions
- Notice small details changing
- Remember specific moments
- Want to screenshot and share
- Feel loss when run ends

### Narrative Coherence

**Evolution should:**
- Feel earned, not random
- Build on previous moments
- Create story arcs
- Lead to meaningful conclusions
- Support player's chosen playstyle

### Replayability

**System should:**
- Create different evolutions each run
- Support multiple relationship paths
- Never feel repetitive
- Reward experimentation
- Make "what if?" compelling

---

## Integration with Core Systems

### Turn Structure (`21-turn-structure.md`)
**When Evolution Happens:**
- After playing card combinations (Character + Activity)
- During significant relationship moments
- At end of meaningful days/weeks
- After decisive decisions or crisis events

**Evolution Tracking:**
```javascript
// Card play resolution
const resolution = await resolveCard(card, gameState);

// Check for evolution trigger
if (shouldEvolve(card, resolution, gameState)) {
  const evolution = await generateEvolution(card, resolution);
  displayEvolutionAnimation(evolution);
  updateDeck(card.id, evolution);
}
```

### Multi-Lifetime Continuity (`22-multi-lifetime-continuity.md`)
**Long-Term Evolution Tracking:**
- All evolutions stored in Tier 1 (Current) and Tier 3 (Compressed)
- Character canonical facts prevent evolution contradictions
- NPC personality drift influences how they evolve with you
- Evolution history feeds novel generation

**Example:**
```
Week 1: Sarah Level 1 (Stranger at café)
Week 28: Sarah Level 2 (Revealed business plan) → Evolution captured
Week 67: Sarah Level 3 (Business partner) → Evolution captured  
Week 95: Sarah Level 4 (Bookshop opening) → Evolution captured
Week 150: Sarah Level 5 (Established success) → Evolution captured

Each evolution preserved with:
- Full narrative context
- Personality snapshot at that moment
- Relationship state
- Memorable quotes/moments
```

### Novel Generation (`novel-generation-data-structure.md`)
**Evolution as Story Beats:**
- Major evolutions become chapter moments
- Character memories inform dialogue
- Personality changes tracked for narrative arc
- Visual evolution described in prose

**Example Novel Callback:**
```
"You remember the day Sarah showed you that business plan. 
Her hands trembling on the worn notebook. That was the day 
everything changed between you."

→ References Level 1 → Level 2 evolution moment
```

### Archive System (`16-archive-persistence.md`)
**Evolution in Archives:**
- Final evolved states preserved in Archive
- Character gallery shows full evolution sequence
- Novel includes evolution moments as key chapters
- Screenshots of major evolutions saved

