# CONTEXT ENGINEERING FRAMEWORK COMPLIANCE TOOL
param(
    [Parameter(Mandatory = $false)]
    [string]$Action = "test"
)

Write-Host "Blackletter Context Engineering Framework Compliance Tool" -ForegroundColor Cyan

if ($Action -eq "test" -or $Action -eq "validate") {
    $score = 0
    $max = 10

    # 1. Docker Compose structure
    if (Test-Path "../docker-compose.yml") {
        $score++
        Write-Host "✓ docker-compose.yml exists" -ForegroundColor Green
    } else {
        Write-Host "✗ docker-compose.yml missing" -ForegroundColor Red
    }

    # 2. Backend config
    if (Test-Path "../backend/app/core/config.py") {
        $score++
        Write-Host "✓ Backend config found" -ForegroundColor Green
    } else {
        Write-Host "✗ Backend config missing" -ForegroundColor Red
    }

    # 3. API 202 Accepted pattern
    if (Test-Path "../backend/app/routers/jobs.py") {
        $content = Get-Content "../backend/app/routers/jobs.py" -Raw
        if ($content -match "202" -and $content -match "Location") {
            $score++
            Write-Host "✓ Jobs API returns 202 Accepted" -ForegroundColor Green
        } else {
            Write-Host "✗ Jobs API missing 202 pattern" -ForegroundColor Red
        }
    }

    # 4. Schemas
    if (Test-Path "../backend/app/models/schemas.py") {
        $score++
        Write-Host "✓ Schemas file found" -ForegroundColor Green
    } else {
        Write-Host "✗ Schemas file missing" -ForegroundColor Red
    }

    # 5. Frontend lib/api.ts
    if (Test-Path "../frontend/app/lib/api.ts") {
        $score++
        Write-Host "✓ Frontend api client exists" -ForegroundColor Green
    } else {
        Write-Host "✗ Frontend api client missing" -ForegroundColor Red
    }

    # 6. Celery config
    if (Test-Path "../backend/workers/celery_app.py") {
        $score++
        Write-Host "✓ Celery config exists" -ForegroundColor Green
    } else {
        Write-Host "✗ Celery config missing" -ForegroundColor Red
    }

    # 7. .env.example
    if (Test-Path "../.env.example") {
        $score++
        Write-Host "✓ .env.example present" -ForegroundColor Green
    } else {
        Write-Host "✗ .env.example missing" -ForegroundColor Red
    }

    # 8. PowerShell scripts ASCII check
    $asciiOk = $true
    Get-ChildItem -Path "../scripts" -Filter "*.ps1" | ForEach-Object {
        $c = Get-Content $_.FullName -Raw -Encoding utf8
        if ($c -match '[^\x00-\x7F]') { $asciiOk = $false }
    }
    if ($asciiOk) {
        $score++
        Write-Host "✓ All scripts ASCII-only" -ForegroundColor Green
    } else {
        Write-Host "✗ Non-ASCII character found in scripts" -ForegroundColor Red
    }

    # 9. Golden test fixture stub
    if (Test-Path "../backend/tests/fixtures/processor_obligations") {
        $score++
        Write-Host "✓ Test fixtures present" -ForegroundColor Green
    } else {
        Write-Host "✗ Test fixtures missing" -ForegroundColor Red
    }

    # 10. README
    if (Test-Path "../README.md") {
        $score++
        Write-Host "✓ README present" -ForegroundColor Green
    } else {
        Write-Host "✗ README missing" -ForegroundColor Red
    }

    $percent = [math]::Round(($score / $max) * 100)
    if ($percent -ge 80) {
        Write-Host "PASS: Compliance score $percent%" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "FAIL: Compliance score $percent%" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Usage: .\context_engineering.ps1 -Action test|validate" -ForegroundColor Yellow
    exit 1
}