# Master Positioning & Layout Guide for Unwritten Game

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Status:** Complete

This is the **ONE-STOP REFERENCE** for all positioning, layout, and coordinate system requirements in Unwritten. Use this guide to eliminate confusion between Flutter and Flame coordinate systems, responsive layouts, and component positioning.

---

## **Quick Reference Summary**

### **Key Concepts at a Glance**
- **Dual System:** Flutter widgets (UI overlays) + Flame components (game canvas)
- **Coordinate Systems:** Flutter screen pixels vs Flame world units
- **Responsive:** Mobile (peek-from-edges) → Tablet/Desktop (side-by-side)
- **Fixed Resolution:** Flame uses 1920x1080 logical resolution that scales
- **Card Pivot:** Bottom-center anchor point for natural card manipulation
- **Priority Layers:** Background (-100) → Board (0) → Cards (50) → UI (100)

### **When to Use Which System**
- **Flutter Widgets:** Responsive UI clusters, menus, buttons, overlays
- **Flame Components:** Cards, game board, animations, physics, particles

---

## **1. Coordinate Systems**

### **Flutter Coordinate System (Screen Pixels)**
```dart
// Screen coordinates: (0,0) = top-left of screen
final screenWidth = MediaQuery.of(context).size.width;   // e.g., 393px (iPhone)
final screenHeight = MediaQuery.of(context).size.height; // e.g., 852px (iPhone)

// Flutter widget positioning
Positioned(
  left: 12.0,    // 12px from left edge
  top: 48.0,     // 48px from top edge
  child: widget,
)
```

### **Flame Coordinate System (World Units)**
```dart
// World coordinates with fixed resolution: 1920x1080 logical units
class UnwrittenGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    // Fixed resolution - scales to fit any screen
    camera = CameraComponent.withFixedResolution(
      width: 1920,   // Logical width (design width)
      height: 1080,  // Logical height (design height)
      world: world,
    );
    camera.viewfinder.anchor = Anchor.center;
  }
}

// Flame component positioning
class CardComponent extends PositionComponent {
  @override
  Future<void> onLoad() async {
    position = Vector2(960, 540);  // Center of 1920x1080 world
    size = Vector2(120, 168);      // Card size in world units
    anchor = Anchor.bottomCenter;  // IO FLIP-style pivot point
  }
}
```

### **Coordinate Conversion**
```dart
// Convert screen coordinates to world coordinates
final worldPosition = camera.viewfinder.globalToLocal(screenPosition);

// Convert world coordinates to screen coordinates  
final screenPosition = camera.viewfinder.localToGlobal(worldPosition);

// In practice - drag event example
@override
void onDragUpdate(DragUpdateEvent event) {
  // event.canvasPosition is already in world coordinates
  position = event.canvasPosition;
  
  // If you have screen coordinates, convert them:
  // final worldPos = camera.viewfinder.globalToLocal(screenPos);
}
```

---

## **2. Responsive Breakpoints**

### **Breakpoint System**
```dart
// File: app/lib/core/constants/responsive_breakpoints.dart

enum ScreenSize {
  mobile,    // < 600px
  tablet,    // 600px - 1200px  
  desktop,   // > 1200px
}

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

### **Responsive Values**
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

## **3. Layout Strategies by Screen Size**

### **Mobile (< 600px): Peek-from-Edges**
```dart
// Pattern: UI clusters peek from screen edges
// - Left clusters peek from left (right corners rounded)
// - Right clusters peek from right (left corners rounded)  
// - Tap to expand full cluster content
// - Card hand always visible at bottom
// - Phase selector hidden (more space)

Widget buildMobileLayout(BuildContext context) {
  return Stack(
    children: [
      // Flame game canvas (full screen)
      GameWidget<UnwrittenGame>(game: game),
      
      // Left clusters (peek from left)
      Positioned(
        left: 0,  // Flush with left edge
        top: 48,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            CharacterStateCluster(peekFromLeft: true),
            SizedBox(height: 6),
            LifeMetersCluster(peekFromLeft: true),
            SizedBox(height: 6),
            ProgressStoryCluster(peekFromLeft: true),
          ],
        ),
      ),
      
      // Right clusters (peek from right)  
      Positioned(
        right: 0,  // Flush with right edge
        top: 48,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            ResourcesCluster(peekFromLeft: false),
            SizedBox(height: 6),
            RelationshipsCluster(peekFromLeft: false),
            SizedBox(height: 6),
            TimelineCluster(peekFromLeft: false),
          ],
        ),
      ),
      
      // Card hand at bottom (always visible)
      Positioned(
        left: 0,
        right: 0,
        bottom: 0,
        child: CardHandWidget(),
      ),
    ],
  );
}

// Peek implementation
class BaseClusterWidget extends StatelessWidget {
  final bool peekFromLeft;
  final bool isExpanded;
  final double defaultWidth;
  
  @override
  Widget build(BuildContext context) {
    final isMobile = context.isMobile;
    
    // Calculate peek offset
    final peekAmount = (isMobile && !isExpanded) 
        ? (peekFromLeft ? -defaultWidth - 48 : defaultWidth - 48)
        : 0.0;
    
    // Border radius based on peek direction
    final borderRadius = (isMobile && !isExpanded)
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

### **Tablet (600-1200px): Side-by-Side**
```dart
// Pattern: Left-right cluster columns fully visible
// - Phase selector visible
// - Medium spacing (8px)
// - Flame canvas centered
// - Optimal for horizontal screens

Widget buildTabletLayout(BuildContext context) {
  return Stack(
    children: [
      // Flame game canvas (centered)
      Center(child: GameWidget<UnwrittenGame>(game: game)),
      
      // Left clusters (fully visible)
      Positioned(
        left: 24,   // Horizontal padding
        top: 48,
        child: SizedBox(
          width: 280,  // Fixed cluster width
          child: SingleChildScrollView(
            child: Column(
              children: [
                CharacterStateCluster(),
                SizedBox(height: 8),
                LifeMetersCluster(),
                SizedBox(height: 8),
                ProgressStoryCluster(),
              ],
            ),
          ),
        ),
      ),
      
      // Right clusters (fully visible)
      Positioned(
        right: 24,  // Horizontal padding  
        top: 48,
        child: SizedBox(
          width: 240,  // Fixed cluster width
          child: SingleChildScrollView(
            child: Column(
              children: [
                ResourcesCluster(),
                SizedBox(height: 8),
                RelationshipsCluster(),
                SizedBox(height: 8),
                TimelineCluster(),
              ],
            ),
          ),
        ),
      ),
      
      // Phase selector (visible)
      Positioned(
        top: 20,
        left: 0,
        right: 0,
        child: Center(child: PhaseSelector()),
      ),
      
      // Card hand at bottom
      Positioned(
        left: 0,
        right: 0,
        bottom: 0,
        child: CardHandWidget(),
      ),
    ],
  );
}
```

### **Desktop (> 1200px): Centered with Max Width**
```dart  
// Pattern: Centered layout with max width constraint
// - Maximum content width: 1400px
// - Larger clusters (320px & 280px)
// - Generous spacing (12px)
// - Prevents over-stretching on ultra-wide monitors

Widget buildDesktopLayout(BuildContext context) {
  return Center(
    child: Container(
      constraints: BoxConstraints(maxWidth: 1400),  // Max width constraint
      child: Stack(
        children: [
          // Flame game canvas
          GameWidget<UnwrittenGame>(game: game),
          
          // Left clusters (larger)
          Positioned(
            left: 48,   // Generous padding
            top: 48,
            child: SizedBox(
              width: 320,  // Larger cluster width
              child: SingleChildScrollView(
                child: Column(
                  children: [
                    CharacterStateCluster(),
                    SizedBox(height: 12),  // Generous spacing
                    LifeMetersCluster(),
                    SizedBox(height: 12),
                    ProgressStoryCluster(),
                  ],
                ),
              ),
            ),
          ),
          
          // Right clusters (larger)
          Positioned(
            right: 48,   // Generous padding
            top: 48,
            child: SizedBox(
              width: 280,  // Larger cluster width  
              child: SingleChildScrollView(
                child: Column(
                  children: [
                    ResourcesCluster(),
                    SizedBox(height: 12),
                    RelationshipsCluster(),
                    SizedBox(height: 12),
                    TimelineCluster(),
                  ],
                ),
              ),
            ),
          ),
          
          // Phase selector (visible)
          Positioned(
            top: 32,
            left: 0,
            right: 0,
            child: Center(child: PhaseSelector()),
          ),
          
          // Card hand at bottom
          Positioned(
            left: 0,
            right: 0,
            bottom: 0,
            child: CardHandWidget(),
          ),
        ],
      ),
    ),
  );
}
```

---

## **4. Card Positioning**

### **Card Anchor Points**
```dart
// CRITICAL: Always use Anchor.bottomCenter for cards (IO FLIP pattern)
class CardComponent extends PositionComponent {
  @override
  Future<void> onLoad() async {
    size = Vector2(120, 168);  // Card dimensions
    anchor = Anchor.bottomCenter;  // Bottom-middle pivot point
    
    // Position represents bottom-center of card
    position = Vector2(960, 900);  // Bottom-center at this point
  }
}

// Other anchor points for reference
anchor = Anchor.topLeft;      // (0,0) = top-left corner
anchor = Anchor.center;       // (0,0) = center of component  
anchor = Anchor.bottomCenter; // (0,0) = bottom-center (USE THIS for cards)
```

### **Card Fan Layout (Deck State)**
```dart
// Cards fanned in arc at bottom of screen
void positionCardsInFan(List<CardComponent> cards) {
  final centerIndex = (cards.length - 1) / 2;
  final spacing = 80.0;  // Distance between card centers
  final baseY = 900.0;   // Y position (bottom of cards)
  final centerX = 960.0; // Screen center (1920/2)
  
  for (int i = 0; i < cards.length; i++) {
    final card = cards[i];
    final offsetFromCenter = i - centerIndex;
    
    // Arc formation
    final arcHeight = offsetFromCenter * offsetFromCenter * 0.4;
    final rotationAngle = offsetFromCenter * 0.08; // 8° max
    
    card.position = Vector2(
      centerX + (offsetFromCenter * spacing),
      baseY - arcHeight,
    );
    
    card.angle = rotationAngle;
    card.priority = i; // Cards stack left-to-right
  }
}
```

### **Card Hover State**
```dart
// Card scales to 2.5x and elevates 170px above deck
void setCardHoverState(CardComponent card) {
  card.addCombinedEffect([
    ScaleEffect.to(Vector2.all(2.5), EffectController(duration: 0.3)),
    MoveEffect.by(Vector2(0, -170), EffectController(duration: 0.3)),
  ]);
  
  card.priority = 1000; // Bring to front
  
  // Other cards move aside
  for (final otherCard in nearbyCards) {
    if (otherCard != card) {
      otherCard.addMoveEffect.by(
        Vector2(getMoveAsideOffset(otherCard, card), 0),
        EffectController(duration: 0.3),
      );
    }
  }
}
```

### **Card Drag State (Bottom-Middle Pivot)**
```dart
// Card follows pointer precisely at bottom-middle pivot point
class CardComponent extends PositionComponent with DragCallbacks {
  @override
  void onDragUpdate(DragUpdateEvent event) {
    // event.canvasPosition is in world coordinates
    // Since anchor = Anchor.bottomCenter, this positions bottom-center at pointer
    position = event.canvasPosition;
    
    // Visual representation:
    // ┌─────────────────┐
    // │                 │
    // │   CARD CONTENT  │  
    // │                 │
    // └─────────────────┘
    //          ▲
    //       POINTER
    //    (bottom-middle)
  }
  
  @override
  void onDragStart(DragStartEvent event) {
    // Scale to 2.5x and change shadow color to blue
    addScaleEffect.to(Vector2.all(2.5), EffectController(duration: 0.2));
    priority = 1000; // Bring to front
  }
}
```

### **Responsive Card Sizing**
```dart
class CardComponent extends SpriteAnimationGroupComponent {
  @override
  Future<void> onLoad() async {
    final gameRef = findGame<UnwrittenGame>()!;
    final screenSize = gameRef.size;
    
    // Adaptive card size based on screen width
    final cardWidth = screenSize.x < 600 
        ? screenSize.x / 6        // Mobile: 6 cards fit
        : screenSize.x < 1200 
        ? 180.0                   // Tablet: fixed size
        : 220.0;                  // Desktop: larger cards
    
    size = Vector2(cardWidth, cardWidth * 1.4);  // 1.4 aspect ratio
    anchor = Anchor.bottomCenter;
  }
  
  @override
  void onGameResize(Vector2 size) {
    super.onGameResize(size);
    updatePositionForScreenSize(size);
  }
  
  void updatePositionForScreenSize(Vector2 screenSize) {
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

---

## **5. Component Priority (Z-Index)**

### **Layer System**
```dart
// Rendering order (lower priority = behind, higher priority = in front)
const PRIORITY_BACKGROUND = -100;  // Background, parallax
const PRIORITY_BOARD = 0;          // Game board, zones
const PRIORITY_CARDS = 50;         // Player's card hand
const PRIORITY_UI = 100;           // HUD, buttons, overlays
const PRIORITY_DEBUG = 1000;       // Debug overlay

class GameBoardWorld extends World {
  @override
  Future<void> onLoad() async {
    await addAll([
      BackgroundLayer()..priority = PRIORITY_BACKGROUND,
      GameBoardLayer()..priority = PRIORITY_BOARD,  
      CardHandLayer()..priority = PRIORITY_CARDS,
      UIOverlayLayer()..priority = PRIORITY_UI,
      DebugOverlay()..priority = PRIORITY_DEBUG,
    ]);
  }
}

// Dynamic priority changes
class DraggableCard extends PositionComponent {
  int originalPriority = PRIORITY_CARDS;
  
  void startDrag() {
    originalPriority = priority;
    priority = 1000;  // Bring to front during drag
  }
  
  void endDrag() {
    priority = originalPriority;  // Return to original layer
  }
}
```

---

## **6. Camera & Viewport**

### **Fixed Resolution Setup**
```dart
class UnwrittenGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    // Fixed resolution viewport - scales to fit any screen
    camera = CameraComponent.withFixedResolution(
      width: 1920,   // Design width (logical units)
      height: 1080,  // Design height (logical units)
      world: world,
    );
    
    // Camera anchor determines world origin
    camera.viewfinder.anchor = Anchor.center;  // (960, 540) = world center
    
    await addAll([world, camera]);
  }
}
```

### **Responsive Viewport (Alternative)**
```dart
class ResponsiveGame extends FlameGame {
  @override
  void onGameResize(Vector2 size) {
    super.onGameResize(size);
    
    final aspectRatio = size.x / size.y;
    
    if (aspectRatio < 0.75) {
      // Portrait mobile
      camera.viewport = FixedResolutionViewport(
        resolution: Vector2(1080, 1920),
      );
    } else if (aspectRatio < 1.5) {
      // Tablet  
      camera.viewport = FixedResolutionViewport(
        resolution: Vector2(1440, 1080),
      );
    } else {
      // Desktop/landscape
      camera.viewport = FixedResolutionViewport(
        resolution: Vector2(1920, 1080),
      );
    }
  }
}
```

---

## **7. Layout Utilities**

### **Pre-configured Responsive Values**
```dart
class GameBoardLayout {
  // Cluster widths
  static double getLeftClusterWidth(BuildContext context) {
    return ResponsiveValue<double>(
      mobile: 200,
      tablet: 280, 
      desktop: 320,
    ).getValue(context);
  }
  
  static double getRightClusterWidth(BuildContext context) {
    return ResponsiveValue<double>(
      mobile: 180,
      tablet: 240,
      desktop: 280,
    ).getValue(context);
  }
  
  // Padding & spacing
  static double getHorizontalPadding(BuildContext context) {
    return ResponsiveValue<double>(
      mobile: 12,
      tablet: 24,
      desktop: 48,
    ).getValue(context);
  }
  
  static double getVerticalPadding(BuildContext context) {
    return ResponsiveValue<double>(
      mobile: 12,
      tablet: 20,
      desktop: 32,
    ).getValue(context);
  }
  
  static double getClusterSpacing(BuildContext context) {
    return ResponsiveValue<double>(
      mobile: 6,
      tablet: 8,
      desktop: 12,
    ).getValue(context);
  }
  
  // Layout decisions
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

### **Layout Implementation Template**
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
                maxWidth: GameBoardLayout.getMaxContentWidth(context) ?? double.infinity,
              ),
              child: Stack(
                children: [
                  // Flame game canvas
                  GameWidget<UnwrittenGame>(game: game),
                  
                  // Flutter UI overlays (responsive)
                  if (GameBoardLayout.showPhaseSelector(context))
                    buildPhaseSelector(context),
                  
                  buildResponsiveClusters(context),
                  buildCardHand(context),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
  
  Widget buildResponsiveClusters(BuildContext context) {
    if (GameBoardLayout.useSideBySideLayout(context)) {
      // Tablet/Desktop: Side-by-side
      return Stack(
        children: [
          buildLeftClusters(context),
          buildRightClusters(context),
        ],
      );
    } else {
      // Mobile: Peek from edges
      return Stack(
        children: [
          buildMobileLeftClusters(context),
          buildMobileRightClusters(context),
        ],
      );
    }
  }
}
```

---

## **8. Performance Optimization**

### **Layout Rebuild Optimization**
```dart
// GOOD - Cache screen size
class GameBoardScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final screenSize = context.screenSize;  // Single lookup
    return screenSize == ScreenSize.mobile 
        ? buildMobileLayout() 
        : buildDesktopLayout();
  }
}

// BAD - Multiple MediaQuery lookups  
Widget build(BuildContext context, WidgetRef ref) {
  if (context.isMobile) ...        // MediaQuery lookup #1
  if (context.isTablet) ...        // MediaQuery lookup #2  
  if (context.isDesktop) ...       // MediaQuery lookup #3
}
```

### **Flame Component Optimization**
```dart
class OptimizedCard extends PositionComponent {
  @override
  void onGameResize(Vector2 size) {
    super.onGameResize(size);
    // Throttle expensive recalculations
    if (_lastResizeTime != null && 
        DateTime.now().difference(_lastResizeTime!) < Duration(milliseconds: 100)) {
      return;
    }
    _lastResizeTime = DateTime.now();
    updatePositionForScreenSize(size);
  }
  
  @override
  void update(double dt) {
    // Skip updates when off-screen
    if (!isVisible || opacity == 0) return;
    
    final screenBounds = game.camera.visibleWorldRect;
    if (!screenBounds.containsPoint(absoluteCenter)) return;
    
    super.update(dt);
  }
}
```

---

## **9. Common Mistakes to Avoid**

### **❌ DON'T**
```dart
// Don't hardcode pixel values
position = Vector2(400, 300);  // BAD - doesn't scale

// Don't mix coordinate systems
final screenPos = event.position;  // Flutter screen coordinates
final flameComponent = MyComponent();
flameComponent.position = screenPos;  // BAD - wrong coordinate system

// Don't assume screen orientation  
if (screenWidth > screenHeight) {  // BAD - might be landscape tablet
  // This could be wrong
}

// Don't use MediaQuery directly in Flame components
class CardComponent extends PositionComponent {
  @override
  void onLoad() {
    final size = MediaQuery.of(context).size;  // BAD - no context in Flame
  }
}

// Don't skip onGameResize
class CardComponent extends PositionComponent {
  // Missing onGameResize - card won't reposition on screen size change
}
```

### **✅ DO**
```dart
// Use responsive values
final cardWidth = screenSize.x < 600 ? screenSize.x / 6 : 180.0;

// Convert coordinates properly
final worldPos = camera.viewfinder.globalToLocal(screenPos);

// Use screen size extensions
if (context.isMobile) {
  // Mobile-specific layout
}

// Use HasGameRef for game access in components
class CardComponent extends PositionComponent with HasGameRef<UnwrittenGame> {
  @override
  void onLoad() {
    final gameSize = gameRef.size;  // GOOD - access game size
  }
}

// Always handle resize
@override
void onGameResize(Vector2 size) {
  super.onGameResize(size);
  updatePositionForScreenSize(size);
}
```

---

## **10. Testing & Debugging**

### **Responsive Testing Workflow**
```bash
# Web (easiest for testing)
flutter run -d chrome
# Resize browser window to test breakpoints:
# - < 600px: Mobile (peek-from-edges)
# - 600-1200px: Tablet (side-by-side) 
# - > 1200px: Desktop (centered)

# Desktop
flutter run -d windows  # or macos/linux

# Mobile  
flutter run -d device-id
```

### **Debug Tools**
```dart
class DebugOverlay extends PositionComponent {
  late TextComponent screenSizeText;
  late TextComponent worldSizeText;
  late TextComponent coordinateText;
  
  @override
  Future<void> onLoad() async {
    screenSizeText = TextComponent(
      position: Vector2(10, 10),
      textRenderer: TextPaint(style: TextStyle(color: Colors.green, fontSize: 16)),
    );
    
    worldSizeText = TextComponent(
      position: Vector2(10, 30),
      textRenderer: TextPaint(style: TextStyle(color: Colors.yellow, fontSize: 16)),
    );
    
    coordinateText = TextComponent(
      position: Vector2(10, 50),
      textRenderer: TextPaint(style: TextStyle(color: Colors.white, fontSize: 16)),
    );
    
    addAll([screenSizeText, worldSizeText, coordinateText]);
  }
  
  @override
  void update(double dt) {
    super.update(dt);
    
    final game = findGame<UnwrittenGame>()!;
    screenSizeText.text = 'Screen: ${game.canvasSize}';
    worldSizeText.text = 'World: ${game.size}';
    coordinateText.text = 'Camera: ${game.camera.viewfinder.position}';
  }
}
```

---

## **11. Implementation Files Reference**

### **Core Files**
- `app/lib/core/constants/responsive_breakpoints.dart` - Breakpoint system
- `app/lib/core/constants/game_constants.dart` - Game layout constants  

### **Game Implementation**
- `app/features/game/presentation/components/unwritten_game_world.dart` - Main game class
- `app/features/game/presentation/screens/game_board_screen.dart` - Main game screen

### **Card Implementation** 
- `app/features/game/presentation/widgets/cards/card_hand_fan_widget.dart` - Card rendering
- `app/features/game/presentation/widgets/cards/card_hand_fan_controller.dart` - Card state management

### **Cluster Implementation**
- `app/features/game/presentation/widgets/clusters/base_cluster_widget.dart` - Base cluster with peek functionality

---

## **Quick Decision Tree**

**Need to position something? Ask:**

1. **Is it a UI element (button, menu, text)?** 
   → Use **Flutter widgets** with responsive values

2. **Is it a game element (card, particle, animation)?**
   → Use **Flame components** with world coordinates

3. **Need to convert coordinates?**
   → Use `camera.viewfinder.globalToLocal()` / `localToGlobal()`

4. **Need responsive behavior?**
   → Use `ResponsiveValue<T>` and `context.screenSize`

5. **Positioning a card?**
   → Use `anchor: Anchor.bottomCenter` and position = bottom-center point

6. **Need layering?**
   → Set component `priority` (higher = in front)

This guide eliminates the need to search through multiple documents. Bookmark this page and refer to it for all positioning and layout decisions.