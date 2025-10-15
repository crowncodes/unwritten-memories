# Marcus Chen - Level 4 Holo Card Animation Prompt

**For generating premium animated portrait loop using Runway ML, Pika Labs, or similar AI video tools**

---

## VIDEO GENERATION PROMPT

```
Generate a premium holo-style animated portrait loop of Marcus Chen, 29-year-old male aspiring documentary filmmaker, at evolution level 4.

CHARACTER IDENTITY:
- East Asian male with defined cheekbones and strong jawline
- Deep brown almond-shaped eyes, alert and passionate
- Black medium-length hair, deliberately styled
- Light olive skin tone with healthy outdoor glow
- Genuine confident smile, open and purposeful
- Well-groomed stubble

SIGNATURE ITEMS (MUST MAINTAIN):
- Worn vintage olive green bomber jacket (iconic, weathered)
- Burgundy flannel shirt underneath
- Silver chain necklace visible at collar
- Circular wire-frame glasses with slight tint
- Vintage Nikon F3 camera hanging from neck strap
- Worn Moleskine notebook tucked under arm
- Coffee cup from independent café in hand
- Small film reel enamel pin on jacket collar

ENVIRONMENT:
- Urban street environment at golden hour
- Brick walls and hints of street art in background
- Bokeh from city lights beginning to glow at dusk
- Documentary subject visible as soft silhouette in far background
- Warm golden and deep blue color palette
- ENTIRE SCENE has persistent holographic rainbow shimmer overlay (like a holographic trading card)

ANIMATION SPECIFICATIONS:
- Duration: 7 seconds SEAMLESS LOOP, 30fps, 1024x1024
- CRITICAL LOOP REQUIREMENT: The last frame must be identical or nearly identical to the first frame
- All motion must return to starting position by frame 210 (7 seconds × 30fps)
- Test by playing frames 1-210-1-210 - there should be no visible jump or pop
- Use ease-in-out timing for all movements so they smoothly reverse
- Format: WebM (VP9) or MP4, file size target <10MB
- Style: Cinematic, documentary photography aesthetic with PERSISTENT holographic overlay
- The entire video has a holographic foil effect - NEVER plain/regular video at any point
- No audio, no text overlays, no logos
- Keep exact same facial identity and anatomy throughout

MOTION LAYERS:

1. BASE LAYER (Static Portrait):
   - Main character portrait as anchor
   - Maintains core composition and lighting

2. DEPTH LAYER (Parallax Background):
   - Brick wall and urban background shift slowly (2px drift)
   - Street art and building elements move at 0.3x speed of foreground
   - Bokeh lights gently float upward
   - Background silhouettes slightly sway

3. LIGHT LAYER (Holographic Shimmer):
   - CRITICAL: Holographic foil effect is ALWAYS VISIBLE for the entire 7 seconds
   - The entire portrait has a persistent rainbow holographic overlay throughout
   - What sweeps: The DIRECTION and intensity of the shimmer gradient rotates
   - Gradient angle rotates smoothly from -30° to +30° and back continuously
   - Think: Trading card holographic foil that's always shimmering, the light just moves across it
   - Foil colors always present: #FFD479 (gold), #5FD9E7 (cyan), #F1B6FF (violet)
   - Base intensity: 0.75 constant, with shimmer highlights moving across surface
   - Extra shimmer intensity on metallic surfaces: camera lens, glasses, silver chain
   - The portrait should NEVER look like regular video - it's always holographic

4. MOTION LAYER (Micro-animations):
   - Eyes blink naturally every 4.5 seconds
   - Subtle breathing motion (chest rises/falls amplitude: 0.3)
   - Hair gently sways from urban breeze (amplitude: 0.25)
   - Bomber jacket collar and flannel subtly move with breath
   - Camera strap shows slight physics-based sway
   - Coffee cup steam rises gently (if visible)

EMOTION CURVE (Blendshape Timeline):
- t=0.0 (0 sec): Confident expression, intensity 0.4
- t=0.35 (2.45 sec): Smile brightens to passionate, intensity 0.65
- t=0.7 (4.9 sec): Returns to confident serene, intensity 0.4
- t=1.0 (7 sec): Loop seamlessly back to start

CAMERA MOVEMENT:
- Slow push-in (dolly forward 3%)
- Parallax layers: 2 (subject + background)
- Focus depth: Subject
- Movement speed: 0.2 (very subtle)

PARTICLE EFFECTS:
- Count: 12-16 active particles
- Type: "page_glint" and "dust_mote"
- Spawn area: Around camera equipment and notebook
- Lifetime: 2.4 seconds per particle
- Size: 2-6 pixels
- Behavior: Drift upward and outward, shimmer in golden light
- Color: Warm gold with holographic rainbow edge

FOIL SHIMMER DETAILS:
- Diagonal gradient sweep from upper-left to lower-right
- Speed: 0.35 (moderate, elegant)
- Follows contours of face, jacket, and camera
- Extra intensity on metallic surfaces (camera, glasses, necklace)
- Particle trails follow bomber jacket edges and camera strap

COLOR GRADING:
- LUT: Golden hour cinematic
- Temperature: +0.3 (warm)
- Tint: +0.05 (slight magenta for skin warmth)
- Contrast: Medium-high
- Saturation: 1.1 (slightly enhanced)

TECHNICAL EXPORT SETTINGS:
- Resolution: 1024x1024
- FPS: 30 (locked)
- Codec: VP9 (WebM) or H.264 (MP4)
- Loop: Seamless (first and last frame blend)
- Alpha channel: False (dark gradient background)
- Compression target: 10MB maximum
- Quality: Ultra
- Audio: None

STYLE DIRECTION:
- Clean illustrated style with cinematic quality
- Documentary photography meets premium collectible card
- Rich color palette: olive green, burgundy, golden yellows, deep blues
- Think: "Hearthstone golden card meets high-end portrait photography"
- Natural realism with subtle magical shimmer
- Emotionally warm and inspiring
- Professional but authentic, not corporate

CRITICAL CONSISTENCY NOTES:
- Facial structure must remain EXACTLY the same throughout
- Bomber jacket must be visible and consistent
- All signature items present in every frame
- Motion should be subtle and elegant, never jarring
- Loop must be perfectly seamless (no pop or jump)
- Maintain documentary filmmaker aesthetic throughout

NEGATIVE PROMPTS:
- No floating objects or awkward physics
- No dramatic fantasy effects or overstyled look
- No anime or cartoon style
- No multiple people or face changes
- No overly bright or neon colors
- No text, logos, or UI elements
- No audio or music
- No abrupt movements or cuts
- No photorealism (maintain illustrated style)
```

---

## METADATA FOR GAME INTEGRATION

```json
{
  "animation_id": "marcus_chen_filmmaker_holo_l4",
  "npc_id": "marcus-chen",
  "level": 4,
  "rarity": "Epic",
  "style_pack": "Documentary Cinematic",
  "loop_duration": 7.0,
  "fps": 30,
  "resolution": "1024x1024",
  
  "layers": {
    "base": "portrait_marcus_l4_base.png",
    "depth": "urban_background_parallax.png",
    "light": "golden_foil_pass.glow",
    "motion": "expression_confidence_curve.anim"
  },
  
  "effects": {
    "foil_shimmer": true,
    "light_rays": "golden_hour_diffuse",
    "particle_sparks": 14,
    "expression_curve": ["confident", "passionate", "confident"],
    "holographic_overlay": true
  },
  
  "camera": {
    "movement": "slow_push_in",
    "parallax_layers": 2,
    "focus_depth": "subject",
    "movement_speed": 0.2
  },
  
  "micro_motion": {
    "blink_interval_sec": 4.5,
    "breath_amplitude": 0.3,
    "hair_sway": 0.25,
    "cloth_sway": 0.25
  },
  
  "foil": {
    "enabled": true,
    "intensity": 0.75,
    "gradient": {
      "palette": ["#FFD479", "#5FD9E7", "#F1B6FF"],
      "direction_deg": -30,
      "speed": 0.35
    },
    "particles": {
      "count": 14,
      "type": "page_glint",
      "spawn_area": "subject",
      "lifetime_sec": 2.4,
      "size_px": [2, 6]
    }
  },
  
  "export": {
    "webm": "cdn://unwritten/video/holo/marcus_filmmaker_l4_v1.webm",
    "mp4": "cdn://unwritten/video/holo/marcus_filmmaker_l4_v1.mp4",
    "poster_frame": "cdn://unwritten/posters/marcus_l4_poster.png",
    "alpha_channel": false,
    "file_size_mb": 9.8
  },
  
  "unlock": {
    "conditions": [
      "npc:marcus-chen.level>=4",
      "account:premium=true"
    ],
    "grants": [
      "achievement:documentary_passion",
      "gallery:epic_holo_slot+1"
    ]
  },
  
  "economy": {
    "is_premium": true,
    "price_usd": 2.49,
    "auto_unlock_at_level": 4
  },
  
  "i18n": {
    "display_name": "Marcus — Filmmaker Awakening (Epic Holo)",
    "tagline": "Finding purpose, one frame at a time.",
    "description": "Golden hour urban scene with parallax depth, holographic shimmer following camera equipment, and a smile that brightens with renewed passion."
  }
}
```

---

## VISUAL REFERENCE GUIDE

**Key Animation Moments:**

**0:00-0:20** - Opens with confident expression, gentle blink
**0:20-0:40** - Camera slowly pushes in, foil shimmer sweeps left to right
**0:40-2:45** - Background parallax becomes noticeable, particles begin drifting
**2:45-3:50** - Expression shifts to passionate smile (emotion curve peak)
**3:50-4:90** - Holographic gradient completes second cycle
**4:90-6:00** - Expression returns to confident serene
**6:00-7:00** - Seamless blend back to frame 0

**Particle Behavior:**
- 2-3 particles spawn per second
- Rise slowly from camera and notebook
- Shimmer with golden-cyan-violet gradient
- Fade out after 2.4 seconds
- Never more than 16 active at once

**Foil Shimmer Path:**
- Starts upper-left corner
- Sweeps diagonally across face and bomber jacket
- Highlights camera lens glass with extra intensity
- Catches glasses frames with rainbow reflection
- Completes sweep at lower-right corner
- Loops 2.5 times during 7-second duration

---

## ALTERNATIVE PROMPT (Simplified for AI Video Tools)

```
Create a 7-second looping animated portrait of an East Asian male filmmaker, age 29, wearing olive green bomber jacket and circular glasses, holding vintage camera. Golden hour urban background with gentle parallax. Subject blinks naturally, breathes subtly, hair sways gently. Holographic foil shimmer sweeps diagonally across image with rainbow gradient. Small glowing particles drift around camera equipment. Warm cinematic color grading. Expression shifts from confident to passionate smile and back. 1024x1024, 30fps, seamless loop. Style: illustrated realism with premium collectible card aesthetic.
```

---

## QUALITY CHECKLIST

Before finalizing the animation, verify:

- ✅ Loop is perfectly seamless (no visible jump)
- ✅ Facial features remain consistent throughout
- ✅ All signature items visible in every frame
- ✅ Motion is subtle and elegant (not exaggerated)
- ✅ Foil shimmer is visible but not overwhelming
- ✅ Particles enhance but don't distract
- ✅ File size under 10MB
- ✅ Resolution exactly 1024x1024
- ✅ FPS locked at 30
- ✅ Emotion curve feels natural and authentic
- ✅ Background parallax is smooth
- ✅ Color grading consistent throughout
- ✅ No audio present
- ✅ No text or UI elements visible
- ✅ Maintains documentary filmmaker aesthetic