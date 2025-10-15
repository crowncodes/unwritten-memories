# 📱 Flutter App Documentation

> **📐 Architecture Planning:** See `docs/5.architecture/` for high-level architecture  
> **💻 Implementation Details:** This folder contains implementation-specific reference

📅 **Last Updated:** October 14, 2025  
✅ **Status:** Complete

---

## 🎯 Overview

This folder contains practical implementation documentation for the Unwritten Flutter app, including setup guides, package references, and implementation details.

**📐 For Architecture & Planning:** See [docs/5.architecture/](../docs/5.architecture/)  
**💻 For Implementation & Code:** You're in the right place!

---

## ⚡ Quick Start

### 🆕 New Developer?

1. **Setup:** [SETUP.md](./SETUP.md) - Get the app running (10-15 min)
2. **Architecture:** [../docs/5.architecture/50-architecture-overview.md](../docs/5.architecture/50-architecture-overview.md) - Understand the design
3. **Packages:** [packages/README.md](./packages/README.md) - Learn the tools
4. **Implementation:** [CARD_DRAG_INTERACTION_FEATURE.md](./CARD_DRAG_INTERACTION_FEATURE.md) - See working code

---

## 📚 Documentation Structure

### ⚙️ Setup & Configuration

| Document | Purpose | Time Required |
|----------|---------|---------------|
| [SETUP.md](./SETUP.md) | Complete setup guide with troubleshooting | 10-15 min |

### 💡 Implementation Guides

| Document | Purpose |
|----------|---------|
| [CARD_DRAG_INTERACTION_FEATURE.md](./CARD_DRAG_INTERACTION_FEATURE.md) | Card drag system implementation details |
| [CARD_INTERACTION_GUIDE.md](./CARD_INTERACTION_GUIDE.md) | Quick reference for card interactions |

### 📦 Package Reference

| Location | Contents |
|----------|----------|
| [packages/](./packages/) | Detailed documentation for all 25+ packages |
| [packages/README.md](./packages/README.md) | Package overview and update status |

**Key Package Docs:**
- [flame.md](./packages/flame.md) - Game engine (Flame 1.20+)
- [flutter_riverpod.md](./packages/flutter_riverpod.md) - State management (Riverpod 3.x)
- [audioplayers.md](./packages/audioplayers.md) - Audio system
- [vibration.md](./packages/vibration.md) - Haptic feedback
- [hive.md](./packages/hive.md) - Local storage
- [dio.md](./packages/dio.md) - HTTP client
- [tflite_flutter.md](./packages/tflite_flutter.md) - AI/ML integration
- [code_generation.md](./packages/code_generation.md) - Freezed, JSON, build_runner
- [ui_packages.md](./packages/ui_packages.md) - UI and animation packages
- [utilities.md](./packages/utilities.md) - Utility packages

### 🏗️ Architecture Analysis

| Document | Purpose |
|----------|---------|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | Deep dive into I/O FLIP architecture patterns |

### 📊 Visual References

| File | Purpose |
|------|---------|
| [ioflip_architecture.png](./ioflip_architecture.png) | I/O FLIP system architecture diagram |
| [project_structure.png](./project_structure.png) | I/O FLIP project structure diagram |
| [chart_script.py](./chart_script.py) | Architecture diagram generator |
| [chart_script (1).py](./chart_script%20(1).py) | Project structure diagram generator |

---

## 👥 Documentation by Role

### 📱 Flutter Developer

**Start Here:**
1. [SETUP.md](./SETUP.md) - Setup environment
2. [packages/flutter_riverpod.md](./packages/flutter_riverpod.md) - State management
3. [packages/flame.md](./packages/flame.md) - Game engine basics
4. [CARD_DRAG_INTERACTION_FEATURE.md](./CARD_DRAG_INTERACTION_FEATURE.md) - Working example

### 🎮 Game Developer (Flame)

**Start Here:**
1. [packages/flame.md](./packages/flame.md) - Flame package reference
2. [CARD_INTERACTION_GUIDE.md](./CARD_INTERACTION_GUIDE.md) - Quick reference
3. [ARCHITECTURE.md](./ARCHITECTURE.md) - I/O FLIP patterns
4. [../docs/5.architecture/56-card-physics-animations.md](../docs/5.architecture/56-card-physics-animations.md) - Physics architecture

### 📦 Package Integration Work

**Start Here:**
1. [packages/README.md](./packages/README.md) - Package overview
2. [packages/{package_name}.md](./packages/) - Specific package docs
3. [../docs/5.architecture/60-package-integration-overview.md](../docs/5.architecture/60-package-integration-overview.md) - Integration architecture

---

## 🛠️ Common Tasks

### 🚀 Setup Development Environment

```bash
cd app
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
flutter run -d chrome
```

See [SETUP.md](./SETUP.md) for full guide.

### ➕ Add New Package

1. Add to `pubspec.yaml`
2. Run `flutter pub get`
3. Create docs at `packages/{package_name}.md`
4. Update `packages/README.md` with version info

### 🔄 Update Package Documentation

1. Update `packages/{package_name}.md` with new APIs
2. Update version numbers in `packages/README.md`
3. Add migration notes if breaking changes

### 🔍 Find Package Usage Examples

All package docs include:
- Installation instructions
- Basic usage with code examples
- Best practices
- Links to official documentation

---

## 🗺️ Architecture to Implementation Mapping

| Architecture Doc | Implementation Doc | Purpose |
|------------------|-------------------|---------|
| [50-architecture-overview.md](../docs/5.architecture/50-architecture-overview.md) | [ARCHITECTURE.md](./ARCHITECTURE.md) | I/O FLIP patterns |
| [52-development-environment-setup.md](../docs/5.architecture/52-development-environment-setup.md) | [SETUP.md](./SETUP.md) | Quick setup |
| [55-flame-engine-fundamentals.md](../docs/5.architecture/55-flame-engine-fundamentals.md) | [packages/flame.md](./packages/flame.md) | Flame basics |
| [56-card-physics-animations.md](../docs/5.architecture/56-card-physics-animations.md) | [CARD_DRAG_INTERACTION_FEATURE.md](./CARD_DRAG_INTERACTION_FEATURE.md) | Card physics |
| [61-riverpod-integration.md](../docs/5.architecture/61-riverpod-integration.md) | [packages/flutter_riverpod.md](./packages/flutter_riverpod.md) | State management |
| [63-audio-haptics-integration.md](../docs/5.architecture/63-audio-haptics-integration.md) | [packages/audioplayers.md](./packages/audioplayers.md), [packages/vibration.md](./packages/vibration.md) | Audio & haptics |

**Full Mapping:** See [../docs/5.architecture/70-implementation-reference.md](../docs/5.architecture/70-implementation-reference.md)

---

## 🔑 Key Technologies

### 🎮 Game Engine
- **Flame 1.20+** - 2D game engine ([docs](./packages/flame.md))
- **Flutter 3.27+** - UI framework

### 🔄 State Management
- **Riverpod 3.x** - Reactive state ([docs](./packages/flutter_riverpod.md))

### ☁️ Backend (Future)
- **Dart Frog** - Backend framework
- **Firebase** - Cloud services

### 🤖 AI/ML
- **TensorFlow Lite** - On-device AI ([docs](./packages/tflite_flutter.md))

### 💾 Data & Storage
- **Hive** - Local database ([docs](./packages/hive.md))
- **Dio** - HTTP client ([docs](./packages/dio.md))

### ✨ Polish
- **audioplayers** - Audio system ([docs](./packages/audioplayers.md))
- **vibration** - Haptic feedback ([docs](./packages/vibration.md))

---

## 🎯 Performance Targets

All code must meet these targets:

| Metric | Target | Monitoring |
|--------|--------|------------|
| **FPS** | 60 stable | Performance overlay |
| **Frame Time** | < 16ms | DevTools |
| **Memory** | < 200MB | DevTools |
| **App Size** | < 50MB | Build analysis |
| **Battery** | < 10%/30min | Manual testing |

See [SETUP.md](./SETUP.md) for performance monitoring tools.

---

## 💬 Getting Help

### 📚 Documentation Issues

- **Missing info?** Check [../docs/5.architecture/](../docs/5.architecture/) for high-level docs
- **Outdated package?** Check [packages/README.md](./packages/README.md) for latest versions
- **Setup problems?** See [SETUP.md](./SETUP.md) troubleshooting section

### 🐛 Code Issues

- **Build errors?** Run `flutter clean && flutter pub get`
- **Performance issues?** Check [../docs/5.architecture/59-performance-optimization-flame.md](../docs/5.architecture/59-performance-optimization-flame.md)
- **State management?** See [packages/flutter_riverpod.md](./packages/flutter_riverpod.md)

### 🌐 External Resources

- **Flutter Docs:** https://flutter.dev/docs
- **Flame Docs:** https://docs.flame-engine.org/
- **Riverpod Docs:** https://riverpod.dev/
- **I/O FLIP Source:** https://github.com/flutter/io_flip

---

## 🤝 Contributing to Documentation

### ➕ Adding New Implementation Doc

1. Create markdown file in `app/docs/`
2. Follow existing formatting
3. Include code examples
4. Update this README with link

### 🔄 Updating Package Docs

1. Edit `packages/{package_name}.md`
2. Update version numbers
3. Add/update code examples
4. Update `packages/README.md` if version changed

### 📊 Visual Diagrams

Use the included Python scripts to generate diagrams:

```bash
# System architecture diagram
python app/docs/chart_script.py

# Project structure diagram
python app/docs/chart_script\ (1).py
```

---

## 📂 File Organization

```
app/docs/
├── README.md                           # This file
├── SETUP.md                            # Setup guide
├── ARCHITECTURE.md                     # I/O FLIP analysis
├── CARD_DRAG_INTERACTION_FEATURE.md    # Card implementation
├── CARD_INTERACTION_GUIDE.md           # Quick reference
├── ioflip_architecture.png             # System diagram
├── project_structure.png               # Structure diagram
├── chart_script.py                     # Diagram generator
├── chart_script (1).py                 # Diagram generator
└── packages/                           # Package documentation
    ├── README.md                       # Package overview
    ├── flame.md                        # Game engine
    ├── flutter_riverpod.md             # State management
    ├── audioplayers.md                 # Audio
    ├── vibration.md                    # Haptics
    ├── hive.md                         # Storage
    ├── dio.md                          # HTTP
    ├── tflite_flutter.md               # AI/ML
    ├── code_generation.md              # Code gen tools
    ├── ui_packages.md                  # UI packages
    └── utilities.md                    # Utility packages
```

---

## 🔗 Related Documentation

### 📐 Architecture Documentation
- **Index:** [../docs/5.architecture/00-INDEX.md](../docs/5.architecture/00-INDEX.md)
- **Bridge Doc:** [../docs/5.architecture/70-implementation-reference.md](../docs/5.architecture/70-implementation-reference.md)

### 📁 Project Root
- **Master Spec:** [../docs/master_truths_canonical_spec_v_1_2.md](../docs/master_truths_canonical_spec_v_1_2.md)
- **Concept Docs:** [../docs/1.concept/](../docs/1.concept/)
- **Gameplay Docs:** [../docs/2.gameplay/](../docs/2.gameplay/)

---

## 🔧 Maintenance

⏰ **Update Frequency:** When implementation changes

🔔 **Triggers:**
- Package version updates
- New features implemented
- API changes
- Build process changes

👤 **Owner:** Development Team  
📆 **Review Cycle:** Every sprint

---

✅ **Status:** Complete & Current  
🎯 **Purpose:** Practical implementation reference  
👥 **Audience:** Developers building features

---

## 🔗 Quick Links
- [Setup Guide](./SETUP.md)
- [Package Reference](./packages/README.md)
- [Architecture Planning](../docs/5.architecture/)
- [I/O FLIP Analysis](./ARCHITECTURE.md)

