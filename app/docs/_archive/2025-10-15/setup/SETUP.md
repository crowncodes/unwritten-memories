# 🎮 Unwritten Flutter App Setup

> **📐 Architecture Setup:** See [Development Environment Setup](../docs/5.architecture/52-development-environment-setup.md)  
> **🚀 This Guide:** Quick setup to run the Flutter app locally

⏱️ **Setup Time:** 10-15 minutes  
🎯 **Difficulty:** Beginner-friendly

---

## ⚡ Quick Start

```bash
cd app
flutter pub get
flutter run -d chrome
```

That's it! The app will launch with Flame engine by default.

---

## 📋 Prerequisites

### Required Software ✅

| Software | Version | Download |
|----------|---------|----------|
| **Flutter** | 3.27.0+ | https://flutter.dev/docs/get-started/install |
| **Dart** | 3.5.0+ | (Included with Flutter) |
| **Git** | 2.x | https://git-scm.com/ |
| **IDE** | VS Code or Android Studio | https://code.visualstudio.com/ |

### Install Flutter

**Windows:**
```powershell
# Download from flutter.dev and extract to C:\flutter
# Add to PATH
$env:Path += ";C:\flutter\bin"

# Or use chocolatey
choco install flutter
```

**macOS:**
```bash
# Install via Homebrew
brew install flutter

# Or download from flutter.dev
cd ~/development
unzip ~/Downloads/flutter_macos_3.27.0-stable.zip
export PATH="$PATH:`pwd`/flutter/bin"
```

**Linux:**
```bash
cd ~/development
wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.27.0-stable.tar.xz
tar xf flutter_linux_3.27.0-stable.tar.xz
export PATH="$PATH:`pwd`/flutter/bin"
```

### Verify Flutter Installation

```bash
flutter doctor -v
```

**Expected output:**
```
[✓] Flutter (Channel stable, 3.27.0+)
[✓] Dart (3.5.0+)
[✓] Android toolchain
[✓] Chrome
```

**Fix common issues:**
```bash
# Accept Android licenses
flutter doctor --android-licenses

# Install CocoaPods (macOS only, for iOS development)
sudo gem install cocoapods
```

---

## 📦 Installation Steps

### Step 1: Install Dependencies 🔽

```bash
cd app
flutter pub get
```

**Expected output:**
```
Running "flutter pub get" in app...
Resolving dependencies...
+ flame 1.20.0
+ flutter_riverpod 3.0.3
+ audioplayers 6.1.0
[... more packages ...]
Got dependencies!
```

### Step 2: Run Code Generation ⚙️

Some features require code generation:

```bash
# One-time build
flutter pub run build_runner build --delete-conflicting-outputs

# Or watch mode (auto-rebuild on changes)
flutter pub run build_runner watch --delete-conflicting-outputs
```

### Step 3: Verify Setup ✓

```bash
flutter analyze
```

**Expected:** "No issues found!"

---

## 🏃 Running the App

### 🌐 On Chrome (Recommended for development)

```bash
flutter run -d chrome
```

### 🤖 On Android Emulator

```bash
# List available emulators
flutter emulators

# Launch emulator
flutter emulators --launch <emulator_name>

# Run app
flutter run
```

### 🍎 On iOS Simulator (macOS only)

```bash
open -a Simulator
flutter run
```

### 📱 On Physical Device

1. Enable Developer Mode on device
2. Connect via USB
3. Run: `flutter devices` to verify connection
4. Run: `flutter run`

---

## 👀 What You'll See

### 🎬 On First Run

The app will display:
1. "Unwritten - Development" screen
2. Resources bar (Energy, Money, Time)
3. 5 cards in fan layout at bottom
4. Interactive cards (tap, drag, hover)
5. Music toggle in app bar
6. Draw Card and End Turn buttons

### 🎯 Test Interactions

1. **Tap a card** - It scales up and hovers above deck
2. **Tap again** - Card plays with animation
3. **Drag a card** - Smooth 60 FPS dragging
4. **Music toggle** - Click icon in app bar (no audio files yet)
5. **Draw cards** - Click "Draw Card" button
6. **End turn** - Advance game time

---

## 🛠️ Development Features

### 🔄 Toggle Between Versions

Edit `lib/main.dart` line 21:

```dart
const bool useFlameEngine = true;  // Flame engine (60 FPS)
const bool useFlameEngine = false; // Flutter widgets
```

Save and hot reload to compare!

### 🔥 Hot Reload

1. Run the app: `flutter run`
2. Make a change to any Dart file
3. Save file
4. Press `r` in terminal (hot reload)
5. Press `R` in terminal (hot restart - use for Flame changes)

### 📊 Performance Overlay

Monitor FPS during development:

```dart
// lib/main.dart
MaterialApp(
  showPerformanceOverlay: true, // Shows FPS
  // ...
)
```

---

## 💻 IDE Setup

### VS Code (Recommended) 🎯

**Install Extensions:**
- Flutter
- Dart
- Error Lens (helpful for debugging)

**Keyboard Shortcuts:**
- `Ctrl/Cmd + S`: Save and hot reload
- `F5`: Start debugging
- `Shift + F5`: Stop debugging

### Android Studio 🟢

1. Install Flutter and Dart plugins
2. Open `app` folder as a project
3. Select device from dropdown
4. Click green ▶️ play button

---

## 🔧 Troubleshooting

### "Flutter command not found"

**Solution:**
```bash
# Add Flutter to PATH
# macOS/Linux: Add to ~/.bashrc or ~/.zshrc
export PATH="$PATH:/path/to/flutter/bin"

# Windows: Add to PATH environment variable via System Properties
```

Restart terminal and verify with `flutter --version`

### "Android licenses not accepted"

**Solution:**
```bash
flutter doctor --android-licenses
# Press 'y' to accept all licenses
```

### "CocoaPods not installed" (macOS)

**Solution:**
```bash
sudo gem install cocoapods
pod setup
```

### "Pub get failed"

**Solution:**
```bash
flutter clean
flutter pub cache repair
flutter pub get
```

### "No devices found"

**Android:**
```bash
# List available emulators
flutter emulators

# Launch emulator
flutter emulators --launch <emulator_id>
```

**iOS (macOS only):**
```bash
open -a Simulator
```

### "Can't see cards in game"

**Check:**
1. GameWidget has explicit height in layout
2. Cards data loaded from `assets/data/cards.json`
3. No errors in console
4. Try hot restart instead of hot reload

### "No audio playing"

**Expected:** Audio service is initialized but no audio files are included yet. See "Adding Audio Assets" section to add MP3 files.

### "No haptics on device"

**Check:**
1. Using physical device (emulators don't support haptics)
2. Device haptics enabled in system settings
3. Not using web/desktop (haptics only on mobile)

### "Performance issues / Low FPS"

**Solutions:**
```bash
# Run in profile mode for accurate performance measurement
flutter run --profile

# Check DevTools for bottlenecks
flutter pub global activate devtools
flutter pub global run devtools
```

**Check for:**
- Maintain 60 FPS during card interactions
- Frame time < 16ms (shown in performance overlay)
- No memory leaks in DevTools

---

## 🎵 Adding Audio Assets (Optional)

### Create Directories 📁

```bash
# Windows PowerShell
New-Item -ItemType Directory -Force -Path assets/audio/sfx
New-Item -ItemType Directory -Force -Path assets/audio/music

# macOS/Linux
mkdir -p assets/audio/sfx assets/audio/music
```

### Add Audio Files 🔊

Place MP3 files in the directories:

```
assets/audio/sfx/
  ├── card_hover.mp3
  ├── card_grab.mp3
  ├── card_play.mp3
  └── card_shuffle.mp3

assets/audio/music/
  └── game_theme.mp3
```

### Free Audio Sources 🆓

- [Freesound.org](https://freesound.org/) - Free SFX
- [Incompetech.com](https://incompetech.com/) - Free music
- [Mixkit.co](https://mixkit.co/free-sound-effects/game/) - Game SFX

### Update pubspec.yaml

Ensure assets are listed:

```yaml
flutter:
  assets:
    - assets/data/
    - assets/audio/music/
    - assets/audio/sfx/
```

Hot reload and audio will work!

---

## 🧪 Testing

### Run Tests ▶️

```bash
# Unit tests
flutter test

# Integration tests (if available)
flutter test integration_test/
```

### Code Quality ✨

```bash
# Check code quality
flutter analyze

# Format code
dart format .
```

---

## 🎯 Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| **FPS** | 60 (stable) | ✅ |
| **Frame Time** | < 16ms | ✅ |
| **Input Latency** | < 100ms | ✅ |
| **Memory** | < 200MB | ✅ |

Monitor with performance overlay and DevTools.

---

## ✨ What's Included

### 🔥 New Flame Engine Features

- ✅ 60 FPS smooth animations
- ✅ Professional game loop
- ✅ Tap, hover, drag interactions
- ✅ Floating animation on active cards
- ✅ Color-coded cards by type
- ✅ Audio system (ready for assets)
- ✅ Haptic feedback (on physical devices)

### ⚙️ Services Initialized

- **AudioService** - Music and SFX management
- **HapticService** - Tactile feedback
- **AppLogger** - Structured logging
- **Riverpod** - State management

---

## 🚀 Next Steps

### 📅 Today
1. ✅ Verify app runs
2. ✅ Test card interactions
3. ✅ Check performance (60 FPS)

### 📆 This Week
1. Add actual card artwork
2. Add audio files (MP3s)
3. Test on physical device for haptics

### 🔮 Future
1. Sprite atlases for optimization
2. Particle effects
3. Custom shaders

---

## 📚 Quick Reference Commands

```bash
# Development
flutter run -d chrome        # Run on Chrome
flutter run --profile        # Run with profiling
flutter test                 # Run tests
flutter analyze              # Check code quality
dart format .                # Format code

# Debugging
flutter clean                # Clean build artifacts
flutter pub get              # Install dependencies
flutter doctor -v            # Diagnose issues

# Code Generation
flutter pub run build_runner build    # Generate once
flutter pub run build_runner watch    # Auto-generate
```

---

## 📖 Related Documentation

### 📐 Architecture & Planning
- [52-development-environment-setup.md](../docs/5.architecture/52-development-environment-setup.md) - Full environment setup
- [70-implementation-reference.md](../docs/5.architecture/70-implementation-reference.md) - Architecture to implementation mapping

### 💡 Implementation Guides
- [CARD_DRAG_INTERACTION_FEATURE.md](./CARD_DRAG_INTERACTION_FEATURE.md) - Card system details
- [CARD_INTERACTION_GUIDE.md](./CARD_INTERACTION_GUIDE.md) - Quick reference
- [packages/](./packages/) - Package documentation

### 🎴 I/O FLIP Reference
- [ARCHITECTURE.md](./ARCHITECTURE.md) - I/O FLIP architecture analysis

---

## ✅ Success Checklist

Setup is complete when:

- [x] `flutter doctor` shows no blocking issues
- [x] `flutter pub get` completes successfully
- [x] `flutter analyze` reports no errors
- [x] `flutter run -d chrome` launches the app
- [x] App displays game screen with cards
- [x] Cards are interactive (tap, drag, hover)
- [x] Performance overlay shows stable 60 FPS
- [x] Hot reload works (press `r` to reload)

---

**Ready to code!** 🎮

**Last Updated:** October 14, 2025  
**Status:** ✅ Ready for Development

