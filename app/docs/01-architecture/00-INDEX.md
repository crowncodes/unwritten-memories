# Architecture Documentation Index

## Overview

Unwritten follows Clean Architecture with feature-based organization. This section details the project structure, layering, and dependency patterns.

## Documentation Files

1. **[Project Structure](./01-project-structure.md)** - Directory layout and file organization
2. **[Clean Architecture Layers](./02-clean-architecture-layers.md)** - Data, Domain, Presentation layers
3. **[Feature Organization](./03-feature-organization.md)** - How to structure new features
4. **[Dependency Injection](./04-dependency-injection.md)** - Riverpod-based DI patterns

## Quick Reference

### Folder Structure

```
lib/
├── core/                   # Shared utilities, constants, errors
│   ├── constants/
│   ├── errors/
│   ├── utils/
│   └── performance/
├── features/               # Feature modules
│   ├── cards/
│   │   ├── data/          # Data layer
│   │   ├── domain/        # Domain layer
│   │   └── presentation/  # Presentation layer (UI + Flame)
│   ├── game/
│   └── ai/
└── shared/                 # Shared across features
    ├── widgets/           # Reusable UI components
    └── services/          # Global services
```

### Layer Dependencies

```
Presentation → Domain → Data
(Flame/UI)     (Logic)   (API/DB)
```

### Feature Template

```
features/feature_name/
├── data/
│   ├── models/
│   ├── repositories/
│   └── datasources/
├── domain/
│   ├── entities/
│   ├── usecases/
│   └── repositories/
└── presentation/
    ├── screens/
    ├── widgets/
    ├── components/  # Flame components
    └── providers/   # Riverpod state
```

---

**Related:** [Overview](../00-overview/00-INDEX.md), [Flame Engine](../02-flame-engine/00-INDEX.md)


