# Development Environment Setup

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete

---

## Overview

Complete setup guide for Unwritten development environment, including Flutter, Flame, Dart Frog backend, and all dependencies.

**Estimated Time:** 30-45 minutes

---

## Prerequisites

### Required Software

| Software | Version | Download |
|----------|---------|----------|
| **Flutter** | 3.27.0+ | https://flutter.dev/docs/get-started/install |
| **Dart** | 3.5.0+ | (Included with Flutter) |
| **Git** | 2.x | https://git-scm.com/ |
| **VS Code** or **Android Studio** | Latest | https://code.visualstudio.com/ or https://developer.android.com/studio |

### Optional But Recommended

| Software | Purpose |
|----------|---------|
| **Firebase CLI** | Backend deployment |
| **Docker** | Backend local testing |
| **Postman** | API testing |
| **Chrome** | Web debugging |

---

## Step 1: Install Flutter

### macOS

```bash
# Install via Homebrew
brew install flutter

# Or download from flutter.dev
cd ~/development
unzip ~/Downloads/flutter_macos_3.27.0-stable.zip
export PATH="$PATH:`pwd`/flutter/bin"
```

### Windows

```powershell
# Download from flutter.dev and extract to C:\flutter
# Add to PATH
$env:Path += ";C:\flutter\bin"

# Or use chocolatey
choco install flutter
```

### Linux

```bash
cd ~/development
wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.27.0-stable.tar.xz
tar xf flutter_linux_3.27.0-stable.tar.xz
export PATH="$PATH:`pwd`/flutter/bin"
```

### Verify Installation

```bash
flutter doctor -v
```

**Expected Output:**
```
[✓] Flutter (Channel stable, 3.27.0, on macOS 14.0, locale en-US)
[✓] Dart (Channel stable, 3.5.0)
[✓] Android toolchain
[✓] Xcode (if on macOS)
[✓] Chrome
[✓] VS Code
```

**Fix Issues:**
```bash
# Accept Android licenses
flutter doctor --android-licenses

# Install missing dependencies
flutter doctor
```

---

## Step 2: IDE Setup

### VS Code (Recommended)

**Install Extensions:**
```json
{
  "recommendations": [
    "dart-code.flutter",
    "dart-code.dart-code",
    "alexisvt.flutter-snippets",
    "pflannery.vscode-versionlens",
    "usernamehw.errorlens",
    "formulahendry.code-runner"
  ]
}
```

**Settings (.vscode/settings.json):**
```json
{
  "dart.flutterSdkPath": "/path/to/flutter",
  "dart.lineLength": 80,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true,
    "source.organizeImports": true
  },
  "[dart]": {
    "editor.rulers": [80],
    "editor.selectionHighlight": false,
    "editor.suggestSelection": "first",
    "editor.tabCompletion": "onlySnippets",
    "editor.wordBasedSuggestions": "off"
  }
}
```

**Keyboard Shortcuts:**
```json
[
  {
    "key": "cmd+shift+r",
    "command": "dart.hotReload"
  },
  {
    "key": "cmd+shift+f5",
    "command": "dart.hotRestart"
  }
]
```

### Android Studio

**Install Plugins:**
- Flutter plugin
- Dart plugin
- Rainbow Brackets
- Key Promoter X

**Configure:**
1. File → Settings → Languages & Frameworks → Flutter
2. Set Flutter SDK path
3. Enable hot reload on save

---

## Step 3: Clone and Setup Project

### Clone Repository

```bash
git clone https://github.com/yourusername/unwritten.git
cd unwritten
```

### Install Dependencies

```bash
# Flutter app dependencies
cd app
flutter pub get

# Backend dependencies
cd ../backend
dart pub get

# Shared packages
cd ../packages/game_logic
dart pub get

cd ../data_models
dart pub get
```

### Code Generation

```bash
# In app/ directory
flutter pub run build_runner build --delete-conflicting-outputs

# Watch mode (auto-rebuild on changes)
flutter pub run build_runner watch --delete-conflicting-outputs
```

---

## Step 4: Configure Environment

### Environment Variables

**Create `.env` files:**

**app/.env.development:**
```env
API_BASE_URL=http://localhost:8080
OPENAI_API_KEY=sk-...
FIREBASE_PROJECT_ID=unwritten-dev
ENABLE_DEBUG_LOGGING=true
```

**app/.env.staging:**
```env
API_BASE_URL=https://staging-api.unwritten.app
OPENAI_API_KEY=sk-...
FIREBASE_PROJECT_ID=unwritten-staging
ENABLE_DEBUG_LOGGING=true
```

**app/.env.production:**
```env
API_BASE_URL=https://api.unwritten.app
OPENAI_API_KEY=sk-...
FIREBASE_PROJECT_ID=unwritten-prod
ENABLE_DEBUG_LOGGING=false
```

### Load Environment Variables

**pubspec.yaml:**
```yaml
dependencies:
  flutter_dotenv: ^5.1.0
```

**Load in app:**
```dart
// lib/main.dart
import 'package:flutter_dotenv/flutter_dotenv.dart';

Future<void> main() async {
  await dotenv.load(fileName: ".env.development");
  runApp(MyApp());
}
```

---

## Step 5: Firebase Setup

### Install Firebase CLI

```bash
npm install -g firebase-tools

# Or via curl
curl -sL https://firebase.tools | bash
```

### Login

```bash
firebase login
```

### Initialize Firebase

```bash
# In app/ directory
firebase init

# Select:
# - Firestore
# - Authentication
# - Storage
# - Hosting
```

### Generate Firebase Options

```bash
# Install FlutterFire CLI
dart pub global activate flutterfire_cli

# Generate configuration
flutterfire configure --project=unwritten-dev
```

**Generates:**
```dart
// lib/core/config/firebase_options.dart
class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    // Platform-specific configuration
  }
}
```

---

## Step 6: Platform-Specific Setup

### Android

**Minimum SDK:**
```gradle
// android/app/build.gradle
android {
    compileSdkVersion 34
    
    defaultConfig {
        minSdkVersion 21
        targetSdkVersion 34
    }
}
```

**Permissions:**
```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<manifest>
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.VIBRATE" />
    <application
        android:label="Unwritten"
        android:icon="@mipmap/ic_launcher">
    </application>
</manifest>
```

### iOS

**Minimum Version:**
```ruby
# ios/Podfile
platform :ios, '13.0'
```

**Info.plist:**
```xml
<!-- ios/Runner/Info.plist -->
<dict>
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <true/>
    </dict>
    <key>UIBackgroundModes</key>
    <array>
        <string>audio</string>
    </array>
</dict>
```

**Install Pods:**
```bash
cd ios
pod install
cd ..
```

### Web

**index.html:**
```html
<!-- web/index.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Unwritten</title>
</head>
<body>
  <script src="main.dart.js" type="application/javascript"></script>
</body>
</html>
```

---

## Step 7: Verify Setup

### Run Tests

```bash
# Unit tests
flutter test

# Integration tests
flutter test integration_test/

# Should see: All tests passed!
```

### Run App

```bash
# List devices
flutter devices

# Run on specific device
flutter run -d chrome
flutter run -d iPhone
flutter run -d emulator-5554

# Run with flavor
flutter run --flavor development -t lib/main_development.dart
```

### Check Performance

```bash
# Run with performance overlay
flutter run --profile --dart-define=ENABLE_PROFILING=true

# Should maintain 60 FPS
```

---

## Step 8: Backend Setup (Dart Frog)

### Install Dart Frog CLI

```bash
dart pub global activate dart_frog_cli
```

### Create Backend

```bash
# Already created, just verify
cd backend
dart pub get

# Run backend locally
dart_frog dev

# Should see: Running on http://localhost:8080
```

### Test Backend

```bash
# Test health endpoint
curl http://localhost:8080/

# Should return: {"status": "ok"}
```

---

## Troubleshooting

### Common Issues

#### "Flutter command not found"

**Solution:**
```bash
# Add Flutter to PATH
export PATH="$PATH:/path/to/flutter/bin"

# Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export PATH="$PATH:/path/to/flutter/bin"' >> ~/.zshrc
```

#### "Android licenses not accepted"

**Solution:**
```bash
flutter doctor --android-licenses
# Press 'y' to accept all
```

#### "CocoaPods not installed" (iOS)

**Solution:**
```bash
sudo gem install cocoapods
cd ios && pod install
```

#### "Build runner fails"

**Solution:**
```bash
# Clean and rebuild
flutter clean
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

#### "Flame hot reload not working"

**Known Issue:** Flame game engine doesn't support hot reload for all changes

**Solution:**
```bash
# Use hot restart instead (cmd+shift+f5)
flutter run --hot
```

#### "Firebase connection failed"

**Solution:**
```bash
# Regenerate Firebase options
flutterfire configure --project=unwritten-dev

# Verify project ID
firebase projects:list
```

---

## Development Workflow

### Daily Workflow

```bash
# 1. Pull latest changes
git pull origin main

# 2. Update dependencies
flutter pub get
dart pub get

# 3. Run code generation (if needed)
flutter pub run build_runner watch

# 4. Run app
flutter run

# 5. Run tests before committing
flutter test
flutter analyze
dart format .

# 6. Commit
git add .
git commit -m "feat(cards): add drag physics"
git push
```

### Hot Reload vs Hot Restart

**Hot Reload (cmd+s):**
- Fast (~1s)
- Preserves state
- Updates most UI changes
- ⚠️ Limited Flame support

**Hot Restart (cmd+shift+f5):**
- Slower (~3s)
- Resets state
- Updates all changes including Flame
- ✅ Use for Flame changes

---

## Performance Monitoring

### Enable DevTools

```bash
# Run app in profile mode
flutter run --profile

# Open DevTools
flutter pub global activate devtools
flutter pub global run devtools
```

### Monitor During Development

**Add performance overlay:**
```dart
// lib/main.dart
MaterialApp(
  showPerformanceOverlay: true, // Shows FPS
  debugShowCheckedModeBanner: false,
  // ...
)
```

**Check frame times:**
- Green bar: Good (< 16ms)
- Yellow bar: Warning (16-33ms)
- Red bar: Bad (> 33ms)

---

## Related Documentation

- **51-project-structure-guide.md** - Project structure
- **53-state-management-architecture.md** - Riverpod setup
- **54-build-configuration-deployment.md** - Build configuration
- **60-package-integration-overview.md** - All packages
- **68-performance-monitoring.md** - Performance tools

---

## Quick Reference

### Essential Commands

```bash
# Setup
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs

# Run
flutter run -d chrome
flutter run --profile

# Test
flutter test
flutter analyze
dart format .

# Clean
flutter clean
flutter pub cache repair

# Backend
dart_frog dev
dart_frog build
```

---

**Status:** ✅ Setup Complete  
**Next:** Build first features  
**Estimated Time:** 30-45 minutes

