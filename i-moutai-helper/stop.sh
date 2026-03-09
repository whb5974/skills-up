#!/bin/bash
# i 茅台申购辅助工具 - 停止脚本

echo "🛑 停止 i 茅台申购辅助工具..."

# 查找进程
PIDS=$(pgrep -f "python3 main.py start" || true)

if [ -z "$PIDS" ]; then
    echo "⚠️  服务未运行"
    exit 0
fi

# 停止进程
for PID in $PIDS; do
    echo "📌 停止进程 PID: $PID"
    kill $PID 2>/dev/null || true
done

# 等待进程结束
sleep 2

# 检查是否还有进程
REMAINING=$(pgrep -f "python3 main.py start" || true)
if [ -n "$REMAINING" ]; then
    echo "⚠️  强制停止进程..."
    for PID in $REMAINING; do
        kill -9 $PID 2>/dev/null || true
    done
fi

echo "✅ 服务已停止"
