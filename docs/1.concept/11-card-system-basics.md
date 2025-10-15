# Unwritten: Card System Basics

## Card Type Taxonomy

### Base Card Count: 470 Cards
- 50 Character (NPC) Cards
- 80 Activity Cards
- 30 Location Cards
- 20 Emotion Cards  
- 20 Resource Cards
- 90 Aspiration Cards (Life goals)
- 150 Situation Cards (Events & choices)
- 30 System Cards (Skills, items, perks)

All base cards available free. Expansion packs add themed card sets.

---

## Core Card Types

### 1. Character Cards (NPCs)

Characters are people you meet and build relationships with.

**Structure:**
```
┌─────────────────────────┐
│ CHARACTER NAME          │
│ Level • Relationship    │
├─────────────────────────┤
│ [Portrait]              │
│                         │
│ OCEAN Personality:      │
│ Openness: 3.5           │
│ Conscientiousness: 4.0  │
│ Extraversion: 2.8       │
│ Agreeableness: 3.9      │
│ Neuroticism: 3.2        │
│                         │
│ Description text        │
│                         │
│ Memories: [List]        │
├─────────────────────────┤
│ Can combine with:       │
│ • Activity Cards        │
│ • Location Cards        │
└─────────────────────────┘
```

**50 Base Character Archetypes:**
- Barista, neighbor, coworker, gym regular
- Each has distinct personality but NO history yet
- Generic descriptions that evolve through play
- Waiting to become something unique

**Relationship Levels (0-5):**
0. Not Met (never interacted - displayed as "Not Met", never "Level 0")
1. Stranger (first meeting through 5 interactions)
2. Acquaintance (6-15 interactions)
3. Friend (16-30 interactions)
4. Close Friend (31-75 interactions)
5. Soulmate/Best Friend (76+ interactions)

**Display Format:** "Level 3 (Trust 0.52)" - showing both discrete level and continuous trust

---

### 2. Activity Cards

Activities are things you do, often with characters.

**Structure:**
```
┌─────────────────────────┐
│ ACTIVITY NAME           │
│ Category • Duration     │
├─────────────────────────┤
│ [Illustration]          │
│                         │
│ Description             │
│                         │
│ Costs:                  │
│ • Energy                │
│ • Time                  │
│ • Money (optional)      │
│                         │
│ Effects:                │
│ • Meter changes         │
│ • Relationship impact   │
│                         │
│ Can combine with:       │
│ • Character Cards       │
│ • Emotion Cards         │
│ • Location Cards        │
└─────────────────────────┘
```

**80 Base Activity Categories:**

**Social Activities:**
- Coffee meetup, dinner date, movie night
- Party, concert, game night
- Deep conversation, casual hangout

**Work Activities:**
- Meeting, project work, networking
- Presentation, career development

**Creative Activities:**
- Painting, music practice, writing
- Crafting, photography

**Physical Activities:**
- Gym workout, sports, hiking
- Yoga, dance class, martial arts

**Learning Activities:**
- Classes, reading, workshop
- Practice skill, research

**Domestic Activities:**
- Cooking, cleaning, decorating
- Gardening, home improvement

---

### 3. Location Cards

Locations are places that gain meaning through the memories made there.

**Structure:**
```
┌─────────────────────────┐
│ LOCATION NAME           │
│ Type                    │
├─────────────────────────┤
│ [Scene illustration]    │
│                         │
│ Description             │
│                         │
│ Available Activities:   │
│ • List of what you      │
│   can do here           │
│                         │
│ Memories Made: [Count]  │
└─────────────────────────┘
```

**30 Base Location Types:**
- Home (apartment, house)
- Workplace (office, studio, shop)
- Social venues (café, bar, restaurant)
- Public spaces (park, library, mall)
- Recreation (gym, theater, museum)
- Special (beach, concert hall, gallery)

**Location Evolution:**
Generic "Local Café" → "Café Luna - Your Third Place"
- Shows YOUR corner table
- Lists memories made there
- May trigger nostalgic events

---

### 4. Emotion Cards

**⚠️ SPECIAL CARD TYPE: Automatic & Persistent**

Unlike other cards, emotional states are **automatically determined** at the start of each turn based on your character's current feelings. They don't occupy hand slots but actively filter and modify your available options.

**How Emotional States Work:**

1. **Automatic Detection:** System analyzes meters, recent events, personality, and context
2. **Active States Displayed:** 1-2 emotional states shown at turn start (Primary + Secondary)
3. **Hand Filtering:** Available cards filtered and weighted by your current emotions
4. **State Evolution:** Your choices affect how you feel, creating dynamic emotional journeys

**Structure:**
```
┌─────────────────────────┐
│ 🔵 YOU FEEL: OVERWHELMED│
│ 🟡 AND ALSO: RESTLESS   │
├─────────────────────────┤
│ [Emotional context text]│
│                         │
│ This affects:           │
│ • Which cards appear    │
│ • Energy costs          │
│ • Success chances       │
│ • Appeal of options     │
│                         │
│ Your choices will shift │
│ how you feel next turn  │
└─────────────────────────┘
```

**20 Emotional States:**

**Energizing (Positive High-Energy):**
- Motivated, Inspired, Excited, Confident

**Calm (Positive Low-Energy):**
- Content, Peaceful, Grateful, Reflective

**Energizing (Negative High-Energy):**
- Frustrated, Anxious, Restless, Passionate

**Withdrawing (Negative Low-Energy):**
- Melancholy, Discouraged, Numb, Exhausted

**Neutral:**
- Curious, Focused, Balanced, Uncertain

**For detailed mechanics, see:** `19-emotional-state-system.md`

**Key Difference from Other Cards:**
- You don't "play" emotion cards
- They're always active, shaping your experience
- They evolve based on what you do
- Managing your emotional state is core gameplay

---

### 5. Aspiration Cards

Aspirations are life goals that structure your playthrough.

**Structure:**
```
┌─────────────────────────┐
│ ASPIRATION NAME         │
│ Life Goal • Duration    │
├─────────────────────────┤
│ Description of goal     │
│                         │
│ Requirements:           │
│ • What you need         │
│                         │
│ Progress: [Bar]         │
│                         │
│ Rewards:                │
│ • Unlocks               │
│ • Bonuses               │
│                         │
│ Compatible with:        │
│ • Life Direction        │
│ • Career path           │
└─────────────────────────┘
```

**90 Base Aspirations:**

**Major Aspirations (24-48 weeks):**
- Start a business
- Write a novel
- Find deep love
- Master a craft
- Build a family
- Achieve financial freedom

**Minor Aspirations (4-12 weeks):**
- Learn a skill to Level 5
- Deepen a friendship
- Complete a creative project
- Improve physical fitness
- Redecorate home

---

### 6. Situation Cards

Situations are events and choices that drive narrative.

**Structure:**
```
┌─────────────────────────┐
│ SITUATION NAME          │
│ Event Type              │
├─────────────────────────┤
│ Scenario description    │
│                         │
│ Choices:                │
│ → Option A              │
│   (Effects)             │
│                         │
│ → Option B              │
│   (Effects)             │
│                         │
│ → Option C              │
│   (Effects)             │
└─────────────────────────┘
```

**150 Base Situation Types:**

**NPC-Initiated (50):**
- Friend asks for help
- Character shares secret
- Invitation to event
- Request for advice
- Confession or revelation

**Random Life Events (50):**
- Job opportunity
- Housing change
- Unexpected windfall
- Minor crisis
- Chance encounter

**Crisis Events (25):**
- Job loss, health scare
- Relationship conflict
- Financial trouble
- Major life decision

**Breakthrough Events (25):**
- Achievement unlock
- Relationship milestone
- Career advancement
- Personal growth moment

---

### 7. Resource Cards

Resources are persistent elements that affect gameplay.

**Types:**

**Housing:**
```
┌─────────────────────────┐
│ YOUR APARTMENT          │
│ Living Space            │
├─────────────────────────┤
│ [Interior sketch]       │
│                         │
│ Monthly Cost: $1200     │
│                         │
│ Effects:                │
│ • +1 Energy/day         │
│ • Can host 2 guests     │
│                         │
│ Upgradeable             │
└─────────────────────────┘
```

**Career:**
- Job title, salary, schedule
- Work activities unlocked
- Career progression path

**Items:**
- Car, laptop, musical instrument
- Enables specific activities
- May evolve with use

**Skills:**
- Cooking, programming, art
- Level 1-10 progression
- Unlocks activities & dialogue

---

## Card Rarity System

### Common (Gray Border)
- Base cards as drawn
- 85% of all cards
- Foundation for evolution

### Uncommon (Green Border)
- First evolution level
- Slight personalization
- 10% of cards

### Rare (Blue Border)
- Deep personalization
- Significant memories
- 4% of cards

### Epic (Purple Border)
- Major fusion results
- Life-changing cards
- 0.9% of cards

### Legendary (Gold Border)
- Ultimate evolutions
- Unique story climax cards
- 0.1% of cards
- Can only exist in specific conditions

**Note:** Rarity is EARNED through play, not random drops. Every card can become legendary through the right story.

---

## Card Anatomy

### Visual Elements

**Portrait (Character Cards):**
- Base: Generic illustration
- Evolved: Specific details from YOUR story
- Shows items you gave them
- Expression reflects relationship

**Border:**
- Color indicates relationship level or rarity
- Glow effects for high-level cards
- Animated particles for legendary

**Background:**
- Base: Simple texture
- Evolved: Meaningful scenery
- Legendary: Collage of shared memories

**Text:**
- Base: Generic description
- Evolved: Personalized narrative
- Includes memory timestamps
- "Micro-narratives" (1-3 quotable lines)

### Metadata

**Every card contains:**
- Unique ID
- Type & category
- Level (if applicable)
- Creation date (base or evolved)
- Parent cards (if fusion)
- Combination possibilities
- Effects & costs
- Unlock requirements

---

## Card Acquisition

### How You Get Base Cards

**Starting Deck:** 50 cards
- 10 characters
- 20 activities
- 10 locations
- 5 emotions
- 5 resources

**Unlock Through Play:**
- Meet milestone → Unlock 10 cards
- Complete aspiration → Unlock 5 cards
- Reach Phase 2 → Unlock 50 cards
- Reach Phase 3 → All 470 base cards available

**Premium/DLC:**
- Subscription: +300 themed cards
- Card packs: +20 cards per pack
- All cards can still evolve same way

---

## Card Limits & Deck Management

### Active Deck
- 20-30 cards in "active rotation"
- These appear in daily draws
- Can manually add/remove cards

### Collection
- All unlocked base cards
- All evolved cards from current run
- Filterable by type, level, recency

### Archive (Past Runs)
- Evolved cards from completed runs
- View-only, cannot be played
- Organized by playthrough

---

## Card Costs

### Energy Cost
- Light activities: 1 energy
- Medium activities: 2 energy
- Heavy activities: 3 energy
- Epic moments: Variable

### Time Cost
- Quick (30 min)
- Short (1-2 hours)
- Medium (3-4 hours)
- Long (6+ hours)

### Money Cost (Optional)
- Free activities (most)
- Budget ($5-20)
- Moderate ($25-50)
- Expensive ($100+)

### Success Chance (Some cards)
- Guaranteed (most cards)
- High (80%+)
- Medium (50-70%)
- Risky (30-50%)
- Long shot (<30%)

---

## Card States

**Active:** Can be played right now
**Locked:** Requirements not met yet
**Cooldown:** Recently used, need time
**Evolved:** New version generated
**Archived:** From past run, view-only
**Favorited:** Manually marked important

---

## Design Principles

### 1. Base Cards Are Blank Slates
They're intentionally generic so YOUR story makes them unique.

### 2. Every Card Can Evolve
No card is "trash." Everything has potential through the right combinations.

### 3. Complexity Through Combination
Simple cards + smart combinations = emergent complexity.

### 4. Meaningful Not Overwhelming
470 base cards, but you only interact with 20-30 actively. Collection grows naturally.

### 5. Visual Storytelling
Every evolved card should be screenshot-worthy and shareable.

