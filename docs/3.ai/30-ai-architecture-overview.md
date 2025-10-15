# AI Architecture Overview

**Purpose:** Strategic decisions and high-level architecture  
**Audience:** Everyone - start here  
**Status:** ✅ Complete  
**Related:** → 31-hybrid-cloud-local-system.md for implementation details

---

## What This Document Covers

This is the **strategic overview** of Unwritten's AI system. After reading this, you'll understand:
- Why we chose a hybrid cloud-local architecture
- What technologies power the system
- Key constraints and targets
- How routing decisions are made
- What's possible and what's not

---

## The Core Challenge

### What We're Building

**Goal:** NPCs that feel like real people
- Evolve based on player interactions
- Remember past experiences
- Show authentic emotions
- Display consistent personalities
- Respond naturally in real-time

**Scale:**
- 50+ unique character NPCs per playthrough
- 10,000+ interactions per player
- 3,000+ weeks of simulated time
- Continuous evolution without contradictions

**Constraints:**
- Mobile devices (limited compute)
- Battery life (<1% drain per 30min)
- Cost sustainability ($2-4 per player/month)
- Real-time feel (<100ms for routine, <3s hidden for important)
- Works offline for basic gameplay

---

## The Architecture Decision

### Why Hybrid? (Not Cloud-Only or Local-Only)

```
┌──────────────────────────────────────────────────────────┐
│               THE HYBRID SOLUTION                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  CLOUD AI                  ⚖️              LOCAL AI      │
│  ├─ Quality ✓                              ├─ Speed ✓   │
│  ├─ Complex reasoning ✓                    ├─ Free ✓    │
│  ├─ Rich personalities ✓                   ├─ Offline ✓ │
│  ├─ 2-5 seconds ✗                          ├─ 90ms ✓    │
│  └─ $0.03 per call ✗                       └─ Limited ✗ │
│                                                          │
│  SMART ROUTING DECIDES WHICH TO USE                     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Three Rejected Approaches

**❌ Approach 1: Cloud AI Only (Claude/GPT-4)**
```
Pros:
✓ Highest quality generations
✓ Complex personality modeling
✓ Deep emotional understanding

Cons:
✗ Cost: $75-150 per player/month (unsustainable)
✗ Latency: 2-15 seconds per interaction
✗ Requires internet always
✗ Privacy concerns
✗ API rate limits
```

**❌ Approach 2: Local AI Only (On-Device)**
```
Pros:
✓ Free (no API costs)
✓ Fast (90ms)
✓ Works offline
✓ Privacy-friendly

Cons:
✗ Quality: Cannot match GPT-4/Claude
✗ Model size: 2-3GB (too large)
✗ Reasoning: Limited complex thought
✗ Consistency: Hard to maintain across NPCs
✗ Evolution: Shallow personality changes
```

**❌ Approach 3: Fully Pre-Generated Content**
```
Pros:
✓ No latency
✓ No cost
✓ Guaranteed quality

Cons:
✗ Not reactive to player choices
✗ Feels scripted and static
✗ Impossible to pre-generate all combinations
✗ Defeats the core promise of the game
```

### ✅ Our Solution: Smart Hybrid Architecture

```
ROUTING LOGIC:
┌─────────────────┐
│ Player Action   │
└────────┬────────┘
         ↓
    ┌────────────┐
    │ Importance │
    │ Assessment │
    └─────┬──────┘
          ↓
    ┌─────────────────┐
    │  < 0.3: LOW     │ → LOCAL AI (90ms, free)
    │  0.3-0.7: MED   │ → HYBRID (local first, cloud enhance)
    │  > 0.7: HIGH    │ → CLOUD AI (2-5s, quality)
    └─────────────────┘
          ↓
    ┌────────────┐
    │ Cache Check│
    └─────┬──────┘
          ↓
    [Pre-generated? → 0ms]
    [Not cached? → Generate now]
```

**Result:**
- 70-85% interactions: Local AI (instant, free)
- 15-30% interactions: Cloud AI (quality, $2-4/month)
- 60-70% cache hit rate (pre-generated)
- 90% of interactions feel instant to player

---

## NPC Response Framework *(Master Truths v1.2)*

### The Core Behavioral System

**This is the foundation of how NPCs respond to player actions.** Every interaction is filtered through a prioritized hierarchy that determines impact and behavior.

> **Critical Truth:** NPCs don't respond the same way to the same action. Response depends on THEIR personality, THEIR current urgency, YOUR relationship history, and THEIR emotional capacity.

### The Response Hierarchy

```
┌────────────────────────────────────────────────────────────┐
│          HOW NPCS RESPOND TO PLAYER ACTIONS                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. OCEAN PERSONALITY (Primary Filter)                    │
│     ├─ Agreeableness: Forgiving vs. Harsh                │
│     ├─ Neuroticism: Stable vs. Anxious                   │
│     ├─ Sets BASELINE response tendency                   │
│     └─ Example: Low-C NPC doesn't care (usually)         │
│                                                            │
│  2. SITUATIONAL URGENCY (Multiplier - CAN OVERRIDE)       │
│     ├─ Routine:   1x (no amplification)                  │
│     ├─ Important: 2x (moderate amplification)            │
│     ├─ Urgent:    3x (strong amplification)              │
│     ├─ Crisis:    5x (MAXIMUM amplification)             │
│     └─ Crisis OVERRIDES personality indifference         │
│                                                            │
│  3. RELATIONSHIP HISTORY (Modifier)                       │
│     ├─ Trust level: 0.0-1.0                              │
│     ├─ Modifier range: 0.5x (low) to 2x (high)          │
│     ├─ High trust = cushions negative actions            │
│     └─ Low trust = amplifies negative actions            │
│                                                            │
│  4. EMOTIONAL CAPACITY (Constraint)                       │
│     ├─ Scale: 0-10 (0 = depleted, 10 = thriving)        │
│     ├─ LIMITS available responses regardless of desire   │
│     ├─ Low capacity = can't process nuance               │
│     └─ Character at 2.5/10 CANNOT act like 8/10          │
│                                                            │
│  5. MEMORY RESONANCE (Context)                            │
│     ├─ Past trauma triggers: 0.95 weight                 │
│     ├─ Opposite emotion growth: 0.9 weight               │
│     ├─ Same emotion pattern: 0.8 weight                  │
│     └─ Amplifies or dampens based on history             │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### The Formula

```javascript
Response_Impact = Base_Personality_Response 
                  × Situational_Urgency_Multiplier (1x-5x)
                  × Relationship_Trust_Modifier (0.5x-2x)
                  × Memory_Resonance_Factor (0.7x-0.95x if applicable)
                  ÷ Emotional_Capacity_Constraint (caps maximum)
```

### Why This Matters for AI Design

**Traditional Approach (WRONG):**
```javascript
// Fixed scoring - same action always has same impact
player.declineHelp() → character.trust -= 0.5;
```

**Unwritten Approach (CORRECT):**
```javascript
// Dynamic scoring based on context
const baseResponse = -0.5;  // Declining help
const urgency = assessUrgency(situation);  // 1x-5x
const personality = character.agreeableness;  // 0-1
const trust = character.trustLevel;  // 0-1
const capacity = character.emotionalCapacity;  // 0-10

const impact = baseResponse 
  × (personality < 0.5 ? 1.4 : 0.6)  // Low A = harsher
  × urgency  // Crisis = 5x amplification!
  × (trust > 0.7 ? 1.2 : 0.8)  // Trust affects interpretation
  × (capacity < 5 ? 1.1 : 0.9);  // Low capacity hardens judgment

// Result: Same action, wildly different impacts:
// Routine + high A + high trust + high capacity = -0.18
// Crisis + low A + low trust + low capacity = -2.8
```

### Example: The Power of Urgency Multipliers

**Scenario:** Player declines to help Sarah move apartments

**Sarah's State:**
- **Personality:** Agreeableness 0.8 (very forgiving)
- **Relationship:** Trust 0.65 (moderate-high)
- **Capacity:** 3.85/10 (low - stressed about move)

**Case A: Routine Context (1x multiplier)**
```
You decline casual coffee next week.

Calculation:
base -0.5 × agreeableness 0.7 × urgency 1x × trust 1.2 = -0.42
Tier: MINOR HARM
Response: "No worries! Maybe next time."
Recovery: Same day
```

**Case B: Crisis Context (5x multiplier)**
```
You decline helping her move THIS WEEKEND (she's desperate).

Calculation:
base -0.5 × agreeableness 0.7 × urgency 5x × trust 1.2 × capacity 0.9 = -1.89
Tier: MAJOR HARM
Response: "Oh. I... I really needed you. I'll figure something out."
Recovery: 2-3 weeks
```

**Same NPC, same base personality, WILDLY different impact.**

This is why the hybrid AI system must track urgency levels and apply multipliers.

### Urgency Assessment in AI Generation

**When generating NPC responses, always assess:**

```javascript
function assessUrgency(context) {
  // Check multiple factors
  const timeConstraints = context.deadline < 7 ? 2 : 0;  // Days
  const emotionalStakes = context.emotionalWeight;  // 0-10
  const lifeImpact = context.impactLevel;  // 0-10
  const dependence = context.needLevel;  // 0-10
  
  const score = (
    timeConstraints * 0.3 +
    emotionalStakes * 0.3 +
    lifeImpact * 0.2 +
    dependence * 0.2
  );
  
  // Map to multiplier
  if (score < 0.3) return { level: "routine", multiplier: 1.0 };
  if (score < 0.5) return { level: "important", multiplier: 2.0 };
  if (score < 0.7) return { level: "urgent", multiplier: 3.0 };
  return { level: "crisis", multiplier: 5.0 };
}
```

### Integration with Hybrid Architecture

**The Response Framework affects routing decisions:**

```javascript
// In AI Router
function determineRoute(context, player) {
  // NEW: Assess urgency FIRST
  const urgency = assessUrgency(context);
  const importance = calculateImportance(context);
  
  // Apply urgency multiplier to importance
  const adjustedImportance = importance * urgency.multiplier;
  
  // High urgency can push routine interactions to cloud AI
  if (adjustedImportance > 0.7) {
    return "CLOUD";  // Crisis needs premium quality
  }
  
  if (adjustedImportance < 0.3) {
    return "LOCAL";  // Routine stays fast and free
  }
  
  return "HYBRID";  // Medium importance
}
```

### Capacity Constraints in Generation

**Characters cannot exceed their capacity:**

```javascript
function validateResponse(response, character) {
  const supportNeeded = assessSupportLevel(response);
  const maxSupport = character.capacity + 2;  // Master Truths rule
  
  if (supportNeeded > maxSupport) {
    return {
      valid: false,
      reason: "Response exceeds capacity constraint",
      required: supportNeeded,
      available: maxSupport,
      suggestion: "Show authentic limitation instead"
    };
  }
  
  return { valid: true };
}
```

### Why This Is Critical for Cost Optimization

**Understanding urgency helps optimize cloud AI spending:**

- **Routine interactions (1x):** 70% of all interactions → Local AI → $0
- **Important interactions (2x):** 20% → Gemini Flash 2.5 → $0.00074 each
- **Urgent interactions (3x):** 8% → Gemini Flash 2.5 → $0.00074 each
- **Crisis interactions (5x):** 2% → Gemini 2.5 Pro → $0.0025 each

Without urgency tracking, you'd either:
- Use cloud AI for everything → 5x cost increase
- Use local AI for everything → poor quality on important moments

**The Response Framework enables smart spending.**

### Numerical Grounding Requirement

> **See:** `NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md` for complete system

Every trust impact calculation MUST include:

1. **Qualitative Anchor:** "This is major harm" → -1.5 to -2.0 range
2. **Explicit Calculation:** base × personality × urgency × trust × capacity
3. **Validation:** Does the dialogue match the numerical tier?

**Example:**
```json
{
  "relationship_impact": -1.9,
  
  "calculation": {
    "base": -0.5,
    "personality_modifier": 0.7,
    "urgency_multiplier": 5.0,
    "trust_modifier": 1.2,
    "capacity_factor": 0.9,
    "formula": "(-0.5 × 0.7 × 5.0 × 1.2 × 0.9) = -1.89 → -1.9"
  },
  
  "qualitative_tier": "MAJOR HARM (-1.5 to -2.0)",
  "narrative_markers": ["This really hurt", "Weeks to recover"],
  "recovery_time": "2-3 weeks",
  
  "validation": {
    "dialogue_matches_tier": true,
    "reasoning": "Response shows hurt without melodrama"
  }
}
```

**No more arbitrary numbers.** Every impact score is traceable and learnable.

---

## Technology Stack

### Cloud AI Models

**Primary: Gemini Flash 2.5**
```
Provider: Google
Use Case: Primary generation for most interactions
Strengths:
  ✓ Extremely fast (sub-second responses)
  ✓ Cost-effective ($0.30 per 1M input, $2.50 per 1M output)
  ✓ High quality for routine to medium complexity
  ✓ 1M token context window
  ✓ Multimodal capabilities
  ✓ Latest Flash iteration with improved quality
  
Costs: $0.30 per 1M input tokens, $2.50 per 1M output
Latency: 0.5-2 seconds typical
Average cost per generation: ~$0.0014 (assuming 500 input + 500 output tokens)
When to use: 
  - Routine evolutions (Level 1-3)
  - Standard interactions
  - Medium-importance moments
  - High-volume scenarios
```

**Premium: Gemini 2.5 Pro**
```
Provider: Google
Use Case: Complex, high-stakes moments requiring deep reasoning
Strengths:
  ✓ Superior reasoning and analysis
  ✓ Deep personality modeling
  ✓ Complex emotional understanding
  ✓ 2M token context window
  ✓ Handles nuanced character development
  
Costs: $1.25 per 1M input tokens, $3.75 per 1M output
Latency: 2-5 seconds typical
Average cost per generation: ~$0.0025 (assuming 500 input + 500 output tokens)
When to use:
  - Level 4-5 evolutions
  - Crisis responses
  - Defining relationship moments
  - Complex fusion outcomes
  - Multi-character interactions
  - When maximum reasoning and depth required
```

### Local AI Models

**Primary: Phi-3-mini (Quantized)**
```
Size: 2.3GB (4-bit quantized)
Speed: 15 tokens/sec on iPhone 15 Pro
Provider: Microsoft
Architecture: 3.8B parameters

Capabilities:
  ✓ Basic dialogue generation
  ✓ Simple personality responses
  ✓ Emotional state modeling
  ✗ Complex reasoning
  ✗ Long-context understanding
  ✗ Nuanced characterization

When to use:
  - Routine greetings (90ms)
  - Ambient dialogue (60ms)
  - Simple reactions (110ms)
  - Background NPC behavior
```

**Secondary: Gemma-2-2b**
```
Size: 2.5GB (4-bit quantized)
Speed: 18 tokens/sec on modern devices
Provider: Google
Architecture: 2B parameters

Capabilities:
  ✓ Very fast inference
  ✓ Good for short responses
  ✓ Efficient on-device
  ✗ Less nuanced than Phi-3
  
When to use:
  - Quick reactions
  - Choice label generation
  - Simple emotional responses
```

### Frameworks & Tools

**LiteRT (formerly TensorFlow Lite)**
```
Purpose: On-device model deployment
Platform: iOS, Android via Flutter
Features:
  - Hardware acceleration (Neural Engine, NNAPI)
  - INT4/INT2 quantization support
  - Optimized for mobile
  
Integration: tflite_flutter package
```

**PyTorch 2.x**
```
Purpose: Model training and conversion
Key Features:
  - torch.compile (40%+ speedup)
  - Better quantization support
  - AI Edge Torch converter
  
Version: 2.5+ required
```

**PEFT/LoRA**
```
Purpose: Parameter-efficient fine-tuning
Benefits:
  - 95% fewer trainable parameters
  - Faster training (days vs weeks)
  - Smaller models
  - Better multi-task learning
  
Library: peft==0.13.0
```

---

## System Architecture Flow

### Complete AI Pipeline

```
┌───────────────────────────────────────────────────────────┐
│                    PLAYER ACTION                          │
└──────────────────────┬────────────────────────────────────┘
                       ↓
┌───────────────────────────────────────────────────────────┐
│                  CONTEXT GATHERING                        │
│  • Character current state                                │
│  • Relationship history                                   │
│  • Recent memories                                        │
│  • Player's approach                                      │
│  • World state                                            │
└──────────────────────┬────────────────────────────────────┘
                       ↓
┌───────────────────────────────────────────────────────────┐
│                 IMPORTANCE ASSESSMENT                     │
│  Factors:                                                 │
│  • Relationship level change potential                    │
│  • Emotional weight                                       │
│  • Narrative significance                                 │
│  • Player engagement                                      │
│  → Importance Score: 0.0 to 1.0                          │
└──────────────────────┬────────────────────────────────────┘
                       ↓
┌───────────────────────────────────────────────────────────┐
│                  ROUTING DECISION                         │
│                                                           │
│  ┌──────────────┐  ┌────────────┐  ┌─────────────┐     │
│  │  < 0.3       │  │ 0.3 - 0.7  │  │   > 0.7     │     │
│  │  LOCAL AI    │  │  HYBRID    │  │  CLOUD AI   │     │
│  │  90ms, free  │  │ Local+Cloud│  │ 2-5s, quality│    │
│  └──────────────┘  └────────────┘  └─────────────┘     │
└──────────────────────┬────────────────────────────────────┘
                       ↓
┌───────────────────────────────────────────────────────────┐
│                  CACHE CHECK                              │
│  • Pre-generated for this scenario?                      │
│  • Template available?                                    │
│  → Cache Hit: 0ms (60-70% hit rate)                      │
│  → Cache Miss: Generate now                              │
└──────────────────────┬────────────────────────────────────┘
                       ↓
┌───────────────────────────────────────────────────────────┐
│                 PROMPT CONSTRUCTION                       │
│  • Select appropriate template                            │
│  • Inject full context                                    │
│  • Add constraints                                        │
│  • Include examples                                       │
└──────────────────────┬────────────────────────────────────┘
                       ↓
┌───────────────────────────────────────────────────────────┐
│                    GENERATION                             │
│  Local: Phi-3-mini on device                             │
│  Cloud: Claude Sonnet via API                            │
└──────────────────────┬────────────────────────────────────┘
                       ↓
┌───────────────────────────────────────────────────────────┐
│                VALIDATION & PARSING                       │
│  • Parse JSON response                                    │
│  • Validate structure                                     │
│  • Check coherence                                        │
│  • Detect contradictions                                  │
│  • Quality score (retry if < 0.75)                       │
└──────────────────────┬────────────────────────────────────┘
                       ↓
┌───────────────────────────────────────────────────────────┐
│                  CARD UPDATE                              │
│  • Update character state                                 │
│  • Add memory                                             │
│  • Adjust personality traits                              │
│  • Update description                                     │
│  • Save to database                                       │
└──────────────────────┬────────────────────────────────────┘
                       ↓
┌───────────────────────────────────────────────────────────┐
│            VISUAL/NARRATIVE RENDERING                     │
│  • Update card portrait                                   │
│  • Display dialogue                                       │
│  • Show evolution animation                               │
│  • Update relationship UI                                 │
└───────────────────────────────────────────────────────────┘
```

---

## Key Constraints & Targets

### Performance Targets

| Metric | Target | Minimum Acceptable | Why |
|--------|--------|-------------------|-----|
| **Inference Time (Local)** | 8-15ms | <20ms | 60 FPS gameplay |
| **Inference Time (Cloud)** | 2-5s (hidden) | <10s | Player patience |
| **Model Size** | 2-3MB | <5MB | App store limits |
| **Battery Drain** | <0.8% per 25 convos | <1.5% | All-day play |
| **Memory Usage** | <25MB | <40MB | Mid-range devices |
| **Cost per Free Player** | $0.12/month | <$0.50 | Free tier sustainability |
| **Cost per Essence Buyer** | $0.21-0.40/month | <$1.00 | Essence profitability |
| **Cost per Plus Sub** | $0.47/month | <$2.00 | Plus profitability |
| **Cost per Ultimate Sub** | $2.70/month | <$5.00 | Ultimate profitability |
| **Essence Profit Margin** | 98-99% | >90% | Business viability |

### Quality Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Personality Accuracy** | >87% | OCEAN trait prediction |
| **Sentiment Accuracy** | >92% | Emotion classification |
| **Coherence Score** | >0.85 | Internal consistency |
| **Player Satisfaction** | >4.2/5 | "NPCs feel real" survey |
| **Contradiction Rate** | <2% | Canonical fact violations |

### Cost Breakdown (Aligned with Essence Monetization)

**Actual Gemini Pricing (2025):**
- Gemini Flash 2.5: $0.30 input / $2.50 output per 1M tokens
- Gemini 2.5 Pro: $1.25 input / $3.75 output per 1M tokens

**Real-World Generation Costs:**
Based on actual measurements from 6,700-word chapter generation:
- Input: 7,267 tokens × $0.30/1M = $0.00218
- Output: 1,667 tokens × $2.50/1M = $0.00417
- **Total: $0.00635 per 6,700 words**

**Scaled to Unwritten Content:**
```
CARD EVOLUTION (500-800 words):
├─ Input: ~800 tokens × $0.30/1M = $0.00024
├─ Output: ~200 tokens × $2.50/1M = $0.00050
└─ Total cost: ~$0.00074 per evolution

MEMORY MOMENT (300-500 words):
├─ Input: ~500 tokens × $0.30/1M = $0.00015
├─ Output: ~150 tokens × $2.50/1M = $0.00038
└─ Total cost: ~$0.00053 per memory

PREMIUM SEASON BOOK (12-15k words):
├─ Input: ~14,000 tokens × $0.30/1M = $0.00420
├─ Output: ~3,000 tokens × $2.50/1M = $0.00750
└─ Total cost: ~$0.01170 per book
```

**Essence Pricing vs Actual Costs:**
```
┌─────────────────────────────────────────────────────────┐
│              ESSENCE REVENUE vs AI COST                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ PREMIUM CARD EVOLUTION:                                 │
│ • Price: 5 Essence (~$0.09-0.10 revenue)               │
│ • Cost: $0.00074 to generate                           │
│ • Profit: $0.089 per evolution                         │
│ • Margin: 99.2% 🎯                                      │
│                                                         │
│ PREMIUM MEMORY MOMENT:                                  │
│ • Price: 3 Essence (~$0.054-0.06 revenue)              │
│ • Cost: $0.00053 to generate                           │
│ • Profit: $0.054 per memory                            │
│ • Margin: 99.1% 🎯                                      │
│                                                         │
│ PREMIUM CARD ART:                                       │
│ • Price: 15 Essence (~$0.27-0.30 revenue)              │
│ • Cost: $0.04-0.06 (image generation)                  │
│ • Profit: $0.22-0.26 per image                         │
│ • Margin: 82-87% 🎯                                     │
│                                                         │
│ ANIMATED HOLO PORTRAIT:                                 │
│ • Price: 50 Essence (~$0.90-1.00 revenue)              │
│ • Cost: $0.10-0.15 (animation generation)              │
│ • Profit: $0.80-0.90 per holo                          │
│ • Margin: 85-90% 🎯                                     │
│                                                         │
│ PREMIUM SEASON BOOK:                                    │
│ • Price: 250 Essence (~$4.50-5.00 revenue)             │
│ • Cost: $0.01170 to generate                           │
│ • Profit: $4.488 per book                              │
│ • Margin: 99.8% 🎯🎯🎯                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Cost Per Player Tier (Monthly Averages):**

```
FREE PLAYERS (50% - 150,000 users):
├─ AI Usage: 95% local, 5% free Essence for cloud
├─ Monthly cloud calls: ~25 (from free 750 Essence)
├─ Cost: ~$0.02 in cloud AI per player
├─ Infrastructure: ~$0.10 per player
└─ Total cost: ~$0.12 per player
   Revenue: $0
   Subsidized by paying users ✓

OCCASIONAL ESSENCE BUYERS (25% - 75,000 users):
├─ Average spend: $15/month in Essence
├─ Cloud AI usage: ~150 generations/month
├─ Cost: ~$0.11 in cloud AI
├─ Infrastructure: ~$0.10
└─ Total cost: ~$0.21 per player
   Revenue: $15.00
   Profit: $14.79 per player (98.6% margin) ✓✓✓

REGULAR ESSENCE BUYERS (10% - 30,000 users):
├─ Average spend: $40/month in Essence
├─ Cloud AI usage: ~400 generations/month
├─ Cost: ~$0.30 in cloud AI
├─ Infrastructure: ~$0.10
└─ Total cost: ~$0.40 per player
   Revenue: $40.00
   Profit: $39.60 per player (99% margin) ✓✓✓

PLUS SUBSCRIBERS (8% - 24,000 users):
├─ Subscription: $14.99/month
├─ Usage: UNLIMITED cloud AI
├─ Typical usage: ~500 cloud generations/month
├─ Cost: ~$0.37 in cloud AI
├─ Infrastructure: ~$0.10
├─ Book discounts: 50% off (reduced revenue)
└─ Total cost: ~$0.47 per player
   Revenue: $14.99
   Profit: $14.52 per player (97% margin) ✓✓

ULTIMATE SUBSCRIBERS (4% - 12,000 users):
├─ Subscription: $29.99/month
├─ Usage: UNLIMITED everything
├─ Typical usage: ~800 cloud generations + art
├─ Cost: ~$0.60 cloud AI + ~$2.00 art generation
├─ Infrastructure: ~$0.10
└─ Total cost: ~$2.70 per player
   Revenue: $29.99
   Profit: $27.29 per player (91% margin) ✓✓
```

**KEY BUSINESS INSIGHTS:**

1. **Essence is MASSIVELY profitable** (98-99% margins)
2. **Subscriptions are highly profitable** (91-97% margins)
3. **Premium books have insane margins** (99.8%!)
4. **Art generation is the most expensive** (but still 85%+ margin)
5. **Free players cost ~$0.12/month** to support (totally sustainable)

**Why This Works:**
- Gemini Flash 2.5 is **extremely cheap** for text generation
- Essence pricing captures **perceived value** (quality upgrade)
- Players pay for **convenience and quality**, not raw API costs
- High margins fund development, marketing, infrastructure

---

## Decision Matrix (Monetization-Aware)

### How AI Routing Works with Essence System

**Critical Distinction:**
- **Free Players:** Choose LOCAL (free, 7/10) or CLOUD (5 Essence, 10/10) manually
- **Subscribers:** System automatically routes to best AI based on importance

```javascript
function determineAIRoute(context, player) {
  // Check player tier first
  if (player.tier === "FREE") {
    return handleFreePlayer(context, player);
  } else if (player.tier === "PLUS" || player.tier === "ULTIMATE") {
    return handleSubscriber(context, player);
  } else if (player.tier === "ESSENCE_BUYER") {
    return handleEssenceBuyer(context, player);
  }
}

// FREE PLAYERS: Manual choice with Essence prompt
function handleFreePlayer(context, player) {
  // Always generate with Local AI first
  const localResult = generateWithLocal(context);
  
  // For important moments, offer premium upgrade
  const importance = assessImportance(context);
  
  if (importance > 0.6) {
    return {
      route: "LOCAL_WITH_UPGRADE_PROMPT",
      result: localResult,
      prompt: {
        show: true,
        message: "Use 5 Essence for premium quality? (You have " + player.essence + ")",
        essenceCost: 5,
        qualityComparison: {
          free: "7/10 - Good, functional dialogue",
          premium: "10/10 - Rich, literary quality with depth"
        }
      },
      cost: 0  // Until they choose premium
    };
  }
  
  return {
    route: "LOCAL",
    result: localResult,
    cost: 0
  };
}

// ESSENCE BUYERS: Manual choice, but with Essence balance awareness
function handleEssenceBuyer(context, player) {
  const importance = assessImportance(context);
  
  // Smart prompting based on Essence balance and importance
  if (importance > 0.7 && player.essence >= 5) {
    return {
      route: "LOCAL_WITH_RECOMMENDATION",
      prompt: {
        show: true,
        message: "Important moment detected! Use 5 Essence for premium?",
        recommendation: "RECOMMENDED",
        essenceCost: 5
      }
    };
  }
  
  // Default to local
  return handleFreePlayer(context, player);
}

// SUBSCRIBERS: Automatic smart routing (no Essence costs)
function handleSubscriber(context, player) {
  const importance = assessImportance(context);
  
  // Category 1: Local AI (fast, routine)
  if (
    importance < 0.3 ||
    context.type === "ROUTINE_GREETING" ||
    context.type === "AMBIENT_DIALOGUE" ||
    context.type === "SIMPLE_REACTION"
  ) {
    return {
      route: "LOCAL",
      model: "phi-3-mini-q4",
      expectedLatency: "90ms",
      cost: 0,
      essenceCharged: 0  // Subscribers never pay Essence for AI
    };
  }
  
  // Category 2: Pre-generated (0ms, cached)
  if (isPredictable(context) || hasCachedTemplate(context)) {
    return {
      route: "CACHE",
      expectedLatency: "0ms",
      cost: 0,
      essenceCharged: 0
    };
  }
  
  // Category 3: Cloud AI (quality moments)
  if (
    importance > 0.7 ||
    context.relationshipLevelChange ||
    context.type === "CRISIS" ||
    context.type === "DEFINING_MOMENT"
  ) {
    // Use Gemini 2.5 Pro for complex/critical moments
    const useProModel = importance > 0.85 || context.type === "CRISIS";
    
    return {
      route: "CLOUD",
      model: useProModel ? "gemini-2.5-pro" : "gemini-flash-2.5",
      expectedLatency: useProModel ? "2-5s" : "0.5-2s",
      hideLatency: true,  // Use UX tricks
      cost: useProModel ? 0.0025 : 0.00074,  // Actual API cost
      essenceCharged: 0,  // Subscribers get unlimited
      subscriptionBenefit: true
    };
  }
  
  // Category 4: Medium importance - default to cloud for subscribers
  return {
    route: "CLOUD",
    model: "gemini-flash-2.5",
    expectedLatency: "0.5-2s",
    cost: 0.00074,
    essenceCharged: 0
  };
}

function assessImportance(context) {
  return (
    context.relationshipLevelChangePotential * 0.3 +
    context.emotionalWeight * 0.3 +
    context.playerEngagement * 0.2 +
    context.narrativeSignificance * 0.2
  );
}
```

### Essence Flow for Different Player Tiers

```
FREE PLAYER FLOW:
┌─────────────────┐
│ Card Evolution  │
└────────┬────────┘
         ↓
    [Generate with Local AI]
         ↓
    [Show result: 7/10 quality]
         ↓
    ┌────────────────────────┐
    │ Prompt: "Use 5 Essence │
    │ for premium quality?"  │
    │ [Yes] or [No, keep it] │
    └────────┬───────────────┘
             ↓
    [If Yes: Charge 5 Essence, regenerate with Gemini]
    [If No: Keep local version]

SUBSCRIBER FLOW:
┌─────────────────┐
│ Card Evolution  │
└────────┬────────┘
         ↓
    [Assess importance]
         ↓
    ┌────────────────────────┐
    │ Important? → Cloud AI  │
    │ Routine? → Local AI    │
    └────────┬───────────────┘
             ↓
    [No Essence charged]
    [Badge: "Subscriber Quality"]
```

### Routing Examples (By Player Tier)

**Example 1: Free Player - Routine Coffee Meetup**
```javascript
Player Tier: FREE (has 450 Essence saved)
Context:
  - Activity: "Coffee with Sarah"
  - Relationship: Level 2 (Acquaintance)
  - Player action: "Say hello"

System Flow:
1. Generate with Local AI (Phi-3-mini)
2. Show result: "Hey! Good to see you. Want your usual?"
3. Importance: 0.17 (low) → No premium prompt shown
4. Player sees local result, continues

Outcome:
  - Latency: 90ms
  - Cost: $0
  - Essence charged: 0
  - Quality: 7/10 - Perfectly fine for routine greeting
```

**Example 2: Free Player - Sarah's Crisis Call**
```javascript
Player Tier: FREE (has 450 Essence saved)
Context:
  - Activity: "Emergency call"
  - Relationship: Level 3 (Friend)
  - Player action: "Rush to help"
  - Situation: Sarah's bookshop funding fell through

System Flow:
1. Generate with Local AI first
2. Show result: "I... I don't know what to do. Everything's falling apart."
3. Importance: 0.90 (VERY HIGH)
4. System prompts: 
   ┌────────────────────────────────────────────┐
   │ ✨ PREMIUM QUALITY AVAILABLE                │
   │                                            │
   │ This is an important moment.               │
   │ Use 5 Essence for premium generation?     │
   │                                            │
   │ FREE (Current): 7/10 quality              │
   │ Functional, clear emotional response       │
   │                                            │
   │ PREMIUM (5 Essence): 10/10 quality       │
   │ Rich prose, deep emotional nuance,        │
   │ sensory details, multi-layered response   │
   │                                            │
   │ You have: 450 Essence                     │
   │                                            │
   │ [Use Premium] [Keep Free Version]         │
   └────────────────────────────────────────────┘

Player Choice A (Keep Free):
  - Cost: $0
  - Essence charged: 0
  - Quality: 7/10 - Good enough, crisis conveyed

Player Choice B (Use Premium):
  - Regenerate with Gemini 2.5 Pro
  - Latency: 3.2s (hidden with "Sarah is gathering her thoughts")
  - Cost to system: $0.0025
  - Essence charged: 5 (player now has 445)
  - Revenue: ~$0.09
  - Profit: $0.088 (97% margin)
  - Quality: 10/10 - Deeply emotional, literary quality
```

**Example 3: Plus Subscriber - Sarah's Crisis Call**
```javascript
Player Tier: PLUS ($14.99/month)
Context: Same crisis scenario

System Flow:
1. Assess importance: 0.90 (VERY HIGH)
2. Automatically route to Gemini 2.5 Pro
3. No prompt shown, no Essence charged
4. Generate premium quality automatically
5. Show badge: "✨ Subscriber Quality"

Outcome:
  - Latency: 3.2s (hidden with UX)
  - Cost to system: $0.0025
  - Essence charged: 0 (unlimited benefit)
  - Quality: 10/10 automatically
  - Player experience: "This is why I subscribe!"
```

**Example 4: Ultimate Subscriber - Any Interaction**
```javascript
Player Tier: ULTIMATE ($29.99/month)
Context: Even routine coffee meetup

System Flow:
1. Assess importance: 0.17 (low)
2. Still uses Local AI (fast enough)
3. BUT premium card art, animated holos all free
4. Premium books all free
5. Everything premium by default

Outcome:
  - AI: Mostly local (fast), cloud for important
  - Art: All premium (unlimited)
  - Books: All premium (unlimited)
  - Essence charged: Never (unlimited everything)
  - Player experience: "I never think about costs"
```

**Example 5: Essence Buyer - Strategic Premium Use**
```javascript
Player Tier: ESSENCE BUYER (bought $19.99 pack = 1,200 Essence)
Context: Various interactions over a week

Week Strategy:
  - Monday coffee: Local (save Essence)
  - Tuesday crisis: Premium (5 Essence) ✓
  - Wednesday chat: Local (routine)
  - Thursday memory: Premium (3 Essence) ✓
  - Friday meetup: Local
  - Saturday Level 4 evolution: Premium (5 Essence) ✓
  - Sunday animated holo: Premium (50 Essence) ✓

Total spent: 63 Essence
Remaining: 1,137 Essence
Cost to system: ~$0.047
Revenue from pack: $19.99
Player satisfaction: "I love choosing when to use premium!"
```

---

## What's Possible vs Impossible

### ✅ What Works Well

**Local AI Excels At:**
- Routine greetings and small talk
- Simple emotional reactions
- Background NPC behavior
- Quick choice generation
- Basic personality-appropriate responses

**Cloud AI Excels At:**
- **Gemini Flash 2.5:** Fast, cost-effective premium generations ($0.00074 each)
- **Gemini 2.5 Pro:** Deep character evolutions requiring complex reasoning ($0.0025 each)
- Complex emotional moments with nuanced understanding
- Crisis responses with appropriate emotional depth
- Personality modeling across time with consistency
- Narrative coherence across 3000+ weeks
- Multi-character relationship dynamics
- **Cost-effective enough for Essence monetization** (99% profit margins!)

**Hybrid System with Essence Monetization Excels At:**
- Cost optimization for free players (mostly local)
- Player choice (pay for quality when YOU want it)
- No subscription pressure (25 free Essence/day)
- Perceived instant responses (90% feel immediate)
- Offline basic functionality (local AI always works)
- Scaling to many NPCs (local handles routine, cloud handles important)
- Premium quality when it matters (and player chooses to spend)
- **Business sustainability** (98-99% margins on Essence purchases)

### ❌ What Doesn't Work

**Local AI Cannot:**
- Match Gemini 2.5 Pro quality for deep reasoning
- Handle complex personality reasoning
- Maintain long-term consistency alone
- Create deeply emotional moments
- Generate nuanced relationship dynamics

**Cloud AI Considerations:**
- **Gemini Flash:** Fast and affordable, but may lack depth for critical moments
- **Gemini 2.5 Pro:** Excellent quality but 10x cost of Flash (still affordable)
- Requires internet connection (mitigated by local fallback)
- Subject to API rate limits (manageable with caching)
- Latency requires UX strategies to hide

**Hybrid Limitations:**
- Complexity in implementation
- Need sophisticated routing logic
- Cache management overhead
- Quality gaps between local/cloud must be managed
- Requires fallbacks for all failure modes

---

## 2025 Technology Improvements

### What's New This Year

**LoRA/PEFT Training:**
```
Old (2024): Fine-tune entire model
  - Requires 24GB+ VRAM
  - 2-4 weeks training time
  - 100% of parameters trainable
  - Expensive compute costs

New (2025): LoRA fine-tuning
  - Requires 12GB VRAM
  - 1-2 weeks training time
  - 0.5-2% of parameters trainable
  - 70% cost reduction
```

**PyTorch 2.x Compilation:**
```
torch.compile(model, mode='max-autotune')
  - 40%+ faster training
  - 25%+ faster inference
  - No code changes required
  - Free performance boost
```

**INT4 Quantization:**
```
Old: INT8 quantization (4-5MB models)
New: INT4 quantization (2-3MB models)
  - 50% size reduction
  - 10% accuracy loss (acceptable)
  - Faster inference
  - Better battery life
```

**Gemma 3 270M Reference:**
```
Google's ultra-efficient model:
  - 270M parameters
  - 0.75% battery for 25 conversations
  - 15-20ms inference on Pixel
  - Proof that aggressive optimization works
```

---

## Implementation Phases

### MVP (Months 1-2)

**Focus:** Prove the concept
```
Strategy:
  - Cloud AI only (accept higher costs)
  - No local AI yet
  - Simple caching
  - Gather data on interaction patterns

Purpose:
  - Validate gameplay loop
  - Measure actual usage patterns
  - Test AI quality requirements
  - Identify optimization opportunities

Expected Costs: $50-100 per player (acceptable for MVP)
```

### Hybrid (Months 3-4)

**Focus:** Add local AI
```
Strategy:
  - Implement Phi-3-mini for routine interactions
  - Basic routing logic (simple importance assessment)
  - Pre-generation for common scenarios
  - UX tricks for latency hiding

Purpose:
  - Reduce costs to sustainable levels
  - Improve perceived responsiveness
  - Enable offline basic gameplay

Expected Costs: $15-25 per player
```

### Optimization (Months 5-6)

**Focus:** Fine-tune everything
```
Strategy:
  - Train custom local model on game data
  - Advanced caching strategies
  - Background generation pipeline
  - Optimize routing algorithm
  - A/B test quality vs cost tradeoffs

Purpose:
  - Hit target cost ($2-4 per player)
  - Maximize cache hit rate (70%+)
  - Perfect UX hiding of latency

Expected Costs: $4-7 per player
```

### Polish (Month 7+)

**Focus:** Production-ready
```
Strategy:
  - Progressive disclosure system
  - Advanced prediction algorithms
  - Streaming responses
  - Maximum optimization
  - Failover and edge case handling

Purpose:
  - Bulletproof reliability
  - Sub-target costs if possible
  - Perfect player experience

Expected Costs: $2-4 per player (target achieved)
```

---

## Success Metrics

### How We'll Measure Success

**Technical Metrics:**
- [ ] 90% of interactions feel instant (<100ms perceived)
- [ ] Local model inference <15ms
- [ ] Cloud calls <5s latency (when needed)
- [ ] Cache hit rate >60%
- [ ] Cost per player <$5/month
- [ ] Battery drain <1% per 30min
- [ ] Model size <3MB

**Quality Metrics:**
- [ ] Personality accuracy >87%
- [ ] Sentiment accuracy >92%
- [ ] Coherence score >0.85
- [ ] Contradiction rate <2%
- [ ] Player satisfaction >4.2/5

**Business Metrics:**
- [ ] Essence purchases highly profitable (98-99% margins) ✅
- [ ] Plus subscriptions profitable (97% margin) ✅
- [ ] Ultimate subscriptions profitable (91% margin) ✅
- [ ] Free players sustainable (cost $0.12/month) ✅
- [ ] Churn rate <15%/month
- [ ] Player reports "NPCs feel real"
- [ ] Average session length >30min

---

## Summary: AI Architecture + v1.2 Behavioral Systems + Essence Monetization

### The Complete Picture

**Technical Foundation:**
- Hybrid cloud + local AI architecture
- Gemini Flash 2.5 ($0.00074/generation) for premium content
- Gemini 2.5 Pro ($0.0025/generation) for critical moments
- Phi-3-mini local model (free, 7/10 quality) for routine
- **NPC Response Framework** for dynamic behavioral modeling

**Behavioral Systems (Master Truths v1.2):**
- **OCEAN → Urgency → Trust → Capacity** response hierarchy
- **Urgency multipliers (1x-5x)** amplify personality baselines
- **Numerical grounding** for all impact calculations (anchor → calculate → validate)
- **Emotional capacity constraints** (0-10 scale, support rule: capacity + 2)
- **Memory resonance** (0.7-0.95 weights) for contextual recall

**Monetization Integration:**
- **Free Players:** Local AI always, optional 5 Essence for cloud upgrade
- **Essence Buyers:** Strategic cloud use, player-controlled spending
- **Plus Subscribers:** Unlimited cloud AI, automatic smart routing
- **Ultimate Subscribers:** Unlimited everything, no cost considerations

**Business Validation:**
```
ACTUAL COSTS (Real-World Measurements):
├─ Card Evolution: $0.00074 to generate
├─ Memory Moment: $0.00053 to generate
├─ Season Book: $0.01170 to generate
└─ Total cost per player: $0.12 (free) to $2.70 (ultimate)

ESSENCE PRICING:
├─ Card Evolution: 5 Essence (~$0.09 revenue) = 99.2% margin
├─ Memory Moment: 3 Essence (~$0.054 revenue) = 99.1% margin
├─ Season Book: 250 Essence (~$4.50 revenue) = 99.8% margin
└─ Business is MASSIVELY profitable on Essence sales

SUBSCRIPTION PRICING:
├─ Plus: $14.99 revenue - $0.47 cost = 97% margin
├─ Ultimate: $29.99 revenue - $2.70 cost = 91% margin
└─ Subscriptions are highly sustainable
```

**Key Success Factors:**

1. **Gemini pricing makes this work**
   - $0.00074 per generation is cheap enough for 99% margins
   - Can offer "unlimited" to subscribers profitably

2. **Essence captures perceived value**
   - Players pay for quality upgrade (7/10 → 10/10)
   - Not paying for raw API costs
   - Strategic use keeps costs low, revenue high

3. **Hybrid architecture is essential**
   - Free players get good experience with local AI
   - Cloud AI reserved for premium/important moments
   - 95% of free player interactions cost nothing

4. **Player choice drives conversions**
   - Free players see quality difference
   - Strategic Essence use is satisfying
   - Subscriptions are natural upgrade for engaged players

**This architecture enables:**
- ✅ Complete free experience (470 cards, local AI)
- ✅ Optional premium quality (Essence system)
- ✅ Unlimited subscriptions (Plus/Ultimate)
- ✅ 98-99% profit margins on Essence
- ✅ 91-97% profit margins on subscriptions
- ✅ Business sustainability at 50k+ players

---

## Related Documents

**For detailed implementation:**
→ 31-hybrid-cloud-local-system.md

**For prompt quality:**
→ 32-prompt-engineering-principles.md  
→ 33-prompt-templates-library.md

**For training local models:**
→ 36-local-model-training.md  
→ 37-model-deployment-optimization.md

**For UX strategies:**
→ 38-latency-ux-strategies.md

**For cost optimization:**
→ 39-cost-performance-targets.md

---

**This architecture balances quality, cost, and performance to create NPCs that feel real while remaining financially sustainable.**

**With Gemini Flash 2.5 pricing, Master Truths v1.2 behavioral systems, and Essence monetization, we achieve:**
- 🎮 Complete free experience for all players
- 🧠 Dynamic NPC responses based on context (urgency × personality × capacity)
- 📊 Numerically grounded impact calculations (no arbitrary numbers)
- 💎 99% profit margins on premium Essence content
- ⭐ 91-97% margins on subscriptions
- 🏆 Business viability at just 50k players
- ✨ Sustainable, ethical monetization that respects players

**The numbers work. The behavioral systems are authentic. The experience is premium. The business is viable. 🎯**

---

## Compliance Checklist (Master Truths v1.2)

- [x] Uses canonical vocab & scales (Levels 0–5; Trust 0.0–1.0; Capacity 0.0-10.0)
- [x] Season = 12/24/36w (player choice at season start); 3 turns/day
- [x] **NPC Response Framework applied: OCEAN primary filter → Situational multiplier (1x-5x) → Relationship/capacity modifiers**
- [x] **Emotional capacity constraints respected (0-10 scale; support rule: capacity + 2)**
- [x] **Memory resonance factors applied to recall (weights: 0.7-0.95)**
- [x] **Numerical grounding required (anchor → calculate → validate for all impacts)**
- [x] Urgency multipliers integrated into routing and cost optimization
- [x] This doc cites **Truths v1.2** throughout

