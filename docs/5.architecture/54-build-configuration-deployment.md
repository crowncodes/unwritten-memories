# Build Configuration & Deployment

**Last Updated:** October 14, 2025  
**Compliance:** Master Truths v1.2  
**Status:** ✅ Complete

---

## Overview

Complete guide for build flavors, environment configuration, and deployment to Firebase Hosting (frontend) and Cloud Run (backend).

**Pattern:** Multi-environment setup (dev, staging, production)

---

## Build Flavors

### Setup

**android/app/build.gradle:**
```gradle
android {
    flavorDimensions "environment"
    
    productFlavors {
        development {
            dimension "environment"
            applicationIdSuffix ".dev"
            versionNameSuffix "-dev"
        }
        
        staging {
            dimension "environment"
            applicationIdSuffix ".staging"
            versionNameSuffix "-staging"
        }
        
        production {
            dimension "environment"
        }
    }
}
```

**ios/Runner/Info.plist (per flavor):**
```xml
<key>CFBundleIdentifier</key>
<string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
```

### Entry Points

**lib/main_development.dart:**
```dart
import 'main.dart' as app;
import 'core/config/environment.dart';

void main() {
  Environment.init(Flavor.development);
  app.main();
}
```

**lib/main_staging.dart:**
```dart
import 'main.dart' as app;
import 'core/config/environment.dart';

void main() {
  Environment.init(Flavor.staging);
  app.main();
}
```

**lib/main_production.dart:**
```dart
import 'main.dart' as app;
import 'core/config/environment.dart';

void main() {
  Environment.init(Flavor.production);
  app.main();
}
```

### Environment Configuration

**lib/core/config/environment.dart:**
```dart
enum Flavor { development, staging, production }

class Environment {
  static late Flavor _flavor;
  static late String _apiBaseUrl;
  static late String _openaiApiKey;
  static late bool _enableLogging;
  
  static void init(Flavor flavor) {
    _flavor = flavor;
    
    switch (flavor) {
      case Flavor.development:
        _apiBaseUrl = 'http://localhost:8080';
        _openaiApiKey = const String.fromEnvironment('OPENAI_API_KEY');
        _enableLogging = true;
        break;
      case Flavor.staging:
        _apiBaseUrl = 'https://staging-api.unwritten.app';
        _openaiApiKey = const String.fromEnvironment('OPENAI_API_KEY');
        _enableLogging = true;
        break;
      case Flavor.production:
        _apiBaseUrl = 'https://api.unwritten.app';
        _openaiApiKey = const String.fromEnvironment('OPENAI_API_KEY');
        _enableLogging = false;
        break;
    }
  }
  
  static Flavor get flavor => _flavor;
  static String get apiBaseUrl => _apiBaseUrl;
  static String get openaiApiKey => _openaiApiKey;
  static bool get enableLogging => _enableLogging;
}
```

---

## Build Commands

### Development

```bash
# Run
flutter run --flavor development -t lib/main_development.dart

# Build
flutter build apk --flavor development -t lib/main_development.dart
flutter build ios --flavor development -t lib/main_development.dart
flutter build web -t lib/main_development.dart
```

### Staging

```bash
flutter run --flavor staging -t lib/main_staging.dart
flutter build apk --flavor staging -t lib/main_staging.dart --release
flutter build ios --flavor staging -t lib/main_staging.dart --release
flutter build web -t lib/main_staging.dart --release
```

### Production

```bash
flutter build apk --flavor production -t lib/main_production.dart --release
flutter build ios --flavor production -t lib/main_production.dart --release
flutter build web -t lib/main_production.dart --release
```

---

## Firebase Deployment (Frontend)

### Setup

**firebase.json:**
```json
{
  "hosting": [
    {
      "target": "development",
      "public": "build/web",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
      "rewrites": [
        {
          "source": "**",
          "destination": "/index.html"
        }
      ]
    },
    {
      "target": "staging",
      "public": "build/web",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"]
    },
    {
      "target": "production",
      "public": "build/web",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"]
    }
  ]
}
```

**.firebaserc:**
```json
{
  "projects": {
    "default": "unwritten-prod",
    "development": "unwritten-dev",
    "staging": "unwritten-staging"
  },
  "targets": {
    "unwritten-dev": {
      "hosting": {
        "development": ["unwritten-dev"]
      }
    },
    "unwritten-staging": {
      "hosting": {
        "staging": ["unwritten-staging"]
      }
    },
    "unwritten-prod": {
      "hosting": {
        "production": ["unwritten-prod"]
      }
    }
  }
}
```

### Deploy

```bash
# Build web
flutter build web -t lib/main_production.dart --release

# Deploy to Firebase Hosting
firebase use production
firebase deploy --only hosting:production
```

---

## Cloud Run Deployment (Backend)

### Dockerfile

**backend/Dockerfile:**
```dockerfile
# Build stage
FROM dart:stable AS build
WORKDIR /app

# Copy dependencies
COPY pubspec.* ./
RUN dart pub get

# Copy source
COPY . .

# Install Dart Frog CLI
RUN dart pub global activate dart_frog_cli

# Build
RUN dart_frog build

# Runtime stage
FROM debian:bullseye-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy build
COPY --from=build /app/build /app
WORKDIR /app

# Expose port
EXPOSE 8080

# Run
CMD ["/app/bin/server"]
```

### Deploy Script

**scripts/deploy_backend.sh:**
```bash
#!/bin/bash
set -e

ENVIRONMENT=$1
PROJECT_ID=""
SERVICE_NAME="unwritten-api"

case $ENVIRONMENT in
  development)
    PROJECT_ID="unwritten-dev"
    ;;
  staging)
    PROJECT_ID="unwritten-staging"
    ;;
  production)
    PROJECT_ID="unwritten-prod"
    ;;
  *)
    echo "Usage: ./deploy_backend.sh [development|staging|production]"
    exit 1
    ;;
esac

# Build and deploy
cd backend
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --project $PROJECT_ID

echo "Deployed to: https://$SERVICE_NAME-XXXXX-uc.a.run.app"
```

---

## CI/CD Pipeline

### GitHub Actions

**.github/workflows/ci.yml:**
```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.27.0'
      
      - name: Install dependencies
        run: flutter pub get
      
      - name: Analyze
        run: flutter analyze
      
      - name: Format
        run: dart format --output=none --set-exit-if-changed .
      
      - name: Test
        run: flutter test
  
  build-android:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      - run: flutter build apk --release --flavor production -t lib/main_production.dart
      
      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: unwritten-release.apk
          path: build/app/outputs/flutter-apk/app-production-release.apk
  
  deploy-web:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      - run: flutter build web -t lib/main_production.dart --release
      
      - name: Deploy to Firebase
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: '${{ secrets.GITHUB_TOKEN }}'
          firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
          channelId: live
          projectId: unwritten-prod
```

---

## Environment Secrets

### GitHub Secrets

Add to repository settings:
- `FIREBASE_SERVICE_ACCOUNT`
- `OPENAI_API_KEY`
- `GOOGLE_CLOUD_PROJECT_ID`

### Local Development

**Create `.env` files (gitignored):**

```bash
# .env.development
OPENAI_API_KEY=sk-dev-xxx
FIREBASE_PROJECT_ID=unwritten-dev

# .env.staging
OPENAI_API_KEY=sk-staging-xxx
FIREBASE_PROJECT_ID=unwritten-staging

# .env.production
OPENAI_API_KEY=sk-prod-xxx
FIREBASE_PROJECT_ID=unwritten-prod
```

**Load in Dart:**
```dart
import 'package:flutter_dotenv/flutter_dotenv.dart';

await dotenv.load(fileName: '.env.${flavor.name}');
```

---

## Performance Optimization

### Build Size

**Analyze size:**
```bash
flutter build apk --analyze-size
flutter build ios --analyze-size
```

**Tree shaking:**
```bash
# Already enabled in release builds
flutter build apk --release --split-debug-info=./debug-info --obfuscate
```

### Web Optimization

**flutter build web with optimizations:**
```bash
flutter build web \
  --release \
  --web-renderer canvaskit \
  --source-maps \
  --dart-define=FLUTTER_WEB_USE_SKIA=true
```

---

## Related Documentation

- **50-architecture-overview.md** - Architecture decisions
- **52-development-environment-setup.md** - Local setup
- **68-performance-monitoring.md** - Performance tools

---

## Quick Reference

### Build Commands

```bash
# Development
flutter run --flavor development -t lib/main_development.dart

# Staging
flutter build apk --flavor staging -t lib/main_staging.dart --release

# Production
flutter build apk --flavor production -t lib/main_production.dart --release
flutter build ios --flavor production -t lib/main_production.dart --release
flutter build web -t lib/main_production.dart --release
```

### Deploy Commands

```bash
# Frontend (Firebase)
flutter build web -t lib/main_production.dart --release
firebase deploy --only hosting:production

# Backend (Cloud Run)
cd backend
gcloud builds submit --tag gcr.io/unwritten-prod/unwritten-api
gcloud run deploy unwritten-api --image gcr.io/unwritten-prod/unwritten-api
```

---

**Status:** ✅ Build & Deployment Complete  
**Environments:** Dev, Staging, Production  
**CI/CD:** GitHub Actions

