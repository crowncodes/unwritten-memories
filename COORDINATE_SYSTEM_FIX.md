# Coordinate System Debug & Fix

## Issue Identified

The game viewport was using a **center-anchored camera** which created confusing coordinate calculations:
- Camera anchor: `Anchor.center`
- Camera position: `(960, 540)`
- Result: Unclear what world coordinates map to screen positions

## Root Cause

With center anchor, the camera was looking at world position (960, 540) and placing it at the center of the viewport. This meant:
- Visible area was technically correct (0, 0) to (1920, 1080)
- But positioning logic was confusing and error-prone
- Cards were being positioned relative to center, not top-left origin

## Solution Applied

Changed camera setup to **top-left anchor** for clarity:

```dart
// OLD (confusing):
gameCamera.viewfinder.anchor = Anchor.center;
gameCamera.viewfinder.position = Vector2(viewportWidth / 2, viewportHeight / 2);

// NEW (clear):
gameCamera.viewfinder.anchor = Anchor.topLeft;
gameCamera.viewfinder.position = Vector2.zero();
```

## Result

**Clear coordinate system:**
- Viewport: 1920x1080 logical units
- Visible area: (0, 0) to (1920, 1080)
- World origin: Top-left corner at (0, 0)

**Card positioning:**
- Hand base Y: 1178 (1080 + 98)
  - Bottom half of cards (98px) extends below screen
  - Top half visible (98px above Y=1080)
- Active card Y: 820
  - Fully visible in lower-middle area
- Center X: 960

**Drop zones:**
- Center Y: 520
- Horizontally centered with 36px gaps

## Expected Behavior After Fix

1. **Cards at rest:** Bottom half off-screen, fanned layout visible
2. **Active card:** Pops up to Y=820, fully visible, enlarged
3. **Drop zones:** Centered horizontally at Y=520
4. **Clusters:** Positioned on sides with correct overflow handling

## Debug Logging Added

```dart
// Camera setup logging
AppLogger.info('Camera setup complete', data: {
  'viewport_logical': '1920x1080',
  'visible_area': '(0,0) to (1920,1080)',
  'camera_position': '[0.0, 0.0]',
  'camera_anchor': 'topLeft',
});

// Card position logging
AppLogger.info('Card position updated', data: {
  'card_id': 'card_1',
  'position': '(960.0, 1178.0)',
  'isActive': false,
  'anchor': 'bottomCenter',
});
```

## Testing Checklist

- [ ] Cards appear with bottom half off-screen
- [ ] Tap card → pops up to center, fully visible
- [ ] Drag card → follows cursor with physics
- [ ] Release outside zone → returns to active hover position
- [ ] Tap outside → card slides back to hand
- [ ] Drop zones centered horizontally
- [ ] Clusters don't overflow viewport
- [ ] Phase selector tabs positioned correctly at top

## Files Modified

1. `unwritten_game_world.dart` - Camera setup fix
2. `card_game_component.dart` - Added position logging
3. `game_board_screen.dart` - Reduced hand reserved height

## Technical Details

**Flame Camera System:**
- `withFixedResolution(1920, 1080)` creates logical viewport
- Components use world coordinates (0-1920, 0-1080)
- Camera auto-scales to actual window size
- Maintains aspect ratio with letterboxing if needed

**Component Anchors:**
- Cards: `Anchor.bottomCenter` (position is bottom-center point)
- Drop zones: `Anchor.center` (position is center point)
- Camera: `Anchor.topLeft` (clean origin-based system)

**Position Calculations:**
```dart
// Card at bottom (half off-screen)
cardY = 1080 + 98 = 1178

// Card active (fully visible)
cardY = 820

// With bottomCenter anchor:
// - position.y = 1178 means bottom of card at Y=1178
// - Top of card = 1178 - 196 = 982 (visible from 982-1080)
// - Bottom of card = 1178 (off-screen from 1080-1178)
```
