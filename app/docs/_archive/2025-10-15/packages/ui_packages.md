# UI & Animation Packages Reference

This document covers UI and animation packages used in Unwritten.

---

## Flutter Animate - Animation Library

**Current Version**: ^4.5.0  
**Latest Version**: ^4.5.0  
**Recommendation**: ✅ UP TO DATE

### Overview
A performant library for adding beautiful animations to your widgets with minimal code. Supports both declarative and imperative animation styles.

### Installation
```yaml
dependencies:
  flutter_animate: ^4.5.0
```

### Basic Usage

#### Simple Animation
```dart
import 'package:flutter_animate/flutter_animate.dart';

// Fade in
Text('Hello').animate().fadeIn(duration: 300.ms);

// Slide and fade
Container()
  .animate()
  .fadeIn(duration: 500.ms)
  .slideY(begin: 0.2, end: 0);
```

#### Chained Animations
```dart
Widget buildCard() {
  return Card()
    .animate()
    .fadeIn(duration: 300.ms)
    .then(delay: 200.ms) // Wait
    .slideY(begin: -0.1, end: 0, duration: 400.ms)
    .scale(begin: Offset(0.8, 0.8), duration: 400.ms);
}
```

#### Effects

```dart
// Fade
.fadeIn()
.fadeOut()

// Move
.moveX(begin: -100, end: 0)
.moveY(begin: 100, end: 0)
.slideX(begin: 0.5, end: 0) // Relative to size
.slideY(begin: -0.2, end: 0)

// Scale
.scale(begin: Offset(0, 0), end: Offset(1, 1))
.scaleX(begin: 0, end: 1)
.scaleY(begin: 0, end: 1)

// Rotate
.rotate(begin: 0, end: 2 * pi)

// Other
.blur(begin: Offset(0, 0), end: Offset(4, 4))
.tint(color: Colors.blue)
.saturate(begin: 0, end: 1)
.shimmer(duration: 1500.ms)
```

### Unwritten Usage

#### Card Draw Animation
```dart
Widget buildNewCard(CardModel card) {
  return CardWidget(card: card)
    .animate()
    .fadeIn(duration: 300.ms)
    .slideY(begin: 0.3, end: 0, curve: Curves.easeOut)
    .then(delay: 100.ms)
    .scale(
      begin: Offset(0.9, 0.9),
      end: Offset(1.0, 1.0),
      duration: 200.ms,
      curve: Curves.elasticOut,
    );
}
```

#### Evolution Animation
```dart
Widget buildEvolvingCard(CardModel card) {
  return CardWidget(card: card)
    .animate(onComplete: (controller) => onEvolveComplete())
    .scale(begin: Offset(1, 1), end: Offset(1.2, 1.2), duration: 300.ms)
    .then()
    .shimmer(duration: 500.ms, color: Colors.amber)
    .rotate(begin: 0, end: pi, duration: 300.ms)
    .then()
    .scale(begin: Offset(1.2, 1.2), end: Offset(1, 1), duration: 300.ms);
}
```

#### Dialogue Panel
```dart
Widget buildDialoguePanel(String text) {
  return DialoguePanel(text: text)
    .animate()
    .fadeIn(duration: 200.ms)
    .slideY(begin: 0.1, end: 0, duration: 300.ms, curve: Curves.easeOut);
}
```

#### List Animation (Staggered)
```dart
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ListTile(...)
      .animate(delay: (index * 100).ms)
      .fadeIn(duration: 300.ms)
      .slideX(begin: -0.1, end: 0);
  },
)
```

### Custom Effects
```dart
class PulseEffect extends Effect {
  @override
  Widget build(
    BuildContext context,
    Widget child,
    AnimationController controller,
    EffectEntry entry,
  ) {
    return ScaleTransition(
      scale: Tween<double>(
        begin: 1.0,
        end: 1.1,
      ).animate(CurvedAnimation(
        parent: controller,
        curve: Curves.easeInOut,
      )),
      child: child,
    );
  }
}

// Usage
widget.animate().addEffect(PulseEffect());
```

### Adapters (for non-Widgets)
```dart
// Animate values
ValueNotifier<double>(0)
  .animate()
  .tween(begin: 0, end: 100, duration: 1.seconds);
```

### Best Practices
1. Use `.ms` and `.seconds` for readability
2. Chain effects for complex animations
3. Use `delay` and `then()` for sequencing
4. Add curves for natural feel
5. Keep animations under 500ms for responsiveness

### Resources
- **Pub.dev**: https://pub.dev/packages/flutter_animate
- **Documentation**: https://pub.dev/packages/flutter_animate#readme
- **Examples**: https://github.com/gskinner/flutter_animate/tree/main/example
- **Visual Tool**: https://animate.style (inspiration)

---

## Google Fonts - Typography

**Current Version**: ^6.2.1  
**Latest Version**: ^6.2.1  
**Recommendation**: ✅ UP TO DATE

### Overview
Allows you to easily use any of the 1000+ fonts from fonts.google.com in your Flutter apps.

### Installation
```yaml
dependencies:
  google_fonts: ^6.2.1
```

### Basic Usage

#### Single Font
```dart
import 'package:google_fonts/google_fonts.dart';

Text(
  'Unwritten',
  style: GoogleFonts.poppins(
    fontSize: 32,
    fontWeight: FontWeight.bold,
  ),
);
```

#### Theme Integration
```dart
MaterialApp(
  theme: ThemeData(
    textTheme: GoogleFonts.poppinsTextTheme(),
    // Or customize
    textTheme: GoogleFonts.poppinsTextTheme(
      Theme.of(context).textTheme,
    ),
  ),
)
```

### Unwritten Typography

```dart
class UnwrittenTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color(0xFF6366F1),
      ),
      
      // Typography
      textTheme: GoogleFonts.poppinsTextTheme().copyWith(
        // Display (large titles)
        displayLarge: GoogleFonts.poppins(
          fontSize: 57,
          fontWeight: FontWeight.bold,
          letterSpacing: -0.25,
        ),
        
        // Headlines (section titles)
        headlineLarge: GoogleFonts.poppins(
          fontSize: 32,
          fontWeight: FontWeight.w600,
        ),
        headlineMedium: GoogleFonts.poppins(
          fontSize: 28,
          fontWeight: FontWeight.w600,
        ),
        
        // Titles (card titles)
        titleLarge: GoogleFonts.poppins(
          fontSize: 22,
          fontWeight: FontWeight.w600,
        ),
        titleMedium: GoogleFonts.poppins(
          fontSize: 16,
          fontWeight: FontWeight.w500,
          letterSpacing: 0.15,
        ),
        
        // Body (content, descriptions)
        bodyLarge: GoogleFonts.inter(
          fontSize: 16,
          fontWeight: FontWeight.normal,
          letterSpacing: 0.5,
        ),
        bodyMedium: GoogleFonts.inter(
          fontSize: 14,
          fontWeight: FontWeight.normal,
          letterSpacing: 0.25,
        ),
        
        // Labels (buttons, tags)
        labelLarge: GoogleFonts.poppins(
          fontSize: 14,
          fontWeight: FontWeight.w500,
          letterSpacing: 0.1,
        ),
      ),
    );
  }
}
```

### Font Recommendations

| Purpose | Font | Weight | Use Case |
|---------|------|--------|----------|
| Headings | Poppins | 600-700 | Titles, headers |
| Body | Inter | 400 | Content, descriptions |
| UI Elements | Poppins | 500-600 | Buttons, labels |
| Numbers | Roboto Mono | 400 | Stats, scores |
| Dialogue | Merriweather | 400 | NPC dialogue |

### Custom Text Styles
```dart
class TextStyles {
  static TextStyle get cardTitle => GoogleFonts.poppins(
    fontSize: 18,
    fontWeight: FontWeight.w600,
    letterSpacing: 0.15,
  );
  
  static TextStyle get cardDescription => GoogleFonts.inter(
    fontSize: 14,
    fontWeight: FontWeight.normal,
    height: 1.5,
  );
  
  static TextStyle get dialogueText => GoogleFonts.merriweather(
    fontSize: 16,
    fontWeight: FontWeight.normal,
    height: 1.6,
  );
  
  static TextStyle get statsNumber => GoogleFonts.robotoMono(
    fontSize: 24,
    fontWeight: FontWeight.bold,
  );
}
```

### Performance Tips
1. **Preload Fonts**: Load fonts at startup
```dart
Future<void> _loadFonts() async {
  await Future.wait([
    GoogleFonts.pendingFonts([
      GoogleFonts.poppins(),
      GoogleFonts.inter(),
    ]),
  ]);
}
```

2. **Cache Fonts**: Fonts are cached automatically
3. **Fallback**: Provide fallback fonts
```dart
GoogleFonts.poppins(
  fallbackFonts: ['Helvetica', 'Arial'],
);
```

### Resources
- **Pub.dev**: https://pub.dev/packages/google_fonts
- **Browse Fonts**: https://fonts.google.com
- **Font Pairing**: https://fontpair.co

---

## HTTP - Official Dart HTTP Client

**Current Project Version**: ^1.2.1  
**Latest Available Version**: ^1.2.2  
**Recommendation**: ⚠️ MINOR UPDATE AVAILABLE

### Overview
A composable, Future-based library for making HTTP requests. Official Dart package maintained by the Dart team.

### Installation
```yaml
dependencies:
  http: ^1.2.2
```

### Basic Usage

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

// GET request
final response = await http.get(
  Uri.parse('https://api.example.com/data'),
);

if (response.statusCode == 200) {
  final data = jsonDecode(response.body);
  print(data);
}

// POST request
final response = await http.post(
  Uri.parse('https://api.example.com/create'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({'name': 'John', 'age': 30}),
);

// PUT, DELETE, etc.
await http.put(uri, body: body);
await http.delete(uri);
```

### When to Use

**Use `http` for**:
- Simple API calls
- Quick prototypes
- Small projects
- Learning

**Use `dio` for**:
- Complex applications (Unwritten)
- Interceptors needed
- File uploads/downloads
- Retry logic
- Better error handling

### Resources
- **Pub.dev**: https://pub.dev/packages/http
- **API Docs**: https://pub.dev/documentation/http/latest/

---

## Flutter Lints - Code Quality

**Current Project Version**: ^6.0.0  
**Latest Available Version**: ^6.0.0  
**Recommendation**: ✅ UP TO DATE

### Overview
Official Flutter lint rules for better code quality. Recommended by the Flutter team.

### Installation
```yaml
dev_dependencies:
  flutter_lints: ^6.0.0
```

### Configuration (analysis_options.yaml)

```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    # Additional rules for Unwritten
    prefer_const_constructors: true
    prefer_const_literals_to_create_immutables: true
    avoid_print: true
    prefer_final_fields: true
    unnecessary_null_checks: true
    prefer_single_quotes: true
```

### Unwritten Analysis Options

```yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  errors:
    # Treat as errors (fail build)
    missing_required_param: error
    missing_return: error
    invalid_assignment: error
    
  exclude:
    - '**/*.g.dart'
    - '**/*.freezed.dart'
    - 'build/**'

linter:
  rules:
    # Required by Unwritten standards
    prefer_const_constructors: true
    prefer_const_literals_to_create_immutables: true
    prefer_const_declarations: true
    avoid_print: true
    prefer_final_fields: true
    prefer_final_locals: true
    unnecessary_null_checks: true
    prefer_single_quotes: true
    always_use_package_imports: true
    
    # Documentation
    public_member_api_docs: false  # Enable later
    
    # Performance
    avoid_unnecessary_containers: true
    sized_box_for_whitespace: true
```

### Run Linter
```bash
# Analyze code
flutter analyze

# Format code
dart format .

# Fix auto-fixable issues
dart fix --apply
```

### Resources
- **Pub.dev**: https://pub.dev/packages/flutter_lints
- **Lint Rules**: https://dart.dev/tools/linter-rules

---

**Last Updated**: October 14, 2025  
**Packages Covered**: flutter_animate, google_fonts, http, flutter_lints

