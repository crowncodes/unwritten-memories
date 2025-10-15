#!/bin/bash
# Bash script to create game asset directories
# Run this when you're ready to add audio, effects, and AI models

echo "Creating Unwritten game asset directories..."

# Create directories
mkdir -p assets/images/backgrounds
mkdir -p assets/images/effects
mkdir -p assets/audio/sfx
mkdir -p assets/audio/music
mkdir -p assets/models

echo "✓ Created asset directories"

# Create placeholder README files
cat > assets/audio/README.md << 'EOF'
# Audio Assets

## Sound Effects (SFX)
Place sound effect files here:
- card_hover.mp3
- card_grab.mp3
- card_play.mp3
- card_shuffle.mp3
- card_draw.mp3

## Free Resources
- Freesound.org - Free SFX
- OpenGameArt.org - Game sounds
- Mixkit.co - Game sound effects
EOF

cat > assets/models/README.md << 'EOF'
# AI Models

Place TensorFlow Lite models here:
- personality.tflite - Big 5 personality traits
- sentiment.tflite - Sentiment analysis

## Creating Models
See docs/3.ai/ for model training instructions
EOF

cat > assets/images/effects/README.md << 'EOF'
# Visual Effects

Place effect sprites and animations here:
- particle effects
- card glow effects
- transition effects
EOF

echo "✅ Asset directories created successfully!"
echo ""
echo "Next steps:"
echo "1. Add audio files to assets/audio/sfx/ and assets/audio/music/"
echo "2. Add visual effects to assets/images/effects/"
echo "3. Add AI models to assets/models/"
echo "4. Update pubspec.yaml to include new directories"
echo ""
echo "See INSTALLATION_INSTRUCTIONS.md for details."


