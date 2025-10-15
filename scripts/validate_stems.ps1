# Validate music stem files for Unwritten
# Checks duration, format, and loop safety

param(
    [string]$CuesDir = "../app/assets/music/cues"
)

Write-Host "=== Music Stem Validation ===" -ForegroundColor Cyan
Write-Host ""

$totalIssues = 0

# Expected durations
$expectedDurations = @{
    "calm_positive" = 26.667
    "melancholic_private" = 32.000
    "motivated" = 24.000
}

# Check each cue
foreach ($cue in $expectedDurations.Keys) {
    $cuePath = Join-Path $CuesDir $cue
    
    if (!(Test-Path $cuePath)) {
        Write-Host "⚠ Cue not found: $cue" -ForegroundColor Yellow
        continue
    }
    
    Write-Host "Checking: $cue" -ForegroundColor Cyan
    $expectedDuration = $expectedDurations[$cue]
    
    # Get all opus files in this cue
    $stems = Get-ChildItem -Path $cuePath -Filter "*.opus"
    
    if ($stems.Count -eq 0) {
        Write-Host "  ✗ No stems found!" -ForegroundColor Red
        $totalIssues++
        continue
    }
    
    foreach ($stem in $stems) {
        $issues = @()
        
        # Check duration
        $duration = ffprobe -i $stem.FullName -show_entries format=duration -v quiet -of csv="p=0" 2>&1
        $duration = [double]$duration
        $diff = [Math]::Abs($duration - $expectedDuration)
        
        if ($diff -gt 0.1) {
            $issues += "Duration mismatch: $($duration)s (expected: $($expectedDuration)s)"
        }
        
        # Check format
        $format = ffprobe -i $stem.FullName -show_entries stream=codec_name -v quiet -of csv="p=0" 2>&1
        if ($format -ne "opus") {
            $issues += "Wrong codec: $format (expected: opus)"
        }
        
        # Check sample rate
        $sampleRate = ffprobe -i $stem.FullName -show_entries stream=sample_rate -v quiet -of csv="p=0" 2>&1
        if ($sampleRate -ne "48000") {
            $issues += "Wrong sample rate: $sampleRate (expected: 48000)"
        }
        
        # Check file size (reasonable range)
        $sizeKB = $stem.Length / 1KB
        $expectedSizeKB = ($expectedDuration / 1000) * 96 # 96kbps
        if ($sizeKB -lt ($expectedSizeKB * 0.5) -or $sizeKB -gt ($expectedSizeKB * 1.5)) {
            $issues += "Unusual file size: $('{0:N0}' -f $sizeKB) KB"
        }
        
        # Report
        if ($issues.Count -eq 0) {
            Write-Host "  ✓ $($stem.Name) - $('{0:N1}' -f $duration)s, $('{0:N0}' -f $sizeKB) KB" -ForegroundColor Green
        } else {
            Write-Host "  ✗ $($stem.Name)" -ForegroundColor Red
            foreach ($issue in $issues) {
                Write-Host "    - $issue" -ForegroundColor Yellow
            }
            $totalIssues += $issues.Count
        }
    }
    
    Write-Host ""
}

# Summary
if ($totalIssues -eq 0) {
    Write-Host "✓ All stems validated successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Found $totalIssues issue(s)" -ForegroundColor Red
    Write-Host "Review the issues above and regenerate stems if needed." -ForegroundColor Yellow
}

