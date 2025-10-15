# Audioplayers - Audio Playback

**Current Project Version**: ^6.1.0  
**Latest Available Version**: ^6.1.0  
**Recommendation**: ✅ UP TO DATE

---

## Overview

A Flutter plugin to play multiple simultaneously audio files, works for Android, iOS, Linux, macOS, Windows, and web.

## Key Features

- **Multiple Players**: Play multiple sounds simultaneously
- **Local & Remote**: Play from assets, files, or URLs
- **Low Latency**: Optimized for game audio
- **Volume Control**: Per-player volume control
- **Playback Control**: Play, pause, stop, seek
- **Looping**: Continuous playback support
- **Notifications**: Playback state callbacks
- **Background**: Continue playing in background (mobile)

## Installation

```yaml
dependencies:
  audioplayers: ^6.1.0
```

## Basic Usage

### Play Sound Effect

```dart
import 'package:audioplayers/audioplayers.dart';

class AudioService {
  static final AudioPlayer _sfxPlayer = AudioPlayer();
  
  static Future<void> playSfx(String sound) async {
    await _sfxPlayer.play(
      AssetSource('audio/sfx/$sound.mp3'),
      volume: 0.5,
    );
  }
}

// Usage
AudioService.playSfx('card_play');
```

### Background Music

```dart
class MusicPlayer {
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
  
  Future<void> stop() async {
    await _player.stop();
    _isPlaying = false;
  }
  
  void dispose() {
    _player.dispose();
  }
}
```

### Listen to State

```dart
_player.onPlayerStateChanged.listen((PlayerState state) {
  switch (state) {
    case PlayerState.playing:
      print('Playing');
      break;
    case PlayerState.paused:
      print('Paused');
      break;
    case PlayerState.stopped:
      print('Stopped');
      break;
    case PlayerState.completed:
      print('Completed');
      break;
  }
});
```

## Unwritten Audio Manager

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

## Best Practices

1. **Audio Pool**: Use multiple players for simultaneous sounds
2. **Preload**: Cache frequently used SFX
3. **Volume Levels**: Music (0.2-0.4), SFX (0.5-0.8)
4. **Dispose**: Always dispose players
5. **Low Latency Mode**: Use for game audio
```dart
await player.setPlayerMode(PlayerMode.lowLatency);
```

## Resources

- **Documentation**: https://pub.dev/packages/audioplayers
- **GitHub**: https://github.com/bluefireteam/audioplayers
- **Examples**: https://github.com/bluefireteam/audioplayers/tree/main/packages/audioplayers/example

---

**Last Updated**: October 14, 2025  
**Update Priority**: None (already latest)

