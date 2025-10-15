# Performance Documentation Index

## Overview

60 FPS gameplay is non-negotiable. This section covers profiling, optimization, and memory management for stable performance.

## Documentation Files

1. **01-60fps-guidelines.md** - Rules for maintaining 60 FPS
2. **02-memory-management.md** - Memory optimization patterns
3. **03-battery-optimization.md** - Power efficiency techniques
4. **04-profiling-tools.md** - DevTools, performance overlays, custom monitoring

## Performance Targets

| Metric | Target |
|--------|--------|
| Frame Time | < 16.67ms |
| Average FPS | ≥ 58 |
| Memory | < 200MB |
| Battery | < 10%/30min |

## Quick Checks

```bash
# Analyze performance
flutter run --profile

# Enable overlay
MaterialApp(showPerformanceOverlay: true)

# DevTools
flutter pub global run devtools
```

---

**Related:** [Performance Targets](../00-overview/02-performance-targets.md), [Flame Performance](../02-flame-engine/09-performance-optimization.md)


