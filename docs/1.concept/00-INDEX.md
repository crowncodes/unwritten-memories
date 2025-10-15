# Unwritten: Concept Documentation Index

**Last Updated:** October 13, 2025  
**Compliance:** master_truths v1.1 (Canonical Spec)

**Recent Updates:**
- Updated season length system (12/24/36 weeks, player choice)
- Clarified relationship levels (0-5, Level 0 = "Not Met")
- All concept docs now comply with master_truths v1.1

---

## Document Organization

This folder contains the complete conceptual design for Unwritten, organized into clean, focused documents. Each document covers a specific aspect of the game design without redundancy.

---

## Core Documents (Read In Order)

### **10-game-vision.md** ⭐ START HERE
**What is Unwritten?**
- Core concept and player fantasy
- Central game loop
- Key differentiators
- Design pillars
- Competitive positioning

**Read this first** to understand what the game is about.

---

### **11-card-system-basics.md**
**The Foundation: Understanding Cards**
- All card types explained (Character, Activity, Location, etc.)
- 470 base cards breakdown
- Card anatomy and structure
- Rarity system
- Card acquisition and limits

**Read this second** to understand the building blocks.

---

### **12-card-evolution.md**
**The Magic: How Cards Transform**
- Evolution philosophy
- Evolution triggers and process
- Character level progression (1-5)
- AI evolution pipeline
- Visual evolution system
- Memory system

**Read this third** to understand how cards become unique.

---

### **13-ai-personality-system.md**
**The Intelligence: NPCs That Feel Real**
- OCEAN personality model explained
- Personality evolution mechanics
- Three-tier memory architecture
- Behavioral generation
- Relationship dynamics (trust, attraction, compatibility)
- Emotional intelligence

**Read this fourth** to understand NPC behavior.

---

### **14-fusion-combinations.md**
**The Depth: Cards Working Together**
- All fusion types (2-card, 3-card, complex)
- Fusion requirements and conditions
- Legendary fusion chains
- Fusion failure states
- Mathematical possibilities

**Read this fifth** to understand emergent gameplay.

---

### **15-progression-phases.md**
**The Journey: Seasons & Life Arcs**
- Season-based structure (12-100 weeks variable)
- Three-act narrative per season
- Dynamic season length system
- Life phases (Establishment → Peak → Legacy)
- Goal evolution and aspiration systems

**Read this sixth** to understand progression structure.

---

### **16-archive-persistence.md**
**The Legacy: What Remains**
- Two-tier archive (seasons + lifetimes)
- Season-aware book generation
- Multi-volume novel compilation
- Character Echoes system
- Skill intuition and permanent unlocks
- Novel generation data structures

**Read this seventh** to understand persistence and archives.

---

### **19-emotional-state-system.md**
**The Experience: How You Feel Shapes What You See**
- Automatic emotional state detection
- 20 emotional states (energizing, calm, withdrawing)
- State-driven card filtering
- Turn structure with emotional drivers
- State evolution and management

**Read this eighth** to understand emotions and gameplay.

---

### **20-character-creation.md**
**The Beginning: Who Are You?**
- Five-stage creation flow (10 minutes)
- Scenario-based personality detection
- Life direction selection (9 paths)
- Initial state and starting deck
- First week goal selection

**Read this ninth** to understand character creation.

---

### **21-turn-structure.md**
**The Loop: Moment-to-Moment Gameplay**
- Multi-scale time architecture (MICRO/MESO/MACRO)
- Individual turn structure (30sec-2min)
- Day structure (morning/afternoon/evening)
- Weekly cycles and end-of-week processing
- Turn-to-novel data tracking

**Read this tenth** to understand gameplay flow.

---

### **22-multi-lifetime-continuity.md**
**The Systems: 3000+ Weeks Without Contradictions**
- Four-tier context management
- Canonical facts system
- NPC lifecycle (parallel lives, aging, leaving, returning)
- Identity evolution tracking
- Memory compression strategy (50:1)

**Read this eleventh** to understand long-term consistency.

---

### **17-monetization-model.md**
**The Business: Fair and Ethical**
- Free vs Premium comparison
- All 10 expansion packs detailed
- Art style packs and animated portraits
- Season-based novel generation pricing
- Ethical safeguards
- Revenue projections

**Read this twelfth** to understand monetization.

---

### **18-json-contracts.md**
**The Technical: Data Structures**
- Card JSON schemas
- AI generation contracts
- Archive data structures
- API specifications
- Performance targets

**Read this thirteenth** (technical audiences) for implementation.

---

## Quick Reference

### For Game Designers
Priority reading: 10 → 20 → 21 → 11 → 19 → 15

### For Writers/Narrative
Priority reading: 10 → 12 → 13 → 19 → 16 → 22
**For novel-quality storytelling:** See `2.gameplay/` docs 30-38 (narrative scaffolding, tension maintenance, stakes escalation, dramatic irony, emotional memory)

### For Developers
Priority reading: 10 → 20 → 21 → 11 → 18 → 22

### For Business/Marketing
Priority reading: 10 → 17 → 16

### For AI Engineers
Priority reading: 10 → 13 → 19 → 12 → 22 → 18

### For Artists
Priority reading: 10 → 11 → 12 (visual sections)

### For Narrative/Novel Generation Systems
Priority reading: 10 → 21 → 16 → 22 → 13

---

## Key Numbers to Remember

**Content:**
- 470 base cards (free)
- +300 premium cards (subscription)
- 10 expansion packs ($2.99 each)
- 50 Character NPCs
- 20 Emotional States
- 6 Relationship Levels (0-5, where 0 = "Not Met")

**Progression:**
- 12/24/36 weeks per season (player choice at season start)
- Potentially 3000+ weeks per lifetime
- 20-40 seasons typical lifetime
- Relationship Levels 0-5 (0=Not Met, 1=Stranger, 2=Acquaintance, 3=Friend, 4=Close Friend, 5=Soulmate)
- Trust 0.0-1.0 (continuous under levels)
- OCEAN traits (1.0-5.0 scale, evolve over time)

**Time Scales:**
- MICRO: 30sec-2min (card plays)
- MESO: 10-15min (day structure)
- MACRO: 45-60min (weekly cycles)
- MEGA: 8-12hrs (season completion)

**Monetization:**
- Free: Complete experience (470 cards)
- Premium: $4.99/month (770 total cards)
- Expansion Packs: $2.99 each (50 cards each)
- Art Style Packs: $1.99 each
- Legacy Edition: $19.99 once

---

## Document Status

| Document | Status | Last Update | Completeness |
|----------|--------|-------------|--------------|
| 10-game-vision.md | ✅ Complete | Oct 13, 2025 | 100% |
| 11-card-system-basics.md | ✅ Complete | Oct 13, 2025 | 100% |
| 12-card-evolution.md | ✅ Complete | Oct 13, 2025 | 100% |
| 13-ai-personality-system.md | ✅ Complete | Oct 13, 2025 | 100% |
| 14-fusion-combinations.md | ✅ Complete | Oct 13, 2025 | 100% |
| 15-progression-phases.md | ✅ Complete | Oct 13, 2025 | 100% |
| 16-archive-persistence.md | ✅ Complete | Oct 13, 2025 | 100% |
| 17-monetization-model.md | ✅ Complete | Oct 13, 2025 | 100% |
| 18-json-contracts.md | ✅ Complete | Oct 13, 2025 | 100% |
| 19-emotional-state-system.md | ✅ Complete | Oct 13, 2025 | 100% |
| 20-character-creation.md | ✅ Complete | Oct 13, 2025 | 100% |
| 21-turn-structure.md | ✅ Complete | Oct 13, 2025 | 100% |
| 22-multi-lifetime-continuity.md | ✅ Complete | Oct 13, 2025 | 100% |

---

## What Happened to Old Documents?

The following original documents were **analyzed and consolidated** into the new structure:

**Kept for Reference:**
- `9cdbfac6.md` - Feature spec (Sims-style comprehensive list)
- `74638e04.md` - Technical game spec (mobile focus, budget/timeline)
- `Game Concept.md` - Original card system design
- `Main Concept Overview.md` - AI agent prompt format
- `Doc 3 Summary.md` - Status update document

**Note:** Old documents contain some information not yet integrated into the new structure (like specific Sims-style features). They remain as reference material but should not be the primary source of truth.

**Primary Source of Truth:** Documents 10-18 (this folder)

---

## Related Documentation

**For Gameplay Details:**
→ See `docs/2.gameplay/` folder
- Categories.md
- fusion_trees_doc.md
- Gameplay Turns.md
- Packs.md
- Expansions.md

**For AI Implementation:**
→ See `docs/3.ai/` folder
- ai_prompt_engineering.md
- Local Models.md
- unwritten-training-2025.md

**For Visual Systems:**
→ See `docs/4.visual/` folder
- visual_generation_tech.md
- Image Generation.md
- Animated.md

**For Technical Architecture:**
→ See `docs/5.architecture/` folder
- tech_architecture_doc.md

**For Monetization Details:**
→ See `docs/6.monetization/` folder
- Prompt+Monetization.md
- Book Concept.md

---

## Standardized Numbers (Use These)

To resolve conflicts found in analysis:

**Base Card Count:** 470 cards
- 50 Character Cards
- 80 Activity Cards
- 30 Location Cards
- 20 Emotion Cards
- 20 Resource Cards
- 90 Aspiration Cards
- 150 Situation Cards
- 30 System Cards

**Premium Book Length:**
- Free: 3-5k words
- Premium: 12-15k words

**Art Pack Pricing:**
- Regular Style Packs: $1.99
- Premium/Holo: $2.99

**Platform:**
- Primary: Mobile (iOS/Android)
- Future consideration: PC/Console

---

## Contributing

When updating these documents:

1. ✅ Use the standardized numbers above
2. ✅ Remove any conversational preambles
3. ✅ Keep focused on single topic per document
4. ✅ Reference other documents instead of repeating content
5. ✅ Update this index when adding new documents
6. ✅ Maintain the 10-18 numbering scheme

---

## Questions or Clarifications?

If anything conflicts or is unclear:
1. Check this index for standardized numbers
2. Cross-reference with gameplay documentation
3. Prioritize documents 10-18 over older docs
4. Update old docs to reference new structure

---

**These 9 documents (10-18) contain everything needed to understand and build Unwritten.**

