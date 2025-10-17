# Location Image Generation - Complete Index & Usage Guide

> **Canonical Reference**: Master Truths v1.2  
> **System Documentation**: `location_image_generation_prompt_structure.md`  
> **Purpose**: Master index for all location examples and implementation guide

---

## System Overview

The **Location Image Generation System** creates consistent, recognizable location images that evolve contextually based on game state while maintaining architectural identity. Every location has:

1. **FIXED BASE**: Canonical architectural description (never changes)
2. **CONTEXT LAYERS**: Dynamic modifiers reflecting time, season, emotional capacity, narrative tension, and relationship level

### Core Formula
```
Final Image = FIXED_BASE + TIME/SEASON + EMOTIONAL_ATMOSPHERE + NARRATIVE_TENSION + RELATIONSHIP_CONTEXT + TECHNICAL_SPECS
```

---

## Available Location Examples

### 1. Riverside Café
**File**: `riverside_cafe_examples.md`  
**Type**: Urban Commercial - Corner Café  
**Best For**: Relationship building, routine establishment, social interactions

#### Fixed Elements
- Brick facade with terracotta color
- Floor-to-ceiling windows
- Forest green awning
- Gold hand-painted lettering
- Marble-topped bar
- Vintage aesthetic

#### Context Variations (5 Examples)
| Example | Capacity | Season | Time | Tension | Level | Key Features |
|---------|----------|--------|------|---------|-------|--------------|
| 1 | 9.0/10 | Spring | Morning | None | 1 | First visit, optimistic discovery |
| 2 | 3.5/10 | Fall | Evening | Mystery Hook | 3 | Unfamiliar figure, exhausted perception |
| 3 | 6.0/10 | Summer | Afternoon | Stakes Escalation | 4 | FOR SALE sign, bittersweet urgency |
| 4 | 1.5/10 | Winter | Morning | Contradiction | 5 | Closed when should be open, crisis |
| 5 | 8.5/10 | Spring | Afternoon | Partial Reveal | 2 | Renovation mystery, curious |

**Use Cases**:
- NPC's workplace (barista, owner)
- Regular meeting spot for characters
- Social hub for community interactions
- Routine establishment location

---

### 2. Riverside Park
**File**: `riverside_park_examples.md`  
**Type**: Urban Outdoor - Waterfront Park  
**Best For**: Meaningful conversations, exercise routines, emotional processing

#### Fixed Elements
- Curved stone walking path
- Historic wrought-iron pedestrian bridge
- Mature weeping willow trees
- Victorian lamp posts (black with glass)
- Wooden benches facing water
- 40-foot wide river

#### Context Variations (4 Examples)
| Example | Capacity | Season | Time | Tension | Level | Key Features |
|---------|----------|--------|------|---------|-------|--------------|
| 1 | 8.0/10 | Summer | Evening | None | 0 | First discovery, golden hour beauty |
| 2 | 3.0/10 | Fall | Morning | Mystery Hook | 3 | Flowers on "your bench", foggy concern |
| 3 | 5.5/10 | Spring | Afternoon | Stakes Escalation | 4 | Friend moving away, urgent conversation |
| 4 | 0.5/10 | Winter | Evening | Contradiction | 5 | Friend where shouldn't be, crisis |

**Use Cases**:
- Running/exercise routine with friend
- Deep conversation setting
- Emotional processing location
- Relationship milestone moments

---

### 3. Sarah's Apartment
**File**: `sarah_apartment_examples.md`  
**Type**: Private Residential - Studio Apartment  
**Best For**: Intimate conversations, vulnerability moments, private revelations

#### Fixed Elements
- Exposed brick wall (left side)
- Bay window with built-in seat
- Honey oak hardwood floors
- Hexagonal kitchen tiles
- Sage green bookshelf
- Plants on every surface
- Vintage brass fixtures

#### Context Variations (4 Examples)
| Example | Capacity | Season | Time | Tension | Level | Key Features |
|---------|----------|--------|------|---------|-------|--------------|
| 1 | 8.0/10 | Spring | Morning | None | 2 | First visit, coffee invitation, boundaries |
| 2 | 3.0/10 | Fall | Evening | Mystery Hook | 3 | Unusual chaos, friend concern |
| 3 | 6.0/10 | Summer | Afternoon | Stakes Escalation | 4 | Major decision visible, your importance |
| 4 | 1.0/10 | Winter | Evening | Partial Reveal | 5 | Your crisis, discover her hidden crisis |

**Use Cases**:
- Private vulnerable conversations
- Relationship deepening moments
- Discovery of character depth
- Intimate life glimpses

---

### 4. TechFlow Office
**File**: `tech_office_examples.md`  
**Type**: Professional Workspace - Open Plan Office  
**Best For**: Work relationships, professional stakes, career decisions

#### Fixed Elements
- 14th floor glass facade
- Floor-to-ceiling windows
- Concrete ceiling with black ductwork
- Polished concrete floors
- Teal geometric logo wall
- Yellow-teal collaboration furniture
- Coral acoustic baffles

#### Context Variations (4 Examples)
| Example | Capacity | Season | Time | Tension | Level | Key Features |
|---------|----------|--------|------|---------|-------|--------------|
| 1 | 9.0/10 | Spring | Morning | None | 1 | First day excitement, evaluation |
| 2 | 3.5/10 | Summer | Afternoon | Mystery Hook | 3 | Colleague suddenly in closed meeting |
| 3 | 5.5/10 | Fall | Evening | Stakes Escalation | 4 | Partner considering leaving, deadline |
| 4 | 1.5/10 | Winter | Morning | Contradiction | 5 | Work anchor destabilized, crisis |

**Use Cases**:
- Professional relationship building
- Career-related decisions
- Work-life balance tensions
- Collaborative achievement moments

---

## Implementation Guide

### Step 1: Choose Location Type

**Decision Tree**:

```
SOCIAL INTERACTION NEEDED?
├─ YES → Public space (Café, Park)
│  ├─ Food/drink involved? → Café
│  └─ Physical activity/nature? → Park
└─ NO → Private space (Apartment, Office)
   ├─ Professional context? → Office
   └─ Personal intimacy? → Apartment
```

### Step 2: Determine Context Layers

Gather from game state:

```python
context = {
    "time": game.current_turn.time,  # Morning/Afternoon/Evening
    "season": game.current_season,    # Spring/Summer/Fall/Winter
    "player_capacity": game.player.emotional_capacity,  # 0.0-10.0
    "narrative_tension": game.current_tension,  # none|mystery|stakes|contradiction|partial_reveal
    "npc_relationship": game.relationships[npc_id].level,  # 0-5
    "npc_id": npc_id  # If location associated with NPC
}
```

### Step 3: Assemble Prompt

```python
def generate_location_image(location_id, context):
    location = LOCATION_DATABASE[location_id]
    
    # Start with fixed base
    prompt_parts = [location.canonical_base_prompt]
    
    # Add context layers
    prompt_parts.append(get_time_layer(context.time, context.season))
    prompt_parts.append(get_season_layer(context.season))
    prompt_parts.append(get_emotional_layer(context.player_capacity))
    
    if context.narrative_tension != "none":
        prompt_parts.append(get_tension_layer(context.narrative_tension))
    
    if context.npc_id and context.npc_relationship > 0:
        prompt_parts.append(get_relationship_layer(
            context.npc_relationship,
            location,
            context.npc_id
        ))
    
    # Add technical specs
    prompt_parts.append(location.technical_specs)
    
    return " ".join(prompt_parts)
```

### Step 4: Generate & Validate

```python
# Generate image
image = tf_lite_model.generate(prompt)

# Validate consistency
validation = validate_location_image(
    image,
    location.signature_elements,
    location.consistency_anchors
)

if validation.score < 0.85:
    # Retry with adjusted prompt
    image = regenerate_with_correction(prompt, validation.issues)

return image
```

---

## Context Layer Specifications

### Time of Day Modifiers

| Time | Light Source | Color Temp | Shadow Length | Atmosphere |
|------|--------------|------------|---------------|------------|
| **Morning** (6-11 AM) | Sun 15-45° | 3600-4200K | Long east→west | Golden, fresh, beginning |
| **Afternoon** (12-5 PM) | Sun 45-70° | 5000-5500K | Short beneath | Bright, clear, active |
| **Evening** (6-11 PM) | Sun 0-15° + artificial | 2700-3500K | Long west→east | Warm interior, cool exterior |

### Season Modifiers

| Season | Foliage | Weather | Color Palette | Atmosphere |
|--------|---------|---------|---------------|------------|
| **Spring** | Fresh green, blooms | Rain, renewal | Pastels, bright greens | Growth, possibility |
| **Summer** | Lush full | Heat, long days | Saturated, vibrant | Peak, abundance |
| **Fall** | Amber/rust, falling | Cooler, shorter days | Warm earth tones | Transition, melancholy |
| **Winter** | Bare, frost | Cold, snow | Muted, blue-gray | Harsh, isolation |

### Emotional Capacity Layers

| Capacity | Saturation | Color Temp Shift | Shadow Weight | Mood Keywords |
|----------|------------|------------------|---------------|---------------|
| **8-10/10** (High) | +15-20% | Warm lift | Light (30-40%) | Vibrant, inviting, clear |
| **5-7/10** (Medium) | Baseline | Neutral | Medium (40-50%) | Realistic, grounded, functional |
| **2-4/10** (Low) | -25-35% | Cool shift | Heavy (55-65%) | Muted, drained, distant |
| **0-1/10** (Crisis) | -70-80% | Very cool | Overwhelming (80-90%) | Monochrome, oppressive, tunnel vision |

### Narrative Tension Types

| Type | Visual Cues | Payoff Timeline | Example |
|------|-------------|-----------------|---------|
| **Mystery Hook** | Unexplained element, partial obscurity | 2-4 weeks | Unfamiliar figure, unexpected object |
| **Partial Reveal** | Visible effect without cause | 2-4 weeks | Evidence of event, unexplained change |
| **Contradiction** | Violation of established pattern | 5-8 weeks | Character where shouldn't be, against nature |
| **Stakes Escalation** | Deadline visible, urgency cues | Immediate-4 weeks | FOR SALE sign, decision documents, timer |

### Relationship Level Detail

| Level | Interior Access | Personal Markers | Camera Distance | Visible Details |
|-------|----------------|------------------|-----------------|-----------------|
| **0** (Not Met) | Public exterior only | None | 30+ feet | Architecture only |
| **1** (Stranger) | Public areas glimpsed | Generic | 25-30 feet | General layout |
| **2** (Acquaintance) | Interior glimpse | Personality hints | 20-25 feet | Some character visible |
| **3** (Friend) | Familiar angles | Your gifts visible | 15-20 feet | Shared history markers |
| **4** (Close Friend) | Intimate details | Deep integration | 10-15 feet | Imperfections comfortable |
| **5** (Soulmate) | Complete access | Maximum enmeshment | 5-10 feet | Chosen family markers |

---

## Performance Optimization

### Caching Strategy

```python
cache_structure = {
    "base_images": {
        # Cache indefinitely - architectural bases rarely change
        "riverside_cafe_base": {
            "prompt_hash": "abc123",
            "image": image_data,
            "generated": timestamp,
            "ttl": None  # Permanent
        }
    },
    "context_variants": {
        # Cache by context hash - seasonal/time variants
        "riverside_cafe_spring_morning_high_capacity": {
            "prompt_hash": "def456",
            "image": image_data,
            "generated": timestamp,
            "ttl": 3600  # 1 hour (may reuse)
        }
    },
    "relationship_variants": {
        # Generate on-demand - evolve frequently
        # Don't cache - always fresh for current relationship state
    }
}
```

### Preloading Logic

```python
def preload_likely_contexts(game_state):
    current_time = game_state.current_turn.time
    current_location = game_state.player.current_location
    
    # Preload next likely time-of-day variant
    next_time = get_next_turn_time(current_time)
    preload_context(current_location, next_time)
    
    # Preload locations player is likely to visit next
    likely_locations = get_routine_locations(game_state.player)
    for location in likely_locations[:3]:  # Top 3 most likely
        preload_base_image(location)
```

### Inference Optimization

**Target**: <15ms per generation on mid-range devices

```python
optimization_strategies = {
    "model_quantization": "INT8 quantization for TFLite model",
    "resolution_scaling": "512x512 for backgrounds, 768x768 for featured",
    "batch_processing": "Generate multiple contexts in single inference when possible",
    "GPU_delegation": "Use GPU delegate when available",
    "model_pruning": "Remove unnecessary parameters while maintaining quality"
}
```

---

## Quality Validation

### Consistency Checklist

Every generated image must validate:

```python
def validate_location_consistency(image, location):
    checks = {
        "signature_elements_present": check_elements(
            image, 
            location.signature_elements,
            threshold=0.85  # 85% confidence all elements present
        ),
        "color_palette_match": check_palette(
            image,
            location.base_palette,
            tolerance=0.15  # 15% deviation allowed for context
        ),
        "camera_anchor_match": check_perspective(
            image,
            location.camera_anchor,
            threshold=0.90  # 90% match to specified angle/distance
        ),
        "architectural_proportions": check_proportions(
            image,
            location.spatial_layout,
            tolerance=0.10  # 10% variation allowed
        ),
        "context_applied": check_context_modifiers(
            image,
            context_layers,
            threshold=0.75  # 75% of context cues present
        )
    }
    
    overall_score = weighted_average(checks)
    return ValidationResult(
        passed=overall_score >= 0.85,
        score=overall_score,
        issues=[k for k, v in checks.items() if v < threshold]
    )
```

### Context Appropriateness

Validate emotional capacity matches visual mood:

```python
def validate_capacity_match(image, context):
    image_mood_score = analyze_mood(image)  # 0.0-10.0
    expected_mood = context.player_capacity
    
    # Allow 2.0 point variation (capacity + mood filtering)
    deviation = abs(image_mood_score - expected_mood)
    
    return deviation <= 2.0
```

---

## Creating New Locations

### Template Structure

```markdown
# [Location Name] - Location Prompt Examples

> **Base Location**: [Type description]  
> **Canonical Reference**: Master Truths v1.2

---

## FIXED BASE (All Examples Use This)

```
[Detailed architectural description]
[Include 8-12 signature elements]
[Specify base color palette]
```

### Consistency Anchors
- **Camera angle**: [Specific angle description]
- **Distance**: [Specific distance]
- **Height**: [Specific height]
- **Framing**: [What's in frame]
- **Signature elements**: [List 5-8 key elements]

---

## Example 1: [Time] | [Capacity] | [Tension] | Level [X]

### Context
- **Turn**: [Specific time]
- **Season**: [Season]
- **Player Capacity**: [X.X/10]
- **Narrative Tension**: [Type]
- **NPC Relationship**: Level [X]

### Complete Prompt
[Full assembled prompt with all layers]

### Visual Characteristics
- **Mood**: [Keywords]
- **Color Temperature**: [Kelvin]
- **Saturation**: [Adjustment]
- **Shadow Density**: [Percentage]
- **Detail Level**: [Description]
- **Emotional Resonance**: [Keywords]
- **Narrative Hook**: [If applicable]
```

### Minimum Examples Per Location

Create at least **4 context variations** showing:
1. **High capacity + Low relationship** (discovery/evaluation)
2. **Low capacity + Medium relationship** (familiar comfort disrupted)
3. **Medium capacity + High relationship** (stakes affecting deep bond)
4. **Crisis capacity + Highest relationship** (anchor point tested)

Include variety of:
- All 4 times of day (prioritize 3 minimum)
- Multiple seasons (minimum 2)
- All tension types (minimum 3)
- Relationship progression (minimum 3 levels)

---

## Location Type Guidelines

### Public Spaces (Café, Park, Plaza)

**Characteristics**:
- Wide camera angles (15-30 feet)
- Multiple people visible (context crowds)
- Relationship shown through shared space markers
- Public behavior appropriate to context

**Relationship Progression**:
- Level 0-1: Exterior or public area only
- Level 2-3: Familiar spots, "your table/bench"
- Level 4-5: Personal markers visible, insider knowledge

### Private Spaces (Apartments, Houses)

**Characteristics**:
- Closer camera angles (5-15 feet)
- Personal details dominant
- Relationship shown through belonging markers
- Intimate viewing access

**Relationship Progression**:
- Level 0-1: Not applicable (don't enter until Level 2)
- Level 2: Guest perspective, public rooms
- Level 3-4: Familiar friend, personal touches visible
- Level 5: Complete access, your presence integrated

### Professional Spaces (Offices, Studios)

**Characteristics**:
- Medium camera angles (10-25 feet)
- Workspace integration visible
- Relationship shown through collaboration markers
- Professional context maintained

**Relationship Progression**:
- Level 0-1: Visitor/new colleague perspective
- Level 2-3: Colleague, shared projects visible
- Level 4: Partner, deep integration
- Level 5: Work soulmate, merged identity

---

## Troubleshooting Common Issues

### Problem: Generated images don't look consistent

**Solutions**:
1. Verify signature elements in prompt (need 5-8 specific anchors)
2. Check consistency score threshold (should be ≥0.85)
3. Increase specificity of fixed base description
4. Add more architectural detail (materials, colors, proportions)

### Problem: Context modifiers too subtle/strong

**Solutions**:
1. Adjust saturation reduction percentages
2. Modify shadow opacity values
3. Tune color temperature shift amounts
4. Balance primary/secondary/tertiary lighting weights

### Problem: Relationship level changes not visible

**Solutions**:
1. Add more specific personal markers per level
2. Adjust camera distance per relationship tier
3. Include explicit "your contributions" in higher levels
4. Show progression through accumulating detail

### Problem: Narrative tension not communicated

**Solutions**:
1. Make tension visual elements more explicit
2. Use composition (rule of thirds) to emphasize hooks
3. Add specific contradictory elements
4. Include stakes countdown visual cues (signs, deadlines)

---

## Analytics & Metrics

Track for optimization:

```python
location_metrics = {
    "generation_time_ms": [12, 14, 11, 15],  # Target: <15ms
    "consistency_scores": [0.87, 0.91, 0.89],  # Target: ≥0.85
    "cache_hit_rate": 0.73,  # Target: ≥0.70
    "player_recognition_rate": 0.94,  # Do players recognize location?
    "context_appropriateness": 0.88,  # Does mood match capacity?
    "memory_usage_mb": 45,  # Target: <50MB per location
}
```

---

## Compliance Checklist

Every location document must include:

- [ ] Fixed base with 8-12 signature elements
- [ ] Consistency anchors (angle, distance, height, framing)
- [ ] Base color palette specified
- [ ] Minimum 4 context variation examples
- [ ] All capacity ranges represented (high/medium/low/crisis)
- [ ] Minimum 3 relationship levels shown
- [ ] Multiple seasons and times of day
- [ ] At least 3 tension types demonstrated
- [ ] Complete prompt for each example
- [ ] Visual characteristics table per example
- [ ] Comparison analysis showing what stays/changes
- [ ] Validation checklist
- [ ] Cites Master Truths v1.2

---

## Quick Reference

### Location Selection by Scene Need

| Need | Location | File |
|------|----------|------|
| Casual social | Riverside Café | `riverside_cafe_examples.md` |
| Deep conversation | Riverside Park | `riverside_park_examples.md` |
| Intimate reveal | Sarah's Apartment | `sarah_apartment_examples.md` |
| Professional stakes | TechFlow Office | `tech_office_examples.md` |

### Capacity to Visual Mapping

| Capacity | Saturation | Temp | Shadows | Keywords |
|----------|-----------|------|---------|----------|
| 8-10 | +20% | Warm | 30% | Vibrant, clear, inviting |
| 5-7 | 0% | Neutral | 45% | Realistic, grounded |
| 2-4 | -30% | Cool | 60% | Muted, drained |
| 0-1 | -75% | Very cool | 85% | Monochrome, oppressive |

### Tension to Visual Mapping

| Tension | Visual Element | Timeline |
|---------|---------------|----------|
| Mystery Hook | Unexplained presence/absence | 2-4 weeks |
| Partial Reveal | Effect without cause | 2-4 weeks |
| Contradiction | Pattern violation | 5-8 weeks |
| Stakes Escalation | Deadline/urgency visible | Immediate |

---

**Document Version:** v1.0  
**Last Updated:** October 15, 2025  
**Total Locations**: 4 (20 total context variations)  
**Canonical Reference:** Master Truths v1.2

**Related Documentation**:
- `location_image_generation_prompt_structure.md` - System architecture
- `visual_generation_tech.md` - Technical implementation
- `Image Generation.md` - General visual generation overview

