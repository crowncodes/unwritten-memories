# Audio & Haptics Integration

**Last Updated:** October 14, 2025  
**Status:** ✅ Complete

---

## Setup

```yaml
dependencies:
  audioplayers: ^6.1.0
  vibration: ^2.0.0
```

---

## Audio Service

```dart
import 'package:audioplayers/audioplayers.dart';

class AudioService {
  static final AudioPlayer _music = AudioPlayer();
  static final AudioPlayer _sfx = AudioPlayer();
  
  static Future<void> playMusic(String track) async {
    await _music.play(AssetSource('audio/music/$track.mp3'));
    await _music.setReleaseMode(ReleaseMode.loop);
  }
  
  static Future<void> playSfx(String sound) async {
    await _sfx.play(AssetSource('audio/sfx/$sound.mp3'));
  }
  
  static Future<void> stopMusic() async {
    await _music.stop();
  }
}
```

---

## Haptic Service

```dart
import 'package:flutter/services.dart';
import 'package:vibration/vibration.dart';

class HapticService {
  static void light() => HapticFeedback.lightImpact();
  static void medium() => HapticFeedback.mediumImpact();
  static void heavy() => HapticFeedback.heavyImpact();
  
  static Future<void> pattern() async {
    if (await Vibration.hasVibrator() ?? false) {
      Vibration.vibrate(pattern: [0, 100, 50, 100]);
    }
  }
}
```

---

## Usage

```dart
// Play sound effect
AudioService.playSfx('card_play');

// Play music
AudioService.playMusic('game_theme');

// Haptic feedback
HapticService.medium();
```

---

**Status:** ✅ Audio & Haptics Complete

