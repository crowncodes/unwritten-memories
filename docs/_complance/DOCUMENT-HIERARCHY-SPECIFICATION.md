# Document Hierarchy & Conflict Resolution

**Purpose:** Establish clear precedence for all Unwritten documentation  
**Status:** Canonical  
**Version:** 1.0.0  
**Last Updated:** October 14, 2025

---

## Document Hierarchy (Absolute Precedence)

```
TIER 0: CANONICAL SOURCE OF TRUTH
┌────────────────────────────────────────────────────────┐
│  master_truths_canonical_spec_v_1_2.md                │
│  ↳ Single source of truth for ALL systems             │
│  ↳ ALWAYS takes precedence                            │
│  ↳ Changes require formal approval process            │
└────────────────────────────────────────────────────────┘
                        ↓
TIER 1: CALIBRATION & GROUNDING SYSTEMS
┌────────────────────────────────────────────────────────┐
│  NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md             │
│  ↳ Required for all numerical assignments             │
│  ↳ Defines qualitative → quantitative mapping         │
│  ↳ Complements Master Truths v1.2                     │
└────────────────────────────────────────────────────────┘
                        ↓
TIER 2: DOMAIN-SPECIFIC SPECIFICATIONS
┌────────────────────────────────────────────────────────┐
│  Individual specification documents (by domain):       │
│  ├─ 1.concept/*.md (Game design concepts)             │
│  ├─ 2.gameplay/*.md (Gameplay mechanics)              │
│  ├─ 3.ai/*.md (AI architecture & training)            │
│  ├─ 4.visual/*.md (Visual systems)                    │
│  ├─ 5.architecture/*.md (Technical architecture)      │
│  ├─ 6.monetization/*.md (Business model)              │
│  └─ 7.schema/*.md (Data schemas)                      │
│                                                        │
│  Rules:                                                │
│  ↳ MUST comply with Master Truths v1.2                │
│  ↳ Can add detail not in Master Truths                │
│  ↳ CANNOT contradict Master Truths                    │
│  ↳ Must cite Master Truths version at top             │
└────────────────────────────────────────────────────────┘
                        ↓
TIER 3: IMPLEMENTATION DOCUMENTATION
┌────────────────────────────────────────────────────────┐
│  Implementation guides, code comments, READMEs         │
│  ↳ Follow specifications from Tier 2                  │
│  ↳ Must maintain consistency with Master Truths       │
│  ↳ Document deviations with explicit justification    │
└────────────────────────────────────────────────────────┘
```

---

## Conflict Resolution Protocol

### When Documents Conflict

**Priority Order:**
1. Master Truths v1.2 **ALWAYS WINS**
2. If not in Master Truths, NUMERICAL-GROUNDING guide takes precedence for numerical values
3. For domain details, most recently updated specification wins (if both compliant with Master Truths)
4. Implementation docs defer to specifications

### Resolution Process

```
STEP 1: IDENTIFY CONFLICT
├─ Compare documents side-by-side
├─ Note exact contradictions
└─ Document locations (file:line)

STEP 2: CHECK MASTER TRUTHS
├─ Does Master Truths v1.2 address this?
│   ├─ YES → Master Truths wins, update other docs
│   └─ NO → Proceed to step 3

STEP 3: ASSESS DOMAIN SPECIFICITY
├─ Is this domain-specific detail not in Master Truths?
│   ├─ YES → Most recent specification wins
│   └─ NO → Escalate for team decision

STEP 4: DOCUMENT RESOLUTION
├─ Update incorrect documents
├─ Add citation to Master Truths
├─ Log in DOCUMENTATION-UPDATE-ANALYSIS.md
└─ Run compliance validator
```

---

## Master Truths Change Process

### When to Propose a Change

Only propose changes to Master Truths when:
- ✅ Found a fundamental system design flaw
- ✅ New feature requires canonical definition
- ✅ Industry standard has changed (pricing, technology)
- ✅ Discovered contradiction within Master Truths itself

### Change Proposal Template

```markdown
# Master Truths Change Proposal

**Proposer:** [Name]  
**Date:** [YYYY-MM-DD]  
**Target Section:** [Master Truths section number]  
**Change Type:** [Addition | Modification | Clarification]

## Current State
[What Master Truths currently says]

## Proposed Change
[What you propose]

## Rationale
[Why this change is necessary]

## Impact Analysis
- Documents affected: [List]
- Code affected: [List]
- Breaking changes: [Yes/No]
- Migration effort: [Hours/Days]

## Backward Compatibility
[How to handle existing content]

## Migration Plan
1. [Step 1]
2. [Step 2]
...

## Approval Required
- [ ] Product Owner
- [ ] Narrative Lead
- [ ] Systems Designer
- [ ] Technical Lead
```

### Approval Process

**Approvers Required (ALL must approve):**
1. **Product Owner** - Business impact, player experience
2. **Narrative Lead** - Story consistency, character impact
3. **Systems Designer** - Game balance, mechanical coherence
4. **Technical Lead** - Implementation feasibility

**Timeline:**
- Proposal submission → Review within 48 hours
- Discussion period: 3-5 days
- Final decision: 1 week maximum
- Implementation: As agreed in migration plan

**Version Updates:**
- MINOR version (0.X) - Clarifications, additions that don't break existing
- MAJOR version (X.0) - Breaking changes, fundamental system updates

---

## Compliance Requirements

### Every Specification Document MUST

1. **Cite Master Truths Version**
   ```markdown
   **Compliance:** `master_truths_canonical_spec_v_1_2.md` (v1.2)
   ```

2. **Include Compliance Checklist**
   - Copy from Master Truths Section 13
   - Check all applicable items
   - Document any intentional deviations

3. **Reference Canonical Constants**
   - Use constants by name, not hardcoded values
   - Example: "Season lengths (12/24/36 weeks)" not "Season = 15 weeks"

4. **Document Deviations**
   - If intentional deviation from Master Truths
   - Must include explicit justification
   - Must propose Master Truths update

### Automated Compliance Checking

**Tool:** `scripts/master_truth_compliance_validator.py`

**Run Before Commit:**
```bash
python scripts/master_truth_compliance_validator.py --doc docs/path/to/file.md
```

**Run Full Scan:**
```bash
python scripts/master_truth_compliance_validator.py --scan-all --report docs/COMPLIANCE_REPORT.md
```

**CI/CD Integration:**
```yaml
# In .github/workflows/compliance.yml
- name: Validate Master Truth Compliance
  run: |
    python scripts/master_truth_compliance_validator.py --scan-all
    if grep -q "Critical Issues: 0" docs/COMPLIANCE_REPORT.md; then
      echo "✅ Compliance check passed"
    else
      echo "❌ Critical compliance issues found"
      exit 1
    fi
```

---

## Escalation Path

### When You're Unsure

```
LEVEL 1: Check Master Truths v1.2
├─ Search canonical spec
├─ Check changelog for recent updates
└─ Review related sections

LEVEL 2: Check Compliance Reports
├─ Review recent compliance scans
├─ Check DOCUMENTATION-UPDATE-ANALYSIS.md
└─ Look for similar resolved conflicts

LEVEL 3: Team Discussion
├─ Post in #documentation channel
├─ Tag relevant domain owners
└─ Reference specific file:line conflicts

LEVEL 4: Formal Change Proposal
├─ Use Change Proposal Template
├─ Submit to Product Owner
└─ Follow approval process
```

---

## Examples

### Example 1: Subscription Pricing Conflict

**Conflict Found:**
- Master Truths v1.2 Section 10: "Plus $14.99/mo, Ultimate $29.99/mo"
- docs/some-old-spec.md line 42: "Plus $9.99/month"

**Resolution:**
1. **Master Truths wins** - Pricing is canonical
2. Update docs/some-old-spec.md line 42 to "$14.99/month"
3. Add citation: "(Master Truths v1.2 Section 10)"
4. Run validator to confirm fix

### Example 2: Emotional State Terminology

**Conflict Found:**
- Master Truths v1.2 Section 2: "Deprecated: DRAINED → EXHAUSTED"
- docs/emotional-system.md: Uses "DRAINED" throughout

**Resolution:**
1. **Master Truths wins** - Terminology is canonical
2. Find/replace "DRAINED" with "EXHAUSTED" in docs/emotional-system.md
3. Add note: "Canonical name: EXHAUSTED (Master Truths v1.2 Section 2)"
4. Run validator to confirm

### Example 3: AI Cost Details (NOT a conflict)

**Apparent Conflict:**
- Master Truths v1.2 Section 10: "Subscriptions: Plus $14.99/mo, Ultimate $29.99/mo"
- docs/3.ai/30-ai-architecture-overview.md: "Card evolution cost: $0.00074 to generate"

**Resolution:**
1. **NOT a conflict** - Master Truths defines pricing to users
2. AI architecture doc provides implementation cost details
3. Both are correct at their respective levels
4. No changes needed

### Example 4: New Feature Needs Canonical Definition

**Situation:**
- Implementing new "Friendship Milestones" feature
- No mention in Master Truths v1.2
- Affects relationship progression

**Resolution:**
1. **Propose Master Truths addition**
2. Submit Change Proposal for Section 2 (Relationships)
3. Get approval from all stakeholders
4. Update Master Truths first
5. Then update feature specifications
6. Maintain consistency from top down

---

## Monitoring & Maintenance

### Weekly

- [ ] Review any new documentation for compliance
- [ ] Check for unresolved conflicts
- [ ] Update compliance dashboard

### Monthly

- [ ] Run full compliance scan (`--scan-all`)
- [ ] Review compliance score trends
- [ ] Address any new issues

### Quarterly

- [ ] Comprehensive documentation audit
- [ ] Review Master Truths for needed updates
- [ ] Clean up archived/deprecated docs

### Before Major Releases

- [ ] **MANDATORY** full compliance scan
- [ ] Zero critical issues required
- [ ] All major issues addressed or documented
- [ ] Compliance score ≥ 95%

---

## Contact & Ownership

**Document Owner:** Technical Lead  
**Master Truths Owner:** Product Manager + Narrative Lead  
**Compliance Tool Owner:** Systems Architecture Team

**Questions?**
- Technical conflicts → #engineering
- Design conflicts → #game-design
- Narrative conflicts → #narrative
- General → #documentation

---

## Conclusion

**The hierarchy is simple:**

1. **Master Truths v1.2 is law**
2. Specifications elaborate on Master Truths
3. Implementation follows specifications
4. Conflicts are resolved upward (Master Truths always wins)
5. Changes to Master Truths require formal process

**When in doubt:**
- Check Master Truths first
- Use compliance validator
- Ask team before deviating
- Document everything

**The goal:** Zero contradictions, 100% consistency, one source of truth.

---

**This document is itself TIER 1 (process specification) and complements Master Truths v1.2.**

