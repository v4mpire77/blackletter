# cleanup_repo_simple.ps1 - ASCII-only Repository Cleanup
param([switch]$DryRun = $false)

$ErrorActionPreference = "Stop"

Write-Host "Blackletter Systems - Repository Bootstrap" -ForegroundColor Green
Write-Host "Context Engineering Framework v2.0.0" -ForegroundColor Cyan

# Validate environment
if (-not (Test-Path "blackletter")) {
    Write-Error "Current directory must contain 'blackletter' folder"
    exit 1
}

# Create backup
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = "blackletter_backup_$timestamp"

Write-Host "`nStep 1: Creating Backup..." -ForegroundColor Yellow
if (-not $DryRun) {
    Copy-Item -Path "blackletter" -Destination $backupDir -Recurse -Force
    Write-Host "Backup created: $backupDir" -ForegroundColor Green
}

# Create clean structure
Write-Host "`nStep 2: Creating Clean Structure..." -ForegroundColor Yellow
$cleanDirs = @(
    "blackletter_clean/backend/app/routers",
    "blackletter_clean/backend/app/services",
    "blackletter_clean/backend/app/models",
    "blackletter_clean/backend/app/core",
    "blackletter_clean/backend/workers",
    "blackletter_clean/backend/tests",
    "blackletter_clean/backend/migrations",
    "blackletter_clean/frontend/app/upload",
    "blackletter_clean/frontend/app/dashboard", 
    "blackletter_clean/frontend/app/compliance",
    "blackletter_clean/frontend/components/ui",
    "blackletter_clean/frontend/lib",
    "blackletter_clean/frontend/__tests__",
    "blackletter_clean/scripts",
    "blackletter_clean/tools",
    "blackletter_clean/docs",
    "blackletter_clean/fixtures"
)

if (-not $DryRun) {
    if (Test-Path "blackletter_clean") {
        Remove-Item "blackletter_clean" -Recurse -Force
    }
    foreach ($dir in $cleanDirs) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    Write-Host "Clean structure created: blackletter_clean/" -ForegroundColor Green
}

Write-Host "`nStep 3: Ready for Implementation Files" -ForegroundColor Yellow
Write-Host "Backup: $backupDir" -ForegroundColor White
Write-Host "Clean: blackletter_clean/" -ForegroundColor White

if ($DryRun) {
    Write-Host "`nDRY RUN COMPLETE" -ForegroundColor Yellow
} else {
    Write-Host "`nCLEANUP COMPLETE - Ready for file generation" -ForegroundColor Green
}