#!/bin/bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RUN_DIR="$SCRIPT_DIR/.run"
LOG_DIR="$SCRIPT_DIR/.run/logs"

mkdir -p "$LOG_DIR"

echo ""
echo "  ╔═══════════════════════════════════════╗"
echo "  ║        🎨 InkIn 入画 - 启动中        ║"
echo "  ╚═══════════════════════════════════════╝"
echo ""

# 检查是否已在运行
if [ -f "$RUN_DIR/backend.pid" ] && kill -0 "$(cat "$RUN_DIR/backend.pid")" 2>/dev/null; then
    echo "⚠️  InkIn 已在运行中！"
    echo "   后端 PID: $(cat "$RUN_DIR/backend.pid")"
    [ -f "$RUN_DIR/frontend.pid" ] && echo "   前端 PID: $(cat "$RUN_DIR/frontend.pid")"
    echo ""
    echo "   如需重启，请先运行 ./stop.sh"
    exit 1
fi

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

# 启动后端（后台常驻）
echo ""
echo "[3/4] 启动后端服务..."
cd "$SCRIPT_DIR/backend"
nohup python3 app.py > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo "$BACKEND_PID" > "$RUN_DIR/backend.pid"
echo "✓ 后端已启动 (PID: $BACKEND_PID)"

# 启动前端（后台常驻）
echo ""
echo "[4/4] 启动前端服务..."
cd "$SCRIPT_DIR/frontend"
nohup pnpm dev > "$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo "$FRONTEND_PID" > "$RUN_DIR/frontend.pid"
echo "✓ 前端已启动 (PID: $FRONTEND_PID)"

# 等待服务就绪
echo ""
echo "等待服务就绪..."
sleep 3

# 检查进程是否存活
if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
    echo "❌ 后端启动失败，请查看日志: $LOG_DIR/backend.log"
    rm -f "$RUN_DIR/backend.pid"
    exit 1
fi
if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
    echo "❌ 前端启动失败，请查看日志: $LOG_DIR/frontend.log"
    rm -f "$RUN_DIR/frontend.pid"
    exit 1
fi

echo ""
echo "  ╔═══════════════════════════════════════╗"
echo "  ║        ✅ InkIn 启动成功！            ║"
echo "  ╠═══════════════════════════════════════╣"
echo "  ║  后端: http://localhost:5000          ║"
echo "  ║  前端: http://localhost:3000          ║"
echo "  ╠═══════════════════════════════════════╣"
echo "  ║  关闭终端不会影响运行                 ║"
echo "  ║  停止服务: ./stop.sh                  ║"
echo "  ╚═══════════════════════════════════════╝"
echo ""

# 尝试打开浏览器
if command -v open &> /dev/null; then
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
fi
