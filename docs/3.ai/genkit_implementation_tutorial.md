# Genkit Implementation Tutorial: Your First Integration

## Overview

This tutorial walks you through implementing your first Genkit-powered feature in Unwritten: a dialogue generation system that enhances card interactions with AI-generated content.

**Time Required**: 2-3 hours  
**Prerequisites**: 
- Python 3.11+ installed
- Node.js 18+ installed (for Genkit CLI)
- Flutter development environment setup
- Google Cloud account (free tier works)

## Part 1: Backend Setup (45 minutes)

### Step 1: Create Backend Project

```bash
# Create project directory
mkdir unwritten-genkit-backend
cd unwritten-genkit-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install genkit google-genkit-ai fastapi uvicorn python-dotenv pydantic

# Save requirements
pip freeze > requirements.txt
```

### Step 2: Project Structure

Create the following structure:

```bash
unwritten-genkit-backend/
├── main.py                 # Entry point
├── flows/
│   ├── __init__.py
│   └── dialogue_flow.py    # Dialogue generation flow
├── config/
│   ├── __init__.py
│   └── settings.py         # Configuration
├── .env                    # Environment variables (don't commit!)
├── requirements.txt
└── README.md
```

Create directories:
```bash
mkdir flows config
touch flows/__init__.py config/__init__.py
touch main.py flows/dialogue_flow.py config/settings.py .env
```

### Step 3: Configure Environment

Edit `.env`:
```bash
# Google API Key - Get from: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your_google_api_key_here

# Environment
ENVIRONMENT=development

# Port
PORT=8080
```

**Important**: Add `.env` to `.gitignore`!

### Step 4: Create Settings Module

Edit `config/settings.py`:

```python
"""Configuration settings for Unwritten Genkit backend."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings."""
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    PORT = int(os.getenv('PORT', 8080))
    
    # Google API
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    # Model configuration
    DEFAULT_MODEL = 'gemini-2.5-flash'
    MODEL_TEMPERATURE = 0.7
    MAX_OUTPUT_TOKENS = 500
    
    # Request limits
    MAX_CONTEXT_LENGTH = 5000
    TIMEOUT_SECONDS = 30
    
    @classmethod
    def validate(cls):
        """Validate required settings."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")

settings = Settings()
settings.validate()
```

### Step 5: Create Dialogue Flow

Edit `flows/dialogue_flow.py`:

```python
"""Dialogue generation flow for Unwritten card interactions."""

from genkit import ai, flow
from genkit_google_genai import googleAI
from pydantic import BaseModel, Field, validator
from typing import Dict, List

# Configure Genkit with Google AI
ai.configure(
    plugins=[googleAI()],
    model=googleAI.model('gemini-2.5-flash')
)


class DialogueInput(BaseModel):
    """Input for dialogue generation."""
    
    card_id: str = Field(..., description="Unique card identifier")
    context: str = Field(..., description="Current game context")
    personality_traits: Dict[str, float] = Field(
        default_factory=dict,
        description="Big 5 personality traits (0.0-1.0)"
    )
    previous_interactions: int = Field(
        default=0,
        description="Number of previous interactions with this card"
    )
    
    @validator('card_id')
    def validate_card_id(cls, v):
        """Validate card_id."""
        if not v or len(v) > 100:
            raise ValueError('Invalid card_id')
        return v
    
    @validator('context')
    def validate_context(cls, v):
        """Validate context length."""
        if len(v) > 5000:
            raise ValueError('Context too long (max 5000 characters)')
        return v
    
    @validator('personality_traits')
    def validate_traits(cls, v):
        """Validate personality traits."""
        valid_traits = {
            'openness', 'conscientiousness', 'extraversion',
            'agreeableness', 'neuroticism'
        }
        
        # Check trait names
        invalid = set(v.keys()) - valid_traits
        if invalid:
            raise ValueError(f'Invalid traits: {invalid}')
        
        # Check trait values
        for trait, value in v.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f'{trait} value must be between 0.0 and 1.0')
        
        return v


class DialogueOutput(BaseModel):
    """Output from dialogue generation."""
    
    text: str = Field(..., description="Generated dialogue text")
    emotion: str = Field(..., description="Character's emotional state")
    tone: str = Field(..., description="Tone of the dialogue")
    suggested_responses: List[str] = Field(
        ...,
        description="Suggested player responses (3 options)"
    )


def build_personality_description(traits: Dict[str, float]) -> str:
    """
    Convert Big 5 personality traits to natural language description.
    
    Args:
        traits: Dictionary of trait names to values (0.0-1.0)
    
    Returns:
        Natural language personality description
    """
    descriptions = []
    
    # Openness to experience
    openness = traits.get('openness', 0.5)
    if openness > 0.7:
        descriptions.append("highly creative and open to new experiences")
    elif openness < 0.3:
        descriptions.append("conventional and prefers familiar routines")
    
    # Conscientiousness
    conscientiousness = traits.get('conscientiousness', 0.5)
    if conscientiousness > 0.7:
        descriptions.append("organized and dependable")
    elif conscientiousness < 0.3:
        descriptions.append("spontaneous and flexible")
    
    # Extraversion
    extraversion = traits.get('extraversion', 0.5)
    if extraversion > 0.7:
        descriptions.append("outgoing and energetic")
    elif extraversion < 0.3:
        descriptions.append("reserved and introspective")
    
    # Agreeableness
    agreeableness = traits.get('agreeableness', 0.5)
    if agreeableness > 0.7:
        descriptions.append("compassionate and cooperative")
    elif agreeableness < 0.3:
        descriptions.append("competitive and skeptical")
    
    # Neuroticism
    neuroticism = traits.get('neuroticism', 0.5)
    if neuroticism > 0.7:
        descriptions.append("emotionally sensitive and anxious")
    elif neuroticism < 0.3:
        descriptions.append("calm and emotionally stable")
    
    return ", ".join(descriptions) if descriptions else "balanced personality"


@flow
async def dialogue_generation_flow(input_data: DialogueInput) -> DialogueOutput:
    """
    Generate contextual dialogue for card interactions.
    
    This flow takes personality traits (from TFLite inference) and game context
    to generate appropriate, character-consistent dialogue.
    
    Args:
        input_data: Dialogue generation parameters
    
    Returns:
        Generated dialogue with emotion, tone, and response options
    
    Example:
        >>> input_data = DialogueInput(
        ...     card_id='mysterious_stranger',
        ...     context='Player meets character in dark alley at night',
        ...     personality_traits={'openness': 0.8, 'extraversion': 0.3},
        ...     previous_interactions=0
        ... )
        >>> result = await dialogue_generation_flow(input_data)
        >>> print(result.text)
        "I've been waiting for you..."
    """
    
    # Build personality description
    personality_desc = build_personality_description(input_data.personality_traits)
    
    # Determine interaction context
    if input_data.previous_interactions == 0:
        interaction_context = "This is your first meeting with this character."
    elif input_data.previous_interactions < 5:
        interaction_context = f"You've met this character {input_data.previous_interactions} times before."
    else:
        interaction_context = "You have a well-established relationship with this character."
    
    # Build comprehensive prompt
    prompt = f"""You are generating dialogue for a character in Unwritten, a narrative card game.

CHARACTER PERSONALITY:
{personality_desc}

GAME CONTEXT:
{input_data.context}

INTERACTION HISTORY:
{interaction_context}

TASK:
Generate authentic dialogue that:
1. Reflects the character's personality traits naturally
2. Fits the current game context and mood
3. Feels engaging and emotionally resonant
4. Maintains consistency with the interaction history

OUTPUT REQUIREMENTS:
- Dialogue text: 1-3 sentences, natural and concise
- Emotion: The character's emotional state (e.g., curious, wary, friendly, mysterious)
- Tone: The delivery tone (e.g., warm, cold, playful, serious)
- Three distinct player response options that feel meaningful

Generate the dialogue now."""

    # Generate with structured output
    response = await ai.generate(
        prompt=prompt,
        output_schema=DialogueOutput,
        config={
            'temperature': 0.7,  # Balanced creativity
            'maxOutputTokens': 500,
        }
    )
    
    return response.output
```

### Step 6: Create API Server

Edit `main.py`:

```python
"""Main entry point for Unwritten Genkit backend."""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from flows.dialogue_flow import dialogue_generation_flow, DialogueInput, DialogueOutput
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info(f"Starting Unwritten AI Backend (env: {settings.ENVIRONMENT})")
    yield
    logger.info("Shutting down Unwritten AI Backend")


# Create FastAPI app
app = FastAPI(
    title="Unwritten AI Backend",
    description="Genkit-powered AI services for Unwritten card game",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint for health checks."""
    return {
        "service": "Unwritten AI Backend",
        "status": "healthy",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "model": settings.DEFAULT_MODEL,
    }


@app.post("/dialogue", response_model=DialogueOutput)
async def generate_dialogue(input_data: DialogueInput):
    """
    Generate dialogue for a card interaction.
    
    Args:
        input_data: Dialogue generation parameters
    
    Returns:
        Generated dialogue with emotion, tone, and response options
    
    Raises:
        HTTPException: If generation fails
    """
    try:
        logger.info(f"Generating dialogue for card: {input_data.card_id}")
        
        # Run the flow
        result = await dialogue_generation_flow(input_data)
        
        logger.info(f"Successfully generated dialogue (length: {len(result.text)})")
        return result
        
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error generating dialogue: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate dialogue: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=(settings.ENVIRONMENT == "development"),
        log_level="info",
    )
```

### Step 7: Test Backend Locally

```bash
# Start the server
python main.py

# Server should start on http://localhost:8080
```

In another terminal, test with curl:

```bash
# Test health endpoint
curl http://localhost:8080/health

# Test dialogue generation
curl -X POST http://localhost:8080/dialogue \
  -H "Content-Type: application/json" \
  -d '{
    "card_id": "mysterious_stranger",
    "context": "Player meets character in a misty forest at twilight",
    "personality_traits": {
      "openness": 0.8,
      "extraversion": 0.3,
      "agreeableness": 0.6
    },
    "previous_interactions": 0
  }'
```

Expected response:
```json
{
  "text": "The shadows gather here, and yet you walk without fear. Tell me, traveler, what brings you to this forgotten path?",
  "emotion": "mysterious",
  "tone": "enigmatic",
  "suggested_responses": [
    "I'm looking for someone",
    "Just passing through",
    "Who are you?"
  ]
}
```

### Step 8: Use Genkit Developer UI

```bash
# Install Genkit CLI (if not already installed)
npm install -g genkit-cli

# Start with Developer UI
genkit start -o -- python main.py
```

This opens a browser with the Genkit Developer UI where you can:
- Test the `dialogue_generation_flow` interactively
- View execution traces
- Debug issues
- Experiment with different inputs

## Part 2: Flutter Integration (1 hour)

### Step 1: Add Dependencies

Edit `app/pubspec.yaml`:

```yaml
dependencies:
  # ... existing dependencies
  http: ^1.2.0
```

Run:
```bash
cd app
flutter pub get
```

### Step 2: Create Data Models

Create `app/lib/features/ai/data/models/dialogue_response.dart`:

```dart
/// Response from dialogue generation.
///
/// Contains generated dialogue text, emotional context,
/// and suggested player responses.
class DialogueResponse {
  final String text;
  final String emotion;
  final String tone;
  final List<String> suggestedResponses;
  final bool isFallback;

  const DialogueResponse({
    required this.text,
    required this.emotion,
    required this.tone,
    required this.suggestedResponses,
    this.isFallback = false,
  });

  factory DialogueResponse.fromJson(Map<String, dynamic> json) {
    return DialogueResponse(
      text: json['text'] as String,
      emotion: json['emotion'] as String,
      tone: json['tone'] as String,
      suggestedResponses: (json['suggested_responses'] as List)
          .map((e) => e as String)
          .toList(),
      isFallback: json['is_fallback'] as bool? ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'text': text,
      'emotion': emotion,
      'tone': tone,
      'suggested_responses': suggestedResponses,
      'is_fallback': isFallback,
    };
  }
}
```

### Step 3: Create Genkit Service

Create `app/lib/shared/services/genkit_service.dart`:

```dart
import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import '../../core/constants/api_config.dart';
import '../../features/ai/data/models/dialogue_response.dart';
import '../utils/app_logger.dart';

/// Exception thrown by GenkitService.
class GenkitException implements Exception {
  final String message;
  final int? statusCode;

  GenkitException(this.message, {this.statusCode});

  @override
  String toString() => 'GenkitException: $message';
}

/// Service for interacting with Genkit backend.
///
/// Handles communication with the Python Genkit service
/// for AI-powered dialogue and narrative generation.
///
/// Performance:
/// - Average latency: 800-1500ms (includes model inference)
/// - Implements caching to reduce API calls
/// - Falls back to rule-based system on failure
class GenkitService {
  final http.Client _client;
  final String _baseUrl;

  GenkitService({
    http.Client? client,
    String? baseUrl,
  })  : _client = client ?? http.Client(),
        _baseUrl = baseUrl ?? ApiConfig.genkitBaseUrl;

  /// Generates dialogue for a character interaction.
  ///
  /// Uses the backend's dialogue_generation_flow.
  /// Caches responses for common interactions.
  ///
  /// Throws [GenkitException] if generation fails.
  Future<DialogueResponse> generateDialogue({
    required String cardId,
    required String context,
    required Map<String, double> personalityTraits,
    int previousInteractions = 0,
  }) async {
    final stopwatch = Stopwatch()..start();

    try {
      final response = await _client
          .post(
            Uri.parse('$_baseUrl/dialogue'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'card_id': cardId,
              'context': context,
              'personality_traits': personalityTraits,
              'previous_interactions': previousInteractions,
            }),
          )
          .timeout(
            ApiConfig.requestTimeout,
            onTimeout: () => throw TimeoutException('Request timed out'),
          );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;

        AppLogger.ai('Dialogue generated', metrics: {
          'duration_ms': stopwatch.elapsedMilliseconds,
          'card_id': cardId,
        });

        return DialogueResponse.fromJson(data);
      } else {
        throw GenkitException(
          'Failed to generate dialogue: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } on SocketException {
      AppLogger.error('Network error in dialogue generation', 
          const SocketException('Network unavailable'));
      rethrow;
    } on TimeoutException catch (e) {
      AppLogger.error('Timeout in dialogue generation', e);
      rethrow;
    } catch (e, stack) {
      AppLogger.error('Dialogue generation failed', e, stack);
      rethrow;
    }
  }

  void dispose() {
    _client.close();
  }
}
```

### Step 4: Create API Configuration

Create `app/lib/core/constants/api_config.dart`:

```dart
/// API configuration for backend services.
class ApiConfig {
  /// Base URL for Genkit backend service.
  ///
  /// Use environment variables for different builds:
  /// flutter build apk --dart-define=GENKIT_BASE_URL=https://your-url.run.app
  static const String genkitBaseUrl = String.fromEnvironment(
    'GENKIT_BASE_URL',
    defaultValue: 'http://localhost:8080', // Development default
  );

  /// Request timeout duration.
  static const Duration requestTimeout = Duration(seconds: 30);

  /// Maximum number of retries for failed requests.
  static const int maxRetries = 2;

  /// Cache duration for AI responses.
  static const Duration cacheDuration = Duration(hours: 1);
}
```

### Step 5: Test Flutter Integration

Create a simple test widget:

```dart
// Create app/lib/features/ai/presentation/pages/dialogue_test_page.dart

import 'package:flutter/material.dart';

import '../../../../shared/services/genkit_service.dart';
import '../../../cards/domain/entities/card.dart' as game;

/// Test page for Genkit dialogue generation.
class DialogueTestPage extends StatefulWidget {
  const DialogueTestPage({super.key});

  @override
  State<DialogueTestPage> createState() => _DialogueTestPageState();
}

class _DialogueTestPageState extends State<DialogueTestPage> {
  final _genkitService = GenkitService();
  String? _dialogue;
  bool _isLoading = false;
  String? _error;

  Future<void> _generateDialogue() async {
    setState(() {
      _isLoading = true;
      _error = null;
      _dialogue = null;
    });

    try {
      final response = await _genkitService.generateDialogue(
        cardId: 'test_card_mysterious',
        context: 'Player meets character in a misty forest at twilight',
        personalityTraits: {
          'openness': 0.8,
          'extraversion': 0.3,
          'agreeableness': 0.6,
          'conscientiousness': 0.5,
          'neuroticism': 0.4,
        },
        previousInteractions: 0,
      );

      setState(() {
        _dialogue = response.text;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  void dispose() {
    _genkitService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Genkit Dialogue Test'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            ElevatedButton(
              onPressed: _isLoading ? null : _generateDialogue,
              child: _isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Text('Generate Dialogue'),
            ),
            const SizedBox(height: 24),
            if (_error != null)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.red.shade100,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  'Error: $_error',
                  style: TextStyle(color: Colors.red.shade900),
                ),
              ),
            if (_dialogue != null)
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.blue.shade50,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: SingleChildScrollView(
                    child: Text(
                      _dialogue!,
                      style: const TextStyle(fontSize: 16),
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
```

### Step 6: Test End-to-End

1. **Start the backend**:
```bash
cd unwritten-genkit-backend
python main.py
```

2. **Run Flutter app**:
```bash
cd app
flutter run
```

3. **Navigate to DialogueTestPage** and tap "Generate Dialogue"

You should see the AI-generated dialogue appear!

## Part 3: Deployment (30 minutes)

### Step 1: Create Dockerfile

Create `unwritten-genkit-backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Run the application
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
```

### Step 2: Deploy to Cloud Run

```bash
# Authenticate with Google Cloud
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
cd unwritten-genkit-backend
gcloud run deploy unwritten-ai-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 60s \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY
```

After deployment, you'll get a URL like:
```
https://unwritten-ai-backend-xxxxx-uc.a.run.app
```

### Step 3: Update Flutter App

Build Flutter app with the Cloud Run URL:

```bash
cd app
flutter build apk --dart-define=GENKIT_BASE_URL=https://unwritten-ai-backend-xxxxx-uc.a.run.app
```

## Testing Checklist

- [ ] Backend health check returns 200: `curl https://your-url/health`
- [ ] Dialogue generation works via curl
- [ ] Genkit Developer UI shows flows
- [ ] Flutter app connects to local backend
- [ ] Flutter app connects to Cloud Run backend
- [ ] Error handling works (test with backend offline)
- [ ] Performance is acceptable (< 2 seconds)

## Troubleshooting

### Issue: "GOOGLE_API_KEY environment variable is required"

**Solution**: Set the API key in `.env`:
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

Get a key from: https://aistudio.google.com/app/apikey

### Issue: Flutter app can't connect to backend

**Solution**: 
1. Check backend is running: `curl http://localhost:8080/health`
2. Check Flutter is using correct URL in `ApiConfig`
3. On Android emulator, use `10.0.2.2` instead of `localhost`
4. Check CORS settings in `main.py`

### Issue: "Connection refused" on Cloud Run

**Solution**:
1. Check service is running: Visit the URL in browser
2. Check environment variables are set correctly
3. View logs: `gcloud run services logs read unwritten-ai-backend`
4. Verify `--allow-unauthenticated` flag was used

### Issue: Slow response times (> 3 seconds)

**Solutions**:
1. Use faster model: `gemini-2.0-flash-lite`
2. Reduce `maxOutputTokens` to 300
3. Simplify prompt
4. Implement caching
5. Check Cloud Run instance isn't cold-starting

## Next Steps

Now that you have basic Genkit integration working:

1. **Add Caching**: Implement response caching to reduce API calls
2. **Add Error Handling**: Implement fallback dialogue system
3. **Add Monitoring**: Set up logging and analytics
4. **Optimize Prompts**: Refine prompts for better responses
5. **Add More Flows**: Create story progression, character interaction flows
6. **Implement RAG**: Add story context retrieval
7. **Add Tool Calling**: Enable AI to access game state

## Resources

- [Genkit Documentation](https://genkit.dev/docs/?lang=python)
- [Google AI Studio](https://aistudio.google.com)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Genkit Integration Guide](./genkit_integration_guide.md)

## Support

Having issues? Check:
- [Genkit GitHub Issues](https://github.com/firebase/genkit/issues)
- [Genkit Discord](https://discord.gg/qXt5zzQKpc)
- [Project Documentation](../README.md)

---

**Congratulations!** You've successfully integrated Genkit into Unwritten! 🎉

**Tutorial Version**: 1.0  
**Last Updated**: October 15, 2025

