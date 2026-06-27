# InkIn 入画 - PowerShell 停止脚本

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RunDir = Join-Path $ScriptDir ".run"

Write-Host ""
Write-Host "  🛑 InkIn 入画 - 停止服务" -ForegroundColor Yellow
Write-Host ""

$stopped = 0

# 停止后端
$backendPidFile = Join-Path $RunDir "backend.pid"
if (Test-Path $backendPidFile) {
    $pid = Get-Content $backendPidFile
    $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
    if ($proc) {
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        Write-Host "✓ 后端已停止 (PID: $pid)" -ForegroundColor Green
        $stopped++
    } else {
        Write-Host "⚠️  后端进程已不存在 (PID: $pid)" -ForegroundColor Yellow
    }
    Remove-Item $backendPidFile -ErrorAction SilentlyContinue
} else {
    Write-Host "⚠️  未找到后端 PID 文件" -ForegroundColor Yellow
}

# 停止前端
$frontendPidFile = Join-Path $RunDir "frontend.pid"
if (Test-Path $frontendPidFile) {
    $pid = Get-Content $frontendPidFile
    $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
    if ($proc) {
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        Write-Host "✓ 前端已停止 (PID: $pid)" -ForegroundColor Green
        $stopped++
    } else {
        Write-Host "⚠️  前端进程已不存在 (PID: $pid)" -ForegroundColor Yellow
    }
    Remove-Item $frontendPidFile -ErrorAction SilentlyContinue
} else {
    Write-Host "⚠️  未找到前端 PID 文件" -ForegroundColor Yellow
}

if ($stopped -gt 0) {
    Write-Host ""
    Write-Host "✅ InkIn 已停止运行" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "ℹ️  没有正在运行的服务" -ForegroundColor Gray
}
Write-Host ""
