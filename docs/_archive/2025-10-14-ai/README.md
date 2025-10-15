# ARCHIVE - Original AI Documentation

This folder contains the original three AI documentation files that were reorganized into a structured, comprehensive set of 11 documents.

**Archived on:** October 14, 2025  
**Reason:** Reorganization for better clarity, navigation, and maintainability

---

## Archived Files

### 1. `ai_prompt_engineering.md`
**Original Size:** ~3,000 lines  
**Content:** Prompt engineering strategies, personality modeling, memory systems, consistency, quality control

**Mapped to New Documents:**
- **32-prompt-engineering-principles.md** - Core principles, OCEAN mapping, emotional resonance
- **33-prompt-templates-library.md** - Ready-to-use prompt templates
- **34-context-memory-systems.md** - Context injection, memory hierarchy
- **35-consistency-coherence.md** - Quality validation, consistency checking

### 2. `unwritten-training-2025.md`
**Original Size:** ~1,000 lines  
**Content:** Model training guide, LoRA/PEFT, PyTorch optimizations, quantization, Flutter integration

**Mapped to New Documents:**
- **36-local-model-training.md** - Complete training pipeline
- **37-model-deployment-optimization.md** - Deployment strategies (partial)

### 3. `Local Models.md`
**Original Size:** ~900 lines  
**Content:** Hybrid architecture, latency management, local AI feasibility, UX strategies

**Mapped to New Documents:**
- **30-ai-architecture-overview.md** - Hybrid AI architecture (partial)
- **31-hybrid-cloud-local-system.md** - Complete hybrid implementation
- **37-model-deployment-optimization.md** - Deployment & optimization (partial)
- **38-latency-ux-strategies.md** - UX strategies for hiding latency
- **39-cost-performance-targets.md** - Cost optimization (partial)

---

## Content Mapping Matrix

| Original File | Section | New Location |
|--------------|---------|--------------|
| `ai_prompt_engineering.md` | Prompt Philosophy | 32-prompt-engineering-principles.md |
| `ai_prompt_engineering.md` | Prompt Templates | 33-prompt-templates-library.md |
| `ai_prompt_engineering.md` | Context Injection | 34-context-memory-systems.md |
| `ai_prompt_engineering.md` | Memory Systems | 34-context-memory-systems.md |
| `ai_prompt_engineering.md` | Consistency Maintenance | 35-consistency-coherence.md |
| `ai_prompt_engineering.md` | Quality Control | 35-consistency-coherence.md |
| `ai_prompt_engineering.md` | Multi-Turn Refinement | 35-consistency-coherence.md |
| `unwritten-training-2025.md` | Environment Setup | 36-local-model-training.md |
| `unwritten-training-2025.md` | Data Collection | 36-local-model-training.md |
| `unwritten-training-2025.md` | Model Architecture | 36-local-model-training.md |
| `unwritten-training-2025.md` | Training Pipeline | 36-local-model-training.md |
| `unwritten-training-2025.md` | Quantization | 36-local-model-training.md |
| `unwritten-training-2025.md` | Flutter Integration | 36-local-model-training.md |
| `Local Models.md` | Hybrid Architecture | 31-hybrid-cloud-local-system.md |
| `Local Models.md` | Predictive Pre-Generation | 38-latency-ux-strategies.md |
| `Local Models.md` | Conversational Pacing | 38-latency-ux-strategies.md |
| `Local Models.md` | Progressive Disclosure | 38-latency-ux-strategies.md |
| `Local Models.md` | Activity-Based Time Compression | 38-latency-ux-strategies.md |
| `Local Models.md` | Background Generation | 37-model-deployment-optimization.md |
| `Local Models.md` | Caching Strategies | 37-model-deployment-optimization.md |

---

## New Structure Benefits

### ✅ Better Organization
- Clear separation of concerns
- Logical progression from architecture → implementation → optimization
- Each document focused on a specific topic

### ✅ Enhanced Navigation
- 00-INDEX.md provides central navigation
- Documents numbered for logical reading order
- Cross-references between related documents

### ✅ Improved Maintainability
- Smaller, focused documents easier to update
- No redundancy or overlap
- Clear ownership of topics

### ✅ Complete Coverage
- Added cost analysis (39-cost-performance-targets.md)
- Aligned AI architecture with monetization strategy
- Updated with Gemini Flash 2.5 & Pro pricing
- Production-ready deployment guides

---

## Total Lines of Code

**Original (3 files):**
- ai_prompt_engineering.md: ~3,000 lines
- unwritten-training-2025.md: ~1,000 lines
- Local Models.md: ~900 lines
- **Total: ~4,900 lines**

**New (11 files):**
- 00-INDEX.md: ~250 lines
- 30-ai-architecture-overview.md: ~1,000 lines
- 31-hybrid-cloud-local-system.md: ~1,200 lines
- 32-prompt-engineering-principles.md: ~970 lines
- 33-prompt-templates-library.md: ~1,150 lines
- 34-context-memory-systems.md: ~1,200 lines
- 35-consistency-coherence.md: ~1,450 lines
- 36-local-model-training.md: ~1,825 lines
- 37-model-deployment-optimization.md: ~2,135 lines
- 38-latency-ux-strategies.md: ~1,850 lines
- 39-cost-performance-targets.md: ~1,950 lines
- **Total: ~15,000 lines**

**Expansion:** 3x more content with better organization, more examples, and production-ready code.

---

## How to Use This Archive

### If You Need Old Content
1. Reference the mapping matrix above
2. Find the corresponding new document(s)
3. New documents contain all original content + enhancements

### If You Need to Restore
```bash
# Copy archived file back to docs/3.ai/
cp ARCHIVE/ai_prompt_engineering.md .

# But consider: New documents are better organized!
```

### If You Need to Compare
```bash
# View differences
diff ARCHIVE/ai_prompt_engineering.md 32-prompt-engineering-principles.md
```

---

## Migration Complete ✅

The reorganization is complete and all content has been successfully migrated to the new structure. These archived files are kept for reference but are no longer maintained.

**For current documentation, see:** `00-INDEX.md` in the parent directory.

---

**Archived by:** AI Documentation Reorganization Project  
**Date:** October 14, 2025  
**Version:** 1.0
