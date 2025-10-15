# Unwritten: AI Documentation Index

**Last Updated:** October 14, 2025  
**Status:** ✅ Complete - Compliant with Master Truths v1.2

---

## Document Organization

This folder contains the complete AI system design for Unwritten, organized into clean, focused documents. Each document covers a specific aspect of the AI architecture without redundancy.

> **Master Truths v1.2 Compliance:** All documents now implement the **NPC Response Framework** (OCEAN → Urgency → Trust → Capacity), **Numerical Grounding** (anchor → calculate → validate), and **Novel-Quality Narrative Systems** (tension injection, memory resonance, dramatic irony).

---

## Master Truths v1.2 Key Systems

### NPC Response Framework
**Where:** Documents 30, 31, 32, 33, 34
- **OCEAN Personality** (Primary Filter): Sets baseline response tendency
- **Situational Urgency** (1x-5x Multiplier): Amplifies or dampens baseline
- **Relationship Trust** (0.5x-2x Modifier): Affects interpretation
- **Emotional Capacity** (0-10 Constraint): Caps maximum response
- **Memory Resonance** (0.7-0.95 Weights): Contextual recall priority

### Numerical Grounding System
**Where:** Documents 30, 32, 33, 37-training-data-quality-standards.md
- **Anchor:** Identify qualitative tier (NEGLIGIBLE/MINOR/MODERATE/MAJOR/SHATTERING)
- **Calculate:** Apply formula: base × personality × urgency × trust × capacity
- **Validate:** Confirm dialogue matches numerical tier

### Novel-Quality Narrative
**Where:** Documents 32, 33, 35, 37-training-data-quality-standards.md
- **Dialogue Length:** 80-250 words for important moments
- **Behavioral Grounding:** Actions must match capacity level
- **OCEAN Influence:** Personality affects response patterns
- **Tension Injection:** Setup → Escalation → Release patterns
- **Emotional Authenticity:** 0.7+ minimum score

---

## Core Documents (Read In Order)

### **30-ai-architecture-overview.md** ⭐ START HERE
**High-Level Strategy & Decisions**
- Why hybrid cloud-local architecture?
- **NPC Response Framework (v1.2)**: OCEAN → Urgency → Trust → Capacity
- **Urgency multipliers (1x-5x)** affect routing decisions
- Technology stack (Gemini Flash 2.5, Phi-3, LiteRT)
- System architecture flow
- Performance targets and constraints
- **Numerical grounding** for all impact calculations

**Read this first** to understand the overall AI strategy.

---

### **31-hybrid-cloud-local-system.md**
**System Design & Implementation**
- Hybrid system architecture
- Smart routing algorithm
- Local AI capabilities and limits
- Cloud AI integration
- iOS, Android, Flutter code examples

**Read this second** for implementation details.

---

### **32-prompt-engineering-principles.md**
**Core Concepts & Philosophy**
- Six prompt engineering principles (including Capacity Realism)
- **OCEAN → Response Framework** connection
- **Numerical grounding process** (anchor → calculate → validate)
- Emotional resonance techniques
- Memory system design (4 tiers with 0.7-0.95 resonance weights)
- Narrative coherence rules

**Read this third** to understand prompt quality and v1.2 systems.

---

### **33-prompt-templates-library.md**
**Reusable Templates & Examples**
- Template overview and conventions
- Evolution templates (Level 1→2, 3→4, Crisis)
- Context injection templates
- Complete Marcus hospital example
- Template customization guide

**Read this fourth** for practical templates.

---

### **34-context-memory-systems.md**
**Context Building & Consistency**
- Six-layer context architecture
- Memory hierarchy (trivial to defining)
- Cross-generation consistency
- Canonical facts system
- Context optimization techniques

**Read this fifth** for consistency maintenance.

---

### **35-consistency-coherence.md**
**Quality Control & Validation**
- **Eight-step validation pipeline** (including Novel-Quality Check v1.2)
- Multi-turn refinement process
- **Emotional authenticity validation** (capacity constraints)
- **Dialogue length requirements** (80-250 words)
- **Behavioral grounding checks** (actions match capacity)
- Eight edge case handlers
- Robustness pipeline

**Read this sixth** for quality assurance and v1.2 validation.

---

### **36-local-model-training.md**
**Training On-Device Models**
- Environment setup (PyTorch 2.x, LoRA)
- Data collection with Claude 3.5
- Multi-task LoRA architecture
- Training process and optimizations
- Timeline (20-25 days) and costs ($50-75)

**Read this seventh** for model training.

---

### **37-model-deployment-optimization.md**
**Model Conversion & Deployment**
- PyTorch to LiteRT conversion
- INT4/INT2 quantization
- Platform-specific optimization
- Performance validation
- Target metrics (2-3MB, 8-15ms)

**Read this eighth** for deployment.

---

### **38-latency-ux-strategies.md**
**Making AI Feel Instant**
- Seven latency hiding strategies
- Predictive pre-generation
- Conversational pacing
- Progressive disclosure
- Activity-based time compression
- Expected results (70% instant)

**Read this ninth** for UX design.

---

### **39-cost-performance-targets.md**
**Optimization & Metrics**
- Cost optimization strategies
- Cloud vs hybrid analysis ($75 vs $2-4)
- Performance benchmarks
- Monitoring and analytics
- Cost-benefit tradeoffs

**Read this tenth** for business metrics.

---

## Quick Reference

### Reading Paths by Role

**AI Engineer:**
- 00 → 30 → 31 → 36 → 37 → 32 → 33
- Focus: Implementation, training, deployment

**Prompt Engineer:**
- 00 → 32 → 33 → 34 → 35
- Focus: Writing quality prompts and maintaining consistency

**Game Designer:**
- 00 → 30 → 38 → 39
- Focus: Understanding capabilities and constraints

**UX Designer:**
- 00 → 30 → 38
- Focus: Making latency invisible to players

**Business/Product:**
- 00 → 30 → 39 → 31
- Focus: Cost, performance, architecture decisions

**Full AI System Understanding:**
- 00 → 30 → 31 → 32 → 33 → 34 → 35 → 36 → 37 → 38 → 39
- ~7,700 lines total

---

## Document Status

| Document | Purpose | Lines | Status |
|----------|---------|-------|--------|
| 00-INDEX.md | Navigation | 400 | ✅ Complete |
| 30-ai-architecture-overview.md | Strategy | 600 | ✅ Complete |
| 31-hybrid-cloud-local-system.md | Architecture | 800 | ✅ Complete |
| 32-prompt-engineering-principles.md | Principles | 700 | ✅ Complete |
| 33-prompt-templates-library.md | Templates | 1,200 | ✅ Complete |
| 34-context-memory-systems.md | Context | 600 | ✅ Complete |
| 35-consistency-coherence.md | Quality | 700 | ✅ Complete |
| 36-local-model-training.md | Training | 800 | ✅ Complete |
| 37-model-deployment-optimization.md | Deployment | 600 | ✅ Complete |
| 38-latency-ux-strategies.md | UX | 800 | ✅ Complete |
| 39-cost-performance-targets.md | Optimization | 500 | ✅ Complete |

---

## Key Numbers to Remember

**Technology Stack:**
- Primary Cloud: Gemini Flash (fast, cost-effective)
- Premium Cloud: Gemini 2.5 Pro (complex cases)
- Local Models: Phi-3-mini, Gemma-2-2b
- Frameworks: LiteRT, PyTorch 2.x, PEFT/LoRA
- Deployment: Flutter with tflite_flutter

**Performance Targets:**
- Model Size: 2-3MB (INT4 quantized)
- Inference Speed: 8-15ms
- Battery Impact: <1% per 30min session
- Memory Usage: <25MB
- Cost per Player: $2-2.50/month (with Gemini Flash 2.5/2.5 Pro)

**Architecture Decision:**
- 70-85% interactions: Local AI (instant, free)
- 15-25% interactions: Gemini Flash 2.5 (fast, $0.0014 each)
- 2-5% interactions: Gemini 2.5 Pro (quality, $0.0025 each)
- Smart routing based on importance
- Seven UX strategies to hide latency

**Training:**
- Timeline: 20-25 days with LoRA
- Cost: ~$50-75 total
- Data needed: 12,000-40,000 examples
- Tools: Claude 3.5 for synthetic data

---

## What Happened to Old Documents?

The following original documents were **reorganized** into the new structure:

**Archived (see ARCHIVE/ folder):**
- `ai_prompt_engineering.md` (2,504 lines) → Split into 30, 32, 33, 34, 35, 39
- `unwritten-training-2025.md` (954 lines) → Split into 30, 31, 36, 37
- `Local Models.md` (935 lines) → Split into 30, 31, 38, 39

**Migration Map:**
- See `AI_REORGANIZATION_PLAN.md` for complete line-by-line mapping
- All content preserved or consciously archived
- No information lost in reorganization

**Primary Source of Truth:** Documents 30-39 (this folder)

---

## Related Documentation

**For Character Personality:**
→ See `docs/1.concept/13-ai-personality-system.md`
- OCEAN model details
- Relationship dynamics
- Emotional intelligence

**For Multi-Lifetime Consistency:**
→ See `docs/1.concept/22-multi-lifetime-continuity.md`
- Context management across 3000+ weeks
- Memory compression (50:1)
- Canonical facts system

**For Card Evolution:**
→ See `docs/1.concept/12-card-evolution.md`
- Evolution triggers
- Character level progression
- Visual evolution

**For Technical Architecture:**
→ See `docs/5.architecture/tech_architecture_doc.md`
- Full system architecture
- Backend services
- Data flow

**For Monetization:**
→ See `docs/1.concept/17-monetization-model.md`
- Cost per player economics
- Premium features
- Revenue projections

---

## Common Questions

### "Which AI model should I use for X?"

**Use Local AI (Phi-3-mini) for:**
- Routine greetings and reactions (90ms)
- Ambient dialogue (60ms)
- Simple emotional responses (110ms)
- Background NPC behaviors

**Use Cloud AI (Claude/GPT-4) for:**
- Character evolutions Level 3+
- Crisis responses
- Defining moments
- Complex personality modeling

**See:** 30-ai-architecture-overview.md for decision matrix

---

### "How do I write good prompts?"

**Start with:**
- 32-prompt-engineering-principles.md (philosophy)
- 33-prompt-templates-library.md (templates)
- 34-context-memory-systems.md (context)

**Key principles:**
- Specificity over generality
- Constraint-driven creativity
- Examples drive consistency
- Small details > big drama
- Incremental not exponential

---

### "How do I hide AI latency?"

**See:** 38-latency-ux-strategies.md

**Seven strategies:**
1. Predictive pre-generation (60-70% hit rate)
2. Conversational pacing (3s feels natural)
3. Progressive disclosure (show quick, enhance later)
4. Activity-based time compression (hide in animations)
5. Batch interactions (group events)
6. Background generation pipeline (idle time)
7. Tiered response system (instant → good → great)

**Result:** 90% of interactions feel instant

---

### "What are the performance targets?"

**See:** 39-cost-performance-targets.md

**Targets:**
- Inference: 8-15ms (local), 2-5s (cloud with UX hiding)
- Battery: <0.8% per 25 conversations
- Memory: <25MB total
- Model Size: 2-3MB
- Cost: $2-4 per player/month
- Accuracy: 87%+ personality, 92%+ sentiment

---

### "How do I maintain consistency?"

**See:** 34-context-memory-systems.md and 35-consistency-coherence.md

**Key techniques:**
- Rolling summaries per character
- Character-specific style guides
- Generation chaining (reference previous)
- Canonical facts list (immutable)
- Five coherence checks before output
- Contradiction detection and resolution

---

## Contributing

When updating AI documentation:

1. ✅ Find the right document using this index
2. ✅ Maintain single-responsibility principle
3. ✅ Add cross-references to related docs
4. ✅ Include code examples with comments
5. ✅ Update this index if adding new sections
6. ✅ Test all code examples before committing

---

## Migration Notes

**Reorganization completed:** October 13, 2025

**Changes:**
- 3 large documents → 11 focused documents
- 4,393 lines → 7,700 lines (added structure/clarity)
- No content lost or duplicated
- All code examples validated
- Cross-references added throughout

**Benefits:**
- Find information in <30 seconds
- Clear reading paths by role
- No duplication
- Better maintainability
- Easier onboarding

---

## Quick Navigation Cheat Sheet

| I want to... | Go to... |
|-------------|----------|
| Understand overall strategy | 30-ai-architecture-overview.md |
| Implement hybrid routing | 31-hybrid-cloud-local-system.md |
| Write better prompts | 32-prompt-engineering-principles.md |
| Use templates | 33-prompt-templates-library.md |
| Build context system | 34-context-memory-systems.md |
| Ensure quality | 35-consistency-coherence.md |
| Train local models | 36-local-model-training.md |
| Deploy models | 37-model-deployment-optimization.md |
| Hide latency | 38-latency-ux-strategies.md |
| Optimize costs | 39-cost-performance-targets.md |

---

## Success Metrics

This reorganization is successful because:

✅ Can find any topic in <30 seconds via this INDEX  
✅ No duplicated content between documents  
✅ Each document has single, clear purpose  
✅ Cross-references are bidirectional  
✅ Code examples are tested and runnable  
✅ New team members can onboard in 2-3 hours  
✅ Each document <1,200 lines (manageable size)  
✅ Technical reviewers can navigate quickly  

---

**These 11 documents contain everything needed to understand and implement Unwritten's AI system.**

**Start with 30-ai-architecture-overview.md for the big picture! ⭐**

---

## Master Truths v1.2 Compliance Status

✅ **All AI documentation is now fully compliant with Master Truths v1.2**

**Key Additions:**
- **NPC Response Framework** integrated across all documents (30-35)
- **Urgency multipliers (1x-5x)** in routing logic (30, 31, 37, 39)
- **Numerical grounding process** in prompt engineering (32, 33)
- **Memory resonance weights (0.7-0.95)** in context systems (34)
- **Novel-quality validation** in quality control (35)
- **Emotional capacity constraints** throughout (30-35)

**Documentation Updated:** October 14, 2025  
**Adherence Assessment:** See `ADHERENCE_ASSESSMENT_REPORT.md` (if created)  
**Canonical Reference:** `../master_truths_canonical_spec_v_1_2.md`

