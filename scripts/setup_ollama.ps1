# Unwritten Training Setup - Ollama Installation & Configuration
# For Windows PowerShell
# RTX 4070 SUPER 12GB VRAM + 128GB RAM

Write-Host "[UNWRITTEN] Training Data Generation Setup" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "[WARNING] Not running as administrator. Some operations may fail." -ForegroundColor Yellow
}

# Step 1: Check if Ollama is installed
Write-Host "`n[STEP 1] Checking Ollama installation..." -ForegroundColor Green
$ollamaPath = Get-Command ollama -ErrorAction SilentlyContinue

if ($null -eq $ollamaPath) {
    Write-Host "[ERROR] Ollama not found. Please install from: https://ollama.ai/download" -ForegroundColor Red
    Write-Host "   1. Visit https://ollama.ai/download" -ForegroundColor Yellow
    Write-Host "   2. Download the Windows installer" -ForegroundColor Yellow
    Write-Host "   3. Run the installer" -ForegroundColor Yellow
    Write-Host "   4. Restart PowerShell" -ForegroundColor Yellow
    Write-Host "   5. Run this script again" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "[OK] Ollama found at: $($ollamaPath.Source)" -ForegroundColor Green
    $ollamaVersion = & ollama --version 2>&1
    Write-Host "   Version: $ollamaVersion" -ForegroundColor Gray
}

# Step 2: Check Ollama service
Write-Host "`n[STEP 2] Checking Ollama service..." -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "[OK] Ollama service is running" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Ollama service not responding. Starting Ollama..." -ForegroundColor Yellow
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 5 -ErrorAction Stop
        Write-Host "[OK] Ollama service started successfully" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Failed to start Ollama service" -ForegroundColor Red
        exit 1
    }
}

# Step 3: Configure environment variables
Write-Host "`n[STEP 3] Configuring environment variables..." -ForegroundColor Green

# Set environment variables for current session
$env:OLLAMA_KEEP_ALIVE = "24h"
$env:OLLAMA_MAX_LOADED_MODELS = "3"
$env:OLLAMA_GPU_LAYERS = "999"

Write-Host "[OK] Environment variables set for current session:" -ForegroundColor Green
Write-Host "   OLLAMA_KEEP_ALIVE=24h" -ForegroundColor Gray
Write-Host "   OLLAMA_MAX_LOADED_MODELS=3" -ForegroundColor Gray
Write-Host "   OLLAMA_GPU_LAYERS=999" -ForegroundColor Gray

# Optionally set system environment variables
$setPermanent = Read-Host "`nSet these permanently for your user account? (y/n)"
if ($setPermanent -eq "y") {
    [Environment]::SetEnvironmentVariable("OLLAMA_KEEP_ALIVE", "24h", "User")
    [Environment]::SetEnvironmentVariable("OLLAMA_MAX_LOADED_MODELS", "3", "User")
    [Environment]::SetEnvironmentVariable("OLLAMA_GPU_LAYERS", "999", "User")
    Write-Host "[OK] Environment variables set permanently" -ForegroundColor Green
}

# Step 4: Check available models
Write-Host "`n[STEP 4] Checking available models..." -ForegroundColor Green
$models = & ollama list 2>&1 | Out-String

Write-Host "Current models:" -ForegroundColor Gray
Write-Host $models -ForegroundColor Gray

# Step 5: Pull required models
Write-Host "`n[STEP 5] Downloading required Qwen3 models..." -ForegroundColor Green
Write-Host "   This will download approximately 60GB total. It may take 30-60 minutes." -ForegroundColor Yellow

$requiredModels = @(
    @{Name="qwen3:30b-a3b"; Description="Primary quality model"; Size="18GB"},
    @{Name="qwen3:8b"; Description="Fast generation model"; Size="5GB"},
    @{Name="qwen3:32b"; Description="Validation model"; Size="20GB"}
)

foreach ($model in $requiredModels) {
    Write-Host "`n   Checking $($model.Name) - $($model.Description) - $($model.Size)" -ForegroundColor Cyan
    
    if ($models -match $model.Name) {
        Write-Host "   [OK] Already installed" -ForegroundColor Green
    } else {
        Write-Host "   [DOWNLOADING] Size: $($model.Size)" -ForegroundColor Yellow
        $downloadConfirm = Read-Host "   Download $($model.Name)? (y/n)"
        
        if ($downloadConfirm -eq "y") {
            & ollama pull $model.Name
            if ($LASTEXITCODE -eq 0) {
                Write-Host "   [SUCCESS] Downloaded $($model.Name)" -ForegroundColor Green
            } else {
                Write-Host "   [ERROR] Failed to download $($model.Name)" -ForegroundColor Red
            }
        } else {
            Write-Host "   [SKIPPED] $($model.Name)" -ForegroundColor Yellow
        }
    }
}

# Step 6: Test generation
Write-Host "`n[STEP 6] Testing model generation..." -ForegroundColor Green
Write-Host "   Testing with qwen3:8b (fastest model)..." -ForegroundColor Gray

$testPrompt = "Say 'Ollama is working correctly' in exactly that phrase."
try {
    $testResult = & ollama run qwen3:8b $testPrompt 2>&1 | Out-String
    
    if ($testResult -match "working correctly") {
        Write-Host "[OK] Model generation test successful!" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Model responded but output unexpected:" -ForegroundColor Yellow
        Write-Host "   $testResult" -ForegroundColor Gray
    }
} catch {
    Write-Host "[ERROR] Model generation test failed" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
}

# Step 7: Create output directory
Write-Host "`n[STEP 7] Creating output directories..." -ForegroundColor Green
$outputDir = Join-Path $PWD "training_output"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
    Write-Host "[OK] Created: $outputDir" -ForegroundColor Green
} else {
    Write-Host "[OK] Directory exists: $outputDir" -ForegroundColor Green
}

# Step 8: Summary and next steps
Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
Write-Host "[SETUP COMPLETE]" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Cyan

Write-Host "`n[SYSTEM CONFIGURATION]" -ForegroundColor Cyan
Write-Host "   GPU: RTX 4070 SUPER 12GB VRAM" -ForegroundColor Gray
Write-Host "   RAM: 128GB" -ForegroundColor Gray
Write-Host "   Ollama: Running on http://localhost:11434" -ForegroundColor Gray
Write-Host "   Output: $outputDir" -ForegroundColor Gray

Write-Host "`n[EXPECTED PERFORMANCE]" -ForegroundColor Cyan
Write-Host "   Daily output: approximately 6,500 training samples" -ForegroundColor Gray
Write-Host "   7-day total: approximately 45,000 samples" -ForegroundColor Gray
Write-Host "   Cost: approximately `$25-35 electricity" -ForegroundColor Gray

Write-Host "`n[NEXT STEPS]" -ForegroundColor Cyan
Write-Host "   1. Activate Python environment:" -ForegroundColor Yellow
Write-Host "      .\unwritten-env\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "`n   2. Install Python dependencies:" -ForegroundColor Yellow
Write-Host "      pip install -e ." -ForegroundColor Gray
Write-Host "`n   3. Start training data generation:" -ForegroundColor Yellow
Write-Host "      python scripts\run_training_pipeline.py" -ForegroundColor Gray
Write-Host "`n   4. Monitor progress:" -ForegroundColor Yellow
Write-Host "      Get-Content training_generation.log -Wait" -ForegroundColor Gray

Write-Host "`n[TIPS]" -ForegroundColor Cyan
Write-Host "   - First generation will be slow as models load into memory" -ForegroundColor Gray
Write-Host "   - After warmup, expect 6,500+ samples/day" -ForegroundColor Gray
Write-Host "   - Check training_output/ for generated data" -ForegroundColor Gray
Write-Host "   - Review logs for quality scores and validation" -ForegroundColor Gray

Write-Host "`n[READY] Ready to generate training data!" -ForegroundColor Green
