# Script to resolve merge conflicts by keeping HEAD content
$conflictFiles = @(
    ".gitignore",
    "README.md",
    ".github/workflows/ci.yml",
    "backend/main.py",
    "backend/requirements.txt",
    "backend/app/__init__.py",
    "backend/app/core/__init__.py",
    "backend/app/services/__init__.py",
    "backend/workers/celery_app.py",
    "frontend/Dockerfile",
    "frontend/next.config.js",
    "frontend/package.json",
    "frontend/tailwind.config.js",
    "frontend/app/globals.css",
    "frontend/app/page.tsx",
    "frontend/app/dashboard/page.tsx",
    "frontend/lib/api.ts",
    "frontend/lib/utils.ts"
)

foreach ($file in $conflictFiles) {
    if (Test-Path $file) {
        Write-Host "Resolving conflicts in: $file"
        $lines = Get-Content $file
        $newLines = @()
        $inConflict = $false
        $keepHead = $false
        
        for ($i = 0; $i -lt $lines.Count; $i++) {
            $line = $lines[$i]
            
            if ($line -match "^<<<<<<< HEAD") {
                $inConflict = $true
                $keepHead = $true
                continue
            }
            
            if ($line -match "^=======") {
                $keepHead = $false
                continue
            }
            
            if ($line -match "^>>>>>>>") {
                $inConflict = $false
                continue
            }
            
            # Add line if not in conflict or if we're keeping HEAD content
            if (-not $inConflict -or $keepHead) {
                $newLines += $line
            }
        }
        
        # Write the resolved content back to the file
        Set-Content $file $newLines -Encoding UTF8
    }
}

Write-Host "Conflict resolution complete!"
