#!/usr/bin/env pwsh
# Configure Ollama Environment Variables for Optimal Performance
# For RTX 4070 SUPER (12GB VRAM) + 128GB RAM

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "OLLAMA ENVIRONMENT CONFIGURATION" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# ===================================================================
# RECOMMENDED SETTINGS FOR SYSTEMATIC GENERATION
# ===================================================================

# Keep models loaded in memory for 24 hours (prevents constant reloading)
$env:OLLAMA_KEEP_ALIVE = "24h"

# Allow up to 3 models to be loaded simultaneously
$env:OLLAMA_MAX_LOADED_MODELS = "3"

# Use all available GPU layers (999 = use as many as possible)
$env:OLLAMA_GPU_LAYERS = "999"

Write-Host "✅ Environment Variables Set (Current Session):" -ForegroundColor Green
Write-Host ""
Write-Host "   OLLAMA_KEEP_ALIVE         = $env:OLLAMA_KEEP_ALIVE" -ForegroundColor Gray
Write-Host "   OLLAMA_MAX_LOADED_MODELS  = $env:OLLAMA_MAX_LOADED_MODELS" -ForegroundColor Gray
Write-Host "   OLLAMA_GPU_LAYERS         = $env:OLLAMA_GPU_LAYERS" -ForegroundColor Gray
Write-Host ""

# ===================================================================
# OPTIONAL: SET PERMANENTLY
# ===================================================================

$setPermanent = Read-Host "Set these variables permanently for your user account? (y/n)"

if ($setPermanent -eq "y" -or $setPermanent -eq "Y") {
    Write-Host ""
    Write-Host "Setting permanent environment variables..." -ForegroundColor Yellow
    
    [Environment]::SetEnvironmentVariable("OLLAMA_KEEP_ALIVE", "24h", "User")
    [Environment]::SetEnvironmentVariable("OLLAMA_MAX_LOADED_MODELS", "3", "User")
    [Environment]::SetEnvironmentVariable("OLLAMA_GPU_LAYERS", "999", "User")
    
    Write-Host "✅ Environment variables set permanently" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  NOTE: You may need to restart your terminal for changes to take effect" -ForegroundColor Yellow
}
else {
    Write-Host ""
    Write-Host "Environment variables set for current session only" -ForegroundColor Yellow
    Write-Host "They will be lost when you close this terminal" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "WHAT THESE SETTINGS DO" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "OLLAMA_KEEP_ALIVE (24h):" -ForegroundColor White
Write-Host "  • Keeps models loaded in memory for 24 hours" -ForegroundColor Gray
Write-Host "  • Prevents slow model reloading between generations" -ForegroundColor Gray
Write-Host "  • Essential for multi-hour training sessions" -ForegroundColor Gray
Write-Host ""
Write-Host "OLLAMA_MAX_LOADED_MODELS (3):" -ForegroundColor White
Write-Host "  • Allows 3 models loaded simultaneously" -ForegroundColor Gray
Write-Host "  • Needed for: qwen3:30b (main), qwen3:8b (fast), qwen3:30b-a3b (validation)" -ForegroundColor Gray
Write-Host "  • Reduces model swap overhead during generation" -ForegroundColor Gray
Write-Host ""
Write-Host "OLLAMA_GPU_LAYERS (999):" -ForegroundColor White
Write-Host "  • Uses maximum GPU layers available" -ForegroundColor Gray
Write-Host "  • Maximizes GPU acceleration vs CPU fallback" -ForegroundColor Gray
Write-Host "  • Critical for generation speed (2-3x faster)" -ForegroundColor Gray
Write-Host ""

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "NEXT STEPS" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Restart Ollama service to apply changes:" -ForegroundColor Yellow
Write-Host "   taskkill /F /IM ollama.exe" -ForegroundColor Gray
Write-Host "   Start-Sleep -Seconds 2" -ForegroundColor Gray
Write-Host "   Start-Process ollama -ArgumentList 'serve' -WindowStyle Hidden" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Verify settings are applied:" -ForegroundColor Yellow
Write-Host "   .\scripts\check_gpu_models.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Start training data generation:" -ForegroundColor Yellow
Write-Host "   python scripts\run_training_pipeline.py" -ForegroundColor Gray
Write-Host ""

# ===================================================================
# OPTIONAL ADVANCED SETTINGS
# ===================================================================

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "OPTIONAL ADVANCED SETTINGS" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "The following are NOT recommended for standard use:" -ForegroundColor Yellow
Write-Host ""
Write-Host "• OLLAMA_GPU_OVERHEAD: Reduce GPU memory overhead (default: conservative)" -ForegroundColor Gray
Write-Host "  $env:OLLAMA_GPU_OVERHEAD = `"1073741824`"  # 1GB instead of ~2GB" -ForegroundColor DarkGray
Write-Host ""
Write-Host "• OLLAMA_FLASH_ATTENTION: Enable flash attention for memory efficiency" -ForegroundColor Gray
Write-Host "  $env:OLLAMA_FLASH_ATTENTION = `"true`"" -ForegroundColor DarkGray
Write-Host ""
Write-Host "• OLLAMA_NUM_PARALLEL: Limit parallel requests (useful for stability)" -ForegroundColor Gray
Write-Host "  $env:OLLAMA_NUM_PARALLEL = `"2`"  # Default: 4" -ForegroundColor DarkGray
Write-Host ""
Write-Host "Only modify these if experiencing issues with the standard configuration." -ForegroundColor Yellow
Write-Host ""

Write-Host "=" * 70 -ForegroundColor Green
Write-Host "✅ CONFIGURATION COMPLETE" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host ""
