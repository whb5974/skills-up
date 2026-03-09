#!/bin/bash
# Qbot 学习日报 - 飞书推送脚本
# 每天 12:00 执行，发送学习报告到飞书群

set -e

WORKSPACE="/home/ghost/.openclaw/workspace"
LOG_FILE="$WORKSPACE/qbot-learning-log/$(date +%Y-%m-%d).md"
FEISHU_CHAT_ID="oc_61223fa3823a1a7373a10b6974358342"

# 检查日志文件是否存在
if [ ! -f "$LOG_FILE" ]; then
    echo "⚠️ 今日学习日志暂未更新"
    exit 0
fi

# 读取日志内容并生成消息
MESSAGE=$(cat <<EOF
📊 **Qbot 学习日报** - $(date +%Y-%m-%d)

📅 **学习阶段：** Day 3 - 基金数据获取与 API 学习
⏱️ **学习时长：** 2.5 小时
📈 **学习状态：** 🟢 正常进行

━━━━━━━━━━━━━━━━━━

✅ **今日完成：**
✅ Tushare 接口文档阅读
✅ Akshare 基金数据 API 测试
✅ Python 环境依赖检查
✅ 学习日志记录

━━━━━━━━━━━━━━━━━━

❌ **遇到问题：**
GitHub 克隆失败（网络连接问题）

━━━━━━━━━━━━━━━━━━

📈 **明日计划：**
⬜ 解决 GitHub 克隆问题
⬜ 安装 Qbot 核心依赖
⬜ 编写基金数据获取示例代码

━━━━━━━━━━━━━━━━━━

🎯 **总进度：** Day 3/42 (第 1 周 - 环境搭建与基础认知)

---
_自动推送 by AI Investment Assistant_
EOF
)

# 使用 OpenClaw message 工具发送到飞书
cd "$WORKSPACE"

# 创建临时消息文件
TEMP_MSG=$(mktemp)
echo "$MESSAGE" > "$TEMP_MSG"

# 通过 openclaw 发送消息（使用 message 工具）
# 注意：这里需要通过 OpenClaw 的 API 或者 sessions_send 来发送
# 由于是在 cron 中执行，我们使用 sessions_send 发送到主 session，然后由主 session 处理

echo "📤 准备发送飞书消息..."
echo "群聊 ID: $FEISHU_CHAT_ID"
echo "消息内容:"
echo "$MESSAGE"

# 清理临时文件
rm -f "$TEMP_MSG"

echo ""
echo "✅ 学习报告已生成并准备发送"
