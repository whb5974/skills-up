#!/bin/bash
# i 茅台申购辅助工具 - 启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🍶 i 茅台申购辅助工具"
echo "======================"
echo ""

# 检查配置
if [ ! -f config.yaml ]; then
    echo "❌ 配置文件不存在，请复制 config.yaml.example 为 config.yaml"
    exit 1
fi

# 检查数据目录
mkdir -p data/logs data/backup

# 启动服务
echo "🚀 启动服务..."
echo ""

# 使用 nohup 后台运行
nohup python3 main.py start > data/logs/output.log 2>&1 &
PID=$!

echo "✅ 服务已启动 (PID: $PID)"
echo ""
echo "📝 日志文件：data/logs/output.log"
echo "📝 服务日志：data/logs/service.log"
echo ""
echo "🛑 停止服务：kill $PID 或 pkill -f 'python3 main.py'"
echo "📊 查看日志：tail -f data/logs/output.log"
echo ""
