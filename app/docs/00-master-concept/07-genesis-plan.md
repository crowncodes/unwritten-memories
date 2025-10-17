# The Genesis Plan: Building the Foundational Architecture

**Document Status**: V3 Canonical Reference  
**Last Updated**: October 16, 2025  
**Authority Level**: Master Truth

---

## ⚠️ Critical: The Anti-Gamification Mandate

**Before designing any template, read and internalize:**
> **IF YOU CAN WRITE A WALKTHROUGH THAT SAYS "DO X 16 TIMES TO UNLOCK Y," YOU'VE FAILED.**

All progression must be assessed by `ENGINE_WRITERS_ROOM` based on **qualitative criteria** (personality compatibility, emotional states, interaction quality, narrative context)—NOT arbitrary numerical thresholds.

**See:** Core design philosophy documentation for full mandate.

---

## 1. Guiding Philosophy: The V3 Architecture

### Three-Layer Architecture

**Our goal is to build the foundational architecture of Unwritten:**

```
Layer 1: CORE SIMULATION ENGINES
  └─ ENGINE_PERSONALITY, ENGINE_CAPACITY, ENGINE_MEMORY, ENGINE_WRITERS_ROOM
     ↓
Layer 2: GAMEPLAY DNA (7 Strands)
  └─ Fundamental concepts of human experience
     ↓
Layer 3: MASTER TEMPLATES (~300)
  └─ Archetypal implementations that instantiate into infinite variations
```

### The Master Template Approach

**We are NOT creating ~300 static, predefined cards.**

**We ARE designing ~300 Master Templates**—structured schematics defining:
- **Qualitative rules** (how this concept behaves, assessed by AI)
- **Potential pathways** (how it can evolve contextually)
- **Narrative tags** (how `ENGINE_WRITERS_ROOM` uses it)
- **Context variables** (what makes each instance unique)

**At the start of each life:**
- `ENGINE_WRITERS_ROOM` analyzes player context (age, personality, goals, location)
- Templates instantiate into **unique, playable cards**
- Same template → different card every playthrough

### Value Proposition

| Approach | Formula | Result |
|----------|---------|--------|
| **Traditional (Static)** | 300 cards + 50 expansion = 350 total | Linear, predictable |
| **Template (Generative)** | 300 templates × infinite contexts | Exponential, emergent |

**Expansion multiplies value:**
- New fusion opportunities (combinatorial)
- New evolution branches (contextual)
- New narrative threads (emergent)
- **Multiplicative, not additive**

---

## 2. The Phased Approach: Foundation Before Content

### Why Build in Phases?

**Critical Principle:** Must build the **simulation engines** before **gameplay DNA** before **content templates**.

**Logical dependencies:**
- Can't design evolution rules without `ENGINE_WRITERS_ROOM` assessment framework
- Can't design Activities without knowing Life Directions (DNA Strand 4)
- Can't design Events without `ENGINE_CAPACITY` mechanics
- Can't design NPCs without Relationship progression systems (DNA Strand 5)

**The Build Order:**

```
PHASE 0: CORE SIMULATION ENGINES (The Foundation)
  └─ Build: ENGINE_PERSONALITY, ENGINE_CAPACITY, ENGINE_MEMORY, ENGINE_WRITERS_ROOM
     ↓
PHASE 1: GAMEPLAY DNA (The Concepts)
  └─ Define: 7 Strands of fundamental human experience
     ↓
PHASE 2-6: MASTER TEMPLATES (The Archetypes)
  └─ Design: ~300 templates that instantiate the DNA
     ↓
CHARACTER CREATION (The Spark)
  ↓
PHASE 2: Life Directions (The "Why")
  ↓
PHASE 3: Aspirations & Activities (The "What" & "How")
  ↓
PHASE 4: Living World (The "Who" & "Where")
  ↓
PHASE 5: Systems & Progression (The "Rules of Growth")
  ↓
PHASE 6: Narrative Catalysts (The "Unexpected")
```

### Phase 0: Core Simulation Engines (Critical First Step)

**Objective:** Implement the foundational systems that drive all simulation logic.

**Must Build:**

| Engine | Purpose | Critical Components |
|--------|---------|---------------------|
| `ENGINE_PERSONALITY` | OCEAN-based behavior | Trait modifiers, Tension Perception Profile (Neuroticism filter) |
| `ENGINE_CAPACITY` | Emotional resilience | Slow-moving Capacity, Capacity Zones, Capacity-Limited Perception |
| `ENGINE_RESOURCES` | Time/Energy economy | Fluid Time, Energy Debt/Collapse mechanics |
| `ENGINE_MEMORY` | Event recording | Metadata tagging, Archive Query System, **Memory Facets generation** |
| `ENGINE_WRITERS_ROOM` | AI narrative director | Specialists framework, Director (Synthesizer), Analyst, **Narrative Priming, Facet generation, Weekly analysis** |

**Why This Can't Wait:**
- Templates reference these engines in their assessment criteria
- Evolution rules require `ENGINE_WRITERS_ROOM` qualitative evaluation
- All mechanics interact with `ENGINE_CAPACITY` and `ENGINE_PERSONALITY`
- Without engines, templates are just static data

---

## 3. Phase 1: Gameplay DNA (Define Before Building)

**Objective:** Define the 7 Strands of fundamental human experience before creating templates.

**The Seven Strands:**
1. **Psyche** - Emotional states, moods, mental health
2. **Volitional Action** - Activities, choices, routines
3. **Catalytic Events** - Situations that disrupt or accelerate
4. **Narrative Structure** - Life Directions, Aspirations, meaning-making
5. **Social Connection** - Characters, relationships, bonds
6. **Spatial Awareness** - Locations, geography, belonging
7. **Progression & Artifacts** - Skills, items, perks, growth

**Process:** For each strand, define core concept, mechanical function, and interaction with Core Engines.

**Cross-Reference:** See DNA Strand documentation in `docs/2.gameplay/` for detailed specifications.

---

## 4. Phase 2: Life Directions (DNA Strand 4)

### Objective

**Define the foundational motivations that shape a character's entire life story.**

These are the **most important templates in the system**—everything else flows from them.

### Templates to Create

**9 Master Templates (Tier 1 Foundation):**

1. `ld_financial_security` - Build wealth and stability
2. `ld_master_craft` - Achieve professional excellence
3. `ld_creative_fulfillment` - Express artistic vision
4. `ld_discover_self` - Understand who you are
5. `ld_deep_connections` - Build meaningful relationships
6. `ld_balance_everything` - Harmony across life domains
7. `ld_adventure_novelty` - Seek new experiences
8. `ld_make_impact` - Change the world
9. `ld_simple_contentment` - Find peace in the everyday

### Design Process (Per Direction)

#### Step 1: Define the Core Fantasy

**Question:** What does it feel like to live a life guided by this principle?

**Example: `ld_discover_self`**
```
Core Fantasy: "The journey of self-discovery"

The character who chooses this is asking:
  - Who am I, really?
  - What do I actually want (not what I'm told to want)?
  - What are my authentic values?
  - Where do I find meaning?

Emotional Experience:
  - Introspective
  - Uncertain but curious
  - Values experience over achievement
  - Fears living inauthentically
```

#### Step 2: Specify Deck Composition Shifts

**Question:** Which card categories should become more/less frequent?

**Example: `ld_discover_self`**
```json
{
  "card_frequency_modifiers": {
    "introspective_activities": +60,
    "exploration_activities": +50,
    "self_reflection_activities": +70,
    "creative_expression": +40,
    "therapy_counseling": +80,
    "solo_travel": +60,
    
    "corporate_ladder_activities": -50,
    "networking_events": -40,
    "wealth_building": -30
  }
}
```

**Why This Matters:**
- A character pursuing self-discovery naturally encounters more therapy cards, fewer networking events
- The card pool **reflects the life path**
- Different directions = different games

#### Step 3: Outline Key Unlocks

**Question:** What specific content becomes available with this direction?

**Example: `ld_discover_self`**
```
Unlocked Aspirations:
  - asp_complete_therapy_arc (6 months of consistent therapy)
  - asp_try_five_new_hobbies (exploration)
  - asp_solo_travel_adventure (finding self through travel)
  - asp_write_personal_manifesto (articulate values)
  - asp_trace_family_history (understand roots)

Unlocked NPCs:
  - char_therapist (professional guide)
  - char_spiritual_mentor (philosophical guide)
  - char_fellow_seeker (companion in uncertainty)

Unlocked Locations:
  - loc_meditation_center
  - loc_artists_retreat
  - loc_quiet_nature_spot

Unlocked Event Types:
  - evt_identity_crisis (catalyst for growth)
  - evt_unexpected_revelation (surprise self-knowledge)
  - evt_values_conflict (test of authenticity)
```

#### Step 4: Establish Personality Affinities

**Question:** Which OCEAN traits make this direction feel natural vs. challenging?

**Example: `ld_discover_self`**
```
Natural Affinity:
  - High Openness (curiosity about inner world)
  - High Neuroticism (questioning and introspection)
  - Low Extraversion (comfort with solitude)

Challenging For:
  - Low Openness (discomfort with ambiguity)
  - High Extraversion (needs external validation)
  - Very High Conscientiousness (wants clear goals/metrics)

Narrative Implications:
  - High Openness character: "You dive into self-exploration with excitement"
  - Low Openness character: "This ambiguity is uncomfortable, but you persist"
```

**Why This Matters:**
- Same Life Direction → different experience based on personality
- Challenging paths create interesting friction (good narrative)
- No "wrong" personality for any direction

#### Step 5: Define Narrative Priming Affinity

**Question:** Which templates under this Life Direction benefit most from Priming? What latent tensions are common?

**Example: `ld_discover_self`**
```
High-Priming Templates:
  - Therapy sessions (vulnerability opportunities)
  - Solo travel moments (identity revelations)
  - Creative expression activities (authentic self-discovery)
  - Values conflict situations (authenticity tests)

Common Latent Tensions:
  - "Is this real growth or self-indulgence?"
  - "Family expectations vs. authentic desires"
  - "Fear of what you'll discover about yourself"
  - "Imposter syndrome during identity shifts"

Observational Hooks That Often Emerge:
  - "Why do I feel resistance to this path?"
  - "Unexplained emotional reactions to certain topics"
  - "Patterns in what brings genuine joy vs. performed happiness"

Volatility Factors:
  - Identity crisis peaks (Act 2 climax)
  - Family confrontations about life choices
  - Revelations that challenge core beliefs
  - Moments of profound self-recognition
```

**Why This Matters:**
- Priming makes self-discovery moments feel weighted with meaning
- Observational Facets track the journey's evolving questions
- Weekly Analysis can detect when character is avoiding vs. embracing discovery
- VolatilityIndex creates breakthrough potential during key moments

---

## 5. Phase 3: Aspirations & Activities (DNA Strands 2 & 4)

### Objective

Design the **primary goals** that drive a season's plot (Aspirations) and the **daily actions** a player takes to live their life (Activities).

### Templates to Create

**Aspiration Templates (Tier 2):**
- 40 Major Aspiration templates (multi-week commitments)
- 50 Minor Aspiration templates (shorter goals)
- **Total: 90 templates**

**Activity Templates (Tier 4):**
- 80 Activity templates (categorized by function)
- **Total: 80 templates**

---

### Design Process for Aspirations

#### Step 1: Define Archetypal Goals

**Create templates for universal human goals:**

**Categories:**
- **Skill Mastery:** "Achieve expertise in X"
- **Relationship Building:** "Form deep connection with Y"
- **Life Transition:** "Navigate major change Z"
- **Creative Output:** "Produce meaningful work"
- **Personal Growth:** "Overcome limitation"
- **Material Achievement:** "Acquire resource/status"

**Examples:**
```
asp_base_master_skill
  → Instances: Master Photography, Learn Spanish, Master Coding
  
asp_base_relationship_milestone
  → Instances: Find True Love, Repair Family Rift, Build Chosen Family
  
asp_base_career_advancement
  → Instances: Get Promoted, Change Careers, Start Business
```

#### Step 2: Structure the "Story Engine"

**For each template, define universal milestone archetypes:**

**The Standard 4-Act Aspiration Structure:**

```
ACT 1: THE COMMITMENT (Week 1)
  - Character commits to goal
  - Initial excitement and energy
  - First steps are easy

ACT 2: THE PLATEAU (Weeks 2-4)
  - Progress slows
  - Challenges emerge
  - Motivation tested
  - "Is this worth it?" moment

ACT 3: THE SETBACK (Weeks 5-6)
  - Major obstacle appears
  - Feels like failure might be inevitable
  - Capacity strain increases
  - Decision point: Push through or give up?

ACT 4: THE BREAKTHROUGH (Weeks 7-8+)
  - If persisted: Major progress suddenly unlocks
  - If gave up: Alternate resolution (not always bad)
  - Aspiration completes (success/failure/partial)
```

**Example: `asp_get_promotion_senior`**
```
ACT 1: Commitment
  Beat: "You decide to go for it. You tell your mentor."
  Mechanic: Aspiration officially tracked

ACT 2: Plateau
  Beat: "You've been working hard, but no feedback from boss."
  Mechanic: Player must perform work activities, feels like grinding

ACT 3: Setback
  Beat: "Surprise presentation to executives goes poorly. You panic."
  Mechanic: Major Situation Card, Capacity hit, decision required

ACT 4: Breakthrough
  Path A (persist): "Your mentor vouches for you. Boss sees your value."
  Path B (give up): "You withdraw candidacy. Peace, but regret?"
  Mechanic: Resolution, relationship consequences, Capacity shift
```

#### Step 3: Define Outcome Spectrums

**Not binary success/failure—qualitative outcomes:**

**Example: `asp_get_promotion_senior`**

```
EXCEPTIONAL SUCCESS (10%)
  - Promoted ahead of schedule
  - Boss publicly praises
  + Capacity +1.5 (confidence surge)
  + Relationship with mentor +1.0
  - New STATE: INSPIRED (high productivity)
  
STANDARD SUCCESS (40%)
  - Promoted on expected timeline
  - Recognition from team
  + Capacity +0.8
  + Relationship with mentor +0.5
  + Increased income
  
PARTIAL SUCCESS (30%)
  - Not promoted YET, but "next time"
  - Boss acknowledges potential
  + Capacity +0.2 (validated but tired)
  - Lingering doubt
  
FAILURE (15%)
  - Not promoted
  - Position given to colleague
  - Capacity -1.0 (rejection stings)
  - Decision: Stay and try again, or leave?
  
WITHDREW (5%)
  - Player chose to stop pursuing
  - Capacity impact depends on reason
  - Could be healthy (wrong goal) or regretful
```

**Why Spectrum Matters:**
- Most outcomes are **mixed** (authentic)
- Failure creates interesting narrative, not just "game over"
- Player choices throughout influence which outcome

---

### Design Process for Activities

#### Step 1: Categorize the "Verbs of Life"

**Create templates for core activities:**

**Categories:**

**SOCIAL (20 templates):**
- Connect: Coffee, dinner, phone call
- Deepen: Vulnerable conversation, shared activity
- Support: Help friend, be present in crisis
- Meet: Attend event, join group, random encounter

**PRODUCTIVE (20 templates):**
- Work: Standard task, difficult project, overtime
- Side hustle: Freelance, build business
- Admin: Pay bills, manage finances, errands
- Learn: Study, practice skill, take class

**RESTORATIVE (15 templates):**
- Rest: Nap, early bedtime, lazy morning
- Entertainment: TV, games, hobbies
- Self-care: Spa day, comfort food, retail therapy
- Nature: Walk, hike, sit in park

**CHALLENGE (15 templates):**
- Physical: Gym, run, sports
- Mental: Puzzle, research, deep learning
- Social: Public speaking, networking, performance
- Risk: Try new thing, take chance, push limit

**EXPLORATION (10 templates):**
- Places: New café, restaurant, neighborhood
- Experiences: Museum, concert, workshop
- People: Strike up conversation, join meetup
- Ideas: Read philosophy, debate, experiment

#### Step 2: Define Evolution Vectors (⚠️ Anti-Gamification Critical)

**Specify pathways from generic → cherished using qualitative AI assessment.**

**Example: `act_base_connect_socially`**

```
EVOLUTION PATH:

Stage 1: Generic Instance
  Instance: "Meet friend for coffee"
  Trigger: First instantiation
  
Stage 2: Personalized Instance (AI detects familiarity)
  Instance: "Coffee with Sarah"
  Trigger: `ENGINE_WRITERS_ROOM` assesses:
    - Personality compatibility (`ENGINE_PERSONALITY`)
    - Interaction pattern quality (from `ENGINE_MEMORY`)
    - Emotional reciprocity established
    - Comfort level reached
  Timing: Could be 3 meetings (highly compatible) OR 20+ (neutral) OR never (incompatible)
  Changes: Named NPC, -0.5 Energy cost, +5% relationship bonding
  
Stage 3: Cherished Memory (AI detects transformative moment)
  Instance: "Tuesday Afternoons at Café Luna"
  Trigger: `ENGINE_WRITERS_ROOM` detects:
    - Deep emotional bond established
    - Significant shared experience occurred
    - Both characters emotionally receptive (`ENGINE_CAPACITY` check)
    - Lasting impact evident in subsequent interactions
  Timing: When the right moment happens with right states—NOT hit count
  Changes: -1 Energy, +0.3 Capacity restore, high memory resonance active

Alternative Evolution: Location-Anchored (different pathway)
  Instance: "Café Luna (My Second Home)"
  Trigger: `ENGINE_WRITERS_ROOM` detects location emotional anchoring pattern:
    - Character returns for emotional reasons (not convenience)
    - Location associated with meaning, comfort, or routine
    - Multiple significant moments recorded here (`ENGINE_MEMORY`)
  Timing: When location attachment forms—not visit count
  Changes: Location becomes cherished, unlocks location-specific events
```

**⚠️ Critical: NO Numerical Thresholds**
- "Must do X 16 times" is forbidden
- AI assesses qualitative readiness contextually
- Interaction count is an indicator, NOT a determinant
- Same template can evolve differently based on WHO the character is and WHAT happens

#### Step 3: Embed Fusion Tags

**Assign narrative tags for fusion opportunities:**

**Example: `act_coffee_with_friend`**
```json
{
  "fusion_tags": [
    "routine_candidate",
    "social_bonding",
    "low_stakes",
    "conversation_opportunity",
    "comfort_zone"
  ],
  
  "fusion_opportunities": [
    {
      "if_paired_with": "evt_relationship_breakup",
      "fusion_type": "Location Memorial",
      "result": "The café becomes 'Where everything changed'"
    },
    {
      "if_paired_with": "evt_career_decision",
      "fusion_type": "Decision Memorial",
      "result": "The table where you decided to quit your job"
    }
  ]
}
```

**Why This Matters:**
- Story Weaver can identify fusion opportunities automatically
- Emergent storytelling artifacts created naturally
- Every mundane activity is a potential significant memory

---

## 6. Phase 4: The Living World (DNA Strands 5 & 6)

### Objective

Create templates for **people** and **places** that populate the player's story, designed to start generic and become deeply personal through qualitative AI assessment.

### Templates to Create

**Living World Templates (Tier 7):**
- 50 Character Archetype templates (DNA Strand 5)
- 30 Location templates (DNA Strand 6)
- **Total: 80 templates**

---

### Design Process for Characters

#### Step 1: Define Core Archetypes

**Create templates for universal relationship roles:**

**Character Archetypes:**

**SUPPORT ROLES:**
- The Mentor (professional or personal guide)
- The Confidante (emotional support)
- The Cheerleader (enthusiastic supporter)
- The Anchor (grounding presence)

**CHALLENGE ROLES:**
- The Rival (competitive peer)
- The Antagonist (active opposition)
- The Critic (harsh feedback, sometimes needed)
- The Chaos Agent (disrupts plans)

**COMPLEX ROLES:**
- The Complicated Family Member (love + frustration)
- The Ex (shared history, lingering feelings)
- The Frenemy (helpful sometimes, harmful others)
- The Dependent (needs more than they give)

**DISCOVERY ROLES:**
- The Stranger (random encounter, potential)
- The Unexpected Ally (surprising support)
- The Catalyst (changes everything)
- The Mirror (reflects your traits back)

#### Step 2: Embed Mystery Hooks

**For each archetype, define hidden depths:**

**Example: `char_base_mentor_professional`**

```
SURFACE LEVEL (First 5 interactions):
  - Successful, competent professional
  - Offers valuable career advice
  - Seems to have it all together
  
MYSTERY HOOKS (Revealed through relationship deepening):
  
  Hook 1: "The Regret"
    Trigger: Relationship Level 5+, vulnerable conversation
    Reveal: "I sacrificed my marriage for this career. 
             Sometimes I wonder if it was worth it."
    Impact: Mentor becomes human, creates dramatic irony
    
  Hook 2: "The Illness"
    Trigger: Random event (10% chance after Level 6)
    Reveal: Mentor is dealing with chronic health condition
    Impact: Support dynamic reverses, player can help them
    
  Hook 3: "The Secret Past"
    Trigger: Relationship Level 8+, coincidental discovery
    Reveal: Mentor had completely different career before this
    Impact: Recontextualizes all previous advice
```

**Why Mystery Matters:**
- NPCs feel **three-dimensional**
- Long-term relationships stay interesting
- Dramatic irony creates depth
- Players invest in learning NPC stories

#### Step 3: Outline Relationship Pathways (⚠️ Journey Beats, Not Interaction Counts)

**Specify qualitative journey beats required for evolution:**

**Example: `char_base_mentor_professional`**

```
RELATIONSHIP PROGRESSION:

Stranger → Acquaintance (`ENGINE_WRITERS_ROOM` detects initial rapport)
  Beat: First meeting, `ENGINE_PERSONALITY` compatibility assessed
  Timing: Immediate if highly compatible, gradual if neutral, may NEVER happen if clash
  AI Criteria: Personality alignment, mutual interest detected
  
Acquaintance → Professional Relationship (`ENGINE_WRITERS_ROOM` detects respect established)
  Beat: Journey Beat "Valuable Guidance" - Mentor's advice proves valuable AND character receptive
  Timing: When character demonstrates willingness to learn AND mentor sees potential
  AI Criteria: Demonstrated competence receptivity, mentor efficacy, trust beginning
  
Professional → Personal (`ENGINE_WRITERS_ROOM` detects vulnerability opening)
  Beat: Journey Beat "Vulnerability Moment" - One person shares non-work struggle
  Requirement: Both emotionally ready (`ENGINE_CAPACITY` sufficient)
  Example: Mentor reveals regret about work-life balance when character has capacity to receive
  Timing: When trust sufficient + emotional states align (not meeting count)
  AI Criteria: Vulnerability offered when both receptive, trust deepens
  
Personal → Deep Trust (`ENGINE_WRITERS_ROOM` detects profound support moment)
  Beat: Journey Beat "Crisis Support Moment"
  Requirement: Capacity + 2 rule satisfied
  Path A: Character receives support when mentor has capacity
  Path B: Character supports mentor through hidden struggle
  Timing: When relationship tested and proves resilient
  AI Criteria: Effective support given, relationship depth proven through adversity
  
Deep Trust → Lifelong Bond (`ENGINE_WRITERS_ROOM` detects enduring connection)
  Beat: Journey Beat "Enduring Bond" - Relationship survives major challenges
  Timing: After weathering multiple storms together (qualitative, not counted)
  AI Criteria: Consistent mutual support, lasting value demonstrated, irreplaceable bond
```

**⚠️ Critical: Journey Beats Are Mandatory**
- Relationships CANNOT progress without qualitative Journey Beats
- Forced interaction without emotional presence = stalled progression
- AI assesses readiness based on personality, capacity, and context
- See `06-growth-and-progression.md` for detailed Journey Beat specifications

---

### Design Process for Locations

#### Step 1: Define Archetypal Spaces

**Create templates for core location types:**

**Location Archetypes:**

**COMMUNITY HUBS:**
- Café/coffee shop (social gathering)
- Library (quiet productive)
- Community center (activity-based)
- Bar/pub (nightlife social)

**WORK SPACES:**
- Office (corporate)
- Studio (creative)
- Shop (retail/service)
- Remote workspace (freelance)

**PERSONAL SANCTUARIES:**
- Home (primary)
- Secret spot (hidden refuge)
- Childhood place (nostalgic)
- Natural place (restorative)

**GROWTH SPACES:**
- Gym/studio (physical)
- Classroom (learning)
- Gallery/theater (cultural)
- Wilderness (adventure)

#### Step 2: Specify Evolution Vectors

**Define how locations accrue meaning:**

**Example: `loc_base_community_hub` (Café)**

```
EVOLUTION PATH:

Stage 1: Generic
  Instance: "A local café"
  Description: "A café near your apartment. It's fine."
  
Stage 2: Familiar Place (AI detects regular pattern)
  Instance: "The Copper Kettle"
  Description: "You've been here enough that the barista recognizes you."
  Trigger: Story Weaver detects consistent visitation + comfort established
  Timing: Could be fast (daily visits while unemployed) or slow (weekly habit)
  Mechanical: -$2 drink cost (regular discount)
  
Stage 3: Personal Sanctuary (AI detects emotional attachment)
  Instance: "The Copper Kettle (My Thinking Spot)"
  Trigger: Significant emotional moment experienced here + character returns for emotional reasons
  Examples: Processed a breakup here, made life decision here, finds peace here
  Timing: When location becomes emotionally significant, not visit count
  Description: "This place has seen you at your worst and best. The corner table is practically yours."
  Mechanical: +0.5 Capacity when visiting (emotional safety)
  
Alternative Evolution: Social Hub (AI detects social association pattern)
  Instance: "The Copper Kettle (Where Everyone Knows Your Name)"
  Trigger: Pattern of bringing different friends here + positive social experiences
  Timing: When location becomes associated with connection, not raw visit count
  Description: "You've brought everyone here. It's become your spot for catching up with friends."
  Mechanical: +10% relationship bonding when meeting NPCs here
```

**Why Location Evolution Matters:**
- Places become **characters** in the story
- Geography carries **emotional weight**
- "Where" becomes as important as "what" and "who"

---

## 7. Phase 5: Systems of Growth (DNA Strand 7)

### Objective

Define the underlying mechanics of character development: Skills, Items, and Perks that integrate with Core Engines.

### Templates to Create

**System Templates (Tier 6):**
- 30 Skill templates
- 30 Item templates  
- 10 Perk templates
- **Total: 70 templates**

---

### Design Process for Skills

#### Step 1: Catalog Core Life Skills

**Skill Categories:**

**CREATIVE (10 skills):**
- Visual arts (photography, painting, design)
- Performing arts (music, dance, theater)
- Writing (fiction, poetry, journalism)
- Craft (woodworking, cooking, fashion)

**PROFESSIONAL (8 skills):**
- Technical (programming, data analysis)
- Business (project management, negotiation)
- Communication (public speaking, writing)
- Leadership (management, mentorship)

**PRACTICAL (7 skills):**
- Life skills (cooking, home repair, budgeting)
- Physical (fitness, self-defense, dance)
- Social (emotional intelligence, networking)

**INTELLECTUAL (5 skills):**
- Academic (research, critical thinking)
- Languages (Spanish, French, etc.)
- Strategic (planning, systems thinking)

#### Step 2: Define Mastery Paths

**For each skill, specify 0-10 progression:**

**Example: `skill_photography`**

```
LEVEL 0-1: NOVICE
  Can: Take basic photos
  Quality: Often blurry, poor composition
  Unlocks: Nothing yet
  
LEVEL 2-3: HOBBYIST
  Can: Understand exposure, basic composition
  Quality: Decent vacation photos
  Unlocks: asp_build_portfolio, item_basic_camera

LEVEL 4-5: COMPETENT
  Can: Shoot in manual mode, edit effectively
  Quality: Good enough to gift or share
  Unlocks: asp_first_paid_gig, act_teach_photography_basics

LEVEL 6-7: PROFICIENT
  Can: Consistent quality, developing style
  Quality: Professional-looking work
  Unlocks: asp_launch_photography_business, act_photography_exhibition

LEVEL 8-9: EXPERT
  Can: Master of craft, teaching others
  Quality: Gallery-worthy, commercial-viable
  Unlocks: asp_quit_day_job_for_art, char_photography_agent

LEVEL 10: MASTER
  Can: Innovating in the field
  Quality: Recognition, awards, influence
  Unlocks: asp_major_exhibition, evt_featured_in_magazine
```

#### Step 3: Integrate Engine Modifiers

**How `ENGINE_CAPACITY` and `ENGINE_PERSONALITY` affect skill growth:**

**`ENGINE_CAPACITY` Impact (ALL Skills):**
| Capacity Level | XP Modifier | Reason |
|----------------|-------------|--------|
| 8.0+ | +30% XP | Thriving, optimal learning state |
| 5.0-7.9 | Normal XP | Healthy baseline |
| 3.0-4.9 | -25% XP | Struggling, distracted |
| < 3.0 | -60% XP | Barely functional |

**`ENGINE_PERSONALITY` Impact (Example: Creative Skills):**
| Personality Trait | Modifier | Effect |
|-------------------|----------|--------|
| High Openness (0.7+) | +50% XP | Faster breakthroughs, embraces experimentation |
| Low Openness (0.3-) | -30% XP | Slower inspiration, resists novelty |
| High Conscientiousness (0.7+) | +30% XP | Consistent practice, disciplined |
| Low Conscientiousness (0.3-) | -40% XP | Inconsistent effort, easily distracted |

**Optimal Combination:** High Openness + High Conscientiousness = +80% XP (creative + disciplined)

**Challenging Combination:** Low Openness + Low Conscientiousness = -70% XP (requires authentic struggle)

**Cross-Reference:** See `06-growth-and-progression.md` for full skill progression specifications and Skill Rust system

---

## 8. Phase 6: Narrative Catalysts (DNA Strand 3)

### Objective

Design templates for **unpredictable events** that make a life story compelling. These are direct inputs for `ENGINE_WRITERS_ROOM` specialists.

### Templates to Create

**Event Templates (Tier 5):**
- 60 Event templates (Situation Cards)
- **Total: 60 templates**

---

### Design Process for Events

#### Step 1: Template Event Archetypes

**Create structured templates for universal narrative beats:**

**Event Categories:**

**CRISIS (15 templates):**
- Health (injury, illness, mental breakdown)
- Financial (job loss, unexpected expense, debt)
- Relationship (betrayal, conflict, loss)
- External (natural disaster, accident, crime)

**OPPORTUNITY (15 templates):**
- Career (job offer, promotion, side hustle)
- Creative (competition, exhibition, publication)
- Relationship (meet someone, reconnect, confession)
- Discovery (hidden talent, unexpected inheritance)

**BREAKTHROUGH (10 templates):**
- Personal (self-realization, overcome fear)
- Skill (sudden mastery moment)
- Relationship (level of intimacy reached)
- Creative (artistic breakthrough)

**SETBACK (10 templates):**
- Aspiration blocked (obstacle to goal)
- Relationship damaged (fight, miscommunication)
- Skill plateau (frustrating lack of progress)
- External force (bureaucracy, bad luck)

**RELATIONSHIP TEST (10 templates):**
- Conflict (values clash, unmet needs)
- Vulnerability demand (emotional risk required)
- Support test (can they show up?)
- Loyalty test (choose between people/priorities)

#### Step 2: Define Generation Triggers (`ENGINE_WRITERS_ROOM` Integration)

**Specify when `ENGINE_WRITERS_ROOM` specialists will generate each event:**

**Example: `evt_base_health_crisis`**

```
GENERATION TRIGGERS:

Pacing Specialist:
  Trigger if: Tension SERENE for 12+ days
  Purpose: Inject URGENT tension to maintain narrative momentum

Narrative Arc Specialist:
  Trigger if: Act 2 and no major obstacle yet
  Purpose: Generate complication for 3-act structure

Character State Specialist:
  Trigger if: `ENGINE_CAPACITY` > 7.0 for 15+ days
  Purpose: Test resilience, prevent unrealistic smooth sailing

The Critic:
  Trigger if: Story feels predictable (lack of surprise)
  Purpose: Inject stakes and uncertainty
```

**The Director (Synthesizer) combines specialist inputs to determine:**
- Event timing (when)
- Event severity (how intense)
- Event specifics (contextual details from `ENGINE_MEMORY`)
- Choice framework (based on `ENGINE_PERSONALITY` and `ENGINE_CAPACITY`)

#### Step 3: Structure the Choices

**For each event template, define choice framework:**

**Example: `evt_health_crisis` (injury/illness)**

```
CHOICE FRAMEWORK:

Setup:
  Severity: Moderate (can work through) vs Severe (must rest)
  Timing: Before major deadline/event (worst timing)
  
Presented Choices:

  CHOICE A: "Push through it"
    Personality alignment: High Conscientiousness, Low Neuroticism
    Immediate: Aspiration progress continues
    Cost: -2 Capacity, risk of worsening condition
    Long-term: Possible STATE_INJURED escalates to chronic
    
  CHOICE B: "Take time off to recover"
    Personality alignment: High Openness, High Neuroticism
    Immediate: Aspiration progress stalls, disappoint others
    Benefit: +1 Capacity (rest), proper healing
    Long-term: Relationships may deepen (who shows up?)
    
  CHOICE C: "Ask for help"
    Personality alignment: High Agreeableness
    Requirement: 5.0+ Capacity to seek support effectively
    Immediate: Test relationships (Capacity + 2 rule)
    Variable: Support received OR disappointment
    Long-term: Relationships either deepen or strain

NO RIGHT ANSWER:
  - Each choice has authentic tradeoffs
  - Personality makes certain choices feel natural
  - Consequences ripple into future story
```

**Why Structure Matters:**
- Choices test character's values and limits
- No "correct" answer (authentic complexity)
- Outcomes feed into ongoing narrative
- Personality creates different optimal strategies

---

## 9. Production Priority Matrix

### What to Build First (Critical Path)

**Prerequisites Before Any Templates:**
1. ✅ **Phase 0: Core Simulation Engines** (complete and tested)
2. ✅ **Phase 1: Gameplay DNA** (7 Strands defined)

**MVP for Vertical Slice (First Playthrough):**

**Must-Have (60 templates minimum):**

| Category | Count | Specific Templates |
|----------|-------|-------------------|
| **Life Directions** | 3 | Financial security, Deep connections, Discover self |
| **Aspirations** | 15 | 5 per direction (mix major/minor) |
| **Activities** | 25 | 5 per category (social, productive, restorative, challenge, exploration) |
| **Characters** | 10 | 2 mentors, 3 friends, 2 family, 1 rival, 2 romantic interests |
| **Locations** | 5 | Café, workplace, home, gym, park |
| **Skills** | 10 | 3 creative, 3 professional, 2 practical, 2 physical |
| **Events** | 5 | 1 crisis, 1 opportunity, 1 breakthrough, 1 setback, 1 relationship test |

**This enables:**
- Complete Season (12 weeks of gameplay)
- All core systems functional
- Proves the simulation loop works
- Foundation for expansion

---

### Full Base Set (300 templates)

**Priority 1: Core Loops (150 templates)**
- All 9 Life Directions
- 45 Aspirations (30 major, 15 minor per direction)
- 50 Activities (10 per category)
- 25 Characters (diverse archetypes)
- 15 Locations (cover all needs)
- 15 Skills (broad coverage)

**Priority 2: Narrative Depth (80 templates)**
- 40 Events (crisis, opportunity, breakthrough, setback, test)
- 20 Items (10 functional, 10 sentimental)
- 10 Perks
- 10 Additional Characters (antagonists, complex roles)

**Priority 3: Polish & Variety (70 templates)**
- 20 Additional Activities (edge cases, unique experiences)
- 20 Additional Aspirations (niche goals)
- 15 Additional Characters (rare archetypes)
- 10 Additional Locations (special places)
- 5 Additional Skills (specialized)

---

## 10. Template Documentation Standard

### Critical Requirements

**⚠️ Every Template MUST:**
1. Define **qualitative assessment criteria** for `ENGINE_WRITERS_ROOM`
2. Specify **NO arbitrary numerical thresholds** for progression
3. Reference relevant **Core Engines** (PERSONALITY, CAPACITY, MEMORY, WRITERS_ROOM)
4. Include **evolution_vectors** with contextual triggers
5. Define **personality_modifiers** and **capacity_modifiers**

### Minimum Viable Template Structure

```json
{
  "template_id": "act_base_connect_socially",
  "template_name": "Social Connection Activity",
  "tier": 4,
  "category": "social",
  
  "instantiation_rules": {
    "context_variables": [
      "character_age",
      "personality_extraversion",
      "current_relationships",
      "location_pool",
      "time_of_day"
    ],
    "generation_prompt": "Generate a social connection activity appropriate for a [age]-year-old with [extraversion] extraversion, at [location], during [time_of_day]",
    "flavor_examples": [
      "Coffee meetup at local café",
      "Dinner party at friend's place",
      "Study group at library",
      "Book club discussion",
      "Networking happy hour"
    ]
  },
  
  "base_mechanics": {
    "time_cost": {"min": 1.0, "max": 3.0, "unit": "hours"},
    "energy_cost": {"min": 1, "max": 3},
    "money_cost": {"min": 0, "max": 50, "currency": "USD"},
    "capacity_cost": {"min": 0, "max": 0.5}
  },
  
  "personality_modifiers": {
    "high_extraversion": {
      "energy_cost": -1,
      "success_bonus": 0.2,
      "narrative_tone": "energizing"
    },
    "low_extraversion": {
      "energy_cost": +1.5,
      "capacity_cost": +0.3,
      "narrative_tone": "draining"
    }
  },
  
  "capacity_modifiers": {
    "capacity_high": {"success_bonus": 0.1, "connection_depth": "deeper"},
    "capacity_low": {"success_penalty": 0.2, "connection_depth": "surface"}
  },
  
  "evolution_vectors": [
    {
      "stage": "personalized",
      "trigger": "ai_detects_familiarity_pattern",
      "assessment_criteria": [
        "interaction_consistency",
        "personality_compatibility",
        "emotional_reciprocity",
        "no_fixed_threshold"
      ],
      "transformation": "Named activity with specific NPC",
      "mechanical_changes": {"energy_cost": -0.5, "relationship_bonus": 0.05},
      "notes": "May happen after 2 meetings (compatible) or 30 (incompatible) or never (clash)"
    },
    {
      "stage": "cherished",
      "trigger": "ai_detects_transformative_moment",
      "assessment_criteria": [
        "significant_shared_experience",
        "both_emotionally_present",
        "lasting_impact_detected",
        "no_fixed_threshold"
      ],
      "transformation": "Ritual with emotional significance",
      "mechanical_changes": {
        "energy_cost": -1,
        "capacity_restore": 0.3,
        "memory_resonance": "high"
      },
      "notes": "One profound moment can trigger this; twenty shallow ones won't"
    }
  ],
  
  "fusion_tags": [
    "routine_candidate",
    "social_bonding",
    "low_stakes",
    "conversation_opportunity",
    "comfort_zone"
  ],
  
  "narrative_hooks": [
    "Opportunity for unexpected encounter",
    "Setting for vulnerable conversation",
    "Routine that can be disrupted for drama",
    "Location where significant decision can be made"
  ],
  
  "related_templates": [
    "loc_base_community_hub",
    "char_base_friend",
    "evt_base_relationship_deepening"
  ]
}
```

---

## 11. The Genesis Plan Promise

**What This Architecture Achieves:**

| Goal | Achievement |
|------|-------------|
| **Systematic build order** | Foundation (Engines) → Concepts (DNA) → Content (Templates) |
| **Anti-gamification** | AI qualitative assessment prevents grinding |
| **Infinite replayability** | 300 templates × infinite contexts = truly unique stories |
| **Exponential expansion value** | New templates multiply fusion/evolution opportunities |
| **Maintainable** | Modify template once, affects all instances |
| **AI-native** | Built for `ENGINE_WRITERS_ROOM` from ground up |

**The Ultimate Goal:**

> By following this plan, we build a living, breathing world that generates **novel-quality life stories** that are **never the same twice**—where progression emerges from authentic emotional experiences, not arbitrary numerical gates.

**This is not a card game. This is a life story simulation engine.**

---

## Cross-Reference Map

**Related Master Truths:**
- `master_truths_canonical_spec_v_1_2.md` - Core design philosophy and DNA Strands
- `master_numerical_grounding_v_1_2.md` - Numerical balance specifications
- `06-growth-and-progression.md` - Detailed progression mechanics and Journey Beats

**Core Design Philosophy:**
- **Anti-Gamification Mandate** - Core principle (see introduction)
- Qualitative AI assessment over numerical thresholds
- Emergence over mechanics

**AI Systems (Phase 0):**
- `ENGINE_PERSONALITY` - OCEAN-based behavior and modifiers
- `ENGINE_CAPACITY` - Emotional resilience and perception
- `ENGINE_MEMORY` - Event recording and query system
- `ENGINE_WRITERS_ROOM` - AI narrative director with specialists

**Gameplay DNA (Phase 1):**
- See `docs/2.gameplay/` for detailed Strand specifications
- DNA Strands 1-7 define fundamental concepts
- Templates implement these concepts

**Implementation:**
- All templates must reference Core Engines in assessment criteria
- Evolution must be contextual (personality, capacity, timing)
- See template documentation standard (Section 10) for structure

