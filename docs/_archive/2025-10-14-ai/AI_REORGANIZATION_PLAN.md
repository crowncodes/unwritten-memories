# Unwritten AI Documentation Reorganization Plan

**Created:** October 13, 2025  
**Purpose:** Restructure AI documentation following the clean, numbered system used in `1.concept/`

---

## Current State Analysis

### Existing Documents
1. **ai_prompt_engineering.md** (2,504 lines)
   - Comprehensive prompt engineering guide
   - Mix of philosophy, templates, and implementation
   - 14 major sections covering everything from basics to edge cases
   - Very detailed but difficult to navigate

2. **unwritten-training-2025.md** (954 lines)
   - Local model training guide
   - Step-by-step implementation with 2025 frameworks
   - 6 phases: setup, data, architecture, training, conversion, deployment
   - Technical and comprehensive

3. **Local Models.md** (935 lines)
   - Feasibility analysis and latency management
   - Hybrid architecture design
   - 7 UX strategies for hiding latency
   - Mix of architecture and implementation

### Key Issues Identified

1. **Content Overlap**
   - All three docs discuss local models
   - Hybrid architecture spread across two docs
   - Cost optimization appears in multiple places

2. **Mixed Abstraction Levels**
   - Strategic decisions mixed with implementation details
   - Architecture mixed with code examples
   - Philosophy mixed with tactics

3. **Navigation Challenges**
   - No index or entry point
   - Difficult to find specific information
   - No clear reading order

4. **Duplication**
   - Local AI capabilities repeated
   - Cost analysis in multiple places
   - Latency strategies scattered

---

## Proposed New Structure

### File Organization (Following 1.concept/ Pattern)

```
docs/3.ai/
├── 00-INDEX.md                           ⭐ START HERE
├── 30-ai-architecture-overview.md        Strategic decisions
├── 31-hybrid-cloud-local-system.md       Architecture design
├── 32-prompt-engineering-principles.md   Core concepts
├── 33-prompt-templates-library.md        Reusable templates
├── 34-context-memory-systems.md          Context injection
├── 35-consistency-coherence.md           Quality maintenance
├── 36-local-model-training.md            Training guide
├── 37-model-deployment-optimization.md   Deployment & conversion
├── 38-latency-ux-strategies.md           Hiding latency
├── 39-cost-performance-targets.md        Metrics & optimization
└── ARCHIVE/
    ├── ai_prompt_engineering.md          [Original]
    ├── unwritten-training-2025.md         [Original]
    └── Local Models.md                   [Original]
```

### Numbering Rationale
- Start at **30** to distinguish from concept docs (10-22)
- Leaves room for future docs (23-29)
- Maintains logical progression
- Consistent with project standards

---

## Document Breakdown

### **00-INDEX.md** 
**Status:** NEW  
**Lines:** ~400  
**Purpose:** Navigation hub for all AI documentation

**Contents:**
- Document organization overview
- Reading order by role (engineer, designer, business)
- Quick reference for key decisions
- Cross-references to related docs
- Status table
- Key numbers to remember

**Sources:** New creation based on 1.concept/00-INDEX.md pattern

---

### **30-ai-architecture-overview.md** ⭐ START HERE
**Status:** NEW  
**Lines:** ~600  
**Purpose:** High-level strategic decisions and architecture

**Contents:**
1. **Strategic Decisions**
   - Why hybrid (not cloud-only or local-only)?
   - Model selection rationale
   - Performance vs quality tradeoffs
   
2. **System Architecture**
   - AI pipeline flow diagram
   - Component overview
   - Data flow
   
3. **Technology Stack**
   - Primary models: Claude Sonnet, GPT-4
   - Local models: Phi-3-mini, Gemma
   - Frameworks: LiteRT, PyTorch 2.x
   
4. **Key Constraints**
   - Performance targets (8-15ms inference)
   - Cost targets ($2-4 per player/month)
   - Battery targets (<1% per 30min)
   - Model size (<3MB)
   
5. **Decision Matrix**
   - When to use local vs cloud
   - Importance assessment algorithm
   - Routing logic

**Sources:**
- Local Models.md: Lines 1-36, 743-799
- ai_prompt_engineering.md: Lines 21-60
- unwritten-training-2025.md: Lines 1-27

**Key Extracts:**
```
FROM Local Models.md:
- Current State of On-Device AI (lines 8-36)
- Recommended Architecture (lines 743-799)

FROM ai_prompt_engineering.md:
- System Architecture Overview (lines 21-60)

FROM unwritten-training-2025.md:
- What's New in 2025 (lines 10-27)
```

---

### **31-hybrid-cloud-local-system.md**
**Status:** NEW  
**Lines:** ~800  
**Purpose:** Detailed hybrid architecture design

**Contents:**
1. **Hybrid System Design**
   - Smart routing algorithm
   - Decision tree flowchart
   - Category breakdown (routine/important/crisis)
   
2. **Local AI Capabilities**
   - What works on-device
   - What requires cloud
   - Performance benchmarks
   
3. **Cloud AI Integration**
   - API setup and failover
   - Rate limiting strategies
   - Caching architecture
   
4. **Communication Protocol**
   - Request/response format
   - Batching strategy
   - Error handling
   
5. **Implementation Examples**
   - iOS/Swift code samples
   - Android/Kotlin code samples
   - Flutter integration

**Sources:**
- Local Models.md: Lines 37-248, 800-896
- unwritten-training-2025.md: Lines 695-866

**Key Extracts:**
```
FROM Local Models.md:
- Hybrid Architecture: Best of Both Worlds (lines 37-130)
- Local AI Implementation (lines 133-248)
- Performance Benchmarks (lines 800-833)
- Implementation Plan (lines 862-896)

FROM unwritten-training-2025.md:
- Flutter Integration (lines 695-866)
```

---

### **32-prompt-engineering-principles.md**
**Status:** NEW  
**Lines:** ~700  
**Purpose:** Core prompt engineering philosophy and techniques

**Contents:**
1. **Prompt Engineering Philosophy**
   - Specificity over generality
   - Constraint-driven creativity
   - Examples drive consistency
   - Emotional authenticity
   - Incremental evolution
   
2. **OCEAN Personality Modeling**
   - Translating scores to behavior
   - Dialogue generation by personality
   - Behavioral consistency
   
3. **Emotional Resonance Engineering**
   - Creating emotional impact
   - Specificity creates emotion
   - Small details > big drama
   - Six resonance techniques
   
4. **Memory System Design**
   - Hierarchical memory tiers (1-4)
   - Memory writing guidelines
   - Sensory grounding
   - Significance assessment
   
5. **Narrative Coherence Rules**
   - Five coherence checks
   - Contradiction handling
   - Consistency scoring

**Sources:**
- ai_prompt_engineering.md: Lines 63-99, 669-1253

**Key Extracts:**
```
FROM ai_prompt_engineering.md:
- Prompt Engineering Philosophy (lines 63-99)
- Personality Modeling Prompts (lines 669-823)
- Memory System Prompts (lines 827-966)
- Emotional Resonance Engineering (lines 970-1088)
- Narrative Coherence Rules (lines 1092-1253)
```

---

### **33-prompt-templates-library.md**
**Status:** NEW  
**Lines:** ~1,200  
**Purpose:** Complete library of reusable prompt templates

**Contents:**
1. **Template Overview**
   - Template naming conventions
   - Variable substitution system
   - Usage guidelines
   
2. **Evolution Templates**
   - Template 1: First Evolution (Level 1→2)
   - Template 2: Deep Relationship (Level 3→4)
   - Template 3: Crisis Response
   - Template 4: Romantic Evolution
   
3. **Context Injection Templates**
   - Comprehensive context format
   - Layer-by-layer breakdown
   - Example filled templates
   
4. **Complete Examples**
   - Full evolution prompt (Marcus hospital scene)
   - Romantic evolution example
   - Crisis with resolution
   
5. **Template Customization**
   - How to adapt templates
   - Variable lists
   - Common modifications

**Sources:**
- ai_prompt_engineering.md: Lines 102-518, 522-665, 1542-1758

**Key Extracts:**
```
FROM ai_prompt_engineering.md:
- Base Prompt Templates (lines 102-518)
- Context Injection System (lines 522-665)
- Complete Prompt Examples (lines 1542-1758)
```

---

### **34-context-memory-systems.md**
**Status:** NEW  
**Lines:** ~600  
**Purpose:** How to build and maintain context across generations

**Contents:**
1. **Context Building Architecture**
   - Six context layers
   - Context injection pipeline
   - Context compression strategies
   
2. **Memory Hierarchy**
   - Four memory tiers
   - Tier selection criteria
   - Memory fading system
   
3. **Cross-Generation Consistency**
   - Rolling summary technique
   - Character-specific style guides
   - Generation chaining
   - Contradiction detection
   
4. **Canonical Facts System**
   - Immutable character facts
   - Fact verification
   - Graceful retconning
   
5. **Context Optimization**
   - Context token budget
   - Prioritization algorithm
   - Compression techniques

**Sources:**
- ai_prompt_engineering.md: Lines 522-665, 827-966, 1257-1439

**Key Extracts:**
```
FROM ai_prompt_engineering.md:
- Context Injection System (lines 522-665)
- Memory System Prompts (lines 827-966)
- Consistency Maintenance (lines 1257-1439)
```

---

### **35-consistency-coherence.md**
**Status:** NEW  
**Lines:** ~700  
**Purpose:** Maintaining quality and consistency across thousands of generations

**Contents:**
1. **Coherence Check System**
   - Five coherence checks
   - Automated validation
   - Scoring algorithm
   
2. **Multi-Turn Refinement**
   - Draft → Critique → Refine → Polish
   - When to use multi-turn
   - Example refinement process
   
3. **Quality Control Pipeline**
   - Seven validation checks
   - Post-generation validation
   - Quality tiers (0.90+ to <0.65)
   
4. **Edge Case Handling**
   - Inappropriate content filtering
   - Mary Sue prevention
   - Trauma dump pacing
   - Cultural sensitivity
   - API failure handling
   - Player exploitation detection
   
5. **Robustness System**
   - Comprehensive validation pipeline
   - Retry logic
   - Fallback content generation

**Sources:**
- ai_prompt_engineering.md: Lines 1092-1253, 1443-1537, 1762-1889, 2096-2480

**Key Extracts:**
```
FROM ai_prompt_engineering.md:
- Narrative Coherence Rules (lines 1092-1253)
- Multi-Turn Refinement (lines 1443-1537)
- Quality Control & Validation (lines 1762-1889)
- Edge Case Handling (lines 2096-2480)
```

---

### **36-local-model-training.md**
**Status:** NEW  
**Lines:** ~800  
**Purpose:** Step-by-step guide to training on-device models

**Contents:**
1. **Environment Setup**
   - Development environment
   - Hardware requirements
   - Cloud alternatives
   - 2025 framework updates
   
2. **Data Collection & Preparation**
   - Data requirements by task
   - Synthetic data generation with Claude
   - Data validation and quality control
   - Dataset creation
   
3. **Model Architecture with LoRA**
   - Base model selection (Gemma-2-2b, Phi-2)
   - Multi-task LoRA design
   - Parameter-efficient training
   - Architecture code examples
   
4. **Training Process**
   - PyTorch 2.x optimizations
   - Quantization-aware training (QAT)
   - Multi-task training loop
   - Progress monitoring
   
5. **Training Timeline & Costs**
   - Week-by-week breakdown
   - Expected results
   - Cost estimates (~$50-75 total)

**Sources:**
- unwritten-training-2025.md: Lines 28-578

**Key Extracts:**
```
FROM unwritten-training-2025.md:
- Phase 1: Environment Setup (lines 28-65)
- Phase 2: Data Collection (lines 68-191)
- Phase 3: Model Architecture with LoRA (lines 194-328)
- Phase 4: Training with Modern Optimizations (lines 331-577)
```

---

### **37-model-deployment-optimization.md**
**Status:** NEW  
**Lines:** ~600  
**Purpose:** Converting, optimizing, and deploying models

**Contents:**
1. **Model Conversion**
   - PyTorch to LiteRT conversion
   - AI Edge Torch usage
   - ONNX alternative path
   
2. **Advanced Quantization**
   - INT4/INT2 quantization
   - AI Edge Quantizer
   - Post-training quantization
   - Quality vs size tradeoffs
   
3. **Platform-Specific Optimization**
   - iOS (CoreML, Metal)
   - Android (NNAPI, GPU delegate)
   - Flutter integration code
   
4. **Performance Validation**
   - Inference speed testing
   - Memory profiling
   - Battery impact measurement
   - Performance monitoring system
   
5. **Target Metrics**
   - Model size: 2-3MB
   - Inference: 8-15ms
   - Battery: <0.8% per 25 conversations
   - Accuracy benchmarks

**Sources:**
- unwritten-training-2025.md: Lines 580-696, 869-954

**Key Extracts:**
```
FROM unwritten-training-2025.md:
- Phase 5: Model Conversion & Compression (lines 580-693)
- Expected Results & Success Metrics (lines 869-898)
- Troubleshooting Guide (lines 911-940)
```

---

### **38-latency-ux-strategies.md**
**Status:** NEW  
**Lines:** ~800  
**Purpose:** UX techniques to make AI latency invisible

**Contents:**
1. **Latency Hiding Philosophy**
   - Why latency matters
   - Perceived vs actual latency
   - Player expectation management
   
2. **Seven Core Strategies**
   - Strategy 1: Predictive Pre-Generation
   - Strategy 2: Conversational Pacing
   - Strategy 3: Progressive Disclosure
   - Strategy 4: Activity-Based Time Compression
   - Strategy 5: Batch Interactions
   - Strategy 6: Background Generation Pipeline
   - Strategy 7: Tiered Response System
   
3. **Implementation Patterns**
   - Pre-generation triggers
   - Typing indicators and timing
   - Animation pairing
   - Cache hit rate optimization
   
4. **UX Best Practices**
   - Visual feedback design
   - Loading state UX
   - Error handling
   - Offline mode
   
5. **Expected Results**
   - 70% instant (pre-generated)
   - 25% fast (feels natural)
   - 5% noticeable (but justified)

**Sources:**
- Local Models.md: Lines 249-741

**Key Extracts:**
```
FROM Local Models.md:
- Strategy 1: Predictive Pre-Generation (lines 252-316)
- Strategy 2: Conversational Pacing (lines 319-382)
- Strategy 3: Progressive Disclosure (lines 385-442)
- Strategy 4: Activity-Based Time Compression (lines 445-510)
- Strategy 5: Batch Interactions (lines 513-588)
- Strategy 6: Background Generation Pipeline (lines 591-673)
- Strategy 7: Tiered Response System (lines 676-738)
```

---

### **39-cost-performance-targets.md**
**Status:** NEW  
**Lines:** ~500  
**Purpose:** Cost optimization and performance benchmarks

**Contents:**
1. **Cost Optimization Strategies**
   - Tiered generation quality
   - Smart caching system
   - Batch processing
   - Progressive enhancement
   - Local fallback prioritization
   
2. **Cost Analysis**
   - Cloud-only: $75-150/player
   - Smart hybrid: $5-13/player
   - Optimized hybrid: $2-4/player
   - Player-funded premium option
   
3. **Performance Targets**
   - Model quality metrics
   - Inference speed requirements
   - Battery consumption limits
   - Memory usage caps
   
4. **Cost-Benefit Tradeoffs**
   - Quality vs cost
   - Speed vs accuracy
   - Local vs cloud decision matrix
   
5. **Monitoring & Analytics**
   - Cost tracking dashboard
   - Performance monitoring
   - A/B testing framework
   - Player satisfaction metrics

**Sources:**
- ai_prompt_engineering.md: Lines 1893-2092
- Local Models.md: Lines 834-861

**Key Extracts:**
```
FROM ai_prompt_engineering.md:
- Cost Optimization Strategies (lines 1893-2092)

FROM Local Models.md:
- Cost Analysis (lines 834-861)
```

---

## Migration Plan

### Phase 1: Create New Structure (Days 1-2)
- [ ] Create 00-INDEX.md
- [ ] Create placeholder files for 30-39
- [ ] Set up ARCHIVE folder
- [ ] Update folder README

### Phase 2: Extract & Write Documents (Days 3-10)
- [ ] Write 30-ai-architecture-overview.md
- [ ] Write 31-hybrid-cloud-local-system.md
- [ ] Write 32-prompt-engineering-principles.md
- [ ] Write 33-prompt-templates-library.md
- [ ] Write 34-context-memory-systems.md
- [ ] Write 35-consistency-coherence.md
- [ ] Write 36-local-model-training.md
- [ ] Write 37-model-deployment-optimization.md
- [ ] Write 38-latency-ux-strategies.md
- [ ] Write 39-cost-performance-targets.md

### Phase 3: Quality Control (Days 11-12)
- [ ] Cross-reference all documents
- [ ] Verify no duplicate content
- [ ] Check all code examples
- [ ] Validate all numbers/metrics
- [ ] Update index with accurate metadata

### Phase 4: Archive & Cleanup (Day 13)
- [ ] Move original docs to ARCHIVE/
- [ ] Update all cross-references in other folders
- [ ] Update project README
- [ ] Create migration notes

---

## Content Mapping Table

| Original Document | Lines | Target Document | Priority |
|-------------------|-------|-----------------|----------|
| **ai_prompt_engineering.md** | | | |
| System Architecture | 21-60 | 30-ai-architecture-overview.md | P0 |
| Philosophy | 63-99 | 32-prompt-engineering-principles.md | P0 |
| Base Templates | 102-518 | 33-prompt-templates-library.md | P0 |
| Context Injection | 522-665 | 34-context-memory-systems.md | P0 |
| Personality Modeling | 669-823 | 32-prompt-engineering-principles.md | P0 |
| Memory System | 827-966 | 34-context-memory-systems.md | P0 |
| Emotional Resonance | 970-1088 | 32-prompt-engineering-principles.md | P0 |
| Coherence Rules | 1092-1253 | 35-consistency-coherence.md | P0 |
| Consistency Maintenance | 1257-1439 | 34-context-memory-systems.md | P0 |
| Multi-Turn Refinement | 1443-1537 | 35-consistency-coherence.md | P1 |
| Complete Examples | 1542-1758 | 33-prompt-templates-library.md | P0 |
| Quality Control | 1762-1889 | 35-consistency-coherence.md | P0 |
| Cost Optimization | 1893-2092 | 39-cost-performance-targets.md | P1 |
| Edge Cases | 2096-2480 | 35-consistency-coherence.md | P1 |
| **unwritten-training-2025.md** | | | |
| What's New 2025 | 10-27 | 30-ai-architecture-overview.md | P0 |
| Environment Setup | 28-65 | 36-local-model-training.md | P0 |
| Data Collection | 68-191 | 36-local-model-training.md | P0 |
| Model Architecture | 194-328 | 36-local-model-training.md | P0 |
| Training Process | 331-577 | 36-local-model-training.md | P0 |
| Conversion | 580-693 | 37-model-deployment-optimization.md | P0 |
| Flutter Integration | 695-866 | 31-hybrid-cloud-local-system.md | P0 |
| Expected Results | 869-898 | 37-model-deployment-optimization.md | P1 |
| Troubleshooting | 911-940 | 37-model-deployment-optimization.md | P2 |
| **Local Models.md** | | | |
| Current State | 8-36 | 30-ai-architecture-overview.md | P0 |
| Hybrid Architecture | 37-130 | 31-hybrid-cloud-local-system.md | P0 |
| Local Implementation | 133-248 | 31-hybrid-cloud-local-system.md | P0 |
| Predictive Pre-Gen | 252-316 | 38-latency-ux-strategies.md | P0 |
| Conversational Pacing | 319-382 | 38-latency-ux-strategies.md | P0 |
| Progressive Disclosure | 385-442 | 38-latency-ux-strategies.md | P0 |
| Activity Compression | 445-510 | 38-latency-ux-strategies.md | P0 |
| Batch Interactions | 513-588 | 38-latency-ux-strategies.md | P1 |
| Background Pipeline | 591-673 | 38-latency-ux-strategies.md | P1 |
| Tiered Response | 676-738 | 38-latency-ux-strategies.md | P1 |
| Recommended Arch | 743-799 | 30-ai-architecture-overview.md | P0 |
| Performance Benchmarks | 800-833 | 31-hybrid-cloud-local-system.md | P1 |
| Cost Analysis | 834-861 | 39-cost-performance-targets.md | P1 |
| Implementation Plan | 862-896 | 31-hybrid-cloud-local-system.md | P2 |

**Priority Legend:**
- P0: Critical content, must be in new docs
- P1: Important content, should be in new docs
- P2: Nice-to-have, can be summarized or linked

---

## Style Guidelines

Following the 1.concept/ pattern:

### Structure
- Start with clear "What is this?" section
- Use hierarchical headings (##, ###, ####)
- Include code examples in fenced blocks
- Use tables for comparisons
- Include diagrams in ASCII/Markdown

### Writing Style
- Direct, technical, no fluff
- Use bullet points liberally
- Include examples for complex concepts
- Cross-reference other docs with → arrows
- Keep sentences concise

### Code Examples
```python
# Always include:
# 1. Language identifier
# 2. Brief comment explaining purpose
# 3. Realistic, runnable code
# 4. Expected output as comments
```

### Formatting
- **Bold** for emphasis
- `code` for technical terms
- ✓ and ✗ for good/bad examples
- → for cross-references
- ⭐ for start here markers

---

## Cross-References to Add

### From Other Folders TO AI Docs

**From 1.concept/:**
- 12-card-evolution.md → Link to 30-ai-architecture-overview.md
- 13-ai-personality-system.md → Link to 32-prompt-engineering-principles.md
- 22-multi-lifetime-continuity.md → Link to 34-context-memory-systems.md

**From 5.architecture/:**
- tech_architecture_doc.md → Link to 31-hybrid-cloud-local-system.md
- tech_architecture_doc.md → Link to 37-model-deployment-optimization.md

### From AI Docs TO Other Folders

**To 1.concept/:**
- 30 → 13-ai-personality-system.md (OCEAN model)
- 32 → 13-ai-personality-system.md (personality behavior)
- 34 → 22-multi-lifetime-continuity.md (memory compression)

**To 6.monetization/:**
- 39 → 17-monetization-model.md (cost per player)

---

## Success Metrics

The reorganization will be considered successful when:

- [ ] All content from original 3 docs is preserved or consciously archived
- [ ] No duplication across new documents
- [ ] Each document has single, clear purpose
- [ ] Index provides clear navigation
- [ ] Reading order is logical for all audiences
- [ ] Code examples are tested and runnable
- [ ] Cross-references are bidirectional
- [ ] Document length is manageable (<1000 lines each)
- [ ] Technical reviewers can find information quickly
- [ ] New team members can onboard using just the index

---

## Questions to Resolve

1. **Numbering Convention:** Should we use 30-39 or start at a different number?
   - Recommendation: 30-39 (leaves room, clear distinction from concept)

2. **Archive Strategy:** Keep originals in ARCHIVE/ or delete after migration?
   - Recommendation: Keep in ARCHIVE/ for 6 months, then remove

3. **Code Example Testing:** Should all code be tested before including?
   - Recommendation: Yes for critical paths, annotate untested examples

4. **Version Control:** Track changes to each doc separately?
   - Recommendation: Use git history, update "Last Modified" in each doc

---

## Timeline

**Total Estimated Time:** 13 days (assuming dedicated work)

**Week 1 (Days 1-5):**
- Day 1: Create structure, index, placeholders
- Day 2-3: Write docs 30-32 (architecture & principles)
- Day 4-5: Write docs 33-34 (templates & context)

**Week 2 (Days 6-10):**
- Day 6-7: Write docs 35-36 (consistency & training)
- Day 8-9: Write docs 37-39 (deployment, UX, costs)
- Day 10: Quality control

**Week 3 (Days 11-13):**
- Day 11-12: Cross-referencing & validation
- Day 13: Archive, cleanup, documentation updates

---

## Next Steps

1. Review and approve this plan
2. Set up new file structure
3. Begin Phase 1: Create skeleton
4. Proceed with content extraction and writing

---

**This plan transforms 4,393 lines of dense documentation into 10 focused, navigable documents totaling ~7,000 lines with clear structure and purpose.**

