# Firebase Integration

**Status:** ✅ Implemented  
**Priority:** High  
**Services:** Auth, App Check, Firestore (ready), Storage (ready)

---

## Overview

Complete Firebase integration for Unwritten, providing authentication, security, cloud storage, and backend services. Configured for development with local emulators and production deployment.

## Services Implemented

```
Firebase Integration
├── Authentication
│   ├── Email/Password
│   ├── Anonymous Auth
│   └── Password Reset
├── App Check
│   ├── Play Integrity (Android)
│   ├── Device Check (iOS)
│   └── reCAPTCHA v3 (Web)
├── Firestore (Ready)
│   └── NoSQL database
└── Storage (Ready)
    └── File storage
```

---

## Firebase Authentication

### Features

- ✅ Email/Password sign-in and registration
- ✅ Anonymous authentication
- ✅ Password reset via email
- ✅ Real-time auth state management
- ✅ ID token changes tracking
- ✅ User profile changes tracking

### Setup Instructions

#### Step 1: Enable in Firebase Console

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Navigate to **Build > Authentication**
4. Click **Get Started**

#### Step 2: Enable Sign-In Methods

**Email/Password:**
1. Click **Sign-in method** tab
2. Find **Email/Password**
3. Toggle **Enable**
4. Click **Save**

**Anonymous:**
1. In **Sign-in method** tab
2. Find **Anonymous**
3. Toggle **Enable**
4. Click **Save**

### Basic Usage

#### Initialize Firebase

```dart
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase
  final firebaseInitialized = await FirebaseService.initialize();
  
  if (!firebaseInitialized) {
    AppLogger.error('Firebase initialization failed');
  }
  
  runApp(const ProviderScope(child: UnwrittenApp()));
}
```

#### Listen to Auth State

```dart
import 'package:unwritten/shared/services/firebase_service.dart';

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return StreamBuilder<User?>(
      stream: FirebaseService.authStateChanges,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return CircularProgressIndicator();
        }
        
        if (snapshot.hasData) {
          // User is signed in
          return HomeScreen();
        } else {
          // User is signed out
          return LoginScreen();
        }
      },
    );
  }
}
```

#### Sign Up

```dart
Future<void> signUp(String email, String password) async {
  try {
    final credential = await FirebaseService.createUserWithEmailAndPassword(
      email: email,
      password: password,
    );
    
    if (credential != null) {
      print('User created: ${credential.user?.uid}');
      // Navigate to home screen
    }
  } catch (e) {
    print('Error: $e');
  }
}
```

#### Sign In

```dart
Future<void> signIn(String email, String password) async {
  try {
    final credential = await FirebaseService.signInWithEmailAndPassword(
      email: email,
      password: password,
    );
    
    if (credential != null) {
      print('User signed in: ${credential.user?.uid}');
      // Navigate to home screen
    }
  } catch (e) {
    print('Error: $e');
  }
}
```

#### Sign In Anonymously

```dart
Future<void> signInAnonymously() async {
  final credential = await FirebaseService.signInAnonymously();
  
  if (credential != null) {
    print('Anonymous user: ${credential.user?.uid}');
  }
}
```

#### Password Reset

```dart
Future<void> resetPassword(String email) async {
  final success = await FirebaseService.sendPasswordResetEmail(email);
  
  if (success) {
    print('Password reset email sent to $email');
  }
}
```

#### Sign Out

```dart
Future<void> signOut() async {
  await FirebaseService.signOut();
  // Navigate to login screen
}
```

### Auth State Streams

```dart
// Listen to auth state changes (sign in/out)
FirebaseService.authStateChanges.listen((user) {
  if (user != null) {
    print('User signed in: ${user.uid}');
  } else {
    print('User signed out');
  }
});

// Listen to ID token changes (custom claims)
FirebaseService.idTokenChanges.listen((user) {
  if (user != null) {
    // Token changed - may need to refresh claims
  }
});

// Listen to user profile changes
FirebaseService.userChanges.listen((user) {
  if (user != null) {
    // User profile updated
  }
});
```

### Error Handling

```dart
Future<void> handleSignIn(String email, String password) async {
  try {
    final credential = await FirebaseService.signInWithEmailAndPassword(
      email: email,
      password: password,
    );
    
    if (credential == null) {
      showErrorDialog('Sign in failed. Please try again.');
    }
  } on FirebaseAuthException catch (e) {
    String message;
    
    switch (e.code) {
      case 'user-not-found':
        message = 'No account found with this email.';
        break;
      case 'wrong-password':
        message = 'Incorrect password.';
        break;
      case 'invalid-email':
        message = 'Invalid email format.';
        break;
      case 'user-disabled':
        message = 'This account has been disabled.';
        break;
      default:
        message = 'Sign in failed: ${e.message}';
    }
    
    showErrorDialog(message);
  } catch (e) {
    showErrorDialog('An unexpected error occurred.');
  }
}
```

---

## Firebase App Check

### What is App Check?

App Check verifies that requests to Firebase services come from your authentic app, not unauthorized clients or bots. It protects your backend from abuse.

### Platform Providers

| Platform | Provider | Configuration |
|----------|----------|---------------|
| **Android** | Play Integrity | Auto-configured |
| **iOS/macOS** | Device Check | Auto-configured |
| **Web** | reCAPTCHA v3 | Requires site key |

### Setup Instructions

#### Step 1: Enable in Firebase Console

1. Go to Firebase Console > **App Check**
2. Click **Get Started**
3. Register each app platform

#### Step 2: Configure Providers

**Android:**
1. Select **Play Integrity** provider
2. Click **Save**

**iOS:**
1. Device Check is auto-enabled
2. Click **Save**

**Web (Optional):**
1. Get reCAPTCHA v3 site key from [Google reCAPTCHA Admin](https://www.google.com/recaptcha/admin)
2. Choose **reCAPTCHA v3**
3. Add your domains
4. Copy site key
5. In Firebase Console > App Check > Web app
6. Select **reCAPTCHA v3**
7. Paste site key
8. Click **Save**

#### Step 3: Configure in Code

**Web Configuration:**

Update `app/lib/shared/services/firebase_service.dart`:

```dart
if (kIsWeb) {
  const recaptchaSiteKey = String.fromEnvironment(
    'RECAPTCHA_SITE_KEY',
    defaultValue: 'YOUR-SITE-KEY-HERE',
  );
  
  try {
    await FirebaseAppCheck.instance.activate(
      webProvider: ReCaptchaV3Provider(recaptchaSiteKey),
    );
    AppLogger.info('Firebase App Check activated for web');
  } catch (e) {
    AppLogger.error('App Check activation failed on web', e);
  }
}
```

### Development: Debug Tokens

Debug tokens allow App Check to work during development without real attestation.

#### Get Debug Token

1. Run app in debug mode:
   ```bash
   flutter run
   ```

2. Check console for:
   ```
   [FirebaseAppCheck] Debug token: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
   ```

3. Copy token

#### Register in Firebase

1. Firebase Console > App Check > **Apps** tab
2. Find your app, click overflow menu (⋮)
3. Select **Manage debug tokens**
4. Click **Add debug token**
5. Paste token
6. Give it a name (e.g., "Dev - Windows PC")
7. Click **Save**

**Important:**
- Debug tokens expire after 30 days
- Never use debug tokens in production
- Each developer needs their own token

### Enforcement

⚠️ **Start with monitoring mode before enforcing!**

1. Firebase Console > App Check
2. Select service (Firestore, Storage, Functions)
3. Click **Enforce** (or **Monitor** for testing)

**Recommendation:** Monitor for 24-48 hours before enabling enforcement.

---

## Firebase Local Emulator Suite

### Benefits

✅ Test without production data  
✅ No network latency  
✅ Free (no Firebase costs)  
✅ Full control over test data  
✅ Works offline

### Installation

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize emulators
firebase init emulators
```

Select emulators:
- [x] Authentication Emulator (port 9099)
- [x] Firestore Emulator (port 8080)
- [x] Storage Emulator (port 9199)

### Starting Emulators

```bash
# Start all emulators
firebase emulators:start

# Start specific emulators
firebase emulators:start --only auth,firestore
```

### Connect App to Emulators

Update `main.dart`:

```dart
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Use emulators in debug mode
  const bool useEmulator = true; // Set to false for production
  
  await FirebaseService.initialize(
    useEmulator: useEmulator,
    emulatorHost: 'localhost',
    authEmulatorPort: 9099,
    firestoreEmulatorPort: 8080,
    storageEmulatorPort: 9199,
  );
  
  runApp(const ProviderScope(child: UnwrittenApp()));
}
```

### Access Emulator UI

- **Main UI**: http://localhost:4000
- **Authentication**: http://localhost:4000/auth
- **Firestore**: http://localhost:4000/firestore
- **Storage**: http://localhost:4000/storage

---

## Security Rules

### Firestore Example

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow authenticated users to read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Allow authenticated users to read public data
    match /public/{document=**} {
      allow read: if request.auth != null;
      allow write: if false; // Only server can write
    }
  }
}
```

### Storage Example

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Allow authenticated users to upload/download their files
    match /users/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

---

## Troubleshooting

### App Check Activation Failed

**Symptoms:** Log shows "Firebase App Check activation failed"

**Solutions:**
- Ensure Firebase initialized first
- Check internet connection
- Verify app registered in Firebase Console
- Check Firebase Console App Check status

### Requests Rejected (403 Forbidden)

**Symptoms:** Firebase requests fail with 403 errors

**Solutions:**
- **Development:** Register debug token
- **Production:** Verify app properly signed and registered
- Check App Check is activated
- Verify enforcement not enabled prematurely

### Web App Check Errors

**Symptoms:** `RethrownDartError: FirebaseError: AppCheck: ReCAPTCHA error`

**Solutions:**
1. Verify reCAPTCHA v3 site key is correct
2. Check domain is allowed in reCAPTCHA admin
3. Use **site key** (not secret key) in client code
4. Set Firebase Console enforcement to "Monitor" for development

### Anonymous Sign-In Failed

**Symptoms:** `firebase-app-check-token-is-invalid`

**Solutions:**
1. Disable App Check enforcement temporarily
2. Register debug token
3. Verify App Check activation succeeded
4. Check Firebase Console logs

---

## Production Checklist

Before deploying:

- [ ] Authentication methods enabled in Console
- [ ] App Check registered for all platforms
- [ ] Debug tokens removed or disabled
- [ ] Apps signed with release keys
- [ ] Release keys registered in Console
- [ ] Security rules configured
- [ ] Tested on real devices
- [ ] Monitored metrics for 24+ hours
- [ ] Enforcement enabled gradually
- [ ] Error monitoring configured (Crashlytics)
- [ ] Rollback plan documented

---

## API Reference

### FirebaseService Methods

```dart
// Initialize
await FirebaseService.initialize();
await FirebaseService.initialize(useEmulator: true);

// Authentication
final credential = await FirebaseService.createUserWithEmailAndPassword(email: ..., password: ...);
final credential = await FirebaseService.signInWithEmailAndPassword(email: ..., password: ...);
final credential = await FirebaseService.signInAnonymously();
final success = await FirebaseService.sendPasswordResetEmail(email);
await FirebaseService.signOut();
await FirebaseService.reloadUser();

// State
final user = FirebaseService.currentUser;
final isAuth = FirebaseService.isAuthenticated;

// Streams
FirebaseService.authStateChanges.listen(...);
FirebaseService.idTokenChanges.listen(...);
FirebaseService.userChanges.listen(...);
```

---

## Resources

### Official Documentation
- [Firebase Authentication](https://firebase.google.com/docs/auth)
- [Firebase App Check](https://firebase.google.com/docs/app-check)
- [Firebase Emulator Suite](https://firebase.google.com/docs/emulator-suite)
- [Firebase Security Rules](https://firebase.google.com/docs/rules)

### Flutter Packages
- [firebase_auth](https://pub.dev/packages/firebase_auth)
- [firebase_app_check](https://pub.dev/packages/firebase_app_check)
- [firebase_core](https://pub.dev/packages/firebase_core)

### Support
- [Firebase Support](https://firebase.google.com/support)
- [FlutterFire Documentation](https://firebase.flutter.dev/)

---

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Package Versions:** firebase_core ^4.2.0, firebase_auth ^6.1.1, firebase_app_check ^0.4.1+1


