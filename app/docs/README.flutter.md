# 📱 Flutter App Documentation

> **🎯 Master Spec:** [`docs/master_flutter_flame_spec_v_1_0.md`](../../docs/master_flutter_flame_spec_v_1_0.md) - Authoritative technical guide  
> **💻 App Implementation:** This folder contains Unwritten-specific implementation documentation

📅 **Last Updated:** October 15, 2025  
✅ **Status:** Reorganized - Flame-First Architecture

---

## 🎯 Overview

Comprehensive documentation for building Unwritten with Flutter and Flame. All patterns derive from the master Flutter/Flame spec and focus on 60 FPS, Unity-level game feel.

**🎮 Master Reference:** [master_flutter_flame_spec_v_1_0.md](../../docs/master_flutter_flame_spec_v_1_0.md)  
**🎨 Visual Generation:** [docs/4.visual/](../../docs/4.visual/) (Asset creation, artistic direction)  
**🎵 Music System:** [docs/9.music/](../../docs/9.music/) (Audio generation, stems)  
**💻 App Implementation:** You're here!

---

## 📚 Documentation Structure

### Core Documentation (Numbered)

| Section | Purpose | Key Files |
|---------|---------|-----------|
| **[00-overview/](./00-overview/)** | Quick start, performance targets, principles | 00-INDEX.md, 01-quick-start.md |
| **[01-architecture/](./01-architecture/)** | Project structure, Clean Architecture | 01-project-structure.md |
| **[02-flame-engine/](./02-flame-engine/)** | Complete Flame implementation guide | 10 detailed docs |
| **[03-state-management/](./03-state-management/)** | Riverpod patterns | Game state providers |
| **[04-audio-visuals/](./04-audio-visuals/)** | Audio, music, haptics, effects | Audio system, SFX pool |
| **[05-performance/](./05-performance/)** | 60 FPS guidelines, profiling | Memory, battery optimization |
| **[06-integration/](./06-integration/)** | Firebase, AI, storage | Setup guides |

### Package Documentation

| Package | Documentation | Flame Integration |
|---------|---------------|-------------------|
| **flame** | [flame.md](./flame.md) | ✓ Complete |
| **audioplayers** | [audioplayers.md](./audioplayers.md) | ✓ With examples |
| **flutter_riverpod** | [flutter_riverpod.md](./flutter_riverpod.md) | ✓ Game state |
| **vibration** | [vibration.md](./vibration.md) | ✓ Patterns |
| **hive** | [hive.md](./hive.md) | Local storage |
| **tflite_flutter** | [tflite_flutter.md](./tflite_flutter.md) | AI inference |

See [README.packages.md](./README.packages.md) for all packages.

---

## ⚡ Quick Start

### 🆕 New to Flame?

1. **Master Spec:** [master_flutter_flame_spec](../../docs/master_flutter_flame_spec_v_1_0.md) (Read lines 1-100)
2. **Component System:** [02-flame-engine/01-component-system.md](./02-flame-engine/01-component-system.md)
3. **Quick Start:** [00-overview/01-quick-start.md](./00-overview/01-quick-start.md)
4. **Example:** [CARD_INTERACTION_GUIDE.md](./CARD_INTERACTION_GUIDE.md)

### 🔨 Building Features?

1. **Architecture:** [01-architecture/01-project-structure.md](./01-architecture/01-project-structure.md)
2. **Performance:** [05-performance/01-60fps-guidelines.md](./05-performance/01-60fps-guidelines.md)
3. **State Management:** [03-state-management/02-game-state-providers.md](./03-state-management/02-game-state-providers.md)
4. **Flame Integration:** [02-flame-engine/](./02-flame-engine/00-INDEX.md)

### 🐛 Debugging?

1. **Linter:** `flutter analyze`
2. **Tests:** `flutter test`
3. **Profiler:** DevTools → Performance tab
4. **Setup Issues:** [SETUP.md](./SETUP.md)

---

## 📦 Additional Resources

### Setup & Configuration

- **[SETUP.md](./SETUP.md)** - Complete setup guide with troubleshooting (10-15 min)
- **[Firebase Integration](./0.firebase/)** - Firebase setup guides

### Implementation Examples

- **[CARD_DRAG_INTERACTION_FEATURE.md](./CARD_DRAG_INTERACTION_FEATURE.md)** - Card drag system (working example)
- **[CARD_INTERACTION_GUIDE.md](./CARD_INTERACTION_GUIDE.md)** - Quick card reference

### Package Docs (All 25+ packages)

See [README.packages.md](./README.packages.md) for complete package list and update status.

---

## 🏗️ Archive

### Archived Reference Material

- **[_archive/2025-10-15/IOFLIP_REFERENCE.md](./_archive/2025-10-15/IOFLIP_REFERENCE.md)** - I/O FLIP architecture study (external reference)
- Note: I/O FLIP was a multiplayer game with Dart Frog backend - NOT applicable to Unwritten's single-player architecture

---

## 👥 Quick Navigation by Role

### 🆕 New to Project

1. [00-overview/01-quick-start.md](./00-overview/01-quick-start.md) - Setup and first run
2. [00-overview/03-architecture-principles.md](./00-overview/03-architecture-principles.md) - Core principles
3. [02-flame-engine/01-component-system.md](./02-flame-engine/01-component-system.md) - Flame basics

### 🎨 Working on UI/Visuals

1. [02-flame-engine/03-sprite-animation-system.md](./02-flame-engine/03-sprite-animation-system.md) - Sprite animations
2. [02-flame-engine/04-particle-effects.md](./02-flame-engine/04-particle-effects.md) - Visual effects
3. [04-audio-visuals/](./04-audio-visuals/00-INDEX.md) - Audio and visual polish

### ⚡ Optimizing Performance

1. [05-performance/01-60fps-guidelines.md](./05-performance/01-60fps-guidelines.md) - 60 FPS rules
2. [02-flame-engine/09-performance-optimization.md](./02-flame-engine/09-performance-optimization.md) - Flame optimization
3. [00-overview/02-performance-targets.md](./00-overview/02-performance-targets.md) - Target metrics

---

## 🔑 Key Technologies

### 🎮 Game Engine
- **Flame 1.20+** - 2D game engine ([docs](./packages/flame.md))
- **Flutter 3.27+** - UI framework

### 🔄 State Management
- **Riverpod 3.x** - Reactive state ([docs](./flutter_riverpod.md))

### ☁️ Cloud Services
- **Firebase** - Auth, Firestore, App Check ([docs](./06-integration/01-firebase-setup.md))

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

