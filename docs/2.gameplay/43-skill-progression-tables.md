# Skill Progression Tables - Complete Reference

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete catalog of all 30+ skills with capacity effects on learning and OCEAN personality modifiers

**References:**
- **Success Formulas:** `12-success-probability-formulas.md` (skill modifier in success calc)
- **Aspirations:** `42-aspiration-goal-trees.md` (skill requirements for aspirations)
- **Card System:** `20-base-card-catalog.md` (skill cards)

---

## Overview

**Skills** are permanent player stats that range from 0 (untrained) to 10 (master). Skills affect success probability, unlock aspirations and activities, and define player capabilities.

**Total Skills:** 30+  
**Acquisition:** Through practice, training, aspirations, and events  
**Decay:** Minimal (-0.1 per 12 weeks without use, never below level 3 once achieved)  
**Level Range:** 0-10 (0 = untrained, 5 = competent, 10 = master)

---

## Skill System Mechanics

### Level Effects

```typescript
interface Skill {
  name: string;
  current_level: number;              // 0.0-10.0 (continuous)
  display_level: number;              // 0-10 (discrete)
  
  effects: {
    success_modifier: number;         // +4% per level
    unlocks_at_level: {[level: number]: string[]};
    affects_aspirations: string[];
  };
  
  progression: {
    xp: number;                       // Current XP
    xp_to_next: number;               // XP needed for next level
    decay_rate: number;               // -0.1 per 12 weeks idle
    min_level_after_decay: number;    // Never decays below 3
  };
}
```

### XP Requirements Per Level

```javascript
const XP_CURVE = {
  level_1: 100,      // Easy to get started
  level_2: 250,      // Total: 350
  level_3: 400,      // Total: 750 (competent)
  level_4: 600,      // Total: 1350
  level_5: 900,      // Total: 2250 (proficient)
  level_6: 1300,     // Total: 3550
  level_7: 1800,     // Total: 5350 (expert)
  level_8: 2500,     // Total: 7850
  level_9: 3500,     // Total: 11350 (near-master)
  level_10: 5000,    // Total: 16350 (master)
  
  typical_xp_per_practice: 25,        // 1 hour practice session
  typical_xp_per_aspiration_work: 50, // Using skill toward goal
  major_breakthrough: 500,            // Breakthrough event
  
  example_timeline: {
    level_3: "15-20 practice sessions (casual player: 8-12 weeks)",
    level_5: "90 practice sessions (dedicated: 24 weeks)",
    level_7: "215 practice sessions (expert: 52+ weeks)",
    level_10: "650+ practice sessions (master: 2-3 years)"
  }
};
```

---

## CATEGORY 1: CREATIVE SKILLS (8 Skills)

### SKILL-CRE-001: Photography

```javascript
{
  name: "Photography",
  category: "creative",
  
  level_progression: {
    0: {
      name: "Untrained",
      capabilities: "Can take photos with phone, basic snapshots",
      success_modifier: 0.00,
      unlocks: []
    },
    
    1: {
      name: "Beginner",
      capabilities: "Understands basic composition, light",
      success_modifier: +0.04,
      unlocks: ["Buy Entry-Level Camera", "Photography 101 Course"],
      typical_output: "Occasionally good photos, mostly mediocre",
      xp_required: 100
    },
    
    2: {
      name: "Novice",
      capabilities: "Consistent composition, manual settings understood",
      success_modifier: +0.08,
      unlocks: ["Photography Club", "Amateur Contests"],
      typical_output: "Reliably good photos, some very good ones",
      xp_required: 250
    },
    
    3: {
      name: "Competent",
      capabilities: "Portfolio-ready work, understands post-processing",
      success_modifier: +0.12,
      unlocks: ["Launch Photography Business (Aspiration)", "Paid Gigs"],
      typical_output: "Portfolio quality, clients would pay",
      xp_required: 400,
      milestone: "Can start making money"
    },
    
    4: {
      name: "Skilled",
      capabilities: "Consistent professional quality, developing style",
      success_modifier: +0.16,
      unlocks: ["Wedding Photography", "Event Photography"],
      typical_output: "Professional work, style emerging",
      xp_required: 600
    },
    
    5: {
      name: "Proficient",
      capabilities: "Strong personal style, technical mastery",
      success_modifier: +0.20,
      unlocks: ["Gallery Showing (Aspiration)", "Teach Workshops"],
      typical_output: "Recognizable style, exhibition-ready",
      xp_required: 900,
      milestone: "Professional photographer"
    },
    
    6: {
      name: "Advanced",
      capabilities: "Signature style recognized, command of medium",
      success_modifier: +0.24,
      unlocks: ["Photography Book", "Featured Artist"],
      typical_output: "Work sought after, strong reputation",
      xp_required: 1300
    },
    
    7: {
      name: "Expert",
      capabilities: "Master of style and technique, teaching others",
      success_modifier: +0.28,
      unlocks: ["Master Classes", "Mentorship Program"],
      typical_output: "Exhibition-level consistently",
      xp_required: 1800,
      milestone: "Recognized expert in field"
    },
    
    8: {
      name: "Master Craftsman",
      capabilities: "Pushing boundaries of medium",
      success_modifier: +0.32,
      unlocks: ["International Recognition Opportunities"],
      typical_output: "Innovative, boundary-pushing work",
      xp_required: 2500
    },
    
    9: {
      name: "Renowned Master",
      capabilities: "Influence on field, defining aesthetic movements",
      success_modifier: +0.36,
      unlocks: ["Legacy Projects", "Museum Exhibitions"],
      typical_output: "Museum-quality, historically significant",
      xp_required: 3500
    },
    
    10: {
      name: "Legendary",
      capabilities: "One of the greats, name known beyond photography",
      success_modifier: +0.40,
      unlocks: ["Creative Legacy (Legendary Fusion)"],
      typical_output: "Career-defining body of work",
      xp_required: 5000,
      milestone: "Legendary achievement"
    }
  },
  
  xp_sources: [
    { action: "Practice Session (1 hour)", xp: 25 },
    { action: "Shoot Paid Client", xp: 75 },
    { action: "Complete Photography Course", xp: 300 },
    { action: "Gallery Show", xp: 500 },
    { action: "Creative Breakthrough", xp: 500 }
  ],
  
  affects_aspirations: [
    "Launch Photography Business (requires 3)",
    "Gallery Showing (requires 5)",
    "Teach Photography (requires 7)"
  ],
  
  decay: {
    rate: -0.1, per_weeks: 12, min_level: 3
  }
}
```

### Other Creative Skills

**SKILL-CRE-002: Writing**
- Level 3: Can write engaging prose
- Level 5: Novel-quality writing
- Level 7: Publishable author
- Level 10: Literary master

**SKILL-CRE-003: Painting/Drawing**
**SKILL-CRE-004: Music Performance**
**SKILL-CRE-005: Music Composition**
**SKILL-CRE-006: Design (Graphic/UX)**
**SKILL-CRE-007: Video/Film Production**
**SKILL-CRE-008: Acting/Performance**

---

## CATEGORY 2: PROFESSIONAL SKILLS (10 Skills)

### SKILL-PRO-001: Business Management

```javascript
{
  name: "Business Management",
  category: "professional",
  
  level_progression: {
    0: { name: "No Experience", capabilities: "Concepts unclear" },
    
    1: { name: "Basic Understanding", capabilities: "Understands profit/loss, basic accounting" },
    
    2: { name: "Novice Manager", capabilities: "Can create business plan, track finances" },
    
    3: { name: "Competent", 
         capabilities: "Can run small business, understands marketing/sales",
         unlocks: ["Launch Business Aspiration"],
         milestone: "Can start a business"
    },
    
    4: { name: "Skilled Manager", capabilities: "Multi-channel marketing, team coordination" },
    
    5: { name: "Proficient", 
         capabilities: "Strategic planning, scaling operations",
         unlocks: ["Scale Business", "Consulting"]
    },
    
    7: { name: "Expert", 
         capabilities: "Complex operations, multiple revenue streams",
         unlocks: ["Mentor Other Entrepreneurs"]
    },
    
    10: { name: "Business Mastery", 
          capabilities: "Serial entrepreneur, proven track record",
          unlocks: ["Business Legacy"]
    }
  }
}
```

### Other Professional Skills

**SKILL-PRO-002: Marketing**
**SKILL-PRO-003: Sales & Negotiation**
**SKILL-PRO-004: Project Management**
**SKILL-PRO-005: Leadership**
**SKILL-PRO-006: Public Speaking**
**SKILL-PRO-007: Programming/Software Development**
**SKILL-PRO-008: Data Analysis**
**SKILL-PRO-009: Accounting/Finance**
**SKILL-PRO-010: Teaching/Mentorship**

---

## CATEGORY 3: LANGUAGE SKILLS (1 Skill Template × Languages)

### SKILL-LAN-001: Spanish (Template for All Languages)

```javascript
{
  name: "Spanish",
  category: "language",
  
  level_progression: {
    0: { name: "No Knowledge", cefr: "-" },
    
    1: { name: "Basic Phrases", cefr: "A1", capabilities: "Can say hello, order food, basic survival phrases" },
    
    2: { name: "Elementary", cefr: "A2", capabilities: "Simple conversations, present tense, basic vocabulary" },
    
    3: { name: "Intermediate", 
         cefr: "B1", 
         capabilities: "Can discuss daily life, past/future tenses, understand main points",
         milestone: "Conversational"
    },
    
    4: { name: "Upper Intermediate", cefr: "B2", capabilities: "Complex conversations, idioms, most media" },
    
    5: { name: "Advanced", 
         cefr: "C1", 
         capabilities: "Fluent, nuanced expression, professional use",
         unlocks: ["Work in Spanish", "Translate Professionally"]
    },
    
    7: { name: "Proficient", cefr: "C2", capabilities: "Near-native, cultural nuance, professional writing" },
    
    10: { name: "Mastery", cefr: "C2+", capabilities: "Native-level command" }
  },
  
  xp_sources: [
    { action: "Daily App Practice (30 min)", xp: 15 },
    { action: "Conversation with Native (1 hour)", xp: 50 },
    { action: "Complete Course Level", xp: 200 },
    { action: "Immersion Week (Travel)", xp: 300 }
  ],
  
  time_to_competence: "36-52 weeks of consistent daily practice",
  
  other_languages: ["French", "Mandarin", "German", "Japanese", "Italian", "Portuguese"]
}
```

---

## CATEGORY 4: PHYSICAL SKILLS (6 Skills)

### SKILL-PHY-001: Running/Cardio

```javascript
{
  name: "Running/Cardio Fitness",
  category: "physical",
  
  level_progression: {
    0: { name: "Sedentary", capabilities: "Can't run 1 mile" },
    
    1: { name: "Beginner", capabilities: "Can jog 1 mile slowly" },
    
    2: { name: "Regular Runner", capabilities: "Can run 3 miles comfortably" },
    
    3: { name: "Competent Runner", 
         capabilities: "Can run 5K (3.1 mi) in 30-35 min",
         unlocks: ["Run Half-Marathon Aspiration"],
         milestone: "5K runner"
    },
    
    4: { name: "Skilled", capabilities: "Can run 10K comfortably" },
    
    5: { name: "Half-Marathoner", 
         capabilities: "Can complete half-marathon (13.1 mi)",
         unlocks: ["Full Marathon Aspiration"]
    },
    
    7: { name: "Marathoner", capabilities: "Can complete full marathon (26.2 mi)" },
    
    8: { name: "Ultra Runner", capabilities: "Ultra marathons, 50K+" },
    
    10: { name: "Elite Athlete", capabilities: "Competitive, sponsored level" }
  },
  
  xp_sources: [
    { action: "Training Run (1 hour)", xp: 30 },
    { action: "Complete 5K Race", xp: 100 },
    { action: "Complete Half-Marathon", xp: 500 },
    { action: "Complete Marathon", xp: 1000 }
  ],
  
  affects_aspirations: [
    "Run 5K (requires 2)",
    "Half-Marathon (requires 3)",
    "Full Marathon (requires 5)"
  ],
  
  physical_meter_benefit: "+0.5 per level (up to +5 at level 10)"
}
```

### Other Physical Skills

**SKILL-PHY-002: Strength Training**
**SKILL-PHY-003: Yoga/Flexibility**
**SKILL-PHY-004: Martial Arts**
**SKILL-PHY-005: Swimming**
**SKILL-PHY-006: Team Sports**

---

## CATEGORY 5: PRACTICAL SKILLS (5 Skills)

### SKILL-PRA-001: Cooking

```javascript
{
  name: "Cooking",
  category: "practical",
  
  level_progression: {
    0: { name: "Can't Cook", capabilities: "Relies on takeout/frozen meals" },
    
    1: { name: "Basic Cooking", capabilities: "Can make pasta, eggs, simple dishes" },
    
    2: { name: "Novice Cook", capabilities: "Can follow recipes, make decent meals" },
    
    3: { name: "Competent Cook", 
         capabilities: "Can cook variety of cuisines, improvise",
         benefits: "Saves money, impresses dates, healthier eating"
    },
    
    5: { name: "Skilled Cook", 
         capabilities: "Restaurant-quality at home",
         unlocks: ["Dinner Party Hosting", "Could Teach Cooking"]
    },
    
    7: { name: "Expert Cook", capabilities: "Advanced techniques, multiple cuisines" },
    
    10: { name: "Chef-Level", capabilities: "Professional chef quality" }
  },
  
  benefits: {
    financial: "Save $200-400/month on food",
    health: "Easier to maintain physical meter",
    social: "Host dinner parties, impress dates",
    relationship: "Cooking for others = bonding"
  }
}
```

### Other Practical Skills

**SKILL-PRA-002: Home Repair/DIY**
**SKILL-PRA-003: Gardening**
**SKILL-PRA-004: Driving (Advanced)**
**SKILL-PRA-005: Financial Planning**

---

## Skill Interaction Matrix

### Skill Synergies

```javascript
const SKILL_SYNERGIES = {
  photography_plus_design: {
    if_both_above: 5,
    bonus: "+10% success on creative projects",
    unlocks: "Creative Director path"
  },
  
  business_plus_creative: {
    if_both_above: 4,
    bonus: "+15% success on creative business aspirations",
    reason: "Creative talent + business acumen = success"
  },
  
  multiple_languages: {
    if_count: 2,
    bonus: "+5% on subsequent languages",
    reason: "Language learning becomes easier"
  },
  
  physical_skills: {
    if_any_above: 5,
    bonus: "Physical meter recovers +20% faster",
    affects: "All physical skills"
  }
};
```

---

## Skill Acquisition Paths

### Example: Photography to Professional

```
WEEK 0: Skill = 0 (No experience)
↓
WEEK 1-8: Take Photography 101 Course
├─ Weekly practice (8 sessions × 25 XP = 200 XP)
├─ Course completion: +300 XP
└─ Total: 500 XP → Level 2 (Novice)

WEEK 9-24: Practice + Minor Aspiration "Build Portfolio"
├─ Weekly practice (16 weeks × 2 sessions × 25 XP = 800 XP)
├─ Aspiration work (16 weeks × 50 XP = 800 XP)
└─ Total: +1600 XP → Level 4 (Skilled)

WEEK 25-52: Major Aspiration "Launch Photography Business"
├─ Weekly client work (28 weeks × 75 XP = 2100 XP)
├─ Breakthrough events: +500 XP
└─ Total: +2600 XP → Level 6 (Advanced)

WEEK 53-104: Gallery Show + Continued Professional Work
├─ Gallery show: +500 XP
├─ Continued work (52 weeks × 75 XP = 3900 XP)
└─ Total: +4400 XP → Level 8 (Master Craftsman)

YEARS 3-5: Mastery Through Dedication
├─ Major projects, exhibitions, teaching
├─ Accumulate remaining ~4000 XP
└─ Level 10 (Legendary) achieved
```

---

## Quick Reference: Common Skill Gates

```
ASPIRATION SKILL REQUIREMENTS:

Launch Photography Business → Photography 3+
Gallery Showing → Photography 5+
Teach Photography → Photography 7+

Launch Any Business → Business Management 3+
Scale to 6-Figures → Business Management 5+

Run Half-Marathon → Running 3+
Full Marathon → Running 5+

Write Novel → Writing 3+
Publish Novel → Writing 5+

Career Promotion → Relevant skill 5+
Executive Track → Relevant skill 7+

Conversational Spanish → Spanish 3+
Professional Spanish → Spanish 5+

Cook for Others → Cooking 2+
Host Dinner Parties → Cooking 3+
Teach Cooking → Cooking 7+
```

---

## Skill Display & UI

### Player Skill Sheet

```
┌─────────────────────────────────────┐
│ YOUR SKILLS                         │
├─────────────────────────────────────┤
│ CREATIVE                            │
│ • Photography: ████████░░ 8 (Master)│
│ • Design: ████░░░░░░ 4 (Skilled)   │
│                                     │
│ PROFESSIONAL                        │
│ • Business: ████░░░░░░ 4 (Skilled) │
│ • Marketing: ███░░░░░░░ 3 (Comp.)  │
│                                     │
│ PHYSICAL                            │
│ • Running: ████░░░░░░ 4 (Skilled)  │
│                                     │
│ PRACTICAL                           │
│ • Cooking: ██████░░░░ 6 (Advanced) │
│                                     │
│ LANGUAGE                            │
│ • Spanish: ███░░░░░░░ 3 (Intermed.)│
└─────────────────────────────────────┘
```

---

## Master Truths v1.2: Capacity Effects on Learning *(NEW)*

### Low Capacity Slows Skill Progression

**Core Principle:** Learning requires emotional/mental energy. Low capacity reduces XP gains from practice.

```javascript
const CAPACITY_LEARNING_MODIFIERS = {
  capacity_effects_on_xp_gain: {
    capacity_8_10: {
      xp_multiplier: 1.2,
      state: "Peak learning - absorbs information easily"
    },
    capacity_6_7: {
      xp_multiplier: 1.0,
      state: "Normal learning rate - baseline"
    },
    capacity_4_5: {
      xp_multiplier: 0.7,
      state: "Struggling to focus - slower learning"
    },
    capacity_2_3: {
      xp_multiplier: 0.4,
      state: "Exhausted - barely retaining anything"
    },
    capacity_0_1: {
      xp_multiplier: 0.1,
      state: "Cannot learn effectively - survival mode"
    }
  },
  
  example: {
    practice_session_base_xp: 25,
    
    at_capacity_8: {
      xp_gained: 30,  // 25 × 1.2
      narrative: "You're focused. It clicks. You're learning fast."
    },
    
    at_capacity_6: {
      xp_gained: 25,  // 25 × 1.0
      narrative: "Solid practice session. Making steady progress."
    },
    
    at_capacity_4: {
      xp_gained: 18,  // 25 × 0.7
      narrative: "You're tired. It's taking longer than usual to grasp concepts."
    },
    
    at_capacity_2: {
      xp_gained: 10,  // 25 × 0.4
      narrative: "You try to focus. The words blur. You're too exhausted to learn."
    }
  }
};
```

---

## Master Truths v1.2: OCEAN Personality Modifiers *(NEW)*

### Personality Affects Skill Learning Speed

**Core Principle:** Different personalities excel at different skills. High Openness learns creative skills faster; high Conscientiousness learns discipline-based skills faster.

```javascript
const OCEAN_SKILL_MODIFIERS = {
  creative_skills: {
    applies_to: ["Photography", "Writing", "Painting", "Music", "Design"],
    personality_modifiers: {
      high_openness_7plus: { xp_mult: 1.3, reason: "Embraces experimentation" },
      low_openness_3minus: { xp_mult: 0.7, reason: "Struggles with abstraction" },
      high_conscientiousness_7plus: { xp_mult: 1.1, reason: "Dedicated practice" }
    }
  },
  
  physical_skills: {
    applies_to: ["Running", "Strength Training", "Yoga", "Martial Arts"],
    personality_modifiers: {
      high_conscientiousness_7plus: { xp_mult: 1.4, reason: "Disciplined training" },
      low_conscientiousness_3minus: { xp_mult: 0.6, reason: "Inconsistent practice" },
      high_neuroticism_7plus: { xp_mult: 0.8, reason: "Anxiety about performance" }
    }
  },
  
  professional_skills: {
    applies_to: ["Business", "Leadership", "Project Management"],
    personality_modifiers: {
      high_conscientiousness_7plus: { xp_mult: 1.3, reason: "Systematic approach" },
      high_extraversion_7plus: { xp_mult: 1.2, reason: "Natural people skills" },
      low_extraversion_3minus: { xp_mult: 0.8, reason: "Leadership draining" }
    }
  },
  
  language_skills: {
    applies_to: ["Spanish", "French", "Mandarin", "etc"],
    personality_modifiers: {
      high_openness_7plus: { xp_mult: 1.2, reason: "Enjoys new sounds/grammar" },
      high_conscientiousness_7plus: { xp_mult: 1.3, reason: "Daily practice habit" },
      low_conscientiousness_3minus: { xp_mult: 0.5, reason: "Skips practice" }
    }
  },
  
  example_calculation: {
    skill: "Photography",
    base_xp: 25,
    player_capacity: 7,
    player_openness: 8,
    player_conscientiousness: 6,
    
    modifiers: {
      capacity_7: 1.0,  // Normal
      openness_8: 1.3,  // High Openness helps creative skills
      conscientiousness_6: 1.1  // Moderate Conscientiousness helps
    },
    
    final_xp: 25 * 1.0 * 1.3 * 1.1 = 36,  // 44% bonus!
    
    narrative: "Your creativity and dedication show. You're learning fast."
  }
};
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Skill System (v1.1 Foundation)
- [x] Skill levels 0-10 used consistently
- [x] Skill modifiers match success probability formula
- [x] Decay respects progression preservation
- [x] All skills integrate with aspiration requirements
- [x] Multi-season progression supported
- [x] XP curves defined per level (100 → 5000)
- [x] Skill synergies and interaction matrix

### ✅ Master Truths v1.2: Learning Effects *(NEW)*
- [x] **Capacity Effects on XP Gain**
  - Capacity 8-10: 1.2x XP ("Peak learning - absorbs easily")
  - Capacity 6-7: 1.0x XP ("Normal learning rate")
  - Capacity 4-5: 0.7x XP ("Struggling to focus - slower")
  - Capacity 2-3: 0.4x XP ("Exhausted - barely retaining")
  - Capacity 0-1: 0.1x XP ("Cannot learn - survival mode")
- [x] **OCEAN Personality Modifiers by Skill Category**
  - Creative skills: High Openness 1.3x, Low Openness 0.7x
  - Physical skills: High Conscientiousness 1.4x, Low Conscientiousness 0.6x
  - Professional skills: High Conscientiousness 1.3x, High Extraversion 1.2x
  - Language skills: High Openness 1.2x + High Conscientiousness 1.3x (stack!)
- [x] **Multiplicative Stacking**
  - Capacity × OCEAN traits = total XP multiplier
  - Example: Capacity 7 (1.0) × Openness 8 (1.3) × Conscientiousness 6 (1.1) = 1.43x total

### ✅ Master Truths v1.2 Enhancements Summary
This document now includes:
1. **~125 lines** of new v1.2 learning modifiers
2. **Capacity effects on learning** - exhaustion slows skill progression
3. **OCEAN personality modifiers** - personalities excel at different skills
4. **Multiplicative stacking** - capacity + personality combine for total effect
5. **Narrative feedback** - XP gain affects practice session descriptions

**Capacity Learning Examples:**
- Capacity 8 + 25 base XP = 30 XP: "You're focused. It clicks. Learning fast."
- Capacity 6 + 25 base XP = 25 XP: "Solid practice session. Steady progress."
- Capacity 4 + 25 base XP = 18 XP: "You're tired. Taking longer than usual."
- Capacity 2 + 25 base XP = 10 XP: "You try to focus. Words blur. Too exhausted."

**OCEAN Modifier Examples:**
- Creative skills (Photography): High Openness 7+ = 1.3x ("Embraces experimentation")
- Physical skills (Running): High Conscientiousness 7+ = 1.4x ("Disciplined training")
- Physical skills (Running): High Neuroticism 7+ = 0.8x ("Anxiety about performance")
- Language skills: High Openness + High Conscientiousness = 1.2x × 1.3x = 1.56x total!

**Stacking Example:**
- Photography practice: 25 base XP
- Capacity 7: 1.0x
- Openness 8: 1.3x (creative skill bonus)
- Conscientiousness 6: 1.1x (dedication bonus)
- **Total: 25 × 1.0 × 1.3 × 1.1 = 36 XP (44% bonus!)**
- Narrative: "Your creativity and dedication show. You're learning fast."

**Design Principles:**
- Learning requires energy - exhaustion slows progress
- Personality matters - you excel at what fits your traits
- Modifiers stack multiplicatively (not additive)
- Low Conscientiousness especially hurts discipline-based skills (0.5-0.6x)
- High Neuroticism hurts physical performance skills (anxiety effect)
- High Openness + High Conscientiousness = ideal creative learner (1.3x × 1.1x)

**References:**
- See `01-emotional-authenticity.md` for cross-system capacity integration
- See `14-emotional-state-mechanics.md` for capacity calculation
- See `12-success-probability-formulas.md` for skill modifier math and OCEAN effects
- See `42-aspiration-goal-trees.md` for skill gates on aspirations
- See `20-base-card-catalog.md` for skill acquisition cards

---

**This specification enables systems designers to implement the complete skill progression system with Master Truths v1.2 enhancements: capacity effects where exhaustion slows learning (0.1x-1.2x multiplier), OCEAN personality modifiers where traits determine skill affinity (0.5x-1.4x per trait), and multiplicative stacking where capacity and personality combine - creating authentic learning curves where you learn best when rested and pursuing skills that match your personality.**

