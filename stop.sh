#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RUN_DIR="$SCRIPT_DIR/.run"

echo ""
echo "  🛑 InkIn 入画 - 停止服务"
echo ""

STOPPED=0

# 停止后端
if [ -f "$RUN_DIR/backend.pid" ]; then
    PID=$(cat "$RUN_DIR/backend.pid")
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID" 2>/dev/null
        echo "✓ 后端已停止 (PID: $PID)"
        STOPPED=1
    else
        echo "⚠️  后端进程已不存在 (PID: $PID)"
    fi
    rm -f "$RUN_DIR/backend.pid"
else
    echo "⚠️  未找到后端 PID 文件"
fi

# 停止前端
if [ -f "$RUN_DIR/frontend.pid" ]; then
    PID=$(cat "$RUN_DIR/frontend.pid")
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID" 2>/dev/null
        echo "✓ 前端已停止 (PID: $PID)"
        STOPPED=1
    else
        echo "⚠️  前端进程已不存在 (PID: $PID)"
    fi
    rm -f "$RUN_DIR/frontend.pid"
else
    echo "⚠️  未找到前端 PID 文件"
fi

if [ "$STOPPED" -eq 1 ]; then
    echo ""
    echo "✅ InkIn 已停止运行"
else
    echo ""
    echo "ℹ️  没有正在运行的服务"
fi
echo ""
