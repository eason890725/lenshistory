# LensHistory One-Click Dev Environment
# Final Bulletproof Version

$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$backendDir = Join-Path $PSScriptRoot "backend"
$frontendDir = Join-Path $PSScriptRoot "frontend"

# 1. Kill old processes and clear cache
Write-Host "1. Cleaning up old processes and clearing cache..." -ForegroundColor Yellow
taskkill /F /IM node.exe /T 2>$null
wsl bash -c "killall -9 java" 2>$null
Remove-Item -Path (Join-Path $frontendDir ".next") -Recurse -Force -ErrorAction SilentlyContinue

# 2. Start Backend in WSL
Write-Host "2. Launching Backend (Port 8083)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendDir'; wsl ./mvnw spring-boot:run"

# 3. Detect Network (with retry and fallback)
Write-Host "3. Configuring Network..." -ForegroundColor Green
$wslIp = ""
try {
    $wslIp = (wsl hostname -I).Trim().Split(' ')[0]
} catch {}

if (!$wslIp) { 
    $wslIp = "127.0.0.1" 
    Write-Host "   WSL IP not found, using 127.0.0.1" -ForegroundColor Yellow
} else {
    Write-Host "   Detected WSL IP: $wslIp" -ForegroundColor Gray
}

# Critical Fix: Ensure the string is correctly formatted
$envContent = "NEXT_PUBLIC_BACKEND_URL=http://$($wslIp):8083"
$envContent | Out-File -FilePath (Join-Path $frontendDir ".env.local") -Encoding utf8 -Force

# 4. Wait for Backend (Self-Testing)
Write-Host "4. Waiting for Database to initialize..." -ForegroundColor Cyan
$maxRetries = 60
$count = 0
$ready = $false
while ($count -lt $maxRetries -and !$ready) {
    try {
        $resp = Invoke-RestMethod -Uri "http://$($wslIp):8083/api/v1/gear/search" -ErrorAction SilentlyContinue
        if ($resp.Count -gt 10) {
            Write-Host "`n   ✅ SUCCESS: Found $($resp.Count) items!" -ForegroundColor Green
            $ready = $true
        } else {
            Write-Host "." -NoNewline
            Start-Sleep -Seconds 2
        }
    } catch {
        Write-Host "." -NoNewline
        Start-Sleep -Seconds 2
    }
    $count++
}

# 5. Start Frontend
Write-Host "5. Launching Frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendDir'; npm run dev -- --port 3000"

Write-Host "`n🚀 SYSTEM IS READY!" -ForegroundColor Green
Write-Host "🌍 Opening browser at http://localhost:3000" -ForegroundColor Cyan
Start-Process "http://localhost:3000"
