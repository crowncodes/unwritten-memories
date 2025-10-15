# PowerShell script to create game asset directories
# Run this when you're ready to add audio, effects, and AI models

Write-Host "Creating Unwritten game asset directories..." -ForegroundColor Green

# Create directories
$directories = @(
    "assets/images/backgrounds",
    "assets/images/effects",
    "assets/audio/sfx",
    "assets/audio/music",
    "assets/models"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    Write-Host "✓ Created $dir" -ForegroundColor Cyan
}

# Create placeholder README files
@"
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
"@ | Out-File -FilePath "assets/audio/README.md" -Encoding UTF8

@"
# AI Models

Place TensorFlow Lite models here:
- personality.tflite - Big 5 personality traits
- sentiment.tflite - Sentiment analysis

## Creating Models
See docs/3.ai/ for model training instructions
"@ | Out-File -FilePath "assets/models/README.md" -Encoding UTF8

@"
# Visual Effects

Place effect sprites and animations here:
- particle effects
- card glow effects
- transition effects
"@ | Out-File -FilePath "assets/images/effects/README.md" -Encoding UTF8

Write-Host "`n✅ Asset directories created successfully!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Add audio files to assets/audio/sfx/ and assets/audio/music/"
Write-Host "2. Add visual effects to assets/images/effects/"
Write-Host "3. Add AI models to assets/models/"
Write-Host "4. Update pubspec.yaml to include new directories"
Write-Host "`nSee INSTALLATION_INSTRUCTIONS.md for details."


