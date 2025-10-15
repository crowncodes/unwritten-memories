# Master Truths v1.1 → v1.2 Changes Summary

**Release Date:** October 14, 2025  
**Change Proposal:** CP-2025-10-14-001  
**Status:** ✅ Integrated

---

## Quick Overview

**What Changed**: Added two major systems (Emotional Authenticity + Novel-Quality Narratives) and updated 5 existing sections to integrate these mechanics as canonical gameplay standards.

**Why**: These aren't AI implementation details—they're fundamental gameplay mechanics that affect how characters behave, how stories build tension, how memories work, and how players experience the game.

---

## New Sections Added

### Section 16: Emotional Authenticity System
- **Emotional Capacity scale (0-10)** with canonical display rules
- **Support constraint rule**: Character at X/10 capacity can provide (X+2)/10 support
- **4 capacity levels** with clear limitations:
  - 0-1: Crisis (cannot help)
  - 2-4: Low (limited support)
  - 5-7: Medium (moderate support)
  - 8-10: High (full support)
- **Capacity factors** table with impacts and recovery
- **Circumstance stacking** mechanics
- **UI integration** requirements (overlays, dialogue gating)

### Section 17: Novel-Quality Narrative Systems
- **4 Tension Types**: Mystery hooks, partial reveals, contradictions, stakes escalation
- **Tension injection frequency** by relationship level
- **Tension metadata** structure (JSON schema)
- **Memory emotional resonance** with 5 factors and weights (0.7-0.95)
- **Dramatic irony system** with 3 response types
- **Quality validation** thresholds (all ≥ 0.7)

---

## Sections Modified

### Section 1: Core Principles
**Added**:
- "Emotional authenticity: Characters respond within realistic human limitations; no 'perfect NPC' behaviors."

### Section 2: Canonical Vocabulary & Scales
**Added 3 new subsections**:

1. **Emotional Systems**
   - Emotional Capacity: 0.0–10.0 (default 5.0)
   - Support Level Needed: 0.0–10.0
   - Display format: "Character Name (Capacity 2.5/10)"

2. **Narrative Tension**
   - Tension Types: 4 canonical types
   - Hook Status: planted | unresolved | payoff_due | resolved
   - Payoff Timeline: 2-4 weeks | 5-8 weeks | season_end
   - Tension Score: 0.0–1.0

3. **Memory Resonance**
   - 5 Resonance Types
   - Resonance Score: 0.0–1.0

### Section 5: Narrative Structure
**Added**:
- "Tension Building (NEW v1.2): Use tension injection framework (Section 17) to maintain engagement"

### Section 6: Card System
**Added**:
- "Tension Metadata (NEW v1.2): Cards track tension_type, hook_description, payoff_timeline, information_debt"

### Section 11: AI Personality & NPC Behavior
**Added 2 new subsections**:

1. **Emotional Capacity Constraints**
   - Capacity tracking (0-10)
   - Support constraint rule
   - Authentic limitation requirements
   - Examples of capacity-appropriate responses

2. **Dramatic Irony Mechanics**
   - Knowledge gap tracking
   - Tension opportunities
   - Capacity-limited perception
   - Player UI overlays
   - 3 response types

### Section 12: UX & Copy Standards
**Added**:
- "Capacity Context (NEW v1.2): Show context when capacity affects responses"

### Section 13: Authoring Rules
**Added 3 new rules** (9-11):
- Rule 9: Capacity Constraints
- Rule 10: Tension Injection
- Rule 11: Quality Standards

### Section 15: Canonical Constants
**Added 4 new constant groups**:

1. **Emotional Capacity** (6 constants)
   - Default: 5.0
   - Thresholds: < 5.0 (low), ≥ 8.0 (high), ≤ 1.0 (crisis)
   - Support rule: capacity + 2
   - Capacity factors with ranges

2. **Tension Injection** (5 constants)
   - Level 1-2: 1 in 3
   - Level 3-4: 1 in 2
   - Level 5: Nearly every
   - Crisis: Always
   - Payoff timelines: 3 options

3. **Memory Resonance** (5 weights)
   - Same emotion: 0.8
   - Opposite emotion: 0.9
   - Past trauma: 0.95
   - Joy/sadness contrast: 0.85
   - Growth callback: 0.7

4. **Novel-Quality Thresholds** (5 thresholds)
   - Emotional Authenticity: ≥ 0.7
   - Tension Building: ≥ 0.6
   - Dramatic Irony: ≥ 0.5
   - Hook Effectiveness: ≥ 0.6
   - Overall: ≥ 0.7

### Compliance Checklist
**Added 5 new checkboxes**:
- Emotional capacity constraints (0-10 scale; support rule)
- Tension injection frequency (level-appropriate)
- Dramatic irony mechanics (when knowledge gaps exist)
- Memory resonance factors (weights 0.7-0.95)
- Novel-quality thresholds (≥ 0.7 overall)

---

## Key Numbers to Remember

| Scale/Threshold | Value | Meaning |
|----------------|-------|---------|
| **Default Emotional Capacity** | 5.0 | Baseline human |
| **Low Capacity** | < 5.0 | Shows limitations |
| **High Capacity** | ≥ 8.0 | Full support available |
| **Crisis Capacity** | ≤ 1.0 | Cannot provide support |
| **Support Rule** | capacity + 2 | Max support character can provide |
| **Tension Frequency (L1-2)** | 1 in 3 | Evolutions with hooks |
| **Tension Frequency (L3-4)** | 1 in 2 | Evolutions with hooks |
| **Highest Resonance** | 0.95 | Past trauma trigger |
| **Quality Threshold** | ≥ 0.7 | Minimum overall score |
| **Authenticity Threshold** | ≥ 0.7 | Must constrain by capacity |

---

## What This Means for Documentation

### All Future Docs Must:
1. ✅ Reference **Truths v1.2** at the top
2. ✅ Include emotional capacity in NPC behavior descriptions
3. ✅ Apply tension injection at correct frequency
4. ✅ Use memory resonance factors for recall
5. ✅ Meet novel-quality thresholds for generated content
6. ✅ Complete the 16-item compliance checklist (was 11 items)

### Examples in New Format:

**Character Description** (v1.1):
```
Sarah is a Level 3 Friend with Trust 0.62.
```

**Character Description** (v1.2):
```
Sarah is a Level 3 Friend with Trust 0.62.
Current Emotional Capacity: 2.5/10 (exhausted from work crisis)
- Can provide: Acknowledgment, basic practical help
- Cannot provide: Deep emotional processing, extended conversations
```

**Card Evolution** (v1.1):
```json
{
  "evolution_type": "relationship_growth",
  "new_memory": "We had coffee and talked about life"
}
```

**Card Evolution** (v1.2):
```json
{
  "evolution_type": "relationship_growth",
  "new_memory": "We had coffee and talked about life",
  "tension_metadata": {
    "tension_type": "mystery_hook",
    "hook_description": "Sarah mentioned someone named 'David' then changed subject",
    "payoff_timeline": "2-4 weeks",
    "player_curiosity_score": 0.85
  }
}
```

---

## Breaking Changes

**None!** All changes are additive.

### Backward Compatibility:
- Existing characters initialized with default capacity (5.0)
- Existing cards get tension_type: "none"
- Existing memories get resonance calculated retroactively
- UI can show capacity progressively (doesn't block existing features)

---

## Implementation Checklist

For teams implementing v1.2:

**Data Layer**:
- [ ] Add emotional_capacity field to character schema (default 5.0)
- [ ] Add tension_metadata to card schema
- [ ] Add resonance_score to memory schema
- [ ] Migration script for existing data

**AI Layer**:
- [ ] Update prompts with capacity constraints
- [ ] Add tension injection logic
- [ ] Implement memory resonance scoring
- [ ] Deploy quality validators

**UI Layer**:
- [ ] Capacity context overlays
- [ ] Dialogue option gating by capacity
- [ ] Tension hook indicators
- [ ] Quality score displays (internal/debug)

**Analytics**:
- [ ] Track capacity distribution
- [ ] Track tension injection frequency
- [ ] Track quality scores
- [ ] Monitor player engagement correlation

---

## Success Metrics

**Target Improvements** (from baseline):

| Metric | Baseline (v1.1) | Target (v1.2) | Status |
|--------|-----------------|---------------|--------|
| Emotional Authenticity | ~0.60 | ≥ 0.85 | ⏳ Pending training |
| Tension Building | ~0.40 | ≥ 0.75 | ⏳ Pending training |
| Player Engagement | "medium" 60% | "high" 60% | ⏳ Pending deployment |
| Novel-Quality Feel | Not measured | ≥ 0.80 | ⏳ Pending validation |

---

## Related Files

**Core Documentation**:
- `docs/master_truths_canonical_spec_v_1_2.md` (this version)
- `docs/master_truths_canonical_spec_v_1.md` (previous version - keep for reference)
- `docs/CHANGE-PROPOSAL-EMOTIONAL-AUTHENTICITY-CANON.md` (change proposal)

**AI Implementation**:
- `docs/3.ai/32-prompt-engineering-principles.md` (Principle 6)
- `docs/3.ai/33-prompt-templates-library.md` (Template 11)
- `docs/3.ai/34-context-memory-systems.md` (Layer 6)
- `docs/3.ai/35-consistency-coherence.md` (NovelQualityValidator)
- `docs/3.ai/36-local-model-training.md` (Enhanced architecture)
- `docs/3.ai/37-model-deployment-optimization.md` (Quality routing)

**Summary**:
- `docs/AI-NOVEL-QUALITY-ENHANCEMENTS-COMPLETE-2025-10-14.md`

---

## Next Steps

1. ✅ Master Truths v1.2 created
2. ⏳ Get Product + Narrative + Systems sign-off on change proposal
3. ⏳ Update all downstream docs to cite v1.2
4. ⏳ Begin 12-week implementation (training → deployment → validation)
5. ⏳ A/B test and monitor metrics

---

**Questions?** See change proposal (CP-2025-10-14-001) for full rationale and migration plan.

