# Vibration - Haptic Feedback

**Current Project Version**: ^2.0.0  
**Latest Available Version**: ^2.0.0  
**Recommendation**: ✅ UP TO DATE

---

## Overview

A plugin for handling Vibration API on iOS, Android, and web. Provides haptic feedback for enhanced user experience.

## Key Features

- **Simple API**: Easy to use vibration patterns
- **Duration Control**: Specify vibration length
- **Pattern Support**: Create complex vibration patterns
- **Platform Check**: Check if device supports vibration
- **Amplitude Control**: Android only (intensity)

## Installation

```yaml
dependencies:
  vibration: ^2.0.0
```

### Permissions

#### Android (AndroidManifest.xml)
```xml
<uses-permission android:name="android.permission.VIBRATE"/>
```

#### iOS
No permissions required (automatically included)

## Basic Usage

### Simple Vibration

```dart
import 'package:vibration/vibration.dart';

// Quick vibration (default 500ms)
await Vibration.vibrate();

// Custom duration
await Vibration.vibrate(duration: 100);

// Check if device supports vibration
if (await Vibration.hasVibrator() ?? false) {
  await Vibration.vibrate();
}
```

### Vibration Patterns

```dart
// Pattern: [wait, vibrate, wait, vibrate]
await Vibration.vibrate(
  pattern: [0, 100, 500, 100, 1000, 100], // Milliseconds
);

// Stop pattern
await Vibration.cancel();
```

### Amplitude (Android Only)

```dart
// Check if amplitude control is supported
if (await Vibration.hasAmplitudeControl() ?? false) {
  // Vibrate with specific intensity (1-255)
  await Vibration.vibrate(
    duration: 100,
    amplitude: 128, // Medium intensity
  );
}
```

## Unwritten Haptic Service

```dart
class HapticService {
  static bool _enabled = true;
  static bool _hasVibrator = false;
  static bool _hasAmplitudeControl = false;
  
  /// Initialize and check device capabilities
  static Future<void> initialize() async {
    _hasVibrator = await Vibration.hasVibrator() ?? false;
    _hasAmplitudeControl = await Vibration.hasAmplitudeControl() ?? false;
    
    AppLogger.info('Haptics initialized', data: {
      'has_vibrator': _hasVibrator,
      'has_amplitude': _hasAmplitudeControl,
    });
  }
  
  /// Light haptic (UI interactions)
  /// Duration: 20ms, Amplitude: 50
  static Future<void> light() async {
    if (!_enabled || !_hasVibrator) return;
    
    if (_hasAmplitudeControl) {
      await Vibration.vibrate(duration: 20, amplitude: 50);
    } else {
      await Vibration.vibrate(duration: 20);
    }
  }
  
  /// Medium haptic (card selection, hover)
  /// Duration: 50ms, Amplitude: 100
  static Future<void> medium() async {
    if (!_enabled || !_hasVibrator) return;
    
    if (_hasAmplitudeControl) {
      await Vibration.vibrate(duration: 50, amplitude: 100);
    } else {
      await Vibration.vibrate(duration: 50);
    }
  }
  
  /// Heavy haptic (card play, important actions)
  /// Duration: 100ms, Amplitude: 200
  static Future<void> heavy() async {
    if (!_enabled || !_hasVibrator) return;
    
    if (_hasAmplitudeControl) {
      await Vibration.vibrate(duration: 100, amplitude: 200);
    } else {
      await Vibration.vibrate(duration: 100);
    }
  }
  
  /// Selection haptic (like iOS UISelectionFeedbackGenerator)
  /// Pattern: Short double tap
  static Future<void> selection() async {
    if (!_enabled || !_hasVibrator) return;
    
    await Vibration.vibrate(pattern: [0, 20, 30, 20]);
  }
  
  /// Success pattern (card evolution, achievement)
  /// Pattern: Three quick pulses
  static Future<void> success() async {
    if (!_enabled || !_hasVibrator) return;
    
    await Vibration.vibrate(pattern: [0, 50, 50, 50, 50, 100]);
  }
  
  /// Error pattern (invalid play)
  /// Pattern: Long buzz
  static Future<void> error() async {
    if (!_enabled || !_hasVibrator) return;
    
    if (_hasAmplitudeControl) {
      await Vibration.vibrate(duration: 200, amplitude: 255);
    } else {
      await Vibration.vibrate(duration: 200);
    }
  }
  
  /// Enable/disable haptics
  static void setEnabled(bool enabled) {
    _enabled = enabled;
  }
  
  /// Check if haptics are enabled
  static bool get isEnabled => _enabled && _hasVibrator;
  
  /// Cancel any ongoing vibration
  static Future<void> cancel() async {
    await Vibration.cancel();
  }
}
```

## Usage in Game Components

```dart
// Card hover
@override
void onHoverEnter() {
  HapticService.light();
}

// Card grab
@override
void onDragStart(DragStartEvent event) {
  HapticService.medium();
  // ...
}

// Card play
@override
void onTapUp(TapUpEvent event) {
  HapticService.heavy();
  // ...
}

// Card rejected
void _onInvalidPlay() {
  HapticService.error();
}

// Evolution/upgrade
void _onCardEvolve() {
  HapticService.success();
}
```

## Best Practices

1. **Check Support**: Always check if device has vibrator
2. **User Control**: Provide settings to disable haptics
3. **Don't Overuse**: Use sparingly for meaningful interactions
4. **Battery**: Haptics consume battery, use wisely
5. **Intensity Levels**:
   - Light (UI): 10-30ms
   - Medium (Interactions): 40-60ms
   - Heavy (Actions): 80-120ms

## Haptic Guidelines (Unwritten)

| Action | Haptic Type | Duration | When |
|--------|-------------|----------|------|
| Hover | Light | 20ms | Card hover enter |
| Select | Selection | Pattern | Card selection |
| Drag Start | Medium | 50ms | Begin card drag |
| Drop Valid | Heavy | 100ms | Card accepted |
| Drop Invalid | Error | 200ms | Card rejected |
| Evolution | Success | Pattern | Card evolves |
| Achievement | Success | Pattern | Milestone reached |

## Resources

- **Documentation**: https://pub.dev/packages/vibration
- **GitHub**: https://github.com/benjamindean/flutter_vibration
- **iOS Haptics Guide**: https://developer.apple.com/design/human-interface-guidelines/haptics
- **Android Haptics**: https://developer.android.com/develop/ui/views/haptics

---

**Last Updated**: October 14, 2025  
**Update Priority**: None (already latest)

