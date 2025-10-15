# Expansion Pack Specifications - Post-Launch Content

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete specifications for 8 expansion pack families with content breakdown, mechanics, pricing, and capacity considerations

**References:**
- **Base Cards:** `20-base-card-catalog.md` (core 480 cards)
- **Monetization:** `1.concept/17-monetization-model.md` (pricing strategy)
- **Card Generation:** `24-card-generation-guidelines.md` (expansion card generation)

---

## Overview

**Expansion packs** add new aspirations, NPCs, activities, locations, and mechanics to the base game. Each pack is thematically cohesive and adds 40-60 hours of new content.

**Launch Year Plan:**
- **Launch (Month 0):** Base game (480 cards, 90 aspirations)
- **Month 3:** First expansion pack
- **Month 6:** Second expansion pack
- **Month 9:** Third expansion pack
- **Month 12:** Major expansion + Year 2 roadmap

**Pricing:**
- **Small Pack:** $4.99 (30-40 cards, 5-8 aspirations)
- **Standard Pack:** $7.99 (50-60 cards, 10-12 aspirations)
- **Major Expansion:** $12.99 (80-100 cards, 15-20 aspirations, new mechanics)

---

## Expansion Pack Architecture

### Standard Pack Structure

```typescript
interface ExpansionPack {
  id: string;
  name: string;
  category: "Career" | "Relationship" | "Lifestyle" | "Creative" | "Culture" | "Fantasy";
  size: "small" | "standard" | "major";
  
  content: {
    // Cards
    aspiration_cards: number;          // 5-20 new major aspirations
    character_cards: number;           // 10-20 new NPCs
    activity_cards: number;            // 20-40 new activities
    location_cards: number;            // 5-10 new locations
    system_cards: number;              // 5-10 (mechanics-specific)
    
    total_cards: number;               // 50-100 cards
  };
  
  mechanics: {
    new_systems?: string[];            // e.g., "Pet ownership", "Language fluency"
    new_fusion_types?: string[];
    new_meters?: string[];
  };
  
  integration: {
    compatible_life_directions: string[];
    unlocked_by?: string;              // e.g., "Complete Season 2"
    synergy_with_packs?: string[];
  };
  
  pricing: {
    usd: number;
    essence_alternative: number;       // Can buy with in-game currency
    plus_discount: number;             // Plus subscribers get 20% off
  };
}
```

---

## EXPANSION CATEGORY 1: CAREER & AMBITION (3 Packs)

### PACK-CAR-001: "Tech Startup"

```javascript
{
  id: "exp_tech_startup",
  name: "Tech Startup",
  category: "Career",
  size: "standard",
  
  content: {
    aspiration_cards: 12,
    character_cards: 15,
    activity_cards: 35,
    location_cards: 8,
    system_cards: 10,
    total_cards: 80
  },
  
  theme: "Launch and scale a tech startup in Silicon Valley culture",
  
  new_aspirations: [
    {
      name: "Launch SaaS Startup",
      duration: 36,
      difficulty: "very_hard",
      milestones: [
        "Validate idea with 10 customer interviews",
        "Build MVP in 12 weeks",
        "Launch to first 100 users",
        "Reach $10K MRR",
        "Raise seed funding OR bootstrap to profitability"
      ],
      success_rewards: [
        "Income: $5K-50K/month (variable)",
        "Unlock: VC pitch opportunities",
        "Reputation: Tech entrepreneur +10",
        "Skill: Programming +2.0, Business +2.5"
      ]
    },
    
    {
      name: "Get Hired at FAANG",
      duration: 24,
      difficulty: "very_hard",
      requires: { skills: { programming: 7 } }
    },
    
    {
      name: "Become Engineering Manager",
      duration: 16,
      requires: { current_job: "Senior Engineer" }
    },
    
    // ... 9 more tech career aspirations
  ],
  
  new_npcs: [
    {
      name: "Priya Sharma",
      role: "Co-founder candidate",
      personality: "Ambitious technical founder (O:4.5, C:4.8, E:3.9, A:3.2, N:3.4)",
      arc: "From colleague → co-founder → potential conflict over company direction"
    },
    {
      name: "David Chen",
      role: "VC investor",
      personality: "Sharp, pattern-matching investor",
      unlock: "When pitching for funding"
    },
    {
      name: "Alex Rodriguez",
      role: "Mentor (exited founder)",
      personality: "Experienced, seen it all, honest advice"
    }
    // ... 12 more tech NPCs
  ],
  
  new_activities: [
    "Code New Feature (3h, -2 Energy, +Programming)",
    "Customer Development Interview (2h, +Validation, -Comfort Zone)",
    "Pitch to Investors (4h, -3 Energy, high stakes)",
    "Hackathon Weekend (8h, -4 Energy, breakthrough potential)",
    "Debug Production Crisis (variable time, high stress)",
    // ... 30 more activities
  ],
  
  new_locations: [
    "Co-working Space (flexible work, network opportunities)",
    "Sand Hill Road VC Office (intimidating, high stakes)",
    "Tech Conference (inspiration, networking)",
    "Your Apartment (basement startup vibes)"
  ],
  
  new_mechanics: {
    startup_metrics: {
      description: "Track MRR, user growth, runway",
      affects: "Funding opportunities, stress level, success probability"
    },
    
    co_founder_relationship: {
      description: "Special relationship type with unique tensions",
      mechanics: "Can have conflicts over equity, direction, work/life"
    },
    
    technical_debt: {
      description: "Move fast = accumulate debt, must be paid eventually",
      consequence: "High debt = higher failure chance"
    }
  },
  
  pricing: {
    usd: 7.99,
    essence_alternative: 800,
    plus_discount: 6.39
  },
  
  target_audience: "Players interested in entrepreneurship, tech careers, startup culture"
}
```

---

### PACK-CAR-002: "Medical Professional"

```javascript
{
  id: "exp_medical",
  name: "Medical Professional",
  category: "Career",
  size: "major",
  
  content: {
    aspiration_cards: 18,
    character_cards: 20,
    activity_cards: 45,
    location_cards: 10,
    system_cards: 15,
    total_cards: 108
  },
  
  theme: "Medicine from med school to attending physician",
  
  new_aspirations: [
    {
      name: "Survive Medical School",
      duration: 52,                      // Full year season (special)
      difficulty: "extreme",
      requires: { prerequisites: "Bachelor's degree, high academic skill" },
      
      mechanics: "Intense time pressure, high stress, constant studying"
    },
    {
      name: "Complete Residency",
      duration: 36,
      difficulty: "very_hard",
      mechanics: "80+ hour weeks, life/death decisions, burnout risk"
    },
    {
      name: "Save a Life",
      duration: "event-triggered",
      emotional_weight: 10
    }
    // ... 15 more medical aspirations
  ],
  
  new_mechanics: {
    medical_cases: {
      description: "Procedurally generated patient cases",
      affects: "Skill growth, reputation, emotional toll"
    },
    
    life_death_decisions: {
      description: "High-stakes medical decisions",
      weight: "Major narrative beats, permanent emotional impact"
    },
    
    burnout_system: {
      description: "Extended version of burnout mechanic",
      unique_to_medical: "More severe, harder to recover"
    }
  },
  
  pricing: {
    usd: 12.99,
    essence_alternative: 1300,
    plus_discount: 10.39
  },
  
  content_warning: "Heavy themes: life/death, medical trauma, extreme stress",
  
  target_audience: "Players interested in medicine, high-stakes careers, intense narratives"
}
```

---

### PACK-CAR-003: "Teaching & Academia"

```javascript
{
  id: "exp_teaching",
  name: "Teaching & Academia",
  size: "standard",
  
  new_aspirations: [
    "Become High School Teacher",
    "Earn PhD",
    "Tenure Track Professor",
    "Transform a Student's Life",
    "Publish Research Paper"
  ],
  
  focus: "Teaching careers, mentorship, academic life",
  
  pricing: { usd: 7.99 }
}
```

---

## EXPANSION CATEGORY 2: RELATIONSHIP & SOCIAL (3 Packs)

### PACK-REL-001: "Parenthood"

```javascript
{
  id: "exp_parenthood",
  name: "Parenthood",
  category: "Relationship",
  size: "major",
  
  content: {
    aspiration_cards: 15,
    character_cards: 8,                // Children NPCs (dynamic)
    activity_cards: 50,
    location_cards: 12,
    system_cards: 20,
    total_cards: 105
  },
  
  theme: "Raise children from infancy through adolescence",
  
  new_aspirations: [
    {
      name: "Prepare for Parenthood",
      duration: 24,
      includes: "Nursery prep, financial planning, relationship strengthening"
    },
    {
      name: "First Year of Parenthood",
      duration: 12,
      mechanics: "Sleep deprivation, relationship strain, joy",
      difficulty: "extreme",
      warning: "Major life change"
    },
    {
      name: "Navigate Teenage Years",
      duration: 36,
      unlocks_after: "12 in-game years",
      mechanics: "Child NPC has agency, can rebel, needs guidance"
    }
  ],
  
  new_mechanics: {
    child_npc_system: {
      description: "Children are special NPCs that grow and change",
      ages: "Infant → Toddler → Child → Tween → Teen",
      
      characteristics: [
        "Have own personalities (generated from parents + randomness)",
        "Age in real-time (1 week = 1 week)",
        "Can have conflicts, need attention, bring joy",
        "Major relationship that spans seasons"
      ]
    },
    
    parenting_style: {
      choices: ["Strict", "Permissive", "Authoritative", "Uninvolved"],
      affects: "Child personality development, relationship quality"
    },
    
    work_life_balance: {
      description: "Parenting adds major time pressure",
      mechanics: "Reduced available time, energy, frequent interruptions"
    }
  },
  
  integration: {
    requires: "Relationship Level 5 with romantic partner NPC",
    or: "Adoption decision available at any time"
  },
  
  pricing: {
    usd: 12.99,
    essence_alternative: 1300
  },
  
  target_audience: "Players interested in family simulation, long-term relationship consequences"
}
```

---

### PACK-REL-002: "Wedding & Marriage"

```javascript
{
  id: "exp_wedding",
  name: "Wedding & Marriage",
  category: "Relationship",
  size: "standard",
  
  new_aspirations: [
    {
      name: "Plan Dream Wedding",
      duration: 24,
      mechanics: "Budget management, family drama, guest list politics"
    },
    {
      name: "Navigate First Year of Marriage",
      duration: 12,
      mechanics: "Adjustment, conflict resolution, deepening bond"
    }
  ],
  
  new_mechanics: {
    wedding_planning: "New mini-game system with budgets, venue, guests",
    married_life: "Joint finances, shared aspirations, new relationship dynamics"
  },
  
  pricing: { usd: 7.99 }
}
```

---

### PACK-REL-003: "Found Family"

```javascript
{
  id: "exp_found_family",
  name: "Found Family",
  category: "Relationship",
  size: "standard",
  
  theme: "Build chosen family through deep friendships",
  
  new_aspirations: [
    "Build Your Chosen Family (6+ Level 4 friendships)",
    "Host Annual Friend Gathering",
    "Support Friend Through Crisis"
  ],
  
  focus: "Platonic love, queer family structures, non-traditional relationships",
  
  pricing: { usd: 7.99 }
}
```

---

## EXPANSION CATEGORY 3: LIFESTYLE & ENVIRONMENT (3 Packs)

### PACK-LIF-001: "City Explorer"

```javascript
{
  id: "exp_city_explorer",
  name: "City Explorer",
  category: "Lifestyle",
  size: "standard",
  
  content: {
    aspiration_cards: 10,
    character_cards: 12,
    activity_cards: 40,
    location_cards: 20,
    system_cards: 8,
    total_cards: 90
  },
  
  theme: "Urban life, public transit, city culture",
  
  new_mechanics: {
    public_transit: {
      description: "Metro system for city navigation",
      affects: "Time management, random encounters",
      unlocks: "New NPCs met on trains, commute rituals"
    },
    
    neighborhood_reputation: {
      description: "Become known in your neighborhood",
      progression: "Stranger → Regular → Local → Neighborhood Icon",
      benefits: "Discounts, favors, community support"
    },
    
    urban_exploration: {
      description: "Discover hidden gems in the city",
      mechanic: "Unlock secret locations through exploration"
    }
  },
  
  new_locations: [
    "Subway Platform (random encounters, people-watching)",
    "Rooftop Bar (networking, city views, expensive)",
    "Late-Night Bodega (24/7 comfort, cat who lives there)",
    "Underground Music Venue (discover bands, make friends)",
    "Farmer's Market (Sunday ritual, quality food)",
    // ... 15 more urban locations
  ],
  
  pricing: { usd: 7.99 }
}
```

---

### PACK-LIF-002: "Rural Homestead"

```javascript
{
  id: "exp_rural",
  name: "Rural Homestead",
  category: "Lifestyle",
  size: "standard",
  
  theme: "Move to countryside, sustainable living, self-sufficiency",
  
  new_mechanics: {
    homestead_management: "Garden, chickens, repairs, seasons",
    seasonal_cycles: "Planting, harvest, winter prep",
    community_reliance: "Small town dynamics, everyone knows everyone"
  },
  
  aspirations: [
    "Move to Rural Area",
    "Build Self-Sufficient Homestead",
    "Become Part of Small Town",
    "Master Seasonal Living"
  ],
  
  pricing: { usd: 7.99 }
}
```

---

### PACK-LIF-003: "Pet Companion"

```javascript
{
  id: "exp_pets",
  name: "Pet Companion",
  category: "Lifestyle",
  size: "small",
  
  new_mechanics: {
    pet_npc: {
      description: "Dog or cat as special NPC",
      characteristics: "Has personality, needs, provides unconditional support",
      benefits: "Emotional support during stress, routine, joy"
    }
  },
  
  activities: [
    "Morning Dog Walk (ritual formation)",
    "Vet Visit (responsibility, cost)",
    "Train Dog (skill building, bonding)",
    "Cat Refuses to Move from Laptop (comic relief)"
  ],
  
  pricing: { usd: 4.99 }
}
```

---

## EXPANSION CATEGORY 4: CULTURE & LANGUAGE (2 Packs)

### PACK-CUL-001: "Spanish-Speaking World"

```javascript
{
  id: "exp_spanish",
  name: "Spanish-Speaking World",
  category: "Culture",
  size: "major",
  
  content: {
    aspiration_cards: 15,
    character_cards: 25,
    activity_cards: 40,
    location_cards: 15,
    system_cards: 10,
    total_cards: 105
  },
  
  new_mechanics: {
    language_fluency_system: {
      levels: "A1 → A2 → B1 → B2 → C1 → C2",
      affects: "NPC interactions, career opportunities, cultural access",
      progression: "Realistic (hundreds of hours to fluency)"
    },
    
    bilingual_npcs: {
      description: "NPCs speak Spanish, conversations adapt to player level",
      early: "Mostly English, some Spanish words",
      intermediate: "Code-switching",
      advanced: "Full Spanish conversations"
    },
    
    cultural_immersion: {
      description: "Access to Spanish-language media, events, communities",
      authenticity: "Culturally researched, region-specific"
    }
  },
  
  new_aspirations: [
    "Achieve Conversational Spanish (B1)",
    "Live in Spanish-Speaking Country (6 months)",
    "Work Bilingually",
    "Connect with Heritage Language",
    "Translate Professionally"
  ],
  
  pricing: { usd: 12.99 },
  
  notes: "Template for other language packs (French, Mandarin, Japanese, etc.)"
}
```

---

## EXPANSION CATEGORY 5: MIND & GROWTH (2 Packs)

### PACK-MIN-001: "Therapy & Healing"

```javascript
{
  id: "exp_therapy",
  name: "Therapy & Healing",
  category: "Mind & Growth",
  size: "standard",
  
  theme: "Mental health, therapy, trauma processing, growth",
  
  new_mechanics: {
    therapy_system: {
      description: "Regular therapy sessions as activity",
      progression: "Resistance → Opening up → Breakthroughs → Integration",
      affects: "Emotional meter stability, trauma resolution, self-awareness"
    },
    
    trauma_processing: {
      description: "Work through past trauma over multiple seasons",
      timeline: "Realistic (takes time, non-linear)",
      benefits: "Reduced anxiety, better relationships, self-compassion"
    }
  },
  
  new_npcs: [
    {
      name: "Dr. Sarah Kim",
      role: "Therapist",
      special: "Professional relationship, boundaries, but deeply meaningful"
    }
  ],
  
  aspirations: [
    "Commit to Therapy (12 sessions)",
    "Process Past Trauma",
    "Build Healthy Coping Mechanisms",
    "Overcome Anxiety",
    "Become Who You Want to Be"
  ],
  
  content_warning: "Mental health themes, trauma discussion",
  
  pricing: { usd: 7.99 }
}
```

---

## EXPANSION CATEGORY 6: META & FANTASY (2 Packs)

### PACK-META-001: "Dream Sequences"

```javascript
{
  id: "exp_dreams",
  name: "Dream Sequences",
  category: "Meta",
  size: "small",
  
  theme: "Surreal dream sequences reveal subconscious",
  
  mechanics: {
    dream_cards: {
      description: "Special cards that appear based on emotional state",
      characteristics: "Surreal, symbolic, process emotions",
      frequency: "1-2 per season during high stress"
    },
    
    dream_interpretation: {
      description: "Dreams reflect player's fears, desires, unresolved issues",
      affects: "Self-awareness, emotional processing"
    }
  },
  
  pricing: { usd: 4.99 }
}
```

---

## Expansion Pack Roadmap

### Year 1 (Launch Year)

```
Month 0: LAUNCH
- Base Game (480 cards, 90 aspirations)

Month 3: "City Explorer" ($7.99)
- Urban life expansion
- Public transit, neighborhoods
- 90 new cards

Month 6: "Therapy & Healing" ($7.99)
- Mental health focus
- Therapy system
- 70 new cards

Month 9: "Tech Startup" ($7.99)
- Career expansion
- Startup mechanics
- 80 new cards

Month 12: "Parenthood" ($12.99) - MAJOR
- Family simulation
- Child NPCs
- 105 new cards
```

### Year 2 Roadmap

```
Q1: "Spanish-Speaking World" ($12.99)
Q2: "Pet Companion" ($4.99) + "Rural Homestead" ($7.99)
Q3: "Medical Professional" ($12.99)
Q4: "Wedding & Marriage" ($7.99)
```

---

## Master Truths v1.2: Capacity Considerations for Expansion Packs *(NEW)*

### Intensive Packs Require Player Capacity Awareness

**Core Principle:** Some expansion packs introduce high-stress content that should only be pursued when player has adequate emotional capacity.

```javascript
const EXPANSION_CAPACITY_CONSIDERATIONS = {
  high_intensity_packs: {
    parenthood: {
      min_recommended_capacity: 7,
      reason: "First year of parenthood is extreme stress",
      warning: "This expansion includes sleep deprivation, relationship strain, and constant demands. Only pursue when emotionally prepared.",
      
      capacity_impact: {
        first_year: "-2 to -3 capacity sustained",
        recovery_time: "6-12 months to stabilize",
        relationship_strain: "Partner capacity also affected"
      }
    },
    
    medical_professional: {
      min_recommended_capacity: 7,
      reason: "80+ hour weeks, life/death decisions, extreme burnout risk",
      warning: "Medical residency is one of most demanding experiences in game. High authenticity = high stress.",
      
      capacity_impact: {
        residency: "-3 to -4 capacity common",
        burnout_risk: "75% chance if starting below capacity 6",
        recovery: "Requires intentional rest mechanics"
      }
    }
  },
  
  moderate_intensity: {
    tech_startup: {
      min_recommended_capacity: 6,
      warning: "Startup life = high stress, long hours, uncertainty"
    },
    
    wedding_marriage: {
      min_recommended_capacity: 6,
      warning: "Wedding planning adds 2-3 active stressors (budget, family, logistics)"
    }
  },
  
  low_intensity: {
    city_explorer: "No special capacity requirements",
    pet_companion: "Actually INCREASES capacity (+1 from pet support)",
    therapy_healing: "Designed for LOW capacity players (helps recovery)"
  },
  
  pack_selection_ui: {
    display_capacity_requirement: true,
    show_warning_if_below: "⚠️ Your current capacity (4) is below recommended (7) for this pack",
    suggest_alternatives: "Consider 'Therapy & Healing' or 'Pet Companion' to build capacity first"
  }
};
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Expansion System (v1.1 Foundation)
- [x] All expansion content integrates with base systems
- [x] No pay-to-win (all content is experience, not advantage)
- [x] Expansions unlock after Season 1 (no FOMO pressure)
- [x] Can be purchased with Essence (in-game currency)
- [x] Plus subscribers get 20% discount

### ✅ Master Truths v1.2: Emotional Authenticity Integration
- [x] **Capacity Considerations:** High-intensity packs display capacity requirements
- [x] **Player Warnings:** UI warns if current capacity below recommended
- [x] **Pack Intensity Classification:** All packs classified (High/Moderate/Low intensity)
- [x] **Capacity Impact Documented:** Each intensive pack shows capacity drain effects
- [x] **Alternative Suggestions:** Low-capacity players guided to appropriate packs

### ✅ Master Truths v1.2: Novel-Quality Narrative Systems
- [x] **Tension Injection:** Expansion packs create novel-worthy content
- [x] **Emotional Journey:** All packs support 8-10 season lifecycle
- [x] **Dramatic Potential:** High-intensity packs create major life transitions

### ✅ Cross-References
- [x] Links to `20-base-card-catalog.md` (base game content)
- [x] Links to `1.concept/17-monetization-model.md` (pricing strategy)
- [x] Links to `42-aspiration-goal-trees.md` (aspiration templates)
- [x] Capacity system references `14-emotional-state-mechanics.md`
- [x] NPC capacity references `44-relationship-progression-spec.md`

### ✅ Terminology Consistency (Master Truths v1.2 §2)
- [x] Emotional Capacity: 0-10 continuous scale used correctly
- [x] Expansion pack naming: Consistent format
- [x] Intensity classification: Clear categories

**References:**
- See `20-base-card-catalog.md` for base game content
- See `1.concept/17-monetization-model.md` for pricing strategy
- See `42-aspiration-goal-trees.md` for aspiration templates
- See `14-emotional-state-mechanics.md` for capacity system mechanics
- See `44-relationship-progression-spec.md` for NPC capacity tracking

---

**This specification enables content teams to develop expansion packs with exact content breakdowns, mechanics, pricing, and capacity considerations that extend the base game experience across diverse life paths while maintaining emotional authenticity.**

