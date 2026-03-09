#!/bin/bash

# Qbot 学习定时任务配置脚本
# 每天早上 9:00 自动执行学习检查

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK_SCRIPT="$SCRIPT_DIR/qbot-daily-check.py"
CRON_LOG="/home/ghost/.openclaw/logs/qbot-learning-cron.log"

echo "🤖 Qbot 学习定时任务配置"
echo "========================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

echo "✅ Python3: $(python3 --version)"

# 检查脚本
if [ ! -f "$CHECK_SCRIPT" ]; then
    echo "❌ 检查脚本不存在：$CHECK_SCRIPT"
    exit 1
fi

echo "✅ 检查脚本：$CHECK_SCRIPT"

# 创建日志目录
mkdir -p "$(dirname "$CRON_LOG")"
echo "✅ 日志目录：$(dirname "$CRON_LOG")"

# 测试运行
echo ""
echo "🧪 测试运行..."
python3 "$CHECK_SCRIPT" > /tmp/qbot-test-run.log 2>&1

if [ $? -eq 0 ]; then
    echo "✅ 测试运行成功"
else
    echo "❌ 测试运行失败"
    cat /tmp/qbot-test-run.log
    exit 1
fi

# 配置 cron
echo ""
echo "⏰ 配置定时任务..."
echo ""

# 检查 crontab
if ! command -v crontab &> /dev/null; then
    echo "❌ crontab 未安装"
    echo "请安装：sudo apt-get install cron"
    exit 1
fi

# 创建 cron 任务
CRON_JOB="0 9 * * * python3 $CHECK_SCRIPT >> $CRON_LOG 2>&1"

# 检查是否已存在
if crontab -l 2>/dev/null | grep -q "$CHECK_SCRIPT"; then
    echo "⚠️  定时任务已存在"
    echo ""
    echo "当前 cron 配置:"
    crontab -l | grep "$CHECK_SCRIPT"
else
    # 添加 cron 任务
    (crontab -l 2>/dev/null | grep -v "$CHECK_SCRIPT"; echo "$CRON_JOB") | crontab -
    echo "✅ 定时任务已添加"
    echo ""
    echo "配置内容:"
    echo "$CRON_JOB"
fi

echo ""
echo "========================"
echo "✅ 配置完成!"
echo ""
echo "📋 定时任务详情:"
echo "   时间：每天早上 9:00"
echo "   脚本：$CHECK_SCRIPT"
echo "   日志：$CRON_LOG"
echo ""
echo "🔍 查看定时任务:"
echo "   crontab -l"
echo ""
echo "📝 查看日志:"
echo "   tail -f $CRON_LOG"
echo ""
echo "🧪 手动测试:"
echo "   python3 $CHECK_SCRIPT"
echo ""
echo "❌ 删除定时任务:"
echo "   crontab -l | grep -v '$CHECK_SCRIPT' | crontab -"
echo ""
