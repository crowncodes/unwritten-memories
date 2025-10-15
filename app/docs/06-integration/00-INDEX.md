# Integration Documentation Index

## Overview

Integration guides for Firebase, AI inference, and local storage systems.

## Documentation Files

1. **01-firebase-setup.md** - Firebase Auth, Firestore, App Check configuration
2. **02-ai-inference.md** - TensorFlow Lite integration and on-device inference
3. **03-local-storage.md** - Hive database for local persistence

## Quick Reference

### Firebase Initialization

```dart
await Firebase.initializeApp(
  options: DefaultFirebaseOptions.currentPlatform,
);
```

### AI Inference

```dart
final aiService = AIService();
await aiService.initialize();
final response = await aiService.predict(request);
```

### Local Storage

```dart
final box = await Hive.openBox('gameData');
box.put('currentLevel', 5);
```

---

**Related:** [Firebase Setup](../0.firebase/FIREBASE_INTEGRATION_COMPLETE.md), [tflite_flutter.md](../tflite_flutter.md), [hive.md](../hive.md)


