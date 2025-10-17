# Unwritten

AI-powered card-based mobile game built with Flutter, featuring on-device TensorFlow Lite inference for personality modeling, sentiment analysis, and dynamic dialogue generation.

## Features

- 🤖 **AI Training Data Generation** - Generate 40,000+ high-quality training samples using Qwen3 models
- 🎮 **Novel-Quality Character Interactions** - Realistic emotional capacity constraints and personality-driven behavior
- 🎭 **Dramatic Irony System** - "Yelling at screen" tension moments with knowledge gap scenarios
- 💰 **Cost-Effective** - Local generation at 5-7x lower cost than cloud APIs
- ⚡ **High Performance** - Optimized for RTX 4070 SUPER: 6,500+ samples/day

## Quick Start - Training Data Generation

### 1. Clone and Setup

```powershell
# Clone repository
git clone https://github.com/yourusername/unwritten.git
cd unwritten

# Create virtual environment
python -m venv unwritten-env
.\unwritten-env\Scripts\Activate.ps1

# Install dependencies
pip install -e .
```

### 2. Install Ollama & Models

```powershell
# Download from https://ollama.ai/download and install

# Run automated setup (downloads ~60GB of models)
.\scripts\setup_ollama.ps1
```

### 3. Test Your Setup

```powershell
# Quick verification (2 minutes)
python scripts\quick_test.py
```

### 4. Start Generating Training Data

```powershell
# Run the pipeline
python scripts\run_training_pipeline.py

# Select your duration:
#   1. Test run (1 hour) - ~270 samples
#   2. Half day (12 hours) - ~3,250 samples  
#   3. Full day (24 hours) - ~6,500 samples
#   4. Custom duration
```

**📚 For detailed setup instructions, see [TRAINING_SETUP.md](TRAINING_SETUP.md)**

## Project Structure

```
unwritten/
├── src/unwritten/
│   ├── training/                      # Training data generation
│   │   ├── qwen3_generator.py        # Main generation pipeline
│   │   └── config.py                  # Configuration
│   ├── utils/
│   │   └── logger.py                  # Structured logging
│   └── ...
├── scripts/
│   ├── setup_ollama.ps1               # Ollama setup (Windows)
│   ├── run_training_pipeline.py       # Main runner
│   └── quick_test.py                  # Quick verification
├── docs/                               # Game design documentation
├── data/                               # Strategy docs & original pipeline
├── training_output/                    # Generated training data
├── TRAINING_SETUP.md                   # Comprehensive setup guide
└── SETUP_COMPLETE.md                   # Setup summary
```

## Training Data Generation

### Generate High-Quality Data

```powershell
# Activate environment
.\unwritten-env\Scripts\Activate.ps1

# Run production cycle
python scripts\run_training_pipeline.py
```

### Programmatic Usage

```python
from unwritten.training import Qwen3DataGenerator, TrainingConfig

# Initialize with custom config
config = TrainingConfig()
config.batch_size_emotional = 20  # Adjust as needed

# Create generator
generator = Qwen3DataGenerator(config)

# Generate specific data types
emotional_data = generator.generate_emotional_authenticity_batch()
dramatic_data = generator.generate_dramatic_irony_batch()

# Or run full production cycle
results = generator.run_production_cycle(duration_hours=24)
```

### Monitor Progress

```powershell
# Watch logs in real-time
Get-Content training_generation.log -Wait

# Check GPU utilization
nvidia-smi -l 1

# View generated files
Get-ChildItem training_output\
```

### What Gets Generated

The pipeline produces 5 types of training data:

1. **Emotional Authenticity** (1,500/day) - Characters constrained by emotional capacity
2. **Dramatic Irony** (1,200/day) - Knowledge gap scenarios with 3 dialogue options
3. **Personality Traits** (2,000/day) - OCEAN trait predictions from dialogue
4. **Tension Building** (800/day) - Narrative tension techniques
5. **Relationship Scoring** (1,000/day) - Interaction quality scores

**Total:** ~6,500 samples/day | ~45,000 in 7 days

## Configuration

### Environment Variables

```powershell
# Ollama optimization
$env:OLLAMA_KEEP_ALIVE = "24h"
$env:OLLAMA_MAX_LOADED_MODELS = "3"
$env:OLLAMA_GPU_LAYERS = "999"

# Training output
$env:TRAINING_OUTPUT_DIR = "D:\unwritten_training"

# Debug logging
$env:UNWRITTEN_DEBUG = "true"
```

### Training Configuration

Edit `src/unwritten/training/config.py`:

```python
@dataclass
class TrainingConfig:
    # Models
    model_primary: str = "qwen3:30b-a3b"
    model_speed: str = "qwen3:8b"
    model_validation: str = "qwen3:32b"
    
    # Batch sizes (adjust for your hardware)
    batch_size_emotional: int = 15
    batch_size_dramatic: int = 10
    
    # Temperature settings
    temp_emotional: float = 0.88
    temp_dramatic: float = 0.82
    
    # Daily targets
    target_emotional_authenticity: int = 1500
    target_dramatic_irony: int = 1200
```

## Hardware Requirements

### Recommended (Your Setup)

- **GPU:** RTX 4070 SUPER (12GB VRAM)
- **RAM:** 128GB
- **Storage:** ~60GB for models + generated data
- **OS:** Windows 10/11

### Minimum

- **GPU:** RTX 3060 (12GB VRAM) or better
- **RAM:** 32GB (can run 1-2 models)
- **Storage:** ~30GB for reduced model set

## Performance Expectations

| Hardware | Models | Speed | Daily Output |
|----------|--------|-------|--------------|
| RTX 4070 SUPER + 128GB | All 3 | 25-50 tok/s | 6,500 samples |
| RTX 3080 + 64GB | 2 models | 20-40 tok/s | 4,000 samples |
| RTX 3060 + 32GB | 1 model | 15-30 tok/s | 2,500 samples |

## Cost Analysis

**Local Generation (Qwen3):**
- Hardware: Already owned
- Electricity: ~$3-5/day
- 7 days: **~$25-35**
- Output: 45,000+ samples

**Cloud Alternative (Claude 3.5 Sonnet):**
- API costs: **~$180**
- Same output

**Savings: 5-7x cheaper locally**

## Development

### Code Style

Follows clean architecture and Flutter best practices:

```powershell
# Format Python code
black src/

# Type checking
mypy src/

# Run tests
pytest tests/
```

## Documentation

- **[TRAINING_SETUP.md](TRAINING_SETUP.md)** - Comprehensive setup guide
- **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - What was created and how to use it
- **[scripts/README.md](scripts/README.md)** - Script documentation
- **[data/qwen3_strategy_doc.md](data/qwen3_strategy_doc.md)** - Generation strategy
- **[docs/](docs/)** - Game design documentation

### Managing Prompts with Dotprompt (Genkit)

Use Dotprompt to centralize and version prompts, models, and parameters. This keeps personas, places, and canonical modifiers consistent across generations while allowing per-call inputs.

- Recommended layout:
  - `functions/prompts/partials/persona.partial.md`
  - `functions/prompts/partials/place.partial.md`
  - `functions/prompts/partials/truths_modifiers.partial.md` (distill rules from `docs/master_truths_canonical_spec_v_1_2.md`)
  - `functions/prompts/image/person_place_image.prompt` (composes partials)

- Minimal prompt example (multi-message + partials):
  ```yaml
  model: googleai/gemini-2.5-flash-image-preview
  input:
    type: object
    properties:
      person_id: { type: string }
      place_id: { type: string }
      action: { type: string }
      style_hint: { type: string, nullable: true }
  messages:
  - role: system
    content: |
      {{> persona }}
      {{> place }}
      {{> truths_modifiers }}
      {{#if style_hint}}Style hint: {{style_hint}}{{/if}}
  - role: user
    content: |
      Generate a single image of {{person_id}} at {{place_id}} doing: {{action}}.
      Maintain persona likeness and place continuity; follow canonical modifiers.
  ```

- Call from a Genkit flow:
  ```ts
  import { genkit, z } from 'genkit';
  import { googleAI } from '@genkit-ai/google-genai';
  import { loadPrompt } from 'genkit/dotprompt';

  const ai = genkit({ plugins: [googleAI()] });

  export const generateImage = ai.defineFlow(
    {
      name: 'generateImage',
      inputSchema: z.object({ person_id: z.string(), place_id: z.string(), action: z.string(), style_hint: z.string().optional() }),
      outputSchema: z.object({ imageUri: z.string() })
    },
    async (input) => {
      const prompt = await loadPrompt('functions/prompts/image/person_place_image.prompt');
      const rendered = await prompt.render(input);
      const { media } = await ai.generate({ model: googleAI.model('gemini-2.5-flash-image-preview'), prompt: rendered, output: { format: 'media' } });
      if (!media?.url) throw new Error('No image produced');
      return { imageUri: media.url };
    }
  );
  ```

Docs: [Managing prompts with Dotprompt](https://genkit.dev/docs/dotprompt/)

## Troubleshooting

### Ollama Issues

```powershell
# Service not running
ollama serve

# Models not loading
ollama pull qwen3:8b

# GPU not detected
$env:OLLAMA_GPU_LAYERS = "999"
```

### Performance Issues

```powershell
# Check GPU utilization
nvidia-smi

# Reduce batch sizes in config.py
# Close other GPU applications
# Ensure adequate cooling
```

### Generation Quality

```powershell
# Review samples
code training_output\emotional_authenticity_batch0001_*.json

# Adjust temperature in config.py
# Modify prompts in qwen3_generator.py
```

## Flutter Game Implementation

**NEW:** Master implementation plan now available!

### Getting Started with Game Development

```bash
# 1. Read the implementation plan
open docs/5.architecture/IMPLEMENTATION-PLAN-MVP.md

# 2. Follow setup guide
open docs/5.architecture/FLUTTER-PROJECT-SETUP.md

# 3. Quick start for developers
open docs/5.architecture/QUICK-START-DEVELOPER-GUIDE.md
```

### Implementation Strategy

**Phase 1 (Weeks 1-4): Foundation**
- Flutter project setup with Clean Architecture
- Core data models (Card, GameState, Relationship)
- Base card JSON with 50 starter cards
- Basic UI framework

**Phase 2 (Weeks 5-8): Core Game Loop**
- Card playing system
- Turn-based progression
- Resource management
- Local storage with Hive

**Phase 3 (Weeks 9-12): Cloud AI Integration**
- OpenAI/Anthropic API integration
- NPC personality-driven responses
- Card evolution with AI
- **Training data collection from real gameplay**

**Phase 4 (Weeks 13-16): Season Structure**
- 12/24/36 week seasons
- Aspiration tracking
- Relationship progression
- Season archives

**Phase 5 (Weeks 17-20): Polish & Beta**
- Onboarding flow
- UI/UX polish
- Analytics & monitoring
- Beta deployment

### Why Cloud AI First?

1. **Training Data Quality**: Collect real gameplay interactions for model fine-tuning
2. **Iteration Speed**: Modify prompts without rebuilding models
3. **Flexibility**: Test different AI providers and strategies
4. **Validation**: Ensure game loop works before local optimization

**Local AI (TensorFlow Lite) comes in Phase 6+** after we have:
- High-quality training data from gameplay
- Validated game mechanics
- Proven prompt engineering
- Beta testing feedback

### Documentation

- **[Master Implementation Plan](docs/5.architecture/IMPLEMENTATION-PLAN-MVP.md)** - Complete roadmap
- **[Flutter Setup Guide](docs/5.architecture/FLUTTER-PROJECT-SETUP.md)** - Technical setup
- **[Developer Quick Start](docs/5.architecture/QUICK-START-DEVELOPER-GUIDE.md)** - Fast onboarding
- **[Architecture Index](docs/5.architecture/README.md)** - Documentation hub

### Current Status

- ✅ Training data generation pipeline operational
- ✅ 45,000+ samples generated in 7 days
- ✅ Master implementation plan completed
- ⏳ Phase 1 (Foundation) - Starting
- ⏳ Flutter project initialization

**Target**: Playable MVP in 16 weeks, Beta-ready in 20 weeks

## AI Integration Options (NEW!)

Unwritten supports **three AI approaches** for different use cases. Choose the right one for each feature:

### 📚 Complete AI Documentation Suite

- **[AI Approach Comparison](docs/3.ai/ai_approach_comparison.md)** - **START HERE!** Compare TFLite vs Firebase AI Logic vs Genkit
- **[Firebase AI Logic Guide](docs/3.ai/firebase_ai_logic_integration_guide.md)** - Simple client-side AI (fastest to implement)
- **[Genkit Documentation Index](docs/3.ai/GENKIT_DOCUMENTATION_INDEX.md)** - Backend AI workflows (full control)
- **[Genkit Implementation Tutorial](docs/3.ai/genkit_implementation_tutorial.md)** - Step-by-step Genkit guide
- **[Genkit Integration Guide](docs/3.ai/genkit_integration_guide.md)** - Comprehensive Genkit reference
- **[Genkit Quick Reference](docs/3.ai/genkit_quick_reference.md)** - Genkit cheat sheet
- **[Genkit Architecture](docs/5.architecture/genkit_architecture.md)** - Design decisions & scaling

### 🎯 Three AI Approaches

```
Fast & Fixed (< 20ms)     Simple & Quick (MVP)      Complex Workflows (Production)
┌───────────────────┐    ┌──────────────────────┐  ┌────────────────────────────┐
│ TFLite            │    │ Firebase AI Logic    │  │ Genkit Backend             │
│ (On-Device)       │    │ (Client SDK)         │  │ (Server)                   │
│                   │    │                      │  │                            │
│ ✓ Personality     │    │ ✓ Simple dialogue    │  │ ✓ Complex story            │
│ ✓ Sentiment       │    │ ✓ Image analysis     │  │ ✓ RAG + Tool calling       │
│ ✓ Quick scoring   │    │ ✓ Quick prototypes   │  │ ✓ Multi-step workflows     │
└───────────────────┘    └──────────────────────┘  └────────────────────────────┘
     Always free            $3.50/1K users/mo          $13.50/1K users/mo
                                                       (better control & caching)
```

### 🚀 Quick Start

**Option 1: Firebase AI Logic** (Fastest - 1-2 hours)
```bash
# Add to Flutter app
cd app
flutter pub add firebase_ai

# Use directly in code - no backend needed!
final model = FirebaseAI.googleAI().generativeModel(model: 'gemini-2.5-flash');
final response = await model.generateContent([Content.text('Generate dialogue')]);
```
📖 [Firebase AI Logic Guide](docs/3.ai/firebase_ai_logic_integration_guide.md)

**Option 2: Genkit Backend** (Full control - 2-3 hours)
```bash
# Set up Python backend
cd unwritten-genkit-backend
pip install genkit google-genkit-ai
python main.py

# Integrate with Flutter
cd app
flutter pub add http
```
📖 [Genkit Implementation Tutorial](docs/3.ai/genkit_implementation_tutorial.md)

**Not Sure Which?** → [AI Approach Comparison](docs/3.ai/ai_approach_comparison.md)

### 💰 Cost-Effective

- 1,000 users × 50 dialogues/month = **~$3.50/month**
- With optimization: **~$1.50-2.00/month**
- Scales efficiently with caching and smart routing

### 🔥 Key Benefits

1. **Flexible Architecture**: Choose TFLite, Firebase AI Logic, or Genkit for each feature
2. **Fast Development**: Firebase AI Logic gets AI working in 1-2 hours
3. **Battery Efficient**: TFLite for fast operations, cloud for creative
4. **Offline Support**: TFLite works offline, cloud has graceful fallbacks
5. **Cost Effective**: $3.50/1K users with Firebase AI, optimizable with Genkit
6. **Production Ready**: Security (App Check), monitoring, error handling

### 📖 Learning Path

- **Start Here** (15 min): [AI Approach Comparison](docs/3.ai/ai_approach_comparison.md) - Choose the right approach
- **Quick Start** (1-2 hours): [Firebase AI Logic Guide](docs/3.ai/firebase_ai_logic_integration_guide.md) - Fastest implementation
- **Intermediate** (2-8 hours): [Genkit Tutorial](docs/3.ai/genkit_implementation_tutorial.md) + [Architecture](docs/5.architecture/genkit_architecture.md)
- **Advanced** (8+ hours): RAG, tool calling, multi-region deployment

### 🔗 External Resources

- [Firebase AI Logic Docs](https://firebase.google.com/docs/ai-logic)
- [Genkit Docs](https://genkit.dev/docs/?lang=python)
- [Google AI Studio](https://aistudio.google.com)
- [Gemini API](https://ai.google.dev/gemini-api)

## Roadmap

### Training Data Pipeline
- [x] Training data generation pipeline
- [x] Qwen3 integration
- [x] Quality validation system
- [x] 45,000+ samples generated

### AI Integration
- [x] Complete AI documentation suite (7 comprehensive guides)
- [x] Three approaches documented: TFLite, Firebase AI Logic, Genkit
- [x] Integration architectures designed
- [x] Comparison guide for choosing approach
- [ ] Firebase AI Logic implementation (MVP approach)
- [ ] Genkit Python backend implementation (production approach)
- [ ] Flutter AI services integration
- [ ] Cloud Run deployment (for Genkit)

### Flutter Game (MVP Focus)
- [x] Master implementation plan
- [ ] Phase 1: Foundation (Weeks 1-4)
- [ ] Phase 2: Core game loop (Weeks 5-8)
- [ ] Phase 3: Cloud AI integration (Weeks 9-12)
- [ ] Phase 4: Season structure (Weeks 13-16)
- [ ] Phase 5: Polish & beta (Weeks 17-20)

### Post-MVP (Phase 6+)
- [ ] Local TensorFlow Lite integration
- [ ] Model fine-tuning from gameplay data
- [ ] On-device inference optimization
- [ ] Novel generation pipeline
- [ ] Cloud save/sync

## Contributing

This project follows conventional commits and clean architecture principles.

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Follow commit conventions: `feat(scope): description`
4. Push to the branch
5. Open a Pull Request

See workspace rules for coding standards and best practices.

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Qwen3 models by Alibaba Cloud
- Ollama for local LLM runtime
- Flutter & Flame game engine
- TensorFlow Lite team

---

**Ready to generate training data? Start with:**

```powershell
.\scripts\setup_ollama.ps1
```

**Questions? Check [TRAINING_SETUP.md](TRAINING_SETUP.md) for comprehensive documentation.**

