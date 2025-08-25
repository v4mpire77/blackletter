# Simple script to find actual merge conflicts
Get-ChildItem -Recurse -File | Where-Object { $_.Name -notlike "*.png" -and $_.Name -notlike "*.jpg" -and $_.Name -notlike "*.gif" -and $_.Name -notlike "*.pdf" -and $_.Name -notlike "*.zip" -and $_.Name -notlike "*.exe" -and $_.Name -notlike "*.dll" -and $_.Name -notlike "node_modules" -and $_.Name -notlike ".git" } | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -match "<<<<<<< HEAD[\s\S]*?=======([\s\S]*?)>>>>>>>") {
        Write-Host "Conflict found in: $($_.FullName)"
    }
}