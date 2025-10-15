# Firebase Setup Guide for Unwritten

## Prerequisites
- Node.js installed (for Firebase CLI)
- Flutter SDK installed
- Google account

## Step-by-Step Setup

### Step 1: Create Firebase Project

1. **Visit Firebase Console**
   ```
   https://console.firebase.google.com/
   ```

2. **Create New Project**
   - Click "Add project" or "Create a project"
   - **Project name:** `unwritten` (or your preferred name)
   - **Google Analytics:** Enable (recommended) or disable
   - Click "Create project"
   - Wait for project creation (~30 seconds)

3. **Note Your Project ID**
   - You'll see it in the Firebase console URL
   - Format: `unwritten-xxxxx` or similar

### Step 2: Install Required CLI Tools

Open PowerShell as Administrator and run:

```powershell
# Install Firebase CLI globally
npm install -g firebase-tools

# Verify installation
firebase --version
```

Then install FlutterFire CLI (no admin needed):

```powershell
# Install FlutterFire CLI
dart pub global activate flutterfire_cli

# Verify installation
flutterfire --version
```

### Step 3: Login to Firebase

```powershell
# Login to Firebase (opens browser)
firebase login

# Verify login
firebase projects:list
```

You should see your `unwritten` project listed.

### Step 4: Navigate to App Directory

```powershell
cd app
```

### Step 5: Configure Firebase for Flutter

```powershell
# Run FlutterFire configuration
flutterfire configure
```

**Interactive Prompts:**

1. **Select a Firebase project:**
   - Use arrow keys to select `unwritten`
   - Press Enter

2. **Which platforms should your configuration support?**
   - Select: `android`, `ios`, `web`, `windows`
   - Use Space to toggle, Enter to confirm

3. **Wait for configuration**
   - FlutterFire will create `firebase_options.dart` automatically
   - This file contains platform-specific Firebase config

**Expected Output:**
```
✔ Firebase configuration file lib/firebase_options.dart generated successfully
```

### Step 6: Install Firebase Packages

```powershell
# Get dependencies
flutter pub get
```

This will install:
- `firebase_core` - Core Firebase SDK
- `firebase_auth` - Authentication
- `cloud_firestore` - Cloud database
- `firebase_storage` - File storage
- `firebase_analytics` - Analytics

### Step 7: Enable Firebase Services in Console

Go back to Firebase Console and enable these services:

#### 7.1 Enable Authentication
1. In Firebase Console, click "Authentication" in left sidebar
2. Click "Get started"
3. Click "Sign-in method" tab
4. Enable "Anonymous" provider (for development)
   - Click "Anonymous"
   - Toggle "Enable"
   - Click "Save"

#### 7.2 Enable Cloud Firestore
1. Click "Firestore Database" in left sidebar
2. Click "Create database"
3. **Security rules:** Start in **test mode** (for development)
   - Production mode requires auth, test mode is open
   - We'll secure it later
4. **Location:** Choose closest to you (e.g., `us-central1`)
5. Click "Enable"

#### 7.3 Enable Firebase Storage
1. Click "Storage" in left sidebar
2. Click "Get started"
3. **Security rules:** Start in **test mode**
4. **Location:** Use same as Firestore
5. Click "Done"

#### 7.4 Enable Firebase Analytics (if enabled in Step 1)
- Should be auto-enabled
- No additional setup needed for development

### Step 8: Verify Setup

Run the app to test Firebase initialization:

```powershell
# Run on Windows
flutter run -d windows

# Or run on Android emulator
flutter run

# Or run on web
flutter run -d chrome
```

**Look for these log messages:**
```
INFO: Unwritten starting...
INFO: Initializing Firebase...
INFO: Firebase initialized successfully
INFO: Anonymous sign-in successful
```

### Step 9: Test Firebase Connection (Optional)

You can verify Firebase is working by checking the Firebase Console:

1. **Authentication:**
   - Go to Authentication > Users
   - You should see 1 anonymous user after running the app

2. **Firestore:**
   - Go to Firestore Database
   - Database should be initialized and ready

## Firestore Security Rules (Production)

⚠️ **IMPORTANT:** Before deploying to production, update Firestore rules.

In Firebase Console > Firestore Database > Rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Game states - only owner can read/write
    match /game_states/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Player profiles
    match /players/{userId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Shared game data (read-only for authenticated users)
    match /cards/{cardId} {
      allow read: if request.auth != null;
      allow write: if false; // Only admins via server
    }
    
    match /npcs/{npcId} {
      allow read: if request.auth != null;
      allow write: if false;
    }
  }
}
```

## Storage Security Rules (Production)

In Firebase Console > Storage > Rules:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // User-specific saves
    match /saves/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Game assets (public read)
    match /assets/{allPaths=**} {
      allow read: if true;
      allow write: if false;
    }
  }
}
```

## Troubleshooting

### Error: "No Firebase App '[DEFAULT]' has been created"
**Solution:** Make sure `firebase_options.dart` exists in `lib/` directory. Re-run `flutterfire configure` if missing.

### Error: "Firebase API key is invalid"
**Solution:** 
1. Check `firebase_options.dart` was generated correctly
2. Verify project ID matches in Firebase Console
3. Re-run `flutterfire configure`

### Error: "PERMISSION_DENIED: Missing or insufficient permissions"
**Solution:** 
1. Check Firestore rules are in "test mode" for development
2. Verify anonymous auth is enabled
3. Check user is signed in (check logs)

### FlutterFire command not found
**Solution:**
```powershell
# Add Dart global bin to PATH
$env:Path += ";$env:USERPROFILE\AppData\Local\Pub\Cache\bin"

# Or add permanently via System Environment Variables
```

### Firebase CLI command not found
**Solution:** Install Node.js first, then re-run `npm install -g firebase-tools`

## Next Steps

Once Firebase is set up:

1. ✅ Test anonymous authentication
2. ✅ Test Firestore read/write
3. ✅ Test Storage upload/download
4. 📝 Implement game state sync
5. 📝 Implement player profiles
6. 📝 Implement cloud saves

## Firebase Usage in Unwritten

### Authentication
```dart
// Already initialized in main.dart
// Access current user:
final user = FirebaseService.currentUser;
final isSignedIn = FirebaseService.isAuthenticated;
```

### Firestore Database
```dart
// Save game state
await FirebaseService.firestore
  .collection('game_states')
  .doc(userId)
  .set(gameStateData);

// Load game state
final doc = await FirebaseService.firestore
  .collection('game_states')
  .doc(userId)
  .get();
```

### Storage
```dart
// Upload save file
final ref = FirebaseService.storage
  .ref()
  .child('saves/$userId/save_1.json');
await ref.putString(jsonData);

// Download save file
final data = await ref.getDownloadURL();
```

### Analytics
```dart
// Log events
await FirebaseService.logEvent('card_played', parameters: {
  'card_id': card.id,
  'card_type': card.type.name,
});
```

## Resources

- [Firebase Console](https://console.firebase.google.com/)
- [FlutterFire Documentation](https://firebase.flutter.dev/)
- [Firebase Security Rules](https://firebase.google.com/docs/rules)
- [Cloud Firestore Guide](https://firebase.google.com/docs/firestore)

---

**Setup Status:**
- ✅ Firebase packages added to `pubspec.yaml`
- ✅ Firebase service wrapper created
- ✅ Firebase initialization in `main.dart`
- ⏳ Waiting for Firebase project configuration

**Last Updated:** October 2025

