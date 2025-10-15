# Flame Integration

**Last Updated:** October 14, 2025  
**Status:** ✅ Complete

---

## Setup

```yaml
dependencies:
  flame: ^1.20.0
```

```bash
flutter pub get
```

---

## Basic Integration

```dart
import 'package:flame/game.dart';

class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    camera = CameraComponent.withFixedResolution(width: 1920, height: 1080);
    await super.onLoad();
  }
}

// In Flutter widget
class GameScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GameWidget(game: MyGame());
  }
}
```

---

## Related Documentation

- **55-flame-engine-fundamentals.md** - Full Flame guide

---

**Status:** ✅ Flame Integration Complete

