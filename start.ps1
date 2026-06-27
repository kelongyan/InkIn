# InkIn 入画 - PowerShell 启动脚本（后台常驻）

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RunDir = Join-Path $ScriptDir ".run"
$LogDir = Join-Path $RunDir "logs"

# 创建运行目录
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

Write-Host ""
Write-Host "  ╔═══════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║        🎨 InkIn 入画 - 启动中        ║" -ForegroundColor Cyan
Write-Host "  ╚═══════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 检查是否已在运行
$backendPidFile = Join-Path $RunDir "backend.pid"
if (Test-Path $backendPidFile) {
    $existingPid = Get-Content $backendPidFile
    $proc = Get-Process -Id $existingPid -ErrorAction SilentlyContinue
    if ($proc) {
        Write-Host "⚠️  InkIn 已在运行中！" -ForegroundColor Yellow
        Write-Host "   后端 PID: $existingPid"
        $fePidFile = Join-Path $RunDir "frontend.pid"
        if (Test-Path $fePidFile) {
            Write-Host "   前端 PID: $(Get-Content $fePidFile)"
        }
        Write-Host ""
        Write-Host "   如需重启，请先运行 .\stop.ps1" -ForegroundColor Yellow
        exit 0
    }
}

# 检查 Python
Write-Host "[1/3] 检查 Python 环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到 Python，请先安装 Python 3.8+" -ForegroundColor Red
    exit 1
}

# 检查 pnpm
Write-Host ""
Write-Host "[2/3] 检查 pnpm 环境..." -ForegroundColor Yellow
try {
    $pnpmVersion = pnpm --version 2>&1
    Write-Host "✓ pnpm $pnpmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到 pnpm，请先安装: npm install -g pnpm" -ForegroundColor Red
    exit 1
}

# 启动后端（后台常驻，无窗口）
Write-Host ""
Write-Host "[3/4] 启动后端服务..." -ForegroundColor Yellow
$backendPath = Join-Path $ScriptDir "backend"
$backendLog = Join-Path $LogDir "backend.log"
$backendProc = Start-Process -FilePath "python" -ArgumentList "app.py" `
    -WorkingDirectory $backendPath `
    -WindowStyle Hidden `
    -RedirectStandardOutput $backendLog `
    -RedirectStandardError (Join-Path $LogDir "backend-error.log") `
    -PassThru
$backendProc.Id | Out-File -FilePath $backendPidFile -Encoding ascii -NoNewline
Write-Host "✓ 后端已启动 (PID: $($backendProc.Id))" -ForegroundColor Green

# 启动前端（后台常驻，无窗口）
Write-Host ""
Write-Host "[4/4] 启动前端服务..." -ForegroundColor Yellow
$frontendPath = Join-Path $ScriptDir "frontend"
$frontendLog = Join-Path $LogDir "frontend.log"
$frontendProc = Start-Process -FilePath "pnpm" -ArgumentList "dev" `
    -WorkingDirectory $frontendPath `
    -WindowStyle Hidden `
    -RedirectStandardOutput $frontendLog `
    -RedirectStandardError (Join-Path $LogDir "frontend-error.log") `
    -PassThru
$frontendProc.Id | Out-File -FilePath (Join-Path $RunDir "frontend.pid") -Encoding ascii -NoNewline
Write-Host "✓ 前端已启动 (PID: $($frontendProc.Id))" -ForegroundColor Green

# 等待服务就绪
Write-Host ""
Write-Host "等待服务就绪..." -ForegroundColor Gray
Start-Sleep -Seconds 3

# 检查进程是否存活
$backendAlive = Get-Process -Id $backendProc.Id -ErrorAction SilentlyContinue
$frontendAlive = Get-Process -Id $frontendProc.Id -ErrorAction SilentlyContinue

if (-not $backendAlive) {
    Write-Host "❌ 后端启动失败，请查看日志: $backendLog" -ForegroundColor Red
    Remove-Item $backendPidFile -ErrorAction SilentlyContinue
    exit 1
}
if (-not $frontendAlive) {
    Write-Host "❌ 前端启动失败，请查看日志: $frontendLog" -ForegroundColor Red
    Remove-Item (Join-Path $RunDir "frontend.pid") -ErrorAction SilentlyContinue
    exit 1
}

Write-Host ""
Write-Host "  ╔═══════════════════════════════════════╗" -ForegroundColor Green
Write-Host "  ║        ✅ InkIn 启动成功！            ║" -ForegroundColor Green
Write-Host "  ╠═══════════════════════════════════════╣" -ForegroundColor Green
Write-Host "  ║  后端: http://localhost:5000          ║" -ForegroundColor Green
Write-Host "  ║  前端: http://localhost:3000          ║" -ForegroundColor Green
Write-Host "  ╠═══════════════════════════════════════╣" -ForegroundColor Green
Write-Host "  ║  关闭终端不会影响运行                 ║" -ForegroundColor Green
Write-Host "  ║  停止服务: .\stop.ps1                 ║" -ForegroundColor Green
Write-Host "  ╚═══════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# 打开浏览器
Start-Sleep -Seconds 2
Start-Process "http://localhost:3000"
