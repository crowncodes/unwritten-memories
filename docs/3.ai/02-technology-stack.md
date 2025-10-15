# Technology Stack Overview

**Purpose:** Complete overview of AI models, frameworks, and pricing  
**Audience:** Technical leads, product managers, engineers  
**Status:** ✅ Active  
**Related:** ← 01-ai-strategy-overview.md | → 03-implementation-phases.md | 04-ai-approach-comparison.md

---

## Quick Summary

| Component | Technology | Cost | Use Case |
|-----------|------------|------|----------|
| **On-Device AI** | TensorFlow Lite (Phi-3/Gemma 2B) | FREE | Simple predictions (70-85% of interactions) |
| **Dev AI (Now)** | Firebase AI Logic + Gemini Flash 2.5 | $0.01/generation | Rapid content generation |
| **Production AI (Target)** | Genkit + Gemini Flash/Pro | $2-2.50/player/month | Complex generations |
| **Storage** | Firebase (Firestore + Cloud Storage) | $0.06/GB + $0.026/GB | AI outputs and metadata |
| **Backend** | Google Cloud Run (Python) | $0.25/player/month | Genkit hosting |

---

## Table of Contents

1. [On-Device AI Stack](#on-device-ai-stack)
2. [Cloud AI Stack](#cloud-ai-stack)
3. [Storage Stack](#storage-stack)
4. [Backend Stack](#backend-stack)
5. [Development Stack](#development-stack)
6. [Cost Summary](#cost-summary)
7. [Model Selection Guide](#model-selection-guide)

---

## On-Device AI Stack

### TensorFlow Lite (LiteRT)

**Purpose:** Free, instant predictions for 70-85% of interactions

#### Model Options

| Model | Size | Latency | Accuracy | Use Case |
|-------|------|---------|----------|----------|
| **Phi-3 (Custom LoRA)** | 2-3MB (INT4) | 8-15ms | 85-90% | Personality prediction, sentiment |
| **Gemma 2B (Quantized)** | 2-3MB (INT4) | 10-18ms | 87-92% | Dialogue classification |
| **Custom TFLite** | 2-3MB | 5-10ms | 80-85% | Simple routing decisions |

#### Flutter Integration

```dart
dependencies:
  tflite_flutter: ^0.10.0
```

**Framework:** TensorFlow 2.x → LiteRT conversion  
**Training:** PyTorch + LoRA/PEFT → ONNX → TFLite  
**Deployment:** Bundled with app (no download)

#### Performance Targets

- **Latency:** < 15ms (p95)
- **Battery:** < 1% per 30min session
- **Memory:** < 50MB RAM
- **Accuracy:** > 85%

**See:** `41-local-model-training.md` for complete training pipeline

---

## Cloud AI Stack

### Gemini Flash 2.5

**Purpose:** Fast, cost-effective AI for routine generations

| Metric | Value |
|--------|-------|
| **Latency** | 2-5 seconds (typical) |
| **Cost** | $0.075 per 1M input tokens<br>$0.30 per 1M output tokens |
| **Context Window** | 1M tokens |
| **Rate Limit** | 2000 RPM (requests per minute) |
| **Best For** | Simple dialogues, card descriptions, routine interactions |

#### Example Cost

```
Typical dialogue generation:
- Input: 500 tokens (context + prompt)
- Output: 150 tokens (dialogue)
- Cost: $0.0000375 (input) + $0.000045 (output) = $0.0000825 per generation

1000 generations: $0.0825
```

### Gemini 2.5 Pro

**Purpose:** High-quality AI for complex generations

| Metric | Value |
|--------|-------|
| **Latency** | 5-10 seconds (typical) |
| **Cost** | $1.25 per 1M input tokens<br>$5.00 per 1M output tokens |
| **Context Window** | 2M tokens |
| **Rate Limit** | 1000 RPM |
| **Best For** | Card evolution, story progression, complex dialogue |

#### Example Cost

```
Card evolution (Level 3→4):
- Input: 2000 tokens (full context + history)
- Output: 500 tokens (detailed evolution)
- Cost: $0.0025 (input) + $0.0025 (output) = $0.005 per evolution

100 evolutions: $0.50
```

### Image Generation: Imagen 3

**Purpose:** AI-generated card art and visual assets

| Metric | Value |
|--------|-------|
| **Latency** | 10-20 seconds |
| **Cost** | $0.040 per image (1024x1024) |
| **SDK** | Google AI SDK (not Vertex AI) |
| **Quality** | High (Imagen 3) |

**See:** `80-image-generation-sdk-change.md` for why we use Google AI SDK

#### Example Cost

```
200 unique cards × 2 variants = 400 images
400 × $0.040 = $16.00 (one-time cost)

Monthly regeneration: 10 images × $0.040 = $0.40/month
```

### Video Generation (Future)

**Purpose:** Card evolution animations, story cutscenes

| Metric | Value |
|--------|-------|
| **Provider** | Google Veo (when available) |
| **Latency** | TBD |
| **Cost** | TBD (estimated $0.10-0.50 per video) |
| **Status** | Not yet available |

### Audio Generation (Current)

**Purpose:** Music stems, ambient audio

| Metric | Value |
|--------|-------|
| **Provider** | Google Lyria (AI Studio Cloud Function) |
| **Latency** | 30-60 seconds |
| **Cost** | $0.10 per stem (estimated) |
| **Status** | ✅ 1 Cloud Function operational |

**See:** `docs/9.music/MUSIC_SYSTEM_IMPLEMENTATION.md` for complete setup

---

## Storage Stack

### Firebase Firestore

**Purpose:** AI output metadata and game state

| Metric | Value |
|--------|-------|
| **Cost** | $0.06 per 100K documents read<br>$0.18 per 100K documents write |
| **Free Tier** | 50K reads/day, 20K writes/day |
| **Best For** | Dialogue metadata, card state, player history |

#### Storage Schema Example

```javascript
// Firestore: ai_outputs/{user_id}/dialogues/{dialogue_id}
{
  card_id: "card_123",
  text: "I understand how you feel...",
  generated_at: Timestamp,
  model: "gemini-2.5-flash",
  cost_usd: 0.0000825,
  personality_traits: {
    openness: 0.75,
    conscientiousness: 0.60,
    // ...
  },
  cached: false
}
```

**See:** `50-ai-output-storage-system.md` for complete architecture

### Firebase Cloud Storage

**Purpose:** AI-generated assets (images, audio, video)

| Metric | Value |
|--------|-------|
| **Cost** | $0.026 per GB stored<br>$0.12 per GB downloaded |
| **Free Tier** | 5GB storage, 1GB/day download |
| **Best For** | Images, audio stems, video clips |

#### Storage Structure

```
users/{user_id}/
  ai_generated/
    images/
      card_123_portrait.webp
      card_123_action.webp
    audio/
      stems/
        bass_stem_001.opus
        drums_stem_001.opus
    video/
      evolution_3_to_4.mp4
```

### Local Cache (Hive)

**Purpose:** Offline-first, instant retrieval

| Metric | Value |
|--------|-------|
| **Cost** | FREE (local storage) |
| **Latency** | < 1ms |
| **Capacity** | 50-100MB (configurable) |
| **Best For** | Recently used dialogues, card data |

```dart
dependencies:
  hive: ^2.2.3
  hive_flutter: ^1.1.0
```

**See:** `52-local-cache-implementation.md` for complete implementation

---

## Backend Stack

### Google Cloud Run

**Purpose:** Host Genkit backend (production)

| Metric | Value |
|--------|-------|
| **Cost** | $0.00002400 per vCPU-second<br>$0.00000250 per GiB-second |
| **Free Tier** | 2M requests/month, 360K vCPU-seconds |
| **Estimated Cost** | $0.25/player/month (100K players) |
| **Best For** | Genkit flows, RAG, tool calling |

#### Container Specs

```dockerfile
FROM python:3.11-slim
# 1 vCPU, 512MB RAM
# Auto-scaling: 0-100 instances
```

### FastAPI (Python)

**Purpose:** HTTP API for Genkit flows

```python
dependencies = [
    "fastapi==0.104.1",
    "genkit==0.5.0",
    "google-genkit-ai==0.5.0",
    "pydantic==2.5.0",
    "gunicorn==21.2.0",
]
```

**See:** `30-genkit-architecture.md` for complete backend structure

---

## Development Stack

### Firebase AI Logic (Current - Phase 1)

**Purpose:** Rapid content generation during development

| Metric | Value |
|--------|-------|
| **SDK** | `firebase_ai: ^3.4.0` (Flutter) |
| **Cost** | Same as Gemini (direct API) |
| **Latency** | 2-5 seconds |
| **Setup Time** | 2-4 hours |
| **Best For** | Dev content generation, prototyping |

```dart
dependencies:
  firebase_ai: ^3.4.0
  firebase_core: ^3.11.0
  firebase_app_check: ^0.3.0
```

**⚠️ Critical:** App Check REQUIRED for security

**See:** `21-firebase-ai-quick-start.md` for 30-minute setup

### Training Pipeline (Python)

**Purpose:** Train local TFLite models

```python
dependencies = [
    "torch==2.2.0",
    "transformers==4.36.0",
    "peft==0.8.0",  # LoRA/PEFT
    "optimum==1.16.0",  # ONNX conversion
    "ai-edge-torch==0.1.0",  # LiteRT conversion
]
```

**See:** `41-local-model-training.md` for complete pipeline

---

## Cost Summary

### Per-Player Monthly Cost Target: $2.00 - $2.50

#### Breakdown

| Component | Cost/Player/Month | Percentage |
|-----------|-------------------|------------|
| **Gemini Flash** | $1.50 | 60% |
| **Gemini Pro** | $0.75 | 30% |
| **Cloud Run** | $0.25 | 10% |
| **Firestore** | $0.10 | 4% |
| **Cloud Storage** | $0.05 | 2% |
| **Image Generation** | $0.004 | <1% |
| **Total (Before Optimization)** | **$2.65** | **106%** |
| | | |
| **Caching Savings** | -$0.50 | -20% |
| **Local AI Savings** | -$0.40 | -16% |
| **Smart Routing** | -$0.25 | -10% |
| **Total (After Optimization)** | **$1.50** | **60%** |

### At Scale (100K Players)

| Metric | Value |
|--------|-------|
| **Monthly AI Cost** | $150,000 |
| **Annual AI Cost** | $1,800,000 |
| **Target Revenue** | $5-10 per player/month (Essence) |
| **Profit Margin** | 70-80% after AI costs |

**See:** `71-cost-performance-targets.md` for optimization strategies

---

## Model Selection Guide

### Decision Tree

```
User Interaction
    ↓
Is it simple prediction? (sentiment, personality, classification)
    ├─ YES → TFLite (local, free, instant)
    └─ NO → Continue
        ↓
Is it routine dialogue? (greeting, simple response)
    ├─ YES → Gemini Flash 2.5 (fast, cheap)
    └─ NO → Continue
        ↓
Is it complex generation? (evolution, story, deep dialogue)
    └─ YES → Gemini 2.5 Pro (high quality)
```

### Feature-by-Feature Recommendations

| Feature | Model | Reason |
|---------|-------|--------|
| **Sentiment Analysis** | TFLite | Simple classification, free |
| **Personality Prediction** | TFLite | 5 scores (OCEAN), free |
| **Dialogue Classification** | TFLite | Route to local/cloud |
| **Simple Greeting** | Gemini Flash | Quick, contextual |
| **Routine Dialogue** | Gemini Flash | Cost-effective |
| **Card Evolution** | Gemini Pro | Complex, important |
| **Story Progression** | Gemini Pro | Deep context needed |
| **Crisis Response** | Gemini Pro | High quality critical |
| **Image Generation** | Imagen 3 | Visual quality |
| **Music Stems** | Lyria | Audio generation |

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| Oct 2025 | 1.0 | Initial technology stack documentation |
| TBD | 1.1 | Add Veo (video generation) when available |

---

## Related Documentation

- **01-ai-strategy-overview.md** - High-level AI strategy
- **03-implementation-phases.md** - Development timeline and phases
- **04-ai-approach-comparison.md** - Technology comparison (TFLite vs Firebase vs Genkit)
- **20-firebase-ai-integration.md** - Firebase AI Logic complete reference
- **30-genkit-architecture.md** - Genkit backend architecture
- **41-local-model-training.md** - TFLite model training
- **71-cost-performance-targets.md** - Cost optimization strategies

---

**Status:** ✅ Complete  
**Last Updated:** October 2025  
**Next Review:** Quarterly (or when new models released)


