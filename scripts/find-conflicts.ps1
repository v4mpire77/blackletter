# Find Merge Conflicts Script
# ASCII-only PowerShell script for Windows compatibility
param(
    [string]$Path = ".",
    [switch]$ShowDetails
)

Write-Host "Searching for merge conflict markers..." -ForegroundColor Yellow

$ConflictPatterns = @(
    '<<<<<<<',
    '=======',
    '>>>>>>>'
)

$FoundConflicts = @()

foreach ($Pattern in $ConflictPatterns) {
    $Results = Get-ChildItem -Path $Path -Recurse -File | 
               Where-Object { $_.Extension -match '\.(yml|yaml|json|ts|tsx|js|jsx|py|md|txt|env|example)$' } |
               ForEach-Object {
                   $Content = Get-Content $_.FullName -ErrorAction SilentlyContinue
                   if ($Content -match $Pattern) {
                       $LineNumbers = @()
                       for ($i = 0; $i -lt $Content.Length; $i++) {
                           if ($Content[$i] -match $Pattern) {
                               $LineNumbers += ($i + 1)
                           }
                       }
                       [PSCustomObject]@{
                           File = $_.FullName
                           Pattern = $Pattern
                           Lines = $LineNumbers
                       }
                   }
               }
    
    if ($Results) {
        $FoundConflicts += $Results
    }
}

if ($FoundConflicts.Count -eq 0) {
    Write-Host "SUCCESS: No merge conflict markers found!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "ERROR: Found $($FoundConflicts.Count) conflict marker(s):" -ForegroundColor Red
    
    foreach ($Conflict in $FoundConflicts) {
        Write-Host "  File: $($Conflict.File)" -ForegroundColor Yellow
        Write-Host "  Pattern: $($Conflict.Pattern)" -ForegroundColor Red
        Write-Host "  Lines: $($Conflict.Lines -join ', ')" -ForegroundColor Cyan
        Write-Host ""
        
        if ($ShowDetails) {
            Write-Host "  Content preview:" -ForegroundColor Gray
            $Content = Get-Content $Conflict.File
            foreach ($LineNum in $Conflict.Lines) {
                $StartLine = [Math]::Max(0, $LineNum - 3)
                $EndLine = [Math]::Min($Content.Length - 1, $LineNum + 2)
                
                for ($i = $StartLine; $i -le $EndLine; $i++) {
                    $Prefix = if ($i + 1 -eq $LineNum) { ">>> " } else { "    " }
                    Write-Host "$Prefix$($i + 1): $($Content[$i])" -ForegroundColor Gray
                }
                Write-Host ""
            }
        }
    }
    
    Write-Host "Please resolve these conflicts before proceeding." -ForegroundColor Red
    exit 1
}