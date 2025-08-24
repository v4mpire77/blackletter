# Context Engineering Framework Compliance Tool (ASCII-only, robust)
param(
    [string]$Action = "test"
)

Write-Host "Blackletter Context Engineering Framework Compliance Tool" -ForegroundColor Cyan

if ($Action -eq "validate" -or $Action -eq "test") {
    $score = 0
    $max = 10

    # 1. Docker Compose structure
    if (Test-Path "../docker-compose.yml") {
        $score++
        Write-Host "OK: docker-compose.yml exists" -ForegroundColor Green
    } else {
        Write-Host "FAIL: docker-compose.yml missing" -ForegroundColor Red
    }

    # 2. Backend config
    if (Test-Path "../backend/app/core/config.py") {
        $score++
        Write-Host "OK: Backend config found" -ForegroundColor Green
    } else {
        Write-Host "FAIL: Backend config missing" -ForegroundColor Red
    }

    # 3. API 202 Accepted pattern
    if (Test-Path "../backend/app/routers/jobs.py") {
        $content = Get-Content "../backend/app/routers/jobs.py" -Raw
        if ($content -match "202" -and $content -match "Location") {
            $score++
            Write-Host "OK: Jobs API returns 202 Accepted" -ForegroundColor Green
        } else {
            Write-Host "FAIL: Jobs API missing 202 pattern" -ForegroundColor Red
        }
    } else {
        Write-Host "FAIL: backend/app/routers/jobs.py missing" -ForegroundColor Red
    }

    # 4. Schemas
    if (Test-Path "../backend/app/models/schemas.py") {
        $score++
        Write-Host "OK: Schemas file found" -ForegroundColor Green
    } else {
        Write-Host "FAIL: Schemas file missing" -ForegroundColor Red
    }

    # 5. Frontend lib/api.ts
    if (Test-Path "../frontend/lib/api.ts") {
        $score++
        Write-Host "OK: Frontend api client exists" -ForegroundColor Green
    } else {
        Write-Host "FAIL: Frontend api client missing" -ForegroundColor Red
    }

    # 6. Celery config
    if (Test-Path "../backend/workers/celery_app.py") {
        $score++
        Write-Host "OK: Celery config exists" -ForegroundColor Green
    } else {
        Write-Host "FAIL: Celery config missing" -ForegroundColor Red
    }

    # 7. .env.example
    if (Test-Path "../.env.example") {
        $score++
        Write-Host "OK: .env.example present" -ForegroundColor Green
    } else {
        Write-Host "FAIL: .env.example missing" -ForegroundColor Red
    }

    # 8. PowerShell scripts ASCII check
    $asciiOk = $true
    if (Test-Path "../scripts") {
        Get-ChildItem -Path "../scripts" -Filter "*.ps1" | ForEach-Object {
            $c = Get-Content $_.FullName -Raw -Encoding utf8
            if ($c -match '[^\x00-\x7F]') { $asciiOk = $false }
        }
    }
    if ($asciiOk) {
        $score++
        Write-Host "OK: All scripts ASCII-only" -ForegroundColor Green
    } else {
        Write-Host "FAIL: Non-ASCII character found in scripts" -ForegroundColor Red
    }

    # 9. Golden test fixture stub
    if (Test-Path "../backend/tests/fixtures/processor_obligations") {
        $score++
        Write-Host "OK: Test fixtures present" -ForegroundColor Green
    } else {
        Write-Host "FAIL: Test fixtures missing" -ForegroundColor Red
    }

    # 10. README
    if (Test-Path "../README.md") {
        $score++
        Write-Host "OK: README present" -ForegroundColor Green
    } else {
        Write-Host "FAIL: README missing" -ForegroundColor Red
    }

    # Output result and percent (avoid % symbol for ASCII)
    $percent = [math]::Round(($score / $max) * 100)
    Write-Host ("Score: $score / $max (" + $percent + " percent)") -ForegroundColor White
    Write-Host "Required: 80 percent" -ForegroundColor White

    if ($percent -ge 80) {
        Write-Host "PASS: Compliance score $percent percent" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "FAIL: Compliance score $percent percent" -ForegroundColor Red
        exit 1
    }
    
} else {
    Write-Host "Usage: .\context_engineering.ps1 -Action test|validate" -ForegroundColor Yellow
    exit 1
}