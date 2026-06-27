# InkIn 入画 - PowerShell 启动脚本

Write-Host ""
Write-Host "  ╔═══════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║        🎨 InkIn 入画 - 启动中        ║" -ForegroundColor Cyan
Write-Host "  ╚═══════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
Write-Host "[1/3] 检查 Python 环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到 Python，请先安装 Python 3.8+" -ForegroundColor Red
    Read-Host "按回车退出"
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
    Read-Host "按回车退出"
    exit 1
}

# 启动后端
Write-Host ""
Write-Host "[3/4] 启动后端服务..." -ForegroundColor Yellow
$backendPath = Join-Path $PSScriptRoot "backend"
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; python app.py" -WindowStyle Normal
Write-Host "✓ 后端启动中..." -ForegroundColor Green

# 启动前端
Write-Host ""
Write-Host "[4/4] 启动前端服务..." -ForegroundColor Yellow
$frontendPath = Join-Path $PSScriptRoot "frontend"
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", -Command, "cd '$frontendPath'; pnpm dev" -WindowStyle Normal
Write-Host "✓ 前端启动中..." -ForegroundColor Green

# 等待服务启动
Write-Host ""
Write-Host "  ╔═══════════════════════════════════════╗" -ForegroundColor Green
Write-Host "  ║        ✅ InkIn 启动成功！            ║" -ForegroundColor Green
Write-Host "  ╠═══════════════════════════════════════╣" -ForegroundColor Green
Write-Host "  ║  后端: http://localhost:5000          ║" -ForegroundColor Green
Write-Host "  ║  前端: http://localhost:3000          ║" -ForegroundColor Green
Write-Host "  ╚═══════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# 等待 3 秒后打开浏览器
Start-Sleep -Seconds 3
Start-Process "http://localhost:3000"

Write-Host "按回车关闭此窗口..." -ForegroundColor Gray
Read-Host
