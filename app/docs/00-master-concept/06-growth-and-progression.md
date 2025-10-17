# Growth & Progression

**Document Status**: V3 Canonical Reference  
**Last Updated**: October 16, 2025  
**Authority Level**: Master Truth

---

## 1. Core Philosophy: Earned, Not Grinded

**The Key Principle:**
> Progression in Unwritten is not about accumulating numbers. It's about accumulating **meaningful experiences** that change who your character is.

**Cross-References:**
- Core design philosophy: See `master_truths_canonical_spec_v_1_2.md`
- AI assessment systems: `ENGINE_WRITERS_ROOM`, `ENGINE_PERSONALITY`, `ENGINE_CAPACITY`
- Card mechanics: DNA Strands 2 (Actions), 5 (Characters), 6 (Locations), 7 (Items/Skills)

**Traditional vs. Unwritten Progression:**

| Traditional Games | Unwritten |
|------------------|-----------|
| Do activity X 100 times → Level up | Have meaningful experience → Evolution |
| Higher level = More power | Evolution = More narrative weight |
| Grinding is optimal | Authentic engagement is only path |

**The Result:**
- **No grinding:** Repetition without meaning doesn't progress anything
- **Every evolution feels earned:** `ENGINE_WRITERS_ROOM` assesses quality, not quantity
- **Relationships are authentic:** You can't farm friendship points

---

## 2. Template Evolution: Generic to Cherished (DNA Strands 2, 5, 6)

### The Three-Stage Evolution

Evolution applies across Master Templates (DNA Strands 2, 5, 6). **Evolution timing is contextual, not numerical.**

```
STAGE 1: Generic Instance (from Master Template)
  ↓ (`ENGINE_WRITERS_ROOM` detects familiarity pattern)
STAGE 2: Personalized Instance (gains specific identity)
  ↓ (`ENGINE_WRITERS_ROOM` detects transformative moment + receptivity)
STAGE 3: Cherished Memory (fully unique, high narrative weight)
```

### Stage Comparison

| Aspect | Generic | Personalized | Cherished |
|--------|---------|--------------|-----------|
| **Name** | `act_coffee_with_friend` | `Coffee with Sarah` | `Tuesday Afternoons at Café Luna` |
| **Narrative** | "You grab coffee with a friend." | "You meet Sarah at your usual spot." | "This ritual has become sacred..." |
| **Energy Cost** | Standard | -0.5 Energy | -1.0 Energy |
| **Special Effects** | None | +5% relationship bond | +0.3 Capacity restoration |
| **Discardable** | Yes | No | Never |
| **Memory Resonance** | None | Beginning | High (triggers callbacks) |

### Evolution Requirements

**Stage 1 → 2 (Personalized):**
- `ENGINE_WRITERS_ROOM` detects **established familiarity pattern**
- Assessed via: `ENGINE_PERSONALITY` compatibility, emotional reciprocity, interaction quality
- **Narrative Priming during interactions may accelerate recognition**
- **NOT a fixed interaction count** (2-3 meetings for compatible personalities, may never happen for incompatible)

**Stage 2 → 3 (Cherished):**
- `ENGINE_WRITERS_ROOM` detects **deep emotional bond** established
- **AND** a **transformative moment** occurred:
  - Vulnerability moment shared (both open via `ENGINE_CAPACITY`)
  - Crisis support given/received (Capacity + 2 rule satisfied)
  - Significant decision made together
  - Breakthrough or revelation experienced
- **Both characters must be emotionally receptive** (checked via `ENGINE_CAPACITY`)
- **Narrative Priming increases VolatilityIndex, making breakthrough more likely**
- **High-Priming interactions create conditions for evolution**

**Why Contextual Assessment Matters:**
- One profound conversation at 3 AM can create a cherished memory
- Twenty surface-level meetings might never evolve
- High-Neuroticism characters may push people away despite opportunities
- Evolution reflects WHO these characters are, not interaction count

### Evolution Example: Maya & Sarah's Journey

**Week 1-2: Generic → Personalized**

*Context:* Maya (high Extraversion, Openness 0.8) meets Sarah (high Extraversion, Openness 0.7)

- **Meeting 1:** Instant rapport, conversation flows naturally
- **Meeting 2:** Already sharing personal stories
- **Meeting 3:** Feel like old friends despite just meeting
- **`ENGINE_WRITERS_ROOM` assessment:** "Personality compatibility high. Familiarity pattern established."
- **EVOLUTION:** `act_coffee_with_friend` → `Coffee with Sarah`

**Week 4: Personalized → Cherished**

*The Transformative Moment:*
- Maya's rough day (Capacity 4.2 - vulnerable but not collapsed)
- Sarah notices immediately (high Agreeableness, Capacity 7.5)
- Maya shares job stress, Sarah responds with empathy
- **All factors align:** Vulnerability offered + support capacity available + timing right
- **`ENGINE_WRITERS_ROOM` assessment:** "Transformative moment detected. Deep bond formed."
- **EVOLUTION:** `Coffee with Sarah` → `Tuesday Afternoons at Café Luna`
- **New mechanics:** +0.3 Capacity restoration, deep dialogue unlocked

**Weeks Later: Memory Resonance Active**
> "You need someone to talk to. You remember that day at Café Luna when you first really opened up to Sarah, and she just... got it."

**Why This Works:**
- Evolution occurred in 4 weeks due to high personality compatibility
- Different pairing might take months or never evolve
- No arbitrary "must meet X times" gate
- Reflects WHO these characters are

---

## 3. Relationship Progression: Journey-Based (DNA Strand 5)

### The Anti-Grinding Mandate

**Traditional Problem:** Do activity X enough times → Level up (encourages grinding)

**Unwritten Solution:** Relationships require **both quantity (time) AND quality (moments)**

### The Relationship Stages & Required Journey Beats

```
STRANGER (0/10)
  ↓ (`ENGINE_WRITERS_ROOM` detects initial rapport)
ACQUAINTANCE (2/10)
  ↓ (Journey Beat: "Connection Moment")
FRIEND (5/10)
  ↓ (Journey Beat: "Vulnerability Moment")
CLOSE FRIEND (7/10)
  ↓ (Journey Beat: "Crisis Support Moment")
SOULMATE (10/10)
```

**Critical Rule:** A relationship can **stall indefinitely** without the qualitative Journey Beats. Forced interaction without emotional presence never progresses relationships.

### Journey Beat Definitions

**"Connection Moment" (Acquaintance → Friend):**
- Sharing personal information
- Discovering unexpected common ground
- Choosing to be present in a meaningful conversation
- **Requires:** Both characters emotionally available (`ENGINE_CAPACITY` sufficient)

**"Vulnerability Moment" (Friend → Close Friend):**
- One person shares deep fear, shame, or pain
- Other person responds with empathy
- **Requires:** Sufficient `ENGINE_CAPACITY` in supporter (Capacity + 2 rule)
- Emotional risk is taken and honored
- **Creates high-weight Memory with rich Facets:**
  - **Primary:** The core of what was shared
  - **Sensory:** The setting, the tone of voice, physical presence
  - **Observational:** Unspoken implications, future hooks

**"Crisis Support Moment" (Close Friend → Soulmate):**
- One person faces major crisis
- Other person shows up significantly
- **Requires:** Capacity + 2 rule satisfied, support must be effective
- Relationship proves its depth through adversity

**Additional Journey Beat Types:**
- **"Shared Joy Moment":** Celebrating success together
- **"Conflict Resolution Moment":** Fighting and repairing
- **"Sacrifice Moment":** Choosing other over self-interest

---

## 4. NPC Emotional Capacity: Dynamic Support (DNA Strand 5)

### The Capacity + 2 Rule

**Core Mechanic:**
> Every NPC has their own `ENGINE_CAPACITY` that fluctuates. An NPC can only provide effective support if:  
> **(NPC Capacity + 2) > Crisis Level**

**Why This Matters:**
- **Support is not guaranteed** (timing matters)
- **Relationships are reciprocal** (you must also support them)
- **Creates authentic complexity** (perfect friends don't exist)
- **NPCs are not vending machines** (they have limits)

### Example: Sarah's Variable Support Capacity

**Scenario: Maya's Job Loss Crisis (Level 5)**

| Sarah's State | Calculation | Result | Outcome |
|---------------|-------------|--------|---------|
| **Capacity 6.5** (healthy) | 6.5 + 2 = 8.5 > 5 ✅ | **Support effective** | Maya's Capacity: 3.0 → 3.8<br>Journey Beat: "Crisis Support" achieved |
| **Capacity 2.8** (mom sick) | 2.8 + 2 = 4.8 < 5 ❌ | **Cannot help effectively** | Maya's Capacity: 3.0 → 2.9<br>Sarah feels guilty, relationship stressed |

**When Support Fails (Capacity 2.8 scenario):**
```
"Oh god, Maya... I'm so sorry. I wish I could be there
for you right now. But I'm barely holding it together. 
My mom's in the hospital and I... I can't..."

Choices:
  [ ] "It's okay. You focus on your mom." (Empathy: +0.2 relationship, but no support gained)
  [ ] "But I really need you." (Strains friendship: -1.0 relationship, damages trust)
```

**The Design Beauty:**
- Both outcomes are **authentic**
- Sometimes **nobody can help** and that's the story
- Forces players to **build multiple support relationships**
- Failed support moments create rich narrative (not dead ends)

---

## 5. Skill Progression: Mastery Through Practice (DNA Strand 7)

### The 0-10 Skill System

Skills range from Level 0 (Untrained) to Level 10 (Master). Examples: `skill_cooking`, `skill_photography`, `skill_programming`, `skill_emotional_intelligence`

**XP Curve:** Exponential scaling (Level 0→1: 50 XP, Level 9→10: 3500 XP)

### Contextual XP Modifiers

**Base XP Gains:**
- Simple activity: 5-10 XP
- Challenging activity: 15-25 XP
- Teaching others: 30-50 XP (mastery through teaching)

**`ENGINE_PERSONALITY` Modifiers:**
| Skill Type | Personality Trait | Modifier |
|------------|------------------|----------|
| Creative (photography, writing) | High Openness | +50% XP |
| Creative (photography, writing) | Low Openness | -25% XP |
| Organizational (project_mgmt) | High Conscientiousness | +50% XP |
| Organizational (project_mgmt) | Low Conscientiousness | -30% XP |

**`ENGINE_CAPACITY` Modifiers (ALL Skills):**
- Capacity >= 7.0: **+20% XP** (learning when healthy)
- Capacity <= 3.0: **-50% XP** (can't focus when overwhelmed)

**Why This Matters:** Your mental state and personality authentically affect learning capacity.

### Skill Level Benefits

| Level | Tier | Success Rate | Benefits | Examples |
|-------|------|--------------|----------|----------|
| 0-2 | **Novice** | 40-60% | None | Can attempt basics |
| 3-4 | **Competent** | 65-75% | Small passive benefits | `skill_cooking`: -$5 meal cost |
| 5-6 | **Proficient** | 80-85% | Significant benefits | `skill_photography`: Unlock business aspiration |
| 7-8 | **Expert** | 90-95% | Major benefits + teaching | `skill_public_speaking`: -1 Energy networking |
| 9-10 | **Master** | 95-98% | Exceptional + reputation | `skill_programming`: Unlock startup aspiration |

### Skill Rust System

**NOT immediate level loss.** Instead: gradual decay with grace period.

**Decay Timeline (if unused):**
1. **Weeks 1-4:** No effect
2. **Week 5+:** Effectiveness drops (Level 5 performs like Level 4)
3. **Week 10+:** XP begins to drain slowly
4. **Week 20+:** Level drops if continued disuse

**Reactivation:** Using skill stops XP drain immediately. One practice session restores 50% rusted effectiveness. Full effectiveness after 2-3 uses.

**Why This Works:** Allows breaks without punishment, but long-term neglect has authentic consequences. Relearning is faster than learning from scratch.

---

## 6. Items & Perks: Tangible Growth (DNA Strand 7)

### Items: Tools and Memories

**Two Categories:**

| Type | Purpose | Examples | Properties |
|------|---------|----------|------------|
| **Functional Items** | Unlock actions, improve performance | `item_professional_camera` (unlock photo activities)<br>`item_laptop` (required for coding)<br>`item_gym_membership` (reduce exercise cost) | Can be lost/broken/stolen<br>Narrative weight when lost<br>Expensive to replace |
| **Sentimental Items** | Emotional/narrative weight | `item_mothers_necklace` (+0.2 Capacity)<br>`item_shattered_mug` (-0.3 Capacity reminder)<br>`item_concert_ticket_stub` (memory trigger) | Cannot accidentally discard<br>Generate memory resonance<br>Can evolve via narrative |

### Perks: Behavioral Rewards

**Earned through sustained behavioral patterns detected by `ENGINE_WRITERS_ROOM`.** Never bought or chosen.

| Perk | Earned By | Effect | Can Be Lost? |
|------|-----------|--------|--------------|
| `perk_morning_person` | Waking early 30 days | +2 Energy, +20% AM productivity | Yes (60 days not early) |
| `perk_resilient` | Surviving 3+ crises without breakdown | -20% Capacity loss from negatives | No (permanent growth) |
| `perk_social_butterfly` | Maintaining 5+ friendships | -1 Energy for social activities | Yes (friendships drop) |
| `perk_night_owl` | Working late 30 days | No Energy penalty at night | Yes (60 days early schedule) |
| `perk_quick_learner` | Reaching Level 5+ in 3 skills | +25% XP gain all skills | No (knowledge retained) |

**Key Properties:**
- **Earned, never chosen** (reflect who you've become)
- **Can be lost if behavior changes** (authentic to lifestyle shifts)
- **Create emergent playstyles** (build synergies with personality/skills)

---

## 7. Critical Design Rules (Non-Negotiable)

| Rule | Principle | Implementation |
|------|-----------|----------------|
| **1. No Grinding Works** | Mechanical thresholds ≠ progression | Journey Beats mandatory for relationship advancement |
| **2. Evolution Is Transformative** | Not "+1 better" | Cherished cards are fundamentally different experiences |
| **3. NPCs Have Limits** | Capacity + 2 rule | Failed support moments are valid story beats |
| **4. Skills Respect Reality** | Context affects learning | `ENGINE_CAPACITY` and `ENGINE_PERSONALITY` modify XP |
| **5. Items Tell Stories** | Everything has narrative weight | Functional items can be lost, sentimental items trigger memory |
| **6. Perks Reflect Identity** | Earned, never chosen | Lost if behavior changes (authentic lifestyle shifts) |

---

## 8. The Progression Promise

**What This System Achieves:**

| Goal | How It's Achieved |
|------|-------------------|
| **Authenticity over optimization** | You can't min-max relationships; `ENGINE_WRITERS_ROOM` assesses quality, not quantity |
| **Every progression feels earned** | Card evolution requires meaningful moments; relationships require Journey Beats |
| **NPCs feel like real people** | They have limits (Capacity + 2 rule); they can't always help |
| **Emergent playstyles** | Perks reflect unique patterns; skills shape opportunities |
| **No dead ends** | Failed moments create new narrative; stalled relationships can revive |

**The Ultimate Goal:**

> When you look at your character at the end of their life, you should see a **unique person shaped by authentic experiences**—not a checklist of completed objectives.

Growth in Unwritten is about **becoming**, not **achieving**.

---

## Cross-Reference Map

**Related Master Truths:**
- `master_truths_canonical_spec_v_1_2.md` - Core design philosophy
- `master_numerical_grounding_v_1_2.md` - Numerical balance specifications
- DNA Strand 2 (`docs/2.gameplay/`) - Action Card mechanics
- DNA Strand 5 (`docs/2.gameplay/`) - Character & relationship systems
- DNA Strand 6 (`docs/2.gameplay/`) - Location evolution
- DNA Strand 7 (`docs/2.gameplay/`) - Items, skills, perks

**AI Systems:**
- `ENGINE_WRITERS_ROOM` - Assesses qualitative progression readiness
- `ENGINE_PERSONALITY` - OCEAN trait modifiers for growth
- `ENGINE_CAPACITY` - Emotional bandwidth affecting learning and support

