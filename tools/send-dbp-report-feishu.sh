#!/bin/bash
# 等保测评自动化项目日报 - 飞书推送脚本
# 每天上午 10 点执行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_SCRIPT="$SCRIPT_DIR/dbp-daily-report.py"
LOG_FILE="$SCRIPT_DIR/dbp-report.log"

# 生成报告
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始生成等保测评项目日报..." >> "$LOG_FILE"

# 执行 Python 脚本生成报告
REPORT=$(python3 "$REPORT_SCRIPT" 2>&1)

if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 报告生成成功" >> "$LOG_FILE"
    
    # 使用 OpenClaw message 工具发送到飞书群
    # 注意：这里需要通过 OpenClaw 的 message 工具发送
    # 由于 shell 无法直接调用 OpenClaw 工具，我们创建一个标记文件
    echo "$REPORT" > "$SCRIPT_DIR/dbp-report-message.txt"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 报告已保存到 dbp-report-message.txt" >> "$LOG_FILE"
    echo "✅ 等保测评项目日报已生成，等待发送到飞书群"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 报告生成失败：$REPORT" >> "$LOG_FILE"
    echo "❌ 报告生成失败：$REPORT"
    exit 1
fi
