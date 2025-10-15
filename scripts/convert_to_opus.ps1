# Convert music stems to Opus format for Unwritten
# Usage: ./convert_to_opus.ps1 -InputDir "./raw_stems" -OutputDir "../app/assets/music/cues"

param(
    [string]$InputDir = ".",
    [string]$OutputDir = "../app/assets/music/cues"
)

# Check if FFmpeg is installed
try {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Host "✓ FFmpeg found: $ffmpegVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ FFmpeg not found. Please install FFmpeg first:" -ForegroundColor Red
    Write-Host "  choco install ffmpeg" -ForegroundColor Yellow
    Write-Host "  or download from: https://ffmpeg.org/download.html" -ForegroundColor Yellow
    exit 1
}

# Function to convert a single file
function Convert-ToOpus {
    param(
        [string]$InputFile,
        [string]$OutputFile
    )
    
    if (!(Test-Path $InputFile)) {
        Write-Host "  ⚠ Skipping $InputFile (not found)" -ForegroundColor Yellow
        return $false
    }
    
    Write-Host "  Converting: $(Split-Path $InputFile -Leaf) → $(Split-Path $OutputFile -Leaf)"
    
    $result = ffmpeg -i $InputFile `
        -c:a libopus `
        -b:a 96k `
        -vn `
        -y `
        $OutputFile 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        $size = (Get-Item $OutputFile).Length / 1KB
        Write-Host "    ✓ Success ($('{0:N0}' -f $size) KB)" -ForegroundColor Green
        return $true
    } else {
        Write-Host "    ✗ Failed: $result" -ForegroundColor Red
        return $false
    }
}

# Convert Calm Positive stems
Write-Host "`n=== Converting calm_positive stems ===" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "$OutputDir/calm_positive" | Out-Null

$calmSuccess = 0
$calmSuccess += [int](Convert-ToOpus "$InputDir/calm_positive_pad_raw.wav" "$OutputDir/calm_positive/pad.opus")
$calmSuccess += [int](Convert-ToOpus "$InputDir/calm_positive_piano_raw.wav" "$OutputDir/calm_positive/piano.opus")
$calmSuccess += [int](Convert-ToOpus "$InputDir/calm_positive_brush_raw.wav" "$OutputDir/calm_positive/brush.opus")

Write-Host "Calm Positive: $calmSuccess/3 stems converted" -ForegroundColor $(if ($calmSuccess -eq 3) { "Green" } else { "Yellow" })

# Convert Melancholic Private stems
Write-Host "`n=== Converting melancholic_private stems ===" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "$OutputDir/melancholic_private" | Out-Null

$melSuccess = 0
$melSuccess += [int](Convert-ToOpus "$InputDir/melancholic_pad_raw.wav" "$OutputDir/melancholic_private/pad.opus")
$melSuccess += [int](Convert-ToOpus "$InputDir/melancholic_piano_raw.wav" "$OutputDir/melancholic_private/piano.opus")
$melSuccess += [int](Convert-ToOpus "$InputDir/melancholic_shaker_raw.wav" "$OutputDir/melancholic_private/shaker.opus")

Write-Host "Melancholic Private: $melSuccess/3 stems converted" -ForegroundColor $(if ($melSuccess -eq 3) { "Green" } else { "Yellow" })

# Convert Motivated stems (optional)
Write-Host "`n=== Converting motivated stems (optional) ===" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "$OutputDir/motivated" | Out-Null

$motSuccess = 0
$motSuccess += [int](Convert-ToOpus "$InputDir/motivated_pad_raw.wav" "$OutputDir/motivated/pad.opus")
$motSuccess += [int](Convert-ToOpus "$InputDir/motivated_piano_raw.wav" "$OutputDir/motivated/piano.opus")
$motSuccess += [int](Convert-ToOpus "$InputDir/motivated_percussion_raw.wav" "$OutputDir/motivated/percussion.opus")
$motSuccess += [int](Convert-ToOpus "$InputDir/motivated_strings_raw.wav" "$OutputDir/motivated/strings.opus")

if ($motSuccess -gt 0) {
    Write-Host "Motivated: $motSuccess/4 stems converted" -ForegroundColor $(if ($motSuccess -eq 4) { "Green" } else { "Yellow" })
}

# Summary
Write-Host "`n=== Conversion Summary ===" -ForegroundColor Cyan
Write-Host "Total stems converted: $($calmSuccess + $melSuccess + $motSuccess)"
Write-Host "Output directory: $OutputDir"

# Validate durations
Write-Host "`n=== Validating Durations ===" -ForegroundColor Cyan

function Test-Duration {
    param(
        [string]$File,
        [double]$ExpectedSeconds,
        [double]$Tolerance = 0.1
    )
    
    if (!(Test-Path $File)) {
        return
    }
    
    $duration = ffprobe -i $File -show_entries format=duration -v quiet -of csv="p=0" 2>&1
    $duration = [double]$duration
    
    $diff = [Math]::Abs($duration - $ExpectedSeconds)
    $status = if ($diff -le $Tolerance) { "✓" } else { "✗" }
    $color = if ($diff -le $Tolerance) { "Green" } else { "Red" }
    
    Write-Host "  $status $(Split-Path $File -Leaf): $($duration)s (expected: $($ExpectedSeconds)s)" -ForegroundColor $color
}

if ($calmSuccess -gt 0) {
    Write-Host "Calm Positive (72 BPM, 8 bars = 26.667s):"
    Test-Duration "$OutputDir/calm_positive/pad.opus" 26.667
    Test-Duration "$OutputDir/calm_positive/piano.opus" 26.667
    Test-Duration "$OutputDir/calm_positive/brush.opus" 26.667
}

if ($melSuccess -gt 0) {
    Write-Host "`nMelancholic Private (60 BPM, 8 bars = 32.000s):"
    Test-Duration "$OutputDir/melancholic_private/pad.opus" 32.000
    Test-Duration "$OutputDir/melancholic_private/piano.opus" 32.000
    Test-Duration "$OutputDir/melancholic_private/shaker.opus" 32.000
}

if ($motSuccess -gt 0) {
    Write-Host "`nMotivated (80 BPM, 8 bars = 24.000s):"
    Test-Duration "$OutputDir/motivated/pad.opus" 24.000
    Test-Duration "$OutputDir/motivated/piano.opus" 24.000
    Test-Duration "$OutputDir/motivated/percussion.opus" 24.000
    Test-Duration "$OutputDir/motivated/strings.opus" 24.000
}

Write-Host "`n✓ Conversion complete!" -ForegroundColor Green
Write-Host "Next: Run 'flutter run' to test in app" -ForegroundColor Cyan

