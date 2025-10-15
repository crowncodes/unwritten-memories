#!/usr/bin/env pwsh
# GPU Monitor - Shows clear indicators of GPU usage for Ollama

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "GPU MONITOR - Tracking Ollama GPU Usage" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop monitoring" -ForegroundColor Yellow
Write-Host ""

$idleMemory = 4000  # Baseline GPU memory (MB) for desktop
$idlePower = 20     # Baseline power (W) when idle
$activeUtil = 15    # GPU-Util % that indicates active work

while ($true) {
    Clear-Host
    
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host "GPU MONITOR - Ollama Status" -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Time: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray
    Write-Host ""
    
    # Parse nvidia-smi output
    $gpuInfo = nvidia-smi --query-gpu=name,temperature.gpu,power.draw,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits
    
    if ($gpuInfo) {
        $parts = $gpuInfo -split ','
        $gpuName = $parts[0].Trim()
        $temp = [int]$parts[1].Trim()
        $power = [int]$parts[2].Trim()
        $memUsed = [int]$parts[3].Trim()
        $memTotal = [int]$parts[4].Trim()
        $gpuUtil = [int]$parts[5].Trim()
        
        # Calculate percentages
        $memPercent = [math]::Round(($memUsed / $memTotal) * 100, 1)
        $powerPercent = [math]::Round(($power / 320) * 100, 0)
        
        # Determine status
        $modelLoaded = $memUsed -gt $idleMemory
        $activeWork = $gpuUtil -gt $activeUtil
        $powerActive = $power -gt $idlePower
        
        # Display GPU info
        Write-Host "GPU: $gpuName" -ForegroundColor White
        Write-Host ""
        
        # Memory status
        Write-Host "VRAM Usage: " -NoNewline
        if ($modelLoaded) {
            Write-Host "$memUsed MB / $memTotal MB ($memPercent%)" -ForegroundColor Green
            Write-Host "            [OK] MODEL LOADED IN GPU MEMORY" -ForegroundColor Green
        } else {
            Write-Host "$memUsed MB / $memTotal MB ($memPercent%)" -ForegroundColor Gray
            Write-Host "            [WARN] No model loaded" -ForegroundColor Yellow
        }
        Write-Host ""
        
        # GPU Utilization
        Write-Host "GPU Compute: " -NoNewline
        if ($activeWork) {
            Write-Host "$gpuUtil%" -ForegroundColor Green
            Write-Host "             [ACTIVE] ACTIVELY GENERATING!" -ForegroundColor Green
        } elseif ($modelLoaded) {
            Write-Host "$gpuUtil%" -ForegroundColor Yellow
            Write-Host "             [READY] Model loaded, waiting for request" -ForegroundColor Yellow
        } else {
            Write-Host "$gpuUtil%" -ForegroundColor Gray
            Write-Host "             [IDLE] Idle" -ForegroundColor Gray
        }
        Write-Host ""
        
        # Power consumption
        Write-Host "Power Draw:  " -NoNewline
        if ($powerActive) {
            Write-Host "$power W ($powerPercent%)" -ForegroundColor Green
            Write-Host "             [WORKING] GPU is working (above idle)" -ForegroundColor Green
        } else {
            Write-Host "$power W ($powerPercent%)" -ForegroundColor Gray
            Write-Host "             [IDLE] Idle power consumption" -ForegroundColor Gray
        }
        Write-Host ""
        
        # Temperature
        Write-Host "Temperature: " -NoNewline
        if ($temp -gt 60) {
            Write-Host "$temp C" -ForegroundColor Red
            Write-Host "             Running hot" -ForegroundColor Red
        } elseif ($temp -gt 50) {
            Write-Host "$temp C" -ForegroundColor Yellow
            Write-Host "             Warm (working)" -ForegroundColor Yellow
        } else {
            Write-Host "$temp C" -ForegroundColor Cyan
            Write-Host "             Cool (idle or light load)" -ForegroundColor Cyan
        }
        Write-Host ""
        Write-Host "-" * 80 -ForegroundColor Gray
        Write-Host ""
        
        # Overall status
        if ($modelLoaded -and $activeWork) {
            Write-Host "STATUS: " -NoNewline -ForegroundColor White
            Write-Host "[ACTIVE] GPU ACTIVELY PROCESSING AI MODEL" -ForegroundColor Green -BackgroundColor DarkGreen
        } elseif ($modelLoaded) {
            Write-Host "STATUS: " -NoNewline -ForegroundColor White
            Write-Host "[READY] GPU Ready - Model Loaded, Waiting for Requests" -ForegroundColor Yellow
        } else {
            Write-Host "STATUS: " -NoNewline -ForegroundColor White
            Write-Host "[IDLE] GPU Idle - No Model Loaded" -ForegroundColor Gray
        }
        
        Write-Host ""
        Write-Host ""
        
        # Check for Ollama processes
        $ollamaProcs = Get-Process -Name ollama* -ErrorAction SilentlyContinue
        if ($ollamaProcs) {
            Write-Host "Ollama Processes:" -ForegroundColor White
            foreach ($proc in $ollamaProcs) {
                Write-Host "  * $($proc.Name) (PID: $($proc.Id))" -ForegroundColor Cyan
            }
        } else {
            Write-Host "[WARN] No Ollama processes detected!" -ForegroundColor Red
        }
        
    } else {
        Write-Host "[ERROR] Could not read GPU info" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host "Refreshing in 2 seconds... (Ctrl+C to stop)" -ForegroundColor Gray
    
    Start-Sleep -Seconds 2
}

