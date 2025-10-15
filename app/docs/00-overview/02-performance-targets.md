# Performance Targets

## Critical Metrics

All features must meet these targets. Performance is a PRIMARY metric for Unwritten.

### 60 FPS Gameplay

| Metric | Target | Measurement |
|--------|--------|-------------|
| Frame Time | < 16.67ms | DevTools Timeline |
| Dropped Frames | < 1% | Performance Overlay |
| Average FPS | ≥ 58 | Sustained over 5min |
| Jank | 0 occurrences | 100ms+ frames |

### AI Inference

| Metric | Target | Context |
|--------|--------|---------|
| Inference Time | < 15ms | Per card analysis |
| Model Load | < 2s | App startup |
| Memory | < 50MB | Model + inference |

### Battery Life

| Metric | Target | Test Conditions |
|--------|--------|-----------------|
| Drain Rate | < 10%/30min | Active gameplay |
| Background | < 1%/hour | App in background |
| Idle | < 0.1%/hour | Game paused |

### Memory Usage

| Metric | Target | Platform |
|--------|--------|----------|
| Base | < 200MB | All platforms |
| Peak | < 300MB | During effects |
| Leak Rate | 0 MB/hour | Memory profiler |

### App Size

| Metric | Target | Notes |
|--------|--------|-------|
| APK/IPA | < 50MB | Without assets |
| With Assets | < 150MB | Including sprites, audio |
| Download | < 30MB | Initial download |

## Monitoring

### DevTools Performance Tab

```bash
flutter pub global activate devtools
flutter pub global run devtools
```

**Check for:**
- Frame rendering time < 16.67ms
- Shader compilation jank (first run only)
- Memory allocation spikes

### Performance Overlay

```dart
MaterialApp(
  showPerformanceOverlay: true,
  checkerboardOffscreenLayers: true,  // Check for excessive layers
  checkerboardRasterCacheImages: true,  // Check for caching issues
)
```

### Custom Performance Logger

```dart
class AppLogger {
  static void performance(String operation, Duration duration) {
    if (duration.inMilliseconds > 16) {
      print('⚠️ PERF: $operation took ${duration.inMilliseconds}ms');
    }
  }
}

// Usage
final stopwatch = Stopwatch()..start();
await heavyOperation();
AppLogger.performance('Heavy operation', stopwatch.elapsed);
```

## Optimization Checklist

Before shipping any feature:

- [ ] Frame time < 16.67ms (DevTools)
- [ ] No memory leaks (Memory profiler)
- [ ] Animations smooth on mid-range devices
- [ ] Battery drain < 10%/30min
- [ ] Component count reasonable (< 200 active)
- [ ] Particle count limited (< 100)
- [ ] Assets properly cached
- [ ] Const constructors used
- [ ] Heavy operations async (compute())

## Performance Budget

### Per-Frame Budget (16.67ms)

- UI Update: < 4ms
- Game Update: < 6ms
- Rendering: < 6ms
- Buffer: 0.67ms

### Component Limits

- Active Components: < 200
- Particles: < 100
- Active Animations: < 50
- Audio Sources: < 10

## Testing Devices

Test on these device categories:

1. **High-end:** iPhone 14+, Pixel 8+
2. **Mid-range:** iPhone SE, Pixel 4a ⭐ (Primary target)
3. **Low-end:** iPhone 8, Budget Android

Target: 60 FPS on mid-range devices.

---

**Previous:** [Quick Start](./01-quick-start.md)  
**Next:** [Architecture Principles](./03-architecture-principles.md)  
**Related:** [Flame Performance](../02-flame-engine/09-performance-optimization.md)


