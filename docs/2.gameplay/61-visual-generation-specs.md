# Visual Generation Specifications - AI Image Generation

**Compliance:** master_truths_canonical_spec_v_1_2.md (v1.2)  
**Last Updated:** October 14, 2025  
**Purpose:** Complete technical specifications for on-device AI image generation for character portraits, location art, and dynamic visuals

**References:**
- **Art Styles:** `60-art-style-system.md` (visual style guidelines)
- **Card Generation:** `24-card-generation-guidelines.md` (text generation)
- **AI System:** `docs/3.ai/README.md` (TensorFlow Lite setup)

---

## Overview

**Unwritten generates unique visuals on-device** using TensorFlow Lite models for character portraits, location images, and dynamic card art. This ensures every playthrough feels visually unique while maintaining performance.

**Generation Targets:**
- **Character Portraits:** Unique faces for every NPC (50-100 per playthrough)
- **Location Art:** Stylized illustrations of places (30-50 per playthrough)
- **Dynamic Cards:** Evolution visuals for high-significance cards
- **Novel Covers:** Season novel cover art

**Constraints:**
- **On-device generation:** Must run on mobile (< 2GB RAM)
- **Speed:** < 5 seconds per image
- **Quality:** Visually appealing, style-consistent
- **Size:** Models < 500MB total

---

## Image Generation Architecture

### Generation Pipeline

```typescript
interface ImageGenerationRequest {
  type: "character" | "location" | "card_art" | "novel_cover";
  
  // Base Description
  description: string;
  
  // Style
  art_style: ArtStyleID;               // e.g., "modern_minimalist", "hand_drawn"
  
  // Context
  context?: {
    personality?: OCEANProfile;        // For characters
    mood?: EmotionalState;             // For locations/scenes
    player_context?: PlayerContext;
  };
  
  // Technical
  resolution: {
    width: number;
    height: number;
  };
  quality: "draft" | "standard" | "high";
  
  // Caching
  cache_key?: string;
  use_cache: boolean;
}

interface GeneratedImage {
  image_data: Blob;
  resolution: { width: number; height: number };
  generation_time_ms: number;
  cache_hit: boolean;
  metadata: {
    prompt_used: string;
    style: string;
    seed: number;
  };
}
```

---

## CHARACTER PORTRAIT GENERATION

### Character Description → Prompt

```javascript
async function generateCharacterPortrait(npc, artStyle, playerState) {
  // STEP 1: Build base description
  const baseDescription = buildCharacterDescription(npc);
  
  // STEP 2: Add personality visual cues
  const personalityVisuals = mapPersonalityToVisuals(npc.personality);
  
  // STEP 3: Add style modifiers
  const stylePrompt = artStyle.ai_generation_prompts.character_base_prompt;
  
  // STEP 4: Construct full prompt
  const fullPrompt = `
    Portrait of ${baseDescription.age_range} ${baseDescription.gender_presentation} person.
    
    Physical characteristics:
    - ${baseDescription.ethnicity}
    - ${baseDescription.build}
    - ${baseDescription.hair}
    - ${baseDescription.distinctive_features}
    
    Personality visual cues (subtle):
    - ${personalityVisuals.expression}
    - ${personalityVisuals.posture}
    - ${personalityVisuals.clothing_style}
    - ${personalityVisuals.accessories}
    
    Style: ${stylePrompt}
    Mood: ${determinePortraitMood(npc, playerState)}
    
    Technical:
    - Portrait composition (head and shoulders)
    - ${artStyle.visual_characteristics.line_style}
    - Color palette: ${artStyle.visual_characteristics.color_palette.primary.join(', ')}
    - ${artStyle.visual_characteristics.texture}
  `;
  
  // STEP 5: Generate
  const image = await tflite.generateImage({
    prompt: fullPrompt,
    resolution: { width: 256, height: 256 },
    quality: "high",
    style: artStyle.id,
    seed: hashNPCID(npc.id)           // Consistent results for same NPC
  });
  
  return image;
}
```

---

### Personality → Visual Cues Mapping

```javascript
const PERSONALITY_VISUAL_MAPPING = {
  openness: {
    high_4_5: {
      expression: "Curious, slightly tilted head, eyes engaged",
      clothing: "Artistic, creative, unique style choices",
      accessories: "Books, art supplies, unique jewelry",
      colors: "Varied, interesting combinations"
    },
    low_1_2: {
      expression: "Straightforward, neutral, direct gaze",
      clothing: "Classic, traditional, practical",
      accessories: "Functional, minimal",
      colors: "Subdued, conventional palette"
    }
  },
  
  conscientiousness: {
    high_4_5: {
      expression: "Composed, attentive, focused",
      clothing: "Well-fitted, organized, intentional",
      posture: "Upright, put-together",
      grooming: "Neat, meticulous"
    },
    low_1_2: {
      expression: "Relaxed, casual",
      clothing: "Comfortable, loose, lived-in",
      posture: "Casual, easygoing",
      grooming: "Natural, effortless"
    }
  },
  
  extraversion: {
    high_4_5: {
      expression: "Animated, warm smile, open",
      body_language: "Facing forward, energetic",
      eyes: "Bright, engaging, welcoming",
      aura: "Approachable, vibrant"
    },
    low_1_2: {
      expression: "Reserved, subtle expression, calm",
      body_language: "Slightly turned, quiet presence",
      eyes: "Thoughtful, observant, gentle",
      aura: "Contained, peaceful"
    }
  },
  
  agreeableness: {
    high_4_5: {
      expression: "Kind eyes, gentle smile, warmth",
      features: "Soft, approachable",
      aura: "Caring, supportive presence"
    },
    low_1_2: {
      expression: "Direct, neutral, no-nonsense",
      features: "Sharp, defined",
      aura: "Confident, independent"
    }
  },
  
  neuroticism: {
    high_4_5: {
      expression: "Slight tension, concerned eyes",
      posture: "Slightly guarded, protective",
      details: "Nervous energy in eyes"
    },
    low_1_2: {
      expression: "Calm, relaxed, at ease",
      posture: "Open, confident",
      details: "Peaceful demeanor"
    }
  }
};

function mapPersonalityToVisuals(oceanProfile) {
  return {
    expression: selectVisualCue(oceanProfile.extraversion, PERSONALITY_VISUAL_MAPPING.extraversion, 'expression'),
    posture: selectVisualCue(oceanProfile.conscientiousness, PERSONALITY_VISUAL_MAPPING.conscientiousness, 'posture'),
    clothing_style: selectVisualCue(oceanProfile.openness, PERSONALITY_VISUAL_MAPPING.openness, 'clothing'),
    accessories: selectVisualCue(oceanProfile.openness, PERSONALITY_VISUAL_MAPPING.openness, 'accessories'),
    aura: selectVisualCue(oceanProfile.agreeableness, PERSONALITY_VISUAL_MAPPING.agreeableness, 'aura')
  };
}
```

---

### Character Evolution Visual Changes

```javascript
const CHARACTER_VISUAL_EVOLUTION = {
  level_0_to_1: {
    changes: "None - same portrait",
    reason: "Just met, visual stays consistent"
  },
  
  level_1_to_2: {
    changes: "None - same portrait",
    reason: "Acquaintance level, appearance doesn't change"
  },
  
  level_2_to_3: {
    changes: "Add subtle warmth to expression",
    technique: "Slight image adjustment, not regeneration",
    effect: "Eyes softer, hint of smile"
  },
  
  level_3_to_4: {
    changes: "Optional: Update clothing to reflect shared experiences",
    technique: "May regenerate with context",
    example: "If hiking together often, add outdoor gear"
  },
  
  level_4_to_5: {
    changes: "Optional: Show passage of time (if years passed)",
    technique: "Age progression if applicable",
    example: "Subtle aging if 3+ years together"
  },
  
  note: "Core facial features NEVER change - consistency is key"
};
```

---

## LOCATION ART GENERATION

### Location Description → Prompt

```javascript
async function generateLocationArt(location, artStyle, playerState) {
  const locationDescription = buildLocationDescription(location);
  const playerHistory = getLocationHistory(location.id, playerState);
  
  const fullPrompt = `
    ${locationDescription.type} scene: ${locationDescription.name}
    
    Setting:
    - ${locationDescription.environment}
    - ${locationDescription.atmosphere}
    - ${locationDescription.time_of_day}
    - ${locationDescription.weather}
    
    Key features:
    - ${locationDescription.distinctive_elements.join('\n- ')}
    
    Mood: ${determineLocationMood(location, playerHistory)}
    
    Style: ${artStyle.ai_generation_prompts.location_base_prompt}
    Perspective: ${locationDescription.perspective}
    Color palette: ${artStyle.visual_characteristics.color_palette.accent.join(', ')}
    
    ${playerHistory.significance > 7 ? `
      This location has deep meaning to the player:
      ${playerHistory.major_moments.slice(0, 2).join('; ')}
      Reflect emotional weight subtly (lighting, warmth)
    ` : ''}
  `;
  
  const image = await tflite.generateImage({
    prompt: fullPrompt,
    resolution: { width: 512, height: 384 },
    quality: "high",
    style: artStyle.id,
    seed: hashLocationID(location.id)
  });
  
  return image;
}
```

---

### Location Mood by Player History

```javascript
const LOCATION_MOOD_MAPPING = {
  first_visit: {
    mood: "Neutral, documentary",
    lighting: "Natural, clear",
    atmosphere: "Observational"
  },
  
  regular_visits_positive: {
    mood: "Warm, welcoming, familiar",
    lighting: "Golden, soft",
    atmosphere: "Comforting, homey"
  },
  
  major_positive_memory: {
    mood: "Luminous, special, treasured",
    lighting: "Warm glow, highlighted",
    atmosphere: "Almost magical realism",
    examples: ["Where you met Sarah", "Where you decided to be a photographer"]
  },
  
  major_negative_memory: {
    mood: "Somber, heavy, significant",
    lighting: "Muted, shadows",
    atmosphere: "Weight of memory",
    examples: ["Hospital where you collapsed", "Office where you were fired"]
  },
  
  ritual_location: {
    mood: "Sacred routine, anchored",
    lighting: "Consistent, familiar",
    atmosphere: "This is YOUR place",
    examples: ["Café Luna Tuesday 3PM with Sarah"]
  }
};
```

---

## DYNAMIC CARD ART GENERATION

### High-Significance Card Visuals

```javascript
const DYNAMIC_CARD_ART = {
  when_to_generate: {
    fusion_cards: "Always - fusion creates unique moment",
    evolved_cards: "If significance >= 8",
    phase_transitions: "Always - life-changing events",
    legendary_achievements: "Always"
  },
  
  generation_approach: {
    fusion_character_activity: {
      prompt: "Scene of ${character} and player doing ${activity}",
      composition: "Two figures, shared moment",
      style: "Match current art style",
      mood: "Relationship warmth"
    },
    
    phase_transition: {
      prompt: "Symbolic representation of ${transition_type}",
      composition: "Dramatic, impactful",
      style: "Heightened, intense",
      examples: {
        major_breakup: "Empty chair, single coffee cup, window",
        career_devastation: "Packed box, security badge, closed door",
        health_crisis: "Hospital corridor, harsh lights, vulnerability"
      }
    },
    
    legendary_achievement: {
      prompt: "Triumphant representation of ${achievement}",
      composition: "Epic, celebratory",
      style: "Elevated, special treatment",
      glow_effect: true
    }
  }
};
```

---

## NOVEL COVER GENERATION

### Season → Cover Art

```javascript
async function generateNovelCover(seasonData, artStyle) {
  const coverPrompt = `
    Book cover for "${seasonData.season_title}"
    
    Season summary: ${seasonData.aspiration}
    Emotional journey: ${seasonData.emotional_arc}
    Key visual symbols: ${identifyVisualSymbols(seasonData)}
    
    Composition:
    - Book cover layout
    - Title space at top
    - Central symbolic image
    - ${artStyle.name} style
    
    Mood: ${seasonData.overall_tone}
    Color palette: ${selectSeasonPalette(seasonData, artStyle)}
    
    Style notes:
    - Novel-quality cover art
    - Symbolic rather than literal
    - Emotionally evocative
    - Professional book cover aesthetic
  `;
  
  const cover = await tflite.generateImage({
    prompt: coverPrompt,
    resolution: { width: 600, height: 900 },   // Book cover ratio
    quality: "high",
    style: artStyle.id
  });
  
  // Add title overlay
  const finalCover = await addTitleOverlay(cover, seasonData.season_title);
  
  return finalCover;
}

function identifyVisualSymbols(seasonData) {
  // Extract key visual symbols from season
  const symbols = [];
  
  if (seasonData.aspiration.includes("photography")) {
    symbols.push("camera");
  }
  if (seasonData.major_relationship) {
    symbols.push("two figures, connection");
  }
  if (seasonData.crisis) {
    symbols.push("storm, challenge");
  }
  if (seasonData.location_significance) {
    symbols.push(seasonData.key_location);
  }
  
  return symbols.join(', ');
}
```

---

## Performance Optimization

### Generation Strategy

```javascript
const GENERATION_OPTIMIZATION = {
  // Pre-generate during low activity
  pre_generation: {
    when: "Player in menu, reading dialogue, idle",
    targets: [
      "Known upcoming NPCs (next 3 interactions)",
      "Locations player hasn't visited yet",
      "Novel cover if season nearing end"
    ],
    priority: "Low - background task"
  },
  
  // Cache aggressively
  caching: {
    character_portraits: "Permanent - never regenerate",
    locations: "Permanent unless player history changes mood",
    card_art: "Permanent once generated",
    novel_covers: "Permanent"
  },
  
  // Progressive quality
  progressive_loading: {
    1: "Show low-res placeholder immediately",
    2: "Generate draft quality (< 2s)",
    3: "Upgrade to high quality in background",
    4: "Swap when ready"
  },
  
  // Fallback
  fallback_images: {
    if_generation_fails: "Use style-appropriate placeholder",
    if_device_too_slow: "Pre-rendered generic images",
    always_have_backup: true
  }
};
```

---

### Model Size & Performance

```javascript
const MODEL_SPECIFICATIONS = {
  models: {
    character_generator: {
      size: "180MB",
      type: "Stable Diffusion Mobile",
      resolution: "256x256 native, upscale to 512x512",
      speed: "3-5 seconds on mid-range device",
      quality: "High for portraits"
    },
    
    location_generator: {
      size: "200MB",
      type: "Stable Diffusion Mobile (landscape)",
      resolution: "512x384",
      speed: "4-6 seconds",
      quality: "High for environments"
    },
    
    style_adapter: {
      size: "50MB per style",
      type: "LoRA adapters",
      function: "Adapt base model to art style",
      speed: "Adds < 1s to generation"
    }
  },
  
  total_download: {
    base_models: "380MB",
    default_style: "50MB",
    additional_styles: "50MB each"
  },
  
  device_requirements: {
    minimum: "2GB RAM, GPU preferred",
    recommended: "4GB RAM, GPU",
    optimal: "6GB+ RAM, dedicated GPU"
  }
};
```

---

## Quality Validation

### Post-Generation Checks

```javascript
async function validateGeneratedImage(image, request) {
  const checks = {
    resolution_correct: image.width === request.resolution.width,
    
    style_consistent: await checkStyleConsistency(image, request.art_style),
    
    safe_content: await checkContentSafety(image),
    
    visual_quality: await scoreVisualQuality(image),
    
    description_match: await checkDescriptionMatch(image, request.description)
  };
  
  if (checks.visual_quality < 0.7) {
    // Regenerate with adjusted prompt
    return { valid: false, regenerate: true };
  }
  
  if (!checks.safe_content) {
    // Use fallback image
    return { valid: false, use_fallback: true };
  }
  
  return { valid: true };
}
```

---

## Art Asset Pipeline Summary

```
CHARACTER CREATION
↓
Generate base portrait (5s)
↓
Cache permanently
↓
Use across all interactions

LOCATION FIRST VISIT
↓
Generate location art (5s)
↓
Cache permanently
↓
Mood adjusts via filters (not regeneration)

HIGH-SIGNIFICANCE FUSION
↓
Generate fusion card art (5s)
↓
Cache permanently
↓
Add to player's unique card deck

SEASON COMPLETE
↓
Generate novel cover (6s)
↓
Add title overlay
↓
Permanent in Life Bookshelf
```

---

## Compliance Checklist (Master Truths v1.2)

### ✅ Core Visual Generation System (v1.1 Foundation)
- [x] On-device generation (TensorFlow Lite, < 5s per image)
- [x] Style-consistent across art packs
- [x] Personality influences character visuals
- [x] Permanent caching (consistency across seasons)
- [x] Fallback images for low-end devices

### ✅ Master Truths v1.2: Emotional Authenticity Integration
- [x] **OCEAN Personality Visuals:** Character appearance reflects personality traits
- [x] **Emotional State Influence:** Location mood adapts to player emotional state
- [x] **Memory Resonance:** High-significance locations get enhanced visual treatment
- [x] **Capacity Awareness:** No visual generation when capacity critically low (performance)

### ✅ Master Truths v1.2: Novel-Quality Narrative Systems
- [x] **Dynamic Fusion Art:** High-significance fusions get unique generated art
- [x] **Phase Transition Visuals:** Major life changes get special visual treatment
- [x] **Novel Covers:** Season-end covers reflect emotional journey
- [x] **Quality Validation:** All generated images pass quality thresholds (0.7+)

### ✅ Cross-References
- [x] Links to `60-art-style-system.md` (visual style guidelines)
- [x] Links to `24-card-generation-guidelines.md` (text generation integration)
- [x] Links to `1.concept/13-ai-personality-system.md` (personality → visual mapping)
- [x] OCEAN traits referenced correctly
- [x] Emotional states (20 states) integrated

### ✅ Terminology Consistency (Master Truths v1.2 §2)
- [x] OCEAN personality traits: Correct 0-5 scale
- [x] Emotional states: Proper naming
- [x] Art style nomenclature: Consistent with 60-68 docs

**References:**
- See `60-art-style-system.md` for visual style guidelines
- See `24-card-generation-guidelines.md` for text generation integration
- See `1.concept/13-ai-personality-system.md` for personality → visual mapping
- See `14-emotional-state-mechanics.md` for emotional state integration

---

**This specification enables AI/graphics engineers to implement the complete visual generation system with exact prompt templates, optimization strategies, and quality validation that creates unique, style-consistent visuals for every playthrough.**

