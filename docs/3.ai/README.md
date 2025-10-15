# Unwritten AI Documentation

**Status:** ✅ Complete & Organized  
**Last Updated:** October 2025  
**Total Documents:** 36 files

---

## 🎯 Quick Start - What To Read First

### Current Implementation Strategy

**Development (Now - Weeks 1-8):** Firebase AI Logic for rapid content generation  
**Production (Target - Weeks 9-24):** Genkit backend as primary architecture  
**Timeline:** See `03-implementation-phases.md` for complete week-by-week plan

---

## 📚 Documentation by Role

### For Game Developers (Need AI NOW)

**Goal:** Get AI working quickly for content generation

**Read in this order:**
1. **`03-implementation-phases.md`** - Understand the strategy (5 min)
2. **`21-firebase-ai-quick-start.md`** - 30-minute quick start
3. **`20-firebase-ai-integration.md`** - Complete reference when needed

**Timeline:** 2-4 hours to have AI working

---

### For Backend Engineers (Building Production Genkit)

**Goal:** Build production-ready Genkit backend

**Read in this order:**
1. **`03-implementation-phases.md`** - Understand timeline and strategy
2. **`30-genkit-architecture.md`** - Unwritten-specific architecture
3. **`31-genkit-integration-guide.md`** - Complete implementation guide
4. **`34-migration-firebase-to-genkit.md`** - Migration strategy

**Timeline:** 2-3 weeks to have Genkit backend operational

---

### For Flame Developers (Integrating AI in Game)

**Goal:** Integrate AI without blocking game loop (60 FPS critical)

**Read in this order:**
1. **`60-flame-ai-integration-patterns.md`** - Architectural patterns
2. **`61-flame-ai-components.md`** - Complete component library
3. **`62-flame-game-loop-ai.md`** - Performance deep dive

**Timeline:** 1-2 weeks to integrate properly

---

### For Storage/Data Engineers

**Goal:** Implement complete AI output storage system

**Read in this order:**
1. **`50-ai-output-storage-system.md`** - Overall architecture
2. **`51-storage-metadata-schemas.md`** - All schemas
3. **`52-local-cache-implementation.md`** - Local caching (Hive + memory)
4. **`53-cloud-storage-integration.md`** - Firebase integration

**Timeline:** 1-2 weeks to implement

---

## 📁 Complete Document Index

### STRATEGY & ARCHITECTURE (00-09)

| Doc | Title | Description |
|-----|-------|-------------|
| **00** | **INDEX** | Complete navigation hub for all AI docs |
| **01** | **AI Strategy Overview** | High-level strategy, constraints, hybrid architecture |
| **02** | **Technology Stack** | Models, pricing, frameworks overview |
| **03** | **Implementation Phases** | ⭐ **CRITICAL** - Week-by-week plan (Firebase AI → Genkit) |
| **04** | **AI Approach Comparison** | TFLite vs Firebase AI vs Genkit decision guide |

### PROMPT ENGINEERING (10-19)

| Doc | Title | Description |
|-----|-------|-------------|
| **10** | **Prompt Engineering Principles** | Core concepts for quality AI content |
| **11** | **Prompt Templates Library** | Production-ready templates (copy-paste) |
| **12** | **Context & Memory Systems** | Context injection, memory management |
| **13** | **Consistency & Coherence** | Quality validation and cliché detection |

### FIREBASE AI (20-29)

| Doc | Title | Description |
|-----|-------|-------------|
| **20** | **Firebase AI Integration** | Complete Firebase AI Logic reference |
| **21** | **Firebase AI Quick Start** | 30-minute getting started guide |

### GENKIT (30-39)

| Doc | Title | Description |
|-----|-------|-------------|
| **30** | **Genkit Architecture** | ⭐ Unwritten-specific implementation (NOT generic) |
| **31** | **Genkit Integration Guide** | Complete Genkit implementation reference |
| **33** | **Genkit Quick Reference** | Daily development cheat sheet |
| **34** | **Migration Guide** | ⭐ Firebase AI → Genkit migration strategy |

### LOCAL AI (40-49)

| Doc | Title | Description |
|-----|-------|-------------|
| **40** | **Hybrid Cloud-Local System** | Smart routing, TFLite integration |
| **41** | **Local Model Training** | Training 2-3MB on-device models |
| **42** | **Model Deployment** | Deployment strategies, caching |
| **43** | **Training Data Quality** | Quality standards for training data |

### AI OUTPUT STORAGE (50-59)

| Doc | Title | Description |
|-----|-------|-------------|
| **50** | **AI Output Storage System** | ⭐ Complete storage architecture (3-tier caching) |
| **51** | **Storage Metadata Schemas** | Schemas for all content types |
| **52** | **Local Cache Implementation** | Hive + memory cache implementation |
| **53** | **Cloud Storage Integration** | Firebase Storage + Firestore setup |

### FLAME INTEGRATION (60-69)

| Doc | Title | Description |
|-----|-------|-------------|
| **60** | **Flame AI Integration Patterns** | ⭐ Non-blocking AI in game loop |
| **61** | **Flame AI Components** | Complete component library with code |
| **62** | **Flame Game Loop AI** | Performance deep dive, optimization |

### UX & PERFORMANCE (70-79)

| Doc | Title | Description |
|-----|-------|-------------|
| **70** | **Latency & UX Strategies** | Hide AI latency, predictive loading |
| **71** | **Cost & Performance Targets** | Cost optimization ($2-2.50/player/month) |

### PROJECT STATUS (80-89)

| Doc | Title | Description |
|-----|-------|-------------|
| **80** | **Image Generation SDK Change** | Why we switched from Vertex AI to Google AI |
| **81** | **Compliance Reports** | Master Truths v1.2 compliance status |

---

## 🏗️ Complete AI Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    UNWRITTEN AI SYSTEM                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐
│   LOCAL AI      │  │  FIREBASE AI     │  │  GENKIT         │
│   (TFLite)      │  │  (Development)   │  │  (Production)   │
├─────────────────┤  ├──────────────────┤  ├─────────────────┤
│ • Free          │  │ • Quick setup    │  │ • RAG support   │
│ • 8-15ms        │  │ • 2-5 seconds    │  │ • Tool calling  │
│ • 70-85% usage  │  │ • Dev content    │  │ • Complex flows │
│ • Offline OK    │  │ • Prototyping    │  │ • Scalable      │
└─────────────────┘  └──────────────────┘  └─────────────────┘
         ↓                    ↓                      ↓
┌─────────────────────────────────────────────────────────────┐
│                      SMART ROUTER                            │
│  Routes based on: complexity, offline state, user tier      │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│                  STORAGE SYSTEM (3-Tier)                     │
│  Memory Cache → Hive Cache → Firebase Cloud                 │
│  < 1ms access    1-5ms access    100-500ms access          │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│                    FLAME GAME LOOP                           │
│  Non-blocking AI integration (60 FPS maintained)            │
└─────────────────────────────────────────────────────────────┘
```

---

## ⏱️ Implementation Timeline

### Phase 1: Development (Weeks 1-8) - Use Firebase AI NOW

**What:** Rapid content generation for development
**Why:** Need content quickly while building Genkit
**How:** `21-firebase-ai-quick-start.md`

### Phase 2: Build Genkit (Weeks 9-16) - Build Production System

**What:** Production-ready Genkit backend
**Why:** Scalable, feature-rich AI system
**How:** `30-genkit-architecture.md` + `31-genkit-integration-guide.md`

### Phase 3: Migration (Weeks 17-24) - Gradual Rollout

**What:** Migrate from Firebase AI to Genkit
**Why:** Move to production architecture safely
**How:** `34-migration-firebase-to-genkit.md`

### Phase 4: Production (Week 25+) - Genkit Primary

**What:** Genkit as main system, Firebase AI as fallback
**Why:** Production-ready, scalable, cost-optimized
**How:** Monitor and optimize

---

## 💰 Cost Targets

**Target:** $2.00 - $2.50 per player per month

**Breakdown:**
- Gemini Flash 2.5 (80% of requests): $1.50/month
- Gemini 2.5 Pro (20% of requests): $0.75/month
- Cloud Run hosting: $0.25/month
- Storage (Firestore + Cloud Storage): $0.15/month
- **Caching savings:** -$0.50/month
- **Local AI savings:** -$0.40/month

**See:** `71-cost-performance-targets.md` for optimization strategies

---

## 🎮 Key Features

### ✅ What's Documented

- **Strategic Planning:** Complete phased implementation (Firebase → Genkit)
- **Three AI Approaches:** TFLite (local), Firebase AI (dev), Genkit (production)
- **Complete Storage:** Three-tier caching for all AI content types
- **Flame Integration:** Non-blocking AI patterns for 60 FPS gameplay
- **Migration Path:** Safe rollout strategy with rollback procedures
- **Cost Optimization:** Strategies to hit $2-2.50/player/month target
- **Performance:** Latency targets, caching, pre-loading
- **Quality:** Validation systems, cliché detection, consistency

### ✅ What's Production-Ready

All documentation is **production-ready** with:
- Complete code examples
- Error handling patterns
- Testing strategies
- Deployment guides
- Monitoring and alerting
- Security best practices

---

## 🔥 Critical Documents (Start Here)

If you're short on time, read these 5 documents first:

1. **`03-implementation-phases.md`** - The complete strategy
2. **`30-genkit-architecture.md`** - Unwritten-specific Genkit design
3. **`50-ai-output-storage-system.md`** - Storage architecture
4. **`60-flame-ai-integration-patterns.md`** - Non-blocking AI patterns
5. **`34-migration-firebase-to-genkit.md`** - Migration guide

These 5 documents cover 80% of what you need to know.

---

## 📖 Learning Paths

### Path 1: Implement Firebase AI (2-4 hours)

```
03-implementation-phases.md (Phase 1 section)
    ↓
21-firebase-ai-quick-start.md
    ↓
11-prompt-templates-library.md (reference)
    ↓
Start building!
```

### Path 2: Build Genkit Backend (2-3 weeks)

```
03-implementation-phases.md (Phase 2 section)
    ↓
30-genkit-architecture.md
    ↓
31-genkit-integration-guide.md
    ↓
11-prompt-templates-library.md (use templates)
    ↓
Deploy to Cloud Run
```

### Path 3: Integrate with Flame (1-2 weeks)

```
60-flame-ai-integration-patterns.md
    ↓
61-flame-ai-components.md
    ↓
62-flame-game-loop-ai.md (if performance issues)
    ↓
Implement non-blocking components
```

### Path 4: Build Storage System (1-2 weeks)

```
50-ai-output-storage-system.md (architecture)
    ↓
51-storage-metadata-schemas.md (schemas)
    ↓
52-local-cache-implementation.md (local)
    ↓
53-cloud-storage-integration.md (cloud)
    ↓
Implement three-tier caching
```

---

## 🚨 Common Pitfalls

### ❌ Don't:
- Block game loop with AI calls (use async patterns)
- Skip App Check security (Firebase AI requires it)
- Use Genkit for everything in MVP (use Firebase AI for speed)
- Forget to cache aggressively (storage is cheaper than AI)
- Hard-code API keys (use environment variables)

### ✅ Do:
- Read `03-implementation-phases.md` first (understand strategy)
- Use feature flags for gradual rollout
- Monitor costs from day 1
- Test on low-end devices
- Implement proper error handling with fallbacks

---

## 📊 Documentation Statistics

- **Total Documents:** 36 files
- **New Documents Created:** 11 files (~9,700 lines)
- **Total Lines of Documentation:** ~50,000+ lines
- **Code Examples:** 200+ working examples
- **Coverage:** Complete (all aspects of AI system documented)

---

## 🔗 Related Documentation

- **`docs/master_flutter_flame_spec_v_1_0.md`** - Overall Flutter + Flame architecture
- **`docs/7.schema/`** - Data schemas and contracts
- **`docs/9.music/`** - Music system (Lyria stem generation)
- **`app/docs/FIREBASE_AUTH_SETUP.md`** - Firebase authentication
- **`app/docs/FIREBASE_APP_CHECK_SETUP.md`** - App Check (required for Firebase AI)

---

## 📝 Document Status Legend

- ✅ **Complete** - Production-ready, fully documented
- 🟡 **In Progress** - Being developed
- ❌ **Not Started** - Planned but not begun

**Current Status:** ✅ All documents complete and production-ready

---

## 💬 Questions?

**For strategic questions:** Read `01-ai-strategy-overview.md` and `03-implementation-phases.md`

**For implementation questions:** Check the relevant section (Firebase AI, Genkit, Storage, Flame)

**For cost questions:** Read `71-cost-performance-targets.md`

**For performance questions:** Read `70-latency-ux-strategies.md` and `62-flame-game-loop-ai.md`

---

**Last Updated:** October 15, 2025  
**Status:** ✅ Complete Documentation Suite  
**Next Review:** When implementation begins
