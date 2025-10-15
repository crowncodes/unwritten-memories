# Migration Guide: Firebase AI Logic → Genkit

**Purpose:** Complete step-by-step migration from Firebase AI to Genkit backend  
**Audience:** Backend engineers, mobile developers, tech leads  
**Status:** ✅ Complete  
**Related:** ← 03-implementation-phases.md | 20-firebase-ai-integration.md | 30-genkit-architecture.md | → 31-genkit-integration-guide.md

---

## What This Document Covers

**Complete migration strategy including:**
- Prerequisites and readiness checklist
- Parallel running (both systems side-by-side)
- Gradual rollout with feature flags
- A/B testing and quality validation
- Monitoring and alerting
- Rollback procedures
- Code changes required
- Timeline and milestones

**Timeline:** Weeks 17-24 (Phase 3 of implementation)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Migration Strategy Overview](#migration-strategy-overview)
3. [Step 1: Parallel Running](#step-1-parallel-running-week-17-18)
4. [Step 2: Gradual Rollout](#step-2-gradual-rollout-week-19-21)
5. [Step 3: Complete Migration](#step-3-complete-migration-week-22-24)
6. [Code Changes Required](#code-changes-required)
7. [Rollback Procedures](#rollback-procedures)
8. [Monitoring & Validation](#monitoring--validation)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Before Starting Migration

**Genkit Backend Must Be:**
- ✅ Deployed to Cloud Run and operational
- ✅ All 5 core flows tested and working (dialogue, evolution, story, relationship, memory)
- ✅ Tools integrated with Firestore
- ✅ RAG system operational
- ✅ Monitoring and logging configured
- ✅ Performance tested (latency < 3 seconds p95)
- ✅ Cost validated ($2-2.50/player/month achievable)

**Firebase AI Implementation Must Be:**
- ✅ Working and stable
- ✅ Serving production traffic
- ✅ Well-understood (know what it does)

**Infrastructure Must Have:**
- ✅ Feature flags configured (Firebase Remote Config)
- ✅ A/B testing framework ready
- ✅ Monitoring dashboards for both systems
- ✅ Alerting rules configured
- ✅ Rollback plan tested

### Readiness Checklist

```markdown
## Technical Readiness
- [ ] Genkit backend deployed and healthy
- [ ] All flows tested with production-like data
- [ ] Performance benchmarks meet targets
- [ ] Cost projections validated
- [ ] Feature flags configured
- [ ] Monitoring dashboards created
- [ ] Alert rules configured
- [ ] Rollback procedure documented

## Team Readiness
- [ ] Backend team trained on Genkit
- [ ] Mobile team understands new client code
- [ ] On-call rotation includes Genkit expertise
- [ ] Incident response plan updated
- [ ] Stakeholders informed of timeline

## Data Readiness
- [ ] Test data prepared (production-like)
- [ ] Quality validation criteria defined
- [ ] Success metrics agreed upon
- [ ] Baseline metrics captured (Firebase AI performance)
```

---

## Migration Strategy Overview

### Three-Phase Approach

```
Week 17-18: PARALLEL RUNNING
├─ Run both Firebase AI and Genkit simultaneously
├─ Compare outputs for quality
├─ Validate Genkit performance
└─ Build confidence in Genkit

Week 19-21: GRADUAL ROLLOUT
├─ 10% of users → Genkit (Week 19)
├─ 50% of users → Genkit (Week 20)
├─ 100% of users → Genkit (Week 21)
└─ Monitor closely, ready to rollback

Week 22-24: COMPLETE MIGRATION
├─ All features use Genkit
├─ Keep Firebase AI as fallback (optional)
├─ Clean up old code (optional)
└─ Celebrate! 🎉
```

### Key Principles

1. **Safety First** - Can rollback at any point
2. **Gradual** - Increase traffic slowly
3. **Monitor Everything** - Watch metrics constantly
4. **Quality Gates** - Must pass before proceeding
5. **Communication** - Keep stakeholders informed

---

## Step 1: Parallel Running (Week 17-18)

### Objective
Run both systems simultaneously to compare outputs and validate Genkit quality.

### Implementation

#### 1.1 Dual AI Service

```dart
// lib/core/services/dual_ai_service.dart
class DualAIService {
  final DevAIService _firebaseAI;      // Firebase AI Logic
  final GenkitAIService _genkitAI;     // Genkit backend
  final RemoteConfig _remoteConfig;
  final AnalyticsService _analytics;
  
  DualAIService({
    required DevAIService firebaseAI,
    required GenkitAIService genkitAI,
    required RemoteConfig remoteConfig,
    required AnalyticsService analytics,
  }) : _firebaseAI = firebaseAI,
       _genkitAI = genkitAI,
       _remoteConfig = remoteConfig,
       _analytics = analytics;
  
  /// Generate dialogue using BOTH systems for comparison
  Future<DialogueResponse> generateDialogueWithComparison({
    required String cardId,
    required String playerId,
    required String context,
  }) async {
    final stopwatch = Stopwatch()..start();
    
    // Run both in parallel
    final results = await Future.wait([
      _generateWithFirebase(cardId, playerId, context),
      _generateWithGenkit(cardId, playerId, context),
    ]);
    
    stopwatch.stop();
    
    final firebaseResult = results[0];
    final genkitResult = results[1];
    
    // Log detailed comparison
    _logComparison(
      firebaseResult: firebaseResult,
      genkitResult: genkitResult,
      totalDuration: stopwatch.elapsed,
    );
    
    // For now, return Firebase result (users don't see Genkit yet)
    // But we're validating Genkit works correctly
    return firebaseResult;
  }
  
  Future<DialogueResponse> _generateWithFirebase(
    String cardId,
    String playerId,
    String context,
  ) async {
    final stopwatch = Stopwatch()..start();
    
    try {
      final result = await _firebaseAI.generateDevDialogue(
        cardId: cardId,
        context: context,
      );
      
      return DialogueResponse(
        text: result,
        source: 'firebase',
        latencyMs: stopwatch.elapsedMilliseconds,
      );
    } catch (e) {
      AppLogger.error('Firebase AI failed during comparison', e);
      rethrow;
    }
  }
  
  Future<DialogueResponse> _generateWithGenkit(
    String cardId,
    String playerId,
    String context,
  ) async {
    final stopwatch = Stopwatch()..start();
    
    try {
      final result = await _genkitAI.generateDialogue(
        cardId: cardId,
        playerId: playerId,
        context: context,
      );
      
      return DialogueResponse(
        text: result.text,
        source: 'genkit',
        latencyMs: stopwatch.elapsedMilliseconds,
        trustDelta: result.trustDelta,
        friendshipDelta: result.friendshipDelta,
      );
    } catch (e) {
      AppLogger.error('Genkit failed during comparison', e);
      
      // Don't fail the request - we're just testing Genkit
      return DialogueResponse(
        text: '[Genkit Error]',
        source: 'genkit_error',
        latencyMs: stopwatch.elapsedMilliseconds,
      );
    }
  }
  
  void _logComparison({
    required DialogueResponse firebaseResult,
    required DialogueResponse genkitResult,
    required Duration totalDuration,
  }) {
    // Log to analytics for comparison dashboard
    _analytics.logEvent(
      name: 'ai_comparison',
      parameters: {
        'firebase_latency_ms': firebaseResult.latencyMs,
        'genkit_latency_ms': genkitResult.latencyMs,
        'firebase_length': firebaseResult.text.length,
        'genkit_length': genkitResult.text.length,
        'genkit_success': genkitResult.source != 'genkit_error',
        'total_duration_ms': totalDuration.inMilliseconds,
        // Quality comparison (manual review needed)
        'comparison_id': _generateComparisonId(),
      },
    );
    
    AppLogger.ai('AI Comparison', metrics: {
      'firebase_ms': firebaseResult.latencyMs,
      'genkit_ms': genkitResult.latencyMs,
      'genkit_success': genkitResult.source != 'genkit_error',
    });
  }
  
  String _generateComparisonId() {
    return 'cmp_${DateTime.now().millisecondsSinceEpoch}';
  }
}
```

#### 1.2 Comparison Dashboard

**Track these metrics:**
- ✅ Success rate (Firebase vs Genkit)
- ✅ Latency (p50, p95, p99)
- ✅ Output length distribution
- ✅ Error rates
- ✅ Quality scores (manual sampling)

**Example Dashboard Query (Firebase Analytics):**
```sql
SELECT
  COUNT(*) as total_comparisons,
  AVG(firebase_latency_ms) as avg_firebase_latency,
  AVG(genkit_latency_ms) as avg_genkit_latency,
  SUM(CASE WHEN genkit_success = true THEN 1 ELSE 0 END) / COUNT(*) as genkit_success_rate
FROM ai_comparison_events
WHERE timestamp > DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
```

#### 1.3 Quality Validation

**Manual quality review process:**

```dart
// Tool for QA team to review and rate outputs
class ComparisonReviewTool {
  Future<void> reviewComparison(String comparisonId) async {
    // Fetch both outputs
    final comparison = await _fetchComparison(comparisonId);
    
    print('=== AI Output Comparison ===');
    print('');
    print('Firebase AI:');
    print(comparison.firebaseOutput);
    print('');
    print('Genkit:');
    print(comparison.genkitOutput);
    print('');
    print('Rate quality (1-5):');
    print('1. Firebase: ');
    print('2. Genkit: ');
    
    // Store ratings for analysis
  }
}
```

**Quality criteria:**
- Natural language flow
- Personality consistency (OCEAN traits)
- Context awareness
- Relationship appropriateness
- No clichés or repetition

**Target:** Genkit quality >= Firebase quality in 90%+ of samples

### Week 17-18 Success Criteria

- [ ] Both systems running in parallel without issues
- [ ] 1000+ comparison samples collected
- [ ] Genkit success rate > 99%
- [ ] Genkit latency p95 < 3 seconds
- [ ] Quality validation: Genkit >= Firebase in 90%+ samples
- [ ] Cost per request matches projections
- [ ] No critical errors in Genkit
- [ ] Team confident to proceed with rollout

**If success criteria not met:** Extend parallel running, fix issues

---

## Step 2: Gradual Rollout (Week 19-21)

### Objective
Gradually shift real user traffic from Firebase AI to Genkit with careful monitoring.

### Implementation

#### 2.1 Feature Flag Configuration

```dart
// lib/core/config/ai_feature_flags.dart
class AIFeatureFlags {
  static const String USE_GENKIT = 'use_genkit_for_dialogue';
  static const String GENKIT_ROLLOUT_PERCENTAGE = 'genkit_rollout_percentage';
  
  final RemoteConfig _remoteConfig;
  
  AIFeatureFlags(this._remoteConfig);
  
  Future<bool> shouldUseGenkit(String userId) async {
    // Check if Genkit enabled globally
    final enabled = await _remoteConfig.getBool(USE_GENKIT);
    if (!enabled) return false;
    
    // Check rollout percentage
    final percentage = await _remoteConfig.getDouble(GENKIT_ROLLOUT_PERCENTAGE);
    
    // Stable hash of user ID to ensure consistent experience
    final userHash = _stableHash(userId);
    final userPercentile = (userHash % 100);
    
    return userPercentile < percentage;
  }
  
  int _stableHash(String input) {
    int hash = 0;
    for (int i = 0; i < input.length; i++) {
      hash = ((hash << 5) - hash) + input.codeUnitAt(i);
      hash = hash & hash; // Convert to 32-bit integer
    }
    return hash.abs();
  }
}
```

#### 2.2 Routing Service

```dart
// lib/core/services/ai_service_router.dart
class AIServiceRouter {
  final DevAIService _firebaseAI;
  final GenkitAIService _genkitAI;
  final AIFeatureFlags _featureFlags;
  final AnalyticsService _analytics;
  
  Future<DialogueResponse> generateDialogue({
    required String cardId,
    required String playerId,
    required String context,
  }) async {
    // Check which service to use
    final useGenkit = await _featureFlags.shouldUseGenkit(playerId);
    
    _analytics.logEvent(
      name: 'ai_request',
      parameters: {
        'service': useGenkit ? 'genkit' : 'firebase',
        'card_id': cardId,
      },
    );
    
    if (useGenkit) {
      return await _generateWithGenkit(cardId, playerId, context);
    } else {
      return await _generateWithFirebase(cardId, context);
    }
  }
  
  Future<DialogueResponse> _generateWithGenkit(
    String cardId,
    String playerId,
    String context,
  ) async {
    try {
      return await _genkitAI.generateDialogue(
        cardId: cardId,
        playerId: playerId,
        context: context,
      );
    } catch (e, stack) {
      AppLogger.error('Genkit failed, falling back to Firebase', e, stack);
      
      // CRITICAL: Fallback to Firebase AI on Genkit failure
      return await _generateWithFirebase(cardId, context);
    }
  }
  
  Future<DialogueResponse> _generateWithFirebase(
    String cardId,
    String context,
  ) async {
    final result = await _firebaseAI.generateDevDialogue(
      cardId: cardId,
      context: context,
    );
    
    return DialogueResponse(
      text: result,
      source: 'firebase',
    );
  }
}
```

#### 2.3 Rollout Schedule

**Week 19: 10% Rollout**

```javascript
// Firebase Remote Config
{
  "use_genkit_for_dialogue": true,
  "genkit_rollout_percentage": 10.0
}
```

**Monitor for 48 hours:**
- Error rate < 1%
- Latency p95 < 3 seconds
- No increase in user complaints
- Cost within budget

**If successful → proceed to 50%**

**Week 20: 50% Rollout**

```javascript
{
  "use_genkit_for_dialogue": true,
  "genkit_rollout_percentage": 50.0
}
```

**Monitor for 48 hours:**
- Same criteria as 10%
- Validate at higher scale

**If successful → proceed to 100%**

**Week 21: 100% Rollout**

```javascript
{
  "use_genkit_for_dialogue": true,
  "genkit_rollout_percentage": 100.0
}
```

**Monitor for 7 days before declaring complete**

### 2.4 Monitoring During Rollout

**Real-Time Dashboard:**
```markdown
## Genkit Rollout Dashboard

Current Rollout: 50%

### Success Metrics
- Success Rate: 99.8% ✅
- Latency p95: 2.8s ✅
- Error Rate: 0.2% ✅
- Cost/Request: $0.00085 ✅

### Alerts
- ⚠️ None

### User Feedback
- Positive: 45
- Neutral: 3
- Negative: 2 (both unrelated to AI)
```

**Alert Rules:**
- Error rate > 2%: **WARNING**
- Error rate > 5%: **CRITICAL - Auto rollback**
- Latency p95 > 5s: **WARNING**
- Latency p95 > 10s: **CRITICAL - Auto rollback**
- Cost > $0.01/request: **WARNING**

### Week 19-21 Success Criteria

**Per Week:**
- [ ] Error rate < 1%
- [ ] Latency p95 < 3 seconds
- [ ] No increase in negative user feedback
- [ ] Cost per player within budget ($2-2.50/month)
- [ ] Fallback system working (Firebase AI catches failures)
- [ ] No critical incidents

**Rollback Triggers:**
- Error rate > 5% sustained for 30+ minutes
- Latency p95 > 10 seconds sustained
- Critical incident caused by Genkit
- User feedback significantly negative

---

## Step 3: Complete Migration (Week 22-24)

### Objective
Finalize migration with all features on Genkit, optionally clean up Firebase AI code.

### 3.1 Migrate All Features

**Feature-by-feature migration:**

```dart
// Week 22: Migrate card evolution
final useGenkitForEvolution = await _remoteConfig.getBool('use_genkit_for_evolution');

// Week 23: Migrate story progression
final useGenkitForStory = await _remoteConfig.getBool('use_genkit_for_story');

// Week 24: Migrate relationship calculations
final useGenkitForRelationship = await _remoteConfig.getBool('use_genkit_for_relationship');
```

### 3.2 Keep Firebase AI as Fallback (Recommended)

```dart
// lib/core/services/production_ai_service.dart
class ProductionAIService {
  final GenkitAIService _genkit;          // Primary
  final DevAIService _firebaseFallback;   // Fallback
  
  Future<DialogueResponse> generateDialogue({
    required String cardId,
    required String playerId,
    required String context,
  }) async {
    try {
      // Primary: Genkit
      return await _genkit.generateDialogue(
        cardId: cardId,
        playerId: playerId,
        context: context,
      );
    } on NetworkException catch (e) {
      AppLogger.error('Genkit network error, using fallback', e);
      
      // Fallback: Firebase AI (for offline scenarios)
      return await _firebaseFallback.generateDevDialogue(
        cardId: cardId,
        context: context,
      );
    } catch (e, stack) {
      AppLogger.error('Genkit failed, using fallback', e, stack);
      
      // Fallback for any other errors
      return await _firebaseFallback.generateDevDialogue(
        cardId: cardId,
        context: context,
      );
    }
  }
}
```

**Why keep fallback:**
- ✅ Safety net for Genkit failures
- ✅ Works offline (Firebase AI is simpler)
- ✅ Minimal cost (only used on failure)
- ✅ Peace of mind

### 3.3 Optional: Remove Firebase AI Code

**Only if:**
- Genkit proven stable for 30+ days
- Fallback not needed (confident in Genkit)
- Team approves removal

**Steps:**
1. Remove `DevAIService` class
2. Remove Firebase AI dependencies from `pubspec.yaml`
3. Update all references to use only `GenkitAIService`
4. Test thoroughly
5. Deploy gradually

**Recommendation:** Keep fallback indefinitely - cost is minimal, safety is valuable

### Week 22-24 Success Criteria

- [ ] All features migrated to Genkit
- [ ] Fallback system tested and working
- [ ] 30 days of stable Genkit operation
- [ ] Cost targets achieved ($2-2.50/player/month)
- [ ] Performance targets met (latency, quality)
- [ ] Team trained and confident
- [ ] Documentation updated
- [ ] **Migration complete! 🎉**

---

## Code Changes Required

### Repository Layer

```dart
// Before (Firebase AI only)
class DialogueRepository {
  final DevAIService _ai;
  
  Future<String> getDialogue(String cardId) async {
    return await _ai.generateDevDialogue(cardId: cardId);
  }
}

// After (Genkit with fallback)
class DialogueRepository {
  final ProductionAIService _ai;  // Includes Genkit + fallback
  
  Future<DialogueResponse> getDialogue(String cardId, String playerId) async {
    return await _ai.generateDialogue(
      cardId: cardId,
      playerId: playerId,
      context: _buildContext(),
    );
  }
}
```

### Service Layer

```dart
// Before
final aiService = DevAIService();

// After
final aiService = ProductionAIService(
  genkit: GenkitAIService(
    baseUrl: 'https://unwritten-genkit-backend-xxx.run.app',
  ),
  firebaseFallback: DevAIService(),
);
```

### Dependency Injection

```dart
// lib/core/di/service_locator.dart
void setupAIServices() {
  // Genkit client
  getIt.registerLazySingleton<GenkitAIService>(
    () => GenkitAIService(
      client: getIt<http.Client>(),
      baseUrl: Environment.genkitBackendUrl,
    ),
  );
  
  // Firebase AI fallback
  getIt.registerLazySingleton<DevAIService>(
    () => DevAIService(),
  );
  
  // Production service (combines both)
  getIt.registerLazySingleton<ProductionAIService>(
    () => ProductionAIService(
      genkit: getIt<GenkitAIService>(),
      firebaseFallback: getIt<DevAIService>(),
    ),
  );
}
```

---

## Rollback Procedures

### Emergency Rollback (< 5 minutes)

**If critical issue detected:**

```bash
# Update Remote Config (immediate)
firebase remoteconfig:set use_genkit_for_dialogue false
firebase remoteconfig:publish

# Result: All traffic back to Firebase AI instantly
```

**No code deployment needed - feature flag controls routing**

### Gradual Rollback (< 30 minutes)

**If issues detected but not critical:**

```bash
# Reduce rollout percentage
firebase remoteconfig:set genkit_rollout_percentage 10.0
firebase remoteconfig:publish

# Monitor for improvement

# If still issues, rollback completely
firebase remoteconfig:set genkit_rollout_percentage 0.0
firebase remoteconfig:publish
```

### Rollback Decision Tree

```
Issue Detected
    ↓
Is error rate > 5%? → YES → EMERGENCY ROLLBACK
    ↓ NO
Is latency > 10s? → YES → EMERGENCY ROLLBACK
    ↓ NO
Is cost > 2x budget? → YES → GRADUAL ROLLBACK
    ↓ NO
User complaints? → YES → INVESTIGATE → May need gradual rollback
    ↓ NO
Monitor closely, may not need rollback
```

---

## Monitoring & Validation

### Key Metrics to Track

**During Migration:**
```dart
class MigrationMetrics {
  // Traffic distribution
  int firebaseRequests = 0;
  int genkitRequests = 0;
  
  // Success rates
  double firebaseSuccessRate = 0.0;
  double genkitSuccessRate = 0.0;
  
  // Latency
  Duration firebaseP95 = Duration.zero;
  Duration genkitP95 = Duration.zero;
  
  // Cost
  double firebaseCostPerRequest = 0.0;
  double genkitCostPerRequest = 0.0;
  
  // Quality
  double firebaseQualityScore = 0.0;
  double genkitQualityScore = 0.0;
}
```

### Validation Checklist

**Before proceeding to next rollout percentage:**
- [ ] Error rate acceptable (< 1%)
- [ ] Latency acceptable (p95 < 3s)
- [ ] Cost within budget
- [ ] Quality maintained
- [ ] No critical incidents
- [ ] User feedback neutral/positive
- [ ] Team comfortable proceeding

---

## Troubleshooting

### Common Issues

**Issue: Genkit latency higher than expected**
- Check Cloud Run cold starts
- Verify model selection (Flash vs Pro)
- Check network latency to Cloud Run
- Consider regional deployment closer to users

**Issue: Genkit error rate elevated**
- Check Cloud Run logs for errors
- Verify Firestore connection
- Check API key validity
- Ensure sufficient Cloud Run capacity

**Issue: Quality degradation**
- Compare prompts (Firebase vs Genkit)
- Verify context is being passed correctly
- Check if tools are working (Firestore access)
- Review RAG retrieval quality

**Issue: Cost higher than expected**
- Check model selection (too much Pro, not enough Flash)
- Verify caching is working
- Check for duplicate requests
- Review token usage patterns

---

## Related Documentation

- **03-implementation-phases.md** - Overall phased strategy
- **20-firebase-ai-integration.md** - Firebase AI reference
- **30-genkit-architecture.md** - Genkit implementation
- **31-genkit-integration-guide.md** - Genkit complete reference

---

**Status:** ✅ Complete Migration Guide  
**Timeline:** Weeks 17-24 (Phase 3)  
**Success Rate:** Target 100% migration with < 1% error rate


