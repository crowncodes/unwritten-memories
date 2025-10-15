# Audio & Haptics System

**Status:** 🎵 Implemented  
**Priority:** Medium  
**Flame Integration:** Ready

---

## Overview

Complete audio and haptic feedback system for Unwritten, providing immersive sound effects, background music, and tactile feedback for card interactions and game events.

## Architecture

```dart
AudioSystem
├── Music Manager (audioplayers)
│   ├── Background music loops
│   ├── Dynamic music layers
│   └── Volume control
├── SFX Pool (audioplayers)
│   ├── Card sounds
│   ├── UI feedback
│   └── Event sounds
└── Haptic Service (vibration)
    ├── Light haptics (UI)
    ├── Medium haptics (interactions)
    └── Heavy haptics (actions)
```

---

## Audio System (audioplayers)

**Package:** `audioplayers ^6.1.0`  
**Status:** ✅ UP TO DATE

### Key Features

- Multiple simultaneous audio players
- Local & remote audio support
- Low-latency playback for games
- Volume control per player
- Looping & background playback
- Playback state callbacks

### Basic Usage

#### Music Player

```dart
class MusicManager {
  final AudioPlayer _player = AudioPlayer();
  bool _isPlaying = false;
  
  Future<void> playMusic(String track) async {
    await _player.setReleaseMode(ReleaseMode.loop);
    await _player.setVolume(0.3);
    await _player.play(AssetSource('audio/music/$track.mp3'));
    _isPlaying = true;
  }
  
  Future<void> pause() async {
    await _player.pause();
    _isPlaying = false;
  }
  
  Future<void> resume() async {
    await _player.resume();
    _isPlaying = true;
  }
  
  void dispose() {
    _player.dispose();
  }
}
```

#### Sound Effects

```dart
class SFXPlayer {
  static final AudioPlayer _sfxPlayer = AudioPlayer();
  
  static Future<void> playSfx(String sound) async {
    await _sfxPlayer.play(
      AssetSource('audio/sfx/$sound.mp3'),
      volume: 0.7,
    );
  }
}

// Usage
SFXPlayer.playSfx('card_play');
```

### Unwritten Audio Manager

```dart
class AudioManager {
  static final AudioPlayer _musicPlayer = AudioPlayer();
  static final AudioCache _sfxCache = AudioCache();
  static bool _musicEnabled = true;
  static bool _sfxEnabled = true;
  static double _musicVolume = 0.3;
  static double _sfxVolume = 0.7;
  
  static Future<void> initialize() async {
    // Preload common SFX
    await _sfxCache.loadAll([
      'audio/sfx/card_draw.mp3',
      'audio/sfx/card_play.mp3',
      'audio/sfx/card_hover.mp3',
      'audio/sfx/card_invalid.mp3',
    ]);
    
    // Set music to loop
    await _musicPlayer.setReleaseMode(ReleaseMode.loop);
  }
  
  static Future<void> playMusic(String track) async {
    if (!_musicEnabled) return;
    
    await _musicPlayer.stop();
    await _musicPlayer.setVolume(_musicVolume);
    await _musicPlayer.play(AssetSource('audio/music/$track.mp3'));
  }
  
  static Future<void> playSfx(String sound) async {
    if (!_sfxEnabled) return;
    
    final player = AudioPlayer();
    await player.setVolume(_sfxVolume);
    await player.play(AssetSource('audio/sfx/$sound.mp3'));
    
    // Auto-dispose after playing
    player.onPlayerComplete.listen((_) {
      player.dispose();
    });
  }
  
  static void setMusicVolume(double volume) {
    _musicVolume = volume.clamp(0.0, 1.0);
    _musicPlayer.setVolume(_musicVolume);
  }
  
  static void setSfxVolume(double volume) {
    _sfxVolume = volume.clamp(0.0, 1.0);
  }
  
  static void toggleMusic(bool enabled) {
    _musicEnabled = enabled;
    if (!enabled) {
      _musicPlayer.pause();
    } else {
      _musicPlayer.resume();
    }
  }
  
  static void toggleSfx(bool enabled) {
    _sfxEnabled = enabled;
  }
  
  static void dispose() {
    _musicPlayer.dispose();
  }
}
```

### Best Practices

1. **Audio Pool**: Use multiple players for simultaneous sounds
2. **Preload**: Cache frequently used SFX
3. **Volume Levels**: 
   - Music: 0.2-0.4
   - SFX: 0.5-0.8
4. **Dispose**: Always dispose players when done
5. **Low Latency**: Enable for game audio
   ```dart
   await player.setPlayerMode(PlayerMode.lowLatency);
   ```

### Flame Integration

```dart
import 'package:audioplayers/audioplayers.dart';

class CardComponent extends PositionComponent with TapCallbacks {
  late AudioPlayer _audioPlayer;
  
  @override
  Future<void> onLoad() async {
    _audioPlayer = AudioPlayer();
    await _audioPlayer.setPlayerMode(PlayerMode.lowLatency);
  }
  
  @override
  void onTapDown(TapDownEvent event) {
    _audioPlayer.play(AssetSource('audio/sfx/card_tap.mp3'));
  }
  
  @override
  void onRemove() {
    _audioPlayer.dispose();
    super.onRemove();
  }
}
```

---

## Haptic Feedback System (vibration)

**Package:** `vibration ^2.0.0`  
**Status:** ✅ UP TO DATE

### Key Features

- Simple vibration API
- Duration control
- Vibration patterns
- Platform capability detection
- Amplitude control (Android)

### Permissions

#### Android (AndroidManifest.xml)
```xml
<uses-permission android:name="android.permission.VIBRATE"/>
```

#### iOS
No permissions required (automatic)

### Basic Usage

```dart
import 'package:vibration/vibration.dart';

// Quick vibration (500ms)
await Vibration.vibrate();

// Custom duration
await Vibration.vibrate(duration: 100);

// Check device support
if (await Vibration.hasVibrator() ?? false) {
  await Vibration.vibrate();
}

// Pattern: [wait, vibrate, wait, vibrate]
await Vibration.vibrate(
  pattern: [0, 100, 500, 100, 1000, 100],
);

// Stop pattern
await Vibration.cancel();

// Amplitude (Android only, 1-255)
if (await Vibration.hasAmplitudeControl() ?? false) {
  await Vibration.vibrate(
    duration: 100,
    amplitude: 128, // Medium intensity
  );
}
```

### Unwritten Haptic Service

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
  
  /// Selection haptic (iOS-style)
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

### Flame Integration

```dart
import 'package:vibration/vibration.dart';

class InteractiveCardComponent extends PositionComponent 
    with TapCallbacks, DragCallbacks, HoverCallbacks {
  
  @override
  void onHoverEnter() {
    HapticService.light();
  }
  
  @override
  void onDragStart(DragStartEvent event) {
    HapticService.medium();
  }
  
  @override
  void onTapUp(TapUpEvent event) {
    HapticService.heavy();
    playCard();
  }
  
  void onInvalidPlay() {
    HapticService.error();
  }
  
  void onCardEvolve() {
    HapticService.success();
  }
}
```

---

## Haptic Guidelines

| Action | Haptic Type | Duration | When |
|--------|-------------|----------|------|
| Hover | Light | 20ms | Card hover enter |
| Select | Selection | Pattern | Card selection |
| Drag Start | Medium | 50ms | Begin card drag |
| Drop Valid | Heavy | 100ms | Card accepted |
| Drop Invalid | Error | 200ms | Card rejected |
| Evolution | Success | Pattern | Card evolves |
| Achievement | Success | Pattern | Milestone reached |

### Intensity Guidelines

- **Light (UI)**: 10-30ms, amplitude 30-60
- **Medium (Interactions)**: 40-60ms, amplitude 80-120
- **Heavy (Actions)**: 80-120ms, amplitude 160-255

---

## Audio Asset Organization

```
assets/audio/
├── music/
│   ├── game_theme.mp3
│   ├── menu_theme.mp3
│   └── tension_layer.mp3
└── sfx/
    ├── card_draw.mp3
    ├── card_play.mp3
    ├── card_hover.mp3
    ├── card_shuffle.mp3
    ├── card_invalid.mp3
    ├── ui_click.mp3
    ├── achievement.mp3
    └── evolution.mp3
```

### File Format Recommendations

- **Format**: MP3 or OGG
- **Music Bitrate**: 128-192 kbps
- **SFX Bitrate**: 96-128 kbps
- **Sample Rate**: 44.1 kHz
- **Channels**: Stereo for music, mono for SFX

### Free Audio Resources

- [Freesound.org](https://freesound.org/) - Free SFX
- [Incompetech.com](https://incompetech.com/) - Free music
- [Mixkit.co](https://mixkit.co/free-sound-effects/game/) - Game SFX

---

## Performance Targets

- ✅ **Audio Latency**: < 50ms for SFX
- ✅ **Memory Usage**: < 20MB for cached audio
- ✅ **Battery Impact**: < 2% for audio/haptics combined
- ✅ **Load Time**: < 500ms for preloading common SFX

---

## Best Practices

### Audio

1. **Preload Critical SFX**: Card sounds, UI feedback
2. **Audio Pool**: Reuse players for same sound type
3. **Volume Control**: Let users adjust music/SFX separately
4. **Background Playback**: Handle app lifecycle properly
5. **Memory Management**: Dispose unused players

### Haptics

1. **Check Support**: Always verify device capabilities
2. **User Control**: Provide settings to disable
3. **Don't Overuse**: Reserve for meaningful interactions
4. **Battery Aware**: Reduce haptics on low battery
5. **Platform Differences**: Test on both iOS and Android

---

## Resources

### Audio
- **Package**: https://pub.dev/packages/audioplayers
- **GitHub**: https://github.com/bluefireteam/audioplayers
- **Examples**: https://github.com/bluefireteam/audioplayers/tree/main/packages/audioplayers/example

### Haptics
- **Package**: https://pub.dev/packages/vibration
- **GitHub**: https://github.com/benjamindean/flutter_vibration
- **iOS Guidelines**: https://developer.apple.com/design/human-interface-guidelines/haptics
- **Android Guidelines**: https://developer.android.com/develop/ui/views/haptics

---

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Master Spec Reference:** `docs/master_flutter_flame_spec_v_1_0.md`


