# Unwritten AI Documentation

**Status:** 🔄 Reorganization in Progress  
**Last Updated:** October 13, 2025

---

## Current State

This folder is currently undergoing a major reorganization to improve navigation and maintainability.

### What's Happening?

We're transforming **3 large, dense documents** (4,393 lines) into **11 focused, well-organized documents** (~7,700 lines) following the same clean structure used in `docs/1.concept/`.

---

## Quick Navigation

### If You're Looking for Something NOW:

**Current Documents (Original):**
- `ai_prompt_engineering.md` - Comprehensive prompt engineering guide (2,504 lines)
- `unwritten-training-2025.md` - Local model training guide (954 lines)
- `Local Models.md` - Hybrid AI architecture and latency strategies (935 lines)

**Planning Documents (New):**
- `AI_REORGANIZATION_PLAN.md` - Detailed reorganization plan
- `REORGANIZATION_SUMMARY.md` - Visual before/after summary
- `REORGANIZATION_CHECKLIST.md` - Implementation checklist

---

## New Structure (Coming Soon)

### Once reorganization is complete:

```
docs/3.ai/
├── 00-INDEX.md                        ⭐ START HERE
│
├── ARCHITECTURE (2 docs)
├── 30-ai-architecture-overview.md     Strategic decisions
├── 31-hybrid-cloud-local-system.md    System design
│
├── PROMPT ENGINEERING (4 docs)
├── 32-prompt-engineering-principles.md Core concepts
├── 33-prompt-templates-library.md      Templates
├── 34-context-memory-systems.md        Context/Memory
├── 35-consistency-coherence.md         Quality control
│
├── LOCAL MODELS (2 docs)
├── 36-local-model-training.md          Training guide
├── 37-model-deployment-optimization.md Deployment
│
├── UX & OPTIMIZATION (2 docs)
├── 38-latency-ux-strategies.md         Hiding latency
└── 39-cost-performance-targets.md      Cost optimization
```

---

## Benefits of Reorganization

✅ **Clear Entry Point** - Start with INDEX, find what you need in <30 seconds  
✅ **No Duplication** - Each topic covered once, completely  
✅ **Logical Flow** - Progressive detail from strategy to implementation  
✅ **Easy Navigation** - Cross-referenced, role-based reading paths  
✅ **Single Responsibility** - Each document has one focused purpose  

---

## Reading Paths (Preview)

### For Different Roles:

**AI Engineer:**  
00 → 30 → 31 → 36 → 37 → 32 → 33

**Prompt Engineer:**  
00 → 32 → 33 → 34 → 35

**Game Designer:**  
00 → 30 → 38 → 39

**UX Designer:**  
00 → 30 → 38

**Business/Product:**  
00 → 30 → 39 → 31

---

## Timeline

- **Planning:** ✅ Complete (October 13, 2025)
- **Phase 1 (Structure):** Days 1-2
- **Phase 2 (Content):** Days 3-10
- **Phase 3 (Quality):** Days 11-12
- **Phase 4 (Archive):** Day 13

**Total Time:** 13 days

---

## What Happens to Old Documents?

Original documents will be moved to `ARCHIVE/` subfolder:
- Preserved for 6 months
- Fully mapped to new documents
- Can be referenced if needed
- Not deleted, just archived

---

## Contributing

### If You Need to Update AI Documentation:

**Before Reorganization:**
- Update existing documents (ai_prompt_engineering.md, etc.)
- Note that reorganization may require re-applying changes

**After Reorganization:**
- Use the INDEX to find the right document
- Update only that specific document
- Follow single-responsibility principle
- Add cross-references where appropriate

---

## Questions?

**"Which document should I read?"**  
→ Once complete, start with `00-INDEX.md`

**"Where do I find [specific topic]?"**  
→ Check `AI_REORGANIZATION_PLAN.md` → Content Mapping Table

**"Can I still use old documents?"**  
→ Yes! They remain available until reorganization is complete

**"How do I help?"**  
→ Check `REORGANIZATION_CHECKLIST.md` for tasks

---

## Key AI System Facts

### Technology Stack
- **Cloud AI:** Claude Sonnet 4, GPT-4
- **Local AI:** Phi-3-mini, Gemma-2-2b
- **Frameworks:** LiteRT, PyTorch 2.x, PEFT/LoRA
- **Deployment:** Flutter with tflite_flutter

### Performance Targets
- **Model Size:** 2-3MB (INT4 quantized)
- **Inference Speed:** 8-15ms
- **Battery Impact:** <1% per 30min session
- **Cost per Player:** $2-4/month

### Architecture Decision
**Hybrid Cloud-Local System:**
- 70-85% interactions: Local AI (instant, free)
- 15-30% interactions: Cloud AI (quality, $2-4/month)
- Smart routing based on importance
- UX strategies to hide latency

---

## Related Documentation

**For Character Personality System:**  
→ `docs/1.concept/13-ai-personality-system.md`

**For Game Architecture:**  
→ `docs/5.architecture/tech_architecture_doc.md`

**For Cost Details:**  
→ `docs/1.concept/17-monetization-model.md`

---

## Status Updates

### October 13, 2025
- ✅ Analysis complete
- ✅ Reorganization plan created
- ✅ Content mapping finalized
- 📋 Ready to begin implementation

---

**For detailed reorganization information, see:**
- `AI_REORGANIZATION_PLAN.md` - Complete plan with line-by-line mapping
- `REORGANIZATION_SUMMARY.md` - Visual before/after comparison
- `REORGANIZATION_CHECKLIST.md` - Step-by-step implementation guide

---

**This reorganization will make the AI documentation as clean and navigable as the concept documentation. 🎯**

