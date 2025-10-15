# Firebase Quick Start - Unwritten

## 🚀 Quick Setup (Copy & Paste)

### 1. Install CLI Tools (PowerShell as Admin)
```powershell
npm install -g firebase-tools
```

### 2. Install FlutterFire (Regular PowerShell)
```powershell
dart pub global activate flutterfire_cli
```

### 3. Login to Firebase
```powershell
firebase login
```

### 4. Configure Firebase (in app/ directory)
```powershell
cd app
flutterfire configure
```

**Select:**
- Your Firebase project (create one at https://console.firebase.google.com/ first)
- Platforms: android, ios, web, windows (use Space to select, Enter to confirm)

### 5. Get Dependencies
```powershell
flutter pub get
```

### 6. Enable Services in Firebase Console

Go to https://console.firebase.google.com/

**Authentication:**
- Navigate to: Authentication > Sign-in method
- Enable: "Anonymous" provider

**Firestore:**
- Navigate to: Firestore Database
- Create database in "test mode"
- Choose location (e.g., us-central1)

**Storage:**
- Navigate to: Storage
- Get started in "test mode"

### 7. Run the App
```powershell
flutter run -d windows
```

**Success Indicators:**
- App launches without errors
- Console shows: "Firebase initialized successfully"
- Console shows: "Anonymous sign-in successful"
- Firebase Console > Authentication shows 1 anonymous user

---

## ✅ Verification Checklist

- [ ] Firebase project created
- [ ] Firebase CLI installed (`firebase --version`)
- [ ] FlutterFire CLI installed (`flutterfire --version`)
- [ ] Logged into Firebase (`firebase projects:list`)
- [ ] `firebase_options.dart` generated in `app/lib/`
- [ ] Dependencies installed (`flutter pub get`)
- [ ] Anonymous auth enabled in Firebase Console
- [ ] Firestore created in test mode
- [ ] Storage enabled
- [ ] App runs successfully
- [ ] Anonymous user appears in Firebase Console

---

## 🔧 Common Commands

```powershell
# Check Firebase login
firebase projects:list

# Reconfigure Firebase (if needed)
cd app
flutterfire configure

# Update Firebase packages
flutter pub upgrade firebase_core

# Run app with Firebase logs
flutter run -d windows --verbose
```

---

## 📖 Full Guide
See `FIREBASE_SETUP_GUIDE.md` for detailed instructions and troubleshooting.

