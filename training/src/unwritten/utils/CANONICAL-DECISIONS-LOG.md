# Unwritten Canonical Decisions Log

**Purpose:** Track all canonical decisions and master_truths updates to maintain consistency across documentation.

---

## Decision Log

### Decision #001: Season Length System
**Date:** October 13, 2025  
**Version:** master_truths v1.0 → v1.1  
**Status:** ✅ RESOLVED

**Issue:**
- master_truths v1.0 specified "12 weeks (Extended: 24/36)"
- 1.concept/15-progression-phases.md specified "12-100 weeks variable"
- Contradiction in how season length is determined

**Decision:**
Use **fixed player-choice season lengths: 12, 24, or 36 weeks**

**Rationale:**
1. **Content balancing:** Fixed lengths easier to balance and test
2. **Player commitment:** Clear time investment up front
3. **Memory architecture:** Simpler context management with known bounds
4. **Narrative flexibility:** Achieved through:
   - Player chooses length based on aspiration complexity
   - Content density varies (routine batching vs. granular days)
   - Early completion option if goal achieved ahead of schedule
   - Can abandon season early if goal becomes impossible

**Implementation:**
- **Standard (12 weeks):** Focused single-goal arc, 2-3 complications
- **Extended (24 weeks):** Complex multi-path arc, 4-6 complications
- **Epic (36 weeks):** Transformational saga, 6-10 complications

**Updates Made:**
- ✅ Updated master_truths v1.0 → v1.1 (clarified player choice)
- ✅ Updated 1.concept/15-progression-phases.md (removed variable length, added player choice explanation)
- ✅ Added "How Season Length Affects Gameplay" section with examples
- ✅ Added "Can You End a Season Early?" explanation

**Downstream Impact:**
- 2.gameplay/ docs will need 40-season-length-calculation.md (removed dynamic calculation, replaced with player choice + density system)
- Novel generation scales per season (12w = short story, 24w = novella, 36w = novel chapter)
- Archive display shows actual weeks played (can be less than selected if ended early)

---

### Decision #002: Relationship Level Progression (0-5)
**Date:** October 13, 2025  
**Version:** master_truths v1.0 → v1.1  
**Status:** ✅ RESOLVED

**Issue:**
- master_truths v1.0 specified "Levels 0-5" but didn't clarify what Level 0 represents
- 1.concept/13-ai-personality-system.md started at Level 1 "Stranger"
- Unclear whether there are 5 or 6 distinct levels

**Decision:**
Use **0-5 (six levels) where Level 0 = "Not Met"**

**Rationale:**
1. **Database clarity:** Level 0 useful for tracking "never met this NPC"
2. **First meeting mechanics:** Enables special "first meeting" triggers
3. **NULL handling:** Cleaner than NULL vs. 1 for unmet NPCs
4. **Progression granularity:** More nuanced relationship tracking
5. **UI consistency:** Display "Not Met" instead of "Level 0" for player clarity

**Level Breakdown:**
```
Level 0: NOT MET
├─ Never interacted with this NPC
├─ Card not yet in deck
└─ First meeting triggers → Level 1

Level 1: STRANGER (0-5 interactions, Trust 0.0-0.2)
Level 2: ACQUAINTANCE (6-15 interactions, Trust 0.2-0.4)
Level 3: FRIEND (16-30 interactions, Trust 0.4-0.6)
Level 4: CLOSE FRIEND (31-75 interactions, Trust 0.6-0.8)
Level 5: SOULMATE/BEST FRIEND (76+ interactions, Trust 0.8-1.0)
```

**Level-Up Requirements:**
- Requires BOTH minimum interaction count AND minimum trust threshold
- High trust alone insufficient (relationship needs time)
- Many interactions with low trust insufficient (relationship needs quality)

**Display Format:**
- UI: "Level 3 (Trust 0.52)"
- Never show "Level 0" (display "Not Met" instead)
- Archives track Level 0 internally
- Never show "Level 6" or "10/10" format

**Updates Made:**
- ✅ Updated master_truths v1.0 → v1.1 (detailed level progression and requirements)
- ✅ Updated 1.concept/13-ai-personality-system.md (added Level 0, detailed all 6 levels)
- ✅ Updated 1.concept/11-card-system-basics.md (clarified 0-5 display)
- ✅ Added level-up requirement formula (interactions + trust)

**Downstream Impact:**
- 2.gameplay/44-relationship-progression-spec.md will need exact thresholds
- Fusion requirements can gate on specific levels (e.g., "Level 3+ required")
- First meeting special mechanics unlocked (Level 0 → 1 transition)
- Archive statistics track "met" vs. "not met" NPCs

---

### Decision #003: Turn Structure (CONFIRMED)
**Date:** October 13, 2025  
**Version:** master_truths v1.1  
**Status:** ✅ NO CHANGES NEEDED

**Issue:**
None - all docs aligned.

**Confirmation:**
- **3 turns per day** (Morning / Afternoon / Evening)
- **7 days per week**
- All concept docs and gameplay docs consistent

**Status:**
✅ **ALIGNED** - No updates required

---

## Master Truths Version History

### v1.1 (October 13, 2025)
**Changes:**
1. Clarified season length system (12/24/36 weeks, player choice at season start)
2. Detailed relationship level progression (0-5 with Level 0 = "Not Met")
3. Added level-up requirements (interaction count + trust threshold)
4. Updated canonical constants
5. Updated compliance checklist

**Breaking Changes:**
None - v1.1 clarifies existing v1.0 intent, doesn't change systems.

**Migration Notes:**
- Docs referencing "variable 12-100 week seasons" should update to "player-choice 12/24/36 weeks"
- Docs starting relationships at "Level 1" should add "Level 0 (Not Met)" state
- All relationship level references should include interaction + trust requirements

---

### v1.0 (Initial)
**Baseline canonical specifications**

---

## Document Compliance Status

### 1.concept/ (Concept Documents)
| Document | Compliance | Last Updated | Notes |
|----------|------------|--------------|-------|
| 00-INDEX.md | ⏳ Pending | - | Update to reference v1.1 |
| 10-game-vision.md | ✅ v1.1 | 2025-10-13 | No changes needed (high-level) |
| 11-card-system-basics.md | ✅ v1.1 | 2025-10-13 | Updated Level 0-5 clarification |
| 12-card-evolution.md | ✅ v1.1 | 2025-10-13 | No changes needed |
| 13-ai-personality-system.md | ✅ v1.1 | 2025-10-13 | Updated Level 0-5, added requirements |
| 14-fusion-combinations.md | ✅ v1.1 | 2025-10-13 | No changes needed |
| 15-progression-phases.md | ✅ v1.1 | 2025-10-13 | Updated season length system |
| 16-archive-persistence.md | ⏳ Pending | - | Review season length references |
| 17-monetization-model.md | ✅ v1.1 | 2025-10-13 | No changes needed |
| 18-json-contracts.md | ⏳ Pending | - | Update schemas for Level 0 |
| 19-emotional-state-system.md | ✅ v1.1 | 2025-10-13 | No changes needed |
| 20-character-creation.md | ✅ v1.1 | 2025-10-13 | No changes needed |
| 21-turn-structure.md | ✅ v1.1 | 2025-10-13 | No changes needed (3 turns/day) |
| 22-multi-lifetime-continuity.md | ⏳ Pending | - | Review season references |

### 2.gameplay/ (Gameplay Implementation)
| Document | Compliance | Status | Notes |
|----------|------------|--------|-------|
| All current files | ⏳ Pending | To be reorganized | See REORGANIZATION-REASSESSMENT.md |

**Next Steps:**
1. Complete 2.gameplay/ reorganization per reassessment plan
2. Ensure all new gameplay docs cite master_truths v1.1
3. Add compliance checklist to all docs

---

## Future Decisions Pending

### Open Questions
None currently - all major contradictions resolved.

### Proposed Changes
None currently.

---

## Change Proposal Template

When proposing changes to master_truths, use this template:

```markdown
### Decision #XXX: [Title]
**Date:** [YYYY-MM-DD]
**Proposer:** [Name]
**Status:** 🟡 PROPOSED

**Issue:**
[Describe the problem or contradiction]

**Proposed Decision:**
[Your proposed solution]

**Rationale:**
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

**Impact Analysis:**
- master_truths changes: [List sections]
- 1.concept/ docs affected: [List files]
- 2.gameplay/ docs affected: [List files]
- Breaking changes: [Yes/No + details]

**Alternatives Considered:**
1. [Alternative 1 + why rejected]
2. [Alternative 2 + why rejected]

**Sign-Off Required:**
- [ ] Product Lead
- [ ] Narrative Lead
- [ ] Systems Lead
```

---

## Contact

**Documentation Maintainer:** [To be assigned]  
**Last Review:** October 13, 2025  
**Next Review:** [Schedule quarterly reviews]

---

**Remember:** All decisions must flow through this log and update master_truths. No "silent" changes to canonical specs.

