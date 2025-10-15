# Setup Firebase RIGHT NOW

## ✅ Step 1: FlutterFire CLI is Installed
You've already completed this step! FlutterFire CLI is installed and ready.

**Note:** The PATH is only set for your current PowerShell session. To make it permanent:
1. Search Windows for "Environment Variables"
2. Click "Edit the system environment variables"
3. Click "Environment Variables" button
4. Under "User variables", find and edit "Path"
5. Add new entry: `C:\Users\TCROW\AppData\Local\Pub\Cache\bin`
6. Click OK on all dialogs
7. Restart PowerShell

## 🔥 Step 2: Create Firebase Project

1. **Go to Firebase Console:**
   ```
   https://console.firebase.google.com/
   ```

2. **Sign in** with your Google account

3. **Click "Add project"** (or "Create a project")

4. **Project name:** `unwritten` (or your choice)

5. **Google Analytics:** 
   - Enable if you want analytics (recommended)
   - Or disable for simpler setup

6. **Click "Create project"**
   - Wait ~30 seconds for completion

## 🔧 Step 3: Login to Firebase CLI

In your PowerShell (in the `unwritten` directory):

```powershell
firebase login
```

This will:
- Open your browser
- Ask you to sign in with Google
- Grant permissions to Firebase CLI

## ⚙️ Step 4: Configure Firebase for Unwritten

**IMPORTANT:** Make sure you're in the `app` directory:

```powershell
# Navigate to app directory if not already there
cd app

# Run FlutterFire configuration
flutterfire configure
```

**Interactive steps:**

1. **Select a Firebase project:**
   - You'll see a list of your Firebase projects
   - Use arrow keys to select `unwritten`
   - Press Enter

2. **Which platforms should your configuration support?**
   - Press Space to select: `android`, `ios`, `web`, `windows`
   - Press Enter when done

3. **Wait for configuration:**
   - FlutterFire will generate `firebase_options.dart`
   - You'll see: `✔ Firebase configuration file lib/firebase_options.dart generated successfully`

## 📦 Step 5: Install Packages

Still in the `app` directory:

```powershell
flutter pub get
```

This downloads all Firebase packages.

## 🔓 Step 6: Enable Firebase Services

Go back to Firebase Console (https://console.firebase.google.com/), select your project, then:

### Enable Authentication
1. Click "**Authentication**" in left sidebar
2. Click "**Get started**"
3. Click "**Sign-in method**" tab
4. Find "**Anonymous**" provider
5. Click on it, toggle "**Enable**", click "**Save**"

### Enable Firestore Database
1. Click "**Firestore Database**" in left sidebar
2. Click "**Create database**"
3. Select "**Start in test mode**" (for development)
4. Choose location (e.g., `us-central1`)
5. Click "**Enable**"

### Enable Firebase Storage (Optional for now)
1. Click "**Storage**" in left sidebar
2. Click "**Get started**"
3. Select "**Start in test mode**"
4. Use same location as Firestore
5. Click "**Done**"

## ✅ Step 7: Test Your Setup

In PowerShell (in `app` directory):

```powershell
flutter run -d windows
```

**Look for these in the console:**
```
ℹ️  INFO: Unwritten starting...
ℹ️  INFO: Initializing Firebase...
ℹ️  INFO: Firebase initialized successfully
ℹ️  INFO: Anonymous sign-in successful
```

**Verify in Firebase Console:**
- Go to Authentication > Users
- You should see 1 anonymous user

## 🎉 Done!

If you see the success messages, Firebase is fully integrated!

---

## 🚨 Troubleshooting

### "flutterfire: command not found" (again)
Run this in your current PowerShell:
```powershell
$env:Path += ";$env:USERPROFILE\AppData\Local\Pub\Cache\bin"
```

### "firebase: command not found"
Install Firebase CLI:
```powershell
npm install -g firebase-tools
```

### "No Firebase projects found"
Make sure you:
1. Created a project in Firebase Console
2. Ran `firebase login`
3. Are signed in with the correct Google account

### App crashes on startup
Check the error message. If it mentions `DefaultFirebaseOptions`:
- Make sure `firebase_options.dart` exists in `app/lib/`
- If not, re-run `flutterfire configure`

### "PERMISSION_DENIED" errors
- Make sure you enabled Authentication > Anonymous in Firebase Console
- Make sure Firestore is in "test mode" (not production mode)

---

## 📞 Need Help?

If you get stuck, share:
1. The exact error message
2. What step you're on
3. Whether `firebase_options.dart` was created


