Write-Host "================================================"
Write-Host "Tool-58 - Final Performance Verification"
Write-Host "================================================"

$body = @{
    title           = "DDoS Attack on Web Application"
    incident_type   = "DDoS"
    severity        = "High"
    affected_system = "Web Application Load Balancer"
    description     = "450,000 requests per second for 3 hours causing complete outage."
} | ConvertTo-Json

$endpoints = @(
    @{ name = "/describe"; url = "http://localhost:5000/describe" },
    @{ name = "/recommend"; url = "http://localhost:5000/recommend" },
    @{ name = "/generate-report"; url = "http://localhost:5000/generate-report" }
)

$times = @()

foreach ($ep in $endpoints) {

    Write-Host ""
    Write-Host "Testing $($ep.name)..."

    $start = Get-Date

    try {

        $r = Invoke-RestMethod `
            -Uri $ep.url `
            -Method POST `
            -ContentType "application/json" `
            -Body $body `
            -TimeoutSec 30

        $elapsed = ((Get-Date) - $start).TotalSeconds
        $elapsed = [math]::Round($elapsed, 2)

        $times += $elapsed

        if ($elapsed -lt 2) {
            $status = "PASS"
        }
        elseif ($elapsed -lt 5) {
            $status = "SLOW"
        }
        else {
            $status = "FAIL"
        }

        Write-Host "  $status - $elapsed sec"

        if ($null -ne $r.is_fallback) {
            Write-Host "  Fallback: $($r.is_fallback)"
        }

        if ($null -ne $r.usage.total_tokens_used) {
            Write-Host "  Tokens: $($r.usage.total_tokens_used)"
        }
    }
    catch {

        Write-Host "  FAIL - $($ep.name)"
        Write-Host "  Error: $($_.Exception.Message)"
    }
}

Write-Host ""
Write-Host "Testing cache..."

$start = Get-Date

try {

    $r = Invoke-RestMethod `
        -Uri "http://localhost:5000/describe" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -TimeoutSec 10

    $elapsed = ((Get-Date) - $start).TotalSeconds
    $elapsed = [math]::Round($elapsed, 2)

    Write-Host "Cache response time: $elapsed sec"
}
catch {

    Write-Host "Cache test failed"
    Write-Host $_.Exception.Message
}

Write-Host ""
Write-Host "Health Check"

try {

    $health = Invoke-RestMethod `
        -Uri "http://localhost:5000/health" `
        -Method GET

    Write-Host "Model: $($health.model)"
    Write-Host "Avg response: $($health.avg_response_time)"
    Write-Host "Cache enabled: $($health.cache_enabled)"

    if ($health.uptime.total_seconds) {
        Write-Host "Uptime: $($health.uptime.total_seconds)"
    }
}
catch {

    Write-Host "Health endpoint failed"
    Write-Host $_.Exception.Message
}

if ($times.Count -gt 0) {

    $avg = [math]::Round(($times | Measure-Object -Average).Average, 2)
    $max = [math]::Round(($times | Measure-Object -Maximum).Maximum, 2)

    Write-Host ""
    Write-Host "Summary"
    Write-Host "Average response: $avg sec"
    Write-Host "Maximum response: $max sec"

    if ($avg -lt 2) {
        Write-Host "Result: ALL TARGETS MET"
    }
    else {
        Write-Host "Result: CHECK API LATENCY"
    }
}

Write-Host ""
Write-Host "================================================"