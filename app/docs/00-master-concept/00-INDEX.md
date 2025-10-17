# Master Concept Documentation - Index

**Document Collection**: Unwritten V2 Master Concepts  
**Last Updated**: October 16, 2025  
**Authority Level**: Canonical Source of Truth

---

## Purpose of This Collection

This folder contains the **definitive synthesis** of Unwritten's V2 design principles, extracted from the comprehensive audit and foundational concepts discussions.

These documents serve as the **primary reference** for all subsequent design and development work, resolving contradictions from V1 documentation and establishing a cohesive vision.

**Use this collection:**
- ✅ As the source of truth for core design decisions
- ✅ To understand the "why" behind every system
- ✅ To maintain design consistency across development
- ✅ To onboard new team members to the vision

---

## Document Structure

### ⚠️ [DESIGN-PHILOSOPHY-CRITICAL.md](./DESIGN-PHILOSOPHY-CRITICAL.md)
**MANDATORY READ - Anti-Gamification Mandate**

**What's Inside:**
- The core problem: numerical gates destroy authenticity
- What we're building vs. what we're NOT building
- The Golden Rule: "If you can write a walkthrough, you've failed"
- Real-world scenarios the system must model
- AI assessment framework (personality, emotional state, quality, context)
- Code review checklist for all progression systems

**Read This First If:**
- You're implementing ANY progression system
- You're tempted to add numerical thresholds
- You need to understand the foundational philosophy

**Key Takeaway:**
> "In real life, do two people become friends after exactly 8 conversations? No. They become friends when personalities click, both are emotionally available, they share meaningful experiences, and timing is right. Sometimes that's 2 conversations. Sometimes it's never."

---

### 🎯 [01-vision-and-goals.md](./01-vision-and-goals.md)
**Core Vision & Design Principles**

**What's Inside:**
- The central promise: "A Life Remembered"
- Design pillars (Emotional Authenticity, Emergent Storytelling, Memory as Progression)
- Target experience qualities (Novel-Quality Output, Infinite Replayability, Psychological Depth)
- The three pillars of authenticity
- What Unwritten is NOT
- Success metrics and competitive differentiation
- Long-term vision and expansion strategy

**Read This First If:**
- You need to understand the big picture
- You're making a design decision and need to check alignment
- You're explaining Unwritten's unique value to others

**Key Takeaway:**
> "Cards are memories. Stories are emergent. Every life tells a story worth remembering."

---

### 🃏 [02-card-system-architecture.md](./02-card-system-architecture.md)
**Template Philosophy & Card Types**

**What's Inside:**
- The Master Template paradigm shift (templates vs. static cards)
- The seven-tier structure (Foundation, Quest, Routine, Action, Catalyst, System, Living World)
- The three card types (Action, Situation, State)
- Master template structure and JSON schema
- Card filtering & pool management
- Card evolution system (Generic → Personalized → Cherished)
- Card fusion mechanics
- The Archive as permanent memory
- Critical design rules

**Read This First If:**
- You're implementing card mechanics
- You need to understand how templates instantiate
- You're designing new card content
- You're building the card draw/filtering system

**Key Takeaway:**
> "300 templates × infinite contexts = infinite unique stories. Evolution is earned, not grinded."

---

### 🧠 [03-psychological-engine.md](./03-psychological-engine.md)
**Emotional Capacity & Personality System**

**What's Inside:**
- The dual resource system (Energy vs. Emotional Capacity)
- Personality as perceptual filter (OCEAN model integration)
- Capacity-limited perception (empathy gates)
- The "Capacity + 2" rule for NPC support
- Personality modifiers on all actions
- State Cards as persistent conditions
- The Perception → Action → Consequence loop
- Critical design rules for authenticity

**Read This First If:**
- You're implementing character psychology systems
- You need to understand how personality shapes gameplay
- You're designing difficulty curves
- You're creating NPC interaction mechanics

**Key Takeaway:**
> "Your Emotional Capacity determines what you can perceive and how you can respond. NPCs have limits too."

---

### ⏱️ [04-gameplay-loop.md](./04-gameplay-loop.md)
**Time, Energy, and Flow Mechanics**

**What's Inside:**
- Fluid time progression (continuous timeline, not phases)
- Flexible energy system with debt mechanics
- Energy collapse events (context-aware consequences)
- Adaptive granularity (AI decides zoom vs. montage)
- Contextual time-of-day filtering
- The day-to-day gameplay rhythm
- The week-to-week and season-to-season rhythm
- Long-duration activity handling
- The 7-card hand management system
- Example: Full day walkthrough

**Read This First If:**
- You're implementing the core gameplay loop
- You need to understand time and resource management
- You're designing UI for daily flow
- You're building the turn/phase system

**Key Takeaway:**
> "Days feel like days. Time flows naturally. Energy constrains but doesn't stop you. The collapse is narrative, not failure."

---

### 🎭 [05-story-weaver-ai.md](./05-story-weaver-ai.md)
**The Writers Room Model**

**What's Inside:**
- The Writers Room architecture (6 specialized flows)
- The Four Specialists (Pacing, Narrative Arc, Character State, The Critic)
- The Narrative Director (synthesizer who resolves conflicts)
- Premium "Director's Cut" iterative review loop
- The Narrative Analyst (post-event metadata enrichment)
- Memory Resonance system powered by Archive queries
- How conflicting recommendations create better stories
- Critical design rules for AI storytelling

**Read This First If:**
- You're implementing the Story Weaver AI
- You need to understand narrative generation logic
- You're building GenKit flows
- You're working on event triggers and pacing

**Key Takeaway:**
> "Great stories come from creative conflict. Multiple specialists debate, the Director synthesizes, and the result feels authored, not generated."

---

### 📈 [06-growth-and-progression.md](./06-growth-and-progression.md)
**Evolution & Relationship Systems**

**What's Inside:**
- Card evolution (Generic → Personalized → Cherished)
- Journey-based relationship progression (quantity + quality required)
- NPC Emotional Capacity and the "Capacity + 2" rule for support
- Skill progression (0-10 mastery system)
- Skill decay and "rust" mechanics
- Items as tools and memories
- Perks as behavioral rewards
- Critical design rules (no grinding works, evolution is transformative)

**Read This First If:**
- You're implementing progression systems
- You need to understand how cards evolve
- You're designing relationship mechanics
- You're building skill or perk systems

**Key Takeaway:**
> "Progression is earned through meaningful moments, not repetition. NPCs are not vending machines—they have limits and needs."

---

### 🗺️ [07-genesis-plan.md](./07-genesis-plan.md)
**Phased Development Blueprint**

**What's Inside:**
- The Master Template philosophy (why templates, not cards)
- The five-phase build approach:
  1. Life Directions (The "Why")
  2. Aspirations & Activities (The "What" & "How")
  3. Living World (The "Who" & "Where")
  4. Systems & Progression (The "Rules of Growth")
  5. Narrative Catalysts (The "Unexpected")
- Detailed design process for each phase
- Production priority matrix (MVP → Full Base Set)
- Template documentation standard (JSON schema)

**Read This First If:**
- You're planning content creation roadmap
- You need to understand build order dependencies
- You're creating new Master Templates
- You're scoping MVP vs. full release

**Key Takeaway:**
> "Build in logical phases that mirror how a life unfolds. Start with identity, then goals, then world, then systems, then surprise."

---

### 📊 [08-template-spec.md](./08-template-spec.md)
**Master Template Specification V2**

**What's Inside:**
- Three-layer architecture (DNA → Template → Instance)
- Complete Master Template JSON schema
- Anti-gamification enforcement patterns
- CFP optimization strategies
- Instantiation rules and tier selection
- Cost structures with personality modifiers
- Outcome spectrums (not binary success/failure)
- Evolution system with qualitative triggers
- Fusion potential and symbolic tags
- Template design checklist and validation

**Read This First If:**
- You're creating new Master Templates
- You need the JSON schema structure
- You're implementing template generation
- You're validating anti-gamification compliance

**Key Takeaway:**
> "Master Templates are design artifacts that generate infinite unique instances through contextual instantiation—not static cards."

---

### ⏱️ [09-turn-structure.md](./09-turn-structure.md)
**Turn Structure V2: Just-in-Time Card Generation**

**What's Inside:**
- Contextually Filtered Pool (CFP) architecture
- Incremental CFP update optimization
- The 7-card hand composition strategy
- Predictive pre-fetching to mask Tier 2 latency
- Batch generation optimization (3-4 cards per EWR call)
- Fluid time progression mechanics
- Time boundaries (end of day/week/season)
- Multi-day fast-forward handling
- The Narrative Interlude (embracing Tier 3 latency)
- State Cards as parallel system
- Asynchronous art generation pipeline
- Complete turn walkthrough example

**Read This First If:**
- You're implementing the core gameplay loop
- You need to understand CFP recalculation
- You're optimizing generation latency
- You're building the pre-fetch system

**Key Takeaway:**
> "Just-in-Time generation with predictive pre-fetching creates seamless gameplay where every card is contextually relevant and narratively unique."

---

### ✅ [10-validating-template-design.md](./10-validating-template-design.md)
**Validating Template Design: Quality Assurance Framework**

**What's Inside:**
- Anti-gamification audit checklist and automated checker
- CFP balance validation and stale hand detection
- Narrative quality scoring framework
- Evolution integrity testing (Grinder/Natural/Incompatibility tests)
- Performance and cost validation
- Production readiness comprehensive checklist
- Internal tooling specifications (Template Editor, CFP Visualizer, Evolution Simulator, Quality Dashboard)
- Common failure modes and fixes
- Continuous monitoring post-launch

**Read This First If:**
- You're validating a new template before implementation
- You need to ensure anti-gamification compliance
- You're building internal design tools
- You're troubleshooting template issues

**Key Takeaway:**
> "Rigorous validation ensures templates deliver authentic, emergent stories that feel earned and impossible to game."

---

## Reading Paths

### 🚀 For New Team Members (Complete Onboarding)

**Read in this order:**

1. **DESIGN-PHILOSOPHY-CRITICAL.md** → Understand what we're NOT building (MANDATORY)
2. **01-vision-and-goals.md** → Understand the "why"
3. **02-card-system-architecture.md** → Learn the core mechanic
4. **03-psychological-engine.md** → Grasp what makes it authentic
5. **04-gameplay-loop.md** → See how a day flows
6. **05-story-weaver-ai.md** → Understand how stories emerge
7. **06-growth-and-progression.md** → Learn how characters grow
8. **07-genesis-plan.md** → See the build roadmap
9. **08-template-spec.md** → Master Template structure (NEW)
10. **09-turn-structure.md** → Just-in-Time generation system (NEW)
11. **10-validating-template-design.md** → Quality assurance framework (NEW)

**Time Investment:** ~7-9 hours for deep read  
**Result:** Complete understanding of Unwritten's design vision, anti-gamification mandate, and implementation architecture

---

### 🎨 For Game Designers (System Focus)

**Priority reading:**

1. **DESIGN-PHILOSOPHY-CRITICAL.md** → Anti-gamification mandate (MANDATORY)
2. **02-card-system-architecture.md** → Core mechanic
3. **08-template-spec.md** → Master Template design (NEW)
4. **03-psychological-engine.md** → Character systems
5. **06-growth-and-progression.md** → Progression mechanics
6. **10-validating-template-design.md** → Validation framework (NEW)

**Skim:** 01-vision, 04-gameplay-loop, 05-story-weaver, 09-turn-structure  
**Time Investment:** ~4-5 hours

---

### 💻 For Engineers (Implementation Focus)

**Priority reading:**

1. **DESIGN-PHILOSOPHY-CRITICAL.md** → What NOT to implement (MANDATORY)
2. **08-template-spec.md** → Master Template JSON schema (NEW)
3. **09-turn-structure.md** → CFP, pre-fetching, generation (NEW)
4. **02-card-system-architecture.md** → Data structures and filtering
5. **04-gameplay-loop.md** → Core loop implementation
6. **05-story-weaver-ai.md** → AI flow architecture

**Skim:** 01-vision, 03-psychological, 06-growth, 10-validating  
**Time Investment:** ~4-5 hours

---

### 🤖 For AI/ML Engineers (GenKit Focus)

**Priority reading:**

1. **05-story-weaver-ai.md** → Complete Writers Room architecture
2. **03-psychological-engine.md** → Character state for prompting
3. **02-card-system-architecture.md** → What AI generates (templates → instances)
4. **07-genesis-plan.md** → Template structure for generation

**Skim:** 04-gameplay-loop, 06-growth  
**Time Investment:** ~2 hours

---

### ✍️ For Content Creators (Writing Focus)

**Priority reading:**

1. **01-vision-and-goals.md** → Tone and quality bar
2. **07-genesis-plan.md** → What to create and how
3. **08-content-audit.md** → Gaps to fill
4. **06-growth-and-progression.md** → How content evolves

**Skim:** 02-card-system, 03-psychological, 05-story-weaver  
**Time Investment:** ~2 hours

---

### 📋 For Product Managers (Strategic Focus)

**Priority reading:**

1. **01-vision-and-goals.md** → Vision and differentiation
2. **08-content-audit.md** → Current state and priorities
3. **07-genesis-plan.md** → Build roadmap
4. **04-gameplay-loop.md** → Core experience

**Skim:** All others for context  
**Time Investment:** ~2-3 hours

---

## Quick Reference

### Design Questions

**"Is this aligned with our vision?"**
→ Check: [01-vision-and-goals.md](./01-vision-and-goals.md) - Design Pillars section

**"How should this card work?"**
→ Check: [02-card-system-architecture.md](./02-card-system-architecture.md) - Tier structure and mechanics

**"How do I create a Master Template?"**
→ Check: [08-template-spec.md](./08-template-spec.md) - Complete JSON schema and examples

**"How does personality affect this?"**
→ Check: [03-psychological-engine.md](./03-psychological-engine.md) - Personality modifiers section

**"When should this event trigger?"**
→ Check: [05-story-weaver-ai.md](./05-story-weaver-ai.md) - Generation triggers section

**"Should this relationship evolve now?"**
→ Check: [06-growth-and-progression.md](./06-growth-and-progression.md) - Journey-based progression

**"How does the CFP work?"**
→ Check: [09-turn-structure.md](./09-turn-structure.md) - CFP architecture and optimization

**"How do I validate my template?"**
→ Check: [10-validating-template-design.md](./10-validating-template-design.md) - Validation checklist and tools

**"What should we build next?"**
→ Check: [07-genesis-plan.md](./07-genesis-plan.md) - Phased development roadmap

---

## Document Status Legend

- **V2 Canonical Reference**: Source of truth, supersedes all V1 documentation
- **Master Truth**: Highest authority for design decisions
- **Living Document**: Will be updated as design evolves (none in this collection—these are foundational)

---

## Resolving Conflicts

**If there's a contradiction:**

1. **This collection supersedes** all other documentation (V1 docs, older design notes)
2. **Within this collection:** Later documents refine earlier ones, but don't contradict
3. **If genuinely contradictory:** Flag for design review—shouldn't happen in this curated set

**Hierarchy of Authority:**
```
00-master-concept/ (this folder) - HIGHEST
  ↓
docs/1.concept/, docs/2.gameplay/, etc. - Supporting detail
  ↓
V1 documentation (_archive/) - Historical reference only
```

---

## Maintenance

**These documents are:**
- ✅ Complete and cohesive
- ✅ Internally consistent
- ✅ Ready for reference and implementation

**Updates should be:**
- 🚫 Rare (these are foundational concepts)
- 🚫 Only when core design philosophy changes
- ✅ Documented with version history if updated
- ✅ Reviewed by full design team before changing

---

## The Promise

**By reading and understanding these eight documents, you will have:**

✅ Complete understanding of Unwritten's vision  
✅ Deep knowledge of all core systems  
✅ Ability to make design decisions aligned with the vision  
✅ Context for implementation and content creation  
✅ Awareness of current gaps and priorities  

**This is everything you need to build Unwritten.**

---

## Contact & Contribution

**Questions about these documents?**
- Tag design leads in relevant channels
- Reference document and section when asking

**Proposing changes?**
- These are foundational—changes should be rare
- Prepare detailed rationale
- Discuss with design team before proposing edits

**Found an inconsistency?**
- Flag immediately—shouldn't exist in this curated collection
- Provide specific citations

---

**Welcome to the foundation of Unwritten.**

Every decision, every system, every line of code should trace back to these principles.

**Let's build something extraordinary.**

