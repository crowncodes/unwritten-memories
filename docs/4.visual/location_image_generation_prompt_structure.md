# Location Image Generation Prompt Structure

> **Compliance**: Master Truths v1.2  
> **Purpose**: Generate consistent base location images with contextual enhancements that reflect game state, emotional capacity, narrative tension, and relationship progression.

---

## Core Principle

**Consistency + Context**: Every location has a **canonical base description** (fixed architectural/spatial identity) plus **contextual modifiers** (time, season, emotional state, narrative tension) that layer on top without changing the location's fundamental identity.

---

## Prompt Structure Template

```
[FIXED BASE] + [TIME/SEASON LAYER] + [EMOTIONAL ATMOSPHERE] + [NARRATIVE TENSION] + [TECHNICAL SPECS]
```

---

## 1. FIXED BASE (Canonical Identity)

**Purpose**: Ensures the same location is always recognizable across all generations.

### Template
```
A [ARCHITECTURE_TYPE] [LOCATION_TYPE] featuring [3-5 DEFINING_FEATURES]. 
[SPATIAL_LAYOUT]. [SIGNATURE_ELEMENTS]. [COLOR_PALETTE_BASE].
```

### Example: "Riverside Café"
```
A brick-facade corner café with floor-to-ceiling windows, weathered wooden entrance door, 
and hand-painted gold lettering reading "Riverside Café". Interior visible through windows 
shows exposed brick walls, mismatched vintage chairs, and a long marble-topped bar. 
Base palette: warm terracotta brick, deep forest green awning, aged brass fixtures.
```

### Canonical Elements (Always Include)
- **Architecture style**: Victorian, Modern, Industrial, etc.
- **Key structural features**: Windows, doors, walls, roofing (3-5 signature elements)
- **Spatial relationship**: Corner building, standalone, row house, etc.
- **Signature visual anchors**: Signs, unique architectural details, defining colors
- **Scale/proportion**: Building size, street width, surrounding context

---

## 2. TIME/SEASON LAYER (Temporal Context)

**Purpose**: Adapt lighting, weather, and seasonal characteristics without changing base structure.

### Time of Day Modifiers

#### Morning (6 AM - 11 AM)
```
Soft golden morning light, long shadows stretching [DIRECTION], dew on windows, 
gentle warm glow, pastel sky tones, low sun angle creating dimensional depth.
```

#### Afternoon (12 PM - 5 PM)
```
Bright overhead lighting, shorter shadows, vibrant colors at peak saturation, 
clear sky or scattered clouds, high-contrast definition, full illumination.
```

#### Evening (6 PM - 11 PM)
```
Warm interior lights glowing through windows contrasting with cool blue exterior dusk, 
amber streetlights beginning to illuminate, gradient sky (orange to deep blue), 
atmospheric twilight mood, inviting warmth radiating outward.
```

### Season Modifiers

#### Spring
```
Fresh green foliage emerging, flower boxes with early blooms, rain-cleaned surfaces, 
soft diffused light through clouds, puddles reflecting sky, renewed textures.
```

#### Summer
```
Lush full foliage, vibrant saturated colors, strong sunlight, outdoor seating populated, 
heat shimmer on pavement, long days extending golden hour, doors open to interior.
```

#### Fall
```
Warm amber and rust foliage, fallen leaves scattered on pavement, rich golden light, 
slightly overcast skies, cozy atmosphere, transition toward shorter days.
```

#### Winter
```
Bare tree branches, frost on windows, warm interior glow contrasting cold exterior, 
muted color palette, possible snow accumulation on ledges, condensation on glass, 
inviting warmth emphasized.
```

---

## 3. EMOTIONAL ATMOSPHERE (Character Capacity Context)

**Purpose**: Reflect the player character's emotional state and capacity (0-10 scale) through visual mood without altering location structure.

### High Capacity (8-10/10)
```
Crisp details, vibrant colors, inviting warmth, clear atmospheric perspective, 
welcoming ambiance, emphasize positive architectural features, slight glow to warm lights, 
optimistic color grading.
```

### Medium Capacity (5-7/10)
```
Balanced neutral tone, realistic color saturation, even lighting distribution, 
comfortable but not idealized, authentic texture representation, grounded atmosphere.
```

### Low Capacity (2-4/10)
```
Slightly muted colors, cooler color temperature shift, emphasized shadows, 
more contrast between light/dark areas, subtle desaturation, heavier atmospheric weight, 
details remain clear but mood shifts toward melancholy.
```

### Crisis Capacity (0-1/10)
```
Desaturated palette, heavy shadows dominating, cool blue-gray tones, oppressive atmosphere, 
windows appear less inviting, emphasize isolation, stark contrast, location feels distant 
or unreachable, foreboding mood.
```

---

## 4. NARRATIVE TENSION (Story Context)

**Purpose**: Layer visual cues reflecting current tension type without changing location identity.

### Mystery Hook
```
Partially obscured details (figure in window, unfamiliar car parked outside), 
something slightly "off" in the scene (door ajar when usually closed), atmospheric fog 
or rain obscuring clarity, sense of anticipation, one element that raises questions.
```

### Partial Reveal
```
Visual evidence of unseen events (new sign, missing familiar element, unexpected change), 
hint of activity but no clear explanation, viewer positioned as observer discovering clues, 
subtle before/after markers.
```

### Contradiction Moment
```
Unexpected visual state (closed when usually open, crowded when usually empty), 
lighting or atmosphere counter to expected time/season, visual dissonance creating intrigue, 
something fundamental has shifted.
```

### Stakes Escalation
```
Heightened dramatic lighting (storm clouds gathering, urgent golden hour), 
visual time pressure cues (moving van, "closing soon" sign), intensity in atmospheric 
rendering, sense of impending change or decision, dynamic weather elements.
```

### Neutral (No Active Tension)
```
Clean, authentic representation, no narrative cues added, location exists in natural state, 
focus on beauty and welcoming atmosphere, daily life rhythm visible.
```

---

## 5. RELATIONSHIP CONTEXT (NPC Presence)

**Purpose**: When location is associated with specific NPC, reflect relationship level (0-5) through environmental intimacy.

### Level 0-1 (Not Met / Stranger)
```
Exterior view only or public interior spaces, observed from distance, no personal details 
visible, generic welcoming atmosphere, professional/public presentation.
```

### Level 2 (Acquaintance)
```
Interior glimpse showing general layout, some personality hints (decor style, color choices), 
inviting but not intimate, comfortable viewing angle, public spaces emphasized.
```

### Level 3 (Friend)
```
Familiar angles, personal touches visible (photos on wall, specific furniture choices), 
warm lighting emphasizing comfort, viewer positioned as welcome guest, details that suggest 
repeated visits.
```

### Level 4 (Close Friend)
```
Intimate details visible (personal items, lived-in authenticity), viewer positioned as 
regular presence, imperfections showing comfort (coffee mug left out, book open on table), 
warm emotional atmosphere, private spaces partially visible.
```

### Level 5 (Soulmate/Best Friend)
```
Deeply personal perspective, full interior access, cherished details emphasized (photo of 
you and NPC, gift you gave them displayed), maximum emotional warmth, location rendered as 
sanctuary, your presence felt in the space.
```

---

## 6. TECHNICAL SPECIFICATIONS

**Purpose**: Ensure consistent quality and on-device optimization for TensorFlow Lite models.

### Model Requirements
```
Style: Painterly digital art with photorealistic foundation
Resolution: 512x512 or 768x768 (optimized for mobile inference)
Color depth: 24-bit RGB
Format: PNG with alpha channel support for UI overlay
Inference target: <15ms on mid-range devices
Model size: <50MB per location base model
```

### Composition Guidelines
```
Aspect ratio: 16:9 or 4:3 depending on UI context
Focal point: Rule of thirds positioning for primary architectural feature
Depth: 3-layer composition (foreground detail, mid-ground subject, background context)
Atmospheric perspective: Subtle depth cues through saturation and contrast falloff
Lighting: Single primary light source with ambient fill
```

### Consistency Anchors
```
Camera angle: [FIXED_ANGLE] for this location (e.g., "45-degree corner view from street level")
Distance: [FIXED_DISTANCE] (e.g., "30 feet from entrance")
Height: [FIXED_HEIGHT] (e.g., "eye level 5.5 feet")
Framing: [FIXED_FRAME] (e.g., "full building facade with 10% street context")
```

---

## Complete Prompt Example

### Location: "Riverside Café" | Morning | Medium Capacity | Mystery Hook | Level 3 Relationship

```
A brick-facade corner café with floor-to-ceiling windows, weathered wooden entrance door, 
and hand-painted gold lettering reading "Riverside Café". Interior visible through windows 
shows exposed brick walls, mismatched vintage chairs, and a long marble-topped bar. 
Base palette: warm terracotta brick, deep forest green awning, aged brass fixtures.

Soft golden morning light, long shadows stretching east to west, dew on windows, 
gentle warm glow, pastel sky tones, low sun angle creating dimensional depth.

Balanced neutral tone, realistic color saturation, even lighting distribution, 
comfortable but not idealized, authentic texture representation, grounded atmosphere.

Partially obscured detail: unfamiliar silhouette visible in upper window (not usually there), 
atmospheric light fog softening street details, one window shows hurried movement inside, 
sense of anticipation, something is about to happen.

Familiar interior angle through main windows showing personal touches: your favorite table 
marked by the barista with reserved sign, photos of café regulars on wall including you, 
warm lighting emphasizing comfort, inviting but not intimate, sense of welcomed regular.

Painterly digital art style with photorealistic foundation. 45-degree corner view from 
street level, 30 feet from entrance, eye level 5.5 feet height, full building facade 
with 10% street context. 16:9 aspect ratio. Rule of thirds composition with café entrance 
as primary focal point. 3-layer depth: foreground (street pavement detail), mid-ground 
(café building), background (adjacent buildings and morning sky). Single golden morning 
sun as primary light source with soft ambient fill from overcast sky.
```

---

## Implementation Workflow

### Step 1: Location Database Entry
Every location stores:
```json
{
  "location_id": "riverside_cafe_001",
  "canonical_base_prompt": "A brick-facade corner café with...",
  "camera_anchor": {
    "angle": "45-degree corner view",
    "distance": "30 feet",
    "height": "eye level 5.5 feet",
    "framing": "full building facade with 10% street context"
  },
  "consistency_keywords": ["terracotta brick", "forest green awning", "gold lettering", "marble bar"],
  "signature_elements": ["floor-to-ceiling windows", "weathered wooden door", "exposed brick interior"]
}
```

### Step 2: Context Aggregation
At generation time, gather:
- Current turn (Morning/Afternoon/Evening)
- Current season (Spring/Summer/Fall/Winter)
- Player emotional capacity (0-10)
- Active narrative tension type (if any)
- NPC relationship level (if location-associated)

### Step 3: Prompt Assembly
```python
def assemble_location_prompt(location, game_context):
    prompt_parts = [
        location.canonical_base_prompt,
        get_time_layer(game_context.turn_time),
        get_season_layer(game_context.season),
        get_emotional_layer(game_context.player_capacity),
        get_tension_layer(game_context.active_tension),
        get_relationship_layer(location.associated_npc, game_context.relationship_level),
        location.technical_specs
    ]
    
    return " ".join([part for part in prompt_parts if part])
```

### Step 4: Quality Validation
After generation, validate:
- [ ] Canonical elements present (brick facade, green awning, gold lettering)
- [ ] Contextual modifiers applied correctly (morning light, medium capacity mood)
- [ ] No structural changes to base location (same windows, door, layout)
- [ ] Inference time <15ms
- [ ] Visual consistency score ≥0.85 compared to reference

### Step 5: Cache Management
- **Base location images**: Cache indefinitely (rarely change)
- **Context variants**: Cache by context hash (time_season_capacity_tension)
- **Relationship variants**: Generate on-demand (evolve frequently)
- **Memory optimization**: Preload likely next-turn contexts

---

## Variation Management

### Same Location, Different Contexts

The same "Riverside Café" should be **instantly recognizable** across all these contexts:

1. **Morning | High Capacity | No Tension | Level 1**
   - Result: Warm welcoming café exterior with morning light, observed from public distance

2. **Evening | Low Capacity | Stakes Escalation | Level 4**
   - Result: Same café with interior warm glow contrasting cold dusk, muted emotional tone, urgent atmosphere, intimate familiar details visible

3. **Afternoon | Crisis Capacity | Mystery Hook | Level 3**
   - Result: Same café desaturated and foreboding, harsh midday light, something unsettling visible in window, familiar but currently unwelcoming

All three maintain: brick facade, green awning, gold lettering, window layout, marble bar visible inside.

All three vary: lighting mood, color temperature, atmospheric weight, level of interior detail.

---

## Edge Cases & Solutions

### Problem: Location Visited Across Multiple Seasons
**Solution**: Season modifier updates vegetation and weather only—architecture unchanged.

### Problem: Relationship Drops from Level 4 to Level 2
**Solution**: Camera pulls back to less intimate angle; personal details remain in scene but less emphasized; lighting shifts from warm to neutral.

### Problem: Same Location, Two NPCs with Different Relationship Levels
**Solution**: Use highest relationship level if both are present; use specific NPC's level if solo encounter.

### Problem: Extreme Capacity (0/10) Makes Location Unrecognizable
**Solution**: Desaturate and darken BUT maintain structural clarity—never obscure signature elements completely. Location must remain identifiable even in crisis.

---

## Compliance Checklist

- [x] Uses canonical emotional capacity scale (0.0-10.0)
- [x] Respects relationship levels (0-5)
- [x] Incorporates narrative tension types (mystery_hook, partial_reveal, contradiction, stakes_escalation)
- [x] Aligns with visual generation system (on-device TensorFlow Lite, <15ms inference)
- [x] Maintains consistency anchors (camera angle, distance, height, framing)
- [x] Contextual integration with OCEAN, emotional state, relationship progression, memory resonance
- [x] Performance targets (<15ms inference, <50MB model size, 60 FPS gameplay)
- [x] Privacy-first (on-device generation, offline capability)
- [x] This doc cites **Truths v1.2**

---

**Document Version:** v1.0  
**Last Updated:** October 15, 2025  
**Canonical Reference:** Master Truths v1.2  
**Related Docs**: `visual_generation_tech.md`, `Image Generation.md`

