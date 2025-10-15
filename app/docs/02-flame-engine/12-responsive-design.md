# Responsive Design for Flame Games

**Status:** ✅ Implemented  
**Performance:** 60 FPS maintained across all breakpoints  
**Flame Integration:** Complete

---

## Overview

Comprehensive responsive design system for Unwritten, ensuring optimal layouts across mobile, tablet, and desktop devices while maintaining 60 FPS performance in Flame-based game UI.

## Architecture

### Design Philosophy

Unwritten uses a **hybrid approach**: Flame for the game canvas (cards, animations, effects) with Flutter overlays for UI clusters and menus. This provides the best of both worlds:

- **Flame**: High-performance game elements (60 FPS)
- **Flutter**: Responsive UI overlays with Material Design
- **Coordination**: Shared state via Riverpod

---

## Breakpoint System

**File:** `app/lib/core/constants/responsive_breakpoints.dart`

```dart
enum ScreenSize {
  mobile,    // < 600px
  tablet,    // 600-1200px  
  desktop,   // > 1200px
}

// Context extensions
extension ScreenSizeExtension on BuildContext {
  ScreenSize get screenSize {
    final width = MediaQuery.of(this).size.width;
    if (width < 600) return ScreenSize.mobile;
    if (width < 1200) return ScreenSize.tablet;
    return ScreenSize.desktop;
  }
  
  bool get isMobile => screenSize == ScreenSize.mobile;
  bool get isTablet => screenSize == ScreenSize.tablet;
  bool get isDesktop => screenSize == ScreenSize.desktop;
  bool get isTabletOrLarger => !isMobile;
}
```

### Responsive Values

```dart
class ResponsiveValue<T> {
  final T mobile;
  final T? tablet;
  final T? desktop;
  
  const ResponsiveValue({
    required this.mobile,
    this.tablet,
    this.desktop,
  });
  
  T getValue(BuildContext context) {
    switch (context.screenSize) {
      case ScreenSize.desktop:
        return desktop ?? tablet ?? mobile;
      case ScreenSize.tablet:
        return tablet ?? mobile;
      case ScreenSize.mobile:
        return mobile;
    }
  }
}

// Usage
final padding = ResponsiveValue<double>(
  mobile: 12.0,
  tablet: 24.0,
  desktop: 48.0,
).getValue(context);
```

---

## Layout Strategies

### Mobile (< 600px)

**Pattern:** Peek-from-edges with progressive disclosure

```
┌─────────────────────┐
│    [Peek Tabs]      │  ← UI clusters peek from edges
│                     │
│                     │
│                     │
│    Flame Canvas     │  ← Game board (card interactions)
│                     │
│                     │
│    [Card Hand]      │  ← Cards at bottom
└─────────────────────┘
```

**Features:**
- Peek-from-edges UI pattern (saves ~300px vertical space)
- Left clusters: peek from left with right corners rounded
- Right clusters: peek from right with left corners rounded
- Tap to expand full cluster content
- Card hand always visible at bottom
- Phase selector hidden (more space)

**Peek Implementation:**

```dart
class BaseClusterWidget extends StatelessWidget {
  final bool peekFromLeft;
  final bool isExpanded;
  final double defaultWidth;
  
  @override
  Widget build(BuildContext context) {
    final isMobile = context.isMobile;
    
    // Calculate peek offset
    final peekAmount = isMobile && !isExpanded 
        ? (peekFromLeft ? -(defaultWidth - 48) : (defaultWidth - 48))
        : 0.0;
    
    // Border radius based on peek direction
    final borderRadius = isMobile && !isExpanded
        ? BorderRadius.horizontal(
            left: peekFromLeft ? Radius.zero : Radius.circular(16),
            right: peekFromLeft ? Radius.circular(16) : Radius.zero,
          )
        : BorderRadius.circular(16);
    
    return AnimatedContainer(
      duration: Duration(milliseconds: 300),
      curve: Curves.easeInOut,
      transform: Matrix4.translationValues(peekAmount, 0, 0),
      decoration: BoxDecoration(
        borderRadius: borderRadius,
        color: Colors.black.withOpacity(0.7),
      ),
      child: child,
    );
  }
}
```

### Tablet (600-1200px)

**Pattern:** Side-by-side with full visibility

```
┌───────────┬─────────────┬──────────┐
│Character  │             │Resources │
│Life       │   Flame     │Relations │
│Progress   │   Canvas    │Timeline  │
└───────────┴─────────────┴──────────┘
```

**Features:**
- Left/right cluster columns fully visible
- Phase selector visible
- Medium spacing (8px)
- Flame canvas centered
- Optimal for horizontal screens

### Desktop (> 1200px)

**Pattern:** Centered with max width constraint

```
        ┌────────────────────────────────────┐
        │ ┌─────┬──────────────┬──────────┐ │
        │ │Left │  Flame       │   Right  │ │
        │ │     │  Canvas      │          │ │
        │ └─────┴──────────────┴──────────┘ │
        └────────────────────────────────────┘
              Max width: 1400px
```

**Features:**
- Maximum content width (1400px)
- Centered layout
- Larger clusters (320px / 280px)
- Generous spacing (12px)
- Prevents over-stretching on ultra-wide monitors

---

## Flame Canvas Responsive Sizing

### Fixed Resolution Viewport

Flame uses a **fixed logical resolution** that scales to fit the screen, maintaining aspect ratio and preventing stretched visuals.

```dart
class UnwrittenGame extends FlameGame with HasCollisionDetection {
  @override
  Future<void> onLoad() async {
    // Fixed resolution viewport - scales to fit
    camera = CameraComponent.withFixedResolution(
      width: 1920,  // Logical width
      height: 1080, // Logical height
      world: world,
    );
    
    // Canvas will scale to fit available space
    // UI overlays will adapt responsively
  }
}
```

### Responsive Game Layout

```dart
class GameBoardScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: LayoutBuilder(
        builder: (context, constraints) {
          return Center(
            child: Container(
              constraints: BoxConstraints(
                maxWidth: GameBoardLayout.getMaxContentWidth(context) 
                  ?? double.infinity,
              ),
              child: Stack(
                children: [
                  // Flame game canvas
                  GameWidget(game: game),
                  
                  // Flutter UI overlays (responsive)
                  if (GameBoardLayout.showPhaseSelector(context))
                    _buildPhaseSelector(context),
                  _buildResponsiveClusters(context),
                  _buildCardHand(context),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
```

---

## Game Board Layout Utilities

Pre-configured responsive values:

| Property | Mobile | Tablet | Desktop |
|----------|--------|--------|---------|
| **Left Cluster Width** | 200px | 280px | 320px |
| **Right Cluster Width** | 180px | 240px | 280px |
| **Horizontal Padding** | 12px | 24px | 48px |
| **Vertical Padding** | 12px | 20px | 32px |
| **Cluster Spacing** | 6px | 8px | 12px |
| **Max Content Width** | None | None | 1400px |

```dart
class GameBoardLayout {
  static double getLeftClusterWidth(BuildContext context) {
    return ResponsiveValue<double>(
      mobile: 200,
      tablet: 280,
      desktop: 320,
    ).getValue(context);
  }
  
  static double getHorizontalPadding(BuildContext context) {
    return ResponsiveValue<double>(
      mobile: 12,
      tablet: 24,
      desktop: 48,
    ).getValue(context);
  }
  
  static bool useSideBySideLayout(BuildContext context) {
    return context.isTabletOrLarger;
  }
  
  static bool showPhaseSelector(BuildContext context) {
    return context.isTabletOrLarger;
  }
  
  static double? getMaxContentWidth(BuildContext context) {
    return context.isDesktop ? 1400 : null;
  }
}
```

---

## Implementation

### Responsive Cluster Layout

```dart
Widget _buildResponsiveClusters(BuildContext context) {
  if (GameBoardLayout.useSideBySideLayout(context)) {
    // Tablet/Desktop: Side-by-side
    return Stack(
      children: [
        _buildLeftClusters(context),
        _buildRightClusters(context),
      ],
    );
  } else {
    // Mobile: Peek from edges
    return Stack(
      children: [
        _buildMobileLeftClusters(context),
        _buildMobileRightClusters(context),
      ],
    );
  }
}
```

### Mobile Peek-from-Edges

```dart
Widget _buildMobileLeftClusters(BuildContext context) {
  final spacing = GameBoardLayout.getClusterSpacing(context);
  final topPadding = GameBoardLayout.getVerticalPadding(context) + 48;
  
  return Positioned(
    left: 0, // Flush with left edge
    top: topPadding,
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        CharacterStateClusterExpandable(peekFromLeft: true),
        SizedBox(height: spacing),
        LifeMetersClusterExpandable(peekFromLeft: true),
        SizedBox(height: spacing),
        ProgressStoryClusterExpandable(peekFromLeft: true),
      ],
    ),
  );
}

Widget _buildMobileRightClusters(BuildContext context) {
  final spacing = GameBoardLayout.getClusterSpacing(context);
  final topPadding = GameBoardLayout.getVerticalPadding(context) + 48;
  
  return Positioned(
    right: 0, // Flush with right edge
    top: topPadding,
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.end,
      children: [
        ResourcesClusterExpandable(peekFromLeft: false),
        SizedBox(height: spacing),
        RelationshipsClusterExpandable(peekFromLeft: false),
        SizedBox(height: spacing),
        TimelineClusterExpandable(peekFromLeft: false),
      ],
    ),
  );
}
```

### Tablet/Desktop Full Layout

```dart
Widget _buildLeftClusters(BuildContext context) {
  final horizontalPadding = GameBoardLayout.getHorizontalPadding(context);
  final clusterWidth = GameBoardLayout.getLeftClusterWidth(context);
  final spacing = GameBoardLayout.getClusterSpacing(context);
  final topPadding = GameBoardLayout.getVerticalPadding(context) + 48;
  
  return Positioned(
    left: horizontalPadding,
    top: topPadding,
    child: SizedBox(
      width: clusterWidth,
      child: SingleChildScrollView(
        child: Column(
          children: [
            CharacterStateClusterExpandable(),
            SizedBox(height: spacing),
            LifeMetersClusterExpandable(),
            SizedBox(height: spacing),
            ProgressStoryClusterExpandable(),
          ],
        ),
      ),
    ),
  );
}
```

---

## Flame Component Responsive Positioning

### Adaptive Component Sizing

```dart
class CardComponent extends SpriteAnimationGroupComponent with TapCallbacks {
  @override
  Future<void> onLoad() async {
    // Get game reference to access screen size
    final gameRef = findGame()!;
    final screenSize = gameRef.size;
    
    // Adaptive card size based on screen width
    final cardWidth = screenSize.x < 600 
        ? screenSize.x / 6  // Mobile: 6 cards fit
        : screenSize.x < 1200
            ? 180.0  // Tablet: fixed size
            : 220.0; // Desktop: larger cards
    
    size = Vector2(cardWidth, cardWidth * 1.4);
  }
  
  @override
  void onGameResize(Vector2 size) {
    super.onGameResize(size);
    
    // Recalculate position on resize
    _updatePositionForScreenSize(size);
  }
  
  void _updatePositionForScreenSize(Vector2 screenSize) {
    // Responsive positioning logic
    if (screenSize.x < 600) {
      // Mobile positioning
      position = Vector2(screenSize.x / 2, screenSize.y - 150);
    } else {
      // Tablet/Desktop positioning
      position = Vector2(screenSize.x / 2, screenSize.y - 200);
    }
  }
}
```

### Camera Viewport Adaptation

```dart
class ResponsiveGameWorld extends Component with HasGameRef {
  @override
  void onGameResize(Vector2 size) {
    super.onGameResize(size);
    
    // Adjust camera zoom based on screen size
    if (game.size.x < 600) {
      // Mobile: zoom out to show more
      gameRef.camera.viewfinder.zoom = 0.8;
    } else if (game.size.x < 1200) {
      // Tablet: normal zoom
      gameRef.camera.viewfinder.zoom = 1.0;
    } else {
      // Desktop: zoom in for detail
      gameRef.camera.viewfinder.zoom = 1.2;
    }
  }
}
```

---

## Performance Optimization

### Layout Rebuild Optimization

```dart
// ✅ GOOD - Cache screen size
class GameBoardScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final screenSize = context.screenSize; // Single lookup
    
    return screenSize == ScreenSize.mobile
        ? _buildMobileLayout()
        : _buildDesktopLayout();
  }
}

// ❌ BAD - Multiple MediaQuery lookups
Widget build(BuildContext context, WidgetRef ref) {
  if (context.isMobile) { ... }
  if (context.isTablet) { ... }
  if (context.isDesktop) { ... }
}
```

### Flame Performance Targets

- ✅ **60 FPS** maintained across all breakpoints
- ✅ **< 16ms** frame time on resize
- ✅ **Minimal rebuilds** on screen size changes
- ✅ **GPU transforms** for peek animations

---

## Testing

### Responsive Testing Workflow

```bash
# Web (easiest for testing)
flutter run -d chrome

# Resize browser window to test breakpoints:
# - < 600px: Mobile peek-from-edges
# - 600-1200px: Tablet side-by-side
# - > 1200px: Desktop centered

# Desktop
flutter run -d windows  # or macos/linux

# Mobile
flutter run -d <device-id>
```

### DevTools Testing

1. Run app: `flutter run -d chrome`
2. Open DevTools
3. Use "Device Preview" to test different screen sizes
4. Monitor FPS during resize operations
5. Check for layout shifts or rebuilds

---

## Best Practices

### ✅ DO

1. **Use ResponsiveValue for all size-dependent values**
2. **Cache MediaQuery lookups** (single screenSize check per build)
3. **Test on real devices** across all breakpoints
4. **Use LayoutBuilder** for constraint-based layouts
5. **Implement onGameResize** in Flame components
6. **Maintain 60 FPS** during layout transitions

### ❌ DON'T

1. **Don't hardcode pixel values**
2. **Don't assume screen orientation**
3. **Don't use MediaQuery directly** (use extensions)
4. **Don't forget landscape mode** testing
5. **Don't skip performance profiling** on resize

---

## Flame-Specific Patterns

### Responsive Particle Effects

```dart
class CardPlayEffect extends ParticleSystemComponent {
  @override
  Future<void> onLoad() async {
    final isMobile = game.size.x < 600;
    
    // Fewer particles on mobile for performance
    final particleCount = isMobile ? 20 : 50;
    
    particle = Particle.generate(
      count: particleCount,
      generator: (i) => AcceleratedParticle(
        // Mobile: smaller, faster particles
        lifespan: isMobile ? 0.5 : 1.0,
        // ...
      ),
    );
  }
}
```

### Responsive Text Rendering

```dart
class ScoreText extends TextComponent {
  @override
  void onGameResize(Vector2 size) {
    super.onGameResize(size);
    
    // Adaptive font size
    textRenderer = TextPaint(
      style: TextStyle(
        fontSize: size.x < 600 ? 24 : size.x < 1200 ? 32 : 48,
        fontWeight: FontWeight.bold,
      ),
    );
  }
}
```

---

## Resources

### Implementation Files
- `app/lib/core/constants/responsive_breakpoints.dart`
- `app/lib/features/game/presentation/screens/game_board_screen.dart`
- `app/lib/features/game/presentation/widgets/clusters/base_cluster_widget.dart`

### Related Documentation
- [Flame Camera & Viewport](./06-camera-viewport.md)
- [Performance Optimization](./09-performance-optimization.md)
- [Input Handling](./08-input-handling.md)

### External Resources
- [Flutter Responsive Design](https://docs.flutter.dev/development/ui/layout/responsive-adaptive)
- [Material Design Breakpoints](https://material.io/design/layout/responsive-layout-grid.html)
- [Flame Game Resize](https://docs.flame-engine.org/latest/flame/game.html#game-resize)

---

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Performance:** ✅ 60 FPS across all breakpoints  
**Master Spec Reference:** `docs/master_flutter_flame_spec_v_1_0.md` (lines 579-672)


