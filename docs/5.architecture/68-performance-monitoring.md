# Performance Monitoring

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete

---

## Performance Overlay

```dart
MaterialApp(
  showPerformanceOverlay: true,
  // ...
)
```

---

## DevTools

```bash
flutter run --profile
flutter pub global activate devtools
flutter pub global run devtools
```

---

## Custom Monitoring

```dart
class PerformanceMonitor {
  static final Stopwatch _frameTimer = Stopwatch();
  static final List<double> _frameTimes = [];
  
  static void startFrame() {
    _frameTimer.start();
  }
  
  static void endFrame() {
    _frameTimer.stop();
    final ms = _frameTimer.elapsedMilliseconds.toDouble();
    _frameTimes.add(ms);
    
    if (ms > 16) {
      AppLogger.performance('Slow frame', Duration(milliseconds: ms.toInt()));
    }
    
    _frameTimer.reset();
  }
  
  static double get averageFPS {
    if (_frameTimes.isEmpty) return 0;
    final avgMs = _frameTimes.reduce((a, b) => a + b) / _frameTimes.length;
    return 1000 / avgMs;
  }
}
```

---

## Battery Monitoring

```dart
import 'package:battery_plus/battery_plus.dart';

class BatteryMonitor {
  static final Battery _battery = Battery();
  
  static Future<int> getBatteryLevel() async {
    return await _battery.batteryLevel;
  }
  
  static Stream<BatteryState> get batteryStateStream {
    return _battery.onBatteryStateChanged;
  }
}
```

---

**Status:** ✅ Performance Monitoring Complete  
**Tools:** DevTools, Custom Monitoring

