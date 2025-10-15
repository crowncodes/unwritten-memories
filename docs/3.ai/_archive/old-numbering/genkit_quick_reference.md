# Genkit Quick Reference for Unwritten

## Quick Start Commands

```bash
# Install Genkit CLI
npm install -g genkit-cli

# Install Python SDK
pip install genkit google-genkit-ai

# Start Developer UI
genkit start -o -- python3 main.py

# Run a flow
genkit flow:run dialogue_generation_flow

# Deploy to Cloud Run
gcloud run deploy unwritten-ai-backend --source .
```

## Common Code Snippets

### Basic AI Generation

```python
from genkit import ai
from genkit_google_genai import googleAI

# Configure
ai.configure(
    plugins=[googleAI()],
    model=googleAI.model('gemini-2.5-flash')
)

# Generate
response = await ai.generate("Your prompt here")
```

### Define a Flow

```python
from genkit import flow
from pydantic import BaseModel

class MyInput(BaseModel):
    text: str

class MyOutput(BaseModel):
    result: str

@flow
async def my_flow(input: MyInput) -> MyOutput:
    response = await ai.generate(input.text)
    return MyOutput(result=response.text)
```

### Define a Tool

```python
from genkit import tool

@tool
async def fetch_data(id: str) -> dict:
    """Tool description for AI."""
    return {'data': 'value'}

# Use in flow
@flow
async def tool_flow(input: MyInput) -> MyOutput:
    response = await ai.generate(
        prompt=input.text,
        tools=[fetch_data]
    )
    return MyOutput(result=response.text)
```

### Flutter HTTP Request

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<DialogueResponse> generateDialogue() async {
  final response = await http.post(
    Uri.parse('https://your-backend-url/dialogue'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'cardId': 'card_1',
      'context': 'Meeting for first time',
      'personalityTraits': {'extraversion': 0.8},
    }),
  );
  
  if (response.statusCode == 200) {
    return DialogueResponse.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to generate dialogue');
  }
}
```

## Decision Matrix: TFLite vs Genkit

| Requirement | Use TFLite | Use Genkit |
|-------------|-----------|------------|
| **Speed** (< 20ms) | ✅ | ❌ |
| **Offline** capability | ✅ | ❌ |
| **Creative text** generation | ❌ | ✅ |
| **Model updates** (no app update) | ❌ | ✅ |
| **Fixed inference** (personality) | ✅ | ❌ |
| **Long narratives** | ❌ | ✅ |
| **Battery** efficiency | ✅ | ⚠️ |
| **Privacy** (no data sent) | ✅ | ❌ |

## Recommended Architecture

```
┌─────────────────────────────────────────┐
│           Flutter App                   │
│                                         │
│  Fast Operations (< 20ms):              │
│  ✓ Personality inference → TFLite      │
│  ✓ Sentiment analysis → TFLite         │
│  ✓ Relationship scoring → TFLite       │
│                                         │
│  Creative Operations (800-1500ms):      │
│  ✓ Dialogue generation → Genkit        │
│  ✓ Story narration → Genkit            │
│  ✓ Dynamic events → Genkit             │
└─────────────────────────────────────────┘
```

## Performance Targets

| Operation | Target | Implementation |
|-----------|--------|---------------|
| Personality inference | < 15ms | TFLite (on-device) |
| Sentiment analysis | < 10ms | TFLite (on-device) |
| Simple dialogue | < 100ms | Cache + fallback |
| Rich dialogue | < 1500ms | Genkit + cache |
| Story generation | < 2000ms | Genkit with streaming |
| Total battery impact | < 10%/30min | Hybrid approach |

## Cost Estimates (Gemini 2.5 Flash)

| Scenario | Monthly Users | Dialogues/User | Cost |
|----------|--------------|----------------|------|
| Small | 100 | 50 | $0.35 |
| Medium | 1,000 | 50 | $3.50 |
| Large | 10,000 | 50 | $35.00 |
| Very Large | 100,000 | 50 | $350.00 |

**Cost Optimization**:
- Cache aggressively: 50-70% reduction
- Use batch requests: 30% reduction
- Smart model routing: 20% reduction
- **Combined savings**: up to 80%

## Error Handling Pattern

```dart
Future<DialogueResponse> generateDialogue() async {
  try {
    // Try Genkit
    return await _genkitService.generateDialogue(...);
  } on SocketException {
    // No network: use cache or fallback
    return await _getCachedOrFallback();
  } on TimeoutException {
    // Timeout: use simpler model or fallback
    return await _generateSimpleDialogue();
  } catch (e) {
    // Other errors: log and use fallback
    AppLogger.error('Dialogue generation failed', e);
    return _getRuleBasedDialogue();
  }
}
```

## Caching Strategy

```dart
// 3-tier caching
class AICache {
  // Tier 1: Memory (fastest, ~100 items)
  final LRUCache<String, Response> _memory = LRUCache(maxSize: 100);
  
  // Tier 2: Disk (persistent, ~1000 items)
  final HiveCache _disk;
  
  // Tier 3: Network (Genkit backend)
  final GenkitService _service;
  
  Future<Response> get(String key) async {
    return _memory.get(key) ??
           await _disk.get(key) ??
           await _service.generate(key);
  }
}
```

## Monitoring Checklist

- [ ] Track API call count (daily)
- [ ] Monitor response latency (p50, p95, p99)
- [ ] Measure cache hit rate (target: > 60%)
- [ ] Track error rate (target: < 1%)
- [ ] Monitor costs (set alerts)
- [ ] Measure battery impact (< 10%/30min)
- [ ] Track user satisfaction (dialogue ratings)

## Deployment Checklist

- [ ] Environment variables configured
- [ ] API keys secured (not in code)
- [ ] Cloud Run deployed and tested
- [ ] HTTPS enforced
- [ ] Rate limiting configured
- [ ] Monitoring/logging enabled
- [ ] Error handling implemented
- [ ] Fallback system tested
- [ ] Caching strategy in place
- [ ] Cost alerts configured

## Useful Links

- **Genkit Docs**: https://genkit.dev/docs/?lang=python
- **Developer UI**: http://localhost:4000 (when running)
- **Cloud Run Console**: https://console.cloud.google.com/run
- **Google AI Studio**: https://aistudio.google.com
- **Gemini API**: https://ai.google.dev/gemini-api

## Support

For Genkit-related issues:
1. Check [Genkit documentation](https://genkit.dev/docs/?lang=python)
2. Search [GitHub issues](https://github.com/firebase/genkit)
3. Ask on [Discord](https://discord.gg/qXt5zzQKpc)

For Unwritten-specific integration:
1. See [Genkit Integration Guide](./genkit_integration_guide.md)
2. Check [AI Architecture](../5.architecture/ai_architecture.md)
3. Review [TFLite Integration](./tensorflow_lite_integration.md)

---

**Last Updated**: October 15, 2025

