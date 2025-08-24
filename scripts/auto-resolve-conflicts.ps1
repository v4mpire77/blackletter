# Auto-resolve Merge Conflicts Script
# ASCII-only PowerShell script for Windows compatibility
param(
    [string]$Strategy = "ours",  # "ours" keeps HEAD, "theirs" keeps incoming
    [switch]$DryRun
)

Write-Host "Auto-resolving merge conflicts with strategy: $Strategy" -ForegroundColor Yellow

# List of files with known conflicts that we want to keep HEAD version
$FilesToKeepHead = @(
    "README.md",
    ".github/workflows/ci.yml", 
    "backend/main.py",
    "backend/requirements.txt",
    "backend/app/__init__.py",
    "frontend/tailwind.config.js",
    "frontend/package.json",
    "frontend/app/page.tsx",
    "frontend/app/dashboard/page.tsx",
    "frontend/lib/api.ts",
    "frontend/lib/utils.ts"
)

foreach ($File in $FilesToKeepHead) {
    $FullPath = Join-Path (Get-Location) $File
    if (Test-Path $FullPath) {
        Write-Host "Resolving conflicts in: $File" -ForegroundColor Cyan
        
        if (-not $DryRun) {
            try {
                git checkout --ours $File
                git add $File
                Write-Host "  SUCCESS: Kept HEAD version" -ForegroundColor Green
            }
            catch {
                Write-Host "  ERROR: Failed to resolve $File" -ForegroundColor Red
            }
        } else {
            Write-Host "  DRY RUN: Would keep HEAD version" -ForegroundColor Gray
        }
    } else {
        Write-Host "  SKIP: File not found - $File" -ForegroundColor Yellow
    }
}

if (-not $DryRun) {
    Write-Host "`nChecking for any remaining conflicts..." -ForegroundColor Yellow
    
    # Run our conflict detection script
    $ConflictCheck = & ".\scripts\find-conflicts.ps1"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: All conflicts resolved!" -ForegroundColor Green
        
        # Stage all resolved files
        git add .
        Write-Host "All resolved files staged for commit." -ForegroundColor Green
    } else {
        Write-Host "WARNING: Some conflicts may still exist. Check manually." -ForegroundColor Yellow
    }
} else {
    Write-Host "`nDRY RUN completed. Use -DryRun:`$false to apply changes." -ForegroundColor Gray
}