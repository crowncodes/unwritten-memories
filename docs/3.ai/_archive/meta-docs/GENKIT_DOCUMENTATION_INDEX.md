# Genkit Documentation Index

## Overview

This index provides a roadmap to all Genkit-related documentation for the Unwritten project. Genkit is a framework for building AI-powered applications that we're integrating to enhance dialogue generation and narrative experiences.

## Documentation Structure

```
docs/
├── 3.ai/
│   ├── genkit_integration_guide.md              # Comprehensive integration guide
│   ├── genkit_quick_reference.md                # Quick reference & cheat sheet
│   ├── genkit_implementation_tutorial.md        # Step-by-step tutorial
│   ├── firebase_ai_logic_integration_guide.md   # Firebase AI Logic (complete guide)
│   ├── firebase_ai_flutter_quick_start.md       # Firebase AI Flutter package (NEW!)
│   ├── ai_approach_comparison.md                # Compare all 3 approaches
│   ├── AI_INTEGRATION_COMPLETE_SUMMARY.md       # Complete documentation summary
│   └── GENKIT_DOCUMENTATION_INDEX.md            # This file
└── 5.architecture/
    └── genkit_architecture.md                   # Architecture & design decisions
```

## Getting Started

### For Developers New to Genkit

**Start here**: [Genkit Implementation Tutorial](./genkit_implementation_tutorial.md)

This hands-on tutorial walks you through:
- Setting up a Genkit backend (45 minutes)
- Integrating with Flutter app (1 hour)
- Deploying to Cloud Run (30 minutes)

**Prerequisites**: Python 3.11+, Node.js 18+, Flutter environment

### For Understanding the Architecture

**Read**: [Genkit Architecture](../5.architecture/genkit_architecture.md)

Comprehensive architecture documentation covering:
- Hybrid TFLite + Genkit approach
- Decision flow diagrams
- Component responsibilities
- Data flow examples
- Scaling strategy
- Performance optimization

### For Daily Development Reference

**Use**: [Genkit Quick Reference](./genkit_quick_reference.md)

Quick access to:
- Common commands
- Code snippets
- Decision matrices
- Performance targets
- Cost estimates
- Troubleshooting tips

### For Complete Integration Details

**Study**: [Genkit Integration Guide](./genkit_integration_guide.md)

In-depth guide covering:
- What is Genkit and why use it
- Installation & setup
- Core features (models, flows, tools, RAG)
- Integration patterns
- Performance optimization
- Monitoring & analytics
- Security best practices
- Testing strategies
- Cost management

## Quick Navigation

### By Topic

#### Installation & Setup
- [Tutorial - Backend Setup](./genkit_implementation_tutorial.md#part-1-backend-setup-45-minutes)
- [Tutorial - Flutter Integration](./genkit_implementation_tutorial.md#part-2-flutter-integration-1-hour)
- [Guide - Installation](./genkit_integration_guide.md#installation--setup)

#### Architecture & Design
- [Architecture Overview](../5.architecture/genkit_architecture.md#architecture-diagram)
- [Decision Flow](../5.architecture/genkit_architecture.md#decision-flow-when-to-use-each-service)
- [Hybrid Approach](./genkit_integration_guide.md#why-use-genkit-with-unwritten)

#### Core Features
- [AI Models](./genkit_integration_guide.md#1-ai-models-aigenerate)
- [Flows](./genkit_integration_guide.md#2-flows-workflows)
- [Tool Calling](./genkit_integration_guide.md#3-tool-calling)
- [RAG](./genkit_integration_guide.md#4-retrieval-augmented-generation-rag)

#### Development
- [Developer Tools](./genkit_integration_guide.md#developer-tools)
- [Testing](./genkit_integration_guide.md#testing)
- [Error Handling](./genkit_quick_reference.md#error-handling-pattern)
- [Caching Strategy](./genkit_quick_reference.md#caching-strategy)

#### Deployment
- [Deploy to Cloud Run](./genkit_implementation_tutorial.md#part-3-deployment-30-minutes)
- [Deployment Guide](./genkit_integration_guide.md#deployment)
- [Scaling Strategy](../5.architecture/genkit_architecture.md#scaling-strategy)

#### Performance
- [Performance Optimization](./genkit_integration_guide.md#performance-optimization)
- [Performance Targets](./genkit_quick_reference.md#performance-targets)
- [Battery-Aware AI](./genkit_integration_guide.md#pattern-2-battery-aware-ai)

#### Cost & Monitoring
- [Cost Management](./genkit_integration_guide.md#cost-management)
- [Cost Estimates](./genkit_quick_reference.md#cost-estimates-gemini-25-flash)
- [Monitoring](./genkit_integration_guide.md#monitoring--analytics)
- [Observability](../5.architecture/genkit_architecture.md#monitoring--observability)

#### Security
- [Security Best Practices](./genkit_integration_guide.md#security-best-practices)
- [Security Architecture](../5.architecture/genkit_architecture.md#security-architecture)

#### Troubleshooting
- [Common Issues](./genkit_integration_guide.md#troubleshooting)
- [Tutorial Troubleshooting](./genkit_implementation_tutorial.md#troubleshooting)
- [Quick Reference](./genkit_quick_reference.md#useful-links)

### By Use Case

#### "I want to add AI dialogue to my Flutter app"
1. Follow [Implementation Tutorial](./genkit_implementation_tutorial.md)
2. Review [Integration Patterns](./genkit_integration_guide.md#integration-patterns)
3. Check [Quick Reference](./genkit_quick_reference.md) for code snippets

#### "I need to understand how Genkit fits with TFLite"
1. Read [Architecture Overview](../5.architecture/genkit_architecture.md)
2. Review [Decision Matrix](./genkit_quick_reference.md#decision-matrix-tflite-vs-genkit)
3. Study [Hybrid Approach](./genkit_integration_guide.md#hybrid-approach-tflite--genkit)

#### "I want to deploy to production"
1. Complete [Tutorial - Deployment](./genkit_implementation_tutorial.md#part-3-deployment-30-minutes)
2. Review [Deployment Checklist](./genkit_quick_reference.md#deployment-checklist)
3. Set up [Monitoring](./genkit_integration_guide.md#monitoring--analytics)
4. Review [Security Best Practices](./genkit_integration_guide.md#security-best-practices)

#### "I need to optimize performance"
1. Review [Performance Targets](./genkit_quick_reference.md#performance-targets)
2. Implement [Caching Strategy](./genkit_integration_guide.md#3-caching-strategy)
3. Use [Request Batching](./genkit_integration_guide.md#1-request-batching)
4. Check [Performance Optimization](../5.architecture/genkit_architecture.md#performance-optimization-strategies)

#### "I need to reduce costs"
1. Review [Cost Estimates](./genkit_quick_reference.md#cost-estimates-gemini-25-flash)
2. Implement [Cost Optimization](./genkit_integration_guide.md#cost-optimization-strategies)
3. Use [Smart Model Routing](../5.architecture/genkit_architecture.md#3-smart-model-routing)
4. Set up [Cost Alerts](./genkit_integration_guide.md#alerting-rules)

## Learning Path

### Beginner (0-2 hours)

1. **Read**: [Quick Reference](./genkit_quick_reference.md) (15 min)
   - Understand what Genkit is
   - See TFLite vs Genkit decision matrix
   - Review basic code snippets

2. **Follow**: [Implementation Tutorial](./genkit_implementation_tutorial.md) (2 hours)
   - Set up backend
   - Integrate with Flutter
   - Deploy to Cloud Run

3. **Test**: Run the example dialogue generation
   - Generate your first AI dialogue
   - See it working end-to-end

### Intermediate (2-8 hours)

1. **Study**: [Architecture Document](../5.architecture/genkit_architecture.md) (1 hour)
   - Understand component responsibilities
   - Review data flow examples
   - Learn scaling strategies

2. **Implement**: Integration patterns from [Integration Guide](./genkit_integration_guide.md) (4 hours)
   - Enhanced dialogue system
   - Battery-aware AI
   - Offline-first with sync

3. **Optimize**: Performance and caching (2 hours)
   - Multi-level caching
   - Request batching
   - Smart model routing

4. **Monitor**: Set up observability (1 hour)
   - Firebase Analytics
   - Cloud Monitoring
   - Error tracking

### Advanced (8+ hours)

1. **Implement**: Advanced features
   - Tool calling for game state access
   - RAG for story consistency
   - Multi-agent systems
   - Streaming responses

2. **Optimize**: Production readiness
   - Security hardening
   - Cost optimization
   - Performance tuning
   - Disaster recovery

3. **Scale**: Multi-region deployment
   - Global load balancing
   - Regional backends
   - Edge caching
   - Advanced monitoring

## Common Workflows

### Daily Development

```bash
# Start backend with Developer UI
cd unwritten-genkit-backend
genkit start -o -- python main.py

# Run Flutter app
cd app
flutter run

# View logs
tail -f backend.log
```

**Reference**: [Quick Reference](./genkit_quick_reference.md#quick-start-commands)

### Testing Changes

```bash
# Test backend endpoint
curl -X POST http://localhost:8080/dialogue -H "Content-Type: application/json" -d @test_payload.json

# Run Flutter tests
cd app
flutter test

# Run backend tests
cd unwritten-genkit-backend
pytest
```

**Reference**: [Testing](./genkit_integration_guide.md#testing)

### Deploying Updates

```bash
# Deploy backend
cd unwritten-genkit-backend
gcloud run deploy unwritten-ai-backend --source .

# Build Flutter app with new backend URL
cd app
flutter build apk --dart-define=GENKIT_BASE_URL=https://new-url.run.app
```

**Reference**: [Deployment](./genkit_implementation_tutorial.md#part-3-deployment-30-minutes)

## Key Concepts

### TFLite vs Genkit
- **TFLite**: On-device, fast (< 15ms), offline, fixed models
- **Genkit**: Cloud-based, creative, updateable, requires network

**When to use which**: [Decision Matrix](./genkit_quick_reference.md#decision-matrix-tflite-vs-genkit)

### Flows
Self-contained AI workflows with input validation, pre/post-processing, and error handling.

**Learn more**: [Flows Documentation](./genkit_integration_guide.md#2-flows-workflows)

### Tool Calling
Enable AI models to call external functions (fetch data, check game state, etc.)

**Learn more**: [Tool Calling](./genkit_integration_guide.md#3-tool-calling)

### RAG (Retrieval-Augmented Generation)
Enhance AI responses with retrieved context for consistency and accuracy.

**Learn more**: [RAG Documentation](./genkit_integration_guide.md#4-retrieval-augmented-generation-rag)

## FAQs

### Do I need to replace TFLite?

**No!** Genkit complements TFLite. Use both:
- TFLite: Fast personality/sentiment inference
- Genkit: Creative dialogue/narrative generation

See: [Hybrid Approach](./genkit_integration_guide.md#hybrid-approach-tflite--genkit)

### What are the costs?

For 1,000 users with 50 dialogues each per month: ~$3.50/month

With optimization: ~$1.50-2.00/month

See: [Cost Estimates](./genkit_quick_reference.md#cost-estimates-gemini-25-flash)

### How fast is it?

- TFLite inference: < 15ms
- Genkit dialogue: 800-1500ms (can be cached)
- Total user experience: < 2 seconds with good UX

See: [Performance Targets](./genkit_quick_reference.md#performance-targets)

### What about offline?

Genkit requires network, but we handle it:
- Aggressive caching for common dialogues
- Fallback to rule-based system
- Offline-first architecture

See: [Offline-First Pattern](./genkit_integration_guide.md#pattern-3-offline-first-with-sync)

### How do I handle errors?

Multi-layered fallback system:
1. Try Genkit (cloud)
2. Use cache
3. Use TFLite + rules
4. Use hardcoded fallbacks

See: [Error Handling](./genkit_quick_reference.md#error-handling-pattern)

### Is it secure?

Yes, with proper implementation:
- API key authentication
- Rate limiting
- Input validation
- No PII logging
- HTTPS encryption

See: [Security Best Practices](./genkit_integration_guide.md#security-best-practices)

## External Resources

### Official Genkit Documentation
- [Genkit Docs (Python)](https://genkit.dev/docs/?lang=python)
- [Developer Tools](https://genkit.dev/docs/devtools/?lang=python)
- [Models](https://genkit.dev/docs/models/?lang=python)
- [Flows](https://genkit.dev/docs/flows/?lang=python)
- [Tool Calling](https://genkit.dev/docs/tool-calling/?lang=python)
- [RAG](https://genkit.dev/docs/rag/?lang=python)
- [Google Generative AI](https://genkit.dev/docs/integrations/google-genai/?lang=python)
- [Cloud Run Deployment](https://genkit.dev/docs/deployment/cloud-run/?lang=python)
- [Client Integration](https://genkit.dev/docs/client/?lang=python)

### Google Cloud
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Google AI Studio](https://aistudio.google.com)
- [Gemini API](https://ai.google.dev/gemini-api)

### Community
- [Genkit GitHub](https://github.com/firebase/genkit)
- [Genkit Discord](https://discord.gg/qXt5zzQKpc)

## Related Project Documentation

### AI Documentation
- [AI Architecture](./ai_model_architecture.md)
- [TensorFlow Lite Integration](./tensorflow_lite_integration.md)
- [Adherence Assessment Report](./ADHERENCE_ASSESSMENT_REPORT.md)

### Architecture Documentation
- [Overall Architecture](../../app/docs/ARCHITECTURE.md)
- [Performance Optimization](../5.architecture/performance_optimization.md)
- [Clean Architecture](../../README.md)

### Implementation Guides
- [Card Interaction Guide](../../app/docs/CARD_INTERACTION_GUIDE.md)
- [Firebase Setup](../../app/FIREBASE_SETUP_GUIDE.md)
- [Phase 1 Status](../../app/PHASE1_STATUS.md)

## Contributing

When adding new Genkit documentation:

1. **Update this index** with links to new documents
2. **Follow naming conventions**: `genkit_*.md` for Genkit-specific docs
3. **Add to appropriate section**: Place in `docs/3.ai/` or `docs/5.architecture/`
4. **Cross-reference**: Link to related documentation
5. **Include examples**: Practical code examples and use cases

## Document Maintenance

| Document | Last Updated | Maintainer | Review Cycle |
|----------|--------------|------------|--------------|
| genkit_integration_guide.md | Oct 15, 2025 | AI Team | Quarterly |
| genkit_quick_reference.md | Oct 15, 2025 | AI Team | Monthly |
| genkit_implementation_tutorial.md | Oct 15, 2025 | AI Team | Quarterly |
| genkit_architecture.md | Oct 15, 2025 | Architecture Team | Quarterly |

## Version History

- **v1.0.0** (Oct 15, 2025): Initial Genkit documentation suite
  - Integration guide
  - Quick reference
  - Implementation tutorial
  - Architecture document

---

**Questions or feedback?** Open an issue or ask in the team channel.

**Document Version**: 1.0  
**Last Updated**: October 15, 2025  
**Maintainer**: Unwritten AI Team

