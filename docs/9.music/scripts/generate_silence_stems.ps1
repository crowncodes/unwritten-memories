# Generate silent placeholder stems for testing architecture
# Usage: ./generate_silence_stems.ps1

param(
    [string]$OutputDir = "../../../app/assets/music/stems"
)

Write-Host "=== Generating Silent Test Stems ===" -ForegroundColor Cyan
Write-Host "This creates placeholder files to test the music engine architecture." -ForegroundColor Yellow
Write-Host ""

# Check if FFmpeg is installed
try {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Host "[OK] FFmpeg found" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] FFmpeg not found. Install with: choco install ffmpeg" -ForegroundColor Red
    exit 1
}

# Function to generate silence
function New-SilentStem {
    param(
        [string]$OutputFile,
        [double]$DurationSeconds
    )
    
    $dir = Split-Path $OutputFile -Parent
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    
    $fileName = Split-Path $OutputFile -Leaf
    Write-Host "  Creating: $fileName ($DurationSeconds seconds)"
    
    ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo `
        -t $DurationSeconds `
        -c:a libopus -b:a 96k `
        -y `
        $OutputFile 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        $size = (Get-Item $OutputFile).Length / 1KB
        $sizeFormatted = '{0:N0}' -f $size
        Write-Host "    [OK] Created ($sizeFormatted KB)" -ForegroundColor Green
        return $true
    } else {
        Write-Host "    [FAIL] Failed" -ForegroundColor Red
        return $false
    }
}

# Generate Calm Positive stems (72 BPM, 8 bars = 26.667s)
Write-Host "`nCalm Positive (72 BPM, 8 bars):" -ForegroundColor Cyan
New-SilentStem "$OutputDir/calm_positive/pad.opus" 26.667
New-SilentStem "$OutputDir/calm_positive/piano.opus" 26.667
New-SilentStem "$OutputDir/calm_positive/brush.opus" 26.667

# Generate Melancholic Private stems (60 BPM, 8 bars = 32.000s)
Write-Host "`nMelancholic Private (60 BPM, 8 bars):" -ForegroundColor Cyan
New-SilentStem "$OutputDir/melancholic_private/pad.opus" 32.000
New-SilentStem "$OutputDir/melancholic_private/piano.opus" 32.000
New-SilentStem "$OutputDir/melancholic_private/shaker.opus" 32.000

Write-Host "`n[SUCCESS] Silent test stems generated!" -ForegroundColor Green
Write-Host ""
Write-Host "These files allow you to test:" -ForegroundColor Cyan
Write-Host "  - Cue loading and selection" -ForegroundColor White
Write-Host "  - Bar-quantized transitions" -ForegroundColor White
Write-Host "  - Stem mixing and crossfades" -ForegroundColor White
Write-Host "  - Game state integration" -ForegroundColor White
Write-Host ""
Write-Host "To test: cd app; flutter run" -ForegroundColor Yellow
Write-Host "To replace with real music: Use Lyria API or DAW" -ForegroundColor Yellow

