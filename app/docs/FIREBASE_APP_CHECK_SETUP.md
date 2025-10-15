# Firebase App Check Setup Guide

Firebase App Check has been integrated into the Unwritten app to protect your backend resources from abuse and unauthorized access.

## What is App Check?

App Check verifies that requests to your Firebase services come from your authentic app, not from unauthorized clients or bots. It works by:

1. Generating attestation tokens from device-specific providers
2. Sending these tokens with each Firebase request
3. Firebase validates tokens before processing requests

## Current Integration Status

✅ **Implemented**: App Check initialization in `FirebaseService`
✅ **Configured**: Default platform-specific providers
⚠️ **Pending**: Firebase Console configuration (see below)

## Platform Providers

### Android
- **Default**: Play Integrity API
- **Fallback**: SafetyNet (for older devices)
- **Development**: Debug tokens (see setup below)

### iOS/macOS
- **Default**: Device Check
- **Development**: Debug tokens (see setup below)

### Web
- **Default**: ReCaptcha v3
- **Requires**: Site key configuration (manual setup required)
- **Status**: ⚠️ Currently disabled until ReCaptcha v3 is configured
- **Note**: Web App Check requires explicit ReCaptcha v3 site key configuration

---

## Setup Instructions

### Step 1: Enable App Check in Firebase Console

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Navigate to **Build > App Check**
4. Click **Get Started** if first time

### Step 2: Register Your Apps

#### For Android App

1. In App Check, click on your Android app
2. Select **Play Integrity** as the provider
3. Click **Save**
4. *(Optional)* Configure SafetyNet as fallback for older devices

#### For iOS App

1. In App Check, click on your iOS app
2. Device Check is automatically enabled
3. No additional configuration needed
4. Click **Save**

#### For Web App (if applicable)

⚠️ **Important**: Web App Check is currently disabled in the code. Follow these steps to enable it:

1. **Register your site with Google reCAPTCHA**
   - Go to [Google reCAPTCHA Admin](https://www.google.com/recaptcha/admin)
   - Click **+** to create a new site
   - Choose **reCAPTCHA v3**
   - Add your domain(s) (e.g., localhost, yourdomain.com)
   - Accept terms and submit
   - **Copy your site key** (you'll need this)

2. **Configure in Firebase Console**
   - In Firebase Console > App Check, click on your Web app
   - Select **reCAPTCHA v3** as provider
   - Paste your site key from step 1
   - Click **Save**

3. **Enable in Code**
   - Open `app/lib/shared/services/firebase_service.dart`
   - Find the `_initializeAppCheck()` method
   - Locate the commented web activation code (around line 516)
   - Replace `'YOUR-RECAPTCHA-V3-SITE-KEY'` with your actual site key
   - Uncomment the code block
   - Save the file

**Example:**
```dart
if (kIsWeb) {
  // Uncomment and update with your actual site key:
  await FirebaseAppCheck.instance.activate(
    webProvider: ReCaptchaV3Provider('6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'),
  );
  return;
}
```

**Security Note**: Consider using environment variables for the site key in production.

### Step 3: Configure Debug Tokens (Development Only)

Debug tokens allow App Check to work during development without real device attestation.

#### Get Your Debug Token

1. Run your app in debug mode:
   ```bash
   cd app
   flutter run
   ```

2. Check the console logs for a message like:
   ```
   [FirebaseAppCheck] Debug token: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
   ```

3. Copy this token

#### Register Debug Token in Firebase

1. Go to Firebase Console > App Check
2. Click **Apps** tab
3. Find your app and click the overflow menu (⋮)
4. Select **Manage debug tokens**
5. Click **Add debug token**
6. Paste your copied token
7. Give it a descriptive name (e.g., "Development - Windows PC")
8. Click **Save**

#### Important Notes

- Debug tokens expire after 30 days
- Each developer needs their own debug token
- **Never** use debug tokens in production builds
- Store tokens securely (don't commit to Git)

### Step 4: Enable Enforcement (Production)

⚠️ **Wait to enable enforcement until you've tested thoroughly!**

Enforcement means Firebase will **reject** requests without valid App Check tokens.

1. In Firebase Console > App Check
2. Select the service you want to protect:
   - Cloud Firestore
   - Firebase Storage
   - Cloud Functions
3. Click **Enforce**
4. Confirm the action

**Recommendation**: Start with **monitoring mode** to see metrics before enforcing.

---

## Testing Your Setup

### 1. Verify App Check is Activated

Run your app and check the logs:

```
ℹ️ INFO: Initializing Firebase App Check...
ℹ️ INFO: Firebase App Check activated successfully
```

If you see this, App Check is working!

### 2. Check Firebase Console Metrics

1. Go to Firebase Console > App Check
2. View the **Metrics** tab
3. You should see:
   - Request counts
   - Valid vs invalid tokens
   - Usage by app/platform

### 3. Test with Enforcement Disabled

Before enabling enforcement:

1. Use your app normally
2. Check that all Firebase operations work:
   - Authentication
   - Firestore reads/writes
   - Storage uploads/downloads
3. Monitor metrics for 24-48 hours

### 4. Test with Enforcement Enabled

After enabling enforcement:

1. Test with your registered debug token
2. Verify all Firebase operations still work
3. Test on multiple devices/platforms
4. Monitor error rates in Firebase Console

---

## Troubleshooting

### App Check Activation Failed

**Symptom**: Log shows "Firebase App Check activation failed"

**Solutions**:
- Ensure Firebase is initialized first (happens automatically in our code)
- Check internet connection
- Verify app is registered in Firebase Console
- Check Firebase Console for App Check registration status

### Requests Rejected (403 Forbidden)

**Symptom**: Firebase requests fail with 403 errors

**Solutions**:
- **Development**: Register debug token in Firebase Console
- **Production**: Ensure app is properly signed and registered
- Check that App Check is activated in your app
- Verify enforcement is not enabled prematurely

### Debug Token Not Working

**Symptom**: Still getting 403 errors with debug token

**Solutions**:
- Verify token is registered correctly in Firebase Console
- Check token hasn't expired (30-day limit)
- Ensure you're using the correct app (Android vs iOS)
- Try generating a new debug token

### Different Token Each Run

**Symptom**: Debug token changes every time you run the app

**Solutions**:
- This is normal for debug mode
- Register multiple tokens OR
- Use release mode with proper provider configuration

---

## Code Reference

### Where App Check is Initialized

**File**: `app/lib/shared/services/firebase_service.dart`

```dart
static Future<bool> initialize() async {
  // ...
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  
  // Initialize Firebase App Check
  await _initializeAppCheck();
  // ...
}
```

### Activation Code

```dart
static Future<void> _initializeAppCheck() async {
  try {
    AppLogger.info('Initializing Firebase App Check...');
    
    // Activate with default platform-specific providers
    await FirebaseAppCheck.instance.activate();
    
    AppLogger.info('Firebase App Check activated successfully');
  } catch (e, stack) {
    AppLogger.error('Firebase App Check activation failed', e, stack);
  }
}
```

---

## Production Checklist

Before releasing to production:

- [ ] App Check registered for all platforms (Android, iOS, Web)
- [ ] Debug tokens removed or disabled
- [ ] Apps properly signed with release keys
- [ ] Release keys registered in Firebase Console
- [ ] Tested on real devices (not emulators)
- [ ] Monitored metrics for 24+ hours
- [ ] Enforcement enabled gradually (one service at a time)
- [ ] Error monitoring set up (Firebase Crashlytics)
- [ ] Rollback plan documented

---

## Additional Resources

- [Firebase App Check Documentation](https://firebase.google.com/docs/app-check)
- [Flutter App Check Plugin](https://pub.dev/packages/firebase_app_check)
- [Play Integrity API](https://developer.android.com/google/play/integrity)
- [Apple Device Check](https://developer.apple.com/documentation/devicecheck)
- [Google reCAPTCHA](https://www.google.com/recaptcha)

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Firebase Console error logs
3. Check app logs with `AppLogger` output
4. Consult [Firebase Support](https://firebase.google.com/support)

---

**Last Updated**: October 2024  
**App Version**: 0.1.0  
**Firebase App Check Version**: 0.4.1+1

