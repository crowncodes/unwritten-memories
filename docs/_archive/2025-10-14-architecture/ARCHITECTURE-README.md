# Unwritten Architecture Documentation

> **Canonical Reference**: Master Truths v1.2  
> **Architecture Pattern**: I/O FLIP (Flutter + Dart Frog + Firebase)  
> **Last Updated**: October 14, 2025

---

## Overview

This directory contains comprehensive architecture documentation for the Unwritten Flutter game, including:
- **I/O FLIP architecture analysis** and adaptation patterns
- **Implementation roadmap** (MVP to production)
- **Flutter project setup** guides
- **Technical architecture** deep-dives

Unwritten adopts proven patterns from Google's I/O FLIP game, adapting them for single-player narrative gameplay with AI generation.

---

## 📚 Core Documentation

### 1. Start Here: I/O FLIP Architecture Analysis

**File**: `IO-FLIP-ARCHITECTURE-ANALYSIS.md`

Comprehensive analysis of I/O FLIP's architecture and how we adapt it for Unwritten:

**What I/O FLIP Does**:
- Flutter Web + Flame game engine
- Dart Frog backend (full-stack Dart)
- Server-authoritative multiplayer card battles
- Firebase ecosystem (Firestore, Auth, Storage)
- Shared game logic packages
- WebSocket real-time connections

**What Unwritten Adapts**:
- Same tech stack (Flutter + Dart Frog + Firebase)
- Backend-authoritative AI generation (not match validation)
- Shared relationship/progression logic
- Cloud-first with future local AI
- Optimistic UI for responsiveness

**Key Sections**:
- Frontend Layer (Flutter + Flame patterns)
- Backend Layer (Dart Frog routes & services)
- Shared Packages Architecture
- State Management (BLoC pattern)
- Deployment & Infrastructure (Cloud Run)

👉 **Read this first** to understand our architectural foundation.

---

### 2. Implementation Plan (MVP Roadmap)

**File**: `IMPLEMENTATION-PLAN-MVP.md`

Phased implementation timeline from foundation to playable MVP:

**Phase 1 (Weeks 1-4)**: Foundation
- Flutter project setup with Clean Architecture
- Core data models (Card, GameState, Relationship)
- Base card JSON (50 starter cards)
- Basic UI framework

**Phase 2 (Weeks 5-8)**: Dart Frog Backend + Shared Packages
- Backend server setup with Cloud Run deployment
- Shared `game_logic` package (used by both client & server)
- API routes: `/game/play-card`, `/ai/generate-dialogue`
- Firebase integration (Firestore + Auth)
- Training data collection infrastructure

**Phase 3 (Weeks 9-12)**: Core Game Loop
- Card play system with backend validation
- Turn management (Morning/Afternoon/Evening)
- Resource management (Energy, Time, Money)
- Local storage + cloud sync

**Phase 4 (Weeks 13-16)**: Cloud AI Integration
- OpenAI/Anthropic API integration (backend-side)
- NPC personality-driven responses
- Card evolution with AI
- **Training data collection from gameplay**

**Phase 5 (Weeks 17-20)**: Season Structure
- 12/24/36 week seasons
- Aspiration tracking
- Relationship progression
- Season archives

**Phase 6 (Weeks 21-24)**: Polish & Beta
- Onboarding flow
- UI/UX polish
- Analytics & monitoring
- Beta deployment

**Timeline**: 24 weeks to beta-ready MVP

---

### 3. Flutter Project Setup Guide

**File**: `FLUTTER-PROJECT-SETUP.md`

Step-by-step instructions for setting up the Flutter project:

**Covered Topics**:
- Prerequisites (Flutter 3.24+, Dart 3.5+)
- Project initialization with Clean Architecture
- Dependencies (Riverpod, Hive, HTTP, etc.)
- Code generation setup (build_runner)
- Environment configuration (.env files)
- Run configurations (VS Code)
- Initial project files (logger, constants, main.dart)
- Verification steps

**Quick Start**:
```bash
# 1. Create Flutter project
flutter create --org com.unwritten unwritten_flutter

# 2. Set up folder structure (see guide)
mkdir -p lib/core lib/features lib/shared

# 3. Install dependencies
flutter pub get

# 4. Run code generation
flutter pub run build_runner build

# 5. Verify setup
flutter analyze
flutter run
```

---

### 4. Technical Architecture Deep-Dive

**File**: `tech_architecture_doc.md`

Detailed technical architecture covering:
- System architecture overview
- Database schemas (SQLite client + PostgreSQL server)
- State management (Redux-like patterns)
- AI integration layer
- Real-time evolution pipeline
- Caching & performance strategies
- Offline capability
- Mobile-specific optimizations
- Security & data protection
- Analytics & telemetry
- Scalability architecture

**Note**: This document contains some Unity-specific content from initial planning. Relevant patterns have been adapted to Flutter/Dart in the I/O FLIP analysis document.

---

## 🏗️ Architecture Highlights

### Full-Stack Dart

```
┌────────────────────────────────────────────────────────┐
│              Flutter Frontend (Dart)                    │
│  • BLoC state management                               │
│  • Riverpod dependency injection                       │
│  • Flame game engine (optional)                        │
└────────────────┬───────────────────────────────────────┘
                 │
                 │ HTTP/REST API
                 │
┌────────────────▼───────────────────────────────────────┐
│           Shared Packages (Dart)                        │
│  • game_logic: Relationship calculator                 │
│  • game_logic: Progression calculator                  │
│  • game_logic: Card validators                         │
└────────────────┬───────────────────────────────────────┘
                 │
                 │ Used by both client & server
                 │
┌────────────────▼───────────────────────────────────────┐
│         Dart Frog Backend (Dart)                        │
│  • API routes: /game/*, /ai/*                          │
│  • OpenAI/Anthropic integration                        │
│  • Training data logging                               │
│  • Firebase Admin SDK                                  │
└────────────────┬───────────────────────────────────────┘
                 │
┌────────────────▼───────────────────────────────────────┐
│               Firebase Services                         │
│  • Firestore (game state, relationships)              │
│  • Firebase Auth (anonymous + email)                  │
│  • Cloud Storage (card assets)                        │
│  • Firebase Hosting (static web)                      │
└─────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

1. **Flame Game Engine from Day 1** 🎮
   - **Required from Phase 1** (not optional)
   - Code structure fundamentally different from pure Flutter
   - Migrating later = complete rewrite (2-3 weeks wasted)
   - I/O FLIP proves it's production-ready
   - Enables "Unity-like game feel" goal
   - See `CARD-DRAG-PHYSICS-GUIDE.md` for full rationale

2. **Backend-Authoritative Model**
   - Backend validates all card plays
   - Backend generates AI content
   - Prevents cheating/tampering
   - Centralizes training data collection

3. **Shared Game Logic**
   - Relationship calculations shared between client/server
   - Client uses for optimistic updates
   - Server uses for authoritative results
   - Single source of truth

4. **Optimistic UI Updates**
   - Client predicts outcome instantly (using shared logic)
   - Displays result immediately
   - Backend validates in background
   - Rollback if server disagrees

5. **Cloud-First AI**
   - Phase 1-5: All AI via cloud APIs (OpenAI/Anthropic)
   - Collect high-quality training data
   - Phase 6+: Migrate to local TensorFlow Lite
   - Hybrid approach for battery efficiency

---

## 🚀 Getting Started

### For Flutter Development

1. Read `FLUTTER-PROJECT-SETUP.md`
2. Read `CARD-DRAG-PHYSICS-GUIDE.md` (Flame setup)
3. Set up Flutter environment
4. Create project structure
5. Install dependencies (**including Flame 1.17+**)
6. Set up Flame game classes (see guide)
7. Begin Phase 1 implementation

### For Backend Development

1. Read `IO-FLIP-ARCHITECTURE-ANALYSIS.md` (Backend Layer section)
2. Install Dart Frog CLI: `dart pub global activate dart_frog_cli`
3. Create backend project: `dart_frog create backend`
4. Set up shared packages (Phase 2)
5. Deploy to Cloud Run

### For Architecture Understanding

1. Read `IO-FLIP-ARCHITECTURE-ANALYSIS.md` (full document)
2. Review I/O FLIP source: https://github.com/flutter/io_flip
3. Understand adaptation patterns
4. Review `IMPLEMENTATION-PLAN-MVP.md` for timeline

---

## 📊 Training Data Generation

Unwritten collects training data from real gameplay for future local AI models.

### Pipeline Files

- **`data/qwen3_training_pipeline.py`** - Training data generator (pre-game)
- **Backend training logger** - Logs all AI interactions during gameplay

### Training Data Categories

1. **Emotional Authenticity** - Realistic emotional responses
2. **Dramatic Irony** - Player-known information NPCs don't know
3. **Tension Building** - Progressive narrative escalation
4. **Personality Traits** - OCEAN-based character profiles
5. **Relationship Scoring** - Trust/interaction dynamics

### Gameplay Data Collection

**Logged by Backend**:
- Every card play with context
- Every NPC response (input + output)
- Every card evolution
- Every relationship impact
- Player engagement signals (read time, continued interaction)

**Export Format**: JSONL for model fine-tuning

```json
{
  "timestamp": "2025-10-14T10:30:00Z",
  "type": "npc_response",
  "input": {...},
  "output": {...},
  "player_feedback": {...},
  "quality_score": 0.85
}
```

---

## 🔗 Related Documentation

### In `docs/1.concept/`
- `10-game-vision.md` - High-level vision
- `11-card-system-basics.md` - Card system design
- `13-ai-personality-system.md` - NPC personality framework

### In `docs/2.gameplay/`
- `01-turn-structure.md` - Turn-based gameplay mechanics
- `02-relationship-system.md` - Relationship progression
- `03-season-structure.md` - Season lifecycle

### In `docs/3.ai/`
- `01-npc-response-framework.md` - NPC behavior system
- `02-training-data-schema.md` - Training data format

### Root Documentation
- `docs/master_truths_canonical_spec_v_1_2.md` - **CANONICAL SPEC**
- `README.md` - Project overview

---

## 🧪 Testing Strategy

### Unit Tests
- Shared `game_logic` package (critical!)
- Relationship calculator validation
- Progression calculator validation
- Card play validators

### Integration Tests
- Flutter app: Card play flow
- Backend: API route tests
- End-to-end: Client → Backend → Firebase

### Load Tests
- Backend stress testing (Cloud Run scaling)
- Firestore query performance
- AI API rate limiting

---

## 📈 Performance Targets

| Metric | Target | Phase |
|--------|--------|-------|
| App Launch Time | < 3s | Phase 1 |
| Card Play Response | < 2s | Phase 3 |
| AI Latency (cloud) | < 3s | Phase 4 |
| AI Latency (local) | < 500ms | Phase 6+ |
| Memory Usage | < 200MB | All phases |
| Battery Drain | < 5%/30min | Phase 6+ |

---

## 🛠️ Tech Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|----------|
| **Frontend** | Flutter 3.24+ | Cross-platform UI |
| | **Flame 1.17+** | **Game engine (REQUIRED)** 🎮 |
| | Riverpod 2.5+ | State management |
| | go_router | Navigation |
| | Hive | Local storage |
| **Backend** | Dart Frog | API server |
| | Cloud Run | Auto-scaling hosting |
| | OpenAI/Anthropic | Cloud AI generation |
| **Data** | Firestore | Database (NoSQL) |
| | Firebase Auth | Authentication |
| | Cloud Storage | Asset storage |
| **Shared** | game_logic package | Shared Dart code |
| **Future** | TensorFlow Lite | Local AI (Phase 6+) |

---

## 📋 Compliance Checklist

All architecture follows Master Truths v1.2:

- [x] Uses canonical vocab & scales (Levels 0-5; Trust 0.0-1.0; Capacity 0.0-10.0)
- [x] Season = 12/24/36w; 3 turns/day
- [x] Relationship Level 0 = "Not Met" (internal only)
- [x] Level-up requires BOTH interaction count AND trust threshold
- [x] NPC Response Framework: OCEAN → Urgency(1-5x) → Trust(0.5-2.0x) → Capacity
- [x] Backend-authoritative for game state
- [x] Training data collected for all AI interactions
- [x] Full-stack Dart architecture (I/O FLIP pattern)

---

## 🎯 Next Steps

1. ✅ **Review I/O FLIP Analysis** - Understand architecture foundation
2. ✅ **Read Implementation Plan** - Understand phase structure
3. ✅ **Set up Flutter Project** - Follow setup guide
4. ⏳ **Begin Phase 1** - Foundation (Weeks 1-4)
5. ⏳ **Set up Dart Frog Backend** - Phase 2 (Weeks 5-8)

---

**Document Version**: 2.0  
**Last Updated**: October 14, 2025  
**Status**: Ready for implementation  
**Architecture**: Based on I/O FLIP patterns

---

## 📖 Document Index

All architecture documentation in this folder:

1. **`IO-FLIP-ARCHITECTURE-ANALYSIS.md`** ⭐ START HERE
   - Complete I/O FLIP architecture breakdown
   - Adaptation patterns for Unwritten
   - Frontend, backend, data layers
   - Deployment strategies

2. **`IMPLEMENTATION-PLAN-MVP.md`** ⭐ IMPLEMENTATION GUIDE
   - 6-phase implementation timeline
   - Detailed deliverables per phase
   - Code examples and patterns
   - Success criteria

3. **`FLUTTER-PROJECT-SETUP.md`** ⭐ SETUP GUIDE
   - Step-by-step Flutter setup
   - Dependencies and configuration
   - Initial project files
   - Verification steps

4. **`tech_architecture_doc.md`**
   - Deep technical architecture
   - Database schemas
   - Performance optimization
   - Scalability patterns

5. **`QUICK-START-DEVELOPER-GUIDE.md`**
   - Quick reference for developers
   - Common commands
   - File locations

6. **`IMPLEMENTATION-DELIVERABLES-SUMMARY.md`**
   - High-level deliverables summary
   - Milestone checklist

7. **`CARD-DRAG-PHYSICS-GUIDE.md`** ⭐ NEW
   - Card drag animations (how I/O FLIP does it)
   - Flame physics components
   - Pure Flutter alternative
   - Implementation recommendations

8. **`ARCHITECTURE-README.md`** (this file)
   - Navigation guide
   - Architecture overview
   - Getting started paths


