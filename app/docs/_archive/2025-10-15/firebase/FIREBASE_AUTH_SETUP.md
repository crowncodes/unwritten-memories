# Firebase Authentication Setup Guide

Firebase Authentication has been fully integrated into the Unwritten app with comprehensive auth state management, email/password authentication, and Firebase Local Emulator Suite support.

## What's Included

✅ **Authentication Methods**
- Anonymous authentication
- Email/Password sign-in and registration
- Password reset functionality

✅ **Auth State Management**
- Real-time auth state listeners
- ID token change tracking
- User profile change tracking

✅ **Development Tools**
- Firebase Local Emulator Suite integration
- Comprehensive logging
- Error handling with detailed messages

---

## Current Integration Status

✅ **Implemented**: Full Firebase Auth integration in `FirebaseService`
✅ **Available**: Email/Password, Anonymous auth
⚠️ **Pending**: Firebase Console configuration (see below)

---

## Setup Instructions

### Step 1: Enable Authentication in Firebase Console

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Navigate to **Build > Authentication**
4. Click **Get Started** if first time

### Step 2: Enable Sign-In Methods

#### Enable Email/Password Authentication

1. In Authentication, click **Sign-in method** tab
2. Find **Email/Password** in the providers list
3. Click on it to expand
4. Toggle **Enable** switch
5. *(Optional)* Enable **Email link (passwordless sign-in)**
6. Click **Save**

#### Enable Anonymous Authentication

1. In **Sign-in method** tab
2. Find **Anonymous** in the providers list
3. Click on it to expand
4. Toggle **Enable** switch
5. Click **Save**

#### (Optional) Enable Other Providers

You can enable additional providers:
- Google Sign-In
- Apple Sign-In
- Facebook Login
- Twitter
- GitHub
- Microsoft
- Yahoo

**Note**: Each provider requires additional configuration (API keys, OAuth setup, etc.)

### Step 3: Configure Security Rules

#### Firestore Security Rules Example

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

#### Storage Security Rules Example

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

## Using Firebase Authentication in Your App

### 1. Initialize Firebase (Already Done)

Firebase is automatically initialized in `main.dart`:

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

### 2. Listen to Authentication State

The service provides three types of auth state listeners:

#### Auth State Changes (Most Common)

Use this to track when users sign in/out:

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

#### ID Token Changes

Use this when you need to track token changes (e.g., custom claims):

```dart
FirebaseService.idTokenChanges.listen((user) {
  if (user != null) {
    // Token changed - may need to refresh claims
    user.getIdTokenResult().then((token) {
      print('Token claims: ${token.claims}');
    });
  }
});
```

#### User Changes

Use this when you need to track user profile updates:

```dart
FirebaseService.userChanges.listen((user) {
  if (user != null) {
    // User profile changed
    print('Display name: ${user.displayName}');
    print('Email: ${user.email}');
  }
});
```

### 3. Sign Up with Email/Password

```dart
Future<void> signUp(String email, String password) async {
  try {
    final credential = await FirebaseService.createUserWithEmailAndPassword(
      email: email,
      password: password,
    );
    
    if (credential != null) {
      print('User created: ${credential.user?.uid}');
      // Navigate to home screen or show success
    } else {
      // Show error message
      print('Sign up failed');
    }
  } catch (e) {
    print('Error: $e');
  }
}
```

### 4. Sign In with Email/Password

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
    } else {
      // Show error message
      print('Sign in failed');
    }
  } catch (e) {
    print('Error: $e');
  }
}
```

### 5. Sign In Anonymously

```dart
Future<void> signInAnonymously() async {
  final credential = await FirebaseService.signInAnonymously();
  
  if (credential != null) {
    print('Anonymous user: ${credential.user?.uid}');
  }
}
```

### 6. Send Password Reset Email

```dart
Future<void> resetPassword(String email) async {
  final success = await FirebaseService.sendPasswordResetEmail(email);
  
  if (success) {
    // Show success message
    print('Password reset email sent to $email');
  } else {
    // Show error message
    print('Failed to send reset email');
  }
}
```

### 7. Sign Out

```dart
Future<void> signOut() async {
  await FirebaseService.signOut();
  // Navigate to login screen
}
```

### 8. Get Current User

```dart
void checkCurrentUser() {
  final user = FirebaseService.currentUser;
  
  if (user != null) {
    print('Current user: ${user.uid}');
    print('Email: ${user.email}');
    print('Anonymous: ${user.isAnonymous}');
  } else {
    print('No user signed in');
  }
}
```

---

## Using Firebase Local Emulator Suite

The Firebase Local Emulator Suite allows you to test authentication locally without using production Firebase.

### Installation

1. Install Firebase CLI:
   ```bash
   npm install -g firebase-tools
   ```

2. Login to Firebase:
   ```bash
   firebase login
   ```

3. Initialize Firebase in your project root:
   ```bash
   firebase init emulators
   ```

4. Select emulators to install:
   - [x] Authentication Emulator
   - [x] Firestore Emulator
   - [x] Storage Emulator

5. Accept default ports or customize:
   - Auth: 9099
   - Firestore: 8080
   - Storage: 9199

### Starting Emulators

From your project root:

```bash
firebase emulators:start
```

Or start specific emulators:

```bash
firebase emulators:start --only auth,firestore
```

### Connect Your App to Emulators

Update your `main.dart`:

```dart
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Connect to emulators in debug mode
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

### Accessing Emulator UI

Once emulators are running, access the UI at:
- **Main UI**: http://localhost:4000
- **Authentication**: http://localhost:4000/auth
- **Firestore**: http://localhost:4000/firestore
- **Storage**: http://localhost:4000/storage

### Benefits of Using Emulators

✅ Test without affecting production data
✅ No network latency
✅ Free (no Firebase costs)
✅ Full control over test data
✅ Easy to reset and start fresh
✅ Works offline

---

## Error Handling

### Common Firebase Auth Error Codes

When authentication fails, you'll receive `FirebaseAuthException` with these codes:

#### Email/Password Sign In
- `user-not-found`: No user exists with this email
- `wrong-password`: Incorrect password
- `invalid-email`: Email format is invalid
- `user-disabled`: User account has been disabled

#### Registration
- `email-already-in-use`: Email is already registered
- `invalid-email`: Email format is invalid
- `operation-not-allowed`: Email/password auth not enabled
- `weak-password`: Password is too weak (< 6 characters)

#### Password Reset
- `invalid-email`: Email format is invalid
- `user-not-found`: No user exists with this email

### Example Error Handling

```dart
Future<void> handleSignIn(String email, String password) async {
  try {
    final credential = await FirebaseService.signInWithEmailAndPassword(
      email: email,
      password: password,
    );
    
    if (credential == null) {
      // Check logs for specific error
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

## Authentication Best Practices

### Security

1. ✅ **Never store passwords** in plain text or logs
2. ✅ **Use strong password requirements** (min 8 chars, uppercase, numbers, symbols)
3. ✅ **Implement rate limiting** to prevent brute force attacks
4. ✅ **Use email verification** for new accounts
5. ✅ **Enable multi-factor authentication** for sensitive accounts

### User Experience

1. ✅ **Show clear error messages** without exposing security details
2. ✅ **Provide password reset** functionality
3. ✅ **Remember user state** across app restarts
4. ✅ **Show loading indicators** during auth operations
5. ✅ **Validate input** before submitting to Firebase

### Performance

1. ✅ **Cache auth state** using StreamBuilder
2. ✅ **Minimize auth state listeners** to avoid unnecessary rebuilds
3. ✅ **Handle offline scenarios** gracefully
4. ✅ **Use anonymous auth** for guest access

---

## Testing Your Authentication

### Manual Testing Checklist

- [ ] Sign up with valid email/password
- [ ] Sign up with existing email (should fail)
- [ ] Sign up with weak password (should fail)
- [ ] Sign in with correct credentials
- [ ] Sign in with wrong password (should fail)
- [ ] Sign in with non-existent email (should fail)
- [ ] Sign in anonymously
- [ ] Send password reset email
- [ ] Sign out
- [ ] Auth state persists after app restart
- [ ] Verify emulator connection works

### Automated Testing

Create tests in `test/shared/services/firebase_service_test.dart`:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:unwritten/shared/services/firebase_service.dart';

void main() {
  setUpAll(() async {
    // Initialize Firebase with emulators
    await FirebaseService.initialize(
      useEmulator: true,
      emulatorHost: 'localhost',
    );
  });

  group('Firebase Authentication', () {
    test('Anonymous sign in works', () async {
      final credential = await FirebaseService.signInAnonymously();
      expect(credential, isNotNull);
      expect(credential!.user, isNotNull);
      expect(credential.user!.isAnonymous, isTrue);
    });

    test('Email sign up works', () async {
      final credential = await FirebaseService.createUserWithEmailAndPassword(
        email: 'test@example.com',
        password: 'testpass123',
      );
      expect(credential, isNotNull);
      expect(credential!.user?.email, equals('test@example.com'));
    });

    // Add more tests...
  });
}
```

---

## Production Checklist

Before deploying to production:

- [ ] Email/Password authentication enabled in Firebase Console
- [ ] Appropriate sign-in methods configured
- [ ] Firestore security rules configured
- [ ] Storage security rules configured
- [ ] Email templates customized (password reset, verification)
- [ ] Authorized domains configured for OAuth
- [ ] Rate limiting configured
- [ ] User data privacy policies implemented
- [ ] Emulator flags disabled (`useEmulator: false`)
- [ ] Error monitoring set up (Crashlytics)
- [ ] Analytics events configured
- [ ] Multi-factor authentication considered

---

## Additional Resources

- [Firebase Authentication Documentation](https://firebase.google.com/docs/auth)
- [Flutter Firebase Auth Plugin](https://pub.dev/packages/firebase_auth)
- [Firebase Local Emulator Suite](https://firebase.google.com/docs/emulator-suite)
- [Firebase Security Rules](https://firebase.google.com/docs/rules)
- [Firebase Authentication Best Practices](https://firebase.google.com/docs/auth/best-practices)

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Firebase Console error logs
3. Check app logs with `AppLogger` output
4. Test with Firebase emulators
5. Consult [Firebase Support](https://firebase.google.com/support)

---

**Last Updated**: October 2024  
**App Version**: 0.1.0  
**Firebase Auth Version**: 6.1.1

