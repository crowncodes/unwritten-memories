# Unwritten 2.gameplay/ Reorganization Plan

## Executive Summary

**Goal:** Reorganize `docs/2.gameplay/` from overlapping unified docs into a clear, numbered structure matching `docs/1.concept/`.

**Status:** Ready to execute  
**Timeline:** Can be completed in phases  
**Breaking Changes:** None (all content preserved, just reorganized)

---

## Current State Analysis

### Existing Files

```
docs/2.gameplay/
├── unified-card-system.md          (1,874 lines) ⚠️ LARGE, overlapping
├── unified-narrative-structure.md  (1,254 lines) ⚠️ LARGE, overlapping
├── unified-content-expansion.md    (870 lines)   ⚠️ LARGE, overlapping
├── unified-gameplay-flow.md        (1,161 lines) ⚠️ LARGE, overlapping
├── Base Cards.md                   (25 lines)    ✓ Simple catalog
├── Categories.md                   (1,649 lines) ✓ Good flow diagram
├── Expansions.md                   (182 lines)   ✓ Pack taxonomy
├── fusion_trees_doc.md             (1,509 lines) ✓ Deep fusion detail
├── Packs.md                        (614 lines)   ✓ Pack specs
├── Gameplay Turns.md               (950 lines)   ✓ Concrete turn economy
└── narrative-arc-system.md         (1,391 lines) ✓ Decision templates
```

**Total:** ~11,479 lines of content

### Problems Identified

1. **Massive Overlap:** The 4 unified docs repeat concepts (card systems appear in 3 docs)
2. **No Clear Entry Point:** Which doc do you read first?
3. **Contradictions:** Different numbers/scales in different files
4. **Missing Index:** No map of the territory
5. **Concrete Details Buried:** Turn economy, decision templates hidden in standalone docs
6. **Hard to Maintain:** Changes must be replicated across multiple files

---

## Target State (Numbered Structure)

### New Organization

```
docs/2.gameplay/
├── 00-INDEX.md                     [CREATED] ✓ Navigation hub
│
├── 10-resource-economy.md          [NEW] Resource types, budgets, scarcity
├── 11-emotional-state-system.md    [NEW] 20 states, filters, transitions
├── 12-personality-integration.md   [NEW] Big 5 affects gameplay
├── 13-success-probability.md       [NEW] Success calculation formula
│
├── 20-card-taxonomy.md             [NEW] 7-tier system
├── 21-base-card-catalog.md         [NEW] 470+ card list
├── 22-card-evolution.md            [NEW] Evolution stages
├── 23-fusion-system.md             [NEW] Fusion mechanics & trees
├── 24-card-generation-ai.md        [NEW] AI personalization
│
├── 30-turn-structure.md            [NEW] Daily/weekly/seasonal turns
├── 31-gameplay-flow.md             [NEW] Pacing, batching, automation
├── 32-decision-weight-system.md    [NEW] 4-tier decisions
├── 33-hand-composition.md          [NEW] Card drawing algorithm
│
├── 40-narrative-arc-system.md      [NEW] Multi-phase arcs
├── 41-decisive-decisions.md        [NEW] Decision templates
├── 42-crisis-events.md             [NEW] Crisis triggers
├── 43-npc-behavior.md              [NEW] NPC agency
├── 44-memory-archive.md            [NEW] What gets remembered
│
├── 50-season-structure.md          [NEW] 12-week arc design
├── 51-lifetime-progression.md      [NEW] Multi-season continuity
├── 52-phase-transitions.md         [NEW] Life-changing events
├── 53-skill-development.md         [NEW] Skill trees
│
├── 60-pack-system-overview.md      [NEW] How packs work
├── 61-pack-catalog.md              [NEW] Complete pack specs
├── 62-pack-integration.md          [NEW] Technical integration
├── 63-content-roadmap.md           [NEW] Release schedule
│
├── 70-monetization-model.md        [NEW] V2 Essence token (canonical)
├── 71-free-tier-spec.md            [NEW] Free tier details
├── 72-subscription-tiers.md        [NEW] Plus/Ultimate benefits
├── 73-ethical-principles.md        [NEW] No dark patterns
│
└── _archive/                       [NEW FOLDER]
    ├── unified-card-system.md           [MOVED] Source for 20s
    ├── unified-narrative-structure.md   [MOVED] Source for 40s
    ├── unified-content-expansion.md     [MOVED] Source for 60s
    ├── unified-gameplay-flow.md         [MOVED] Source for 30s
    ├── Base Cards.md                    [MOVED] Merged into 21
    ├── Categories.md                    [MOVED] Diagram into 33
    ├── Expansions.md                    [MOVED] Into 61, 63
    ├── fusion_trees_doc.md              [MOVED] Into 23
    ├── Packs.md                         [MOVED] Into 61
    ├── Gameplay Turns.md                [MOVED] Into 10, 30
    └── narrative-arc-system.md          [MOVED] Into 40, 41
```

---

## Content Mapping (What Goes Where)

### CORE SYSTEMS (10s)

#### 10-resource-economy.md
**Sources:**
- `unified-gameplay-flow.md` lines 42-326 (Resource Management System)
- `Gameplay Turns.md` lines 1-450 (The 6 Resources section)

**Content:**
- Energy (daily regeneration, costs, modifiers)
- Time (168h/week, weekday/weekend split)
- Money (income, fixed expenses, activity costs)
- Social Capital (earning, spending, consequences)
- Comfort Zone (personality stretch, growth)
- Success Chance (formula, modifiers)

**Canonicalization Applied:**
- Keep EXHAUSTED state (not DRAINED)
- Energy regeneration: 3/3/2 per phase
- Weekend bonus: +1 per phase

---

#### 11-emotional-state-system.md
**Sources:**
- `unified-gameplay-flow.md` lines 551-731 (Emotional State-Driven Gameplay)
- `unified-card-system.md` lines 1587-1619 (Emotional State Integration)

**Content:**
- 20 canonical emotional states (with OVERWHELMED, EXHAUSTED)
- State detection algorithm
- Appeal multipliers per state
- Energy cost modifiers
- Hand composition filters
- State transition rules
- Temporary vs persistent vs chronic

**Canonicalization Applied:**
- Remove DRAINED → map to EXHAUSTED
- Explicitly include OVERWHELMED in the 20-state list
- State persistence patterns: 1-3, 3-10, 10+ turns

---

#### 12-personality-integration.md
**Sources:**
- `unified-card-system.md` lines 1644-1676 (Personality System Integration)
- `unified-narrative-structure.md` lines 359-411 (OCEAN Personality Model, Evolution)

**Content:**
- Big 5 (OCEAN) model
- Card appearance frequency weights
- Success rate modifiers by trait
- Routine formation rules (3 vs 5 reps based on Conscientiousness)
- Comfort zone calculation
- Personality evolution through play
- NPC compatibility matching

---

#### 13-success-probability.md
**Sources:**
- `unified-gameplay-flow.md` lines 272-325 (Success Chance)
- `Gameplay Turns.md` lines 420-520 (Success Probability System)

**Content:**
- Success formula with weights
- Personality fit (30%)
- Skill level (25%)
- Emotional state (20%)
- Preparation (15%)
- Random chance (10%)
- Player modification options
- Outcome distribution (success/partial/failure/critical)

---

### CARD SYSTEMS (20s)

#### 20-card-taxonomy.md
**Sources:**
- `unified-card-system.md` lines 11-1061 (Card Taxonomy, Tiers 1-7)
- `Categories.md` lines 1-200 (Category overview)

**Content:**
- 7-tier organizational system
- Tier 1: Foundation (Life Direction, Phase Transitions)
- Tier 2: Aspirations (Major, Minor)
- Tier 3: Structure (Routines, Obligations, Scheduled)
- Tier 4: Quest Chains (Milestones, Repeatable)
- Tier 5: Activities (Social, Solo, Exploration, Challenge)
- Tier 6: Events (NPC-initiated, Random, Crisis, Breakthrough)
- Tier 7: System (Skills, Items, Perks, Memory)
- When/how each tier appears
- Gameplay function of each tier

---

#### 21-base-card-catalog.md
**Sources:**
- `unified-card-system.md` lines 1544-1580 (Base Card Catalog, Quantitative Summary)
- `Base Cards.md` (full file)
- `Categories.md` lines 200-1400 (Detailed card lists)

**Content:**
- Complete enumeration of 470+ base cards
- By tier and category
- 9 Life Direction cards (listed)
- 82 Aspiration cards (40 Major, 42 Minor - listed)
- 30 Structure cards (listed)
- 150 Activity cards (listed by subcategory)
- 60 Event cards (listed)
- 80 System cards (listed)
- 50 Character NPCs (listed with personalities)
- 30 Locations (listed)
- Each card: tier, category, base costs, effects, personality fit

---

#### 22-card-evolution.md
**Sources:**
- `unified-card-system.md` lines 1194-1351 (Card Evolution Mechanics)
- `fusion_trees_doc.md` lines 1-300 (Evolution context)

**Content:**
- Evolution stages: Base → First → Deep → Legendary
- Evolution triggers: relationship, time, event, fusion
- AI generation parameters
- Context integration (personality, emotional state, history)
- Portrait and narrative generation
- Example progressions (Stranger → Sarah Anderson → Level 4 → Level 5)
- Evolution request JSON structure

**Canonicalization Applied:**
- Relationship levels: 0-5 (not 10/10)
- Trust meter: 0.0-1.0 (continuous)
- Level 5 = MAX, no Level 6 (Life Partnership is a status, not level)

---

#### 23-fusion-system.md
**Sources:**
- `unified-card-system.md` lines 1353-1541 (Fusion System)
- `fusion_trees_doc.md` (full file, 1,509 lines)

**Content:**
- Fusion principles
- Fusion categories: Simple (2 cards), Complex (3+), Chain (sequences), Legendary (4+)
- Fusion trees with level progressions
- Automatic vs contextual vs player-initiated
- Compatibility matrices
- Fusion rarity tiers: Common 70%, Uncommon 20%, Rare 8%, Legendary 2%
- Fusion mathematics (220k+ 2-card, 100k+ 3-card valid combinations)
- Integration with Archive system
- Detailed fusion tree examples

**Canonicalization Applied:**
- Update fusion_trees_doc examples: MAX (10/10) → Trust 1.0 (Level 5)
- Life Partnership as status flag, not Level 6

---

#### 24-card-generation-ai.md
**Sources:**
- `unified-card-system.md` lines 1304-1349 (AI Generation Parameters)
- Cross-reference `docs/3.ai/` for detailed prompts

**Content:**
- Prompt engineering for evolution
- Context injection: personality, emotional state, history, relationships
- Constraints: art style, NPC archetype, narrative role
- AI output structure: personality, appearance, narrative hook, dialogue sample
- Consistency enforcement across playthroughs
- Portrait generation parameters
- Dialogue generation rules
- Quality assurance filters

---

### TURN & FLOW (30s)

#### 30-turn-structure.md
**Sources:**
- `unified-gameplay-flow.md` lines 327-548 (Turn Structure)
- `Gameplay Turns.md` lines 1-450 (Complete turn economy)

**Content:**
- Daily structure: 3 turns (Morning 6am-12pm, Afternoon 12pm-6pm, Evening 6pm-12am)
- Energy regeneration: 3/3/2 per phase
- Weekend bonus: +1 energy per phase
- Weekly rhythm (21 turn opportunities)
- Weekday vs weekend patterns
- Week phases: Routine (Mon-Tue), Progression (Wed-Thu), Transition (Fri), Event (Sat-Sun)
- Seasonal structure: 12-week arcs
- Example turn walkthrough

---

#### 31-gameplay-flow.md
**Sources:**
- `unified-gameplay-flow.md` lines 851-1003 (Time Management & Pacing)
- `Gameplay Turns.md` lines 600-900 (Flow optimization)

**Content:**
- Adaptive flow system
- Routine-heavy flow (High Conscientiousness): batch processing, auto-resolve
- Freeform flow (High Openness): variety, choice-rich
- Time skip system
- Focus mode toggle ("Interesting Only")
- Smart automation rules
- Fast-forward to next meaningful moment
- Pacing aid systems

**Canonicalization Applied:**
- Replace "FOMO creates interesting decisions" with "Time and energy scarcity create meaningful trade-offs"
- Clarify: in-world deadlines OK, but time pauses for player decisions

---

#### 32-decision-weight-system.md
**Sources:**
- `unified-gameplay-flow.md` lines 986-1054 (Decision Weight System)
- `narrative-arc-system.md` lines 200-350 (Decision templates)

**Content:**
- 4-tier decision hierarchy
- Tier 1: Auto-resolve (trivial, 0-2 sec) - Default yes, one-click
- Tier 2: Quick choice (minor, 3-5 sec) - 2-3 options, small impact
- Tier 3: Considered choice (significant, 30-60 sec) - 3-5 options, medium-term consequences
- Tier 4: Life-defining (major, unlimited time) - Full context, no pressure, permanent impact
- UI patterns per tier
- Information disclosure rules
- Time pressure vs time pause

**Canonicalization Applied:**
- Tier 4: "Time Pauses. No rush." (explicit)
- Remove any "EXPIRES IN: X" real-time urgency
- Keep in-world deadlines but clarify time is paused

---

#### 33-hand-composition.md
**Sources:**
- `unified-gameplay-flow.md` lines 938-963 (Card Generation Priority System)
- `unified-card-system.md` lines 1587-1828 (Integration systems)
- `Categories.md` lines 1400-1649 (Complete Card Flow Diagram)

**Content:**
- Priority hierarchy: Decisive > Crisis > Arc > Base
- Emotional state filtering (appeal multipliers)
- Personality weighting (base preferences)
- Life Direction alignment (40-60% weight)
- Pack content integration (if owned)
- Hand size by phase: Morning 8, Afternoon 8, Evening 6
- Weighted random draw algorithm
- Complete card flow diagram

---

### NARRATIVE & STORY (40s)

#### 40-narrative-arc-system.md
**Sources:**
- `unified-narrative-structure.md` lines 57-181 (Story Arc Architecture)
- `narrative-arc-system.md` lines 1-600 (Multi-phase arc templates)

**Content:**
- Multi-phase arc template (5-7 phases typical)
- Photography Dream arc example (full phases)
- Arc integration with seasons
- Arc categories: Career/Financial, Personal Development, Relationship, Creative, Lifestyle
- Within-season arcs (2-4 concurrent)
- Across-season arcs (continuity)
- Failure conditions
- Success variations
- Arc properties: duration 8-16 weeks, success rate 30-70%, generates 10-30 sub-cards

---

#### 41-decisive-decisions.md
**Sources:**
- `unified-narrative-structure.md` lines 183-268 (Decisive Decision Points)
- `narrative-arc-system.md` lines 600-900 (Decision templates + preconditions)

**Content:**
- Structure of major decisions
- Foreshadowing (1-2 weeks before)
- The Decisive Card template
- Immediate consequences (Week 0-2)
- Long-term consequences (Weeks 4-16+)
- Memory entry creation
- Decision-NPC integration (reactions)
- Implementation template with preconditions
- Example: Wedding Shoot vs Overtime (full flow)

**Canonicalization Applied:**
- Time Pauses for Tier 4 decisions
- Full context provided (meters, money, relationships)

---

#### 42-crisis-events.md
**Sources:**
- `unified-narrative-structure.md` lines 270-352 (Crisis Events System)
- `narrative-arc-system.md` lines 900-1100 (Crisis templates)

**Content:**
- Crisis trigger mechanics (meter thresholds, neglect tracking)
- Crisis types: Health, Relationship, Financial, Parent Illness
- Escalation pattern: Week 4 (early warning), Week 8 (clear warning), Week 12 (crisis point)
- Health crisis example (burnout hospitalization)
- Relationship crisis (confrontation)
- Financial crisis (rent due)
- Parent illness crisis (worst timing)
- Crisis memory weight: 0.85-1.0
- Permanent effects vs recovery

---

#### 43-npc-behavior.md
**Sources:**
- `unified-narrative-structure.md` lines 479-518 (NPC Agency & Behavior)
- `unified-card-system.md` lines 796-853 (NPC-Initiated Cards)

**Content:**
- NPCs actively initiate contact
- Request types: Help, Invitation, Confrontation, Revelation, Crisis
- Personality-driven behavior patterns
- Contextual awareness (your stress, events, time since interaction)
- Bad days and boundaries
- "We need to talk" triggers
- AI integration: personality determines request type
- Example: Sarah needs help moving (relationship test)

---

#### 44-memory-archive.md
**Sources:**
- `unified-narrative-structure.md` lines 520-646 (Archive & Persistence System)
- `unified-card-system.md` lines 1677-1742 (Archive Integration)

**Content:**
- What creates Archive memories (automatic, significant, landmark)
- Season archive structure
- Lifetime archive organization
- What carries forward between seasons (personality, skills, NPCs, money, career, location)
- What doesn't carry (character echoes only)
- Book generation tiers (free 3-5k, premium 12-15k)
- Multi-season collections
- Full lifetime novel (80-150k words)
- Archive JSON structure example

**Canonicalization Applied:**
- Free: unlimited season archives, 3 lifetime archives
- Plus/Ultimate: unlimited lifetime archives

---

### PROGRESSION & SEASONS (50s)

#### 50-season-structure.md
**Sources:**
- `unified-narrative-structure.md` lines 13-54 (Season Model)
- `unified-gameplay-flow.md` lines 455-548 (Seasonal Structure)

**Content:**
- 12-week season as default (not 12-100; extended seasons are optional mode)
- 3-act structure: Act I Setup (Weeks 1-4, 33%), Act II Conflict (Weeks 5-9, 50%), Act III Resolution (Weeks 10-12, 17%)
- Week-by-week pacing guide
- Season initiation (choose Major Aspiration)
- Progression phase (quest chains)
- Decision point / crisis (Week 8-9 typical)
- Season climax (Week 12)
- Success/partial/failure outcomes
- Archive generation trigger
- Book generation offer
- Choice: Start new season or end lifetime

**Canonicalization Applied:**
- Default 12 weeks (remove "12-100" phrasing)
- Optional extended seasons (24, 36 weeks) as separate mode

---

#### 51-lifetime-progression.md
**Sources:**
- `unified-narrative-structure.md` lines 37-54 (Lifetime Structure)
- `unified-gameplay-flow.md` lines 735-772 (Life Phases)

**Content:**
- Lifetime = 20-40 seasons potential (3000+ weeks, years of character life)
- Phase structure: Exploration (Age 28-32), Establishment (33-38), Mastery (39-44), Wisdom (45+)
- What carries forward between seasons
- Character aging and development
- Lifetime book generation (80-150k words, trilogy structure)
- When/how players choose to end a character's story
- No forced endings
- Example: Alex Chen's lifetime (Age 28 → 47, 8 seasons)

---

#### 52-phase-transitions.md
**Sources:**
- `unified-card-system.md` lines 109-157 (Phase Transition Cards)
- `unified-narrative-structure.md` lines 270-352 (Crisis overlap)

**Content:**
- 8 Phase Transition cards: Major Breakup, Career Devastation, Health Crisis, Loss of Loved One, Financial Catastrophe, Achievement Peak, Existential Crisis, Unexpected Opportunity
- Trigger conditions and timing (automatically at major life junctures)
- Frequency: 2-4 times per playthrough
- Mandatory choice structure
- Life Direction may shift
- Active Aspirations may cancel
- New Aspirations unlock
- Deck resets for new phase
- Example: Major Breakup (full flow)

---

#### 53-skill-development.md
**Sources:**
- `unified-card-system.md` lines 1012-1060 (Skill Cards)
- Cross-reference for skill trees

**Content:**
- 30+ skill trees
- Categories: Physical (fitness, sports, dance), Creative (instruments, art, writing), Intellectual (languages, programming), Social (public speaking, negotiation), Practical (cooking, repair, finance)
- 10-level progression per skill
- Unlock conditions: 5+ repetitions of related activity
- Success rate bonuses: +5% per level
- Fusion interactions (Cooking 5 + Dinner Party → Culinary Experience)
- Cross-season persistence
- Example: Cooking Skill Level 4 (full progression)

---

### EXPANSION & CONTENT (60s)

#### 60-pack-system-overview.md
**Sources:**
- `unified-content-expansion.md` lines 13-80 (Expansion Philosophy + Pack System Overview)
- `Packs.md` lines 1-150 (How packs work)

**Content:**
- Modular enhancement philosophy (not fragmentation)
- What packs contain: 20-80 cards (depending on tier), NPCs, Locations, Skills, Story Arcs, Achievements
- Life Direction filtering (compatibility matrix)
- Emotional state integration
- Fusion compatibility across base+packs
- Try-before-buy preview system (3 cards, 1 NPC, 1 location)
- Permanent ownership model (DLC, not subscription)
- Integration examples (Gallery District with Sarah's Bookshop)

**Canonicalization Applied:**
- Pack sizes: Standard 20-30, Deluxe 35-50, Mega 60-80
- Remove "15-25" old phrasing

---

#### 61-pack-catalog.md
**Sources:**
- `unified-content-expansion.md` lines 148-458 (Pack Categories, full specs)
- `Packs.md` (full file, 614 lines)
- `Expansions.md` (182 lines, broader taxonomy)

**Content:**
- **World & Destination Packs:**
  - City Explorer (60 cards, Mega $9.99): Sofia Chen, Isabella Rodriguez, Aisha Kumar
  - Nature Adventure (55 cards, Deluxe $7.99): Elena Vasquez, Tom Blackwood, Maya Summers
  - Historical Discovery (50 cards, Deluxe $7.99): Dr. Rachel Morrison, Samuel Chen, Abigail Stone
  - Luxury Travel (55 cards, Deluxe $7.99): Victoria Ashford, Alessandro Romano, Priya Mehta

- **Activity & Hobby Packs:**
  - Creative Arts (60 cards, Mega $9.99): Luna Martinez, David Kim, Beatrice Johnson
  - Philosophy & Ethics (52 cards, Deluxe $7.99): Philosophy professors, debate club
  - Psychology & Self-Discovery (58 cards, Deluxe $7.99): Therapists, support groups
  - Resilience & Recovery (62 cards, Deluxe $7.99): Crisis counselors, recovery sponsors

- **Future Expansion Families (from Expansions.md):**
  - Career & Ambition, Relationship & Social, Mind & Growth, Lifestyle & Environment, Culture & Language, Meta & Fantasy, Utility, Art & Aesthetic

Each pack: Full card breakdown, NPCs with personalities, story arcs, special mechanics, achievements.

**Canonicalization Applied:**
- Pack pricing: Standard $4.99 (20-30), Deluxe $7.99 (35-50), Mega $9.99 (60-80)
- Art Style packs: $2.99 (aesthetic only)

---

#### 62-pack-integration.md
**Sources:**
- `unified-content-expansion.md` lines 460-509 (Integration with Core Systems)
- `Packs.md` lines 400-600 (Technical integration)

**Content:**
- Deck composition algorithm: 70% base, 30% packs (if owned)
- Life Direction compatibility matrix (0.3-0.9 multipliers)
- Emotional state appeal (same rules as base cards)
- NPC evolution across packs (Sarah + Creative Arts → Gallery Bookshop fusion)
- Archive handling of pack content
- Book generation with pack characters (seamless, noted which packs used)
- Pack discovery in-game (non-intrusive, contextual)

---

#### 63-content-roadmap.md
**Sources:**
- `unified-content-expansion.md` lines 716-751 (Release Schedule)
- `Expansions.md` (broader taxonomy for future)

**Content:**
- Year 1 launch plan: Base game + 2 packs (Creative Arts, Nature Adventure)
- Month 3: City Explorer + Philosophy & Ethics
- Month 6: Historical Discovery + Psychology
- Month 9: Luxury Travel + Resilience
- Month 12: Education & Learning + Social Justice
- Year 2+: New pack every 2 months, quarterly free updates, seasonal events
- Long-term expansion families (from Expansions.md)
- Community-requested features pipeline

---

### ECONOMY & MONETIZATION (70s)

#### 70-monetization-model.md
**Sources:**
- `docs/1.concept/17-monetization-model.md` (V2 Essence token model)
- `unified-content-expansion.md` lines 602-713 (older model, to be updated)

**CANONICAL V2 MODEL** (this supersedes older $4.99 Premium / $2.99 packs):

**Content:**
- **Free Tier:** 25 Essence/day, unlimited season archives, 3 lifetime archives, 470+ base cards, full gameplay
- **Plus ($14.99/mo):** 100 Essence/day, unlimited lifetime archives, early access (1 month), enhanced memory cinema
- **Ultimate ($29.99/mo):** Unlimited Essence, all future packs included, exclusive NPCs, priority AI processing
- **Packs (DLC, permanent):** Standard $4.99, Deluxe $7.99, Mega $9.99
- **Art Style Packs:** $2.99 (aesthetic only, no gameplay)
- Essence costs per action
- Conversion rates (Essence to premium features)
- Ethical boundaries (no gacha, no timers, no FOMO)

---

#### 71-free-tier-spec.md
**Sources:**
- `unified-content-expansion.md` lines 607-629 (Free Tier)
- Update with V2 details

**Content:**
- 470+ base cards (100% of core content)
- Full card evolution system (AI-generated personalization)
- All fusion types (including legendary)
- Complete emotional state system (all 20 states)
- Unlimited gameplay (no time/turn limits, no energy caps)
- Unlimited season archives
- 3 lifetime archives (delete old to save new)
- Basic book generation (3-5k word novellas per season)
- 25 Essence per day (regenerates)
- No ads, no FOMO, no pressure
- Complete, satisfying experience (100+ hours)

**Canonicalization Applied:**
- Unlimited season archives (not 3)
- 3 lifetime archives (not unlimited)

---

#### 72-subscription-tiers.md
**Sources:**
- V2 monetization model
- `unified-content-expansion.md` lines 632-658 (Premium Tier, to be updated)

**Content:**
- Feature comparison matrix (Free vs Plus vs Ultimate)
- Plus ($14.99/mo) benefits: 100 Essence/day, unlimited lifetime archives, early access, enhanced memory cinema, premium book generation (12-15k words)
- Ultimate ($29.99/mo) benefits: Unlimited Essence, all future packs included, exclusive NPCs (2-4 per season), priority AI processing (instant vs 750ms), developer support
- Value proposition per tier
- Value per hour calculations ($14.99/50 hours = $0.30/hour)
- Subscription vs DLC purchase guidance

---

#### 73-ethical-principles.md
**Sources:**
- `unified-content-expansion.md` lines 705-713 (Ethical Considerations)
- Policy documents

**Content:**
- No energy/turn timers (unlimited play)
- No gacha/loot boxes (all packs are DLC, permanent, no RNG)
- No pay-to-win mechanics
- No dark patterns or manipulation
- No required packs for complete experience
- No real-time FOMO (in-world urgency OK, but time pauses for player decisions)
- Transparent pricing (no hidden costs)
- Try-before-buy (preview system for all packs)
- Respect player time and money
- Complete base experience for free (not demo/teaser)
- Long-term player satisfaction over short-term extraction

**Canonicalization Applied:**
- "No FOMO" clarified: in-world deadlines fine (Sarah's party Saturday), but time pauses when deciding
- Remove any "EXPIRES IN: 2 hours (decide now!)" real-time pressure framing

---

## Migration Workflow

### Phase 1: Setup (30 min)

1. **Create Index**
   - ✅ DONE: `00-INDEX.md` created

2. **Create Archive Folder**
   ```bash
   mkdir docs/2.gameplay/_archive
   ```

3. **Create Placeholder Files**
   ```bash
   # Create all numbered files as placeholders
   touch docs/2.gameplay/{10..13}-*.md
   touch docs/2.gameplay/{20..24}-*.md
   touch docs/2.gameplay/{30..33}-*.md
   touch docs/2.gameplay/{40..44}-*.md
   touch docs/2.gameplay/{50..53}-*.md
   touch docs/2.gameplay/{60..63}-*.md
   touch docs/2.gameplay/{70..73}-*.md
   ```

### Phase 2: Core Systems (2-3 hours)

**Order:** 10 → 11 → 12 → 13

For each file:
1. Copy relevant sections from source docs
2. Apply canonicalization edits (see below)
3. Remove redundancy
4. Add cross-references
5. Test readability

**10-resource-economy.md:**
- Extract from `unified-gameplay-flow.md` lines 42-326
- Extract from `Gameplay Turns.md` lines 1-450
- Normalize: EXHAUSTED (not DRAINED)
- Add energy regeneration table: 3/3/2 per phase

**11-emotional-state-system.md:**
- Extract from `unified-gameplay-flow.md` lines 551-731
- Extract from `unified-card-system.md` lines 1587-1619
- Normalize: 20 states list with OVERWHELMED and EXHAUSTED
- Remove DRAINED
- Add state persistence patterns

**12-personality-integration.md:**
- Extract from `unified-card-system.md` lines 1644-1676
- Extract from `unified-narrative-structure.md` lines 359-411
- Routine formation: 3 reps (High C) vs 5 reps (Low C)

**13-success-probability.md:**
- Extract from `unified-gameplay-flow.md` lines 272-325
- Extract from `Gameplay Turns.md` lines 420-520
- Success formula with percentages

### Phase 3: Card Systems (3-4 hours)

**Order:** 20 → 21 → 22 → 23 → 24

**20-card-taxonomy.md:**
- Extract from `unified-card-system.md` lines 11-1061
- Extract from `Categories.md` lines 1-200
- 7-tier system with examples

**21-base-card-catalog.md:**
- Extract from `unified-card-system.md` lines 1544-1580
- Extract from `Base Cards.md` (full)
- Extract from `Categories.md` lines 200-1400
- Complete 470+ card enumeration

**22-card-evolution.md:**
- Extract from `unified-card-system.md` lines 1194-1351
- Extract from `fusion_trees_doc.md` lines 1-300
- **CRITICAL:** Apply canonicalization
  - Find: `MAX (10/10)` → Replace: `Trust 1.0 (Level 5 reached)`
  - Find: `Lv.6`, `Level 6` → Replace: `Status: Life Partnership` (not a level)
  - Normalize all examples to Levels 0-5

**23-fusion-system.md:**
- Extract from `unified-card-system.md` lines 1353-1541
- Extract from `fusion_trees_doc.md` (full file)
- **CRITICAL:** Apply canonicalization
  - Update all fusion examples: `MAX (10/10)` → `Level 5 (Trust 1.0)`
  - Life Partnership = status flag, not Level 6

**24-card-generation-ai.md:**
- Extract from `unified-card-system.md` lines 1304-1349
- Cross-reference `docs/3.ai/` for prompts

### Phase 4: Turn & Flow (2-3 hours)

**Order:** 30 → 31 → 32 → 33

**30-turn-structure.md:**
- Extract from `unified-gameplay-flow.md` lines 327-548
- Extract from `Gameplay Turns.md` lines 1-450
- 3-turn daily structure, 12-week seasons

**31-gameplay-flow.md:**
- Extract from `unified-gameplay-flow.md` lines 851-1003
- Extract from `Gameplay Turns.md` lines 600-900
- **CRITICAL:** Apply canonicalization
  - Replace: "FOMO creates interesting decisions" → "Time and energy scarcity create meaningful trade-offs"
  - Clarify: in-world deadlines OK, time pauses for decisions

**32-decision-weight-system.md:**
- Extract from `unified-gameplay-flow.md` lines 986-1054
- Extract from `narrative-arc-system.md` lines 200-350
- **CRITICAL:** Tier 4 decisions: "Time Pauses. No rush."
  - Any "EXPIRES IN: X (decide now!)" → add "In-world deadline; time is paused while you decide"

**33-hand-composition.md:**
- Extract from `unified-gameplay-flow.md` lines 938-963
- Extract from `unified-card-system.md` lines 1587-1828
- Extract from `Categories.md` lines 1400-1649 (Complete Card Flow Diagram)
- Priority hierarchy, filtering algorithm

### Phase 5: Narrative & Story (3-4 hours)

**Order:** 40 → 41 → 42 → 43 → 44

**40-narrative-arc-system.md:**
- Extract from `unified-narrative-structure.md` lines 57-181
- Extract from `narrative-arc-system.md` lines 1-600
- Multi-phase arc template, Photography Dream example

**41-decisive-decisions.md:**
- Extract from `unified-narrative-structure.md` lines 183-268
- Extract from `narrative-arc-system.md` lines 600-900
- Decision template with preconditions, foreshadowing, consequences
- **CRITICAL:** Time Pauses for major decisions

**42-crisis-events.md:**
- Extract from `unified-narrative-structure.md` lines 270-352
- Extract from `narrative-arc-system.md` lines 900-1100
- Crisis triggers, escalation patterns, examples

**43-npc-behavior.md:**
- Extract from `unified-narrative-structure.md` lines 479-518
- Extract from `unified-card-system.md` lines 796-853
- NPC agency, personality-driven requests

**44-memory-archive.md:**
- Extract from `unified-narrative-structure.md` lines 520-646
- Extract from `unified-card-system.md` lines 1677-1742
- **CRITICAL:** Apply canonicalization
  - Free: unlimited season archives, 3 lifetime archives
  - Plus/Ultimate: unlimited lifetime archives

### Phase 6: Progression & Seasons (2-3 hours)

**Order:** 50 → 51 → 52 → 53

**50-season-structure.md:**
- Extract from `unified-narrative-structure.md` lines 13-54
- Extract from `unified-gameplay-flow.md` lines 455-548
- **CRITICAL:** 12-week default (remove "12-100" phrasing)
- Optional extended seasons as separate mode

**51-lifetime-progression.md:**
- Extract from `unified-narrative-structure.md` lines 37-54
- Extract from `unified-gameplay-flow.md` lines 735-772
- Lifetime = 20-40 seasons, phase structure

**52-phase-transitions.md:**
- Extract from `unified-card-system.md` lines 109-157
- Extract from `unified-narrative-structure.md` lines 270-352
- 8 Phase Transition cards

**53-skill-development.md:**
- Extract from `unified-card-system.md` lines 1012-1060
- 30+ skill trees, 10-level progression

### Phase 7: Expansion & Content (2-3 hours)

**Order:** 60 → 61 → 62 → 63

**60-pack-system-overview.md:**
- Extract from `unified-content-expansion.md` lines 13-80
- Extract from `Packs.md` lines 1-150
- **CRITICAL:** Pack sizes: Standard 20-30, Deluxe 35-50, Mega 60-80

**61-pack-catalog.md:**
- Extract from `unified-content-expansion.md` lines 148-458
- Extract from `Packs.md` (full file)
- Extract from `Expansions.md` (182 lines)
- **CRITICAL:** Update pack counts, pricing
  - Gallery District 60 cards → classify as Mega $9.99
  - Apply pricing: Standard $4.99, Deluxe $7.99, Mega $9.99

**62-pack-integration.md:**
- Extract from `unified-content-expansion.md` lines 460-509
- Extract from `Packs.md` lines 400-600
- Technical integration, compatibility matrices

**63-content-roadmap.md:**
- Extract from `unified-content-expansion.md` lines 716-751
- Extract from `Expansions.md` (broader taxonomy)
- Year 1-2+ release schedule

### Phase 8: Economy & Monetization (2-3 hours)

**Order:** 70 → 71 → 72 → 73

**70-monetization-model.md:**
- Extract from `docs/1.concept/17-monetization-model.md` (V2 canonical)
- **CRITICAL:** This is V2 Essence token model
- Retire old $4.99 Premium / $2.99 packs
- Free: 25 Essence/day
- Plus: $14.99/mo
- Ultimate: $29.99/mo
- Packs: $4.99/$7.99/$9.99 (DLC, permanent)

**71-free-tier-spec.md:**
- Extract from `unified-content-expansion.md` lines 607-629
- **CRITICAL:** Unlimited season archives, 3 lifetime archives

**72-subscription-tiers.md:**
- V2 model details
- Plus vs Ultimate comparison

**73-ethical-principles.md:**
- Extract from `unified-content-expansion.md` lines 705-713
- **CRITICAL:** "No FOMO" clarified
  - In-world urgency OK (Sarah's party Saturday)
  - Time pauses for player decisions
  - Remove real-time pressure framing

### Phase 9: Archive Old Files (30 min)

```bash
# Move old files to archive
mv docs/2.gameplay/unified-*.md docs/2.gameplay/_archive/
mv docs/2.gameplay/Base\ Cards.md docs/2.gameplay/_archive/
mv docs/2.gameplay/Categories.md docs/2.gameplay/_archive/
mv docs/2.gameplay/Expansions.md docs/2.gameplay/_archive/
mv docs/2.gameplay/fusion_trees_doc.md docs/2.gameplay/_archive/
mv docs/2.gameplay/Packs.md docs/2.gameplay/_archive/
mv docs/2.gameplay/Gameplay\ Turns.md docs/2.gameplay/_archive/
mv docs/2.gameplay/narrative-arc-system.md docs/2.gameplay/_archive/
```

**Add README to archive:**
```markdown
# Archive Folder

These files have been reorganized into the numbered structure (10-73).

Content has been:
- Split into logical sections
- De-duplicated
- Canonicalized (contradictions resolved)
- Cross-referenced

**Do not edit these files.** They are preserved for reference only.

See `../00-INDEX.md` for the new structure.
```

### Phase 10: Update Cross-References (1-2 hours)

**In 1.concept/ files:**
- Update any links to `2.gameplay/unified-*` → point to new numbered files
- Example: `See unified-card-system.md` → `See 20-card-taxonomy.md and 21-base-card-catalog.md`

**In 2.gameplay/ files:**
- Add cross-references between numbered files
- Example: `11-emotional-state-system.md` references `33-hand-composition.md` (how states filter cards)

**In other folders (3.ai/, 4.visual/, etc.):**
- Update any references to old gameplay docs

### Phase 11: Validation (1 hour)

**Check:**
1. All numbered files created (10-13, 20-24, 30-33, 40-44, 50-53, 60-63, 70-73)
2. 00-INDEX.md accurate (all files listed, descriptions match)
3. Canonicalization applied (no contradictions):
   - Relationship scale: 5 levels + Trust 0.0-1.0 ✓
   - Archives: Free = unlimited season + 3 lifetime ✓
   - Seasons: Default 12 weeks ✓
   - Monetization: V2 model (Essence) ✓
   - Pack sizes: Standard/Deluxe/Mega ✓
   - States: EXHAUSTED, OVERWHELMED (no DRAINED) ✓
   - FOMO: In-world OK, time pauses ✓
4. No broken links
5. Reading paths work (try following "For Developers" path)
6. Old files in `_archive/` with README

---

## Canonicalization Edit Checklist

### Search & Replace (Automated)

Run these across all new numbered files:

```bash
# Relationship scale
find docs/2.gameplay/*.md -type f -exec sed -i 's/MAX (10\/10)/Trust 1.0 (Level 5 reached)/g' {} +
find docs/2.gameplay/*.md -type f -exec sed -i 's/Level 6/Status: Life Partnership (not a level)/g' {} +
find docs/2.gameplay/*.md -type f -exec sed -i 's/Lv\.6/Status: Life Partnership/g' {} +

# Emotional states
find docs/2.gameplay/*.md -type f -exec sed -i 's/DRAINED/EXHAUSTED/g' {} +

# Pack sizes
find docs/2.gameplay/*.md -type f -exec sed -i 's/15-25 cards/20-30 cards (Standard)/g' {} +
find docs/2.gameplay/*.md -type f -exec sed -i 's/15–25 cards/20–30 cards (Standard)/g' {} +

# FOMO tone
find docs/2.gameplay/*.md -type f -exec sed -i 's/FOMO creates interesting decisions/Time and energy scarcity create meaningful trade-offs/g' {} +
```

### Manual Edits (Context-Dependent)

**In 22-card-evolution.md and 23-fusion-system.md:**
- Find all relationship examples
- Update to Levels 0-5 (not 10/10)
- Show Trust as meter: "Trust 0.8 (Level 4)"
- Remove any "Level 6" or "MAX 10" references

**In 31-gameplay-flow.md:**
- Find any "EXPIRES IN: 2 hours (decide now!)" urgency
- Add clarification: "In-world deadline; time is paused while you decide"

**In 44-memory-archive.md:**
- Update archive policy: "Free: unlimited season archives, 3 lifetime archives"
- Remove any "3 season archives" or "unlimited archives for Free"

**In 50-season-structure.md:**
- Default: 12 weeks
- Remove "12-100 weeks" phrasing
- Add: "Optional extended seasons (24, 36 weeks) available as separate mode"

**In 60-pack-system-overview.md and 61-pack-catalog.md:**
- Update pack sizes: Standard 20-30, Deluxe 35-50, Mega 60-80
- Update pricing: $4.99/$7.99/$9.99
- Classify any 60-card packs as "Mega"

**In 70-monetization-model.md:**
- Confirm V2 Essence model as canonical
- Retire any mention of old "$4.99 Premium" or "$2.99 packs"
- Update to: Free (25 Essence/day), Plus ($14.99/mo), Ultimate ($29.99/mo)

**In 73-ethical-principles.md:**
- Clarify FOMO policy: "No real-time FOMO. In-world urgency (deadlines) OK, but time pauses when player is deciding."

---

## Testing the New Structure

### Reading Path Test

**Follow "For Developers" path from 00-INDEX.md:**
1. Read 10-resource-economy.md + 11-emotional-state-system.md
2. Read 20-card-taxonomy.md → 21-base-card-catalog.md → 22-card-evolution.md
3. Read 30-turn-structure.md → 31-gameplay-flow.md → 33-hand-composition.md
4. Read 40-narrative-arc-system.md → 50-season-structure.md
5. Read 60-pack-system-overview.md → 61-pack-catalog.md

**Questions to answer:**
- Can you build the game from this path?
- Are resource budgets clear?
- Is card taxonomy understandable?
- Is turn structure implementable?
- Are pack specs complete?

### Cross-Reference Test

**Pick a topic and follow it across files:**

Example: "Emotional States"
- Defined in: 11-emotional-state-system.md
- Used in: 31-gameplay-flow.md (pacing)
- Affects: 33-hand-composition.md (filtering)
- Referenced in: 40-narrative-arc-system.md (crisis states)

**Questions:**
- Are cross-references present?
- Do they point to correct files?
- Is the narrative coherent across files?

### Contradiction Test

**Check for contradictions:**
- Relationship scale: Should be consistent (0-5 levels + Trust 0.0-1.0)
- Archives: Free should have unlimited season, 3 lifetime
- Pack sizes: Should be Standard/Deluxe/Mega (not 15-25)
- Monetization: Should reference V2 Essence model

**Scan for old terms:**
```bash
# Check for old relationship scale
grep -r "10/10\|Lv\.6\|Level 6" docs/2.gameplay/*.md

# Check for DRAINED state
grep -r "DRAINED" docs/2.gameplay/*.md

# Check for old pricing
grep -r "\$2\.99.*pack\|\$4\.99.*Premium" docs/2.gameplay/*.md

# Check for old archive policy
grep -r "3 season archives\|unlimited.*free" docs/2.gameplay/*.md
```

---

## Benefits of New Structure

### For Developers
- ✅ Clear implementation order (10s → 20s → 30s → 40s)
- ✅ Single source of truth per topic
- ✅ Smaller, focused files (easier to read)
- ✅ Quick reference via numbered index

### For Designers
- ✅ Card catalog in one place (21)
- ✅ Fusion mechanics isolated (23)
- ✅ Pack specs organized (61)
- ✅ Narrative arc templates (40, 41)

### For Product/Business
- ✅ Monetization model canonical (70)
- ✅ Free tier clearly defined (71)
- ✅ Ethical principles documented (73)
- ✅ Content roadmap (63)

### For Writers/Content Creators
- ✅ NPC behavior guidelines (43)
- ✅ Memory/archive system (44)
- ✅ Decision templates (41)
- ✅ Crisis events (42)

### For Maintenance
- ✅ Logical organization (easier to find things)
- ✅ Reduced duplication (single edit, not 4)
- ✅ Version control friendly (smaller diffs)
- ✅ Clear ownership (one file per topic)

---

## Timeline Estimate

**Total Time:** 18-24 hours

- Phase 1: Setup (0.5h)
- Phase 2: Core Systems (2-3h)
- Phase 3: Card Systems (3-4h)
- Phase 4: Turn & Flow (2-3h)
- Phase 5: Narrative & Story (3-4h)
- Phase 6: Progression & Seasons (2-3h)
- Phase 7: Expansion & Content (2-3h)
- Phase 8: Economy & Monetization (2-3h)
- Phase 9: Archive Old Files (0.5h)
- Phase 10: Update Cross-References (1-2h)
- Phase 11: Validation (1h)

**Can be parallelized:** Multiple people can work on different number ranges simultaneously (e.g., one person does 10s, another does 20s).

---

## Success Criteria

### Complete When:
- ✅ All 28 numbered files created (10-13, 20-24, 30-33, 40-44, 50-53, 60-63, 70-73)
- ✅ 00-INDEX.md accurate and complete
- ✅ Old files moved to `_archive/` with README
- ✅ Canonicalization applied (no contradictions)
- ✅ Cross-references updated
- ✅ Reading paths tested
- ✅ All search & replace automated edits completed
- ✅ Manual context-dependent edits completed
- ✅ Validation tests pass

### Quality Checks:
- ✅ No broken links
- ✅ Consistent terminology
- ✅ No duplication across files
- ✅ Each file 200-800 lines (manageable size)
- ✅ Clear section headers
- ✅ Examples present where needed
- ✅ Cross-references to related topics

---

## Next Steps

1. **Review & Approve Plan** - Team reviews this reorganization plan
2. **Assign Ownership** - Designate who will work on which phases
3. **Create Branch** - `feature/reorganize-gameplay-docs`
4. **Execute Phases** - Follow workflow above
5. **Review & Iterate** - Team reviews each phase as completed
6. **Merge to Main** - Once validation passes
7. **Update 1.concept/** - Fix any broken links
8. **Announce** - Inform team of new structure

**Start with:** Phase 1 (Setup) → Phase 2 (Core Systems, 10-13) as a proof of concept. Review that before proceeding.

---

**Document Status:** Ready for execution  
**Last Updated:** 2025-10-13  
**Owner:** Development team  
**Approvals Needed:** Lead Developer, Lead Designer, Product Manager

