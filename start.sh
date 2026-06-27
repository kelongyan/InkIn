#!/bin/bash

# InkIn 入画 - Linux/Mac 启动脚本

echo ""
echo "  ╔═══════════════════════════════════════╗"
echo "  ║        🎨 InkIn 入画 - 启动中        ║"
echo "  ╚═══════════════════════════════════════╝"
echo ""

# 检查 Python
echo "[1/3] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi
echo "✓ $(python3 --version)"

# 检查 pnpm
echo ""
echo "[2/3] 检查 pnpm 环境..."
if ! command -v pnpm &> /dev/null; then
    echo "❌ 未找到 pnpm，请先安装: npm install -g pnpm"
    exit 1
fi
echo "✓ pnpm $(pnpm --version)"

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 启动后端
echo ""
echo "[3/4] 启动后端服务..."
cd "$SCRIPT_DIR/backend"
python3 app.py &
BACKEND_PID=$!
echo "✓ 后端启动中 (PID: $BACKEND_PID)"

# 启动前端
echo ""
echo "[4/4] 启动前端服务..."
cd "$SCRIPT_DIR/frontend"
pnpm dev &
FRONTEND_PID=$!
echo "✓ 前端启动中 (PID: $FRONTEND_PID)"

# 等待服务启动
sleep 2

echo ""
echo "  ╔═══════════════════════════════════════╗"
echo "  ║        ✅ InkIn 启动成功！            ║"
echo "  ╠═══════════════════════════════════════╣"
echo "  ║  后端: http://localhost:5000          ║"
echo "  ║  前端: http://localhost:3000          ║"
echo "  ╚═══════════════════════════════════════╝"
echo ""

# 尝试打开浏览器
if command -v open &> /dev/null; then
    # macOS
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open http://localhost:3000
fi

# 等待 Ctrl+C
echo "按 Ctrl+C 停止所有服务..."
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo ''; echo '服务已停止'; exit 0" INT TERM
wait
