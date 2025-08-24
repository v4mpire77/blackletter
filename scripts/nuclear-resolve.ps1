# Nuclear Conflict Resolution Script
# ASCII-only PowerShell script for Windows compatibility
param(
    [switch]$Execute
)

Write-Host "Starting nuclear conflict resolution..." -ForegroundColor Yellow

# Files we've already fixed manually - don't touch these
$CleanFiles = @(
    "docker-compose.yml",
    ".env.example",  
    "frontend/tsconfig.json",
    "frontend/app/layout.tsx"
)

# Files with conflicts that need to be reset to HEAD
$ConflictedFiles = @(
    "README.md",
    ".github/workflows/ci.yml",
    "backend/main.py", 
    "backend/requirements.txt",
    "backend/app/__init__.py",
    "backend/app/core/__init__.py",
    "backend/app/services/__init__.py",
    "backend/workers/celery_app.py",
    "backend/VAGUE_TERMS_README.md",
    "frontend/next.config.js",
    "frontend/package.json",
    "frontend/tailwind.config.js", 
    "frontend/app/page.tsx",
    "frontend/app/dashboard/page.tsx",
    "frontend/lib/api.ts",
    "frontend/lib/utils.ts",
    "tools/README.md",
    "tools/validate_framework.py",
    ".github/workflows/rust_and_pip.yml"
)

if ($Execute) {
    Write-Host "EXECUTING: Backing up current state..." -ForegroundColor Red
    
    # Create backup directory with timestamp
    $BackupDir = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    
    foreach ($File in $ConflictedFiles) {
        $SourcePath = $File
        $BackupPath = Join-Path $BackupDir $File
        
        if (Test-Path $SourcePath) {
            # Create directory structure in backup
            $BackupFileDir = Split-Path $BackupPath -Parent
            if ($BackupFileDir -and -not (Test-Path $BackupFileDir)) {
                New-Item -ItemType Directory -Path $BackupFileDir -Force | Out-Null
            }
            
            # Copy to backup
            Copy-Item $SourcePath $BackupPath -Force
            Write-Host "  Backed up: $File" -ForegroundColor Gray
            
            # Reset to clean HEAD version
            try {
                git show HEAD:$File > $SourcePath
                Write-Host "  Reset to HEAD: $File" -ForegroundColor Green
            }
            catch {
                Write-Host "  ERROR resetting: $File" -ForegroundColor Red
            }
        }
    }
    
    Write-Host "`nStaging all changes..." -ForegroundColor Yellow
    git add .
    
    Write-Host "`nFinal conflict check..." -ForegroundColor Yellow
    $FinalCheck = & ".\scripts\find-conflicts.ps1"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: All conflicts resolved!" -ForegroundColor Green
        Write-Host "Backup created in: $BackupDir" -ForegroundColor Cyan
    } else {
        Write-Host "WARNING: Some conflicts may remain." -ForegroundColor Yellow
    }
} else {
    Write-Host "DRY RUN MODE" -ForegroundColor Gray
    Write-Host "Would reset these files to HEAD version:" -ForegroundColor Yellow
    foreach ($File in $ConflictedFiles) {
        if (Test-Path $File) {
            Write-Host "  - $File" -ForegroundColor Cyan
        } else {
            Write-Host "  - $File (NOT FOUND)" -ForegroundColor Red
        }
    }
    Write-Host "`nWould preserve these clean files:" -ForegroundColor Yellow
    foreach ($File in $CleanFiles) {
        Write-Host "  - $File" -ForegroundColor Green
    }
    Write-Host "`nRun with -Execute to apply changes" -ForegroundColor Yellow
}