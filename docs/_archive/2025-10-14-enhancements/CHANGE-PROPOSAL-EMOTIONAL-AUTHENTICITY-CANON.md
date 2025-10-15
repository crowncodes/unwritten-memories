# Change Proposal: Emotional Authenticity & Novel-Quality Systems

**CP ID:** CP-2025-10-14-001  
**Title:** Integrate Emotional Authenticity & Novel-Quality AI Systems into Master Truths  
**Date:** October 14, 2025  
**Status:** Proposed  
**Target Master Truths Version:** v1.2  

---

## Rationale

The novel-quality AI enhancements (emotional capacity realism, dramatic irony, tension building, emotional resonance) are not just AI implementation details—they are **core gameplay mechanics** that fundamentally affect:

1. **NPC Behavior** - How characters respond based on their current emotional state
2. **Player Experience** - Decision-making with authentic human limitations
3. **Narrative Structure** - How stories build tension and maintain engagement
4. **Relationship Evolution** - How connections deepen through emotionally resonant moments
5. **Card System** - How cards evolve with tension metadata and emotional journeys

These systems touch so many aspects of gameplay that they must be canonical to ensure consistency across all future documentation and implementation.

---

## Impacted Sections

### Primary Additions (New Sections)

**New Section 16: Emotional Authenticity System**
- Emotional Capacity (0-10 scale)
- Capacity factors and limitations
- Circumstance stacking rules
- Authentic response constraints

**New Section 17: Novel-Quality Narrative Systems**
- Dramatic Irony mechanics
- Tension Injection framework (4 types)
- Memory Emotional Resonance
- Hook tracking and payoff timelines

### Modified Sections

**Section 2: Canonical Vocabulary & Scales**
- Add: Emotional Capacity (0-10 continuous scale)
- Add: Tension types (mystery_hook, partial_reveal, contradiction, stakes_escalation)
- Add: Memory resonance factors

**Section 11: AI Personality & NPC Behavior**
- Add: Emotional capacity constraints on behavior
- Add: Capacity-based response limitations
- Add: Knowledge gap mechanics (dramatic irony)

**Section 15: Canonical Constants**
- Add: Default emotional capacity (5.0)
- Add: Capacity threshold for limitations (< 5.0)
- Add: Tension injection frequency (1 in 3 for Level 1-2, 1 in 2 for Level 3-4)

---

## Proposed Changes

### NEW SECTION 16: Emotional Authenticity System

```markdown
## 16) Emotional Authenticity System

**Purpose**: Ensure characters respond within realistic human limitations, creating authentic emotional experiences rather than "perfect NPC" behaviors.

**Emotional Capacity**
- **Scale**: **0.0–10.0** (continuous, internal tracking)
- **Display**: Show as context in UI overlays when relevant: "Exhausted (Capacity 2.5/10)"
- **Default**: 5.0 (baseline human capacity)
- **Factors Affecting Capacity**:
  - Current stress level (-1 to -3 per major stressor)
  - Sleep deprivation (-0.5 to -2.0)
  - Recent trauma or crisis (-2.0 to -4.0)
  - Number of active problems (-0.5 per problem)
  - Physical exhaustion (-1.0 to -3.0)
  - Positive factors: rest, resolution, support (+0.5 to +2.0)

**Capacity Levels & Limitations**
- **0-1/10 (Crisis)**: Cannot provide any emotional support; may withdraw or apologize
- **2-4/10 (Low)**: Limited support; may try but fail, say wrong thing, or offer practical help only
- **5-7/10 (Medium)**: Moderate support; can listen and provide basic emotional processing
- **8-10/10 (High)**: Full support; can provide deep emotional processing and sustained attention

**Canonical Rule**: 
> A character at X/10 capacity can provide UP TO (X + 2)/10 level of emotional support. 
> Beyond this, responses must show authentic limitations.

**Implementation Requirements**:
- Track capacity per character per turn
- Gate dialogue options by current capacity
- Show capacity warnings in UI when mismatch exists
- Award authenticity for acknowledging limitations

**Examples**:
- Character at 2.5/10 capacity CANNOT provide 8/10 level support
- Character at 8.5/10 capacity CAN provide full emotional processing
- Character at 4/10 capacity might listen for 10 minutes then need to excuse themselves

**Circumstance Stacking**:
Multiple stressors compound:
```
Base capacity: 8.0
- Job deadline: -2.0
- Family crisis: -3.0
- Money problems: -2.0
= Effective capacity: 1.0
```

At 1.0 capacity, character can only acknowledge problem, not process it.
```

### MODIFIED SECTION 2: Vocabulary & Scales (Additions)

```markdown
**Emotional Systems** (NEW)
- **Emotional Capacity**: **0.0–10.0** continuous scale (internal tracking; show in UI context when relevant)
  - Default: 5.0 (baseline)
  - Low capacity: < 5.0 (shows limitations)
  - High capacity: ≥ 8.0 (full support available)
- **Support Level Needed**: **0.0–10.0** scale (assessed per interaction)
- **Display**: "Character Name (Capacity 2.5/10)" in UI overlays when relevant

**Narrative Tension** (NEW)
- **Tension Types**: mystery_hook | partial_reveal | contradiction | stakes_escalation
- **Hook Status**: planted | unresolved | payoff_due | resolved
- **Payoff Timeline**: 2-4 weeks | 5-8 weeks | season_end
- **Tension Score**: **0.0–1.0** (internal quality metric)

**Memory Resonance** (NEW)
- **Resonance Types**: same_emotion_different_context | opposite_emotion_growth | past_trauma_trigger | joy_sadness_contrast | growth_callback
- **Resonance Score**: **0.0–1.0** (affects memory recall priority)
```

### MODIFIED SECTION 11: AI Personality & NPC Behavior

```markdown
## 11) AI Personality & NPC Behavior

- **Stable voices**: NPCs maintain personality, goals, and memory across sessions.
- **Knowledge boundaries**: POV access is limited to what the character would plausibly know.
- **Authoring knobs**: Traits, goals, secrets, and trust thresholds are explicit dials; random drift is disallowed.

**Emotional Capacity Constraints** (NEW):
- NPCs track current emotional capacity (0-10 scale)
- Responses are CONSTRAINED by capacity:
  - Low capacity (< 5): Cannot provide full emotional support
  - Character at 2.5/10 capacity CANNOT act like 8/10 capacity
  - Must show authentic limitations: trying but failing, withdrawing, acknowledging inadequacy
- Capacity affected by: stress, exhaustion, trauma, active problems, time since rest
- Positive gameplay: Characters acknowledge limitations authentically ("I want to help, but I'm overwhelmed myself")

**Dramatic Irony Mechanics** (NEW):
- **Knowledge Gaps**: Track what player knows vs. what character knows
- **Tension Opportunities**: When knowledge gap exists, create "yelling at screen" moments
- **Capacity-Limited Perception**: Low capacity characters MORE LIKELY to misread situations
- **Player Overlays**: UI shows "(You know this is wrong, but [Character] doesn't...)"
- **Three Response Types**:
  - Tone-deaf (character acts on incomplete information)
  - Well-intentioned but misguided (tries to help incorrectly)
  - Growth choice (acknowledges limitations honestly)
```

### NEW SECTION 17: Novel-Quality Narrative Systems

```markdown
## 17) Novel-Quality Narrative Systems

**Purpose**: Create page-turner experiences that feel like literary fiction rather than typical game dialogue.

**Tension Injection Framework**
- **Frequency**: 
  - Level 1-2 relationships: 1 in 3 evolutions includes tension hook
  - Level 3-4 relationships: 1 in 2 evolutions includes tension
  - Level 5 relationships: Nearly every evolution maintains tension
  - Crisis evolutions: Always include stakes escalation

**Four Tension Types**:

1. **Mystery Hook**
   - Character mentions something but doesn't elaborate
   - Unexplained behavior change
   - Reference to unseen events/people
   - Example: "Sarah mentions someone named 'David' then changes subject"

2. **Partial Reveal**
   - Show effect without cause (or vice versa)
   - Create "information debt" - promise future explanation
   - Example: "Phone lights up: '15 missed calls from Mom'. Character goes pale."

3. **Contradiction Moment**
   - Character acts against established pattern
   - Signals major life events happening off-screen
   - Example: "Reserved Sarah suddenly takes big social risk"

4. **Stakes Escalation**
   - Add time pressure
   - Introduce consequences for inaction
   - Example: "If you don't help Sarah this week, she makes major decision alone"

**Tension Metadata**
- Track per card: tension_type, hook_description, payoff_timeline, information_debt[]
- Store as special memory type: TENSION_HOOK
- Resolution tracked: HOOK_PAYOFF memory type
- Analytics: player_curiosity_score (0-1)

**Memory Emotional Resonance**
- Prioritize memory recall based on emotional impact, not just recency
- **Five Resonance Factors** (weights):
  1. Same emotion, different context (0.8)
  2. Opposite emotion, growth opportunity (0.9)
  3. Past trauma, current trigger (0.95)
  4. Past joy, current sadness contrast (0.85)
  5. Emotional growth callback (0.7)

**Dramatic Irony System**
- **Player Knowledge**: Track secrets, witnessed events, overheard conversations
- **Character Knowledge**: Track internal struggles, hidden feelings, off-screen events
- **Knowledge Gap Score**: Quantify tension potential (0-1)
- **Tension Opportunity**: When score ≥ 0.6, use dramatic irony template
- **Irony Types**: character_oblivious_to_npc_truth | character_misinterprets_situation | capacity_limited_perception

**Quality Validation**
- Every AI generation validated against:
  - Emotional Authenticity (≥ 0.7)
  - Tension Building (≥ 0.6)
  - Dramatic Irony (≥ 0.5 when applicable)
  - Hook Effectiveness (≥ 0.6)
- Overall Novel-Quality Score: ≥ 0.7 required
- Retry with better AI model if quality insufficient
```

### MODIFIED SECTION 15: Canonical Constants

```markdown
## 15) Canonical Constants (v1.2)

- Season length options: **12 weeks (Standard)**, **24 weeks (Extended)**, **36 weeks (Epic)** (player choice at season start)
- Turns per day: **3** (Morning/Afternoon/Evening); Days per week: **7**
- Free daily Essence: **25** (subject to tiering)
- Relationship Levels: **0–5** (0=Not Met, 1-5 displayed); Trust: **0.0–1.0** (continuous)
- Level-up requirements: **Interaction count + Trust threshold** (both required)
- Pack sizes: **Standard 20–30**, **Deluxe 35–50**, **Mega 60–80**

**Emotional Capacity (NEW v1.2)**:
- Default capacity: **5.0** (baseline human)
- Low capacity threshold: **< 5.0** (shows limitations)
- High capacity threshold: **≥ 8.0** (full support available)
- Crisis capacity: **≤ 1.0** (cannot provide support)
- Support rule: Can provide up to **(capacity + 2)** level support

**Tension Injection (NEW v1.2)**:
- Level 1-2 frequency: **1 in 3** evolutions
- Level 3-4 frequency: **1 in 2** evolutions
- Level 5 frequency: **Nearly every** evolution
- Payoff timelines: **2-4 weeks** | **5-8 weeks** | **season_end**

**Novel-Quality Thresholds (NEW v1.2)**:
- Emotional Authenticity: **≥ 0.7**
- Tension Building: **≥ 0.6**
- Dramatic Irony: **≥ 0.5** (when applicable)
- Hook Effectiveness: **≥ 0.6**
- Overall Novel-Quality: **≥ 0.7**

> **v1.2 Updates:** Added emotional capacity system, tension injection framework, memory resonance, and novel-quality validation thresholds
```

---

## Backward Compatibility Notes

**Breaking Changes**: None - these are additive systems

**Affected Systems**:
1. **AI Generation**: All prompts must include emotional capacity context
2. **Card Evolution**: Must check for tension injection frequency
3. **Memory System**: Add resonance scoring to recall algorithm
4. **UI**: Add capacity overlays when showing character responses
5. **Validation**: Add novel-quality validators to pipeline

**Migration Path**:
1. Initialize all existing characters with default capacity (5.0)
2. Backfill existing cards with tension_type: "none"
3. Add resonance metadata to existing memories (calculate retroactively)
4. Update UI templates to show capacity context
5. Deploy enhanced validation pipeline

**Deprecations**: None

---

## Migration Plan

### Phase 1: Documentation (Weeks 1-2)
- ✅ AI enhancement specs complete (done)
- [ ] Update Master Truths to v1.2
- [ ] Update all gameplay docs to reference new sections
- [ ] Update card evolution templates with tension requirements
- [ ] Update relationship mechanics to include capacity

### Phase 2: Data & Training (Weeks 3-6)
- [ ] Generate emotional authenticity training data (5K examples)
- [ ] Generate tension building training data (3K examples)
- [ ] Retrain local AI model with new task heads
- [ ] Validate enhanced model performance

### Phase 3: Implementation (Weeks 7-10)
- [ ] Implement emotional capacity tracking system
- [ ] Implement tension injection logic
- [ ] Implement memory resonance scoring
- [ ] Implement dramatic irony detection
- [ ] Deploy quality-aware AI routing
- [ ] Add UI overlays for capacity context

### Phase 4: Validation & Rollout (Weeks 11-12)
- [ ] A/B test novel-quality improvements
- [ ] Monitor authenticity, tension, and engagement metrics
- [ ] Gradual rollout (5% → 10% → 25% → 50% → 100%)
- [ ] Gather player feedback
- [ ] Iterate based on metrics

---

## Updated Compliance Checklist

Add to Section 13 checklist:

```markdown
### Compliance Checklist (paste into new docs)
- [ ] Uses canonical vocab & scales (Levels 0–5; Trust 0.0–1.0; EXHAUSTED/OVERWHELMED)
- [ ] Season = 12/24/36w (player choice at season start); 3 turns/day
- [ ] Relationship Level 0 = "Not Met" (never displayed as "Level 0")
- [ ] Level-up requires BOTH interaction count AND trust threshold
- [ ] Currencies limited to Time/Energy/Money/Social Capital
- [ ] Decisive decisions pause time; copy avoids FOMO framing
- [ ] Packs classified (Standard/Deluxe/Mega) with counts
- [ ] Archive policy respected by tier
- [ ] Fusion type, inputs, prerequisites, outputs defined
- [ ] NPC personality/memory constraints respected
- [ ] **Emotional capacity constraints respected (0-10 scale)** (NEW)
- [ ] **Tension injection frequency followed (Level-appropriate)** (NEW)
- [ ] **Dramatic irony mechanics used when knowledge gaps exist** (NEW)
- [ ] **Memory resonance factors applied to recall** (NEW)
- [ ] **Novel-quality thresholds met (≥ 0.7 overall)** (NEW)
- [ ] This doc cites **Truths v1.2** at the top
```

---

## Owner & Approvals

**Owner:** AI Systems Team  
**Technical Lead:** [Your Name]  

**Required Sign-offs**:
- [ ] **Product**: ______________ (Date: ______)
- [ ] **Narrative**: ______________ (Date: ______)
- [ ] **Systems**: ______________ (Date: ______)

**Target Release:** v1.2 (following 12-week implementation)

---

## Success Metrics

**Pre-Enhancement Baseline**:
- Emotional authenticity: ~0.60
- Tension building: ~0.40
- Player engagement: "medium" 60% of time

**Post-Enhancement Targets**:
- Emotional authenticity: ≥ 0.85
- Tension building: ≥ 0.75
- Player engagement: "high"/"very_high" 60% of time
- Novel-quality overall: ≥ 0.80

**Player Experience Goals**:
- Characters feel like "real people" not NPCs
- Stories create "one more week" desire to continue
- Emotional moments feel authentic and impactful
- Generated content readable as literary fiction

---

## Related Documentation

**Primary Sources**:
- `docs/3.ai/32-prompt-engineering-principles.md` (Principle 6: Emotional Capacity)
- `docs/3.ai/33-prompt-templates-library.md` (Template 11: Dramatic Irony)
- `docs/3.ai/34-context-memory-systems.md` (Layer 6: Dramatic Irony Context)
- `docs/3.ai/35-consistency-coherence.md` (NovelQualityValidator)
- `docs/3.ai/36-local-model-training.md` (Enhanced training data & architecture)
- `docs/3.ai/37-model-deployment-optimization.md` (Quality-aware routing)

**Summary**:
- `docs/AI-NOVEL-QUALITY-ENHANCEMENTS-COMPLETE-2025-10-14.md`

---

## Rationale Summary

These systems are **core gameplay mechanics**, not AI implementation details:

1. **Emotional Capacity** affects what characters can/can't do → affects player decisions
2. **Dramatic Irony** creates unique narrative tension → affects player experience
3. **Tension Injection** drives "one more week" engagement → affects retention
4. **Memory Resonance** creates powerful emotional callbacks → affects story quality

Making these canonical ensures:
- ✅ Consistency across all future features
- ✅ Clear constraints for AI generation
- ✅ Predictable player experience
- ✅ Measurable quality standards
- ✅ Single source of truth for all teams

---

**Status:** ⏳ Awaiting Product + Narrative + Systems approval  
**Next Step:** Review and sign-off  
**Timeline:** Target v1.2 release following 12-week implementation

